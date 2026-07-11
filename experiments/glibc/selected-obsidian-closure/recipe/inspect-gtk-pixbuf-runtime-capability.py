#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import os
import re
import subprocess
import sys
import traceback
from pathlib import Path

B9_OUT = Path(os.environ["B9_OUT"])
B10_OUT = Path(os.environ["B10_OUT"])
OUT = Path(os.environ["OUT"])
PREFIX = Path(os.environ["PREFIX"])
ROOTFS = Path(
    os.environ.get(
        "ROOTFS",
        str(PREFIX / "var/lib/proot-distro/containers/debian/rootfs"),
    )
)
REPO = Path(
    subprocess.check_output(
        ["git", "-C", str(Path(__file__).resolve().parent), "rev-parse", "--show-toplevel"],
        text=True,
    ).strip()
)

stage = "initialization"


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, fields: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fields,
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def summary_map(path: Path) -> dict[str, str]:
    return {row["field"]: row["value"] for row in read_tsv(path)}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_status(value: str) -> None:
    (OUT / "analysis.status").write_text(value + "\n")


def fail(stage_name: str, message: str, rc: int = 1) -> None:
    write_status("FAIL")
    (OUT / "failure-stage.txt").write_text(stage_name + "\n")
    print(message, file=sys.stderr)
    print(f"evidence: {OUT}", file=sys.stderr)
    raise SystemExit(rc)


def parse_dpkg_status(path: Path) -> dict[tuple[str, str], str]:
    result: dict[tuple[str, str], str] = {}
    if not path.is_file():
        return result
    paragraph: dict[str, str] = {}
    for line in path.read_text(errors="replace").splitlines() + [""]:
        if not line:
            package = paragraph.get("Package")
            architecture = paragraph.get("Architecture", "")
            version = paragraph.get("Version", "")
            if package:
                result[(package, architecture)] = version
            paragraph = {}
            continue
        if line[0].isspace() or ":" not in line:
            continue
        key, value = line.split(":", 1)
        paragraph[key] = value.strip()
    return result


def package_inventory(rootfs: Path) -> tuple[dict[str, list[str]], dict[tuple[str, str], str]]:
    ownership: dict[str, list[str]] = {}
    info_dir = rootfs / "var/lib/dpkg/info"
    if info_dir.is_dir():
        for list_file in sorted(info_dir.glob("*.list")):
            package_key = list_file.name[:-5]
            for line in list_file.read_text(errors="replace").splitlines():
                if line.startswith("/"):
                    ownership.setdefault(line, []).append(package_key)
    versions = parse_dpkg_status(rootfs / "var/lib/dpkg/status")
    return ownership, versions


def package_version(package_key: str, versions: dict[tuple[str, str], str]) -> str:
    if ":" in package_key:
        package, architecture = package_key.rsplit(":", 1)
        return versions.get((package, architecture), versions.get((package, "all"), "UNKNOWN"))
    matches = [value for (package, _arch), value in versions.items() if package == package_key]
    return matches[0] if matches else "UNKNOWN"


def rootfs_rel(path: Path) -> str:
    return "/" + str(path.relative_to(ROOTFS))


def owners_for(path: Path, ownership: dict[str, list[str]], versions: dict[tuple[str, str], str]) -> tuple[str, str]:
    keys = ownership.get(rootfs_rel(path), [])
    if not keys:
        return "UNOWNED", "UNKNOWN"
    packages = ",".join(sorted(keys))
    package_versions = ",".join(
        f"{key}={package_version(key, versions)}" for key in sorted(keys)
    )
    return packages, package_versions


def discover(patterns: list[str]) -> list[Path]:
    found: set[Path] = set()
    for pattern in patterns:
        found.update(path for path in ROOTFS.glob(pattern) if path.is_file())
    return sorted(found)


