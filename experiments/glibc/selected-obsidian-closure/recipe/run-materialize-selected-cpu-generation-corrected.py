#!/usr/bin/env python3
from __future__ import annotations

import ctypes
import csv
import errno
import os
import runpy
import subprocess
import sys
import time
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
BASE = SCRIPT_DIR / "materialize-selected-cpu-generation.py"
EXPECTED_BASE_BLOB = "98a188a314178e345049cfe296c51d60a485fc2a"
OUT = Path(
    os.environ.get(
        "OUT",
        "/tmp/selected-obsidian-phase-b9-staging-generation-materialization-corrected",
    )
)
OUT.mkdir(parents=True, exist_ok=True)


def write_tsv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def wrapper_fail(stage: str, message: str, rc: int = 2) -> None:
    (OUT / "analysis.status").write_text("FAIL\n")
    (OUT / "failure-stage.txt").write_text(stage + "\n")
    print(message, file=sys.stderr)
    print(f"evidence: {OUT}", file=sys.stderr)
    raise SystemExit(rc)


def fsync_dir(path: Path) -> None:
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def errno_name(value: int) -> str:
    return errno.errorcode.get(value, "-") if value else "-"


repo = Path(
    subprocess.check_output(
        ["git", "-C", str(SCRIPT_DIR), "rev-parse", "--show-toplevel"],
        text=True,
    ).strip()
)
observed_blob = subprocess.check_output(
    ["git", "-C", str(repo), "hash-object", str(BASE)],
    text=True,
).strip()

write_tsv(
    OUT / "corrected-entrypoint.tsv",
    ["field", "value"],
    [
        {"field": "base_script", "value": str(BASE)},
        {"field": "expected_base_git_blob", "value": EXPECTED_BASE_BLOB},
        {"field": "observed_base_git_blob", "value": observed_blob},
        {"field": "object_publication_contract", "value": "renameat2_RENAME_NOREPLACE"},
        {"field": "generation_publication_contract", "value": "probed_renameat2_RENAME_NOREPLACE"},
        {"field": "frozen_root_direct_attempt", "value": "REQUIRED_FIRST"},
        {"field": "android_root_thaw_refreeze_fallback", "value": "EACCES_OR_EPERM_ONLY_AFTER_PROBE"},
        {"field": "ordinary_overwrite_rename_fallback", "value": "DISABLED"},
    ],
)

if observed_blob != EXPECTED_BASE_BLOB:
    wrapper_fail(
        "corrected_entrypoint_base_identity",
        "base materializer Git blob differs from the reviewed corrected-entrypoint contract",
    )

libc = ctypes.CDLL(None, use_errno=True)
AT_FDCWD = -100
RENAME_NOREPLACE = 1

renameat2 = getattr(libc, "renameat2", None)
if renameat2 is not None:
    renameat2.argtypes = [
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_uint,
    ]
    renameat2.restype = ctypes.c_int
    primitive = "libc.renameat2"

    def call_rename_noreplace(source: bytes, target: bytes) -> int:
        return renameat2(
            AT_FDCWD,
            source,
            AT_FDCWD,
            target,
            RENAME_NOREPLACE,
        )

else:
    machine = os.uname().machine
    syscall_numbers = {
        "aarch64": 276,
        "armv7l": 382,
        "x86_64": 316,
        "i686": 353,
    }
    syscall_number = syscall_numbers.get(machine)
    if syscall_number is None:
        wrapper_fail(
            "publication_primitive_discovery",
            f"renameat2 symbol unavailable and no reviewed syscall number for {machine}",
        )
    libc.syscall.restype = ctypes.c_long
    primitive = f"libc.syscall({syscall_number})"

    def call_rename_noreplace(source: bytes, target: bytes) -> int:
        return int(
            libc.syscall(
                ctypes.c_long(syscall_number),
                ctypes.c_int(AT_FDCWD),
                ctypes.c_char_p(source),
                ctypes.c_int(AT_FDCWD),
                ctypes.c_char_p(target),
                ctypes.c_uint(RENAME_NOREPLACE),
            )
        )


