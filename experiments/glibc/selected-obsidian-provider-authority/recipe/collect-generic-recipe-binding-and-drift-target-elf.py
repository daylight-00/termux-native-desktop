#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import os
import re
import stat
import struct
import subprocess
import tarfile
from collections import Counter, defaultdict
from pathlib import Path, PurePosixPath
from typing import Iterable

PROJECT_REPO = Path(os.environ["PROJECT_REPO"]).resolve()
OUT = Path(os.environ["OUT"]).resolve()
RULES = Path(os.environ.get(
    "GENERIC_RECIPE_DRIFT_RULES",
    PROJECT_REPO / "experiments/glibc/selected-obsidian-provider-authority/review/generic-recipe-binding-and-drift-target-rules.tsv",
)).resolve()
ARTIFACTS = Path(os.environ.get(
    "GENERIC_COMPARISON_ARTIFACTS",
    PROJECT_REPO / "experiments/glibc/selected-obsidian-provider-authority/review/generic-artifact-member-comparison-artifacts.tsv",
)).resolve()
SOURCE_REPO = Path(os.environ.get(
    "GENERIC_SOURCE_REPO",
    PROJECT_REPO / "experiments/glibc/selected-obsidian-provider-authority/work/source/termux-pacman-glibc-packages",
)).resolve()
ARTIFACT_CACHE = Path(os.environ.get(
    "GENERIC_ARTIFACT_CACHE",
    PROJECT_REPO / "experiments/glibc/selected-obsidian-provider-authority/work/artifacts/generic-artifact-member-inventory",
)).resolve()
SOURCE_EXPECTED_HEAD = os.environ.get("GENERIC_SOURCE_EXPECTED_HEAD", "fd2ae25e04f3ea26d6c7b4678020814889331d86")
SOURCE_EXPECTED_TREE = os.environ.get("GENERIC_SOURCE_EXPECTED_TREE", "e502a4c18ab9092ec119e3a498a0bf192ef60e6f")
TEST_MODE = os.environ.get("GENERIC_RECIPE_DRIFT_TEST_MODE", "0") == "1"
MAX_MEMBER_BYTES = int(os.environ.get("GENERIC_DRIFT_MAX_MEMBER_BYTES", str(64 * 1024 * 1024)))
APPROVED_ORIGINS = {
    "https://github.com/termux-pacman/glibc-packages.git",
    "git@github.com:termux-pacman/glibc-packages.git",
    "ssh://git@github.com/termux-pacman/glibc-packages.git",
}
stage = "initialization"


def fail(message: str) -> None:
    raise SystemExit(f"generic recipe binding and drift target ELF collector: FAIL [{stage}]: {message}")


