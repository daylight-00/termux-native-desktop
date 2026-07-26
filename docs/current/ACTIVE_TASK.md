# Active task: close retained supply-result coordinates and generation-root prerequisites

> Task ID: `close-retained-supply-result-coordinate-and-generation-root-prerequisite-gaps`
>
> Expected state on completion: all 41 concrete objects have exact retained result coordinates and verification contracts, and the non-live generation-root, staging, resource, receipt, rollback and failure-observability prerequisites are either bounded or remain explicit blockers. No bytes are acquired or populated.

## Objective

Close the 27 `RETAINED-RESULT-COORDINATE-OPEN` gaps recorded by `TARGET-POPULATION-INTERVENTION-SUPPLY-REVIEW-001`. Separately define the absolute non-live generation-root and preflight contracts needed for a future materializer-design review.

## Why now

The accepted 82-row target policy remains unpopulated. The read-only v107 census found only 14 digest-bound retained-result inputs and 27 missing retained-result coordinates, while seven intervention prerequisites remain blocked or open. These gaps must become explicit immutable metadata and preflight contracts before materializer design can be reviewed.

## In scope

- locate exact retained project result archives by immutable Drive/repository coordinate;
- bind each coordinate to its recorded result SHA and provider authority row;
- define result-index and package/member verification contracts;
- define a non-live immutable generation root without creating it;
- review same-filesystem staging, byte budget, free space, owner/mode feasibility, verification receipts, rollback selector and orphan-staging policy.

## Out of scope

Downloading or extracting provider bytes, creating directories or symlinks, writing a materializer, package installation, target population, immutable-generation creation, selector publication, deployment, loader mutation, service/module/schema/cache generation, display execution or activation.

## Required reading

- `docs/evidence/selected-target-population-intervention-supply-binding-review.md`
- `experiments/glibc/selected-obsidian-provider-authority/review/selected-target-supply-byte-binding-review.tsv`
- `experiments/glibc/selected-obsidian-provider-authority/review/selected-target-population-intervention-review.tsv`
- `docs/evidence/selected-obsidian-target-manifest-boundary-acceptance.md`
- `docs/decisions/0005-proportional-assurance-depth.md`

## Pending external inputs

None are required to perform metadata-only repository and Drive coordinate discovery. Any result archive that cannot be located by an existing immutable coordinate remains an explicit blocker; its absence does not authorize acquisition or reproduction.

## Stop conditions

Stop if any coordinate cannot be bound to an exact digest, if a result archive lacks an independently verified index, if the proposed root overlaps the live glibc prefix or package database, or if validation would require byte acquisition or filesystem mutation.

## Completion criteria

A read-only review records 41 exact result coordinates or retains explicit per-object blockers, and records generation-root/preflight decisions. Only a later separate transaction may decide whether bounded materializer design is authorized.

## Next valid action

Perform metadata-only retained-result coordinate discovery and generation-root contract review. Do not acquire or populate bytes.
