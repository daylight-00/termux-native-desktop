# Active task: close three missing coordinates, upgrade legacy result indexes and census member sizes

> Task ID: `close-three-missing-result-coordinates-upgrade-legacy-indexes-and-census-member-sizes`
>
> Expected state on completion: Fontconfig, HarfBuzz and libxkbcommon have immutable retained-result coordinates; all twenty-four legacy authority archives have a digest-index upgrade or explicit replacement receipt; and all 41 concrete members have exact byte sizes. No provider bytes are acquired or populated.

## Objective

Close the remaining verification blockers after `RETAINED-SUPPLY-COORDINATE-GENERATION-CONTRACT-001`. Preserve the seven accepted generation contracts while upgrading supply evidence only.

## Why now

Twenty-four formerly blocked objects now have exact Drive file IDs and outer SHA-256 values, but their legacy transaction archives lack `result-index.sha256`. Three provider families still lack a retained result coordinate. The generation-root, publication, receipt, rollback and cleanup contracts are now bounded, but exact object-size input is still missing.

## In scope

- locate immutable Fontconfig, HarfBuzz and libxkbcommon result coordinates;
- define a non-mutating index-upgrade receipt for each legacy archive or bind a newer indexed replacement result;
- record exact size for all 41 concrete members from trusted artifact/member evidence;
- recompute the resource preflight budget without creating the generation root.

## Out of scope

Provider-byte download or extraction, directory or symlink creation, materializer implementation, package installation, target population, selector publication, deployment, loader mutation, service/module/schema/cache generation, display execution or activation.

## Required reading

- `docs/evidence/selected-target-retained-result-coordinate-generation-contract-review.md`
- `experiments/glibc/selected-obsidian-provider-authority/review/selected-target-retained-result-coordinate-review.tsv`
- `experiments/glibc/selected-obsidian-provider-authority/review/selected-target-generation-root-contract-review.tsv`
- `docs/evidence/selected-target-population-intervention-supply-binding-review.md`

## Pending external inputs

None for bounded coordinate search and metadata review. A missing immutable result remains a blocker and never creates acquisition or reproduction authority.

## Stop conditions

Stop if an archive digest cannot be verified, if an index upgrade would rewrite historical evidence, if size evidence is not bound to the exact member digest, or if any step would create or modify target/runtime state.

## Completion criteria

A separate read-only review records three coordinates or explicit terminal blockers, twenty-four append-only index-upgrade receipts or indexed replacements, and exact 41-member sizes. Population and materializer design remain separate decisions.

## Next valid action

Perform metadata-only coordinate, index-upgrade and size census work. Do not acquire or populate provider bytes.
