#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import os
import shutil
import stat
import subprocess
import sys
import traceback
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable

B1_OUT = Path(os.environ["B1_OUT"])
B2_OUT = Path(os.environ["B2_OUT"])
B9_OUT = Path(os.environ["B9_OUT"])
MAP_OUT = Path(os.environ["MAP_OUT"])
PIXBUF_OUT = Path(os.environ["PIXBUF_OUT"])
OUT = Path(os.environ["OUT"])

PREFIX = Path(os.environ["PREFIX"])
HOME = Path(os.environ["HOME"])
GLIBC_ROOT = PREFIX / "glibc"
DPKG_ROOT = PREFIX / "var/lib/dpkg"
DPKG_INFO = DPKG_ROOT / "info"
DPKG_STATUS = DPKG_ROOT / "status"
ROOTFS = Path(
    os.environ.get(
        "ROOTFS",
        str(PREFIX / "var/lib/proot-distro/containers/debian/rootfs"),
    )
)
APP = Path(os.environ.get("APP", str(HOME / "gl/apps/obsidian")))

REPO = Path(
    subprocess.check_output(
        ["git", "-C", str(Path(__file__).resolve().parent), "rev-parse", "--show-toplevel"],
        text=True,
    ).strip()
)
SCHEMA_DIR = REPO / "experiments/glibc/selected-obsidian-provider-authority/schema"
READELF = shutil.which("readelf")

stage = "initialization"


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(
    path: Path,
    fieldnames: list[str],
    rows: Iterable[dict[str, object]],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
            delimiter="\t",
            lineterminator="\n",
            extrasaction="ignore",
        )
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def summary_map(path: Path) -> dict[str, str]:
    return {row["field"]: row["value"] for row in read_tsv(path)}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


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


def within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def current_state(path: Path) -> dict[str, object]:
    if not path.exists() and not path.is_symlink():
        return {
            "state": "ABSENT",
            "path": str(path),
            "link_target": "-",
            "resolved_target": "-",
            "inode": "-",
        }
    metadata = path.lstat()
    if stat.S_ISLNK(metadata.st_mode):
        target = os.readlink(path)
        resolved = Path(os.path.normpath(str(path.parent / target)))
        return {
            "state": "SYMLINK",
            "path": str(path),
            "link_target": target,
            "resolved_target": str(resolved),
            "inode": metadata.st_ino,
        }
    return {
        "state": "NON_SYMLINK",
        "path": str(path),
        "link_target": "-",
        "resolved_target": str(path.resolve()),
        "inode": metadata.st_ino,
    }


def metadata_manifest(root: Path) -> str:
    digest = hashlib.sha256()
    if not root.is_dir():
        return "MISSING"
    for path in sorted(root.iterdir(), key=lambda item: item.name):
        try:
            metadata = path.lstat()
            line = (
                f"{path.name}\0{metadata.st_mode:o}\0{metadata.st_size}\0"
                f"{metadata.st_mtime_ns}\0"
            )
        except OSError as exc:
            line = f"{path.name}\0ERROR\0{type(exc).__name__}\0"
        digest.update(line.encode(errors="surrogateescape"))
    return digest.hexdigest()


def parse_dpkg_status(path: Path) -> dict[tuple[str, str], dict[str, str]]:
    records: dict[tuple[str, str], dict[str, str]] = {}
    paragraph: dict[str, str] = {}
    if not path.is_file():
        return records
    for line in path.read_text(errors="replace").splitlines() + [""]:
        if not line:
            package = paragraph.get("Package")
            architecture = paragraph.get("Architecture", "")
            if package:
                records[(package, architecture)] = dict(paragraph)
            paragraph = {}
            continue
        if line[0].isspace() or ":" not in line:
            continue
        key, value = line.split(":", 1)
        paragraph[key] = value.strip()
    return records


def package_identity(
    package_key: str,
    status_records: dict[tuple[str, str], dict[str, str]],
) -> dict[str, str]:
    if ":" in package_key:
        package, architecture = package_key.rsplit(":", 1)
        record = status_records.get((package, architecture))
    else:
        package = package_key
        matches = [
            record
            for (candidate, _architecture), record in status_records.items()
            if candidate == package
        ]
        record = matches[0] if len(matches) == 1 else None
        architecture = record.get("Architecture", "") if record else ""
    if record is None:
        return {
            "package_key": package_key,
            "package": package,
            "version": "UNKNOWN",
            "architecture": architecture or "UNKNOWN",
            "status": "UNKNOWN",
        }
    return {
        "package_key": package_key,
        "package": record.get("Package", package),
        "version": record.get("Version", "UNKNOWN"),
        "architecture": record.get("Architecture", architecture or "UNKNOWN"),
        "status": record.get("Status", "UNKNOWN"),
    }


def classify_file_type(mode: int) -> str:
    if stat.S_ISREG(mode):
        return "REGULAR"
    if stat.S_ISLNK(mode):
        return "SYMLINK"
    if stat.S_ISDIR(mode):
        return "DIRECTORY"
    if stat.S_ISCHR(mode):
        return "CHAR_DEVICE"
    if stat.S_ISBLK(mode):
        return "BLOCK_DEVICE"
    if stat.S_ISFIFO(mode):
        return "FIFO"
    if stat.S_ISSOCK(mode):
        return "SOCKET"
    return "OTHER"


def parse_bracket_value(line: str) -> str:
    if "[" not in line or "]" not in line:
        return ""
    return line.split("[", 1)[1].split("]", 1)[0]


def inspect_elf(path: Path) -> dict[str, str]:
    result = {
        "elf_state": "NOT_ELF",
        "elf_class": "-",
        "elf_data": "-",
        "elf_type": "-",
        "elf_machine": "-",
        "interpreter": "-",
        "soname": "-",
        "needed": "-",
        "rpath": "-",
        "runpath": "-",
        "build_id": "-",
        "readelf_error": "-",
    }
    try:
        with path.open("rb") as handle:
            if handle.read(4) != b"\x7fELF":
                return result
    except OSError as exc:
        result["elf_state"] = "READ_ERROR"
        result["readelf_error"] = f"{type(exc).__name__}:{exc}"
        return result

    result["elf_state"] = "ELF"
    if READELF is None:
        result["elf_state"] = "READELF_MISSING"
        result["readelf_error"] = "readelf not found"
        return result

    completed = subprocess.run(
        [READELF, "-h", "-l", "-d", "-n", "-W", str(path)],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=30,
        check=False,
    )
    if completed.returncode != 0:
        result["elf_state"] = "READELF_FAILED"
        result["readelf_error"] = completed.stderr.strip().replace("\t", " ") or f"rc={completed.returncode}"
        return result

    needed: list[str] = []
    for raw in completed.stdout.splitlines():
        line = raw.strip()
        if line.startswith("Class:"):
            result["elf_class"] = line.split(":", 1)[1].strip()
        elif line.startswith("Data:"):
            result["elf_data"] = line.split(":", 1)[1].strip()
        elif line.startswith("Type:"):
            result["elf_type"] = line.split(":", 1)[1].strip()
        elif line.startswith("Machine:"):
            result["elf_machine"] = line.split(":", 1)[1].strip()
        elif "Requesting program interpreter:" in line:
            value = line.split("Requesting program interpreter:", 1)[1].strip()
            result["interpreter"] = value.rstrip("]")
        elif "(NEEDED)" in line:
            value = parse_bracket_value(line)
            if value:
                needed.append(value)
        elif "(SONAME)" in line:
            value = parse_bracket_value(line)
            if value:
                result["soname"] = value
        elif "(RPATH)" in line:
            value = parse_bracket_value(line)
            if value:
                result["rpath"] = value
        elif "(RUNPATH)" in line:
            value = parse_bracket_value(line)
            if value:
                result["runpath"] = value
        elif "Build ID:" in line:
            result["build_id"] = line.split("Build ID:", 1)[1].strip()
    if needed:
        result["needed"] = ";".join(needed)
    return result