def invoke_rename_noreplace(source: os.PathLike[str] | str, target: os.PathLike[str] | str) -> tuple[int, int]:
    ctypes.set_errno(0)
    result = call_rename_noreplace(os.fsencode(source), os.fsencode(target))
    observed_errno = ctypes.get_errno() if result != 0 else 0
    return result, observed_errno


object_attempts_path = OUT / "publication-primitive-attempts.tsv"
object_attempt_fields = [
    "attempt",
    "primitive",
    "source",
    "target",
    "state",
    "errno",
    "errno_name",
]
object_attempt_rows: list[dict[str, object]] = []


def flush_object_attempts() -> None:
    write_tsv(object_attempts_path, object_attempt_fields, object_attempt_rows)


def atomic_noreplace_link(
    source: os.PathLike[str] | str,
    target: os.PathLike[str] | str,
    *args: object,
    **kwargs: object,
) -> None:
    if args or kwargs:
        raise TypeError("corrected object publication accepts only source and target")

    source_text = os.fspath(source)
    target_text = os.fspath(target)
    result, observed_errno = invoke_rename_noreplace(source_text, target_text)

    if result == 0:
        state = "PUBLISHED"
    elif observed_errno == errno.EEXIST:
        state = "DESTINATION_EXISTS"
    else:
        state = "FAILED"

    object_attempt_rows.append(
        {
            "attempt": len(object_attempt_rows) + 1,
            "primitive": primitive,
            "source": source_text,
            "target": target_text,
            "state": state,
            "errno": observed_errno,
            "errno_name": errno_name(observed_errno),
        }
    )
    flush_object_attempts()

    if result == 0:
        return
    if observed_errno == errno.EEXIST:
        raise FileExistsError(observed_errno, os.strerror(observed_errno), target_text)
    raise OSError(
        observed_errno,
        f"renameat2 RENAME_NOREPLACE failed via {primitive}: {os.strerror(observed_errno)}",
        target_text,
    )


generation_attempts_path = OUT / "generation-publication-attempts.tsv"
generation_attempt_fields = [
    "attempt",
    "phase",
    "primitive",
    "source_mode",
    "source",
    "target",
    "state",
    "errno",
    "errno_name",
]
generation_attempt_rows: list[dict[str, object]] = []


def record_generation_attempt(
    phase: str,
    source_mode: str,
    source: Path,
    target: Path,
    result: int,
    observed_errno: int,
) -> None:
    generation_attempt_rows.append(
        {
            "attempt": len(generation_attempt_rows) + 1,
            "phase": phase,
            "primitive": primitive,
            "source_mode": source_mode,
            "source": str(source),
            "target": str(target),
            "state": (
                "PUBLISHED"
                if result == 0
                else "DESTINATION_EXISTS"
                if observed_errno == errno.EEXIST
                else "FAILED"
            ),
            "errno": observed_errno,
            "errno_name": errno_name(observed_errno),
        }
    )
    write_tsv(
        generation_attempts_path,
        generation_attempt_fields,
        generation_attempt_rows,
    )


def cleanup_probe(path: Path) -> None:
    if not path.exists() and not path.is_symlink():
        return
    if path.is_symlink() or path.is_file():
        path.unlink()
        return
    path.chmod(0o700)
    path.rmdir()


def raise_rename_failure(observed_errno: int, target: Path, context: str) -> None:
    if observed_errno == errno.EEXIST:
        raise FileExistsError(observed_errno, os.strerror(observed_errno), str(target))
    raise OSError(
        observed_errno,
        f"{context} via {primitive}: {os.strerror(observed_errno)}",
        str(target),
    )


