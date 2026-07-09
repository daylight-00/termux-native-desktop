# uv-base module

`uv-base` is the native disposable personal base environment of the workstation.

It provides:

```text
default interactive Python
+
curated common Python libraries
+
selected PyPI-distributed console tools
```

The durable definition is tracked:

```text
$HOME/uv-base/pyproject.toml
$HOME/uv-base/uv.lock
```

The generated environment is disposable:

```text
$HOME/uv-base/.venv
```

The module consumes the installed custom Android CPython runtime described by `packages/cpython-android-runtime/`. It does not own the CPython build or artifact archive.

`uv-base` coexists with isolated uv tools, `uvx`, project-local uv environments, and the separate future glibc Conda ecosystem.
