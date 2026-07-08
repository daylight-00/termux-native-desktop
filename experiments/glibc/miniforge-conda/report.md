# Termux glibc Miniforge Experiment Report

## 1. Purpose

This document records the complete experiment performed before starting the PyMOL installation phase.

The goal was to determine whether a native Termux environment could host and run a practical Linux `glibc` Miniforge/Conda stack without using `proot-distro`, and whether environments created by Conda or Mamba could execute real compiled packages.

The experiment focused on the following questions:

1. Can the official Miniforge Linux installer be adapted for Termux?
2. Can Miniforge run through Termux's `glibc` compatibility stack?
3. Can `conda` and `mamba` execute successfully?
4. Can new Conda environments be created?
5. Can compiled packages such as NumPy be installed and executed?
6. What modifications are required for ELF interpreters, RPATH/RUNPATH, linker scripts, and Termux-specific preload behavior?
7. What parts of the workflow must be preserved or avoided for future GUI workloads such as PyMOL?

The final result was positive:

> A Miniforge installation under Termux `glibc` was made operational. Conda and Mamba executed successfully, Python environments were created successfully, a Python 3.11 environment ran successfully, and a NumPy environment imported and executed NumPy successfully.

However, several important Termux-specific runtime constraints were discovered and must remain part of the final workflow.

---

## 2. Environment

The relevant environment observed during the experiment was:

- Host: Android / Termux
- Architecture: `aarch64`
- Kernel as reported by Conda:
  - `Linux/5.10.236-android12-9-31998796-abS908NKSS9GZE5`
- Termux glibc location:
  - `/data/data/com.termux/files/usr/glibc`
- Miniforge installation prefix:
  - `/data/data/com.termux/files/home/miniforge3-glibc`
- Helper command directory:
  - `/data/data/com.termux/files/home/.local/bin`
- Runtime shim directory:
  - `/data/data/com.termux/files/home/.local/lib/termux-glibc-runtime`
- Base Miniforge Python:
  - Python 3.13.13
- Conda:
  - 26.3.2
- Mamba:
  - 2.5.0
- Tested created environment:
  - Python 3.11.15
- Tested NumPy version:
  - NumPy 2.4.6

Observed Termux preload:

```text
/data/data/com.termux/files/usr/lib/libtermux-exec-ld-preload.so
```

This preload later became one of the most important compatibility findings.

---

## 3. Initial Design

The first design attempted to adapt the official Miniforge Linux installer.

The main difficulty was that the installer is not only a shell script. During installation it extracts a bootstrap Conda executable and then directly executes the extracted ELF binaries.

A simple execution such as:

```bash
bash Miniforge3-Linux-aarch64.sh
```

was therefore not sufficient for the Termux environment.

The original plan was to modify the installer so that the bootstrap executable would run through `glibc-runner` or an equivalent loader wrapper.

The approach was then refined.

Instead of wrapping every bootstrap invocation with `grun`, the selected strategy became:

1. Download the official Miniforge installer.
2. Patch the installer header.
3. After extracting the bootstrap ELF, patch its ELF interpreter and RPATH.
4. Patch the installed Miniforge prefix.
5. Create helper wrappers for Python, Conda, Mamba, and post-install environment patching.

The installer was intended to install to:

```text
$HOME/miniforge3-glibc
```

---

## 4. First Installer Script Failure

The initial installer script successfully reached architecture detection:

```text
[termux-glibc-miniforge] 아키텍처 감지: aarch64 -> Miniforge aarch64, conda subdir linux-aarch64
```

and then terminated unexpectedly.

The problem was traced to the glibc path discovery logic.

The initial implementation used constructs similar to:

```bash
find ... | head -n 1
```

inside a script running with:

```bash
set -Eeuo pipefail
```

This can cause the pipeline to terminate in a way that triggers `pipefail`, while the script exits before useful diagnostics are printed.

The glibc path detection logic was rewritten to use:

```bash
find "$glibc_root" -type f -name "$GLIBC_LD_NAME" -print -quit
```

instead of `find | head`.

The revised logic searched for:

```text
ld-linux-aarch64.so.1
libc.so.6
```

under:

```text
$PREFIX/glibc
```

and exported:

```text
TERMUX_GLIBC_LD
TERMUX_GLIBC_LIB
TERMUX_GLIBC_LIBC
CONDA_OVERRIDE_GLIBC
```

