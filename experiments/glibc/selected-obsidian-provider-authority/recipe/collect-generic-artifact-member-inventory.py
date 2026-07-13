#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import os
import re
import ssl
import stat
import struct
import subprocess
import sys
import tarfile
import traceback
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path, PurePosixPath
from typing import BinaryIO, Iterable

REPO = Path(os.environ["PROJECT_REPO"]).resolve()
PREFIX = Path(os.environ["PREFIX"]).resolve()
OUT = Path(os.environ["OUT"]).resolve()
ARTIFACT_DIR = Path(os.environ["ARTIFACT_DIR"]).resolve()
SSL_CERT_FILE = Path(os.environ["SSL_CERT_FILE"]).resolve()
ARTIFACTS = Path(os.environ["COMPARISON_ARTIFACTS"]).resolve()
EDGES = Path(os.environ["COMPARISON_EDGES"]).resolve()
META = Path(os.environ["COMPARISON_METADATA"]).resolve()
REPOSITORY = Path(os.environ["REPOSITORY_METADATA"]).resolve()
TEST_MODE = os.environ.get("GENERIC_MEMBER_INVENTORY_TEST_MODE", "0") == "1"
MAX_IN_MEMORY_MATCH_MEMBER = int(os.environ.get("MAX_IN_MEMORY_MATCH_MEMBER", str(64 * 1024 * 1024)))
APPROVED_ARTIFACT_HOSTS = {"packages-cf.termux.dev", "packages.termux.dev"}
LOOPBACK_TEST_HOSTS = {"127.0.0.1", "localhost", "::1"}
stage = "initialization"


