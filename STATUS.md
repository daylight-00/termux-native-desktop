# Status

> **State:** selected-Obsidian-closure Phase B4 static capability matrix after corrected Phase B3 PASS  
> **Updated:** 2026-07-11

## Working conclusions

- **No PRoot-mediated normal application runtime.** PRoot remains an install/debug-time tool, package/library warehouse, and behavioral oracle.
- **The glibc application world is viable for real desktop applications.** Official VS Code and an extracted Obsidian AppImage run as glibc processes while the surrounding desktop remains bionic-native.
- **The core/provider boundary is load-bearing.** Termux glibc and Android-sensitive libraries must remain protected from Debian-derived provider closure; application-local `$ORIGIN` locality must be preserved where valid.
- **The scoped graphics-policy promotion transaction is closed.** Current OpenGL/Zink, VS Code GPU/CPU, and Obsidian GPU/CPU claims are trigger-routed and are not rerun for selected-closure analysis.
- **`modules/gl` and the broad farm remain transitional.** They are the current compatibility baseline, not the accepted final world/provider/application object model.
- **The selected Obsidian parent pilot continues.** Candidate materialization, actual selection, and control/candidate equivalence remain open.
- **Phase B1 passed read-only.** All 136 candidate-relevant paths matched captured SHA-256 identities; 113 ELF objects and 531 `DT_NEEDED` edges had zero review, collision, missing, unresolved, or ambiguous rows.
- **App-local locality is bounded.** The five AppDir ELF objects retain `$ORIGIN` first and have no observed external lookup-name competitor. `$ORIGIN` preservation and future collision rejection are candidate invariants.
- **Phase B2 passed read-only.** The graph contains 95 entrypoint-static objects, 98 objects in the union of all app-local static roots, 15 mapped-only dynamic/discovery objects, and 17 non-ELF data capability objects.
- **The first Phase B3 run failed in the recipe, not in evidence.** It aborted during family lookup because one Bash `local` command expanded associative-array lookups before local assignment. The invalid receipt is preserved in `0096`.
- **The corrected Phase B3 passed.** The 15 mapped-only objects reduce to five roots with zero unclassified roots: two graphics roots and three NSS/security roots.
- **Graphics dynamic ownership is separate.** `libvulkan_freedreno.so` and `libVkLayer_MESA_device_select.so` plus their support closure belong to the separately closed graphics feature/provider composition and are excluded from the minimum provider-neutral CPU candidate.
- **NSS/security is a required dynamic application capability direction.** `libfreeblpriv3.so`, `libnssckbi.so`, and `libsoftokn3.so` were mapped in the main process; `libsqlite3.so.0` supports `libsoftokn3.so`; NSPR/NSS static members already exist in the entrypoint closure.
- **The entrypoint has 34 direct providers.** They split into 1 app-local, 5 world substrate, 6 prefix, 21 rootfs, and 1 GBM direct root. This is heterogeneous and must not become one permanent provider object.
- **Locale, font, and GSettings data remain outside ELF closure.** The 12 locale, 4 font, and 1 schema objects require explicit data-provider ownership; `gschemas.compiled` remains `UNOWNED/UNKNOWN` despite stable byte identity.
- **Phase B4 is read-only.** It derives the closure and overlap matrix for the 28 external entrypoint-static direct roots before static capability ownership is decided.
- **No fresh Obsidian capture is required for identity drift.** No candidate bytes are materialized yet.
- **The recovered glibc substrate remains 2.42 and held.** The hold is temporary incident containment, not a permanent lifecycle design.
- **Atomic activation remains mandatory before the next multi-file promoted migration.** Implementation is deferred until the selected semantic object set is known.
- **`ELECTRON_DISABLE_SANDBOX=1` remains the highest-priority over-scoped global policy.** Ownership movement is deferred until the application/provider model is decided and validated.
- **Device evidence handoff uses stage-specific archives.** Each stage ends with `tar czf ~/Downloads/$out.tgz $OUT`; generic archive names are rejected.

## Architecture authority

```text
main/docs/system-foundation/11-architecture-reassessment-and-hard-refactor-decision.md
main/docs/system-foundation/12-document-consistency-audit-and-execution-order.md

docs/refactor/0092-post-graphics-closure-architecture-midpoint-audit.md
docs/refactor/0093-post-audit-direction-validator-lifecycle-and-selected-closure-reentry.md
docs/refactor/0094-selected-obsidian-phase-b1-retained-control-locality-pass.md
docs/refactor/0095-selected-obsidian-phase-b2-static-runtime-closure-pass.md
docs/refactor/0096-selected-obsidian-phase-b3-first-run-script-failure.md
docs/refactor/0097-selected-obsidian-phase-b3-capability-grouping-pass.md
docs/refactor/0091-scoped-graphics-policy-promotion-closure.md
docs/refactor/README.md
```

## Current focus

### Application-domain/provider architecture

- [x] continue the selected Obsidian parent pilot
- [x] pass Phase B1 retained identity/locality audit
- [x] pass Phase B2 static/runtime graph partition
- [x] preserve and diagnose the first Phase B3 script failure
- [x] pass corrected Phase B3 capability-grouping analysis
- [x] separate graphics dynamic roots from NSS/security roots
- [ ] run Phase B4 entrypoint-static direct-root closure/overlap matrix
- [ ] decide reusable static capability groups versus application-domain bindings
- [ ] decide locale/font/schema data ownership
- [ ] materialize and validate a selected CPU candidate if the pilot remains viable

### Runtime ownership and lifecycle

- [ ] define atomic activation after the selected object set is known
- [ ] complete world/provider/bridge/toolchain/family ownership split
- [ ] move over-scoped Electron/security policy out of the world baseline
- [ ] define glibc upgrade/recovery lifecycle beyond the 2.42 hold

### Next workload

- [ ] define the PyMOL capability contract without runtime mutation
- [ ] defer PyMOL implementation until reusable objects are decided
- [ ] use PyMOL as proof of the corrected architecture

## Current stop lines

Do not:

```text
rerun closed graphics gates without a documented trigger;
rerun Phase B1/B2/B3 without a source trigger;
make the broad farm the final provider by inertia;
include graphics dynamic roots in the minimum CPU candidate;
drop NSS dynamic roots or sqlite support;
materialize all 113 ELF objects as one candidate library directory;
treat all 95 static objects or all 34 direct providers as one semantic capability;
merge locale/font/schema data into ELF closure;
remove $ORIGIN or accept $HOME/gl/lib as final candidate authority;
materialize candidate bytes before static capability ownership is decided;
start PyMOL by extending the unresolved broad closure;
apply another multi-file promoted migration before activation semantics are defined;
use ambiguous evidence archive names such as results.tgz.
```

## Evidence policy

A mapped object is not automatically static, optional, or independently discovered. A static dependency is not automatically one semantic provider capability. Application-local selection, dynamic-root closure, static direct-root overlap, data ownership, and actual candidate selection are separate claims. Closed runtime gates are rerun only when their claim surface changes.

```bash
out=<stage-specific-slug>-$(date +%Y%m%d-%H%M%S)
OUT=<stage output root>/$out
# run the stage
tar czf ~/Downloads/$out.tgz $OUT
```

The tgz is a transport object. The contained receipt and original device evidence root remain authoritative.
