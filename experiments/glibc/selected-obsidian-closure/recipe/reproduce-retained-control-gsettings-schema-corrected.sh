#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
REPO=$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel)
B5_OUT=${B5_OUT:?set B5_OUT to the completed Phase B5 directory}
OUT=${OUT:?set OUT to a fresh corrected Phase B6 output directory}
BASE_RECIPE="$SCRIPT_DIR/reproduce-retained-control-gsettings-schema.py"

for command in git python cp mv mkdir grep awk wc cat; do
    command -v "$command" >/dev/null 2>&1 || {
        printf 'missing required command: %s\n' "$command" >&2
        exit 1
    }
done

tracked_dirty=$(git -C "$REPO" status --porcelain --untracked-files=no)
if [ -n "$tracked_dirty" ]; then
    printf 'tracked working-tree changes detected; corrected Phase B6 requires exact HEAD:\n' >&2
    printf '%s\n' "$tracked_dirty" >&2
    exit 2
fi

mkdir -p "$OUT"
OVERLAY="$OUT/.phase-b5-corrected-overlay"
mkdir -p "$OVERLAY"
cp -a "$B5_OUT"/. "$OVERLAY"/

python - "$B5_OUT" "$OVERLAY" "$OUT" <<'PY'
import csv, hashlib, pathlib, sys

source_root = pathlib.Path(sys.argv[1])
overlay = pathlib.Path(sys.argv[2])
out = pathlib.Path(sys.argv[3])

def rows(path):
    with path.open(newline='') as handle:
        return list(csv.DictReader(handle, delimiter='\t'))

def sha256(path):
    value = hashlib.sha256()
    with path.open('rb') as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b''):
            value.update(chunk)
    return value.hexdigest()

def rootfs_split(path):
    marker = '/rootfs/'
    text = str(path)
    if marker not in text:
        return None, None
    before, after = text.split(marker, 1)
    return pathlib.Path(before + '/rootfs'), '/' + after

aggregate_rows = [
    row for row in rows(source_root / 'data-object-verification.tsv')
    if row['semantic_class'] == 'PROVIDER_SCHEMA_DATA'
]
if len(aggregate_rows) != 1 or aggregate_rows[0]['identity_state'] != 'MATCH':
    raise SystemExit('expected one identity-matched schema aggregate')
aggregate = pathlib.Path(aggregate_rows[0]['path'])
schema_dir = aggregate.parent
rootfs, _ = rootfs_split(aggregate)
index = {}
if rootfs:
    for item in sorted((rootfs / 'var/lib/dpkg/info').glob('*.list')):
        package = item.name[:-5]
        for line in item.read_text(errors='replace').splitlines():
            if line.startswith('/'):
                index.setdefault(line, set()).add(package)

original = {row['source_path']: row for row in rows(source_root / 'schema-source-manifest.tsv')}
found = sorted(
    {path for pattern in ('*.xml', '*.gschema.override') for path in schema_dir.glob(pattern) if path.is_file()},
    key=lambda path: path.name,
)
if not found:
    raise SystemExit(f'no schema sources found in {schema_dir}')

fields = [
    'aggregate_path', 'source_kind', 'source_path', 'rootfs_relative_path',
    'sha256', 'dpkg_file_owners'
]
with (overlay / 'schema-source-manifest.tsv').open('w', newline='') as handle:
    writer = csv.DictWriter(handle, fields, delimiter='\t', lineterminator='\n')
    writer.writeheader()
    for path in found:
        _, relative = rootfs_split(path)
        owners = sorted(index.get(relative or '', set()))
        kind = 'OVERRIDE' if path.name.endswith('.gschema.override') else 'XML'
        writer.writerow({
            'aggregate_path': str(aggregate),
            'source_kind': kind,
            'source_path': str(path),
            'rootfs_relative_path': relative or '-',
            'sha256': sha256(path),
            'dpkg_file_owners': ','.join(owners) if owners else 'UNOWNED',
        })

current = {str(path) for path in found}
previous = set(original)
with (out / 'schema-source-manifest-delta.tsv').open('w', newline='') as handle:
    writer = csv.writer(handle, delimiter='\t', lineterminator='\n')
    writer.writerow(['state', 'source_path'])
    for value in sorted(current - previous):
        writer.writerow(['ADDED_BY_CORRECTED_DISCOVERY', value])
    for value in sorted(previous - current):
        writer.writerow(['MISSING_FROM_CURRENT_SCHEMA_DIR', value])
PY

if B5_OUT="$OVERLAY" OUT="$OUT" python "$BASE_RECIPE"; then
    base_rc=0
