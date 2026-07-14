#!/usr/bin/env python3
"""Produce one strict SUP-02 custodian-export candidate response from an instrumented build.

This program runs in the producing build environment. It does not accept build
attestation, provider authority, or target population. It emits only the exact
three-record candidate response consumed by the bounded 0163 acquirer, plus an
audit directory kept outside the response root.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import os
import platform
import re
import shlex
import shutil
import stat
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path, PurePosixPath
from typing import Any, Iterable, NoReturn

EXPECTED_REQUESTS = 28
EXPECTED_CONTRACTS = 84
RECORD_NAMES = (
    "build-invocation-record.json",
    "build-environment-record.json",
    "build-output-manifest.tsv",
)
RESPONSE_MANIFEST = "custodian-export-response-manifest.tsv"
CLAIM_BOUNDARY = (
    "CANDIDATE_CUSTODIAN_EXPORT_RESPONSE_REVIEW_REQUIRED_"
    "NO_BUILD_ATTESTATION_OR_AUTHORITY_EFFECT"
)
SAFE_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
GIT_OID_RE = re.compile(r"^[0-9a-f]{40}$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
UTC_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
MAX_ARTIFACTS = 64
MAX_MEMBERS = 200_000
MAX_MEMBER_SIZE = 512 * 1024 * 1024
MAX_TOTAL_MEMBER_BYTES = 8 * 1024 * 1024 * 1024
DEFAULT_ENV_KEYS = (
    "ANDROID_HOME",
    "ANDROID_NDK_HOME",
    "ANDROID_NDK_LATEST_HOME",
    "ANDROID_SDK_ROOT",
    "ARCH",
    "CI",
    "GITHUB_ACTION",
    "GITHUB_ACTIONS",
    "GITHUB_JOB",
    "GITHUB_REF",
    "GITHUB_REPOSITORY",
    "GITHUB_RUN_ATTEMPT",
    "GITHUB_RUN_ID",
    "GITHUB_RUN_NUMBER",
    "GITHUB_SHA",
    "LANG",
    "LC_ALL",
    "NDK",
    "SOURCE_DATE_EPOCH",
    "TERMUX_ARCH",
    "TERMUX_BUILDER_IMAGE_NAME",
)
SECRET_NAME_RE = re.compile(r"(TOKEN|SECRET|PASSWORD|PASSWD|PRIVATE|CREDENTIAL|AUTH|COOKIE|KEY)$", re.I)
OUTPUT_FIELDS = [
    "request_id",
    "root_review_id",
    "recipe_root",
    "recipe_tree",
    "build_run_id",
    "package_name",
    "package_version",
    "package_revision",
    "artifact_path",
    "artifact_sha256",
    "member_path",
    "member_sha256",
    "member_elf_soname",
    "custodian_identity",
    "immutable_locator_or_signed_envelope",
]
RESPONSE_MANIFEST_FIELDS = [
    "response_record_id",
    "request_id",
    "root_review_id",
    "recipe_root",
    "recipe_tree",
    "record_name",
    "relative_path",
    "sha256",
    "size_bytes",
    "custodian_identity",
    "immutable_locator_or_signed_envelope",
    "claim_boundary",
]


def fail(message: str) -> NoReturn:
    raise SystemExit(f"SUP-02 custodian-export response producer: FAIL: {message}")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ")


def run_text(argv: list[str], *, cwd: Path | None = None, check: bool = True) -> str:
    proc = subprocess.run(
        argv,
        cwd=cwd,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if check and proc.returncode != 0:
        fail(f"command failed ({proc.returncode}): {shlex.join(argv)}\n{proc.stderr[-4000:]}")
    return proc.stdout.strip()


def read_tsv(path: Path) -> list[dict[str, str]]:
    if not path.is_file() or path.is_symlink():
        fail(f"missing regular TSV: {path}")
    with path.open("r", encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream, delimiter="\t")
        if not reader.fieldnames:
            fail(f"missing TSV header: {path}")
        return [{key: value or "" for key, value in row.items()} for row in reader]


def write_tsv(path: Path, fields: list[str], rows: Iterable[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(
            stream,
            fieldnames=fields,
            delimiter="\t",
            lineterminator="\n",
            extrasaction="ignore",
        )
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.write_text(json.dumps(value, sort_keys=True, indent=2) + "\n", encoding="utf-8")


def safe_text(value: str, label: str, *, limit: int = 8192) -> str:
    if not value or len(value) > limit or any(ord(ch) < 32 for ch in value):
        fail(f"invalid {label}")
    return value


def safe_relative(value: str, label: str) -> PurePosixPath:
    path = PurePosixPath(value)
    if not value or path.is_absolute() or ".." in path.parts or any(part in {"", "."} for part in path.parts):
        fail(f"unsafe {label}: {value!r}")
    return path


def verify_contracts(
    request_rows: list[dict[str, str]], contract_rows: list[dict[str, str]], request_id: str
) -> tuple[dict[str, str], dict[str, dict[str, str]]]:
    if len(request_rows) != EXPECTED_REQUESTS:
        fail(f"request denominator drift: {len(request_rows)} != {EXPECTED_REQUESTS}")
    if len(contract_rows) != EXPECTED_CONTRACTS:
        fail(f"record-contract denominator drift: {len(contract_rows)} != {EXPECTED_CONTRACTS}")
    request_by_id: dict[str, dict[str, str]] = {}
    for row in request_rows:
        rid = row.get("request_id", "")
        if not SAFE_ID_RE.fullmatch(rid) or rid in request_by_id:
            fail(f"invalid or duplicate request ID: {rid!r}")
        if row.get("batch_id") != "SUP-02" or row.get("requirement_ids") != "BA-001;BA-002;BA-003":
            fail(f"request batch or requirement drift: {rid}")
        if row.get("request_state") != "REQUEST_ISSUED_REPOSITORY_PUBLICATION":
            fail(f"request is not issued: {rid}")
        if row.get("acknowledgement_state") != "NOT_ACKNOWLEDGED":
            fail(f"unexpected pre-existing acknowledgement: {rid}")
        if row.get("required_record_names") != ";".join(RECORD_NAMES):
            fail(f"record-name contract drift: {rid}")
        if not GIT_OID_RE.fullmatch(row.get("recipe_tree", "")):
            fail(f"invalid recipe tree: {rid}")
        safe_text(row.get("root_review_id", ""), f"root review ID {rid}")
        safe_relative(row.get("recipe_root", ""), f"recipe root {rid}")
        request_by_id[rid] = row
    if request_id not in request_by_id:
        fail(f"unknown request ID: {request_id}")
    contracts: dict[str, dict[str, str]] = {}
    per_request: dict[str, int] = {rid: 0 for rid in request_by_id}
    for row in contract_rows:
        rid = row.get("request_id", "")
        name = row.get("record_name", "")
        if rid not in request_by_id:
            fail(f"orphan contract: {rid}/{name}")
        if name not in RECORD_NAMES:
            fail(f"unknown record name: {rid}/{name}")
        per_request[rid] += 1
        if rid == request_id:
            if name in contracts:
                fail(f"duplicate selected contract: {name}")
            request = request_by_id[rid]
            for field in ("root_review_id", "recipe_root", "recipe_tree"):
                if row.get(field) != request.get(field):
                    fail(f"selected contract binding drift: {name}/{field}")
            if row.get("record_state") != "ISSUED_REQUIRED_NOT_SUPPLIED" or row.get("acceptance_state") != "OPEN_NO_ACCEPTANCE":
                fail(f"selected contract state drift: {name}")
            contracts[name] = row
    if any(count != 3 for count in per_request.values()) or set(contracts) != set(RECORD_NAMES):
        fail("per-request record-contract denominator drift")
    return request_by_id[request_id], contracts


def git_value(repo: Path, *args: str) -> str:
    return run_text(["git", "-C", str(repo), *args])


def recipe_manifest(repo: Path, recipe_root: str) -> tuple[str, list[dict[str, str]]]:
    root = repo / Path(recipe_root)
    if not root.is_dir() or root.is_symlink():
        fail(f"missing regular recipe directory: {root}")
    rows: list[dict[str, str]] = []
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(repo).as_posix()
        mode = path.lstat().st_mode
        if stat.S_ISLNK(mode):
            target = os.readlink(path)
            digest = sha256_bytes(("SYMLINK\0" + target).encode("utf-8"))
            kind = "symlink"
        elif stat.S_ISREG(mode):
            digest = sha256_file(path)
            kind = "file"
        elif stat.S_ISDIR(mode):
            continue
        else:
            fail(f"unsupported recipe member type: {rel}")
        rows.append({"path": rel, "kind": kind, "sha256": digest})
    if not rows:
        fail("empty recipe file manifest")
    payload = "".join(f"{row['sha256']}\t{row['kind']}\t{row['path']}\n" for row in rows).encode("utf-8")
    return sha256_bytes(payload), rows


def command_version(path: str) -> str:
    candidates = ([path, "--version"], [path, "-version"], [path, "-V"])
    for argv in candidates:
        proc = subprocess.run(
            argv,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        text = proc.stdout.strip()
        if text:
            return text.splitlines()[0][:500]
    return "version-unavailable"


def toolchain_snapshot() -> tuple[dict[str, str], dict[str, str]]:
    names = ("bash", "cc", "clang", "gcc", "ld", "cmake", "meson", "ninja", "make", "python3", "readelf", "tar", "zstd", "xz")
    components: dict[str, str] = {}
    digests: dict[str, str] = {}
    for name in names:
        resolved = shutil.which(name)
        if not resolved:
            continue
        real = str(Path(resolved).resolve())
        components[name] = f"{real} :: {command_version(real)}"
        digests[name] = sha256_file(Path(real))
    if not components or not digests:
        fail("empty toolchain snapshot")
    return components, digests


def environment_snapshot(extra_keys: list[str]) -> dict[str, str]:
    keys = sorted(set(DEFAULT_ENV_KEYS).union(extra_keys))
    result: dict[str, str] = {}
    for key in keys:
        if SECRET_NAME_RE.search(key):
            fail(f"refusing secret-like environment key: {key}")
        if key in os.environ:
            value = os.environ[key]
            if any(ord(ch) < 32 and ch not in "\t" for ch in value):
                fail(f"control character in environment value: {key}")
            result[key] = value[:8192]
    return result or {"capture": "no allowlisted environment values were set"}


def dependency_snapshot(audit_dir: Path) -> dict[str, object]:
    candidates = [
        ("dpkg", ["dpkg-query", "-W", "-f=${binary:Package}\t${Version}\n"]),
        ("pacman", ["pacman", "-Q"]),
        ("rpm", ["rpm", "-qa", "--qf", "%{NAME}\t%{VERSION}-%{RELEASE}\n"]),
    ]
    for kind, argv in candidates:
        if not shutil.which(argv[0]):
            continue
        proc = subprocess.run(
            argv, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, encoding="utf-8", errors="replace", check=False
        )
        if proc.returncode != 0 or not proc.stdout.strip():
            continue
        lines = sorted(set(line for line in proc.stdout.splitlines() if line))
        payload = ("\n".join(lines) + "\n").encode("utf-8")
        path = audit_dir / f"system-package-snapshot-{kind}.tsv"
        path.write_bytes(payload)
        return {
            "kind": kind,
            "relative_path": path.name,
            "sha256": sha256_bytes(payload),
            "row_count": len(lines),
        }
    fail("no supported non-empty system package snapshot (dpkg, pacman, or rpm)")


def collect_regular_globs(working_directory: Path, patterns: list[str], label: str, maximum: int) -> list[dict[str, object]]:
    found: dict[Path, str] = {}
    for pattern in patterns:
        safe_text(pattern, f"{label} glob")
        candidate = Path(pattern)
        if candidate.is_absolute() or ".." in candidate.parts:
            fail(f"{label} glob must be relative and bounded: {pattern}")
        for path in working_directory.glob(pattern):
            resolved = path.resolve()
            try:
                relative = resolved.relative_to(working_directory.resolve()).as_posix()
            except ValueError:
                fail(f"{label} escaped working directory: {path}")
            if path.is_file() and not path.is_symlink():
                found[resolved] = relative
    if not found:
        fail(f"{label} globs matched no regular files")
    if len(found) > maximum:
        fail(f"{label} count outside bound: {len(found)}")
    return [
        {"relative_path": relative, "sha256": sha256_file(path), "size_bytes": path.stat().st_size}
        for path, relative in sorted(found.items(), key=lambda item: item[1])
    ]


def os_snapshot() -> str:
    path = Path("/etc/os-release")
    if path.is_file() and not path.is_symlink():
        values: dict[str, str] = {}
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            if "=" not in line:
                continue
            key, value = line.split("=", 1)
            values[key] = value.strip().strip('"')
        return f"{values.get('ID', 'unknown')} {values.get('VERSION_ID', values.get('VERSION', 'unknown'))}"
    return platform.platform()


def decompressed_tar(artifact: Path, temp: Path) -> Path:
    name = artifact.name
    if name.endswith((".tar.gz", ".tgz", ".tar.bz2", ".tbz2", ".tar.xz", ".txz", ".tar")):
        return artifact
    if name.endswith((".tar.zst", ".tar.zstd", ".pkg.tar.zst")):
        zstd = shutil.which("zstd")
        if not zstd:
            fail("zstd is required for .zst package artifacts")
        target = temp / (artifact.name + ".decompressed.tar")
        with target.open("wb") as stream:
            proc = subprocess.run([zstd, "-q", "-d", "-c", str(artifact)], stdin=subprocess.DEVNULL, stdout=stream, stderr=subprocess.PIPE, check=False)
        if proc.returncode != 0:
            fail(f"zstd decompression failed: {artifact}: {proc.stderr.decode(errors='replace')[-2000:]}")
        return target
    fail(f"unsupported package archive suffix: {artifact}")


def parse_pkginfo(data: bytes, artifact: Path) -> tuple[str, str, str]:
    values: dict[str, list[str]] = {}
    for raw in data.decode("utf-8", errors="strict").splitlines():
        if " = " not in raw:
            continue
        key, value = raw.split(" = ", 1)
        values.setdefault(key, []).append(value)
    name = (values.get("pkgname") or [""])[0]
    full = (values.get("pkgver") or [""])[0]
    if not name or not full:
        fail(f"missing pkgname/pkgver in .PKGINFO: {artifact}")
    version, revision = full, "-"
    if "-" in full:
        prefix, suffix = full.rsplit("-", 1)
        if suffix and all(part.isdigit() for part in suffix.split(".")):
            version, revision = prefix, suffix
    return name, version, revision


def elf_soname(data: bytes, temp: Path) -> str:
    if not data.startswith(b"\x7fELF"):
        return "-"
    readelf = shutil.which("readelf")
    if not readelf:
        fail("readelf is required to retain ELF SONAME")
    path = temp / f"member-{sha256_bytes(data)}.elf"
    path.write_bytes(data)
    proc = subprocess.run([readelf, "-d", str(path)], stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="replace", check=False)
    if proc.returncode != 0:
        fail(f"readelf failed for ELF member: {proc.stderr[-2000:]}")
    match = re.search(r"\(SONAME\).*?\[([^\]]+)\]", proc.stdout)
    return match.group(1) if match else "-"


def inventory_artifact(artifact: Path, artifact_path: str, request: dict[str, str], common: dict[str, str], temp: Path) -> list[dict[str, str]]:
    if not artifact.is_file() or artifact.is_symlink():
        fail(f"artifact is not a regular file: {artifact}")
    artifact_sha = sha256_file(artifact)
    archive = decompressed_tar(artifact, temp)
    rows: list[dict[str, str]] = []
    total_bytes = 0
    package: tuple[str, str, str] | None = None
    seen: set[str] = set()
    with tarfile.open(archive, mode="r:*") as tf:
        members = tf.getmembers()
        if len(members) > MAX_MEMBERS:
            fail(f"artifact member count outside bound: {artifact}")
        for member in members:
            normalized = member.name[2:] if member.name.startswith("./") else member.name
            path = safe_relative(normalized, f"archive member in {artifact.name}")
            canonical = path.as_posix()
            if canonical in seen:
                fail(f"duplicate artifact member: {artifact.name}:{canonical}")
            seen.add(canonical)
            if member.isdir():
                continue
            if member.isreg():
                if member.size < 0 or member.size > MAX_MEMBER_SIZE:
                    fail(f"member size outside bound: {artifact.name}:{canonical}")
                total_bytes += member.size
                if total_bytes > MAX_TOTAL_MEMBER_BYTES:
                    fail(f"artifact expanded byte total outside bound: {artifact}")
                source = tf.extractfile(member)
                if source is None:
                    fail(f"unable to stream regular member: {artifact.name}:{canonical}")
                data = source.read(MAX_MEMBER_SIZE + 1)
                if len(data) != member.size:
                    fail(f"member size mismatch: {artifact.name}:{canonical}")
                if canonical in {".PKGINFO", ".MTREE"} or canonical.endswith("/.PKGINFO"):
                    if canonical.endswith(".PKGINFO"):
                        package = parse_pkginfo(data, artifact)
                digest = sha256_bytes(data)
                soname = elf_soname(data, temp)
            elif member.issym():
                target = safe_text(member.linkname, f"symlink target {artifact.name}:{canonical}")
                digest = sha256_bytes(("SYMLINK\0" + target).encode("utf-8"))
                soname = "-"
            elif member.islnk():
                target = safe_text(member.linkname, f"hardlink target {artifact.name}:{canonical}")
                digest = sha256_bytes(("HARDLINK\0" + target).encode("utf-8"))
                soname = "-"
            else:
                fail(f"unsupported artifact member type: {artifact.name}:{canonical}")
            rows.append(
                {
                    "request_id": request["request_id"],
                    "root_review_id": request["root_review_id"],
                    "recipe_root": request["recipe_root"],
                    "recipe_tree": request["recipe_tree"],
                    "build_run_id": common["build_run_id"],
                    "package_name": "__PENDING_PKGINFO__",
                    "package_version": "__PENDING_PKGINFO__",
                    "package_revision": "__PENDING_PKGINFO__",
                    "artifact_path": artifact_path,
                    "artifact_sha256": artifact_sha,
                    "member_path": canonical,
                    "member_sha256": digest,
                    "member_elf_soname": soname,
                    "custodian_identity": common["custodian_identity"],
                    "immutable_locator_or_signed_envelope": common["locator"],
                }
            )
    if package is None:
        fail(f"artifact lacks .PKGINFO: {artifact}")
    if not rows:
        fail(f"artifact has no non-directory members: {artifact}")
    for row in rows:
        row["package_name"], row["package_version"], row["package_revision"] = package
    return rows


def collect_artifacts(working_directory: Path, patterns: list[str]) -> list[tuple[Path, str]]:
    rows = collect_regular_globs(working_directory, patterns, "artifact", MAX_ARTIFACTS)
    return [(working_directory / str(row["relative_path"]), str(row["relative_path"])) for row in rows]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--request-issuance", required=True, type=Path)
    parser.add_argument("--record-contract-issuance", required=True, type=Path)
    parser.add_argument("--request-id", required=True)
    parser.add_argument("--source-repository", required=True, type=Path)
    parser.add_argument("--working-directory", type=Path)
    parser.add_argument("--artifact-glob", action="append", required=True)
    parser.add_argument("--input-source-glob", action="append", required=True)
    parser.add_argument("--build-run-id", required=True)
    parser.add_argument("--custodian-identity", required=True)
    parser.add_argument("--immutable-locator-or-signed-envelope", required=True)
    parser.add_argument("--container-or-vm-image-digest", required=True)
    parser.add_argument("--source-date-epoch", required=True)
    parser.add_argument("--environment-key", action="append", default=[])
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()

    if args.command and args.command[0] == "--":
        args.command = args.command[1:]
    if not args.command:
        fail("missing build command after --")
    for label, value in (
        ("request ID", args.request_id),
        ("build run ID", args.build_run_id),
        ("custodian identity", args.custodian_identity),
        ("immutable locator or signed envelope", args.immutable_locator_or_signed_envelope),
        ("container or VM image digest", args.container_or_vm_image_digest),
        ("source date epoch", args.source_date_epoch),
    ):
        safe_text(value, label)
    if not SAFE_ID_RE.fullmatch(args.request_id):
        fail("invalid request ID")
    if not SAFE_ID_RE.fullmatch(args.build_run_id):
        fail("build run ID must be a stable identifier, not free-form prose")
    if not args.source_date_epoch.isdigit():
        fail("source date epoch must be decimal seconds")
    if args.out.exists() or args.out.is_symlink():
        fail(f"refusing existing output: {args.out}")

    request_rows = read_tsv(args.request_issuance)
    contract_rows = read_tsv(args.record_contract_issuance)
    request, contracts = verify_contracts(request_rows, contract_rows, args.request_id)

    repo = args.source_repository.resolve()
    if not (repo / ".git").exists():
        fail(f"source repository is not a Git worktree: {repo}")
    if git_value(repo, "status", "--porcelain", "--untracked-files=no"):
        fail("source repository has tracked modifications")
    head = git_value(repo, "rev-parse", "HEAD")
    tree = git_value(repo, "rev-parse", "HEAD^{tree}")
    recipe_tree = git_value(repo, "rev-parse", f"HEAD:{request['recipe_root']}")
    if recipe_tree != request["recipe_tree"]:
        fail(f"recipe tree mismatch: {recipe_tree} != {request['recipe_tree']}")
    working = (args.working_directory or repo).resolve()
    try:
        working.relative_to(repo)
    except ValueError:
        fail("working directory must remain inside source repository")
    if not working.is_dir() or working.is_symlink():
        fail(f"invalid working directory: {working}")

    recipe_manifest_sha, recipe_rows = recipe_manifest(repo, request["recipe_root"])
    build_script = repo / request["recipe_root"] / "build.sh"
    if not build_script.is_file() or build_script.is_symlink():
        fail(f"missing regular build script: {build_script}")
    build_script_sha = sha256_file(build_script)
    tool_components, tool_digests = toolchain_snapshot()
    relevant_environment = environment_snapshot(args.environment_key)

    response_root = args.out / "response-root"
    response_dir = response_root / args.request_id
    audit_dir = args.out / "producer-audit" / args.request_id
    response_dir.mkdir(parents=True)
    audit_dir.mkdir(parents=True)
    write_tsv(audit_dir / "recipe-file-manifest.tsv", ["path", "kind", "sha256"], recipe_rows)

    started = utc_now()
    log_path = audit_dir / "build-command.log"
    with log_path.open("wb") as log:
        proc = subprocess.run(
            args.command,
            cwd=working,
            stdin=subprocess.DEVNULL,
            stdout=log,
            stderr=subprocess.STDOUT,
            env=os.environ.copy(),
            check=False,
        )
    finished = utc_now()
    (audit_dir / "build-command.rc").write_text(f"{proc.returncode}\n", encoding="utf-8")
    if proc.returncode != 0:
        fail(f"build command failed with exit code {proc.returncode}; see {log_path}")

    input_sources = collect_regular_globs(working, args.input_source_glob, "input source", 4096)
    artifacts = collect_artifacts(working, args.artifact_glob)
    write_tsv(
        audit_dir / "input-source-manifest.tsv",
        ["relative_path", "sha256", "size_bytes"],
        input_sources,
    )
    system_packages = dependency_snapshot(audit_dir)
    common = {
        "build_run_id": args.build_run_id,
        "custodian_identity": args.custodian_identity,
        "locator": args.immutable_locator_or_signed_envelope,
    }
    with tempfile.TemporaryDirectory(prefix="sup02-producer-") as temp_name:
        temp = Path(temp_name)
        output_rows: list[dict[str, str]] = []
        for artifact, relative in artifacts:
            output_rows.extend(inventory_artifact(artifact, relative, request, common, temp))
    output_rows.sort(key=lambda row: (row["artifact_path"], row["member_path"]))
    write_tsv(response_dir / "build-output-manifest.tsv", OUTPUT_FIELDS, output_rows)

    invocation = {
        "schema_version": "1",
        "request_id": request["request_id"],
        "root_review_id": request["root_review_id"],
        "recipe_root": request["recipe_root"],
        "recipe_tree": request["recipe_tree"],
        "build_run_id": args.build_run_id,
        "build_started_at_utc": started,
        "build_finished_at_utc": finished,
        "working_directory": str(working),
        "invocation_argv": args.command,
        "input_source_digests": {
            "source_repository_head": head,
            "source_repository_tree": tree,
            "recipe_root": request["recipe_root"],
            "recipe_tree": request["recipe_tree"],
            "recipe_file_manifest_sha256": recipe_manifest_sha,
            "build_input_files": input_sources,
        },
        "build_script_digest": build_script_sha,
        "custodian_identity": args.custodian_identity,
        "immutable_locator_or_signed_envelope": args.immutable_locator_or_signed_envelope,
    }
    environment = {
        "schema_version": "1",
        "request_id": request["request_id"],
        "root_review_id": request["root_review_id"],
        "recipe_tree": request["recipe_tree"],
        "build_run_id": args.build_run_id,
        "host_os": os_snapshot(),
        "host_kernel": platform.release(),
        "host_arch": platform.machine(),
        "toolchain_components": tool_components,
        "toolchain_digests": tool_digests,
        "dependency_lock_or_snapshot": {
            "source_repository_head": head,
            "source_repository_tree": tree,
            "recipe_tree": request["recipe_tree"],
            "recipe_file_manifest_sha256": recipe_manifest_sha,
            "system_package_snapshot": system_packages,
        },
        "container_or_vm_image_digest": args.container_or_vm_image_digest,
        "relevant_environment": relevant_environment,
        "source_date_epoch": args.source_date_epoch,
        "custodian_identity": args.custodian_identity,
        "immutable_locator_or_signed_envelope": args.immutable_locator_or_signed_envelope,
    }
    write_json(response_dir / "build-invocation-record.json", invocation)
    write_json(response_dir / "build-environment-record.json", environment)

    manifest_rows: list[dict[str, object]] = []
    for index, name in enumerate(RECORD_NAMES, 1):
        path = response_dir / name
        contract = contracts[name]
        mandatory = contract["mandatory_fields"].split(";")
        if name.endswith(".json"):
            value = json.loads(path.read_text(encoding="utf-8"))
            missing = [field for field in mandatory if field not in value or value[field] in (None, "", [], {})]
        else:
            rows = read_tsv(path)
            missing = [field for field in mandatory if not rows or any(not row.get(field) for row in rows)]
        if missing:
            fail(f"producer emitted missing mandatory fields for {name}: {missing}")
        manifest_rows.append(
            {
                "response_record_id": f"{args.request_id}:record:{index}",
                "request_id": request["request_id"],
                "root_review_id": request["root_review_id"],
                "recipe_root": request["recipe_root"],
                "recipe_tree": request["recipe_tree"],
                "record_name": name,
                "relative_path": name,
                "sha256": sha256_file(path),
                "size_bytes": path.stat().st_size,
                "custodian_identity": args.custodian_identity,
                "immutable_locator_or_signed_envelope": args.immutable_locator_or_signed_envelope,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_tsv(response_dir / RESPONSE_MANIFEST, RESPONSE_MANIFEST_FIELDS, manifest_rows)

    status = {
        "producer_state": "COMPLETE_CANDIDATE_RESPONSE_EMITTED_REVIEW_REQUIRED",
        "request_id": request["request_id"],
        "recipe_root": request["recipe_root"],
        "recipe_tree": request["recipe_tree"],
        "build_run_id": args.build_run_id,
        "input_source_count": len(input_sources),
        "artifact_count": len(artifacts),
        "output_manifest_rows": len(output_rows),
        "build_attestations_accepted": 0,
        "final_provider_decisions_accepted": 0,
        "target_rows_populated": 0,
        "response_root": str(response_root),
        "next_action": "RUN_0163_ACQUIRER_THEN_SEPARATE_RECEIPT_REVIEW",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(audit_dir / "producer-status.json", status)
    print("SUP02_CUSTODIAN_EXPORT_RESPONSE_PRODUCER=PASS_BOUNDED")
    for key, value in status.items():
        print(f"{key.upper()}={value}")


if __name__ == "__main__":
    main()