def atomic_generation_rename(
    source: os.PathLike[str] | str,
    target: os.PathLike[str] | str,
    *args: object,
    **kwargs: object,
) -> None:
    if args or kwargs:
        raise TypeError("corrected generation publication accepts only source and target")

    source_path = Path(source)
    target_path = Path(target)
    if not source_path.is_dir() or source_path.is_symlink():
        raise OSError(errno.EINVAL, "generation publication source is not a plain directory", str(source_path))
    if target_path.exists() or target_path.is_symlink():
        raise FileExistsError(errno.EEXIST, os.strerror(errno.EEXIST), str(target_path))

    probe_id = f".generation-rename-probe-{os.getpid()}-{time.time_ns()}"
    probe_source = source_path.parent / probe_id
    probe_target = target_path.parent / probe_id
    selected_mode = ""

    try:
        probe_source.mkdir(mode=0o700)
        probe_source.chmod(0o555)
        fsync_dir(probe_source.parent)

        result, observed_errno = invoke_rename_noreplace(probe_source, probe_target)
        record_generation_attempt(
            "PROBE_FROZEN_ROOT",
            "0555",
            probe_source,
            probe_target,
            result,
            observed_errno,
        )
        if result == 0:
            selected_mode = "FROZEN_ROOT_DIRECT"
            cleanup_probe(probe_target)
            fsync_dir(probe_target.parent)
        elif observed_errno in {errno.EACCES, errno.EPERM}:
            probe_source.chmod(0o700)
            fsync_dir(probe_source)
            result, observed_errno = invoke_rename_noreplace(probe_source, probe_target)
            record_generation_attempt(
                "PROBE_WRITABLE_ROOT",
                "0700",
                probe_source,
                probe_target,
                result,
                observed_errno,
            )
            if result != 0:
                raise_rename_failure(
                    observed_errno,
                    probe_target,
                    "writable-root generation publication probe failed",
                )
            selected_mode = "THAW_ROOT_PUBLISH_REFREEZE"
            cleanup_probe(probe_target)
            fsync_dir(probe_target.parent)
        else:
            raise_rename_failure(
                observed_errno,
                probe_target,
                "frozen-root generation publication probe failed",
            )
    finally:
        cleanup_probe(probe_source)
        cleanup_probe(probe_target)

    if selected_mode == "FROZEN_ROOT_DIRECT":
        result, observed_errno = invoke_rename_noreplace(source_path, target_path)
        record_generation_attempt(
            "GENERATION_PUBLICATION",
            "0555",
            source_path,
            target_path,
            result,
            observed_errno,
        )
        if result != 0:
            raise_rename_failure(
                observed_errno,
                target_path,
                "frozen-root generation publication failed",
            )
        return

    if selected_mode != "THAW_ROOT_PUBLISH_REFREEZE":
        raise RuntimeError("generation publication probe did not select a mode")

    source_path.chmod(0o700)
    fsync_dir(source_path)
    result, observed_errno = invoke_rename_noreplace(source_path, target_path)
    record_generation_attempt(
        "GENERATION_PUBLICATION",
        "0700_THEN_0555",
        source_path,
        target_path,
        result,
        observed_errno,
    )
    if result != 0:
        if source_path.exists() and source_path.is_dir():
            source_path.chmod(0o555)
            fsync_dir(source_path)
        raise_rename_failure(
            observed_errno,
            target_path,
            "thawed-root generation publication failed",
        )

    target_path.chmod(0o555)
    fsync_dir(target_path)
    fsync_dir(target_path.parent)


# The reviewed base materializer invokes os.link only for no-overwrite content
# object publication and os.rename only for final generation publication.
os.link = atomic_noreplace_link  # type: ignore[assignment]
os.rename = atomic_generation_rename  # type: ignore[assignment]

try:
    runpy.run_path(str(BASE), run_name="__main__")
finally:
    if not object_attempts_path.exists():
        flush_object_attempts()
    if not generation_attempts_path.exists():
        write_tsv(
            generation_attempts_path,
            generation_attempt_fields,
            generation_attempt_rows,
        )
