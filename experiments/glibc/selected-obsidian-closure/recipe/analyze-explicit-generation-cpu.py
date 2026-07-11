#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import os
import subprocess
import sys
import traceback
from collections import Counter
from pathlib import Path

B9_OUT = Path(os.environ["B9_OUT"])
CAPTURE_OUT = Path(os.environ["CAPTURE_OUT"])
OUT = Path(os.environ["OUT"])
VALIDATION_ROOT = Path(os.environ["VALIDATION_ROOT"])
LAUNCH_RECEIPT_DIR = Path(os.environ["LAUNCH_RECEIPT_DIR"])
APP = Path(os.environ.get("APP", str(Path.home() / "gl/apps/obsidian")))
ROOTFS = Path(
    os.environ.get(
        "ROOTFS",
        str(Path(os.environ["PREFIX"]) / "var/lib/proot-distro/containers/debian/rootfs"),
    )
)
PREFIX = Path(os.environ["PREFIX"])
HOME = Path(os.environ["HOME"])
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


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def summary_map(path: Path) -> dict[str, str]:
    return {row["field"]: row["value"] for row in read_tsv(path)}


def write_status(value: str) -> None:
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
        B9_OUT / "input/content-object-plan.tsv",
        CAPTURE_OUT / "topology.status",
        CAPTURE_OUT / "survival.status",
        CAPTURE_OUT / "maps-capture.status",
        CAPTURE_OUT / "processes.tsv",
        CAPTURE_OUT / "unique-objects.tsv",
        LAUNCH_RECEIPT_DIR / "launch-environment.tsv",
        LAUNCH_RECEIPT_DIR / "argv.txt",
        OUT / "current-state-before.tsv",
        OUT / "current-state-after.tsv",
    ]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        fail(stage, "missing explicit-validation inputs: " + ", ".join(missing))

    if (B9_OUT / "analysis.status").read_text().strip() != "PASS":
        fail(stage, "Phase B9 status is not PASS")
    if (
        B9_OUT / "next-state.txt"
    ).read_text().strip() != "READY_FOR_EXPLICIT_GENERATION_VALIDATION":
        fail(stage, "Phase B9 is not ready for explicit validation")
    for status_name in ("topology.status", "survival.status", "maps-capture.status"):
        if (CAPTURE_OUT / status_name).read_text().strip() != "PASS":
            fail(stage, f"capture status is not PASS: {status_name}")

    b9_summary = summary_map(B9_OUT / "summary.tsv")
    generation_dir = Path(b9_summary["generation_dir"])
    generation_id = b9_summary["generation_id"]
    generation_base = generation_dir.parent.parent
    current_path = generation_base / "current"
    world_lib = PREFIX / "glibc/lib"

    if not generation_dir.is_dir() or generation_dir.is_symlink():
        fail("generation_state", f"generation is not a plain directory: {generation_dir}")
    if generation_dir.stat().st_mode & 0o200:
        fail("generation_state", f"generation root is owner-writable: {generation_dir}")

    before_rows = read_tsv(OUT / "current-state-before.tsv")
    after_rows = read_tsv(OUT / "current-state-after.tsv")
    if len(before_rows) != 1 or len(after_rows) != 1:
        fail("current_guard", "unexpected current-state receipt shape")
    if before_rows[0] != after_rows[0]:
        fail("current_guard", "current changed during explicit validation")
    if before_rows[0]["state"] != "ABSENT":
        fail("current_guard", "initial explicit validation requires current to remain absent")
    if current_path.exists() or current_path.is_symlink():
        fail("current_guard", "current exists after explicit validation")

    stage = "launch_contract"
    launch = summary_map(LAUNCH_RECEIPT_DIR / "launch-environment.tsv")
    expected_launch = {
        "generation_dir": str(generation_dir),
        "generation_lib": str(generation_dir / "lib"),
        "generation_schema_dir": str(generation_dir / "share/glib-2.0/schemas"),
        "generation_font_dir": str(generation_dir / "share/fonts/selected"),
        "world_lib": str(world_lib),
        "ld_library_path": f"{generation_dir / 'lib'}:{world_lib}",
        "xdg_data_dirs": f"{APP / 'usr/share'}:{generation_dir / 'share'}",
        "gl_gpu": "0",
        "gpu_flags": "--disable-gpu",
        "ld_preload_exec_value": "EMPTY",
        "current_reference": "NO",
    }
    for key, expected in expected_launch.items():
        if launch.get(key) != expected:
            fail(stage, f"unexpected launch contract {key}: {launch.get(key)!r}")

    runtime_keys = (
        "fontconfig_file",
        "fontconfig_path",
        "xdg_config_home",
        "xdg_cache_home",
        "xdg_data_home",
        "xdg_state_home",
        "xdg_runtime_dir",
        "tmpdir",
    )
    for key in runtime_keys:
        value = launch.get(key)
        if not value:
            fail(stage, f"missing launch runtime path: {key}")
        if not within(Path(value), VALIDATION_ROOT):
            fail(stage, f"launch runtime path escapes receipt root: {key}={value}")

    fontconfig_file = Path(launch["fontconfig_file"])
    fontconfig_text = fontconfig_file.read_text()
    if str(generation_dir / "share/fonts/selected") not in fontconfig_text:
        fail(stage, "fontconfig input does not select the generation font directory")
    if str(VALIDATION_ROOT / "fontconfig/cache") not in fontconfig_text:
        fail(stage, "fontconfig cache is not receipt-local")

    argv_lines = (LAUNCH_RECEIPT_DIR / "argv.txt").read_text().splitlines()
    if argv_lines.count("--disable-gpu") != 1:
        fail(stage, "launcher argv does not contain exact --disable-gpu once")
    forbidden_argv = {
        "--enable-features=Vulkan",
        "--use-gl=angle",
        "--use-angle=vulkan",
        "--ignore-gpu-blocklist",
        "--disable-gpu-sandbox",
    }
    if forbidden_argv.intersection(argv_lines):
        fail(stage, "launcher argv contains forbidden GPU-enable flags")

    stage = "process_contract"
    processes = read_tsv(CAPTURE_OUT / "processes.tsv")
    class_counts = Counter(row["class"] for row in processes)
    if class_counts["main"] != 1:
        fail(stage, f"expected one main process, found {class_counts['main']}")
    if class_counts["renderer"] < 1 or class_counts["zygote"] < 1:
        fail(stage, "renderer/zygote topology is incomplete")
    if class_counts["gpu"] != 0:
        fail(stage, "GPU process observed in CPU validation")

    main_row = next(row for row in processes if row["class"] == "main")
    main_tokens = main_row["cmdline"].split()
    if main_tokens.count("--disable-gpu") != 1:
        fail(stage, "main process does not contain exact --disable-gpu once")
    if any(flag in main_tokens for flag in forbidden_argv):
        fail(stage, "main process contains a forbidden GPU-enable flag")

    renderers = [row for row in processes if row["class"] == "renderer"]
    if any("--disable-gpu-compositing" not in row["cmdline"].split() for row in renderers):
        fail(stage, "renderer without --disable-gpu-compositing observed")

    process_rows = [
        {"check": "main_count", "state": "PASS", "value": class_counts["main"]},
        {"check": "renderer_count", "state": "PASS", "value": class_counts["renderer"]},
        {"check": "zygote_count", "state": "PASS", "value": class_counts["zygote"]},
        {"check": "gpu_count", "state": "PASS", "value": class_counts["gpu"]},
        {"check": "main_disable_gpu_exact", "state": "PASS", "value": 1},
        {
            "check": "renderer_disable_gpu_compositing",
            "state": "PASS",
            "value": len(renderers),
        },
    ]
    write_tsv(
        OUT / "process-contract.tsv",
        ["check", "state", "value"],
        process_rows,
    )

    stage = "expected_mapping_model"
    semantic_rows = read_tsv(B9_OUT / "input/input__semantic-object-disposition.tsv")
    content_rows = read_tsv(B9_OUT / "input/content-object-plan.tsv")

    selected_expected: dict[str, dict[str, str]] = {}
    for row in content_rows:
        target = generation_base / row["object_relpath"]
        selected_expected[str(target)] = {
            "category": "SELECTED_OBJECT",
            "semantic_class": row["content_kind"],
            "sha256": row["sha256"],
            "source_path": row["source_path"],
        }

    app_expected: dict[str, dict[str, str]] = {}
    world_expected: dict[str, dict[str, str]] = {}
    excluded_graphics: set[str] = set()
    gpu_devices: set[str] = set()
    for row in semantic_rows:
        action = row["primary_action"]
        record = {
            "category": "",
            "semantic_class": row["semantic_class"],
            "sha256": row["sha256"],
            "source_path": row["path"],
        }
        if action == "REFERENCE_APP_LOCAL":
            record["category"] = "APP_LOCAL"
            app_expected[row["path"]] = record
        elif action in {"REFERENCE_WORLD_SUBSTRATE", "REFERENCE_WORLD_LOCALE"}:
            record["category"] = "PROTECTED_WORLD"
            world_expected[row["path"]] = record
        elif action == "EXCLUDE_CPU_BASE_GRAPHICS_FEATURE":
            excluded_graphics.add(row["path"])
        elif action == "REFERENCE_OPTIONAL_GPU_DEVICE":
            gpu_devices.add(row["path"])

    if len(selected_expected) != 96:
        fail(stage, f"expected 96 selected object paths, found {len(selected_expected)}")
    if len(app_expected) != 11:
        fail(stage, f"expected 11 app-local paths, found {len(app_expected)}")
    if len(world_expected) != 18:
        fail(stage, f"expected 18 protected-world paths, found {len(world_expected)}")
    if len(excluded_graphics) != 11:
        fail(stage, f"expected 11 excluded graphics paths, found {len(excluded_graphics)}")

    expected = {**selected_expected, **app_expected, **world_expected}
    if len(expected) != 125:
        fail(stage, f"expected immutable mapping set is not 125: {len(expected)}")

    stage = "mapped_identity"
    unique_rows = read_tsv(CAPTURE_OUT / "unique-objects.tsv")
    observed = {row["path"]: row["path_class"] for row in unique_rows}

    missing_expected = sorted(set(expected) - set(observed))
    write_tsv(
        OUT / "missing-expected-mapped-paths.tsv",
        ["path"],
        [{"path": path} for path in missing_expected],
    )
    if missing_expected:
        fail(stage, f"missing expected mapped paths: {len(missing_expected)}")

    if excluded_graphics.intersection(observed):
        fail(stage, "excluded graphics source path mapped in CPU validation")
    if gpu_devices.intersection(observed):
        fail(stage, "optional GPU device mapped in CPU validation")

    runtime_allowed: set[str] = set()
    device_allowed: set[str] = set()
    unexpected: list[str] = []
    for path_text in observed:
        path = Path(path_text)
        if path_text in expected:
            continue
        if path_text.startswith("/memfd:"):
            runtime_allowed.add(path_text)
            continue
        if path_text.startswith("/dev/"):
            device_allowed.add(path_text)
            continue
        if within(path, VALIDATION_ROOT):
            runtime_allowed.add(path_text)
            continue
        unexpected.append(path_text)

    write_tsv(
        OUT / "unexpected-mapped-paths.tsv",
        ["path"],
        [{"path": path} for path in sorted(unexpected)],
    )
    if unexpected:
        fail(stage, f"unexpected external mapped paths: {len(unexpected)}")

    broad_farm = str(HOME / "gl/lib") + "/"
    rootfs_prefix = str(ROOTFS) + "/"
    if any(path.startswith(broad_farm) for path in observed):
        fail(stage, "broad-farm mapping observed")
    if any(path.startswith(rootfs_prefix) for path in observed):
        fail(stage, "rootfs-provider mapping observed")
    if any("/current/" in path or path.endswith("/current") for path in observed):
        fail(stage, "current path observed in mapped set")

    identity_rows: list[dict[str, object]] = []
    identity_failures = 0
    category_counts: Counter[str] = Counter()
    for path_text, metadata in sorted(expected.items()):
        path = Path(path_text)
        exists = path.is_file() and not path.is_symlink()
        observed_sha = sha256(path) if exists else "MISSING"
        state_value = (
            "MATCH"
            if exists and observed_sha == metadata["sha256"]
            else "MISSING"
            if not exists
            else "HASH_MISMATCH"
        )
        identity_failures += int(state_value != "MATCH")
        category_counts[metadata["category"]] += 1
        identity_rows.append(
            {
                "category": metadata["category"],
                "semantic_class": metadata["semantic_class"],
                "mapped_path": path_text,
                "source_path": metadata["source_path"],
                "expected_sha256": metadata["sha256"],
                "observed_sha256": observed_sha,
                "state": state_value,
            }
        )

    write_tsv(
        OUT / "mapped-identity-verification.tsv",
        [
            "category",
            "semantic_class",
            "mapped_path",
            "source_path",
            "expected_sha256",
            "observed_sha256",
            "state",
        ],
        identity_rows,
    )
    if identity_failures:
        fail(stage, f"mapped identity failures: {identity_failures}")

    mapping_rows: list[dict[str, object]] = []
    for path_text in sorted(observed):
        if path_text in selected_expected:
            category = "SELECTED_OBJECT"
        elif path_text in app_expected:
            category = "APP_LOCAL"
        elif path_text in world_expected:
            category = "PROTECTED_WORLD"
        elif path_text in runtime_allowed:
            category = "RECEIPT_RUNTIME"
        elif path_text in device_allowed:
            category = "NON_GPU_DEVICE"
        else:
            category = "UNEXPECTED"
        mapping_rows.append(
            {
                "category": category,
                "capture_path_class": observed[path_text],
                "path": path_text,
            }
        )
    write_tsv(
        OUT / "mapped-path-classification.tsv",
        ["category", "capture_path_class", "path"],
        mapping_rows,
    )

    selected_kind_counts = Counter(row["content_kind"] for row in content_rows)
    summary_rows = [
        {"field": "branch", "value": branch},
        {"field": "head", "value": head},
        {"field": "phase_b9_root", "value": str(B9_OUT)},
        {"field": "phase_b9_head", "value": b9_summary.get("head", "")},
        {"field": "generation_id", "value": generation_id},
        {"field": "generation_dir", "value": str(generation_dir)},
        {"field": "topology_status", "value": "PASS"},
        {"field": "survival_status", "value": "PASS"},
        {"field": "maps_capture_status", "value": "PASS"},
        {"field": "main_processes", "value": class_counts["main"]},
        {"field": "renderer_processes", "value": class_counts["renderer"]},
        {"field": "zygote_processes", "value": class_counts["zygote"]},
        {"field": "gpu_processes", "value": class_counts["gpu"]},
        {"field": "selected_mapped_objects", "value": category_counts["SELECTED_OBJECT"]},
        {"field": "selected_elf_mapped", "value": selected_kind_counts["COPIED_ELF"]},
        {"field": "selected_font_mapped", "value": selected_kind_counts["COPIED_FONT"]},
        {
            "field": "selected_schema_mapped",
            "value": selected_kind_counts["GENERATED_GSETTINGS"],
        },
        {"field": "app_local_mapped_objects", "value": category_counts["APP_LOCAL"]},
        {
            "field": "protected_world_mapped_objects",
            "value": category_counts["PROTECTED_WORLD"],
        },
        {"field": "expected_immutable_mapped_objects", "value": len(expected)},
        {"field": "mapped_identity_failures", "value": identity_failures},
        {"field": "unexpected_external_mapped_paths", "value": len(unexpected)},
        {"field": "receipt_runtime_mapped_paths", "value": len(runtime_allowed)},
        {"field": "non_gpu_device_mapped_paths", "value": len(device_allowed)},
        {"field": "excluded_graphics_mapped_paths", "value": 0},
        {"field": "broad_farm_mapped_paths", "value": 0},
        {"field": "rootfs_provider_mapped_paths", "value": 0},
        {"field": "current_state_before", "value": before_rows[0]["state"]},
        {"field": "current_state_after", "value": after_rows[0]["state"]},
        {"field": "current_pointer_changed", "value": "NO"},
        {"field": "explicit_generation_selected", "value": "YES"},
        {"field": "runtime_launch_performed", "value": "YES"},
        {"field": "promoted_runtime_mutated", "value": "NO"},
    ]
    write_tsv(OUT / "summary.tsv", ["field", "value"], summary_rows)

    (OUT / "claim-boundary.txt").write_text(
        "This stage launches Obsidian in CPU mode through the explicit immutable generation path.\n"
        "It proves process survival, exact CPU flags, selection of all 96 selected content identities, "
        "preservation of 11 app-local and 18 protected-world identities, and absence of broad-farm, "
        "rootfs-provider, excluded-graphics, GPU-process, and current-pointer selection.\n"
        "Receipt-local runtime files and non-GPU device mappings are recorded separately and are not immutable candidate content.\n"
        "It does not activate current, test rollback, or mutate the promoted launcher.\n"
    )
    (OUT / "next-state.txt").write_text(
        "READY_FOR_ATOMIC_ACTIVATION_IMPLEMENTATION\n"
    )
    write_status("PASS")
    if (OUT / "failure-stage.txt").exists():
        (OUT / "failure-stage.txt").unlink()

    print("selected Obsidian Phase B10 explicit generation CPU validation: PASS")
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
