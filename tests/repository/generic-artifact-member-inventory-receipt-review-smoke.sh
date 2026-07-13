#!/usr/bin/env bash
set -euo pipefail

REPO=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
BASE="$REPO/experiments/glibc/selected-obsidian-provider-authority"
REVIEWER="$BASE/recipe/review-generic-artifact-member-inventory.py"
RULES="$BASE/review/generic-artifact-member-inventory-review-rules.tsv"
REVIEW="$BASE/review/generic-artifact-member-inventory-receipt-review.tsv"
META="$BASE/review/generic-artifact-member-inventory-receipt-metadata.tsv"

fail() {
    printf 'generic artifact member inventory receipt review smoke: FAIL: %s\n' "$*" >&2
    exit 1
}

for path in "$REVIEWER" "$RULES" "$REVIEW" "$META"; do
    [ -f "$path" ] || fail "missing review input: $path"
done
[ -x "$REVIEWER" ] || fail "reviewer is not executable"
python3 -m py_compile "$REVIEWER"

python3 - "$RULES" "$REVIEW" "$META" <<'PY'
import csv
import hashlib
import sys
from collections import Counter
from pathlib import Path

rules_path, review_path, meta_path = map(Path, sys.argv[1:])

def read(path):
    with path.open(newline='', encoding='utf-8') as stream:
        return list(csv.DictReader(stream, delimiter='\t'))

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

rules = read(rules_path)
review = read(review_path)
meta = {row['field']: row['value'] for row in read(meta_path)}
assert len(rules) == 37
assert len(review) == 37
assert len({row['evidence_row_id'] for row in rules}) == 37
assert {row['evidence_row_id'] for row in review} == {row['evidence_row_id'] for row in rules}
assert all(row['review_policy'] == 'EXACT_OR_ALIAS_EVIDENCE_ONLY_NOT_AUTHORITY' for row in rules)
assert all(row['authority_state'] == 'CANDIDATE_ONLY' for row in rules)
counts = Counter(row['review_state'] for row in review)
assert counts == Counter({
    'EXACT_CONCRETE_MEMBER_AND_EXPECTED_SONAME_OBSERVED': 21,
    'EXPECTED_SONAME_ALIAS_SYMLINK_PRESENT_CONCRETE_FILENAME_DRIFT': 15,
    'EXPECTED_SONAME_ALIAS_NOT_OBSERVED_DIFFERENT_FAMILY_MEMBERS_PRESENT': 1,
})
assert all(row['artifact_to_recipe_binding_state'] == 'OPEN' for row in review)
assert all(row['termux_android_adaptation_state'] == 'OPEN' for row in review)
assert all(row['final_provider_state'] == 'UNRESOLVED' for row in review)
assert all(row['target_population_state'] == 'BLOCKED' for row in review)
assert meta['review_rules_sha256'] == digest(rules_path)
assert meta['review_receipt_sha256'] == digest(review_path)
assert meta['review_identity_rows'] == '37'
assert meta['authority_decisions_accepted'] == '0'
assert meta['target_rows_populated'] == '0'
by_label = {row['identity_label']: row for row in review}
assert by_label['libsqlite3.so.0.8.6']['review_state'] == 'EXPECTED_SONAME_ALIAS_SYMLINK_PRESENT_CONCRETE_FILENAME_DRIFT'
assert by_label['libsqlite3.so.0.8.6']['expected_soname_alias'] == 'libsqlite3.so.0'
assert by_label['libsqlite3.so.0.8.6']['alias_link_target'] == 'libsqlite3.so.3.49.1'
assert by_label['libjpeg.so.62.3.0']['review_state'] == 'EXPECTED_SONAME_ALIAS_NOT_OBSERVED_DIFFERENT_FAMILY_MEMBERS_PRESENT'
assert 'libjpeg.so.8' in by_label['libjpeg.so.62.3.0']['family_observed_basenames'].split(';')
PY

TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
python3 - "$TMP" <<'PY'
import csv
import sys
from pathlib import Path

root=Path(sys.argv[1])

def write(name, fields, rows):
    path=root/name
    with path.open('w', newline='', encoding='utf-8') as stream:
        writer=csv.DictWriter(stream, fieldnames=fields, delimiter='\t', lineterminator='\n')
        writer.writeheader(); writer.writerows(rows)

rules_fields=['evidence_row_id','capability_partition','identity_label','expected_soname_alias','family_member_prefix','review_policy','authority_state']
rules=[
 {'evidence_row_id':'selected:exact','capability_partition':'test','identity_label':'libfoo.so.1.0.0','expected_soname_alias':'libfoo.so.1','family_member_prefix':'libfoo.so','review_policy':'EXACT_OR_ALIAS_EVIDENCE_ONLY_NOT_AUTHORITY','authority_state':'CANDIDATE_ONLY'},
 {'evidence_row_id':'selected:drift','capability_partition':'test','identity_label':'libbar.so.2.9.0','expected_soname_alias':'libbar.so.2','family_member_prefix':'libbar.so','review_policy':'EXACT_OR_ALIAS_EVIDENCE_ONLY_NOT_AUTHORITY','authority_state':'CANDIDATE_ONLY'},
 {'evidence_row_id':'selected:absent','capability_partition':'test','identity_label':'libjpeg.so.62.3.0','expected_soname_alias':'libjpeg.so.62','family_member_prefix':'libjpeg.so','review_policy':'EXACT_OR_ALIAS_EVIDENCE_ONLY_NOT_AUTHORITY','authority_state':'CANDIDATE_ONLY'},
]
write('rules.tsv', rules_fields, rules)
obs_fields=['evidence_row_id','capability_partition','identity_label','artifact_id','package','version','architecture','expected_member_basename','exact_basename_match_count','observed_member_paths','observed_member_types','observed_elf_sonames','observed_member_sha256s','elf_observation_states','member_observation_state','object_member_binding_state','artifact_to_recipe_binding_state','termux_android_adaptation_state','final_provider_state','target_population_state']
base={'version':'1','architecture':'aarch64','object_member_binding_state':'OBSERVED_CANDIDATE_NOT_AUTHORITY_ACCEPTED','artifact_to_recipe_binding_state':'OPEN','termux_android_adaptation_state':'OPEN','final_provider_state':'UNRESOLVED','target_population_state':'BLOCKED'}
obs=[]
obs.append(base|{'evidence_row_id':'selected:exact','capability_partition':'test','identity_label':'libfoo.so.1.0.0','artifact_id':'artifact:foo','package':'foo','expected_member_basename':'libfoo.so.1.0.0','exact_basename_match_count':'1','observed_member_paths':'usr/lib/libfoo.so.1.0.0','observed_member_types':'REGULAR','observed_elf_sonames':'libfoo.so.1','observed_member_sha256s':'a'*64,'elf_observation_states':'ELF_SONAME_PARSED','member_observation_state':'UNIQUE_EXACT_BASENAME_MEMBER_OBSERVED'})
obs.append(base|{'evidence_row_id':'selected:drift','capability_partition':'test','identity_label':'libbar.so.2.9.0','artifact_id':'artifact:bar','package':'bar','expected_member_basename':'libbar.so.2.9.0','exact_basename_match_count':'0','observed_member_paths':'-','observed_member_types':'-','observed_elf_sonames':'-','observed_member_sha256s':'-','elf_observation_states':'-','member_observation_state':'NO_EXACT_BASENAME_MEMBER_OBSERVED'})
obs.append(base|{'evidence_row_id':'selected:absent','capability_partition':'test','identity_label':'libjpeg.so.62.3.0','artifact_id':'artifact:jpeg','package':'jpeg','expected_member_basename':'libjpeg.so.62.3.0','exact_basename_match_count':'0','observed_member_paths':'-','observed_member_types':'-','observed_elf_sonames':'-','observed_member_sha256s':'-','elf_observation_states':'-','member_observation_state':'NO_EXACT_BASENAME_MEMBER_OBSERVED'})
write('observations.tsv', obs_fields, obs)
inv_fields=['artifact_id','package','archive_kind','member_path','normalized_path','basename','member_type','mode_octal','uid','gid','size','link_target','exact_named_search_member','elf_parse_state','elf_class','elf_data','elf_machine','observed_soname','member_sha256']
def inv(artifact,package,path,basename,typ,target='-'):
    return {'artifact_id':artifact,'package':package,'archive_kind':'DATA','member_path':path,'normalized_path':path,'basename':basename,'member_type':typ,'mode_octal':'777' if typ=='SYMLINK' else '755','uid':'0','gid':'0','size':'0','link_target':target,'exact_named_search_member':'NO','elf_parse_state':'NOT_INSPECTED','elf_class':'-','elf_data':'-','elf_machine':'-','observed_soname':'-','member_sha256':'-'}
