# Status

> **State:** selected-Obsidian-closure GTK pixbuf/data inventory after Phase B10 topology PASS and survival FAIL  
> **Updated:** 2026-07-12

## Working conclusions

- **No PRoot-mediated normal application runtime.** PRoot remains an install/debug-time tool, package/library warehouse, and behavioral oracle.
- **The glibc application world is viable.** Official VS Code and extracted Obsidian run as glibc applications while the desktop remains bionic-native.
- **The core/provider boundary is load-bearing.** App-local `$ORIGIN` remains first; protected world glibc remains separate; rootfs/prefix location is provenance rather than final ownership.
- **Phase B1-B8 are closed.** Identity, static closure, capability ownership, selected data provenance, semantic disposition, and generation design are explicit.
- **Phase B9 passed.** Ninety-six content objects totaling 70,897,301 bytes are hash-correct; the 175-alias immutable generation is published; staged/final validation is 1851/1851 PASS; `current` remains absent.
- **The first B10 failure was launcher-shell loader contamination.** It was corrected by injecting candidate `LD_LIBRARY_PATH` only in the final Obsidian exec.
- **The second B10 failure exposed long runtime/socket paths.** It observed only a short-lived main and no renderer/zygote.
- **The short-runtime discriminator passed topology.** With a 48-character runtime root and 52-character TMPDIR, main, three zygotes, one utility process, and one renderer formed; no GPU process appeared.
- **The long-path hypothesis is supported for startup.** `SingletonSocket` and `SingletonCookie` were created only in the short-path run.
- **Phase B10 still failed survival.** The topology remained present through 28 survival samples, then the main aborted approximately 72 seconds after startup.
- **The fatal boundary is GTK icon/pixbuf handling.** `hicolor` was absent; GTK fallback `image-missing.png` failed with `Unrecognized image file format`; `gtkiconhelper.c` asserted and the application bailed out.
- **Inotify, missing system D-Bus, and missing `xdg-settings` remain non-fatal warnings in this receipt.**
- **The generation already contains libgdk-pixbuf, libpng, and libjpeg.** The open boundary is runtime data/plugin discovery rather than the direct DT_NEEDED ELF closure.
- **The B9 data manifest has no explicit gdk-pixbuf loader cache/modules, icon-theme data, or shared MIME database.** Maps-derived closure did not establish later file-open/plugin capabilities.
- **The next stage is read-only inventory, not blind generation mutation.** It will identify loader caches/modules and icon/MIME data by path, package, version, hash, and semantic-manifest coverage.
- **No accepted rootfs-provider leakage is permitted.** A later controlled rootfs pixbuf diagnostic may intentionally allow and record it, but that run cannot be acceptance.
- **`current` remained absent before and after the short-runtime run.**
- **Phase B10 mapped-identity acceptance was not reached.** Survival must pass before exact 125-identity analysis.
- **Atomic activation and rollback remain unimplemented.** They may begin only after B10 passes.
- **Garbage collection remains forbidden.**
- **Archive symlink handling is explicit.** The short-runtime receipt contains an application-created absolute `SingletonSocket` target; analysis must not follow archived symlinks.
- **Evidence archives remain stage-specific.** Each stage defines `out` and `OUT` and ends with `tar czf ~/Downloads/$out.tgz $OUT`.

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
docs/refactor/0099-selected-obsidian-phase-b5-data-provenance-review.md
docs/refactor/0100-selected-obsidian-phase-b6-source-manifest-gap.md
docs/refactor/0101-selected-obsidian-phase-b6-corrected-schema-reproduction-pass.md
docs/refactor/0102-selected-obsidian-phase-b7-complete-cpu-manifest-pass.md
docs/refactor/0103-selected-obsidian-phase-b8-generation-layout-preflight-pass.md
docs/refactor/0104-selected-obsidian-phase-b9-first-run-hardlink-publication-failure.md
docs/refactor/0105-selected-obsidian-phase-b9-generation-directory-publication-failure.md
docs/refactor/0106-selected-obsidian-phase-b9-generation-materialization-pass.md
docs/refactor/0107-selected-obsidian-phase-b10-first-run-launcher-environment-failure.md
docs/refactor/0108-selected-obsidian-phase-b10-second-run-short-lived-main-diagnostic.md
docs/refactor/0109-selected-obsidian-phase-b10-short-runtime-topology-pass-gtk-pixbuf-survival-failure.md
docs/refactor/0091-scoped-graphics-policy-promotion-closure.md
```

## Current focus

### Application-domain/provider architecture

- [x] close retained identity, ownership, selected data provenance, and schema reproduction
- [x] synthesize and materialize the immutable CPU generation
- [x] close B10 launcher-shell loader contamination
- [x] prove short runtime paths form the required CPU topology
- [x] isolate the survival fatal boundary to GTK icon/pixbuf handling
- [ ] run read-only gdk-pixbuf/icon/MIME source and package inventory
- [ ] run a controlled pixbuf runtime diagnostic
- [ ] correct and rematerialize data capability only after evidence
- [ ] pass Phase B10 survival and exact mapped identity
- [ ] implement and test atomic activation and rollback

### Runtime ownership and lifecycle

- [ ] implement one-generation atomic activation and rollback
- [ ] complete world/provider/bridge/toolchain/family ownership split
- [ ] move over-scoped Electron/security policy out of the world baseline
- [ ] define glibc upgrade/recovery lifecycle beyond the 2.42 hold

### Next workload

- [ ] define PyMOL capability contract without runtime mutation
- [ ] defer PyMOL implementation until the reusable generation model is closed
- [ ] use PyMOL as proof of the corrected architecture

## Current stop lines

Do not:

```text
rerun Phase B1-B9 without a source trigger;
rerun B10 blindly without addressing the GTK pixbuf capability;
modify the immutable generation before source/provenance inventory;
copy all rootfs icon or MIME data wholesale;
add broad-farm or rootfs paths to an acceptance run;
create current before B10 passes;
change the promoted launcher;
include Vulkan provider/layer objects in CPU mode;
follow archived SingletonSocket symlinks during extraction;
implement garbage collection;
start PyMOL by extending the broad farm;
use ambiguous evidence archive names.
```

## Evidence policy

Materialization, explicit loader selection, runtime-path viability, GTK data/plugin capability, survival, exact mapped identity, atomic activation, rollback, and promoted equivalence are separate claims. Topology PASS does not imply B10 PASS.

```bash
out=<stage-specific-slug>-$(date +%Y%m%d-%H%M%S)
OUT=<stage output root>/$out
# run stage
tar czf ~/Downloads/$out.tgz $OUT
```
