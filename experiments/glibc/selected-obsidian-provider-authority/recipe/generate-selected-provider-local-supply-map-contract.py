#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

BASE = Path('experiments/glibc/selected-obsidian-provider-authority')
REVIEW = BASE / 'review'
REVIEW_ID = 'SELECTED-PROVIDER-LOCAL-SUPPLY-MAP-CONTRACT-REVIEW-001'
ACCEPTANCE_GATE = 'SELECTED-PROVIDER-LOCAL-SUPPLY-MAP-CONTRACT-ACCEPTANCE-OPEN'
NEXT_ACTION = 'review-and-accept-non-mutating-selected-provider-local-supply-map-contract-boundary'

OBJECT_PLAN = REVIEW / 'selected-target-materializer-object-plan.tsv'
DESIGN_ACCEPTANCE = REVIEW / 'selected-target-materializer-runtime-preflight-design-boundary-acceptance.tsv'
CONTRACT = REVIEW / 'selected-provider-local-supply-map-contract.tsv'
VALIDATION = REVIEW / 'selected-provider-local-supply-map-validation-contract.tsv'
RECEIPT_SCHEMA = REVIEW / 'selected-provider-local-supply-map-receipt-schema.json'
METADATA = REVIEW / 'selected-provider-local-supply-map-contract-metadata.tsv'

CONTRACT_FIELDS = [
    'contract_row_id', 'sequence', 'materializer_plan_row_id', 'composition_row_id',
    'provider_object_id', 'provider_review_id', 'artifact_package', 'artifact_version',
    'member_basename', 'expected_member_sha256', 'expected_member_size_bytes',
    'expected_soname', 'expected_result_remote', 'expected_drive_file_id',
    'expected_result_sha256', 'result_index_contract_kind',
    'expected_result_index_identity', 'container_class', 'expected_container_locator',
    'expected_member_locator', 'expected_object_store_relative_path',
    'expected_generation_regular_relative_path', 'expected_generation_alias_relative_path',
    'local_path_binding_state', 'local_regular_file_path', 'future_local_path_rule',
    'future_file_type_rule', 'future_symlink_rule', 'future_owner_rule',
    'future_mode_rule', 'future_identity_stability_rule', 'future_content_rule',
    'future_elf_rule', 'future_map_row_state', 'acceptance_gate', 'authority_effect',
    'prohibited_inference'
]

VALIDATION_FIELDS = [
    'validation_id', 'sequence', 'category', 'subject', 'required_rule',
    'future_receipt_field', 'failure_code', 'candidate_evidence_state',
    'mutation_effect', 'authority_effect', 'prohibited_inference'
]


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline='', encoding='utf-8') as fh:
        return list(csv.DictReader(fh, delimiter='\t'))


