#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import os
import subprocess
import sys
import traceback
from collections import Counter
from pathlib import Path

B1_OUT = Path(os.environ["B1_OUT"])
B2_OUT = Path(os.environ["B2_OUT"])
B9_OUT = Path(os.environ["B9_OUT"])
B10_OUT = Path(os.environ["B10_OUT"])
OUT = Path(os.environ["OUT"])
PREFIX = Path(os.environ["PREFIX"])
HOME = Path(os.environ["HOME"])
ROOTFS = Path(
    os.environ.get(
        "ROOTFS",
        str(PREFIX / "var/lib/proot-distro/containers/debian/rootfs"),
    )
)
APP = Path(os.environ.get("APP", str(HOME / "gl/apps/obsidian")))
REPO = Path(
    subprocess.check_output(
        ["git", "-C", str(Path(__file__).resolve().parent), "rev-parse", "--show-toplevel"],
        text=True,
    ).strip()
)

stage = "initialization"


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, fields: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fields,
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def summary_map(path: Path) -> dict[str, str]:
    return {row["field"]: row["value"] for row in read_tsv(path)}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def write_status(value: str) -> None:
    (OUT / "analysis.status").write_text(value + "\n")


def fail(stage_name: str, message: str, rc: int = 1) -> None:
    write_status("FAIL")
    (OUT / "failure-stage.txt").write_text(stage_name + "\n")
    print(message, file=sys.stderr)
    print(f"evidence: {OUT}", file=sys.stderr)
    raise SystemExit(rc)


