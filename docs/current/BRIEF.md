# Current project brief

> Semantic state version: `2026-07-16.07`
>
> This is the compact current-state entry point. Exact commit and tree coordinates come from the checked-out full Git bundle, not from self-referential repository text.

## Purpose and constitutional boundary

`termux-native-desktop` turns a stock, non-root Android phone into a practical native Termux research and development workstation. The compact constitutional authority remains `docs/constitution/PROJECT.md`, `docs/constitution/PRINCIPLES.md`, and `AGENTS.md`.

## Operational boundary

Web-chat capability failures follow a stop-loss contract: perform one bounded representative probe, classify the limitation, stop equivalent retries, and switch to the registered authority fallback.

- The user Termux checkout is authoritative for network-backed Git clone, pull and push and for Android/device execution.
- Web-chat receives a user-created full Git bundle and may materialize it locally for bounded analysis and package authoring.
- Google Drive is the first and only connector attempt for each outbound artifact delivery; failure falls back to one identical user-visible artifact, and the next artifact tries Drive first again.
- Related exchange contents are delivered as one `.tar.zst`; runners contain the executable workflow and use `$HOME/Downloads` as the user receipt location.
- Sandbox DNS/egress failures are not retried through equivalent download paths; exact acquisition moves into a pinned user-Termux runner.

## Current provider boundary

ADR 0005 separates artifact identity, adaptation semantics, provider authority, composition, target population and activation. The claim inventory remains:

```text
28 roots
37 reviewed objects
89 separated claims
36 Class A
49 Class B
 1 conditional Class C
 3 Class D
```

The exact `libXcursor.so.1.0.2` member is now accepted only for GTK 3.24.49 X11 cursor theme, image, surface and custom-cursor handling. The Class B patch relocates built-in cursor-theme and pixmap search paths into the Termux prefix without changing the ELF ABI, SONAME or Xcursor API surface. GTK's X11 backend links `xcursor_dep` and directly invokes the Xcursor theme/image/cursor APIs, so no device probe was needed.

Other accepted bounded providers remain unchanged, including the X.Org base tranche, libtasn1, libepoxy, Pango family, project libjpeg, project GDK Pixbuf, GLib/libpng and official libmount/libblkid pair.

```text
bounded provider roots accepted overall: 13
accepted roots inside the 28-root inventory: 12
open roots inside the inventory: 16
accepted exact members: 19
included current-scope members: 18
deferred members: 1
composition review: REVIEWED_BLOCKED_INCOMPLETE
selected identity gaps: 19
target population: blocked
activation: blocked
```

Canonical decisions are under `docs/evidence/`; the current composition review is [`../evidence/selected-obsidian-provider-composition-review.md`](../evidence/selected-obsidian-provider-composition-review.md), and the new provider decision is [`../evidence/libxcursor-bounded-provider-authority.md`](../evidence/libxcursor-bounded-provider-authority.md).

## Current project phase

The active task is `review-libthai-bounded-provider-authority`.

The next proportional tranche is the exact `libthai.so.0.3.1` Class B provider review. It must bound `BUILD_IN_SRC` semantics, selected Pango/GTK Thai text necessity, `libdatrie` and runtime data binding, conflicts, update and rollback. No target population, materialization, deployment or activation is allowed.

## Current non-goals

Do not currently:

- fulfill SUP-02 without explicit Class C reclassification or escalation;
- broaden any accepted provider beyond its exact capability scope;
- infer cursor-theme data authority from the libXcursor shared-library decision;
- populate a provider target or activate a selected generation;
- use GitHub connector reads as repository reconstruction;
- use Docker or a PRoot application baseline.

## Start and navigation

- Active task: [`ACTIVE_TASK.md`](ACTIVE_TASK.md)
- Machine state: [`STATE.yaml`](STATE.yaml)
- Pending external inputs: [`PENDING_ARTIFACTS.yaml`](PENDING_ARTIFACTS.yaml)
- Documentation model: [`../DOCUMENTATION_MODEL.md`](../DOCUMENTATION_MODEL.md)
- Operations: [`../operations/README.md`](../operations/README.md)
- Evidence: [`../evidence/README.md`](../evidence/README.md)
