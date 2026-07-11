# Status

> **State:** selected-Obsidian-closure Phase B6 schema reproduction after Phase B5 PASS/REVIEW  
> **Updated:** 2026-07-11

## Working conclusions

- **No PRoot-mediated normal application runtime.** PRoot remains an install/debug-time tool, package/library warehouse, and behavioral oracle.
- **The glibc application world is viable.** Official VS Code and extracted Obsidian run as glibc applications while the desktop remains bionic-native.
- **The core/provider boundary is load-bearing.** App-local `$ORIGIN` remains first; world glibc remains protected; rootfs/prefix location is provenance rather than final ownership.
- **The scoped graphics transaction is closed and trigger-routed.** Turnip and the Mesa Vulkan layer are feature/provider capabilities, not minimum CPU-candidate members.
- **The broad farm and `modules/gl` remain transitional.** They are compatibility adapters, not final application-domain architecture.
- **Phase B1 passed.** All 136 candidate-relevant paths matched retained identity; the 113-ELF/531-edge graph had no review, collision, missing, unresolved, or ambiguous rows.
- **Phase B2 passed.** The retained graph partitions into 95 entrypoint-static objects, 98 all-app-local static objects, 15 mapped-only objects, and 17 data objects.
- **Corrected Phase B3 passed.** The mapped-only set reduces to two graphics roots and three required NSS/security roots.
- **Phase B4 passed.** Twenty-eight external direct roots form an 87-object deduplicated static union with 51 shared objects, 111 overlap pairs, and 144 package dependency edges.
- **Static ownership is manifest-based.** The target is typed semantic manifests over one deduplicated application-domain generation—not one tree per root and not one untyped blob.
- **The minimum CPU ELF direction is explicit.** Include the 87 external static objects plus NSS/security dynamic modules/support; leave app-local and world ELF in place; exclude Vulkan-provider dynamic roots; retain static GBM.
- **Phase B5 completed as `PASS + REVIEW_DATA_PROVENANCE_GAPS`.** This is a valid audit, not a script failure.
- **All 17 data bytes are stable.** Identity mismatches and missing paths are zero.
- **Locale ownership is closed.** Twelve glibc 2.42 locale files remain `WORLD_LOCALE_GLIBC` and are referenced from the protected prefix rather than copied.
- **Font ownership is closed.** All four selected font files match exact package ownership and become `SELECTED_FONT_DATA` with path/version/hash provenance.
- **Schema source ownership is closed.** The aggregate has 36 owned inputs: 32 from `gsettings-desktop-schemas` and 4 from `libgtk-3-common`; no source is unowned.
- **Only schema compiler lineage remains open.** The retained rootfs has no `/usr/bin/glib-compile-schemas`, so source-to-aggregate reproducibility is not yet proven.
- **Phase B6 is read-only.** It discovers explicit compiler candidates, records identity/version/package provenance, recompiles only in receipt-local directories, and compares generated aggregate SHA-256 with the retained byte.
- **No fresh Obsidian run or graphics rerun is required.** Candidate bytes remain unmaterialized.
- **Atomic activation remains mandatory before promotion.** Its object is the completed receipt-owned generation, but implementation waits for the complete data/candidate manifest.
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
docs/refactor/0091-scoped-graphics-policy-promotion-closure.md
```

## Current focus

### Application-domain/provider architecture

- [x] close retained identity/locality
- [x] partition static/runtime/data sets
- [x] group dynamic graphics and NSS/security roots
- [x] choose typed manifests over one deduplicated static generation
- [x] close locale, font, and schema-source ownership
- [ ] run Phase B6 GSettings compiler reproduction
- [ ] close schema aggregate compiler lineage
- [ ] emit the complete selected CPU candidate manifest
- [ ] materialize and validate the selected CPU candidate

### Runtime ownership and lifecycle

- [ ] define atomic activation for the complete generation manifest
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
rerun closed graphics gates or Phase B1-B5 without a source trigger;
install a rootfs schema compiler merely to make the audit pass;
copy the opaque rootfs gschemas.compiled without compiler/source provenance;
copy glibc locale data into the application generation;
expand the selected font set by package or directory inertia;
make one provider tree per direct root or one untyped candidate blob;
copy app-local/world ELF or include Vulkan provider roots in the CPU base;
materialize candidate bytes before schema reproduction is interpreted;
implement activation before the complete generation manifest;
start PyMOL by expanding the broad farm;
use ambiguous evidence archive names.
```

## Evidence policy

Identity, ownership, source provenance, compiler reproducibility, manifest membership, materialization, actual selection, and workload equivalence are separate claims. A generated data aggregate is reproducible only for a recorded source set and compiler identity.

```bash
out=<stage-specific-slug>-$(date +%Y%m%d-%H%M%S)
OUT=<stage output root>/$out
# run stage
tar czf ~/Downloads/$out.tgz $OUT
```
