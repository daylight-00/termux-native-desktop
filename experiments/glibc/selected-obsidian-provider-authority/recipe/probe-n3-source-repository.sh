#!/data/data/com.termux/files/usr/bin/bash
set -u

SOURCE_REPO=${SOURCE_REPO:-$HOME/Downloads/termux-pacman-glibc-packages-source}

printf 'SOURCE_REPOSITORY_PROBE=BEGIN\n'
printf 'SOURCE_REPO=%s\n' "$SOURCE_REPO"

if [ ! -e "$SOURCE_REPO" ]; then
    printf 'SOURCE_PATH_STATE=MISSING\n'
    printf 'SOURCE_REPOSITORY_PROBE=INVALID\n'
    exit 1
fi

if [ -d "$SOURCE_REPO" ]; then
    printf 'SOURCE_PATH_STATE=DIRECTORY\n'
elif [ -L "$SOURCE_REPO" ]; then
    printf 'SOURCE_PATH_STATE=SYMLINK\n'
else
    printf 'SOURCE_PATH_STATE=OTHER\n'
fi

if [ -d "$SOURCE_REPO/.git" ]; then
    printf 'GIT_MARKER_TYPE=DIRECTORY\n'
elif [ -f "$SOURCE_REPO/.git" ]; then
    printf 'GIT_MARKER_TYPE=FILE\n'
    IFS= read -r gitfile_line < "$SOURCE_REPO/.git" || gitfile_line='UNREADABLE'
    printf 'GITFILE_FIRST_LINE=%s\n' "$gitfile_line"
elif [ -L "$SOURCE_REPO/.git" ]; then
    printf 'GIT_MARKER_TYPE=SYMLINK\n'
else
    printf 'GIT_MARKER_TYPE=MISSING_OR_OTHER\n'
fi

probe_git() {
    local label=$1
    shift
    local stdout_file stderr_file rc
    stdout_file=$(mktemp)
    stderr_file=$(mktemp)
    git -C "$SOURCE_REPO" "$@" >"$stdout_file" 2>"$stderr_file"
    rc=$?
    printf '%s_RC=%s\n' "$label" "$rc"
    if [ -s "$stdout_file" ]; then
        while IFS= read -r line; do
            printf '%s_STDOUT=%s\n' "$label" "$line"
        done < "$stdout_file"
    fi
    if [ -s "$stderr_file" ]; then
        while IFS= read -r line; do
            printf '%s_STDERR=%s\n' "$label" "$line"
        done < "$stderr_file"
    fi
    rm -f "$stdout_file" "$stderr_file"
    return "$rc"
}

valid=true
probe_git REV_PARSE_GIT_DIR rev-parse --absolute-git-dir || valid=false
probe_git REV_PARSE_TOPLEVEL rev-parse --show-toplevel || valid=false
probe_git REV_PARSE_HEAD rev-parse --verify HEAD || valid=false
probe_git REV_PARSE_BARE rev-parse --is-bare-repository || valid=false
probe_git REV_PARSE_SHALLOW rev-parse --is-shallow-repository || valid=false
probe_git STATUS status --porcelain --untracked-files=all || valid=false
probe_git REMOTES remote -v || true

if [ "$valid" = true ]; then
    printf 'SOURCE_REPOSITORY_PROBE=VALID_GIT_CHECKOUT\n'
    exit 0
fi

printf 'SOURCE_REPOSITORY_PROBE=INVALID_GIT_CHECKOUT\n'
exit 1
