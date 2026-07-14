# 0154 — Selected Obsidian generic build-attestation and adaptation gap-evidence acquirer

## Status

```text
ACQUIRER: IMPLEMENTED / BOUNDED / INPUT-ONLY
SOURCE CONTRACTS: 10
CLOSURE LANES: 6
EVIDENCE REQUIREMENTS: 16
PINNED ROOT ACQUISITION UNITS: 28
NAMED OBJECT ACQUISITION UNITS: 37
NETWORK DISCOVERY: FORBIDDEN
UNMANIFESTED INPUT: REJECTED
STRICT 0151 EVIDENCE ROOT: EMITTED
EVIDENCE ACCEPTANCE: 0
BUILD ATTESTATIONS ACCEPTED: 0
TERMUX/ANDROID ADAPTATIONS ACCEPTED: 0
CONCRETE FILENAME DRIFTS ACCEPTED: 0
OBJECT CORRECTIONS ACCEPTED: 0
FINAL PROVIDER AUTHORITY: 0 ACCEPTED
TARGET POPULATION: BLOCKED
```

This transaction implements the bounded acquirer required by `0153`.

The acquirer does not search for evidence and does not create semantic or policy claims. It accepts only explicitly staged, integrity-bound acquisition inputs whose requirement, lane, source contract, scope, acquisition unit, acquisition mode and locator class match the canonical acquisition set.

A successful acquisition creates candidate review input only. It cannot satisfy a requirement or change provider authority.

## Canonical implementation

```text
experiments/glibc/selected-obsidian-provider-authority/recipe/
    acquire-generic-build-attestation-and-adaptation-gap-evidence.py
    run-generic-build-attestation-and-adaptation-gap-evidence-acquirer.sh

tests/repository/
    generic-build-attestation-adaptation-gap-evidence-acquirer-smoke.sh
```

Canonical inputs:

```text
review/generic-build-attestation-adaptation-gap-evidence-source-contracts.tsv
review/generic-build-attestation-adaptation-gap-evidence-acquisition-lanes.tsv
review/generic-build-attestation-adaptation-gap-evidence-acquisition-requirements.tsv
review/generic-build-attestation-adaptation-root-gap-evidence-acquisition-set.tsv
review/generic-build-attestation-adaptation-object-gap-evidence-acquisition-set.tsv
```

## Acquisition input root

Default location:

```text
$HOME/.cache/hw-t-evidence/termux-native-desktop/
    generic-build-attestation-adaptation-gap-acquisition-input/
```

The root is optional. If it is absent, the acquirer succeeds and emits an empty strict evidence manifest plus explicit unavailable-input states.

If the root exists, it must contain a regular file:

```text
acquisition-input-manifest.tsv
```

The exact manifest contract is:

```text
input_id
acquisition_unit_id
requirement_id
lane_id
scope_kind
scope_id
source_kind
acquisition_mode
locator_class
source_locator
relative_path
sha256
size_bytes
evidence_class
claim_boundary
```

Every payload file under the input root must occur exactly once in the manifest. Unmanifested files, missing files, duplicate paths, symlinks, special files, absolute paths and parent traversal are rejected.

## Canonical validation

For each input row the acquirer verifies:

```text
input ID syntax and uniqueness;
exact requirement and closure lane identity;
source kind permitted by the requirement;
source kind permitted by the source contract;
ROOT or OBJECT scope required by the requirement;
exact acquisition-unit membership;
exact manifest scope identity;
source-contract acquisition mode;
source-contract locator class;
non-empty bounded source locator;
SHA-256 and byte-size binding;
fixed claim boundary;
regular non-symlink payload;
complete manifest-to-filesystem equality.
```

The acquirer does not reinterpret a source class. A file with a valid digest is rejected if its acquisition mode, locator class, requirement, scope or acquisition unit does not match the canonical contract.

## Bounded resource limits

```text
maximum manifest rows:       256
maximum single input file:    64 MiB
maximum total input bytes:   512 MiB
```

These are collector-safety bounds, not evidence sufficiency criteria.

## Output evidence root

The acquirer emits:

```text
evidence-root/
    evidence-manifest.tsv
    files/
        <deterministic digest-bound candidate files>
```

The evidence manifest is exactly compatible with the `0151` strict collector:

```text
evidence_id
requirement_id
lane_id
scope_kind
scope_id
evidence_class
source_kind
source_locator
relative_path
sha256
size_bytes
claim_boundary
```

