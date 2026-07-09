# Persistent uv-managed base environment

**Status:** passed; promoted as the `uv-base` module  
**Provenance:** first-hand session report (`report.md`)

## Question

Can an existing standalone CPython runtime back a persistent user-level environment that plays the practical role of Conda `base`, while leaving the system Python untouched and keeping dependency state declarative?

## Design

```text
existing standalone CPython 3.14.6
        |
        | explicit uv interpreter selection
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

The currently captured base definition has an empty dependency list. This is the accepted baseline state: environment mechanism, interpreter substrate, lock identity, rebuild model, and shell exposure are established before selecting additional base packages.

## Promotion

Current owners:

```text
modules/uv-base/
    project definition
    lockfile
    shell integration
    sync/reset hooks
    validation

modules/shell/
    thin Bash bootstrap
    generic interactive behavior
    final PATH composition

packages/cpython-android-runtime/
    consumer-side CPython artifact/runtime identity
```

The legacy `~/uv-base/.uvrc` is retired during hash-guarded adoption because it is shell integration rather than uv-native project configuration.

## Boundary

This is a workstation workflow experiment, not the CPython Android adaptation project itself. The interpreter source comes from the companion `cpython-android-cli` work, while this record remains here because the question is how the completed workstation should expose a default native personal environment.

`uv-base` is complementary to isolated uv tools, `uvx`, project-local uv environments, and the separate glibc Conda ecosystem.

See [`report.md`](report.md).
