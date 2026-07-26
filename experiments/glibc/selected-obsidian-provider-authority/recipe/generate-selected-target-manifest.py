#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path, PurePosixPath

BASE = Path('experiments/glibc/selected-obsidian-provider-authority')
REVIEW = BASE / 'review'
COMPOSITION = REVIEW / 'selected-provider-composition-members.tsv'
ACCEPTANCE = REVIEW / 'selected-provider-composition-boundary-acceptance.tsv'
MANIFEST = REVIEW / 'selected-target-manifest.tsv'
OBJECTS = REVIEW / 'selected-target-manifest-object-bindings.tsv'
ALIASES = REVIEW / 'selected-target-manifest-alias-bindings.tsv'
COLLISIONS = REVIEW / 'selected-target-manifest-collisions.tsv'
METADATA = REVIEW / 'selected-target-manifest-metadata.tsv'

MANIFEST_FIELDS = [
    'target_record_id', 'application_composition_id', 'provider_object_id',
    'application_identity_key', 'supply_artifact_id', 'source_artifact_member_path',
    'target_domain', 'target_relative_path', 'target_node_type', 'target_mode_policy',
    'target_owner_policy', 'target_mutability', 'target_alias_class',
    'target_collision_policy', 'update_domain', 'rollback_domain',
    'validation_gate_ids', 'authority_issue_ids', 'authority_acceptance_state',
    'population_state'
]
OBJECT_FIELDS = [
    'provider_object_id', 'composition_row_id', 'provider_review_id', 'recipe_root',
    'artifact_package', 'artifact_version', 'member_basename', 'member_sha256',
    'soname', 'binding_state', 'authority_effect'
]
ALIAS_FIELDS = [
    'alias_target_record_id', 'alias_relative_path', 'concrete_target_record_id',
    'concrete_relative_path', 'alias_class', 'alias_target_basename',
    'resolution_state', 'authority_effect'
]
COLLISION_FIELDS = [
    'collision_id', 'target_relative_path', 'first_target_record_id',
    'second_target_record_id', 'collision_class', 'resolution_state',
    'authority_effect'
]

COMPOSITION_ID = 'SELECTED-COMPOSITION-ACCEPT-001'
REVIEW_ID = 'SELECTED-TARGET-MANIFEST-REVIEW-001'


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline='', encoding='utf-8') as fh:
        return list(csv.DictReader(fh, delimiter='\t'))


