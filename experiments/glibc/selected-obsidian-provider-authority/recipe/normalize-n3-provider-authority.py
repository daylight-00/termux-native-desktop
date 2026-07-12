#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import os
import shutil
import subprocess
import sys
import traceback
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable

N2_OUT = Path(os.environ["N2_OUT"])
OUT = Path(os.environ["OUT"])
REPO = Path(subprocess.check_output([
    "git", "-C", str(Path(__file__).resolve().parent), "rev-parse", "--show-toplevel"
], text=True).strip())
SCHEMA_DIR = REPO / "experiments/glibc/selected-obsidian-provider-authority/schema"
stage = "initialization"


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


def semicolon(values: Iterable[str]) -> str:
    cleaned = sorted({value for value in values if value and value != "-"})
    return ";".join(cleaned) if cleaned else "-"


def package_keys(value: str) -> list[str]:
    return [item for item in value.split(";") if item and item != "-"]


def profile_for_semantic(semantic: str) -> str:
    if semantic in {
        "WORLD_CORE_SUBSTRATE",
        "PLATFORM_INTEGRATION_PROVIDER",
        "GENERIC_SHARED_CAPABILITY_PROVIDER",
        "APPLICATION_LOCAL",
        "APPLICATION_DOMAIN_SUPPLEMENT",
        "DATA_CAPABILITY_PROVIDER",
    }:
        return "RUNTIME"
    if semantic == "TOOLCHAIN_ONLY":
        return "RESEARCH_BUILD_MAINTENANCE"
    if semantic in {"ORACLE_ONLY", "MUTABLE_OR_CACHE"}:
        return "NEITHER"
    return "UNRESOLVED"


def update_owner_for_semantic(semantic: str) -> str:
    return {
        "WORLD_CORE_SUBSTRATE": "WORLD_SUBSTRATE",
        "PLATFORM_INTEGRATION_PROVIDER": "PROVIDER",
        "GENERIC_SHARED_CAPABILITY_PROVIDER": "PROVIDER",
        "APPLICATION_LOCAL": "APPLICATION",
        "APPLICATION_DOMAIN_SUPPLEMENT": "APPLICATION",
        "DATA_CAPABILITY_PROVIDER": "PROVIDER",
        "TOOLCHAIN_ONLY": "TOOLCHAIN",
        "ORACLE_ONLY": "ORACLE_SCENARIO",
        "MUTABLE_OR_CACHE": "MUTABLE_STATE",
    }.get(semantic, "UNRESOLVED")


def scope_for_semantic(semantic: str) -> str:
    return {
        "WORLD_CORE_SUBSTRATE": "WORLD",
        "PLATFORM_INTEGRATION_PROVIDER": "PLATFORM_INTEGRATION",
        "GENERIC_SHARED_CAPABILITY_PROVIDER": "SHARED_CAPABILITY",
        "APPLICATION_LOCAL": "APPLICATION_LOCAL",
        "APPLICATION_DOMAIN_SUPPLEMENT": "APPLICATION_DOMAIN",
        "DATA_CAPABILITY_PROVIDER": "DATA_CAPABILITY",
        "TOOLCHAIN_ONLY": "BUILD_SUPPLY",
        "ORACLE_ONLY": "ORACLE_SCENARIO",
        "MUTABLE_OR_CACHE": "MUTABLE_CACHE",
    }.get(semantic, "UNRESOLVED")


def group_semantic(group_ids: str) -> str:
    groups = set(group_ids.split(";"))
    if "app.obsidian.local" in groups:
        return "APPLICATION_LOCAL"
    if "runtime.mutable-cache" in groups:
        return "MUTABLE_OR_CACHE"
    if any(group.startswith("data.") for group in groups):
        return "DATA_CAPABILITY_PROVIDER"
    if any(group.startswith("platform.") for group in groups):
        return "PLATFORM_INTEGRATION_PROVIDER"
    if "world.glibc.core" in groups:
        return "WORLD_CORE_SUBSTRATE"
    if any(group.startswith("shared.") for group in groups):
        return "GENERIC_SHARED_CAPABILITY_PROVIDER"
    if "app.obsidian.supplement" in groups:
        return "APPLICATION_DOMAIN_SUPPLEMENT"
    if "build.glibc-target" in groups:
        return "TOOLCHAIN_ONLY"
    if "oracle.debian-scenarios" in groups:
        return "ORACLE_ONLY"
    return "UNRESOLVED"


def selected_pressure(seed_row: dict[str, str]) -> tuple[str, str]:
    groups = {group for group in seed_row["capability_group_seed"].split(";") if group}
    package_key = seed_row["package"].split(":", 1)[0]
    mapped_group = PACKAGE_GROUPS.get(package_key)
    if mapped_group and mapped_group != "unassigned.prefix-surface":
        groups.add(mapped_group)

    action = seed_row["historical_action"]
    path_name = Path(seed_row["path"]).name

    if action == "EXCLUDE_CPU_BASE_GRAPHICS_FEATURE":
        semantic = "GENERIC_SHARED_CAPABILITY_PROVIDER"
    elif action == "REFERENCE_APP_LOCAL":
        semantic = "APPLICATION_LOCAL"
    elif action in {"ISOLATED_MUTABLE_STATE", "REGENERATE_RUNTIME_CACHE"}:
        semantic = "MUTABLE_OR_CACHE"
    elif action in {"MATERIALIZE_SELECTED_FONT", "GENERATE_GSETTINGS_SCHEMA", "REFERENCE_WORLD_LOCALE"}:
        semantic = "DATA_CAPABILITY_PROVIDER"
    elif action == "REFERENCE_WORLD_SUBSTRATE":
        semantic = "WORLD_CORE_SUBSTRATE"
    elif package_key in PLATFORM_X11_PACKAGES:
        groups.add("platform.x11-xcb.termux")
        semantic = "PLATFORM_INTEGRATION_PROVIDER"
    elif package_key == "termux-exec-glibc":
        groups.add("platform.glibc-adaptation.termux")
        semantic = "PLATFORM_INTEGRATION_PROVIDER"
    elif package_key in {"libudev", "libudev1"} or path_name.startswith("libudev.so"):
        groups.add("platform.device-udev.termux")
        semantic = "PLATFORM_INTEGRATION_PROVIDER"
    else:
        # Historical capability membership records consumer responsibility, not
        # automatic source authority. Ignore platform membership unless the
        # concrete object itself carries platform-specific pressure above.
        non_platform = {group for group in groups if not group.startswith("platform.")}
        semantic = group_semantic(";".join(sorted(non_platform)))

    return semicolon(groups), semantic


