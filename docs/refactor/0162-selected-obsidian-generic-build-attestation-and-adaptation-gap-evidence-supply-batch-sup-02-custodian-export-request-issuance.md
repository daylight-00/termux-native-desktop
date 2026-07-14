# 0162 — Selected Obsidian SUP-02 custodian-export request issuance

## Status

```text
SUPPLY BATCH: SUP-02
REQUIREMENTS: BA-001, BA-002, BA-003
ROOT REQUESTS ISSUED: 28
RECORD CONTRACTS PUBLISHED: 84
REQUESTS ACKNOWLEDGED: 0
RESPONSES RECEIVED: 0
BUILD ATTESTATIONS ACCEPTED: 0
FINAL PROVIDER AUTHORITY: 0
TARGET POPULATION: 0
```

The exact twenty-eight-root request set is now published through the canonical repository request transport. Publication of the remote branch is the issuance event. It is not custodian acknowledgement, response receipt, or evidence acceptance.

Each issued request remains bound to one root review identity and one recipe tree. It requires the same three records from one producing build:

```text
build-invocation-record.json
build-environment-record.json
build-output-manifest.tsv
```

The three records must share the request ID, root review ID, recipe tree, build-run ID, custodian identity, and immutable locator or signed envelope. The output manifest must additionally bind artifacts and package members by SHA-256 and retain ELF SONAME where applicable.

## Canonical issuance surface

```text
experiments/glibc/selected-obsidian-provider-authority/evidence-supply/requests/SUP-02/custodian-export/
    custodian-export-request-issuance.tsv
    custodian-export-record-contract-issuance.tsv
    custodian-export-request-issuance-metadata.tsv
    analysis.status
    claim-boundary.txt
    next-state.txt
```

Every issuance row has:

```text
issuance ID
request ID
root and recipe-tree binding
repository-published request locator
canonical response-drop locator
required record names
one-build completion gate
REQUEST_ISSUED_REPOSITORY_PUBLICATION
NOT_ACKNOWLEDGED
```

## Publication boundary

The transaction receipt binds the issuance surface to the resulting remote commit and tree. The tracked files intentionally do not claim a custodian received or acknowledged the request.

```text
remote branch publication
    = request issued

request issued
    != custodian acknowledgement

custodian acknowledgement
    != response receipt

response receipt
    != build-attestation acceptance
```

No repository, workflow, release, package, or artifact proximity may be substituted for the three required producing-build records.

## Stop line

Do not:

```text
mark a request acknowledged without a custodian receipt;
mark a record supplied because a response directory exists;
infer a build-run identity from an artifact digest;
accept build attestation, provider authority, or target population from issuance alone.
```

## Next state

```text
IMPLEMENT_BOUNDED_GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_EVIDENCE_SUPPLY_BATCH_SUP_02_CUSTODIAN_EXPORT_RESPONSE_ACQUIRER
```
