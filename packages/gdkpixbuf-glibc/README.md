# GdkPixbuf glibc provider build

This package owns the repository definition for producing the bounded
GdkPixbuf glibc provider candidate.

## Build-tool boundary

Python build tooling is managed by uv:

```text
packages/gdkpixbuf-glibc/build-env/pyproject.toml
packages/gdkpixbuf-glibc/build-env/uv.lock
```

The generated environment is disposable and must live below the transaction
scratch root, not in the repository and not in a global Python environment.
The runner syncs it with the installed Android CPython runtime:

```bash
UV_PROJECT_ENVIRONMENT="$scratch/build-venv" \
uv --project packages/gdkpixbuf-glibc/build-env \
  sync --locked --no-python-downloads \
  --python "$HOME/opt/cpython-3.14/prefix/bin/python3.14"
```

Meson is a pure-Python locked dependency. Ninja remains a native Termux host
command because the PyPI Ninja distributions carry platform executables and
are not the authority for the Bionic host. CMake is not required for the
GdkPixbuf build and is therefore not part of this environment.

The compilers, linker, archiver, pkg-config and produced binaries remain in
the explicit Termux glibc toolchain boundary. Managing Meson with uv does not
change target ABI authority.
