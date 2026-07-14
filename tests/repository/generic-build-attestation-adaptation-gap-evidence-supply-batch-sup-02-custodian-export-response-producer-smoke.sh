#!/usr/bin/env bash
set -euo pipefail

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
BASE="$ROOT/experiments/glibc/selected-obsidian-provider-authority"
PRODUCER="$BASE/recipe/produce-generic-build-attestation-and-adaptation-gap-evidence-supply-batch-sup-02-custodian-export-response.py"
ACQUIRER="$BASE/recipe/acquire-generic-build-attestation-and-adaptation-gap-evidence-supply-batch-sup-02-custodian-export-responses.py"
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

for cmd in git python3 bash tar zstd sha256sum readelf; do
  command -v "$cmd" >/dev/null || { echo "missing command: $cmd" >&2; exit 1; }
done

SRC="$TMP/source"
mkdir -p "$SRC/gpkg/fixture"
cat > "$SRC/gpkg/fixture/build.sh" <<'EOF'
TERMUX_PKG_HOMEPAGE=https://example.invalid/
TERMUX_PKG_DESCRIPTION="SUP-02 producer fixture"
TERMUX_PKG_LICENSE="MIT"
TERMUX_PKG_VERSION=1.2.3
EOF
cat > "$SRC/make-fixture.sh" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
rm -rf package output sources
mkdir -p package/usr/lib output sources
printf 'fixture source bytes\n' > sources/fixture-source.tar.xz
cat > package/.PKGINFO <<'PKG'
pkgname = fixture-glibc
pkgver = 1.2.3-1
arch = aarch64
PKG
printf 'fixture library bytes\n' > package/usr/lib/libfixture.so.1
ln -s libfixture.so.1 package/usr/lib/libfixture.so
(
  cd package
  tar -cf - .
) | zstd -q -T1 -o output/fixture-glibc-1.2.3-1-aarch64.pkg.tar.zst
EOF
chmod +x "$SRC/make-fixture.sh"
git -C "$SRC" init -q
git -C "$SRC" config user.name fixture
git -C "$SRC" config user.email fixture@example.invalid
git -C "$SRC" add .
git -C "$SRC" commit -q -m fixture
HEAD=$(git -C "$SRC" rev-parse HEAD)
TREE=$(git -C "$SRC" rev-parse HEAD^{tree})
RECIPE_TREE=$(git -C "$SRC" rev-parse HEAD:gpkg/fixture)

