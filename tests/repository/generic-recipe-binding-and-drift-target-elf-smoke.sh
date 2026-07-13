#!/usr/bin/env bash
set -euo pipefail

REPO=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
BASE="$REPO/experiments/glibc/selected-obsidian-provider-authority"
COLLECTOR="$BASE/recipe/collect-generic-recipe-binding-and-drift-target-elf.py"
RUNNER="$BASE/recipe/run-generic-recipe-binding-and-drift-target-elf.sh"
RULES="$BASE/review/generic-recipe-binding-and-drift-target-rules.tsv"
ARTIFACTS="$BASE/review/generic-artifact-member-comparison-artifacts.tsv"
METADATA="$BASE/review/generic-recipe-binding-and-drift-target-metadata.tsv"

fail() {
    printf 'generic recipe binding and drift target ELF smoke: FAIL: %s\n' "$*" >&2
    exit 1
}

for path in "$COLLECTOR" "$RUNNER" "$RULES" "$ARTIFACTS" "$METADATA"; do
    [ -f "$path" ] || fail "missing input: $path"
done
[ -x "$COLLECTOR" ] || fail "collector is not executable"
[ -x "$RUNNER" ] || fail "runner is not executable"
python3 -m py_compile "$COLLECTOR"
bash -n "$RUNNER"

[ "$(awk 'END {print NR-1}' "$RULES")" -eq 37 ] || fail "canonical rules denominator drift"
[ "$(awk 'END {print NR-1}' "$ARTIFACTS")" -eq 34 ] || fail "full artifact cache denominator drift"
[ "$(awk -F '\t' 'NR > 1 {seen[$5]=1} END {print length(seen)}' "$RULES")" -eq 29 ] || fail "selected artifact denominator drift"
observed_rules_sha=$(sha256sum "$RULES" | awk '{print $1}')
expected_rules_sha=$(awk -F '\t' '$1 == "rules_sha256" {print $2}' "$METADATA")
[ "$observed_rules_sha" = "$expected_rules_sha" ] || fail "canonical rules hash drift"
[ "$(awk -F '\t' '$1 == "verified_artifact_cache_rows_required" {print $2}' "$METADATA")" = 34 ] || fail "metadata full artifact denominator drift"
[ "$(awk -F '\t' '$1 == "selected_unique_artifacts_referenced" {print $2}' "$METADATA")" = 29 ] || fail "metadata selected artifact denominator drift"
[ "$(awk -F '\t' 'NR > 1 && $30 == "PENDING_READ_ONLY_TARGET_ELF_INSPECTION" {n++} END {print n+0}' "$RULES")" -eq 15 ] || fail "canonical drift denominator drift"
[ "$(awk -F '\t' 'NR > 1 && $31 != "OPEN_NO_BUILD_ATTESTATION" {n++} END {print n+0}' "$RULES")" -eq 0 ] || fail "artifact-to-recipe stop state drift"
[ "$(awk -F '\t' 'NR > 1 && ($32 != "UNRESOLVED" || $33 != "BLOCKED") {n++} END {print n+0}' "$RULES")" -eq 0 ] || fail "final/target stop state drift"

for forbidden in \
    'apt[[:space:]]+(update|install|download|upgrade|remove)' \
    'pkg[[:space:]]+(install|upgrade|uninstall)' \
    'dpkg[[:space:]]+-i' \
    'dpkg[[:space:]]+--install' \
    'extractall[[:space:]]*\(' \
    '\.extract[[:space:]]*\(' \
    'git[[:space:]]+(fetch|pull|clone)' \
    'target_population_state.*ACCEPTED'; do
    if grep -E "$forbidden" "$COLLECTOR" "$RUNNER" >/dev/null; then
        fail "forbidden operation appears: $forbidden"
    fi
done

grep -F '"--fsys-tarfile"' "$COLLECTOR" >/dev/null || fail "read-only data tar stream missing"
grep -F 'OPEN_NO_BUILD_ATTESTATION' "$COLLECTOR" >/dev/null || fail "build-attestation stop state missing"
grep -F 'final_provider_decisions_accepted", 0' "$COLLECTOR" >/dev/null || fail "authority zero boundary missing"
grep -F 'target_rows_populated", 0' "$COLLECTOR" >/dev/null || fail "target zero boundary missing"

