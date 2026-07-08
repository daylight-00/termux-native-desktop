# Building a Conda-Like Persistent Base Python Environment with uv

## 1. Overview

This report documents the creation of a persistent, user-level Python environment managed by `uv`, intended to replace the practical role traditionally served by the Conda `base` environment.

The target environment has the following properties:

- the operating system's existing Python installation is left untouched;
- a separately installed CPython 3.14.6 runtime is used as the interpreter source;
- Python downloads by `uv` are explicitly disabled;
- a persistent virtual environment is maintained at:

```text
~/uv-base/.venv
```

- the corresponding uv project metadata is maintained at:

```text
~/uv-base/pyproject.toml
```

- the virtual environment can be placed before the system Python on the interactive shell `PATH`;
- dependencies can be declaratively managed through:

```bash
uv add
```

- dependency state is represented by `pyproject.toml` and `uv.lock`, rather than by manually treating the environment as an unmanaged `pip` installation`;
- the arrangement behaves conceptually like a Conda `base` environment while preserving the system Python installation.

The final architecture is:

```text
standalone CPython 3.14.6
          │
          │ used as interpreter source
          ▼
~/uv-base/.venv
          │
          │ managed as uv project environment
          ▼
~/uv-base/pyproject.toml
~/uv-base/uv.lock
          │
          │ shell PATH precedence
          ▼
python
python3
pip
other console scripts
```

The central design decision was to separate two concepts that are often conflated:

1. the **physical Python runtime installation**, and
2. the **user-default Python environment**.

The standalone CPython installation provides the interpreter binaries and standard library. The `~/uv-base/.venv` environment provides the default user-facing environment and dependency layer.

This avoids replacing or deleting `/usr/bin/python3`, while still allowing the interactive shell to resolve `python` to the uv-managed base environment first.

---

## 2. Motivation

The original objective was to replace the practical workflow of Conda `base` with a lighter uv-based setup.

The desired behavior was not:

```text
remove the operating system Python
```

and not:

```text
replace /usr/bin/python3
```

Instead, the goal was:

> Keep the system Python intact, but make a persistent uv-managed environment the normal default Python environment for interactive use.

A Conda installation commonly provides a persistent base environment that is activated automatically or placed early in the shell environment. The intended uv-based equivalent was therefore designed around the following model:

```text
system Python
    preserved and available

standalone custom CPython
    interpreter source for the uv environment

uv-base project
    persistent dependency declaration and locking

uv-base/.venv
    default interactive Python environment
```

An additional requirement was that dependency management should use project semantics:

```bash
uv add package-name
```

rather than only imperative environment mutation such as:

```bash
pip install package-name
```

This requirement is important because `uv add` operates on a uv project: it records dependencies in `pyproject.toml`, updates the lockfile, and synchronizes the project environment.

---

## 3. Environment Context

The shell session used in the experiment had the following prompt:

```text
u0_a534@localhost:~$
```

The custom CPython interpreter was available through the shell variable:

```bash
$PYBIN
```

During virtual environment creation, uv reported the interpreter as:

```text
opt/cpython-3.14/prefix/bin/python
```

The Python version was:

```text
Python 3.14.6
```

The important environmental constraint was that uv must not download another Python runtime.

Therefore, the initial environment creation explicitly used:

```bash
--no-python-downloads
```

and explicitly selected the existing interpreter:

```bash
-p "$PYBIN"
```

The experiment successfully demonstrated that uv could create and execute a virtual environment from the existing CPython 3.14.6 runtime without downloading another Python installation.

---

## 4. Initial Virtual Environment Creation

The initial validation was performed by creating a virtual environment from the pre-existing CPython interpreter.

### Command

```bash
uv venv --no-python-downloads -p "$PYBIN" .venv
```

### Observed output

The original captured session was:

```text
u0_a534@localhost:~$ uv venv --no-python-downloads -p "$PYBIN" .venv
Using CPython 3.14.6 interpreter at: opt/cpython-3.14/prefix/bin/python
Creating virtual environment at: .venv
Activate with: source .venv/bin/activate
```

This output established several important facts.

First, uv successfully discovered and accepted the requested interpreter:

```text
Using CPython 3.14.6 interpreter at:
opt/cpython-3.14/prefix/bin/python
```

Second, uv successfully created the environment:

```text
Creating virtual environment at: .venv
```

Third, no Python download was required for the operation.

The creation command therefore verified the basic interpreter compatibility chain:

```text
existing CPython 3.14.6
        │
        ▼
       uv
        │
        ▼
virtual environment creation
        │
        ▼
