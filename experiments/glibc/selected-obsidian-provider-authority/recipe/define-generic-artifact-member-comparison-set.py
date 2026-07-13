#!/usr/bin/env python3
"""Define a bounded exact-artifact/member-inventory comparison set.

This tool is intentionally non-networking and non-extracting. It reads a
previously collected apt candidate receipt plus the canonical reviewed receipt,
then selects only exact indexed dynamic/split-runtime artifact candidates for
the 37 direct-family identities. Static-only and architecture-independent
Mesa development artifacts are recorded as exclusions rather than silently
ignored.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
from collections import defaultdict
from pathlib import Path
from typing import Iterable

DIRECT_STATE = "DIRECT_APT_AND_RECIPE_FAMILY_CANDIDATE"
IN_SCOPE_CLASS = "DYNAMIC_OR_SPLIT_RUNTIME_CANDIDATE"
IN_SCOPE_STATE = "NAMED_DOWNLOAD_ONLY_MEMBER_INVENTORY_SCOPE"
STATIC_EXCLUSION = "STATIC_ONLY_PACKAGE_OUTSIDE_DYNAMIC_MEMBER_SEARCH"
DEV_EXCLUSION = "ARCH_ALL_DEVELOPMENT_PACKAGE_OUTSIDE_AARCH64_ELF_MEMBER_SEARCH"
EDGE_STATE = "NAMED_MEMBER_SEARCH_CANDIDATE_ONLY"
OPEN_MEMBER_STATE = "OPEN_NO_DEB_DOWNLOAD_OR_EXTRACTION"
UNRESOLVED = "UNRESOLVED"
BLOCKED = "BLOCKED"

EXPECTED_DIRECT_IDENTITIES = 37
EXPECTED_INCLUDED_ARTIFACTS = 34
EXPECTED_INCLUDED_EDGES = 44
EXPECTED_EXCLUDED_ARTIFACTS = 15
EXPECTED_TOTAL_BYTES = 51_771_348
EXPECTED_INDEX_SHA256 = "565df3058a51a200fd83e851cce2d99a2faa2277142c50adc20f071d6c7b4a3a"
EXPECTED_REPOSITORY_METADATA_ID = "repository-metadata:01"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def write_tsv(path: Path, fieldnames: list[str], rows: Iterable[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def split_set(value: str) -> set[str]:
    return {item for item in value.split(";") if item and item != "-"}


def artifact_id(artifact_sha256: str) -> str:
    return f"generic-artifact:{artifact_sha256[:20]}"


def package_class(package: str, architecture: str) -> tuple[str, str]:
    if package.endswith("-glibc-static"):
        return "EXCLUDED", STATIC_EXCLUSION
    if package == "mesa-dev-glibc" and architecture == "all":
        return "EXCLUDED", DEV_EXCLUSION
    return "IN_SCOPE", IN_SCOPE_CLASS


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--evidence-dir", type=Path, required=True)
    parser.add_argument("--review", type=Path, required=True)
    parser.add_argument("--repository-metadata", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    apt_path = args.evidence_dir / "apt-candidate-records.tsv"
    review_rows = read_tsv(args.review)
    apt_rows = read_tsv(apt_path)
    repository_rows = read_tsv(args.repository_metadata)

    if len(repository_rows) != 1:
        raise ValueError("repository metadata registry must contain exactly one row")
    repository = repository_rows[0]
    if repository.get("repository_metadata_id") != EXPECTED_REPOSITORY_METADATA_ID:
        raise ValueError("unexpected repository metadata identity")
    if repository.get("packages_index_sha256") != EXPECTED_INDEX_SHA256:
        raise ValueError("repository Packages index hash drift")
    if repository.get("target_population_state") != BLOCKED:
        raise ValueError("repository metadata target state is not BLOCKED")

    direct_rows = {
        row["evidence_row_id"]: row
        for row in review_rows
        if row.get("review_state") == DIRECT_STATE
    }
    if len(direct_rows) != EXPECTED_DIRECT_IDENTITIES:
        raise ValueError(f"direct identity denominator drift: {len(direct_rows)}")

    exact_edges: dict[tuple[str, str], dict[str, str]] = {}
    artifact_records: dict[tuple[str, str, str, str, str, str], dict[str, str]] = {}
    for row in apt_rows:
        evidence_row_id = row.get("evidence_row_id", "")
        direct = direct_rows.get(evidence_row_id)
        if not direct:
            continue
        if row.get("candidate_package") not in split_set(direct.get("direct_apt_packages", "")):
            continue
        if row.get("index_sha256") != EXPECTED_INDEX_SHA256:
            raise ValueError(f"direct artifact came from an unexpected Packages index: {row.get('candidate_package')}")
        if row.get("candidate_state") != "EXACT_INDEX_ARTIFACT_IDENTITY_CANDIDATE":
            raise ValueError("direct apt record is not exact indexed artifact identity")
        if row.get("object_member_binding_state") != "OPEN_NO_DEB_EXTRACTION":
            raise ValueError("direct apt record unexpectedly contains member binding")
        if row.get("authority_state") != "CANDIDATE_ONLY":
            raise ValueError("direct apt record unexpectedly accepts authority")
        key = (
            row["candidate_package"],
            row["candidate_version"],
            row["architecture"],
            row["repository_filename"],
            row["artifact_size"],
            row["artifact_sha256"],
        )
        artifact_records[key] = row
        exact_edges[(evidence_row_id, row["candidate_package"])] = row

    included_artifacts: dict[str, dict[str, object]] = {}
    excluded_artifacts: dict[str, dict[str, object]] = {}
    included_edges: list[dict[str, object]] = []
    affected_exclusions: defaultdict[str, set[str]] = defaultdict(set)

    for (evidence_row_id, package), apt in sorted(exact_edges.items()):
        direct = direct_rows[evidence_row_id]
        state, classification = package_class(package, apt["architecture"])
        aid = artifact_id(apt["artifact_sha256"])
        common = {
            "artifact_id": aid,
            "repository_metadata_id": EXPECTED_REPOSITORY_METADATA_ID,
            "package": package,
            "version": apt["candidate_version"],
            "architecture": apt["architecture"],
            "repository_filename": apt["repository_filename"],
            "artifact_size": apt["artifact_size"],
            "artifact_sha256": apt["artifact_sha256"],
            "packages_index_sha256": apt["index_sha256"],
        }
        if state == "EXCLUDED":
            affected_exclusions[aid].add(evidence_row_id)
            excluded_artifacts[aid] = {
                **common,
                "exclusion_reason": classification,
                "comparison_scope_state": "EXCLUDED_FROM_DOWNLOAD_SET_RETAINED_AS_NEGATIVE_PACKAGE_CLASS_EVIDENCE",
                "object_member_binding_state": OPEN_MEMBER_STATE,
                "authority_state": UNRESOLVED,
                "target_population_state": BLOCKED,
            }
            continue

        included_artifacts[aid] = {
            **common,
            "artifact_class": classification,
            "comparison_scope_state": IN_SCOPE_STATE,
            "download_state": "NOT_DOWNLOADED_CONTRACT_ONLY",
            "member_inventory_state": "OPEN",
            "authority_state": UNRESOLVED,
            "target_population_state": BLOCKED,
        }
        included_edges.append({
            "evidence_row_id": evidence_row_id,
            "capability_partition": direct["capability_partition"],
            "identity_label": direct["identity_label"],
            "artifact_id": aid,
            "package": package,
            "version": apt["candidate_version"],
            "architecture": apt["architecture"],
            "expected_member_basename": direct["identity_label"],
            "direct_recipe_packages": direct["direct_recipe_packages"],
            "comparison_edge_state": EDGE_STATE,
            "member_match_state": "OPEN",
            "artifact_to_recipe_binding_state": "OPEN",
            "termux_android_adaptation_state": "OPEN",
            "final_provider_state": UNRESOLVED,
            "target_population_state": BLOCKED,
        })

    if len(included_artifacts) != EXPECTED_INCLUDED_ARTIFACTS:
        raise ValueError(f"included artifact count drift: {len(included_artifacts)}")
    if len(included_edges) != EXPECTED_INCLUDED_EDGES:
        raise ValueError(f"included edge count drift: {len(included_edges)}")
    if len(excluded_artifacts) != EXPECTED_EXCLUDED_ARTIFACTS:
        raise ValueError(f"excluded artifact count drift: {len(excluded_artifacts)}")
    included_identity_ids = {row["evidence_row_id"] for row in included_edges}
    if included_identity_ids != set(direct_rows):
        missing = sorted(set(direct_rows) - included_identity_ids)
        raise ValueError(f"direct identity lost all in-scope artifact edges: {missing}")
    total_bytes = sum(int(row["artifact_size"]) for row in included_artifacts.values())
    if total_bytes != EXPECTED_TOTAL_BYTES:
        raise ValueError(f"included compressed byte total drift: {total_bytes}")

    exclusion_rows = []
    for aid, row in sorted(excluded_artifacts.items(), key=lambda item: (str(item[1]["package"]), item[0])):
        exclusion_rows.append({
            **row,
            "affected_identity_rows": len(affected_exclusions[aid]),
            "affected_evidence_row_ids": ";".join(sorted(affected_exclusions[aid])),
        })

    out = args.out
    out.mkdir(parents=True, exist_ok=False)
    artifact_fields = [
        "artifact_id", "repository_metadata_id", "package", "version", "architecture",
        "repository_filename", "artifact_size", "artifact_sha256", "packages_index_sha256",
        "artifact_class", "comparison_scope_state", "download_state", "member_inventory_state",
        "authority_state", "target_population_state",
    ]
    edge_fields = [
        "evidence_row_id", "capability_partition", "identity_label", "artifact_id", "package",
        "version", "architecture", "expected_member_basename", "direct_recipe_packages",
        "comparison_edge_state", "member_match_state", "artifact_to_recipe_binding_state",
        "termux_android_adaptation_state", "final_provider_state", "target_population_state",
    ]
    exclusion_fields = [
        "artifact_id", "repository_metadata_id", "package", "version", "architecture",
        "repository_filename", "artifact_size", "artifact_sha256", "packages_index_sha256",
        "exclusion_reason", "affected_identity_rows", "affected_evidence_row_ids",
        "comparison_scope_state", "object_member_binding_state", "authority_state",
        "target_population_state",
    ]

    artifacts_path = out / "generic-artifact-member-comparison-artifacts.tsv"
    edges_path = out / "generic-artifact-member-comparison-edges.tsv"
    exclusions_path = out / "generic-artifact-member-comparison-exclusions.tsv"
    write_tsv(artifacts_path, artifact_fields, sorted(included_artifacts.values(), key=lambda row: (str(row["package"]), str(row["version"]))))
    write_tsv(edges_path, edge_fields, sorted(included_edges, key=lambda row: (str(row["evidence_row_id"]), str(row["package"]))))
    write_tsv(exclusions_path, exclusion_fields, exclusion_rows)

    metadata_rows = [
        {"field": "source_evidence_apt_candidates_sha256", "value": sha256(apt_path)},
        {"field": "reviewed_receipt_sha256", "value": sha256(args.review)},
        {"field": "repository_metadata_registry_sha256", "value": sha256(args.repository_metadata)},
        {"field": "repository_metadata_id", "value": EXPECTED_REPOSITORY_METADATA_ID},
        {"field": "repository_base_uri", "value": repository["repository_base_uri"]},
        {"field": "packages_index_sha256", "value": EXPECTED_INDEX_SHA256},
        {"field": "direct_identity_rows", "value": EXPECTED_DIRECT_IDENTITIES},
        {"field": "download_scope_artifacts", "value": EXPECTED_INCLUDED_ARTIFACTS},
        {"field": "download_scope_edges", "value": EXPECTED_INCLUDED_EDGES},
        {"field": "download_scope_compressed_bytes", "value": EXPECTED_TOTAL_BYTES},
        {"field": "excluded_static_or_dev_artifacts", "value": EXPECTED_EXCLUDED_ARTIFACTS},
        {"field": "artifact_set_sha256", "value": sha256(artifacts_path)},
        {"field": "edge_set_sha256", "value": sha256(edges_path)},
        {"field": "exclusion_set_sha256", "value": sha256(exclusions_path)},
        {"field": "network_download_performed", "value": "NO"},
        {"field": "deb_extraction_performed", "value": "NO"},
        {"field": "authority_decisions_accepted", "value": 0},
        {"field": "target_rows_populated", "value": 0},
        {"field": "next_state", "value": "IMPLEMENT_BOUNDED_GENERIC_ARTIFACT_MEMBER_INVENTORY_COLLECTOR"},
    ]
    write_tsv(out / "generic-artifact-member-comparison-metadata.tsv", ["field", "value"], metadata_rows)
    (out / "definition.status").write_text("PASS\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
