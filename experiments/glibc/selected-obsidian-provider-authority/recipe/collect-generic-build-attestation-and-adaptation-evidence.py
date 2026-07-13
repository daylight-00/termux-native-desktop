#!/usr/bin/env python3
"""Collect bounded local evidence for the generic build/adaptation review set.

This collector deliberately separates locally observable evidence from external
build provenance, semantic review, policy decisions, and authority acceptance.
It does not build, install, extract, promote, or populate any runtime target.
"""
from __future__ import annotations

import csv
import hashlib
import os
import re
import stat
import subprocess
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable, NoReturn

PROJECT_REPO = Path(os.environ["PROJECT_REPO"]).resolve()
OUT = Path(os.environ["OUT"]).resolve()
BASE = PROJECT_REPO / "experiments/glibc/selected-obsidian-provider-authority"
REVIEW = BASE / "review"
REQUIREMENTS = Path(os.environ.get("GENERIC_EVIDENCE_REQUIREMENTS", REVIEW / "generic-build-attestation-adaptation-review-requirements.tsv")).resolve()
ROOT_SET = Path(os.environ.get("GENERIC_EVIDENCE_ROOT_SET", REVIEW / "generic-build-attestation-adaptation-root-review-set.tsv")).resolve()
OBJECT_SET = Path(os.environ.get("GENERIC_EVIDENCE_OBJECT_SET", REVIEW / "generic-build-attestation-adaptation-object-review-set.tsv")).resolve()
MEMBER_RECEIPT = Path(os.environ.get("GENERIC_MEMBER_RECEIPT_REVIEW", REVIEW / "generic-artifact-member-inventory-receipt-review.tsv")).resolve()
RECIPE_RECEIPT = Path(os.environ.get("GENERIC_RECIPE_RECEIPT_REVIEW", REVIEW / "generic-recipe-binding-and-drift-target-receipt-review.tsv")).resolve()
FOUNDATION = Path(os.environ["GENERIC_EVIDENCE_FOUNDATION_OUT"]).resolve()
SOURCE_REPO = Path(os.environ.get("GENERIC_SOURCE_REPO", BASE / "work/source/termux-pacman-glibc-packages")).resolve()
EXPECTED_REQUIREMENTS = int(os.environ.get("GENERIC_EVIDENCE_EXPECTED_REQUIREMENTS", "16"))
EXPECTED_ROOTS = int(os.environ.get("GENERIC_EVIDENCE_EXPECTED_ROOTS", "28"))
EXPECTED_OBJECTS = int(os.environ.get("GENERIC_EVIDENCE_EXPECTED_OBJECTS", "37"))
EXPECTED_EXACT = int(os.environ.get("GENERIC_EVIDENCE_EXPECTED_EXACT", "21"))
EXPECTED_DRIFT = int(os.environ.get("GENERIC_EVIDENCE_EXPECTED_DRIFT", "15"))
EXPECTED_BLOCKED = int(os.environ.get("GENERIC_EVIDENCE_EXPECTED_BLOCKED", "1"))
NEXT_STATE = "REVIEW_BOUNDED_GENERIC_BUILD_ATTESTATION_AND_ADAPTATION_EVIDENCE_RECEIPT"

SIGNAL_PATTERNS = [
    ("TERMUX_PREFIX_REFERENCE", re.compile(r"TERMUX_PREFIX|\$PREFIX|\$\{PREFIX\}")),
    ("EXTRA_CONFIGURE_ARGS", re.compile(r"TERMUX_PKG_EXTRA_CONFIGURE_ARGS|meson|cmake|configure")),
    ("CUSTOM_BUILD_STEP", re.compile(r"termux_step_|make\b|ninja\b|autoreconf|patch\b|sed\b|perl\b|python\b")),
    ("PACKAGE_LAYOUT_OR_HOOK", re.compile(r"TERMUX_PKG_BUILD_IN_SRC|TERMUX_PKG_RM_AFTER_INSTALL|postinst|prerm|ldconfig")),
    ("SUBPACKAGE_DECLARATION", re.compile(r"_subpackage|TERMUX_SUBPKG|subpackage")),
    ("ANDROID_PLATFORM_REFERENCE", re.compile(r"ANDROID|__ANDROID__|bionic|aarch64-linux-android")),
]