try:
    OUT.mkdir(parents=True, exist_ok=True)

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
        fail(stage, "tracked working-tree changes detected", 2)

    branch = subprocess.check_output(
        ["git", "-C", str(REPO), "branch", "--show-current"],
        text=True,
    ).strip()
    head = subprocess.check_output(
        ["git", "-C", str(REPO), "rev-parse", "HEAD"],
        text=True,
    ).strip()

    stage = "input_verification"
    required = [
        B1_OUT / "audit.status",
        B1_OUT / "elf-objects.tsv",
        B2_OUT / "analysis.status",
        B2_OUT / "resolved-edges.tsv",
        B9_OUT / "analysis.status",
        B9_OUT / "summary.tsv",
        B9_OUT / "input/content-object-plan.tsv",
        B9_OUT / "input/input__semantic-object-disposition.tsv",
        B10_OUT / "interaction-contract.tsv",
        B10_OUT / "analysis.status",
        B10_OUT / "failure-stage.txt",
        B10_OUT / "capture/topology.status",
        B10_OUT / "capture/survival.status",
        B10_OUT / "capture/maps-capture.status",
        B10_OUT / "capture/unique-objects.tsv",
        B10_OUT / "capture/processes.tsv",
        B10_OUT / "current-state-before.tsv",
        B10_OUT / "current-state-after.tsv",
        B10_OUT / "runtime-root-contract.tsv",
        B10_OUT / "missing-expected-mapped-paths.tsv",
    ]
    verification_rows: list[dict[str, object]] = []
    missing_inputs: list[str] = []
    for path in required:
        state_value = "PASS" if path.is_file() else "FAIL"
        verification_rows.append({"path": str(path), "state": state_value})
        if state_value == "FAIL":
            missing_inputs.append(str(path))
    write_tsv(OUT / "input-verification.tsv", ["path", "state"], verification_rows)
    if missing_inputs:
        fail(stage, "missing required inputs: " + ", ".join(missing_inputs))

    if (B1_OUT / "audit.status").read_text().strip() != "PASS":
        fail(stage, "Phase B1 status is not PASS")
    if (B2_OUT / "analysis.status").read_text().strip() != "PASS":
        fail(stage, "Phase B2 status is not PASS")
    if (B9_OUT / "analysis.status").read_text().strip() != "PASS":
        fail(stage, "Phase B9 status is not PASS")
    if (B10_OUT / "analysis.status").read_text().strip() != "FAIL":
        fail(stage, "passive B10 analysis status is not FAIL")
    if (B10_OUT / "failure-stage.txt").read_text().strip() != "mapped_identity":
        fail(stage, "passive B10 failure stage is not mapped_identity")
    for name in ("topology.status", "survival.status", "maps-capture.status"):
        if (B10_OUT / "capture" / name).read_text().strip() != "PASS":
            fail(stage, f"passive B10 capture gate is not PASS: {name}")

    interaction = summary_map(B10_OUT / "interaction-contract.tsv")
    if interaction.get("mode") != "PASSIVE_NO_GUI_INPUT":
        fail(stage, "interaction contract is not passive")

    before = read_tsv(B10_OUT / "current-state-before.tsv")
    after = read_tsv(B10_OUT / "current-state-after.tsv")
    if len(before) != 1 or len(after) != 1 or before[0] != after[0]:
        fail(stage, "current-state before/after evidence differs")
    if before[0]["state"] != "ABSENT":
        fail(stage, "current was not absent")

    b9_summary = summary_map(B9_OUT / "summary.tsv")
    generation_dir = Path(b9_summary["generation_dir"])
    generation_base = generation_dir.parent.parent
    validation_root = Path(summary_map(B10_OUT / "runtime-root-contract.tsv")["validation_root"])

    content_rows = read_tsv(B9_OUT / "input/content-object-plan.tsv")
    semantic_rows = read_tsv(B9_OUT / "input/input__semantic-object-disposition.tsv")
    elf_rows = read_tsv(B1_OUT / "elf-objects.tsv")
    edge_rows = read_tsv(B2_OUT / "resolved-edges.tsv")
    unique_rows = read_tsv(B10_OUT / "capture/unique-objects.tsv")
    process_rows = read_tsv(B10_OUT / "capture/processes.tsv")

    actual_paths = {row["path"] for row in unique_rows}
    elf_by_path = {row["path"]: row for row in elf_rows}

    stage = "selected_map_state"
    selected_rows: list[dict[str, object]] = []
    selected_expected_paths: set[str] = set()
    selected_source_paths: set[str] = set()
    selected_state_counts: Counter[str] = Counter()
    selected_kind_mapped: Counter[str] = Counter()
    live_identity_rows: list[dict[str, object]] = []

    for row in content_rows:
        object_path = generation_base / row["object_relpath"]
        source_path = Path(row["source_path"])
        object_text = str(object_path)
        source_text = str(source_path)
        selected_expected_paths.add(object_text)
        selected_source_paths.add(source_text)

        object_mapped = object_text in actual_paths
        source_mapped = source_text in actual_paths
        if object_mapped:
            state_value = "MAPPED_SELECTED_OBJECT"
            selected_kind_mapped[row["content_kind"]] += 1
        elif source_mapped:
            state_value = "MAPPED_SOURCE_SUBSTITUTE"
        else:
            state_value = "NOT_MAPPED"
        selected_state_counts[state_value] += 1

        object_exists = object_path.is_file() and not object_path.is_symlink()
        object_sha = sha256(object_path) if object_exists else "MISSING"
        object_identity = (
            "MATCH"
            if object_exists and object_sha == row["sha256"]
            else "MISSING"
            if not object_exists
            else "HASH_MISMATCH"
        )
        live_identity_rows.append(
            {
                "role": "SELECTED_OBJECT",
                "path": object_text,
                "expected_sha256": row["sha256"],
                "observed_sha256": object_sha,
                "state": object_identity,
            }
        )
        if object_identity != "MATCH":
            fail(stage, f"selected object identity failed: {object_text}")

        source_identity = "NOT_CHECKED"
        source_sha = "-"
        if source_mapped:
            if source_path.is_file() and not source_path.is_symlink():
                source_sha = sha256(source_path)
                source_identity = "MATCH" if source_sha == row["sha256"] else "HASH_MISMATCH"
            else:
                source_identity = "MISSING"
            live_identity_rows.append(
                {
                    "role": "MAPPED_SOURCE_SUBSTITUTE",
                    "path": source_text,
                    "expected_sha256": row["sha256"],
                    "observed_sha256": source_sha,
                    "state": source_identity,
                }
            )
            if source_identity != "MATCH":
                fail(stage, f"mapped source substitute identity failed: {source_text}")

        selected_rows.append(
            {
                "content_kind": row["content_kind"],
                "sha256": row["sha256"],
                "source_path": source_text,
                "object_path": object_text,
                "object_mapped": "YES" if object_mapped else "NO",
                "source_mapped": "YES" if source_mapped else "NO",
                "map_state": state_value,
                "source_identity": source_identity,
            }
        )

    write_tsv(
        OUT / "selected-map-state.tsv",
        [
            "content_kind",
            "sha256",
            "source_path",
            "object_path",
            "object_mapped",
            "source_mapped",
            "map_state",
            "source_identity",
        ],
        selected_rows,
    )

    expected_missing = {
        "0245743bb594ee1ac2c1325873d70407c790f890477d8a0fe8323bda8803f705",
        "0d3c03d1b667192f91223660a3163325cf83132662fe4d9f7d6e596bf7a995c2",
        "1a8bc733979360f2e3327d805efe64f9306247bacb90cac9efdc0cf1e033bb89",
    }
    observed_missing = {
        row["sha256"]
        for row in selected_rows
        if row["map_state"] != "MAPPED_SELECTED_OBJECT"
    }
    if observed_missing != expected_missing:
        fail(stage, f"unexpected selected-map missing set: {sorted(observed_missing)}")

    stage = "rpath_analysis"
    selected_elf_sources = {
        row["source_path"] for row in content_rows if row["content_kind"] == "COPIED_ELF"
    }
    rpath_rows: list[dict[str, object]] = []
    rpath_consumers: set[str] = set()
    for source_text in sorted(selected_elf_sources):
        elf = elf_by_path.get(source_text)
        if elf is None:
            fail(stage, f"selected ELF absent from B1 metadata: {source_text}")
        if elf["rpath"] == "-" and elf["runpath"] == "-":
            continue
        rpath_consumers.add(source_text)
        content = next(row for row in content_rows if row["source_path"] == source_text)
        object_path = generation_base / content["object_relpath"]
        rpath_rows.append(
            {
                "source_path": source_text,
                "object_path": str(object_path),
                "soname": elf["soname"],
                "lookup_name": elf["lookup_name"],
                "rpath": elf["rpath"],
                "runpath": elf["runpath"],
                "object_mapped": "YES" if str(object_path) in actual_paths else "NO",
            }
        )
    write_tsv(
        OUT / "selected-rpath-consumers.tsv",
        [
            "source_path",
            "object_path",
            "soname",
            "lookup_name",
            "rpath",
            "runpath",
            "object_mapped",
        ],
        rpath_rows,
    )

    bypass_source_paths = {
        row["source_path"]
        for row in selected_rows
        if row["map_state"] == "MAPPED_SOURCE_SUBSTITUTE"
    }
    rpath_edge_rows = [
        row
        for row in edge_rows
        if row["consumer_path"] in rpath_consumers
        and row["provider_path"] in bypass_source_paths
    ]
    write_tsv(
        OUT / "rpath-provider-edges.tsv",
        ["consumer_path", "provider_path", "needed"],
        rpath_edge_rows,
    )

    if len(rpath_rows) != 4:
        fail(stage, f"expected four selected ELF RPATH consumers, found {len(rpath_rows)}")
    if any(row["rpath"] != str(PREFIX / "glibc/lib") for row in rpath_rows):
        fail(stage, "selected RPATH consumer does not use the expected absolute world prefix")
    if len(rpath_edge_rows) != 6:
        fail(stage, f"expected six RPATH-to-bypassed-provider edges, found {len(rpath_edge_rows)}")

    stage = "semantic_classification"
    app_expected = {
        row["path"]
        for row in semantic_rows
        if row["primary_action"] == "REFERENCE_APP_LOCAL"
    }
    world_expected = {
        row["path"]
        for row in semantic_rows
        if row["primary_action"]
        in {"REFERENCE_WORLD_SUBSTRATE", "REFERENCE_WORLD_LOCALE"}
    }
    excluded = {
        row["path"]
        for row in semantic_rows
        if row["primary_action"] == "EXCLUDE_CPU_BASE_GRAPHICS_FEATURE"
    }

    missing_app = sorted(app_expected - actual_paths)
    missing_world = sorted(world_expected - actual_paths)
    if missing_app or missing_world:
        fail(stage, "expected app-local or protected-world mappings are missing")

    classification_rows: list[dict[str, object]] = []
    classification_counts: Counter[str] = Counter()
    exception_paths: list[dict[str, object]] = []
    for path_text in sorted(actual_paths):
        path = Path(path_text)
        if path_text in selected_expected_paths:
            category = "SELECTED_OBJECT"
        elif path_text in app_expected:
            category = "APP_LOCAL_EXPECTED"
        elif path_text in world_expected:
            category = "PROTECTED_WORLD_EXPECTED"
        elif path_text in bypass_source_paths:
            category = "SELECTED_SOURCE_SUBSTITUTE"
        elif path_text in excluded:
            category = "EXCLUDED_SEMANTIC_MAPPING"
            exception_paths.append({"category": category, "path": path_text})
        elif within(path, validation_root):
            category = "RECEIPT_MUTABLE_STATE"
        elif within(path, APP):
            category = "UNMODELLED_APP_LOCAL"
            exception_paths.append({"category": category, "path": path_text})
        elif within(path, HOME / "gl/lib"):
            category = "BROAD_FARM"
            exception_paths.append({"category": category, "path": path_text})
        elif within(path, ROOTFS):
            category = "ROOTFS_PROVIDER"
            exception_paths.append({"category": category, "path": path_text})
        else:
            category = "OTHER_UNMODELLED"
            exception_paths.append({"category": category, "path": path_text})
        classification_counts[category] += 1
        classification_rows.append({"category": category, "path": path_text})

    write_tsv(
        OUT / "mapped-path-classification.tsv",
        ["category", "path"],
        classification_rows,
    )
    write_tsv(
        OUT / "cpu-map-exceptions.tsv",
        ["category", "path"],
        exception_paths,
    )

    expected_exception_set = {
        ("EXCLUDED_SEMANTIC_MAPPING", str(PREFIX / "glibc/lib/libX11-xcb.so.1.0.0")),
        ("UNMODELLED_APP_LOCAL", str(APP / "libvk_swiftshader.so")),
    }
    observed_nonruntime_exceptions = {
        (row["category"], row["path"])
        for row in exception_paths
        if row["category"]
        not in {"BROAD_FARM", "ROOTFS_PROVIDER", "OTHER_UNMODELLED"}
    }
    if observed_nonruntime_exceptions != expected_exception_set:
        fail(stage, f"unexpected CPU map exception set: {sorted(observed_nonruntime_exceptions)}")
    if classification_counts["BROAD_FARM"] != 0:
        fail(stage, "broad-farm mapping observed")
    if classification_counts["ROOTFS_PROVIDER"] != 0:
        fail(stage, "rootfs-provider mapping observed")
    if classification_counts["OTHER_UNMODELLED"] != 0:
        fail(stage, "unexpected unmodelled absolute mapping observed")
    if any("/current/" in path or path.endswith("/current") for path in actual_paths):
        fail(stage, "current path observed in maps")

    relevant_identity_paths = {
        str(PREFIX / "glibc/lib/libX11-xcb.so.1.0.0"),
        str(APP / "libvk_swiftshader.so"),
    }
    semantic_hash = {row["path"]: row["sha256"] for row in semantic_rows}
    for path_text in sorted(relevant_identity_paths):
        path = Path(path_text)
        expected_hash = semantic_hash.get(path_text, "UNMODELLED")
        observed_hash = sha256(path) if path.is_file() and not path.is_symlink() else "MISSING"
        state_value = (
            "MATCH"
            if expected_hash != "UNMODELLED" and observed_hash == expected_hash
            else "CAPTURED_UNMODELLED_IDENTITY"
            if expected_hash == "UNMODELLED" and observed_hash != "MISSING"
            else "FAIL"
        )
        live_identity_rows.append(
            {
                "role": "CPU_MAP_EXCEPTION",
                "path": path_text,
                "expected_sha256": expected_hash,
                "observed_sha256": observed_hash,
                "state": state_value,
            }
        )
        if state_value == "FAIL":
            fail(stage, f"CPU map exception identity failed: {path_text}")

    write_tsv(
        OUT / "live-identity-verification.tsv",
        ["role", "path", "expected_sha256", "observed_sha256", "state"],
        live_identity_rows,
    )

    process_counts = Counter(row["class"] for row in process_rows)
    content_kind_counts = Counter(row["content_kind"] for row in content_rows)
    summary_rows = [
        {"field": "branch", "value": branch},
        {"field": "head", "value": head},
        {"field": "phase_b1_root", "value": str(B1_OUT)},
        {"field": "phase_b2_root", "value": str(B2_OUT)},
        {"field": "phase_b9_root", "value": str(B9_OUT)},
        {"field": "passive_b10_root", "value": str(B10_OUT)},
        {"field": "generation_id", "value": b9_summary["generation_id"]},
        {"field": "passive_topology_status", "value": "PASS"},
        {"field": "passive_survival_status", "value": "PASS"},
        {"field": "maps_capture_status", "value": "PASS"},
        {"field": "main_processes", "value": process_counts["main"]},
        {"field": "renderer_processes", "value": process_counts["renderer"]},
        {"field": "zygote_processes", "value": process_counts["zygote"]},
        {"field": "gpu_processes", "value": process_counts["gpu"]},
        {"field": "unique_mapped_regular_objects", "value": len(actual_paths)},
        {"field": "selected_objects_total", "value": len(content_rows)},
        {"field": "selected_objects_mapped", "value": selected_state_counts["MAPPED_SELECTED_OBJECT"]},
        {"field": "selected_source_substitutes", "value": selected_state_counts["MAPPED_SOURCE_SUBSTITUTE"]},
        {"field": "selected_not_mapped", "value": selected_state_counts["NOT_MAPPED"]},
        {"field": "selected_elf_total", "value": content_kind_counts["COPIED_ELF"]},
        {"field": "selected_elf_mapped", "value": selected_kind_mapped["COPIED_ELF"]},
        {"field": "selected_font_total", "value": content_kind_counts["COPIED_FONT"]},
        {"field": "selected_font_mapped", "value": selected_kind_mapped["COPIED_FONT"]},
        {"field": "selected_schema_total", "value": content_kind_counts["GENERATED_GSETTINGS"]},
        {"field": "selected_schema_mapped", "value": selected_kind_mapped["GENERATED_GSETTINGS"]},
        {"field": "expected_app_local_mapped", "value": len(app_expected)},
        {"field": "expected_protected_world_mapped", "value": len(world_expected)},
        {"field": "absolute_rpath_selected_consumers", "value": len(rpath_rows)},
        {"field": "rpath_edges_to_source_substitutes", "value": len(rpath_edge_rows)},
        {"field": "excluded_semantic_mappings", "value": classification_counts["EXCLUDED_SEMANTIC_MAPPING"]},
        {"field": "unmodelled_app_local_mappings", "value": classification_counts["UNMODELLED_APP_LOCAL"]},
        {"field": "receipt_mutable_mappings", "value": classification_counts["RECEIPT_MUTABLE_STATE"]},
        {"field": "broad_farm_mappings", "value": classification_counts["BROAD_FARM"]},
        {"field": "rootfs_provider_mappings", "value": classification_counts["ROOTFS_PROVIDER"]},
        {"field": "current_pointer_changed", "value": "NO"},
        {"field": "generation_mutated", "value": "NO"},
        {"field": "runtime_launch_performed", "value": "NO"},
        {"field": "promoted_runtime_mutated", "value": "NO"},
    ]
    write_tsv(OUT / "summary.tsv", ["field", "value"], summary_rows)

    (OUT / "claim-boundary.txt").write_text(
        "This stage is a read-only diagnostic over the retained B1/B2 graph, the immutable B9 generation, and the passive B10 maps receipt.\n"
        "It proves passive topology, 100-second survival, and maps capture passed; identifies two selected ELF source substitutions, one demand-unmapped font, four selected absolute-RPATH consumers, six retained edges to the substituted providers, one excluded semantic mapping, and one unmodelled app-local mapping.\n"
        "It does not choose between world reclassification, deterministic RPATH transformation, or another loader contract; it does not launch Obsidian or mutate the generation.\n"
    )
    (OUT / "next-state.txt").write_text("READY_FOR_CPU_MAP_CONTRACT_REDESIGN\n")
    write_status("PASS")
    if (OUT / "failure-stage.txt").exists():
        (OUT / "failure-stage.txt").unlink()

    print("selected Obsidian passive map-selection diagnostic: PASS")
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