This allowed installation to continue.

---

## 5. Miniforge Installation Completed

After the path-discovery fix, Miniforge installation itself completed.

Relevant output:

```text
installation finished.
[termux-glibc-miniforge] 설치 후 전체 prefix 재패치
[termux-glibc-miniforge] 최종 ELF patch: /data/data/com.termux/files/home/miniforge3-glibc
[termux-glibc-miniforge] helper 생성 완료: /data/data/com.termux/files/home/.local/bin/{conda-glibc,mamba-glibc,python-glibc,patch-conda-glibc}
[warn] /data/data/com.termux/files/home/.local/bin 가 PATH에 없습니다. 다음 줄을 ~/.bashrc에 추가하세요:
[warn] export PATH="$HOME/.local/bin:$PATH"
[termux-glibc-miniforge] smoke test 실행
/data/data/com.termux/files/home/miniforge3-glibc/bin/python: error while loading shared libraries: /data/data/com.termux/files/usr/glibc/lib/libc.so: invalid ELF header
```

This established an important fact:

> Miniforge installation succeeded, but runtime library resolution was still incorrect.

---

## 6. `libc.so: invalid ELF header`

The first runtime failure was:

```text
/data/data/com.termux/files/home/miniforge3-glibc/bin/python:
error while loading shared libraries:
/data/data/com.termux/files/usr/glibc/lib/libc.so:
invalid ELF header
```

The relevant checks were:

```bash
patchelf --print-rpath "$HOME/miniforge3-glibc/bin/python"
patchelf --print-needed "$HOME/miniforge3-glibc/bin/python" | grep libc || true
file "$PREFIX/glibc/lib/libc.so"
```

Observed output:

```text
/data/data/com.termux/files/home/.local/lib/termux-glibc-runtime:/data/data/com.termux/files/home/miniforge3-glibc/lib:/data/data/com.termux/files/home/miniforge3-glibc/lib64:$ORIGIN/../lib:/data/data/com.termux/files/home/miniforge3-glibc/lib:/data/data/com.termux/files/home/miniforge3-glibc/lib64:/data/data/com.termux/files/home/miniforge3-glibc/lib:/data/data/com.termux/files/home/miniforge3-glibc/lib64
```

The Python binary itself required:

```text
libc.so.6
```

and:

```bash
file "$PREFIX/glibc/lib/libc.so"
```

returned:

```text
/data/data/com.termux/files/usr/glibc/lib/libc.so: ASCII text
```

This proved that `libc.so` was not a runtime ELF shared object. It was a linker script.

The runtime design was therefore changed.

---

## 7. Runtime Shim Directory

A dedicated runtime shim directory was created:

```text
$HOME/.local/lib/termux-glibc-runtime
```

The intended purpose was:

1. Include only actual ELF runtime libraries.
2. Avoid directly placing the entire Termux glibc library directory in the runtime search path.
3. Prevent the loader from opening linker scripts such as `libc.so`.
4. Provide safe aliases where required.

The shim creation logic conceptually used:

```bash
find "$GLIBC_DIR" -maxdepth 1 \( -type f -o -type l \) -name '*.so*'
```

and only linked files whose resolved target passed:

```bash
file -b "$target" | grep -q '^ELF '
```

A special alias was also created:

```bash
ln -sfn "$GLIBC_DIR/libc.so.6" "$RUNTIME_DIR/libc.so"
```

Similar compatibility aliases were later considered for:

```text
libm.so
libdl.so
libpthread.so
librt.so
libutil.so
libresolv.so
```

The ELF patching logic was also changed so that:

```text
$PREFIX/glibc/lib
```

would not remain in the patched RPATH.

---

## 8. `LD_LIBRARY_PATH` Was Checked

Because the same error continued, the shell environment was checked:

```bash
echo "$LD_LIBRARY_PATH"
```

The output was empty.

Therefore, the runtime problem was not caused by a user-set `LD_LIBRARY_PATH`.

This narrowed the problem to:

- ELF RPATH/RUNPATH,
- inherited preload behavior,
- or a dependency loaded by the Python executable.

---

## 9. Direct Loader Wrappers

The helper wrappers were redesigned to directly invoke the glibc loader:

```bash
"$PREFIX/glibc/lib/ld-linux-aarch64.so.1"
```

with an explicit library path:

```text
$HOME/.local/lib/termux-glibc-runtime
$HOME/miniforge3-glibc/lib
$HOME/miniforge3-glibc/lib64
```