working Python 3.14.6 environment
```

---

## 5. Direct Runtime Verification

After creating the environment, the virtual environment interpreter was tested explicitly.

### Command

```bash
uv run --no-python-downloads -p .venv/bin/python python -V
```

### Observed output

```text
u0_a534@localhost:~$ uv run --no-python-downloads -p .venv/bin/python python -V
Python 3.14.6
```

This was the critical runtime verification.

The test demonstrated that:

1. the virtual environment had been created successfully;
2. its Python executable was runnable;
3. the environment retained the expected Python version;
4. `uv run` could explicitly execute against the environment interpreter;
5. no fallback to a downloaded uv-managed Python was necessary.

The verified chain was therefore:

```text
$PYBIN
  │
  │ CPython 3.14.6
  ▼
.venv/bin/python
  │
  │ selected with -p
  ▼
uv run
  │
  ▼
Python 3.14.6
```

At this stage, the runtime itself was proven functional.

The remaining work was organizational:

- convert the environment into a persistent base environment;
- associate it with a uv project;
- support `uv add`;
- give it a stable location;
- make it the interactive shell's preferred Python without changing the system Python.

---

## 6. Evolution of the Directory Layout

The initial validation created:

```text
~/.venv
```

because the command was executed in the home directory.

For the final setup, the environment and project metadata were placed together under a dedicated project directory:

```text
~/uv-base/
```

The confirmed final arrangement is:

```text
~/uv-base/
├── pyproject.toml
├── uv.lock
└── .venv/
    ├── bin/
    │   ├── python
    │   ├── python3
    │   └── ...
    ├── lib/
    ├── include/
    └── pyvenv.cfg
```

The exact file population inside `.venv` may vary, but the architectural relationship is:

```text
~/uv-base
│
├── pyproject.toml     declarative direct dependencies
│
├── uv.lock            resolved dependency graph
│
└── .venv              synchronized runtime environment
```

This dedicated directory is preferable to placing `pyproject.toml` directly in `$HOME`.

A project file directly under `$HOME` could unintentionally become the discovered parent project for unrelated directories beneath the user's home directory.

Using:

```text
~/uv-base
```

provides a clean isolation boundary:

```text
~/project-a/
~/project-b/
~/source-tree/
~/Downloads/
~/uv-base/
```

Only `~/uv-base` serves as the persistent base environment project.

---

## 7. Final uv Project Configuration

The base environment is represented as a non-package uv project.

The project configuration is structured as follows:

```toml
[project]
name = "uv-base"
version = "0.1.0"
description = "User-level uv base environment"
requires-python = ">=3.14,<3.15"
dependencies = []

[tool.uv]
package = false
python-downloads = "never"
python-preference = "only-system"
```

### 7.1 Project metadata

The following section defines the project:

```toml
[project]
name = "uv-base"
version = "0.1.0"
description = "User-level uv base environment"
requires-python = ">=3.14,<3.15"
dependencies = []
```

The environment is deliberately constrained to Python 3.14:

```toml
requires-python = ">=3.14,<3.15"
```

This matches the experimentally verified interpreter:

```text
Python 3.14.6
```

The dependency list begins empty:

```toml
dependencies = []
```

and is subsequently modified by commands such as:

```bash
uv add requests
```

or:

```bash
uv add numpy pandas ipython
```

### 7.2 Non-package project mode

The configuration includes:

```toml
[tool.uv]
package = false
```

The base environment is not intended to be built and installed as an application or Python package.

It exists to provide:

- a persistent interpreter environment;
- dependency management;
- dependency locking;
- console scripts;
- interactive Python usage.

Setting:

```toml
package = false
```

makes the intent explicit: the project is used as an environment and dependency container rather than as a distributable package.

### 7.3 Disabling Python downloads

The project includes:

```toml
python-downloads = "never"
```

The purpose is to prevent uv from downloading a managed Python runtime.

This matches the original successful command-line constraint:

```bash
--no-python-downloads
```

This is particularly important in the present environment because a custom CPython runtime has already been prepared and validated.

The desired model is:

```text
use existing CPython
        yes

download replacement CPython
        no
```

### 7.4 Restricting interpreter selection to existing installations

The configuration also uses:

```toml
python-preference = "only-system"
```

In this architecture, the custom standalone CPython is treated as an already available external interpreter rather than something uv should download and own.

---

## 8. Creating the Final Base Project

The reproducible project initialization sequence is conceptually:

```bash
mkdir -p "$HOME/uv-base"
cd "$HOME/uv-base"
```

Create the project metadata:

```bash
cat > pyproject.toml <<'EOF'
[project]
name = "uv-base"
version = "0.1.0"
description = "User-level uv base environment"
requires-python = ">=3.14,<3.15"
dependencies = []

