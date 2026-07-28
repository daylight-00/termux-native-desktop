# Selected-provider local-supply-map evidence transaction implementation review

## Decision

```text
review_id=SELECTED-PROVIDER-LOCAL-SUPPLY-MAP-EVIDENCE-TRANSACTION-IMPLEMENTATION-REVIEW-001
decision=QUALIFIED_NON_EXECUTING_SYNTHETIC_READ_ONLY_LOCAL_SUPPLY_MAP_EVIDENCE_TRANSACTION_IMPLEMENTATION_CANDIDATE
acceptance_gate=SELECTED-PROVIDER-LOCAL-SUPPLY-MAP-EVIDENCE-TRANSACTION-IMPLEMENTATION-ACCEPTANCE-OPEN
```

The accepted read-only evidence-transaction design now has a deterministic repository-owned implementation candidate. This is synthetic implementation evidence only. It does not authorize a provider path open, provider byte read, local-supply-map receipt, replay write or runtime mutation.

## Frozen candidate artifacts

| Artifact | SHA-256 |
|---|---|
| `experiments/glibc/selected-obsidian-provider-authority/implementation/selected_provider_local_supply_map_evidence_transaction_candidate.py` | `8c3e0cb0866e7d40807126a65130b1fd654db50241af1758a1397735fd513b42` |
| `experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-map-evidence-transaction-implementation-synthetic-fixture.json` | `b19929b19de45d9c6147060f9025dbbff13ce662cc7eeeff7bec3f178aeef020` |
| `experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-map-evidence-transaction-implementation-negative-cases.json` | `b2a8047076502b30fca2b659b16b9ce4d741523a72175a828d5774aa105a7c82` |
| `experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-map-evidence-transaction-implementation-coverage.tsv` | `8fe3cf19c7cace1f9e7087b51551caa7a86c75c5300d3f586da32a003b0ae785` |
| `experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-map-evidence-transaction-implementation-synthetic-success.json` | `1aa5d18db7f0ca871bb7a1925ef96d35c82a15d8b445c2cd648de61e7ff26efb` |
| `experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-local-supply-map-evidence-transaction-implementation-metadata.tsv` | `ed33fe8025ba8db12465425fc231b4c568d215c34bad2e040eaec266f53a56c9` |

## Accepted-design coverage

```text
input contracts:              12
state-machine states:         16
ordered operations:           32
failure contracts:            18
total coverage rows:          78
inherited validation rules:   24
```

Every accepted input, state, operation and failure ID appears exactly once in the coverage ledger. The implementation also preserves the inherited 41-row local-supply contract and its 24 validation rules.

## Synthetic-only execution boundary

The CLI accepts only the exact repository fixture marked `SYNTHETIC_REPOSITORY_FIXTURE_ONLY`. Its 41 coordinate rows contain ten fields each and use only paths under:

```text
/__synthetic__/termux-native-desktop/selected-provider/
```

The operations that would perform component `lstat`, no-follow open, ownership/mode checks, streaming SHA-256, stability checks and ELF/SONAME parsing are modeled as ordered state transitions only. The candidate does not call those operating-system surfaces.

## Synthetic verification

```text
success cases:                 1
negative cases:               18
synthetic coordinate rows:    41
provider paths opened:         0
provider descriptors opened:   0
provider bytes read:            0
writes:                         0
persistent replay writes:       0
live authority:                 0
```

The positive fixture covers all 32 operations and all non-rejected states. The eighteen negative cases map one-to-one to `LSME-FAIL-001` through `LSME-FAIL-018` and remain fail-closed with zero provider reads, writes and live authority.

## Candidate output

The synthetic success result is:

```text
QUALIFIED_SYNTHETIC_READ_ONLY_LOCAL_SUPPLY_MAP_EVIDENCE_TRANSACTION_IMPLEMENTATION_CANDIDATE
```

It remains `SYNTHETIC_ONLY_NOT_AUTHORITY`. No live local-supply map is produced or accepted.

## Authority boundary

```text
OWNER_AUTHORIZATION_ISSUANCE_STATE=NOT_AUTHORIZED
COORDINATE_RECEIPT_PRODUCTION_STATE=NOT_AUTHORIZED
EXECUTION_AUTHORIZATION_STATE=NOT_ISSUED_NOT_AUTHORIZED
LOCAL_PATH_DISCOVERY_STATE=NOT_AUTHORIZED
PROVIDER_OPEN_STATE=NOT_AUTHORIZED
PROVIDER_BYTE_READ_STATE=NOT_AUTHORIZED
EVIDENCE_TRANSACTION_EXECUTION_STATE=NOT_AUTHORIZED
LOCAL_SUPPLY_MAP_STATE=NOT_PRODUCED_NOT_AUTHORIZED
GENERATION_ROOT_STATE=NOT_CREATED_NOT_AUTHORIZED
TARGET_POPULATION_STATE=NOT_AUTHORIZED_UNPOPULATED_SCHEMA_ONLY
MATERIALIZATION_STATE=NOT_AUTHORIZED
PUBLICATION_STATE=NOT_AUTHORIZED
DEPLOYMENT_STATE=NOT_AUTHORIZED
ACTIVATION_STATE=NOT_AUTHORIZED
```

## Next action

Review and accept the exact six-artifact implementation candidate boundary. Acceptance must freeze the candidate without granting provider-read, evidence-execution, local-map or runtime authority.
