#!/usr/bin/env bash
set -euo pipefail

REPO=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
BASE="$REPO/experiments/glibc/selected-obsidian-provider-authority"
COLLECTOR="$BASE/recipe/collect-generic-artifact-member-inventory.py"
RUNNER="$BASE/recipe/run-generic-artifact-member-inventory.sh"
ARTIFACTS="$BASE/review/generic-artifact-member-comparison-artifacts.tsv"
EDGES="$BASE/review/generic-artifact-member-comparison-edges.tsv"
META="$BASE/review/generic-artifact-member-comparison-metadata.tsv"
REPOSITORY="$BASE/profiles/supply-repository-metadata-registry.tsv"

fail() {
    printf 'generic artifact member inventory collector smoke: FAIL: %s\n' "$*" >&2
    exit 1
}

for path in "$COLLECTOR" "$RUNNER" "$ARTIFACTS" "$EDGES" "$META" "$REPOSITORY"; do
    [ -f "$path" ] || fail "missing collector input: $path"
done
[ -x "$COLLECTOR" ] || fail "collector is not executable"
[ -x "$RUNNER" ] || fail "runner is not executable"
python3 -m py_compile "$COLLECTOR"
bash -n "$RUNNER"

[ "$(awk 'END {print NR-1}' "$ARTIFACTS")" -eq 34 ] || fail "canonical artifact denominator drift"
[ "$(awk 'END {print NR-1}' "$EDGES")" -eq 44 ] || fail "canonical edge denominator drift"
[ "$(awk -F '\t' 'NR > 1 {sum += $7} END {print sum+0}' "$ARTIFACTS")" -eq 51771348 ] || fail "canonical byte ceiling drift"

for forbidden in \
    'apt[[:space:]]+(update|install|download|upgrade|remove)' \
    'pkg[[:space:]]+(install|upgrade|uninstall)' \
    'dpkg[[:space:]]+-i' \
    'dpkg[[:space:]]+--install' \
    'extractall[[:space:]]*\(' \
    '\.extract[[:space:]]*\(' \
    'target_population_state.*ACCEPTED'; do
    if grep -E "$forbidden" "$COLLECTOR" "$RUNNER" >/dev/null; then
        fail "forbidden package/materialization implementation appears: $forbidden"
    fi
done

grep -F '"--fsys-tarfile"' "$COLLECTOR" >/dev/null || fail "data archive stream inventory missing"
grep -F '"--ctrl-tarfile"' "$COLLECTOR" >/dev/null || fail "control archive stream inventory missing"
grep -F 'authority_decisions_accepted", "value": 0' "$COLLECTOR" >/dev/null || fail "authority zero boundary missing"
grep -F 'target_rows_populated", "value": 0' "$COLLECTOR" >/dev/null || fail "target zero boundary missing"

for command in git python3 gcc dpkg-deb sha256sum; do
    command -v "$command" >/dev/null 2>&1 || fail "missing smoke prerequisite: $command"
done

TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
mkdir -p "$TMP/repo" "$TMP/prefix/var/lib/dpkg" "$TMP/prefix/var/lib/apt/lists" \
    "$TMP/http/pool/test/f/foo-glibc" "$TMP/http/pool/test/b/bar-glibc" \
    "$TMP/pkg-foo/DEBIAN" "$TMP/pkg-foo/usr/lib" "$TMP/pkg-bar/DEBIAN" "$TMP/pkg-bar/usr/share/bar"

git -C "$TMP/repo" init -q
git -C "$TMP/repo" config user.name smoke
git -C "$TMP/repo" config user.email smoke@example.invalid
printf 'synthetic\n' > "$TMP/repo/README"
git -C "$TMP/repo" add README
git -C "$TMP/repo" commit -qm initial
printf 'Package: base\nStatus: install ok installed\nVersion: 1\nArchitecture: aarch64\n\n' > "$TMP/prefix/var/lib/dpkg/status"
printf 'retained apt list sentinel\n' > "$TMP/prefix/var/lib/apt/lists/sentinel"
printf 'dummy test mode CA\n' > "$TMP/ca.pem"

cat > "$TMP/foo.c" <<'C'
int foo(void) { return 7; }
C
gcc -shared -fPIC -Wl,-soname,libfoo.so.1 -o "$TMP/pkg-foo/usr/lib/libfoo.so.1.0.0" "$TMP/foo.c"
ln -s libfoo.so.1.0.0 "$TMP/pkg-foo/usr/lib/libfoo.so.1"
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
FOO_DEB="$TMP/http/pool/test/f/foo-glibc/foo-glibc_1.0-1_aarch64.deb"
BAR_DEB="$TMP/http/pool/test/b/bar-glibc/bar-glibc_2.0-1_aarch64.deb"
dpkg-deb --build "$TMP/pkg-foo" "$FOO_DEB" >/dev/null
dpkg-deb --build "$TMP/pkg-bar" "$BAR_DEB" >/dev/null

python3 - "$COLLECTOR" "$TMP" <<'PY'
import csv
import hashlib
import http.server
import os
import socketserver
import subprocess
import sys
import threading
from pathlib import Path