The conceptual Python wrapper became:

```bash
exec "$GLIBC_LD" \
  --library-path "$RUNTIME_DIR:$MF_PREFIX/lib:$MF_PREFIX/lib64" \
  "$MF_PREFIX/bin/python" "$@"
```

Equivalent wrappers were made for:

```text
conda-glibc
mamba-glibc
python-glibc
```

This removed dependence on normal host ELF startup behavior.

---

## 10. Termux `LD_PRELOAD` Conflict

The next failure was:

```text
/data/data/com.termux/files/home/miniforge3-glibc/bin/python:
/data/data/com.termux/files/home/.local/lib/termux-glibc-runtime/libc.so.6:
version `LIBC' not found
(required by /data/data/com.termux/files/usr/lib/libtermux-exec-ld-preload.so)
```

The environment was checked:

```bash
echo "$LD_PRELOAD"
```

Output:

```text
/data/data/com.termux/files/usr/lib/libtermux-exec-ld-preload.so
```

This identified a major compatibility issue.

Termux had injected a native Termux/Android preload library into the process. The glibc loader attempted to load this Bionic-oriented shared object into the glibc process.

The wrappers were therefore updated to explicitly clear both:

```bash
unset LD_PRELOAD
unset LD_LIBRARY_PATH
```

before running any glibc Miniforge executable.

The critical direct test was:

```bash
env -u LD_PRELOAD -u LD_LIBRARY_PATH \
  "$HOME/.local/bin/conda-glibc" info
```

This succeeded in running Conda.

---

## 11. First Successful `conda info`

The command:

```bash
env -u LD_PRELOAD -u LD_LIBRARY_PATH \
  "$HOME/.local/bin/conda-glibc" info
```

produced a traceback from a spawned child process, but the main Conda process completed and printed its environment information.

Relevant output:

```text
/data/data/com.termux/files/home/miniforge3-glibc/lib/python3.13/signal.py:71:
RuntimeWarning: invalid signal number 32, please use valid_signals()
```

Then:

```text
Traceback (most recent call last):
  File "<string>", line 1, in <module>
    from multiprocessing.spawn import spawn_main;
    spawn_main(tracker_fd=6, pipe_handle=8)
...
  File "/data/data/com.termux/files/home/miniforge3-glibc/lib/python3.13/multiprocessing/synchronize.py", line 115, in __setstate__
    self._semlock = _multiprocessing.SemLock._rebuild(*state)
OSError: [Errno 40] Too many levels of symbolic links
```

Despite the child-process traceback, Conda printed:

```text
active environment : None
user config file : /data/data/com.termux/files/home/.condarc
populated config files : /data/data/com.termux/files/home/miniforge3-glibc/.condarc
conda version : 26.3.2
conda-build version : not installed
python version : 3.13.13.final.0
solver : libmamba (default)
virtual packages : __archspec=1=neoverse_n1
                   __conda=26.3.2=0
                   __glibc=2.17=0
                   __linux=5.10.236=0
                   __unix=0=0
base environment : /data/data/com.termux/files/home/miniforge3-glibc  (writable)
channel URLs : https://conda.anaconda.org/conda-forge/linux-aarch64
               https://conda.anaconda.org/conda-forge/noarch
platform : linux-aarch64
```

This was the first major proof that the Miniforge installation was operational.

---

## 12. Base Runtime Validation

The helper commands were tested.

### Python

Input:

```bash
python-glibc --version
```

Output:

```text
Python 3.13.13
```

### Mamba

Input:

```bash
mamba-glibc --version
```

Output:

```text
2.5.0
```

### Python standard library and C-extension smoke test

Input:

```bash
python-glibc - <<'PY'
import sys
import ssl
import sqlite3
import ctypes
import hashlib
import zlib

print(sys.version)
print("basic imports ok")
PY
```

Output:

```text
3.13.13 | packaged by conda-forge | (main, Apr  8 2026, 01:54:17) [GCC 14.3.0]
basic imports ok
```

This validated several important compiled/runtime components:

- OpenSSL integration
- SQLite
- `ctypes`
- hashing modules
- zlib

---

## 13. Multiprocessing Semaphore Test

Because Conda emitted a multiprocessing traceback, a direct semaphore test was performed.

Input:

```bash
python-glibc - <<'PY'
import multiprocessing as mp

