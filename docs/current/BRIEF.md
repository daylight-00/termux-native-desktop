# Current project brief

> Semantic state version: `2026-07-15.17`
>
> This is the compact current-state entry point. Exact commit and tree coordinates come from the checked-out full Git bundle, not from self-referential repository text.

## Purpose and constitutional boundary

`termux-native-desktop` is a systems-engineering project for turning a stock, non-root Android phone into a practical native Termux research and development workstation.

```text
Android / Termux native host authority
    + coherent bionic and glibc execution worlds
    + explicit bridges and capability providers
    + application runtime domains
    + evidence-gated promotion and activation
```

PRoot and Debian may serve as oracle, supply, reference, or debugging control. They are excluded from the normal promoted application runtime.

Current constitutional authority is deliberately compact:

```text
docs/constitution/PROJECT.md
    identity, boundary, quality goals and non-goals

docs/constitution/PRINCIPLES.md
    engineering, evidence, promotion and assurance invariants

AGENTS.md
    agent/user authority, context, transport and execution discipline
```

Former project-context/principles and system-foundation documents are preserved as design provenance.

## Web-chat operational boundary

Web-chat capability failures follow a stop-loss contract: perform one bounded representative probe, classify the missing capability, stop equivalent retries, and switch to the registered fallback authority. In particular, exact bytes blocked by sandbox DNS or egress are acquired or analyzed through one self-contained user-Termux wrapper with pinned coordinates and digests. Reusable new limitations are committed to the platform registry rather than rediscovered by later sessions.

## Current structural state

- `main` is the only intended long-lived integration branch.
- The user Termux checkout is authoritative for remote Git mutation and device execution.
- A checkout is authoring state, not live runtime authority.
- Repository deployment uses immutable releases with explicit `current` activation and retained rollback state.
- The historical `$HOME/gl/.git` authority is retired and preserved in safety artifacts.
- Mesa mutable work and provider candidates are canonical under XDG state.
- Legacy `$HOME/gl/build` and `$HOME/gl/opt` are compatibility coordinates only.
- Application bodies, selected generations, provider contents, and user data remain outside repository ownership.

## Current provider boundary

The provider-authority corpus is now classified under accepted ADR 0005.

```text
28 roots
37 reviewed objects
89 separated claims
36 Class A
49 Class B
 1 conditional Class C
 3 Class D
```

The 28 historical SUP-02 requests are classified as:

```text
still necessary now: 0
narrowed:            14
replaced:             7
unnecessary:          7
```

The seven no-token recipe roots have completed bounded semantic review and bounded provider selection. The four X.Org roots `libxfixes`, `libxcomposite`, `libxi`, and `libxinerama` are accepted for their exact Termux members and selected GTK 3.24.49 X11 capabilities. `libtasn1` is accepted for the selected external GnuTLS 3.8.9 ASN.1/security capability. `libepoxy` is accepted only for GTK 3.24.49 X11 GLX dispatch; EGL is not claimed. The exact Pango 1.54.0 `libpango`, `libpangoft2`, and `libpangocairo` members are accepted as one GTK text provider family with explicit SONAME successor, update, and rollback continuity. The decisions are recorded in [`../evidence/xorg-reference-consumed-provider-authority.md`](../evidence/xorg-reference-consumed-provider-authority.md), [`../evidence/libtasn1-reference-consumed-provider-authority.md`](../evidence/libtasn1-reference-consumed-provider-authority.md), [`../evidence/libepoxy-reference-consumed-provider-authority.md`](../evidence/libepoxy-reference-consumed-provider-authority.md), and [`../evidence/pango-reference-consumed-provider-authority-and-filename-continuity.md`](../evidence/pango-reference-consumed-provider-authority-and-filename-continuity.md).

```text
bounded providers accepted: 7
remaining no-token provider roots open: 0
provider claims still open: 21
complete composition: not reached
target population: blocked
activation: blocked
```

