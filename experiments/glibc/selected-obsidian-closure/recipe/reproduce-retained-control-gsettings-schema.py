#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import os
import shutil
import subprocess
import sys
import traceback
from pathlib import Path

B5_OUT = Path(os.environ["B5_OUT"])
OUT = Path(
    os.environ.get(
        "OUT",
        "/tmp/selected-obsidian-phase-b6-gsettings-schema-reproduction",
    )
)
REPO = Path(
    subprocess.check_output(
        [
            "git",
            "-C",
            str(Path(__file__).resolve().parent),
            "rev-parse",
            "--show-toplevel",
        ],
        text=True,
    ).strip()
)

OUT.mkdir(parents=True, exist_ok=True)
(OUT / "input").mkdir(exist_ok=True)
(OUT / "attempts").mkdir(exist_ok=True)
stage = "initialization"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(
    path: Path,
    fieldnames: list[str],
    rows: list[dict[str, object]],
) -> None:
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def write_status(value: str) -> None:
    (OUT / "analysis.status").write_text(value + "\n")


def fail(stage_name: str, message: str, rc: int = 1) -> None:
    write_status("FAIL")
    (OUT / "failure-stage.txt").write_text(stage_name + "\n")
    print(message, file=sys.stderr)
    print(f"evidence: {OUT}", file=sys.stderr)
    raise SystemExit(rc)


def safe_id(path: Path) -> str:
    text = str(path).strip("/") or "root"
    return "".join(character if character.isalnum() else "_" for character in text)


def rootfs_split(path: Path) -> tuple[Path | None, str | None]:
    text = str(path)
    marker = "/rootfs/"
    if marker not in text:
        return None, None
    before, after = text.split(marker, 1)
    return Path(before + "/rootfs"), "/" + after


def build_dpkg_file_index(rootfs: Path) -> dict[str, set[str]]:
    result: dict[str, set[str]] = {}
    info_dir = rootfs / "var/lib/dpkg/info"
    if not info_dir.is_dir():
        return result
    for list_file in sorted(info_dir.glob("*.list")):
        package = list_file.name[: -len(".list")]
        try:
            lines = list_file.read_text(errors="replace").splitlines()
        except OSError:
            continue
        for line in lines:
            if not line.startswith("/"):
                continue
            result.setdefault(line, set()).add(package)
    return result


def native_package_owner(path: Path) -> str:
    for command in ("dpkg-query", "dpkg"):
        executable = shutil.which(command)
        if not executable:
            continue
        try:
            completed = subprocess.run(
                [executable, "-S", str(path)],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=10,
                check=False,
            )
        except (OSError, subprocess.TimeoutExpired):
            continue
        if completed.returncode == 0:
            owners = sorted(
                {
                    line.split(":", 1)[0]
                    for line in completed.stdout.splitlines()
                    if ":" in line
                }
            )
            if owners:
                return ",".join(owners)
    return "UNKNOWN"


def compiler_owner(path: Path, rootfs_indexes: dict[Path, dict[str, set[str]]]) -> str:
    rootfs, relative = rootfs_split(path)
    if rootfs is not None and relative is not None:
        index = rootfs_indexes.setdefault(rootfs, build_dpkg_file_index(rootfs))
        owners = sorted(index.get(relative, set()))
        return ",".join(owners) if owners else "UNOWNED"
    return native_package_owner(path)


