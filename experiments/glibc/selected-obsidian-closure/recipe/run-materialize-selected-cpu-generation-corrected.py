#!/usr/bin/env python3
from __future__ import annotations

import ctypes
import csv
import errno
import os
import runpy
import subprocess
import sys
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
        {"field": "publication_contract", "value": "renameat2_RENAME_NOREPLACE"},
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


attempts_path = OUT / "publication-primitive-attempts.tsv"
attempt_fields = [
    "attempt",
    "primitive",
    "source",
    "target",
    "state",
    "errno",
    "errno_name",
]
attempt_rows: list[dict[str, object]] = []


def flush_attempts() -> None:
    write_tsv(attempts_path, attempt_fields, attempt_rows)


def atomic_noreplace_link(source: os.PathLike[str] | str, target: os.PathLike[str] | str, *args: object, **kwargs: object) -> None:
    if args or kwargs:
        raise TypeError("corrected publication primitive accepts only source and target")

    source_text = os.fspath(source)
    target_text = os.fspath(target)
    ctypes.set_errno(0)
    result = call_rename_noreplace(os.fsencode(source_text), os.fsencode(target_text))
    observed_errno = ctypes.get_errno() if result != 0 else 0

    if result == 0:
        state = "PUBLISHED"
    elif observed_errno == errno.EEXIST:
        state = "DESTINATION_EXISTS"
    else:
        state = "FAILED"

    attempt_rows.append(
        {
            "attempt": len(attempt_rows) + 1,
            "primitive": primitive,
            "source": source_text,
            "target": target_text,
            "state": state,
            "errno": observed_errno,
            "errno_name": errno.errorcode.get(observed_errno, "-") if observed_errno else "-",
        }
    )
    flush_attempts()

    if result == 0:
        return
    if observed_errno == errno.EEXIST:
        raise FileExistsError(observed_errno, os.strerror(observed_errno), target_text)
    raise OSError(
        observed_errno,
        f"renameat2 RENAME_NOREPLACE failed via {primitive}: {os.strerror(observed_errno)}",
        target_text,
    )


# The reviewed base materializer invokes os.link only for no-overwrite object
# publication. Replace that call in-process with renameat2 RENAME_NOREPLACE.
os.link = atomic_noreplace_link  # type: ignore[assignment]

try:
    runpy.run_path(str(BASE), run_name="__main__")
finally:
    if not attempts_path.exists():
        flush_attempts()
