#!/usr/bin/env bash
set -euo pipefail

REPO=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
COLLECTOR="$REPO/experiments/glibc/selected-obsidian-provider-authority/recipe/collect-generic-exact-candidate-evidence.py"
RUNNER="$REPO/experiments/glibc/selected-obsidian-provider-authority/recipe/run-generic-exact-candidate-evidence.sh"
TOKENS="$REPO/experiments/glibc/selected-obsidian-provider-authority/review/generic-exact-candidate-search-tokens.tsv"

fail() {
    printf 'generic exact candidate collector smoke: FAIL: %s\n' "$*" >&2
    exit 1
}

[ -x "$COLLECTOR" ] || fail "missing executable collector"
[ -x "$RUNNER" ] || fail "missing executable runner"
[ -f "$TOKENS" ] || fail "missing token contract"
[ "$(awk 'END {print NR-1}' "$TOKENS")" -eq 61 ] || fail "token denominator is not 61"
awk -F '\t' 'NR > 1 && ($9 != "SEARCH_ONLY_NOT_AUTHORITY" || $10 != "OPEN_NO_DEB_EXTRACTION" || $11 != "UNRESOLVED" || $13 != "BLOCKED") {exit 1}' "$TOKENS" || fail "token authority boundary drift"

python3 -m py_compile "$COLLECTOR"
bash -n "$RUNNER"

for forbidden in \
    '^[[:space:]]*(sudo[[:space:]]+)?apt[[:space:]]+(update|install|download|remove|upgrade|full-upgrade)' \
    '^[[:space:]]*pkg[[:space:]]+(install|upgrade)' \
    '^[[:space:]]*git[[:space:]]+(fetch|pull|clone)' \
    '^[[:space:]]*(curl|wget)[[:space:]]' \
    '^[[:space:]]*dpkg-deb[[:space:]]+(-x|--extract)' \
    '^[[:space:]]*ar[[:space:]]+x'; do
    if grep -E "$forbidden" "$RUNNER" >/dev/null; then
        fail "forbidden mutating/network shell command appears: $forbidden"
    fi
done
for forbidden_python in \
    '\["apt",[[:space:]]*"(update|install|download|remove|upgrade|full-upgrade)"' \
    '\["git",[[:space:]]*"(fetch|pull|clone)"' \
    '\["(curl|wget)"' \
    '\["dpkg-deb",[[:space:]]*"(-x|--extract)"'; do
    if grep -E "$forbidden_python" "$COLLECTOR" >/dev/null; then
        fail "forbidden mutating/network Python command appears: $forbidden_python"
    fi
done

TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
PREFIX_ROOT="$TMP/prefix"
SOURCE_ROOT="$TMP/source"
OUT="$TMP/out"
mkdir -p "$PREFIX_ROOT/etc/apt/sources.list.d" "$PREFIX_ROOT/var/lib/apt/lists" "$PREFIX_ROOT/var/cache/apt/archives" "$PREFIX_ROOT/var/lib/dpkg" "$SOURCE_ROOT"
printf 'deb https://example.invalid/apt/termux-glibc glibc stable\n' > "$PREFIX_ROOT/etc/apt/sources.list.d/glibc.list"
printf 'Status: synthetic\n' > "$PREFIX_ROOT/var/lib/dpkg/status"
cat > "$PREFIX_ROOT/var/lib/apt/lists/example.invalid_apt_termux-glibc_dists_glibc_stable_binary-aarch64_Packages" <<'EOF'
Package: nss-glibc
Version: 3.110
Architecture: aarch64
Filename: pool/n/nss-glibc_3.110_aarch64.deb
Size: 1234
SHA256: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
Description: NSS and NSPR security provider

Package: gtk3-glibc
Version: 3.24.49
Architecture: aarch64
Filename: pool/g/gtk3-glibc_3.24.49_aarch64.deb
Size: 2345
SHA256: bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb
Description: GTK GDK Pango ATK GUI provider

Package: mesa-vulkan-icd-freedreno-dri3
Version: 25.0.7
Architecture: aarch64
Filename: pool/m/mesa-vulkan-icd-freedreno-dri3_25.0.7_aarch64.deb
Size: 3456
SHA256: cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
Description: Mesa GBM Vulkan Freedreno provider