Exact artifact/member identity, adaptation semantics, provider selection, composition, target population, and activation remain separate states. OJ-001 is dispositioned at [`../evidence/libjpeg-so-62-provider-candidate-disposition.md`](../evidence/libjpeg-so-62-provider-candidate-disposition.md), and the rejected first-candidate review is at [`../evidence/libjpeg-so-62-compatibility-provider-candidate-result-review.md`](../evidence/libjpeg-so-62-compatibility-provider-candidate-result-review.md), and the corrected candidate review is at [`../evidence/libjpeg-so-62-runpath-free-compatibility-provider-candidate-result-review.md`](../evidence/libjpeg-so-62-runpath-free-compatibility-provider-candidate-result-review.md). The claim inventory remains at [`../evidence/provider-claim-classification.md`](../evidence/provider-claim-classification.md).

## Documentation and web-session state

- New web-chat sessions receive a user-created full Git bundle and start at `START_HERE.md`.
- `docs/current/` owns current semantic state, the active task, and pending external artifacts.
- [`../DOCUMENTATION_MODEL.md`](../DOCUMENTATION_MODEL.md) defines authority and lifecycle by question.
- [`../catalog.tsv`](../catalog.tsv) is the machine-readable document catalog.
- Default onboarding is exactly four files and loads no history.
- Narrative handoffs, numbered refactor records, experiment reports, and system-foundation documents are not default onboarding authority.
- GitHub connector use is limited to lightweight remote inspection; it is not clone/commit/push transport.
- [`../operations/README.md`](../operations/README.md) is the single current surface for collaboration, bundle transport, execution transactions, result review, checkpoints, troubleshooting, and platform capabilities.
- The former `docs/session-operations/` surface and narrative handoffs are historical only.
- Google Drive is the primary exchange path for bundles, patches, runners, results, logs, and safety artifacts.
- The first connector upload after runtime initialization or reset may block file-reference rewriting even in an existing chat; use a user-visible sandbox link only for that delivery, then attempt Drive first again on the next outbound artifact.

## Current project phase

The active task is `diagnose-libjpeg-so-62-gdkpixbuf-functional-segfault`.

All no-token provider roots are complete. The corrected OJ-001 candidate `a537840e…` retains accepted identity: exact `libjpeg.so.62.4.0`, `DT_SONAME=libjpeg.so.62`, no dynamic search path and the expected symbol versions. The first GdkPixbuf consumer analyzer verified exact consumer identity, `DT_NEEDED=libjpeg.so.62`, and complete 22-symbol coverage, then exited with `SIGSEGV` during the fixed JPEG file decode before mapped-path evidence. Because that process mixed the Termux-glibc loader/libc with a Debian consumer dependency world, the crash does not yet isolate candidate behavior. The active phase runs direct-libjpeg, candidate-versus-oracle, memory-versus-file API and loader-boundary controls. The `libjpeg.so.8` family remains an invalid substitute, and no provider authority, composition, target population, materialization or activation is accepted.

## Current non-goals

Do not currently:

- issue or fulfill a SUP-02 request without a recorded Class C reclassification or escalation trigger;
- broaden the seven accepted provider rows beyond their exact bounded capability scopes;
- populate a provider target layout;
- activate the selected Obsidian generation;
- redesign the runtime around Docker or a PRoot application baseline;
- reconstruct the repository through raw GitHub connector reads;
- read or move the full historical corpus by default.

## Start and navigation

- Active task: [`ACTIVE_TASK.md`](ACTIVE_TASK.md)
- Machine state: [`STATE.yaml`](STATE.yaml)
- Pending external inputs: [`PENDING_ARTIFACTS.yaml`](PENDING_ARTIFACTS.yaml)
- Documentation model: [`../DOCUMENTATION_MODEL.md`](../DOCUMENTATION_MODEL.md)
- Documentation router: [`../INDEX.md`](../INDEX.md)
- Constitution: [`../constitution/README.md`](../constitution/README.md)
- Agent contract: [`../../AGENTS.md`](../../AGENTS.md)
