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

## Accepted bounded provider identity

The exact final object produced by the reviewed scratch transaction is:

```text
libgdk_pixbuf-2.0.so.0.4200.12
SHA-256 0c1404c6854e7674428a5b653b240759dac0374631697fe61ae275898f6a809f
DT_SONAME libgdk_pixbuf-2.0.so.0
```

Its bounded provider decision is in `docs/evidence/gdkpixbuf-2-42-12-provider-candidate-result-review.md`. The accepted identity includes the documented post-link removal of one build-tree search-path tag. Rebuilding, updating, or materializing it requires re-review of source, build environment, options, final digest, dependency set, functional matrix and rollback boundary.

The decision does not accept provider authority for GLib, libpng, libmount or libblkid.