Package: alsa-lib-glibc
Version: 1.2.14
Architecture: aarch64
Filename: pool/a/alsa-lib-glibc_1.2.14_aarch64.deb
Size: 4567
SHA256: dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd
Description: ALSA asound provider

Package: libudev-zero-glibc
Version: 1.0.3
Architecture: aarch64
Filename: pool/l/libudev-zero-glibc_1.0.3_aarch64.deb
Size: 5678
SHA256: eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
Description: udev compatibility provider

Package: cups-glibc
Version: 2.4.10
Architecture: aarch64
Filename: pool/c/cups-glibc_2.4.10_aarch64.deb
Size: 6789
SHA256: ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
Description: CUPS printing provider with gnutls avahi
EOF

cd "$SOURCE_ROOT"
git init -q
git config user.name synthetic
git config user.email synthetic@example.invalid
for package in nss-glibc gtk3-glibc mesa-vulkan-icd-freedreno-dri3 alsa-lib-glibc libudev-zero-glibc cups-glibc; do
    mkdir -p "gpkg/$package"
    case "$package" in
        nss-glibc) src=nss; desc='NSS NSPR security' ;;
        gtk3-glibc) src=gtk; desc='GTK GDK Pango ATK GUI' ;;
        mesa-vulkan-icd-freedreno-dri3) src=mesa; desc='Mesa GBM Vulkan Freedreno' ;;
        alsa-lib-glibc) src=alsa; desc='ALSA asound' ;;
        libudev-zero-glibc) src=libudev-zero; desc='udev systemd compatibility' ;;
        cups-glibc) src=cups; desc='CUPS gnutls avahi printing' ;;
    esac
    cat > "gpkg/$package/build.sh" <<EOF
TERMUX_PKG_VERSION=1.0
TERMUX_PKG_SRCURL=https://example.invalid/$src.tar.xz
TERMUX_PKG_SHA256=0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef
TERMUX_PKG_DESCRIPTION="$desc"
EOF
done
git add gpkg
git commit -q -m synthetic
SOURCE_HEAD=$(git rev-parse HEAD)
SOURCE_STATE_BEFORE=$(git status --porcelain --untracked-files=all | sha256sum | awk '{print $1}')
APT_SHA_BEFORE=$(sha256sum "$PREFIX_ROOT/var/lib/apt/lists/example.invalid_apt_termux-glibc_dists_glibc_stable_binary-aarch64_Packages" | awk '{print $1}')

PROJECT_REPO="$REPO" \
SOURCE_REPO="$SOURCE_ROOT" \
SOURCE_REPO_EXPECTED_HEAD="$SOURCE_HEAD" \
PREFIX="$PREFIX_ROOT" \
OUT="$OUT" \
python3 "$COLLECTOR"

[ "$(cat "$OUT/analysis.status")" = PASS ] || fail "synthetic collector did not pass"
[ "$(awk 'END {print NR-1}' "$OUT/object-candidate-edges.tsv")" -eq 61 ] || fail "output denominator is not 61"
awk -F '\t' 'NR > 1 && ($11 != "OPEN_NO_DEB_EXTRACTION" || $13 != "UNRESOLVED" || $14 != "BLOCKED") {exit 1}' "$OUT/object-candidate-edges.tsv" || fail "collector promoted authority"
[ "$(awk -F '\t' 'NR > 1 && $10 != "NO_CANDIDATE_FOUND_IN_RETAINED_INPUTS" {n++} END {print n+0}' "$OUT/object-candidate-edges.tsv")" -gt 0 ] || fail "synthetic candidates were not discovered"
[ "$(awk -F '\t' '$1 == "authority_decisions_accepted" {print $2}' "$OUT/summary.tsv")" = 0 ] || fail "collector accepted authority"
[ "$(awk -F '\t' '$1 == "deb_extraction_performed" {print $2}' "$OUT/summary.tsv")" = NO ] || fail "collector claims deb extraction"
[ "$(git status --porcelain --untracked-files=all | sha256sum | awk '{print $1}')" = "$SOURCE_STATE_BEFORE" ] || fail "source repo changed"
[ "$(sha256sum "$PREFIX_ROOT/var/lib/apt/lists/example.invalid_apt_termux-glibc_dists_glibc_stable_binary-aarch64_Packages" | awk '{print $1}')" = "$APT_SHA_BEFORE" ] || fail "apt index changed"

printf 'generic exact candidate collector smoke: PASS\n'