def write_tsv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', newline='', encoding='utf-8') as fh:
        writer = csv.DictWriter(fh, fieldnames=fields, delimiter='\t', lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def index_contract(row: dict[str, str]) -> tuple[str, str, str]:
    kind = row['supply_closure_kind']
    artifact = row['artifact_evidence_path']
    if kind == 'V101_INDEXED_REPLACEMENT':
        if not artifact.endswith('.deb'):
            raise SystemExit(f'V101 row without exact .deb locator: {row["plan_row_id"]}')
        return 'RESULT_INDEX_SHA256', row['supply_result_index_sha256'], 'INDEXED_RESULT_DEB_MEMBER'
    if kind == 'APPEND_ONLY_LEGACY_INDEX_UPGRADE':
        if not artifact.endswith('.tsv'):
            raise SystemExit(f'legacy row without append-only index locator: {row["plan_row_id"]}')
        return 'APPEND_ONLY_INDEX_RECEIPT_SHA256', row['supply_result_index_sha256'], 'APPEND_ONLY_RESULT_FILE_INDEX_MEMBER'
    if kind == 'EXISTING_DIGEST_BOUND_UNCHANGED':
        if row['supply_result_index_sha256'] != 'EXISTING_AUTHORITY_DIGEST':
            raise SystemExit(f'existing row index sentinel drift: {row["plan_row_id"]}')
        return 'EXISTING_AUTHORITY_DIGEST_SENTINEL', 'EXISTING_AUTHORITY_DIGEST', 'EXISTING_AUTHORITY_RECORD_MEMBER'
    raise SystemExit(f'unsupported supply closure kind: {kind}')


def validations() -> list[dict[str, str]]:
    specs = [
        ('SOURCE_ACCEPTANCE', 'accepted design authority', 'exact SELECTED-PROVIDER-MATERIALIZER-DESIGN-ACCEPT-001 row and frozen object-plan digest must match', 'design_acceptance_id;source_object_plan_sha256', 'LSM_SOURCE_ACCEPTANCE_MISMATCH'),
        ('CONTRACT_CARDINALITY', 'contract rows', 'exactly 41 contract rows are required', 'contract_row_count', 'LSM_ROW_COUNT_MISMATCH'),
        ('PLAN_BIJECTION', 'materializer plan binding', 'each accepted MAT-OBJ row occurs exactly once and no unknown plan row is present', 'materializer_plan_row_id', 'LSM_PLAN_BIJECTION_FAILED'),
        ('OBJECT_UNIQUENESS', 'provider object identity', 'provider_object_id and expected_member_sha256 are unique across all 41 rows', 'provider_object_id;expected_member_sha256', 'LSM_OBJECT_DUPLICATE'),
        ('CANDIDATE_EMPTY_PATHS', 'candidate local paths', 'candidate contract contains zero populated local_regular_file_path values', 'populated_local_path_count', 'LSM_CANDIDATE_PATH_PRESENT'),
        ('FUTURE_RECEIPT_CARDINALITY', 'future local map rows', 'a future receipt must contain exactly 41 rows with the same contract_row_id set', 'rows', 'LSM_FUTURE_ROW_COUNT_MISMATCH'),
        ('ABSOLUTE_CANONICAL_PATH', 'future local regular-file path', 'path must be absolute canonical text with no dot dot component, glob, variable or search expression', 'local_regular_file_path', 'LSM_PATH_NOT_CANONICAL'),
        ('PATH_UNIQUENESS', 'future local regular-file path set', 'all 41 future local paths must be unique', 'local_regular_file_path', 'LSM_PATH_COLLISION'),
        ('NO_SEARCH_DISCOVERY', 'path provenance', 'path must be supplied by a separately authorized localization receipt; recursive search and filename discovery are forbidden', 'localization_receipt_id;local_regular_file_path', 'LSM_DISCOVERY_NOT_AUTHORIZED'),
        ('NO_SYMLINK_COMPONENTS', 'path traversal', 'lstat every path component and reject symlinks; final open uses O_RDONLY O_CLOEXEC O_NOFOLLOW', 'component_lstat;open_flags', 'LSM_SYMLINK_REJECTED'),
        ('REGULAR_FILE_ONLY', 'opened local object', 'final lstat and fstat must both report a regular file', 'lstat_mode;fstat_mode', 'LSM_NOT_REGULAR_FILE'),
        ('OWNER_BOUNDARY', 'local object owner', 'st_uid must equal the read-only localization transaction uid', 'st_uid;transaction_uid', 'LSM_OWNER_MISMATCH'),
        ('MODE_BOUNDARY', 'local object mode', 'group-write and other-write bits must be zero', 'st_mode', 'LSM_MODE_WRITABLE'),
        ('STABLE_FILE_IDENTITY', 'read stability', 'device inode size mtime_ns and ctime_ns must remain identical before open after open and after hashing', 'st_dev;st_ino;st_size;st_mtime_ns;st_ctime_ns', 'LSM_FILE_CHANGED_DURING_READ'),
        ('EXACT_MEMBER_SIZE', 'member byte size', 'fstat size must equal expected_member_size_bytes', 'observed_size_bytes', 'LSM_SIZE_MISMATCH'),
        ('EXACT_MEMBER_SHA256', 'member content digest', 'streamed SHA-256 must equal expected_member_sha256', 'observed_member_sha256', 'LSM_MEMBER_SHA_MISMATCH'),
        ('ELF_IDENTITY', 'ELF class machine and type', 'member must be ELF64 little-endian AArch64 ET_DYN', 'elf_class;elf_data;elf_machine;elf_type', 'LSM_ELF_IDENTITY_MISMATCH'),
        ('SONAME_IDENTITY', 'ELF SONAME', 'DT_SONAME must equal expected_soname exactly', 'observed_soname', 'LSM_SONAME_MISMATCH'),
        ('RESULT_OUTER_IDENTITY', 'retained result identity', 'future localization receipt must bind expected_result_sha256 and expected_result_remote or accepted digest sentinel exactly', 'result_remote;result_sha256', 'LSM_RESULT_IDENTITY_MISMATCH'),
        ('RESULT_INDEX_IDENTITY', 'result index identity', 'result index kind and exact SHA or accepted existing-authority sentinel must match the contract', 'result_index_contract_kind;result_index_identity', 'LSM_RESULT_INDEX_MISMATCH'),
        ('CONTAINER_LOCATOR', 'container locator', 'container class and exact container locator must match; no basename fallback is permitted', 'container_class;container_locator', 'LSM_CONTAINER_LOCATOR_MISMATCH'),
        ('MEMBER_LOCATOR', 'member locator', 'exact member locator must match with no absolute-to-relative rewriting or basename fallback', 'member_locator', 'LSM_MEMBER_LOCATOR_MISMATCH'),
        ('ATOMIC_FAMILY_COMPLETENESS', 'atomic provider families', 'AT-SPI2 Cairo Pango and GDK/GTK families must be present and valid as complete units', 'atomic_family_results', 'LSM_ATOMIC_FAMILY_INCOMPLETE'),
        ('CANONICAL_RECEIPT_AND_FAIL_CLOSED', 'receipt and failure semantics', 'canonical compact UTF-8 JSON is digest-bound; any failed row rejects the whole map and produces no accepted local map', 'receipt_sha256;decision', 'LSM_RECEIPT_REJECTED'),
    ]
    rows = []
    for i, (cat, subj, rule, field, code) in enumerate(specs, 1):
        rows.append({
            'validation_id': f'LSM-VAL-{i:03d}', 'sequence': str(i), 'category': cat,
            'subject': subj, 'required_rule': rule, 'future_receipt_field': field,
            'failure_code': code, 'candidate_evidence_state': 'CONTRACT_DEFINED_NOT_RUN',
            'mutation_effect': 'NONE_READ_ONLY_VALIDATION_CONTRACT',
            'authority_effect': 'FUTURE_LOCAL_MAP_VALIDATION_RULE_ONLY_NO_PATH_OR_BYTE_AUTHORITY',
            'prohibited_inference': 'VALIDATION_CONTRACT_DOES_NOT_AUTHORIZE_SEARCH_READ_DOWNLOAD_EXTRACTION_LOCALIZATION_EXECUTION_OBJECT_WRITE_POPULATION_PUBLICATION_DEPLOYMENT_OR_ACTIVATION'
        })
    return rows


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo-root', type=Path, default=Path('.'))
    ap.add_argument('--output-root', type=Path, default=None)
    args = ap.parse_args()
    repo = args.repo_root.resolve()
    out = (args.output_root or repo).resolve()

    plan_path = repo / OBJECT_PLAN
    acceptance_path = repo / DESIGN_ACCEPTANCE
    plan = read_tsv(plan_path)
    acceptance = read_tsv(acceptance_path)
    if len(plan) != 41:
        raise SystemExit(f'expected 41 materializer object rows, got {len(plan)}')
    if len(acceptance) != 1 or acceptance[0]['decision'] != 'ACCEPTED_BOUNDED_NON_EXECUTING_READ_ONLY_MATERIALIZER_RUNTIME_PREFLIGHT_DESIGN':
        raise SystemExit('accepted materializer design boundary missing')
    if acceptance[0]['source_object_plan_sha256'] != sha256_file(plan_path):
        raise SystemExit('accepted object-plan digest mismatch')
    if acceptance[0]['execution_authorization_state'] != 'NOT_AUTHORIZED_SEPARATE_EXPLICIT_DECISION_REQUIRED':
        raise SystemExit('execution authority unexpectedly widened')

    contract_rows: list[dict[str, str]] = []
    seen_plan: set[str] = set()
    seen_obj: set[str] = set()
    seen_sha: set[str] = set()
    for n, source in enumerate(plan, 1):
        if source['plan_row_id'] in seen_plan or source['provider_object_id'] in seen_obj or source['member_sha256'] in seen_sha:
            raise SystemExit(f'duplicate plan/object/member identity at {source["plan_row_id"]}')
        seen_plan.add(source['plan_row_id']); seen_obj.add(source['provider_object_id']); seen_sha.add(source['member_sha256'])
        index_kind, index_identity, container_class = index_contract(source)
        contract_rows.append({
            'contract_row_id': f'LSM-CONTRACT-{n:03d}', 'sequence': str(n),
            'materializer_plan_row_id': source['plan_row_id'], 'composition_row_id': source['composition_row_id'],
            'provider_object_id': source['provider_object_id'], 'provider_review_id': source['provider_review_id'],
            'artifact_package': source['artifact_package'], 'artifact_version': source['artifact_version'],
            'member_basename': source['member_basename'], 'expected_member_sha256': source['member_sha256'],
            'expected_member_size_bytes': source['member_size_bytes'], 'expected_soname': source['soname'],
            'expected_result_remote': source['supply_result_remote'], 'expected_drive_file_id': source['supply_drive_file_id'],
            'expected_result_sha256': source['supply_result_sha256'], 'result_index_contract_kind': index_kind,
            'expected_result_index_identity': index_identity, 'container_class': container_class,
            'expected_container_locator': source['artifact_evidence_path'], 'expected_member_locator': source['member_evidence_path'],
            'expected_object_store_relative_path': source['object_store_relative_path'],
            'expected_generation_regular_relative_path': source['generation_regular_relative_path'],
            'expected_generation_alias_relative_path': source['generation_alias_relative_path'],
            'local_path_binding_state': 'UNBOUND_CONTRACT_ONLY', 'local_regular_file_path': '',
            'future_local_path_rule': 'SEPARATE_AUTHORIZED_READ_ONLY_LOCALIZATION_RECEIPT_SUPPLIES_ONE_ABSOLUTE_CANONICAL_PATH_NO_GLOB_SEARCH_OR_VARIABLE_EXPANSION',
            'future_file_type_rule': 'LSTAT_AND_FSTAT_REGULAR_FILE_ONLY_OPEN_RDONLY_CLOEXEC_NOFOLLOW',
            'future_symlink_rule': 'LSTAT_EACH_COMPONENT_REJECT_ANY_SYMLINK_FINAL_PATH_O_NOFOLLOW_AND_DEV_INO_MATCH',
            'future_owner_rule': 'ST_UID_EQUALS_LOCALIZATION_TRANSACTION_UID',
            'future_mode_rule': 'GROUP_AND_OTHER_WRITE_BITS_MUST_BE_ZERO',
            'future_identity_stability_rule': 'DEV_INO_SIZE_MTIME_NS_CTIME_NS_STABLE_BEFORE_OPEN_AFTER_OPEN_AND_AFTER_HASH',
            'future_content_rule': 'EXACT_SIZE_AND_STREAMED_SHA256_MUST_MATCH_CONTRACT',
            'future_elf_rule': 'ELF64_LITTLE_ENDIAN_AARCH64_ET_DYN_AND_EXACT_DT_SONAME',
            'future_map_row_state': 'SCHEMA_QUALIFIED_NOT_POPULATED', 'acceptance_gate': ACCEPTANCE_GATE,
            'authority_effect': 'NON_MUTATING_LOCAL_SUPPLY_MAP_CONTRACT_ROW_ONLY_NO_LOCAL_PATH_OR_BYTE_AUTHORITY',
            'prohibited_inference': 'CONTRACT_ROW_DOES_NOT_PRODUCE_OR_AUTHORIZE_LOCAL_PATH_SEARCH_BYTE_READ_DOWNLOAD_EXTRACTION_EXECUTION_OBJECT_STORE_GENERATION_POPULATION_PUBLICATION_DEPLOYMENT_OR_ACTIVATION'
        })

    validation_rows = validations()
    contract_out = out / CONTRACT
    validation_out = out / VALIDATION
    schema_out = out / RECEIPT_SCHEMA
    metadata_out = out / METADATA
    write_tsv(contract_out, CONTRACT_FIELDS, contract_rows)
    write_tsv(validation_out, VALIDATION_FIELDS, validation_rows)

    schema = {
        'schema_version': 1,
        'receipt_schema_id': 'SELECTED-PROVIDER-LOCAL-SUPPLY-MAP-RECEIPT-SCHEMA-001',
        'contract_review_id': REVIEW_ID,
        'candidate_state': 'QUALIFIED_NON_MUTATING_LOCAL_SUPPLY_MAP_CONTRACT_CANDIDATE',
        'acceptance_gate': ACCEPTANCE_GATE,
        'receipt_state': 'SCHEMA_ONLY_NO_RECEIPT_PRODUCED',
        'required_future_row_count': 41,
        'current_populated_row_count': 0,
        'current_rows': [],
        'canonicalization': 'UTF8_JSON_SORT_KEYS_TRUE_SEPARATORS_COMMA_COLON_TRAILING_NEWLINE_NONE',
        'required_top_level_fields': [
            'schema_version', 'receipt_schema_id', 'contract_review_id', 'design_acceptance_id',
            'localization_transaction_id', 'transaction_uid', 'generated_at_utc',
            'contract_sha256', 'validation_contract_sha256', 'row_count', 'rows',
            'atomic_family_results', 'decision', 'failure_codes', 'receipt_sha256'
        ],
        'required_row_fields': [
            'contract_row_id', 'materializer_plan_row_id', 'provider_object_id',
            'local_regular_file_path', 'result_remote', 'result_sha256',
            'result_index_contract_kind', 'result_index_identity', 'container_class',
            'container_locator', 'member_locator', 'st_uid', 'st_mode', 'st_dev',
            'st_ino', 'st_size', 'st_mtime_ns', 'st_ctime_ns', 'observed_member_sha256',
            'elf_class', 'elf_data', 'elf_machine', 'elf_type', 'observed_soname',
            'validation_state', 'failure_codes'
        ],
        'validation_order': [r['validation_id'] for r in validation_rows],
        'decision_rule': 'ACCEPT_ONLY_IF_ALL_41_ROWS_AND_ALL_24_VALIDATIONS_PASS_OTHERWISE_REJECT_WHOLE_MAP',
        'path_authority': 'NONE_SCHEMA_ONLY',
        'byte_read_authority': 'NONE_SCHEMA_ONLY',
        'execution_authority': 'NONE_SEPARATE_EXPLICIT_DECISION_REQUIRED',
        'target_population_authority': 'NONE',
        'materialization_authority': 'NONE',
        'publication_authority': 'NONE',
        'prohibited_inference': 'RECEIPT_SCHEMA_DOES_NOT_AUTHORIZE_LOCAL_DISCOVERY_READ_DOWNLOAD_EXTRACTION_PATH_CREATION_OBJECT_WRITE_EXECUTION_POPULATION_PUBLICATION_DEPLOYMENT_OR_ACTIVATION'
    }
    schema_out.parent.mkdir(parents=True, exist_ok=True)
    schema_out.write_text(json.dumps(schema, sort_keys=True, separators=(',', ':'), ensure_ascii=True) + '\n', encoding='utf-8')

    metadata_rows = [
        ('schema_version', '1'),
        ('contract_review_id', REVIEW_ID),
        ('candidate_state', 'QUALIFIED_NON_MUTATING_LOCAL_SUPPLY_MAP_CONTRACT_CANDIDATE'),
        ('acceptance_gate', ACCEPTANCE_GATE),
        ('source_design_acceptance_id', 'SELECTED-PROVIDER-MATERIALIZER-DESIGN-ACCEPT-001'),
        ('source_design_acceptance_sha256', sha256_file(acceptance_path)),
        ('source_object_plan_sha256', sha256_file(plan_path)),
        ('contract_row_count', str(len(contract_rows))),
        ('validation_rule_count', str(len(validation_rows))),
        ('expected_future_map_row_count', '41'),
        ('current_populated_local_path_count', '0'),
        ('result_index_sha256_row_count', str(sum(r['result_index_contract_kind'] == 'RESULT_INDEX_SHA256' for r in contract_rows))),
        ('append_only_index_receipt_row_count', str(sum(r['result_index_contract_kind'] == 'APPEND_ONLY_INDEX_RECEIPT_SHA256' for r in contract_rows))),
        ('existing_authority_digest_sentinel_row_count', str(sum(r['result_index_contract_kind'] == 'EXISTING_AUTHORITY_DIGEST_SENTINEL' for r in contract_rows))),
        ('contract_sha256', sha256_file(contract_out)),
        ('validation_contract_sha256', sha256_file(validation_out)),
        ('receipt_schema_sha256', sha256_file(schema_out)),
        ('local_supply_map_contract_state', 'QUALIFIED_CANDIDATE_ACCEPTANCE_OPEN'),
        ('local_supply_map_state', 'NOT_PRODUCED_NOT_AUTHORIZED'),
        ('local_path_discovery_authorized', 'NO'),
        ('byte_read_authorized', 'NO'),
        ('execution_authorized', 'NO'),
        ('generation_root_creation_authorized', 'NO'),
        ('target_population_authorized', 'NO'),
        ('materialization_authorized', 'NO'),
        ('publication_authorized', 'NO'),
        ('deployment_authorized', 'NO'),
        ('activation_authorized', 'NO'),
        ('next_action', NEXT_ACTION),
        ('authority_effect', 'QUALIFIED_NON_MUTATING_41_ROW_LOCAL_SUPPLY_MAP_CONTRACT_CANDIDATE_ONLY'),
        ('prohibited_inference', 'CONTRACT_QUALIFICATION_DOES_NOT_PRODUCE_A_LOCAL_MAP_OR_AUTHORIZE_PATH_SEARCH_BYTE_READ_DOWNLOAD_EXTRACTION_EXECUTION_ROOT_CREATION_POPULATION_MATERIALIZATION_PUBLICATION_DEPLOYMENT_OR_ACTIVATION'),
    ]
    write_tsv(metadata_out, ['key', 'value'], [{'key': k, 'value': v} for k, v in metadata_rows])


if __name__ == '__main__':
    main()
