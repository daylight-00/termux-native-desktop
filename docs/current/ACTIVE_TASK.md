# Active task: review the selected Obsidian provider composition

> Task ID: `review-selected-obsidian-provider-composition`
>
> Expected state on completion: one non-materializing composition manifest identifies the exact accepted provider objects required by the bounded Obsidian/GdkPixbuf/GTK scope, records exclusions and unresolved dependencies, and decides whether target-manifest generation may begin. No target population or activation occurs.

## Objective

Move from individually accepted provider rows to an explicit composition decision without inferring completeness from package presence or successful isolated tests.

## Why now

The project-produced `libjpeg.so.62.4.0` candidate now has bounded provider authority for the exact GdkPixbuf 2.42.12 JPEG file and memory decode capability. Together with the seven previously accepted no-token providers, eight provider claims are accepted. Composition remains a separate Class D claim.

## Known facts

- Exact provider candidate: `libjpeg.so.62.4.0`, SHA-256 `a537840e…`, `DT_SONAME=libjpeg.so.62`.
- The candidate has no `DT_RPATH` or `DT_RUNPATH`.
- The exact GdkPixbuf consumer requires `libjpeg.so.62`; all 22 unresolved JPEG symbols are supplied.
- Candidate and Debian oracle direct `djpeg` controls produced the same output digest.
- Candidate and oracle both passed GdkPixbuf file and memory decode through the direct Termux-glibc loader and ELF-only core shim.
- Provider authority is accepted only for the bounded GdkPixbuf JPEG capability.
- Eight bounded provider claims are accepted; complete runtime composition is not.

## In scope

- Enumerate exact accepted provider members and SONAME aliases required by the selected Obsidian/GdkPixbuf/GTK capability scope.
- Bind each member to its provider-authority decision and exact digest.
- Record ordering, collision, exclusion and dependency-provider gaps.
- Define update and rollback boundaries for the composition as a unit.
- Produce a non-materializing composition manifest and deterministic checker.
- Decide whether a dry-run target manifest is the next valid action.

## Out of scope

- Installing or copying provider bytes.
- Creating target directories or aliases.
- Selecting Debian oracle bytes as target authority.
- Treating accepted providers as a complete composition without a manifest.
- Target population, deployment, selector mutation or activation.

## Required reading

- `docs/current/STATE.yaml`
- `docs/constitution/PRINCIPLES.md`
- `docs/decisions/0005-proportional-assurance-depth.md`
- `docs/evidence/provider-claim-classification.md`
- `docs/evidence/libjpeg-so-62-loader-isolated-provider-authority.md`
- `docs/evidence/xorg-reference-consumed-provider-authority.md`
- `docs/evidence/libepoxy-reference-consumed-provider-authority.md`
- `docs/evidence/pango-reference-consumed-provider-authority-and-filename-continuity.md`

## Pending external inputs

None.

## Next valid action

Author and review a non-materializing selected-provider composition manifest from the eight accepted bounded provider decisions and the exact selected consumer requirements.

## Stop conditions

Stop if an exact provider digest, SONAME, accepted capability, consumer binding, conflict set or dependency requirement cannot be traced to a current provider decision; or if the review would require materialization, installation, target mutation or activation.

## Completion criteria

- every included member is linked to an accepted provider decision;
- all required aliases are explicit and ABI-correct;
- oracle, static, development and incompatible-family exclusions are explicit;
- unresolved dependency-provider claims remain visible rather than inferred closed;
- composition authority is decided separately from target population;
- no live runtime state changes.