def run(args: list[str], *, check: bool = True, text: bool = True, stdout=None) -> subprocess.CompletedProcess:
    return subprocess.run(
        args,
        check=check,
        text=text,
        stdout=stdout if stdout is not None else subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8", errors="strict") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def write_tsv(path: Path, fields: list[str], rows: Iterable[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as stream:
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


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def bytes_sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def metadata_map(path: Path) -> dict[str, str]:
    return {row["field"]: row["value"] for row in read_tsv(path)}


def file_snapshot(path: Path) -> dict[str, object]:
    if not path.exists():
        return {"path": str(path), "state": "MISSING", "size": 0, "sha256": "MISSING"}
    if path.is_symlink() or not path.is_file():
        return {"path": str(path), "state": "UNSAFE", "size": 0, "sha256": "UNSAFE"}
    return {"path": str(path), "state": "REGULAR", "size": path.stat().st_size, "sha256": sha256(path)}


def directory_metadata_manifest(root: Path) -> str:
    digest = hashlib.sha256()
    if not root.is_dir() or root.is_symlink():
        return "MISSING_OR_UNSAFE"
    for path in sorted(root.rglob("*"), key=lambda item: str(item.relative_to(root))):
        rel = str(path.relative_to(root))
        info = path.lstat()
        if stat.S_ISREG(info.st_mode):
            kind = "FILE"
            payload = sha256(path)
        elif stat.S_ISDIR(info.st_mode):
            kind = "DIR"
            payload = "-"
        elif stat.S_ISLNK(info.st_mode):
            kind = "SYMLINK"
            payload = os.readlink(path)
        else:
            kind = "SPECIAL"
            payload = f"mode={info.st_mode:o}"
        digest.update(
            f"{rel}\0{kind}\0{info.st_mode:o}\0{info.st_size}\0{info.st_mtime_ns}\0{payload}\0".encode(
                errors="surrogateescape"
            )
        )
    return digest.hexdigest()


def validate_relative_repository_path(value: str) -> str:
    if "\x00" in value or "\\" in value:
        raise ValueError(f"unsafe repository filename: {value!r}")
    parsed = PurePosixPath(value)
    if parsed.is_absolute() or not parsed.parts or any(part in {"", ".", ".."} for part in parsed.parts):
        raise ValueError(f"unsafe repository filename: {value!r}")
    return str(parsed)


def normalize_tar_member(name: str) -> str:
    if "\x00" in name or "\\" in name:
        raise ValueError(f"unsafe tar member path: {name!r}")
    while name.startswith("./"):
        name = name[2:]
    if name in {"", "."}:
        return ""
    parsed = PurePosixPath(name)
    if parsed.is_absolute() or any(part in {"", ".", ".."} for part in parsed.parts):
        raise ValueError(f"unsafe tar member path: {name!r}")
    return str(parsed)


def member_type(member: tarfile.TarInfo) -> str:
    if member.isreg():
        return "REGULAR"
    if member.isdir():
        return "DIRECTORY"
    if member.issym():
        return "SYMLINK"
    if member.islnk():
        return "HARDLINK"
    if member.ischr():
        return "CHAR_DEVICE"
    if member.isblk():
        return "BLOCK_DEVICE"
    if member.isfifo():
        return "FIFO"
    return "OTHER"


def url_allowed(url: str) -> bool:
    parsed = urllib.parse.urlparse(url)
    host = (parsed.hostname or "").lower()
    if parsed.username or parsed.password or parsed.fragment:
        return False
    if TEST_MODE:
        return parsed.scheme == "http" and host in LOOPBACK_TEST_HOSTS
    return parsed.scheme == "https" and parsed.port in {None, 443} and host in APPROVED_ARTIFACT_HOSTS


def make_ssl_context() -> ssl.SSLContext | None:
    if TEST_MODE:
        return None
    return ssl.create_default_context(cafile=str(SSL_CERT_FILE))


def download_verified(
    *,
    url: str,
    destination: Path,
    expected_size: int,
    expected_sha256: str,
) -> dict[str, object]:
    if destination.exists() or destination.is_symlink():
        if destination.is_symlink() or not destination.is_file():
            raise ValueError(f"unsafe existing artifact cache entry: {destination}")
        actual_size = destination.stat().st_size
        actual_sha256 = sha256(destination)
        if actual_size != expected_size or actual_sha256 != expected_sha256:
            raise ValueError(f"existing artifact cache identity mismatch: {destination}")
        return {
            "acquisition_state": "REUSED_VERIFIED",
            "final_url": url,
            "actual_size": actual_size,
            "actual_sha256": actual_sha256,
        }

    if not url_allowed(url):
        raise ValueError(f"unapproved artifact URL: {url}")
    part = destination.with_name(f".{destination.name}.part-{os.getpid()}")
    if part.exists() or part.is_symlink():
        raise ValueError(f"refusing existing partial artifact: {part}")

    digest = hashlib.sha256()
    size = 0
    try:
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "termux-native-desktop-generic-member-inventory/1"},
        )
        with urllib.request.urlopen(request, context=make_ssl_context(), timeout=120) as response, part.open("xb") as output:
            final_url = response.geturl()
            if not url_allowed(final_url):
                raise ValueError(f"unapproved artifact redirect: {final_url}")
            content_length = response.headers.get("Content-Length")
            if content_length and int(content_length) != expected_size:
                raise ValueError(
                    f"artifact Content-Length mismatch: {content_length} != {expected_size}: {url}"
                )
            while True:
                chunk = response.read(1024 * 1024)
                if not chunk:
                    break
                size += len(chunk)
                if size > expected_size:
                    raise ValueError(f"artifact exceeds expected size: {url}")
                digest.update(chunk)
                output.write(chunk)
            output.flush()
            os.fsync(output.fileno())
        actual_sha256 = digest.hexdigest()
        if size != expected_size or actual_sha256 != expected_sha256:
            raise ValueError(
                f"downloaded artifact identity mismatch: size={size}/{expected_size} "
                f"sha256={actual_sha256}/{expected_sha256}: {url}"
            )
        os.chmod(part, 0o600)
        os.replace(part, destination)
        return {
            "acquisition_state": "DOWNLOADED_VERIFIED",
            "final_url": final_url,
            "actual_size": size,
            "actual_sha256": actual_sha256,
        }
    finally:
        if part.exists():
            part.unlink()


def control_fields(artifact: Path) -> dict[str, str]:
    fmt = "${Package}\t${Version}\t${Architecture}\t${Installed-Size}\n"
    proc = run(["dpkg-deb", "-W", f"--showformat={fmt}", str(artifact)], check=False)
    if proc.returncode != 0:
        raise ValueError(f"dpkg-deb control query failed for {artifact}: {proc.stderr.strip()}")
    parts = proc.stdout.rstrip("\n").split("\t")
    if len(parts) != 4:
        raise ValueError(f"unexpected control query output for {artifact}: {proc.stdout!r}")
    return {
        "control_package": parts[0],
        "control_version": parts[1],
        "control_architecture": parts[2],
        "control_installed_size_kib": parts[3] or "-",
    }


