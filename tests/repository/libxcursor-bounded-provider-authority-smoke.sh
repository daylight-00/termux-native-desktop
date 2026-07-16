#!/usr/bin/env bash
set -euo pipefail
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
TMP_BASE=${TND_TEST_TMPDIR:-${TMPDIR:-$ROOT/.tmp}}; mkdir -p "$TMP_BASE"; FIXTURE=$(mktemp -d "$TMP_BASE/libxcursor-provider.XXXXXX")
cleanup(){ chmod -R u+w "$FIXTURE" 2>/dev/null || true; rm -rf "$FIXTURE"; }; trap cleanup EXIT HUP INT TERM
git -C "$ROOT" archive HEAD | tar -xf - -C "$FIXTURE"
CHECK="$FIXTURE/tools/docs/check-libxcursor-bounded-provider-authority"
TABLE="$FIXTURE/experiments/glibc/selected-obsidian-provider-authority/review/libxcursor-bounded-provider-authority.tsv"
bash "$CHECK" >/dev/null
cp "$TABLE" "$TABLE.orig"
sed -i 's/379e15f8152af7a9665b113bc470042f73c3a8a8/0000000000000000000000000000000000000000/' "$TABLE"
if bash "$CHECK" >/dev/null 2>&1; then echo 'libxcursor smoke: patch coordinate drift accepted' >&2; exit 1; fi
cp "$TABLE.orig" "$TABLE"
sed -i 's/GDKCURSOR_X11_INCLUDES_X11_XCURSOR_HEADER_AND_CALLS_XCURSOR_GET_THEME_GET_DEFAULT_SIZE_LIBRARY_LOAD_IMAGES_SHAPE_LOAD_IMAGES_LIBRARY_LOAD_CURSOR_SHAPE_LOAD_CURSOR_SET_THEME_SET_DEFAULT_SIZE_AND_IMAGE_LOAD_CURSOR/UNBOUND_CONSUMER/' "$TABLE"
if bash "$CHECK" >/dev/null 2>&1; then echo 'libxcursor smoke: consumer binding removal accepted' >&2; exit 1; fi
cp "$TABLE.orig" "$TABLE"
sed -i 's/ACCEPTED_BOUNDED_PROVIDER/OPEN_CONSUMER_BINDING_REQUIRED/' "$TABLE"
if bash "$CHECK" >/dev/null 2>&1; then echo 'libxcursor smoke: accepted provider reopened silently' >&2; exit 1; fi
cp "$TABLE.orig" "$TABLE"
sed -i 's/NO_COMPOSITION_TARGET_OR_ACTIVATION_EFFECT/COMPLETE_COMPOSITION_TARGET_AND_ACTIVATION_ACCEPTED/' "$TABLE"
if bash "$CHECK" >/dev/null 2>&1; then echo 'libxcursor smoke: authority widening accepted' >&2; exit 1; fi
echo 'libxcursor bounded provider authority smoke: PASS'
