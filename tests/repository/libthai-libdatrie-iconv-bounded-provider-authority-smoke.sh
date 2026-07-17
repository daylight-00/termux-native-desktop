#!/usr/bin/env bash
set -euo pipefail
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
TMP_BASE=${TND_TEST_TMPDIR:-${TMPDIR:-$ROOT/.tmp}}; mkdir -p "$TMP_BASE"; FIXTURE=$(mktemp -d "$TMP_BASE/thai-provider.XXXXXX")
cleanup(){ chmod -R u+w "$FIXTURE" 2>/dev/null || true; rm -rf "$FIXTURE"; }; trap cleanup EXIT HUP INT TERM
git -C "$ROOT" archive HEAD | tar -xf - -C "$FIXTURE"
CHECK="$FIXTURE/tools/docs/check-libthai-libdatrie-iconv-bounded-provider-authority"
bash "$CHECK" >/dev/null
TABLE="$FIXTURE/experiments/glibc/selected-obsidian-provider-authority/review/libthai-libdatrie-bounded-provider-authority.tsv"
ICONV="$FIXTURE/experiments/glibc/selected-obsidian-provider-authority/review/libiconv-transitive-provider-authority.tsv"
cp "$TABLE" "$TABLE.orig"; sed -i 's/d411879359c81553f3b508f7c27918f88ec2b42b8b249594af0de84e8a79dd25/aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/' "$TABLE"
if bash "$CHECK" >/dev/null 2>&1; then echo 'thai provider smoke: dictionary drift accepted' >&2; exit 1; fi
mv "$TABLE.orig" "$TABLE"; cp "$ICONV" "$ICONV.orig"; sed -i 's/ACCEPTED_BOUNDED_TRANSITIVE_PROVIDER/OPEN_NO_ACCEPTANCE/' "$ICONV"
if bash "$CHECK" >/dev/null 2>&1; then echo 'thai provider smoke: iconv reopening accepted' >&2; exit 1; fi
mv "$ICONV.orig" "$ICONV"; cp "$TABLE" "$TABLE.orig"; sed -i 's/DEFAULT_TARGET_PATH_NOT_AUTHORIZED/DEFAULT_TARGET_PATH_AUTHORIZED/' "$TABLE"
if bash "$CHECK" >/dev/null 2>&1; then echo 'thai provider smoke: target path widening accepted' >&2; exit 1; fi
mv "$TABLE.orig" "$TABLE"; cp "$ICONV" "$ICONV.orig"; sed -i 's/LIBCHARSET_PRESENT_BUT_NOT_NEEDED_OR_MAPPED_AND_EXCLUDED/LIBCHARSET_ACCEPTED/' "$ICONV"
if bash "$CHECK" >/dev/null 2>&1; then echo 'thai provider smoke: libcharset widening accepted' >&2; exit 1; fi
echo 'libthai/libdatrie/iconv bounded provider authority smoke: PASS'
