# Active task: diagnose the bounded GdkPixbuf JPEG `SIGSEGV`

> Task ID: `diagnose-libjpeg-so-62-gdkpixbuf-functional-segfault`
>
> Expected state on completion: the functional crash is isolated to candidate-specific behavior, the mixed runtime boundary, or the GdkPixbuf file/API path using read-only controls. Provider authority remains a later repository decision.

## Objective

Explain the `SIGSEGV` from the first bounded consumer analyzer without weakening the accepted candidate identity or inferring provider authority.

```text
candidate: libjpeg.so.62.4.0
candidate SHA-256: a537840ef9da6135cb3284bc3b3e0d1fb4f624180a416c2a3964b94714eb7fe5
consumer: libgdk_pixbuf-2.0.so.0.4200.12
consumer SHA-256: 16d15168c69d4ad61862462da9fe811b5be3bef898b940a4023e15b039f5b43c
failed result SHA-256: b010695561974c491aa0706600e867ea3a2b8b8abf43f8573c075418a047d92a
```

## Why now

The first exact consumer-binding attempt closed identity and static-symbol questions but crashed before it could produce decode or mapped-provider evidence. The smallest safe next step is to isolate the failing boundary with candidate/oracle, API-path, and loader controls rather than infer provider failure or repeat the same broad call.

## Known facts

- Candidate, consumer, SONAME binding and static symbol coverage passed.
- The consumer requires 22 JPEG symbols and the candidate provides all 22.
- The fixed decode process exited `139` during `gdk_pixbuf_new_from_file()` before any mapped-path output.
- The process used the Termux-glibc loader/libc with a Debian GdkPixbuf dependency world.
- Protected live state was unchanged.

## In scope

- Direct candidate and Debian-oracle libjpeg decode controls.
- Candidate-versus-oracle GdkPixbuf controls with identical environment.
- Memory-loader API versus file API controls.
- Termux-glibc loader versus Debian-rootfs loader controls when the latter is available and version-compatible.
- Pre-call loader, libc, dependency and `/proc/self/maps` evidence.
- Optional `LD_DEBUG` and `strace` diagnostics without requiring extra package installation.
- One structured failure-or-success result archive.

## Out of scope

- Installing or replacing any libjpeg.
- Mutating the Debian rootfs, Termux glibc prefix, provider store, target or deployment.
- Accepting or rejecting provider authority from the prior crash alone.
- Selecting Debian oracle bytes as target authority.
- Treating `libjpeg.so.8` as compatible.
- Full Obsidian or GTK runtime composition.

## Required reading

- `docs/current/STATE.yaml`
- `docs/constitution/PRINCIPLES.md`
- `docs/decisions/0005-proportional-assurance-depth.md`
- `docs/evidence/libjpeg-so-62-runpath-free-compatibility-provider-candidate-result-review.md`
- `docs/evidence/libjpeg-so-62-gdkpixbuf-consumer-binding-result-review.md`
- `docs/operations/COLLABORATION.md`
- `docs/operations/EXECUTION.md`
- `docs/operations/platforms/chatgpt-web.md`

## Pending external inputs

None. Exact candidate bytes, fixture and retained Debian consumer coordinates are known. The authoritative Termux environment owns the diagnostic execution.

## Next valid action

Prepare one self-contained read-only diagnostic matrix. It must preserve candidate/oracle separation, record every control independently, survive individual process crashes, and fail closed without provider acceptance.

## Stop conditions

Stop if exact candidate, consumer or oracle identity drifts; required loader/dependency coordinates cannot be bounded; protected state changes; or the diagnostic would require installation or rootfs mutation.

## Completion criteria

- direct libjpeg candidate/oracle controls are recorded;
- GdkPixbuf candidate/oracle controls are recorded for memory and file APIs;
- runtime-loader boundaries are explicit;
- a crash in one cell does not prevent collection of the remaining cells;
- the matrix identifies the smallest boundary that changes pass/fail behavior;
- provider authority remains a separate decision.
