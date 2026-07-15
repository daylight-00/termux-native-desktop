#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT_REVIEW = Path('experiments/glibc/selected-obsidian-provider-authority/review/generic-build-attestation-adaptation-root-review-set.tsv')
OBJECT_REVIEW = Path('experiments/glibc/selected-obsidian-provider-authority/review/generic-build-attestation-adaptation-object-review-set.tsv')
SUP02_REQUESTS = Path('experiments/glibc/selected-obsidian-provider-authority/review/generic-build-attestation-adaptation-gap-evidence-supply-batch-sup-02-custodian-export-requests.tsv')
SEMANTIC_REVIEW = Path('experiments/glibc/selected-obsidian-provider-authority/review/no-token-recipe-semantic-review.tsv')
PROVIDER_REVIEW = Path('experiments/glibc/selected-obsidian-provider-authority/review/xorg-reference-consumed-provider-authority.tsv')

CLAIM_OUTPUT = Path('experiments/glibc/selected-obsidian-provider-authority/review/provider-claim-classification.tsv')
SUP02_OUTPUT = Path('experiments/glibc/selected-obsidian-provider-authority/review/provider-sup-02-request-disposition.tsv')
METADATA_OUTPUT = Path('experiments/glibc/selected-obsidian-provider-authority/review/provider-claim-classification-metadata.tsv')

CLAIM_FIELDS = [
    'claim_id', 'subject_kind', 'subject_id', 'subject_label', 'claim_type',
    'requested_state', 'adr_class', 'supplier_or_reference_boundary',
    'project_owned_changed_boundary', 'risk_modifiers', 'existing_evidence',
    'remaining_gap', 'minimum_closure_action', 'explicitly_excluded_evidence',
    'escalation_trigger', 'classification_state', 'authority_effect',
    'prohibited_inference',
]