def profile_pressure(path: Path, file_type: str, elf_state: str) -> str:
    relative = str(path.relative_to(GLIBC_ROOT)) if within(path, GLIBC_ROOT) else str(path)
    parts = Path(relative).parts
    lower = relative.lower()
    if any(part in {"include", "libexec"} for part in parts):
        return "TOOLCHAIN_OR_BUILD_PRESSURE"
    if "/gcc/" in f"/{lower}/" or any(
        token in path.name
        for token in ("gcc", "g++", "cpp", "ld.bfd", "as", "ar", "ranlib", "strip")
    ):
        return "TOOLCHAIN_OR_BUILD_PRESSURE"
    if any(part in {"man", "info", "doc"} for part in parts):
        return "DOCUMENTATION_PRESSURE"
    if elf_state == "ELF" or parts[:1] in {("bin",), ("lib",), ("lib64",)}:
        return "RUNTIME_OR_TOOLCHAIN_UNRESOLVED"
    if parts[:1] in {("etc",), ("share",)}:
        return "DATA_OR_CONFIGURATION_PRESSURE"
    if file_type == "DIRECTORY":
        return "STRUCTURAL_PATH_ONLY"
    return "UNRESOLVED"


def capability_seed(
    primary_capability: str,
    historical_class: str,
    historical_action: str,
) -> str:
    tokens = set(filter(None, primary_capability.split(";")))
    groups: set[str] = set()
    mapping = {
        "app.obsidian.local": "app.obsidian.local",
        "app.obsidian.state": "runtime.mutable-cache",
        "world.glibc": "world.glibc.core",
        "world.locale.glibc": "data.locale",
        "provider.fonts.selected": "data.fonts",
        "provider.schemas.gsettings": "data.gsettings",
        "electron.gui.gtk3": "shared.gtk-stack",
        "electron.printing.cups": "shared.printing",
        "electron.security.nss": "shared.nss",
        "electron.graphics.gbm-base": "shared.graphics-frontend",
        "electron.device.udev": "platform.device-udev.termux",
        "electron.audio.alsa": "shared.audio",
        "runtime.compiler-support": "shared.compiler-runtime",
        "graphics.vulkan.feature": "shared.graphics-frontend",
        "runtime.cache.fontconfig": "runtime.mutable-cache",
        "runtime.cache.mesa": "runtime.mutable-cache",
        "device.gpu": "shared.graphics-frontend",
    }
    for token in tokens:
        groups.add(mapping.get(token, "app.obsidian.supplement"))

    if historical_class == "PROVIDER_LOCALE_DATA":
        groups.add("data.locale")
    elif historical_class == "PROVIDER_FONT_DATA":
        groups.add("data.fonts")
    elif historical_class == "PROVIDER_SCHEMA_DATA":
        groups.add("data.gsettings")
    elif historical_class.startswith("RUNTIME_CACHE_") or historical_class == "APP_MUTABLE_STATE":
        groups.add("runtime.mutable-cache")
    elif historical_class.startswith("APP_LOCAL_"):
        groups.add("app.obsidian.local")
    elif historical_class == "WORLD_SUBSTRATE_ELF":
        groups.add("world.glibc.core")
    elif historical_action in {
        "MATERIALIZE_SELECTED_STATIC_ELF",
        "MATERIALIZE_REQUIRED_DYNAMIC_ELF",
    } and not groups:
        groups.add("app.obsidian.supplement")

    return ";".join(sorted(groups)) if groups else "unassigned.prefix-surface"


def evidence_row_kind(historical_class: str) -> str:
    if historical_class == "DEVICE_NODE_GPU":
        return "DEVICE_RELATION"
    if historical_class == "APP_MUTABLE_STATE":
        return "MUTABLE_STATE"
    if historical_class.startswith("RUNTIME_CACHE_"):
        return "CACHE_CLASS"
    if historical_class == "PROVIDER_SCHEMA_DATA":
        return "GENERATED_DATA"
    if historical_class.endswith("_DATA"):
        return "DATA_OBJECT"
    if historical_class.startswith("APP_LOCAL_"):
        return "APP_LOCAL_OBJECT"
    if historical_class.endswith("_ELF"):
        return "ELF_OBJECT"
    return "PACKAGE_SURFACE"


def origin_relation(
    historical_class: str,
    rpath: str,
    runpath: str,
) -> str:
    if not historical_class.startswith("APP_LOCAL_"):
        return "NO_ORIGIN_RELATION"
    combined = f"{rpath}:{runpath}"
    if "$ORIGIN" in combined:
        return "PRESERVE_ORIGIN"
    return "REPLACEMENT_REQUIRES_EVIDENCE"


def semicolon(values: Iterable[str]) -> str:
    cleaned = sorted({value for value in values if value and value != "-"})
    return ";".join(cleaned) if cleaned else "-"