TOOLCHAIN_PACKAGES = {
    "gcc-glibc", "binutils-glibc", "binutils-libs-glibc", "linux-api-headers-glibc",
    "xorgproto-glibc", "xcb-proto-glibc", "xorg-util-macros-glibc", "vulkan-headers-glibc",
    "patchelf-glibc", "strace-glibc", "libdebuginfod-glibc",
}
PLATFORM_X11_PACKAGES = {
    "libx11-glibc", "libxau-glibc", "libxcb-glibc", "libxdmcp-glibc", "libxext-glibc",
    "libxrandr-glibc", "libxrender-glibc", "libxshmfence-glibc", "libxxf86vm-glibc",
}
GRAPHICS_PACKAGES = {
    "libdrm-glibc", "libpciaccess-glibc", "libwayland-glibc", "vulkan-icd-loader-glibc",
}
DATA_PACKAGES = {"ca-certificates-glibc"}
MAINTENANCE_PACKAGES = {
    "bash-completion-glibc", "bash-glibc", "coreutils-glibc", "curl-glibc", "findutils-glibc",
    "grep-glibc", "less-glibc", "sed-glibc", "tar-glibc", "xz-utils-glibc", "perl-glibc",
    "util-linux-glibc", "e2fsprogs-glibc", "vulkan-tools-glibc", "glibc-runner",
}
PACKAGE_GROUPS = {
    "openssl-glibc": "shared.tls", "ca-certificates-glibc": "shared.tls",
    "krb5-glibc": "shared.tls", "gcc-libs-glibc": "shared.compiler-runtime",
    "brotli-glibc": "shared.compression-archive", "bzip2-glibc": "shared.compression-archive",
    "libbz2-glibc": "shared.compression-archive", "liblz4-glibc": "shared.compression-archive",
    "liblzma-glibc": "shared.compression-archive", "xz-utils-glibc": "shared.compression-archive",
    "zlib-glibc": "shared.compression-archive", "zstd-glibc": "shared.compression-archive",
    "libx11-glibc": "platform.x11-xcb.termux", "libxau-glibc": "platform.x11-xcb.termux",
    "libxcb-glibc": "platform.x11-xcb.termux", "libxdmcp-glibc": "platform.x11-xcb.termux",
    "libxext-glibc": "platform.x11-xcb.termux", "libxrandr-glibc": "platform.x11-xcb.termux",
    "libxrender-glibc": "platform.x11-xcb.termux", "libxshmfence-glibc": "platform.x11-xcb.termux",
    "libxxf86vm-glibc": "platform.x11-xcb.termux", "libdrm-glibc": "shared.graphics-frontend",
    "libpciaccess-glibc": "shared.graphics-frontend", "libwayland-glibc": "shared.graphics-frontend",
    "vulkan-icd-loader-glibc": "shared.graphics-frontend", "glibc": "world.glibc.core",
    "termux-exec-glibc": "platform.glibc-adaptation.termux", "glibc-runner": "unassigned.prefix-surface",
}


def package_pressure(package_key: str, selected_pressure: int = 0) -> dict[str, str]:
    group = PACKAGE_GROUPS.get(package_key, "unassigned.prefix-surface")
    semantic = "UNRESOLVED"
    profile = "UNRESOLVED"
    update_owner = "UNRESOLVED"
    adaptation = "UNKNOWN"
    rationale = "package presence alone is not semantic authority"

    if package_key == "glibc":
        semantic = "WORLD_CORE_SUBSTRATE"
        profile = "BOTH_WITH_SEPARATE_ARTIFACTS"
        update_owner = "WORLD_SUBSTRATE"
        rationale = "package mixes loader/libc runtime with tools, headers, and data; object split required"
    elif package_key in PLATFORM_X11_PACKAGES or package_key == "termux-exec-glibc":
        semantic = "PLATFORM_INTEGRATION_PROVIDER"
        profile = "RUNTIME"
        update_owner = "PROVIDER"
        adaptation = "POSSIBLE"
        rationale = "Termux/Android integration pressure; recipe/patch comparison required"
    elif package_key in GRAPHICS_PACKAGES:
        semantic = "GENERIC_SHARED_CAPABILITY_PROVIDER"
        profile = "RUNTIME"
        update_owner = "PROVIDER"
        adaptation = "POSSIBLE"
        rationale = "graphics relation retained under closed graphics authority"
    elif package_key in DATA_PACKAGES:
        semantic = "DATA_CAPABILITY_PROVIDER"
        profile = "RUNTIME"
        update_owner = "PROVIDER"
        rationale = "data capability pressure; native/Termux authority comparison required"
    elif package_key in TOOLCHAIN_PACKAGES:
        semantic = "TOOLCHAIN_ONLY"
        profile = "RESEARCH_BUILD_MAINTENANCE"
        update_owner = "TOOLCHAIN"
        rationale = "compiler, binutils, headers, protocol/build metadata, or inspection tool"
    elif package_key in MAINTENANCE_PACKAGES:
        profile = "RESEARCH_BUILD_MAINTENANCE"
        rationale = "maintenance utility presence without accepted workstation runtime claim"
    elif package_key.startswith("lib") or package_key in {
        "openssl-glibc", "krb5-glibc", "pcre2-glibc", "ncurses-glibc", "readline-glibc",
        "zlib-glibc", "zstd-glibc", "brotli-glibc", "bzip2-glibc", "attr-glibc",
    }:
        semantic = "GENERIC_SHARED_CAPABILITY_PROVIDER"
        profile = "RUNTIME" if selected_pressure else "UNRESOLVED"
        update_owner = "PROVIDER"
        rationale = "generic shared library pressure; consumer and source comparison required"

    return {
        "capability_group": group,
        "semantic_class": semantic,
        "minimum_valid_scope": scope_for_semantic(semantic),
        "profile": profile,
        "update_owner": update_owner,
        "adaptation": adaptation,
        "rationale": rationale,
    }