for command in git python3 gcc dpkg-deb sha256sum truncate; do
    command -v "$command" >/dev/null 2>&1 || fail "missing smoke prerequisite: $command"
done

TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
SOURCE="$TMP/source"
CACHE="$TMP/cache"
mkdir -p "$SOURCE/gpkg/foo" "$SOURCE/gpkg/bar" "$CACHE" \
    "$TMP/pkg-foo/DEBIAN" "$TMP/pkg-foo/usr/lib" "$TMP/pkg-foo/usr/share/zz-stream-drain" \
    "$TMP/pkg-bar/DEBIAN" "$TMP/pkg-bar/usr/share/bar" "$TMP/inputs" "$TMP/fakebin"
chmod 0755 "$TMP/pkg-foo/DEBIAN" "$TMP/pkg-bar/DEBIAN"

cat > "$SOURCE/gpkg/foo/build.sh" <<'EOF'
TERMUX_PKG_VERSION=1.0
TERMUX_PKG_REVISION=1
TERMUX_PKG_SRCURL=https://example.invalid/foo-${TERMUX_PKG_VERSION}.tar.xz
TERMUX_PKG_SHA256=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
TERMUX_PKG_EXTRA_CONFIGURE_ARGS="--enable-shared"
termux_step_pre_configure() {
    printf '%s\n' "$TERMUX_PREFIX" >/dev/null
}
EOF
printf 'synthetic patch\n' > "$SOURCE/gpkg/foo/android.patch"
printf 'TERMUX_SUBPKG_DESCRIPTION="tools"\n' > "$SOURCE/gpkg/foo/foo-tools.subpackage.sh"
cat > "$SOURCE/gpkg/bar/build.sh" <<'EOF'
TERMUX_PKG_VERSION=2.0
TERMUX_PKG_REVISION=1
TERMUX_PKG_SRCURL=https://example.invalid/bar-${TERMUX_PKG_VERSION}.tar.xz
TERMUX_PKG_SHA256=bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb
EOF

git -C "$SOURCE" init -q
git -C "$SOURCE" config user.name smoke
git -C "$SOURCE" config user.email smoke@example.invalid
git -C "$SOURCE" remote add origin https://example.invalid/source.git
git -C "$SOURCE" add gpkg
git -C "$SOURCE" commit -qm source-pin
SOURCE_HEAD=$(git -C "$SOURCE" rev-parse HEAD)
SOURCE_TREE=$(git -C "$SOURCE" rev-parse HEAD^{tree})

cat > "$TMP/foo.c" <<'C'
int foo(void) { return 7; }
C
gcc -shared -fPIC -Wl,-soname,libfoo.so.1 -o "$TMP/pkg-foo/usr/lib/libfoo.so.1.0.0" "$TMP/foo.c"
ln -s libfoo.so.1.0.0 "$TMP/pkg-foo/usr/lib/libfoo.so.1"
# Keep substantial data after the target member so an early pipe close reliably
# reproduces dpkg-deb's Broken pipe failure instead of passing by timing.
truncate -s 16777216 "$TMP/pkg-foo/usr/share/zz-stream-drain/trailing-zeroes.bin"
cat > "$TMP/pkg-foo/DEBIAN/control" <<'EOF'
Package: foo-glibc
Version: 1.0-1
Architecture: aarch64
Maintainer: smoke <smoke@example.invalid>
Description: synthetic foo
EOF
cat > "$TMP/pkg-bar/DEBIAN/control" <<'EOF'
Package: bar-glibc
Version: 2.0-1
Architecture: aarch64
Maintainer: smoke <smoke@example.invalid>
Description: synthetic bar
EOF
printf 'bar\n' > "$TMP/pkg-bar/usr/share/bar/data.txt"
FOO_DEB="$CACHE/foo-glibc_1.0-1_aarch64.deb"
BAR_DEB="$CACHE/bar-glibc_2.0-1_aarch64.deb"
dpkg-deb --build "$TMP/pkg-foo" "$FOO_DEB" >/dev/null
dpkg-deb --build "$TMP/pkg-bar" "$BAR_DEB" >/dev/null

