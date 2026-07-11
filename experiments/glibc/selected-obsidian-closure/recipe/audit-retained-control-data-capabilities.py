#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import os
import shutil
import subprocess
import sys
import traceback
from collections import defaultdict
from pathlib import Path

B2_OUT = Path(os.environ["B2_OUT"])
OUT = Path(
    os.environ.get(
        "OUT",
        "/tmp/selected-obsidian-phase-b5-data-capability-provenance",
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
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def write_status(value: str) -> None:
    (OUT / "analysis.status").write_text(value + "\n")


def fail(stage_name: str, message: str, rc: int = 1) -> None:
    write_status("FAIL")
    (OUT / "failure-stage.txt").write_text(stage_name + "\n")
    print(message, file=sys.stderr)
    print(f"evidence: {OUT}", file=sys.stderr)
    raise SystemExit(rc)


def rootfs_split(path: Path) -> tuple[Path | None, str | None]:
    text = str(path)
    marker = "/rootfs/"
    if marker not in text:
        return None, None
    before, after = text.split(marker, 1)
    return Path(before + "/rootfs"), "/" + after


def build_dpkg_file_index(rootfs: Path) -> dict[str, set[str]]:
    index: dict[str, set[str]] = defaultdict(set)
    info_dir = rootfs / "var/lib/dpkg/info"
    if not info_dir.is_dir():
        return index
    for list_file in sorted(info_dir.glob("*.list")):
        package = list_file.name[: -len(".list")]
        try:
            lines = list_file.read_text(errors="replace").splitlines()
        except OSError:
            continue
        for line in lines:
            if line.startswith("/"):
                index[line].add(package)
    return index


def owner_text(index: dict[str, set[str]], relative: str | None) -> str:
    if not relative:
        return "-"
    owners = sorted(index.get(relative, set()))
    return ",".join(owners) if owners else "UNOWNED"


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
            "tracked working-tree changes detected; Phase B5 requires exact HEAD",
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
    (OUT / "phase-b2-root.txt").write_text(str(B2_OUT) + "\n")

    required = [
        "analysis.status",
        "summary.tsv",
        "data-capabilities.tsv",
    ]
    verify_rows: list[dict[str, object]] = []
    missing: list[str] = []
    stage = "input_verification"
    for name in required:
        source = B2_OUT / name
        embedded = OUT / "input" / name.replace("/", "_")
        state = "PASS" if source.is_file() else "FAIL"
        verify_rows.append(
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
        verify_rows,
    )
    if missing:
        fail(stage, f"missing Phase B2 inputs: {', '.join(missing)}")

    if (B2_OUT / "analysis.status").read_text().strip() != "PASS":
        fail("phase_b2_status", "Phase B2 status is not PASS")

    b2_summary = {
        row["field"]: row["value"]
        for row in read_tsv(B2_OUT / "summary.tsv")
    }
    data_rows = read_tsv(B2_OUT / "data-capabilities.tsv")
    if not data_rows:
        fail("data_input", "Phase B2 data-capabilities.tsv is empty")

    rootfs_values: set[Path] = set()
    split_cache: dict[str, tuple[Path | None, str | None]] = {}
    for row in data_rows:
        path = Path(row["path"])
        split = rootfs_split(path)
        split_cache[row["path"]] = split
        if split[0] is not None:
            rootfs_values.add(split[0])

    if len(rootfs_values) > 1:
        fail(
            "rootfs_detection",
            "multiple rootfs roots detected in retained data objects: "
            + ", ".join(str(value) for value in sorted(rootfs_values)),
        )

    rootfs = next(iter(rootfs_values), None)
    dpkg_index = build_dpkg_file_index(rootfs) if rootfs else {}

    stage = "data_identity_and_ownership"
    object_rows: list[dict[str, object]] = []
    identity_mismatch = 0
    missing_paths = 0
    rootfs_unowned_nonaggregate = 0
    semantic_counts: dict[str, int] = defaultdict(int)

    for row in data_rows:
        path = Path(row["path"])
        semantic = row["semantic_class"]
        semantic_counts[semantic] += 1
        exists = path.is_file()
        current_sha = sha256(path) if exists else "MISSING"
        identity_state = (
            "MATCH"
            if exists and current_sha == row["sha256"]
            else "MISSING"
            if not exists
            else "HASH_MISMATCH"
        )
        if identity_state == "MISSING":
            missing_paths += 1
        elif identity_state == "HASH_MISMATCH":
            identity_mismatch += 1

        detected_rootfs, relative = split_cache[row["path"]]
        owners = owner_text(dpkg_index, relative)
        expected_package = row["package"]
        ownership_state = "NOT_ROOTFS"
        if detected_rootfs is not None:
            if owners == "UNOWNED":
                ownership_state = "GENERATED_OR_UNOWNED"
                if semantic != "PROVIDER_SCHEMA_DATA":
                    rootfs_unowned_nonaggregate += 1
            else:
                owner_set = set(owners.split(","))
                normalized_expected = expected_package
                ownership_state = (
                    "MATCH"
                    if normalized_expected in owner_set
                    else "OWNER_DIFFERS_FROM_CAPTURE"
                )

        object_rows.append(
            {
                "semantic_class": semantic,
                "path": row["path"],
                "captured_package": expected_package,
                "captured_version": row["version"],
                "captured_sha256": row["sha256"],
                "current_sha256": current_sha,
                "identity_state": identity_state,
                "rootfs_relative_path": relative or "-",
                "dpkg_file_owners": owners,
                "ownership_state": ownership_state,
            }
        )

    write_tsv(
        OUT / "data-object-verification.tsv",
        [
            "semantic_class",
            "path",
            "captured_package",
            "captured_version",
            "captured_sha256",
            "current_sha256",
            "identity_state",
            "rootfs_relative_path",
            "dpkg_file_owners",
            "ownership_state",
        ],
        sorted(object_rows, key=lambda row: (str(row["semantic_class"]), str(row["path"]))),
    )

    schema_rows = [
        row for row in data_rows if row["semantic_class"] == "PROVIDER_SCHEMA_DATA"
    ]
    schema_source_rows: list[dict[str, object]] = []
    schema_tool_rows: list[dict[str, object]] = []
    schema_source_count = 0
    schema_unowned_source_count = 0
    schema_compiler_present = 0

    stage = "schema_source_inventory"
    for aggregate in schema_rows:
        aggregate_path = Path(aggregate["path"])
        schema_dir = aggregate_path.parent
        detected_rootfs, _ = rootfs_split(aggregate_path)
        local_index = dpkg_index if detected_rootfs == rootfs else build_dpkg_file_index(detected_rootfs) if detected_rootfs else {}

        for pattern in ("*.gschema.xml", "*.gschema.override"):
            for source in sorted(schema_dir.glob(pattern)):
                if not source.is_file():
                    continue
                source_rootfs, relative = rootfs_split(source)
                owners = owner_text(local_index, relative)
                schema_source_count += 1
                if owners == "UNOWNED":
                    schema_unowned_source_count += 1
                schema_source_rows.append(
                    {
                        "aggregate_path": str(aggregate_path),
                        "source_kind": "XML" if pattern.endswith("xml") else "OVERRIDE",
                        "source_path": str(source),
                        "rootfs_relative_path": relative or "-",
                        "sha256": sha256(source),
                        "dpkg_file_owners": owners,
                    }
                )

        if detected_rootfs is not None:
            compiler = detected_rootfs / "usr/bin/glib-compile-schemas"
            compiler_exists = compiler.is_file()
            if compiler_exists:
                schema_compiler_present += 1
            compiler_rootfs, compiler_relative = rootfs_split(compiler)
            schema_tool_rows.append(
                {
                    "aggregate_path": str(aggregate_path),
                    "compiler_path": str(compiler),
                    "compiler_present": "YES" if compiler_exists else "NO",
                    "compiler_sha256": sha256(compiler) if compiler_exists else "MISSING",
                    "dpkg_file_owners": owner_text(local_index, compiler_relative),
                }
            )

    write_tsv(
        OUT / "schema-source-manifest.tsv",
        [
            "aggregate_path",
            "source_kind",
            "source_path",
            "rootfs_relative_path",
            "sha256",
            "dpkg_file_owners",
        ],
        schema_source_rows,
    )
    write_tsv(
        OUT / "schema-compiler-verification.tsv",
        [
            "aggregate_path",
            "compiler_path",
            "compiler_present",
            "compiler_sha256",
            "dpkg_file_owners",
        ],
        schema_tool_rows,
    )

    decision_rows: list[dict[str, object]] = []
    for semantic in sorted(semantic_counts):
        if semantic == "PROVIDER_LOCALE_DATA":
            owner = "WORLD_LOCALE_GLIBC"
            materialization = "REFERENCE_PREFIX_MANAGED_DATA"
            rationale = "glibc-version-coupled locale data already owned by the protected prefix substrate"
        elif semantic == "PROVIDER_FONT_DATA":
            owner = "SELECTED_FONT_DATA"
            materialization = "MATERIALIZE_EXACT_PACKAGE_OWNED_FILES"
            rationale = "passive reusable font files should not require rootfs runtime authority"
        elif semantic == "PROVIDER_SCHEMA_DATA":
            owner = "SELECTED_GSETTINGS_SCHEMA_DATA"
            materialization = "REBUILD_FROM_OWNED_SOURCE_MANIFEST"
            rationale = "compiled aggregate is generated and must be tied to source and compiler provenance"
        else:
            owner = "REVIEW"
            materialization = "REVIEW"
            rationale = "unexpected semantic class"
        decision_rows.append(
            {
                "semantic_class": semantic,
                "object_count": semantic_counts[semantic],
                "proposed_owner": owner,
                "proposed_materialization": materialization,
                "rationale": rationale,
            }
        )

    write_tsv(
        OUT / "data-ownership-decision-input.tsv",
        [
            "semantic_class",
            "object_count",
            "proposed_owner",
            "proposed_materialization",
            "rationale",
        ],
        decision_rows,
    )

    rootfs_owned_font_count = sum(
        1
        for row in object_rows
        if row["semantic_class"] == "PROVIDER_FONT_DATA"
        and row["ownership_state"] == "MATCH"
    )
    font_count = semantic_counts.get("PROVIDER_FONT_DATA", 0)
    schema_aggregate_count = semantic_counts.get("PROVIDER_SCHEMA_DATA", 0)

    summary_rows = [
        {"field": "branch", "value": branch},
        {"field": "head", "value": head},
        {"field": "phase_b2_root", "value": str(B2_OUT)},
        {"field": "phase_b2_head", "value": b2_summary.get("head", "")},
        {"field": "data_objects", "value": len(data_rows)},
        {"field": "locale_objects", "value": semantic_counts.get("PROVIDER_LOCALE_DATA", 0)},
        {"field": "font_objects", "value": font_count},
        {"field": "schema_aggregate_objects", "value": schema_aggregate_count},
        {"field": "identity_mismatches", "value": identity_mismatch},
        {"field": "missing_paths", "value": missing_paths},
        {"field": "rootfs_owned_font_objects", "value": rootfs_owned_font_count},
        {"field": "rootfs_unowned_nonaggregate_objects", "value": rootfs_unowned_nonaggregate},
        {"field": "schema_source_files", "value": schema_source_count},
        {"field": "schema_unowned_source_files", "value": schema_unowned_source_count},
        {"field": "schema_compiler_instances_present", "value": schema_compiler_present},
        {"field": "runtime_launch_performed", "value": "NO"},
        {"field": "promoted_runtime_mutated", "value": "NO"},
    ]
    write_tsv(OUT / "summary.tsv", ["field", "value"], summary_rows)

    (OUT / "claim-boundary.txt").write_text(
        "This is a read-only identity, package-ownership, and schema-source inventory.\n"
        "Package ownership is derived from rootfs dpkg .list files, not by executing rootfs package tools.\n"
        "Schema source inventory does not yet prove that recompilation reproduces the retained aggregate byte-for-byte.\n"
        "Proposed owners are architecture decision inputs, not promoted runtime state.\n"
        "The analysis does not materialize data, launch Obsidian, or mutate the promoted runtime.\n"
    )

    blocking = (
        identity_mismatch
        + missing_paths
        + rootfs_unowned_nonaggregate
        + schema_unowned_source_count
    )
    if schema_aggregate_count and schema_source_count == 0:
        blocking += 1
    if schema_aggregate_count and schema_compiler_present == 0:
        blocking += 1
    if rootfs_owned_font_count != font_count:
        blocking += 1

    if blocking:
        (OUT / "next-state.txt").write_text("REVIEW_DATA_PROVENANCE_GAPS\n")
    else:
        (OUT / "next-state.txt").write_text("READY_FOR_DATA_OWNERSHIP_DECISION\n")

    write_status("PASS")
    if (OUT / "failure-stage.txt").exists():
        (OUT / "failure-stage.txt").unlink()

    print("selected Obsidian Phase B5 data capability provenance audit: PASS")
    print(f"evidence: {OUT}")
    print("\n===== summary =====")
    for row in summary_rows:
        print(f"{row['field']}\t{row['value']}")
    print("\n===== next state =====")
    print((OUT / "next-state.txt").read_text(), end="")

except SystemExit:
    raise
except Exception:
    write_status("FAIL")
    (OUT / "failure-stage.txt").write_text(stage + "\n")
    traceback.print_exc()
    print(f"evidence: {OUT}", file=sys.stderr)
    raise SystemExit(1)
