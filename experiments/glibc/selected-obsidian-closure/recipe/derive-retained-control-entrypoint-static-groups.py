#!/usr/bin/env python3
from __future__ import annotations

import csv
import os
import shutil
import subprocess
import sys
import traceback
from collections import defaultdict, deque
from pathlib import Path

B3_OUT = Path(os.environ["B3_OUT"])
OUT = Path(
    os.environ.get(
        "OUT",
        "/tmp/selected-obsidian-phase-b4-entrypoint-static-capability-matrix",
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


def write_status(value: str) -> None:
    (OUT / "analysis.status").write_text(value + "\n")


def fail(stage_name: str, message: str, rc: int = 1) -> None:
    write_status("FAIL")
    (OUT / "failure-stage.txt").write_text(stage_name + "\n")
    print(message, file=sys.stderr)
    print(f"evidence: {OUT}", file=sys.stderr)
    raise SystemExit(rc)


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
            "tracked working-tree changes detected; Phase B4 requires exact HEAD",
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
    (OUT / "phase-b3-root.txt").write_text(str(B3_OUT) + "\n")

    required = [
        "analysis.status",
        "summary.tsv",
        "input/resolved-edges.tsv",
        "input/candidate-elf-partition.tsv",
        "entrypoint-direct-providers.tsv",
        "dynamic-root-candidates.tsv",
        "data-capability-summary.tsv",
    ]

    verify_rows: list[dict[str, object]] = []
    missing: list[str] = []
    stage = "input_verification"
    for name in required:
        source = B3_OUT / name
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
        fail(stage, f"missing Phase B3 inputs: {', '.join(missing)}")

    if (B3_OUT / "analysis.status").read_text().strip() != "PASS":
        fail("phase_b3_status", "Phase B3 status is not PASS")

    b3_summary = {
        row["field"]: row["value"]
        for row in read_tsv(B3_OUT / "summary.tsv")
    }
    entrypoint = b3_summary.get("entrypoint", "")
    if not entrypoint:
        fail("phase_b3_summary", "Phase B3 summary has no entrypoint")

    partitions = read_tsv(B3_OUT / "input/candidate-elf-partition.tsv")
    edges = read_tsv(B3_OUT / "input/resolved-edges.tsv")
    direct = read_tsv(B3_OUT / "entrypoint-direct-providers.tsv")

    info = {row["path"]: row for row in partitions}
    adjacency: dict[str, list[str]] = defaultdict(list)
    for row in edges:
        adjacency[row["consumer_path"]].append(row["provider_path"])

    stage = "direct_root_validation"
    direct_paths = sorted(row["provider_path"] for row in direct)
    edge_direct_paths = sorted(
        row["provider_path"]
        for row in edges
        if row["consumer_path"] == entrypoint
    )
    if direct_paths != edge_direct_paths:
        fail(
            stage,
            "entrypoint-direct-providers.tsv does not match resolved entrypoint edges",
        )

    external_direct = [
        row
        for row in direct
        if row["semantic_class"]
        not in {"APP_LOCAL_ELF", "WORLD_SUBSTRATE_ELF"}
    ]

    root_rows: list[dict[str, object]] = []
    closure_rows: list[dict[str, object]] = []
    root_members: dict[str, set[str]] = {}
    root_packages: dict[str, set[str]] = {}

    stage = "root_closure_derivation"
    for root in external_direct:
        root_path = root["provider_path"]
        seen = {root_path}
        queue = deque([root_path])

        while queue:
            current = queue.popleft()
            for provider in adjacency.get(current, []):
                if provider not in seen:
                    seen.add(provider)
                    queue.append(provider)

        external_members = {
            path
            for path in seen
            if info[path]["semantic_class"]
            not in {"APP_LOCAL_ELF", "WORLD_SUBSTRATE_ELF"}
        }
        root_members[root_path] = external_members
        root_packages[root_path] = {
            info[path]["package"] for path in external_members
        }

        root_rows.append(
            {
                "needed": root["needed"],
                "root_semantic_class": root["semantic_class"],
                "root_package": root["package"],
                "root_version": root["version"],
                "root_path": root_path,
                "external_closure_count": len(external_members),
                "full_closure_count": len(seen),
                "external_package_count": len(root_packages[root_path]),
            }
        )

        for member in sorted(seen):
            member_info = info[member]
            if member == root_path:
                relation = "ROOT"
            elif member_info["semantic_class"] == "WORLD_SUBSTRATE_ELF":
                relation = "WORLD_SUPPORT"
            elif member_info["semantic_class"] == "APP_LOCAL_ELF":
                relation = "APP_LOCAL_SUPPORT"
            else:
                relation = "EXTERNAL_SUPPORT"

            closure_rows.append(
                {
                    "root_path": root_path,
                    "root_needed": root["needed"],
                    "root_package": root["package"],
                    "member_relation": relation,
                    "member_partition": member_info["partition"],
                    "member_semantic_class": member_info["semantic_class"],
                    "member_package": member_info["package"],
                    "member_version": member_info["version"],
                    "member_path": member,
                }
            )

    root_rows.sort(
        key=lambda row: (
            str(row["root_semantic_class"]),
            str(row["root_package"]),
            str(row["needed"]),
        )
    )
    closure_rows.sort(
        key=lambda row: (
            str(row["root_package"]),
            str(row["root_needed"]),
            str(row["member_relation"]),
            str(row["member_path"]),
        )
    )

    write_tsv(
        OUT / "external-direct-root-candidates.tsv",
        [
            "needed",
            "root_semantic_class",
            "root_package",
            "root_version",
            "root_path",
            "external_closure_count",
            "full_closure_count",
            "external_package_count",
        ],
        root_rows,
    )
    write_tsv(
        OUT / "external-direct-root-closure.tsv",
        [
            "root_path",
            "root_needed",
            "root_package",
            "member_relation",
            "member_partition",
            "member_semantic_class",
            "member_package",
            "member_version",
            "member_path",
        ],
        closure_rows,
    )

    package_rows: list[dict[str, object]] = []
    for root in root_rows:
        root_path = str(root["root_path"])
        for package in sorted(root_packages[root_path]):
            package_rows.append(
                {
                    "root_path": root_path,
                    "root_needed": root["needed"],
                    "root_package": root["root_package"],
                    "member_package": package,
                }
            )

    write_tsv(
        OUT / "external-direct-root-packages.tsv",
        ["root_path", "root_needed", "root_package", "member_package"],
        package_rows,
    )

    member_to_roots: dict[str, list[str]] = defaultdict(list)
    for root_path, members in root_members.items():
        for member in members:
            member_to_roots[member].append(root_path)

    shared_rows: list[dict[str, object]] = []
    for member, roots in member_to_roots.items():
        if len(roots) > 1:
            member_info = info[member]
            shared_rows.append(
                {
                    "member_path": member,
                    "member_semantic_class": member_info["semantic_class"],
                    "member_package": member_info["package"],
                    "root_count": len(roots),
                    "roots": ";".join(sorted(roots)),
                }
            )

    shared_rows.sort(
        key=lambda row: (
            -int(row["root_count"]),
            str(row["member_package"]),
            str(row["member_path"]),
        )
    )
    write_tsv(
        OUT / "shared-external-support.tsv",
        [
            "member_path",
            "member_semantic_class",
            "member_package",
            "root_count",
            "roots",
        ],
        shared_rows,
    )

    overlap_rows: list[dict[str, object]] = []
    for index, left in enumerate(root_rows):
        left_path = str(left["root_path"])
        for right in root_rows[index + 1 :]:
            right_path = str(right["root_path"])
            common = root_members[left_path] & root_members[right_path]
            if common:
                overlap_rows.append(
                    {
                        "left_needed": left["needed"],
                        "left_package": left["root_package"],
                        "right_needed": right["needed"],
                        "right_package": right["root_package"],
                        "shared_external_object_count": len(common),
                    }
                )

    overlap_rows.sort(
        key=lambda row: (
            -int(row["shared_external_object_count"]),
            str(row["left_package"]),
            str(row["right_package"]),
        )
    )
    write_tsv(
        OUT / "direct-root-overlap.tsv",
        [
            "left_needed",
            "left_package",
            "right_needed",
            "right_package",
            "shared_external_object_count",
        ],
        overlap_rows,
    )

    package_edge_set: set[tuple[str, str]] = set()
    for edge in edges:
        consumer = info[edge["consumer_path"]]
        provider = info[edge["provider_path"]]
        if consumer["semantic_class"] in {
            "APP_LOCAL_ELF",
            "WORLD_SUBSTRATE_ELF",
        }:
            continue
        if provider["semantic_class"] in {
            "APP_LOCAL_ELF",
            "WORLD_SUBSTRATE_ELF",
        }:
            continue
        if consumer["package"] != provider["package"]:
            package_edge_set.add(
                (consumer["package"], provider["package"])
            )

    package_edge_rows = [
        {
            "consumer_package": consumer,
            "provider_package": provider,
        }
        for consumer, provider in sorted(package_edge_set)
    ]
    write_tsv(
        OUT / "external-package-dependency-edges.tsv",
        ["consumer_package", "provider_package"],
        package_edge_rows,
    )

    semantic_counts: dict[str, int] = defaultdict(int)
    for row in direct:
        semantic_counts[row["semantic_class"]] += 1

    semantic_rows = [
        {
            "semantic_class": semantic_class,
            "direct_provider_count": count,
        }
        for semantic_class, count in sorted(semantic_counts.items())
    ]
    write_tsv(
        OUT / "entrypoint-direct-semantic-summary.tsv",
        ["semantic_class", "direct_provider_count"],
        semantic_rows,
    )

    package_group: dict[str, dict[str, object]] = defaultdict(
        lambda: {
            "direct_roots": 0,
            "members": set(),
            "packages": set(),
        }
    )
    for root in root_rows:
        root_path = str(root["root_path"])
        group = package_group[str(root["root_package"])]
        group["direct_roots"] = int(group["direct_roots"]) + 1
        group["members"].update(root_members[root_path])
        group["packages"].update(root_packages[root_path])

    package_group_rows: list[dict[str, object]] = []
    for package, group in package_group.items():
        package_group_rows.append(
            {
                "root_package": package,
                "direct_root_count": group["direct_roots"],
                "union_external_object_count": len(group["members"]),
                "union_external_package_count": len(group["packages"]),
            }
        )

    package_group_rows.sort(
        key=lambda row: (
            -int(row["union_external_object_count"]),
            str(row["root_package"]),
        )
    )
    write_tsv(
        OUT / "root-package-group-summary.tsv",
        [
            "root_package",
            "direct_root_count",
            "union_external_object_count",
            "union_external_package_count",
        ],
        package_group_rows,
    )

    summary_rows = [
        {"field": "branch", "value": branch},
        {"field": "head", "value": head},
        {"field": "phase_b3_root", "value": str(B3_OUT)},
        {
            "field": "phase_b3_head",
            "value": b3_summary.get("head", ""),
        },
        {"field": "entrypoint", "value": entrypoint},
        {
            "field": "entrypoint_direct_providers",
            "value": len(direct),
        },
        {
            "field": "external_direct_roots",
            "value": len(external_direct),
        },
        {
            "field": "app_local_direct_roots",
            "value": semantic_counts.get("APP_LOCAL_ELF", 0),
        },
        {
            "field": "world_direct_roots",
            "value": semantic_counts.get("WORLD_SUBSTRATE_ELF", 0),
        },
        {
            "field": "prefix_direct_roots",
            "value": semantic_counts.get("PROVIDER_PREFIX_ELF", 0),
        },
        {
            "field": "rootfs_direct_roots",
            "value": semantic_counts.get("PROVIDER_ROOTFS_ELF", 0),
        },
        {
            "field": "graphics_gbm_direct_roots",
            "value": semantic_counts.get("PROVIDER_GRAPHICS_GBM_ELF", 0),
        },
        {
            "field": "shared_external_support_objects",
            "value": len(shared_rows),
        },
        {
            "field": "direct_root_overlap_pairs",
            "value": len(overlap_rows),
        },
        {
            "field": "external_package_dependency_edges",
            "value": len(package_edge_rows),
        },
        {"field": "runtime_launch_performed", "value": "NO"},
        {"field": "promoted_runtime_mutated", "value": "NO"},
    ]
    write_tsv(OUT / "summary.tsv", ["field", "value"], summary_rows)

    (OUT / "claim-boundary.txt").write_text(
        "This is a read-only entrypoint-static direct-root closure and overlap analysis.\n"
        "A direct root is an external provider named directly by the Obsidian entrypoint.\n"
        "Closures are derived only from the captured resolved DT_NEEDED graph.\n"
        "Shared objects and package overlap are grouping inputs, not final capability ownership.\n"
        "The analysis does not include dynamic discovery roots as entrypoint-static roots.\n"
        "It does not prove candidate search-path selection, materialization, or workload equivalence.\n"
    )
    (OUT / "next-state.txt").write_text(
        "READY_FOR_STATIC_CAPABILITY_OWNERSHIP_DECISION\n"
    )
    write_status("PASS")
    if (OUT / "failure-stage.txt").exists():
        (OUT / "failure-stage.txt").unlink()

    print(
        "selected Obsidian Phase B4 entrypoint-static capability matrix: PASS"
    )
    print(f"evidence: {OUT}")

except SystemExit:
    raise
except Exception:
    write_status("FAIL")
    (OUT / "failure-stage.txt").write_text(stage + "\n")
    traceback.print_exc()
    print(f"evidence: {OUT}", file=sys.stderr)
    raise SystemExit(1)