def candidate_paths(aggregate_path: Path) -> list[Path]:
    values: list[Path] = []

    explicit = os.environ.get("SCHEMA_COMPILERS", "")
    for value in explicit.split(os.pathsep):
        if value:
            values.append(Path(value))

    which_value = shutil.which("glib-compile-schemas")
    if which_value:
        values.append(Path(which_value))

    prefix = Path(os.environ.get("PREFIX", "/data/data/com.termux/files/usr"))
    home = Path(os.environ.get("HOME", "/data/data/com.termux/files/home"))
    rootfs, _ = rootfs_split(aggregate_path)

    values.extend(
        [
            prefix / "bin/glib-compile-schemas",
            prefix / "glibc/bin/glib-compile-schemas",
            home / "gl/bin/glib-compile-schemas",
            home / "gl/libexec/glib-2.0/glib-compile-schemas",
        ]
    )
    if rootfs is not None:
        values.extend(
            [
                rootfs / "usr/bin/glib-compile-schemas",
                rootfs / "usr/libexec/glib-2.0/glib-compile-schemas",
            ]
        )

    for pattern in (
        prefix / "opt/*/bin/glib-compile-schemas",
        home / "gl/opt/*/bin/glib-compile-schemas",
    ):
        values.extend(pattern.parent.parent.glob(pattern.parent.name + "/bin/glib-compile-schemas"))

    unique: list[Path] = []
    seen: set[str] = set()
    for value in values:
        normalized = str(value)
        if normalized in seen:
            continue
        seen.add(normalized)
        unique.append(value)
    return unique


def run_command(command: list[str], timeout: int = 60) -> tuple[str, str, str, int | None]:
    try:
        completed = subprocess.run(
            command,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
            check=False,
        )
        return "EXECUTED", completed.stdout, completed.stderr, completed.returncode
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout if isinstance(exc.stdout, str) else ""
        stderr = exc.stderr if isinstance(exc.stderr, str) else ""
        return "TIMEOUT", stdout, stderr, None
    except OSError as exc:
        return "EXEC_ERROR", "", str(exc) + "\n", None