print("start method:", mp.get_start_method())

try:
    s = mp.Semaphore(1)
    print("multiprocessing semaphore ok")
except Exception as e:
    print("multiprocessing semaphore failed:", repr(e))
PY
```

Output:

```text
start method: fork
multiprocessing semaphore ok
```

This result was important.

It showed that:

> `multiprocessing.Semaphore` itself was not generally broken.

The Conda traceback was more specific to a particular spawned child-process path used during Conda information collection.

---

## 14. `--no-plugins` Test

To determine whether the traceback was caused by a Conda plugin, the following command was run:

```bash
conda-glibc --no-plugins info
```

The traceback still appeared:

```text
OSError: [Errno 40] Too many levels of symbolic links
```

but Conda again completed and printed full environment information.

This ruled out the simplest plugin-only explanation.

The solver was switched to classic mode.

Observed Conda output included:

```text
solver : classic
```

The child-process traceback still appeared.

---

## 15. Conda Exit Code Validation

The critical validation was:

```bash
conda-glibc info
echo "exit=$?"
```

Observed result:

```text
exit=0
```

This established that the main Conda process completed successfully despite the child-process stderr traceback.

The working interpretation became:

> Conda itself was operational; a specific auxiliary child process was failing, but this failure was non-fatal for `conda info`.

---

## 16. First Environment Creation Test

A Python 3.11 environment named `smoke` was created.

Input:

```bash
conda-glibc create -y -n smoke python=3.11
echo "create_exit=$?"
```

The transaction completed.

Output included:

```text
Executing transaction: done

#
# To activate this environment, use
#
#     $ conda activate smoke
#
# To deactivate an active environment, use
#
#     $ conda deactivate
```

Exit code:

```text
create_exit=0
```

The environment was then patched:

```bash
patch-conda-glibc "$HOME/miniforge3-glibc/envs/smoke"
```

Output:

```text
[patch-conda-glibc] scanning /data/data/com.termux/files/home/miniforge3-glibc/envs/smoke
```

---

## 17. `run-conda-glibc` Environment Runner

A generic environment runner was created.

The important logic was:

```bash
ENV_NAME="${1:?usage: run-conda-glibc <env-name> <program> [args...]}"
shift

PROGRAM="${1:?usage: run-conda-glibc <env-name> <program> [args...]}"
shift

MF_PREFIX="$HOME/miniforge3-glibc"
ENV_PREFIX="$MF_PREFIX/envs/$ENV_NAME"
RUNTIME_DIR="$HOME/.local/lib/termux-glibc-runtime"
GLIBC_LD="$PREFIX/glibc/lib/ld-linux-aarch64.so.1"

unset LD_PRELOAD
unset LD_LIBRARY_PATH

exec "$GLIBC_LD" \
  --library-path "$RUNTIME_DIR:$ENV_PREFIX/lib:$ENV_PREFIX/lib64:$MF_PREFIX/lib:$MF_PREFIX/lib64" \
  "$ENV_PREFIX/bin/$PROGRAM" "$@"
```

This allowed commands such as:

```bash
run-conda-glibc smoke python ...
```

without activating the environment globally.

---

## 18. Successful Python 3.11 Environment Test

Input:

```bash
run-conda-glibc smoke python - <<'PY'
import sys
import ssl
import sqlite3
import ctypes
print(sys.version)
print("smoke env ok")
PY
```

Output:

```text
3.11.15 | packaged by conda-forge | (main, Jun 11 2026, 03:24:48) [GCC 14.3.0]
smoke env ok
```

This proved that:

- Conda environment creation worked.
- A different Python version could be installed.
- The environment's Python executable could run.
- Important standard libraries and compiled modules loaded successfully.

---

## 19. NumPy Environment Creation

The next test created a real scientific Python environment:

```bash
conda-glibc create -y -n np311 python=3.11 numpy
```

Conda resolved and installed a full aarch64 scientific stack including packages such as:

```text
libblas
libcblas
libgfortran
libgfortran5
liblapack
libopenblas
numpy
python_abi
```

The plan showed:

```text
numpy-2.4.6
python-3.11.15
libopenblas-0.3.33
```

The transaction completed successfully.

The exit code was:

```text
numpy_create_exit=0
```

The new environment was patched:

```bash
patch-conda-glibc "$HOME/miniforge3-glibc/envs/np311"
```

Output:

```text
[patch-conda-glibc] scanning /data/data/com.termux/files/home/miniforge3-glibc/envs/np311
```

---

## 20. NumPy Runtime Validation

Input:

```bash
run-conda-glibc np311 python - <<'PY'
import numpy as np
print(np.__version__)
print(np.arange(5) ** 2)
print("numpy ok")
PY
```

Output:

```text
2.4.6
[ 0  1  4  9 16]
numpy ok
```

This was the strongest practical validation in the experiment.

It proved that:

- Conda could create an environment.
- Conda could install compiled `linux-aarch64` packages.
- BLAS/OpenBLAS dependencies were installable.
- NumPy could import successfully.
- NumPy could execute actual array operations successfully.

---

## 21. SafetyError Investigation

During both the `smoke` and `np311` environment creation, Conda printed many `SafetyError` warnings.

Examples:

```text
SafetyError: The package for tk located at
/data/data/com.termux/files/home/miniforge3-glibc/pkgs/tk-8.6.13-noxft_h0dc03b3_103
appears to be corrupted.