SUP02_FIELDS = [
    'request_id', 'root_review_id', 'recipe_root', 'review_tier',
    'primary_claim_class', 'disposition', 'required_now', 'replacement_or_narrowed_scope',
    'retained_escalation_trigger', 'rationale', 'authority_effect', 'next_action',
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


def slug(value: str) -> str:
    return re.sub(r'[^A-Z0-9]+', '-', value.upper()).strip('-')


def join_unique(values: list[str]) -> str:
    return ';'.join(sorted({v for v in values if v})) or 'NONE'


def root_risk(root: dict[str, str], objects: list[dict[str, str]]) -> str:
    risks: list[str] = []
    partitions = {row['capability_partition'] for row in objects}
    if 'security' in partitions:
        risks.append('SECURITY_OR_DATA_INTEGRITY')
    if 'graphics' in partitions:
        risks.append('GPU_ABI_OR_MEMORY_SAFETY')
    if 'printing' in partitions:
        risks.append('SERVICE_TLS_OR_NETWORK_INTEGRATION')
    if 'audio' in partitions:
        risks.append('DEVICE_IO')
    if 'gtk-gui' in partitions:
        risks.append('GUI_MULTI_CONSUMER')
    if len(objects) > 1:
        risks.append('MULTI_OBJECT_ROOT')
    if root['concrete_filename_requirement_set'] != 'NONE':
        risks.append('CONCRETE_FILENAME_DRIFT')
    tier = root['review_tier']
    if tier.startswith(('T1_', 'T2_')):
        risks.append('MATERIAL_RECIPE_DELTA')
    elif tier.startswith('T4_'):
        risks.append('CONFIGURATION_OR_PACKAGING_DELTA')
    elif tier.startswith(('T5_', 'T6_')):
        risks.append('NO_EXPLICIT_DELTA_TOKEN')
    if root['object_correction_requirement_set'] != 'NONE':
        risks.append('OBJECT_REQUIREMENT_CONFLICT')
    return join_unique(risks)


def sup02_disposition(tier: str) -> str:
    if tier.startswith(('T1_', 'T2_')):
        return 'NARROWED'
    if tier.startswith(('T4_', 'T5_')):
        return 'REPLACED'
    if tier.startswith(('T0_', 'T6_')):
        return 'UNNECESSARY'
    raise ValueError(f'unclassified review tier: {tier}')


def adaptation_class(root: dict[str, str]) -> str:
    return 'A' if root['adaptation_evidence_tokens'] == 'NONE_DECLARED' else 'B'


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo-root', type=Path, default=Path.cwd())
    parser.add_argument('--output-root', type=Path)
    args = parser.parse_args()
    repo = args.repo_root.resolve()
    out_root = args.output_root.resolve() if args.output_root else repo

    roots = read_tsv(repo / ROOT_REVIEW)
    objects = read_tsv(repo / OBJECT_REVIEW)
    requests = read_tsv(repo / SUP02_REQUESTS)
    semantic_reviews = read_tsv(repo / SEMANTIC_REVIEW)
    provider_reviews = read_tsv(repo / PROVIDER_REVIEW)
    if len(roots) != 28:
        raise SystemExit(f'expected 28 root rows, found {len(roots)}')
    if len(objects) != 37:
        raise SystemExit(f'expected 37 object rows, found {len(objects)}')
    if len(requests) != 28:
        raise SystemExit(f'expected 28 SUP-02 requests, found {len(requests)}')
    if len(semantic_reviews) != 7:
        raise SystemExit(f'expected 7 no-token semantic reviews, found {len(semantic_reviews)}')
    if len(provider_reviews) != 4:
        raise SystemExit(f'expected 4 X.Org provider reviews, found {len(provider_reviews)}')
    semantic_by_root = {row['root_review_id']: row for row in semantic_reviews}
    if len(semantic_by_root) != len(semantic_reviews):
        raise SystemExit('duplicate root_review_id in no-token semantic review')
    expected_no_token = {row['root_review_id'] for row in roots if row['adaptation_evidence_tokens'] == 'NONE_DECLARED'}
    if set(semantic_by_root) != expected_no_token:
        raise SystemExit('no-token semantic reviews do not exactly cover canonical no-token roots')
    for row in semantic_reviews:
        if row['semantic_result'] not in {'CONFIRMED_A', 'RECLASSIFIED_B'}:
            raise SystemExit(f"invalid semantic result for {row['root_review_id']}: {row['semantic_result']}")

    provider_by_root = {row['root_review_id']: row for row in provider_reviews}
    if len(provider_by_root) != len(provider_reviews):
        raise SystemExit('duplicate root_review_id in X.Org provider review')
    expected_provider_roots = {
        row['root_review_id'] for row in semantic_reviews
        if row['recipe_root'] in {'gpkg/libxfixes', 'gpkg/libxcomposite', 'gpkg/libxi', 'gpkg/libxinerama'}
    }
    if set(provider_by_root) != expected_provider_roots:
        raise SystemExit('X.Org provider reviews do not exactly cover the four canonical roots')
    for row in provider_reviews:
        if row['decision'] != 'ACCEPTED_BOUNDED_PROVIDER':
            raise SystemExit(f"invalid X.Org provider decision for {row['root_review_id']}: {row['decision']}")

    objects_by_root: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in objects:
        objects_by_root[row['recipe_root']].append(row)

    claims: list[dict[str, str]] = []
    for root in sorted(roots, key=lambda row: row['recipe_root']):
        recipe_root = root['recipe_root']
        root_objects = objects_by_root[recipe_root]
        root_slug = slug(recipe_root.removeprefix('gpkg/'))
        object_ids = join_unique([row['object_review_id'] for row in root_objects])
        partitions = join_unique([row['capability_partition'] for row in root_objects])
        risks = root_risk(root, root_objects)
        common_evidence = (
            f"{root['root_review_id']};{root['artifact_ids']};{object_ids};"
            'generic-artifact-member-comparison-artifacts.tsv;'
            'generic-recipe-binding-and-drift-target-receipt-review.tsv'
        )

        if root['object_correction_requirement_set'] != 'NONE':
            artifact_gap = 'OJ-001_REQUIRED_SONAME_LIBJPEG_SO_62_HAS_NO_BOUND_PROVIDER_CANDIDATE'
            artifact_action = 'LOCATE_EXACT_LIBJPEG_SO_62_PROVIDER_OR_REVIEW_AUTHORITATIVE_REQUIREMENT'
            artifact_state = 'OPEN_REQUIREMENT_CORRECT_PROVIDER_CANDIDATE_ABSENT'
        else:
            artifact_gap = 'NONE_FOR_EXACT_CANDIDATE_ARTIFACT_AND_NAMED_MEMBER_IDENTITY'
            artifact_action = 'NONE_RETAIN_EXACT_ARTIFACT_AND_MEMBER_DIGESTS_AT_TRANSFER'
            artifact_state = 'EVIDENCE_SUFFICIENT_FOR_CANDIDATE_IDENTITY_ONLY'

        claims.append({
            'claim_id': f'PCC-{root_slug}-ARTIFACT',
            'subject_kind': 'ROOT',
            'subject_id': root['root_review_id'],
            'subject_label': recipe_root,
            'claim_type': 'ARTIFACT_IDENTITY',
            'requested_state': 'EXACT_REFERENCE_ARTIFACT_AND_NAMED_MEMBER_CANDIDATE_IDENTITY',
            'adr_class': 'A',
            'supplier_or_reference_boundary': 'AUTHORITATIVE_TERMUX_GLIBC_PACKAGE_REPOSITORY_ARTIFACT',
            'project_owned_changed_boundary': 'ACQUIRE_RETAIN_HASH_AND_BIND_NAMED_MEMBERS_WITHOUT_RECONSTRUCTING_SUPPLIER_BUILD_HISTORY',
            'risk_modifiers': risks,
            'existing_evidence': common_evidence,
            'remaining_gap': artifact_gap,
            'minimum_closure_action': artifact_action,
            'explicitly_excluded_evidence': 'CUSTODIAN_BUILD_INVOCATION;FULL_BUILD_ENVIRONMENT;INDEPENDENT_REPRODUCTION',
            'escalation_trigger': 'ARTIFACT_DIGEST_MISMATCH;MEMBER_OR_SONAME_MISMATCH;SUPPLIER_OPACITY_AFFECTING_THE_EXACT_IDENTITY_CLAIM',
            'classification_state': artifact_state,
            'authority_effect': 'CANDIDATE_IDENTITY_ONLY_NO_PROVIDER_OR_TARGET_EFFECT',
            'prohibited_inference': 'EXACT_ARTIFACT_IDENTITY_DOES_NOT_IMPLY_ADAPTATION_ACCEPTANCE_PROVIDER_AUTHORITY_OR_TARGET_MEMBERSHIP',
        })

        no_tokens = root['adaptation_evidence_tokens'] == 'NONE_DECLARED'
        semantic_review = semantic_by_root.get(root['root_review_id'])
        aclass = semantic_review['adr_class_result'] if semantic_review else adaptation_class(root)
        if no_tokens and semantic_review:
            adaptation_gap = 'NONE_FOR_PACKAGE_SPECIFIC_RECIPE_ADAPTATION_CLASSIFICATION'
            adaptation_action = 'PROCEED_TO_BOUNDED_PROVIDER_AUTHORITY_REVIEW_WITHOUT_SUPPLIER_BUILD_RECONSTRUCTION'
            adaptation_state = ('CLASS_A_CONFIRMED_RECIPE_SEMANTIC_REVIEW_COMPLETE' if semantic_review['semantic_result'] == 'CONFIRMED_A' else 'CLASS_B_RECLASSIFIED_RECIPE_SEMANTIC_REVIEW_COMPLETE')
            adaptation_boundary = semantic_review['project_owned_changed_boundary']
            adaptation_evidence_suffix = f";{SEMANTIC_REVIEW.name};{semantic_review['review_id']}"
        else:
            adaptation_gap = 'AD-001_AD-002_AD-003_AD-004_SEMANTIC_DELTA_NECESSITY_AND_OBJECT_IMPACT_REVIEW'
            adaptation_action = 'AGENT_SEMANTIC_DELTA_REVIEW_WITH_OBJECT_IMPACT_AND_PLATFORM_NECESSITY_CLASSIFICATION'
            adaptation_state = 'CLASSIFIED_OPEN_REVIEW_REQUIRED'
            adaptation_boundary = 'EXACT_RECIPE_PATCH_HOOK_CONFIGURATION_AND_PACKAGING_DELTAS_RELIED_ON_BY_THE_PROJECT'
            adaptation_evidence_suffix = ''
        if root['concrete_filename_requirement_set'] != 'NONE':
            adaptation_gap += ';CF-001_CF-002_CF-003_CF-004_ALIAS_SUCCESSOR_AND_ROLLBACK_POLICY'
            adaptation_action += ';REVIEW_CONSUMER_ALIAS_BINDING_AND_VERSION_DRIFT_POLICY'
        if root['object_correction_requirement_set'] != 'NONE':
            adaptation_gap += ';OJ-001_PROVIDER_CANDIDATE_ABSENT'
            adaptation_action = 'DEFER_ROOT_PROVIDER_REVIEW_UNTIL_OJ-001_EXACT_PROVIDER_CANDIDATE_IS_RESOLVED'

        claims.append({
            'claim_id': f'PCC-{root_slug}-ADAPTATION',
            'subject_kind': 'ROOT',
            'subject_id': root['root_review_id'],
            'subject_label': recipe_root,
            'claim_type': 'ADAPTATION_SEMANTICS',
            'requested_state': 'REFERENCE_RECIPE_EQUIVALENCE_OR_BOUNDED_TERMUX_ANDROID_ADAPTATION',
            'adr_class': aclass,
            'supplier_or_reference_boundary': 'PINNED_TERMUX_GLIBC_RECIPE_TREE_AND_PINNED_UPSTREAM_SOURCE',
            'project_owned_changed_boundary': adaptation_boundary,
            'risk_modifiers': risks,
            'existing_evidence': (
                f"{root['root_review_id']};recipe_tree={root['recipe_tree']};tokens={root['adaptation_evidence_tokens']};"
                'generic-recipe-binding-and-drift-target-receipt-review.tsv;'
                'generic-build-attestation-adaptation-root-evidence-receipt-review.tsv' + adaptation_evidence_suffix
            ),
            'remaining_gap': adaptation_gap,
            'minimum_closure_action': adaptation_action,
            'explicitly_excluded_evidence': 'SUP-02_CUSTODIAN_EXPORT_UNLESS_RECLASSIFICATION_OR_ESCALATION_TRIGGER_REQUIRES_CLASS_C_DEPTH',
            'escalation_trigger': 'SEMANTIC_REVIEW_CANNOT_BOUND_GENERATED_OUTPUT;OBSERVED_ARTIFACT_BEHAVIOR_CONFLICTS_WITH_RECIPE;CLAIM_RECLASSIFIED_AS_INDEPENDENT_REPRODUCTION;HIGH_RISK_OUTPUT_REMAINS_OPAQUE',
            'classification_state': adaptation_state,
            'authority_effect': ('ADAPTATION_CLASSIFICATION_ONLY_NO_PROVIDER_COMPOSITION_TARGET_OR_ACTIVATION_EFFECT' if semantic_review else 'REVIEW_PLAN_ONLY_NO_ADAPTATION_OR_PROVIDER_ACCEPTANCE'),
            'prohibited_inference': 'RECIPE_TOKEN_PRESENCE_OR_ABSENCE_DOES_NOT_BY_ITSELF_ESTABLISH_PLATFORM_NECESSITY_OR_EQUIVALENCE',
        })

        provider_review = provider_by_root.get(root['root_review_id'])
        if provider_review:
            provider_existing_evidence = (
                f"{common_evidence};authority-coverage-ledger.tsv;generic-source-authority-boundary.tsv;"
                f"selected-object-authority-base.tsv;{PROVIDER_REVIEW.name};{provider_review['review_id']}"
            )
            provider_gap = provider_review['remaining_gap']
            provider_action = 'RETAIN_BOUNDED_PROVIDER_AUTHORITY_AND_REVALIDATE_ON_RECORDED_UPDATE_OR_ROLLBACK_TRIGGER'
            provider_state = 'BOUNDED_PROVIDER_AUTHORITY_ACCEPTED'
            provider_effect = provider_review['authority_effect']
            provider_prohibited = provider_review['prohibited_inference']
        else:
            provider_existing_evidence = (
                f"{common_evidence};authority-coverage-ledger.tsv;generic-source-authority-boundary.tsv;"
                'selected-object-authority-base.tsv'
            )
            provider_gap = ('CAPABILITY_NECESSITY_AND_CONSUMER_BINDING;CONFLICT_AND_EXCLUSION_REVIEW;UPDATE_AND_ROLLBACK_BOUNDARY' if semantic_review else 'ADAPTATION_CLASSIFICATION;CAPABILITY_NECESSITY_AND_CONSUMER_BINDING;CONFLICT_AND_EXCLUSION_REVIEW;UPDATE_AND_ROLLBACK_BOUNDARY')
            provider_action = ('CAPABILITY_LEVEL_PROVIDER_REVIEW_WITH_TARGETED_PASSIVE_CONSUMER_BINDING_ONLY_WHERE_AMBIGUOUS' if semantic_review else 'CAPABILITY_LEVEL_PROVIDER_REVIEW_AFTER_ADAPTATION_CLASSIFICATION_WITH_TARGETED_PASSIVE_CONSUMER_BINDING_ONLY_WHERE_AMBIGUOUS')
            provider_state = 'CLASSIFIED_OPEN_PROVIDER_AUTHORITY_NOT_ACCEPTED'
            provider_effect = 'NO_PROVIDER_COMPOSITION_TARGET_OR_ACTIVATION_EFFECT'
            provider_prohibited = 'PACKAGE_MEMBER_AND_RECIPE_EVIDENCE_DO_NOT_IMPLY_PROVIDER_AUTHORITY_OR_COMPLETE_RUNTIME_COMPOSITION'

        claims.append({
            'claim_id': f'PCC-{root_slug}-PROVIDER',
            'subject_kind': 'ROOT',
            'subject_id': root['root_review_id'],
            'subject_label': recipe_root,
            'claim_type': 'PROVIDER_AUTHORITY',
            'requested_state': 'PACKAGE_MEMBERS_AUTHORIZED_AS_RUNTIME_PROVIDER_FOR_THEIR_CAPABILITY_SCOPE',
            'adr_class': 'B',
            'supplier_or_reference_boundary': f'AUTHORITATIVE_PACKAGE_MEMBERS_FOR_CAPABILITY_PARTITIONS={partitions}',
            'project_owned_changed_boundary': 'PROJECT_SELECTION_AND_INTEGRATION_OF_REFERENCE_MEMBERS_IN_A_CUSTOM_MIXED_WORLD_APPLICATION_RUNTIME',
            'risk_modifiers': risks,
            'existing_evidence': provider_existing_evidence,
            'remaining_gap': provider_gap,
            'minimum_closure_action': provider_action,
            'explicitly_excluded_evidence': 'SUPPLIER_BUILD_PROVENANCE_AS_A_SUBSTITUTE_FOR_PROVIDER_SELECTION_OR_RUNTIME_BINDING',
            'escalation_trigger': 'AMBIGUOUS_CONSUMER_BINDING;ABI_OR_SECURITY_CONFLICT;MULTIPLE_NON_EQUIVALENT_PROVIDER_CANDIDATES;NO_OBSERVABLE_FALLBACK;ARTIFACT_MEMBER_RECIPE_OR_CONSUMER_BINDING_CHANGE',
            'classification_state': provider_state,
            'authority_effect': provider_effect,
            'prohibited_inference': provider_prohibited,
        })

    claims.append({
        'claim_id': 'PCC-OJ-001-REQUIRED-OBJECT',
        'subject_kind': 'OBJECT_REQUIREMENT',
        'subject_id': 'OJ-001',
        'subject_label': 'libjpeg.so.62',
        'claim_type': 'OBJECT_REQUIREMENT_IDENTITY',
        'requested_state': 'AUTHORITATIVE_REQUIRED_SONAME_AND_EXACT_PROVIDER_CANDIDATE',
        'adr_class': 'A',
        'supplier_or_reference_boundary': 'AUTHORITATIVE_WORKLOAD_OR_REFERENCE_REQUIREMENT',
        'project_owned_changed_boundary': 'PROJECT_INTERPRETATION_OF_THE_REQUIRED_RUNTIME_IDENTITY',
        'risk_modifiers': 'ABI_FAMILY_SUBSTITUTION;GUI_IMAGE_DECODING',
        'existing_evidence': '0157_SUP-01_RESPONSE;0158_SUP-01_RESPONSE_REVIEW;libjpeg.so.8_SUBSTITUTION_REJECTED',
        'remaining_gap': 'NO_EXACT_LIBJPEG_SO_62_PROVIDER_CANDIDATE_BOUND',
        'minimum_closure_action': 'LOCATE_EXACT_CANDIDATE_OR_REVIEW_AUTHORITATIVE_REQUIREMENT_WITHOUT_SUBSTITUTING_LIBJPEG_SO_8',
        'explicitly_excluded_evidence': 'SUP-02_BUILD_ATTESTATION_FOR_THE_WRONG_ABI_FAMILY',
        'escalation_trigger': 'EXACT_CANDIDATE_LOCATED_OR_AUTHORITATIVE_REQUIREMENT_CORRECTED',
        'classification_state': 'REQUIREMENT_CORRECTION_ACCEPTED_PROVIDER_CANDIDATE_OPEN',
        'authority_effect': 'NO_PROVIDER_OR_TARGET_EFFECT',
        'prohibited_inference': 'A_BUILD_RECORD_FOR_LIBJPEG_SO_8_CANNOT_SATISFY_A_LIBJPEG_SO_62_REQUIREMENT',
    })

    claims.extend([
        {
            'claim_id': 'PCC-GLOBAL-BUILD-PROVENANCE',
            'subject_kind': 'GLOBAL',
            'subject_id': 'SUPPLIER_BUILD_PROVENANCE',
            'subject_label': 'producing-build equivalence or independent reproduction',
            'claim_type': 'BUILD_PROVENANCE',
            'requested_state': 'DIGEST_BOUND_PRODUCING_BUILD_OR_INDEPENDENT_REPRODUCTION_CLAIM',
            'adr_class': 'C',
            'supplier_or_reference_boundary': 'EXACT_PRODUCING_ENVIRONMENT_OR_PROJECT_REPRODUCTION_BOUNDARY',
            'project_owned_changed_boundary': 'ONLY_ACTIVE_WHEN_THE_PROJECT_CLAIMS_REPRODUCED_EQUIVALENCE_OR_WHEN_A_REFERENCE_ARTIFACT_REQUIRES_EXPLICIT_ESCALATION',
            'risk_modifiers': 'CLAIM_DEPENDENT',
            'existing_evidence': 'SUP-02_REQUEST_AND_PRODUCER_MECHANISM_EXIST;ZERO_CANONICAL_RESPONSES_ACCEPTED',
            'remaining_gap': 'NO_ACTIVE_CLASS_C_ROOT_CLAIM_SELECTED_BY_THIS_CLASSIFICATION',
            'minimum_closure_action': 'NONE_UNTIL_A_RECORDED_ESCALATION_TRIGGER_OR_CLASS_C_RECLASSIFICATION',
            'explicitly_excluded_evidence': 'BLANKET_CUSTODIAN_EXPORTS_FOR_ALL_REFERENCE_CONSUMED_OR_REFERENCE_ADAPTED_ROOTS',
            'escalation_trigger': 'CLASS_C_RECLASSIFICATION;ARTIFACT_RECIPE_MISMATCH;OPAQUE_HIGH_RISK_GENERATED_OUTPUT;UNRESOLVED_SUPPLIER_CLAIM_REQUIRED_FOR_A_SPECIFIC_PROMOTION',
            'classification_state': 'DEFERRED_NOT_REQUIRED_BY_CURRENT_ACTIVE_CLAIMS',
            'authority_effect': 'NO_BUILD_ATTESTATION_PROVIDER_OR_TARGET_EFFECT',
            'prohibited_inference': 'IMPLEMENTED_PRODUCER_OR_ISSUED_REQUEST_DOES_NOT_CREATE_A_BUILD_ATTESTATION',
        },
        {
            'claim_id': 'PCC-GLOBAL-COMPOSITION',
            'subject_kind': 'GLOBAL',
            'subject_id': 'APPLICATION_RUNTIME_COMPOSITION',
            'subject_label': 'selected Obsidian provider composition',
            'claim_type': 'COMPOSITION',
            'requested_state': 'COMPLETE_NON_CONFLICTING_APPLICATION_RUNTIME_PROVIDER_SET',
            'adr_class': 'D',
            'supplier_or_reference_boundary': 'REFERENCE_COMPONENTS_WITH_PROJECT_AUTHORED_COMPOSITION',
            'project_owned_changed_boundary': 'CAPABILITY_COVERAGE_EXCLUSIONS_ORDERING_ALIAS_POLICY_AND_MIXED_WORLD_COMPOSITION',
            'risk_modifiers': 'BROAD_RUNTIME_BLAST_RADIUS;MULTI_PROVIDER_CONFLICT;WEAK_GLOBAL_OBSERVABILITY',
            'existing_evidence': 'authority-coverage-ledger.tsv;world-lifecycle-authority-boundary.tsv;application-authority-boundary.tsv',
            'remaining_gap': 'EXPLICIT_COMPOSITION_MANIFEST;CONFLICT_AND_EXCLUSION_REVIEW;CAPABILITY_COMPLETENESS;ROLLBACK_BOUNDARY',
            'minimum_closure_action': 'AUTHOR_AND_REVIEW_NON_MATERIALIZING_COMPOSITION_MANIFEST_AFTER_PROVIDER_CLAIMS_ARE_DECIDED',
            'explicitly_excluded_evidence': 'PACKAGE_WIDE_INFERENCE;SUCCESSFUL_HISTORICAL_LAUNCH;SUPPLIER_BUILD_ATTESTATION_AS_COMPOSITION_PROOF',
            'escalation_trigger': 'PROVIDER_CLAIMS_ACCEPTED_FOR_A_BOUNDED_CAPABILITY_SET',
            'classification_state': 'CLASSIFIED_OPEN_NOT_REACHED',
            'authority_effect': 'NO_COMPOSITION_TARGET_OR_ACTIVATION_EFFECT',
            'prohibited_inference': 'INDIVIDUAL_PROVIDER_ACCEPTANCE_DOES_NOT_IMPLY_COMPLETE_COMPOSITION',
        },
        {
            'claim_id': 'PCC-GLOBAL-TARGET',
            'subject_kind': 'GLOBAL',
            'subject_id': 'TARGET_POPULATION',
            'subject_label': 'selected-generation target population',
            'claim_type': 'TARGET_POPULATION',
            'requested_state': 'EXACT_OBJECTS_DATA_ALIASES_AND_PATHS_AUTHORIZED_FOR_TARGET_LAYOUT',
            'adr_class': 'D',
            'supplier_or_reference_boundary': 'ACCEPTED_PROVIDER_AND_COMPOSITION_INPUTS',
            'project_owned_changed_boundary': 'PROJECT_AUTHORED_TARGET_PATH_ALIAS_COLLISION_AND_MATERIALIZATION_POLICY',
            'risk_modifiers': 'FILESYSTEM_COLLISION;ABI_ALIAS_DRIFT;ROLLBACK_AND_REPRODUCIBILITY',
            'existing_evidence': 'TARGET_LAYOUT_SCHEMA_ONLY_PASS;OBJECT_MEMBER_CANDIDATE_EVIDENCE',
            'remaining_gap': 'ACCEPTED_PROVIDER_SET;ACCEPTED_COMPOSITION;DRY_RUN_MANIFEST;COLLISION_AND_ALIAS_VALIDATION',
            'minimum_closure_action': 'GENERATE_AND_REVIEW_A_NON_MUTATING_TARGET_MANIFEST_ONLY_AFTER_COMPOSITION_ACCEPTANCE',
            'explicitly_excluded_evidence': 'DIRECT_EXTRACTION_OR_COPY_BEFORE_TARGET_REVIEW',
            'escalation_trigger': 'BOUNDED_COMPOSITION_ACCEPTED',
            'classification_state': 'CLASSIFIED_OPEN_BLOCKED',
            'authority_effect': 'NO_TARGET_POPULATION_OR_ACTIVATION_EFFECT',
            'prohibited_inference': 'PROVIDER_AUTHORITY_DOES_NOT_IMPLY_TARGET_MEMBERSHIP_OR_PATH_CHOICE',
        },
        {
            'claim_id': 'PCC-GLOBAL-ACTIVATION',
            'subject_kind': 'GLOBAL',
            'subject_id': 'SELECTED_GENERATION_ACTIVATION',
            'subject_label': 'activate successor selected generation',
            'claim_type': 'ACTIVATION',
            'requested_state': 'RUNTIME_SELECTION_ACCEPTANCE_WITH_OBSERVABILITY_AND_ROLLBACK',
            'adr_class': 'D',
            'supplier_or_reference_boundary': 'VERIFIED_MATERIALIZED_TARGET_AND_PROMOTED_LAUNCHER_CONTRACT',
            'project_owned_changed_boundary': 'ACTIVATION_SELECTOR_RUNTIME_ENVIRONMENT_OBSERVABILITY_AND_ROLLBACK',
            'risk_modifiers': 'USER_VISIBLE_RUNTIME_CHANGE;PERSISTENCE;BROAD_APPLICATION_BLAST_RADIUS',
            'existing_evidence': 'IMMUTABLE_GENERATION_AND_PASSIVE_RUNTIME_EVIDENCE;CURRENT_SELECTOR_ABSENT',
            'remaining_gap': 'ACCEPTED_TARGET;BOUNDED_RUNTIME_VALIDATION;ROLLBACK_TEST;OBSERVABILITY_CONTRACT',
            'minimum_closure_action': 'RUN_SEPARATE_ACTIVATION_REVIEW_ONLY_AFTER_TARGET_POPULATION_AND_RUNTIME_VALIDATION',
            'explicitly_excluded_evidence': 'ACTIVATION_BY_DOCUMENT_CLASSIFICATION_OR_SUCCESSFUL_BUILD_ONLY',
            'escalation_trigger': 'VERIFIED_TARGET_POPULATED_AND_BOUNDED_RUNTIME_TEST_READY',
            'classification_state': 'CLASSIFIED_OPEN_BLOCKED',
            'authority_effect': 'NO_ACTIVATION_OR_ACCEPTANCE_EFFECT',
            'prohibited_inference': 'MATERIALIZATION_OR_LAUNCH_SUCCESS_DOES_NOT_AUTOMATICALLY_AUTHORIZE_PERSISTENT_ACTIVATION',
        },
    ])

    requests_by_root = {row['root_review_id']: row for row in requests}
    dispositions: list[dict[str, str]] = []
    for root in sorted(roots, key=lambda row: row['recipe_root']):
        request = requests_by_root.get(root['root_review_id'])
        if request is None:
            raise SystemExit(f'missing SUP-02 request for {root["root_review_id"]}')
        disposition = sup02_disposition(root['review_tier'])
        if disposition == 'NARROWED':
            replacement = 'SEMANTIC_RECIPE_REVIEW_FIRST;RETAIN_ONLY_CLAIM_SPECIFIC_BUILD_OUTPUT_OR_INVOCATION_FIELDS_IF_AN_ESCALATION_TRIGGER_FIRES'
            rationale = 'MATERIAL_DELTA_REQUIRES_CLASS_B_REVIEW_BUT_DOES_NOT_BY_ITSELF_CREATE_A_CLASS_C_REPRODUCTION_CLAIM'
            next_action = 'COMPLETE_CLASS_B_SEMANTIC_AND_OBJECT_IMPACT_REVIEW_BEFORE_DECIDING_ANY_NARROWED_CUSTODIAN_EXPORT'
        elif disposition == 'REPLACED':
            if root['root_review_id'] in semantic_by_root:
                replacement = 'AUTHORITATIVE_ARTIFACT_AND_MEMBER_IDENTITY_PLUS_COMPLETED_CLASS_A_RECIPE_REVIEW_PLUS_SEPARATE_CONCRETE_FILENAME_DRIFT_POLICY'
                rationale = 'PACKAGE_SPECIFIC_RECIPE_BOUNDARY_IS_CLASS_A_WHILE_FILENAME_DRIFT_REMAINS_A_SEPARATE_PROVIDER_INTEGRATION_CLAIM'
                next_action = 'KEEP_SUP-02_HISTORICAL_AND_REVIEW_PROVIDER_AUTHORITY_AND_FILENAME_DRIFT_WITHOUT_CUSTODIAN_BUILD_EXPORT'
            else:
                replacement = 'AUTHORITATIVE_ARTIFACT_AND_MEMBER_IDENTITY_PLUS_RECIPE_UPSTREAM_SEMANTIC_REVIEW_AND_INTEGRATION_EVIDENCE'
                rationale = 'CONFIGURATION_OR_PACKAGING_CLAIM_IS_REFERENCE_CONSUMED_OR_REFERENCE_ADAPTED_NOT_INDEPENDENTLY_REPRODUCED'
                next_action = 'COMPLETE_AGENT_SEMANTIC_REVIEW_AND_DRIFT_POLICY_WITHOUT_EXTERNAL_CUSTODIAN_EXPORT'
        else:
            if root['root_review_id'] in semantic_by_root:
                replacement = 'NO_SUP-02_ACTION;NO_TOKEN_RECIPE_SEMANTIC_REVIEW_COMPLETE;PROCEED_TO_BOUNDED_PROVIDER_REVIEW'
                rationale = 'CLASS_A_PACKAGE_SPECIFIC_RECIPE_BOUNDARY_CONFIRMED_WITHOUT_AN_ACTIVE_CLASS_C_CLAIM'
                next_action = 'KEEP_REQUEST_HISTORICAL_AND_REVIEW_PROVIDER_AUTHORITY_WITHOUT_CUSTODIAN_BUILD_EXPORT'
            else:
                replacement = 'NO_SUP-02_ACTION;RESOLVE_OBJECT_REQUIREMENT_BEFORE_ANY_BUILD_PROVENANCE_ESCALATION'
                rationale = 'THE_REQUIRED_OBJECT_IDENTITY_IS_NOT_YET_SATISFIED_AND_NO_ACTIVE_CLASS_C_CLAIM_EXISTS'
                next_action = 'KEEP_REQUEST_HISTORICAL_AND_DO_NOT_FULFILL_UNLESS_A_NEW_RECORDED_ESCALATION_TRIGGER_APPEARS'
        dispositions.append({
            'request_id': request['request_id'],
            'root_review_id': root['root_review_id'],
            'recipe_root': root['recipe_root'],
            'review_tier': root['review_tier'],
            'primary_claim_class': adaptation_class(root),
            'disposition': disposition,
            'required_now': 'NO',
            'replacement_or_narrowed_scope': replacement,
            'retained_escalation_trigger': 'CLASS_C_RECLASSIFICATION;ARTIFACT_RECIPE_MISMATCH;OPAQUE_HIGH_RISK_GENERATED_OUTPUT;CLAIM_SPECIFIC_SUPPLIER_PROVENANCE_NEEDED_FOR_PROMOTION',
            'rationale': rationale,
            'authority_effect': 'REQUEST_RECLASSIFICATION_ONLY_NO_EVIDENCE_OR_AUTHORITY_EFFECT',
            'next_action': next_action,
        })

    claim_counts = Counter(row['adr_class'] for row in claims)
    claim_type_counts = Counter(row['claim_type'] for row in claims)
    disposition_counts = Counter(row['disposition'] for row in dispositions)
    metadata = [
        ('schema_version', '1'),
        ('classification_policy', 'ADR-0005'),
        ('root_count', str(len(roots))),
        ('object_count', str(len(objects))),
        ('claim_count', str(len(claims))),
        ('artifact_identity_claim_count', str(claim_type_counts['ARTIFACT_IDENTITY'])),
        ('adaptation_claim_count', str(claim_type_counts['ADAPTATION_SEMANTICS'])),
        ('provider_authority_claim_count', str(claim_type_counts['PROVIDER_AUTHORITY'])),
        ('object_requirement_claim_count', str(claim_type_counts['OBJECT_REQUIREMENT_IDENTITY'])),
        ('global_claim_count', str(sum(1 for row in claims if row['subject_kind'] == 'GLOBAL'))),
        ('class_a_claim_count', str(claim_counts['A'])),
        ('class_b_claim_count', str(claim_counts['B'])),
        ('class_c_claim_count', str(claim_counts['C'])),
        ('class_d_claim_count', str(claim_counts['D'])),
        ('sup02_request_count', str(len(dispositions))),
        ('sup02_still_necessary_count', str(disposition_counts['STILL_NECESSARY'])),
        ('sup02_narrowed_count', str(disposition_counts['NARROWED'])),
        ('sup02_replaced_count', str(disposition_counts['REPLACED'])),
        ('sup02_unnecessary_count', str(disposition_counts['UNNECESSARY'])),
        ('no_token_semantic_review_count', str(len(semantic_reviews))),
        ('no_token_confirmed_a_count', str(sum(1 for row in semantic_reviews if row['semantic_result'] == 'CONFIRMED_A'))),
        ('no_token_reclassified_b_count', str(sum(1 for row in semantic_reviews if row['semantic_result'] == 'RECLASSIFIED_B'))),
        ('provider_review_count', str(len(provider_reviews))),
        ('provider_authority_accepted_count', str(sum(1 for row in provider_reviews if row['decision'] == 'ACCEPTED_BOUNDED_PROVIDER'))),
        ('provider_authority_open_count', str(claim_type_counts['PROVIDER_AUTHORITY'] - len(provider_reviews))),
        ('authority_effect', 'FOUR_BOUNDED_PROVIDER_CLAIMS_ACCEPTED_NO_COMPOSITION_TARGET_OR_ACTIVATION_EFFECT'),
        ('next_review_tranche', 'LIBTASN1_REFERENCE_CONSUMED_PROVIDER_ROOT'),
    ]

    write_tsv(out_root / CLAIM_OUTPUT, CLAIM_FIELDS, claims)
    write_tsv(out_root / SUP02_OUTPUT, SUP02_FIELDS, dispositions)
    write_tsv(out_root / METADATA_OUTPUT, ['key', 'value'], [{'key': k, 'value': v} for k, v in metadata])


if __name__ == '__main__':
    main()