The fixed claim boundary is:

```text
CANDIDATE_EVIDENCE_REVIEW_REQUIRED_NO_AUTHORITY_EFFECT
```

Copied candidate files are rehashed after copying and made read-only inside the receipt output. The output path is derived from the input ID and content digest rather than from an authority or provider decision.

## Acquisition receipt

```text
analysis.status
claim-boundary.txt
next-state.txt
summary.tsv
input-verification.tsv
acquisition-file-inventory.tsv
requirement-acquisition-status.tsv
lane-acquisition-status.tsv
root-acquisition-status.tsv
object-acquisition-status.tsv
unavailable-acquisition-inputs.tsv
evidence-root/evidence-manifest.tsv
```

### Requirement states

A direct-gap requirement with no staged input remains:

```text
ACQUISITION_INPUT_UNAVAILABLE_EXPLICIT_GAP
```

A local-foundation completion requirement with no staged input remains:

```text
LOCAL_FOUNDATION_ONLY_NO_NEW_ACQUISITION
```

A verified direct-gap candidate becomes:

```text
CANDIDATE_EVIDENCE_ACQUIRED_REVIEW_REQUIRED
```

A verified candidate supplementing a local foundation becomes:

```text
LOCAL_FOUNDATION_AND_CANDIDATE_EVIDENCE_ACQUIRED_REVIEW_REQUIRED
```

All states retain:

```text
closure_state:   OPEN_SEPARATE_REVIEW_REQUIRED
authority_state: OPEN_NO_ACCEPTANCE
```

### Root and object states

Each root and object row reports only candidates assigned to its exact acquisition-unit ID. Package-wide or family-wide propagation is not performed.

Every object row remains:

```text
final_provider_state:    UNRESOLVED
authority_state:         OPEN_NO_ACCEPTANCE
target_population_state: UNPOPULATED
```

## Absent-input production behavior

With no acquisition input root, the deterministic receipt is:

```text
candidate evidence files acquired: 0
candidate requirements:             0
local-foundation-only requirements: 6
direct-gap unavailable requirements: 10
root units with candidates:          0
object units with candidates:        0
```

Absence is not failure and is not closure. It records that the acquisition mechanism is ready but no qualified evidence was supplied.

## Execution boundary

The acquirer may only:

```text
read canonical repository acquisition contracts;
read an explicitly staged local acquisition input root;
verify regular files, identities, digests and sizes;
copy verified candidates into a bounded receipt-local evidence root;
emit strict-manifest-compatible candidate records.
```

It performs no:

```text
network acquisition or discovery;
latest-version selection;
package installation, removal, upgrade or downgrade;
maintainer-script execution;
artifact build or independent reproduction;
payload extraction into runtime paths;
target runtime execution;
semantic-review fabrication;
continuity-policy fabrication;
provider or object-correction promotion;
target population;
materialization or activation;
launcher, loader, current or RPATH mutation.
```

Independent reproduction remains a separately authorized input-producing operation. This acquirer may import its bounded receipt but cannot perform the reproduction itself.

## Rejection gates

The smoke suite confirms rejection of:

```text
digest or size mismatch;
unmanifested payload files;
source-contract acquisition-mode substitution;
unsafe paths and filesystem members;
requirement, lane, scope or acquisition-unit mismatch;
authority, provider or target-state promotion in canonical inputs.
```

It also confirms that the emitted evidence root is accepted structurally by the existing `0151` collector while retaining zero authority effect.

## Accepted by this transaction

```text
bounded acquisition input-manifest contract;
strict source-contract and acquisition-unit validation;
manifest/filesystem equality validation;
deterministic candidate copying and post-copy integrity verification;
0151-compatible evidence-root generation;
explicit no-input and unavailable-input states;
requirement, lane, root and object acquisition receipts;
read-only and no-authority execution boundary.
```

Not accepted:

```text
any candidate evidence as sufficient;
object requirement correction;
producing-build provenance;
independent reproduction;
output-to-build linkage;
Termux/Android adaptation necessity;
filename-drift policy;
consumer binding;
successor or rollback continuity;
final provider authority;
target population.
```

## Next state

```text
RUN_BOUNDED_GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_EVIDENCE_ACQUIRER
```

The production receipt must then be reviewed separately:

```text
REVIEW_BOUNDED_GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_EVIDENCE_ACQUISITION_RECEIPT
```
