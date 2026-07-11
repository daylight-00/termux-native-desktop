# Status

> **State:** selected-Obsidian-closure Phase B5 data provenance after Phase B4 PASS  
> **Updated:** 2026-07-11

## Working conclusions

- **No PRoot-mediated normal application runtime.** PRoot remains an install/debug-time tool, package/library warehouse, and behavioral oracle.
- **The glibc application world is viable for real desktop applications.** Official VS Code and an extracted Obsidian AppImage run as glibc processes while the surrounding desktop remains bionic-native.
- **The core/provider boundary is load-bearing.** Termux glibc and Android-sensitive libraries remain protected from Debian-derived provider closure; application-local `$ORIGIN` locality remains first.
- **The scoped graphics-policy promotion transaction is closed.** Current OpenGL/Zink, VS Code GPU/CPU, and Obsidian GPU/CPU claims are trigger-routed and are not rerun for selected-closure analysis.
- **`modules/gl` and the broad farm remain transitional.** They are the current compatibility baseline, not the accepted final world/provider/application object model.
- **The selected Obsidian parent pilot continues.** Candidate materialization, actual selection, and control/candidate equivalence remain open.
- **Phase B1 passed read-only.** All 136 candidate-relevant paths matched captured SHA-256 identities; 113 ELF objects and 531 `DT_NEEDED` edges had zero review, collision, missing, unresolved, or ambiguous rows.
- **Phase B2 passed read-only.** The graph contains 95 entrypoint-static objects, 98 objects in all app-local static roots, 15 mapped-only dynamic/discovery objects, and 17 non-ELF data objects.
- **Corrected Phase B3 passed.** The 15 mapped-only objects reduce to two graphics roots and three NSS/security roots with zero unclassified roots.
- **Graphics dynamic ownership is separate.** Turnip and the Mesa device-selection layer are excluded from the minimum provider-neutral CPU candidate and composed only by the separately closed graphics feature contract.
- **NSS/security is required.** NSS/NSPR static members, freebl/trust/softokn dynamic modules, and SQLite support form one required application capability direction.
- **Phase B4 passed read-only.** The entrypoint has 34 direct providers, including 28 external roots. Their static union contains 87 external ELF objects.
- **Static direct-root closures overlap heavily.** There are 51 shared external objects, 111 overlapping root pairs, and 144 external package dependency edges.
- **GTK is the dominant static root.** Its 60-object external closure contains 18 other external direct roots completely. CUPS, NSS/NSPR, ALSA, udev, GBM, and compiler support remain residual directions.
- **Static provider ownership is now manifest-based.** The target is typed semantic capability manifests over one deduplicated application-domain generation—not one copied tree per root and not one untyped flat blob.
- **The minimum CPU candidate static direction is explicit.** It includes 87 selected external static ELF objects plus required NSS/security dynamic objects, references but does not copy world substrate, leaves app-local objects in the AppDir, and excludes Vulkan provider dynamic roots.
- **Static GBM remains required in CPU mode.** The executable directly needs `libgbm.so.1`; static graphics ABI support is distinct from selected GPU provider/feature capability.
- **Data remains the final pre-materialization blocker.** Twelve locale objects, four fonts, and one generated `gschemas.compiled` aggregate require identity, package, source, compiler, and ownership decisions.
- **Phase B5 is read-only.** It verifies data byte identity, derives rootfs package ownership from dpkg `.list` files, inventories GSettings XML/override sources and compiler provenance, and proposes data ownership directions.
- **No fresh Obsidian capture is required for identity drift.** No candidate bytes are materialized yet.
- **The recovered glibc substrate remains 2.42 and held.** The hold is temporary incident containment, not a permanent lifecycle design.
- **Atomic activation remains mandatory before the next multi-file promoted migration.** Implementation is deferred until the complete generation manifest is known.
- **`ELECTRON_DISABLE_SANDBOX=1` remains the highest-priority over-scoped global policy.** Ownership movement is deferred until the application/provider model is validated.
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
docs/refactor/0098-selected-obsidian-phase-b4-entrypoint-static-matrix-pass.md
docs/refactor/0091-scoped-graphics-policy-promotion-closure.md
docs/refactor/README.md
```

## Current focus

### Application-domain/provider architecture

- [x] pass Phase B1 retained identity/locality audit
- [x] pass Phase B2 static/runtime graph partition
- [x] pass corrected Phase B3 dynamic capability grouping
- [x] pass Phase B4 static direct-root closure/overlap matrix
- [x] choose typed manifests over one deduplicated application-domain generation
- [ ] run Phase B5 locale/font/schema provenance audit
- [ ] decide data ownership and schema compilation contract
- [ ] build the selected CPU candidate manifest
- [ ] materialize and validate the selected CPU candidate

### Runtime ownership and lifecycle

- [ ] define atomic activation for the completed generation manifest
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
rerun closed graphics gates or Phase B1-B4 without a source trigger;
make one copied provider tree per direct root;
make one untyped 87-object candidate blob;
copy app-local or world substrate ELF into the candidate;
include Vulkan provider roots in the minimum CPU candidate;
drop required NSS modules, SQLite support, or static GBM;
merge locale/font/schema data into the ELF closure;
materialize candidate bytes before data ownership is closed;
remove $ORIGIN or accept $HOME/gl/lib as final candidate authority;
start PyMOL by extending the broad farm;
apply another multi-file promoted migration before activation semantics are defined;
use ambiguous evidence archive names such as results.tgz.
```

## Evidence policy

Application-local selection, static closure, dynamic-root closure, semantic manifest membership, data provenance, materialization, and actual candidate selection are separate claims. Package boundaries identify provenance but do not automatically define physical deployment boundaries. Closed runtime gates are rerun only when their claim surface changes.

```bash
out=<stage-specific-slug>-$(date +%Y%m%d-%H%M%S)
OUT=<stage output root>/$out
# run the stage
tar czf ~/Downloads/$out.tgz $OUT
```

The tgz is a transport object. The contained receipt and original device evidence root remain authoritative.