REAL_DPKG_DEB=$(command -v dpkg-deb)
cat > "$TMP/fakebin/dpkg-deb" <<'SH'
#!/usr/bin/env bash
set -u
real=${REAL_DPKG_DEB:?}
if [ "${1:-}" = --fsys-tarfile ]; then
    tmp=$(mktemp)
    trap 'rm -f "$tmp"' EXIT
    "$real" "$@" > "$tmp" || exit $?
    set +e
    cat "$tmp"
    rc=$?
    set -e
    if [ "$rc" -ne 0 ]; then
        printf '%s\n' 'dpkg-deb: error: paste subprocess was killed by signal (Broken pipe)' >&2
        exit 2
    fi
    exit 0
fi
exec "$real" "$@"
SH
chmod 0755 "$TMP/fakebin/dpkg-deb"

python3 - "$SOURCE" "$SOURCE_HEAD" "$FOO_DEB" "$BAR_DEB" "$TMP/inputs" <<'PY'
import csv
import hashlib
import subprocess
import sys
from collections import Counter
from pathlib import Path

source, head, foo, bar, inputs = map(Path, sys.argv[1:])
head = str(head)

def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def write(path: Path, fields, rows):
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(rows)

def git(*args, binary=False):
    return subprocess.run(["git", "-C", str(source), *args], check=True, stdout=subprocess.PIPE, text=not binary).stdout

def recipe(root: str):
    tree = git("rev-parse", f"{head}:{root}").strip()
    lines = []
    counts = Counter()
    build_blob = build_sha = None
    for raw in git("ls-tree", "-r", "-l", head, "--", root).splitlines():
        meta, path = raw.split("\t", 1)
        mode, kind, oid, _size = meta.split(None, 3)
        payload = git("show", f"{head}:{path}", binary=True)
        content_sha = hashlib.sha256(payload).hexdigest()
        lines.append("\t".join([path, oid, str(len(payload)), content_sha]))
        if path.endswith("/build.sh"):
            counts["build"] += 1; build_blob = oid; build_sha = content_sha
        elif path.endswith(".patch"): counts["patch"] += 1
        elif path.endswith(".subpackage.sh"): counts["subpackage"] += 1
        elif path.endswith("Termux.layout") or "/hooks/" in path or path.endswith(".in"): counts["layout_hook"] += 1
        else: counts["other"] += 1
    return {
        "tree": tree, "manifest": hashlib.sha256(("\n".join(lines) + "\n").encode()).hexdigest(),
        "count": len(lines), "patch": counts["patch"], "subpackage": counts["subpackage"],
        "layout_hook": counts["layout_hook"], "other": counts["other"],
        "build_blob": build_blob, "build_sha": build_sha,
    }

