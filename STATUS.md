# Status

> **State:** selected-Obsidian-closure corrected Phase B10 after launcher-shell loader-path failure  
> **Updated:** 2026-07-12

## Working conclusions

- **No PRoot-mediated normal application runtime.** PRoot remains an install/debug-time tool, package/library warehouse, and behavioral oracle.
- **The glibc application world is viable.** Official VS Code and extracted Obsidian run as glibc applications while the desktop remains bionic-native.
- **The core/provider boundary is load-bearing.** App-local `$ORIGIN` remains first; world glibc remains protected; rootfs/prefix location is provenance rather than final ownership.
- **The scoped graphics transaction is closed and trigger-routed.** Turnip and the Mesa Vulkan layer are optional feature/provider capability, not minimum CPU-base members.
- **Phase B1-B8 are closed.** Identity, closure, capability ownership, data provenance, complete semantic disposition, and physical generation design are explicit.
- **Phase B9 passed.** All 96 content objects—70,897,301 bytes—are hash-correct, the 175-alias immutable generation is published, and 1851/1851 staged/final validation rows passed.
- **The published generation remains unactivated.** `current` was absent before and after Phase B9; the promoted launcher was not changed.
- **The first Phase B10 receipt is a valid launcher diagnostic failure.** The published generation and receipt-local runtime setup were found, but no Obsidian process was executed.
- **The topology timeout was secondary.** `poll-observed.tsv` and `last-processes.tsv` contain no process rows because the launcher failed before the final application `exec`.
- **The exact failure was bionic/glibc loader-policy leakage inside the launcher shell.** Candidate `LD_LIBRARY_PATH=<generation>/lib:$PREFIX/glibc/lib` was exported before a Termux `mkdir`; bionic `mkdir` then attempted to load glibc-world `libc.so` and failed with bad ELF magic.
- **Candidate loader policy must be consumer-scoped.** The corrected launcher unsets inherited `LD_LIBRARY_PATH` and injects the candidate path only in the final `exec env` for Obsidian.
- **No Termux/bionic utility may run under the candidate glibc library path.** Launch-contract files are written while launcher-shell `LD_LIBRARY_PATH` is unset.
- **The corrected launch receipt records `launcher_shell_ld_library_path=UNSET` and `candidate_loader_injection=EXEC_ENV_ONLY`.**
- **The B10 runner now records and compares `current-state-after.tsv` even when capture fails.**
- **Phase B10 still requires an exact CPU validation.** Expected immutable mappings remain 96 selected object-store identities, 11 app-local identities, and 18 protected-world identities.
- **Rootfs provider, broad-farm, excluded graphics, GPU process/device, unexpected external mapping, and `current` selection remain forbidden.**
- **Atomic activation and rollback remain unimplemented.** They may begin only after corrected Phase B10 passes.
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
docs/refactor/0091-scoped-graphics-policy-promotion-closure.md
```

## Current focus

### Application-domain/provider architecture

- [x] close retained identity, ownership, data provenance, and schema reproduction
- [x] synthesize the complete candidate manifest and generation layout
- [x] materialize 96 content objects and publish the immutable generation
- [x] diagnose the first B10 launcher-shell loader-path failure
- [ ] rerun corrected Phase B10 explicit-generation CPU validation
- [ ] implement and test atomic activation and rollback
- [ ] validate the activated candidate and promotion equivalence

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
export candidate LD_LIBRARY_PATH in a bionic launcher shell;
run Termux utilities under the candidate glibc loader path;
create current before corrected Phase B10 passes;
change the promoted launcher;
mutate the published generation or content objects;
include Vulkan provider/layer objects in CPU mode;
implement garbage collection;
start PyMOL by extending the broad farm;
use ambiguous evidence archive names.
```

## Evidence policy

Materialization, explicit loader selection, exact mapped identity, process survival, atomic activation, rollback, and promoted equivalence are separate claims. A topology timeout caused before application `exec` is a launcher failure, not a workload compatibility result.

```bash
out=<stage-specific-slug>-$(date +%Y%m%d-%H%M%S)
OUT=<stage output root>/$out
# run stage
tar czf ~/Downloads/$out.tgz $OUT
```