try:
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
        fail(stage, "tracked working-tree changes detected; Phase B6 requires exact HEAD", 2)

    branch = subprocess.check_output(
        ["git", "-C", str(REPO), "branch", "--show-current"],
        text=True,
    ).strip()
    head = subprocess.check_output(
        ["git", "-C", str(REPO), "rev-parse", "HEAD"],
        text=True,
    ).strip()

    (OUT / "repository-root.txt").write_text(str(REPO) + "\n")
    (OUT / "branch.txt").write_text(branch + "\n")
    (OUT / "head.txt").write_text(head + "\n")
    (OUT / "phase-b5-root.txt").write_text(str(B5_OUT) + "\n")

    required = [
        "analysis.status",
        "summary.tsv",
        "data-object-verification.tsv",
        "schema-source-manifest.tsv",
        "schema-compiler-verification.tsv",
    ]
    verification_rows: list[dict[str, object]] = []
    missing_inputs: list[str] = []
    stage = "input_verification"
    for name in required:
        source = B5_OUT / name
        embedded = OUT / "input" / name
        state = "PASS" if source.is_file() else "FAIL"
        verification_rows.append(
            {
                "file": name,
                "state": state,
                "path": str(source),
                "embedded_path": str(embedded) if state == "PASS" else "-",
            }
        )
        if state == "PASS":
            shutil.copy2(source, embedded)
        else:
            missing_inputs.append(name)

    write_tsv(
        OUT / "input-verification.tsv",
        ["file", "state", "path", "embedded_path"],
        verification_rows,
    )
    if missing_inputs:
        fail(stage, f"missing Phase B5 inputs: {', '.join(missing_inputs)}")

    if (B5_OUT / "analysis.status").read_text().strip() != "PASS":
        fail("phase_b5_status", "Phase B5 status is not PASS")

    b5_summary = {
        row["field"]: row["value"]
        for row in read_tsv(B5_OUT / "summary.tsv")
    }
    schema_objects = [
        row
        for row in read_tsv(B5_OUT / "data-object-verification.tsv")
        if row["semantic_class"] == "PROVIDER_SCHEMA_DATA"
    ]
    if len(schema_objects) != 1:
        fail("schema_aggregate", f"expected one schema aggregate, found {len(schema_objects)}")

    aggregate = schema_objects[0]
    aggregate_path = Path(aggregate["path"])
    retained_sha = aggregate["captured_sha256"]
    if aggregate["identity_state"] != "MATCH":
        fail("schema_aggregate", "retained schema aggregate identity is not MATCH")

    source_rows = read_tsv(B5_OUT / "schema-source-manifest.tsv")
    if not source_rows:
        fail("schema_sources", "schema source manifest is empty")

    stage = "schema_source_verification"
    source_verification_rows: list[dict[str, object]] = []
    source_failures = 0
    basenames: set[str] = set()
    for row in source_rows:
        source = Path(row["source_path"])
        exists = source.is_file()
        current_sha = sha256(source) if exists else "MISSING"
        identity_state = (
            "MATCH"
            if exists and current_sha == row["sha256"]
            else "MISSING"
            if not exists
            else "HASH_MISMATCH"
        )
        basename = source.name
        duplicate_basename = basename in basenames
        basenames.add(basename)
        if identity_state != "MATCH" or duplicate_basename:
            source_failures += 1
        source_verification_rows.append(
            {
                "source_kind": row["source_kind"],
                "source_path": str(source),
                "basename": basename,
                "captured_sha256": row["sha256"],
                "current_sha256": current_sha,
                "identity_state": identity_state,
                "duplicate_basename": "YES" if duplicate_basename else "NO",
                "dpkg_file_owners": row["dpkg_file_owners"],
            }
        )

    write_tsv(
        OUT / "schema-source-verification.tsv",
        [
            "source_kind",
            "source_path",
            "basename",
            "captured_sha256",
            "current_sha256",
            "identity_state",
            "duplicate_basename",
            "dpkg_file_owners",
        ],
        source_verification_rows,
    )
    if source_failures:
        fail(stage, f"schema source verification failures: {source_failures}")

    stage = "compiler_discovery"
    rootfs_indexes: dict[Path, dict[str, set[str]]] = {}
    compiler_rows: list[dict[str, object]] = []
    attempt_rows: list[dict[str, object]] = []
    candidates_found = 0
    runnable_candidates = 0
    successful_compiles = 0
    identical_outputs = 0
    compile_attempts = 0

    for candidate in candidate_paths(aggregate_path):
        exists = candidate.is_file()
        executable = os.access(candidate, os.X_OK) if exists else False
        realpath = candidate.resolve() if exists else candidate
        candidate_hash = sha256(candidate) if exists else "MISSING"
        package_owner = compiler_owner(candidate, rootfs_indexes) if exists else "-"
        if exists:
            candidates_found += 1

        version_state = "NOT_ATTEMPTED"
        version_stdout = ""
        version_stderr = ""
        version_rc: int | None = None
        if exists and executable:
            version_state, version_stdout, version_stderr, version_rc = run_command(
                [str(candidate), "--version"], timeout=20
            )
            if version_state == "EXECUTED":
                runnable_candidates += 1

        compiler_rows.append(
            {
                "candidate_path": str(candidate),
                "realpath": str(realpath),
                "present": "YES" if exists else "NO",
                "executable": "YES" if executable else "NO",
                "sha256": candidate_hash,
                "package_owner": package_owner,
                "version_state": version_state,
                "version_rc": "-" if version_rc is None else version_rc,
                "version_output": (version_stdout + version_stderr).strip().replace("\t", " ").replace("\n", " | "),
            }
        )

        if not (exists and executable):
            continue

        for mode, extra_args in (
            ("default", []),
            ("strict", ["--strict"]),
        ):
            compile_attempts += 1
            attempt_id = f"{safe_id(candidate)}__{mode}"
            attempt_dir = OUT / "attempts" / attempt_id
            schemas_dir = attempt_dir / "schemas"
            schemas_dir.mkdir(parents=True, exist_ok=True)

            for row in source_rows:
                source = Path(row["source_path"])
                shutil.copy2(source, schemas_dir / source.name)

            command = [str(candidate), *extra_args, str(schemas_dir)]
            state, stdout, stderr, rc = run_command(command, timeout=120)
            (attempt_dir / "command.txt").write_text("\n".join(command) + "\n")
            (attempt_dir / "stdout.txt").write_text(stdout)
            (attempt_dir / "stderr.txt").write_text(stderr)

            generated = schemas_dir / "gschemas.compiled"
            generated_present = generated.is_file()
            generated_sha = sha256(generated) if generated_present else "MISSING"
            match = generated_present and generated_sha == retained_sha
            if state == "EXECUTED" and rc == 0 and generated_present:
                successful_compiles += 1
            if match:
                identical_outputs += 1

            attempt_rows.append(
                {
                    "candidate_path": str(candidate),
                    "candidate_sha256": candidate_hash,
                    "package_owner": package_owner,
                    "mode": mode,
                    "execution_state": state,
                    "return_code": "-" if rc is None else rc,
                    "generated_present": "YES" if generated_present else "NO",
                    "generated_sha256": generated_sha,
                    "retained_sha256": retained_sha,
                    "byte_identical": "YES" if match else "NO",
                    "attempt_directory": str(attempt_dir),
                }
            )

    write_tsv(
        OUT / "schema-compiler-candidates.tsv",
        [
            "candidate_path",
            "realpath",
            "present",
            "executable",
            "sha256",
            "package_owner",
            "version_state",
            "version_rc",
            "version_output",
        ],
        compiler_rows,
    )
    write_tsv(
        OUT / "schema-reproduction-attempts.tsv",
        [
            "candidate_path",
            "candidate_sha256",
            "package_owner",
            "mode",
            "execution_state",
            "return_code",
            "generated_present",
            "generated_sha256",
            "retained_sha256",
            "byte_identical",
            "attempt_directory",
        ],
        attempt_rows,
    )

    summary_rows = [
        {"field": "branch", "value": branch},
        {"field": "head", "value": head},
        {"field": "phase_b5_root", "value": str(B5_OUT)},
        {"field": "phase_b5_head", "value": b5_summary.get("head", "")},
        {"field": "schema_source_files", "value": len(source_rows)},
        {"field": "schema_source_verification_failures", "value": source_failures},
        {"field": "retained_schema_sha256", "value": retained_sha},
        {"field": "compiler_candidate_paths", "value": len(compiler_rows)},
        {"field": "compiler_candidates_present", "value": candidates_found},
        {"field": "runnable_compiler_candidates", "value": runnable_candidates},
        {"field": "compile_attempts", "value": compile_attempts},
        {"field": "successful_compiles", "value": successful_compiles},
        {"field": "byte_identical_outputs", "value": identical_outputs},
        {"field": "runtime_launch_performed", "value": "NO"},
        {"field": "promoted_runtime_mutated", "value": "NO"},
    ]
    write_tsv(OUT / "summary.tsv", ["field", "value"], summary_rows)

    if identical_outputs:
        next_state = "READY_FOR_COMPLETE_DATA_MANIFEST"
    elif successful_compiles:
        next_state = "REVIEW_SCHEMA_COMPILER_VERSION_DIFFERENCE"
    else:
        next_state = "ACQUIRE_SCHEMA_COMPILER_ORACLE"

    (OUT / "next-state.txt").write_text(next_state + "\n")
    (OUT / "claim-boundary.txt").write_text(
        "This is a read-only GSettings compiler discovery and reproduction audit.\n"
        "All compilation occurs in receipt-local temporary directories copied from the retained source manifest.\n"
        "A byte-identical output proves reproducibility only for the recorded source and compiler identities.\n"
        "A different generated hash is evidence of a compiler/version/mode difference and is not an authorization to replace the retained aggregate.\n"
        "No rootfs package is installed, no application is launched, and no promoted runtime is mutated.\n"
    )
    write_status("PASS")
    if (OUT / "failure-stage.txt").exists():
        (OUT / "failure-stage.txt").unlink()

    print("selected Obsidian Phase B6 GSettings schema reproduction: PASS")
    print(f"evidence: {OUT}")
    print("\n===== summary =====")
    for row in summary_rows:
        print(f"{row['field']}\t{row['value']}")
    print("\n===== next state =====")
    print(next_state)

except SystemExit:
    raise
except Exception:
    write_status("FAIL")
    (OUT / "failure-stage.txt").write_text(stage + "\n")
    traceback.print_exc()
    print(f"evidence: {OUT}", file=sys.stderr)
    raise SystemExit(1)
