# Status

> **State:** selected-Obsidian-closure Phase B7 complete CPU manifest after corrected Phase B6 PASS  
> **Updated:** 2026-07-11

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
- **Static ownership is manifest-based.** The target is typed semantic manifests over one deduplicated application-domain generation—not one tree per root and not one untyped blob.
- **The minimum CPU ELF direction is explicit.** Include 87 external static objects plus 4 NSS/security dynamic objects; leave app-local and world ELF in place; exclude 11 graphics-feature dynamic objects; retain static GBM.
- **Phase B5 closed identity and ownership for locale and selected fonts.** All 17 retained external data bytes are stable.
- **The first Phase B6 remains diagnostic only.** Its incomplete 36-file source set caused ten ignored schema files and did not isolate compiler-version behavior.
- **Corrected Phase B6 passed.** Complete source closure is 37 files; the missing file was `org.gnome.desktop.enums.xml`, owned by `gsettings-desktop-schemas`.
- **Schema provenance is closed.** All 37 sources match, no enum/flags reference is undefined, and native Termux `glib-compile-schemas` 2.88.2 reproduces the retained aggregate byte-for-byte in both default and strict modes.
- **All data ownership directions are now closed for manifest synthesis.** Locale references protected world data; four fonts are selected materialized files; GSettings is generated from a 37-source/compiler contract.
- **Phase B7 is read-only.** It accounts for all 161 retained semantic objects with exactly one primary disposition and emits the complete minimum CPU candidate manifest inputs.
- **Expected immutable selected payload is explicit.** Ninety-one ELF objects are materialization candidates: 87 static plus 4 required NSS dynamic objects. Four fonts are materialized and one schema aggregate is generated.
- **App-local, world, state, caches, graphics feature, and device objects stay outside the immutable CPU generation according to explicit dispositions.**
- **No candidate bytes have been materialized.** Phase B7 does not choose the object-store layout, loader search path, activation pointer, or rollback implementation.
- **Atomic activation remains mandatory before promotion.** Its unit is one complete receipt-owned application-domain generation.
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
docs/refactor/0091-scoped-graphics-policy-promotion-closure.md
```

## Current focus

### Application-domain/provider architecture

- [x] close retained identity/locality
- [x] partition static/runtime/data sets
- [x] group dynamic graphics and NSS/security roots
- [x] choose typed manifests over one deduplicated static generation
- [x] close locale and selected-font ownership
- [x] close complete schema source/compiler lineage
- [ ] run Phase B7 complete semantic disposition and CPU manifest synthesis
- [ ] design immutable object-store layout and atomic activation
- [ ] materialize and validate the selected CPU candidate

### Runtime ownership and lifecycle

- [ ] define one-generation atomic activation and rollback
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
rerun closed graphics gates or Phase B1-B6 without a source trigger;
accept the first incomplete-source B6 aggregate;
copy opaque rootfs gschemas.compiled instead of the source/compiler contract;
copy glibc locale into the application generation;
expand the selected font set by package or directory inertia;
make one provider tree per direct root or one untyped candidate blob;
copy app-local/world ELF or include Vulkan provider roots in the CPU base;
materialize candidate bytes before Phase B7 is interpreted;
implement activation before object-store and rollback semantics are documented;
start PyMOL by expanding the broad farm;
use ambiguous evidence archive names.
```

## Evidence policy

Identity, complete source closure, compiler cleanliness, semantic disposition, manifest membership, materialization, actual selection, activation, and workload equivalence are separate claims. Typed capabilities may share physical objects, but every retained semantic object must have exactly one primary lifecycle disposition.

```bash
out=<stage-specific-slug>-$(date +%Y%m%d-%H%M%S)
OUT=<stage output root>/$out
# run stage
tar czf ~/Downloads/$out.tgz $OUT
```
