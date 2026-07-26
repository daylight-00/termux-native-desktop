#!/usr/bin/env python3
import argparse
import csv
import hashlib
from pathlib import Path

FIELDS = [
    'review_id', 'decision', 'source_members_sha256', 'source_gaps_sha256',
    'source_review_metadata_sha256', 'accepted_provider_root_count',
    'accepted_member_count', 'included_member_count', 'deferred_member_count',
    'active_gap_count', 'accepted_soname_collision_count',
    'accepted_alias_collision_count', 'included_scope', 'deferred_scope',
    'ordering_boundary', 'alias_boundary', 'atomic_family_boundary',
    'capability_exclusion_boundary', 'update_boundary', 'rollback_boundary',
    'target_manifest_state', 'target_population_state', 'materialization_state',
    'deployment_state', 'activation_state', 'next_action', 'authority_effect',
    'prohibited_inference',
]


def read(path: Path):
    with path.open(newline='', encoding='utf-8') as handle:
        return list(csv.DictReader(handle, delimiter='\t'))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo-root', type=Path, required=True)
    parser.add_argument('--output-root', type=Path, required=True)
    args = parser.parse_args()

    root = args.repo_root.resolve()
    review = root / 'experiments/glibc/selected-obsidian-provider-authority/review'
    members = review / 'selected-provider-composition-members.tsv'
    gaps = review / 'selected-provider-composition-gaps.tsv'
    metadata = review / 'selected-provider-composition-metadata.tsv'

    member_rows = read(members)
    gap_rows = read(gaps)
    meta = {row['key']: row['value'] for row in read(metadata)}

    if len(member_rows) != 42 or gap_rows:
        raise SystemExit('composition set is not exact 42/0')
    if sum(row['composition_inclusion'].startswith('INCLUDED_') for row in member_rows) != 41:
        raise SystemExit('included member count mismatch')
    deferred = [row for row in member_rows if row['composition_inclusion'] == 'DEFERRED_PROFILE_REQUIREMENT_OPEN']
    if len(deferred) != 1 or deferred[0]['member_basename'] != 'libtasn1.so.6.6.4':
        raise SystemExit('deferred libtasn1 boundary mismatch')
    if len({row['soname'] for row in member_rows}) != 42:
        raise SystemExit('SONAME collision')
    if len({row['alias_basename'] for row in member_rows}) != 42:
        raise SystemExit('alias collision')

    expected = {
        'accepted_provider_root_count': '31',
        'accepted_member_count': '42',
        'included_member_count': '41',
        'deferred_member_count': '1',
        'unresolved_selected_identity_count': '0',
        'accepted_soname_collision_count': '0',
        'accepted_alias_collision_count': '0',
    }
    for key, value in expected.items():
        if meta.get(key) != value:
            raise SystemExit(f'metadata mismatch: {key}')

    row = {
        'review_id': 'SELECTED-COMPOSITION-ACCEPT-001',
        'decision': 'ACCEPTED_BOUNDED_COMPLETE_SELECTED_PROVIDER_COMPOSITION',
        'source_members_sha256': 'ce60f71248db0568f52a1230b086f6af272555fff6187a3ca1a76c83014e2e70',
        'source_gaps_sha256': '14568107bbe4f28f101a31488b93db1920365c1893edc6d47d4d6530aff86673',
        'source_review_metadata_sha256': '14e340dbd8f5d1ec4f72e0ccf287810d02a60486cb50e78fcb13987035251dde',
        'accepted_provider_root_count': '31',
        'accepted_member_count': '42',
        'included_member_count': '41',
        'deferred_member_count': '1',
        'active_gap_count': '0',
        'accepted_soname_collision_count': '0',
        'accepted_alias_collision_count': '0',
        'included_scope': 'EXACT_41_MEMBER_SELECTED_GTK_AND_TRANSITIVE_RUNTIME_SET',
        'deferred_scope': 'EXACT_LIBTASN1_SO_6_6_4_RETAINED_PROVIDER_EXCLUDED_UNTIL_GNUTLS_SECURITY_OR_PRINTING_PROFILE_SELECTION',
        'ordering_boundary': 'DETERMINISTIC_REVIEW_ROW_ORDER_ACCEPTED_ONLY_NO_FILESYSTEM_COPY_ORDER_OR_DYNAMIC_LOADER_SEARCH_ORDER_DECIDED',
        'alias_boundary': 'EXACT_42_UNIQUE_SONAME_ALIAS_IDENTITIES_ACCEPTED_AS_COMPOSITION_DECISIONS_NO_TARGET_PATHS_CREATED',
        'atomic_family_boundary': 'PANGO_THREE_MEMBER_CAIRO_TWO_MEMBER_AT_SPI2_THREE_MEMBER_AND_GDK_GTK_TWO_MEMBER_FAMILIES_REMAIN_ATOMIC',
        'capability_exclusion_boundary': 'PACKAGE_WIDE_DEV_TOOLS_MODULES_SCHEMAS_PRINT_BACKENDS_SERVICES_DATA_GIR_TYPELIB_TARGET_MEMBERSHIP_AND_DEFERRED_LIBTASN1_EXCLUDED',
        'update_boundary': 'REVIEW_ANY_MEMBER_SHA_VERSION_SONAME_ALIAS_INCLUSION_CAPABILITY_ATOMICITY_PROVIDER_OR_DEPENDENCY_CHANGE_AS_NEW_CLASS_D_COMPOSITION',
        'rollback_boundary': 'BEFORE_TARGET_MANIFEST_REVOKE_ACCEPTANCE;AFTER_FUTURE_MATERIALIZATION_REVERSE_WHOLE_IMMUTABLE_COMPOSITION_GENERATION_WITH_ATOMIC_FAMILIES_INTACT',
        'target_manifest_state': 'NOT_GENERATED_SEPARATE_NON_MUTATING_REVIEW_REQUIRED',
        'target_population_state': 'NOT_AUTHORIZED',
        'materialization_state': 'NOT_AUTHORIZED',
        'deployment_state': 'NOT_AUTHORIZED',
        'activation_state': 'NOT_AUTHORIZED',
        'next_action': 'generate-and-review-non-mutating-selected-target-manifest',
        'authority_effect': 'BOUNDED_APPLICATION_RUNTIME_COMPOSITION_ACCEPTED_NO_TARGET_MEMBERSHIP_PATH_POPULATION_MATERIALIZATION_DEPLOYMENT_OR_ACTIVATION',
        'prohibited_inference': 'COMPOSITION_ACCEPTANCE_DOES_NOT_ACCEPT_PACKAGE_WIDE_SURFACES_DEFERRED_LIBTASN1_CURRENT_MEMBERSHIP_TARGET_PATHS_COPY_INSTALL_LOADER_POLICY_SERVICE_MODULE_SCHEMA_PRINT_DISPLAY_DEPLOYMENT_OR_ACTIVATION',
    }

    if sha256(members) != row['source_members_sha256']:
        raise SystemExit('review member table digest mismatch')
    if sha256(gaps) != row['source_gaps_sha256']:
        raise SystemExit('review gap table digest mismatch')

    output = args.output_root / 'experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-composition-boundary-acceptance.tsv'
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('w', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, delimiter='\t', fieldnames=FIELDS, lineterminator='\n')
        writer.writeheader()
        writer.writerow(row)


if __name__ == '__main__':
    main()
