# Status

> **State:** selected-Obsidian-closure Phase B10 short-runtime-path discriminator after two diagnostic failures  
> **Updated:** 2026-07-12

## Working conclusions

- **No PRoot-mediated normal application runtime.** PRoot remains an install/debug-time tool, package/library warehouse, and behavioral oracle.
- **The glibc application world is viable.** Official VS Code and extracted Obsidian run as glibc applications while the desktop remains bionic-native.
- **The core/provider boundary is load-bearing.** App-local `$ORIGIN` remains first; protected world glibc remains separate; rootfs/prefix location is provenance rather than final ownership.
- **Phase B1-B8 are closed.** Identity, closure, capability ownership, data provenance, semantic disposition, and physical generation design are explicit.
- **Phase B9 passed.** Ninety-six content objects totaling 70,897,301 bytes are hash-correct; the 175-alias immutable generation is published; staged/final validation is 1851/1851 PASS; `current` remains absent.
- **The first B10 failure was launcher-shell loader contamination.** Candidate `LD_LIBRARY_PATH` reached a bionic `mkdir`; the launcher was corrected to inject the generation path only in the final Obsidian `exec env`.
- **The second B10 run verifies that correction.** Launch receipt records `launcher_shell_ld_library_path=UNSET` and `candidate_loader_injection=EXEC_ENV_ONLY`; the explicit Obsidian main process was observed.
- **The second B10 main was short-lived.** One main row was observed, then no stable main/renderer/zygote process remained; maps capture was not reached.
- **No fatal loader or missing-library message was emitted.** Stderr contains only inotify sysctl access and missing system-D-Bus warnings.
- **The strongest remaining discriminator is runtime/socket path length.** The failed run used 170-179 character XDG/TMP paths, created `SingletonLock` and one Chromium scoped temp directory, but no `SingletonSocket`, renderer, or zygote.
- **Path length is not yet a closed root cause.** The next run changes only the receipt-owned runtime path length; generation contents, loader order, CPU flags, schema, fonts, and `current` boundary remain unchanged.
- **The corrected B10 runner allocates `$PREFIX/tmp/o10.XXXXXXXX`.** It requires `TMPDIR` length <= 64, snapshots the short live runtime tree byte-for-byte into `$OUT/runtime-evidence`, verifies the copy with `diff -qr`, then removes the live root.
- **The capture exit-code receipt bug is fixed.** The previous `if ! command; capture_rc=$?` recorded the negation status; the runner now preserves the real capture return code.
- **`current` remained absent before and after the second B10 run.**
- **Phase B10 still requires exact CPU topology, survival, and mapped identity.** Expected immutable mappings remain 96 selected object-store identities, 11 app-local identities, and 18 protected-world identities.
- **Broad-farm, rootfs-provider, excluded-graphics, GPU-process/device, unexpected external mapping, and `current` selection remain forbidden.**
- **Atomic activation and rollback remain unimplemented.** They may begin only after B10 passes.
- **Garbage collection remains forbidden.**
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
docs/refactor/0091-scoped-graphics-policy-promotion-closure.md
```

## Current focus

### Application-domain/provider architecture

- [x] close retained identity, ownership, data provenance, and schema reproduction
- [x] synthesize the complete candidate manifest and generation layout
- [x] materialize and publish the immutable CPU generation
- [x] diagnose B10 launcher-shell loader contamination
- [x] diagnose B10 short-lived main under long runtime paths
- [ ] rerun B10 with short receipt-owned runtime/socket paths
- [ ] implement and test atomic activation and rollback
- [ ] validate activated-candidate equivalence

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
rerun Phase B1-B9 without a source or validation trigger;
change generation content or loader order during the short-path discriminator;
export candidate LD_LIBRARY_PATH in a bionic launcher shell;
create current before B10 passes;
change the promoted launcher;
include Vulkan provider/layer objects in CPU mode;
interpret inotify or missing system-D-Bus warnings as the fatal cause;
implement garbage collection;
start PyMOL by extending the broad farm;
use ambiguous evidence archive names.
```

## Evidence policy

Materialization, explicit loader selection, runtime-path viability, exact mapped identity, process survival, atomic activation, rollback, and promoted equivalence are separate claims. The short-path run is a single-variable discriminator, not a new generation build.

```bash
out=<stage-specific-slug>-$(date +%Y%m%d-%H%M%S)
OUT=<stage output root>/$out
# run stage
tar czf ~/Downloads/$out.tgz $OUT
```
