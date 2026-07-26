#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

BASE = Path('experiments/glibc/selected-obsidian-provider-authority')
REVIEW = BASE / 'review'
DESIGN_ID = 'SELECTED-PROVIDER-MATERIALIZER-DESIGN-REVIEW-001'
ACCEPTANCE_GATE = 'SELECTED-PROVIDER-MATERIALIZER-DESIGN-ACCEPTANCE-OPEN'
NEXT_ACTION = 'review-and-accept-read-only-selected-provider-materializer-runtime-preflight-design-boundary'
GENERATION_BASE = '/data/data/com.termux/files/home/.local/state/termux-native-desktop/selected-provider-runtime'
FINAL_PREFLIGHT_BYTES = 59_142_800
RECEIPT_RESERVATION_BYTES = 1_048_576
EXACT_MEMBER_BYTES = 29_047_112

SOURCE_PATHS = {
    'composition_members': REVIEW / 'selected-provider-composition-members.tsv',
    'composition_acceptance': REVIEW / 'selected-provider-composition-boundary-acceptance.tsv',
    'target_manifest': REVIEW / 'selected-target-manifest.tsv',
    'object_bindings': REVIEW / 'selected-target-manifest-object-bindings.tsv',
    'alias_bindings': REVIEW / 'selected-target-manifest-alias-bindings.tsv',
    'target_acceptance': REVIEW / 'selected-target-manifest-boundary-acceptance.tsv',
    'indexed_supply': REVIEW / 'selected-target-indexed-replacement-review.tsv',
    'size_census': REVIEW / 'selected-target-member-size-census.tsv',
    'pixman_evidence': REVIEW / 'selected-target-pixman-size-evidence.tsv',
    'resource_budget': REVIEW / 'selected-target-resource-budget-metadata.tsv',
    'generation_contracts': REVIEW / 'selected-target-generation-root-contract-review.tsv',
    'intervention_lift': REVIEW / 'selected-target-population-intervention-lift-review.tsv',
    'receipt_prototype': REVIEW / 'selected-target-verification-receipt-prototype.json',
}

OBJECT_PLAN = REVIEW / 'selected-target-materializer-object-plan.tsv'
INPUT_CONTRACT = REVIEW / 'selected-target-materializer-input-contract.tsv'
STATE_MACHINE = REVIEW / 'selected-target-materializer-state-machine.tsv'
OPERATIONS = REVIEW / 'selected-target-materializer-operation-contract.tsv'
PREFLIGHT = REVIEW / 'selected-target-runtime-preflight-contract.tsv'
VERIFICATION = REVIEW / 'selected-target-materializer-verification-contract.tsv'
RECOVERY = REVIEW / 'selected-target-materializer-publication-recovery-contract.tsv'
DESIGN_JSON = REVIEW / 'selected-target-materializer-runtime-preflight-design.json'
METADATA = REVIEW / 'selected-target-materializer-design-metadata.tsv'

OBJECT_FIELDS = [
    'plan_row_id', 'sequence', 'composition_row_id', 'provider_object_id',
    'provider_review_id', 'artifact_package', 'artifact_version', 'member_basename',
    'member_sha256', 'member_size_bytes', 'soname', 'target_relative_path',
    'alias_relative_path', 'alias_target_basename', 'atomic_family_id',
    'supply_closure_kind', 'supply_result_remote', 'supply_drive_file_id',
    'supply_result_sha256', 'supply_result_index_sha256', 'artifact_evidence_path',
    'member_evidence_path', 'object_store_relative_path',
    'generation_regular_relative_path', 'generation_alias_relative_path',
    'localization_requirement', 'object_materialization_policy', 'alias_policy',
    'design_state', 'authority_effect', 'prohibited_inference'
]
INPUT_FIELDS = [
    'input_id', 'input_class', 'source_path', 'source_sha256',
    'required_identity_or_count', 'validation_rule', 'consumption_mode',
    'failure_action', 'current_mutation_effect', 'authority_effect',
    'prohibited_inference'
]
STATE_FIELDS = [
    'state_id', 'phase_order', 'state_name', 'state_class', 'entry_requirements',
    'permitted_effects', 'required_checks', 'success_transition',
    'failure_transition', 'resume_rule', 'authorization_gate',
    'current_authority_state', 'prohibited_inference'
]
OP_FIELDS = [
    'step_id', 'sequence', 'operation', 'input_contract', 'output_contract',
    'mutation_class', 'path_scope', 'precondition', 'verification',
    'fsync_or_atomic_rule', 'rollback_or_failure_rule', 'authorization_gate',
    'current_authority_state', 'prohibited_inference'
]
PREFLIGHT_FIELDS = [
    'check_id', 'sequence', 'category', 'subject', 'required_rule',
    'pass_evidence', 'failure_code', 'timing', 'current_execution_state',
    'authority_effect', 'prohibited_inference'
]
VERIFY_FIELDS = [
    'verification_id', 'sequence', 'stage', 'subject', 'exact_rule',
    'receipt_field', 'failure_action', 'publication_blocking',
    'current_execution_state', 'authority_effect', 'prohibited_inference'
]
RECOVERY_FIELDS = [
    'contract_id', 'sequence', 'category', 'normal_path', 'atomic_boundary',
    'crash_window_state', 'recovery_action', 'deletion_policy',
    'authorization_gate', 'current_authority_state', 'prohibited_inference'
]

ATOMIC_PROVIDERS = {
    'ATSPI2-CORE-PROV-001': 'ATOMIC-ATSPI2-3',
    'CAIRO-PROV-001': 'ATOMIC-CAIRO-2',
    'PANGO-PROV-001': 'ATOMIC-PANGO-3',
    'GTK3-CORE-PROV-001': 'ATOMIC-GDK-GTK-2',
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline='', encoding='utf-8') as fh:
        return list(csv.DictReader(fh, delimiter='\t'))


