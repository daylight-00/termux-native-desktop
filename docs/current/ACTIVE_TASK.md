# Active task: validate bounded `libjpeg.so.62` consumer binding

> Task ID: `validate-libjpeg-so-62-compatibility-provider-consumer-binding`
>
> Expected state on completion: the exact runpath-free candidate is either validated against the exact retained GdkPixbuf consumer with a fixed JPEG decode and mapped-path proof, or explicitly blocked with bounded diagnostics. Provider authority remains a later repository decision.

## Objective

Validate the exact candidate:

```text
member: libjpeg.so.62.4.0
SHA-256: a537840ef9da6135cb3284bc3b3e0d1fb4f624180a416c2a3964b94714eb7fe5
DT_SONAME: libjpeg.so.62
DT_RPATH/DT_RUNPATH: absent
```

against the bounded retained consumer:

```text
package: libgdk-pixbuf-2.0-0:arm64 2.42.12+dfsg-4+deb13u1
member: libgdk_pixbuf-2.0.so.0.4200.12
SHA-256: 16d15168c69d4ad61862462da9fe811b5be3bef898b940a4023e15b039f5b43c
capability: electron.gui.gtk3 image decoding
```

## Why now

The corrected scratch build closed source, producing-command, output identity, SONAME, symbol-version and dynamic-search-path requirements. ADR 0005 Class C assurance still requires bounded functional equivalence and exact consumer binding before provider authority can be decided.

## In scope

- Verify exact candidate and consumer bytes.
- Verify consumer `DT_NEEDED` includes `libjpeg.so.62`.
- Compare consumer undefined JPEG symbols with candidate definitions.
- Stage the candidate only under scratch with a SONAME link to its exact member.
- Load the exact consumer with the scratch candidate selected first.
- Decode one fixed JPEG fixture and record dimensions/channels.
- Record the actually mapped candidate path and competing SONAME-62 objects.
- Preserve protected live state and return one structured result archive.

## Out of scope

- Installing either candidate or consumer.
- Mutating the Debian rootfs, live prefix, provider store, deployment, target or selector.
- Selecting the Debian oracle `libjpeg.so.62.3.0` as target authority.
- Treating `libjpeg.so.8` as compatible.
- Accepting provider authority, composition, target population or activation in the analyzer.
- Launching the full Obsidian workload.

## Required reading

- `docs/current/STATE.yaml`
- `docs/constitution/PRINCIPLES.md`
- `docs/decisions/0005-proportional-assurance-depth.md`
- `docs/evidence/libjpeg-so-62-provider-candidate-disposition.md`
- `docs/evidence/libjpeg-so-62-runpath-free-compatibility-provider-candidate-result-review.md`
- `docs/operations/COLLABORATION.md`
- `docs/operations/EXECUTION.md`
- `docs/operations/platforms/chatgpt-web.md`

## Pending external inputs

None. The candidate bytes are already verified and can be embedded in the analyzer package. The authoritative Termux environment owns the exact rootfs consumer and runtime test.

## Next valid action

Prepare and synthetic-test one self-contained read-only Termux consumer-binding analyzer. It must fail closed on consumer digest drift, missing SONAME binding, unresolved JPEG symbols, wrong mapped candidate, decode failure, any protected-state change or any attempt to install or populate a target.

## Stop conditions

Stop without provider acceptance if the exact consumer is absent or changed, the consumer no longer needs `libjpeg.so.62`, candidate symbol coverage is incomplete, the candidate is not the mapped provider, fixed JPEG decoding fails, competing candidates create an unresolved collision, or protected state changes.

## Completion criteria

- exact consumer and candidate identities are verified;
- static symbol binding is complete;
- the fixed JPEG fixture decodes through the exact consumer;
- `/proc/self/maps` proves the scratch candidate was loaded;
- conflict/exclusion evidence is recorded;
- no installation or runtime mutation occurs;
- provider authority remains a separate next decision.
