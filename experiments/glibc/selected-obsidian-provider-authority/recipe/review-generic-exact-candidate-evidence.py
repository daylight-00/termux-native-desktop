#!/usr/bin/env python3
"""Review generic exact-candidate collector output without promoting authority."""

from __future__ import annotations

import argparse
import csv
import hashlib
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

EXPECTED_RULE_ROWS = 61
ALLOWED_STATES = {
    "DIRECT_APT_AND_RECIPE_FAMILY_CANDIDATE",
    "DIRECT_APT_FAMILY_CANDIDATE",
    "DIRECT_RECIPE_FAMILY_CANDIDATE",
    "INDIRECT_TOKEN_ONLY",
    "NO_RETAINED_CANDIDATE",
}


def fail(message: str) -> "NoReturn":
    raise SystemExit(f"generic exact candidate receipt review: FAIL: {message}")


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


def package_root(name: str) -> str:
    value = name.strip().lower()
    value = re.sub(r":.*$", "", value)
    for suffix in ("-glibc-static", "-glibc-dev", "-glibc", "-static", "-dev"):
        if value.endswith(suffix):
            return value[: -len(suffix)]
    return value


def split_roots(value: str) -> set[str]:
    return {item.strip().lower() for item in value.split(";") if item.strip() and item.strip() != "-"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--evidence-dir", required=True, type=Path)
    parser.add_argument("--rules", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()

    rules = read_tsv(args.rules)
    if len(rules) != EXPECTED_RULE_ROWS:
        fail(f"rule denominator is {len(rules)}, expected {EXPECTED_RULE_ROWS}")

    required_rule_fields = {
        "evidence_row_id",
        "capability_partition",
        "identity_label",
        "direct_family_roots",
        "review_policy",
        "authority_state",
    }
    if not required_rule_fields.issubset(rules[0]):
        fail("rule schema is incomplete")

    ids = [row["evidence_row_id"] for row in rules]
    if len(ids) != len(set(ids)):
        fail("duplicate evidence_row_id in rules")
    if any(row["review_policy"] != "FAMILY_NAME_MATCH_ONLY_NOT_AUTHORITY" for row in rules):
        fail("review policy drift")
    if any(row["authority_state"] != "CANDIDATE_ONLY" for row in rules):
        fail("authority state drift")

    apt_path = args.evidence_dir / "apt-candidate-records.tsv"
    recipe_path = args.evidence_dir / "recipe-candidate-records.tsv"
    apt_rows = read_tsv(apt_path)
    recipe_rows = read_tsv(recipe_path)

    allowed_ids = set(ids)
    if any(row.get("evidence_row_id", "") not in allowed_ids for row in apt_rows + recipe_rows):
        fail("candidate input contains an unknown evidence_row_id")

    apt_by_id: dict[str, list[dict[str, str]]] = defaultdict(list)
    recipe_by_id: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in apt_rows:
        apt_by_id[row["evidence_row_id"]].append(row)
    for row in recipe_rows:
        recipe_by_id[row["evidence_row_id"]].append(row)

    output: list[dict[str, str]] = []
    counts: Counter[str] = Counter()
    for rule in rules:
        evidence_id = rule["evidence_row_id"]
        roots = split_roots(rule["direct_family_roots"])
        direct_apt = sorted(
            {
                row.get("candidate_package", "")
                for row in apt_by_id[evidence_id]
                if package_root(row.get("candidate_package", "")) in roots
            }
        )
        direct_recipe = sorted(
            {
                row.get("candidate_package", "")
                for row in recipe_by_id[evidence_id]
                if row.get("candidate_package", "").lower() in roots
                or Path(row.get("recipe_root", "")).name.lower() in roots
            }
        )
        apt_count = len(apt_by_id[evidence_id])
        recipe_count = len(recipe_by_id[evidence_id])

        if direct_apt and direct_recipe:
            state = "DIRECT_APT_AND_RECIPE_FAMILY_CANDIDATE"
        elif direct_apt:
            state = "DIRECT_APT_FAMILY_CANDIDATE"
        elif direct_recipe:
            state = "DIRECT_RECIPE_FAMILY_CANDIDATE"
        elif apt_count or recipe_count:
            state = "INDIRECT_TOKEN_ONLY"
        else:
            state = "NO_RETAINED_CANDIDATE"
        if state not in ALLOWED_STATES:
            fail(f"internal invalid state: {state}")
        counts[state] += 1

        output.append(
            {
                "evidence_row_id": evidence_id,
                "capability_partition": rule["capability_partition"],
                "identity_label": rule["identity_label"],
                "direct_family_roots": rule["direct_family_roots"],
                "direct_apt_packages": ";".join(direct_apt) if direct_apt else "-",
                "direct_recipe_packages": ";".join(direct_recipe) if direct_recipe else "-",
                "indirect_apt_candidate_rows": str(apt_count - len(direct_apt)),
                "indirect_recipe_candidate_rows": str(recipe_count - len(direct_recipe)),
                "review_state": state,
                "artifact_member_binding_state": "OPEN_NO_DEB_EXTRACTION",
                "final_provider_state": "UNRESOLVED",
                "target_population_state": "BLOCKED",
            }
        )

    review_path = args.out / "generic-exact-candidate-receipt-review.tsv"
    write_tsv(
        review_path,
        [
            "evidence_row_id",
            "capability_partition",
            "identity_label",
            "direct_family_roots",
            "direct_apt_packages",
            "direct_recipe_packages",
            "indirect_apt_candidate_rows",
            "indirect_recipe_candidate_rows",
            "review_state",
            "artifact_member_binding_state",
            "final_provider_state",
            "target_population_state",
        ],
        output,
    )

    summary_rows = [
        {"field": "review_identity_rows", "value": str(len(output))},
        {"field": "direct_apt_and_recipe_family_candidates", "value": str(counts["DIRECT_APT_AND_RECIPE_FAMILY_CANDIDATE"])},
        {"field": "direct_apt_family_candidates", "value": str(counts["DIRECT_APT_FAMILY_CANDIDATE"])},
        {"field": "direct_recipe_family_candidates", "value": str(counts["DIRECT_RECIPE_FAMILY_CANDIDATE"])},
        {"field": "indirect_token_only", "value": str(counts["INDIRECT_TOKEN_ONLY"])},
        {"field": "no_retained_candidate", "value": str(counts["NO_RETAINED_CANDIDATE"])},
        {"field": "authority_decisions_accepted", "value": "0"},
        {"field": "deb_extraction_performed", "value": "NO"},
        {"field": "target_rows_populated", "value": "0"},
        {"field": "review_sha256", "value": sha256(review_path)},
    ]
    write_tsv(args.out / "review-summary.tsv", ["field", "value"], summary_rows)
    (args.out / "claim-boundary.txt").write_text(
        "Direct family-name matches rank retained apt artifact identities and pinned recipe roots for later object/member comparison.\n"
        "They do not prove that an artifact contains the named object and do not accept adaptation, necessity, final provider authority, composition or target population.\n",
        encoding="utf-8",
    )
    (args.out / "review.status").write_text("PASS\n", encoding="utf-8")
    print("generic exact candidate receipt review: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
