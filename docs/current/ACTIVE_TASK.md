# Active task: review exact libXcursor provider authority

> Task ID: `review-libxcursor-bounded-provider-authority`
>
> Expected state on completion: exact `libXcursor.so.1.0.2` is either accepted for the selected GTK X11 cursor capability or left open with a precise Class B adaptation or consumer-binding blocker. No target population, deployment or activation occurs.

## Objective

Review the single-member `gpkg/libxcursor` root under ADR 0005 using its exact artifact/member identity, pinned recipe tree, patch semantics, selected GTK necessity, dependency binding, conflict/exclusion, update and rollback boundaries.

## Why now

The exact GDK Pixbuf dependency chain through official `libmount` and `libblkid` is now bounded and accepted, reducing the composition gap count from 21 to 20. `libXcursor` is the smallest remaining reviewed-root, single-member GTK gap and therefore the next proportional tranche.

## Known coordinates

```text
root review:    generic-root-review:54ab99c9280e70c43600
recipe root:    gpkg/libxcursor
recipe tree:    bb2495e04b246f60203d48720225ef13fa8a25bf
artifact:       libxcursor-glibc 1.2.3
artifact SHA:   7901dd136016df9d694e38bb17923812f539241475e7ac97935c8dcdfcceb902
member:         libXcursor.so.1.0.2
member SHA:     86e70b94186edb4c16cf00f2bcea4a03ea09bb486ee6a079dd11d3ef6fffe722
SONAME:         libXcursor.so.1
selected row:   selected:e57423d1cb58b1b78ba4
```

## In scope

- exact member and SONAME identity;
- Class B patch and Termux-prefix semantics;
- selected GTK cursor necessity and bounded consumer binding;
- dependency, collision and exclusion review;
- update and rollback boundary.

## Out of scope

- other Xcursor package surfaces;
- complete composition acceptance;
- target generation, installation, materialization, deployment or activation;
- SUP-02 evidence collection.

## Required reading

- `docs/current/STATE.yaml`
- `docs/decisions/0005-proportional-assurance-depth.md`
- `docs/evidence/gdkpixbuf-exact-util-linux-provider-authority.md`
- `docs/evidence/selected-obsidian-provider-composition-review.md`
- `experiments/glibc/selected-obsidian-provider-authority/review/generic-build-attestation-adaptation-root-review-set.tsv`
- `experiments/glibc/selected-obsidian-provider-authority/review/generic-artifact-member-inventory-receipt-review.tsv`

## Pending external inputs

None before static review. Request one bounded Termux probe only if exact consumer binding or conflict cannot be resolved from retained evidence.

## Next valid action

Perform a bounded exact-file recipe and provider review. Request device execution only if static evidence cannot resolve consumer binding or conflict.

## Stop conditions

Stop without accepting authority if exact identity, patch semantics, dependency binding, selected necessity, collision/exclusion, update or rollback boundaries cannot be bounded.

## Completion criteria

- Exact artifact, member, SONAME and recipe coordinates remain pinned.
- Class B patch semantics are bounded to the accepted member.
- Necessity, consumer binding, conflict/exclusion, update and rollback are explicit.
- The provider is accepted narrowly or left open with one precise blocker.
- Composition, target population and activation remain separate.
