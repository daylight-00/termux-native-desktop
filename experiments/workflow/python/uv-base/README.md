# Persistent uv-managed base environment

**Status:** passed  
**Provenance:** first-hand session report (`report.md`)

## Question

Can an existing standalone CPython runtime back a persistent user-level environment that plays the practical role of Conda `base`, while leaving the system Python untouched and keeping dependency state declarative?

## Design

```text
existing standalone CPython 3.14.6
        |
        | uv venv --no-python-downloads -p <python>
        v
~/uv-base/.venv
        |
        +-- default interactive Python through PATH precedence
        |
        +-- managed by ~/uv-base/pyproject.toml + uv.lock
```

## Result

Passed. The experiment verified:

- no replacement or removal of the system Python;
- explicit use of the existing CPython 3.14.6 runtime;
- no automatic Python download by uv;
- persistent project metadata and lock state;
- dependency management through uv project semantics;
- default interactive Python selection through shell PATH precedence;
- continued support for separate per-project uv environments.

## Boundary

This is a workstation workflow experiment, not the CPython Android adaptation project itself. The interpreter source can come from the companion `cpython-android-cli` work, while this record remains here because the question is how the completed workstation should expose a default user Python environment.

See [`report.md`](report.md).
