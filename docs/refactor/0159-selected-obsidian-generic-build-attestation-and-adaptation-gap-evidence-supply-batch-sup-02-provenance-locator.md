# 0159 — Selected Obsidian SUP-02 producing-build provenance locator

## Status

```text
SUPPLY BATCH: SUP-02
REQUIREMENTS: BA-001, BA-002, BA-003
TRANSACTION: BOUNDED PROVENANCE LOCATOR
ROOT DENOMINATOR: 28
EVIDENCE ACCEPTANCE: 0
FINAL PROVIDER AUTHORITY: 0
TARGET POPULATION: 0
```

This transaction does not synthesize producing-build provenance from repository proximity, package versions, workflow names, or already-observed package members. It implements a bounded locator that searches explicit custodian-export roots for the three exact records required from one producing build:

```text
build-invocation-record.json
build-environment-record.json
build-output-manifest.tsv
```

The locator records complete, partial, or absent exports for every pinned root. GitHub repository, workflow, and release metadata may be captured through the operator's local `gh` environment, but those surfaces are locator metadata only and are not accepted as build provenance.

## Local interaction boundary

The wrapper uses the operator environment for `git fetch`, `git ls-remote`, `git push`, and bounded `gh api` reads. The GitHub connector remains suitable for lightweight verification, but is not the transport for cloning, committing, pushing, or bulk evidence acquisition.

## Stop line

Do not infer a build invocation from a recipe commit, infer an immutable environment from a workflow definition, treat a package member inventory as a producing-build output manifest, or derive a build-run identity from an artifact digest. No build attestation, adaptation, provider, target, materialization, activation, launcher, loader, or RPATH effect is permitted.

## Next state

```text
REVIEW_BOUNDED_GENERIC_BUILD_ATTESTATION_ADAPTATION_GAP_EVIDENCE_SUPPLY_BATCH_SUP_02_PROVENANCE_LOCATOR_RECEIPT
```
