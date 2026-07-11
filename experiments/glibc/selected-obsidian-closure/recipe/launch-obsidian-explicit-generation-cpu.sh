#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

GENERATION_DIR=${GENERATION_DIR:?set GENERATION_DIR to the explicit published generation}
VALIDATION_ROOT=${VALIDATION_ROOT:?set VALIDATION_ROOT to the receipt-local runtime root}
LAUNCH_RECEIPT_DIR=${LAUNCH_RECEIPT_DIR:?set LAUNCH_RECEIPT_DIR}
FONTCONFIG_FILE=${FONTCONFIG_FILE:?set FONTCONFIG_FILE}
XDG_CONFIG_HOME=${XDG_CONFIG_HOME:?set XDG_CONFIG_HOME}
XDG_CACHE_HOME=${XDG_CACHE_HOME:?set XDG_CACHE_HOME}
XDG_DATA_HOME=${XDG_DATA_HOME:?set XDG_DATA_HOME}
XDG_STATE_HOME=${XDG_STATE_HOME:?set XDG_STATE_HOME}
XDG_RUNTIME_DIR=${XDG_RUNTIME_DIR:?set XDG_RUNTIME_DIR}
TMPDIR=${TMPDIR:?set TMPDIR}

APP=${APP:-$HOME/gl/apps/obsidian}
APP_ENTRYPOINT=${APP_ENTRYPOINT:-$APP/obsidian}
WORLD_LIB=${WORLD_LIB:-$PREFIX/glibc/lib}
FONTCONFIG_PATH=${FONTCONFIG_FILE%/*}
CANDIDATE_LD_LIBRARY_PATH="$GENERATION_DIR/lib:$WORLD_LIB"

[ -d "$GENERATION_DIR" ] && [ ! -L "$GENERATION_DIR" ] || {
    printf 'explicit generation is not a plain directory: %s\n' "$GENERATION_DIR" >&2
    exit 1
}
[ -d "$GENERATION_DIR/lib" ] || {
    printf 'missing generation lib directory: %s\n' "$GENERATION_DIR/lib" >&2
    exit 1
}
[ -f "$GENERATION_DIR/share/glib-2.0/schemas/gschemas.compiled" ] || {
    printf 'missing generation schema aggregate\n' >&2
    exit 1
}
[ -d "$GENERATION_DIR/share/fonts/selected" ] || {
    printf 'missing generation font directory\n' >&2
    exit 1
}
[ -x "$APP_ENTRYPOINT" ] || {
    printf 'missing Obsidian entrypoint: %s\n' "$APP_ENTRYPOINT" >&2
    exit 1
}
[ -f "$FONTCONFIG_FILE" ] || {
    printf 'missing receipt-owned fontconfig file: %s\n' "$FONTCONFIG_FILE" >&2
    exit 1
}
[ -d "$LAUNCH_RECEIPT_DIR" ] || {
    printf 'missing launch receipt directory: %s\n' "$LAUNCH_RECEIPT_DIR" >&2
    exit 1
}

requested_generation_dir=$GENERATION_DIR
requested_validation_root=$VALIDATION_ROOT
requested_launch_receipt_dir=$LAUNCH_RECEIPT_DIR
requested_fontconfig_file=$FONTCONFIG_FILE
requested_fontconfig_path=$FONTCONFIG_PATH
requested_xdg_config_home=$XDG_CONFIG_HOME
requested_xdg_cache_home=$XDG_CACHE_HOME
requested_xdg_data_home=$XDG_DATA_HOME
requested_xdg_state_home=$XDG_STATE_HOME
requested_xdg_runtime_dir=$XDG_RUNTIME_DIR
requested_tmpdir=$TMPDIR
requested_candidate_ld_library_path=$CANDIDATE_LD_LIBRARY_PATH

source "$HOME/gl/env"

GENERATION_DIR=$requested_generation_dir
VALIDATION_ROOT=$requested_validation_root
LAUNCH_RECEIPT_DIR=$requested_launch_receipt_dir
FONTCONFIG_FILE=$requested_fontconfig_file
FONTCONFIG_PATH=$requested_fontconfig_path
XDG_CONFIG_HOME=$requested_xdg_config_home
XDG_CACHE_HOME=$requested_xdg_cache_home
XDG_DATA_HOME=$requested_xdg_data_home
XDG_STATE_HOME=$requested_xdg_state_home
XDG_RUNTIME_DIR=$requested_xdg_runtime_dir
TMPDIR=$requested_tmpdir
CANDIDATE_LD_LIBRARY_PATH=$requested_candidate_ld_library_path

unset \
    LD_LIBRARY_PATH \
    VK_ICD_FILENAMES \
    VK_DRIVER_FILES \
    VK_ADD_DRIVER_FILES \
    VK_LAYER_PATH \
    VK_INSTANCE_LAYERS \
    VK_LOADER_DEBUG \
    MESA_LOADER_DRIVER_OVERRIDE \
    GALLIUM_DRIVER \
    LIBGL_ALWAYS_SOFTWARE \
    LIBGL_DRIVERS_PATH \
    MESA_VK_WSI_PRESENT_MODE \
    MESA_DISK_CACHE_DATABASE \
    MESA_DISK_CACHE_SINGLE_FILE \
    GIO_EXTRA_MODULES \
    GTK_PATH \
    GTK_EXE_PREFIX \
    GTK_DATA_PREFIX \
    GDK_PIXBUF_MODULE_FILE \
    PANGO_RC_FILE

export APPDIR="$APP"
export PATH="$HOME/gl/shims:$APP:$APP/usr/sbin:$PATH"
export XDG_DATA_DIRS="$APP/usr/share:$GENERATION_DIR/share"
export GSETTINGS_SCHEMA_DIR="$GENERATION_DIR/share/glib-2.0/schemas"
export FONTCONFIG_PATH
export XDG_CONFIG_HOME XDG_CACHE_HOME XDG_DATA_HOME XDG_STATE_HOME XDG_RUNTIME_DIR
export TMPDIR
export TMP="$TMPDIR"
export TEMP="$TMPDIR"
export GL_GPU=0

current_reference=NO
case "$CANDIDATE_LD_LIBRARY_PATH:$GSETTINGS_SCHEMA_DIR:$FONTCONFIG_FILE" in
    *"/current"*) current_reference=YES ;;
esac

{
    printf 'field\tvalue\n'
    printf 'generation_dir\t%s\n' "$GENERATION_DIR"
    printf 'generation_lib\t%s\n' "$GENERATION_DIR/lib"
    printf 'generation_schema_dir\t%s\n' "$GSETTINGS_SCHEMA_DIR"
    printf 'generation_font_dir\t%s\n' "$GENERATION_DIR/share/fonts/selected"
    printf 'world_lib\t%s\n' "$WORLD_LIB"
    printf 'ld_library_path\t%s\n' "$CANDIDATE_LD_LIBRARY_PATH"
    printf 'launcher_shell_ld_library_path\tUNSET\n'
    printf 'candidate_loader_injection\tEXEC_ENV_ONLY\n'
    printf 'fontconfig_file\t%s\n' "$FONTCONFIG_FILE"
    printf 'fontconfig_path\t%s\n' "$FONTCONFIG_PATH"
    printf 'xdg_config_home\t%s\n' "$XDG_CONFIG_HOME"
    printf 'xdg_cache_home\t%s\n' "$XDG_CACHE_HOME"
    printf 'xdg_data_home\t%s\n' "$XDG_DATA_HOME"
    printf 'xdg_state_home\t%s\n' "$XDG_STATE_HOME"
    printf 'xdg_runtime_dir\t%s\n' "$XDG_RUNTIME_DIR"
    printf 'tmpdir\t%s\n' "$TMPDIR"
    printf 'xdg_data_dirs\t%s\n' "$XDG_DATA_DIRS"
    printf 'gl_gpu\t%s\n' "$GL_GPU"
    printf 'gpu_flags\t--disable-gpu\n'
    printf 'ld_preload_exec_value\tEMPTY\n'
    printf 'current_reference\t%s\n' "$current_reference"
} >"$LAUNCH_RECEIPT_DIR/launch-environment.tsv"

{
    printf '%s\n' "$APP_ENTRYPOINT"
    printf '%s\n' \
        --disable-dev-shm-usage \
        --ozone-platform=x11 \
        --disable-gpu
    printf '%s\n' "$@"
} >"$LAUNCH_RECEIPT_DIR/argv.txt"

exec env \
    LD_PRELOAD= \
    LD_LIBRARY_PATH="$CANDIDATE_LD_LIBRARY_PATH" \
    "$APP_ENTRYPOINT" \
    --disable-dev-shm-usage \
    --ozone-platform=x11 \
    --disable-gpu \
    "$@"
