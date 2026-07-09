# Native disposable personal base environment.
export PYBIN="$HOME/opt/cpython-3.14/prefix/bin/python3.14"
export UV_PYTHON="$PYBIN"
export UV_PYTHON_DOWNLOADS=never
export UV_BASE="$HOME/uv-base"

uva() {
    uv --project "$UV_BASE" add "$@"
}

uvr() {
    uv --project "$UV_BASE" remove "$@"
}

uvs() {
    uv --project "$UV_BASE" \
        sync \
        --locked \
        --no-python-downloads \
        --python "$PYBIN"
}
