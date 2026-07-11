# Status

> **State:** selected-Obsidian-closure Phase B10 explicit-generation CPU validation after Phase B9 PASS  
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
- **Phase B9 passed after two implementation diagnostics.** Hard-link object publication was rejected; frozen-root generation rename was also rejected. Both failures were documented rather than hidden.
- **All 96 content objects are present and hash-correct.** The final immutable payload is 70,897,301 bytes in the content-addressed store.
- **The immutable generation is published.** `obsidian-cpu-435ac66d15de2e9a3188` contains 175 aliases plus manifests and receipts.
- **Android generation publication behavior is explicit.** A `0555` same-boundary probe returns `EACCES`; a `0700` probe and generation publication succeed with `renameat2 RENAME_NOREPLACE`; the final root is restored to `0555` and fsynced.
- **Generation validation closed with 1851/1851 PASS rows.** Both staged and final trees passed alias, object, manifest, path-set, and immutable-mode checks.
- **`current` remained absent.** Phase B9 materialized and published candidate bytes but did not activate them, launch a workload, or modify the promoted launcher.
- **Phase B10 uses only the explicit final generation path.** It must not use `current` or the broad farm.
- **The Phase B10 CPU launcher overwrites inherited loader policy with `generation/lib:$PREFIX/glibc/lib`, sets exact `--disable-gpu`, clears Vulkan/Mesa overrides, and isolates XDG, temporary, and fontconfig state under the validation receipt.**
- **The Phase B10 map gate is exact for immutable identities.** It expects 96 selected object-store mappings, 11 app-local mappings, and 18 protected-world mappings—125 identities total.
- **Receipt-local runtime files and non-GPU device mappings are recorded separately.** Any other external path is a failure.
- **Rootfs provider, broad-farm, excluded graphics, GPU process/device, and `current` selection are forbidden.**
- **Atomic activation and rollback remain unimplemented.** They may begin only after Phase B10 passes.
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
docs/refactor/0106-selected-obsidian-phase-b9-generation-materialization-pass.md
docs/refactor/0091-scoped-graphics-policy-promotion-closure.md
```

## Current focus

### Application-domain/provider architecture

- [x] close retained identity/locality
- [x] close static/runtime/data ownership and schema reproduction
- [x] synthesize the complete candidate manifest
- [x] close content/alias/generation-layout preflight
- [x] materialize 96 content objects and publish the immutable generation
- [x] preserve `current` as absent through materialization
- [ ] run Phase B10 explicit-generation CPU topology/survival/maps validation
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
create current before Phase B10 passes;
change the promoted launcher;
run Phase B10 through the broad farm;
include Vulkan provider/layer objects in CPU mode;
mutate the published generation or its content objects;
allow runtime state outside the receipt-owned validation root;
implement garbage collection before current/previous/active references exist;
start PyMOL by extending the broad farm;
use ambiguous evidence archive names.
```

## Evidence policy

Materialization, explicit loader selection, exact mapped identity, process survival, atomic activation, rollback, and promoted equivalence are separate claims. Phase B9 closes the physical generation only; Phase B10 must prove actual use of that generation.

```bash
out=<stage-specific-slug>-$(date +%Y%m%d-%H%M%S)
OUT=<stage output root>/$out
# run stage
tar czf ~/Downloads/$out.tgz $OUT
```