collector = Path(sys.argv[1])
root = Path(sys.argv[2])
http_root = root / "http"
inputs = root / "inputs"
inputs.mkdir()

def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def write(path: Path, fields, rows):
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

def read(path: Path):
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))

foo = http_root / "pool/test/f/foo-glibc/foo-glibc_1.0-1_aarch64.deb"
bar = http_root / "pool/test/b/bar-glibc/bar-glibc_2.0-1_aarch64.deb"
artifacts_path = inputs / "artifacts.tsv"
edges_path = inputs / "edges.tsv"
meta_path = inputs / "metadata.tsv"
repository_path = inputs / "repository.tsv"
artifact_fields = [
    "artifact_id", "repository_metadata_id", "package", "version", "architecture",
    "repository_filename", "artifact_size", "artifact_sha256", "packages_index_sha256",
    "artifact_class", "comparison_scope_state", "download_state", "member_inventory_state",
    "authority_state", "target_population_state",
]
artifacts = [
    {
        "artifact_id": "artifact:foo", "repository_metadata_id": "repository:test",
        "package": "foo-glibc", "version": "1.0-1", "architecture": "aarch64",
        "repository_filename": "pool/test/f/foo-glibc/foo-glibc_1.0-1_aarch64.deb",
        "artifact_size": str(foo.stat().st_size), "artifact_sha256": digest(foo),
        "packages_index_sha256": "1" * 64,
        "artifact_class": "DYNAMIC_OR_SPLIT_RUNTIME_CANDIDATE",
        "comparison_scope_state": "NAMED_DOWNLOAD_ONLY_MEMBER_INVENTORY_SCOPE",
        "download_state": "NOT_DOWNLOADED_CONTRACT_ONLY", "member_inventory_state": "OPEN",
        "authority_state": "UNRESOLVED", "target_population_state": "BLOCKED",
    },
    {
        "artifact_id": "artifact:bar", "repository_metadata_id": "repository:test",
        "package": "bar-glibc", "version": "2.0-1", "architecture": "aarch64",
        "repository_filename": "pool/test/b/bar-glibc/bar-glibc_2.0-1_aarch64.deb",
        "artifact_size": str(bar.stat().st_size), "artifact_sha256": digest(bar),
        "packages_index_sha256": "1" * 64,
        "artifact_class": "DYNAMIC_OR_SPLIT_RUNTIME_CANDIDATE",
        "comparison_scope_state": "NAMED_DOWNLOAD_ONLY_MEMBER_INVENTORY_SCOPE",
        "download_state": "NOT_DOWNLOADED_CONTRACT_ONLY", "member_inventory_state": "OPEN",
        "authority_state": "UNRESOLVED", "target_population_state": "BLOCKED",
    },
]
write(artifacts_path, artifact_fields, artifacts)
edge_fields = [
    "evidence_row_id", "capability_partition", "identity_label", "artifact_id", "package",
    "version", "architecture", "expected_member_basename", "direct_recipe_packages",
    "comparison_edge_state", "member_match_state", "artifact_to_recipe_binding_state",
    "termux_android_adaptation_state", "final_provider_state", "target_population_state",
]
edges = [
    {"evidence_row_id": "selected:foo-real", "capability_partition": "test", "identity_label": "libfoo.so.1.0.0", "artifact_id": "artifact:foo", "package": "foo-glibc", "version": "1.0-1", "architecture": "aarch64", "expected_member_basename": "libfoo.so.1.0.0", "direct_recipe_packages": "foo", "comparison_edge_state": "NAMED_MEMBER_SEARCH_CANDIDATE_ONLY", "member_match_state": "OPEN", "artifact_to_recipe_binding_state": "OPEN", "termux_android_adaptation_state": "OPEN", "final_provider_state": "UNRESOLVED", "target_population_state": "BLOCKED"},
    {"evidence_row_id": "selected:foo-link", "capability_partition": "test", "identity_label": "libfoo.so.1", "artifact_id": "artifact:foo", "package": "foo-glibc", "version": "1.0-1", "architecture": "aarch64", "expected_member_basename": "libfoo.so.1", "direct_recipe_packages": "foo", "comparison_edge_state": "NAMED_MEMBER_SEARCH_CANDIDATE_ONLY", "member_match_state": "OPEN", "artifact_to_recipe_binding_state": "OPEN", "termux_android_adaptation_state": "OPEN", "final_provider_state": "UNRESOLVED", "target_population_state": "BLOCKED"},
    {"evidence_row_id": "selected:missing", "capability_partition": "test", "identity_label": "libmissing.so.1", "artifact_id": "artifact:bar", "package": "bar-glibc", "version": "2.0-1", "architecture": "aarch64", "expected_member_basename": "libmissing.so.1", "direct_recipe_packages": "bar", "comparison_edge_state": "NAMED_MEMBER_SEARCH_CANDIDATE_ONLY", "member_match_state": "OPEN", "artifact_to_recipe_binding_state": "OPEN", "termux_android_adaptation_state": "OPEN", "final_provider_state": "UNRESOLVED", "target_population_state": "BLOCKED"},
]
write(edges_path, edge_fields, edges)