def fail(message: str) -> NoReturn:
    raise SystemExit(f"generic build attestation and adaptation evidence collector: FAIL: {message}")


def read_tsv(path: Path) -> list[dict[str, str]]:
    if not path.is_file() or path.is_symlink():
        fail(f"missing regular input: {path}")
    with path.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream, delimiter="\t")
        if not reader.fieldnames:
            fail(f"missing header: {path}")
        return [{key: value or "" for key, value in row.items()} for row in reader]


def write_tsv(path: Path, fields: list[str], rows: Iterable[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, delimiter="\t", lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def bytes_sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def directory_manifest(root: Path) -> str:
    digest = hashlib.sha256()
    if not root.is_dir() or root.is_symlink():
        return "MISSING_OR_UNSAFE"
    for path in sorted(root.rglob("*"), key=lambda item: str(item.relative_to(root))):
        rel = str(path.relative_to(root))
        info = path.lstat()
        if stat.S_ISREG(info.st_mode):
            kind, payload = "FILE", sha256(path)
        elif stat.S_ISDIR(info.st_mode):
            kind, payload = "DIR", "-"
        elif stat.S_ISLNK(info.st_mode):
            kind, payload = "SYMLINK", os.readlink(path)
        else:
            kind, payload = "SPECIAL", f"mode={info.st_mode:o}"
        digest.update(f"{rel}\0{kind}\0{info.st_mode:o}\0{info.st_size}\0{payload}\0".encode(errors="surrogateescape"))
    return digest.hexdigest()


def git(args: list[str], *, text: bool = True, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=SOURCE_REPO, text=text, check=check, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def split_set(value: str) -> set[str]:
    return {item for item in value.split(";") if item and item != "NONE"}


def classify_recipe_file(path: str) -> str:
    name = Path(path).name
    if name == "build.sh":
        return "BUILD_SCRIPT"
    if name.endswith((".patch", ".diff")):
        return "PATCH"
    if "subpackage" in name or name.endswith(".subpackage.sh"):
        return "SUBPACKAGE_SCRIPT"
    if name in {"postinst", "prerm", "postrm", "preinst"} or "hook" in name:
        return "PACKAGE_HOOK"
    return "OTHER_RECIPE_FILE"


def requirement_state(requirement_id: str, counts: dict[str, int]) -> tuple[str, str, str]:
    table = {
        "BA-001": ("EXTERNAL_BUILD_PROVENANCE_REQUIRED", "NONE", "Exact artifact digest is observed, but no digest-bound producing build invocation is present in bounded local inputs."),
        "BA-002": ("EXTERNAL_BUILD_ENVIRONMENT_RECORD_REQUIRED", "NONE", "Current host state is not evidence of the producing build environment."),
        "BA-003": ("LOCAL_OUTPUT_BINDING_EVIDENCE_COLLECTED_BUILD_LINK_OPEN", "artifact-member-output-evidence.tsv", f"{counts['output_rows']} artifact/object output rows are digest-bound locally but not tied to a producing build record."),
        "BA-004": ("EXTERNAL_INDEPENDENT_VERIFICATION_REQUIRED", "NONE", "No independent reproduction or independently verifiable provenance is present."),
        "BA-005": ("ATTESTATION_CONTINUITY_POLICY_REQUIRED", "NONE", "Successor and rollback provenance continuity is not defined."),
        "AD-001": ("LOCAL_COMPLETE_RECIPE_FILE_AND_SIGNAL_INVENTORY_COLLECTED_REVIEW_REQUIRED", "recipe-file-evidence.tsv;recipe-build-script-signal-evidence.tsv", f"{counts['recipe_files']} recipe files and {counts['signal_rows']} bounded script signals were recorded without semantic acceptance."),
        "AD-002": ("LOCAL_UPSTREAM_DECLARATIONS_COLLECTED_SEMANTIC_COMPARISON_REQUIRED", "root-evidence-observations.tsv", "Pinned upstream URL/hash declarations are recorded; upstream semantic comparison is not performed."),
        "AD-003": ("ADAPTATION_NECESSITY_CLASSIFICATION_REQUIRED", "recipe-build-script-signal-evidence.tsv", "Syntactic signals are evidence inventory only and do not classify necessity."),
        "AD-004": ("LOCAL_ROOT_OBJECT_CROSSWALK_COLLECTED_IMPACT_REVIEW_REQUIRED", "root-object-impact-crosswalk.tsv", f"{counts['object_rows']} object links are recorded; semantic object impact is not accepted."),
        "AD-005": ("ADAPTATION_UPDATE_ROLLBACK_POLICY_REQUIRED", "NONE", "Update and rollback implications are not defined."),
        "AD-006": ("LOCAL_FULL_RECIPE_MANIFEST_COLLECTED_NO_TOKEN_SEMANTIC_REVIEW_REQUIRED", "recipe-file-evidence.tsv", "Full pinned recipe manifests are recorded; absence of a token is not upstream equivalence."),
        "CF-001": ("CONSUMER_BINDING_EVIDENCE_REQUIRED", "NONE", "Provider SONAME evidence does not show how consumers bind."),
        "CF-002": ("LOCAL_EXACT_ALIAS_TARGET_EVIDENCE_COLLECTED_REVIEW_REQUIRED", "artifact-member-output-evidence.tsv", f"{counts['drift_rows']} current alias-to-target rows are artifact/member digest and SONAME bound."),
        "CF-003": ("SUCCESSOR_FILENAME_DRIFT_POLICY_REQUIRED", "NONE", "No successor concrete-target acceptance policy is defined."),
        "CF-004": ("ROLLBACK_FILENAME_DRIFT_POLICY_REQUIRED", "NONE", "No rollback concrete-target policy is defined."),
        "OJ-001": ("OBJECT_REQUIREMENT_CORRECTION_REQUIRED", "artifact-member-output-evidence.tsv", f"{counts['blocked_rows']} object requirement remains unsatisfied; a different ABI family is not substituted."),
    }
    if requirement_id not in table:
        fail(f"unknown requirement id: {requirement_id}")
    return table[requirement_id]


def main() -> None:
    if OUT.exists() or OUT.is_symlink():
        fail(f"refusing existing output: {OUT}")
    OUT.mkdir(parents=True)

    requirements = read_tsv(REQUIREMENTS)
    roots = read_tsv(ROOT_SET)
    objects = read_tsv(OBJECT_SET)
    member_rows = read_tsv(MEMBER_RECEIPT)
    recipe_rows = read_tsv(RECIPE_RECEIPT)
    foundation_source = read_tsv(FOUNDATION / "source-repository-state.tsv")
    foundation_recipe_files = read_tsv(FOUNDATION / "recipe-file-inventory.tsv")
    foundation_artifacts = read_tsv(FOUNDATION / "artifact-verification.tsv")
    foundation_drift = read_tsv(FOUNDATION / "drift-target-elf-review.tsv")
    foundation_binding = read_tsv(FOUNDATION / "recipe-binding-review.tsv")
    foundation_summary = {row["field"]: row["value"] for row in read_tsv(FOUNDATION / "summary.tsv")}

    if len(requirements) != EXPECTED_REQUIREMENTS or len(roots) != EXPECTED_ROOTS or len(objects) != EXPECTED_OBJECTS:
        fail(f"denominator mismatch requirements/roots/objects={len(requirements)}/{len(roots)}/{len(objects)}")
    if len(foundation_source) != 1 or len(foundation_binding) != EXPECTED_OBJECTS:
        fail("foundation source or binding denominator mismatch")
    if len(foundation_drift) != EXPECTED_DRIFT:
        fail(f"foundation drift denominator mismatch: {len(foundation_drift)}")
    if foundation_summary.get("artifact_to_recipe_bindings_accepted") != "0":
        fail("foundation unexpectedly accepts artifact-to-recipe bindings")

    source = foundation_source[0]
    source_head, source_tree = source["head"], source["tree"]
    if git(["rev-parse", "HEAD"]).stdout.strip() != source_head or git(["rev-parse", "HEAD^{tree}"]).stdout.strip() != source_tree:
        fail("source checkout differs from foundation pin")
    if git(["status", "--porcelain", "--untracked-files=all"]).stdout:
        fail("source checkout is not clean")
    source_before = directory_manifest(SOURCE_REPO)

    root_by_path = {row["recipe_root"]: row for row in roots}
    object_by_evidence = {row["evidence_row_id"]: row for row in objects}
    member_by_evidence = {row["evidence_row_id"]: row for row in member_rows}
    recipe_by_evidence = {row["evidence_row_id"]: row for row in recipe_rows}
    drift_by_evidence = {row["evidence_row_id"]: row for row in foundation_drift}
    binding_by_evidence = {row["evidence_row_id"]: row for row in foundation_binding}
    if set(object_by_evidence) != set(member_by_evidence) or set(object_by_evidence) != set(recipe_by_evidence) or set(object_by_evidence) != set(binding_by_evidence):
        fail("object/receipt/foundation evidence row sets differ")

    # Verify every pinned root tree and collect complete file evidence directly from Git objects.
    recipe_file_rows: list[dict[str, object]] = []
    signal_rows: list[dict[str, object]] = []
    root_file_counts: Counter[str] = Counter()
    root_signal_counts: Counter[str] = Counter()
    for recipe_root, root_row in sorted(root_by_path.items()):
        observed_tree = git(["rev-parse", f"{source_head}:{recipe_root}"], check=False).stdout.strip()
        if observed_tree != root_row["recipe_tree"]:
            fail(f"recipe tree mismatch for {recipe_root}: {observed_tree}")
        listing = git(["ls-tree", "-r", "-l", source_head, "--", recipe_root]).stdout
        if not listing.strip():
            fail(f"empty recipe root: {recipe_root}")
        for raw in listing.splitlines():
            meta, path = raw.split("\t", 1)
            mode, kind, oid, _size = meta.split(None, 3)
            if kind != "blob":
                fail(f"non-blob recipe entry: {path}")
            payload = git(["show", f"{source_head}:{path}"], text=False).stdout
            file_class = classify_recipe_file(path)
            recipe_file_rows.append({
                "recipe_root": recipe_root, "recipe_tree": observed_tree, "path": path,
                "mode": mode, "blob_oid": oid, "size": len(payload), "content_sha256": bytes_sha256(payload),
                "file_class": file_class, "semantic_review_state": "NOT_PERFORMED_EVIDENCE_INVENTORY_ONLY",
            })
            root_file_counts[recipe_root] += 1
            if Path(path).name == "build.sh":
                text = payload.decode("utf-8", errors="replace")
                for line_number, line in enumerate(text.splitlines(), 1):
                    stripped = line.strip()
                    if not stripped or stripped.startswith("#"):
                        continue
                    classes = sorted({name for name, pattern in SIGNAL_PATTERNS if pattern.search(stripped)})
                    if not classes:
                        continue
                    signal_rows.append({
                        "recipe_root": recipe_root, "recipe_tree": observed_tree, "path": path,
                        "line_number": line_number, "signal_classes": ";".join(classes),
                        "line_sha256": bytes_sha256(stripped.encode()), "line_text": stripped,
                        "semantic_classification_state": "UNCLASSIFIED_SYNTACTIC_SIGNAL_ONLY",
                    })
                    root_signal_counts[recipe_root] += 1

    foundation_recipe_map = {(row["recipe_root"], row["path"]): row for row in foundation_recipe_files}
    for row in recipe_file_rows:
        key = (str(row["recipe_root"]), str(row["path"]))
        other = foundation_recipe_map.get(key)
        if not other or other["blob_oid"] != row["blob_oid"] or other["content_sha256"] != row["content_sha256"]:
            fail(f"recipe file evidence differs from foundation: {key}")
    if len(recipe_file_rows) != len(foundation_recipe_files):
        fail("recipe file inventory denominator differs from foundation")

    # Bind artifact and member observations, without claiming a producing build.
    artifact_ids = {row["artifact_id"] for row in foundation_artifacts}
    output_rows: list[dict[str, object]] = []
    exact_count = drift_count = blocked_count = 0
    for evidence_id, obj in sorted(object_by_evidence.items()):
        member = member_by_evidence[evidence_id]
        recipe = recipe_by_evidence[evidence_id]
        if obj["artifact_id"] not in artifact_ids:
            fail(f"object artifact not foundation verified: {obj['artifact_id']}")
        state = obj["object_member_review_state"]
        if state == "EXACT_MEMBER_EXPECTED_SONAME_CANDIDATE_CONFIRMED":
            exact_count += 1
            member_path = member["exact_member_path"]
            member_sha = member["exact_member_sha256"]
            soname = member["exact_observed_elf_soname"]
            alias_path = alias_target = "-"
            evidence_state = "EXACT_MEMBER_DIGEST_AND_SONAME_OBSERVED_NOT_BUILD_ATTESTED"
        elif state == "DRIFT_TARGET_ELF_EXPECTED_SONAME_CANDIDATE_CONFIRMED":
            drift_count += 1
            drift = drift_by_evidence.get(evidence_id)
            if not drift:
                fail(f"missing foundation drift row: {evidence_id}")
            member_path = drift["target_member_path"]
            member_sha = drift["target_member_sha256"]
            soname = drift["observed_soname"]
            alias_path = drift["alias_member_path"]
            alias_target = member["alias_link_target"]
            evidence_state = "ALIAS_TARGET_MEMBER_DIGEST_AND_SONAME_OBSERVED_NOT_BUILD_ATTESTED"
        elif state == "EXPECTED_SONAME_ALIAS_ABSENT_CORRECT_CANDIDATE_REQUIRED":
            blocked_count += 1
            member_path = member_sha = soname = alias_path = alias_target = "-"
            evidence_state = "OBJECT_REQUIREMENT_UNSATISFIED_NO_OUTPUT_BINDING"
        else:
            fail(f"unexpected object member state: {state}")
        output_rows.append({
            "object_review_id": obj["object_review_id"], "evidence_row_id": evidence_id,
            "identity_label": obj["identity_label"], "artifact_id": obj["artifact_id"],
            "artifact_package": obj["artifact_package"], "artifact_version": obj["artifact_version"],
            "artifact_sha256": obj["artifact_sha256"], "recipe_root": obj["recipe_root"],
            "recipe_tree": obj["recipe_tree"], "member_path": member_path, "member_sha256": member_sha,
            "observed_soname": soname, "alias_member_path": alias_path, "alias_link_target": alias_target,
            "output_binding_evidence_state": evidence_state,
            "producing_build_binding_state": "OPEN_NO_DIGEST_BOUND_BUILD_RECORD",
            "authority_state": "OPEN_NO_ACCEPTANCE", "target_population_state": "UNPOPULATED",
        })
    if (exact_count, drift_count, blocked_count) != (EXPECTED_EXACT, EXPECTED_DRIFT, EXPECTED_BLOCKED):
        fail(f"object class mismatch exact/drift/blocked={exact_count}/{drift_count}/{blocked_count}")

    objects_by_root: dict[str, list[dict[str, str]]] = defaultdict(list)
    for obj in objects:
        objects_by_root[obj["recipe_root"]].append(obj)
    crosswalk_rows: list[dict[str, object]] = []
    root_observations: list[dict[str, object]] = []
    for recipe_root, root in sorted(root_by_path.items()):
        members = sorted(objects_by_root[recipe_root], key=lambda row: row["identity_label"])
        for obj in members:
            crosswalk_rows.append({
                "root_review_id": root["root_review_id"], "object_review_id": obj["object_review_id"],
                "evidence_row_id": obj["evidence_row_id"], "recipe_root": recipe_root,
                "identity_label": obj["identity_label"], "artifact_id": obj["artifact_id"],
                "adaptation_evidence_tokens": obj["adaptation_evidence_tokens"],
                "adaptation_requirement_set": obj["adaptation_requirement_set"],
                "object_impact_evidence_state": "ROOT_OBJECT_CROSSWALK_COLLECTED_SEMANTIC_IMPACT_REVIEW_OPEN",
                "authority_state": "OPEN_NO_ACCEPTANCE",
            })
        sample = recipe_by_evidence[members[0]["evidence_row_id"]]
        root_observations.append({
            "root_review_id": root["root_review_id"], "review_tier": root["review_tier"],
            "recipe_root": recipe_root, "recipe_tree": root["recipe_tree"],
            "recipe_resolved_full_version": root["recipe_resolved_full_version"],
            "recipe_source_url_raw": sample["recipe_source_url_raw"], "recipe_source_sha256": sample["recipe_source_sha256"],
            "recipe_file_count": root_file_counts[recipe_root], "build_script_signal_count": root_signal_counts[recipe_root],
            "artifact_count": root["artifact_count"], "identity_count": root["identity_count"],
            "adaptation_evidence_tokens": root["adaptation_evidence_tokens"],
            "build_provenance_collection_state": "EXTERNAL_DIGEST_BOUND_BUILD_RECORD_REQUIRED",
            "recipe_inventory_collection_state": "COMPLETE_PINNED_RECIPE_FILE_INVENTORY_COLLECTED",
            "upstream_semantic_comparison_state": "NOT_PERFORMED_REQUIRES_BOUNDED_SEMANTIC_REVIEW",
            "adaptation_classification_state": "OPEN_NO_NECESSITY_CLASSIFICATION",
            "update_rollback_state": "OPEN_NO_CONTINUITY_POLICY",
            "authority_state": "OPEN_NO_ACCEPTANCE",
        })

    counts = {
        "output_rows": len(output_rows), "drift_rows": drift_count, "blocked_rows": blocked_count,
        "recipe_files": len(recipe_file_rows), "signal_rows": len(signal_rows), "object_rows": len(objects),
    }
    requirement_rows: list[dict[str, object]] = []
    for req in requirements:
        collection_state, refs, note = requirement_state(req["requirement_id"], counts)
        requirement_rows.append({
            **req, "collection_state": collection_state, "evidence_references": refs,
            "collection_note": note, "review_state": "EVIDENCE_COLLECTED_OR_GAP_RECORDED_REVIEW_REQUIRED",
            "authority_state": "OPEN_NO_ACCEPTANCE",
        })

    external_gap_rows = [
        {
            "requirement_id": row["requirement_id"], "dimension": row["dimension"], "scope": row["scope"],
            "collection_state": row["collection_state"], "gap": row["collection_note"],
            "next_action": "PROVIDE_BOUNDED_EVIDENCE_FOR_SEPARATE_RECEIPT_REVIEW",
        }
        for row in requirement_rows
        if not row["collection_state"].startswith("LOCAL_")
    ]

    source_after = directory_manifest(SOURCE_REPO)
    if source_before != source_after:
        fail("pinned source checkout mutated during evidence collection")

    write_tsv(OUT / "input-verification.tsv", ["input", "path", "sha256_or_state", "verification_state"], [
        {"input": "requirements", "path": REQUIREMENTS, "sha256_or_state": sha256(REQUIREMENTS), "verification_state": "PASS"},
        {"input": "root_review_set", "path": ROOT_SET, "sha256_or_state": sha256(ROOT_SET), "verification_state": "PASS"},
        {"input": "object_review_set", "path": OBJECT_SET, "sha256_or_state": sha256(OBJECT_SET), "verification_state": "PASS"},
        {"input": "member_receipt_review", "path": MEMBER_RECEIPT, "sha256_or_state": sha256(MEMBER_RECEIPT), "verification_state": "PASS"},
        {"input": "recipe_receipt_review", "path": RECIPE_RECEIPT, "sha256_or_state": sha256(RECIPE_RECEIPT), "verification_state": "PASS"},
        {"input": "foundation_summary", "path": FOUNDATION / "summary.tsv", "sha256_or_state": sha256(FOUNDATION / "summary.tsv"), "verification_state": "PASS"},
        {"input": "source_checkout", "path": SOURCE_REPO, "sha256_or_state": source_before, "verification_state": "PINNED_CLEAN_IMMUTABLE_PASS"},
    ])
    write_tsv(OUT / "requirement-evidence-status.tsv", [
        "requirement_id", "dimension", "scope", "requirement", "acceptable_evidence", "blocking_or_insufficient_evidence",
        "authority_effect", "collection_state", "evidence_references", "collection_note", "review_state", "authority_state",
    ], requirement_rows)
    write_tsv(OUT / "root-evidence-observations.tsv", list(root_observations[0]), root_observations)
    write_tsv(OUT / "recipe-file-evidence.tsv", list(recipe_file_rows[0]), recipe_file_rows)
    write_tsv(OUT / "recipe-build-script-signal-evidence.tsv", [
        "recipe_root", "recipe_tree", "path", "line_number", "signal_classes", "line_sha256", "line_text", "semantic_classification_state",
    ], signal_rows)
    write_tsv(OUT / "root-object-impact-crosswalk.tsv", list(crosswalk_rows[0]), crosswalk_rows)
    write_tsv(OUT / "artifact-member-output-evidence.tsv", list(output_rows[0]), output_rows)
    write_tsv(OUT / "external-evidence-gaps.tsv", ["requirement_id", "dimension", "scope", "collection_state", "gap", "next_action"], external_gap_rows)

    local_rows = sum(row["collection_state"].startswith("LOCAL_") for row in requirement_rows)
    summary = [
        ("requirements", len(requirement_rows)), ("root_work_units", len(root_observations)),
        ("object_work_units", len(output_rows)), ("verified_foundation_artifacts", len(foundation_artifacts)),
        ("recipe_files_collected", len(recipe_file_rows)), ("build_script_signal_rows", len(signal_rows)),
        ("exact_output_rows", exact_count), ("drift_output_rows", drift_count),
        ("blocked_object_rows", blocked_count), ("local_evidence_or_partial_evidence_requirement_rows", local_rows),
        ("external_semantic_policy_or_correction_gap_rows", len(external_gap_rows)),
        ("artifact_build_attestations_accepted", 0), ("termux_android_adaptations_accepted", 0),
        ("concrete_filename_drifts_accepted", 0), ("final_provider_decisions_accepted", 0),
        ("target_rows_populated", 0), ("package_operations_performed", 0),
        ("maintainer_scripts_executed", 0), ("filesystem_payload_extractions", 0),
        ("network_acquisitions", 0), ("source_manifest_before", source_before),
        ("source_manifest_after", source_after), ("next_state", NEXT_STATE),
    ]
    write_tsv(OUT / "summary.tsv", ["field", "value"], ({"field": key, "value": value} for key, value in summary))
    (OUT / "analysis.status").write_text("PASS\n", encoding="utf-8")
    (OUT / "claim-boundary.txt").write_text(
        "Local recipe, artifact/member and crosswalk observations are review evidence, not build provenance or adaptation acceptance.\n"
        "Missing external, semantic and policy evidence is recorded explicitly and is not inferred from current host state.\n"
        "No build, package operation, maintainer script, payload extraction, network acquisition, provider promotion or target population is performed.\n",
        encoding="utf-8",
    )
    (OUT / "next-state.txt").write_text(NEXT_STATE + "\n", encoding="utf-8")
    print("generic build attestation and adaptation evidence collector: PASS")


if __name__ == "__main__":
    main()