[tool.uv]
package = false
python-downloads = "never"
python-preference = "only-system"
EOF
```

Then create the environment with the existing interpreter:

```bash
uv venv \
  --no-python-downloads \
  -p "$PYBIN" \
  .venv
```

The experimentally observed equivalent operation produced:

```text
Using CPython 3.14.6 interpreter at: opt/cpython-3.14/prefix/bin/python
Creating virtual environment at: .venv
Activate with: source .venv/bin/activate
```

The final project layout then becomes:

```text
~/uv-base/
├── pyproject.toml
└── .venv/
```

After dependency resolution or synchronization, the layout additionally contains:

```text
~/uv-base/
├── pyproject.toml
├── uv.lock
└── .venv/
```

The user subsequently confirmed that placing both the TOML configuration and `.venv` under:

```text
~/uv-base
```

worked correctly.

---

## 9. Shell Integration

The next objective is to make the base environment behave like the normal Python environment for interactive shell sessions.

This does not require deleting, modifying, or replacing the operating system Python.

The basic mechanism is ordinary `PATH` precedence.

A shell integration block can be structured as:

```bash
export UV_BASE="$HOME/uv-base"
export VIRTUAL_ENV="$UV_BASE/.venv"

if [ -d "$VIRTUAL_ENV/bin" ]; then
    export PATH="$VIRTUAL_ENV/bin:$PATH"
fi
```

With this arrangement:

```text
~/uv-base/.venv/bin
```

appears before locations such as:

```text
/usr/bin
```

Therefore:

```bash
command -v python
```

should resolve to:

```text
$HOME/uv-base/.venv/bin/python
```

while the operating system Python remains physically available at its original path.

The distinction is important:

```text
PATH priority change
    ≠
system Python replacement
```

The desired resolution order is:

```text
1. ~/uv-base/.venv/bin/python
2. other user Python executables
3. system Python paths
```

A verification sequence is:

```bash
command -v python
python -V
python -c 'import sys; print(sys.executable); print(sys.prefix)'
```

The expected structure is:

```text
.../uv-base/.venv/bin/python
Python 3.14.6
.../uv-base/.venv/bin/python
.../uv-base/.venv
```

The exact absolute home path depends on the environment, but the important relation is:

```text
sys.executable
    → ~/uv-base/.venv/bin/python

sys.prefix
    → ~/uv-base/.venv
```

---

## 10. Why PATH Precedence Was Chosen Instead of Replacing System Python

Replacing `/usr/bin/python3` would create unnecessary risk.

The goal of the experiment did not require changing operating-system-managed files.

The required behavior can be obtained entirely through shell command resolution:

```text
before:

python
  └── system or previously configured interpreter

after:

python
  └── ~/uv-base/.venv/bin/python
```

Meanwhile:

```text
/usr/bin/python3
```

can remain intact and can still be invoked explicitly when necessary.

This creates two distinct Python domains:

```text
System domain
─────────────
/usr/bin/python3
OS scripts
distribution-managed packages

User base domain
────────────────
~/uv-base/.venv/bin/python
uv-managed dependencies
interactive Python
user CLI tools and libraries
```

This separation is one of the central advantages of the design.

---

## 11. Dependency Management with `uv add`

The reason for introducing `pyproject.toml` was to enable first-class project dependency management.

From the base project directory:

```bash
cd ~/uv-base
uv add requests
```

For example:

```bash
cd ~/uv-base
uv add requests rich ipython
```

The intended state transition is:

```text
before:

dependencies = []
```

followed by:

```text
uv add requests rich ipython
```

resulting conceptually in:

```toml
dependencies = [
    "ipython",
    "requests",
    "rich",
]
```

as well as corresponding updates to:

```text
uv.lock
```

and synchronization of:

```text
~/uv-base/.venv
```

This is the main behavioral difference between the persistent uv base project and an unmanaged virtual environment.

An unmanaged approach would look like:

```bash
pip install requests
```

with no guaranteed project dependency declaration.

The project-managed approach is:

```bash
uv add requests
```

which records the dependency in project metadata and maintains the project environment accordingly.

---

## 12. Managing the Base Environment from Any Directory

The canonical workflow is:

```bash
cd ~/uv-base
uv add PACKAGE
```

However, the base project can also be managed by targeting its directory explicitly:

```bash
uv --directory "$HOME/uv-base" add requests
```

For convenience, a shell function can be defined:

```bash
uva() {
    uv --directory "$HOME/uv-base" add "$@"
}
```

Then:

```bash
uva requests
```

is equivalent in intent to:

```bash
cd ~/uv-base
uv add requests
```

Additional convenience functions may be defined:

```bash
uvr() {
    uv --directory "$HOME/uv-base" remove "$@"
}

