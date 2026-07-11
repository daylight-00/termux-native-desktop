#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import os
import shutil
import stat
import subprocess
import sys
import time
import traceback
from pathlib import Path, PurePosixPath

B8_OUT = Path(os.environ["B8_OUT"])
OUT = Path(
    os.environ.get(
        "OUT",
        "/tmp/selected-obsidian-phase-b9-staging-generation-materialization",
    )
)
REPO = Path(
    subprocess.check_output(
        [
            "git",
            "-C",
            str(Path(__file__).resolve().parent),
            "rev-parse",
            "--show-toplevel",
        ],
        text=True,
    ).strip()
)

OUT.mkdir(parents=True, exist_ok=True)
(OUT / "input").mkdir(exist_ok=True)
stage = "initialization"
staging_generation: Path | None = None
schema_build_root: Path | None = None


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(
    path: Path,
    fieldnames: list[str],
    rows: list[dict[str, object]],
) -> None:
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def summary_map(path: Path) -> dict[str, str]:
    return {row["field"]: row["value"] for row in read_tsv(path)}


def write_status(value: str) -> None:
    (OUT / "analysis.status").write_text(value + "\n")


def fail(stage_name: str, message: str, rc: int = 1) -> None:
    write_status("FAIL")
    (OUT / "failure-stage.txt").write_text(stage_name + "\n")
    print(message, file=sys.stderr)
    print(f"evidence: {OUT}", file=sys.stderr)
    raise SystemExit(rc)


