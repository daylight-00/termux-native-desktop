# Status

> **State:** selected-Obsidian-closure Phase B3 capability-grouping input after Phase B2 pass  
> **Updated:** 2026-07-11

## Working conclusions

- **No PRoot-mediated normal application runtime.** PRoot remains an install/debug-time tool, package/library warehouse, and behavioral oracle.
- **The glibc application world is viable for real desktop applications.** Official VS Code and an extracted Obsidian AppImage run as glibc processes while the surrounding desktop remains bionic-native.
- **The core/provider boundary is load-bearing.** Termux glibc and Android-sensitive libraries must remain protected from Debian-derived provider closure; application-local `$ORIGIN` locality must be preserved where valid.
- **The scoped graphics-policy promotion transaction is closed.** Current OpenGL/Zink, VS Code GPU/CPU, and Obsidian GPU/CPU claims are trigger-routed and are not rerun for the selected-closure analysis.
- **Current graphics helpers are adapters, not permanent architecture.** World-boundary sanitation, consumer-scoped provider/bridge selection, application-owned feature mode, isolated state authority, and selected-device evidence are the durable contract.
- **`modules/gl` and the broad farm remain transitional.** They are the current compatibility baseline, not the accepted final world/provider/application object model.
- **The selected Obsidian parent pilot continues.** Candidate materialization, actual selection, and control/candidate equivalence remain open.
- **Phase B1 passed read-only.** All 136 candidate-relevant paths matched captured SHA-256 identities; 113 ELF objects and 531 `DT_NEEDED` edges had zero review, collision, missing, unresolved, or ambiguous rows.
- **App-local locality is now bounded.** The five AppDir ELF objects retain `$ORIGIN` first and have no observed external lookup-name competitor. `$ORIGIN` preservation and future collision rejection are candidate invariants.
- **Phase B2 passed read-only.** The graph contains 95 entrypoint-static objects, 98 objects in the union of all app-local static roots, 15 mapped-only dynamic/discovery objects, and 17 non-ELF data capability objects.
- **The 15 mapped-only objects reduce to five dynamic roots.** The roots are `libvulkan_freedreno.so`, `libVkLayer_MESA_device_select.so`, `libfreeblpriv3.so`, `libnssckbi.so`, and `libsoftokn3.so`; the remaining ten are root support dependencies.
- **Dynamic capability directions are separated.** The Turnip and Mesa-layer roots form a graphics direction with shared X11/DRI support; the three NSS roots form a security/database direction with `libsqlite3.so.0` supporting `libsoftokn3.so`.
- **The 95-object entrypoint-static closure remains heterogeneous.** Static reachability is not by itself one reusable provider capability.
- **Locale, font, and GSettings data remain outside ELF closure.** The 12 locale, 4 font, and 1 schema objects require explicit data-provider ownership.
- **The B2 calculation is valid but its tgz is not independently self-contained.** `input/semantic-objects.tsv` was verified on device but not embedded. The separately retained B1+B2 archive chain supports complete verification; no runtime rerun is justified for this packaging-only boundary.
- **Phase B3 is read-only.** It derives dynamic roots, root-specific closures, shared support, entrypoint direct providers, package summaries, and data summaries before capability ownership is decided.
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
docs/refactor/0091-scoped-graphics-policy-promotion-closure.md
docs/refactor/README.md
```

## Open architecture questions

- Which entrypoint-static packages form reusable capability groups rather than application-domain bindings?
- Which dynamic roots and support objects belong to graphics and NSS/security capabilities?
- Which locale/font/schema objects remain rootfs-backed and which become selected data objects?
- Which global policies belong to world base, bridge, provider, Electron family, or individual application?
- What exact object set must atomic activation promote and roll back?
- How should a corrected/newer glibc substrate be accepted, retained, rolled back, and released from hold?
- When are normal-profile long-duration checks required for operational rather than architecture acceptance?

## Current focus

### Knowledge/control-plane closure

- [x] close the scoped graphics-policy promotion transaction
- [x] record the post-closure architecture audit and direction adjustment
- [x] classify graphics validator lifecycle
- [x] establish stage-specific tgz handoff

### Application-domain/provider architecture

- [x] continue the selected Obsidian parent pilot
- [x] pass Phase B1 retained identity/locality audit
- [x] pass Phase B2 static/runtime graph partition
- [x] identify five dynamic roots and ten support dependencies
- [ ] run Phase B3 capability-grouping input analysis
- [ ] decide dynamic graphics and NSS/security ownership
- [ ] decompose the heterogeneous entrypoint-static provider set
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
make the broad farm the final provider by inertia;
materialize all 113 ELF objects as one candidate library directory;
treat all 95 static objects as one semantic capability;
treat all 15 mapped-only objects as independent roots;
drop dynamic support dependencies;
merge graphics and NSS/security dynamic closures;
merge locale/font/schema data into ELF closure;
remove $ORIGIN or accept $HOME/gl/lib as final candidate authority;
materialize candidate bytes before capability ownership is decided;
start PyMOL by extending the unresolved broad closure;
apply another multi-file promoted migration before activation semantics are defined;
use ambiguous evidence archive names such as results.tgz.
```

## Evidence policy

A mapped object is not automatically static, optional, or independently discovered. A static dependency is not automatically one semantic provider capability. Application-local selection, dynamic-root closure, data ownership, and actual candidate selection are separate claims. Closed runtime gates are rerun only when their claim surface changes.

```bash
out=<stage-specific-slug>-$(date +%Y%m%d-%H%M%S)
OUT=<stage output root>/$out
# run the stage
tar czf ~/Downloads/$out.tgz $OUT
```

The tgz is a transport object. The contained receipt and original device evidence root remain authoritative.
