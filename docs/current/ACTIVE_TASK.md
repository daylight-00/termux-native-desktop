# Active task: review exact libcloudproviders provider authority

> Task ID: `review-libcloudproviders-bounded-provider-authority`
>
> Expected state on completion: exact `libcloudproviders.so.0.3.6` is either accepted for the selected GTK cloud-provider integration capability or left open with a precise Class B configuration, consumer-binding, conflict, update or rollback blocker. No target population, deployment or activation occurs.

## Objective

Review the single-member `gpkg/libcloudproviders` root under ADR 0005 using its exact artifact/member identity, pinned recipe tree, extra configure semantics, selected GTK necessity, consumer binding, conflict/exclusion, update and rollback boundaries.

## Why now

The exact libthai/libdatrie/libiconv Thai-break chain and `thbrk.tri` content are bounded and accepted, reducing the selected composition gap count from 19 to 17. `libcloudproviders` is the smallest remaining reviewed-root, single-member T4 configuration tranche.

## Known coordinates

```text
root review:    generic-root-review:d5acfe552821242c8bec
recipe root:    gpkg/libcloudproviders
recipe tree:    ca7597d86cb1610e64f209ff2b84c3ea13c4357a
artifact:       libcloudproviders-glibc 0.3.6
artifact SHA:   62b4d4f5263a7750f56e4655fdf91011ec5dc2e137f4e73a08506ddbaa64c1ae
member:         libcloudproviders.so.0.3.6
member SHA:     54dea7e30b9e02f5626a374e5b62e5e975684a426a940f525a18eb4ce9e4f030
SONAME:         libcloudproviders.so.0
selected row:   selected:b912b41387c558b52895
```

## In scope

- exact member and SONAME identity;
- Class B extra configure semantics;
- selected GTK cloud-provider integration necessity and bounded consumer binding;
- conflict, exclusion, update and rollback review.

## Out of scope

- unrelated cloud-provider services or package surfaces;
- complete GTK composition acceptance;
- target generation, installation, materialization, deployment or activation;
- SUP-02 evidence collection.

## Required reading

- `docs/current/STATE.yaml`
- `docs/decisions/0005-proportional-assurance-depth.md`
- `docs/evidence/libthai-libdatrie-iconv-bounded-provider-authority.md`
- `docs/evidence/selected-obsidian-provider-composition-review.md`
- `experiments/glibc/selected-obsidian-provider-authority/review/generic-build-attestation-adaptation-root-review-set.tsv`
- `experiments/glibc/selected-obsidian-provider-authority/review/generic-artifact-member-inventory-receipt-review.tsv`

## Pending external inputs

None before static review. Request one bounded Termux probe only if exact consumer or feature binding cannot be resolved from retained evidence.

## Next valid action

Perform a bounded exact-file recipe and GTK consumer review. Request device execution only if static evidence cannot resolve a material ambiguity.

## Stop conditions

Stop without accepting authority if exact identity, configuration semantics, consumer binding, conflict/exclusion, update or rollback boundaries cannot be bounded.

## Completion criteria

- Exact artifact, member, SONAME and recipe coordinates remain pinned.
- Class B configuration semantics are explicit.
- Necessity, consumer binding, conflict/exclusion, update and rollback are explicit.
- The provider is accepted narrowly or left open with one precise blocker.
- Composition, target population and activation remain separate.