def parse_elf64_little_soname(payload: bytes) -> dict[str, str]:
    result = {
        "elf_parse_state": "NOT_ELF",
        "elf_class": "-",
        "elf_data": "-",
        "elf_machine": "-",
        "observed_soname": "-",
    }
    if len(payload) < 64 or payload[:4] != b"\x7fELF":
        return result
    elf_class = payload[4]
    elf_data = payload[5]
    result["elf_class"] = {1: "ELF32", 2: "ELF64"}.get(elf_class, f"UNKNOWN_{elf_class}")
    result["elf_data"] = {1: "LITTLE", 2: "BIG"}.get(elf_data, f"UNKNOWN_{elf_data}")
    if elf_class != 2 or elf_data != 1:
        result["elf_parse_state"] = "ELF_UNSUPPORTED_CLASS_OR_ENDIAN"
        return result
    try:
        (
            _ident,
            _etype,
            machine,
            _version,
            _entry,
            phoff,
            _shoff,
            _flags,
            _ehsize,
            phentsize,
            phnum,
            _shentsize,
            _shnum,
            _shstrndx,
        ) = struct.unpack_from("<16sHHIQQQIHHHHHH", payload, 0)
        result["elf_machine"] = str(machine)
        if phentsize < 56 or phoff + phentsize * phnum > len(payload):
            result["elf_parse_state"] = "ELF_PROGRAM_HEADER_BOUNDS_INVALID"
            return result
        loads: list[tuple[int, int, int]] = []
        dynamic: tuple[int, int] | None = None
        for index in range(phnum):
            offset = phoff + index * phentsize
            p_type, _p_flags, p_offset, p_vaddr, _p_paddr, p_filesz, _p_memsz, _p_align = struct.unpack_from(
                "<IIQQQQQQ", payload, offset
            )
            if p_type == 1:  # PT_LOAD
                loads.append((p_vaddr, p_offset, p_filesz))
            elif p_type == 2:  # PT_DYNAMIC
                dynamic = (p_offset, p_filesz)
        if dynamic is None:
            result["elf_parse_state"] = "ELF_NO_DYNAMIC_SEGMENT"
            return result
        dyn_offset, dyn_size = dynamic
        if dyn_offset + dyn_size > len(payload):
            result["elf_parse_state"] = "ELF_DYNAMIC_BOUNDS_INVALID"
            return result
        strtab_vaddr: int | None = None
        strtab_size: int | None = None
        soname_index: int | None = None
        for offset in range(dyn_offset, dyn_offset + dyn_size, 16):
            if offset + 16 > len(payload):
                break
            tag, value = struct.unpack_from("<QQ", payload, offset)
            if tag == 0:
                break
            if tag == 5:  # DT_STRTAB
                strtab_vaddr = value
            elif tag == 10:  # DT_STRSZ
                strtab_size = value
            elif tag == 14:  # DT_SONAME
                soname_index = value
        if strtab_vaddr is None or soname_index is None:
            result["elf_parse_state"] = "ELF_DYNAMIC_NO_SONAME"
            return result
        strtab_offset: int | None = None
        for p_vaddr, p_offset, p_filesz in loads:
            if p_vaddr <= strtab_vaddr < p_vaddr + p_filesz:
                strtab_offset = p_offset + (strtab_vaddr - p_vaddr)
                break
        if strtab_offset is None:
            result["elf_parse_state"] = "ELF_STRTAB_NOT_FILE_MAPPED"
            return result
        string_offset = strtab_offset + soname_index
        upper_bound = len(payload)
        if strtab_size is not None:
            upper_bound = min(upper_bound, strtab_offset + strtab_size)
        if string_offset >= upper_bound:
            result["elf_parse_state"] = "ELF_SONAME_OFFSET_INVALID"
            return result
        terminator = payload.find(b"\x00", string_offset, upper_bound)
        if terminator < 0:
            result["elf_parse_state"] = "ELF_SONAME_UNTERMINATED"
            return result
        result["observed_soname"] = payload[string_offset:terminator].decode("utf-8", errors="replace")
        result["elf_parse_state"] = "ELF_SONAME_PARSED"
        return result
    except (struct.error, ValueError, OverflowError) as exc:
        result["elf_parse_state"] = f"ELF_PARSE_ERROR_{type(exc).__name__}"
        return result


