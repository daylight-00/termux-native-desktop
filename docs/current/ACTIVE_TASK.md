# Active task: review the GdkPixbuf core provider tranche

> Task ID: `review-gdkpixbuf-core-provider-tranche`
>
> Expected state on completion: exact GdkPixbuf, GLib-family and libpng provider candidates are either accepted with bounded capability, conflict, update and rollback decisions or remain explicit blockers. No target population or activation occurs.

## Objective

Close the smallest composition blocker around the already accepted project `libjpeg.so.62` provider: the exact GdkPixbuf runtime, its GLib family, and the selected PNG provider.

## Why now

The non-materializing selected-provider composition review is complete and rejected composition acceptance because 27 selected GTK runtime identities lack accepted providers. Six rows form the smallest coherent image-core tranche:

```text
libgdk_pixbuf-2.0.so.0
libglib-2.0.so.0
libgobject-2.0.so.0
libgio-2.0.so.0
libgmodule-2.0.so.0
libpng16.so.16
```

The exact `libjpeg.so.62.4.0` provider is already accepted and validated through the selected GdkPixbuf file and memory decode paths.

## In scope

- Locate or produce exact Termux-glibc provider candidates for the six image-core identities.
- Bind exact artifact/member digests and ELF SONAMEs.
- Review the pinned `gpkg/glib` and `gpkg/libpng` adaptation boundaries under ADR 0005.
- Establish exact GdkPixbuf source/supply authority rather than selecting Debian oracle bytes.
- Record dependency, conflict, exclusion, update and rollback boundaries.
- Decide bounded provider authority for this tranche.

## Out of scope

- Installing or copying provider bytes.
- Treating the Debian GdkPixbuf object used by the functional oracle as target authority.
- Reviewing the remaining GTK, Cairo, font, accessibility, Xcursor/Xdamage or graphics blockers.
- Generating a target manifest.
- Target population, deployment, selector mutation or activation.

## Required reading

- `docs/current/STATE.yaml`
- `docs/constitution/PRINCIPLES.md`
- `docs/decisions/0005-proportional-assurance-depth.md`
- `docs/evidence/selected-obsidian-provider-composition-review.md`
- `docs/evidence/provider-claim-classification.md`
- `docs/evidence/libjpeg-so-62-loader-isolated-provider-authority.md`
- `experiments/glibc/selected-obsidian-provider-authority/review/selected-provider-composition-gaps.tsv`

## Pending external inputs

None. Existing repository indexes and local Termux package/source caches must be inspected before requesting new evidence.

## Next valid action

Inspect existing exact-candidate, artifact-index and recipe evidence for GdkPixbuf, the four GLib-family members and libpng; then define one bounded acquisition or review runner only for missing coordinates.

## Stop conditions

Stop if the work would require installation, live-prefix mutation, target population or Debian oracle selection; or if a candidate cannot be bound to exact source/artifact/member identity without a new explicit evidence request.

## Completion criteria

- six required identities are each accepted or explicitly blocked;
- exact candidate and SONAME conflicts are visible;
- Debian oracle bytes remain excluded from target authority;
- composition remains separate from provider decisions;
- no runtime or target state changes.
