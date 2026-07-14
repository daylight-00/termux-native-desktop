# 0160 — Selected Obsidian SUP-02 producing-build provenance locator receipt review

## Status

```text
SUPPLY BATCH: SUP-02
REQUIREMENTS: BA-001, BA-002, BA-003
PRODUCTION LOCATOR RECEIPT: REVIEWED / PASS / BOUNDED
ROOTS REVIEWED: 28
COMPLETE CUSTODIAN EXPORTS: 0
PARTIAL CUSTODIAN EXPORTS: 0
ABSENT CUSTODIAN EXPORTS: 28
RECORD FILES LOCATED: 0
BUILD ATTESTATIONS ACCEPTED: 0
FINAL PROVIDER AUTHORITY: 0 ACCEPTED
TARGET POPULATION: 0
```

The exact production locator receipt is bound to source HEAD `8bcbf79d1e79b6fdcbe4c4440ccee144372853e7`, source tree `297775f099d7b8b21a3b2e356e8f999360acee2d`, and result archive SHA-256 `91698e4737ab101e4798cfc555c31f0eaa9d885c07c606111a1227e61a1db6bc`.

## Receipt decision

All twenty-eight pinned roots were searched through the bounded custodian-export locator. No root contained any of the three required records:

```text
build-invocation-record.json
build-environment-record.json
build-output-manifest.tsv
```

The header-only local record inventory therefore proves only that no explicit existing export was found at the searched surface. It is not proof that a producing build never existed, and it does not close `BA-001`, `BA-002`, or `BA-003`.

GitHub repository metadata, two workflow definitions, and four release records were captured. They remain locator metadata only:

```text
repository commit or recipe proximity
    != producing-build invocation

workflow definition
    != immutable producing-build environment

release or package presence
    != digest-bound output manifest from one producing build

artifact digest
    != build-run identity
```

## Accepted effect

```text
BA-001:
    OPEN_CUSTODIAN_INVOCATION_EXPORT_REQUIRED

BA-002:
    OPEN_CUSTODIAN_ENVIRONMENT_EXPORT_REQUIRED

BA-003:
    OPEN_CUSTODIAN_OUTPUT_MANIFEST_REQUIRED

build attestation acceptance:
    0

final provider authority:
    OPEN

target population:
    BLOCKED
```

The next transaction must define an exact custodian-export request set. Re-running the same empty locator without a new export surface is rejected as non-progress.

## Required next request boundary

For each of the twenty-eight pinned roots, the request set must require records from one producing build and bind at least:

```text
root review identity
recipe tree
build-run identity
artifact SHA-256
invocation command and inputs
immutable toolchain, dependency and relevant environment description
package/member output path and member SHA-256
custodian identity
immutable locator or signed envelope
```

The request definition itself accepts no evidence or authority. It must not ask the project agent to synthesize missing provenance from repository state, workflow YAML, package indexes, observed members, versions, or timestamps.

## Next state

```text
DEFINE_BOUNDED_GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_EVIDENCE_SUPPLY_BATCH_SUP_02_CUSTODIAN_EXPORT_REQUEST_SET
```
