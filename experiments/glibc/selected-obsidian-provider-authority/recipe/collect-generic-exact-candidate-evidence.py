#!/usr/bin/env python3
from __future__ import annotations

import bz2
import csv
import gzip
import hashlib
import lzma
import os
import re
import shutil
import subprocess
import sys
import traceback
from collections import defaultdict
from pathlib import Path
from typing import Iterable

REPO = Path(os.environ.get("PROJECT_REPO", subprocess.check_output([
    "git", "-C", str(Path(__file__).resolve().parent), "rev-parse", "--show-toplevel"
], text=True).strip())).resolve()
SOURCE_REPO = Path(os.environ["SOURCE_REPO"]).resolve()
SOURCE_REPO_EXPECTED_HEAD = os.environ["SOURCE_REPO_EXPECTED_HEAD"]
PREFIX = Path(os.environ["PREFIX"]).resolve()
OUT = Path(os.environ["OUT"]).resolve()
TOKENS = REPO / "experiments/glibc/selected-obsidian-provider-authority/review/generic-exact-candidate-search-tokens.tsv"
APT_ETC = PREFIX / "etc/apt"
APT_LISTS = PREFIX / "var/lib/apt/lists"
APT_ARCHIVES = PREFIX / "var/cache/apt/archives"
DPKG_STATUS = PREFIX / "var/lib/dpkg/status"
APPROVED_ORIGINS = {
    "",
    "https://github.com/termux-pacman/glibc-packages.git",
    "git@github.com:termux-pacman/glibc-packages.git",
    "ssh://git@github.com/termux-pacman/glibc-packages.git",
}
stage = "initialization"