def write_tsv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', newline='', encoding='utf-8') as fh:
        writer = csv.DictWriter(fh, fieldnames=fields, delimiter='\t', lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


def kv(path: Path) -> dict[str, str]:
    return {r['key']: r['value'] for r in read_tsv(path)}


def row(**kwargs: str) -> dict[str, str]:
    return kwargs


def validate_sources(repo: Path) -> dict[str, object]:
    p = {k: repo / v for k, v in SOURCE_PATHS.items()}
    composition = read_tsv(p['composition_members'])
    included = [r for r in composition if r['composition_inclusion'] != 'DEFERRED_PROFILE_REQUIREMENT_OPEN']
    if len(composition) != 42 or len(included) != 41:
        raise SystemExit('expected 42 composition rows / 41 included')
    comp_accept = read_tsv(p['composition_acceptance'])
    if len(comp_accept) != 1 or comp_accept[0]['decision'] != 'ACCEPTED_BOUNDED_COMPLETE_SELECTED_PROVIDER_COMPOSITION':
        raise SystemExit('composition acceptance missing')
    manifest = read_tsv(p['target_manifest'])
    regular = [r for r in manifest if r['target_node_type'] == 'REGULAR']
    symlinks = [r for r in manifest if r['target_node_type'] == 'SYMLINK']
    if len(manifest) != 82 or len(regular) != 41 or len(symlinks) != 41:
        raise SystemExit('target manifest count mismatch')
    if any(r['population_state'] != 'UNPOPULATED_SCHEMA_ONLY' for r in manifest):
        raise SystemExit('target manifest unexpectedly populated')
    objects = read_tsv(p['object_bindings'])
    aliases = read_tsv(p['alias_bindings'])
    if len(objects) != 41 or len(aliases) != 41:
        raise SystemExit('object or alias count mismatch')
    target_accept = read_tsv(p['target_acceptance'])
    if len(target_accept) != 1 or target_accept[0]['decision'] != 'ACCEPTED_BOUNDED_NON_MUTATING_SELECTED_TARGET_MANIFEST':
        raise SystemExit('target policy acceptance missing')
    indexed = read_tsv(p['indexed_supply'])
    if len(indexed) != 41 or any(r['coordinate_state'] != 'CLOSED' for r in indexed):
        raise SystemExit('indexed supply coordinate closure incomplete')
    if any(not r['index_state'].startswith('CLOSED_') for r in indexed):
        raise SystemExit('indexed supply index closure incomplete')
    sizes = read_tsv(p['size_census'])
    nonempty = [r for r in sizes if r['member_size']]
    open_rows = [r for r in sizes if not r['member_size']]
    if len(sizes) != 41 or len(nonempty) != 40 or len(open_rows) != 1:
        raise SystemExit('historical size census split mismatch')
    pixman = read_tsv(p['pixman_evidence'])
    if len(pixman) != 1 or pixman[0]['member_basename'] != open_rows[0]['member_basename']:
        raise SystemExit('Pixman evidence does not close the one historical size gap')
    exact_total = sum(int(r['member_size']) for r in nonempty) + int(pixman[0]['member_size'])
    if exact_total != EXACT_MEMBER_BYTES:
        raise SystemExit(f'exact member byte total mismatch: {exact_total}')
    budget = kv(p['resource_budget'])
    if budget.get('exact_member_size_count') != '41' or budget.get('final_resource_preflight_bytes') != str(FINAL_PREFLIGHT_BYTES):
        raise SystemExit('resource budget metadata mismatch')
    if budget.get('receipt_overhead_budget_bytes') != str(RECEIPT_RESERVATION_BYTES):
        raise SystemExit('receipt reservation mismatch')
    generation = read_tsv(p['generation_contracts'])
    if len(generation) != 7 or any(r['review_state'] != 'BOUNDED_CONTRACT_DEFINED' for r in generation):
        raise SystemExit('generation contracts incomplete')
    lift = read_tsv(p['intervention_lift'])
    if len(lift) != 10 or any(r['review_result'] != 'SATISFIED_FOR_READ_ONLY_MATERIALIZER_DESIGN_REVIEW' for r in lift):
        raise SystemExit('design-only intervention gate not satisfied')
    receipt = json.loads(p['receipt_prototype'].read_text(encoding='utf-8'))
    if receipt.get('object_count') != 41 or receipt.get('alias_count') != 41:
        raise SystemExit('receipt prototype counts mismatch')
    return {
        'paths': p, 'composition': composition, 'included': included,
        'manifest': manifest, 'regular': regular, 'objects': objects,
        'aliases': aliases, 'indexed': indexed, 'sizes': sizes,
        'pixman': pixman[0], 'budget': budget, 'generation': generation,
        'lift': lift, 'receipt': receipt,
    }


def build_object_plan(data: dict[str, object]) -> list[dict[str, str]]:
    objects = {r['composition_row_id']: r for r in data['objects']}  # type: ignore[index]
    included = {r['composition_row_id']: r for r in data['included']}  # type: ignore[index]
    regular_by_object = {r['provider_object_id']: r for r in data['regular']}  # type: ignore[index]
    aliases_by_concrete = {r['concrete_target_record_id']: r for r in data['aliases']}  # type: ignore[index]
    indexed_by_sha = {r['member_sha256']: r for r in data['indexed']}  # type: ignore[index]
    sizes_by_sha = {r['member_sha256']: r for r in data['sizes']}  # type: ignore[index]
    pixman = data['pixman']  # type: ignore[assignment]
    rows: list[dict[str, str]] = []
    candidates: list[tuple[str, dict[str, str], dict[str, str], dict[str, str], dict[str, str], dict[str, str]]] = []
    for comp_id, obj in objects.items():
        comp = included[comp_id]
        reg = regular_by_object[obj['provider_object_id']]
        alias = aliases_by_concrete[reg['target_record_id']]
        idx = indexed_by_sha[obj['member_sha256']]
        candidates.append((reg['target_relative_path'], obj, comp, reg, alias, idx))
    for seq, (_, obj, comp, reg, alias, idx) in enumerate(sorted(candidates), 1):
        size_row = sizes_by_sha[obj['member_sha256']]
        size = size_row['member_size']
        if not size:
            if obj['member_sha256'] != pixman['member_sha256']:
                raise SystemExit('unexpected blank size outside Pixman')
            size = pixman['member_size']
        atomic = ATOMIC_PROVIDERS.get(obj['provider_review_id'], f"SINGLE-{obj['provider_object_id']}")
        sha = obj['member_sha256']
        rows.append({
            'plan_row_id': f'MAT-OBJ-{seq:03d}',
            'sequence': str(seq),
            'composition_row_id': obj['composition_row_id'],
            'provider_object_id': obj['provider_object_id'],
            'provider_review_id': obj['provider_review_id'],
            'artifact_package': obj['artifact_package'],
            'artifact_version': obj['artifact_version'],
            'member_basename': obj['member_basename'],
            'member_sha256': sha,
            'member_size_bytes': size,
            'soname': obj['soname'],
            'target_relative_path': reg['target_relative_path'],
            'alias_relative_path': alias['alias_relative_path'],
            'alias_target_basename': alias['alias_target_basename'],
            'atomic_family_id': atomic,
            'supply_closure_kind': idx['closure_kind'],
            'supply_result_remote': idx['replacement_result_remote'],
            'supply_drive_file_id': idx['replacement_drive_file_id'],
            'supply_result_sha256': idx['replacement_result_sha256'],
            'supply_result_index_sha256': idx['replacement_result_index_sha256'],
            'artifact_evidence_path': idx['artifact_evidence_path'],
            'member_evidence_path': idx['member_evidence_path'],
            'object_store_relative_path': f'objects/sha256/{sha[:2]}/{sha}',
            'generation_regular_relative_path': reg['target_relative_path'],
            'generation_alias_relative_path': alias['alias_relative_path'],
            'localization_requirement': 'SEPARATE_FUTURE_LOCAL_READ_ONLY_SUPPLY_MAP_BINDS_EXACT_REGULAR_FILE_PATH_OUTER_SHA_RESULT_INDEX_AND_CONTAINER_MEMBER_LOCATOR',
            'object_materialization_policy': 'STREAM_EXACT_MEMBER_TO_O_EXCL_NOFOLLOW_TEMP_VERIFY_SIZE_SHA_ELF_SONAME_THEN_FSYNC_CHMOD_0444_RENAME_TO_CONTENT_ADDRESS_NO_COPY_FALLBACK',
            'alias_policy': 'CREATE_ONLY_AFTER_ALL_41_REGULARS_AND_ATOMIC_FAMILIES_VERIFY_RELATIVE_BASENAME_TARGET_NO_ABSOLUTE_OR_PARENT_COMPONENT',
            'design_state': 'QUALIFIED_NON_EXECUTING_PLAN_ROW',
            'authority_effect': 'READ_ONLY_DESIGN_ROW_ONLY_NO_LOCALIZATION_EXTRACTION_COPY_LINK_SYMLINK_OR_WRITE',
            'prohibited_inference': 'PLAN_ROW_DOES_NOT_AUTHORIZE_PROVIDER_DOWNLOAD_LOCALIZATION_BYTE_READ_EXTRACTION_OBJECT_STORE_CREATION_GENERATION_WRITE_POPULATION_PUBLICATION_DEPLOYMENT_OR_ACTIVATION',
        })
    if len(rows) != 41 or sum(int(r['member_size_bytes']) for r in rows) != EXACT_MEMBER_BYTES:
        raise SystemExit('object plan count or size mismatch')
    return rows


def build_inputs(repo: Path, data: dict[str, object]) -> list[dict[str, str]]:
    p: dict[str, Path] = data['paths']  # type: ignore[assignment]
    specs = [
        ('MAT-IN-001', 'COMPOSITION_MEMBERS', 'composition_members', '42_ROWS_41_INCLUDED_ONE_DEFERRED', 'VERIFY_ACCEPTED_MEMBER_IDENTITIES_AND_FOUR_DECLARED_ATOMIC_FAMILIES'),
        ('MAT-IN-002', 'COMPOSITION_ACCEPTANCE', 'composition_acceptance', 'SELECTED-COMPOSITION-ACCEPT-001', 'VERIFY_ACCEPTED_BOUNDED_COMPLETE_SELECTED_PROVIDER_COMPOSITION'),
        ('MAT-IN-003', 'TARGET_MANIFEST', 'target_manifest', '82_ROWS_41_REGULAR_41_ALIAS_ZERO_POPULATED', 'VERIFY_NORMALIZED_RELATIVE_PATHS_NODE_TYPES_AND_ZERO_COLLISIONS'),
        ('MAT-IN-004', 'TARGET_OBJECT_BINDINGS', 'object_bindings', '41_CONTENT_ADDRESSED_OBJECT_BINDINGS', 'VERIFY_MEMBER_SHA_SONAME_COMPOSITION_AND_TARGET_RELATION'),
        ('MAT-IN-005', 'TARGET_ALIAS_BINDINGS', 'alias_bindings', '41_RESOLVED_RELATIVE_SONAME_ALIASES', 'VERIFY_ALIAS_TO_CONCRETE_RELATION_AND_NO_PARENT_OR_ABSOLUTE_TARGET'),
        ('MAT-IN-006', 'TARGET_POLICY_ACCEPTANCE', 'target_acceptance', 'SELECTED-TARGET-MANIFEST-ACCEPT-001', 'VERIFY_ACCEPTED_BOUNDED_NON_MUTATING_TARGET_POLICY'),
        ('MAT-IN-007', 'INDEXED_SUPPLY_EVIDENCE', 'indexed_supply', '41_ROWS_ZERO_COORDINATE_OR_INDEX_GAPS', 'VERIFY_CLOSURE_KIND_RESULT_DIGEST_INDEX_DIGEST_AND_STATUS_SURFACE_BOUNDARY'),
        ('MAT-IN-008', 'HISTORICAL_SIZE_CENSUS', 'size_census', '40_EXACT_ONE_HISTORICAL_PIXMAN_OPEN', 'VERIFY_APPEND_ONLY_HISTORY_AND_DO_NOT_REWRITE_V109'),
        ('MAT-IN-009', 'PIXMAN_SIZE_EVIDENCE', 'pixman_evidence', 'ONE_EXACT_460920_BYTE_PIXMAN_ROW', 'VERIFY_EXACT_RESULT_OUTER_SHA_MEMBER_PATH_SIZE_AND_MEMBER_SHA'),
        ('MAT-IN-010', 'RESOURCE_BUDGET', 'resource_budget', '29047112_MEMBER_BYTES_1048576_RECEIPT_RESERVATION_59142800_PREFLIGHT', 'VERIFY_100_PERCENT_MARGIN_AND_OVERFLOW_ABORT_POLICY'),
        ('MAT-IN-011', 'GENERATION_CONTRACTS', 'generation_contracts', 'SEVEN_BOUNDED_NON_LIVE_CONTRACTS', 'VERIFY_ROOT_LAYOUT_ATOMIC_PUBLICATION_SPACE_RECEIPT_ROLLBACK_AND_CLEANUP'),
        ('MAT-IN-012', 'DESIGN_ONLY_INTERVENTION_LIFT', 'intervention_lift', 'TEN_SATISFIED_FOR_READ_ONLY_DESIGN_REVIEW', 'VERIFY_NO_RUNTIME_AUTHORITY_WIDENING'),
        ('MAT-IN-013', 'VERIFICATION_RECEIPT_PROTOTYPE', 'receipt_prototype', '41_OBJECTS_41_ALIASES_44332_BYTES_1048576_CAP', 'VERIFY_CANONICAL_JSON_FIELDS_AND_PUBLICATION_PLACEHOLDERS'),
    ]
    rows = []
    for iid, cls, key, identity, rule in specs:
        rel = SOURCE_PATHS[key]
        rows.append({
            'input_id': iid,
            'input_class': cls,
            'source_path': str(rel),
            'source_sha256': sha256_file(p[key]),
            'required_identity_or_count': identity,
            'validation_rule': rule,
            'consumption_mode': 'READ_ONLY_CANONICAL_INPUT_LOCKED_BY_SHA256_BEFORE_ANY_FUTURE_EXECUTION',
            'failure_action': 'ABORT_BEFORE_LOCK_ACQUISITION_PATH_CREATION_BYTE_READ_OR_MUTATION',
            'current_mutation_effect': 'NONE',
            'authority_effect': 'READ_ONLY_DESIGN_INPUT_ONLY',
            'prohibited_inference': 'SOURCE_LOCK_DOES_NOT_AUTHORIZE_LOCALIZATION_DOWNLOAD_EXTRACTION_ROOT_CREATION_OBJECT_WRITE_GENERATION_WRITE_SELECTOR_CHANGE_POPULATION_OR_ACTIVATION',
        })
    return rows


def build_states() -> list[dict[str, str]]:
    future = 'FUTURE_SEPARATE_EXECUTION_AUTHORIZATION_REQUIRED'
    design = 'DESIGN_REVIEW_ONLY_NOT_EXECUTABLE'
    rows = [
        ('MAT-S00', 0, 'DESIGN_CANDIDATE_QUALIFIED', 'CURRENT_READ_ONLY', 'ALL_DESIGN_TABLES_REGENERATE_AND_CHECK', 'DOCUMENT_AND_REVIEW_ONLY', 'NO_PATH_OR_BYTE_EFFECT', 'MAT-S01', 'MAT-F00', 'REGENERATE_FROM_LOCKED_SOURCES', 'NONE', 'QUALIFIED_CANDIDATE_ACCEPTANCE_OPEN'),
        ('MAT-S01', 1, 'DESIGN_ACCEPTANCE_REQUIRED', 'CURRENT_GATE', 'SEPARATE_ACCEPTANCE_TRANSACTION', 'ACCEPT_OR_REJECT_DESIGN_ONLY', 'EXACT_CANDIDATE_DIGESTS_AND_NO_AUTHORITY_WIDENING', 'MAT-S02', 'MAT-F00', 'NO_EXECUTION_RESUME', 'SEPARATE_DESIGN_ACCEPTANCE_REQUIRED', 'OPEN_NOT_ACCEPTED'),
        ('MAT-S02', 2, 'EXECUTION_AUTHORIZATION_REQUIRED', 'FUTURE_GATE', 'ACCEPTED_DESIGN_AND_SEPARATE_EXECUTION_AUTHORIZATION_ID', 'NO_MUTATION_UNTIL_TOKEN_VALIDATES', 'TOKEN_BINDS_DESIGN_JSON_SHA_AUTHORITY_SNAPSHOT_GENERATION_ID_AND_ALLOWED_EFFECTS', 'MAT-S10', 'MAT-F00', 'REVALIDATE_TOKEN', future, 'NOT_AUTHORIZED'),
        ('MAT-S10', 10, 'EXCLUSIVE_LOCK_HELD', 'FUTURE_MUTATING', 'VALID_EXECUTION_AUTHORIZATION', 'OPEN_NOFOLLOW_LOCK_FILE_AND_FCNTL_EXCLUSIVE_LOCK', 'OWNER_MODE_PATH_AND_STALE_METADATA', 'MAT-S20', 'MAT-F10', 'REENTER_ONLY_WITH_SAME_AUTHORIZATION_ID', future, 'NOT_AUTHORIZED'),
        ('MAT-S20', 20, 'RUNTIME_PREFLIGHT_PASSED', 'FUTURE_READ_ONLY', 'LOCK_HELD', 'LSTAT_STATVFS_STATFS_AND_INPUT_METADATA_READS_ONLY', 'ROOT_PROTECTED_PATH_DEVICE_OWNER_MODE_SPACE_HARDLINK_RENAME_AND_INPUT_CHECKS', 'MAT-S30', 'MAT-F10', 'RERUN_ALL_PREFLIGHT_CHECKS', future, 'NOT_AUTHORIZED'),
        ('MAT-S30', 30, 'SUPPLY_LOCALIZATION_BOUND', 'FUTURE_READ_ONLY', 'PREFLIGHT_PASSED_AND_41_ROW_LOCALIZATION_RECEIPT', 'READ_LOCAL_RESULT_ARCHIVES_ONLY', 'REGULAR_NOFOLLOW_EXACT_OUTER_SHA_RESULT_INDEX_AND_MEMBER_LOCATOR', 'MAT-S40', 'MAT-F10', 'REVERIFY_ALL_41_LOCAL_INPUTS', future, 'NOT_AUTHORIZED'),
        ('MAT-S40', 40, 'TRANSACTION_STAGING_OPEN', 'FUTURE_MUTATING', 'SUPPLY_BOUND', 'CREATE_EXACT_TRANSACTION_SCOPED_STAGING_AND_JOURNAL_ONLY', 'O_EXCL_NOFOLLOW_OWNER_0700_SAME_DEVICE', 'MAT-S50', 'MAT-F20', 'RESUME_ONLY_IF_TRANSACTION_JOURNAL_DIGEST_MATCHES', future, 'NOT_AUTHORIZED'),
        ('MAT-S50', 50, 'CONTENT_ADDRESSED_OBJECTS_COMPLETE', 'FUTURE_MUTATING', 'STAGING_OPEN', 'STREAM_VERIFY_AND_PUBLISH_41_OBJECTS_TO_CONTENT_ADDRESS_STORE', 'SIZE_SHA_ELF_SONAME_RPATH_RUNPATH_NEEDED_AND_OBJECT_PATH', 'MAT-S60', 'MAT-F20', 'REUSE_ONLY_EXACT_VERIFIED_FINAL_OBJECTS', future, 'NOT_AUTHORIZED'),
        ('MAT-S60', 60, 'GENERATION_REGULARS_COMPLETE', 'FUTURE_MUTATING', 'ALL_41_OBJECTS_COMPLETE', 'CREATE_STAGING_GENERATION_DIRS_AND_HARDLINK_41_REGULARS', 'NO_COPY_FALLBACK_SAME_DEVICE_TARGET_PATH_COUNT_AND_ATOMIC_FAMILY_BARRIER', 'MAT-S70', 'MAT-F20', 'REVERIFY_EXISTING_TX_SCOPED_LINKS', future, 'NOT_AUTHORIZED'),
        ('MAT-S70', 70, 'GENERATION_ALIASES_COMPLETE', 'FUTURE_MUTATING', 'ALL_REGULARS_AND_ATOMIC_FAMILIES_COMPLETE', 'CREATE_41_RELATIVE_SONAME_SYMLINKS', 'ALIAS_BASENAME_TARGET_NO_ABSOLUTE_PARENT_OR_COLLISION', 'MAT-S80', 'MAT-F20', 'REVERIFY_EXACT_TX_SCOPED_SYMLINKS', future, 'NOT_AUTHORIZED'),
        ('MAT-S80', 80, 'WHOLE_GENERATION_VERIFIED', 'FUTURE_READ_ONLY', 'REGULARS_AND_ALIASES_COMPLETE', 'READ_ONLY_WHOLE_TREE_ELF_DEPENDENCY_AND_LOADER_CHECKS', '82_ROWS_41_OBJECTS_41_ALIASES_ZERO_COLLISIONS_ATOMIC_FAMILIES_COMPLETE_NO_FORBIDDEN_LOADER_PATHS', 'MAT-S90', 'MAT-F20', 'RERUN_COMPLETE_VERIFICATION', future, 'NOT_AUTHORIZED'),
        ('MAT-S90', 90, 'RECEIPT_SEALED', 'FUTURE_MUTATING', 'WHOLE_GENERATION_VERIFIED', 'WRITE_CANONICAL_RECEIPT_AND_RESULT_INDEX', 'CANONICAL_JSON_SIZE_AT_MOST_1048576_AND_ALL_FIELDS_COMPLETE', 'MAT-S100', 'MAT-F20', 'REGENERATE_ONLY_IN_TX_STAGING_BEFORE_PUBLICATION', future, 'NOT_AUTHORIZED'),
        ('MAT-S100', 100, 'GENERATION_PUBLISHED', 'FUTURE_MUTATING', 'RECEIPT_SEALED_AND_TREE_FSYNCED', 'RENAME_STAGING_GENERATION_TO_IMMUTABLE_FINAL_GENERATION', 'SAME_DEVICE_NOREPLACE_PARENT_FSYNC_AND_FINAL_RECEIPT_MATCH', 'MAT-S110', 'MAT-F30', 'VERIFY_EXISTING_FINAL_GENERATION_AND_CONTINUE_IF_EXACT', future, 'NOT_AUTHORIZED'),
        ('MAT-S110', 110, 'SELECTORS_PUBLISHED', 'FUTURE_MUTATING', 'FINAL_GENERATION_AND_RECEIPT_VERIFY', 'PUBLISH_PREVIOUS_THEN_CURRENT_RELATIVE_SELECTORS_BY_TEMP_RENAME', 'SELECTOR_TARGET_COMPLETE_RELATIVE_AND_PARENT_FSYNC', 'MAT-S120', 'MAT-F40', 'RECOVER_FROM_SELECTOR_JOURNAL_WITHOUT_GENERATION_MUTATION', future, 'NOT_AUTHORIZED'),
        ('MAT-S120', 120, 'TRANSACTION_COMPLETE', 'FUTURE_TERMINAL', 'SELECTORS_PUBLISHED_AND_POST_INVARIANCE_PASS', 'WRITE_COMPLETION_RECEIPT_ONLY', 'CURRENT_TARGET_GENERATION_RECEIPT_REMOTE_AND_PROTECTED_STATE', 'MAT-S120', 'MAT-F40', 'IDEMPOTENT_COMPLETE', future, 'NOT_AUTHORIZED'),
        ('MAT-F00', 900, 'DESIGN_OR_AUTHORIZATION_REJECTED', 'FAILURE_TERMINAL', 'DESIGN_ACCEPTANCE_OR_EXECUTION_TOKEN_FAILURE', 'NONE', 'FAILURE_RECEIPT_METADATA_ONLY', 'MAT-F00', 'MAT-F00', 'NEW_REVIEW_REQUIRED', 'NONE', 'NO_AUTHORITY'),
        ('MAT-F10', 910, 'FAILED_BEFORE_STAGING', 'FAILURE_TERMINAL', 'LOCK_PREFLIGHT_OR_SUPPLY_BINDING_FAILURE', 'NO_TARGET_OR_STAGING_MUTATION', 'RELEASE_LOCK_AND_RECORD_FAILURE', 'MAT-F10', 'MAT-F10', 'RERUN_AFTER_CAUSE_FIXED', future, 'NOT_AUTHORIZED'),
        ('MAT-F20', 920, 'FAILED_IN_TRANSACTION_STAGING', 'FAILURE_RECOVERABLE', 'TX_SCOPED_MUTATION_STARTED_NO_FINAL_GENERATION', 'PRESERVE_FAILURE_RECEIPT_AND_EXACT_STAGING_FOR_RESUME_OR_QUARANTINE', 'NO_AUTOMATIC_DELETE_OUTSIDE_EXACT_TRANSACTION_ID', 'MAT-F20', 'MAT-F20', 'RESUME_ONLY_WITH_MATCHING_JOURNAL', future, 'NOT_AUTHORIZED'),
        ('MAT-F30', 930, 'FAILED_AFTER_GENERATION_BEFORE_SELECTOR', 'FAILURE_RECOVERABLE', 'FINAL_IMMUTABLE_GENERATION_EXISTS_SELECTORS_UNCHANGED', 'LEAVE_GENERATION_UNSELECTED_AND_REPORT_ORPHAN_GENERATION', 'VERIFY_RECEIPT_BEFORE_ANY_RESUME', 'MAT-F30', 'MAT-F30', 'RESUME_SELECTOR_PUBLICATION_ONLY', future, 'NOT_AUTHORIZED'),
        ('MAT-F40', 940, 'FAILED_DURING_SELECTOR_PUBLICATION', 'FAILURE_RECOVERABLE', 'SELECTOR_JOURNAL_EXISTS', 'DO_NOT_MUTATE_GENERATION_RECONCILE_RELATIVE_SELECTORS_FROM_JOURNAL', 'CURRENT_ALWAYS_POINTS_TO_COMPLETE_VERIFIED_GENERATION_OR_PREVIOUS_SAFE_TARGET', 'MAT-F40', 'MAT-F40', 'LOCKED_SELECTOR_RECOVERY_ONLY', future, 'NOT_AUTHORIZED'),
    ]
    out = []
    for sid, order, name, cls, entry, effects, checks, success, fail, resume, gate, current in rows:
        out.append({
            'state_id': sid, 'phase_order': str(order), 'state_name': name,
            'state_class': cls, 'entry_requirements': entry,
            'permitted_effects': effects, 'required_checks': checks,
            'success_transition': success, 'failure_transition': fail,
            'resume_rule': resume, 'authorization_gate': gate,
            'current_authority_state': current,
            'prohibited_inference': 'STATE_DEFINITION_DOES_NOT_AUTHORIZE_EXECUTION_BYTE_ACQUISITION_ROOT_CREATION_TARGET_WRITE_POPULATION_PUBLICATION_DEPLOYMENT_OR_ACTIVATION',
        })
    return out


def build_operations() -> list[dict[str, str]]:
    future = 'FUTURE_SEPARATE_EXECUTION_AUTHORIZATION_REQUIRED'
    specs = [
        ('MAT-OP-001', 'LOCK_AUTHORITY_SNAPSHOT', '13_CANONICAL_INPUT_DIGESTS', 'IMMUTABLE_AUTHORITY_SNAPSHOT_JSON', 'READ_ONLY', 'REPOSITORY', 'DESIGN_ACCEPTED_AND_EXECUTION_TOKEN_PRESENT', 'ALL_SOURCE_DIGESTS_AND_COUNTS_MATCH', 'NONE', 'ABORT_BEFORE_LOCK_OR_PATH_EFFECT'),
        ('MAT-OP-002', 'DERIVE_GENERATION_AND_TRANSACTION_IDS', 'AUTHORITY_SNAPSHOT_AND_EXECUTION_AUTHORIZATION_ID', 'GENERATION_SHA256_AND_TRANSACTION_SHA256', 'READ_ONLY', 'MEMORY_ONLY', 'AUTHORITY_SNAPSHOT_LOCKED', 'GENERATION_ID_IS_SHA256_CANONICAL_AUTHORITY_SNAPSHOT;TRANSACTION_ID_BINDS_GENERATION_AND_AUTHORIZATION', 'NONE', 'ABORT_ON_NONCANONICAL_ID'),
        ('MAT-OP-003', 'ACQUIRE_EXCLUSIVE_LOCK', 'TRANSACTION_ID', 'LOCK_HELD', 'MUTATING_METADATA', 'locks/materialize.lock', 'RUNTIME_PREFLIGHT_PATH_PARENT_SAFE', 'O_NOFOLLOW_REGULAR_OWNER_MODE_AND_FCNTL_EXCLUSIVE', 'FSYNC_LOCK_METADATA_IF_CREATED', 'NO_STALE_LOCK_BREAK_WITHOUT_SEPARATE_OPERATOR_DECISION'),
        ('MAT-OP-004', 'RUN_RUNTIME_PREFLIGHT', 'PREFLIGHT_CONTRACT', 'PREFLIGHT_RECEIPT', 'READ_ONLY', 'GENERATION_BASE_AND_LOCAL_INPUTS', 'LOCK_HELD', 'ALL_20_PREFLIGHT_ROWS_PASS', 'NONE', 'ABORT_AND_RELEASE_LOCK'),
        ('MAT-OP-005', 'VERIFY_LOCAL_SUPPLY_MAP', '41_ROW_LOCALIZATION_RECEIPT', '41_VERIFIED_LOCAL_RESULT_HANDLES', 'READ_ONLY', 'EXTERNAL_READ_ONLY_CACHE', 'PREFLIGHT_PASSED', 'NOFOLLOW_REGULAR_EXACT_OUTER_SHA_RESULT_INDEX_AND_LOCATOR', 'NONE', 'ABORT_NO_BYTE_EXTRACTION'),
        ('MAT-OP-006', 'OPEN_TRANSACTION_STAGING', 'TRANSACTION_ID', 'staging/<transaction_id>', 'MUTATING', 'staging', 'SUPPLY_MAP_VERIFIED', 'O_EXCL_NOFOLLOW_UID_MODE_0700_SAME_DEVICE_EMPTY_OR_MATCHING_JOURNAL', 'FSYNC_STAGING_PARENT', 'PRESERVE_EXACT_TX_STAGING_ON_FAILURE'),
        ('MAT-OP-007', 'WRITE_TRANSACTION_JOURNAL', 'AUTHORITY_SNAPSHOT_AND_IDS', 'staging/<transaction_id>/transaction.json', 'MUTATING_METADATA', 'staging/<transaction_id>', 'STAGING_OPEN', 'CANONICAL_JSON_O_EXCL_SIZE_CAP_AND_HASH', 'FSYNC_FILE_AND_PARENT', 'MISMATCH_QUARANTINE_NO_AUTO_DELETE'),
        ('MAT-OP-008', 'STREAM_EXACT_MEMBER_TO_OBJECT_TEMP', 'OBJECT_PLAN_ROW_AND_LOCAL_RESULT_HANDLE', 'objects/sha256/<prefix>/.<sha>.<tx>.tmp', 'MUTATING', 'objects/sha256', 'TX_JOURNAL_VALID', 'EXACT_CONTAINER_MEMBER_ONLY_O_EXCL_NOFOLLOW_MODE_0600_SIZE_LIMIT', 'FSYNC_TEMP_AFTER_STREAM', 'DELETE_ONLY_EXACT_UNPUBLISHED_TEMP_FOR_SAME_TX_OR_PRESERVE_FOR_DIAGNOSTIC'),
        ('MAT-OP-009', 'VERIFY_OBJECT_TEMP', 'OBJECT_TEMP', 'OBJECT_VERIFICATION_RECORD', 'READ_ONLY', 'OBJECT_TEMP', 'STREAM_COMPLETE', 'SIZE_SHA256_ELF64_AARCH64_DYN_SONAME_RPATH_RUNPATH_NEEDED_CAPTURE', 'NONE', 'FAIL_TX_NO_FINAL_OBJECT_RENAME'),
        ('MAT-OP-010', 'PUBLISH_CONTENT_ADDRESSED_OBJECT', 'VERIFIED_OBJECT_TEMP', 'objects/sha256/<prefix>/<sha256>', 'MUTATING', 'objects/sha256', 'OBJECT_VERIFIED', 'CHMOD_0444_OWNER_UID_NO_SETID_NO_WORLD_WRITE_NOREPLACE_OR_EXACT_REUSE', 'FSYNC_OBJECT_AND_PARENT_BEFORE_OR_AFTER_ATOMIC_RENAME', 'NEVER_OVERWRITE_MISMATCHING_FINAL_OBJECT'),
        ('MAT-OP-011', 'CREATE_STAGING_GENERATION_LAYOUT', '82_ROW_TARGET_POLICY', 'staging/<tx>/generation/lib', 'MUTATING', 'staging/<tx>/generation', 'ALL_41_OBJECTS_COMPLETE', 'DIRECTORIES_ONLY_NO_TARGET_FILES_YET_MODE_0700', 'FSYNC_CREATED_DIRECTORY_PARENTS', 'PRESERVE_TX_SCOPED_STAGING'),
        ('MAT-OP-012', 'HARDLINK_REGULAR_TARGETS', '41_OBJECT_PLAN_ROWS', '41_REGULAR_TARGET_PATHS', 'MUTATING', 'staging/<tx>/generation/lib', 'OBJECT_STORE_COMPLETE_AND_SAME_DEVICE', 'HARDLINK_ONLY_NO_COPY_FALLBACK_EXACT_TARGET_PATH_O_EXCL_ZERO_COLLISIONS', 'FSYNC_TARGET_DIRECTORIES_AFTER_BATCH', 'REMOVE_OR_RESUME_ONLY_TX_SCOPED_LINKS'),
        ('MAT-OP-013', 'ENFORCE_ATOMIC_FAMILY_BARRIER', 'FOUR_DECLARED_ATOMIC_FAMILIES', 'ATOMIC_FAMILY_VERIFICATION_RECORD', 'READ_ONLY', 'STAGING_GENERATION', '41_REGULARS_LINKED', 'ATSPI2_3_CAIRO_2_PANGO_3_GDK_GTK_2_ALL_OR_NONE', 'NONE', 'ABORT_BEFORE_ALIAS_CREATION'),
        ('MAT-OP-014', 'CREATE_RELATIVE_SONAME_ALIASES', '41_ALIAS_PLAN_ROWS', '41_RELATIVE_SYMLINKS', 'MUTATING', 'staging/<tx>/generation/lib', 'REGULARS_AND_ATOMIC_FAMILIES_COMPLETE', 'RELATIVE_BASENAME_TARGET_EXISTS_NO_ABSOLUTE_PARENT_OR_COLLISION', 'FSYNC_ALIAS_PARENT_DIRECTORY', 'PRESERVE_TX_SCOPED_STAGING'),
        ('MAT-OP-015', 'VERIFY_WHOLE_GENERATION', 'STAGING_GENERATION', 'WHOLE_GENERATION_VERIFICATION_RECORD', 'READ_ONLY', 'staging/<tx>/generation', '82_TARGET_ROWS_PRESENT', 'ALL_18_VERIFICATION_CONTRACT_ROWS_PASS', 'NONE', 'ABORT_BEFORE_RECEIPT_SEAL'),
        ('MAT-OP-016', 'GENERATE_CANONICAL_RECEIPT', 'VERIFICATION_RECORDS_AND_PUBLICATION_PLACEHOLDERS', 'staging/<tx>/receipt.json', 'MUTATING_METADATA', 'staging/<tx>', 'WHOLE_GENERATION_VERIFIED', 'CANONICAL_UTF8_JSON_SORTED_KEYS_NEWLINE_COMPLETE_FIELDS_SIZE_AT_MOST_1048576', 'FSYNC_RECEIPT', 'ABORT_BEFORE_PUBLICATION_ON_OVERFLOW_OR_MISSING_FIELD'),
        ('MAT-OP-017', 'GENERATE_RECEIPT_RESULT_INDEX', 'RECEIPT_AND_SUPPORTING_RECORDS', 'staging/<tx>/result-index.sha256', 'MUTATING_METADATA', 'staging/<tx>', 'RECEIPT_CANONICAL', 'SORTED_SHA256_INDEX_EXCLUDES_ITSELF', 'FSYNC_INDEX_AND_PARENT', 'ABORT_BEFORE_PUBLICATION'),
        ('MAT-OP-018', 'SEAL_GENERATION_TREE', 'VERIFIED_STAGING_GENERATION', 'READ_ONLY_IMMUTABLE_TREE', 'MUTATING_METADATA', 'staging/<tx>/generation', 'RECEIPT_AND_INDEX_COMPLETE', 'FILES_0444_DIRECTORIES_0555_SYMLINKS_UNCHANGED_NO_SETID_WORLD_WRITE', 'FSYNC_ALL_FILES_DIRECTORIES_BOTTOM_UP_AND_PARENT', 'ABORT_BEFORE_FINAL_RENAME'),
        ('MAT-OP-019', 'PUBLISH_IMMUTABLE_GENERATION', 'SEALED_STAGING_GENERATION', 'generations/<generation_id>', 'MUTATING', 'generations', 'TREE_AND_RECEIPT_FSYNC_COMPLETE', 'ATOMIC_NOREPLACE_RENAME_SAME_DEVICE_FINAL_PATH_ABSENT_OR_EXACT_VERIFIED', 'FSYNC_GENERATIONS_PARENT', 'LEAVE_UNSELECTED_GENERATION_AND_FAILURE_RECEIPT'),
        ('MAT-OP-020', 'PUBLISH_RECEIPT', 'SEALED_RECEIPT', 'receipts/<generation_id>.json', 'MUTATING_METADATA', 'receipts', 'FINAL_GENERATION_VERIFY', 'ATOMIC_NOREPLACE_RENAME_AND_DIGEST_MATCH', 'FSYNC_RECEIPTS_PARENT', 'NO_SELECTOR_CHANGE_IF_RECEIPT_FAILS'),
        ('MAT-OP-021', 'PUBLISH_PREVIOUS_SELECTOR', 'CURRENT_SELECTOR_TARGET_IF_PRESENT', 'previous', 'MUTATING', 'GENERATION_BASE', 'NEW_GENERATION_AND_RECEIPT_COMPLETE', 'TEMP_RELATIVE_SYMLINK_RENAME_TO_PREVIOUS_TARGET_VERIFIED', 'FSYNC_SELECTOR_PARENT', 'CURRENT_REMAINS_UNCHANGED_ON_FAILURE'),
        ('MAT-OP-022', 'PUBLISH_CURRENT_SELECTOR', 'NEW_GENERATION_RELATIVE_TARGET', 'current', 'MUTATING', 'GENERATION_BASE', 'PREVIOUS_SELECTOR_PUBLISHED_OR_NO_PRIOR_CURRENT', 'TEMP_RELATIVE_SYMLINK_RENAME_TO_CURRENT_TARGET_VERIFIED', 'FSYNC_SELECTOR_PARENT', 'RECOVER_FROM_SELECTOR_JOURNAL_WITH_CURRENT_POINTING_ONLY_TO_COMPLETE_GENERATION'),
        ('MAT-OP-023', 'WRITE_COMPLETION_RECEIPT', 'FINAL_SELECTOR_AND_PROTECTED_STATE', 'TRANSACTION_COMPLETION_RECORD', 'MUTATING_METADATA', 'receipts', 'CURRENT_SELECTOR_VERIFY_AND_POST_INVARIANCE_PASS', 'BINDS_GENERATION_RECEIPT_CURRENT_PREVIOUS_REMOTE_AND_PROTECTED_STATE', 'FSYNC_COMPLETION_RECORD_AND_PARENT', 'REPORT_FAILURE_WITHOUT_GENERATION_MUTATION'),
        ('MAT-OP-024', 'REPORT_ORPHANS_AND_RESUME_STATE', 'STAGING_GENERATIONS_TEMP_SELECTORS_AND_JOURNALS', 'ORPHAN_REPORT', 'READ_ONLY', 'GENERATION_BASE', 'LOCK_HELD', 'LIST_ONLY_CLASSIFY_EXACT_TX_RESUMABLE_UNKNOWN_QUARANTINE_AND_UNSELECTED_COMPLETE_GENERATIONS', 'NONE', 'NO_AUTOMATIC_DELETE_OUTSIDE_EXACT_TX_ID'),
    ]
    rows = []
    for seq, (sid, op, inp, outp, mutation, scope, pre, verify, fsync, failure) in enumerate(specs, 1):
        rows.append({
            'step_id': sid, 'sequence': str(seq), 'operation': op,
            'input_contract': inp, 'output_contract': outp,
            'mutation_class': mutation, 'path_scope': scope, 'precondition': pre,
            'verification': verify, 'fsync_or_atomic_rule': fsync,
            'rollback_or_failure_rule': failure, 'authorization_gate': future,
            'current_authority_state': 'NOT_AUTHORIZED_DESIGN_ROW_ONLY',
            'prohibited_inference': 'OPERATION_CONTRACT_IS_NOT_IMPLEMENTATION_OR_PERMISSION_TO_DOWNLOAD_READ_PROVIDER_BYTES_CREATE_PATHS_WRITE_LINK_RENAME_POPULATE_PUBLISH_DEPLOY_OR_ACTIVATE',
        })
    return rows


def build_preflight() -> list[dict[str, str]]:
    specs = [
        ('MAT-PREF-001', 'AUTHORIZATION', 'EXECUTION_AUTHORIZATION_TOKEN', 'SEPARATE_ACCEPTED_TOKEN_BINDS_DESIGN_JSON_SHA_AUTHORITY_SNAPSHOT_GENERATION_ID_ALLOWED_EFFECTS_AND_EXPIRY', 'SIGNED_OR_REPOSITORY_ACCEPTED_EXECUTION_AUTHORIZATION_RECEIPT', 'EXECUTION_AUTHORIZATION_MISSING_OR_MISMATCH'),
        ('MAT-PREF-002', 'ROOT_PATH', 'GENERATION_BASE', f'EXACT_ABSOLUTE_PATH_{GENERATION_BASE}_NO_NORMALIZATION_DRIFT', 'CANONICAL_PATH_STRING_AND_LSTAT_CHAIN', 'GENERATION_ROOT_PATH_MISMATCH'),
        ('MAT-PREF-003', 'PROTECTED_PATHS', 'GENERATION_BASE_AND_ALL_DESCENDANTS', 'DISJOINT_FROM_PREFIX_HOME_GL_REPOSITORY_PACKAGE_DATABASES_AND_LIVE_GLIBC_PREFIX', 'REALPATH_FREE_COMPONENT_COMPARISON_AND_PROTECTED_SNAPSHOT', 'PROTECTED_PATH_OVERLAP'),
        ('MAT-PREF-004', 'SYMLINK_SAFETY', 'ALL_EXISTING_ANCESTORS_AND_LOCAL_INPUTS', 'LSTAT_EACH_COMPONENT_NO_SYMLINK_NO_MAGICLINK_NO_DOTDOT', 'DEVICE_INODE_MODE_UID_COMPONENT_RECEIPT', 'SYMLINK_OR_UNSAFE_COMPONENT'),
        ('MAT-PREF-005', 'OWNERSHIP_MODE', 'ROOT_LAYOUT_AND_EXISTING_OBJECTS', 'CURRENT_UID_OWNER_ROOT_AND_MUTABLE_DIRS_0700_FINAL_OBJECTS_0444_SEALED_GENERATION_DIRS_0555_NO_SETUID_SETGID_OR_WORLD_WRITE', 'LSTAT_MODE_UID_GID_RECEIPT', 'OWNER_OR_MODE_POLICY_FAILURE'),
        ('MAT-PREF-006', 'FILESYSTEM_DEVICE', 'OBJECTS_STAGING_GENERATIONS_RECEIPTS_LOCKS_AND_SELECTOR_PARENT', 'ALL_ST_DEV_EQUAL', 'LSTAT_ST_DEV_VALUES', 'CROSS_DEVICE_ATOMICITY_UNAVAILABLE'),
        ('MAT-PREF-007', 'FREE_SPACE', 'GENERATION_FILESYSTEM', f'STATVFS_AVAILABLE_BYTES_AT_LEAST_{FINAL_PREFLIGHT_BYTES}', 'F_BAVAIL_TIMES_F_FRSIZE_AND_REQUIRED_BYTES', 'INSUFFICIENT_FREE_SPACE'),
        ('MAT-PREF-008', 'HARDLINK_CAPABILITY', 'OBJECT_STORE_TO_STAGING_GENERATION', 'SAME_DEVICE_HARDLINK_SUPPORTED_NO_COPY_FALLBACK', 'BOUNDED_TEMP_PROBE_ONLY_AFTER_EXECUTION_AUTHORIZATION_OR_FILESYSTEM_CAPABILITY_RECEIPT', 'HARDLINK_CAPABILITY_MISSING'),
        ('MAT-PREF-009', 'ATOMIC_RENAME', 'STAGING_GENERATIONS_RECEIPTS_AND_SELECTOR_PARENT', 'SAME_DEVICE_ATOMIC_NOREPLACE_RENAME_SUPPORTED', 'FILESYSTEM_CAPABILITY_RECEIPT', 'ATOMIC_RENAME_CAPABILITY_MISSING'),
        ('MAT-PREF-010', 'LOCK', 'locks/materialize.lock', 'REGULAR_NOFOLLOW_CURRENT_UID_NOT_WORLD_WRITABLE_EXCLUSIVE_FCNTL_LOCK', 'LOCK_FILE_DEVICE_INODE_UID_MODE_AND_OWNER_PID_METADATA', 'LOCK_BUSY_OR_UNSAFE'),
        ('MAT-PREF-011', 'SUPPLY_LOCALIZATION', '41_ROW_LOCAL_READ_ONLY_SUPPLY_MAP', 'EXACTLY_41_UNIQUE_MEMBER_SHA_ROWS_EACH_BOUND_TO_REGULAR_NOFOLLOW_LOCAL_RESULT_PATH', 'LOCALIZATION_RECEIPT_SHA_AND_ROW_COUNT', 'LOCALIZATION_INCOMPLETE_OR_DUPLICATE'),
        ('MAT-PREF-012', 'SUPPLY_OUTER_DIGEST', 'LOCAL_RESULT_ARCHIVES', 'OUTER_SHA256_EQUALS_OBJECT_PLAN_SUPPLY_RESULT_SHA_OR_ACCEPTED_EXISTING_AUTHORITY_DIGEST', 'PER_INPUT_SHA256_RECEIPT', 'SUPPLY_RESULT_SHA_MISMATCH'),
        ('MAT-PREF-013', 'SUPPLY_RESULT_INDEX', 'LOCAL_RESULT_ARCHIVES_OR_APPEND_ONLY_RECEIPTS', 'RESULT_INDEX_OR_ACCEPTED_APPEND_ONLY_INDEX_DIGEST_MATCHES_OBJECT_PLAN', 'INDEX_SHA_AND_MEMBER_PATH_RECEIPT', 'SUPPLY_RESULT_INDEX_MISMATCH'),
        ('MAT-PREF-014', 'CONTAINER_LOCATOR', 'ARTIFACT_AND_MEMBER_EVIDENCE_PATHS', 'EXACT_CONTAINER_CHAIN_AND_REGULAR_MEMBER_LOCATOR_RESOLVES_ONE_MEMBER_WITHOUT_WHOLE_ARCHIVE_EXTRACTION', 'DECODER_CLASS_MEMBER_PATH_AND_TYPE_RECEIPT', 'MEMBER_LOCATOR_AMBIGUOUS_OR_MISSING'),
        ('MAT-PREF-015', 'TARGET_POLICY', '82_ROW_TARGET_MANIFEST', 'EXACT_41_REGULAR_41_ALIAS_ZERO_COLLISIONS_ZERO_UNRESOLVED_AND_ALL_RELATIVE_NORMALIZED', 'TARGET_POLICY_SOURCE_DIGESTS_AND_COUNTS', 'TARGET_POLICY_DRIFT'),
        ('MAT-PREF-016', 'ATOMIC_FAMILIES', 'ATSPI2_CAIRO_PANGO_GDK_GTK', 'EXACT_MEMBER_COUNTS_3_2_3_2_AND_ALL_MEMBER_ROWS_PRESENT', 'ATOMIC_FAMILY_ROW_SET_DIGEST', 'PARTIAL_ATOMIC_FAMILY'),
        ('MAT-PREF-017', 'RECEIPT_CAP', 'CANONICAL_RECEIPT', f'RESERVATION_{RECEIPT_RESERVATION_BYTES}_BYTES_ABORT_BEFORE_PUBLICATION_ON_OVERFLOW', 'PROTOTYPE_SHA_SIZE_AND_RUNTIME_CANONICAL_SIZE', 'RECEIPT_RESERVATION_OVERFLOW'),
        ('MAT-PREF-018', 'CURRENT_GENERATION', 'current_AND_previous_SELECTORS', 'RELATIVE_SYMLINKS_ONLY_TARGET_COMPLETE_RECEIPT_VERIFIED_GENERATIONS_NO_ACTIVE_GENERATION_MUTATION', 'SELECTOR_LSTAT_TARGET_AND_RECEIPT_DIGEST', 'SELECTOR_OR_ACTIVE_GENERATION_UNSAFE'),
        ('MAT-PREF-019', 'ORPHAN_POLICY', 'STAGING_TEMP_OBJECTS_UNSELECTED_GENERATIONS_AND_TEMP_SELECTORS', 'ENUMERATE_AND_CLASSIFY_NO_AUTOMATIC_DELETE_OUTSIDE_EXACT_TRANSACTION_ID', 'ORPHAN_REPORT', 'UNKNOWN_ORPHAN_REQUIRES_OPERATOR_REVIEW'),
        ('MAT-PREF-020', 'PROTECTED_INVARIANCE', 'PACKAGE_DATABASES_AND_LIVE_GLIBC_PREFIX', 'PRE_SNAPSHOT_COMPLETE_AND_POST_COMPARISON_REQUIRED', 'PROTECTED_BEFORE_JSON', 'PROTECTED_SNAPSHOT_FAILURE'),
    ]
    rows=[]
    for seq,(cid,cat,subject,rule,evidence,fail) in enumerate(specs,1):
        rows.append({'check_id':cid,'sequence':str(seq),'category':cat,'subject':subject,'required_rule':rule,'pass_evidence':evidence,'failure_code':fail,'timing':'BEFORE_FIRST_MUTATING_OPERATION_AND_RECHECK_BEFORE_PUBLICATION_WHERE_APPLICABLE','current_execution_state':'NOT_RUN_DESIGN_ONLY','authority_effect':'READ_ONLY_PREFLIGHT_CONTRACT_ONLY','prohibited_inference':'PREFLIGHT_CONTRACT_OR_FUTURE_PASS_DOES_NOT_BY_ITSELF_AUTHORIZE_BYTE_ACQUISITION_ROOT_CREATION_POPULATION_PUBLICATION_DEPLOYMENT_OR_ACTIVATION'})
    return rows


def build_verification() -> list[dict[str, str]]:
    specs=[
        ('MAT-VER-001','AUTHORITY','AUTHORITY_SNAPSHOT','ALL_13_SOURCE_DIGESTS_AND_DESIGN_JSON_DIGEST_MATCH_ACCEPTED_DESIGN','authority_snapshot_sha256'),
        ('MAT-VER-002','SUPPLY','RESULT_ARCHIVE','OUTER_SHA256_AND_RESULT_INDEX_OR_APPEND_ONLY_RECEIPT_MATCH','supply_results'),
        ('MAT-VER-003','SUPPLY','MEMBER_LOCATOR','EXACT_CONTAINER_CHAIN_RESOLVES_ONE_REGULAR_MEMBER_NO_WHOLE_ARCHIVE_EXTRACTION','member_locator'),
        ('MAT-VER-004','OBJECT','SIZE_AND_SHA','ACTUAL_SIZE_AND_SHA256_EQUAL_OBJECT_PLAN','objects[].actual_size_bytes;objects[].actual_sha256'),
        ('MAT-VER-005','OBJECT','ELF_IDENTITY','ELF64_LITTLE_ENDIAN_AARCH64_DYN','objects[].elf_class;objects[].elf_data;objects[].elf_machine;objects[].elf_type'),
        ('MAT-VER-006','OBJECT','SONAME','DT_SONAME_EQUALS_OBJECT_PLAN_SONAME','objects[].actual_soname'),
        ('MAT-VER-007','OBJECT','RPATH_RUNPATH','CAPTURE_EXACT_VALUES_AND_REJECT_FORBIDDEN_CLASSICAL_OR_BIONIC_PATHS','objects[].rpath;objects[].runpath'),
        ('MAT-VER-008','OBJECT','DT_NEEDED','CAPTURE_SORTED_NEEDED_LIST_AND_REJECT_UNREVIEWED_DIRECT_DEPENDENCY','objects[].needed'),
        ('MAT-VER-009','OBJECT','LOADER_RESOLUTION','CANONICAL_GLIBC_LOADER_RESOLVES_SELECTED_PROVIDER_LIBS_TO_STAGING_GENERATION_OR_ACCEPTED_BASELINE_WITH_NO_HOME_GL_BIONIC_OR_PACKAGE_DB_MAPPING','objects[].loader_resolutions'),
        ('MAT-VER-010','OBJECT_STORE','CONTENT_ADDRESS','FINAL_OBJECT_PATH_SUFFIX_EQUALS_ACTUAL_SHA_AND_EXISTING_OBJECT_IS_BYTE_IDENTICAL_REGULAR_0444','objects[].object_store_path'),
        ('MAT-VER-011','GENERATION','REGULAR_TARGETS','EXACTLY_41_REGULAR_HARDLINKS_MATCH_OBJECT_INODES_AND_TARGET_PATHS','generation.regular_count'),
        ('MAT-VER-012','GENERATION','ALIASES','EXACTLY_41_RELATIVE_SYMLINKS_MATCH_ALIAS_BINDINGS_AND_RESOLVE_WITHIN_GENERATION_LIB','generation.alias_count'),
        ('MAT-VER-013','GENERATION','COLLISIONS','ZERO_DUPLICATE_PATHS_ZERO_UNRESOLVED_ALIAS_ZERO_NONMANIFEST_NODES','generation.collision_count;generation.unexpected_node_count'),
        ('MAT-VER-014','GENERATION','ATOMIC_FAMILIES','ATSPI2_3_CAIRO_2_PANGO_3_GDK_GTK_2_COMPLETE','generation.atomic_families'),
        ('MAT-VER-015','GENERATION','MODES_OWNERS','REGULARS_0444_DIRS_0555_CURRENT_UID_NO_SETID_OR_WORLD_WRITE','generation.mode_owner_summary'),
        ('MAT-VER-016','RECEIPT','CANONICAL_SERIALIZATION','UTF8_SORTED_KEYS_COMPACT_CANONICAL_NEWLINE_ALL_FIELDS_PRESENT_SIZE_AT_MOST_1048576','receipt_sha256;receipt_size_bytes'),
        ('MAT-VER-017','RECEIPT','RESULT_INDEX','SORTED_SHA256_INDEX_BINDS_RECEIPT_AND_SUPPORTING_RECORDS_EXCLUDES_ITSELF','result_index_sha256'),
        ('MAT-VER-018','PUBLICATION','GENERATION_AND_SELECTORS','GENERATION_ID_MATCHES_AUTHORITY_SNAPSHOT_RECEIPT_TARGET_COMPLETE_CURRENT_PREVIOUS_RELATIVE_AND_PARENT_FSYNC_COMPLETE','publication_fields'),
    ]
    rows=[]
    for seq,(vid,stage,subject,rule,field) in enumerate(specs,1):
        rows.append({'verification_id':vid,'sequence':str(seq),'stage':stage,'subject':subject,'exact_rule':rule,'receipt_field':field,'failure_action':'ABORT_BEFORE_NEXT_PUBLICATION_BOUNDARY_AND_PRESERVE_FAILURE_RECEIPT','publication_blocking':'YES','current_execution_state':'NOT_RUN_DESIGN_ONLY','authority_effect':'READ_ONLY_VERIFICATION_CONTRACT_ONLY','prohibited_inference':'VERIFICATION_RULE_IS_NOT_EVIDENCE_THAT_RUNTIME_BYTES_PATHS_RECEIPTS_OR_SELECTORS_EXIST'})
    return rows


def build_recovery() -> list[dict[str, str]]:
    future='FUTURE_SEPARATE_EXECUTION_AUTHORIZATION_REQUIRED'
    specs=[
        ('MAT-REC-001','GENERATION_PUBLICATION','RENAME_SEALED_TX_GENERATION_TO_GENERATIONS_GENERATION_ID','SAME_DEVICE_NOREPLACE_RENAME_AFTER_TREE_AND_PARENT_FSYNC','FINAL_GENERATION_MAY_EXIST_UNSELECTED','VERIFY_RECEIPT_AND_RESUME_SELECTOR_ONLY_IF_EXACT','NEVER_DELETE_AUTOMATICALLY'),
        ('MAT-REC-002','RECEIPT_PUBLICATION','RENAME_SEALED_RECEIPT_TO_RECEIPTS_GENERATION_ID_JSON','SAME_DEVICE_NOREPLACE_RENAME_AND_PARENT_FSYNC','GENERATION_EXISTS_RECEIPT_MISSING','DO_NOT_SELECT_GENERATION_REGENERATE_ONLY_FROM_PRESERVED_TX_IF_EXACT','NEVER_DELETE_GENERATION_AUTOMATICALLY'),
        ('MAT-REC-003','PREVIOUS_SELECTOR','TEMP_RELATIVE_SYMLINK_TO_PRIOR_CURRENT_THEN_RENAME_PREVIOUS','PREVIOUS_BEFORE_CURRENT_AND_SELECTOR_PARENT_FSYNC','PREVIOUS_UPDATED_CURRENT_STILL_PRIOR_CURRENT','SAFE_BOTH_SELECTORS_MAY_POINT_PRIOR_CURRENT_RESUME_CURRENT_PUBLICATION','TEMP_SELECTOR_ONLY_EXACT_TX_MAY_BE_REMOVED'),
        ('MAT-REC-004','CURRENT_SELECTOR','TEMP_RELATIVE_SYMLINK_TO_NEW_GENERATION_THEN_RENAME_CURRENT','CURRENT_ONLY_AFTER_PREVIOUS_AND_NEW_RECEIPT_VERIFY','CURRENT_RENAMED_PARENT_FSYNC_PENDING','VERIFY_CURRENT_TARGET_COMPLETE_THEN_FSYNC_PARENT_AND_COMPLETE','NEVER_DELETE_SELECTED_GENERATION'),
        ('MAT-REC-005','ROLLBACK_PRECHECK','VERIFY_CURRENT_PREVIOUS_AND_BOTH_RECEIPTS','NO_GENERATION_MUTATION_OR_DELETE','PREVIOUS_MISSING_OR_INVALID','ABORT_ROLLBACK_NO_SELECTOR_CHANGE','NO_DELETE'),
        ('MAT-REC-006','ROLLBACK_SELECTOR_SWAP','LOCKED_TEMP_RELATIVE_SELECTORS_WITH_JOURNAL_SWAP_CURRENT_AND_PREVIOUS','EACH_RENAME_TARGETS_COMPLETE_GENERATION_AND_PARENT_FSYNC','BOTH_SELECTORS_TEMPORARILY_MAY_POINT_SAME_SAFE_GENERATION','RECOVER_FROM_JOURNAL_TO_ONE_OF_TWO_VERIFIED_COMPLETE_STATES','TEMP_SELECTOR_ONLY'),
        ('MAT-REC-007','IDEMPOTENT_RESUME','REOPEN_EXACT_STAGING_TRANSACTION_ID','JOURNAL_DESIGN_AUTHORIZATION_GENERATION_AND_INPUT_DIGESTS_MUST_MATCH','PARTIAL_OBJECTS_LINKS_ALIASES_OR_RECEIPT','REVERIFY_FROM_LAST_SEALED_CHECKPOINT_NEVER_TRUST_FILENAME_ONLY','EXACT_TX_TEMP_ONLY_AFTER_EXPLICIT_QUARANTINE_DECISION'),
        ('MAT-REC-008','CONTENT_ADDRESS_REUSE','REUSE_EXISTING_FINAL_OBJECT_ONLY_AFTER_FULL_VERIFY','NO_OVERWRITE_NO_REPAIR_IN_PLACE','MISMATCHING_OBJECT_AT_EXPECTED_SHA_PATH','ABORT_AND_REPORT_STORE_CORRUPTION','NEVER_DELETE_OR_REPLACE_AUTOMATICALLY'),
        ('MAT-REC-009','ORPHAN_REPORTING','LIST_UNKNOWN_STAGING_TEMP_OBJECTS_UNSELECTED_GENERATIONS_AND_TEMP_SELECTORS','READ_ONLY_CLASSIFICATION_WITH_DEVICE_INODE_OWNER_MODE_AGE_AND_JOURNAL_DIGEST','UNKNOWN_ORPHAN_EXISTS','BLOCK_NEW_MUTATION_IF_COLLIDING_SCOPE_OTHERWISE_REPORT_FOR_OPERATOR','NO_AUTOMATIC_DELETE'),
        ('MAT-REC-010','FAILURE_RECEIPT','WRITE_TX_SCOPED_CANONICAL_FAILURE_RECORD','BINDS_FIRST_FAILURE_STATE_LAST_COMPLETED_CHECKPOINT_PATHS_AND_PROTECTED_SNAPSHOT','FAILURE_RECEIPT_WRITE_FAILS','STOP_AND_PRESERVE_EXISTING_BYTES_NO_BROADER_CLEANUP','NO_DELETE_OUTSIDE_EXACT_TX'),
        ('MAT-REC-011','PROTECTED_STATE','COMPARE_PACKAGE_DB_AND_LIVE_PREFIX_SNAPSHOTS','ZERO_DIFF_REQUIRED','PROTECTED_DIFF_DETECTED','FAIL_TRANSACTION_DO_NOT_PUBLISH_OR_ATTEMPT_AUTOMATIC_REPAIR','NO_PROTECTED_PATH_MUTATION'),
    ]
    rows=[]
    for seq,(cid,cat,normal,atomic,crash,recover,delete) in enumerate(specs,1):
        rows.append({'contract_id':cid,'sequence':str(seq),'category':cat,'normal_path':normal,'atomic_boundary':atomic,'crash_window_state':crash,'recovery_action':recover,'deletion_policy':delete,'authorization_gate':future,'current_authority_state':'NOT_AUTHORIZED_DESIGN_ONLY','prohibited_inference':'RECOVERY_CONTRACT_IS_NOT_PERMISSION_TO_RENAME_DELETE_REPAIR_SELECT_ROLLBACK_POPULATE_DEPLOY_OR_ACTIVATE'})
    return rows


def main() -> None:
    ap=argparse.ArgumentParser()
    ap.add_argument('--repo-root',type=Path,default=Path.cwd())
    ap.add_argument('--output-root',type=Path)
    args=ap.parse_args()
    repo=args.repo_root.resolve(); out=(args.output_root.resolve() if args.output_root else repo)
    data=validate_sources(repo)
    object_plan=build_object_plan(data)
    inputs=build_inputs(repo,data)
    states=build_states(); operations=build_operations(); preflight=build_preflight(); verification=build_verification(); recovery=build_recovery()
    outputs=[
        (OBJECT_PLAN,OBJECT_FIELDS,object_plan),(INPUT_CONTRACT,INPUT_FIELDS,inputs),(STATE_MACHINE,STATE_FIELDS,states),
        (OPERATIONS,OP_FIELDS,operations),(PREFLIGHT,PREFLIGHT_FIELDS,preflight),(VERIFICATION,VERIFY_FIELDS,verification),
        (RECOVERY,RECOVERY_FIELDS,recovery),
    ]
    for rel,fields,rows in outputs: write_tsv(out/rel,fields,rows)
    source_locks={k:{'path':str(SOURCE_PATHS[k]),'sha256':sha256_file(repo/SOURCE_PATHS[k])} for k in sorted(SOURCE_PATHS)}
    design={
        'schema_version':1,'design_review_id':DESIGN_ID,'candidate_state':'QUALIFIED_NON_EXECUTING_READ_ONLY_DESIGN_CANDIDATE',
        'acceptance_gate':ACCEPTANCE_GATE,'next_action':NEXT_ACTION,'generation_base':GENERATION_BASE,
        'exact_member_count':41,'alias_count':41,'target_row_count':82,'exact_member_bytes':EXACT_MEMBER_BYTES,
        'receipt_reservation_bytes':RECEIPT_RESERVATION_BYTES,'final_resource_preflight_bytes':FINAL_PREFLIGHT_BYTES,
        'generation_id_rule':'SHA256_CANONICAL_AUTHORITY_SNAPSHOT_JSON_FULL_64_HEX',
        'transaction_id_rule':'SHA256_GENERATION_ID_NUL_EXECUTION_AUTHORIZATION_ID_FULL_64_HEX',
        'object_store_rule':'objects/sha256/<first-two-hex>/<full-member-sha256>',
        'generation_rule':'generations/<generation-id>/lib/<manifest-basename>',
        'selector_rule':'current_and_previous_are_relative_symlinks_to_complete_verified_generations',
        'local_supply_interface':'SEPARATE_FUTURE_41_ROW_LOCAL_READ_ONLY_SUPPLY_MAP_REQUIRED_NO_DOWNLOAD_AUTHORITY_FROM_DESIGN',
        'copy_policy':'HARDLINK_ONLY_FROM_VERIFIED_CONTENT_ADDRESS_STORE_NO_COPY_FALLBACK',
        'receipt_policy':'CANONICAL_JSON_AT_MOST_1048576_BYTES_OVERFLOW_ABORTS_BEFORE_PUBLICATION',
        'authority_boundary':'READ_ONLY_DESIGN_CANDIDATE_ONLY_NO_BYTE_ACQUISITION_ROOT_CREATION_TARGET_WRITE_MATERIALIZATION_POPULATION_PUBLICATION_DEPLOYMENT_OR_ACTIVATION',
        'source_locks':source_locks,'object_plan':object_plan,'input_contracts':inputs,'state_machine':states,
        'operation_contracts':operations,'runtime_preflight_contracts':preflight,'verification_contracts':verification,
        'publication_recovery_contracts':recovery,
    }
    design_path=out/DESIGN_JSON;design_path.parent.mkdir(parents=True,exist_ok=True)
    design_bytes=(json.dumps(design,sort_keys=True,indent=2,separators=(',',': '),ensure_ascii=True)+'\n').encode()
    design_path.write_bytes(design_bytes)
    meta_rows=[
        ('schema_version','1'),('design_review_id',DESIGN_ID),('candidate_state','QUALIFIED_NON_EXECUTING_READ_ONLY_DESIGN_CANDIDATE'),
        ('acceptance_gate',ACCEPTANCE_GATE),('source_input_count',str(len(inputs))),('object_plan_row_count',str(len(object_plan))),
        ('state_machine_row_count',str(len(states))),('operation_contract_row_count',str(len(operations))),('runtime_preflight_row_count',str(len(preflight))),
        ('verification_contract_row_count',str(len(verification))),('publication_recovery_row_count',str(len(recovery))),
        ('target_row_count','82'),('regular_object_count','41'),('alias_count','41'),('atomic_family_count','4'),
        ('exact_member_bytes',str(EXACT_MEMBER_BYTES)),('receipt_reservation_bytes',str(RECEIPT_RESERVATION_BYTES)),
        ('final_resource_preflight_bytes',str(FINAL_PREFLIGHT_BYTES)),('generation_base',GENERATION_BASE),
        ('object_store_rule','objects/sha256/<first-two-hex>/<full-member-sha256>'),
        ('copy_policy','HARDLINK_ONLY_FROM_VERIFIED_CONTENT_ADDRESS_STORE_NO_COPY_FALLBACK'),
        ('local_supply_interface','SEPARATE_FUTURE_41_ROW_LOCAL_READ_ONLY_SUPPLY_MAP_REQUIRED'),
        ('design_json_sha256',sha256_bytes(design_bytes)),('design_json_bytes',str(len(design_bytes))),
        ('design_acceptance_state','OPEN_SEPARATE_ACCEPTANCE_REQUIRED'),('execution_authorized','NO'),
        ('target_population_authorized','NO'),('byte_acquisition_authorized','NO'),('generation_root_creation_authorized','NO'),
        ('materialization_authorized','NO'),('publication_authorized','NO'),('deployment_authorized','NO'),('activation_authorized','NO'),
        ('next_action',NEXT_ACTION),
        ('authority_effect','QUALIFIED_NON_EXECUTING_READ_ONLY_DESIGN_CANDIDATE_ONLY'),
        ('prohibited_inference','DESIGN_QUALIFICATION_DOES_NOT_AUTHORIZE_LOCALIZATION_DOWNLOAD_BYTE_READ_EXTRACTION_ROOT_CREATION_OBJECT_STORE_OR_GENERATION_WRITE_HARDLINK_SYMLINK_RECEIPT_SELECTOR_POPULATION_PUBLICATION_DEPLOYMENT_OR_ACTIVATION'),
    ]
    write_tsv(out/METADATA,['key','value'],[{'key':k,'value':v} for k,v in meta_rows])

if __name__=='__main__':main()
