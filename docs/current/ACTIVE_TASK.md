# Active task: acquire exact util-linux binding for the accepted GDK Pixbuf stack

> Task ID: `acquire-gdkpixbuf-exact-util-linux-provider-binding`
>
> Expected state on completion: the official exact `libmount-glibc` and `libblkid-glibc` pair is either accepted for the bounded GDK Pixbuf stack or left open with a precise failure boundary. No installation, target population, deployment or activation occurs.

## Objective

Run one bounded, read-only Termux acquisition/analyzer transaction that replaces the scratch util-linux evidence with exact official package/member and runtime-binding evidence.

## Why now

The exact GLib `2.82.2-2` four-member family and libpng `1.6.47` shared member are accepted for the project-built GDK Pixbuf `2.42.12` fixed JPEG/PNG file and memory decode scope. The successful functional probe mapped scratch `libmount` and `libblkid` bytes whose digests differ from the official exact candidates already recorded by the repository.

```text
official libmount member SHA-256:
6864b9050ddd5884642c98ea4df07e3ceaf78727324d6e9068d1866594ece1c2

scratch mapped libmount SHA-256:
951a7e682476045acaa598eb05e2b79adc5f800b6fc34133eac49f797b064b40

official libblkid member SHA-256:
21d47963d42a5b1c4008c88a311c17142f57ee2f19cd30770f0befa364908fb3

scratch mapped libblkid SHA-256:
bd63dcc600487615ee6256b9cfe4d474ebc76899c911f8134d66765810e7db51
```

Scratch success cannot authorize the official pair.

## In scope

- Package all feasible download, checksum, extraction, recipe collection, ELF inspection, map assertion, functional execution, result packaging and upload logic in one Termux wrapper.
- Acquire exact `libmount-glibc 2.40.2-1` artifact SHA-256 `9004e88a9f43b2d5cf74fd8921e4b74146e3ced64c4f94490cc52d9b138b011a`.
- Acquire exact `libblkid-glibc 2.40.2-1` artifact SHA-256 `b6692956495df59ce70a854db5af86bae5f63791440e2cc5f21c26194b965fe`.
- Verify exact member names, SHA-256, SONAMEs and dependency edge `libmount.so.1 -> libblkid.so.1`.
- Review the pinned util-linux recipe tree `e91a0c476ef4355dbfff46e2bcab23d0085ddd01` under ADR 0005.
- Run the accepted exact GDK Pixbuf, GLib, libpng and libjpeg stack with the official pair.
- Assert exact `/proc/self/maps` identities and rerun JPEG/PNG file and memory cells.
- Preserve protected repository, provider, selected-generation and user state.

## Out of scope

- Installing either package into the live Termux/glibc prefix.
- Copying any provider into a target layout.
- Accepting unrelated util-linux libraries, tools or executables.
- Broad GIO service validation outside the fixed GDK Pixbuf decode scope.
- Complete composition acceptance, target generation, deployment or activation.
- SUP-02 evidence collection.

## Required reading

- `docs/current/STATE.yaml`
- `docs/constitution/PRINCIPLES.md`
- `docs/decisions/0005-proportional-assurance-depth.md`
- `docs/evidence/gdkpixbuf-reference-dependency-provider-authority.md`
- `docs/evidence/gdkpixbuf-2-42-12-provider-candidate-result-review.md`
- `docs/evidence/selected-obsidian-provider-composition-review.md`
- `experiments/glibc/selected-obsidian-provider-authority/review/gdkpixbuf-util-linux-transitive-provider-disposition.tsv`
- `experiments/glibc/selected-obsidian-provider-authority/review/generic-artifact-member-inventory-receipt-review.tsv`

## Known facts

- Exact GLib four-member and libpng provider authority is accepted only for the bounded GDK Pixbuf decode scope.
- Existing pcre2, libffi and zlib object authority remains separate and is not widened by this task.
- `libmount.so.1` is a direct dependency of exact `libgio-2.0.so.0.8200.2`.
- `libblkid.so.1` is a direct dependency of libmount and is outside the 36 selected GTK identity rows, but it is required for a coherent exact runtime binding.
- The successful scratch pair and official exact pair are not byte-identical.
- Composition has 21 unresolved selected identities and remains `REVIEWED_BLOCKED_INCOMPLETE`.

## Pending external inputs

None before package construction. See [`PENDING_ARTIFACTS.yaml`](PENDING_ARTIFACTS.yaml).

## Next valid action

Construct and simulate one read-only Termux acquisition/analyzer package for the exact official util-linux pair. The package must emit one `.tar.zst` result and must not mutate live provider or target state.

## Stop conditions

Stop without accepting provider authority if:

- either package or member digest differs;
- SONAME or dependency edges differ;
- the pinned recipe cannot be bounded semantically;
- the official pair fails exact mapping;
- any fixed JPEG/PNG functional cell fails;
- protected state changes;
- exact accepted GDK Pixbuf, GLib, libpng or libjpeg bytes cannot be bound.

## Completion criteria

- Exact official package and member identities are verified.
- util-linux Class B adaptation semantics are reviewed for the bounded objects.
- The fixed functional matrix and exact map set pass with the official pair, or a precise blocker is recorded.
- Provider authority remains object- and capability-scoped.
- Composition, target and activation boundaries remain explicit.
