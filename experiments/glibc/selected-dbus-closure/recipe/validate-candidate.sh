#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

CANDIDATE=${CANDIDATE:?set CANDIDATE to a materialized selected D-Bus candidate directory}

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
EXPERIMENT_DIR=$(cd -- "$SCRIPT_DIR/.." && pwd)
WORK_DIR=${WORK_DIR:-$EXPERIMENT_DIR/work}
PROBE=${PROBE:-$WORK_DIR/dbus-version-probe}
LOADER=${LOADER:-$PREFIX/glibc/lib/ld-linux-aarch64.so.1}
ROOTFS=${ROOTFS:-$PREFIX/var/lib/proot-distro/containers/debian/rootfs}
OUT=${OUT:-$PREFIX/tmp/selected-dbus-candidate-validation-$(date +%Y%m%d-%H%M%S)}
HOLD_SECONDS=${HOLD_SECONDS:-20}

RECEIPT="$CANDIDATE/receipt.tsv"
WORLD="$CANDIDATE/meta/world-substrate.tsv"

[ -d "$CANDIDATE/lib" ] || { printf 'missing candidate lib directory\n' >&2; exit 1; }
[ -f "$RECEIPT" ] || { printf 'missing candidate receipt\n' >&2; exit 1; }
[ -f "$WORLD" ] || { printf 'missing world substrate snapshot\n' >&2; exit 1; }
[ -x "$LOADER" ] || { printf 'missing loader: %s\n' "$LOADER" >&2; exit 1; }

[ -x "$PROBE" ] || "$SCRIPT_DIR/build-probe.sh"

mkdir -p "$OUT"

build_id_of() {
    readelf -n "$1" 2>/dev/null \
        | awk '
            /Build ID:/ && id == "" { id = $3 }
            END { if (id != "") print id }
        '
}

LIBRARY_PATH="$CANDIDATE/lib:$PREFIX/glibc/lib"

printf 'candidate: %s\n' "$CANDIDATE" | tee "$OUT/candidate.txt"
printf 'library path: %s\n' "$LIBRARY_PATH" | tee "$OUT/library-path.txt"

printf '\n===== candidate relocation check =====\n'
env \
    LD_PRELOAD= \
    LD_LIBRARY_PATH="$LIBRARY_PATH" \
    "$PREFIX/glibc/bin/ldd" -r "$PROBE" \
    >"$OUT/candidate-ldd.txt" 2>&1
cat "$OUT/candidate-ldd.txt"

if grep -q 'undefined symbol:' "$OUT/candidate-ldd.txt"; then
    printf 'candidate relocation: FAIL\n' >&2
    exit 1
fi

printf '\n===== start candidate probe =====\n'

DBUS_PROBE_HOLD_SECONDS=$HOLD_SECONDS \
LD_DEBUG=libs,files \
LD_PRELOAD= \
"$LOADER" \
    --library-path "$LIBRARY_PATH" \
    "$PROBE" \
    >"$OUT/probe.stdout" \
    2>"$OUT/loader-debug.log" &
PROBE_PID=$!

printf '%s\n' "$PROBE_PID" >"$OUT/probe.pid"
printf 'pid: %s\n' "$PROBE_PID"

for _ in $(seq 1 40); do
    if [ -r "/proc/$PROBE_PID/maps" ]; then
        break
    fi
    sleep 0.25
done

if [ ! -r "/proc/$PROBE_PID/maps" ]; then
    printf 'candidate probe maps unavailable\n' >&2
    wait "$PROBE_PID" || true
    exit 1
fi

cat "/proc/$PROBE_PID/maps" >"$OUT/maps.txt"

set +e
wait "$PROBE_PID"
status=$?
set -e
printf '%s\n' "$status" >"$OUT/probe.status"

[ "$status" -eq 0 ] || {
    printf 'candidate probe failed with status %s\n' "$status" >&2
    exit "$status"
}

printf '\n===== probe output =====\n'
cat "$OUT/probe.stdout"

awk '{print $NF}' "$OUT/maps.txt" \
    | grep -F "$CANDIDATE/lib/" \
    | sort -u \
    >"$OUT/mapped-candidate-paths.txt" || true