The path 'lib/thread2.8.8/libthread2.8.8.so'
has an incorrect size.

reported size: 145120 bytes
actual size: 330873 bytes
```

Readline example:

```text
SafetyError: The package for readline located at
/data/data/com.termux/files/home/miniforge3-glibc/pkgs/readline-8.3-hb682ff5_0
appears to be corrupted.

The path 'lib/libreadline.so.8.3'
has an incorrect size.

reported size: 540864 bytes
actual size: 739809 bytes
```

More examples were seen for:

```text
libgomp
libzlib
zstd
ld_impl_linux-aarch64
libgcc
bzip2
libffi
liblzma
libstdcxx
ncurses
tk
readline
```

Despite the warnings:

```text
Executing transaction: done
```

and exit codes were zero.

The root cause was identified as the patching workflow itself.

The previous `patch-conda-glibc` implementation had patched the Conda package cache under:

```text
$HOME/miniforge3-glibc/pkgs
```

Using `patchelf` changed the file sizes.

Conda package metadata still contained the original package file sizes, so Conda compared:

```text
reported size
```

against the modified:

```text
actual size
```

and emitted `SafetyError`.

Therefore:

> The packages were not necessarily corrupted during download. The extracted package cache had been modified after extraction by the ELF patching process.

---

## 22. Package Cache Policy

A new rule was established:

> Never patch Conda package cache directories.

The patcher must skip:

```text
$MF_PREFIX/pkgs/*
$HOME/.conda/pkgs/*
```

Only installed prefixes should be patched:

```text
$HOME/miniforge3-glibc
$HOME/miniforge3-glibc/envs/<env-name>
```

The recommended cleanup for already modified extracted package caches was:

```bash
for cache in "$HOME/miniforge3-glibc/pkgs" "$HOME/.conda/pkgs"; do
  [ -d "$cache" ] || continue

  find "$cache" -mindepth 1 -maxdepth 1 -type d | while IFS= read -r d; do
    base="$(basename "$d")"

    [ "$base" = "cache" ] && continue

    echo "remove extracted package cache: $d"
    rm -rf "$d"
  done
done
```

The intent is to remove extracted package directories that were modified, while preserving package archives where possible.

---

## 23. Final Runtime Rules

By the end of the experiment, the working rules were:

### Rule 1: Clear Termux preload state

Before running glibc Miniforge programs:

```bash
unset LD_PRELOAD
unset LD_LIBRARY_PATH
```

This is critical because the Termux preload library:

```text
/data/data/com.termux/files/usr/lib/libtermux-exec-ld-preload.so
```

must not be injected into the glibc process.

### Rule 2: Use the Termux glibc loader explicitly

For `aarch64`:

```text
$PREFIX/glibc/lib/ld-linux-aarch64.so.1
```

### Rule 3: Use a controlled runtime library path

The preferred order is conceptually:

```text
runtime shim
environment lib
environment lib64
base Miniforge lib
base Miniforge lib64
```

### Rule 4: Patch installed environments after package changes

After:

```bash
conda-glibc create ...
```

or:

```bash
mamba-glibc create ...
```

or after installing new binary packages, patch the installed environment prefix:

```bash
patch-conda-glibc "$HOME/miniforge3-glibc/envs/<env-name>"
```

### Rule 5: Never patch Conda package caches

Do not patch:

```text
*/pkgs/*
```

### Rule 6: Prefer explicit environment runners over global activation

The validated execution model was:

```bash
run-conda-glibc <env-name> <program> [args...]
```

Example:

```bash
run-conda-glibc np311 python -c "import numpy as np; print(np.arange(5))"
```

---

## 24. Conda Activation Decision

The experiment did not require `conda init`.

The chosen design avoided making the glibc Miniforge stack the default shell runtime because the normal Termux shell environment contains native Termux/Bionic assumptions.

In particular, simple global activation can reintroduce issues involving:

- `LD_PRELOAD`
- `LD_LIBRARY_PATH`
- direct ELF execution without the intended loader
- native Termux vs glibc library mixing

Therefore the preferred model before the PyMOL phase was:

```text
conda-glibc
mamba-glibc
python-glibc
patch-conda-glibc
run-conda-glibc
```

rather than:

```text
conda init
conda activate
```

The experiment did not establish that activation is impossible. Instead, it established that explicit wrappers were safer and already sufficient for successful environment creation and runtime execution.

---

## 25. Mamba Status

Mamba was validated at the executable level.

Input:

```bash
mamba-glibc --version
```

Output:

```text
2.5.0
```

This confirmed that the Mamba executable itself was operational in the Termux glibc Miniforge environment.

The same workflow principles apply:

```bash
mamba-glibc create -y -n <env> ...
patch-conda-glibc "$HOME/miniforge3-glibc/envs/<env>"
run-conda-glibc <env> <program> ...
```

A full package installation benchmark using Mamba was not yet completed in the recorded experiment before the PyMOL phase, but the executable itself was confirmed working.

---

## 26. Known Remaining Issue: Conda Child-Process Traceback

The main unresolved issue before the PyMOL phase was the non-fatal traceback:

```text
OSError: [Errno 40] Too many levels of symbolic links
```

from:

```text
multiprocessing.spawn
multiprocessing.synchronize.SemLock._rebuild
```

The issue appeared during Conda operations such as metadata collection or `conda info`.

It persisted with:

```bash
conda-glibc --no-plugins info
```

and also after switching to the classic solver.

However:

```bash
conda-glibc info
echo "exit=$?"
```

returned:

```text
exit=0
```

and both environment creation tests completed with exit code zero.

Also, the direct multiprocessing semaphore test succeeded:

```text
start method: fork
multiprocessing semaphore ok
```

Therefore the working conclusion was:

> A specific spawned auxiliary Conda child process remains incompatible or misconfigured, but this did not prevent Conda from completing tested `info` and `create` operations.

This should be investigated later if it becomes functionally relevant, but it did not block the successful creation and execution of tested environments.

---

## 27. Validated Results

The following results were directly validated.

### Base Miniforge Python

```text
Python 3.13.13
```

### Base Python imports

```text
ssl            OK
sqlite3        OK
ctypes         OK
hashlib        OK
zlib           OK
```

### Mamba

```text
mamba 2.5.0
```

### Conda

```text
conda 26.3.2
platform linux-aarch64
base environment writable
```

### Conda exit status

```text
conda-glibc info -> exit 0
```

### Python 3.11 environment

```text
3.11.15 | packaged by conda-forge | ... [GCC 14.3.0]
smoke env ok
```

### NumPy environment

```text
NumPy 2.4.6
[ 0  1  4  9 16]
numpy ok
```

---

## 28. Final Assessment Before the PyMOL Phase

The pre-PyMOL Miniforge experiment was successful.

The experiment demonstrated that a Termux `aarch64` host can operate a practical Miniforge/Conda stack through the Termux glibc runtime without moving the entire workflow into `proot-distro`.

The working architecture is:

```text
Android
└── Termux native shell
    ├── Termux glibc runtime
    │   └── ld-linux-aarch64.so.1
    ├── runtime shim
    │   └── ELF-only glibc runtime links
    ├── Miniforge base
    │   ├── Python 3.13
    │   ├── Conda 26.3.2
    │   └── Mamba 2.5.0
    └── Conda environments
        ├── smoke
        │   └── Python 3.11.15
        └── np311
            ├── Python 3.11
            ├── NumPy 2.4.6
            └── OpenBLAS/Fortran dependencies
```

The key compatibility requirements are:

```text
1. unset LD_PRELOAD
2. unset LD_LIBRARY_PATH
3. use the Termux glibc loader explicitly
4. use the runtime shim
5. patch installed prefixes after package changes
6. never patch Conda package caches
7. execute through controlled wrappers
```

The experiment therefore reached the point where the Miniforge runtime itself was no longer the main unknown.

The next phase could move on to the actual application target:

```text
PyMOL GUI
+
Conda package selection
+
Qt/OpenGL/X11 dependencies
+
Termux:X11 integration
+
application launcher / desktop shortcut
```

That next phase is intentionally outside the scope of this report.

---

## Appendix A. Core Wrapper Model

### `python-glibc`

Conceptual behavior:

```bash
unset LD_PRELOAD
unset LD_LIBRARY_PATH

exec "$PREFIX/glibc/lib/ld-linux-aarch64.so.1" \
  --library-path \
  "$HOME/.local/lib/termux-glibc-runtime:$HOME/miniforge3-glibc/lib:$HOME/miniforge3-glibc/lib64" \
  "$HOME/miniforge3-glibc/bin/python" "$@"
```

### `conda-glibc`

Conceptual behavior:

```bash
unset LD_PRELOAD
unset LD_LIBRARY_PATH

export CONDA_OVERRIDE_GLIBC="${CONDA_OVERRIDE_GLIBC:-2.17}"
export CONDA_SUBDIR="${CONDA_SUBDIR:-linux-aarch64}"
export CONDA_SOLVER="${CONDA_SOLVER:-classic}"

exec "$PREFIX/glibc/lib/ld-linux-aarch64.so.1" \
  --library-path \
  "$HOME/.local/lib/termux-glibc-runtime:$HOME/miniforge3-glibc/lib:$HOME/miniforge3-glibc/lib64" \
  "$HOME/miniforge3-glibc/bin/python" -m conda "$@"
```

### `run-conda-glibc`

Conceptual behavior:

```bash
ENV_NAME="$1"
PROGRAM="$2"

MF_PREFIX="$HOME/miniforge3-glibc"
ENV_PREFIX="$MF_PREFIX/envs/$ENV_NAME"
RUNTIME_DIR="$HOME/.local/lib/termux-glibc-runtime"
GLIBC_LD="$PREFIX/glibc/lib/ld-linux-aarch64.so.1"

unset LD_PRELOAD
unset LD_LIBRARY_PATH

exec "$GLIBC_LD" \
  --library-path \
  "$RUNTIME_DIR:$ENV_PREFIX/lib:$ENV_PREFIX/lib64:$MF_PREFIX/lib:$MF_PREFIX/lib64" \
  "$ENV_PREFIX/bin/$PROGRAM" "${@:3}"
```

---

## Appendix B. Final Minimal Validation Sequence

```bash
export PATH="$HOME/.local/bin:$PATH"

python-glibc --version

mamba-glibc --version

conda-glibc info
echo "exit=$?"

conda-glibc create -y -n smoke python=3.11
echo "create_exit=$?"

patch-conda-glibc \
  "$HOME/miniforge3-glibc/envs/smoke"

run-conda-glibc smoke python - <<'PY'
import sys
import ssl
import sqlite3
import ctypes
print(sys.version)
print("smoke env ok")
PY

conda-glibc create -y -n np311 python=3.11 numpy
echo "numpy_create_exit=$?"

patch-conda-glibc \
  "$HOME/miniforge3-glibc/envs/np311"

run-conda-glibc np311 python - <<'PY'
import numpy as np
print(np.__version__)
print(np.arange(5) ** 2)
print("numpy ok")
PY
```

Observed final NumPy result:

```text
2.4.6
[ 0  1  4  9 16]
numpy ok
```

---

## Appendix C. Important Failure Signatures

### Incorrect RPATH / linker script loaded as runtime library

```text
error while loading shared libraries:
.../glibc/lib/libc.so:
invalid ELF header
```

### Termux native preload injected into glibc runtime

```text
.../termux-glibc-runtime/libc.so.6:
version `LIBC' not found
(required by .../libtermux-exec-ld-preload.so)
```

### Non-fatal Conda auxiliary multiprocessing issue

```text
OSError: [Errno 40] Too many levels of symbolic links
```

### Patched Conda package cache detected by size verification

```text
SafetyError:
reported size: ...
actual size: ...
```

The correct response to the last category is not to keep patching the cache. The package cache must remain unmodified, while installed prefixes and environment prefixes are patched separately.