try:
    OUT.mkdir(parents=True, exist_ok=True)

    stage = "repository_state"
    dirty = subprocess.check_output(
        [
            "git",
            "-C",
            str(REPO),
            "status",
            "--porcelain",
            "--untracked-files=no",
        ],
        text=True,
    ).strip()
    if dirty:
        fail(stage, "tracked working-tree changes detected", 2)

    branch = subprocess.check_output(
        ["git", "-C", str(REPO), "branch", "--show-current"],
        text=True,
    ).strip()
    head = subprocess.check_output(
        ["git", "-C", str(REPO), "rev-parse", "HEAD"],
        text=True,
    ).strip()

    stage = "input_status"
    required = [
        B9_OUT / "analysis.status",
        B9_OUT / "next-state.txt",
        B9_OUT / "summary.tsv",
        B9_OUT / "input/input__semantic-object-disposition.tsv",
        B10_OUT / "analysis.status",
        B10_OUT / "failure-stage.txt",
        B10_OUT / "runtime-root-contract.tsv",
        B10_OUT / "runtime-snapshot.tsv",
        B10_OUT / "current-state-before.tsv",
        B10_OUT / "current-state-after.tsv",
        B10_OUT / "capture/topology.status",
        B10_OUT / "capture/survival.status",
        B10_OUT / "capture/poll-observed.tsv",
        B10_OUT / "capture/launch.stderr",
        B10_OUT / "capture/launch.stdout",
    ]
    verification_rows: list[dict[str, object]] = []
    missing: list[str] = []
    for path in required:
        state_value = "PASS" if path.is_file() else "FAIL"
        verification_rows.append({"path": str(path), "state": state_value})
        if state_value == "FAIL":
            missing.append(str(path))
    write_tsv(OUT / "input-verification.tsv", ["path", "state"], verification_rows)
    if missing:
        fail(stage, "missing required input files: " + ", ".join(missing))

    if (B9_OUT / "analysis.status").read_text().strip() != "PASS":
        fail(stage, "Phase B9 status is not PASS")
    if (
        B9_OUT / "next-state.txt"
    ).read_text().strip() != "READY_FOR_EXPLICIT_GENERATION_VALIDATION":
        fail(stage, "Phase B9 next-state is unexpected")
    if (B10_OUT / "analysis.status").read_text().strip() != "FAIL":
        fail(stage, "short-runtime B10 receipt is not FAIL")
    if (B10_OUT / "failure-stage.txt").read_text().strip() != "capture":
        fail(stage, "short-runtime B10 failure stage is not capture")
    if (B10_OUT / "capture/topology.status").read_text().strip() != "PASS":
        fail(stage, "short-runtime topology did not pass")
    survival = (B10_OUT / "capture/survival.status").read_text().strip()
    if survival != "FAIL main process exited":
        fail(stage, f"unexpected survival result: {survival}")

    before = read_tsv(B10_OUT / "current-state-before.tsv")
    after = read_tsv(B10_OUT / "current-state-after.tsv")
    if len(before) != 1 or len(after) != 1 or before[0] != after[0]:
        fail(stage, "current-state evidence changed or has unexpected shape")
    if before[0]["state"] != "ABSENT":
        fail(stage, "current was not absent")

    runtime_contract = summary_map(B10_OUT / "runtime-root-contract.tsv")
    if int(runtime_contract["tmpdir_length"]) > 64:
        fail(stage, "short-runtime TMPDIR contract did not pass")
    if summary_map(B10_OUT / "runtime-snapshot.tsv").get("snapshot_state") != "MATCH":
        fail(stage, "runtime snapshot did not match")

    stderr_text = (B10_OUT / "capture/launch.stderr").read_text(errors="replace")
    stdout_text = (B10_OUT / "capture/launch.stdout").read_text(errors="replace")
    evidence_checks = [
        ("hicolor_missing", "Could not find the icon 'user-home-symbolic-ltr'" in stderr_text),
        ("image_missing_pixbuf_failure", "Failed to load /org/gtk/libgtk/icons/48x48/status/image-missing.png" in stderr_text),
        ("unrecognized_image_format", "Unrecognized image file format" in stderr_text),
        ("gtk_fatal_assertion", "Gtk:ERROR:" in stderr_text and "assertion failed" in stderr_text),
        ("application_bailout", "Bail out! Gtk:ERROR:" in stdout_text),
        ("bad_elf_absent", "bad ELF magic" not in stderr_text),
        ("missing_library_absent", "error while loading shared libraries" not in stderr_text),
    ]
    write_tsv(
        OUT / "failure-evidence.tsv",
        ["check", "state"],
        [
            {"check": check, "state": "PASS" if passed else "FAIL"}
            for check, passed in evidence_checks
        ],
    )
    if not all(passed for _check, passed in evidence_checks):
        fail(stage, "short-runtime GTK failure evidence did not match the accepted diagnostic")

    process_rows = read_tsv(B10_OUT / "capture/poll-observed.tsv")
    process_classes = sorted({row["class"] for row in process_rows})
    if "main" not in process_classes or "renderer" not in process_classes or "zygote" not in process_classes:
        fail(stage, "expected short-runtime topology classes were not observed")
    if "gpu" in process_classes:
        fail(stage, "GPU process was observed")

    stage = "package_inventory"
    if not ROOTFS.is_dir():
        fail(stage, f"rootfs is not present: {ROOTFS}")
    ownership, versions = package_inventory(ROOTFS)

    caches = discover(
        [
            "usr/lib/*/gdk-pixbuf-2.0/*/loaders.cache",
            "usr/lib/gdk-pixbuf-2.0/*/loaders.cache",
        ]
    )
    modules = discover(
        [
            "usr/lib/*/gdk-pixbuf-2.0/*/loaders/*.so",
            "usr/lib/gdk-pixbuf-2.0/*/loaders/*.so",
        ]
    )
    icon_indexes = discover(["usr/share/icons/*/index.theme"])
    mime_files = discover(
        [
            "usr/share/mime/mime.cache",
            "usr/share/mime/globs",
            "usr/share/mime/globs2",
            "usr/share/mime/aliases",
            "usr/share/mime/subclasses",
        ]
    )

    cache_rows: list[dict[str, object]] = []
    reference_rows: list[dict[str, object]] = []
    quoted_path = re.compile(r'^"([^"]+\.so)"')
    for cache in caches:
        package, package_version_text = owners_for(cache, ownership, versions)
        references: list[str] = []
        for line in cache.read_text(errors="replace").splitlines():
            match = quoted_path.match(line.strip())
            if match:
                references.append(match.group(1))
        cache_rows.append(
            {
                "path": str(cache),
                "sha256": sha256(cache),
                "package": package,
                "package_version": package_version_text,
                "referenced_modules": len(references),
            }
        )
        for referenced in references:
            written = Path(referenced)
            rootfs_candidate = ROOTFS / referenced.lstrip("/")
            reference_rows.append(
                {
                    "cache_path": str(cache),
                    "referenced_path": referenced,
                    "written_path_exists": "YES" if written.is_file() else "NO",
                    "rootfs_prefixed_path": str(rootfs_candidate),
                    "rootfs_prefixed_exists": "YES" if rootfs_candidate.is_file() else "NO",
                    "rootfs_prefixed_sha256": sha256(rootfs_candidate) if rootfs_candidate.is_file() else "-",
                }
            )

    module_rows: list[dict[str, object]] = []
    for module in modules:
        package, package_version_text = owners_for(module, ownership, versions)
        module_rows.append(
            {
                "path": str(module),
                "basename": module.name,
                "sha256": sha256(module),
                "size_bytes": module.stat().st_size,
                "package": package,
                "package_version": package_version_text,
            }
        )

    data_rows: list[dict[str, object]] = []
    for kind, paths in (
        ("ICON_THEME_INDEX", icon_indexes),
        ("MIME_DATABASE", mime_files),
    ):
        for path in paths:
            package, package_version_text = owners_for(path, ownership, versions)
            data_rows.append(
                {
                    "kind": kind,
                    "path": str(path),
                    "sha256": sha256(path),
                    "size_bytes": path.stat().st_size,
                    "package": package,
                    "package_version": package_version_text,
                }
            )

    write_tsv(
        OUT / "pixbuf-loader-cache.tsv",
        ["path", "sha256", "package", "package_version", "referenced_modules"],
        cache_rows,
    )
    write_tsv(
        OUT / "pixbuf-cache-references.tsv",
        [
            "cache_path",
            "referenced_path",
            "written_path_exists",
            "rootfs_prefixed_path",
            "rootfs_prefixed_exists",
            "rootfs_prefixed_sha256",
        ],
        reference_rows,
    )
    write_tsv(
        OUT / "pixbuf-loader-modules.tsv",
        ["path", "basename", "sha256", "size_bytes", "package", "package_version"],
        module_rows,
    )
    write_tsv(
        OUT / "gtk-data-capability.tsv",
        ["kind", "path", "sha256", "size_bytes", "package", "package_version"],
        data_rows,
    )

    stage = "semantic_gap"
    semantic_rows = read_tsv(B9_OUT / "input/input__semantic-object-disposition.tsv")
    semantic_paths = {row["path"] for row in semantic_rows}
    discovered_paths = [*caches, *modules, *icon_indexes, *mime_files]
    gap_rows: list[dict[str, object]] = []
    for path in discovered_paths:
        if path in caches:
            kind = "PIXBUF_LOADER_CACHE"
        elif path in modules:
            kind = "PIXBUF_LOADER_MODULE"
        elif path in icon_indexes:
            kind = "ICON_THEME_INDEX"
        else:
            kind = "MIME_DATABASE"
        gap_rows.append(
            {
                "kind": kind,
                "path": str(path),
                "present_in_b9_semantic_manifest": "YES" if str(path) in semantic_paths else "NO",
            }
        )
    write_tsv(
        OUT / "semantic-coverage-gaps.tsv",
        ["kind", "path", "present_in_b9_semantic_manifest"],
        gap_rows,
    )

    if not caches:
        fail("pixbuf_capability", "no gdk-pixbuf loader cache discovered")
    if not modules:
        fail("pixbuf_capability", "no gdk-pixbuf loader modules discovered")
    if not any(row["rootfs_prefixed_exists"] == "YES" for row in reference_rows):
        fail("pixbuf_capability", "loader cache does not resolve to rootfs modules")

    missing_semantic = sum(
        row["present_in_b9_semantic_manifest"] == "NO" for row in gap_rows
    )
    written_missing = sum(row["written_path_exists"] == "NO" for row in reference_rows)
    rootfs_reference_matches = sum(
        row["rootfs_prefixed_exists"] == "YES" for row in reference_rows
    )

    b9_summary = summary_map(B9_OUT / "summary.tsv")
    summary_rows = [
        {"field": "branch", "value": branch},
        {"field": "head", "value": head},
        {"field": "phase_b9_root", "value": str(B9_OUT)},
        {"field": "phase_b9_head", "value": b9_summary.get("head", "")},
        {"field": "short_runtime_b10_root", "value": str(B10_OUT)},
        {"field": "rootfs", "value": str(ROOTFS)},
        {"field": "topology_status", "value": "PASS"},
        {"field": "survival_status", "value": survival},
        {"field": "gpu_process_observed", "value": "NO"},
        {"field": "current_pointer_changed", "value": "NO"},
        {"field": "pixbuf_loader_caches", "value": len(caches)},
        {"field": "pixbuf_loader_modules", "value": len(modules)},
        {"field": "cache_module_references", "value": len(reference_rows)},
        {"field": "cache_written_paths_missing", "value": written_missing},
        {"field": "cache_rootfs_reference_matches", "value": rootfs_reference_matches},
        {"field": "icon_theme_indexes", "value": len(icon_indexes)},
        {"field": "mime_database_files", "value": len(mime_files)},
        {"field": "discovered_paths_missing_from_b9_semantic_manifest", "value": missing_semantic},
        {"field": "generation_mutated", "value": "NO"},
        {"field": "runtime_launch_performed", "value": "NO"},
        {"field": "promoted_runtime_mutated", "value": "NO"},
    ]
    write_tsv(OUT / "summary.tsv", ["field", "value"], summary_rows)

    (OUT / "claim-boundary.txt").write_text(
        "This stage is a read-only source/provenance inventory for the GTK gdk-pixbuf, icon-theme, and MIME capability exposed by the short-runtime B10 fatal assertion.\n"
        "It verifies the accepted B9 generation and B10 failure receipt, inventories loader caches/modules and selected GTK data with package/version/hash identity, and reports which discovered paths were absent from the B9 semantic manifest.\n"
        "It does not prove which loader module is required at runtime, does not launch Obsidian, and does not mutate or replace the immutable generation.\n"
    )
    (OUT / "next-state.txt").write_text(
        "READY_FOR_CONTROLLED_PIXBUF_RUNTIME_DIAGNOSTIC\n"
    )
    write_status("PASS")
    if (OUT / "failure-stage.txt").exists():
        (OUT / "failure-stage.txt").unlink()

    print("selected Obsidian GTK pixbuf runtime capability inventory: PASS")
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