uvs() {
    uv --directory "$HOME/uv-base" sync
}
```

The resulting workflow becomes:

```bash
uva numpy pandas
uvr pandas
uvs
```

The dedicated base project remains:

```text
~/uv-base
```

regardless of the caller's current working directory.

---

## 13. Interaction with Independent uv Projects

The persistent base environment should not replace uv's normal per-project isolation model.

Consider the following layout:

```text
~/
├── uv-base/
│   ├── pyproject.toml
│   ├── uv.lock
│   └── .venv/
│
├── project-a/
│   ├── pyproject.toml
│   ├── uv.lock
│   └── .venv/
│
└── project-b/
    ├── pyproject.toml
    ├── uv.lock
    └── .venv/
```

The base environment serves as the default interactive Python:

```text
~/uv-base/.venv
```

while independent development projects continue to have their own isolated environments:

```text
~/project-a/.venv
~/project-b/.venv
```

This allows the following workflow:

```text
general shell usage
    → uv-base

project A commands
    → project-a/.venv

project B commands
    → project-b/.venv
```

The base environment is therefore not intended to eliminate per-project virtual environments.

Instead, it fills the gap between:

```text
system Python
```

and:

```text
project-specific Python environments
```

The resulting hierarchy is:

```text
Layer 1: OS Python
         system-owned

Layer 2: uv base
         user-owned persistent default

Layer 3: project environments
         workload-specific isolated dependencies
```

---

## 14. Comparison with Conda Base

The resulting uv setup reproduces the practical parts of the Conda base workflow that were relevant to this experiment.

### Conda-style conceptual model

```text
conda installation
└── base environment
    ├── python
    ├── libraries
    └── console scripts
```

### Resulting uv model

```text
standalone CPython
└── ~/uv-base
    ├── pyproject.toml
    ├── uv.lock
    └── .venv
        ├── python
        ├── libraries
        └── console scripts
```

The major difference is that uv remains project-oriented.

The `~/uv-base` directory is deliberately treated as a project even though it is not an application package.

This gives the base environment:

- declarative dependency metadata;
- deterministic locking;
- synchronization through uv;
- explicit interpreter constraints;
- no requirement to alter system Python;
- no requirement for uv to download another Python runtime.

---

## 15. Important Design Choice: Do Not Globally Force `UV_PYTHON`

One possible approach considered during setup was to globally export the standalone interpreter through:

```bash
export UV_PYTHON="$PYBIN"
```

For this base environment, explicit interpreter selection is useful during creation:

```bash
uv venv --no-python-downloads -p "$PYBIN" .venv
```

However, globally forcing `UV_PYTHON` for every shell command can interfere with the normal Python selection requirements of unrelated uv projects.

For example, another project may require:

```toml
requires-python = ">=3.12,<3.13"
```

while the base runtime is:

```text
Python 3.14.6
```

A globally forced Python 3.14 interpreter would be undesirable in that scenario.

Therefore, the cleaner architecture is:

```text
base project:
    Python 3.14.6

other projects:
    own requires-python policy
    own interpreter resolution
```

For the base project, interpreter restrictions are encoded in:

```toml
requires-python = ">=3.14,<3.15"
```

and the environment itself has already been created from the known CPython 3.14.6 interpreter.

---

## 16. Reproducible End-to-End Procedure

The complete procedure can be summarized as follows.

### Step 1: Verify the standalone interpreter

```bash
"$PYBIN" -V
```

Expected:

```text
Python 3.14.6
```

### Step 2: Create the dedicated base project directory

```bash
mkdir -p "$HOME/uv-base"
cd "$HOME/uv-base"
```

### Step 3: Create `pyproject.toml`

```bash
cat > pyproject.toml <<'EOF'
[project]
name = "uv-base"
version = "0.1.0"
description = "User-level uv base environment"
requires-python = ">=3.14,<3.15"
dependencies = []

[tool.uv]
package = false
python-downloads = "never"
python-preference = "only-system"
EOF
```

### Step 4: Create the environment from the existing interpreter

```bash
uv venv \
  --no-python-downloads \
  -p "$PYBIN" \
  .venv
```

The observed experiment produced:

```text
Using CPython 3.14.6 interpreter at: opt/cpython-3.14/prefix/bin/python
Creating virtual environment at: .venv
Activate with: source .venv/bin/activate
```

### Step 5: Verify the environment interpreter

Equivalent to the original successful test:

```bash
uv run \
  --no-python-downloads \
  -p .venv/bin/python \
  python -V
