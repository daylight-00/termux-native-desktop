#!/usr/bin/env bash
set -euo pipefail
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
TMP_BASE=${TND_TEST_TMPDIR:-${TMPDIR:-$ROOT/.tmp}}; mkdir -p "$TMP_BASE"; FIXTURE=$(mktemp -d "$TMP_BASE/util-provider.XXXXXX")
cleanup(){ chmod -R u+w "$FIXTURE" 2>/dev/null || true; rm -rf "$FIXTURE"; }; trap cleanup EXIT HUP INT TERM
git -C "$ROOT" archive HEAD | tar -xf - -C "$FIXTURE"
bash "$FIXTURE/tools/docs/check-gdkpixbuf-exact-util-linux-provider-authority" >/dev/null
TABLE=experiments/glibc/selected-obsidian-provider-authority/review/gdkpixbuf-exact-util-linux-provider-authority.tsv
sed -i 's/ACCEPTED_BOUNDED_PROVIDER/OPEN_EXACT_RUNTIME_BINDING_REQUIRED/' "$FIXTURE/$TABLE"
if bash "$FIXTURE/tools/docs/check-gdkpixbuf-exact-util-linux-provider-authority" >/dev/null 2>&1; then echo 'util provider smoke: reopened accepted pair' >&2; exit 1; fi
git -C "$ROOT" show HEAD:"$TABLE" > "$FIXTURE/$TABLE"
sed -i 's/NO_COMPLETE_COMPOSITION_TARGET_OR_ACTIVATION_EFFECT/COMPLETE_COMPOSITION_ACCEPTED/' "$FIXTURE/$TABLE"
if bash "$FIXTURE/tools/docs/check-gdkpixbuf-exact-util-linux-provider-authority" >/dev/null 2>&1; then echo 'util provider smoke: authority widened' >&2; exit 1; fi
echo 'gdkpixbuf exact util-linux provider authority smoke: PASS'
