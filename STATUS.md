# Status

> **State:** selected-Obsidian-closure passive B10 survival PASS, CPU map-selection contract open  
> **Updated:** 2026-07-12

## Working conclusions

- **Phase B1-B8 are closed.** Identity, static closure, selected data provenance, semantic disposition, and generation design are explicit.
- **Phase B9 passed.** Ninety-six content objects totaling 70,897,301 bytes are hash-correct; the 175-alias immutable generation is published; staged/final validation is 1851/1851 PASS.
- **`current` remains absent.** The promoted launcher and immutable generation are unchanged.
- **The passive no-input B10 run is valid operator evidence.** The operator observed only and did not click any GUI control.
- **Passive startup, topology, 100-second survival, and maps capture all passed.** Main, renderer, three zygotes, and one utility process survived; GPU-process count was zero.
- **Overall B10 still failed at `mapped_identity`.** Ninety-three of ninety-six selected object-store identities mapped.
- **Two selected ELF objects were bypassed.** `libXau.so.6` and `libXdmcp.so.6` mapped from `$PREFIX/glibc/lib` instead of the selected object store.
- **Absolute DT_RPATH is the leading explanation.** Four selected copied consumers retain `$PREFIX/glibc/lib` as DT_RPATH; retained edges connect three of them to both bypassed providers.
- **One selected font was merely demand-unmapped.** `DejaVuSansMono-Bold.ttf` did not map in the passive initial-window state. Requiring every selected data object to map is invalid.
- **The CPU graphics map model is incomplete.** `$PREFIX/glibc/lib/libX11-xcb.so.1.0.0`, previously classified as excluded graphics, mapped in main; app-local `libvk_swiftshader.so`, absent from the B9 semantic manifest, mapped in a zygote.
- **Process CPU policy and mapped graphics-object policy are distinct.** Exact `--disable-gpu`, renderer `--disable-gpu-compositing`, and zero GPU process do not imply zero graphics-related mappings.
- **Negative boundaries remain clean.** No broad-farm, rootfs-provider, or `current` mapping was observed.
- **The GTK vault-open capability remains separately open.** The earlier icon/pixbuf failure was interaction-triggered and does not negate passive survival.
- **Next action is read-only map-selection diagnosis.** Do not patch RPATH or rebuild the generation before source hashes, retained edges, and exception identities are recorded on-device.
- **Atomic activation, rollback, and garbage collection remain forbidden.**

## Architecture authority

```text
docs/refactor/0106-selected-obsidian-phase-b9-generation-materialization-pass.md
docs/refactor/0110-selected-obsidian-pixbuf-inventory-pass-and-interaction-boundary-correction.md
docs/refactor/0111-selected-obsidian-passive-b10-survival-pass-map-selection-failure.md
```

## Current focus

- [x] materialize and publish the immutable CPU generation
- [x] close launcher-shell contamination and long runtime-path startup failure
- [x] pass passive no-input topology, 100-second survival, and maps capture
- [x] identify two selected ELF substitutions and one demand-unmapped font
- [x] identify excluded/unmodelled graphics mappings
- [ ] run read-only B1/B2/B9/B10 map-selection diagnostic
- [ ] redesign selected/world/RPATH and CPU-map contracts
- [ ] run controlled vault-open pixbuf diagnostic
- [ ] create a new generation only after the corrected contract is explicit
- [ ] pass passive and interactive acceptance
- [ ] implement atomic activation and rollback

## Current stop lines

Do not:

```text
claim overall B10 PASS;
activate current;
mutate the existing immutable generation;
patch selected ELF RPATH before the diagnostic;
require every demand-loaded font/data object to map;
ignore libX11-xcb or libvk_swiftshader;
proceed to activation or garbage collection.
```

## Evidence policy

Passive survival, selected-ELF ownership, demand-loaded data use, mapped graphics policy, interactive file-chooser capability, activation, and rollback are separate claims.

```bash
out=<stage-specific-slug>-$(date +%Y%m%d-%H%M%S)
OUT=<stage output root>/$out
# run stage
tar czf ~/Downloads/$out.tgz $OUT
```
