# Final interactive command precedence policy.
# Capability fragments declare paths and behavior; this fragment composes them.

_path_managed_gl=${GL_BIN:-"$HOME/gl/bin"}
_path_managed_uv=${UV_BASE:-"$HOME/uv-base"}/.venv/bin
_path_managed_local="$HOME/.local/bin"

_path_rest=
_path_old_ifs=$IFS
IFS=:
for _path_entry in $PATH; do
    [ -n "$_path_entry" ] || continue
    case "$_path_entry" in
        "$_path_managed_gl"|"$_path_managed_uv"|"$_path_managed_local")
            continue
            ;;
    esac
    case ":$_path_rest:" in
        *":$_path_entry:"*) ;;
        *) _path_rest=${_path_rest:+"$_path_rest:"}$_path_entry ;;
    esac
done
IFS=$_path_old_ifs

_path_front=$_path_managed_gl
[ -d "$_path_managed_uv" ] && _path_front="$_path_front:$_path_managed_uv"
_path_front="$_path_front:$_path_managed_local"

PATH=$_path_front${_path_rest:+":$_path_rest"}
export PATH

unset _path_managed_gl _path_managed_uv _path_managed_local
unset _path_rest _path_old_ifs _path_entry _path_front