def inventory_tar_stream(
    artifact: Path,
    option: str,
    archive_kind: str,
    expected_basenames: set[str],
) -> tuple[list[dict[str, object]], dict[str, list[dict[str, object]]]]:
    proc = subprocess.Popen(
        ["dpkg-deb", option, str(artifact)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert proc.stdout is not None
    rows: list[dict[str, object]] = []
    matched: dict[str, list[dict[str, object]]] = defaultdict(list)
    try:
        with tarfile.open(fileobj=proc.stdout, mode="r|*") as archive:
            for member in archive:
                normalized = normalize_tar_member(member.name)
                basename = PurePosixPath(normalized).name if normalized else "-"
                kind = member_type(member)
                row: dict[str, object] = {
                    "archive_kind": archive_kind,
                    "member_path": member.name,
                    "normalized_path": normalized or ".",
                    "basename": basename,
                    "member_type": kind,
                    "mode_octal": f"{member.mode:o}",
                    "uid": member.uid,
                    "gid": member.gid,
                    "size": member.size,
                    "link_target": member.linkname or "-",
                    "exact_named_search_member": "YES" if basename in expected_basenames else "NO",
                    "elf_parse_state": "NOT_INSPECTED",
                    "elf_class": "-",
                    "elf_data": "-",
                    "elf_machine": "-",
                    "observed_soname": "-",
                    "member_sha256": "-",
                }
                if archive_kind == "DATA" and basename in expected_basenames:
                    if member.isreg():
                        if member.size > MAX_IN_MEMORY_MATCH_MEMBER:
                            row["elf_parse_state"] = "MATCH_MEMBER_EXCEEDS_IN_MEMORY_LIMIT"
                        else:
                            source = archive.extractfile(member)
                            if source is None:
                                row["elf_parse_state"] = "MATCH_MEMBER_STREAM_UNAVAILABLE"
                            else:
                                payload = source.read(MAX_IN_MEMORY_MATCH_MEMBER + 1)
                                if len(payload) != member.size:
                                    row["elf_parse_state"] = "MATCH_MEMBER_STREAM_SIZE_MISMATCH"
                                else:
                                    row["member_sha256"] = bytes_sha256(payload)
                                    row.update(parse_elf64_little_soname(payload))
                    elif member.issym() or member.islnk():
                        row["elf_parse_state"] = "MATCH_MEMBER_LINK_NO_ELF_BYTES"
                    else:
                        row["elf_parse_state"] = "MATCH_MEMBER_NON_REGULAR"
                    matched[basename].append(dict(row))
                rows.append(row)
        proc.stdout.close()
        stderr = proc.stderr.read() if proc.stderr is not None else b""
        returncode = proc.wait()
        if returncode != 0:
            raise ValueError(
                f"dpkg-deb {option} failed for {artifact}: {stderr.decode(errors='replace').strip()}"
            )
        return rows, matched
    except Exception:
        proc.kill()
        proc.wait()
        raise


def write_failure(stage_name: str, exc: BaseException) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    write_tsv(
        OUT / "failure.tsv",
        ["stage", "exception_type", "message"],
        [{"stage": stage_name, "exception_type": type(exc).__name__, "message": str(exc)}],
    )
    (OUT / "analysis.status").write_text("FAIL\n", encoding="utf-8")
    (OUT / "traceback.txt").write_text(traceback.format_exc(), encoding="utf-8")


def main() -> int:
    global stage
    try:
        stage = "input_paths"
        for path in (ARTIFACTS, EDGES, META, REPOSITORY):
            if path.is_symlink() or not path.is_file():
                raise ValueError(f"missing or unsafe canonical input: {path}")
        if OUT.exists() or OUT.is_symlink():
            raise ValueError(f"refusing existing output: {OUT}")
        if ARTIFACT_DIR.is_symlink():
            raise ValueError(f"unsafe artifact directory: {ARTIFACT_DIR}")
        ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
        if not ARTIFACT_DIR.is_dir():
            raise ValueError(f"artifact directory unavailable: {ARTIFACT_DIR}")
        OUT.mkdir(parents=True, exist_ok=False)

        stage = "canonical_input_verification"
        artifacts = read_tsv(ARTIFACTS)
        edges = read_tsv(EDGES)
        meta = metadata_map(META)
        repositories = read_tsv(REPOSITORY)
        required_meta = {
            "repository_metadata_id",
            "repository_base_uri",
            "artifact_set_sha256",
            "edge_set_sha256",
            "download_scope_artifacts",
            "download_scope_edges",
            "download_scope_compressed_bytes",
            "authority_decisions_accepted",
            "target_rows_populated",
        }
        missing_meta = required_meta - set(meta)
        if missing_meta:
            raise ValueError(f"missing comparison metadata fields: {sorted(missing_meta)}")
        if sha256(ARTIFACTS) != meta["artifact_set_sha256"]:
            raise ValueError("artifact comparison-set hash mismatch")
        if sha256(EDGES) != meta["edge_set_sha256"]:
            raise ValueError("edge comparison-set hash mismatch")
        if len(artifacts) != int(meta["download_scope_artifacts"]):
            raise ValueError("artifact row count mismatch")
        if len(edges) != int(meta["download_scope_edges"]):
            raise ValueError("edge row count mismatch")
        if sum(int(row["artifact_size"]) for row in artifacts) != int(meta["download_scope_compressed_bytes"]):
            raise ValueError("artifact byte ceiling mismatch")
        if meta["authority_decisions_accepted"] != "0" or meta["target_rows_populated"] != "0":
            raise ValueError("comparison input already crosses authority or target boundary")
        repository_rows = [
            row for row in repositories if row["repository_metadata_id"] == meta["repository_metadata_id"]
        ]
        if len(repository_rows) != 1:
            raise ValueError("repository metadata identity is not unique")
        repository = repository_rows[0]
        base_uri = meta["repository_base_uri"]
        if repository["repository_base_uri"] != base_uri:
            raise ValueError("repository base URI mismatch")
        if not base_uri.endswith("/") or not url_allowed(base_uri):
            raise ValueError(f"unapproved repository base URI: {base_uri}")

        artifact_by_id: dict[str, dict[str, str]] = {}
        for artifact in artifacts:
            artifact_id = artifact["artifact_id"]
            if artifact_id in artifact_by_id:
                raise ValueError(f"duplicate artifact id: {artifact_id}")
            validate_relative_repository_path(artifact["repository_filename"])
            if not re.fullmatch(r"[0-9a-f]{64}", artifact["artifact_sha256"]):
                raise ValueError(f"invalid artifact SHA-256: {artifact_id}")
            if artifact["comparison_scope_state"] != "NAMED_DOWNLOAD_ONLY_MEMBER_INVENTORY_SCOPE":
                raise ValueError(f"artifact outside comparison scope: {artifact_id}")
            artifact_by_id[artifact_id] = artifact
        expected_by_artifact: dict[str, set[str]] = defaultdict(set)
        edges_by_artifact: dict[str, list[dict[str, str]]] = defaultdict(list)
        for edge in edges:
            artifact_id = edge["artifact_id"]
            if artifact_id not in artifact_by_id:
                raise ValueError(f"edge references unknown artifact: {artifact_id}")
            expected = edge["expected_member_basename"]
            if PurePosixPath(expected).name != expected or expected in {"", ".", ".."}:
                raise ValueError(f"unsafe expected member basename: {expected!r}")
            expected_by_artifact[artifact_id].add(expected)
            edges_by_artifact[artifact_id].append(edge)

        stage = "pre_transaction_snapshots"
        dpkg_status = PREFIX / "var/lib/dpkg/status"
        apt_lists = PREFIX / "var/lib/apt/lists"
        repo_head = run(["git", "-C", str(REPO), "rev-parse", "HEAD"]).stdout.strip()
        repo_tree = run(["git", "-C", str(REPO), "rev-parse", "HEAD^{tree}"]).stdout.strip()
        repo_tracked_status = run(
            ["git", "-C", str(REPO), "status", "--porcelain", "--untracked-files=no"]
        ).stdout
        if repo_tracked_status:
            raise ValueError("tracked repository changes detected")
        before_dpkg = file_snapshot(dpkg_status)
        before_apt_manifest = directory_metadata_manifest(apt_lists)
        before_artifact_manifest = directory_metadata_manifest(ARTIFACT_DIR)

        stage = "bounded_download_plan"
        plan_rows: list[dict[str, object]] = []
        local_names: set[str] = set()
        for artifact in artifacts:
            repository_filename = validate_relative_repository_path(artifact["repository_filename"])
            url = urllib.parse.urljoin(base_uri, repository_filename)
            if not url_allowed(url):
                raise ValueError(f"unapproved resolved artifact URL: {url}")
            local_name = PurePosixPath(repository_filename).name
            if local_name in local_names:
                raise ValueError(f"duplicate artifact cache basename: {local_name}")
            local_names.add(local_name)
            local_path = ARTIFACT_DIR / local_name
            plan_rows.append({
                "artifact_id": artifact["artifact_id"],
                "package": artifact["package"],
                "version": artifact["version"],
                "architecture": artifact["architecture"],
                "repository_filename": repository_filename,
                "artifact_url": url,
                "expected_size": artifact["artifact_size"],
                "expected_sha256": artifact["artifact_sha256"],
                "local_path": str(local_path),
                "download_scope_state": "EXACT_BOUNDED_ARTIFACT_ONLY",
            })
        write_tsv(OUT / "download-plan.tsv", list(plan_rows[0]), plan_rows)

        stage = "bounded_artifact_acquisition"
        acquisition_rows: list[dict[str, object]] = []
        control_rows: list[dict[str, object]] = []
        control_member_rows: list[dict[str, object]] = []
        data_member_rows: list[dict[str, object]] = []
        matched_by_artifact: dict[str, dict[str, list[dict[str, object]]]] = {}
        for plan in plan_rows:
            artifact_id = str(plan["artifact_id"])
            artifact = artifact_by_id[artifact_id]
            local_path = Path(str(plan["local_path"]))
            acquired = download_verified(
                url=str(plan["artifact_url"]),
                destination=local_path,
                expected_size=int(plan["expected_size"]),
                expected_sha256=str(plan["expected_sha256"]),
            )
            control = control_fields(local_path)
            if (
                control["control_package"] != artifact["package"]
                or control["control_version"] != artifact["version"]
                or control["control_architecture"] != artifact["architecture"]
            ):
                raise ValueError(
                    f"artifact control identity mismatch for {artifact_id}: "
                    f"{control['control_package']} {control['control_version']} "
                    f"{control['control_architecture']}"
                )
            acquisition_rows.append({
                **plan,
                **acquired,
                "control_identity_state": "EXACT_PACKAGE_VERSION_ARCHITECTURE_MATCH",
                "package_operation_performed": "NO",
            })
            control_rows.append({
                "artifact_id": artifact_id,
                "package": artifact["package"],
                "version": artifact["version"],
                "architecture": artifact["architecture"],
                **control,
                "control_identity_state": "EXACT_PACKAGE_VERSION_ARCHITECTURE_MATCH",
                "maintainer_script_execution_state": "NOT_EXECUTED",
            })
            expected = expected_by_artifact[artifact_id]
            ctrl_rows, _ = inventory_tar_stream(local_path, "--ctrl-tarfile", "CONTROL", set())
            data_rows, matches = inventory_tar_stream(local_path, "--fsys-tarfile", "DATA", expected)
            for row in ctrl_rows:
                control_member_rows.append({"artifact_id": artifact_id, "package": artifact["package"], **row})
            for row in data_rows:
                data_member_rows.append({"artifact_id": artifact_id, "package": artifact["package"], **row})
            matched_by_artifact[artifact_id] = matches

        write_tsv(OUT / "downloaded-artifacts.tsv", list(acquisition_rows[0]), acquisition_rows)
        write_tsv(OUT / "artifact-control-fields.tsv", list(control_rows[0]), control_rows)
        member_fields = [
            "artifact_id", "package", "archive_kind", "member_path", "normalized_path", "basename",
            "member_type", "mode_octal", "uid", "gid", "size", "link_target",
            "exact_named_search_member", "elf_parse_state", "elf_class", "elf_data", "elf_machine",
            "observed_soname", "member_sha256",
        ]
        write_tsv(OUT / "artifact-control-member-inventory.tsv", member_fields, control_member_rows)
        write_tsv(OUT / "artifact-data-member-inventory.tsv", member_fields, data_member_rows)

        stage = "named_member_edge_observation"
        edge_rows: list[dict[str, object]] = []
        for edge in edges:
            artifact_id = edge["artifact_id"]
            expected = edge["expected_member_basename"]
            matches = matched_by_artifact.get(artifact_id, {}).get(expected, [])
            if not matches:
                observation = "NO_EXACT_BASENAME_MEMBER_OBSERVED"
            elif len(matches) == 1:
                observation = "UNIQUE_EXACT_BASENAME_MEMBER_OBSERVED"
            else:
                observation = "MULTIPLE_EXACT_BASENAME_MEMBERS_OBSERVED"
            observed_paths = ";".join(sorted(str(row["normalized_path"]) for row in matches)) or "-"
            observed_types = ";".join(sorted({str(row["member_type"]) for row in matches})) or "-"
            observed_sonames = ";".join(
                sorted({str(row["observed_soname"]) for row in matches if row["observed_soname"] != "-"})
            ) or "-"
            elf_states = ";".join(sorted({str(row["elf_parse_state"]) for row in matches})) or "-"
            observed_hashes = ";".join(
                sorted({str(row["member_sha256"]) for row in matches if row["member_sha256"] != "-"})
            ) or "-"
            edge_rows.append({
                "evidence_row_id": edge["evidence_row_id"],
                "capability_partition": edge["capability_partition"],
                "identity_label": edge["identity_label"],
                "artifact_id": artifact_id,
                "package": edge["package"],
                "version": edge["version"],
                "architecture": edge["architecture"],
                "expected_member_basename": expected,
                "exact_basename_match_count": len(matches),
                "observed_member_paths": observed_paths,
                "observed_member_types": observed_types,
                "observed_elf_sonames": observed_sonames,
                "observed_member_sha256s": observed_hashes,
                "elf_observation_states": elf_states,
                "member_observation_state": observation,
                "object_member_binding_state": "OBSERVED_CANDIDATE_NOT_AUTHORITY_ACCEPTED",
                "artifact_to_recipe_binding_state": "OPEN",
                "termux_android_adaptation_state": "OPEN",
                "final_provider_state": "UNRESOLVED",
                "target_population_state": "BLOCKED",
            })
        write_tsv(OUT / "named-member-observations.tsv", list(edge_rows[0]), edge_rows)

        stage = "post_transaction_invariants"
        after_dpkg = file_snapshot(dpkg_status)
        after_apt_manifest = directory_metadata_manifest(apt_lists)
        after_artifact_manifest = directory_metadata_manifest(ARTIFACT_DIR)
        if before_dpkg != after_dpkg:
            raise ValueError("dpkg status changed during download-only transaction")
        if before_apt_manifest != after_apt_manifest:
            raise ValueError("apt list metadata changed during download-only transaction")
        final_repo_head = run(["git", "-C", str(REPO), "rev-parse", "HEAD"]).stdout.strip()
        final_repo_tree = run(["git", "-C", str(REPO), "rev-parse", "HEAD^{tree}"]).stdout.strip()
        final_repo_tracked_status = run(
            ["git", "-C", str(REPO), "status", "--porcelain", "--untracked-files=no"]
        ).stdout
        if repo_head != final_repo_head or repo_tree != final_repo_tree or final_repo_tracked_status:
            raise ValueError("repository state changed during member-inventory transaction")

        acquisition_counts = Counter(str(row["acquisition_state"]) for row in acquisition_rows)
        observation_counts = Counter(str(row["member_observation_state"]) for row in edge_rows)
        unique_identity_observed = {
            row["evidence_row_id"] for row in edge_rows if int(row["exact_basename_match_count"]) > 0
        }
        input_rows = [
            {"input": "comparison_artifacts", "path": str(ARTIFACTS), "sha256": sha256(ARTIFACTS)},
            {"input": "comparison_edges", "path": str(EDGES), "sha256": sha256(EDGES)},
            {"input": "comparison_metadata", "path": str(META), "sha256": sha256(META)},
            {"input": "repository_metadata", "path": str(REPOSITORY), "sha256": sha256(REPOSITORY)},
            {"input": "dpkg_status_before", **before_dpkg},
            {"input": "dpkg_status_after", **after_dpkg},
            {"input": "apt_lists_manifest_before", "path": str(apt_lists), "sha256": before_apt_manifest},
            {"input": "apt_lists_manifest_after", "path": str(apt_lists), "sha256": after_apt_manifest},
            {"input": "artifact_cache_manifest_before", "path": str(ARTIFACT_DIR), "sha256": before_artifact_manifest},
            {"input": "artifact_cache_manifest_after", "path": str(ARTIFACT_DIR), "sha256": after_artifact_manifest},
        ]
        write_tsv(
            OUT / "input-verification.tsv",
            ["input", "path", "state", "size", "sha256"],
            input_rows,
        )
        summary_rows = [
            {"field": "repository_head", "value": repo_head},
            {"field": "repository_tree", "value": repo_tree},
            {"field": "repository_metadata_id", "value": meta["repository_metadata_id"]},
            {"field": "repository_base_uri", "value": base_uri},
            {"field": "artifacts_planned", "value": len(plan_rows)},
            {"field": "artifacts_verified", "value": len(acquisition_rows)},
            {"field": "artifacts_downloaded", "value": acquisition_counts["DOWNLOADED_VERIFIED"]},
            {"field": "artifacts_reused", "value": acquisition_counts["REUSED_VERIFIED"]},
            {"field": "artifact_bytes_verified", "value": sum(int(row["actual_size"]) for row in acquisition_rows)},
            {"field": "control_member_rows", "value": len(control_member_rows)},
            {"field": "data_member_rows", "value": len(data_member_rows)},
            {"field": "named_edges", "value": len(edge_rows)},
            {"field": "edges_with_exact_basename_observation", "value": sum(1 for row in edge_rows if int(row["exact_basename_match_count"]) > 0)},
            {"field": "edges_without_exact_basename_observation", "value": observation_counts["NO_EXACT_BASENAME_MEMBER_OBSERVED"]},
            {"field": "unique_identities_with_observation", "value": len(unique_identity_observed)},
            {"field": "network_download_performed", "value": "YES" if acquisition_counts["DOWNLOADED_VERIFIED"] else "NO_REUSED_ONLY"},
            {"field": "package_operation_performed", "value": "NO"},
            {"field": "maintainer_script_execution_performed", "value": "NO"},
            {"field": "deb_filesystem_materialization_performed", "value": "NO"},
            {"field": "deb_archive_stream_inventory_performed", "value": "YES"},
            {"field": "authority_decisions_accepted", "value": 0},
            {"field": "target_rows_populated", "value": 0},
            {"field": "next_state", "value": "REVIEW_GENERIC_ARTIFACT_MEMBER_INVENTORY_RECEIPT"},
        ]
        write_tsv(OUT / "summary.tsv", ["field", "value"], summary_rows)
        (OUT / "claim-boundary.txt").write_text(
            "Exact indexed artifact bytes were downloaded or byte-identically reused and verified.\n"
            "Control identity and control/data tar member metadata were inspected as streams only.\n"
            "No package was installed, no maintainer script was executed, and no package payload was materialized into a filesystem tree.\n"
            "Exact-basename and in-memory ELF SONAME observations are candidate evidence only.\n"
            "Object/member authority, recipe build binding, Android adaptation, necessity, final provider, composition and target population remain open or blocked.\n",
            encoding="utf-8",
        )
        (OUT / "next-state.txt").write_text(
            "REVIEW_GENERIC_ARTIFACT_MEMBER_INVENTORY_RECEIPT\n", encoding="utf-8"
        )
        (OUT / "analysis.status").write_text("PASS\n", encoding="utf-8")
        return 0
    except Exception as exc:
        try:
            write_failure(stage, exc)
        except Exception:
            pass
        print(f"generic artifact member inventory failed during {stage}: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
