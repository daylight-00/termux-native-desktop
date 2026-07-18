# Active task: acquire exact libXdamage provider evidence

> Task ID: `acquire-libxdamage-provider-evidence`
>
> Expected state on completion: an exact Termux glibc candidate for selected `libXdamage.so.1` is acquired and retained with package, member, SONAME, alias, recipe, dependency, and GTK consumer coordinates, or the identity remains open with one precise repository/candidate blocker. No installation, target population, deployment, or activation occurs.

## Objective

Close the next selected GTK composition gap by finding an authoritative exact provider candidate for `libXdamage.so.1`, retaining it without installation, and preparing a bounded provider review under ADR 0005.

## Why now

The exact Cairo and Cairo-GObject root is accepted atomically. Eight selected GTK identities remain, all outside the original 28-root provider inventory. `libXdamage.so.1` is the smallest X11 rendering prerequisite gap and has an exact selected SONAME but no retained Termux candidate.

## Known coordinates

```text
selected identity:      libXdamage.so.1.1.0
selected row:           selected:b0a8934c10bddecfc8ae
selected SHA-256:       032523eb33646cf6e1fad0f6c966cd86b33e3979db8c4901647d30854ca2779e
required lookup/SONAME: libXdamage.so.1
reference package:      libxdamage1:arm64 1:1.1.6-1+b2
candidate state:        NO_RETAINED_CANDIDATE
current root mapping:   NONE_REVIEWED_ROOT
```

## In scope

- approved-repository package metadata and exact archive acquisition without installation;
- exact member digest, ELF identity, SONAME and alias chain;
- pinned Termux recipe root/tree and Class A/B adaptation classification;
- runtime dependency closure and selected GTK X11 consumer binding;
- conflict, exclusion, update and rollback boundaries.

## Out of scope

Installation, package-manager mutation, target generation, materialization, deployment, activation, broad X11 provider ownership, and complete GTK composition.

## Required reading

- `docs/current/STATE.yaml`
- `docs/decisions/0005-proportional-assurance-depth.md`
- `docs/evidence/cairo-bounded-provider-authority.md`
- `docs/evidence/selected-obsidian-provider-composition-review.md`
- `experiments/glibc/selected-obsidian-provider-authority/review/generic-exact-candidate-receipt-review.tsv`
- `experiments/glibc/selected-obsidian-provider-authority/review/non-priority-generic-authority-ledger/gtk-gui.tsv`

## Pending external inputs

None before static repository and approved-index inspection. Request one read-only Termux acquisition probe only if exact package bytes or signed-index coordinates cannot be retained in the sandbox evidence path.

## Stop conditions

Stop without authority if no exact candidate can be acquired, the SONAME or alias does not match, recipe semantics cannot be bounded, runtime closure contains an unresolved provider, GTK consumer binding is ambiguous, or a member/alias collision exists.

## Next valid action

Inspect the approved Termux glibc package index and pinned recipe history for `libxdamage`, then acquire and extract the exact package without installation if available.

## Completion criteria

- Exact package, member, SHA-256, SONAME, alias, and recipe coordinates are retained, or one precise blocker is recorded.
- Adaptation, consumer, dependency, conflict, update, and rollback boundaries are explicit.
- No target, materialization, deployment, or activation occurs.
