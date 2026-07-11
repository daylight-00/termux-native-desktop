#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import json
import os
import shutil
import subprocess
import sys
import traceback
from collections import Counter, defaultdict
from pathlib import Path, PurePosixPath

B7_OUT = Path(os.environ["B7_OUT"])
OUT = Path(
    os.environ.get(
        "OUT",
        "/tmp/selected-obsidian-phase-b8-generation-layout-preflight",
    )
)
HOME = Path(os.environ.get("HOME", "/data/data/com.termux/files/home"))
GENERATION_BASE = Path(
    os.environ.get(
        "GENERATION_BASE",
        str(HOME / "gl/selected/obsidian"),
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


def write_status(value: str) -> None:
    (OUT / "analysis.status").write_text(value + "\n")


def fail(stage_name: str, message: str, rc: int = 1) -> None:
    write_status("FAIL")
    (OUT / "failure-stage.txt").write_text(stage_name + "\n")
    print(message, file=sys.stderr)
    print(f"evidence: {OUT}", file=sys.stderr)
    raise SystemExit(rc)


def safe_alias(value: str) -> bool:
    if not value or value in {"-", ".", "..", "NONE", "UNKNOWN"}:
        return False
    path = PurePosixPath(value)
    return len(path.parts) == 1 and "/" not in value and "\x00" not in value


def object_relpath(digest: str) -> Path:
    return Path("objects/sha256") / digest[:2] / digest


def nearest_existing(path: Path) -> Path:
    current = path
    while not current.exists() and current != current.parent:
        current = current.parent
    return current


def canonical_digest(rows: list[dict[str, object]]) -> str:
    payload = json.dumps(
        rows,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode()
    return hashlib.sha256(payload).hexdigest()


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
        fail(
            stage,
            "tracked working-tree changes detected; Phase B8 requires exact HEAD",
            2,
        )

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
    (OUT / "phase-b7-root.txt").write_text(str(B7_OUT) + "\n")

    required = [
        "analysis.status",
        "next-state.txt",
        "summary.tsv",
        "semantic-object-disposition.tsv",
        "candidate-elf-manifest.tsv",
        "candidate-data-manifest.tsv",
        "capability-membership.tsv",
        "reference-runtime-owned-manifest.tsv",
        "schema-source-manifest.tsv",
        "schema-build-contract.tsv",
        "claim-boundary.txt",
    ]

    stage = "input_verification"
    input_rows: list[dict[str, object]] = []
    missing: list[str] = []
    for name in required:
        source = B7_OUT / name
        embedded = OUT / "input" / name
        state = "PASS" if source.is_file() else "FAIL"
        input_rows.append(
            {
                "file": name,
                "state": state,
                "path": str(source),
                "embedded_path": str(embedded) if state == "PASS" else "-",
            }
        )
        if state == "PASS":
            shutil.copy2(source, embedded)
        else:
            missing.append(name)
    write_tsv(
        OUT / "input-verification.tsv",
        ["file", "state", "path", "embedded_path"],
        input_rows,
    )
    if missing:
        fail(stage, "missing Phase B7 inputs: " + ", ".join(missing))

    if (B7_OUT / "analysis.status").read_text().strip() != "PASS":
        fail("phase_b7_status", "Phase B7 status is not PASS")
    if (
        B7_OUT / "next-state.txt"
    ).read_text().strip() != "READY_FOR_CANDIDATE_MATERIALIZATION_DESIGN":
        fail(
            "phase_b7_status",
            "Phase B7 is not ready for candidate materialization design",
        )

    b7_summary = {
        row["field"]: row["value"]
        for row in read_tsv(B7_OUT / "summary.tsv")
    }
    if (
        b7_summary.get("semantic_disposition_coverage") != "161"
        or b7_summary.get("total_elf_materialize") != "91"
        or b7_summary.get("selected_elf_lookup_collisions") != "0"
        or b7_summary.get("unclassified_objects") != "0"
    ):
        fail("phase_b7_summary", "Phase B7 structural gates are not accepted")

    elf_rows = read_tsv(B7_OUT / "candidate-elf-manifest.tsv")
    data_rows = read_tsv(B7_OUT / "candidate-data-manifest.tsv")
    schema_sources = read_tsv(B7_OUT / "schema-source-manifest.tsv")
    schema_contract_rows = read_tsv(B7_OUT / "schema-build-contract.tsv")

    if len(elf_rows) != 91:
        fail("manifest_shape", f"expected 91 ELF rows, found {len(elf_rows)}")
    font_rows = [
        row
        for row in data_rows
        if row["runtime_action"] == "MATERIALIZE_SELECTED_FONT"
    ]
    schema_data_rows = [
        row
        for row in data_rows
        if row["runtime_action"] == "GENERATE_GSETTINGS_SCHEMA"
    ]
    if len(font_rows) != 4 or len(schema_data_rows) != 1:
        fail("manifest_shape", "unexpected selected font or schema aggregate count")
    if len(schema_sources) != 37 or len(schema_contract_rows) != 1:
        fail("manifest_shape", "unexpected schema source/build-contract count")

    schema_contract = schema_contract_rows[0]
    compiler_path = Path(schema_contract["compiler_path"])
    expected_schema_sha = schema_contract["aggregate_expected_sha256"]

    source_specs: list[dict[str, str]] = []
    for row in elf_rows:
        source_specs.append(
            {
                "kind": "ELF",
                "source_path": row["source_path"],
                "expected_sha256": row["sha256"],
                "package": row["package"],
                "version": row["version"],
            }
        )
    for row in font_rows:
        source_specs.append(
            {
                "kind": "FONT",
                "source_path": row["source_path"],
                "expected_sha256": row["sha256"],
                "package": row["package"],
                "version": row["version"],
            }
        )
    for row in schema_sources:
        source_specs.append(
            {
                "kind": "SCHEMA_SOURCE",
                "source_path": row["source_path"],
                "expected_sha256": row["sha256"],
                "package": row["dpkg_file_owners"],
                "version": "FROM_SOURCE_PACKAGE_RECEIPT",
            }
        )
    source_specs.append(
        {
            "kind": "SCHEMA_COMPILER",
            "source_path": str(compiler_path),
            "expected_sha256": schema_contract["compiler_sha256"],
            "package": schema_contract["compiler_package"],
            "version": schema_contract["compiler_version"],
        }
    )

    stage = "source_identity_preflight"
    source_verification: list[dict[str, object]] = []
    source_failures = 0
    for spec in sorted(
        source_specs,
        key=lambda row: (row["kind"], row["source_path"]),
    ):
        source = Path(spec["source_path"])
        exists = source.is_file()
        current_sha = sha256(source) if exists else "MISSING"
        state = (
            "MATCH"
            if exists and current_sha == spec["expected_sha256"]
            else "MISSING"
            if not exists
            else "HASH_MISMATCH"
        )
        if state != "MATCH":
            source_failures += 1
        source_verification.append(
            {
                "kind": spec["kind"],
                "source_path": str(source),
                "package": spec["package"],
                "version": spec["version"],
                "expected_sha256": spec["expected_sha256"],
                "current_sha256": current_sha,
                "identity_state": state,
                "size_bytes": source.stat().st_size if exists else "-",
            }
        )
    write_tsv(
        OUT / "source-identity-verification.tsv",
        [
            "kind",
            "source_path",
            "package",
            "version",
            "expected_sha256",
            "current_sha256",
            "identity_state",
            "size_bytes",
        ],
        source_verification,
    )
    if source_failures:
        fail(stage, f"source identity failures: {source_failures}")

    content_rows: list[dict[str, object]] = []
    for row in elf_rows:
        content_rows.append(
            {
                "content_kind": "COPIED_ELF",
                "sha256": row["sha256"],
                "source_path": row["source_path"],
                "package": row["package"],
                "version": row["version"],
                "object_relpath": str(object_relpath(row["sha256"])),
            }
        )
    for row in font_rows:
        content_rows.append(
            {
                "content_kind": "COPIED_FONT",
                "sha256": row["sha256"],
                "source_path": row["source_path"],
                "package": row["package"],
                "version": row["version"],
                "object_relpath": str(object_relpath(row["sha256"])),
            }
        )
    content_rows.append(
        {
            "content_kind": "GENERATED_GSETTINGS",
            "sha256": expected_schema_sha,
            "source_path": "GENERATED_FROM_SCHEMA_BUILD_CONTRACT",
            "package": schema_contract["compiler_package"],
            "version": schema_contract["compiler_version"],
            "object_relpath": str(object_relpath(expected_schema_sha)),
        }
    )

    hash_to_rows: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in content_rows:
        hash_to_rows[str(row["sha256"])].append(row)
    duplicate_content_hashes = {
        digest: rows
        for digest, rows in hash_to_rows.items()
        if len(rows) > 1
    }

    canonical_content = sorted(
        [
            {
                "content_kind": row["content_kind"],
                "sha256": row["sha256"],
                "source_path": row["source_path"],
                "package": row["package"],
                "version": row["version"],
                "object_relpath": row["object_relpath"],
            }
            for row in content_rows
        ],
        key=lambda row: (
            str(row["sha256"]),
            str(row["content_kind"]),
            str(row["source_path"]),
        ),
    )

    seed_rows: list[dict[str, object]] = [
        {
            "b7_head": b7_summary.get("head", ""),
            "generation_base": str(GENERATION_BASE),
        }
    ]
    seed_rows.extend(canonical_content)
    seed_rows.extend(
        sorted(
            [
                {
                    "schema_source_path": row["source_path"],
                    "sha256": row["sha256"],
                    "owner": row["dpkg_file_owners"],
                }
                for row in schema_sources
            ],
            key=lambda row: str(row["schema_source_path"]),
        )
    )
    seed_rows.append(
        {
            "compiler_path": schema_contract["compiler_path"],
            "compiler_sha256": schema_contract["compiler_sha256"],
            "accepted_modes": schema_contract["accepted_modes"],
            "aggregate_expected_sha256": expected_schema_sha,
        }
    )
    generation_digest = canonical_digest(seed_rows)
    generation_id = f"obsidian-cpu-{generation_digest[:20]}"

    object_store_root = GENERATION_BASE / "objects/sha256"
    staging_root = GENERATION_BASE / "staging"
    generations_root = GENERATION_BASE / "generations"
    generation_dir = generations_root / generation_id
    current_link = GENERATION_BASE / "current"

    alias_candidates: list[dict[str, object]] = []
    for row in elf_rows:
        source = Path(row["source_path"])
        aliases = {
            ("LOOKUP_NAME", row["lookup_name"]),
            ("SONAME", row["soname"]),
            ("SOURCE_BASENAME", source.name),
        }
        for alias_kind, alias in sorted(aliases):
            if not safe_alias(alias):
                continue
            alias_relpath = Path("lib") / alias
            object_path = GENERATION_BASE / object_relpath(row["sha256"])
            alias_path = generation_dir / alias_relpath
            alias_candidates.append(
                {
                    "alias_kind": alias_kind,
                    "alias_relpath": str(alias_relpath),
                    "alias_name": alias,
                    "sha256": row["sha256"],
                    "source_path": row["source_path"],
                    "object_relpath": str(object_relpath(row["sha256"])),
                    "relative_symlink_target": os.path.relpath(
                        object_path,
                        alias_path.parent,
                    ),
                }
            )

    for row in font_rows:
        alias = Path(row["source_path"]).name
        if not safe_alias(alias):
            fail("alias_namespace", f"unsafe font alias: {alias}")
        alias_relpath = Path("share/fonts/selected") / alias
        object_path = GENERATION_BASE / object_relpath(row["sha256"])
        alias_path = generation_dir / alias_relpath
        alias_candidates.append(
            {
                "alias_kind": "FONT_BASENAME",
                "alias_relpath": str(alias_relpath),
                "alias_name": alias,
                "sha256": row["sha256"],
                "source_path": row["source_path"],
                "object_relpath": str(object_relpath(row["sha256"])),
                "relative_symlink_target": os.path.relpath(
                    object_path,
                    alias_path.parent,
                ),
            }
        )

    schema_alias_relpath = Path("share/glib-2.0/schemas/gschemas.compiled")
    schema_object_path = GENERATION_BASE / object_relpath(expected_schema_sha)
    schema_alias_path = generation_dir / schema_alias_relpath
    alias_candidates.append(
        {
            "alias_kind": "GENERATED_SCHEMA_AGGREGATE",
            "alias_relpath": str(schema_alias_relpath),
            "alias_name": "gschemas.compiled",
            "sha256": expected_schema_sha,
            "source_path": "GENERATED_FROM_SCHEMA_BUILD_CONTRACT",
            "object_relpath": str(object_relpath(expected_schema_sha)),
            "relative_symlink_target": os.path.relpath(
                schema_object_path,
                schema_alias_path.parent,
            ),
        }
    )

    stage = "alias_namespace"
    alias_map: dict[str, dict[str, object]] = {}
    alias_collisions: list[dict[str, object]] = []
    for row in sorted(
        alias_candidates,
        key=lambda item: (
            str(item["alias_relpath"]),
            str(item["alias_kind"]),
            str(item["source_path"]),
        ),
    ):
        key = str(row["alias_relpath"])
        previous = alias_map.get(key)
        if previous is None:
            alias_map[key] = row
        elif previous["sha256"] != row["sha256"]:
            alias_collisions.append(
                {
                    "alias_relpath": key,
                    "left_sha256": previous["sha256"],
                    "left_source": previous["source_path"],
                    "right_sha256": row["sha256"],
                    "right_source": row["source_path"],
                }
            )

    write_tsv(
        OUT / "alias-collisions.tsv",
        [
            "alias_relpath",
            "left_sha256",
            "left_source",
            "right_sha256",
            "right_source",
        ],
        alias_collisions,
    )
    if alias_collisions:
        fail(stage, f"generation alias collisions: {len(alias_collisions)}")

    alias_rows = sorted(
        alias_map.values(),
        key=lambda row: str(row["alias_relpath"]),
    )

    write_tsv(
        OUT / "content-object-plan.tsv",
        [
            "content_kind",
            "sha256",
            "source_path",
            "package",
            "version",
            "object_relpath",
        ],
        canonical_content,
    )
    write_tsv(
        OUT / "generation-alias-plan.tsv",
        [
            "alias_kind",
            "alias_relpath",
            "alias_name",
            "sha256",
            "source_path",
            "object_relpath",
            "relative_symlink_target",
        ],
        alias_rows,
    )

    existing_ancestor = nearest_existing(GENERATION_BASE)
    layout_rows = [
        {"field": "generation_base", "value": str(GENERATION_BASE)},
        {"field": "existing_base_ancestor", "value": str(existing_ancestor)},
        {"field": "base_device_id", "value": existing_ancestor.stat().st_dev},
        {"field": "object_store_root", "value": str(object_store_root)},
        {"field": "staging_root", "value": str(staging_root)},
        {"field": "generations_root", "value": str(generations_root)},
        {"field": "generation_digest", "value": generation_digest},
        {"field": "generation_id", "value": generation_id},
        {"field": "generation_dir", "value": str(generation_dir)},
        {"field": "current_link", "value": str(current_link)},
        {
            "field": "candidate_library_dir",
            "value": str(generation_dir / "lib"),
        },
        {
            "field": "candidate_font_dir",
            "value": str(generation_dir / "share/fonts/selected"),
        },
        {
            "field": "candidate_schema_dir",
            "value": str(generation_dir / "share/glib-2.0/schemas"),
        },
    ]
    write_tsv(OUT / "generation-layout.tsv", ["field", "value"], layout_rows)

    (OUT / "activation-contract.txt").write_text(
        "Materialize content-addressed objects before constructing a generation.\n"
        "Create the generation under generation_base/staging on the same filesystem as generations and current.\n"
        "Populate only generation-local relative symlinks plus copied manifests and receipts.\n"
        "Validate every object hash, alias target, manifest count, schema aggregate hash, and zero collision before publication.\n"
        "Publish the immutable generation with one rename from staging to generations/<generation-id>.\n"
        "Validate the candidate with an explicit generation path before changing current.\n"
        "Activate by creating a temporary symlink beside current and atomically renaming it over current.\n"
        "Never change current while generation construction or candidate validation is incomplete.\n"
    )
    (OUT / "rollback-contract.txt").write_text(
        "Record the previously resolved current generation before activation.\n"
        "Rollback uses the same temporary-symlink plus atomic-rename operation to point current at the previous complete generation.\n"
        "Never mutate an immutable generation during rollback.\n"
        "Do not garbage-collect any generation referenced by current, the previous-generation receipt, or an active process-validation receipt.\n"
    )
    (OUT / "launcher-selection-contract.txt").write_text(
        "Candidate validation must use the explicit generation library directory, not current and not the broad farm.\n"
        "The candidate library namespace contains no app-local or world-substrate ELF.\n"
        "App-local locality remains protected by the verified zero-collision contract.\n"
        "The protected glibc world and locale remain referenced outside the application generation.\n"
        "GSETTINGS_SCHEMA_DIR must point to the explicit generation schema directory during candidate validation.\n"
        "Selected font discovery must be scoped to the explicit generation font directory or an explicit receipt-owned fontconfig input.\n"
    )

    kind_counts = Counter(str(row["content_kind"]) for row in content_rows)
    alias_kind_counts = Counter(str(row["alias_kind"]) for row in alias_rows)
    summary_rows = [
        {"field": "branch", "value": branch},
        {"field": "head", "value": head},
        {"field": "phase_b7_root", "value": str(B7_OUT)},
        {"field": "phase_b7_head", "value": b7_summary.get("head", "")},
        {"field": "generation_id", "value": generation_id},
        {"field": "generation_digest", "value": generation_digest},
        {"field": "source_identity_checks", "value": len(source_verification)},
        {"field": "source_identity_failures", "value": source_failures},
        {"field": "copied_elf_content_objects", "value": kind_counts["COPIED_ELF"]},
        {"field": "copied_font_content_objects", "value": kind_counts["COPIED_FONT"]},
        {"field": "generated_schema_content_objects", "value": kind_counts["GENERATED_GSETTINGS"]},
        {"field": "content_plan_rows", "value": len(content_rows)},
        {"field": "unique_content_hashes", "value": len(hash_to_rows)},
        {"field": "duplicate_content_hashes", "value": len(duplicate_content_hashes)},
        {
            "field": "elf_aliases",
            "value": sum(
                count
                for kind, count in alias_kind_counts.items()
                if kind in {"LOOKUP_NAME", "SONAME", "SOURCE_BASENAME"}
            ),
        },
        {"field": "font_aliases", "value": alias_kind_counts["FONT_BASENAME"]},
        {"field": "schema_aliases", "value": alias_kind_counts["GENERATED_SCHEMA_AGGREGATE"]},
        {"field": "total_generation_aliases", "value": len(alias_rows)},
        {"field": "generation_alias_collisions", "value": len(alias_collisions)},
        {"field": "schema_source_files", "value": len(schema_sources)},
        {"field": "runtime_launch_performed", "value": "NO"},
        {"field": "candidate_bytes_materialized", "value": "NO"},
        {"field": "promoted_runtime_mutated", "value": "NO"},
    ]
    write_tsv(OUT / "summary.tsv", ["field", "value"], summary_rows)

    (OUT / "claim-boundary.txt").write_text(
        "This is a read-only source-identity, content-object, alias-namespace, and activation-contract preflight.\n"
        "It does not create the generation base, content store, staging tree, generation, current pointer, or launcher changes.\n"
        "The generation identifier is derived from the accepted Phase B7 content/build contract and configured generation base.\n"
        "The contract requires explicit-generation validation before atomic current-pointer replacement.\n"
        "No application is launched and no promoted runtime is mutated.\n"
    )
    (OUT / "next-state.txt").write_text(
        "READY_FOR_STAGING_MATERIALIZER_IMPLEMENTATION\n"
    )
    write_status("PASS")
    if (OUT / "failure-stage.txt").exists():
        (OUT / "failure-stage.txt").unlink()

    print("selected Obsidian Phase B8 generation layout preflight: PASS")
    print(f"evidence: {OUT}")
    print("\n===== summary =====")
    for row in summary_rows:
        print(f"{row['field']}\t{row['value']}")

except SystemExit:
    raise
except Exception:
    write_status("FAIL")
    (OUT / "failure-stage.txt").write_text(stage + "\n")
    traceback.print_exc()
    print(f"evidence: {OUT}", file=sys.stderr)
    raise SystemExit(1)
