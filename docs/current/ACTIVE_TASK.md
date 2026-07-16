# Active task: review the GdkPixbuf reference dependency providers

> Task ID: `review-gdkpixbuf-reference-dependency-providers`
>
> Expected state on completion: the exact GLib-family and libpng candidates used by the accepted GdkPixbuf provider are either accepted with bounded provider authority or left open with a precise minimal evidence action; the `libmount`/`libblkid` transitive boundary is explicitly resolved. No target population or activation occurs.

## Objective

Close the smallest remaining dependency-provider boundary exposed by the accepted GdkPixbuf 2.42.12 object.

## Why now

The exact project-built GdkPixbuf object passed JPEG and PNG file and memory decoding and now has bounded provider authority. Its tested runtime still depends on five reference candidates whose provider authority is open:

```text
libglib-2.0.so.0
libgobject-2.0.so.0
libgmodule-2.0.so.0
libgio-2.0.so.0
libpng16.so.16
```

The exact GIO path also mapped scratch `libmount.so.1` and `libblkid.so.1`. Those two objects were diagnostic candidates only and must not be silently absorbed into the accepted composition.

## In scope

- Review the exact pinned GLib 2.82.2-2 four-member family and libpng 1.6.47 candidate identities.
- Review their package-specific recipe adaptations under ADR 0005.
- Bind their necessity to the accepted GdkPixbuf object and exact tested mappings.
- Identify conflicts, exclusions, update and rollback boundaries.
- Resolve whether exact Termux `libmount` and `libblkid` candidates can be reviewed from existing evidence or require one bounded acquisition/analyzer action.
- Update the non-materializing composition review only for accepted provider rows.

## Established inputs

```text
accepted GdkPixbuf member:
    libgdk_pixbuf-2.0.so.0.4200.12
    SHA-256 0c1404c6854e7674428a5b653b240759dac0374631697fe61ae275898f6a809f

exact GLib artifact:
    glib-glibc 2.82.2-2
    artifact SHA-256 d91fe1202c51f7e59b120d3b475e24cdc2ac2cc28f2804e9bcf4919b775978e6

exact libpng artifact:
    libpng-glibc 1.6.47
    artifact SHA-256 b2835404d3b0f54b75eb464a58ad5eb46f2d64d4fe1167a7984031f0e990b33f

observed transitive diagnostic objects:
    libmount.so.1.1.0 / 951a7e682476045acaa598eb05e2b79adc5f800b6fc34133eac49f797b064b40
    libblkid.so.1.1.0 / bd63dcc600487615ee6256b9cfe4d474ebc76899c911f8134d66765810e7db51
```

## Required reading

- `docs/current/STATE.yaml`
- `docs/constitution/PRINCIPLES.md`
- `docs/decisions/0005-proportional-assurance-depth.md`
- `docs/evidence/gdkpixbuf-2-42-12-provider-candidate-result-review.md`
- `docs/evidence/gdkpixbuf-core-provider-acquisition-result-review.md`
- `docs/evidence/selected-obsidian-provider-composition-review.md`
- `experiments/glibc/selected-obsidian-provider-authority/review/gdkpixbuf-core-provider-acquisition-result-review.tsv`
- `experiments/glibc/selected-obsidian-provider-authority/review/generic-artifact-member-inventory-receipt-review.tsv`

## Pending external inputs

None for the initial review. Request one bounded Termux acquisition/analyzer package only if the existing exact Termux `libmount`/`libblkid` artifact or ELF evidence is insufficient.

## Next valid action

Perform a non-mutating provider-authority review of the GLib family, libpng and the observed util-linux transitive boundary. Do not build or acquire new bytes before identifying the exact remaining evidence gap.

## Out of scope

- Installing or copying provider bytes.
- Accepting scratch util-linux objects merely because they enabled the diagnostic run.
- Generating a target manifest.
- Population, deployment, selector mutation or activation.
- Broad GTK provider review outside this dependency tranche.

## Stop conditions

Stop if a provider decision would require assuming recipe semantics not yet reviewed, if exact Termux artifact/member identity is missing, if a consumer maps a different object than the proposed provider, or if the transitive closure cannot be separated from unreviewed runtime policy.

## Completion criteria

- each of the five direct reference candidates has an explicit provider decision or exact minimal blocker;
- `libmount` and `libblkid` have an explicit authority/disposition state;
- composition counts reflect only accepted rows;
- no target or live mutation;
- the next task is fully repository-owned and does not depend on chat memory.