def write_tsv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', newline='', encoding='utf-8') as fh:
        writer = csv.DictWriter(fh, fieldnames=fields, delimiter='\t', lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


def stable_id(prefix: str, *parts: str) -> str:
    digest = hashlib.sha256('\0'.join(parts).encode('utf-8')).hexdigest()[:24]
    return f'{prefix}:{digest}'


def validate_relative_path(value: str) -> None:
    path = PurePosixPath(value)
    if not value or value.startswith('/') or value.endswith('/'):
        raise SystemExit(f'invalid target path: {value!r}')
    if any(part in ('', '.', '..') for part in path.parts):
        raise SystemExit(f'unsafe target path: {value!r}')
    if str(path) != value:
        raise SystemExit(f'non-normalized target path: {value!r}')


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo-root', type=Path, default=Path.cwd())
    parser.add_argument('--output-root', type=Path)
    args = parser.parse_args()

    repo = args.repo_root.resolve()
    out = args.output_root.resolve() if args.output_root else repo
    composition = read_tsv(repo / COMPOSITION)
    acceptance = read_tsv(repo / ACCEPTANCE)
    if len(acceptance) != 1:
        raise SystemExit('expected one composition acceptance row')
    accepted = acceptance[0]
    if accepted['review_id'] != COMPOSITION_ID:
        raise SystemExit('unexpected composition acceptance id')
    if accepted['decision'] != 'ACCEPTED_BOUNDED_COMPLETE_SELECTED_PROVIDER_COMPOSITION':
        raise SystemExit('composition is not accepted')

    included = [r for r in composition if r['composition_inclusion'] != 'DEFERRED_PROFILE_REQUIREMENT_OPEN']
    deferred = [r for r in composition if r['composition_inclusion'] == 'DEFERRED_PROFILE_REQUIREMENT_OPEN']
    if len(composition) != 42 or len(included) != 41 or len(deferred) != 1:
        raise SystemExit('expected 42 composition rows split 41 included / 1 deferred')
    if deferred[0]['member_basename'] != 'libtasn1.so.6.6.4':
        raise SystemExit('unexpected deferred composition member')

    manifest_rows: list[dict[str, str]] = []
    object_rows: list[dict[str, str]] = []
    alias_rows: list[dict[str, str]] = []
    path_owner: dict[str, str] = {}
    collisions: list[dict[str, str]] = []

    for row in sorted(included, key=lambda r: r['composition_row_id']):
        member = row['member_basename']
        alias = row['alias_basename']
        alias_target = row['alias_target_basename']
        if member != alias_target:
            raise SystemExit(f'alias target does not match concrete member: {row["composition_row_id"]}')
        if alias == member:
            raise SystemExit(f'alias and member basenames collide: {member}')
        object_id = f'object:{row["member_sha256"][:24]}'
        concrete_path = f'lib/{member}'
        alias_path = f'lib/{alias}'
        validate_relative_path(concrete_path)
        validate_relative_path(alias_path)
        concrete_id = stable_id('target', COMPOSITION_ID, row['composition_row_id'], 'REGULAR', concrete_path)
        alias_id = stable_id('target', COMPOSITION_ID, row['composition_row_id'], 'SYMLINK', alias_path)
        gates = f'{COMPOSITION_ID};{REVIEW_ID}'

        common = {
            'application_composition_id': COMPOSITION_ID,
            'provider_object_id': object_id,
            'application_identity_key': '-',
            'supply_artifact_id': '-',
            'source_artifact_member_path': '-',
            'target_domain': 'SHARED_PROVIDER',
            'target_owner_policy': 'PROVIDER_OWNER',
            'target_mutability': 'IMMUTABLE',
            'target_collision_policy': 'ERROR',
            'update_domain': 'GENERIC_PROVIDER_UPDATE',
            'rollback_domain': 'PROVIDER',
            'validation_gate_ids': gates,
            'authority_issue_ids': 'TARGET-MANIFEST-ACCEPTANCE-OPEN',
            'authority_acceptance_state': 'PROVISIONAL_BLOCKED',
            'population_state': 'UNPOPULATED_SCHEMA_ONLY',
        }
        concrete = dict(common)
        concrete.update({
            'target_record_id': concrete_id,
            'target_relative_path': concrete_path,
            'target_node_type': 'REGULAR',
            'target_mode_policy': 'IMMUTABLE_READONLY',
            'target_alias_class': 'NONE',
        })
        alias_row = dict(common)
        alias_row.update({
            'target_record_id': alias_id,
            'target_relative_path': alias_path,
            'target_node_type': 'SYMLINK',
            'target_mode_policy': 'DOMAIN_DEFAULT',
            'target_alias_class': 'SONAME_RUNTIME_ALIAS',
        })
        manifest_rows.extend([concrete, alias_row])

        object_rows.append({
            'provider_object_id': object_id,
            'composition_row_id': row['composition_row_id'],
            'provider_review_id': row['provider_review_id'],
            'recipe_root': row['recipe_root'],
            'artifact_package': row['artifact_package'],
            'artifact_version': row['artifact_version'],
            'member_basename': member,
            'member_sha256': row['member_sha256'],
            'soname': row['soname'],
            'binding_state': 'CONTENT_ADDRESSED_COMPOSITION_LOCAL_CANONICAL_BINDING',
            'authority_effect': 'TARGET_REVIEW_REFERENCE_ONLY_NO_NEW_PROVIDER_OR_SUPPLY_AUTHORITY',
        })
        alias_rows.append({
            'alias_target_record_id': alias_id,
            'alias_relative_path': alias_path,
            'concrete_target_record_id': concrete_id,
            'concrete_relative_path': concrete_path,
            'alias_class': 'SONAME_RUNTIME_ALIAS',
            'alias_target_basename': alias_target,
            'resolution_state': 'RESOLVED_TO_EXACT_INCLUDED_CONCRETE_MEMBER',
            'authority_effect': 'REVIEWED_RELATION_ONLY_NO_SYMLINK_CREATED',
        })

        for target_path, target_id in ((concrete_path, concrete_id), (alias_path, alias_id)):
            if target_path in path_owner:
                collisions.append({
                    'collision_id': stable_id('collision', target_path, path_owner[target_path], target_id),
                    'target_relative_path': target_path,
                    'first_target_record_id': path_owner[target_path],
                    'second_target_record_id': target_id,
                    'collision_class': 'DUPLICATE_TARGET_PATH',
                    'resolution_state': 'UNRESOLVED_BLOCKING',
                    'authority_effect': 'BLOCKS_TARGET_MANIFEST_QUALIFICATION',
                })
            else:
                path_owner[target_path] = target_id

    manifest_rows.sort(key=lambda r: (r['target_relative_path'], r['target_node_type'], r['target_record_id']))
    object_rows.sort(key=lambda r: r['composition_row_id'])
    alias_rows.sort(key=lambda r: r['alias_relative_path'])

    if len(manifest_rows) != 82 or len(object_rows) != 41 or len(alias_rows) != 41:
        raise SystemExit('unexpected target manifest row counts')
    if collisions:
        raise SystemExit(f'blocking target collisions: {len(collisions)}')
    if len(path_owner) != 82:
        raise SystemExit('target path uniqueness failure')
    if len({r['target_record_id'] for r in manifest_rows}) != 82:
        raise SystemExit('target record id collision')
    if len({r['provider_object_id'] for r in object_rows}) != 41:
        raise SystemExit('provider object id collision')

    atomic_expected = {
        'ATSPI2-CORE-PROV-001': 3,
        'CAIRO-PROV-001': 2,
        'GTK3-CORE-PROV-001': 2,
        'PANGO-PROV-001': 3,
    }
    for review_id, count in atomic_expected.items():
        if sum(r['provider_review_id'] == review_id for r in object_rows) != count:
            raise SystemExit(f'atomic family incomplete: {review_id}')

    metadata = [
        ('schema_version', '1'),
        ('review_id', REVIEW_ID),
        ('application_composition_id', COMPOSITION_ID),
        ('decision', 'QUALIFIED_NON_MUTATING_SELECTED_TARGET_MANIFEST'),
        ('composition_member_count', '42'),
        ('included_concrete_member_count', '41'),
        ('deferred_member_count', '1'),
        ('target_manifest_row_count', '82'),
        ('regular_target_row_count', '41'),
        ('soname_alias_target_row_count', '41'),
        ('unique_target_path_count', '82'),
        ('target_path_collision_count', '0'),
        ('unresolved_alias_count', '0'),
        ('target_domain', 'SHARED_PROVIDER'),
        ('target_relative_root', 'lib'),
        ('authority_acceptance_state', 'PROVISIONAL_BLOCKED'),
        ('population_state', 'UNPOPULATED_SCHEMA_ONLY'),
        ('target_population_authorized', 'NO'),
        ('materialization_authorized', 'NO'),
        ('deployment_authorized', 'NO'),
        ('activation_authorized', 'NO'),
        ('next_review_tranche', 'NON_MUTATING_SELECTED_TARGET_MANIFEST_BOUNDARY_ACCEPTANCE'),
        ('authority_effect', 'DETERMINISTIC_TARGET_REVIEW_ONLY_NO_COPY_INSTALL_POPULATION_MATERIALIZATION_DEPLOYMENT_OR_ACTIVATION'),
    ]

    write_tsv(out / MANIFEST, MANIFEST_FIELDS, manifest_rows)
    write_tsv(out / OBJECTS, OBJECT_FIELDS, object_rows)
    write_tsv(out / ALIASES, ALIAS_FIELDS, alias_rows)
    write_tsv(out / COLLISIONS, COLLISION_FIELDS, collisions)
    write_tsv(out / METADATA, ['key', 'value'], [{'key': k, 'value': v} for k, v in metadata])


if __name__ == '__main__':
    main()
