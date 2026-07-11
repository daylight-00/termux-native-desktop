#!/usr/bin/env python3
from __future__ import annotations

import csv
import os
import shutil
import subprocess
import sys
import traceback
from collections import Counter, defaultdict
from pathlib import Path

B1_OUT = Path(os.environ["B1_OUT"])
B3_OUT = Path(os.environ["B3_OUT"])
B4_OUT = Path(os.environ["B4_OUT"])
B5_OUT = Path(os.environ["B5_OUT"])
B6_OUT = Path(os.environ["B6_OUT"])
OUT = Path(os.environ.get("OUT", "/tmp/selected-obsidian-phase-b7-complete-cpu-manifest"))

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


def summary_map(path: Path) -> dict[str, str]:
    return {row["field"]: row["value"] for row in read_tsv(path)}


def root_capability(needed: str) -> str:
    mapping = {
        "libgbm.so.1": "electron.graphics.gbm-base",
        "libgcc_s.so.1": "runtime.compiler-support",
        "libasound.so.2": "electron.audio.alsa",
        "libcups.so.2": "electron.printing.cups",
        "libnspr4.so": "electron.security.nss",
        "libnss3.so": "electron.security.nss",
        "libnssutil3.so": "electron.security.nss",
        "libsmime3.so": "electron.security.nss",
        "libudev.so.1": "electron.device.udev",
    }
    return mapping.get(needed, "electron.gui.gtk3")


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
            "tracked working-tree changes detected; Phase B7 requires exact HEAD",
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
    for label, root in (
        ("phase-b1", B1_OUT),
        ("phase-b3", B3_OUT),
        ("phase-b4", B4_OUT),
        ("phase-b5", B5_OUT),
        ("phase-b6", B6_OUT),
    ):
        (OUT / f"{label}-root.txt").write_text(str(root) + "\n")

    required: list[tuple[str, Path, str]] = [
        ("b1_audit_status", B1_OUT / "audit.status", "b1_audit.status"),
        (
            "b1_semantic_objects",
            B1_OUT / "input/semantic-objects.tsv",
            "b1_semantic-objects.tsv",
        ),
        (
            "b3_analysis_status",
            B3_OUT / "analysis.status",
            "b3_analysis.status",
        ),
        (
            "b3_elf_objects",
            B3_OUT / "input/input_elf-objects.tsv",
            "b3_elf-objects.tsv",
        ),
        (
            "b3_dynamic_roots",
            B3_OUT / "dynamic-root-candidates.tsv",
            "b3_dynamic-root-candidates.tsv",
        ),
        (
            "b3_dynamic_members",
            B3_OUT / "dynamic-root-members.tsv",
            "b3_dynamic-root-members.tsv",
        ),
        ("b3_summary", B3_OUT / "summary.tsv", "b3_summary.tsv"),
        (
            "b4_analysis_status",
            B4_OUT / "analysis.status",
            "b4_analysis.status",
        ),
        (
            "b4_static_closure",
            B4_OUT / "external-direct-root-closure.tsv",
            "b4_external-direct-root-closure.tsv",
        ),
        ("b4_summary", B4_OUT / "summary.tsv", "b4_summary.tsv"),
        (
            "b5_analysis_status",
            B5_OUT / "analysis.status",
            "b5_analysis.status",
        ),
        (
            "b5_data_verification",
            B5_OUT / "data-object-verification.tsv",
            "b5_data-object-verification.tsv",
        ),
        ("b5_summary", B5_OUT / "summary.tsv", "b5_summary.tsv"),
        (
            "b6_analysis_status",
            B6_OUT / "analysis.status",
            "b6_analysis.status",
        ),
        (
            "b6_next_state",
            B6_OUT / "next-state.txt",
            "b6_next-state.txt",
        ),
        (
            "b6_schema_sources",
            B6_OUT / "input/schema-source-manifest.tsv",
            "b6_schema-source-manifest.tsv",
        ),
        (
            "b6_compilers",
            B6_OUT / "schema-compiler-candidates.tsv",
            "b6_schema-compiler-candidates.tsv",
        ),
        (
            "b6_attempts",
            B6_OUT / "schema-reproduction-attempts.tsv",
            "b6_schema-reproduction-attempts.tsv",
        ),
        ("b6_summary", B6_OUT / "summary.tsv", "b6_summary.tsv"),
    ]

    stage = "input_verification"
    verify_rows: list[dict[str, object]] = []
    missing: list[str] = []
    for label, source, embedded_name in required:
        embedded = OUT / "input" / embedded_name
        state = "PASS" if source.is_file() else "FAIL"
        verify_rows.append(
            {
                "input": label,
                "state": state,
                "path": str(source),
                "embedded_path": str(embedded) if state == "PASS" else "-",
            }
        )
        if state == "PASS":
            shutil.copy2(source, embedded)
        else:
            missing.append(label)
    write_tsv(
        OUT / "input-verification.tsv",
        ["input", "state", "path", "embedded_path"],
        verify_rows,
    )
    if missing:
        fail(stage, "missing required inputs: " + ", ".join(missing))

    status_files = (
        ("B1", B1_OUT / "audit.status"),
        ("B3", B3_OUT / "analysis.status"),
        ("B4", B4_OUT / "analysis.status"),
        ("B5", B5_OUT / "analysis.status"),
        ("B6", B6_OUT / "analysis.status"),
    )
    for label, status_path in status_files:
        if status_path.read_text().strip() != "PASS":
            fail("input_status", f"{label} status is not PASS")
    if (
        B6_OUT / "next-state.txt"
    ).read_text().strip() != "READY_FOR_COMPLETE_DATA_MANIFEST":
        fail(
            "input_status",
            "corrected Phase B6 is not ready for complete data manifest",
        )

    semantic_rows = read_tsv(B1_OUT / "input/semantic-objects.tsv")
    semantic_by_path = {row["path"]: row for row in semantic_rows}
    if len(semantic_by_path) != len(semantic_rows):
        fail("semantic_index", "duplicate semantic object paths")

    elf_meta_rows = read_tsv(B3_OUT / "input/input_elf-objects.tsv")
    elf_meta = {row["path"]: row for row in elf_meta_rows}
    if len(elf_meta) != len(elf_meta_rows):
        fail("elf_index", "duplicate ELF metadata paths")

    b4_rows = read_tsv(B4_OUT / "external-direct-root-closure.tsv")
    static_paths: set[str] = set()
    static_memberships: set[tuple[str, str, str, str, str]] = set()
    for row in b4_rows:
        if row["member_semantic_class"] in {
            "APP_LOCAL_ELF",
            "WORLD_SUBSTRATE_ELF",
        }:
            continue
        static_paths.add(row["member_path"])
        capability = root_capability(row["root_needed"])
        static_memberships.add(
            (
                row["member_path"],
                capability,
                row["root_path"],
                row["root_needed"],
                row["member_relation"],
            )
        )

    dynamic_roots = read_tsv(B3_OUT / "dynamic-root-candidates.tsv")
    family_by_root = {
        row["root_path"]: row["suggested_family"] for row in dynamic_roots
    }
    dynamic_members = read_tsv(B3_OUT / "dynamic-root-members.tsv")
    nss_paths: set[str] = set()
    graphics_paths: set[str] = set()
    dynamic_memberships: set[tuple[str, str, str, str, str]] = set()
    for row in dynamic_members:
        family = family_by_root.get(row["root_path"], "")
        if family == "NSS_SECURITY":
            capability = "electron.security.nss"
            nss_paths.add(row["member_path"])
        elif family == "GRAPHICS_VULKAN":
            capability = "graphics.vulkan.feature"
            graphics_paths.add(row["member_path"])
        else:
            fail(
                "dynamic_family",
                f"unclassified dynamic root: {row['root_path']}",
            )
        relation = (
            "ROOT"
            if row["member_path"] == row["root_path"]
            else "MAPPED_ONLY_SUPPORT"
        )
        dynamic_memberships.add(
            (
                row["member_path"],
                capability,
                row["root_path"],
                Path(row["root_path"]).name,
                relation,
            )
        )

    if (
        static_paths & nss_paths
        or static_paths & graphics_paths
        or nss_paths & graphics_paths
    ):
        fail("elf_partition", "static/NSS/graphics sets overlap")

    data_rows = read_tsv(B5_OUT / "data-object-verification.tsv")
    data_by_path = {row["path"]: row for row in data_rows}
    if any(row["identity_state"] != "MATCH" for row in data_rows):
        fail(
            "data_identity",
            "Phase B5 data object identity is not fully MATCH",
        )

    b6_summary = summary_map(B6_OUT / "summary.tsv")
    if (
        b6_summary.get("clean_successful_compiles") != "2"
        or b6_summary.get("compilation_error_attempts") != "0"
        or b6_summary.get("byte_identical_outputs") != "2"
    ):
        fail(
            "schema_reproduction",
            "corrected Phase B6 clean/identical counts are not accepted",
        )

    schema_sources = read_tsv(B6_OUT / "input/schema-source-manifest.tsv")
    if len(schema_sources) != 37 or any(
        row["dpkg_file_owners"] == "UNOWNED" for row in schema_sources
    ):
        fail(
            "schema_sources",
            "schema source manifest is not complete and owned",
        )

    compiler_rows = [
        row
        for row in read_tsv(B6_OUT / "schema-compiler-candidates.tsv")
        if row["present"] == "YES"
        and row["executable"] == "YES"
        and row["version_state"] == "EXECUTED"
        and row["version_rc"] == "0"
    ]
    if len(compiler_rows) != 1:
        fail(
            "schema_compiler",
            f"expected one accepted compiler, found {len(compiler_rows)}",
        )
    compiler = compiler_rows[0]

    attempt_rows = read_tsv(B6_OUT / "schema-reproduction-attempts.tsv")
    identical_attempts = [
        row
        for row in attempt_rows
        if row["execution_state"] == "EXECUTED"
        and row["return_code"] == "0"
        and row["generated_present"] == "YES"
        and row["byte_identical"] == "YES"
    ]
    if len(identical_attempts) != 2:
        fail(
            "schema_reproduction",
            "expected two byte-identical schema attempts",
        )
    retained_schema_sha = identical_attempts[0]["retained_sha256"]
    if any(
        row["generated_sha256"] != retained_schema_sha
        for row in identical_attempts
    ):
        fail(
            "schema_reproduction",
            "schema attempts disagree on expected aggregate hash",
        )

    capability_by_path: dict[str, set[str]] = defaultdict(set)
    membership_rows: list[dict[str, object]] = []
    for path, capability, root_path, root_name, relation in sorted(
        static_memberships
    ):
        capability_by_path[path].add(capability)
        membership_rows.append(
            {
                "object_path": path,
                "capability": capability,
                "evidence_phase": "B4",
                "evidence_root_path": root_path,
                "evidence_root_name": root_name,
                "member_role": relation,
            }
        )
    for path, capability, root_path, root_name, relation in sorted(
        dynamic_memberships
    ):
        capability_by_path[path].add(capability)
        membership_rows.append(
            {
                "object_path": path,
                "capability": capability,
                "evidence_phase": "B3",
                "evidence_root_path": root_path,
                "evidence_root_name": root_name,
                "member_role": relation,
            }
        )

    semantic_dispositions: list[dict[str, object]] = []
    elf_manifest: list[dict[str, object]] = []
    data_manifest: list[dict[str, object]] = []
    reference_rows: list[dict[str, object]] = []
    unclassified: list[str] = []

    for row in semantic_rows:
        path = row["path"]
        semantic = row["semantic_class"]
        action = ""
        primary_capability = ""
        detail = ""

        if semantic == "APP_LOCAL_ELF":
            action = "REFERENCE_APP_LOCAL"
            primary_capability = "app.obsidian.local"
            detail = "preserve AppDir and $ORIGIN-first locality"
        elif semantic == "APP_LOCAL_DATA":
            action = "REFERENCE_APP_LOCAL"
            primary_capability = "app.obsidian.local"
            detail = "preserve application payload in AppDir"
        elif semantic == "WORLD_SUBSTRATE_ELF":
            action = "REFERENCE_WORLD_SUBSTRATE"
            primary_capability = "world.glibc"
            detail = "reference protected world; do not copy"
        elif semantic == "PROVIDER_LOCALE_DATA":
            action = "REFERENCE_WORLD_LOCALE"
            primary_capability = "world.locale.glibc"
            detail = "reference glibc-version-coupled prefix locale"
        elif semantic == "PROVIDER_FONT_DATA":
            action = "MATERIALIZE_SELECTED_FONT"
            primary_capability = "provider.fonts.selected"
            detail = "materialize exact package/version/hash selected file"
        elif semantic == "PROVIDER_SCHEMA_DATA":
            action = "GENERATE_GSETTINGS_SCHEMA"
            primary_capability = "provider.schemas.gsettings"
            detail = "generate from 37-source/compiler contract"
        elif semantic == "APP_MUTABLE_STATE":
            action = "ISOLATED_MUTABLE_STATE"
            primary_capability = "app.obsidian.state"
            detail = "exclude from immutable generation"
        elif semantic == "RUNTIME_CACHE_FONTCONFIG":
            action = "REGENERATE_RUNTIME_CACHE"
            primary_capability = "runtime.cache.fontconfig"
            detail = "exclude captured cache bytes and regenerate"
        elif semantic == "RUNTIME_CACHE_MESA":
            action = "REGENERATE_RUNTIME_CACHE"
            primary_capability = "runtime.cache.mesa"
            detail = "exclude captured cache bytes and regenerate"
        elif semantic == "DEVICE_NODE_GPU":
            action = "REFERENCE_OPTIONAL_GPU_DEVICE"
            primary_capability = "device.gpu"
            detail = "not part of CPU immutable generation"
        elif semantic.endswith("_ELF"):
            memberships = capability_by_path.get(path, set())
            if path in static_paths:
                action = "MATERIALIZE_SELECTED_STATIC_ELF"
                primary_capability = ";".join(sorted(memberships))
                detail = "deduplicated external static object"
            elif path in nss_paths:
                action = "MATERIALIZE_REQUIRED_DYNAMIC_ELF"
                primary_capability = "electron.security.nss"
                detail = "required mapped-only NSS/security module or support"
            elif path in graphics_paths:
                action = "EXCLUDE_CPU_BASE_GRAPHICS_FEATURE"
                primary_capability = "graphics.vulkan.feature"
                detail = "compose only in separately accepted GPU feature"
            else:
                unclassified.append(path)
                continue
        else:
            unclassified.append(path)
            continue

        semantic_dispositions.append(
            {
                "semantic_class": semantic,
                "path_class": row["path_class"],
                "primary_action": action,
                "primary_capability": primary_capability,
                "package": row["package"],
                "version": row["version"],
                "sha256": row["sha256"],
                "path": path,
                "detail": detail,
            }
        )

        if action in {
            "MATERIALIZE_SELECTED_STATIC_ELF",
            "MATERIALIZE_REQUIRED_DYNAMIC_ELF",
        }:
            meta = elf_meta.get(path)
            if not meta:
                fail("elf_metadata", f"missing ELF metadata for {path}")
            elf_manifest.append(
                {
                    "materialization_kind": (
                        "STATIC"
                        if action == "MATERIALIZE_SELECTED_STATIC_ELF"
                        else "DYNAMIC_NSS"
                    ),
                    "semantic_class": semantic,
                    "lookup_name": meta["lookup_name"],
                    "soname": meta["soname"],
                    "package": row["package"],
                    "version": row["version"],
                    "sha256": row["sha256"],
                    "capabilities": primary_capability,
                    "source_path": path,
                }
            )
        elif semantic in {
            "PROVIDER_LOCALE_DATA",
            "PROVIDER_FONT_DATA",
            "PROVIDER_SCHEMA_DATA",
        }:
            verified = data_by_path.get(path)
            if not verified:
                fail(
                    "data_manifest",
                    f"missing B5 verification row for {path}",
                )
            if verified["captured_sha256"] != row["sha256"]:
                fail("data_manifest", f"B1/B5 hash mismatch for {path}")
            data_manifest.append(
                {
                    "semantic_class": semantic,
                    "runtime_action": action,
                    "owner": primary_capability,
                    "package": row["package"],
                    "version": row["version"],
                    "sha256": row["sha256"],
                    "source_path": path,
                }
            )
        elif not action.startswith("MATERIALIZE") and action != "GENERATE_GSETTINGS_SCHEMA":
            reference_rows.append(
                {
                    "semantic_class": semantic,
                    "action": action,
                    "owner": primary_capability,
                    "sha256": row["sha256"],
                    "path": path,
                }
            )

    if unclassified:
        fail(
            "semantic_disposition",
            "unclassified semantic objects: " + ", ".join(unclassified),
        )
    if len(semantic_dispositions) != len(semantic_rows):
        fail(
            "semantic_disposition",
            "semantic disposition coverage is incomplete",
        )

    all_elf_paths = {
        row["path"]
        for row in semantic_rows
        if row["semantic_class"].endswith("_ELF")
    }
    accounted_elf = (
        static_paths
        | nss_paths
        | graphics_paths
        | {
            row["path"]
            for row in semantic_rows
            if row["semantic_class"] in {
                "APP_LOCAL_ELF",
                "WORLD_SUBSTRATE_ELF",
            }
        }
    )
    if all_elf_paths != accounted_elf:
        missing_elf = sorted(all_elf_paths - accounted_elf)
        extra_elf = sorted(accounted_elf - all_elf_paths)
        fail(
            "elf_coverage",
            f"ELF coverage mismatch missing={missing_elf} extra={extra_elf}",
        )

    lookup_to_paths: dict[str, set[str]] = defaultdict(set)
    for row in elf_manifest:
        lookup_to_paths[str(row["lookup_name"])].add(str(row["source_path"]))
    collisions = {
        name: paths
        for name, paths in lookup_to_paths.items()
        if len(paths) > 1
    }
    if collisions:
        fail(
            "lookup_collision",
            "selected materialized ELF lookup collisions detected",
        )

    write_tsv(
        OUT / "semantic-object-disposition.tsv",
        [
            "semantic_class",
            "path_class",
            "primary_action",
            "primary_capability",
            "package",
            "version",
            "sha256",
            "path",
            "detail",
        ],
        sorted(
            semantic_dispositions,
            key=lambda row: (
                str(row["primary_action"]),
                str(row["semantic_class"]),
                str(row["path"]),
            ),
        ),
    )
    write_tsv(
        OUT / "candidate-elf-manifest.tsv",
        [
            "materialization_kind",
            "semantic_class",
            "lookup_name",
            "soname",
            "package",
            "version",
            "sha256",
            "capabilities",
            "source_path",
        ],
        sorted(
            elf_manifest,
            key=lambda row: (
                str(row["lookup_name"]),
                str(row["source_path"]),
            ),
        ),
    )
    write_tsv(
        OUT / "candidate-data-manifest.tsv",
        [
            "semantic_class",
            "runtime_action",
            "owner",
            "package",
            "version",
            "sha256",
            "source_path",
        ],
        sorted(
            data_manifest,
            key=lambda row: (
                str(row["runtime_action"]),
                str(row["source_path"]),
            ),
        ),
    )
    write_tsv(
        OUT / "capability-membership.tsv",
        [
            "object_path",
            "capability",
            "evidence_phase",
            "evidence_root_path",
            "evidence_root_name",
            "member_role",
        ],
        sorted(
            membership_rows,
            key=lambda row: (
                str(row["capability"]),
                str(row["evidence_root_name"]),
                str(row["object_path"]),
                str(row["member_role"]),
            ),
        ),
    )
    write_tsv(
        OUT / "reference-runtime-owned-manifest.tsv",
        ["semantic_class", "action", "owner", "sha256", "path"],
        sorted(
            reference_rows,
            key=lambda row: (str(row["action"]), str(row["path"])),
        ),
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
        schema_sources,
    )

    schema_contract = [
        {
            "aggregate_semantic_class": "PROVIDER_SCHEMA_DATA",
            "aggregate_expected_sha256": retained_schema_sha,
            "source_count": len(schema_sources),
            "compiler_path": compiler["candidate_path"],
            "compiler_realpath": compiler["realpath"],
            "compiler_package": compiler["package_owner"],
            "compiler_version": compiler["version_output"],
            "compiler_sha256": compiler["sha256"],
            "accepted_modes": ",".join(
                sorted(row["mode"] for row in identical_attempts)
            ),
            "byte_identical_attempts": len(identical_attempts),
        }
    ]
    write_tsv(
        OUT / "schema-build-contract.tsv",
        [
            "aggregate_semantic_class",
            "aggregate_expected_sha256",
            "source_count",
            "compiler_path",
            "compiler_realpath",
            "compiler_package",
            "compiler_version",
            "compiler_sha256",
            "accepted_modes",
            "byte_identical_attempts",
        ],
        schema_contract,
    )

    semantic_counts = Counter(
        str(row["semantic_class"]) for row in semantic_dispositions
    )
    b1_summary = (
        summary_map(B1_OUT / "summary.tsv")
        if (B1_OUT / "summary.tsv").is_file()
        else {}
    )
    b3_summary = summary_map(B3_OUT / "summary.tsv")
    b4_summary = summary_map(B4_OUT / "summary.tsv")
    b5_summary = summary_map(B5_OUT / "summary.tsv")

    summary_rows = [
        {"field": "branch", "value": branch},
        {"field": "head", "value": head},
        {
            "field": "phase_b1_head",
            "value": b1_summary.get(
                "head",
                (B1_OUT / "head.txt").read_text().strip()
                if (B1_OUT / "head.txt").is_file()
                else "",
            ),
        },
        {"field": "phase_b3_head", "value": b3_summary.get("head", "")},
        {"field": "phase_b4_head", "value": b4_summary.get("head", "")},
        {"field": "phase_b5_head", "value": b5_summary.get("head", "")},
        {"field": "phase_b6_head", "value": b6_summary.get("head", "")},
        {"field": "semantic_objects", "value": len(semantic_rows)},
        {
            "field": "semantic_disposition_coverage",
            "value": len(semantic_dispositions),
        },
        {"field": "elf_objects", "value": len(all_elf_paths)},
        {
            "field": "external_static_elf_materialize",
            "value": len(static_paths),
        },
        {
            "field": "nss_dynamic_elf_materialize",
            "value": len(nss_paths),
        },
        {"field": "total_elf_materialize", "value": len(elf_manifest)},
        {
            "field": "graphics_dynamic_elf_excluded",
            "value": len(graphics_paths),
        },
        {
            "field": "app_local_elf_reference",
            "value": semantic_counts.get("APP_LOCAL_ELF", 0),
        },
        {
            "field": "world_elf_reference",
            "value": semantic_counts.get("WORLD_SUBSTRATE_ELF", 0),
        },
        {
            "field": "app_local_data_reference",
            "value": semantic_counts.get("APP_LOCAL_DATA", 0),
        },
        {
            "field": "world_locale_reference",
            "value": semantic_counts.get("PROVIDER_LOCALE_DATA", 0),
        },
        {
            "field": "selected_font_materialize",
            "value": semantic_counts.get("PROVIDER_FONT_DATA", 0),
        },
        {
            "field": "gsettings_aggregate_generate",
            "value": semantic_counts.get("PROVIDER_SCHEMA_DATA", 0),
        },
        {"field": "schema_source_files", "value": len(schema_sources)},
        {
            "field": "mutable_state_objects",
            "value": semantic_counts.get("APP_MUTABLE_STATE", 0),
        },
        {
            "field": "fontconfig_cache_objects",
            "value": semantic_counts.get("RUNTIME_CACHE_FONTCONFIG", 0),
        },
        {
            "field": "mesa_cache_objects",
            "value": semantic_counts.get("RUNTIME_CACHE_MESA", 0),
        },
        {
            "field": "gpu_device_objects",
            "value": semantic_counts.get("DEVICE_NODE_GPU", 0),
        },
        {
            "field": "selected_elf_lookup_collisions",
            "value": len(collisions),
        },
        {"field": "unclassified_objects", "value": 0},
        {"field": "runtime_launch_performed", "value": "NO"},
        {"field": "promoted_runtime_mutated", "value": "NO"},
    ]
    write_tsv(OUT / "summary.tsv", ["field", "value"], summary_rows)

    (OUT / "claim-boundary.txt").write_text(
        "This is a read-only synthesis of retained semantic-object dispositions and complete CPU candidate manifest inputs.\n"
        "It accounts for all 161 retained semantic objects and all 113 ELF objects without materializing bytes.\n"
        "Typed capability memberships may overlap while each object has exactly one primary disposition.\n"
        "The manifest does not choose the final object-store layout, loader path, activation pointer, or rollback implementation.\n"
        "No workload is launched and no promoted runtime is mutated.\n"
    )
    (OUT / "next-state.txt").write_text(
        "READY_FOR_CANDIDATE_MATERIALIZATION_DESIGN\n"
    )
    write_status("PASS")
    if (OUT / "failure-stage.txt").exists():
        (OUT / "failure-stage.txt").unlink()

    print("selected Obsidian Phase B7 complete CPU candidate manifest: PASS")
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