def prefix_elf_pressure(
    row: dict[str, str],
    package_key: str,
    selected_pressure: int,
    glibc_root: Path,
) -> dict[str, str]:
    pressure = package_pressure(package_key, selected_pressure).copy()
    path = Path(row["path"])
    try:
        rel = path.relative_to(glibc_root)
    except ValueError:
        rel = path
    top = rel.parts[0] if rel.parts else ""

    if package_key == "glibc":
        name = path.name
        tool_names = {
            "Mcrt1.o", "Scrt1.o", "crt1.o", "crti.o", "crtn.o", "gcrt1.o",
            "sotruss-lib.so", "libc_malloc_debug.so.0", "libmemusage.so",
            "libpcprofile.so", "libmcheck.a",
        }
        if name == "libsyscall_without_fsc.so":
            pressure.update({
                "capability_group": "platform.glibc-adaptation.termux",
                "semantic_class": "PLATFORM_INTEGRATION_PROVIDER",
                "minimum_valid_scope": "PLATFORM_INTEGRATION",
                "profile": "RUNTIME",
                "update_owner": "WORLD_SUBSTRATE",
                "adaptation": "YES",
                "rationale": "Termux-glibc syscall adaptation object requires source/consumer authority review",
            })
        elif top in {"bin", "sbin", "libexec"} or name in tool_names:
            pressure.update({
                "capability_group": "build.glibc-target" if name in tool_names else "world.glibc.core",
                "semantic_class": "TOOLCHAIN_ONLY" if name in tool_names else "UNRESOLVED",
                "minimum_valid_scope": "BUILD_SUPPLY" if name in tool_names else "UNRESOLVED",
                "profile": "RESEARCH_BUILD_MAINTENANCE",
                "update_owner": "TOOLCHAIN" if name in tool_names else "WORLD_SUBSTRATE",
                "rationale": "glibc-package executable/diagnostic/startfile is not automatically world core",
            })
        else:
            pressure.update({
                "semantic_class": "WORLD_CORE_SUBSTRATE",
                "minimum_valid_scope": "WORLD",
                "profile": "RUNTIME",
                "update_owner": "WORLD_SUBSTRATE",
                "rationale": "glibc-package library/module is world-version-coupled; exact core boundary still requires review",
            })
        return pressure

    if top in {"bin", "sbin", "libexec"} or row.get("elf_type", "").startswith("EXEC"):
        if package_key in TOOLCHAIN_PACKAGES:
            pressure.update({
                "semantic_class": "TOOLCHAIN_ONLY",
                "minimum_valid_scope": "BUILD_SUPPLY",
                "profile": "RESEARCH_BUILD_MAINTENANCE",
                "update_owner": "TOOLCHAIN",
                "rationale": "ELF executable belongs to an explicit build/inspection tool package",
            })
        elif package_key not in {"termux-exec-glibc"}:
            pressure.update({
                "semantic_class": "UNRESOLVED",
                "minimum_valid_scope": "UNRESOLVED",
                "profile": "RESEARCH_BUILD_MAINTENANCE",
                "update_owner": "UNRESOLVED",
                "rationale": "installed ELF executable has no accepted workstation runtime claim",
            })
    return pressure


def aggregate_semantic_pressure(
    package_key: str,
    surface_kind: str,
    pressure: dict[str, str],
) -> tuple[str, str, str, str]:
    semantic = pressure["semantic_class"]
    group = pressure["capability_group"]
    profile = pressure["profile"]
    update_owner = pressure["update_owner"]

    if surface_kind in {"HEADER", "STATIC_OR_STARTFILE", "BUILD_METADATA"}:
        return "TOOLCHAIN_ONLY", "build.glibc-target", "RESEARCH_BUILD_MAINTENANCE", "TOOLCHAIN"
    if surface_kind == "DOCUMENTATION":
        return "TOOLCHAIN_ONLY", "build.glibc-target", "NEITHER", "TOOLCHAIN"
    if surface_kind == "EXECUTABLE_TOOL":
        if package_key in TOOLCHAIN_PACKAGES:
            return "TOOLCHAIN_ONLY", "build.glibc-target", "RESEARCH_BUILD_MAINTENANCE", "TOOLCHAIN"
        return "UNRESOLVED", pressure["capability_group"], "RESEARCH_BUILD_MAINTENANCE", "UNRESOLVED"
    if surface_kind == "LOCALE_DATA":
        return "DATA_CAPABILITY_PROVIDER", "data.locale", "RUNTIME", "PROVIDER"
    if surface_kind == "CONFIGURATION" and package_key == "glibc":
        return "WORLD_CORE_SUBSTRATE", "world.glibc.core", "RUNTIME", "WORLD_SUBSTRATE"
    if surface_kind == "SHARED_DATA" and package_key in DATA_PACKAGES:
        return "DATA_CAPABILITY_PROVIDER", "shared.tls", "RUNTIME", "PROVIDER"
    if package_key == "glibc" and surface_kind not in {"CONFIGURATION", "LOCALE_DATA"}:
        return "UNRESOLVED", "world.glibc.core", pressure["profile"], "WORLD_SUBSTRATE"
    return semantic, group, profile, update_owner