class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

handler = lambda *args, **kwargs: QuietHandler(*args, directory=str(http_root), **kwargs)
server = socketserver.ThreadingTCPServer(("127.0.0.1", 0), handler)
port = server.server_address[1]
thread = threading.Thread(target=server.serve_forever, daemon=True)
thread.start()
base_uri = f"http://127.0.0.1:{port}/"
repository_fields = ["repository_metadata_id", "repository_base_uri", "packages_index_path", "packages_index_sha256", "inrelease_path", "inrelease_sha256", "repository_metadata_state", "repository_trust_policy_state", "target_population_state"]
write(repository_path, repository_fields, [{"repository_metadata_id": "repository:test", "repository_base_uri": base_uri, "packages_index_path": str(root / "prefix/var/lib/apt/lists/sentinel"), "packages_index_sha256": "1" * 64, "inrelease_path": "-", "inrelease_sha256": "-", "repository_metadata_state": "SYNTHETIC_TEST", "repository_trust_policy_state": "TEST_ONLY", "target_population_state": "BLOCKED"}])
meta_rows = [
    ("repository_metadata_id", "repository:test"),
    ("repository_base_uri", base_uri),
    ("artifact_set_sha256", digest(artifacts_path)),
    ("edge_set_sha256", digest(edges_path)),
    ("download_scope_artifacts", "2"),
    ("download_scope_edges", "3"),
    ("download_scope_compressed_bytes", str(foo.stat().st_size + bar.stat().st_size)),
    ("authority_decisions_accepted", "0"),
    ("target_rows_populated", "0"),
]
write(meta_path, ["field", "value"], [{"field": k, "value": v} for k, v in meta_rows])

def invoke(out: Path):
    env = os.environ.copy()
    env.update({
        "PROJECT_REPO": str(root / "repo"),
        "PREFIX": str(root / "prefix"),
        "OUT": str(out),
        "ARTIFACT_DIR": str(root / "cache"),
        "SSL_CERT_FILE": str(root / "ca.pem"),
        "COMPARISON_ARTIFACTS": str(artifacts_path),
        "COMPARISON_EDGES": str(edges_path),
        "COMPARISON_METADATA": str(meta_path),
        "REPOSITORY_METADATA": str(repository_path),
        "GENERIC_MEMBER_INVENTORY_TEST_MODE": "1",
    })
    return subprocess.run([sys.executable, str(collector)], env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

first = invoke(root / "out-first")
if first.returncode:
    raise SystemExit(f"first collector run failed\nstdout={first.stdout}\nstderr={first.stderr}")
summary = {row["field"]: row["value"] for row in read(root / "out-first/summary.tsv")}
assert summary["artifacts_planned"] == "2"
assert summary["artifacts_downloaded"] == "2"
assert summary["artifacts_reused"] == "0"
assert summary["named_edges"] == "3"
assert summary["edges_with_exact_basename_observation"] == "2"
assert summary["edges_without_exact_basename_observation"] == "1"
assert summary["package_operation_performed"] == "NO"
assert summary["maintainer_script_execution_performed"] == "NO"
assert summary["deb_filesystem_materialization_performed"] == "NO"
assert summary["authority_decisions_accepted"] == "0"
assert summary["target_rows_populated"] == "0"
observations = {row["evidence_row_id"]: row for row in read(root / "out-first/named-member-observations.tsv")}
assert observations["selected:foo-real"]["member_observation_state"] == "UNIQUE_EXACT_BASENAME_MEMBER_OBSERVED"
assert observations["selected:foo-real"]["observed_elf_sonames"] == "libfoo.so.1"
assert len(observations["selected:foo-real"]["observed_member_sha256s"]) == 64
assert observations["selected:foo-link"]["observed_member_types"] == "SYMLINK"
assert observations["selected:missing"]["member_observation_state"] == "NO_EXACT_BASENAME_MEMBER_OBSERVED"
cache_entries = sorted(path.name for path in (root / "cache").iterdir())
assert cache_entries == [bar.name, foo.name]
assert all(path.is_file() and not path.is_symlink() for path in (root / "cache").iterdir())

server.shutdown()
server.server_close()
thread.join(timeout=5)
second = invoke(root / "out-second")
if second.returncode:
    raise SystemExit(f"cache-only collector run failed\nstdout={second.stdout}\nstderr={second.stderr}")
summary2 = {row["field"]: row["value"] for row in read(root / "out-second/summary.tsv")}
assert summary2["artifacts_downloaded"] == "0"
assert summary2["artifacts_reused"] == "2"
assert summary2["network_download_performed"] == "NO_REUSED_ONLY"
assert (root / "prefix/var/lib/dpkg/status").read_text().startswith("Package: base")
assert (root / "prefix/var/lib/apt/lists/sentinel").read_text() == "retained apt list sentinel\n"
PY

printf 'generic artifact member inventory collector smoke: PASS\n'