ISSUANCE="$TMP/custodian-export-request-issuance.tsv"
CONTRACTS="$TMP/custodian-export-record-contract-issuance.tsv"
python3 - "$ISSUANCE" "$CONTRACTS" "$RECIPE_TREE" <<'PY'
import csv, sys
from pathlib import Path
issuance, contracts, recipe_tree = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
request_fields = [
 'issuance_id','request_id','batch_id','acquisition_unit_id','root_review_id','recipe_root','recipe_tree','requirement_ids','supplier_role','publication_model','transport_class','issued_request_locator','response_drop_locator','required_record_names','one_build_linkage','custodian_binding','completion_gate','request_state','acknowledgement_state','responses_received','build_attestations_accepted','claim_boundary','next_action'
]
contract_fields = ['issuance_id','request_id','root_review_id','recipe_root','recipe_tree','requirement_id','record_name','record_format','mandatory_fields','cross_record_binding','issued_request_locator','response_drop_locator','record_state','acceptance_state','claim_boundary']
mandatory = {
 'build-invocation-record.json': 'schema_version;request_id;root_review_id;recipe_root;recipe_tree;build_run_id;build_started_at_utc;build_finished_at_utc;working_directory;invocation_argv;input_source_digests;build_script_digest;custodian_identity;immutable_locator_or_signed_envelope',
 'build-environment-record.json': 'schema_version;request_id;root_review_id;recipe_tree;build_run_id;host_os;host_kernel;host_arch;toolchain_components;toolchain_digests;dependency_lock_or_snapshot;container_or_vm_image_digest;relevant_environment;source_date_epoch;custodian_identity;immutable_locator_or_signed_envelope',
 'build-output-manifest.tsv': 'request_id;root_review_id;recipe_root;recipe_tree;build_run_id;package_name;package_version;package_revision;artifact_path;artifact_sha256;member_path;member_sha256;member_elf_soname;custodian_identity;immutable_locator_or_signed_envelope',
}
requirements = {'build-invocation-record.json':'BA-001','build-environment-record.json':'BA-002','build-output-manifest.tsv':'BA-003'}
with issuance.open('w', newline='', encoding='utf-8') as f:
 w=csv.DictWriter(f, fieldnames=request_fields, delimiter='\t', lineterminator='\n'); w.writeheader()
 for i in range(1,29):
  rid=f'SUP02-CER-fixture-{i:04d}'
  root=f'generic-root-review:fixture-{i:04d}'
  w.writerow({
   'issuance_id':f'SUP02-ISSUE-fixture-{i:04d}','request_id':rid,'batch_id':'SUP-02','acquisition_unit_id':f'generic-root-acquisition:fixture-{i:04d}','root_review_id':root,'recipe_root':'gpkg/fixture','recipe_tree':recipe_tree,'requirement_ids':'BA-001;BA-002;BA-003','supplier_role':'PRODUCING_BUILD_RECORD_CUSTODIAN','publication_model':'REMOTE_BRANCH_PUBLICATION_IS_REQUEST_ISSUANCE_NOT_CUSTODIAN_ACKNOWLEDGEMENT','transport_class':'REPOSITORY_PUBLISHED_IMMUTABLE_REQUEST_PACKET','issued_request_locator':f'fixture.tsv#request_id={rid}','response_drop_locator':f'evidence-supply/responses/SUP-02/{rid}/','required_record_names':'build-invocation-record.json;build-environment-record.json;build-output-manifest.tsv','one_build_linkage':'SAME_BUILD_RUN_ID_RECIPE_TREE_AND_ARTIFACT_SET_ACROSS_ALL_THREE_RECORDS','custodian_binding':'NAMED_CUSTODIAN_IDENTITY_AND_IMMUTABLE_LOCATOR_OR_SIGNED_ENVELOPE_REQUIRED','completion_gate':'ALL_THREE_RECORDS_VALID_DIGEST_BOUND_AND_CROSS_LINKED_TO_ONE_PRODUCING_BUILD','request_state':'REQUEST_ISSUED_REPOSITORY_PUBLICATION','acknowledgement_state':'NOT_ACKNOWLEDGED','responses_received':'0','build_attestations_accepted':'0','claim_boundary':'CUSTODIAN_EXPORT_REQUEST_ISSUANCE_ONLY_NO_RESPONSE_BUILD_ATTESTATION_OR_AUTHORITY_EFFECT','next_action':'AWAIT_OR_IMPORT_EXACT_CUSTODIAN_EXPORT_RESPONSE'
  })
with contracts.open('w', newline='', encoding='utf-8') as f:
 w=csv.DictWriter(f, fieldnames=contract_fields, delimiter='\t', lineterminator='\n'); w.writeheader()
 for i in range(1,29):
  rid=f'SUP02-CER-fixture-{i:04d}'; root=f'generic-root-review:fixture-{i:04d}'
  for name in mandatory:
   w.writerow({'issuance_id':f'SUP02-ISSUE-fixture-{i:04d}','request_id':rid,'root_review_id':root,'recipe_root':'gpkg/fixture','recipe_tree':recipe_tree,'requirement_id':requirements[name],'record_name':name,'record_format':'TSV_WITH_ROWS' if name.endswith('.tsv') else 'JSON_OBJECT','mandatory_fields':mandatory[name],'cross_record_binding':'request_id;root_review_id;recipe_tree;build_run_id;custodian_identity;immutable_locator_or_signed_envelope','issued_request_locator':f'fixture.tsv#request_id={rid}','response_drop_locator':f'evidence-supply/responses/SUP-02/{rid}/','record_state':'ISSUED_REQUIRED_NOT_SUPPLIED','acceptance_state':'OPEN_NO_ACCEPTANCE','claim_boundary':'CUSTODIAN_EXPORT_REQUEST_ISSUANCE_ONLY_NO_RESPONSE_BUILD_ATTESTATION_OR_AUTHORITY_EFFECT'})
PY

OUT="$TMP/producer-output"
SOURCE_DATE_EPOCH=1700000000 python3 "$PRODUCER" \
  --request-issuance "$ISSUANCE" \
  --record-contract-issuance "$CONTRACTS" \
  --request-id SUP02-CER-fixture-0001 \
  --source-repository "$SRC" \
  --artifact-glob 'output/*.pkg.tar.zst' \
  --input-source-glob 'sources/*' \
  --build-run-id build-run-fixture-0001 \
  --custodian-identity fixture-custodian \
  --immutable-locator-or-signed-envelope signed-envelope:fixture:0001 \
  --container-or-vm-image-digest sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa \
  --source-date-epoch 1700000000 \
  --out "$OUT" \
  -- bash ./make-fixture.sh >"$TMP/producer.log"