: >"$OUT/mapped-candidate-realpaths.txt"
while IFS= read -r path; do
    [ -n "$path" ] || continue
    readlink -f "$path"
done <"$OUT/mapped-candidate-paths.txt" \
    | sort -u \
    >"$OUT/mapped-candidate-realpaths.txt"

printf '\n===== mapped candidate objects =====\n'
cat "$OUT/mapped-candidate-realpaths.txt"

printf '\n===== provider leakage check =====\n'
if grep -F "$HOME/gl/lib/" "$OUT/maps.txt" >"$OUT/leaked-farm-maps.txt"; then
    cat "$OUT/leaked-farm-maps.txt" >&2
    printf 'candidate validation: FAIL (broad-farm object mapped)\n' >&2
    exit 1
fi

if grep -F "$ROOTFS/" "$OUT/maps.txt" >"$OUT/leaked-rootfs-maps.txt"; then
    cat "$OUT/leaked-rootfs-maps.txt" >&2
    printf 'candidate validation: FAIL (rootfs provider object mapped)\n' >&2
    exit 1
fi

printf 'no broad-farm/rootfs provider leakage: PASS\n'

printf '\n===== candidate receipt verification =====\n'
: >"$OUT/expected-candidate-realpaths.txt"

while IFS=$'\t' read -r source package version source_sha source_build soname candidate_file candidate_sha candidate_build; do
    [ "$source" = source_path ] && continue
    [ -n "$candidate_file" ] || continue

    file="$CANDIDATE/$candidate_file"
    [ -f "$file" ] || {
        printf 'missing candidate file from receipt: %s\n' "$file" >&2
        exit 1
    }

    actual_sha=$(sha256sum "$file" | awk '{print $1}')
    [ "$actual_sha" = "$candidate_sha" ] || {
        printf 'candidate hash drift: %s\n' "$file" >&2
        exit 1
    }

    actual_build=$(build_id_of "$file")
    [ -n "$actual_build" ] || actual_build=NONE
    [ "$actual_build" = "$candidate_build" ] || {
        printf 'candidate Build ID drift: %s\n' "$file" >&2
        exit 1
    }

    real=$(readlink -f "$file")
    printf '%s\n' "$real" >>"$OUT/expected-candidate-realpaths.txt"

    grep -Fxq "$real" "$OUT/mapped-candidate-realpaths.txt" || {
        printf 'receipt provider was not actually mapped: %s\n' "$real" >&2
        exit 1
    }

done <"$RECEIPT"

sort -u "$OUT/expected-candidate-realpaths.txt" -o "$OUT/expected-candidate-realpaths.txt"

if ! diff -u \
    "$OUT/expected-candidate-realpaths.txt" \
    "$OUT/mapped-candidate-realpaths.txt" \
    >"$OUT/candidate-map-set.diff"; then
    cat "$OUT/candidate-map-set.diff" >&2
    printf 'candidate validation: FAIL (mapped candidate set differs from receipt)\n' >&2
    exit 1
fi

printf 'candidate receipt/map equality: PASS\n'

printf '\n===== protected world mapping check =====\n'
awk '{print $NF}' "$OUT/maps.txt" \
    | grep -F "$PREFIX/glibc/lib/" \
    | sort -u \
    >"$OUT/mapped-prefix-paths.txt" || true

awk -F $'\t' 'NR > 1 { print $1 }' "$WORLD" \
    | sort -u \
    >"$OUT/allowed-world-paths.txt"

while IFS= read -r path; do
    [ -n "$path" ] || continue
    grep -Fxq "$path" "$OUT/allowed-world-paths.txt" || {
        printf 'unexpected prefix object mapped outside protected world set: %s\n' "$path" >&2
        exit 1
    }
done <"$OUT/mapped-prefix-paths.txt"

printf 'mapped prefix objects are within protected world set: PASS\n'

printf '\n===== actual selected provider proof =====\n'
printf 'candidate providers mapped from candidate bytes only\n'
printf 'protected world objects mapped from substrate whitelist only\n'
printf 'no broad-farm or rootfs provider mapping observed\n'

printf '\ncandidate validation: PASS\n'
printf 'evidence: %s\n' "$OUT"