invrows=[
 inv('artifact:foo','foo','usr/lib/libfoo.so.1.0.0','libfoo.so.1.0.0','REGULAR'),
 inv('artifact:bar','bar','usr/lib/libbar.so.2','libbar.so.2','SYMLINK','libbar.so.2.8.0'),
 inv('artifact:bar','bar','usr/lib/libbar.so.2.8.0','libbar.so.2.8.0','REGULAR'),
 inv('artifact:jpeg','jpeg','usr/lib/libjpeg.so','libjpeg.so','SYMLINK','libjpeg.so.8'),
 inv('artifact:jpeg','jpeg','usr/lib/libjpeg.so.8','libjpeg.so.8','SYMLINK','libjpeg.so.8.3.2'),
 inv('artifact:jpeg','jpeg','usr/lib/libjpeg.so.8.3.2','libjpeg.so.8.3.2','REGULAR'),
]
write('inventory.tsv', inv_fields, invrows)
PY

python3 "$REVIEWER" \
    --rules "$TMP/rules.tsv" \
    --named-observations "$TMP/observations.tsv" \
    --data-inventory "$TMP/inventory.tsv" \
    --out "$TMP/out" \
    --expected-identities 3 \
    --expected-edges 3 >/dev/null
python3 - "$TMP/out/generic-artifact-member-inventory-receipt-review.tsv" <<'PY'
import csv, sys
from pathlib import Path
with Path(sys.argv[1]).open(newline='', encoding='utf-8') as stream:
    rows={row['evidence_row_id']:row for row in csv.DictReader(stream, delimiter='\t')}
assert rows['selected:exact']['review_state']=='EXACT_CONCRETE_MEMBER_AND_EXPECTED_SONAME_OBSERVED'
assert rows['selected:drift']['review_state']=='EXPECTED_SONAME_ALIAS_SYMLINK_PRESENT_CONCRETE_FILENAME_DRIFT'
assert rows['selected:absent']['review_state']=='EXPECTED_SONAME_ALIAS_NOT_OBSERVED_DIFFERENT_FAMILY_MEMBERS_PRESENT'
PY

cp "$TMP/observations.tsv" "$TMP/bad-observations.tsv"
sed -i 's/libfoo\.so\.1\t/libfoo.so.9\t/' "$TMP/bad-observations.tsv"
if python3 "$REVIEWER" \
    --rules "$TMP/rules.tsv" \
    --named-observations "$TMP/bad-observations.tsv" \
    --data-inventory "$TMP/inventory.tsv" \
    --out "$TMP/bad-out" \
    --expected-identities 3 \
    --expected-edges 3 >/dev/null 2>&1; then
    fail "reviewer accepted exact-member SONAME mismatch"
fi

printf 'generic artifact member inventory receipt review smoke: PASS\n'
