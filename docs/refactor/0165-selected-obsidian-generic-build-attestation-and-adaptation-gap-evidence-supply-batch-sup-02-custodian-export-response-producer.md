# 0165 — Selected Obsidian SUP-02 custodian-export response producer

## Status

```text
SUPPLY BATCH: SUP-02
REQUIREMENTS: BA-001, BA-002, BA-003
CUSTODIAN-SIDE RESPONSE PRODUCER: IMPLEMENTED / BOUNDED
ISSUED REQUESTS: 28
RECORD CONTRACTS: 84
CANONICAL REQUESTS EXECUTED BY THIS TRANSACTION: 0
RESPONSES PRODUCED: 0
RESPONSES ACQUIRED: 0
BUILD ATTESTATIONS ACCEPTED: 0
FINAL PROVIDER AUTHORITY: 0
TARGET POPULATION: 0
```

The reviewed 0164 receipt established that repeating an empty response acquisition is non-progress. This transaction therefore implements the missing producing-build-side mechanism. It does not invent or infer a response from repository metadata, release metadata, package presence or historical workflow configuration.

## Producer boundary

Canonical implementation:

```text
experiments/glibc/selected-obsidian-provider-authority/recipe/
    produce-generic-build-attestation-and-adaptation-gap-evidence-supply-batch-sup-02-custodian-export-response.py
```

The producer runs the actual build command in the producing environment and emits one response only when all of the following remain exact:

```text
issued request ID;
root review ID;
recipe root and Git tree;
producing build-run ID;
named custodian identity;
immutable locator or signed envelope;
actual invocation argv and timestamps;
recipe and build-input digests;
host, toolchain and system-package environment snapshot;
container or VM image digest;
output package artifact digest;
package member digest and ELF SONAME where present.
```

A mismatched recipe tree, dirty tracked source repository, missing input source, failed build, absent package artifact, malformed package metadata, unsafe archive path, unsupported archive member, secret-like environment capture request, or incomplete record contract fails closed.

## Output layout

For one request, the producer creates:

```text
<out>/response-root/<request-id>/
    build-invocation-record.json
    build-environment-record.json
    build-output-manifest.tsv
    custodian-export-response-manifest.tsv

<out>/producer-audit/<request-id>/
    build-command.log
    build-command.rc
    recipe-file-manifest.tsv
    input-source-manifest.tsv
    system-package-snapshot-*.tsv
    producer-status.json
```

Only `response-root/` is input to the 0163 acquirer. Audit material remains outside the strict response file set.

Regular archive members are hashed over their bytes. Symbolic-link and hard-link rows use domain-separated SHA-256 over `SYMLINK\0<target>` and `HARDLINK\0<target>` respectively. This preserves exact link identity without extracting the package. Directories are omitted; special members are rejected.

## Required invocation model

The custodian supplies one exact request, the producing source checkout, bounded source and artifact globs, a stable build-run identity, a custodian identity, an immutable locator or signed envelope, the actual container or VM image digest, and the exact build command.

Illustrative shape:

```text
python3 produce-...custodian-export-response.py \
  --request-issuance <custodian-export-request-issuance.tsv> \
  --record-contract-issuance <custodian-export-record-contract-issuance.tsv> \
  --request-id <SUP02-CER-...> \
  --source-repository <exact-glibc-packages-checkout> \
  --input-source-glob '<bounded build input glob>' \
  --artifact-glob '<bounded package artifact glob>' \
  --build-run-id <stable producing-run ID> \
  --custodian-identity <named identity> \
  --immutable-locator-or-signed-envelope <immutable locator> \
  --container-or-vm-image-digest <exact digest> \
  --source-date-epoch <decimal seconds> \
  --out <new output directory> \
  -- <actual build command and argv>
```

The producer captures only an explicit environment allowlist and rejects secret-like variable names. It never serializes the complete process environment.

## Validation result

The repository smoke test creates a 28-request/84-contract fixture, executes an instrumented package build, emits one complete candidate response, and passes that response through the existing 0163 acquirer:

```text
complete candidate responses acquired: 1
requests without response:             27
verified response records:              3
build attestations accepted:            0
```

Negative checks reject recipe-tree drift and secret-like environment capture.

## Claim boundary

```text
producer implementation
    != canonical request execution

candidate response emission
    != response acquisition

response acquisition
    != receipt-review acceptance

receipt-review acceptance
    != build-attestation acceptance

build-attestation acceptance
    != provider authority or target population
```

No canonical SUP-02 response exists merely because this producer is implemented.

## Next state

```text
RUN_BOUNDED_GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_EVIDENCE_SUPPLY_BATCH_SUP_02_CUSTODIAN_EXPORT_RESPONSE_PRODUCER_FOR_EXACT_REQUEST
```

The first meaningful execution should use one exact issued request and an environment that genuinely owns the resulting build record. Its `response-root/` must then pass the 0163 acquirer and a separate receipt review before any build-attestation claim is considered.

## Stop line

Do not:

```text
construct records from GitHub metadata alone;
substitute a workflow definition for an executed build;
reuse an artifact without its producing invocation and environment;
record a guessed container image digest or build-run identity;
capture secrets in the environment record;
mark a request acknowledged merely because the producer was run;
accept build attestation, provider authority or target population;
advance to SUP-03 before SUP-02 response review establishes the required boundary.
```