def fsync_file(path: Path) -> None:
    descriptor = os.open(path, os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def fsync_dir(path: Path) -> None:
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def sync_tree(root: Path) -> None:
    files: list[Path] = []
    directories: list[Path] = [root]
    for path in root.rglob("*"):
        if path.is_symlink():
            continue
        if path.is_file():
            files.append(path)
        elif path.is_dir():
            directories.append(path)
    for path in files:
        fsync_file(path)
    for path in sorted(directories, key=lambda item: len(item.parts), reverse=True):
        fsync_dir(path)


def ensure_plain_dir(path: Path, mode: int = 0o700) -> None:
    if path.is_symlink():
        fail("filesystem_preflight", f"directory path is a symlink: {path}")
    if path.exists():
        if not path.is_dir():
            fail("filesystem_preflight", f"path is not a directory: {path}")
        return
    parent = path.parent
    path.mkdir(parents=True, mode=mode, exist_ok=False)
    existing_parent = parent
    while not existing_parent.exists() and existing_parent != existing_parent.parent:
        existing_parent = existing_parent.parent
    if parent.exists() and parent.is_dir():
        fsync_dir(parent)


def lexical_resolve(base: Path, relative: str) -> Path:
    return Path(os.path.normpath(str(base / relative)))


def path_is_within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def current_state(path: Path) -> dict[str, object]:
    if not path.exists() and not path.is_symlink():
        return {
            "state": "ABSENT",
            "path": str(path),
            "link_target": "-",
            "resolved_target": "-",
            "inode": "-",
        }
    metadata = path.lstat()
    if stat.S_ISLNK(metadata.st_mode):
        target = os.readlink(path)
        return {
            "state": "SYMLINK",
            "path": str(path),
            "link_target": target,
            "resolved_target": str(lexical_resolve(path.parent, target)),
            "inode": metadata.st_ino,
        }
    return {
        "state": "NON_SYMLINK",
        "path": str(path),
        "link_target": "-",
        "resolved_target": str(path.resolve()),
        "inode": metadata.st_ino,
    }


def remove_tree(path: Path) -> None:
    if not path.exists() and not path.is_symlink():
        return
    if path.is_symlink() or path.is_file():
        path.unlink()
        return
    try:
        path.chmod(0o700)
    except OSError:
        pass
    for entry in list(path.iterdir()):
        if entry.is_symlink() or entry.is_file():
            entry.unlink()
        else:
            remove_tree(entry)
    path.rmdir()


def copy_readonly(source: Path, destination: Path) -> str:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with source.open("rb") as src, destination.open("xb") as dst:
        shutil.copyfileobj(src, dst, 1024 * 1024)
        dst.flush()
        os.fsync(dst.fileno())
    destination.chmod(0o444)
    return sha256(destination)


def install_content_object(
    source: Path,
    expected_sha: str,
    target: Path,
) -> tuple[str, int]:
    if target.is_symlink():
        fail("content_materialization", f"object target is a symlink: {target}")

    parent_existed = target.parent.exists()
    target.parent.mkdir(parents=True, exist_ok=True)
    if not parent_existed:
        fsync_dir(target.parent.parent)

    if target.exists():
        if not target.is_file() or target.is_symlink():
            fail("content_materialization", f"object target is invalid: {target}")
        if sha256(target) != expected_sha:
            fail("content_materialization", f"existing object hash mismatch: {target}")
        target.chmod(0o444)
        fsync_file(target)
        return "REUSED", target.stat().st_size

    temporary = target.parent / f".{target.name}.tmp-{os.getpid()}-{time.time_ns()}"
    try:
        with source.open("rb") as src, temporary.open("xb") as dst:
            shutil.copyfileobj(src, dst, 1024 * 1024)
            dst.flush()
            os.fsync(dst.fileno())
        if sha256(temporary) != expected_sha:
            fail("content_materialization", f"temporary object hash mismatch: {source}")
        temporary.chmod(0o444)
        fsync_file(temporary)
        try:
            os.link(temporary, target)
            disposition = "CREATED"
        except FileExistsError:
            if target.is_symlink() or not target.is_file():
                fail("content_materialization", f"raced object target is invalid: {target}")
            if sha256(target) != expected_sha:
                fail("content_materialization", f"raced object hash mismatch: {target}")
            disposition = "REUSED_AFTER_RACE"
        fsync_dir(target.parent)
        return disposition, target.stat().st_size
    finally:
        if temporary.exists():
            temporary.unlink()


def freeze_generation(root: Path) -> None:
    files: list[Path] = []
    directories: list[Path] = []
    for path in root.rglob("*"):
        if path.is_symlink():
            continue
        if path.is_file():
            files.append(path)
        elif path.is_dir():
            directories.append(path)
    for path in files:
        path.chmod(0o444)
    for path in sorted(directories, key=lambda item: len(item.parts), reverse=True):
        path.chmod(0o555)
    root.chmod(0o555)


def validate_generation(
    root: Path,
    generation_base: Path,
    object_plan: list[dict[str, str]],
    alias_plan: list[dict[str, str]],
    manifest_expectations: dict[str, str],
    *,
    require_immutable: bool,
) -> list[dict[str, object]]:
    checks: list[dict[str, object]] = []

    def add(check: str, passed: bool, detail: str) -> None:
        checks.append(
            {
                "check": check,
                "state": "PASS" if passed else "FAIL",
                "detail": detail,
            }
        )
        if not passed:
            fail("generation_validation", f"{check}: {detail}")

    add("generation_root_plain_directory", root.is_dir() and not root.is_symlink(), str(root))

    expected_aliases = {row["alias_relpath"] for row in alias_plan}
    observed_aliases = {
        str(path.relative_to(root))
        for path in root.rglob("*")
        if path.is_symlink()
    }
    add(
        "alias_path_set",
        observed_aliases == expected_aliases,
        f"expected={len(expected_aliases)} observed={len(observed_aliases)}",
    )

    for row in alias_plan:
        alias = root / row["alias_relpath"]
        add("alias_is_symlink", alias.is_symlink(), row["alias_relpath"])
        observed_target = os.readlink(alias)
        add(
            "alias_target_text",
            observed_target == row["relative_symlink_target"],
            row["alias_relpath"],
        )
        expected_object = generation_base / row["object_relpath"]
        add(
            "alias_resolves_to_object",
            lexical_resolve(alias.parent, observed_target) == expected_object,
            row["alias_relpath"],
        )
        add(
            "alias_object_hash",
            expected_object.is_file()
            and not expected_object.is_symlink()
            and sha256(expected_object) == row["sha256"],
            row["alias_relpath"],
        )

    for row in object_plan:
        target = generation_base / row["object_relpath"]
        add(
            "object_hash",
            target.is_file()
            and not target.is_symlink()
            and sha256(target) == row["sha256"],
            row["object_relpath"],
        )
        add(
            "object_not_owner_writable",
            not bool(target.stat().st_mode & stat.S_IWUSR),
            row["object_relpath"],
        )

    for relative, expected_hash in sorted(manifest_expectations.items()):
        target = root / relative
        add(
            "manifest_hash",
            target.is_file()
            and not target.is_symlink()
            and sha256(target) == expected_hash,
            relative,
        )

    if require_immutable:
        for path in [root, *root.rglob("*")]:
            if path.is_symlink():
                continue
            add(
                "generation_node_not_owner_writable",
                not bool(path.stat().st_mode & stat.S_IWUSR),
                str(path.relative_to(root)) if path != root else ".",
            )

    return checks


try:
    stage = "repository_state"
    dirty = subprocess.check_output(
        [
            "git",
            "-C",
            str(REPO),
            "status",
            "--porcelain",
            "--untracked-files=no",
        ],
        text=True,
    ).strip()
    if dirty:
        fail(stage, "tracked working-tree changes detected; Phase B9 requires exact HEAD", 2)

    branch = subprocess.check_output(
        ["git", "-C", str(REPO), "branch", "--show-current"],
        text=True,
    ).strip()
    head = subprocess.check_output(
        ["git", "-C", str(REPO), "rev-parse", "HEAD"],
        text=True,
    ).strip()

    (OUT / "repository-root.txt").write_text(str(REPO) + "\n")
    (OUT / "branch.txt").write_text(branch + "\n")
    (OUT / "head.txt").write_text(head + "\n")
    (OUT / "phase-b8-root.txt").write_text(str(B8_OUT) + "\n")

    required = [
        "analysis.status",
        "next-state.txt",
        "summary.tsv",
        "source-identity-verification.tsv",
        "content-object-plan.tsv",
        "generation-alias-plan.tsv",
        "alias-collisions.tsv",
        "generation-layout.tsv",
        "activation-contract.txt",
        "rollback-contract.txt",
        "launcher-selection-contract.txt",
        "claim-boundary.txt",
        "input/semantic-object-disposition.tsv",
        "input/candidate-elf-manifest.tsv",
        "input/candidate-data-manifest.tsv",
        "input/capability-membership.tsv",
        "input/reference-runtime-owned-manifest.tsv",
        "input/schema-source-manifest.tsv",
        "input/schema-build-contract.tsv",
    ]

    stage = "input_verification"
    verification_rows: list[dict[str, object]] = []
    missing: list[str] = []
    for name in required:
        source = B8_OUT / name
        embedded = OUT / "input" / name.replace("/", "__")
        state_value = "PASS" if source.is_file() else "FAIL"
        verification_rows.append(
            {
                "file": name,
                "state": state_value,
                "path": str(source),
                "embedded_path": str(embedded) if state_value == "PASS" else "-",
            }
        )
        if state_value == "PASS":
            shutil.copy2(source, embedded)
        else:
            missing.append(name)
    write_tsv(
        OUT / "input-verification.tsv",
        ["file", "state", "path", "embedded_path"],
        verification_rows,
    )
    if missing:
        fail(stage, "missing Phase B8 inputs: " + ", ".join(missing))

    if (B8_OUT / "analysis.status").read_text().strip() != "PASS":
        fail("phase_b8_status", "Phase B8 status is not PASS")
    if (
        B8_OUT / "next-state.txt"
    ).read_text().strip() != "READY_FOR_STAGING_MATERIALIZER_IMPLEMENTATION":
        fail("phase_b8_status", "Phase B8 is not ready for materialization")

    b8_summary = summary_map(B8_OUT / "summary.tsv")
    required_summary = {
        "source_identity_failures": "0",
        "content_plan_rows": "96",
        "unique_content_hashes": "96",
        "duplicate_content_hashes": "0",
        "total_generation_aliases": "175",
        "generation_alias_collisions": "0",
        "candidate_bytes_materialized": "NO",
        "promoted_runtime_mutated": "NO",
    }
    for key, expected in required_summary.items():
        if b8_summary.get(key) != expected:
            fail("phase_b8_summary", f"unexpected B8 summary {key}")

    layout = summary_map(B8_OUT / "generation-layout.tsv")
    generation_base = Path(layout["generation_base"])
    object_store_root = Path(layout["object_store_root"])
    staging_root = Path(layout["staging_root"])
    generations_root = Path(layout["generations_root"])
    generation_id = layout["generation_id"]
    final_generation = Path(layout["generation_dir"])
    current_link = Path(layout["current_link"])

    configured_base = os.environ.get("GENERATION_BASE")
    if configured_base and Path(configured_base) != generation_base:
        fail("filesystem_preflight", "GENERATION_BASE differs from Phase B8")
    if final_generation.parent != generations_root:
        fail("filesystem_preflight", "generation directory is outside generations root")
    for path in (object_store_root, staging_root, generations_root, final_generation):
        if not path_is_within(path, generation_base):
            fail("filesystem_preflight", f"planned path escapes generation base: {path}")

    current_before = current_state(current_link)
    write_tsv(
        OUT / "current-state-before.tsv",
        ["state", "path", "link_target", "resolved_target", "inode"],
        [current_before],
    )
    if current_before["state"] == "NON_SYMLINK":
        fail("filesystem_preflight", f"current is not a symlink: {current_link}")

    ensure_plain_dir(generation_base)
    ensure_plain_dir(object_store_root)
    ensure_plain_dir(staging_root)
    ensure_plain_dir(generations_root)
    if len(
        {
            generation_base.stat().st_dev,
            object_store_root.stat().st_dev,
            staging_root.stat().st_dev,
            generations_root.stat().st_dev,
        }
    ) != 1:
        fail("filesystem_preflight", "generation roots are not on one filesystem")

    stage = "source_identity_recheck"
    source_rows = read_tsv(B8_OUT / "source-identity-verification.tsv")
    source_recheck: list[dict[str, object]] = []
    source_failures = 0
    for row in source_rows:
        source = Path(row["source_path"])
        exists = source.is_file() and not source.is_symlink()
        observed = sha256(source) if exists else "MISSING"
        state_value = (
            "MATCH"
            if exists and observed == row["expected_sha256"]
            else "MISSING"
            if not exists
            else "HASH_MISMATCH"
        )
        source_failures += int(state_value != "MATCH")
        source_recheck.append(
            {
                "kind": row["kind"],
                "source_path": row["source_path"],
                "expected_sha256": row["expected_sha256"],
                "observed_sha256": observed,
                "state": state_value,
            }
        )
    write_tsv(
        OUT / "source-identity-recheck.tsv",
        ["kind", "source_path", "expected_sha256", "observed_sha256", "state"],
        source_recheck,
    )
    if source_failures:
        fail(stage, f"source identity changed since Phase B8: {source_failures}")

    object_plan = read_tsv(B8_OUT / "content-object-plan.tsv")
    alias_plan = read_tsv(B8_OUT / "generation-alias-plan.tsv")
    schema_sources = read_tsv(B8_OUT / "input/schema-source-manifest.tsv")
    schema_contract_rows = read_tsv(B8_OUT / "input/schema-build-contract.tsv")
    if len(object_plan) != 96 or len(alias_plan) != 175:
        fail("manifest_shape", "unexpected object or alias plan size")
    if len(schema_sources) != 37 or len(schema_contract_rows) != 1:
        fail("manifest_shape", "unexpected schema source/build-contract size")
    schema_contract = schema_contract_rows[0]

    transaction_id = f"{generation_id}.stage-{os.getpid()}-{time.time_ns()}"
    staging_generation = staging_root / transaction_id
    schema_build_root = staging_root / f"{transaction_id}.schema-build"
    staging_generation.mkdir(mode=0o700)
    schema_dir = schema_build_root / "schemas"
    schema_dir.mkdir(parents=True, mode=0o700)
    fsync_dir(staging_root)

    stage = "schema_generation"
    for row in schema_sources:
        copy_readonly(Path(row["source_path"]), schema_dir / Path(row["source_path"]).name)
    compiler = Path(schema_contract["compiler_path"])
    completed = subprocess.run(
        [str(compiler), "--strict", str(schema_dir)],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=120,
        check=False,
    )
    generated_schema = schema_dir / "gschemas.compiled"
    generated_sha = sha256(generated_schema) if generated_schema.is_file() else "MISSING"
    write_tsv(
        OUT / "schema-generation.tsv",
        [
            "compiler",
            "compiler_sha256",
            "mode",
            "return_code",
            "stdout_empty",
            "stderr_empty",
            "generated_present",
            "generated_sha256",
            "expected_sha256",
        ],
        [
            {
                "compiler": str(compiler),
                "compiler_sha256": sha256(compiler),
                "mode": "strict",
                "return_code": completed.returncode,
                "stdout_empty": "YES" if not completed.stdout else "NO",
                "stderr_empty": "YES" if not completed.stderr else "NO",
                "generated_present": "YES" if generated_schema.is_file() else "NO",
                "generated_sha256": generated_sha,
                "expected_sha256": schema_contract["aggregate_expected_sha256"],
            }
        ],
    )
    (OUT / "schema-generation.stdout.txt").write_text(completed.stdout)
    (OUT / "schema-generation.stderr.txt").write_text(completed.stderr)
    if (
        completed.returncode != 0
        or completed.stdout
        or completed.stderr
        or generated_sha != schema_contract["aggregate_expected_sha256"]
    ):
        fail(stage, "schema generation did not reproduce the accepted aggregate")

    stage = "content_materialization"
    source_by_sha = {
        row["sha256"]: (
            generated_schema
            if row["content_kind"] == "GENERATED_GSETTINGS"
            else Path(row["source_path"])
        )
        for row in object_plan
    }
    materialization_rows: list[dict[str, object]] = []
    for row in object_plan:
        target = generation_base / row["object_relpath"]
        if not path_is_within(target, object_store_root):
            fail("content_materialization", f"object path escapes store: {target}")
        disposition, size = install_content_object(
            source_by_sha[row["sha256"]],
            row["sha256"],
            target,
        )
        materialization_rows.append(
            {
                "content_kind": row["content_kind"],
                "sha256": row["sha256"],
                "source_path": row["source_path"],
                "object_path": str(target),
                "disposition": disposition,
                "size_bytes": size,
            }
        )
    write_tsv(
        OUT / "object-materialization.tsv",
        [
            "content_kind",
            "sha256",
            "source_path",
            "object_path",
            "disposition",
            "size_bytes",
        ],
        materialization_rows,
    )

    stage = "generation_construction"
    for row in alias_plan:
        relative = PurePosixPath(row["alias_relpath"])
        if relative.is_absolute() or ".." in relative.parts:
            fail("generation_construction", f"unsafe alias path: {relative}")
        if os.path.isabs(row["relative_symlink_target"]):
            fail("generation_construction", f"absolute alias target: {relative}")
        alias = staging_generation / Path(*relative.parts)
        alias.parent.mkdir(parents=True, exist_ok=True)
        expected_object = generation_base / row["object_relpath"]
        if lexical_resolve(alias.parent, row["relative_symlink_target"]) != expected_object:
            fail("generation_construction", f"alias target mismatch: {relative}")
        alias.symlink_to(row["relative_symlink_target"])

    manifest_sources = {
        "manifests/semantic-object-disposition.tsv": B8_OUT / "input/semantic-object-disposition.tsv",
        "manifests/candidate-elf-manifest.tsv": B8_OUT / "input/candidate-elf-manifest.tsv",
        "manifests/candidate-data-manifest.tsv": B8_OUT / "input/candidate-data-manifest.tsv",
        "manifests/capability-membership.tsv": B8_OUT / "input/capability-membership.tsv",
        "manifests/reference-runtime-owned-manifest.tsv": B8_OUT / "input/reference-runtime-owned-manifest.tsv",
        "manifests/schema-source-manifest.tsv": B8_OUT / "input/schema-source-manifest.tsv",
        "manifests/schema-build-contract.tsv": B8_OUT / "input/schema-build-contract.tsv",
        "manifests/content-object-plan.tsv": B8_OUT / "content-object-plan.tsv",
        "manifests/generation-alias-plan.tsv": B8_OUT / "generation-alias-plan.tsv",
        "manifests/generation-layout.tsv": B8_OUT / "generation-layout.tsv",
        "receipts/phase-b8-summary.tsv": B8_OUT / "summary.tsv",
        "receipts/phase-b8-analysis.status": B8_OUT / "analysis.status",
        "receipts/phase-b8-next-state.txt": B8_OUT / "next-state.txt",
        "receipts/activation-contract.txt": B8_OUT / "activation-contract.txt",
        "receipts/rollback-contract.txt": B8_OUT / "rollback-contract.txt",
        "receipts/launcher-selection-contract.txt": B8_OUT / "launcher-selection-contract.txt",
        "receipts/phase-b8-claim-boundary.txt": B8_OUT / "claim-boundary.txt",
    }
    manifest_expectations: dict[str, str] = {}
    for relative, source in manifest_sources.items():
        destination = staging_generation / relative
        copied_sha = copy_readonly(source, destination)
        expected_sha = sha256(source)
        if copied_sha != expected_sha:
            fail("generation_construction", f"manifest copy mismatch: {relative}")
        manifest_expectations[relative] = expected_sha

    generation_metadata = staging_generation / "receipts/generation-metadata.tsv"
    write_tsv(
        generation_metadata,
        ["field", "value"],
        [
            {"field": "generation_id", "value": generation_id},
            {"field": "generation_digest", "value": layout["generation_digest"]},
            {"field": "phase_b8_head", "value": b8_summary.get("head", "")},
            {"field": "content_objects", "value": len(object_plan)},
            {"field": "generation_aliases", "value": len(alias_plan)},
            {"field": "activation_state", "value": "NOT_ACTIVATED"},
        ],
    )
    generation_metadata.chmod(0o444)
    manifest_expectations["receipts/generation-metadata.tsv"] = sha256(generation_metadata)

    validation_rows = validate_generation(
        staging_generation,
        generation_base,
        object_plan,
        alias_plan,
        manifest_expectations,
        require_immutable=False,
    )
    sync_tree(staging_generation)

    stage = "generation_publication"
    if final_generation.exists() or final_generation.is_symlink():
        if final_generation.is_symlink() or not final_generation.is_dir():
            fail("generation_publication", f"invalid final generation: {final_generation}")
        validation_rows.extend(
            validate_generation(
                final_generation,
                generation_base,
                object_plan,
                alias_plan,
                manifest_expectations,
                require_immutable=True,
            )
        )
        remove_tree(staging_generation)
        staging_generation = None
        fsync_dir(staging_root)
        publication_state = "REUSED_EXISTING_VALID_GENERATION"
    else:
        freeze_generation(staging_generation)
        sync_tree(staging_generation)
        os.rename(staging_generation, final_generation)
        staging_generation = None
        fsync_dir(staging_root)
        fsync_dir(generations_root)
        publication_state = "PUBLISHED_NEW_GENERATION"
        validation_rows.extend(
            validate_generation(
                final_generation,
                generation_base,
                object_plan,
                alias_plan,
                manifest_expectations,
                require_immutable=True,
            )
        )

    write_tsv(
        OUT / "generation-validation.tsv",
        ["check", "state", "detail"],
        validation_rows,
    )

    current_after = current_state(current_link)
    write_tsv(
        OUT / "current-state-after.tsv",
        ["state", "path", "link_target", "resolved_target", "inode"],
        [current_after],
    )
    if current_after != current_before:
        fail("current_pointer_guard", "current pointer changed during Phase B9")

    created = sum(row["disposition"] == "CREATED" for row in materialization_rows)
    reused = len(materialization_rows) - created
    summary_rows = [
        {"field": "branch", "value": branch},
        {"field": "head", "value": head},
        {"field": "phase_b8_root", "value": str(B8_OUT)},
        {"field": "phase_b8_head", "value": b8_summary.get("head", "")},
        {"field": "generation_id", "value": generation_id},
        {"field": "generation_dir", "value": str(final_generation)},
        {"field": "publication_state", "value": publication_state},
        {"field": "source_identity_checks", "value": len(source_recheck)},
        {"field": "source_identity_failures", "value": source_failures},
        {"field": "content_objects", "value": len(object_plan)},
        {"field": "content_objects_created", "value": created},
        {"field": "content_objects_reused", "value": reused},
        {
            "field": "content_bytes",
            "value": sum(int(row["size_bytes"]) for row in materialization_rows),
        },
        {"field": "generation_aliases", "value": len(alias_plan)},
        {"field": "generation_validation_failures", "value": 0},
        {"field": "schema_generated_cleanly", "value": "YES"},
        {"field": "schema_byte_identical", "value": "YES"},
        {"field": "current_state_before", "value": current_before["state"]},
        {"field": "current_state_after", "value": current_after["state"]},
        {"field": "current_pointer_changed", "value": "NO"},
        {"field": "runtime_launch_performed", "value": "NO"},
        {"field": "candidate_bytes_materialized", "value": "YES"},
        {"field": "promoted_runtime_mutated", "value": "NO"},
    ]
    write_tsv(OUT / "summary.tsv", ["field", "value"], summary_rows)

    (OUT / "claim-boundary.txt").write_text(
        "This stage materializes hash-addressed candidate content and publishes one immutable generation.\n"
        "It rebuilds and verifies the selected GSettings aggregate and validates aliases, manifests, permissions, and current-pointer non-mutation.\n"
        "It does not launch Obsidian, change current, modify the promoted launcher, or establish runtime equivalence.\n"
        "The generation must be validated through its explicit path before any activation transaction.\n"
    )
    (OUT / "next-state.txt").write_text("READY_FOR_EXPLICIT_GENERATION_VALIDATION\n")
    write_status("PASS")
    if (OUT / "failure-stage.txt").exists():
        (OUT / "failure-stage.txt").unlink()

    print("selected Obsidian Phase B9 staging generation materialization: PASS")
    print(f"evidence: {OUT}")
    print("\n===== summary =====")
    for row in summary_rows:
        print(f"{row['field']}\t{row['value']}")

except SystemExit:
    if staging_generation is not None:
        try:
            remove_tree(staging_generation)
        except Exception:
            pass
    if schema_build_root is not None:
        try:
            remove_tree(schema_build_root)
        except Exception:
            pass
    raise
except Exception:
    write_status("FAIL")
    (OUT / "failure-stage.txt").write_text(stage + "\n")
    traceback.print_exc()
    print(f"evidence: {OUT}", file=sys.stderr)
    if staging_generation is not None:
        try:
            remove_tree(staging_generation)
        except Exception:
            pass
    if schema_build_root is not None:
        try:
            remove_tree(schema_build_root)
        except Exception:
            pass
    raise SystemExit(1)
finally:
    if schema_build_root is not None:
        try:
            remove_tree(schema_build_root)
        except Exception:
            pass
