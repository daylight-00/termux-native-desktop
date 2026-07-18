# Active task: review exact Cairo and Cairo-GObject provider authority and filename continuity

> Task ID: `review-cairo-bounded-provider-authority`
>
> Expected state on completion: the exact Termux candidates `libcairo.so.2.11802.2` and `libcairo-gobject.so.2.11802.2` are either accepted as one bounded root tranche for selected Pango/GTK rendering and GObject integration while preserving SONAMEs `libcairo.so.2` and `libcairo-gobject.so.2`, or left open with a precise configure, patch, prefix, dependency, concrete-filename drift, consumer-binding, conflict, update, or rollback blocker. No target population, deployment, or activation occurs.

## Objective

Review the two selected members from `gpkg/libcairo` under ADR 0005 as one atomic recipe-root tranche, explicitly reconciling both selected concrete labels with the retained exact Termux candidates and bounding all recipe adaptation tokens.

## Why now

Exact Fontconfig authority is bounded and accepted. The read-only Cairo/Pixman acquisition probe then established exact `libcairo.so.2.11802.2 -> libpixman-1.so.0` binding and exact Pixman `libpixman-1.so.0.46.4` authority, reducing selected composition gaps from 11 to 10. Cairo remains the coupled reviewed root in the selected GTK gap set and covers two identities from one exact artifact and recipe tree.

## Known coordinates

```text
root review:             generic-root-review:0263d4b55d6a43edad7b
recipe root:             gpkg/libcairo
recipe tree:             b80a0990d43609e09f1480394225d2b068ce5881
artifact:                libcairo-glibc 1.18.2
artifact SHA:            3250dba4dc3312b4fcaa763c788614c63ba611ee82451224ba10da50622a0db2
selected cairo identity: libcairo.so.2.11804.4
selected cairo row:      selected:553839925ebeb658612d
exact cairo candidate:   libcairo.so.2.11802.2
cairo candidate SHA:     43cd64f07e1c33e5bd574fe7f50a20062a2ab6836adf80e1b5f4b6846e05264d
cairo SONAME:            libcairo.so.2
selected gobject identity: libcairo-gobject.so.2.11804.4
selected gobject row:      selected:e8ccf42491e69aba6284
exact gobject candidate:   libcairo-gobject.so.2.11802.2
gobject candidate SHA:     2440680a9d0c94d58d87d5916d168535b7dc4263648df9aa0b787ef2f7d3a166
gobject SONAME:            libcairo-gobject.so.2
```

## In scope

- both exact candidate/member digests and SONAME identities;
- configure arguments, patch files, and Termux-prefix semantics;
- concrete filename drift and both SONAME-alias continuities;
- selected Pango/GTK Cairo rendering and Cairo-GObject consumer binding;
- dependency, conflict, exclusion, update, and atomic rollback boundaries.

## Out of scope

Cairo tools, headers, pkg-config, static and development surfaces, non-selected backends, complete rendering composition, target generation, installation, materialization, deployment, activation, and SUP-02 evidence collection.

## Required reading

- `docs/current/STATE.yaml`
- `docs/decisions/0005-proportional-assurance-depth.md`
- `docs/evidence/fontconfig-bounded-provider-authority.md`
- `docs/evidence/pixman-cairo-prerequisite-provider-authority.md`
- `docs/evidence/selected-obsidian-provider-composition-review.md`
- `experiments/glibc/selected-obsidian-provider-authority/review/generic-build-attestation-adaptation-root-review-set.tsv`
- `experiments/glibc/selected-obsidian-provider-authority/review/generic-recipe-binding-and-drift-target-receipt-review.tsv`

## Pending external inputs

None. Pixman prerequisite authority is accepted from result archive SHA-256 `3df4f72452b6fb36525ea651f58a0d9d0e551d6ab1f0076653588e767fb1ad9a`; the archive retains both exact Cairo members, the exact Pixman member, aliases, package metadata, and dynamic sections. Request another bounded Termux probe only if a new material ambiguity appears outside this retained evidence.

## Stop conditions

Stop without accepting authority if either exact candidate digest, configure/patch/prefix semantics, selected identity-to-SONAME continuity, Pango/GTK consumer binding, accepted Pixman prerequisite binding, another dependency/exclusion boundary, update, or atomic rollback cannot be bounded.

## Next valid action

Perform a bounded exact-file recipe, configure/patch/prefix, two-member filename-continuity, and Pango/GTK rendering consumer review using the retained exact Cairo/Pixman result archive. Request device execution only if this retained evidence cannot resolve a new material ambiguity.

## Completion criteria

- Exact artifact, both candidate members, SONAMEs, and recipe coordinates remain pinned.
- Every adaptation token and both concrete-filename continuity rules are explicit.
- Necessity, consumer binding, conflict/exclusion, update, and atomic rollback are explicit.
- The two-member provider root is accepted narrowly or left open with one precise blocker.
- Composition, target population, and activation remain separate.