grep -Fxq 'SUP02_CUSTODIAN_EXPORT_RESPONSE_PRODUCER=PASS_BOUNDED' "$TMP/producer.log"
RESP="$OUT/response-root/SUP02-CER-fixture-0001"
for name in build-invocation-record.json build-environment-record.json build-output-manifest.tsv custodian-export-response-manifest.tsv; do
  test -f "$RESP/$name"
done
python3 - "$RESP" "$RECIPE_TREE" <<'PY'
import csv, hashlib, json, sys
from pathlib import Path
root=Path(sys.argv[1]); tree=sys.argv[2]
inv=json.loads((root/'build-invocation-record.json').read_text())
env=json.loads((root/'build-environment-record.json').read_text())
rows=list(csv.DictReader((root/'build-output-manifest.tsv').open(),delimiter='\t'))
manifest=list(csv.DictReader((root/'custodian-export-response-manifest.tsv').open(),delimiter='\t'))
assert inv['recipe_tree']==tree and env['recipe_tree']==tree
assert inv['build_run_id']==env['build_run_id']=='build-run-fixture-0001'
assert len(rows)>=3 and any(r['member_path']=='usr/lib/libfixture.so.1' for r in rows)
assert any(r['member_path']=='usr/lib/libfixture.so' for r in rows)
assert len(manifest)==3
for row in manifest:
 p=root/row['relative_path']
 assert hashlib.sha256(p.read_bytes()).hexdigest()==row['sha256']
 assert p.stat().st_size==int(row['size_bytes'])
PY

ACQUIRED="$TMP/acquired"
python3 "$ACQUIRER" \
  --request-issuance "$ISSUANCE" \
  --record-contract-issuance "$CONTRACTS" \
  --input-root "$OUT/response-root" \
  --source-head "$HEAD" \
  --source-tree "$TREE" \
  --out "$ACQUIRED" >"$TMP/acquirer.log"
grep -Fxq 'COMPLETE_CANDIDATE_RESPONSES_ACQUIRED=1' "$TMP/acquirer.log"
grep -Fxq 'REQUESTS_WITHOUT_RESPONSE=27' "$TMP/acquirer.log"
grep -Fxq 'VERIFIED_RESPONSE_RECORDS=3' "$TMP/acquirer.log"

BAD_ISSUANCE="$TMP/bad-issuance.tsv"
python3 - "$ISSUANCE" "$BAD_ISSUANCE" <<'PY'
import csv, sys
rows=list(csv.DictReader(open(sys.argv[1]), delimiter='\t'))
fields=list(rows[0])
rows[0]['recipe_tree']='0'*40
with open(sys.argv[2], 'w', newline='', encoding='utf-8') as f:
 w=csv.DictWriter(f, fieldnames=fields, delimiter='\t', lineterminator='\n'); w.writeheader(); w.writerows(rows)
PY
if python3 "$PRODUCER" \
  --request-issuance "$BAD_ISSUANCE" \
  --record-contract-issuance "$CONTRACTS" \
  --request-id SUP02-CER-fixture-0001 \
  --source-repository "$SRC" \
  --artifact-glob 'output/*.pkg.tar.zst' \
  --input-source-glob 'sources/*' \
  --build-run-id build-run-fixture-bad-tree \
  --custodian-identity fixture-custodian \
  --immutable-locator-or-signed-envelope signed-envelope:fixture:bad-tree \
  --container-or-vm-image-digest sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb \
  --source-date-epoch 1700000000 \
  --out "$TMP/bad-tree-output" \
  -- bash -c 'exit 99' >/dev/null 2>&1; then
  echo 'recipe-tree drift unexpectedly accepted' >&2
  exit 1
fi

if GITHUB_TOKEN=secret python3 "$PRODUCER" \
  --request-issuance "$ISSUANCE" \
  --record-contract-issuance "$CONTRACTS" \
  --request-id SUP02-CER-fixture-0001 \
  --source-repository "$SRC" \
  --artifact-glob 'output/*.pkg.tar.zst' \
  --input-source-glob 'sources/*' \
  --build-run-id build-run-fixture-secret \
  --custodian-identity fixture-custodian \
  --immutable-locator-or-signed-envelope signed-envelope:fixture:secret \
  --container-or-vm-image-digest sha256:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc \
  --source-date-epoch 1700000000 \
  --environment-key GITHUB_TOKEN \
  --out "$TMP/secret-output" \
  -- bash -c 'exit 99' >/dev/null 2>&1; then
  echo 'secret-like environment key unexpectedly accepted' >&2
  exit 1
fi

after=$(git -C "$SRC" status --porcelain --untracked-files=no)
test -z "$after"

echo 'SUP02_CUSTODIAN_EXPORT_RESPONSE_PRODUCER_SMOKE=PASS'