foo_recipe = recipe("gpkg/foo")
bar_recipe = recipe("gpkg/bar")
artifact_fields = [
    "artifact_id", "repository_metadata_id", "package", "version", "architecture", "repository_filename",
    "artifact_size", "artifact_sha256", "packages_index_sha256", "artifact_class", "comparison_scope_state",
    "download_state", "member_inventory_state", "authority_state", "target_population_state",
]
artifacts = [
    {"artifact_id":"artifact:foo","repository_metadata_id":"repo:test","package":"foo-glibc","version":"1.0-1","architecture":"aarch64","repository_filename":foo.name,"artifact_size":str(foo.stat().st_size),"artifact_sha256":digest(foo),"packages_index_sha256":"1"*64,"artifact_class":"TEST","comparison_scope_state":"TEST","download_state":"VERIFIED","member_inventory_state":"REVIEWED","authority_state":"UNRESOLVED","target_population_state":"BLOCKED"},
    {"artifact_id":"artifact:bar","repository_metadata_id":"repo:test","package":"bar-glibc","version":"2.0-1","architecture":"aarch64","repository_filename":bar.name,"artifact_size":str(bar.stat().st_size),"artifact_sha256":digest(bar),"packages_index_sha256":"1"*64,"artifact_class":"TEST","comparison_scope_state":"TEST","download_state":"VERIFIED","member_inventory_state":"REVIEWED","authority_state":"UNRESOLVED","target_population_state":"BLOCKED"},
]
write(inputs/"artifacts.tsv", artifact_fields, artifacts)
rule_fields = [
    "evidence_row_id","capability_partition","identity_label","member_receipt_review_state","artifact_id","artifact_package","artifact_version","artifact_architecture","artifact_sha256","expected_soname_alias","alias_member_path","alias_target_member_path","recipe_root","recipe_tree","recipe_declared_version_raw","recipe_revision_raw","recipe_resolved_full_version","recipe_source_url_raw","recipe_source_sha256","recipe_build_sh_blob","recipe_build_sh_sha256","recipe_file_manifest_sha256","recipe_file_count","patch_file_count","subpackage_file_count","layout_hook_file_count","other_recipe_file_count","recipe_lineage_candidate_state","termux_android_adaptation_state","drift_target_elf_review_state","artifact_to_recipe_binding_state","final_provider_state","target_population_state",
]
def row(eid, identity, review, artifact, recipe_root, rec, alias="-", target="-", drift="NOT_REQUIRED_EXACT_MEMBER_ALREADY_OBSERVED"):
    version = "1.0-1" if artifact == "artifact:foo" else "2.0-1"
    package = "foo-glibc" if artifact == "artifact:foo" else "bar-glibc"
    sha = digest(foo if artifact == "artifact:foo" else bar)
    raw_version = "1.0" if artifact == "artifact:foo" else "2.0"
    source_sha = "a"*64 if artifact == "artifact:foo" else "b"*64
    return {"evidence_row_id":eid,"capability_partition":"test","identity_label":identity,"member_receipt_review_state":review,"artifact_id":artifact,"artifact_package":package,"artifact_version":version,"artifact_architecture":"aarch64","artifact_sha256":sha,"expected_soname_alias":"libfoo.so.1" if artifact == "artifact:foo" else "libmissing.so.1","alias_member_path":alias,"alias_target_member_path":target,"recipe_root":recipe_root,"recipe_tree":rec["tree"],"recipe_declared_version_raw":raw_version,"recipe_revision_raw":"1","recipe_resolved_full_version":version,"recipe_source_url_raw":f"https://example.invalid/{recipe_root.split('/')[-1]}-${{TERMUX_PKG_VERSION}}.tar.xz","recipe_source_sha256":source_sha,"recipe_build_sh_blob":rec["build_blob"],"recipe_build_sh_sha256":rec["build_sha"],"recipe_file_manifest_sha256":rec["manifest"],"recipe_file_count":str(rec["count"]),"patch_file_count":str(rec["patch"]),"subpackage_file_count":str(rec["subpackage"]),"layout_hook_file_count":str(rec["layout_hook"]),"other_recipe_file_count":str(rec["other"]),"recipe_lineage_candidate_state":"PINNED_RECIPE_FAMILY_VERSION_ALIGNED_NO_BUILD_ATTESTATION","termux_android_adaptation_state":"PINNED_RECIPE_EVIDENCE_INVENTORY_PENDING_REVIEW","drift_target_elf_review_state":drift,"artifact_to_recipe_binding_state":"OPEN_NO_BUILD_ATTESTATION","final_provider_state":"UNRESOLVED","target_population_state":"BLOCKED"}