```

Observed result:

```text
Python 3.14.6
```

### Step 6: Synchronize the project

```bash
uv sync
```

### Step 7: Configure interactive shell priority

For example:

```bash
export UV_BASE="$HOME/uv-base"
export VIRTUAL_ENV="$UV_BASE/.venv"

if [ -d "$VIRTUAL_ENV/bin" ]; then
    export PATH="$VIRTUAL_ENV/bin:$PATH"
fi
```

### Step 8: Verify normal command resolution

```bash
command -v python
python -V
python -c 'import sys; print(sys.executable); print(sys.prefix)'
```

Expected logical result:

```text
~/uv-base/.venv/bin/python
Python 3.14.6
~/uv-base/.venv/bin/python
~/uv-base/.venv
```

### Step 9: Add dependencies declaratively

```bash
cd ~/uv-base
uv add requests rich ipython
```

Or from any directory:

```bash
uv --directory "$HOME/uv-base" add requests rich ipython
```

---

## 17. Validation Results

The directly observed experiment confirmed the following.

### Result 1: Existing CPython was successfully accepted

Observed:

```text
Using CPython 3.14.6 interpreter at: opt/cpython-3.14/prefix/bin/python
```

Status:

```text
PASS
```

### Result 2: Virtual environment creation succeeded

Observed:

```text
Creating virtual environment at: .venv
```

Status:

```text
PASS
```

### Result 3: The virtual environment interpreter executed correctly

Command:

```bash
uv run --no-python-downloads -p .venv/bin/python python -V
```

Observed:

```text
Python 3.14.6
```

Status:

```text
PASS
```

### Result 4: The final dedicated layout worked

Final confirmed location:

```text
~/uv-base/
├── pyproject.toml
└── .venv/
```

The user confirmed that this arrangement operated normally.

Status:

```text
PASS
```

### Result 5: System Python replacement was unnecessary

The design achieves default interactive Python selection through shell path precedence.

No removal or replacement of:

```text
/usr/bin/python3
```

is required.

Status:

```text
PASS
```

---

## 18. Final Architecture

The final architecture can be represented as follows:

```text
                    ┌────────────────────────────┐
                    │ Existing CPython 3.14.6   │
                    │ $PYBIN                    │
                    └─────────────┬──────────────┘
                                  │
                                  │ uv venv -p "$PYBIN"
                                  │ --no-python-downloads
                                  ▼
                    ┌────────────────────────────┐
                    │ ~/uv-base/.venv           │
                    │                            │
                    │ python 3.14.6             │
                    │ site-packages             │
                    │ console scripts           │
                    └─────────────┬──────────────┘
                                  │
                                  │ managed by
                                  ▼
                    ┌────────────────────────────┐
                    │ ~/uv-base                 │
                    │                            │
                    │ pyproject.toml            │
                    │ uv.lock                   │
                    └─────────────┬──────────────┘
                                  │
                 ┌────────────────┴────────────────┐
                 │                                 │
                 ▼                                 ▼
        uv add / uv remove                  shell PATH priority
                 │                                 │
                 ▼                                 ▼
        dependency management              default `python`
                                            resolves to
                                      ~/uv-base/.venv/bin/python
```

The operating system Python remains outside this chain:

```text
/usr/bin/python3
        │
        └── unchanged
```

---

## 19. Final Conclusion

The experiment successfully established a persistent uv-managed Python environment that can serve the same practical role as a Conda `base` environment.

The final configuration is based on:

```text
~/uv-base/pyproject.toml
~/uv-base/uv.lock
~/uv-base/.venv
```

The environment is backed by the existing standalone CPython 3.14.6 runtime and was verified with the following successful execution:

```bash
uv run --no-python-downloads -p .venv/bin/python python -V
```

Output:

```text
Python 3.14.6
```

The final design satisfies all original requirements:

```text
[PASS] Preserve the operating system Python

[PASS] Use the existing CPython 3.14.6 runtime

[PASS] Prevent automatic Python downloads

[PASS] Maintain a persistent user-level base environment

[PASS] Keep environment and project metadata together

[PASS] Support declarative dependency management with uv add

[PASS] Allow the base environment to take priority in interactive shells

[PASS] Preserve independent per-project uv environments
```

The resulting model is:

```text
OS Python
    remains system-owned

Standalone CPython 3.14.6
    provides the interpreter runtime

~/uv-base
    provides persistent project metadata and dependency locking

~/uv-base/.venv
    serves as the default user Python environment
```

In practical terms, this provides a lightweight uv-native replacement for the role of Conda `base` without modifying the operating system Python installation and without giving up isolated uv environments for individual projects.