try:
    if OUT.exists():
        print(f"OUT already exists: {OUT}", file=sys.stderr)
        raise SystemExit(2)
    OUT.mkdir(parents=True, exist_ok=False)
    (OUT / "input").mkdir()

    for forbidden in (GLIBC_ROOT, ROOTFS, APP, HOME / "gl/selected/obsidian"):
        if within(OUT.resolve(), forbidden.resolve()):
            fail("output_preflight", f"OUT is inside a protected input tree: {forbidden}", 2)

    stage = "repository_state"
    dirty = subprocess.check_output(
        ["git", "-C", str(REPO), "status", "--porcelain", "--untracked-files=no"],
        text=True,
    ).strip()
    if dirty:
        fail(stage, "tracked working-tree changes detected; N2 requires exact HEAD", 2)
    branch = subprocess.check_output(
        ["git", "-C", str(REPO), "branch", "--show-current"],
        text=True,
    ).strip()
    head = subprocess.check_output(
        ["git", "-C", str(REPO), "rev-parse", "HEAD"],
        text=True,
    ).strip()

    required_inputs = {
        "b1_audit_status": B1_OUT / "audit.status",
        "b1_elf_objects": B1_OUT / "elf-objects.tsv",
        "b2_analysis_status": B2_OUT / "analysis.status",
        "b2_resolved_edges": B2_OUT / "resolved-edges.tsv",
        "b9_analysis_status": B9_OUT / "analysis.status",
        "b9_summary": B9_OUT / "summary.tsv",
        "b9_semantic_disposition": B9_OUT / "input/input__semantic-object-disposition.tsv",
        "b9_candidate_elf": B9_OUT / "input/input__candidate-elf-manifest.tsv",
        "b9_candidate_data": B9_OUT / "input/input__candidate-data-manifest.tsv",
        "b9_capability_membership": B9_OUT / "input/input__capability-membership.tsv",
        "b9_reference_manifest": B9_OUT / "input/input__reference-runtime-owned-manifest.tsv",
        "b9_content_plan": B9_OUT / "input/content-object-plan.tsv",
        "map_analysis_status": MAP_OUT / "analysis.status",
        "map_selected_state": MAP_OUT / "selected-map-state.tsv",
        "map_rpath_consumers": MAP_OUT / "selected-rpath-consumers.tsv",
        "map_rpath_edges": MAP_OUT / "rpath-provider-edges.tsv",
        "map_path_classification": MAP_OUT / "mapped-path-classification.tsv",
        "map_live_identity": MAP_OUT / "live-identity-verification.tsv",
        "map_summary": MAP_OUT / "summary.tsv",
        "pixbuf_analysis_status": PIXBUF_OUT / "analysis.status",
        "pixbuf_loader_cache": PIXBUF_OUT / "pixbuf-loader-cache.tsv",
        "pixbuf_cache_references": PIXBUF_OUT / "pixbuf-cache-references.tsv",
        "pixbuf_loader_modules": PIXBUF_OUT / "pixbuf-loader-modules.tsv",
        "pixbuf_gtk_data": PIXBUF_OUT / "gtk-data-capability.tsv",
        "pixbuf_semantic_gaps": PIXBUF_OUT / "semantic-coverage-gaps.tsv",
        "pixbuf_summary": PIXBUF_OUT / "summary.tsv",
        "schema_census_columns": SCHEMA_DIR / "census-columns.tsv",
        "schema_capability_groups": SCHEMA_DIR / "capability-groups.tsv",
    }

    stage = "input_verification"
    verification_rows: list[dict[str, object]] = []
    missing: list[str] = []
    for label, path in required_inputs.items():
        state_value = "PASS" if path.is_file() and not path.is_symlink() else "FAIL"
        embedded = OUT / "input" / f"{label}__{path.name}"
        verification_rows.append(
            {
                "input": label,
                "state": state_value,
                "path": str(path),
                "embedded_path": str(embedded) if state_value == "PASS" else "-",
                "sha256": sha256(path) if state_value == "PASS" else "-",
            }
        )
        if state_value == "PASS":
            shutil.copy2(path, embedded)
        else:
            missing.append(label)
    write_tsv(
        OUT / "input-verification.tsv",
        ["input", "state", "path", "embedded_path", "sha256"],
        verification_rows,
    )
    if missing:
        fail(stage, "missing required inputs: " + ", ".join(missing))

    expected_statuses = {
        B1_OUT / "audit.status": "PASS",
        B2_OUT / "analysis.status": "PASS",
        B9_OUT / "analysis.status": "PASS",
        MAP_OUT / "analysis.status": "PASS",
        PIXBUF_OUT / "analysis.status": "PASS",
    }
    for path, expected in expected_statuses.items():
        if path.read_text().strip() != expected:
            fail(stage, f"input status is not {expected}: {path}")

    if not GLIBC_ROOT.is_dir() or GLIBC_ROOT.is_symlink():
        fail("glibc_prefix_preflight", f"glibc prefix is not a plain directory: {GLIBC_ROOT}")
    if not DPKG_STATUS.is_file() or not DPKG_INFO.is_dir():
        fail("dpkg_preflight", "Termux dpkg status/info state is unavailable")
    if READELF is None:
        fail("tool_preflight", "readelf is required for complete ELF metadata")

    b9_summary = summary_map(B9_OUT / "summary.tsv")
    generation_dir = Path(b9_summary["generation_dir"])
    generation_base = generation_dir.parent.parent
    current_path = generation_base / "current"

    current_before = current_state(current_path)
    write_tsv(
        OUT / "current-state-before.tsv",
        ["state", "path", "link_target", "resolved_target", "inode"],
        [current_before],
    )
    if current_before["state"] != "ABSENT":
        fail("current_guard", "provider-authority census requires current to remain absent")

    dpkg_status_sha_before = sha256(DPKG_STATUS)
    dpkg_info_manifest_before = metadata_manifest(DPKG_INFO)

    stage = "generation_identity"
    content_rows = read_tsv(B9_OUT / "input/content-object-plan.tsv")
    generation_checks: list[dict[str, object]] = []
    generation_failures = 0
    for row in content_rows:
        object_path = generation_base / row["object_relpath"]
        exists = object_path.is_file() and not object_path.is_symlink()
        observed_sha = sha256(object_path) if exists else "MISSING"
        state_value = (
            "MATCH"
            if exists and observed_sha == row["sha256"]
            else "MISSING"
            if not exists
            else "HASH_MISMATCH"
        )
        generation_failures += int(state_value != "MATCH")
        generation_checks.append(
            {
                "content_kind": row["content_kind"],
                "source_path": row["source_path"],
                "object_path": str(object_path),
                "expected_sha256": row["sha256"],
                "observed_sha256": observed_sha,
                "state": state_value,
            }
        )
    write_tsv(
        OUT / "generation-identity-check.tsv",
        [
            "content_kind",
            "source_path",
            "object_path",
            "expected_sha256",
            "observed_sha256",
            "state",
        ],
        generation_checks,
    )
    if generation_failures:
        fail(stage, f"immutable generation identity failures: {generation_failures}")

    stage = "selected_reference_seed"
    semantic_rows = read_tsv(B9_OUT / "input/input__semantic-object-disposition.tsv")
    candidate_elf_rows = read_tsv(B9_OUT / "input/input__candidate-elf-manifest.tsv")
    candidate_data_rows = read_tsv(B9_OUT / "input/input__candidate-data-manifest.tsv")
    capability_rows = read_tsv(B9_OUT / "input/input__capability-membership.tsv")
    b1_elf_rows = read_tsv(B1_OUT / "elf-objects.tsv")
    edge_rows = read_tsv(B2_OUT / "resolved-edges.tsv")
    map_state_rows = read_tsv(MAP_OUT / "selected-map-state.tsv")
    map_class_rows = read_tsv(MAP_OUT / "mapped-path-classification.tsv")
    map_identity_rows = read_tsv(MAP_OUT / "live-identity-verification.tsv")
    map_rpath_rows = read_tsv(MAP_OUT / "selected-rpath-consumers.tsv")

    b1_elf_by_path = {row["path"]: row for row in b1_elf_rows}
    candidate_elf_by_path = {row["source_path"]: row for row in candidate_elf_rows}
    candidate_data_by_path = {row["source_path"]: row for row in candidate_data_rows}
    content_by_source = {
        row["source_path"]: row
        for row in content_rows
        if row["source_path"] != "GENERATED_FROM_SCHEMA_BUILD_CONTRACT"
    }
    content_by_sha = {row["sha256"]: row for row in content_rows}
    map_state_by_source = {row["source_path"]: row for row in map_state_rows}
    map_class_by_path = {row["path"]: row["category"] for row in map_class_rows}
    map_identity_by_path = defaultdict(list)
    for row in map_identity_rows:
        map_identity_by_path[row["path"]].append(row)
    map_rpath_by_source = {row["source_path"]: row for row in map_rpath_rows}

    capabilities_by_path: dict[str, set[str]] = defaultdict(set)
    for row in capability_rows:
        capabilities_by_path[row["object_path"]].add(row["capability"])

    consumers_by_provider: dict[str, list[str]] = defaultdict(list)
    needed_by_consumer: dict[str, list[str]] = defaultdict(list)
    for row in edge_rows:
        consumers_by_provider[row["provider_path"]].append(
            f"{row['consumer_path']}|{row['needed']}"
        )
        needed_by_consumer[row["consumer_path"]].append(row["needed"])

    seed_rows: list[dict[str, object]] = []
    semantic_by_path = {row["path"]: row for row in semantic_rows}
    for row in semantic_rows:
        path_text = row["path"]
        historical_class = row["semantic_class"]
        historical_action = row["primary_action"]
        b1_elf = b1_elf_by_path.get(path_text, {})
        candidate_elf = candidate_elf_by_path.get(path_text, {})
        candidate_data = candidate_data_by_path.get(path_text, {})
        content = content_by_source.get(path_text)
        if content is None and historical_action == "GENERATE_GSETTINGS_SCHEMA":
            content = content_by_sha.get(row["sha256"])
        map_state = map_state_by_source.get(path_text, {})
        map_category = map_class_by_path.get(path_text, "NOT_OBSERVED_OR_NOT_APPLICABLE")
        identities = map_identity_by_path.get(path_text, [])
        rpath_row = map_rpath_by_source.get(path_text, {})
        primary_capability = row.get("primary_capability", "")
        observed_caps = set(capabilities_by_path.get(path_text, set()))
        observed_caps.update(filter(None, primary_capability.split(";")))

        elf_rpath = b1_elf.get("rpath", "-")
        elf_runpath = b1_elf.get("runpath", "-")
        generation_object_path = "-"
        generation_content_kind = "-"
        if content:
            generation_content_kind = content["content_kind"]
            generation_object_path = str(generation_base / content["object_relpath"])

        identity_states = semicolon(identity["state"] for identity in identities)
        seed_rows.append(
            {
                "evidence_row_id": stable_id("selected", path_text),
                "evidence_row_kind": evidence_row_kind(historical_class),
                "capability_group_seed": capability_seed(
                    primary_capability,
                    historical_class,
                    historical_action,
                ),
                "path": path_text,
                "path_class": row.get("path_class", ""),
                "historical_semantic_class": historical_class,
                "historical_action": historical_action,
                "historical_primary_capability": primary_capability,
                "capability_memberships": semicolon(observed_caps),
                "package": row.get("package", ""),
                "version": row.get("version", ""),
                "sha256": row.get("sha256", ""),
                "lookup_name": candidate_elf.get(
                    "lookup_name", b1_elf.get("lookup_name", "-")
                ),
                "soname": candidate_elf.get("soname", b1_elf.get("soname", "-")),
                "rpath": rpath_row.get("rpath", elf_rpath),
                "runpath": rpath_row.get("runpath", elf_runpath),
                "app_local_origin_relation": origin_relation(
                    historical_class,
                    elf_rpath,
                    elf_runpath,
                ),
                "generation_content_kind": generation_content_kind,
                "generation_object_path": generation_object_path,
                "passive_map_state": map_state.get(
                    "map_state",
                    "REFERENCE_PATH" if map_category != "NOT_OBSERVED_OR_NOT_APPLICABLE" else "NOT_OBSERVED",
                ),
                "passive_map_category": map_category,
                "passive_identity_state": identity_states,
                "direct_consumer_count": len(consumers_by_provider.get(path_text, [])),
                "direct_consumers": semicolon(consumers_by_provider.get(path_text, [])),
                "needed_names": semicolon(needed_by_consumer.get(path_text, [])),
                "evidence_state": "OBSERVED",
                "authority_decision_state": "OPEN",
                "evidence_refs": (
                    "B9:semantic-object-disposition.tsv;"
                    "B1:elf-objects.tsv;"
                    "B2:resolved-edges.tsv;"
                    "MAP:selected-map-state.tsv"
                ),
                "notes": candidate_data.get("runtime_action", ""),
            }
        )

    if len(seed_rows) != len(semantic_rows) or len(seed_rows) != 161:
        fail(stage, f"selected/reference seed coverage mismatch: {len(seed_rows)}")
    write_tsv(
        OUT / "selected-reference-object-seed.tsv",
        [
            "evidence_row_id",
            "evidence_row_kind",
            "capability_group_seed",
            "path",
            "path_class",
            "historical_semantic_class",
            "historical_action",
            "historical_primary_capability",
            "capability_memberships",
            "package",
            "version",
            "sha256",
            "lookup_name",
            "soname",
            "rpath",
            "runpath",
            "app_local_origin_relation",
            "generation_content_kind",
            "generation_object_path",
            "passive_map_state",
            "passive_map_category",
            "passive_identity_state",
            "direct_consumer_count",
            "direct_consumers",
            "needed_names",
            "evidence_state",
            "authority_decision_state",
            "evidence_refs",
            "notes",
        ],
        seed_rows,
    )

    stage = "pixbuf_supplemental_evidence"
    supplemental_rows: list[dict[str, object]] = []
    pixbuf_cache_rows = read_tsv(PIXBUF_OUT / "pixbuf-loader-cache.tsv")
    pixbuf_module_rows = read_tsv(PIXBUF_OUT / "pixbuf-loader-modules.tsv")
    gtk_data_rows = read_tsv(PIXBUF_OUT / "gtk-data-capability.tsv")

    for row in pixbuf_cache_rows:
        supplemental_rows.append(
            {
                "evidence_row_id": stable_id("pixbuf-cache", row["path"]),
                "evidence_row_kind": "GENERATED_DATA",
                "capability_group_seed": "shared.pixbuf-codecs",
                "kind": "PIXBUF_LOADER_CACHE",
                "path": row["path"],
                "package": row["package"],
                "version": row["package_version"],
                "sha256": row["sha256"],
                "size_bytes": "-",
                "present_in_b9_semantic_manifest": "NO",
                "evidence_state": "OBSERVED",
                "authority_decision_state": "OPEN",
                "evidence_refs": "PIXBUF:pixbuf-loader-cache.tsv",
            }
        )
    for row in pixbuf_module_rows:
        supplemental_rows.append(
            {
                "evidence_row_id": stable_id("pixbuf-module", row["path"]),
                "evidence_row_kind": "ELF_OBJECT",
                "capability_group_seed": "shared.pixbuf-codecs",
                "kind": "PIXBUF_LOADER_MODULE",
                "path": row["path"],
                "package": row["package"],
                "version": row["package_version"],
                "sha256": row["sha256"],
                "size_bytes": row["size_bytes"],
                "present_in_b9_semantic_manifest": "NO",
                "evidence_state": "OBSERVED",
                "authority_decision_state": "OPEN",
                "evidence_refs": "PIXBUF:pixbuf-loader-modules.tsv",
            }
        )
    for row in gtk_data_rows:
        group = "data.icons" if row["kind"] == "ICON_THEME_INDEX" else "data.mime"
        supplemental_rows.append(
            {
                "evidence_row_id": stable_id("gtk-data", row["path"]),
                "evidence_row_kind": "DATA_OBJECT",
                "capability_group_seed": group,
                "kind": row["kind"],
                "path": row["path"],
                "package": row["package"],
                "version": row["package_version"],
                "sha256": row["sha256"],
                "size_bytes": row["size_bytes"],
                "present_in_b9_semantic_manifest": "NO",
                "evidence_state": "OBSERVED",
                "authority_decision_state": "OPEN",
                "evidence_refs": "PIXBUF:gtk-data-capability.tsv",
            }
        )
    write_tsv(
        OUT / "supplemental-capability-evidence.tsv",
        [
            "evidence_row_id",
            "evidence_row_kind",
            "capability_group_seed",
            "kind",
            "path",
            "package",
            "version",
            "sha256",
            "size_bytes",
            "present_in_b9_semantic_manifest",
            "evidence_state",
            "authority_decision_state",
            "evidence_refs",
        ],
        supplemental_rows,
    )

    stage = "package_surface_inventory"
    status_records = parse_dpkg_status(DPKG_STATUS)
    ownership: dict[str, set[str]] = defaultdict(set)
    package_list_files: dict[str, Path] = {}
    for list_file in sorted(DPKG_INFO.glob("*.list")):
        package_key = list_file.name[:-5]
        package_list_files[package_key] = list_file
        for line in list_file.read_text(errors="replace").splitlines():
            if not line.startswith("/"):
                continue
            listed = Path(line)
            if within(listed, GLIBC_ROOT):
                ownership[str(listed)].add(package_key)

    actual_paths = {str(GLIBC_ROOT)}
    for root, directories, files in os.walk(GLIBC_ROOT, followlinks=False):
        root_path = Path(root)
        actual_paths.add(str(root_path))
        for name in directories:
            actual_paths.add(str(root_path / name))
        for name in files:
            actual_paths.add(str(root_path / name))

    all_surface_paths = sorted(set(ownership) | actual_paths)
    selected_paths = set(semantic_by_path)
    surface_rows: list[dict[str, object]] = []
    surface_errors = 0

    for path_text in all_surface_paths:
        path = Path(path_text)
        owner_keys = sorted(ownership.get(path_text, set()))
        identities = [package_identity(key, status_records) for key in owner_keys]
        packages = semicolon(identity["package"] for identity in identities)
        versions = semicolon(
            f"{identity['package_key']}={identity['version']}" for identity in identities
        )
        architectures = semicolon(identity["architecture"] for identity in identities)
        statuses = semicolon(identity["status"] for identity in identities)

        exists = path.exists() or path.is_symlink()
        filesystem_state = "PRESENT" if exists else "LISTED_MISSING"
        file_type = "MISSING"
        mode_text = "-"
        size_bytes: object = "-"
        symlink_target = "-"
        resolved_path = "-"
        resolved_within_glibc = "-"
        file_sha = "-"
        hash_state = "NOT_APPLICABLE"
        elf = {
            "elf_state": "NOT_APPLICABLE",
            "elf_class": "-",
            "elf_data": "-",
            "elf_type": "-",
            "elf_machine": "-",
            "interpreter": "-",
            "soname": "-",
            "needed": "-",
            "rpath": "-",
            "runpath": "-",
            "build_id": "-",
            "readelf_error": "-",
        }

        if exists:
            try:
                metadata = path.lstat()
                file_type = classify_file_type(metadata.st_mode)
                mode_text = f"{stat.S_IMODE(metadata.st_mode):04o}"
                size_bytes = metadata.st_size
                if file_type == "SYMLINK":
                    symlink_target = os.readlink(path)
                    resolved = Path(os.path.normpath(str(path.parent / symlink_target)))
                    resolved_path = str(resolved)
                    resolved_within_glibc = "YES" if within(resolved, GLIBC_ROOT) else "NO"
                elif file_type == "REGULAR":
                    file_sha = sha256(path)
                    hash_state = "HASHED"
                    elf = inspect_elf(path)
                    if elf["elf_state"] in {"READ_ERROR", "READELF_MISSING", "READELF_FAILED"}:
                        surface_errors += 1
                elif file_type == "DIRECTORY":
                    hash_state = "DIRECTORY"
                else:
                    hash_state = "SPECIAL_FILE"
            except OSError as exc:
                filesystem_state = f"STAT_ERROR:{type(exc).__name__}"
                surface_errors += 1

        related_paths = {path_text}
        if resolved_path != "-":
            related_paths.add(resolved_path)
        selected_relations = [
            f"{candidate}:{semantic_by_path[candidate]['semantic_class']}:{semantic_by_path[candidate]['primary_action']}"
            for candidate in sorted(related_paths & selected_paths)
        ]
        consumers: list[str] = []
        for candidate in related_paths:
            consumers.extend(consumers_by_provider.get(candidate, []))

        surface_rows.append(
            {
                "path": path_text,
                "package_keys": semicolon(owner_keys),
                "packages": packages,
                "versions": versions,
                "architectures": architectures,
                "package_statuses": statuses,
                "ownership_state": "OWNED" if owner_keys else "UNOWNED",
                "filesystem_state": filesystem_state,
                "file_type": file_type,
                "mode": mode_text,
                "size_bytes": size_bytes,
                "symlink_target": symlink_target,
                "resolved_path": resolved_path,
                "resolved_within_glibc": resolved_within_glibc,
                "sha256": file_sha,
                "hash_state": hash_state,
                **elf,
                "selected_reference_relations": semicolon(selected_relations),
                "direct_consumer_count": len(set(consumers)),
                "direct_consumers": semicolon(consumers),
                "profile_pressure": profile_pressure(path, file_type, elf["elf_state"]),
                "evidence_state": "OBSERVED" if exists else "OBSERVED_LISTED_MISSING",
            }
        )

    write_tsv(
        OUT / "glibc-prefix-package-surface.tsv",
        [
            "path",
            "package_keys",
            "packages",
            "versions",
            "architectures",
            "package_statuses",
            "ownership_state",
            "filesystem_state",
            "file_type",
            "mode",
            "size_bytes",
            "symlink_target",
            "resolved_path",
            "resolved_within_glibc",
            "sha256",
            "hash_state",
            "elf_state",
            "elf_class",
            "elf_data",
            "elf_type",
            "elf_machine",
            "interpreter",
            "soname",
            "needed",
            "rpath",
            "runpath",
            "build_id",
            "readelf_error",
            "selected_reference_relations",
            "direct_consumer_count",
            "direct_consumers",
            "profile_pressure",
            "evidence_state",
        ],
        surface_rows,
    )
    if surface_errors:
        fail(stage, f"package-surface metadata errors: {surface_errors}")

    owner_packages = sorted({key for keys in ownership.values() for key in keys})
    control_suffixes = (
        "list",
        "md5sums",
        "conffiles",
        "preinst",
        "postinst",
        "prerm",
        "postrm",
        "triggers",
        "shlibs",
        "symbols",
    )
    control_rows: list[dict[str, object]] = []
    for package_key in owner_packages:
        identity = package_identity(package_key, status_records)
        for suffix in control_suffixes:
            path = DPKG_INFO / f"{package_key}.{suffix}"
            present = path.is_file() and not path.is_symlink()
            executable = "YES" if present and os.access(path, os.X_OK) else "NO"
            control_rows.append(
                {
                    **identity,
                    "control_kind": suffix,
                    "path": str(path),
                    "present": "YES" if present else "NO",
                    "executable": executable,
                    "sha256": sha256(path) if present else "-",
                    "size_bytes": path.stat().st_size if present else "-",
                }
            )
    write_tsv(
        OUT / "package-control-surface.tsv",
        [
            "package_key",
            "package",
            "version",
            "architecture",
            "status",
            "control_kind",
            "path",
            "present",
            "executable",
            "sha256",
            "size_bytes",
        ],
        control_rows,
    )

    surface_by_package: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in surface_rows:
        for package_key in str(row["package_keys"]).split(";"):
            if package_key and package_key != "-":
                surface_by_package[package_key].append(row)
    control_by_package: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in control_rows:
        if row["present"] == "YES":
            control_by_package[str(row["package_key"])].append(row)

    package_summary_rows: list[dict[str, object]] = []
    for package_key in owner_packages:
        identity = package_identity(package_key, status_records)
        rows = surface_by_package.get(package_key, [])
        package_summary_rows.append(
            {
                **identity,
                "surface_paths": len(rows),
                "regular_files": sum(row["file_type"] == "REGULAR" for row in rows),
                "symlinks": sum(row["file_type"] == "SYMLINK" for row in rows),
                "directories": sum(row["file_type"] == "DIRECTORY" for row in rows),
                "listed_missing": sum(row["filesystem_state"] == "LISTED_MISSING" for row in rows),
                "elf_files": sum(row["elf_state"] == "ELF" for row in rows),
                "total_regular_bytes": sum(
                    int(row["size_bytes"])
                    for row in rows
                    if row["file_type"] == "REGULAR"
                ),
                "selected_reference_paths": sum(
                    row["selected_reference_relations"] != "-" for row in rows
                ),
                "direct_consumer_edges": sum(int(row["direct_consumer_count"]) for row in rows),
                "present_control_files": semicolon(
                    str(row["control_kind"]) for row in control_by_package.get(package_key, [])
                ),
                "authority_decision_state": "OPEN",
            }
        )
    write_tsv(
        OUT / "glibc-prefix-package-summary.tsv",
        [
            "package_key",
            "package",
            "version",
            "architecture",
            "status",
            "surface_paths",
            "regular_files",
            "symlinks",
            "directories",
            "listed_missing",
            "elf_files",
            "total_regular_bytes",
            "selected_reference_paths",
            "direct_consumer_edges",
            "present_control_files",
            "authority_decision_state",
        ],
        package_summary_rows,
    )

    stage = "census_skeleton"
    census_field_rows = read_tsv(SCHEMA_DIR / "census-columns.tsv")
    census_fields = [row["field"] for row in sorted(census_field_rows, key=lambda row: int(row["ordinal"]))]
    group_rows = read_tsv(SCHEMA_DIR / "capability-groups.tsv")
    census_rows: list[dict[str, object]] = []

    def blank_census() -> dict[str, object]:
        return {field: "" for field in census_fields}

    for group in group_rows:
        row = blank_census()
        row.update(
            {
                "row_id": f"capability:{group['group_id']}",
                "row_type": "CAPABILITY",
                "capability_group": group["group_id"],
                "object_or_capability": group["capability_group"],
                "current_selected_or_reference_path": "NOT_APPLICABLE",
                "current_package_or_source_provenance": group["seed_evidence"],
                "historical_semantic_class": "NOT_APPLICABLE",
                "historical_action": "NOT_APPLICABLE",
                "semantic_class": "UNRESOLVED",
                "minimum_valid_scope": "UNRESOLVED",
                "application_domains": group["application_domains"],
                "app_local_origin_relation": "NO_ORIGIN_RELATION",
                "content_sha256": "NOT_APPLICABLE",
                "elf_build_id": "NOT_APPLICABLE",
                "lookup_name": "NOT_APPLICABLE",
                "soname": "NOT_APPLICABLE",
                "candidate_source_termux_glibc_package": "UNASSESSED",
                "candidate_source_exact_debian_artifact": "UNASSESSED",
                "candidate_source_upstream_or_app_local": "UNASSESSED",
                "candidate_source_project_build": "UNASSESSED",
                "candidate_source_native_termux_or_android": "UNASSESSED",
                "termux_android_adaptation_required": "UNKNOWN",
                "abi_version_coupling": "UNRESOLVED",
                "profile_runtime_or_research": "UNRESOLVED",
                "update_owner": "UNRESOLVED",
                "revalidation_trigger": "UNRESOLVED pending source and dependent identity classification",
                "provisional_final_authority": "UNRESOLVED",
                "unresolved_discriminating_evidence": group["unresolved_discriminating_evidence"],
                "evidence_state": "PROVISIONAL",
                "evidence_refs": group["seed_evidence"],
                "evidence_claim_scope": "N1 capability grouping seed; no provider decision",
                "evidence_conflict": "NONE",
                "authority_decision_state": "OPEN",
                "notes": f"initial_semantic_pressure={group['initial_semantic_pressure']};minimum_scope_pressure={group['minimum_scope_pressure']}",
            }
        )
        census_rows.append(row)

    for seed in seed_rows:
        row = blank_census()
        row_type = str(seed["evidence_row_kind"])
        row.update(
            {
                "row_id": seed["evidence_row_id"],
                "row_type": row_type,
                "capability_group": seed["capability_group_seed"],
                "object_or_capability": Path(str(seed["path"])).name or str(seed["path"]),
                "current_selected_or_reference_path": seed["path"],
                "current_package_or_source_provenance": f"{seed['package']}={seed['version']}",
                "historical_semantic_class": seed["historical_semantic_class"],
                "historical_action": seed["historical_action"],
                "semantic_class": "UNRESOLVED",
                "minimum_valid_scope": "UNRESOLVED",
                "application_domains": "obsidian",
                "app_local_origin_relation": seed["app_local_origin_relation"],
                "content_sha256": seed["sha256"],
                "elf_build_id": "UNKNOWN" if row_type in {"ELF_OBJECT", "APP_LOCAL_OBJECT"} else "NOT_APPLICABLE",
                "lookup_name": seed["lookup_name"],
                "soname": seed["soname"],
                "candidate_source_termux_glibc_package": "UNASSESSED",
                "candidate_source_exact_debian_artifact": "UNASSESSED",
                "candidate_source_upstream_or_app_local": "UNASSESSED",
                "candidate_source_project_build": "UNASSESSED",
                "candidate_source_native_termux_or_android": "UNASSESSED",
                "termux_android_adaptation_required": "UNKNOWN",
                "abi_version_coupling": f"needed={seed['needed_names']};direct_consumers={seed['direct_consumer_count']}",
                "profile_runtime_or_research": "UNRESOLVED",
                "update_owner": "UNRESOLVED",
                "revalidation_trigger": "content, provider, application, or workload-contract identity change",
                "provisional_final_authority": "UNRESOLVED",
                "unresolved_discriminating_evidence": "Compare all candidate authorities and adaptation/version coupling under 0116",
                "evidence_state": seed["evidence_state"],
                "evidence_refs": seed["evidence_refs"],
                "evidence_claim_scope": "retained selected-Obsidian B1/B2/B9/passive-map evidence",
                "evidence_conflict": "NONE",
                "authority_decision_state": "OPEN",
                "notes": (
                    f"generation_content_kind={seed['generation_content_kind']};"
                    f"generation_object_path={seed['generation_object_path']};"
                    f"passive_map_state={seed['passive_map_state']};"
                    f"passive_map_category={seed['passive_map_category']};"
                    f"historical_capabilities={seed['capability_memberships']}"
                ),
            }
        )
        census_rows.append(row)

    existing_member_paths = {str(seed["path"]) for seed in seed_rows}
    for supplemental in supplemental_rows:
        row = blank_census()
        row.update(
            {
                "row_id": supplemental["evidence_row_id"],
                "row_type": supplemental["evidence_row_kind"],
                "capability_group": supplemental["capability_group_seed"],
                "object_or_capability": Path(str(supplemental["path"])).name,
                "current_selected_or_reference_path": supplemental["path"],
                "current_package_or_source_provenance": f"{supplemental['package']}={supplemental['version']}",
                "historical_semantic_class": "ABSENT_FROM_B9_SEMANTIC_MANIFEST",
                "historical_action": "DIAGNOSTIC_INVENTORY_ONLY",
                "semantic_class": "UNRESOLVED",
                "minimum_valid_scope": "UNRESOLVED",
                "application_domains": "obsidian interactive Vault-open diagnostic",
                "app_local_origin_relation": "NO_ORIGIN_RELATION",
                "content_sha256": supplemental["sha256"],
                "elf_build_id": "UNKNOWN" if supplemental["evidence_row_kind"] == "ELF_OBJECT" else "NOT_APPLICABLE",
                "lookup_name": "UNKNOWN" if supplemental["evidence_row_kind"] == "ELF_OBJECT" else "NOT_APPLICABLE",
                "soname": "UNKNOWN" if supplemental["evidence_row_kind"] == "ELF_OBJECT" else "NOT_APPLICABLE",
                "candidate_source_termux_glibc_package": "UNASSESSED",
                "candidate_source_exact_debian_artifact": "CANDIDATE_IDENTIFIED: current rootfs package evidence",
                "candidate_source_upstream_or_app_local": "UNASSESSED",
                "candidate_source_project_build": "UNASSESSED",
                "candidate_source_native_termux_or_android": "UNASSESSED",
                "termux_android_adaptation_required": "UNKNOWN",
                "abi_version_coupling": "UNRESOLVED loader/cache/data compatibility",
                "profile_runtime_or_research": "UNRESOLVED",
                "update_owner": "UNRESOLVED",
                "revalidation_trigger": "bounded pixbuf/icon/MIME discriminator or source identity change",
                "provisional_final_authority": "UNRESOLVED",
                "unresolved_discriminating_evidence": "Minimum required capability and final source authority remain open",
                "evidence_state": "OBSERVED",
                "evidence_refs": supplemental["evidence_refs"],
                "evidence_claim_scope": "read-only diagnostic inventory; no runtime requirement proven",
                "evidence_conflict": "NONE",
                "authority_decision_state": "OPEN",
                "notes": f"kind={supplemental['kind']};present_in_b9_semantic_manifest=NO",
            }
        )
        census_rows.append(row)

    for surface in surface_rows:
        if surface["file_type"] == "DIRECTORY":
            continue
        path_text = str(surface["path"])
        if path_text in existing_member_paths:
            continue
        row = blank_census()
        row_type = "ELF_OBJECT" if surface["elf_state"] == "ELF" else "PACKAGE_SURFACE"
        group_id = "unassigned.prefix-surface"
        row.update(
            {
                "row_id": stable_id("prefix", path_text),
                "row_type": row_type,
                "capability_group": group_id,
                "object_or_capability": Path(path_text).name,
                "current_selected_or_reference_path": path_text,
                "current_package_or_source_provenance": (
                    f"packages={surface['packages']};versions={surface['versions']};"
                    f"ownership={surface['ownership_state']}"
                ),
                "historical_semantic_class": "NOT_IN_B9_SELECTED_REFERENCE_SET",
                "historical_action": "PREFIX_SURFACE_INVENTORY_ONLY",
                "semantic_class": "UNRESOLVED",
                "minimum_valid_scope": "UNRESOLVED",
                "application_domains": "UNRESOLVED",
                "app_local_origin_relation": "NO_ORIGIN_RELATION",
                "content_sha256": surface["sha256"] if surface["sha256"] != "-" else "NOT_APPLICABLE",
                "elf_build_id": surface["build_id"] if row_type == "ELF_OBJECT" else "NOT_APPLICABLE",
                "lookup_name": (
                    surface["soname"]
                    if row_type == "ELF_OBJECT" and surface["soname"] != "-"
                    else Path(path_text).name
                    if row_type == "ELF_OBJECT"
                    else "NOT_APPLICABLE"
                ),
                "soname": surface["soname"] if row_type == "ELF_OBJECT" else "NOT_APPLICABLE",
                "candidate_source_termux_glibc_package": (
                    "ARTIFACT_IDENTIFIED: installed dpkg ownership"
                    if surface["ownership_state"] == "OWNED"
                    else "UNASSESSED"
                ),
                "candidate_source_exact_debian_artifact": "UNASSESSED",
                "candidate_source_upstream_or_app_local": "UNASSESSED",
                "candidate_source_project_build": "UNASSESSED",
                "candidate_source_native_termux_or_android": "UNASSESSED",
                "termux_android_adaptation_required": "UNKNOWN",
                "abi_version_coupling": (
                    f"needed={surface['needed']};direct_consumers={surface['direct_consumer_count']}"
                ),
                "profile_runtime_or_research": "UNRESOLVED",
                "update_owner": "UNRESOLVED",
                "revalidation_trigger": "package/content/provider dependency identity change",
                "provisional_final_authority": "UNRESOLVED",
                "unresolved_discriminating_evidence": (
                    "Assign semantic capability, minimum scope, adaptation rationale, candidate sources, and profile"
                ),
                "evidence_state": surface["evidence_state"],
                "evidence_refs": "N2:glibc-prefix-package-surface.tsv",
                "evidence_claim_scope": "current read-only Termux dpkg and filesystem observation",
                "evidence_conflict": "NONE",
                "authority_decision_state": "OPEN",
                "notes": (
                    f"file_type={surface['file_type']};profile_pressure={surface['profile_pressure']};"
                    f"resolved_path={surface['resolved_path']};selected_relations={surface['selected_reference_relations']}"
                ),
            }
        )
        census_rows.append(row)

    write_tsv(
        OUT / "provider-authority-census.tsv",
        census_fields,
        census_rows,
    )

    group_member_counts: Counter[str] = Counter()
    for row in census_rows:
        if row["row_type"] != "CAPABILITY":
            for group_id in str(row["capability_group"]).split(";"):
                group_member_counts[group_id] += 1

    ledger_rows: list[dict[str, object]] = []
    for group in group_rows:
        group_id = group["group_id"]
        ledger_rows.append(
            {
                "group_id": group_id,
                "capability_group": group["capability_group"],
                "current_state": group["current_state"],
                "evidence_member_rows": group_member_counts[group_id],
                "seed_evidence": group["seed_evidence"],
                "unresolved_discriminating_evidence": group["unresolved_discriminating_evidence"],
                "next_permitted_action": (
                    "READ_ONLY_CLASSIFICATION_AND_SOURCE_COMPARISON"
                    if group_id not in {"shared.pixbuf-codecs", "data.icons", "data.mime"}
                    else "READ_ONLY_CLASSIFICATION_OR_BOUNDED_PIXBUF_DISCRIMINATOR"
                ),
                "authority_decision_state": "OPEN",
            }
        )
    write_tsv(
        OUT / "unresolved-evidence-ledger.tsv",
        [
            "group_id",
            "capability_group",
            "current_state",
            "evidence_member_rows",
            "seed_evidence",
            "unresolved_discriminating_evidence",
            "next_permitted_action",
            "authority_decision_state",
        ],
        ledger_rows,
    )

    stage = "final_guards"
    current_after = current_state(current_path)
    write_tsv(
        OUT / "current-state-after.tsv",
        ["state", "path", "link_target", "resolved_target", "inode"],
        [current_after],
    )
    dpkg_status_sha_after = sha256(DPKG_STATUS)
    dpkg_info_manifest_after = metadata_manifest(DPKG_INFO)
    if current_after != current_before:
        fail(stage, "current pointer changed during read-only census")
    if dpkg_status_sha_after != dpkg_status_sha_before:
        fail(stage, "dpkg status changed during read-only census")
    if dpkg_info_manifest_after != dpkg_info_manifest_before:
        fail(stage, "dpkg info metadata changed during read-only census")

    file_type_counts = Counter(str(row["file_type"]) for row in surface_rows)
    elf_count = sum(row["elf_state"] == "ELF" for row in surface_rows)
    unowned_count = sum(row["ownership_state"] == "UNOWNED" for row in surface_rows)
    summary_rows = [
        {"field": "branch", "value": branch},
        {"field": "head", "value": head},
        {"field": "phase_b1_root", "value": str(B1_OUT)},
        {"field": "phase_b2_root", "value": str(B2_OUT)},
        {"field": "phase_b9_root", "value": str(B9_OUT)},
        {"field": "map_diagnostic_root", "value": str(MAP_OUT)},
        {"field": "pixbuf_inventory_root", "value": str(PIXBUF_OUT)},
        {"field": "glibc_root", "value": str(GLIBC_ROOT)},
        {"field": "generation_id", "value": b9_summary.get("generation_id", "")},
        {"field": "generation_content_checks", "value": len(generation_checks)},
        {"field": "generation_identity_failures", "value": generation_failures},
        {"field": "selected_reference_seed_rows", "value": len(seed_rows)},
        {"field": "supplemental_pixbuf_icon_mime_rows", "value": len(supplemental_rows)},
        {"field": "glibc_prefix_surface_rows", "value": len(surface_rows)},
        {"field": "glibc_prefix_packages", "value": len(owner_packages)},
        {"field": "glibc_prefix_regular_files", "value": file_type_counts["REGULAR"]},
        {"field": "glibc_prefix_symlinks", "value": file_type_counts["SYMLINK"]},
        {"field": "glibc_prefix_directories", "value": file_type_counts["DIRECTORY"]},
        {"field": "glibc_prefix_listed_missing", "value": file_type_counts["MISSING"]},
        {"field": "glibc_prefix_elf_files", "value": elf_count},
        {"field": "glibc_prefix_unowned_paths", "value": unowned_count},
        {"field": "package_surface_metadata_errors", "value": surface_errors},
        {"field": "capability_group_rows", "value": len(group_rows)},
        {"field": "provider_authority_census_rows", "value": len(census_rows)},
        {"field": "authority_decisions_accepted", "value": 0},
        {"field": "dpkg_status_sha256_before", "value": dpkg_status_sha_before},
        {"field": "dpkg_status_sha256_after", "value": dpkg_status_sha_after},
        {"field": "dpkg_info_manifest_before", "value": dpkg_info_manifest_before},
        {"field": "dpkg_info_manifest_after", "value": dpkg_info_manifest_after},
        {"field": "current_state_before", "value": current_before["state"]},
        {"field": "current_state_after", "value": current_after["state"]},
        {"field": "current_pointer_changed", "value": "NO"},
        {"field": "package_operation_performed", "value": "NO"},
        {"field": "runtime_launch_performed", "value": "NO"},
        {"field": "generation_mutated", "value": "NO"},
        {"field": "promoted_launcher_changed", "value": "NO"},
        {"field": "successor_manifest_finalized", "value": "NO"},
    ]
    write_tsv(OUT / "summary.tsv", ["field", "value"], summary_rows)

    (OUT / "claim-boundary.txt").write_text(
        "This stage is a read-only N2 provider-authority evidence census.\n"
        "It reuses accepted B1/B2/B9/passive-map/pixbuf receipts, verifies the existing immutable generation, "
        "and inventories the current Termux dpkg-owned and unowned filesystem surface under $PREFIX/glibc.\n"
        "The provider-authority census is an OPEN skeleton: historical classes, path ownership, package presence, "
        "and candidate availability are evidence only and do not choose final providers.\n"
        "No package operation, workload launch, generation mutation, current activation, launcher change, "
        "provider cleanup, successor manifest finalization, or graphics-gate reopening is performed.\n"
    )
    (OUT / "next-state.txt").write_text(
        "READY_FOR_N3_PROVISIONAL_AUTHORITY_CLASSIFICATION\n"
    )
    write_status("PASS")
    if (OUT / "failure-stage.txt").exists():
        (OUT / "failure-stage.txt").unlink()

    print("selected Obsidian provider-authority N2 read-only evidence: PASS")
    print(f"evidence: {OUT}")
    print("\n===== summary =====")
    for row in summary_rows:
        print(f"{row['field']}\t{row['value']}")

except SystemExit:
    raise
except Exception:
    write_status("FAIL")
    (OUT / "failure-stage.txt").write_text(stage + "\n")
    traceback.print_exc()
    print(f"evidence: {OUT}", file=sys.stderr)
    raise SystemExit(1)