else
    base_rc=$?
fi

if [ "$base_rc" -ne 0 ]; then
    printf 'FAIL\n' >"$OUT/analysis.status"
    printf 'base_reproduction\n' >"$OUT/failure-stage.txt"
    exit "$base_rc"
fi

cp "$OUT/summary.tsv" "$OUT/raw-summary.tsv"
cp "$OUT/next-state.txt" "$OUT/raw-next-state.txt"

python - "$B5_OUT" "$OVERLAY" "$OUT" <<'PY'
import csv, pathlib, sys

b5 = pathlib.Path(sys.argv[1])
overlay = pathlib.Path(sys.argv[2])
out = pathlib.Path(sys.argv[3])

def read(path):
    with path.open(newline='') as handle:
        return list(csv.DictReader(handle, delimiter='\t'))

def count_errors(path):
    if not path.is_file():
        return 0
    return sum('Error on line' in line for line in path.read_text(errors='replace').splitlines())

original_sources = read(b5 / 'schema-source-manifest.tsv')
corrected_sources = read(overlay / 'schema-source-manifest.tsv')
delta = read(out / 'schema-source-manifest-delta.tsv')
attempts = read(out / 'schema-reproduction-attempts.tsv')

clean = 0
identical = 0
error_attempts = 0
for row in attempts:
    stderr = pathlib.Path(row['attempt_directory']) / 'stderr.txt'
    errors = count_errors(stderr)
    error_attempts += int(errors > 0)
    accepted = (
        row['execution_state'] == 'EXECUTED'
        and row['return_code'] == '0'
        and row['generated_present'] == 'YES'
        and errors == 0
    )
    clean += int(accepted)
    identical += int(accepted and row['byte_identical'] == 'YES')

if identical:
    next_state = 'READY_FOR_COMPLETE_DATA_MANIFEST'
elif clean:
    next_state = 'REVIEW_SCHEMA_COMPILER_VERSION_DIFFERENCE'
elif attempts:
    next_state = 'REVIEW_SCHEMA_COMPILATION_ERRORS'
else:
    next_state = 'ACQUIRE_SCHEMA_COMPILER_ORACLE'

raw = {row['field']: row['value'] for row in read(out / 'raw-summary.tsv')}
summary = [
    ('branch', raw.get('branch', '')),
    ('head', raw.get('head', '')),
    ('phase_b5_root', str(b5)),
    ('phase_b5_head', raw.get('phase_b5_head', '')),
    ('b5_schema_source_files', len(original_sources)),
    ('corrected_schema_source_files', len(corrected_sources)),
    ('sources_added_by_corrected_discovery', sum(row['state'] == 'ADDED_BY_CORRECTED_DISCOVERY' for row in delta)),
    ('b5_sources_missing_from_current_dir', sum(row['state'] == 'MISSING_FROM_CURRENT_SCHEMA_DIR' for row in delta)),
    ('compiler_candidates_present', raw.get('compiler_candidates_present', '0')),
    ('runnable_compiler_candidates', raw.get('runnable_compiler_candidates', '0')),
    ('compile_attempts', len(attempts)),
    ('clean_successful_compiles', clean),
    ('compilation_error_attempts', error_attempts),
    ('byte_identical_outputs', identical),
    ('runtime_launch_performed', 'NO'),
    ('promoted_runtime_mutated', 'NO'),
]
with (out / 'summary.tsv').open('w', newline='') as handle:
    writer = csv.writer(handle, delimiter='\t', lineterminator='\n')
    writer.writerow(['field', 'value'])
    writer.writerows(summary)
(out / 'next-state.txt').write_text(next_state + '\n')
(out / 'analysis.status').write_text('PASS\n')
(out / 'failure-stage.txt').unlink(missing_ok=True)
(out / 'claim-boundary.txt').write_text(
    'This corrected Phase B6 expands source discovery to all XML and override files in the retained schema directory.\n'
    'It records the delta from the incomplete Phase B5 suffix-filtered manifest.\n'
    'Return code zero is not accepted when compiler stderr reports schema errors or ignored files.\n'
    'Compilation remains receipt-local; no package, application, or promoted runtime is changed.\n'
)
PY

printf 'selected Obsidian corrected Phase B6 schema reproduction: PASS\n'
printf 'evidence: %s\n' "$OUT"
printf '\n===== summary =====\n'
cat "$OUT/summary.tsv"
printf '\n===== source manifest delta =====\n'
cat "$OUT/schema-source-manifest-delta.tsv"
printf '\n===== next state =====\n'
cat "$OUT/next-state.txt"
