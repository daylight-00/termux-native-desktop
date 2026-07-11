# Status

> **State:** active selected-Obsidian-closure re-entry after post-graphics architecture audit  
> **Updated:** 2026-07-11

## Working conclusions

- **No PRoot-mediated normal application runtime.** PRoot remains an install/debug-time tool, package/library warehouse, and behavioral oracle.
- **The glibc application world is viable for real desktop applications.** Official VS Code and an extracted Obsidian AppImage run as glibc processes while the surrounding desktop remains bionic-native.
- **The core/provider boundary is load-bearing.** Termux glibc and Android-sensitive libraries must remain protected from Debian-derived provider closure; application-local `$ORIGIN` locality must be preserved where valid.
- **Real GPU acceleration works in both ABI worlds.** Promoted VS Code and Obsidian GPU branches select Turnip/Adreno 730 through correlated environment, argv, CDP, provider-map, and KGSL evidence.
- **Graphics policy is consumer-scoped.** The bionic desktop owns its bionic ICD and Zink session policy. The glibc boundary sanitizes inherited provider/bridge policy. Individual consumers deliberately compose provider, bridge, and feature mode.
- **The scoped graphics-policy promotion transaction is closed.** Expanded source/live installation, current OpenGL/Zink consumer, VS Code GPU/CPU, and Obsidian GPU/CPU have authoritative zero-failure receipts. Revalidation is trigger-based, not periodic.
- **The closure accepts semantic behavior, not permanent adapter identity.** `~/gl/env`, `gl-run`, `freedreno.sh`, `GL_GPU`, and `modules/gl` are current realizations. They are not architecture invariants merely because the transaction passed.
- **Application-state authority is part of evidence.** VS Code uses receipt-local user-data/extensions paths. Obsidian requires a receipt-local `XDG_CONFIG_HOME` plus the actual derived `<config>/obsidian` directory. Normal user profiles are outside promotion evidence.
- **A Chromium `gpu-process` name is not an acceleration or CPU-failure claim.** Acceptance is based on selected policy, effective feature/argv mode, renderer viability, and correlated provider/device evidence.
- **The ownership refactor remains accepted.** Project capabilities, package lifecycles, experiments, and repository tools have separate source owners. Semantic ownership still requires further decomposition.
- **`modules/gl` is transitional.** It still combines world baseline, passive data policy, Electron-family/security policy, farm materialization, OpenGL adapter, URL bridge, and target toolchain responsibilities.
- **The broad farm is still the current compatibility baseline, not an accepted final production provider model.** The D-Bus pilot proves selected materialized provider bytes are viable, but the shared/app-local boundary is not fully decided.
- **The parent Obsidian selected-closure pilot continues.** Graphics sub-questions are closed, while locality-shadowing, non-graphics static/runtime closure agreement, candidate materialization, actual candidate selection, and control/candidate equivalence remain open.
- **The first re-entry step is read-only.** Retained Obsidian control evidence is audited for identity stability, locality collisions, ELF dependency facts, and process-class semantic use before any candidate is materialized or any workload is relaunched.
- **The recovered glibc substrate remains 2.42 and held.** The hold is temporary incident containment, not a permanent lifecycle design.
- **Mutable checkout symlinks remain an activation defect.** Source changes can immediately alter live leaves, so another multi-file promoted migration must not proceed without a minimum activation boundary.
- **Atomic activation is not the next implementation object by itself.** Its complete managed-leaf set must follow the selected-closure result and semantic owner decision; it is mandatory immediately before the next multi-file promoted migration.
- **Current global non-graphics policy is over-scoped.** `ELECTRON_DISABLE_SANDBOX=1` is the highest-priority example: Electron-family/security policy currently lives in the world baseline.
- **Graphics validator lifecycle is classified.** Seven top-level active contract gates remain trigger-routed; invoked probes/classifiers are active gate dependencies; comparison helpers are evidence helpers; discovery scripts are historical diagnostics; superseded false-negative models remain historical records rather than scheduled tests.
- **The current Mesa graphics composition is cross-version.** Rootfs GLVND/GLX/Gallium-Zink, prefix loader/support, and provider-store Turnip identities form one validated composition; independent changes to any layer require composition-aware revalidation.
- **Device evidence handoff uses stage-specific archives.** Each evidence-producing stage defines `out` and `OUT`, then ends with `tar czf ~/Downloads/$out.tgz $OUT`; generic archive names are rejected.

## Architecture authority

Read in this order:

```text
main/docs/system-foundation/11-architecture-reassessment-and-hard-refactor-decision.md
main/docs/system-foundation/12-document-consistency-audit-and-execution-order.md

docs/refactor/0092-post-graphics-closure-architecture-midpoint-audit.md
    -> post-closure top-down audit and architectural gaps

docs/refactor/0093-post-audit-direction-validator-lifecycle-and-selected-closure-reentry.md
    -> accepted direction adjustment, gate lifecycle, evidence handoff, and next action

docs/refactor/0091-scoped-graphics-policy-promotion-closure.md
    -> closed graphics transaction and evidence-backed contract

docs/refactor/README.md
    -> chronological index and current stop lines
```

## Integrated guides

- `docs/architecture.md` — current integrated runtime model and target semantic architecture.
- `docs/glibc-layer.md` — current compatibility baseline, application-domain target, and lifecycle boundaries.
- `docs/gpu.md` — current graphics composition and revalidation contract.
- `docs/refactor/0091-scoped-graphics-policy-promotion-closure.md` — closed graphics-policy evidence matrix.
- `docs/refactor/0092-post-graphics-closure-architecture-midpoint-audit.md` — semantic-vs-adapter distinction and missing architecture work.
- `docs/refactor/0093-post-audit-direction-validator-lifecycle-and-selected-closure-reentry.md` — revised execution order and selected-closure re-entry.
- `docs/refactor/` — full transaction and evidence history.

## Open architecture questions

- How should a real Electron application domain consume selected provider bytes while preserving app-local `$ORIGIN` locality?
- Which prefix/rootfs providers are reusable capability groups, and which are application-domain bindings?
- Which global `gl/env` policies belong to world base, bridge, provider, Electron family, or individual application?
- What exact managed object set must the minimum atomic activation mechanism promote and roll back?
- How should a corrected current/newer glibc substrate be accepted, retained, rolled back, and released from hold?
- Which passive rootfs data capabilities remain intentionally rootfs-backed, and which should be materialized?
- How should the cross-version graphics composition be identified and revalidated across independent provider-layer updates?
- When are VS Code/Obsidian normal-profile long-duration checks required for operational acceptance rather than architecture promotion?

## Current focus

### Knowledge/control-plane closure

- [x] close the scoped graphics-policy promotion transaction
- [x] record the post-closure architecture midpoint audit
- [x] synchronize canonical experiment READMEs and migration journal
- [x] classify semantic invariants versus current adapters in integrated/module/package docs
- [x] classify graphics validators by active/dependency/evidence/historical/superseded status
- [x] establish the stage-specific tgz evidence handoff convention

### Application-domain/provider architecture

- [x] explicitly continue the selected Obsidian closure pilot
- [ ] run the retained-control locality input audit without launching a workload
- [ ] interpret identity mismatches, locality collisions, unresolved edges, and ambiguous edges
- [ ] finish locality-shadowing and non-graphics static/runtime closure agreement
- [ ] decide capability grouping and application-domain bindings
- [ ] prove selected candidate materialization/equivalence if the pilot remains viable

### Runtime ownership and lifecycle

- [ ] define atomic activation after the selected object set is known and before another multi-file live migration
- [ ] complete remaining world/provider/bridge/toolchain/family ownership split
- [ ] move high-risk global Electron/security policy out of world baseline when validated
- [ ] define glibc upgrade/recovery lifecycle beyond the 2.42 hold
- [ ] decide passive font/locale/schema data-provider ownership

### Next workload

- [ ] define PyMOL domain/capability contract now
- [ ] defer PyMOL runtime mutation until reusable objects above are decided
- [ ] use PyMOL as proof of the corrected architecture, not as a reason to expand global env/farm policy

## Current stop lines

Do not:

```text
rerun closed graphics gates without a documented trigger;
call current path/command/variable names permanent invariants;
expand gl-run into lifecycle authority;
make the broad farm the final production provider by inertia;
add new global policy to gl/env because it is convenient;
materialize an Obsidian candidate before retained evidence is interpreted;
analyze changed current bytes as though they were the captured control identity;
start PyMOL by copying an Electron launcher or expanding the farm blindly;
apply another multi-file promoted migration before activation semantics are defined;
maintain every experiment script as a permanent active gate;
claim isolated promotion receipts prove normal-profile long-duration behavior;
use ambiguous evidence archive names such as results.tgz.
```

## Evidence policy

A passing screenshot is insufficient. Claims remain at the strongest level supported by correlated evidence. Empty child `/proc/<pid>/environ` is an observability boundary. A mapped provider is not selected-device proof. Isolated application state must follow the application's real authority. A closed transaction validates a semantic contract; it does not automatically make its current helper names or paths permanent architecture. Runtime gates are rerun only when their claim surface changes.

Device evidence handoff is stage-specific:

```bash
out=<stage-specific-slug>-$(date +%Y%m%d-%H%M%S)
OUT=<stage output root>/$out
# run the stage
tar czf ~/Downloads/$out.tgz $OUT
```

The tgz is a transport object. The contained receipt and original device evidence root remain the evidence authority.