rules = [
    row("selected:exact", "libfoo.so.1.0.0", "EXACT_CONCRETE_MEMBER_AND_EXPECTED_SONAME_OBSERVED", "artifact:foo", "gpkg/foo", foo_recipe),
    row("selected:drift", "libfoo.so.1.0.1", "EXPECTED_SONAME_ALIAS_SYMLINK_PRESENT_CONCRETE_FILENAME_DRIFT", "artifact:foo", "gpkg/foo", foo_recipe, "./usr/lib/libfoo.so.1", "./usr/lib/libfoo.so.1.0.0", "PENDING_READ_ONLY_TARGET_ELF_INSPECTION"),
    row("selected:absent", "libmissing.so.1.0.0", "EXPECTED_SONAME_ALIAS_NOT_OBSERVED_DIFFERENT_FAMILY_MEMBERS_PRESENT", "artifact:bar", "gpkg/bar", bar_recipe, drift="NOT_APPLICABLE_EXPECTED_ALIAS_ABSENT_CORRECT_CANDIDATE_REQUIRED"),
]
write(inputs/"rules.tsv", rule_fields, rules)
PY

OUT="$TMP/out"
PROJECT_REPO="$REPO" \
OUT="$OUT" \
GENERIC_RECIPE_DRIFT_RULES="$TMP/inputs/rules.tsv" \
GENERIC_COMPARISON_ARTIFACTS="$TMP/inputs/artifacts.tsv" \
GENERIC_SOURCE_REPO="$SOURCE" \
GENERIC_ARTIFACT_CACHE="$CACHE" \
GENERIC_SOURCE_EXPECTED_HEAD="$SOURCE_HEAD" \
GENERIC_SOURCE_EXPECTED_TREE="$SOURCE_TREE" \
GENERIC_RECIPE_DRIFT_TEST_MODE=1 \
REAL_DPKG_DEB="$REAL_DPKG_DEB" \
PATH="$TMP/fakebin:$PATH" \
python3 "$COLLECTOR"

[ "$(cat "$OUT/analysis.status")" = PASS ] || fail "analysis did not pass"
[ "$(awk -F '\t' '$1 == "review_identity_rows" {print $2}' "$OUT/summary.tsv")" = 3 ] || fail "review denominator mismatch"
[ "$(awk -F '\t' '$1 == "unique_recipe_roots" {print $2}' "$OUT/summary.tsv")" = 2 ] || fail "recipe-root denominator mismatch"
[ "$(awk -F '\t' '$1 == "selected_rule_artifacts" {print $2}' "$OUT/summary.tsv")" = 2 ] || fail "selected artifact summary mismatch"
[ "$(awk -F '\t' '$1 == "verified_cached_artifacts" {print $2}' "$OUT/summary.tsv")" = 2 ] || fail "artifact verification denominator mismatch"
[ "$(awk -F '\t' '$1 == "drift_target_expected_soname_confirmed" {print $2}' "$OUT/summary.tsv")" = 1 ] || fail "drift SONAME confirmation mismatch"
[ "$(awk -F '\t' 'NR > 1 {print $15}' "$OUT/drift-target-elf-review.tsv")" = libfoo.so.1 ] || fail "drift target SONAME mismatch"
[ "$(awk -F '\t' 'NR > 1 {print $16}' "$OUT/drift-target-elf-review.tsv")" = DRIFT_TARGET_ELF_EXPECTED_SONAME_CONFIRMED ] || fail "drift target state mismatch"
[ "$(awk -F '\t' 'NR > 1 && $16 != "PINNED_RECIPE_FAMILY_VERSION_ALIGNED_CANDIDATE" {n++} END {print n+0}' "$OUT/recipe-binding-review.tsv")" -eq 0 ] || fail "recipe lineage candidate mismatch"
[ "$(awk -F '\t' 'NR > 1 && ($17 != "OPEN_NO_BUILD_ATTESTATION" || $20 != "UNRESOLVED" || $21 != "BLOCKED") {n++} END {print n+0}' "$OUT/recipe-binding-review.tsv")" -eq 0 ] || fail "authority boundary mismatch"

grep -F 'PATCH_FILE' "$OUT/recipe-binding-review.tsv" >/dev/null || fail "adaptation patch evidence missing"
grep -F 'CUSTOM_TERMUX_STEP' "$OUT/recipe-binding-review.tsv" >/dev/null || fail "custom Termux step evidence missing"

printf 'generic recipe binding and drift target ELF smoke: PASS\n'
