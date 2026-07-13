#!/usr/bin/env python3
"""Review a bounded generic artifact member-inventory receipt without promoting authority."""

from __future__ import annotations

import argparse
import csv
import hashlib
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import NoReturn

EXPECTED_IDENTITIES = 37
EXPECTED_EDGES = 44
ALLOWED_STATES = {
    "EXACT_CONCRETE_MEMBER_AND_EXPECTED_SONAME_OBSERVED",
    "EXPECTED_SONAME_ALIAS_SYMLINK_PRESENT_CONCRETE_FILENAME_DRIFT",
    "EXPECTED_SONAME_ALIAS_NOT_OBSERVED_DIFFERENT_FAMILY_MEMBERS_PRESENT",
}


def fail(message: str) -> NoReturn:
    raise SystemExit(f"generic artifact member inventory receipt review: FAIL: {message}")


def read_tsv(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        fail(f"missing input: {path}")
    with path.open("r", encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream, delimiter="\t")
        if not reader.fieldnames:
            fail(f"missing TSV header: {path}")
        return [{key: (value or "") for key, value in row.items()} for row in reader]


def write_tsv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def split_values(value: str) -> list[str]:
    if not value or value == "-":
        return []
    return [item for item in value.split(";") if item and item != "-"]


def valid_sha256(value: str) -> bool:
    return bool(re.fullmatch(r"[0-9a-f]{64}", value))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rules", required=True, type=Path)
    parser.add_argument("--named-observations", required=True, type=Path)
    parser.add_argument("--data-inventory", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--expected-identities", type=int, default=EXPECTED_IDENTITIES)
    parser.add_argument("--expected-edges", type=int, default=EXPECTED_EDGES)
    args = parser.parse_args()

    rules = read_tsv(args.rules)
    observations = read_tsv(args.named_observations)
    inventory = read_tsv(args.data_inventory)

    if len(rules) != args.expected_identities:
        fail(f"rule denominator is {len(rules)}, expected {args.expected_identities}")
    if len(observations) != args.expected_edges:
        fail(f"observation denominator is {len(observations)}, expected {args.expected_edges}")

    required_rule_fields = {
        "evidence_row_id",
        "capability_partition",
        "identity_label",
        "expected_soname_alias",
        "family_member_prefix",
        "review_policy",
        "authority_state",
    }
    if not required_rule_fields.issubset(rules[0]):
        fail("rule schema is incomplete")
    ids = [row["evidence_row_id"] for row in rules]
    if len(ids) != len(set(ids)):
        fail("duplicate evidence_row_id in rules")
    if any(row["review_policy"] != "EXACT_OR_ALIAS_EVIDENCE_ONLY_NOT_AUTHORITY" for row in rules):
        fail("review policy drift")
    if any(row["authority_state"] != "CANDIDATE_ONLY" for row in rules):
        fail("rule authority state drift")

    required_observation_fields = {
        "evidence_row_id",
        "capability_partition",
        "identity_label",
        "artifact_id",
        "package",
        "exact_basename_match_count",
        "observed_member_paths",
        "observed_member_types",
        "observed_elf_sonames",
        "observed_member_sha256s",
        "elf_observation_states",
        "object_member_binding_state",
        "artifact_to_recipe_binding_state",
        "termux_android_adaptation_state",
        "final_provider_state",
        "target_population_state",
    }
    if not required_observation_fields.issubset(observations[0]):
        fail("named observation schema is incomplete")

    rule_by_id = {row["evidence_row_id"]: row for row in rules}
    allowed_ids = set(rule_by_id)
    if {row["evidence_row_id"] for row in observations} != allowed_ids:
        fail("observation identity set differs from rules")
    for row in observations:
        rule = rule_by_id[row["evidence_row_id"]]
        if row["capability_partition"] != rule["capability_partition"] or row["identity_label"] != rule["identity_label"]:
            fail(f"identity metadata drift: {row['evidence_row_id']}")
        if row["object_member_binding_state"] != "OBSERVED_CANDIDATE_NOT_AUTHORITY_ACCEPTED":
            fail("input observation promoted object/member authority")
        if row["artifact_to_recipe_binding_state"] != "OPEN" or row["termux_android_adaptation_state"] != "OPEN":
            fail("input observation promoted source/adaptation authority")
        if row["final_provider_state"] != "UNRESOLVED" or row["target_population_state"] != "BLOCKED":
            fail("input observation promoted final authority or target population")

    required_inventory_fields = {
        "artifact_id",
        "package",
        "member_path",
        "basename",
        "member_type",
        "link_target",
    }
    if not inventory or not required_inventory_fields.issubset(inventory[0]):
        fail("data inventory schema is incomplete")

    observations_by_id: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in observations:
        observations_by_id[row["evidence_row_id"]].append(row)
    inventory_by_artifact: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in inventory:
        inventory_by_artifact[row["artifact_id"]].append(row)

    output: list[dict[str, str]] = []
    counts: Counter[str] = Counter()
    for rule in rules:
        evidence_id = rule["evidence_row_id"]
        edges = observations_by_id[evidence_id]
        artifact_ids = sorted({row["artifact_id"] for row in edges})
        packages = sorted({row["package"] for row in edges})
        exact_edges = [row for row in edges if int(row["exact_basename_match_count"]) > 0]

        exact_artifact = exact_path = exact_hash = exact_soname = "-"
        alias_artifact = alias_path = alias_target = alias_target_path = "-"
        family_basenames = "-"

        if exact_edges:
            if len(exact_edges) != 1 or int(exact_edges[0]["exact_basename_match_count"]) != 1:
                fail(f"exact member is not unique for {evidence_id}")
            edge = exact_edges[0]
            paths = split_values(edge["observed_member_paths"])
            types = split_values(edge["observed_member_types"])
            sonames = split_values(edge["observed_elf_sonames"])
            hashes = split_values(edge["observed_member_sha256s"])
            states = split_values(edge["elf_observation_states"])
            if len(paths) != 1 or types != ["REGULAR"] or len(hashes) != 1 or not valid_sha256(hashes[0]):
                fail(f"exact regular-member evidence is incomplete for {evidence_id}")
            if sonames != [rule["expected_soname_alias"]] or states != ["ELF_SONAME_PARSED"]:
                fail(f"exact member SONAME does not match expected alias for {evidence_id}")
            state = "EXACT_CONCRETE_MEMBER_AND_EXPECTED_SONAME_OBSERVED"
            evidence_state = "EXACT_MEMBER_AND_SONAME_OBSERVED_CANDIDATE_ONLY"
            exact_artifact = edge["artifact_id"]
            exact_path = paths[0]
            exact_hash = hashes[0]
            exact_soname = sonames[0]
        else:
            alias_rows: list[dict[str, str]] = []
            family_rows: list[dict[str, str]] = []
            for artifact_id in artifact_ids:
                for item in inventory_by_artifact.get(artifact_id, []):
                    if item["basename"] == rule["expected_soname_alias"]:
                        alias_rows.append(item)
                    if item["basename"].startswith(rule["family_member_prefix"]):
                        family_rows.append(item)
            if alias_rows:
                if len(alias_rows) != 1 or alias_rows[0]["member_type"] != "SYMLINK" or alias_rows[0]["link_target"] in {"", "-"}:
                    fail(f"expected SONAME alias evidence is not one symlink for {evidence_id}")
                alias = alias_rows[0]
                target_rows = [
                    item
                    for item in inventory_by_artifact.get(alias["artifact_id"], [])
                    if item["basename"] == alias["link_target"] and item["member_type"] == "REGULAR"
                ]
                if len(target_rows) != 1:
                    fail(f"alias target regular member is not unique for {evidence_id}")
                state = "EXPECTED_SONAME_ALIAS_SYMLINK_PRESENT_CONCRETE_FILENAME_DRIFT"
                evidence_state = "EXPECTED_SONAME_ALIAS_PRESENT_TARGET_ELF_NOT_REVIEWED"
                alias_artifact = alias["artifact_id"]
                alias_path = alias["member_path"]
                alias_target = alias["link_target"]
                alias_target_path = target_rows[0]["member_path"]
                family_basenames = ";".join(sorted({item["basename"] for item in family_rows}))
            else:
                if not family_rows:
                    fail(f"no family member evidence exists for alias-absent row {evidence_id}")
                state = "EXPECTED_SONAME_ALIAS_NOT_OBSERVED_DIFFERENT_FAMILY_MEMBERS_PRESENT"
                evidence_state = "EXPECTED_SONAME_ALIAS_ABSENT"
                family_basenames = ";".join(sorted({item["basename"] for item in family_rows}))

        if state not in ALLOWED_STATES:
            fail(f"internal invalid state: {state}")
        counts[state] += 1
        output.append(
            {
                "evidence_row_id": evidence_id,
                "capability_partition": rule["capability_partition"],
                "identity_label": rule["identity_label"],
                "expected_soname_alias": rule["expected_soname_alias"],
                "candidate_artifact_ids": ";".join(artifact_ids),
                "candidate_packages": ";".join(packages),
                "exact_artifact_id": exact_artifact,
                "exact_member_path": exact_path,
                "exact_member_sha256": exact_hash,
                "exact_observed_elf_soname": exact_soname,
                "alias_artifact_id": alias_artifact,
                "alias_member_path": alias_path,
                "alias_link_target": alias_target,
                "alias_target_member_path": alias_target_path,
                "family_observed_basenames": family_basenames,
                "review_state": state,
                "object_member_evidence_state": evidence_state,
                "artifact_to_recipe_binding_state": "OPEN",
                "termux_android_adaptation_state": "OPEN",
                "final_provider_state": "UNRESOLVED",
                "target_population_state": "BLOCKED",
            }
        )

    review_path = args.out / "generic-artifact-member-inventory-receipt-review.tsv"
    fields = list(output[0])
    write_tsv(review_path, fields, output)
    summary = [
        {"field": "review_identity_rows", "value": str(len(output))},
        {"field": "exact_concrete_member_and_expected_soname_observed", "value": str(counts["EXACT_CONCRETE_MEMBER_AND_EXPECTED_SONAME_OBSERVED"])},
        {"field": "expected_soname_alias_symlink_present_concrete_filename_drift", "value": str(counts["EXPECTED_SONAME_ALIAS_SYMLINK_PRESENT_CONCRETE_FILENAME_DRIFT"])},
        {"field": "expected_soname_alias_not_observed", "value": str(counts["EXPECTED_SONAME_ALIAS_NOT_OBSERVED_DIFFERENT_FAMILY_MEMBERS_PRESENT"])},
        {"field": "authority_decisions_accepted", "value": "0"},
        {"field": "target_rows_populated", "value": "0"},
        {"field": "review_sha256", "value": sha256(review_path)},
    ]
    write_tsv(args.out / "review-summary.tsv", ["field", "value"], summary)
    (args.out / "claim-boundary.txt").write_text(
        "Exact concrete member and ELF SONAME observations are candidate object/member evidence only.\n"
        "A SONAME-named symlink does not prove the ELF SONAME of its different concrete target.\n"
        "No row accepts artifact-to-recipe binding, Termux/Android adaptation, necessity, final provider authority, composition or target population.\n",
        encoding="utf-8",
    )
    (args.out / "review.status").write_text("PASS\n", encoding="utf-8")
    print("generic artifact member inventory receipt review: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
