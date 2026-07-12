#!/usr/bin/env python3
from __future__ import annotations

import bz2
import csv
import gzip
import hashlib
import io
import lzma
import os
import re
import shutil
import subprocess
import sys
import traceback
from collections import defaultdict
from pathlib import Path, PurePosixPath
from typing import Iterable, Iterator

N3_OUT = Path(os.environ["N3_OUT"])
SOURCE_REPO = Path(os.environ["SOURCE_REPO"])
OUT = Path(os.environ["OUT"])
PREFIX = Path(os.environ["PREFIX"])
REPO = Path(subprocess.check_output([
    "git", "-C", str(Path(__file__).resolve().parent), "rev-parse", "--show-toplevel"
], text=True).strip())
DPKG_STATUS = PREFIX / "var/lib/dpkg/status"
DPKG_INFO = PREFIX / "var/lib/dpkg/info"
APT_ETC = PREFIX / "etc/apt"
APT_LISTS = PREFIX / "var/lib/apt/lists"
APT_ARCHIVES = PREFIX / "var/cache/apt/archives"
stage = "initialization"

EXPECTED_N3_SUMMARY = {
    "raw_n2_census_rows": "26419",
    "raw_prefix_surface_rows": "27279",
    "normalized_census_rows": "1551",
    "capability_rows": "26",
    "selected_reference_rows": "161",
    "supplemental_rows": "20",
    "prefix_elf_rows_added": "911",
    "package_aggregate_rows": "86",
    "unowned_loader_state_rows": "2",
    "non_elf_surface_aggregate_rows": "345",
    "duplicate_normalized_row_ids": "0",
    "authority_decisions_accepted": "0",
}

SPECIAL_PRIORITY = {
    "termux-exec-glibc": "T0_PLATFORM_ADAPTATION",
    "glibc-runner": "T0_BOOTSTRAP_CONTEXT",
}

T0_PLATFORM_PACKAGES = {
    "glibc",
    "termux-exec-glibc",
    "libx11-glibc",
    "libxau-glibc",
    "libxcb-glibc",
    "libxdmcp-glibc",
    "libxext-glibc",
    "libxrandr-glibc",
    "libxrender-glibc",
    "libxshmfence-glibc",
}

APPROVED_SOURCE_REMOTES = {
    "https://github.com/termux-pacman/glibc-packages.git",
    "git@github.com:termux-pacman/glibc-packages.git",
    "ssh://git@github.com/termux-pacman/glibc-packages.git",
}

REQUIRED_N3_INPUTS = [
    "analysis.status",
    "next-state.txt",
    "summary.tsv",
    "claim-boundary.txt",
    "package-authority-pressure.tsv",
    "normalized-provider-authority-census.tsv",
    "unresolved-evidence-ledger.tsv",
]


