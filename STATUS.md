# Status

> **State:** selected-Obsidian-closure passive B10 rerun after interaction-trigger correction and pixbuf inventory PASS  
> **Updated:** 2026-07-12

## Working conclusions

- **No PRoot-mediated normal application runtime.** PRoot remains an install/debug-time tool, package/library warehouse, and behavioral oracle.
- **Phase B1-B8 are closed.** Identity, static closure, selected data provenance, semantic disposition, and generation design are explicit.
- **Phase B9 passed.** Ninety-six content objects totaling 70,897,301 bytes are hash-correct; the 175-alias immutable generation is published; staged/final validation is 1851/1851 PASS; `current` remains absent.
- **The B10 launcher-shell contamination is closed.** Candidate `LD_LIBRARY_PATH` is injected only in the final Obsidian exec.
- **Short runtime/socket paths form the required CPU topology.** Main, renderer, zygote, and utility processes appeared with zero GPU process; `SingletonSocket` and `SingletonCookie` were created.
- **The preceding GTK failure was interaction-triggered.** The initial Obsidian window was visible and usable enough to present the vault controls; the operator clicked the vault-open control before the fatal GTK chain.
- **The prior receipt is not a clean passive-survival failure.** It proves the interactive vault-open/file-chooser path fails, not that the idle initial window spontaneously aborts.
- **Passive and interactive claims are separate.** Passive B10 requires 100 seconds with no GUI input plus maps; interactive acceptance requires opening a vault without GTK/pixbuf failure.
- **The GTK pixbuf/icon/MIME inventory passed.** One loader cache references twelve modules; all written `/usr/...` module paths are absent in the native namespace, while all twelve rootfs-prefixed modules exist.
- **Twenty runtime capability paths were absent from the B9 semantic manifest.** One loader cache, twelve loader modules, two icon-theme indexes, and five MIME database files are uncovered.
- **All twenty are not automatically final-generation members.** The minimum required subset remains unresolved.
- **The rootfs loader cache cannot be used unchanged.** A controlled native diagnostic must relocate its module paths into a receipt-local cache.
- **The next action is a passive no-input B10 rerun.** The operator must observe only and must not click Open vault, Create vault, or any other control.
- **After passive B10, the vault-open capability gets a separate controlled diagnostic.** Rootfs module references in that run are diagnostic-only and cannot count as acceptance.
- **`current` remains absent and the promoted launcher is unchanged.**
- **Atomic activation, rollback, and garbage collection remain forbidden until both passive and interactive runtime claims close.**

## Architecture authority

```text
docs/refactor/0106-selected-obsidian-phase-b9-generation-materialization-pass.md
docs/refactor/0107-selected-obsidian-phase-b10-first-run-launcher-environment-failure.md
docs/refactor/0108-selected-obsidian-phase-b10-second-run-short-lived-main-diagnostic.md
docs/refactor/0109-selected-obsidian-phase-b10-short-runtime-topology-pass-gtk-pixbuf-survival-failure.md
docs/refactor/0110-selected-obsidian-pixbuf-inventory-pass-and-interaction-boundary-correction.md
```

## Current focus

### Application-domain/provider architecture

- [x] materialize and publish the immutable CPU generation
- [x] close launcher-shell loader contamination
- [x] prove short runtime paths form CPU topology
- [x] identify vault-open GTK icon/pixbuf failure
- [x] inventory loader cache/modules, icon indexes, and MIME files
- [x] correct passive-versus-interactive evidence boundary
- [ ] run passive no-input B10 for 100-second survival and exact maps
- [ ] run controlled vault-open pixbuf diagnostic
- [ ] define and rematerialize the minimum data/plugin capability
- [ ] pass interactive vault-open acceptance
- [ ] implement atomic activation and rollback

## Current stop lines

Do not:

```text
rerun Phase B1-B9 without a source trigger;
interact with the GUI during the passive B10 run;
describe the prior failure as spontaneous idle abort;
mutate the existing immutable generation;
copy all twenty inventory paths wholesale;
use rootfs loaders.cache unchanged;
add rootfs or the broad farm to an acceptance run;
create current;
change the promoted launcher;
implement garbage collection.
```

## Evidence policy

Operator interaction is an explicit evidence class. Machine capture proves process and error timing; it does not prove when a human clicked. Passive survival, interactive file chooser capability, mapped identity, activation, and rollback are separate claims.

```bash
out=<stage-specific-slug>-$(date +%Y%m%d-%H%M%S)
OUT=<stage output root>/$out
# run stage
tar czf ~/Downloads/$out.tgz $OUT
```
