# Status

> **State:** selected-Obsidian-closure passive runtime PASS; CPU map contract decided; interactive vault-open capability next  
> **Updated:** 2026-07-12

## Working conclusions

- **Phase B1-B8 are closed.** Identity, static closure, selected data provenance, semantic disposition, and generation design are explicit.
- **Phase B9 passed.** Ninety-six content objects totaling 70,897,301 bytes are hash-correct; the 175-alias immutable generation is published; staged/final validation is 1851/1851 PASS.
- **The existing generation remains immutable and unactivated.** `current` is absent and the promoted launcher is unchanged.
- **Passive B10 startup, topology, 100-second survival, and maps capture passed.** Main, renderer, three zygotes, and one utility process survived with zero GPU process.
- **The passive mapped-identity diagnostic passed.** All 96 selected objects remain hash-correct; the two mapped source substitutes also match their selected hashes.
- **`libXau` and `libXdmcp` are exact world-source substitutions.** Four selected consumers retain absolute `DT_RPATH=$PREFIX/glibc/lib`, and six retained edges connect three consumers to both substituted providers.
- **Minimum-manipulation decision: reclassify Xau/Xdmcp as protected world.** Do not patch RPATH. Remove their duplicate materialization only in the next generation; never mutate the current generation.
- **The passive missing Bold font was demand-unmapped.** Selected data requires immutable presence/hash, not universal mapping in every workload state.
- **`libX11-xcb` is CPU-required X11 substrate.** It moves from excluded graphics to protected-world CPU bridge.
- **App-local `libvk_swiftshader.so` is an allowed CPU auxiliary mapping.** Its presence does not imply a GPU process or enabled GPU path; it must enter the semantic manifest with exact identity.
- **The old exact 125-object mapped-set rule is retired.** Passive acceptance becomes class/set based: required selected ELF, required protected world, required app-local, allowed app-local auxiliary, demand-loaded selected data, receipt state, and forbidden providers.
- **Clean negative boundaries remain.** Broad-farm, rootfs-provider, and `current` mappings are zero.
- **The corrected pre-pixbuf generation baseline is 94 content identities.** Eighty-nine selected ELF, four fonts, and one generated schema; final counts wait for the interactive data/plugin delta.
- **The GTK vault-open capability remains open.** Inventory found one unusable FHS-path loader cache, twelve rootfs loader modules, two icon-theme indexes, and five MIME database files absent from the B9 manifest.
- **The next action is a controlled interactive pixbuf diagnostic.** It must use a receipt-local relocated loader cache and treat rootfs module mappings as diagnostic-only, not acceptance.
- **Do not create a new generation yet.** CPU-map and GTK data/plugin corrections must enter one unified generation preflight.
- **Atomic activation, rollback, and garbage collection remain forbidden.**

## Architecture authority

```text
docs/refactor/0106-selected-obsidian-phase-b9-generation-materialization-pass.md
docs/refactor/0110-selected-obsidian-pixbuf-inventory-pass-and-interaction-boundary-correction.md
docs/refactor/0111-selected-obsidian-passive-b10-survival-pass-map-selection-failure.md
docs/refactor/0112-selected-obsidian-passive-map-selection-diagnostic-pass-and-contract-decision.md
```

## Current focus

- [x] materialize and publish the immutable CPU generation
- [x] pass passive no-input startup, topology, 100-second survival, and maps capture
- [x] close Xau/Xdmcp source substitutions and absolute-RPATH cause
- [x] redesign passive selected/world/data/graphics map classes
- [x] choose protected-world reclassification over RPATH patching
- [ ] run controlled interactive vault-open pixbuf diagnostic
- [ ] identify the minimum loader/icon/MIME capability
- [ ] synthesize one unified corrected generation manifest
- [ ] materialize and validate a new generation
- [ ] pass passive and interactive acceptance
- [ ] implement atomic activation and rollback

## Current stop lines

Do not:

```text
claim full Obsidian acceptance from passive PASS;
patch RPATH or mutate the existing generation;
materialize Xau/Xdmcp in the next generation;
copy every pixbuf/icon/MIME inventory path wholesale;
use the rootfs loaders.cache unchanged;
add rootfs or broad-farm paths to an acceptance run;
create current;
create a new generation before the interactive capability is closed;
implement garbage collection.
```

## Evidence policy

Passive survival, ELF ownership, demand-loaded data, CPU graphics mappings, interactive file chooser capability, generation synthesis, activation, and rollback are separate claims.

```bash
out=<stage-specific-slug>-$(date +%Y%m%d-%H%M%S)
OUT=<stage output root>/$out
# run stage
tar czf ~/Downloads/$out.tgz $OUT
```