def surface_class(row: dict[str, str], glibc_root: Path) -> str:
    path = Path(row["path"])
    try:
        rel = path.relative_to(glibc_root)
    except ValueError:
        rel = path
    parts = rel.parts
    lower = str(rel).lower()
    name = path.name.lower()
    if parts and parts[0] == "include":
        return "HEADER"
    if name.endswith(".a") or name.endswith(".o") or name.startswith("crt"):
        return "STATIC_OR_STARTFILE"
    if "pkgconfig" in parts or "cmake" in parts or "aclocal" in parts or name.endswith((".pc", ".cmake", ".m4")):
        return "BUILD_METADATA"
    if parts and parts[0] in {"bin", "sbin", "libexec"}:
        return "EXECUTABLE_TOOL"
    if parts and parts[0] == "etc":
        return "CONFIGURATION"
    if "share/locale" in lower or "lib/locale" in lower:
        return "LOCALE_DATA"
    if any(token in parts for token in ("man", "info", "doc")):
        return "DOCUMENTATION"
    if parts and parts[0] == "share":
        return "SHARED_DATA"
    if any(token in lower for token in ("/perl", "/python", "/bash-completion")):
        return "SCRIPT_OR_LANGUAGE_MODULE"
    if row["file_type"] == "SYMLINK":
        return "SYMLINK_ALIAS"
    return "OTHER_NON_ELF"


def candidate_fields(path: str, package: str, version: str, semantic: str) -> dict[str, str]:
    result = {
        "candidate_source_termux_glibc_package": "UNASSESSED",
        "candidate_source_exact_debian_artifact": "UNASSESSED",
        "candidate_source_upstream_or_app_local": "UNASSESSED",
        "candidate_source_project_build": "UNASSESSED",
        "candidate_source_native_termux_or_android": "UNASSESSED",
    }
    if "/files/usr/glibc/" in path:
        result["candidate_source_termux_glibc_package"] = f"ARTIFACT_IDENTIFIED: installed {package}={version}"
    if "/proot-distro/" in path:
        result["candidate_source_exact_debian_artifact"] = f"CANDIDATE_IDENTIFIED: {package}={version}; exact artifact not locked"
    if "/gl/apps/obsidian/" in path or semantic == "APPLICATION_LOCAL":
        result["candidate_source_upstream_or_app_local"] = "BYTE_IDENTITY_PROVEN: retained AppDir identity"
    return result