def run(args: list[str], *, cwd: Path | None = None, check: bool = True, text: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(args, cwd=cwd, check=check, text=text, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def git(args: list[str], *, check: bool = True, text: bool = True) -> subprocess.CompletedProcess:
    return run(["git", "-C", str(SOURCE_REPO), *args], check=check, text=text)


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


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def bytes_sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def stable_id(prefix: str, value: str) -> str:
    return f"{prefix}:{hashlib.sha256(value.encode()).hexdigest()[:20]}"


def write_status(value: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "analysis.status").write_text(value + "\n")


def fail(stage_name: str, message: str, rc: int = 1) -> None:
    write_status("FAIL")
    (OUT / "failure-stage.txt").write_text(stage_name + "\n")
    print(message, file=sys.stderr)
    print(f"evidence: {OUT}", file=sys.stderr)
    raise SystemExit(rc)


def metadata_manifest(root: Path) -> str:
    digest = hashlib.sha256()
    if not root.is_dir():
        return "MISSING"
    for path in sorted(root.iterdir(), key=lambda item: item.name):
        try:
            metadata = path.lstat()
            line = f"{path.name}\0{metadata.st_mode:o}\0{metadata.st_size}\0{metadata.st_mtime_ns}\0"
        except OSError as exc:
            line = f"{path.name}\0ERROR\0{type(exc).__name__}\0"
        digest.update(line.encode(errors="surrogateescape"))
    return digest.hexdigest()


def tree_metadata_manifest(root: Path) -> str:
    digest = hashlib.sha256()
    if not root.is_dir():
        return "MISSING"
    for path in sorted(root.rglob("*"), key=lambda item: str(item.relative_to(root))):
        rel = str(path.relative_to(root))
        try:
            metadata = path.lstat()
            line = f"{rel}\0{metadata.st_mode:o}\0{metadata.st_size}\0{metadata.st_mtime_ns}\0"
        except OSError as exc:
            line = f"{rel}\0ERROR\0{type(exc).__name__}\0"
        digest.update(line.encode(errors="surrogateescape"))
    return digest.hexdigest()


def parse_deb822_text(text: str) -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    paragraph: dict[str, str] = {}
    current_key: str | None = None
    for line in text.splitlines() + [""]:
        if not line:
            if paragraph:
                records.append(paragraph)
            paragraph = {}
            current_key = None
            continue
        if line[0].isspace() and current_key:
            paragraph[current_key] += "\n" + line.strip()
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        current_key = key
        paragraph[key] = value.strip()
    return records


def parse_dpkg_status(path: Path) -> dict[tuple[str, str], dict[str, str]]:
    records: dict[tuple[str, str], dict[str, str]] = {}
    if not path.is_file():
        return records
    for record in parse_deb822_text(path.read_text(errors="replace")):
        package = record.get("Package")
        architecture = record.get("Architecture", "")
        if package:
            records[(package, architecture)] = record
    return records


def detect_compression(path: Path) -> str:
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


def read_maybe_compressed(path: Path) -> tuple[str, str, str]:
    compression = detect_compression(path)
    try:
        if compression == "gzip":
            data = gzip.open(path, "rb").read()
        elif compression == "bzip2":
            data = bz2.open(path, "rb").read()
        elif compression == "xz":
            data = lzma.open(path, "rb").read()
        elif compression == "lz4":
            command = shutil.which("lz4") or shutil.which("lz4cat")
            if not command:
                return compression, "UNSUPPORTED_NO_LZ4", ""
            args = [command, "-dc", str(path)] if Path(command).name == "lz4" else [command, str(path)]
            proc = subprocess.run(args, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if proc.returncode:
                return compression, f"DECOMPRESS_FAIL_RC_{proc.returncode}", ""
            data = proc.stdout
        elif compression == "zstd":
            command = shutil.which("zstd") or shutil.which("zstdcat")
            if not command:
                return compression, "UNSUPPORTED_NO_ZSTD", ""
            args = [command, "-dc", str(path)] if Path(command).name == "zstd" else [command, str(path)]
            proc = subprocess.run(args, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if proc.returncode:
                return compression, f"DECOMPRESS_FAIL_RC_{proc.returncode}", ""
            data = proc.stdout
        else:
            data = path.read_bytes()
        return compression, "PARSED", data.decode(errors="replace")
    except Exception as exc:
        return compression, f"READ_FAIL_{type(exc).__name__}", ""


def parse_summary(path: Path) -> dict[str, str]:
    return {row["field"]: row["value"] for row in read_tsv(path)}


def copy_verified_input(source: Path, embedded_name: str, rows: list[dict[str, object]]) -> None:
    if not source.is_file():
        fail("input_verification", f"missing required input: {source}")
    destination = OUT / "input" / embedded_name
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)
    expected = sha256(source)
    actual = sha256(destination)
    if expected != actual:
        fail("input_verification", f"embedded input hash mismatch: {source}")
    rows.append({
        "file": source.name,
        "source_path": str(source),
        "sha256": expected,
        "embedded_path": str(destination),
        "state": "PASS",
    })


def strip_shell_value(value: str) -> str:
    value = value.strip()
    if value.endswith(";"):
        value = value[:-1].rstrip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def parse_shell_assignments(text: str) -> dict[str, str]:
    result: dict[str, str] = {}
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        match = re.match(r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)$", line)
        if not match:
            i += 1
            continue
        key, value = match.group(1), match.group(2)
        # Join simple multi-line quoted assignments and arrays as raw text.
        quote = value[0] if value[:1] in {"'", '"'} else None
        while quote and not re.search(rf"(?<!\\){re.escape(quote)}\s*$", value) and i + 1 < len(lines):
            i += 1
            value += "\n" + lines[i]
        if value.startswith("(") and not value.rstrip().endswith(")"):
            while i + 1 < len(lines):
                i += 1
                value += "\n" + lines[i]
                if lines[i].rstrip().endswith(")"):
                    break
        result[key] = strip_shell_value(value)
        i += 1
    return result


def expand_recipe_value(value: str, version: str) -> str:
    if not value:
        return "-"
    expanded = value
    expanded = expanded.replace("${TERMUX_PKG_VERSION}", version).replace("$TERMUX_PKG_VERSION", version)
    expanded = expanded.replace("${TERMUX_PKG_VERSION:2}", version[2:] if len(version) >= 2 else "")
    return expanded


def recipe_full_version(assignments: dict[str, str]) -> tuple[str, str, str]:
    version = assignments.get("TERMUX_PKG_VERSION", "")
    revision = assignments.get("TERMUX_PKG_REVISION", "0") or "0"
    if not version or any(token in version for token in ("$", "`", "$(")):
        return version or "-", revision, "UNPARSED_DYNAMIC_VERSION"
    revision_clean = revision.strip('"\'')
    if revision_clean in {"", "0"}:
        return version, revision_clean or "0", "PARSED"
    if not re.fullmatch(r"[0-9]+", revision_clean):
        return version, revision_clean, "UNPARSED_DYNAMIC_REVISION"
    return f"{version}-{revision_clean}", revision_clean, "PARSED"


def package_name_for_recipe(recipe: str) -> str:
    if recipe in {"glibc", "glibc-runner"}:
        return recipe
    return f"{recipe}-glibc"


def package_name_for_subpackage(path: str, content: str) -> str:
    assignments = parse_shell_assignments(content)
    explicit = assignments.get("TERMUX_SUBPKG_NAME") or assignments.get("TERMUX_PKG_NAME")
    if explicit and not any(token in explicit for token in ("$", "`", "$(")):
        return explicit
    stem = Path(path).name.removesuffix(".subpackage.sh")
    if stem in {"glibc", "glibc-runner"} or stem.endswith("-glibc"):
        return stem
    return f"{stem}-glibc"


def git_show_bytes(commit: str, path: str) -> bytes | None:
    proc = git(["show", f"{commit}:{path}"], check=False, text=False)
    return proc.stdout if proc.returncode == 0 else None


def git_show_text(commit: str, path: str) -> str | None:
    data = git_show_bytes(commit, path)
    return data.decode(errors="replace") if data is not None else None


def source_repo_state() -> dict[str, str]:
    if not (SOURCE_REPO / ".git").exists():
        fail("source_repository", f"SOURCE_REPO is not a regular git checkout: {SOURCE_REPO}")
    remote = git(["remote", "get-url", "origin"]).stdout.strip()
    if remote not in APPROVED_SOURCE_REMOTES:
        fail("source_repository", f"unexpected source repository origin: {remote}")
    shallow = git(["rev-parse", "--is-shallow-repository"]).stdout.strip()
    if shallow != "false":
        fail("source_repository", "SOURCE_REPO must be a full non-shallow clone")
    dirty = git(["status", "--porcelain", "--untracked-files=all"]).stdout
    if dirty:
        fail("source_repository", "SOURCE_REPO must be clean, including untracked files")
    fsck = git(["fsck", "--connectivity-only", "--no-dangling"], check=False)
    if fsck.returncode:
        fail("source_repository", f"source repository fsck failed: {fsck.stderr.strip()}")
    head = git(["rev-parse", "HEAD"]).stdout.strip()
    branch = git(["symbolic-ref", "--quiet", "--short", "HEAD"], check=False).stdout.strip() or "DETACHED"
    commit_meta = git(["show", "-s", "--format=%H%x09%T%x09%P%x09%cI%x09%s", head]).stdout.rstrip("\n").split("\t", 4)
    refs = git(["for-each-ref", "--format=%(refname)%00%(objectname)%00%(objecttype)%00"]).stdout
    refs_sha = hashlib.sha256(refs.encode()).hexdigest()
    return {
        "path": str(SOURCE_REPO),
        "origin": remote,
        "head": head,
        "tree": commit_meta[1],
        "parents": commit_meta[2] or "-",
        "commit_time": commit_meta[3],
        "subject": commit_meta[4] if len(commit_meta) > 4 else "-",
        "branch": branch,
        "shallow": shallow,
        "worktree_state": "CLEAN",
        "fsck_state": "PASS",
        "refs_sha256": refs_sha,
    }


def build_recipe_index(head: str) -> tuple[dict[str, dict[str, str]], list[dict[str, str]]]:
    proc = git(["ls-tree", "-r", "--name-only", head, "--", "gpkg"])
    paths = [line for line in proc.stdout.splitlines() if line]
    build_paths = [path for path in paths if re.fullmatch(r"gpkg/[^/]+/build\.sh", path)]
    subpackage_paths = [path for path in paths if path.endswith(".subpackage.sh") and path.count("/") >= 2]
    index: dict[str, dict[str, str]] = {}
    rows: list[dict[str, str]] = []
    for build_path in build_paths:
        recipe = build_path.split("/")[1]
        package = package_name_for_recipe(recipe)
        index.setdefault(package, {
            "package": package,
            "recipe": recipe,
            "build_path": build_path,
            "subpackage_path": "-",
            "mapping_source": "MAIN_RECIPE_DIRECTORY",
        })
        rows.append(dict(index[package]))
    for sub_path in subpackage_paths:
        content = git_show_text(head, sub_path)
        if content is None:
            continue
        package = package_name_for_subpackage(sub_path, content)
        recipe = sub_path.split("/")[1]
        build_path = f"gpkg/{recipe}/build.sh"
        mapping = {
            "package": package,
            "recipe": recipe,
            "build_path": build_path,
            "subpackage_path": sub_path,
            "mapping_source": "SUBPACKAGE_FILENAME_OR_STATIC_NAME",
        }
        index[package] = mapping
        rows.append(mapping)
    return index, sorted(rows, key=lambda row: (row["package"], row["recipe"]))


def recipe_history_candidates(mapping: dict[str, str], installed_version: str) -> tuple[list[dict[str, str]], dict[str, str]]:
    # Search the complete recipe directory, not only build.sh/subpackage files.
    # Patch or auxiliary-file changes can alter the recipe tree without touching
    # the version declaration, and those distinct trees must remain candidates.
    recipe_root = f"gpkg/{mapping['recipe']}"
    log = git(["log", "--all", "--format=%H", "--", recipe_root]).stdout.splitlines()
    commits = list(dict.fromkeys(commit for commit in log if commit))
    candidates: list[dict[str, str]] = []
    current_info: dict[str, str] = {
        "current_version": "-",
        "current_parse_state": "NOT_READ",
        "current_source_url": "-",
        "current_source_sha256": "-",
    }
    current_build = git_show_text("HEAD", mapping["build_path"])
    if current_build is not None:
        assignments = parse_shell_assignments(current_build)
        current_version, _, parse_state = recipe_full_version(assignments)
        current_info = {
            "current_version": current_version,
            "current_parse_state": parse_state,
            "current_source_url": expand_recipe_value(assignments.get("TERMUX_PKG_SRCURL", "-"), assignments.get("TERMUX_PKG_VERSION", "")),
            "current_source_sha256": assignments.get("TERMUX_PKG_SHA256", "-"),
        }
    for commit in commits:
        build_content = git_show_text(commit, mapping["build_path"])
        if build_content is None:
            continue
        assignments = parse_shell_assignments(build_content)
        full_version, revision, parse_state = recipe_full_version(assignments)
        if parse_state != "PARSED" or full_version != installed_version:
            continue
        if mapping["subpackage_path"] != "-" and git_show_bytes(commit, mapping["subpackage_path"]) is None:
            continue
        tree_proc = git(["rev-parse", f"{commit}:gpkg/{mapping['recipe']}"], check=False)
        if tree_proc.returncode:
            continue
        meta = git(["show", "-s", "--format=%H%x09%T%x09%cI%x09%s", commit]).stdout.rstrip("\n").split("\t", 3)
        candidates.append({
            "commit": commit,
            "commit_tree": meta[1],
            "commit_time": meta[2],
            "commit_subject": meta[3] if len(meta) > 3 else "-",
            "recipe_tree": tree_proc.stdout.strip(),
            "recipe_version": full_version,
            "recipe_revision": revision,
            "parse_state": parse_state,
            "source_url": expand_recipe_value(assignments.get("TERMUX_PKG_SRCURL", "-"), assignments.get("TERMUX_PKG_VERSION", "")),
            "source_sha256": assignments.get("TERMUX_PKG_SHA256", "-"),
            "depends": assignments.get("TERMUX_PKG_DEPENDS", "-"),
            "build_depends": assignments.get("TERMUX_PKG_BUILD_DEPENDS", "-"),
            "recommends": assignments.get("TERMUX_PKG_RECOMMENDS", "-"),
        })
    # Preserve newest commit for each unique recipe tree.
    unique: dict[str, dict[str, str]] = {}
    for candidate in candidates:
        unique.setdefault(candidate["recipe_tree"], candidate)
    return list(unique.values()), current_info


def embed_recipe_tree(package: str, recipe: str, candidate: dict[str, str], embedded_trees: set[str], manifest_rows: list[dict[str, object]]) -> None:
    commit = candidate["commit"]
    tree = candidate["recipe_tree"]
    ls = git(["ls-tree", "-r", "-l", "-z", commit, "--", f"gpkg/{recipe}"], text=False).stdout
    entries = ls.split(b"\0")
    total_embedded = sum(int(row.get("size", 0)) for row in manifest_rows if row.get("embedded_state") == "EMBEDDED")
    for entry in entries:
        if not entry:
            continue
        header, raw_path = entry.split(b"\t", 1)
        parts = header.decode().split()
        mode, object_type, blob_sha = parts[:3]
        size = int(parts[3]) if len(parts) > 3 and parts[3] != "-" else -1
        path = raw_path.decode(errors="surrogateescape")
        relative = PurePosixPath(path).relative_to(PurePosixPath(f"gpkg/{recipe}"))
        role = "AUXILIARY"
        name = relative.name
        if name == "build.sh":
            role = "BUILD_RECIPE"
        elif name.endswith(".subpackage.sh"):
            role = "SUBPACKAGE_RECIPE"
        elif name.endswith((".patch", ".diff")):
            role = "PATCH"
        elif name.endswith((".c", ".cc", ".cpp", ".h", ".S", ".sh", ".json", ".txt")):
            role = "AUXILIARY_SOURCE_OR_SCRIPT"
        embedded_path = "-"
        content_sha = "-"
        embedded_state = "MANIFEST_ONLY"
        data = git_show_bytes(commit, path)
        if data is not None:
            content_sha = bytes_sha256(data)
            if size <= 5 * 1024 * 1024 and total_embedded + len(data) <= 100 * 1024 * 1024:
                destination = OUT / "recipe-trees" / tree / Path(*relative.parts)
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(data)
                embedded_path = str(destination)
                embedded_state = "EMBEDDED"
                total_embedded += len(data)
        manifest_rows.append({
            "package": package,
            "recipe": recipe,
            "candidate_commit": commit,
            "recipe_tree": tree,
            "path": path,
            "relative_path": str(relative),
            "git_mode": mode,
            "object_type": object_type,
            "blob_sha": blob_sha,
            "size": size,
            "content_sha256": content_sha,
            "role": role,
            "embedded_state": embedded_state,
            "embedded_path": embedded_path,
        })
    embedded_trees.add(tree)


def parse_apt_sources() -> tuple[list[dict[str, object]], list[Path]]:
    files: list[Path] = []
    direct = APT_ETC / "sources.list"
    if direct.is_file():
        files.append(direct)
    source_dir = APT_ETC / "sources.list.d"
    if source_dir.is_dir():
        files.extend(sorted(path for path in source_dir.iterdir() if path.is_file() and path.suffix in {".list", ".sources"}))
    rows: list[dict[str, object]] = []
    for path in sorted(files):
        text = path.read_text(errors="replace")
        if path.suffix == ".sources":
            records = parse_deb822_text(text)
            for number, record in enumerate(records, start=1):
                option_fields = []
                for key in ("Architectures", "Signed-By", "Trusted", "Check-Valid-Until"):
                    if record.get(key):
                        option_fields.append(f"{key}={record[key]}")
                rows.append({
                    "file": str(path),
                    "file_sha256": sha256(path),
                    "line_number": number,
                    "line_state": "PARSED_DEB822_STANZA",
                    "source_type": record.get("Types", "-"),
                    "options": ";".join(option_fields) or "-",
                    "uri": record.get("URIs", "-"),
                    "suite": record.get("Suites", "-"),
                    "components": record.get("Components", "-"),
                    "raw_line": ";".join(f"{key}={value}" for key, value in sorted(record.items())),
                })
            if not records:
                rows.append({
                    "file": str(path),
                    "file_sha256": sha256(path),
                    "line_number": 0,
                    "line_state": "EMPTY_OR_UNPARSED_DEB822_SOURCE",
                    "source_type": "-",
                    "options": "-",
                    "uri": "-",
                    "suite": "-",
                    "components": "-",
                    "raw_line": "-",
                })
            continue
        for number, line in enumerate(text.splitlines(), start=1):
            stripped = line.strip()
            state = "COMMENT_OR_BLANK"
            source_type = uri = suite = components = options = "-"
            if stripped and not stripped.startswith("#"):
                tokens = stripped.split()
                if tokens and tokens[0] in {"deb", "deb-src"}:
                    state = "PARSED"
                    source_type = tokens.pop(0)
                    if tokens and tokens[0].startswith("["):
                        opt_tokens = []
                        while tokens:
                            token = tokens.pop(0)
                            opt_tokens.append(token)
                            if token.endswith("]"):
                                break
                        options = " ".join(opt_tokens)
                    if tokens:
                        uri = tokens.pop(0)
                    if tokens:
                        suite = tokens.pop(0)
                    components = " ".join(tokens) if tokens else "-"
                else:
                    state = "UNPARSED_ACTIVE_LINE"
            rows.append({
                "file": str(path),
                "file_sha256": sha256(path),
                "line_number": number,
                "line_state": state,
                "source_type": source_type,
                "options": options,
                "uri": uri,
                "suite": suite,
                "components": components,
                "raw_line": line,
            })
    return rows, files


def apt_index_records() -> tuple[list[dict[str, object]], list[dict[str, str]], list[dict[str, object]]]:
    file_rows: list[dict[str, object]] = []
    package_records: list[dict[str, str]] = []
    release_rows: list[dict[str, object]] = []
    if not APT_LISTS.is_dir():
        return file_rows, package_records, release_rows
    for path in sorted(p for p in APT_LISTS.iterdir() if p.is_file()):
        name = path.name
        if "Packages" in name:
            compression, state, text = read_maybe_compressed(path)
            count = 0
            if state == "PARSED":
                records = parse_deb822_text(text)
                count = len(records)
                for record in records:
                    record = dict(record)
                    record["_index_file"] = str(path)
                    record["_index_sha256"] = sha256(path)
                    package_records.append(record)
            file_rows.append({
                "path": str(path),
                "name": name,
                "kind": "PACKAGES",
                "size": path.stat().st_size,
                "sha256": sha256(path),
                "compression": compression,
                "parse_state": state,
                "paragraphs": count,
            })
        elif name.endswith("InRelease") or name.endswith("Release"):
            text = path.read_text(errors="replace")
            # InRelease includes a signed preamble; parse only recognized top-level fields.
            fields: dict[str, str] = {}
            for line in text.splitlines():
                if re.match(r"^[A-Za-z][A-Za-z0-9-]*:", line):
                    key, value = line.split(":", 1)
                    fields[key] = value.strip()
            file_rows.append({
                "path": str(path),
                "name": name,
                "kind": "RELEASE",
                "size": path.stat().st_size,
                "sha256": sha256(path),
                "compression": "plain",
                "parse_state": "PARSED_FIELDS",
                "paragraphs": 1,
            })
            release_rows.append({
                "path": str(path),
                "sha256": sha256(path),
                "origin": fields.get("Origin", "-"),
                "label": fields.get("Label", "-"),
                "suite": fields.get("Suite", "-"),
                "codename": fields.get("Codename", "-"),
                "date": fields.get("Date", "-"),
                "valid_until": fields.get("Valid-Until", "-"),
                "architectures": fields.get("Architectures", "-"),
                "components": fields.get("Components", "-"),
            })
    return file_rows, package_records, release_rows


def cached_archives() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    if not APT_ARCHIVES.is_dir():
        return rows
    for path in sorted(APT_ARCHIVES.glob("*.deb")):
        rows.append({
            "path": str(path),
            "filename": path.name,
            "size": path.stat().st_size,
            "sha256": sha256(path),
        })
    return rows


def classify_priority(package_row: dict[str, str]) -> tuple[str, str]:
    package = package_row["package"]
    selected = int(package_row["selected_reference_paths"])
    edges = int(package_row["direct_consumer_edges"])
    if package in T0_PLATFORM_PACKAGES:
        return "T0_WORLD_PLATFORM", "WORLD_OR_PLATFORM_BOUNDARY"
    if selected > 0 or edges > 0:
        return "T1_SELECTED_RUNTIME_PRESSURE", "SELECTED_REFERENCE_OR_DIRECT_CONSUMER"
    if package in SPECIAL_PRIORITY:
        return SPECIAL_PRIORITY[package], "EXPLICIT_ARCHITECTURE_CONTEXT"
    return "T2_INSTALLED_CONTEXT", "INSTALLED_CONTEXT_ONLY"


def main() -> None:
    global stage
    OUT.mkdir(parents=True, exist_ok=False)
    write_status("IN_PROGRESS")

    stage = "n3_input_verification"
    input_rows: list[dict[str, object]] = []
    for name in REQUIRED_N3_INPUTS:
        copy_verified_input(N3_OUT / name, name, input_rows)
    if (N3_OUT / "analysis.status").read_text().strip() != "PASS":
        fail(stage, "N3 analysis.status is not PASS")
    if (N3_OUT / "next-state.txt").read_text().strip() != "READY_FOR_N3_SOURCE_RECIPE_AND_ARTIFACT_COMPARISON":
        fail(stage, "unexpected N3 next-state")
    n3_summary = parse_summary(N3_OUT / "summary.tsv")
    for field, expected in EXPECTED_N3_SUMMARY.items():
        if n3_summary.get(field) != expected:
            fail(stage, f"N3 summary mismatch for {field}: {n3_summary.get(field)!r} != {expected!r}")

    stage = "live_package_guard"
    n2_summary = parse_summary(N3_OUT / "input/summary.tsv") if (N3_OUT / "input/summary.tsv").is_file() else {}
    expected_status_sha = n2_summary.get("dpkg_status_sha256_after")
    expected_info_manifest = n2_summary.get("dpkg_info_manifest_after")
    if not expected_status_sha or not expected_info_manifest:
        fail(stage, "corrected N3 input does not expose accepted N2 dpkg guards")
    status_sha_before = sha256(DPKG_STATUS) if DPKG_STATUS.is_file() else "MISSING"
    info_manifest_before = metadata_manifest(DPKG_INFO)
    if status_sha_before != expected_status_sha:
        fail(stage, "live dpkg status changed since accepted N2 evidence")
    if info_manifest_before != expected_info_manifest:
        fail(stage, "live dpkg info metadata changed since accepted N2 evidence")

    stage = "source_repository_guard"
    source_before = source_repo_state()
    source_tree_manifest_before = tree_metadata_manifest(SOURCE_REPO / ".git/refs")

    stage = "package_identity"
    pressure_rows = read_tsv(N3_OUT / "package-authority-pressure.tsv")
    if len(pressure_rows) != 86:
        fail(stage, f"expected 86 package pressure rows, got {len(pressure_rows)}")
    status_records = parse_dpkg_status(DPKG_STATUS)
    installed_rows: list[dict[str, object]] = []
    priority_rows: list[dict[str, object]] = []
    package_by_name: dict[str, dict[str, str]] = {}
    for row in pressure_rows:
        package = row["package"]
        architecture = row["architecture"]
        record = status_records.get((package, architecture))
        if record is None:
            matches = [value for (candidate, _arch), value in status_records.items() if candidate == package]
            record = matches[0] if len(matches) == 1 else None
        if record is None:
            fail(stage, f"installed package missing from dpkg status: {package}:{architecture}")
        if record.get("Version") != row["version"] or record.get("Status") != row["status"]:
            fail(stage, f"package identity drift for {package}: N3={row['version']} {row['status']} live={record.get('Version')} {record.get('Status')}")
        package_by_name[package] = row
        tier, reason = classify_priority(row)
        installed_rows.append({
            "package": package,
            "version": row["version"],
            "architecture": architecture,
            "status": row["status"],
            "source_field": record.get("Source", "-"),
            "maintainer": record.get("Maintainer", "-"),
            "homepage": record.get("Homepage", "-"),
            "depends": record.get("Depends", "-"),
            "pre_depends": record.get("Pre-Depends", "-"),
            "recommends": record.get("Recommends", "-"),
            "provides": record.get("Provides", "-"),
            "conflicts": record.get("Conflicts", "-"),
            "breaks": record.get("Breaks", "-"),
            "replaces": record.get("Replaces", "-"),
            "installed_size": record.get("Installed-Size", "-"),
            "priority_tier": tier,
            "priority_reason": reason,
            "selected_reference_paths": row["selected_reference_paths"],
            "direct_consumer_edges": row["direct_consumer_edges"],
            "semantic_class_pressure": row["semantic_class_pressure"],
            "capability_group_pressure": row["capability_group_pressure"],
        })
        if tier != "T2_INSTALLED_CONTEXT":
            priority_rows.append(dict(installed_rows[-1]))
    if len([row for row in pressure_rows if int(row["selected_reference_paths"]) > 0 or int(row["direct_consumer_edges"]) > 0]) != 26:
        fail(stage, "selected-related package count is not 26")
    # Add specials that are present but not selected-related.
    priority_names = {str(row["package"]) for row in priority_rows}
    for package, tier in SPECIAL_PRIORITY.items():
        if package in package_by_name and package not in priority_names:
            base = next(row for row in installed_rows if row["package"] == package)
            extra = dict(base)
            extra["priority_tier"] = tier
            extra["priority_reason"] = "EXPLICIT_ARCHITECTURE_CONTEXT"
            priority_rows.append(extra)
            priority_names.add(package)

    stage = "apt_metadata"
    apt_source_rows, apt_source_files = parse_apt_sources()
    for path in apt_source_files:
        safe_name = "apt_source__" + re.sub(r"[^A-Za-z0-9_.-]+", "_", str(path.relative_to(APT_ETC)))
        copy_verified_input(path, safe_name, input_rows)
    apt_index_file_rows, apt_records, release_rows = apt_index_records()
    cache_rows = cached_archives()
    exact_records_by_package: dict[str, list[dict[str, str]]] = defaultdict(list)
    other_versions_by_package: dict[str, set[str]] = defaultdict(set)
    for record in apt_records:
        package = record.get("Package", "")
        if package not in package_by_name:
            continue
        if record.get("Version") == package_by_name[package]["version"]:
            exact_records_by_package[package].append(record)
        elif record.get("Version"):
            other_versions_by_package[package].add(record["Version"])
    repository_rows: list[dict[str, object]] = []
    for package_row in installed_rows:
        package = str(package_row["package"])
        matches = exact_records_by_package.get(package, [])
        if matches:
            for record in matches:
                repository_rows.append({
                    "package": package,
                    "installed_version": package_row["version"],
                    "architecture": package_row["architecture"],
                    "match_state": "EXACT_VERSION_INDEXED",
                    "index_file": record.get("_index_file", "-"),
                    "index_sha256": record.get("_index_sha256", "-"),
                    "filename": record.get("Filename", "-"),
                    "size": record.get("Size", "-"),
                    "sha256": record.get("SHA256", "-"),
                    "md5sum": record.get("MD5sum", "-"),
                    "source": record.get("Source", "-"),
                    "depends": record.get("Depends", "-"),
                    "homepage": record.get("Homepage", "-"),
                    "other_indexed_versions": ";".join(sorted(other_versions_by_package.get(package, set()))) or "-",
                })
        else:
            repository_rows.append({
                "package": package,
                "installed_version": package_row["version"],
                "architecture": package_row["architecture"],
                "match_state": "PACKAGE_ONLY_OTHER_VERSION" if other_versions_by_package.get(package) else "NOT_FOUND_IN_PARSED_INDEX",
                "index_file": "-",
                "index_sha256": "-",
                "filename": "-",
                "size": "-",
                "sha256": "-",
                "md5sum": "-",
                "source": "-",
                "depends": "-",
                "homepage": "-",
                "other_indexed_versions": ";".join(sorted(other_versions_by_package.get(package, set()))) or "-",
            })

    stage = "recipe_index"
    recipe_index, recipe_mapping_rows = build_recipe_index(source_before["head"])
    recipe_lineage_rows: list[dict[str, object]] = []
    candidate_rows: list[dict[str, object]] = []
    recipe_file_rows: list[dict[str, object]] = []
    ledger_rows: list[dict[str, object]] = []
    embedded_trees: set[str] = set()
    repository_state_by_package = defaultdict(list)
    for row in repository_rows:
        repository_state_by_package[str(row["package"])].append(row)

    for package_row in sorted(priority_rows, key=lambda row: (str(row["priority_tier"]), str(row["package"]))):
        package = str(package_row["package"])
        installed_version = str(package_row["version"])
        mapping = recipe_index.get(package)
        if mapping is None:
            recipe_lineage_rows.append({
                "package": package,
                "installed_version": installed_version,
                "priority_tier": package_row["priority_tier"],
                "recipe_mapping_state": "NOT_FOUND",
                "recipe": "-",
                "build_path": "-",
                "subpackage_path": "-",
                "current_recipe_version": "-",
                "current_recipe_parse_state": "-",
                "candidate_recipe_trees": "0",
                "candidate_commits": "0",
                "lineage_state": "RECIPE_MAPPING_NOT_FOUND",
            })
            ledger_rows.append({
                "package": package,
                "priority_tier": package_row["priority_tier"],
                "installed_version": installed_version,
                "apt_artifact_state": repository_state_by_package[package][0]["match_state"] if repository_state_by_package[package] else "NO_INDEX_RECORD",
                "recipe_lineage_state": "RECIPE_MAPPING_NOT_FOUND",
                "candidate_recipe_trees": 0,
                "cached_deb_candidates": 0,
                "authority_decision_state": "OPEN",
                "next_permitted_action": "RESOLVE_PACKAGE_TO_SOURCE_RECIPE_MAPPING",
            })
            continue
        candidates, current_info = recipe_history_candidates(mapping, installed_version)
        candidate_trees = {candidate["recipe_tree"] for candidate in candidates}
        lineage_state = "RECIPE_VERSION_NOT_FOUND"
        if len(candidate_trees) == 1:
            lineage_state = "RECIPE_VERSION_UNIQUE_TREE_MATCH"
        elif len(candidate_trees) > 1:
            lineage_state = "RECIPE_VERSION_MULTIPLE_TREE_MATCH"
        recipe_lineage_rows.append({
            "package": package,
            "installed_version": installed_version,
            "priority_tier": package_row["priority_tier"],
            "recipe_mapping_state": "FOUND",
            "recipe": mapping["recipe"],
            "build_path": mapping["build_path"],
            "subpackage_path": mapping["subpackage_path"],
            "current_recipe_version": current_info["current_version"],
            "current_recipe_parse_state": current_info["current_parse_state"],
            "current_source_url": current_info["current_source_url"],
            "current_source_sha256": current_info["current_source_sha256"],
            "candidate_recipe_trees": len(candidate_trees),
            "candidate_commits": len(candidates),
            "lineage_state": lineage_state,
        })
        for candidate in candidates:
            candidate_rows.append({
                "package": package,
                "installed_version": installed_version,
                "priority_tier": package_row["priority_tier"],
                "recipe": mapping["recipe"],
                "build_path": mapping["build_path"],
                "subpackage_path": mapping["subpackage_path"],
                **candidate,
            })
            if candidate["recipe_tree"] not in embedded_trees:
                embed_recipe_tree(package, mapping["recipe"], candidate, embedded_trees, recipe_file_rows)
        apt_states = repository_state_by_package.get(package, [])
        apt_state = "EXACT_VERSION_INDEXED" if any(row["match_state"] == "EXACT_VERSION_INDEXED" for row in apt_states) else (apt_states[0]["match_state"] if apt_states else "NO_INDEX_RECORD")
        cached_count = sum(1 for row in cache_rows if package.replace("+", "%2b") in str(row["filename"]) and installed_version.replace(":", "%3a") in str(row["filename"]))
        if lineage_state == "RECIPE_VERSION_UNIQUE_TREE_MATCH" and apt_state == "EXACT_VERSION_INDEXED":
            next_action = "BOUND_BINARY_ARTIFACT_ACQUISITION_OR_CACHED_ARTIFACT_COMPARE"
        elif lineage_state == "RECIPE_VERSION_MULTIPLE_TREE_MATCH":
            next_action = "RESOLVE_RECIPE_TREE_WITH_BUILD_OR_BINARY_EVIDENCE"
        elif lineage_state == "RECIPE_VERSION_NOT_FOUND":
            next_action = "LOCATE_HISTORICAL_RECIPE_OR_MIRROR_LINEAGE"
        else:
            next_action = "RESOLVE_REPOSITORY_ARTIFACT_METADATA"
        ledger_rows.append({
            "package": package,
            "priority_tier": package_row["priority_tier"],
            "installed_version": installed_version,
            "apt_artifact_state": apt_state,
            "recipe_lineage_state": lineage_state,
            "candidate_recipe_trees": len(candidate_trees),
            "cached_deb_candidates": cached_count,
            "authority_decision_state": "OPEN",
            "next_permitted_action": next_action,
        })

    stage = "write_outputs"
    write_tsv(OUT / "input-verification.tsv", ["file", "source_path", "sha256", "embedded_path", "state"], input_rows)
    write_tsv(OUT / "source-repository-state.tsv", list(source_before.keys()), [source_before])
    write_tsv(OUT / "recipe-package-map.tsv", ["package", "recipe", "build_path", "subpackage_path", "mapping_source"], recipe_mapping_rows)
    write_tsv(OUT / "installed-package-lineage.tsv", list(installed_rows[0].keys()), installed_rows)
    write_tsv(OUT / "priority-package-set.tsv", list(priority_rows[0].keys()), sorted(priority_rows, key=lambda row: (str(row["priority_tier"]), str(row["package"]))))
    write_tsv(OUT / "apt-source-lines.tsv", ["file", "file_sha256", "line_number", "line_state", "source_type", "options", "uri", "suite", "components", "raw_line"], apt_source_rows)
    write_tsv(OUT / "apt-index-files.tsv", ["path", "name", "kind", "size", "sha256", "compression", "parse_state", "paragraphs"], apt_index_file_rows)
    write_tsv(OUT / "apt-release-metadata.tsv", ["path", "sha256", "origin", "label", "suite", "codename", "date", "valid_until", "architectures", "components"], release_rows)
    write_tsv(OUT / "repository-package-records.tsv", ["package", "installed_version", "architecture", "match_state", "index_file", "index_sha256", "filename", "size", "sha256", "md5sum", "source", "depends", "homepage", "other_indexed_versions"], repository_rows)
    write_tsv(OUT / "cached-deb-artifacts.tsv", ["path", "filename", "size", "sha256"], cache_rows)
    write_tsv(OUT / "priority-recipe-lineage.tsv", ["package", "installed_version", "priority_tier", "recipe_mapping_state", "recipe", "build_path", "subpackage_path", "current_recipe_version", "current_recipe_parse_state", "current_source_url", "current_source_sha256", "candidate_recipe_trees", "candidate_commits", "lineage_state"], recipe_lineage_rows)
    write_tsv(OUT / "recipe-candidate-commits.tsv", ["package", "installed_version", "priority_tier", "recipe", "build_path", "subpackage_path", "commit", "commit_tree", "commit_time", "commit_subject", "recipe_tree", "recipe_version", "recipe_revision", "parse_state", "source_url", "source_sha256", "depends", "build_depends", "recommends"], candidate_rows)
    write_tsv(OUT / "recipe-file-manifest.tsv", ["package", "recipe", "candidate_commit", "recipe_tree", "path", "relative_path", "git_mode", "object_type", "blob_sha", "size", "content_sha256", "role", "embedded_state", "embedded_path"], recipe_file_rows)
    write_tsv(OUT / "source-comparison-ledger.tsv", ["package", "priority_tier", "installed_version", "apt_artifact_state", "recipe_lineage_state", "candidate_recipe_trees", "cached_deb_candidates", "authority_decision_state", "next_permitted_action"], ledger_rows)

    stage = "after_guards"
    status_sha_after = sha256(DPKG_STATUS) if DPKG_STATUS.is_file() else "MISSING"
    info_manifest_after = metadata_manifest(DPKG_INFO)
    source_after = source_repo_state()
    source_tree_manifest_after = tree_metadata_manifest(SOURCE_REPO / ".git/refs")
    if status_sha_after != status_sha_before or info_manifest_after != info_manifest_before:
        fail(stage, "live dpkg state changed during source evidence collection")
    if source_after != source_before or source_tree_manifest_after != source_tree_manifest_before:
        fail(stage, "source repository state changed during evidence collection")

    summary_rows = [
        {"field": "branch", "value": run(["git", "-C", str(REPO), "rev-parse", "--abbrev-ref", "HEAD"]).stdout.strip()},
        {"field": "head", "value": run(["git", "-C", str(REPO), "rev-parse", "HEAD"]).stdout.strip()},
        {"field": "n3_root", "value": str(N3_OUT)},
        {"field": "n3_head", "value": n3_summary.get("head", "-")},
        {"field": "source_repo", "value": str(SOURCE_REPO)},
        {"field": "source_repo_head", "value": source_before["head"]},
        {"field": "source_repo_recipe_tree_evidence", "value": len(embedded_trees)},
        {"field": "installed_packages", "value": len(installed_rows)},
        {"field": "selected_related_packages", "value": 26},
        {"field": "priority_packages", "value": len(priority_rows)},
        {"field": "recipe_mappings_found", "value": sum(1 for row in recipe_lineage_rows if row["recipe_mapping_state"] == "FOUND")},
        {"field": "unique_recipe_tree_matches", "value": sum(1 for row in recipe_lineage_rows if row["lineage_state"] == "RECIPE_VERSION_UNIQUE_TREE_MATCH")},
        {"field": "multiple_recipe_tree_matches", "value": sum(1 for row in recipe_lineage_rows if row["lineage_state"] == "RECIPE_VERSION_MULTIPLE_TREE_MATCH")},
        {"field": "recipe_versions_not_found", "value": sum(1 for row in recipe_lineage_rows if row["lineage_state"] == "RECIPE_VERSION_NOT_FOUND")},
        {"field": "recipe_mappings_not_found", "value": sum(1 for row in recipe_lineage_rows if row["lineage_state"] == "RECIPE_MAPPING_NOT_FOUND")},
        {"field": "exact_repository_package_records", "value": sum(1 for package in package_by_name if exact_records_by_package.get(package))},
        {"field": "parsed_apt_package_records", "value": len(apt_records)},
        {"field": "apt_index_files", "value": len(apt_index_file_rows)},
        {"field": "apt_source_files", "value": len(apt_source_files)},
        {"field": "cached_deb_artifacts", "value": len(cache_rows)},
        {"field": "recipe_candidate_commits", "value": len(candidate_rows)},
        {"field": "recipe_file_manifest_rows", "value": len(recipe_file_rows)},
        {"field": "dpkg_status_sha256_before", "value": status_sha_before},
        {"field": "dpkg_status_sha256_after", "value": status_sha_after},
        {"field": "dpkg_info_manifest_before", "value": info_manifest_before},
        {"field": "dpkg_info_manifest_after", "value": info_manifest_after},
        {"field": "source_repo_head_before", "value": source_before["head"]},
        {"field": "source_repo_head_after", "value": source_after["head"]},
        {"field": "source_repo_refs_sha256_before", "value": source_before["refs_sha256"]},
        {"field": "source_repo_refs_sha256_after", "value": source_after["refs_sha256"]},
        {"field": "package_operation_performed", "value": "NO"},
        {"field": "package_download_performed", "value": "NO"},
        {"field": "runtime_launch_performed", "value": "NO"},
        {"field": "generation_operation_performed", "value": "NO"},
        {"field": "current_operation_performed", "value": "NO"},
        {"field": "source_repo_fetch_performed", "value": "NO"},
        {"field": "authority_decisions_accepted", "value": "0"},
    ]
    write_tsv(OUT / "summary.tsv", ["field", "value"], summary_rows)
    (OUT / "claim-boundary.txt").write_text(
        "This stage correlates the accepted corrected N3 package pressure with unchanged live dpkg/APT metadata and a clean, full local clone of the termux-pacman glibc-packages source repository.\n"
        "It records recipe-history candidates, source declarations, patch/auxiliary recipe trees, and indexed binary artifact metadata.\n"
        "It performs no apt update, package download, install, remove, upgrade, maintainer-script execution, runtime launch, generation operation, current operation, source-repository fetch, provider selection, or successor composition.\n"
    )
    (OUT / "next-state.txt").write_text("READY_FOR_BOUNDED_BINARY_ARTIFACT_ACQUISITION_AND_RECIPE_REVIEW\n")
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
        print(f"source evidence collector failed during {stage}: {exc}", file=sys.stderr)
        print(f"evidence: {OUT}", file=sys.stderr)
        raise SystemExit(1)