def run(args: list[str], *, cwd: Path | None = None, check: bool = True, text: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(args, cwd=cwd, check=check, text=text, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8", errors="strict") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def write_tsv(path: Path, fields: list[str], rows: Iterable[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, delimiter="\t", lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
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


def source_git(args: list[str], *, check: bool = True, text: bool = True) -> subprocess.CompletedProcess:
    return run(["git", *args], cwd=SOURCE_REPO, check=check, text=text)


def source_state() -> dict[str, str]:
    if not (SOURCE_REPO / ".git").exists():
        fail(f"missing regular source checkout: {SOURCE_REPO}")
    head = source_git(["rev-parse", "HEAD"]).stdout.strip()
    tree = source_git(["rev-parse", "HEAD^{tree}"]).stdout.strip()
    shallow = source_git(["rev-parse", "--is-shallow-repository"]).stdout.strip()
    bare = source_git(["rev-parse", "--is-bare-repository"]).stdout.strip()
    status = source_git(["status", "--porcelain", "--untracked-files=all"]).stdout
    origin = source_git(["remote", "get-url", "origin"], check=False).stdout.strip()
    if head != SOURCE_EXPECTED_HEAD or tree != SOURCE_EXPECTED_TREE:
        fail(f"source pin mismatch: {head}/{tree}")
    if shallow != "false" or bare != "false" or status:
        fail("source checkout must be full, non-bare and clean")
    if not TEST_MODE and origin not in APPROVED_ORIGINS:
        fail(f"unexpected source origin: {origin}")
    if source_git(["fsck", "--connectivity-only", "--no-dangling"], check=False).returncode:
        fail("source repository fsck failed")
    return {
        "path": str(SOURCE_REPO), "head": head, "tree": tree, "origin": origin or "-",
        "is_shallow": shallow, "is_bare": bare, "worktree_state": "CLEAN", "fsck_state": "PASS",
    }


def normalize_tar_path(value: str) -> str:
    while value.startswith("./"):
        value = value[2:]
    parsed = PurePosixPath(value)
    if parsed.is_absolute() or not parsed.parts or any(part in {"", ".", ".."} for part in parsed.parts):
        fail(f"unsafe tar path: {value!r}")
    return str(parsed)


def parse_elf64_little_soname(payload: bytes) -> dict[str, str]:
    result = {"elf_parse_state": "NOT_ELF", "elf_class": "-", "elf_data": "-", "elf_machine": "-", "observed_soname": "-"}
    if len(payload) < 64 or payload[:4] != b"\x7fELF":
        return result
    elf_class, elf_data = payload[4], payload[5]
    result["elf_class"] = {1: "ELF32", 2: "ELF64"}.get(elf_class, f"UNKNOWN_{elf_class}")
    result["elf_data"] = {1: "LITTLE", 2: "BIG"}.get(elf_data, f"UNKNOWN_{elf_data}")
    if elf_class != 2 or elf_data != 1:
        result["elf_parse_state"] = "ELF_UNSUPPORTED_CLASS_OR_ENDIAN"
        return result
    try:
        header = struct.unpack_from("<16sHHIQQQIHHHHHH", payload, 0)
        machine, phoff, phentsize, phnum = header[2], header[5], header[9], header[10]
        result["elf_machine"] = str(machine)
        if phentsize < 56 or phoff + phentsize * phnum > len(payload):
            result["elf_parse_state"] = "ELF_PROGRAM_HEADER_BOUNDS_INVALID"; return result
        loads: list[tuple[int, int, int]] = []
        dynamic: tuple[int, int] | None = None
        for index in range(phnum):
            offset = phoff + index * phentsize
            p_type, _flags, p_offset, p_vaddr, _paddr, p_filesz, _memsz, _align = struct.unpack_from("<IIQQQQQQ", payload, offset)
            if p_type == 1: loads.append((p_vaddr, p_offset, p_filesz))
            elif p_type == 2: dynamic = (p_offset, p_filesz)
        if dynamic is None:
            result["elf_parse_state"] = "ELF_NO_DYNAMIC_SEGMENT"; return result
        dyn_offset, dyn_size = dynamic
        if dyn_offset + dyn_size > len(payload):
            result["elf_parse_state"] = "ELF_DYNAMIC_BOUNDS_INVALID"; return result
        strtab_vaddr = strtab_size = soname_index = None
        for offset in range(dyn_offset, dyn_offset + dyn_size, 16):
            if offset + 16 > len(payload): break
            tag, value = struct.unpack_from("<QQ", payload, offset)
            if tag == 0: break
            if tag == 5: strtab_vaddr = value
            elif tag == 10: strtab_size = value
            elif tag == 14: soname_index = value
        if strtab_vaddr is None or soname_index is None:
            result["elf_parse_state"] = "ELF_DYNAMIC_NO_SONAME"; return result
        strtab_offset = None
        for p_vaddr, p_offset, p_filesz in loads:
            if p_vaddr <= strtab_vaddr < p_vaddr + p_filesz:
                strtab_offset = p_offset + (strtab_vaddr - p_vaddr); break
        if strtab_offset is None:
            result["elf_parse_state"] = "ELF_STRTAB_NOT_FILE_MAPPED"; return result
        string_offset = strtab_offset + soname_index
        upper = min(len(payload), strtab_offset + strtab_size) if strtab_size is not None else len(payload)
        if string_offset >= upper:
            result["elf_parse_state"] = "ELF_SONAME_OFFSET_INVALID"; return result
        end = payload.find(b"\x00", string_offset, upper)
        if end < 0:
            result["elf_parse_state"] = "ELF_SONAME_UNTERMINATED"; return result
        result["observed_soname"] = payload[string_offset:end].decode("utf-8", errors="replace")
        result["elf_parse_state"] = "ELF_SONAME_PARSED"
        return result
    except (struct.error, ValueError, OverflowError) as exc:
        result["elf_parse_state"] = f"ELF_PARSE_ERROR_{type(exc).__name__}"
        return result


def read_data_member(artifact: Path, target: str) -> tuple[bytes, dict[str, object]]:
    wanted = normalize_tar_path(target)
    proc = subprocess.Popen(["dpkg-deb", "--fsys-tarfile", str(artifact)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    assert proc.stdout is not None and proc.stderr is not None
    found: tuple[bytes, dict[str, object]] | None = None
    try:
        with tarfile.open(fileobj=proc.stdout, mode="r|*") as archive:
            for member in archive:
                normalized = normalize_tar_path(member.name) if member.name not in {"", ".", "./"} else ""
                if normalized != wanted:
                    continue
                if not member.isreg():
                    fail(f"drift target is not regular: {target}")
                if member.size > MAX_MEMBER_BYTES:
                    fail(f"drift target exceeds in-memory ceiling: {target} size={member.size}")
                stream = archive.extractfile(member)
                if stream is None:
                    fail(f"unable to read drift target: {target}")
                payload = stream.read(MAX_MEMBER_BYTES + 1)
                if len(payload) != member.size or len(payload) > MAX_MEMBER_BYTES:
                    fail(f"drift target read-size mismatch: {target}")
                found = (payload, {"member_path": normalized, "member_size": member.size, "member_mode_octal": format(member.mode, "o")})
                break
    finally:
        proc.stdout.close()
    stderr = proc.stderr.read().decode(errors="replace")
    rc = proc.wait()
    if rc != 0:
        fail(f"dpkg-deb stream failed for {artifact}: {stderr.strip()}")
    if found is None:
        fail(f"drift target not found: {wanted} in {artifact.name}")
    return found


def recipe_inventory(recipe_root: str) -> tuple[list[dict[str, object]], str, Counter[str], set[str]]:
    proc = source_git(["ls-tree", "-r", "-l", SOURCE_EXPECTED_HEAD, "--", recipe_root])
    rows: list[dict[str, object]] = []
    counts: Counter[str] = Counter()
    tokens: set[str] = set()
    manifest_lines: list[str] = []
    for line in proc.stdout.splitlines():
        meta, path = line.split("\t", 1)
        mode, obj_type, oid, size_text = meta.split(None, 3)
        if obj_type != "blob":
            continue
        payload = source_git(["show", f"{SOURCE_EXPECTED_HEAD}:{path}"], text=False).stdout
        size = len(payload)
        content_sha = bytes_sha256(payload)
        manifest_lines.append("\t".join([path, oid, str(size), content_sha]))
        if path.endswith("/build.sh"): counts["build"] += 1
        elif path.endswith(".patch"): counts["patch"] += 1; tokens.add("PATCH_FILE")
        elif path.endswith(".subpackage.sh"): counts["subpackage"] += 1; tokens.add("SUBPACKAGE_SCRIPT")
        elif path.endswith("Termux.layout") or "/hooks/" in path or path.endswith(".in"):
            counts["layout_hook"] += 1; tokens.add("LAYOUT_OR_HOOK")
        else: counts["other"] += 1
        text = payload.decode(errors="replace")
        if "TERMUX_PKG_EXTRA_CONFIGURE_ARGS" in text: tokens.add("EXTRA_CONFIGURE_ARGS")
        if "termux_step_" in text: tokens.add("CUSTOM_TERMUX_STEP")
        if "TERMUX_PREFIX" in text: tokens.add("TERMUX_PREFIX_REFERENCE")
        if "TERMUX_PKG_BUILD_IN_SRC" in text: tokens.add("BUILD_IN_SRC")
        if "TERMUX_PKG_REVISION" in text: tokens.add("PACKAGE_REVISION")
        rows.append({"recipe_root": recipe_root, "path": path, "mode": mode, "blob_oid": oid, "size": size, "content_sha256": content_sha})
    manifest_sha = bytes_sha256(("\n".join(manifest_lines) + "\n").encode())
    return rows, manifest_sha, counts, tokens


def main() -> None:
    global stage
    if OUT.exists() or OUT.is_symlink():
        fail(f"refusing existing output: {OUT}")
    OUT.mkdir(parents=True)
    (OUT / "analysis.status").write_text("IN_PROGRESS\n", encoding="utf-8")

    stage = "canonical_inputs"
    rules = read_tsv(RULES)
    artifacts = read_tsv(ARTIFACTS)
    expected_count = 3 if TEST_MODE else 37
    expected_artifact_count = 2 if TEST_MODE else 34
    expected_selected_artifact_count = 2 if TEST_MODE else 29
    selected_artifact_ids = {row["artifact_id"] for row in rules}
    if len(rules) != expected_count or len({row["evidence_row_id"] for row in rules}) != expected_count:
        fail(f"rule denominator mismatch: {len(rules)} != {expected_count}")
    if len(artifacts) != expected_artifact_count or len({row["artifact_id"] for row in artifacts}) != expected_artifact_count:
        fail(f"artifact denominator mismatch: {len(artifacts)} != {expected_artifact_count}")
    if len(selected_artifact_ids) != expected_selected_artifact_count:
        fail(f"selected artifact denominator mismatch: {len(selected_artifact_ids)} != {expected_selected_artifact_count}")
    classes = Counter(row["drift_target_elf_review_state"] for row in rules)
    if not TEST_MODE and classes != Counter({
        "NOT_REQUIRED_EXACT_MEMBER_ALREADY_OBSERVED": 21,
        "PENDING_READ_ONLY_TARGET_ELF_INSPECTION": 15,
        "NOT_APPLICABLE_EXPECTED_ALIAS_ABSENT_CORRECT_CANDIDATE_REQUIRED": 1,
    }):
        fail(f"rule class cardinality drifted: {dict(classes)}")
    if any(row["artifact_to_recipe_binding_state"] != "OPEN_NO_BUILD_ATTESTATION" or row["final_provider_state"] != "UNRESOLVED" or row["target_population_state"] != "BLOCKED" for row in rules):
        fail("authority stop states drifted")
    artifact_by_id = {row["artifact_id"]: row for row in artifacts}
    for row in rules:
        artifact = artifact_by_id.get(row["artifact_id"])
        if artifact is None:
            fail(f"unknown artifact id: {row['artifact_id']}")
        for key, artifact_key in (("artifact_package", "package"), ("artifact_version", "version"), ("artifact_architecture", "architecture"), ("artifact_sha256", "artifact_sha256")):
            if row[key] != artifact[artifact_key]:
                fail(f"artifact rule mismatch {row['identity_label']} {key}")

    source_before_manifest = directory_manifest(SOURCE_REPO)
    cache_before_manifest = directory_manifest(ARTIFACT_CACHE)

    stage = "source_repository"
    source = source_state()
    write_tsv(OUT / "source-repository-state.tsv", list(source), [source])

    stage = "recipe_inventory"
    recipe_rows: list[dict[str, object]] = []
    recipe_summary: dict[str, dict[str, object]] = {}
    for recipe_root in sorted({row["recipe_root"] for row in rules}):
        observed_tree = source_git(["rev-parse", f"{SOURCE_EXPECTED_HEAD}:{recipe_root}"], check=False).stdout.strip()
        rule_rows = [row for row in rules if row["recipe_root"] == recipe_root]
        expected_tree = {row["recipe_tree"] for row in rule_rows}
        if len(expected_tree) != 1 or observed_tree not in expected_tree:
            fail(f"recipe tree mismatch for {recipe_root}: {observed_tree} != {expected_tree}")
        rows, manifest_sha, counts, tokens = recipe_inventory(recipe_root)
        expected_manifest = {row["recipe_file_manifest_sha256"] for row in rule_rows}
        if len(expected_manifest) != 1 or manifest_sha not in expected_manifest:
            fail(f"recipe file manifest mismatch for {recipe_root}")
        expected_counts = {
            (row["recipe_file_count"], row["patch_file_count"], row["subpackage_file_count"], row["layout_hook_file_count"], row["other_recipe_file_count"])
            for row in rule_rows
        }
        observed_counts = (str(len(rows)), str(counts["patch"]), str(counts["subpackage"]), str(counts["layout_hook"]), str(counts["other"]))
        if expected_counts != {observed_counts}:
            fail(f"recipe file counts mismatch for {recipe_root}: {observed_counts} != {expected_counts}")
        build = next((row for row in rows if str(row["path"]).endswith("/build.sh")), None)
        if build is None:
            fail(f"missing build.sh for {recipe_root}")
        expected_build = {(row["recipe_build_sh_blob"], row["recipe_build_sh_sha256"]) for row in rule_rows}
        if expected_build != {(build["blob_oid"], build["content_sha256"])}:
            fail(f"build.sh identity mismatch for {recipe_root}")
        recipe_rows.extend(rows)
        recipe_summary[recipe_root] = {
            "recipe_tree": observed_tree, "recipe_file_manifest_sha256": manifest_sha,
            "recipe_file_count": len(rows), "patch_file_count": counts["patch"],
            "subpackage_file_count": counts["subpackage"], "layout_hook_file_count": counts["layout_hook"],
            "other_recipe_file_count": counts["other"], "adaptation_evidence_tokens": ";".join(sorted(tokens)) or "NONE_DECLARED",
        }
    write_tsv(OUT / "recipe-file-inventory.tsv", ["recipe_root", "path", "mode", "blob_oid", "size", "content_sha256"], recipe_rows)

    stage = "artifact_verification"
    artifact_verification: list[dict[str, object]] = []
    artifact_paths: dict[str, Path] = {}
    for artifact_id in sorted(artifact_by_id):
        artifact = artifact_by_id[artifact_id]
        path = ARTIFACT_CACHE / Path(artifact["repository_filename"]).name
        if path.is_symlink() or not path.is_file():
            fail(f"missing regular cached artifact: {path}")
        actual_size, actual_sha = path.stat().st_size, sha256(path)
        if actual_size != int(artifact["artifact_size"]) or actual_sha != artifact["artifact_sha256"]:
            fail(f"cached artifact identity mismatch: {path.name}")
        control_text = run(["dpkg-deb", "-W", "--showformat=${Package}\t${Version}\t${Architecture}\n", str(path)]).stdout.rstrip("\n")
        control = control_text.split("\t")
        if len(control) != 3 or control != [artifact["package"], artifact["version"], artifact["architecture"]]:
            fail(f"cached artifact control mismatch: {path.name}: {control}")
        artifact_paths[artifact_id] = path
        artifact_verification.append({
            "artifact_id": artifact_id, "package": artifact["package"], "version": artifact["version"],
            "architecture": artifact["architecture"], "local_path": str(path), "actual_size": actual_size,
            "actual_sha256": actual_sha, "control_identity_state": "EXACT_PACKAGE_VERSION_ARCHITECTURE_MATCH",
            "package_operation_performed": "NO",
        })
    write_tsv(OUT / "artifact-verification.tsv", [
        "artifact_id", "package", "version", "architecture", "local_path", "actual_size", "actual_sha256",
        "control_identity_state", "package_operation_performed",
    ], artifact_verification)

    stage = "drift_target_elf"
    drift_rows: list[dict[str, object]] = []
    for row in rules:
        pending = row["drift_target_elf_review_state"] == "PENDING_READ_ONLY_TARGET_ELF_INSPECTION"
        if not pending:
            continue
        payload, member_meta = read_data_member(artifact_paths[row["artifact_id"]], row["alias_target_member_path"])
        elf = parse_elf64_little_soname(payload)
        state = "DRIFT_TARGET_ELF_EXPECTED_SONAME_CONFIRMED" if elf["elf_parse_state"] == "ELF_SONAME_PARSED" and elf["observed_soname"] == row["expected_soname_alias"] else "DRIFT_TARGET_ELF_EXPECTED_SONAME_NOT_CONFIRMED"
        drift_rows.append({
            "evidence_row_id": row["evidence_row_id"], "identity_label": row["identity_label"],
            "artifact_id": row["artifact_id"], "artifact_package": row["artifact_package"],
            "expected_soname_alias": row["expected_soname_alias"], "alias_member_path": normalize_tar_path(row["alias_member_path"]),
            "target_member_path": member_meta["member_path"], "target_member_size": member_meta["member_size"],
            "target_member_mode_octal": member_meta["member_mode_octal"], "target_member_sha256": bytes_sha256(payload),
            "elf_parse_state": elf["elf_parse_state"], "elf_class": elf["elf_class"], "elf_data": elf["elf_data"],
            "elf_machine": elf["elf_machine"], "observed_soname": elf["observed_soname"], "drift_target_elf_review_state": state,
            "object_member_evidence_state": "OBSERVED_CANDIDATE_NOT_AUTHORITY_ACCEPTED",
            "artifact_to_recipe_binding_state": "OPEN_NO_BUILD_ATTESTATION", "termux_android_adaptation_state": "OPEN_REVIEW_REQUIRED",
            "final_provider_state": "UNRESOLVED", "target_population_state": "BLOCKED",
        })
    expected_drift = 1 if TEST_MODE else 15
    if len(drift_rows) != expected_drift:
        fail(f"drift target denominator mismatch: {len(drift_rows)} != {expected_drift}")
    if any(row["drift_target_elf_review_state"] != "DRIFT_TARGET_ELF_EXPECTED_SONAME_CONFIRMED" for row in drift_rows):
        fail("one or more drift target ELF SONAMEs were not confirmed")
    write_tsv(OUT / "drift-target-elf-review.tsv", [
        "evidence_row_id", "identity_label", "artifact_id", "artifact_package", "expected_soname_alias",
        "alias_member_path", "target_member_path", "target_member_size", "target_member_mode_octal", "target_member_sha256",
        "elf_parse_state", "elf_class", "elf_data", "elf_machine", "observed_soname", "drift_target_elf_review_state",
        "object_member_evidence_state", "artifact_to_recipe_binding_state", "termux_android_adaptation_state",
        "final_provider_state", "target_population_state",
    ], drift_rows)

    stage = "recipe_binding_review"
    binding_rows: list[dict[str, object]] = []
    for row in rules:
        summary = recipe_summary[row["recipe_root"]]
        if row["recipe_lineage_candidate_state"] != "PINNED_RECIPE_FAMILY_VERSION_ALIGNED_NO_BUILD_ATTESTATION":
            fail(f"recipe lineage rule not aligned: {row['identity_label']}")
        drift_state = row["drift_target_elf_review_state"]
        if drift_state == "PENDING_READ_ONLY_TARGET_ELF_INSPECTION":
            drift_state = next(item["drift_target_elf_review_state"] for item in drift_rows if item["evidence_row_id"] == row["evidence_row_id"])
        binding_rows.append({
            "evidence_row_id": row["evidence_row_id"], "capability_partition": row["capability_partition"], "identity_label": row["identity_label"],
            "member_receipt_review_state": row["member_receipt_review_state"], "artifact_id": row["artifact_id"],
            "artifact_package": row["artifact_package"], "artifact_version": row["artifact_version"], "artifact_sha256": row["artifact_sha256"],
            "recipe_root": row["recipe_root"], "recipe_tree": summary["recipe_tree"], "recipe_resolved_full_version": row["recipe_resolved_full_version"],
            "recipe_source_url_raw": row["recipe_source_url_raw"], "recipe_source_sha256": row["recipe_source_sha256"],
            "recipe_file_manifest_sha256": summary["recipe_file_manifest_sha256"], "adaptation_evidence_tokens": summary["adaptation_evidence_tokens"],
            "recipe_lineage_candidate_state": "PINNED_RECIPE_FAMILY_VERSION_ALIGNED_CANDIDATE",
            "artifact_to_recipe_binding_state": "OPEN_NO_BUILD_ATTESTATION",
            "termux_android_adaptation_state": "PINNED_RECIPE_ADAPTATION_EVIDENCE_INVENTORIED_REVIEW_OPEN",
            "drift_target_elf_review_state": drift_state,
            "final_provider_state": "UNRESOLVED", "target_population_state": "BLOCKED",
        })
    write_tsv(OUT / "recipe-binding-review.tsv", [
        "evidence_row_id", "capability_partition", "identity_label", "member_receipt_review_state", "artifact_id",
        "artifact_package", "artifact_version", "artifact_sha256", "recipe_root", "recipe_tree", "recipe_resolved_full_version",
        "recipe_source_url_raw", "recipe_source_sha256", "recipe_file_manifest_sha256", "adaptation_evidence_tokens",
        "recipe_lineage_candidate_state", "artifact_to_recipe_binding_state", "termux_android_adaptation_state",
        "drift_target_elf_review_state", "final_provider_state", "target_population_state",
    ], binding_rows)

    stage = "immutability"
    source_after_manifest = directory_manifest(SOURCE_REPO)
    cache_after_manifest = directory_manifest(ARTIFACT_CACHE)
    if source_before_manifest != source_after_manifest or cache_before_manifest != cache_after_manifest:
        fail("source checkout or artifact cache mutated during read-only review")

    summary = [
        ("source_repository_head", source["head"]), ("source_repository_tree", source["tree"]),
        ("review_identity_rows", len(binding_rows)), ("unique_recipe_roots", len(recipe_summary)),
        ("selected_rule_artifacts", len(selected_artifact_ids)),
        ("verified_cached_artifacts", len(artifact_verification)), ("recipe_family_version_aligned_rows", len(binding_rows)),
        ("drift_target_elf_rows", len(drift_rows)), ("drift_target_expected_soname_confirmed", len(drift_rows)),
        ("expected_alias_absent_correct_candidate_required", sum(row["drift_target_elf_review_state"].startswith("NOT_APPLICABLE") for row in rules)),
        ("artifact_to_recipe_bindings_accepted", 0), ("termux_android_adaptations_accepted", 0),
        ("final_provider_decisions_accepted", 0), ("target_rows_populated", 0),
        ("next_state", "REVIEW_BOUNDED_GENERIC_RECIPE_BINDING_AND_DRIFT_TARGET_ELF_RECEIPT"),
    ]
    write_tsv(OUT / "summary.tsv", ["field", "value"], ({"field": key, "value": value} for key, value in summary))
    (OUT / "claim-boundary.txt").write_text(
        "Pinned recipe family/version/tree alignment is candidate lineage evidence, not artifact build attestation.\n"
        "Recipe files and Termux-specific tokens are adaptation evidence inventory, not adaptation acceptance.\n"
        "A drift target ELF SONAME match is object/member candidate evidence, not final provider authority.\n"
        "No package transaction, maintainer script, filesystem extraction, target population or runtime execution is permitted.\n",
        encoding="utf-8",
    )
    (OUT / "next-state.txt").write_text("REVIEW_BOUNDED_GENERIC_RECIPE_BINDING_AND_DRIFT_TARGET_ELF_RECEIPT\n", encoding="utf-8")
    (OUT / "analysis.status").write_text("PASS\n", encoding="utf-8")
    print("generic recipe binding and drift target ELF collector: PASS")


if __name__ == "__main__":
    main()