try:
    if OUT.exists():
        print(f"OUT already exists: {OUT}", file=sys.stderr)
        raise SystemExit(2)
    OUT.mkdir(parents=True, exist_ok=False)
    (OUT / "input").mkdir()

    dirty = subprocess.check_output([
        "git", "-C", str(REPO), "status", "--porcelain", "--untracked-files=no"
    ], text=True).strip()
    if dirty:
        fail("repository_state", "tracked working-tree changes detected", 2)
    branch = subprocess.check_output(["git", "-C", str(REPO), "branch", "--show-current"], text=True).strip()
    head = subprocess.check_output(["git", "-C", str(REPO), "rev-parse", "HEAD"], text=True).strip()

    required = [
        "analysis.status", "next-state.txt", "summary.tsv", "claim-boundary.txt",
        "selected-reference-object-seed.tsv", "supplemental-capability-evidence.tsv",
        "glibc-prefix-package-surface.tsv", "glibc-prefix-package-summary.tsv",
        "provider-authority-census.tsv", "unresolved-evidence-ledger.tsv",
        "input/schema_capability_groups__capability-groups.tsv",
        "input/schema_census_columns__census-columns.tsv",
        str(SCHEMA_DIR / "capability-groups.tsv"),
    ]
    checks=[]
    missing=[]
    for name in required:
        candidate = Path(name)
        src = candidate if candidate.is_absolute() else N2_OUT / candidate
        label = "current_schema_capability_groups.tsv" if candidate.is_absolute() else name
        embedded=OUT/"input"/label.replace("/","__")
        state="PASS" if src.is_file() and not src.is_symlink() else "FAIL"
        checks.append({"file":label,"state":state,"path":str(src),"sha256":sha256(src) if state=="PASS" else "-","embedded_path":str(embedded) if state=="PASS" else "-"})
        if state=="PASS":
            shutil.copy2(src, embedded)
        else:
            missing.append(label)
    write_tsv(OUT/"input-verification.tsv",["file","state","path","sha256","embedded_path"],checks)
    if missing:
        fail("input_verification","missing N2 inputs: "+", ".join(missing))
    if (N2_OUT/"analysis.status").read_text().strip()!="PASS":
        fail("input_status","N2 is not PASS")
    if (N2_OUT/"next-state.txt").read_text().strip()!="READY_FOR_N3_PROVISIONAL_AUTHORITY_CLASSIFICATION":
        fail("input_status","N2 next-state is unexpected")

    n2_summary={r["field"]:r["value"] for r in read_tsv(N2_OUT/"summary.tsv")}
    seed=read_tsv(N2_OUT/"selected-reference-object-seed.tsv")
    supplemental=read_tsv(N2_OUT/"supplemental-capability-evidence.tsv")
    surface=read_tsv(N2_OUT/"glibc-prefix-package-surface.tsv")
    package_summary=read_tsv(N2_OUT/"glibc-prefix-package-summary.tsv")
    n2_census=read_tsv(N2_OUT/"provider-authority-census.tsv")
    group_registry=read_tsv(SCHEMA_DIR/"capability-groups.tsv")
    census_fields=list(n2_census[0].keys())
    glibc_root=Path(n2_summary["glibc_root"])

    if len(seed)!=161 or len(supplemental)!=20 or len(package_summary)!=86:
        fail("input_shape","unexpected N2 evidence shape")

    n2_by_id={r["row_id"]:r for r in n2_census}
    selected_paths={r["path"] for r in seed}
    supplemental_paths={r["path"] for r in supplemental}

    package_pressure_rows=[]
    selected_by_package=Counter()
    for r in package_summary:
        selected_by_package[r["package_key"]]=int(r["selected_reference_paths"])
        pressure=package_pressure(r["package_key"],int(r["selected_reference_paths"]))
        package_pressure_rows.append({
            **r,
            "capability_group_pressure":pressure["capability_group"],
            "semantic_class_pressure":pressure["semantic_class"],
            "minimum_scope_pressure":pressure["minimum_valid_scope"],
            "profile_pressure":pressure["profile"],
            "update_owner_pressure":pressure["update_owner"],
            "termux_android_adaptation_pressure":pressure["adaptation"],
            "classification_rationale":pressure["rationale"],
            "authority_decision_state":"PROVISIONAL" if pressure["semantic_class"]!="UNRESOLVED" else "OPEN",
        })
    write_tsv(OUT/"package-authority-pressure.tsv",list(package_pressure_rows[0].keys()),package_pressure_rows)

    def blank() -> dict[str,object]:
        return {field:"" for field in census_fields}

    normalized=[]
    # Capability rows with provisional pressure only.
    for group in group_registry:
        base=n2_by_id.get(f"capability:{group['group_id']}",blank()).copy()
        if not base.get("row_id"):
            base.update({
                "row_id": f"capability:{group['group_id']}",
                "row_type": "CAPABILITY",
                "capability_group": group["group_id"],
                "object_or_capability": group["capability_group"],
                "current_selected_or_reference_path": "NOT_APPLICABLE",
                "current_package_or_source_provenance": group["seed_evidence"],
                "historical_semantic_class": "N3_CAPABILITY_EXTENSION",
                "historical_action": "SCHEMA_EXTENSION",
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
                "revalidation_trigger": "source/consumer/adaptation identity change",
                "unresolved_discriminating_evidence": group["unresolved_discriminating_evidence"],
                "evidence_refs": group["seed_evidence"],
                "evidence_claim_scope": "N3 capability extension; no provider decision",
                "evidence_conflict": "NONE",
            })
        semantic=group["initial_semantic_pressure"]
        if semantic not in {
            "WORLD_CORE_SUBSTRATE","PLATFORM_INTEGRATION_PROVIDER","GENERIC_SHARED_CAPABILITY_PROVIDER",
            "APPLICATION_LOCAL","APPLICATION_DOMAIN_SUPPLEMENT","DATA_CAPABILITY_PROVIDER","TOOLCHAIN_ONLY",
            "ORACLE_ONLY","MUTABLE_OR_CACHE"
        }:
            semantic="UNRESOLVED"
        base.update({
            "semantic_class":semantic,
            "minimum_valid_scope":group["minimum_scope_pressure"] if semantic!="UNRESOLVED" else "UNRESOLVED",
            "profile_runtime_or_research":profile_for_semantic(semantic),
            "update_owner":update_owner_for_semantic(semantic),
            "provisional_final_authority":"UNRESOLVED_CANDIDATE_COMPARISON_REQUIRED",
            "evidence_state":"PROVISIONAL",
            "authority_decision_state":"BLOCKED" if group["current_state"]=="BLOCKED" else ("PROVISIONAL" if semantic!="UNRESOLVED" else "OPEN"),
            "notes":f"N3 capability pressure; initial_state={group['current_state']}",
        })
        normalized.append(base)

    # Selected/reference rows.
    for s in seed:
        base=n2_by_id[s["evidence_row_id"]].copy()
        capability_groups,semantic=selected_pressure(s)
        candidates=candidate_fields(s["path"],s["package"],s["version"],semantic)
        authority="UNRESOLVED_CANDIDATE_COMPARISON_REQUIRED"
        if semantic=="APPLICATION_LOCAL":
            authority="UPSTREAM_APP_LOCAL_CURRENT_IDENTITY_PROVISIONAL"
        elif semantic=="WORLD_CORE_SUBSTRATE":
            authority="ACTIVE_TERMUX_GLIBC_WORLD_PROVISIONAL"
        base.update({
            "capability_group":capability_groups,
            "semantic_class":semantic,
            "minimum_valid_scope":scope_for_semantic(semantic),
            "profile_runtime_or_research":profile_for_semantic(semantic),
            "update_owner":update_owner_for_semantic(semantic),
            "termux_android_adaptation_required":"POSSIBLE" if semantic=="PLATFORM_INTEGRATION_PROVIDER" else "UNKNOWN",
            "provisional_final_authority":authority,
            "unresolved_discriminating_evidence":"source artifact, adaptation, ABI/version, profile, and update comparison required",
            "evidence_state":"PROVISIONAL",
            "authority_decision_state":"BLOCKED" if s["historical_action"]=="EXCLUDE_CPU_BASE_GRAPHICS_FEATURE" else "PROVISIONAL",
            "notes":base.get("notes","")+";N3 normalized selected/reference pressure",
            **candidates,
        })
        if semantic=="MUTABLE_OR_CACHE":
            base["provisional_final_authority"]="RUNTIME_OWNED_REGENERATED_OR_MUTABLE_STATE_PROVISIONAL"
        normalized.append(base)

    # Supplemental diagnostic rows.
    for s in supplemental:
        base=n2_by_id[s["evidence_row_id"]].copy()
        semantic="DATA_CAPABILITY_PROVIDER" if s["capability_group_seed"].startswith("data.") else "GENERIC_SHARED_CAPABILITY_PROVIDER"
        candidates=candidate_fields(s["path"],s["package"],s["version"],semantic)
        base.update({
            "semantic_class":semantic,
            "minimum_valid_scope":scope_for_semantic(semantic),
            "profile_runtime_or_research":"UNRESOLVED",
            "update_owner":"PROVIDER",
            "provisional_final_authority":"UNRESOLVED_BOUNDED_PIXBUF_DIAGNOSTIC_AND_SOURCE_COMPARISON_REQUIRED",
            "unresolved_discriminating_evidence":"minimum required module/data set and final source authority",
            "evidence_state":"PROVISIONAL",
            "authority_decision_state":"OPEN",
            "notes":base.get("notes","")+";N3 normalized diagnostic-only pressure",
            **candidates,
        })
        normalized.append(base)

    # Prefix ELF objects, excluding selected/reference paths already represented.
    prefix_elf_rows=[]
    for r in surface:
        if r["elf_state"]!="ELF" or r["file_type"]!="REGULAR" or r["path"] in selected_paths:
            continue
        keys=package_keys(r["package_keys"])
        key=keys[0] if len(keys)==1 else r["package_keys"]
        selected_pressure=sum(selected_by_package[k] for k in keys)
        pressure=prefix_elf_pressure(r,key,selected_pressure,glibc_root)
        semantic=pressure["semantic_class"]
        candidates=candidate_fields(r["path"],r["packages"],r["versions"],semantic)
        row=blank()
        row.update({
            "row_id":stable_id("n3-prefix-elf",r["path"]),
            "row_type":"ELF_OBJECT",
            "capability_group":pressure["capability_group"],
            "object_or_capability":Path(r["path"]).name,
            "current_selected_or_reference_path":r["path"],
            "current_package_or_source_provenance":f"packages={r['packages']};versions={r['versions']};ownership={r['ownership_state']}",
            "historical_semantic_class":"N2_PREFIX_ELF_INVENTORY",
            "historical_action":"READ_ONLY_INVENTORY",
            "semantic_class":semantic,
            "minimum_valid_scope":pressure["minimum_valid_scope"],
            "application_domains":"selected graph" if r["direct_consumer_count"]!="0" else "UNRESOLVED",
            "app_local_origin_relation":"NO_ORIGIN_RELATION",
            "content_sha256":r["sha256"],
            "elf_build_id":r["build_id"],
            "lookup_name":r["soname"] if r["soname"]!="-" else Path(r["path"]).name,
            "soname":r["soname"],
            "termux_android_adaptation_required":pressure["adaptation"],
            "abi_version_coupling":f"needed={r['needed']};direct_consumers={r['direct_consumer_count']}",
            "profile_runtime_or_research":pressure["profile"],
            "update_owner":pressure["update_owner"],
            "revalidation_trigger":"package/content/ABI/dependent-domain identity change",
            "provisional_final_authority":"UNRESOLVED_CANDIDATE_COMPARISON_REQUIRED",
            "unresolved_discriminating_evidence":pressure["rationale"],
            "evidence_state":"PROVISIONAL" if semantic!="UNRESOLVED" else "OBSERVED",
            "evidence_refs":"N2:glibc-prefix-package-surface.tsv",
            "evidence_claim_scope":"current prefix ELF inventory; no final provider decision",
            "evidence_conflict":"NONE",
            "authority_decision_state":"PROVISIONAL" if semantic!="UNRESOLVED" else "OPEN",
            "notes":f"package_pressure={pressure['rationale']};direct_consumers={r['direct_consumers']}",
            **candidates,
        })
        prefix_elf_rows.append(row)
        normalized.append(row)

    # Package aggregate rows.
    package_rows=[]
    for p in package_pressure_rows:
        semantic=p["semantic_class_pressure"]
        if p["package_key"] == "glibc":
            semantic="UNRESOLVED"
        row=blank()
        row.update({
            "row_id":f"n3-package:{p['package_key']}",
            "row_type":"PACKAGE_SURFACE",
            "capability_group":p["capability_group_pressure"],
            "object_or_capability":p["package_key"],
            "current_selected_or_reference_path":"PACKAGE_AGGREGATE",
            "current_package_or_source_provenance":f"{p['package']}={p['version']};architecture={p['architecture']};status={p['status']}",
            "historical_semantic_class":"N2_PACKAGE_AGGREGATE",
            "historical_action":"READ_ONLY_AGGREGATION",
            "semantic_class":semantic,
            "minimum_valid_scope":scope_for_semantic(semantic),
            "application_domains":"obsidian selected graph" if p["selected_reference_paths"]!="0" else "UNRESOLVED",
            "app_local_origin_relation":"NO_ORIGIN_RELATION",
            "content_sha256":"NOT_APPLICABLE",
            "elf_build_id":"NOT_APPLICABLE",
            "lookup_name":"NOT_APPLICABLE",
            "soname":"NOT_APPLICABLE",
            "candidate_source_termux_glibc_package":f"ARTIFACT_IDENTIFIED: installed {p['package_key']}={p['version']}",
            "candidate_source_exact_debian_artifact":"UNASSESSED",
            "candidate_source_upstream_or_app_local":"UNASSESSED",
            "candidate_source_project_build":"UNASSESSED",
            "candidate_source_native_termux_or_android":"UNASSESSED",
            "termux_android_adaptation_required":p["termux_android_adaptation_pressure"],
            "abi_version_coupling":f"elf_files={p['elf_files']};selected_paths={p['selected_reference_paths']};consumer_edges={p['direct_consumer_edges']}",
            "profile_runtime_or_research":p["profile_pressure"],
            "update_owner":p["update_owner_pressure"],
            "revalidation_trigger":"package artifact/version/control-state change",
            "provisional_final_authority":"UNRESOLVED_PACKAGE_IS_NOT_AUTHORITY",
            "unresolved_discriminating_evidence":p["classification_rationale"],
            "evidence_state":"PROVISIONAL" if semantic!="UNRESOLVED" else "OBSERVED",
            "evidence_refs":"N2:glibc-prefix-package-summary.tsv;N2:package-control-surface.tsv",
            "evidence_claim_scope":"package aggregate pressure only; mixed packages require object split",
            "evidence_conflict":"NONE",
            "authority_decision_state":"PROVISIONAL" if semantic!="UNRESOLVED" else "OPEN",
            "notes":f"surface_paths={p['surface_paths']};regular={p['regular_files']};symlinks={p['symlinks']};control={p['present_control_files']}",
        })
        package_rows.append(row)
        normalized.append(row)

    # Explicit unowned loader state.
    unowned_rows=[]
    for r in surface:
        if r["ownership_state"]!="UNOWNED" or r["file_type"]=="DIRECTORY":
            continue
        name=Path(r["path"]).name
        semantic="MUTABLE_OR_CACHE" if name=="ld.so.cache" else "WORLD_CORE_SUBSTRATE"
        row=blank()
        row.update({
            "row_id":stable_id("n3-unowned-loader",r["path"]),
            "row_type":"CACHE_CLASS" if name=="ld.so.cache" else "PACKAGE_SURFACE",
            "capability_group":"runtime.mutable-cache" if name=="ld.so.cache" else "world.glibc.core",
            "object_or_capability":name,
            "current_selected_or_reference_path":r["path"],
            "current_package_or_source_provenance":"UNOWNED_CURRENT_PREFIX_STATE",
            "historical_semantic_class":"N2_UNOWNED_PREFIX_STATE",
            "historical_action":"READ_ONLY_INVENTORY",
            "semantic_class":semantic,
            "minimum_valid_scope":scope_for_semantic(semantic),
            "application_domains":"glibc loader state",
            "app_local_origin_relation":"NO_ORIGIN_RELATION",
            "content_sha256":r["sha256"],
            "elf_build_id":"NOT_APPLICABLE",
            "lookup_name":"NOT_APPLICABLE",
            "soname":"NOT_APPLICABLE",
            "candidate_source_termux_glibc_package":"NO_KNOWN_CANDIDATE: current path is unowned",
            "candidate_source_exact_debian_artifact":"UNASSESSED",
            "candidate_source_upstream_or_app_local":"UNASSESSED",
            "candidate_source_project_build":"REQUIRES_DISCRIMINATOR: define generation/config owner",
            "candidate_source_native_termux_or_android":"UNASSESSED",
            "termux_android_adaptation_required":"POSSIBLE",
            "abi_version_coupling":"loader configuration/cache coupled to active world and provider paths",
            "profile_runtime_or_research":"RUNTIME" if name=="ld.so.conf" else "NEITHER",
            "update_owner":"WORLD_SUBSTRATE" if name=="ld.so.conf" else "MUTABLE_STATE",
            "revalidation_trigger":"world/provider path or loader version change",
            "provisional_final_authority":"PROJECT_OR_WORLD_LIFECYCLE_OWNER_UNRESOLVED",
            "unresolved_discriminating_evidence":"producer, regeneration rule, package/project ownership, rollback behavior",
            "evidence_state":"PROVISIONAL",
            "evidence_refs":"N2:glibc-prefix-package-surface.tsv",
            "evidence_claim_scope":"current unowned loader-state identity",
            "evidence_conflict":"NONE",
            "authority_decision_state":"PROVISIONAL",
            "notes":f"mode={r['mode']};size={r['size_bytes']}",
        })
        unowned_rows.append(row)
        normalized.append(row)

    # Aggregate remaining non-ELF package surface.
    aggregates=defaultdict(lambda:{"paths":[],"bytes":0,"regular":0,"symlink":0,"selected":0,"consumers":0})
    for r in surface:
        if r["file_type"]=="DIRECTORY" or r["elf_state"]=="ELF" or r["path"] in selected_paths or r["path"] in supplemental_paths or r["ownership_state"]=="UNOWNED":
            continue
        cls=surface_class(r,glibc_root)
        keys=r["package_keys"] if r["package_keys"]!="-" else "UNOWNED"
        key=(keys,cls)
        a=aggregates[key]
        a["paths"].append(r["path"])
        if r["file_type"]=="REGULAR" and r["size_bytes"].isdigit():
            a["bytes"]+=int(r["size_bytes"])
            a["regular"]+=1
        if r["file_type"]=="SYMLINK":
            a["symlink"]+=1
        a["selected"]+=int(r["selected_reference_relations"]!="-")
        a["consumers"]+=int(r["direct_consumer_count"])

    aggregate_rows=[]
    for (keys,cls),a in sorted(aggregates.items()):
        key_list=package_keys(keys)
        primary=key_list[0] if len(key_list)==1 else keys
        pressure=package_pressure(primary,sum(selected_by_package[k] for k in key_list))
        semantic, aggregate_group, profile, update_owner = aggregate_semantic_pressure(primary, cls, pressure)
        row=blank()
        row.update({
            "row_id":stable_id("n3-surface-aggregate",f"{keys}|{cls}"),
            "row_type":"PACKAGE_SURFACE",
            "capability_group":aggregate_group,
            "object_or_capability":f"{keys}:{cls}",
            "current_selected_or_reference_path":"AGGREGATED_PATH_SET",
            "current_package_or_source_provenance":keys,
            "historical_semantic_class":"N2_NON_ELF_SURFACE_AGGREGATE",
            "historical_action":"READ_ONLY_AGGREGATION",
            "semantic_class":semantic,
            "minimum_valid_scope":scope_for_semantic(semantic),
            "application_domains":"UNRESOLVED",
            "app_local_origin_relation":"NO_ORIGIN_RELATION",
            "content_sha256":"MULTIPLE_IDENTITIES_IN_RAW_N2_SURFACE",
            "elf_build_id":"NOT_APPLICABLE",
            "lookup_name":"NOT_APPLICABLE",
            "soname":"NOT_APPLICABLE",
            "candidate_source_termux_glibc_package":f"ARTIFACT_IDENTIFIED: installed package surface {keys}",
            "candidate_source_exact_debian_artifact":"UNASSESSED",
            "candidate_source_upstream_or_app_local":"UNASSESSED",
            "candidate_source_project_build":"UNASSESSED",
            "candidate_source_native_termux_or_android":"UNASSESSED",
            "termux_android_adaptation_required":pressure["adaptation"],
            "abi_version_coupling":f"path_count={len(a['paths'])};selected_relations={a['selected']};consumer_edges={a['consumers']}",
            "profile_runtime_or_research":profile,
            "update_owner":update_owner,
            "revalidation_trigger":"package artifact or semantic surface class change",
            "provisional_final_authority":"UNRESOLVED_AGGREGATED_PACKAGE_SURFACE",
            "unresolved_discriminating_evidence":pressure["rationale"],
            "evidence_state":"PROVISIONAL" if semantic!="UNRESOLVED" else "OBSERVED",
            "evidence_refs":"N2:glibc-prefix-package-surface.tsv",
            "evidence_claim_scope":"aggregated non-ELF package surface; raw paths retained in N2",
            "evidence_conflict":"NONE",
            "authority_decision_state":"PROVISIONAL" if semantic!="UNRESOLVED" else "OPEN",
            "notes":f"surface_class={cls};path_count={len(a['paths'])};regular={a['regular']};symlinks={a['symlink']};bytes={a['bytes']};samples={';'.join(a['paths'][:5])}",
        })
        aggregate_rows.append(row)
        normalized.append(row)

    selected_x11_rows = [
        normalized_row
        for selected_row in seed
        if selected_row["package"].split(":", 1)[0] in PLATFORM_X11_PACKAGES
        for normalized_row in [next(row for row in normalized if row["row_id"] == selected_row["evidence_row_id"])]
    ]
    if any("platform.x11-xcb.termux" not in row["capability_group"].split(";") for row in selected_x11_rows):
        fail("selected_platform_pressure", "selected X11/XCB rows lost platform capability pressure")
    if any(
        row["semantic_class"] != "PLATFORM_INTEGRATION_PROVIDER"
        for row in selected_x11_rows
        if row["authority_decision_state"] != "BLOCKED"
    ):
        fail("selected_platform_pressure", "active selected X11/XCB rows are not platform-integration pressure")

    termux_exec_rows = [
        row for row in normalized
        if row["row_id"].startswith("n3-package:termux-exec-glibc")
        or (
            row["row_id"].startswith("n3-prefix-elf:")
            and "termux-exec-glibc" in row["current_package_or_source_provenance"]
        )
    ]
    if any("platform.glibc-adaptation.termux" not in row["capability_group"].split(";") for row in termux_exec_rows):
        fail("termux_exec_pressure", "termux-exec rows are not assigned to glibc adaptation pressure")

    ids=[r["row_id"] for r in normalized]
    if len(ids)!=len(set(ids)):
        fail("normalized_identity","duplicate normalized row IDs")
    required_fields = [
        row["field"]
        for row in read_tsv(N2_OUT/"input/schema_census_columns__census-columns.tsv")
        if row["required"] == "YES"
    ]
    blank_required = [
        f"{row['row_id']}:{field}"
        for row in normalized
        for field in required_fields
        if not str(row.get(field, ""))
    ]
    if blank_required:
        fail("normalized_shape", f"blank required census fields: {len(blank_required)}")

    write_tsv(OUT/"normalized-provider-authority-census.tsv",census_fields,normalized)
    write_tsv(OUT/"non-elf-surface-aggregates.tsv",census_fields,aggregate_rows)

    semantic_counts=Counter(r["semantic_class"] for r in normalized)
    state_counts=Counter(r["authority_decision_state"] for r in normalized)
    row_type_counts=Counter(r["row_type"] for r in normalized)
    summary_rows=[
        {"field":"branch","value":branch},{"field":"head","value":head},{"field":"n2_root","value":str(N2_OUT)},
        {"field":"n2_head","value":n2_summary.get("head","")},{"field":"raw_n2_census_rows","value":len(n2_census)},
        {"field":"raw_prefix_surface_rows","value":len(surface)},{"field":"normalized_census_rows","value":len(normalized)},
        {"field":"capability_rows","value":len(group_registry)},{"field":"selected_reference_rows","value":len(seed)},
        {"field":"supplemental_rows","value":len(supplemental)},{"field":"prefix_elf_rows_added","value":len(prefix_elf_rows)},
        {"field":"package_aggregate_rows","value":len(package_rows)},{"field":"unowned_loader_state_rows","value":len(unowned_rows)},
        {"field":"non_elf_surface_aggregate_rows","value":len(aggregate_rows)},
        {"field":"duplicate_normalized_row_ids","value":0},{"field":"authority_decisions_accepted","value":0},
        {"field":"package_operation_performed","value":"NO"},{"field":"runtime_launch_performed","value":"NO"},
        {"field":"generation_operation_performed","value":"NO"},{"field":"current_operation_performed","value":"NO"},{"field":"live_current_checked","value":"NO"},
    ]
    for key,value in sorted(row_type_counts.items()): summary_rows.append({"field":f"row_type_{key}","value":value})
    for key,value in sorted(semantic_counts.items()): summary_rows.append({"field":f"semantic_{key}","value":value})
    for key,value in sorted(state_counts.items()): summary_rows.append({"field":f"decision_state_{key}","value":value})
    write_tsv(OUT/"summary.tsv",["field","value"],summary_rows)

    unresolved=[]
    for group in group_registry:
        rows=[r for r in normalized if group["group_id"] in r["capability_group"].split(";") and r["row_type"]!="CAPABILITY"]
        unresolved.append({
            "group_id":group["group_id"],"capability_group":group["capability_group"],"normalized_member_rows":len(rows),
            "provisional_rows":sum(r["authority_decision_state"]=="PROVISIONAL" for r in rows),
            "open_rows":sum(r["authority_decision_state"]=="OPEN" for r in rows),
            "blocked_rows":sum(r["authority_decision_state"]=="BLOCKED" for r in rows),
            "unresolved_discriminating_evidence":group["unresolved_discriminating_evidence"],
            "next_permitted_action":"SOURCE_RECIPE_AND_ARTIFACT_COMPARISON" if group["group_id"] not in {"shared.pixbuf-codecs","data.icons","data.mime"} else "BOUNDED_PIXBUF_DISCRIMINATOR_OR_SOURCE_COMPARISON",
        })
    write_tsv(OUT/"unresolved-evidence-ledger.tsv",list(unresolved[0].keys()),unresolved)

    (OUT/"claim-boundary.txt").write_text(
        "This stage normalizes the accepted N2 raw provider evidence into a smaller N3 provisional decision surface.\n"
        "It retains all raw N2 paths by reference, creates object-level rows for selected/reference, diagnostic, and prefix ELF evidence, "
        "creates package aggregates, and groups remaining non-ELF package files by package and semantic path class.\n"
        "Provisional semantic pressure is not final provider authority. No source superiority, locked artifact, runtime package list, "
        "successor composition, package operation, workload launch, generation mutation, current change, or graphics reopening is performed.\n"
    )
    (OUT/"next-state.txt").write_text("READY_FOR_N3_SOURCE_RECIPE_AND_ARTIFACT_COMPARISON\n")
    write_status("PASS")
    if (OUT/"failure-stage.txt").exists(): (OUT/"failure-stage.txt").unlink()
    print("selected Obsidian provider-authority N3 normalization: PASS")
    print(f"evidence: {OUT}")
    print("\n===== summary =====")
    for row in summary_rows: print(f"{row['field']}\t{row['value']}")
except SystemExit:
    raise
except Exception:
    write_status("FAIL")
    (OUT/"failure-stage.txt").write_text(stage+"\n")
    traceback.print_exc()
    print(f"evidence: {OUT}",file=sys.stderr)
    raise SystemExit(1)