def run(args: list[str], *, cwd: Path | None = None, check: bool = True, text: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(args, cwd=cwd, check=check, text=text, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def source_git(args: list[str], *, check: bool = True, text: bool = True) -> subprocess.CompletedProcess:
    return run(["git", "-c", f"safe.directory={SOURCE_REPO}", "-C", str(SOURCE_REPO), *args], check=check, text=text)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def bytes_sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, fields: list[str], rows: Iterable[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def write_status(value: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "analysis.status").write_text(value + "\n")


def fail(name: str, message: str, rc: int = 1) -> None:
    write_status("FAIL")
    (OUT / "failure-stage.txt").write_text(name + "\n")
    print(message, file=sys.stderr)
    print(f"evidence: {OUT}", file=sys.stderr)
    raise SystemExit(rc)


def parse_deb822(text: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    row: dict[str, str] = {}
    current: str | None = None
    for line in text.splitlines() + [""]:
        if not line:
            if row:
                rows.append(row)
            row = {}
            current = None
            continue
        if line[0].isspace() and current:
            row[current] += "\n" + line.strip()
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        current = key
        row[key] = value.strip()
    return rows


def compression(path: Path) -> str:
    with path.open("rb") as handle:
        magic = handle.read(8)
    if magic.startswith(b"\x1f\x8b"):
        return "gzip"
    if magic.startswith(b"BZh"):
        return "bzip2"
    if magic.startswith(b"\xfd7zXZ\x00"):
        return "xz"
    if magic.startswith(b"\x04\x22\x4d\x18"):
        return "lz4"
    if magic.startswith(b"\x28\xb5\x2f\xfd"):
        return "zstd"
    return "plain"


def read_index(path: Path) -> tuple[str, str, str]:
    kind = compression(path)
    try:
        if kind == "gzip":
            data = gzip.open(path, "rb").read()
        elif kind == "bzip2":
            data = bz2.open(path, "rb").read()
        elif kind == "xz":
            data = lzma.open(path, "rb").read()
        elif kind in {"lz4", "zstd"}:
            command = shutil.which("lz4") if kind == "lz4" else shutil.which("zstd")
            cat_command = shutil.which("lz4cat") if kind == "lz4" else shutil.which("zstdcat")
            if command:
                proc = run([command, "-dc", str(path)], check=False, text=False)
            elif cat_command:
                proc = run([cat_command, str(path)], check=False, text=False)
            else:
                return kind, f"UNSUPPORTED_NO_{kind.upper()}", ""
            if proc.returncode:
                return kind, f"DECOMPRESS_FAIL_RC_{proc.returncode}", ""
            data = proc.stdout
        else:
            data = path.read_bytes()
        return kind, "PARSED", data.decode(errors="replace")
    except Exception as exc:
        return kind, f"READ_FAIL_{type(exc).__name__}", ""


def snapshot_files(paths: Iterable[Path]) -> dict[str, tuple[int, str]]:
    result: dict[str, tuple[int, str]] = {}
    for path in sorted({p.resolve() for p in paths if p.is_file()}, key=str):
        result[str(path)] = (path.stat().st_size, sha256(path))
    return result


def apt_files() -> list[Path]:
    paths: list[Path] = []
    direct = APT_ETC / "sources.list"
    if direct.is_file():
        paths.append(direct)
    source_dir = APT_ETC / "sources.list.d"
    if source_dir.is_dir():
        paths.extend(p for p in source_dir.iterdir() if p.is_file())
    if APT_LISTS.is_dir():
        paths.extend(p for p in APT_LISTS.iterdir() if p.is_file())
    if APT_ARCHIVES.is_dir():
        paths.extend(APT_ARCHIVES.glob("*.deb"))
    if DPKG_STATUS.is_file():
        paths.append(DPKG_STATUS)
    return paths


def source_state() -> dict[str, str]:
    return {
        "logical_path": str(SOURCE_REPO),
        "head": source_git(["rev-parse", "HEAD"]).stdout.strip(),
        "tree": source_git(["rev-parse", "HEAD^{tree}"]).stdout.strip(),
        "branch": source_git(["rev-parse", "--abbrev-ref", "HEAD"]).stdout.strip(),
        "is_bare": source_git(["rev-parse", "--is-bare-repository"]).stdout.strip(),
        "is_shallow": source_git(["rev-parse", "--is-shallow-repository"]).stdout.strip(),
        "status_sha256": bytes_sha256(source_git(["status", "--porcelain", "--untracked-files=all"]).stdout.encode()),
        "refs_sha256": bytes_sha256(source_git(["for-each-ref", "--format=%(refname)%00%(objectname)%00%(objecttype)%00"]).stdout.encode()),
        "origin": source_git(["remote", "get-url", "origin"], check=False).stdout.strip(),
    }


def normalized(value: str) -> str:
    return " ".join(re.sub(r"[^a-z0-9+.-]+", " ", value.lower()).split())


def token_match(tokens: list[str], text: str) -> list[str]:
    haystack = f" {normalized(text)} "
    matches: list[str] = []
    for token in tokens:
        needle = normalized(token)
        if len(needle) < 3:
            continue
        if needle in haystack and needle not in matches:
            matches.append(needle)
    return matches


def parse_shell_assignments(text: str) -> dict[str, str]:
    rows: dict[str, str] = {}
    for line in text.splitlines():
        match = re.match(r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)$", line)
        if not match:
            continue
        key, value = match.groups()
        value = value.strip().rstrip(";")
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
            value = value[1:-1]
        rows.setdefault(key, value)
    return rows


def recipe_inventory(head: str) -> tuple[list[dict[str, object]], dict[str, list[dict[str, object]]]]:
    paths = source_git(["ls-tree", "-r", "--name-only", head, "--", "gpkg"]).stdout.splitlines()
    recipe_roots = sorted({"/".join(path.split("/")[:2]) for path in paths if path.startswith("gpkg/") and len(path.split("/")) >= 3})
    inventory: list[dict[str, object]] = []
    by_recipe: dict[str, list[dict[str, object]]] = defaultdict(list)
    for recipe_root in recipe_roots:
        root_paths = [path for path in paths if path.startswith(recipe_root + "/")]
        texts: list[str] = []
        build_text = ""
        for path in root_paths:
            proc = source_git(["show", f"{head}:{path}"], check=False, text=False)
            if proc.returncode:
                continue
            data = proc.stdout
            if path.endswith("/build.sh"):
                build_text = data.decode(errors="replace")
            if len(data) <= 1024 * 1024:
                texts.append(data.decode(errors="replace"))
        assignments = parse_shell_assignments(build_text)
        recipe_name = recipe_root.split("/", 1)[1]
        package_names = {recipe_name}
        for path in root_paths:
            if path.endswith(".subpackage.sh"):
                package_names.add(Path(path).name.removesuffix(".subpackage.sh"))
        tree_proc = source_git(["rev-parse", f"{head}:{recipe_root}"], check=False)
        recipe_tree = tree_proc.stdout.strip() if tree_proc.returncode == 0 else "-"
        row = {
            "recipe_root": recipe_root,
            "recipe_name": recipe_name,
            "package_names": ";".join(sorted(package_names)),
            "recipe_tree": recipe_tree,
            "version": assignments.get("TERMUX_PKG_VERSION", "-"),
            "revision": assignments.get("TERMUX_PKG_REVISION", "0"),
            "source_url": assignments.get("TERMUX_PKG_SRCURL", "-"),
            "source_sha256": assignments.get("TERMUX_PKG_SHA256", "-"),
            "depends": assignments.get("TERMUX_PKG_DEPENDS", "-"),
            "build_depends": assignments.get("TERMUX_PKG_BUILD_DEPENDS", "-"),
            "search_text": "\n".join([recipe_root, *sorted(package_names), *texts]),
            "paths": root_paths,
        }
        inventory.append(row)
        for package in package_names:
            by_recipe[package].append(row)
    return inventory, by_recipe


def main() -> None:
    global stage
    if OUT.exists() or OUT.is_symlink():
        raise SystemExit(f"refusing existing output: {OUT}")
    OUT.mkdir(parents=True)
    write_status("IN_PROGRESS")

    stage = "canonical_input"
    token_rows = read_tsv(TOKENS)
    if len(token_rows) != 61 or len({row["evidence_row_id"] for row in token_rows}) != 61:
        fail(stage, "canonical generic token denominator is not 61")
    if any(row["candidate_binding_state"] != "SEARCH_ONLY_NOT_AUTHORITY" or row["target_population_state"] != "BLOCKED" for row in token_rows):
        fail(stage, "canonical generic token authority boundary drifted")
    input_dir = OUT / "input"
    input_dir.mkdir()
    shutil.copyfile(TOKENS, input_dir / TOKENS.name)

    stage = "source_repository_guard"
    if not SOURCE_REPO.is_dir() or not (SOURCE_REPO / ".git").exists():
        fail(stage, f"missing full source checkout: {SOURCE_REPO}")
    before_source = source_state()
    if before_source["head"] != SOURCE_REPO_EXPECTED_HEAD:
        fail(stage, f"source HEAD mismatch: {before_source['head']} != {SOURCE_REPO_EXPECTED_HEAD}")
    if before_source["is_bare"] != "false" or before_source["is_shallow"] != "false":
        fail(stage, "source checkout must be full and non-bare")
    if before_source["status_sha256"] != bytes_sha256(b""):
        fail(stage, "source checkout must be clean including untracked files")
    if before_source["origin"] not in APPROVED_ORIGINS:
        fail(stage, f"unexpected source origin: {before_source['origin']}")
    source_git(["fsck", "--connectivity-only", "--no-dangling"])

    stage = "apt_snapshot"
    before_apt = snapshot_files(apt_files())
    if not APT_LISTS.is_dir():
        fail(stage, f"missing apt lists: {APT_LISTS}")

    stage = "apt_index_parse"
    apt_index_rows: list[dict[str, object]] = []
    apt_records: list[dict[str, str]] = []
    for path in sorted(p for p in APT_LISTS.iterdir() if p.is_file() and "Packages" in p.name):
        kind, state, text = read_index(path)
        records = parse_deb822(text) if state == "PARSED" else []
        apt_index_rows.append({
            "path": str(path), "size": path.stat().st_size, "sha256": sha256(path),
            "compression": kind, "parse_state": state, "paragraphs": len(records),
        })
        for record in records:
            item = dict(record)
            item["_index_file"] = str(path)
            item["_index_sha256"] = sha256(path)
            apt_records.append(item)
    if not apt_index_rows or not any(row["parse_state"] == "PARSED" for row in apt_index_rows):
        fail(stage, "no apt Packages index could be parsed without mutation")

    stage = "recipe_inventory"
    recipe_rows, _ = recipe_inventory(before_source["head"])

    stage = "candidate_edges"
    apt_candidates: list[dict[str, object]] = []
    recipe_candidates: list[dict[str, object]] = []
    edges: list[dict[str, object]] = []
    apt_by_object: dict[str, set[str]] = defaultdict(set)
    recipe_by_object: dict[str, set[str]] = defaultdict(set)
    recipe_match_rows: dict[tuple[str, str], dict[str, object]] = {}

    for generic in token_rows:
        evidence_id = generic["evidence_row_id"]
        tokens = [token for token in generic["search_tokens"].split(";") if token]
        for record in apt_records:
            package = record.get("Package", "")
            source = record.get("Source", "")
            index_file = record.get("_index_file", "")
            source_package = source.split()[0] if source.split() else ""
            candidate_domain = package.endswith("-glibc") or source_package.endswith("-glibc") or "termux-glibc" in index_file or "_glibc_" in index_file
            if not candidate_domain:
                continue
            search_text = "\n".join(record.get(field, "") for field in ("Package", "Source", "Description", "Provides", "Depends", "Filename"))
            matches = token_match(tokens, search_text)
            if not matches:
                continue
            apt_by_object[evidence_id].add(package)
            apt_candidates.append({
                "evidence_row_id": evidence_id,
                "capability_partition": generic["capability_partition"],
                "lookup_name": generic["lookup_name"],
                "candidate_package": package,
                "candidate_version": record.get("Version", "-"),
                "architecture": record.get("Architecture", "-"),
                "match_tokens": ";".join(matches),
                "index_file": record.get("_index_file", "-"),
                "index_sha256": record.get("_index_sha256", "-"),
                "repository_filename": record.get("Filename", "-"),
                "artifact_size": record.get("Size", "-"),
                "artifact_sha256": record.get("SHA256", "-"),
                "source_field": source or "-",
                "candidate_state": "EXACT_INDEX_ARTIFACT_IDENTITY_CANDIDATE" if record.get("Filename") and record.get("Size") and record.get("SHA256") else "INDEX_RECORD_CANDIDATE_INCOMPLETE",
                "object_member_binding_state": "OPEN_NO_DEB_EXTRACTION",
                "authority_state": "CANDIDATE_ONLY",
            })
        for recipe in recipe_rows:
            matches = token_match(tokens, str(recipe["search_text"]))
            if not matches:
                continue
            packages = str(recipe["package_names"]).split(";")
            for package in packages:
                recipe_by_object[evidence_id].add(package)
                key = (evidence_id, package)
                recipe_match_rows[key] = {
                    "evidence_row_id": evidence_id,
                    "capability_partition": generic["capability_partition"],
                    "lookup_name": generic["lookup_name"],
                    "candidate_package": package,
                    "recipe_root": recipe["recipe_root"],
                    "recipe_tree": recipe["recipe_tree"],
                    "candidate_version": recipe["version"],
                    "candidate_revision": recipe["revision"],
                    "match_tokens": ";".join(matches),
                    "source_url": recipe["source_url"],
                    "source_sha256": recipe["source_sha256"],
                    "depends": recipe["depends"],
                    "build_depends": recipe["build_depends"],
                    "candidate_state": "PINNED_RECIPE_SOURCE_DECLARATION_CANDIDATE",
                    "artifact_build_binding_state": "OPEN_NO_BUILD_ATTESTATION",
                    "authority_state": "CANDIDATE_ONLY",
                    "_paths": recipe["paths"],
                }
        apt_set = apt_by_object[evidence_id]
        recipe_set = recipe_by_object[evidence_id]
        overlap = apt_set & recipe_set
        if overlap:
            state = "APT_AND_RECIPE_CANDIDATE"
        elif apt_set:
            state = "APT_ONLY_CANDIDATE"
        elif recipe_set:
            state = "RECIPE_ONLY_CANDIDATE"
        else:
            state = "NO_CANDIDATE_FOUND_IN_RETAINED_INPUTS"
        edges.append({
            "evidence_row_id": evidence_id,
            "capability_partition": generic["capability_partition"],
            "identity_label": generic["identity_label"],
            "lookup_name": generic["lookup_name"],
            "soname": generic["soname"],
            "search_tokens": generic["search_tokens"],
            "apt_candidate_packages": ";".join(sorted(apt_set)) or "-",
            "recipe_candidate_packages": ";".join(sorted(recipe_set)) or "-",
            "apt_recipe_overlap_packages": ";".join(sorted(overlap)) or "-",
            "candidate_discovery_state": state,
            "object_member_binding_state": "OPEN_NO_DEB_EXTRACTION",
            "termux_android_adaptation_state": "OPEN_RECIPE_REVIEW_REQUIRED",
            "final_provider_state": "UNRESOLVED",
            "target_population_state": "BLOCKED",
        })

    recipe_candidates = list(recipe_match_rows.values())

    stage = "embed_recipe_candidates"
    file_rows: list[dict[str, object]] = []
    embedded_roots: set[str] = set()
    embedded_bytes = 0
    for candidate in recipe_candidates:
        recipe_root = str(candidate["recipe_root"])
        if recipe_root in embedded_roots:
            continue
        for path in candidate.pop("_paths"):
            proc = source_git(["show", f"{before_source['head']}:{path}"], check=False, text=False)
            if proc.returncode:
                continue
            data = proc.stdout
            blob = source_git(["rev-parse", f"{before_source['head']}:{path}"], check=False).stdout.strip() or "-"
            relative = Path(path).relative_to(recipe_root)
            embedded_state = "MANIFEST_ONLY_OVER_1_MIB"
            embedded_path = "-"
            if len(data) <= 1024 * 1024 and embedded_bytes + len(data) <= 50 * 1024 * 1024:
                destination = OUT / "recipe-files" / recipe_root.replace("/", "__") / relative
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(data)
                embedded_bytes += len(data)
                embedded_state = "EMBEDDED"
                embedded_path = str(destination.relative_to(OUT))
            file_rows.append({
                "recipe_root": recipe_root,
                "path": path,
                "blob_sha": blob,
                "size": len(data),
                "content_sha256": bytes_sha256(data),
                "embedded_state": embedded_state,
                "embedded_path": embedded_path,
            })
        embedded_roots.add(recipe_root)

    stage = "cached_artifacts"
    cache_rows: list[dict[str, object]] = []
    candidate_packages = {str(row["candidate_package"]) for row in apt_candidates}
    if APT_ARCHIVES.is_dir():
        for path in sorted(APT_ARCHIVES.glob("*.deb")):
            matches = sorted(package for package in candidate_packages if path.name.startswith(package + "_"))
            if matches:
                cache_rows.append({
                    "path": str(path), "filename": path.name, "size": path.stat().st_size,
                    "sha256": sha256(path), "candidate_packages": ";".join(matches),
                    "artifact_state": "CACHED_ARTIFACT_BYTES_CANDIDATE_NOT_EXTRACTED",
                })

    stage = "after_guards"
    after_apt = snapshot_files(apt_files())
    after_source = source_state()
    if before_apt != after_apt:
        fail(stage, "apt/dpkg/cache evidence changed during read-only collection")
    if before_source != after_source:
        fail(stage, "source checkout changed during read-only collection")

    stage = "write_outputs"
    write_tsv(OUT / "source-repository-state.tsv", list(before_source), [before_source])
    write_tsv(OUT / "apt-index-files.tsv", ["path", "size", "sha256", "compression", "parse_state", "paragraphs"], apt_index_rows)
    write_tsv(OUT / "apt-candidate-records.tsv", [
        "evidence_row_id", "capability_partition", "lookup_name", "candidate_package", "candidate_version", "architecture", "match_tokens",
        "index_file", "index_sha256", "repository_filename", "artifact_size", "artifact_sha256", "source_field", "candidate_state",
        "object_member_binding_state", "authority_state",
    ], apt_candidates)
    write_tsv(OUT / "recipe-candidate-records.tsv", [
        "evidence_row_id", "capability_partition", "lookup_name", "candidate_package", "recipe_root", "recipe_tree", "candidate_version",
        "candidate_revision", "match_tokens", "source_url", "source_sha256", "depends", "build_depends", "candidate_state",
        "artifact_build_binding_state", "authority_state",
    ], recipe_candidates)
    write_tsv(OUT / "recipe-file-manifest.tsv", ["recipe_root", "path", "blob_sha", "size", "content_sha256", "embedded_state", "embedded_path"], file_rows)
    write_tsv(OUT / "cached-deb-candidates.tsv", ["path", "filename", "size", "sha256", "candidate_packages", "artifact_state"], cache_rows)
    write_tsv(OUT / "object-candidate-edges.tsv", [
        "evidence_row_id", "capability_partition", "identity_label", "lookup_name", "soname", "search_tokens", "apt_candidate_packages",
        "recipe_candidate_packages", "apt_recipe_overlap_packages", "candidate_discovery_state", "object_member_binding_state",
        "termux_android_adaptation_state", "final_provider_state", "target_population_state",
    ], edges)
    state_counts = defaultdict(int)
    for row in edges:
        state_counts[str(row["candidate_discovery_state"])] += 1
    summary = [
        {"field": "project_head", "value": run(["git", "-C", str(REPO), "rev-parse", "HEAD"]).stdout.strip()},
        {"field": "generic_identity_rows", "value": len(edges)},
        {"field": "parsed_apt_records", "value": len(apt_records)},
        {"field": "apt_candidate_rows", "value": len(apt_candidates)},
        {"field": "recipe_candidate_rows", "value": len(recipe_candidates)},
        {"field": "candidate_recipe_roots_embedded", "value": len(embedded_roots)},
        {"field": "recipe_file_manifest_rows", "value": len(file_rows)},
        {"field": "cached_deb_candidates", "value": len(cache_rows)},
        {"field": "apt_and_recipe_candidate_objects", "value": state_counts["APT_AND_RECIPE_CANDIDATE"]},
        {"field": "apt_only_candidate_objects", "value": state_counts["APT_ONLY_CANDIDATE"]},
        {"field": "recipe_only_candidate_objects", "value": state_counts["RECIPE_ONLY_CANDIDATE"]},
        {"field": "no_candidate_objects", "value": state_counts["NO_CANDIDATE_FOUND_IN_RETAINED_INPUTS"]},
        {"field": "source_repo_head", "value": before_source["head"]},
        {"field": "source_repo_tree", "value": before_source["tree"]},
        {"field": "apt_state_unchanged", "value": "YES"},
        {"field": "source_repo_state_unchanged", "value": "YES"},
        {"field": "network_operation_performed", "value": "NO"},
        {"field": "package_operation_performed", "value": "NO"},
        {"field": "package_download_performed", "value": "NO"},
        {"field": "deb_extraction_performed", "value": "NO"},
        {"field": "source_fetch_performed", "value": "NO"},
        {"field": "build_performed", "value": "NO"},
        {"field": "authority_decisions_accepted", "value": "0"},
        {"field": "target_rows_populated", "value": "0"},
    ]
    write_tsv(OUT / "summary.tsv", ["field", "value"], summary)
    (OUT / "claim-boundary.txt").write_text(
        "This receipt discovers exact repository artifact identities and pinned source-recipe candidates for the 61 canonical non-priority generic identities using only retained apt metadata, cached files and a pre-existing clean source checkout.\n"
        "Search-token and package/recipe matches are candidate edges, not object-member binding, final provider authority, necessity, composition or target population.\n"
        "No apt update, package download, install, removal, upgrade, maintainer script, deb extraction, source fetch, build, runtime launch, generation/current operation or target mutation is performed.\n"
    )
    (OUT / "next-state.txt").write_text("READY_FOR_GENERIC_CANDIDATE_ARTIFACT_MEMBER_COMPARISON_OR_GAP_REVIEW\n")
    write_status("PASS")


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as exc:
        OUT.mkdir(parents=True, exist_ok=True)
        write_status("FAIL")
        (OUT / "failure-stage.txt").write_text(stage + "\n")
        (OUT / "exception.txt").write_text("".join(traceback.format_exception(exc)))
        print(f"generic candidate collector failed during {stage}: {exc}", file=sys.stderr)
        print(f"evidence: {OUT}", file=sys.stderr)
        raise SystemExit(1)
