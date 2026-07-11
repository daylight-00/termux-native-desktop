# Status

> **State:** selected-Obsidian-closure corrected Phase B9 after generation-directory publication failure  
> **Updated:** 2026-07-12

## Working conclusions

- **No PRoot-mediated normal application runtime.** PRoot remains an install/debug-time tool, package/library warehouse, and behavioral oracle.
- **The glibc application world is viable.** Official VS Code and extracted Obsidian run as glibc applications while the desktop remains bionic-native.
- **The core/provider boundary is load-bearing.** App-local `$ORIGIN` remains first; world glibc remains protected; rootfs/prefix location is provenance rather than final ownership.
- **The scoped graphics transaction is closed and trigger-routed.** Turnip and the Mesa Vulkan layer are optional feature/provider capability, not minimum CPU-base members.
- **The broad farm and `modules/gl` remain transitional.** They are compatibility adapters, not final application-domain architecture.
- **Phase B1 passed.** All 136 candidate-relevant paths matched retained identity; the 113-ELF/531-edge graph had no review, collision, missing, unresolved, or ambiguous rows.
- **Phase B2 passed.** The retained graph partitions into 95 entrypoint-static objects, 98 all-app-local static objects, 15 mapped-only objects, and 17 external data objects.
- **Corrected Phase B3 passed.** The mapped-only set reduces to two graphics roots and three required NSS/security roots.
- **Phase B4 passed.** Twenty-eight external direct roots form an 87-object deduplicated static union with 51 shared objects, 111 overlap pairs, and 144 package dependency edges.
- **Corrected Phase B6 closed schema provenance.** The complete source set is 37 files, and native Termux `glib-compile-schemas` 2.88.2 reproduces the retained aggregate byte-for-byte in default and strict modes.
- **Phase B7 passed.** All 161 retained semantic objects have one primary lifecycle disposition; all 113 ELF objects are fully and disjointly accounted.
- **Phase B8 passed read-only.** All 133 materialization inputs still matched; 96 immutable content identities and 175 generation aliases had zero duplicate hashes or alias collisions.
- **The accepted generation ID is deterministic.** `obsidian-cpu-435ac66d15de2e9a3188` derives from the accepted content/build/base contract.
- **The first Phase B9 run failed only at hard-link object publication.** It published no object and no generation.
- **The second Phase B9 run closed content publication.** All 133 source identities matched, strict schema generation was clean, and all 96 content objects—70,897,301 bytes—were published with `renameat2(..., RENAME_NOREPLACE)`.
- **The 96 content-addressed objects are valid reusable state.** They must not be deleted merely because final-generation publication failed.
- **The second B9 failure was isolated to the frozen staged-generation directory rename.** `os.rename()` returned `EACCES` after staged construction, validation, fsync, and owner-read-only freeze.
- **The failure receipt does not isolate the exact Android rule.** Source-root mode, Python/libc syscall path, directory contents, or another filesystem/security rule remain possible until the same-boundary probe runs.
- **The corrected entry point now probes generation publication before touching the real staged generation.** It tests `0555` and, only after `EACCES/EPERM`, `0700` using `renameat2 RENAME_NOREPLACE` across the same staging-to-generations boundary.
- **Frozen-root direct publication remains preferred.** If the device rejects it but accepts a writable root, only the complete staged root is temporarily changed to `0700`; all child nodes remain immutable, publication is no-overwrite, and the final root is restored to `0555` and fsynced before return.
- **No ordinary overwrite-capable rename fallback exists.** Unsupported behavior or any unexpected errno is a hard failure.
- **Phase B9 still must not create or change `current`.** The final generation is not activated merely by publication.
- **The immutable generation must validate all 175 aliases, 96 object hashes, embedded manifest hashes, and non-writable modes before Phase B9 passes.**
- **No workload launch or promoted launcher change occurs in Phase B9.** Explicit-generation loader/workload validation remains the next claim.
- **Atomic activation and rollback remain mandatory but unimplemented.** They may begin only after explicit-generation validation passes.
- **Garbage collection remains forbidden until current, previous-generation, and active-validation references are defined.**
- **The glibc 2.42 hold remains incident containment.** It is not the final lifecycle contract.
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
docs/refactor/0091-scoped-graphics-policy-promotion-closure.md
```

## Current focus

### Application-domain/provider architecture

- [x] close retained identity/locality
- [x] partition static/runtime/data sets
- [x] group dynamic graphics and NSS/security roots
- [x] close static/data ownership and corrected schema reproduction
- [x] pass complete semantic/candidate manifest synthesis
- [x] pass source/content/alias/generation-layout preflight
- [x] publish and verify all 96 content-addressed objects
- [x] diagnose frozen generation-directory publication failure
- [ ] rerun corrected Phase B9 with same-boundary generation publication probe
- [ ] validate the explicit generation before activation
- [ ] implement and test atomic activation and rollback
- [ ] validate promoted candidate equivalence

### Runtime ownership and lifecycle

- [ ] define one-generation atomic activation and rollback implementation
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
rerun closed graphics gates or Phase B1-B8 without a source trigger;
delete the 96 valid content-addressed objects;
retry the corrected entry point at d44de24;
use ordinary overwrite-capable rename;
blindly delete staging or final-generation paths before inventory;
create or replace current during Phase B9;
activate a partial or unvalidated generation;
change the promoted launcher before explicit-generation validation;
make final immutable generations owner-writable;
implement garbage collection before current/previous/active references exist;
start PyMOL by extending the broad farm;
use ambiguous evidence archive names.
```

## Evidence policy

Identity, source-at-copy verification, content publication, generation publication mode, immutable-generation validation, explicit-generation selection, atomic activation, rollback, and workload equivalence are separate claims. The 96 object-store entries may be closed while generation publication remains open.

```bash
out=<stage-specific-slug>-$(date +%Y%m%d-%H%M%S)
OUT=<stage output root>/$out
# run stage
tar czf ~/Downloads/$out.tgz $OUT
```
