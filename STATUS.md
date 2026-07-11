# Status

> **State:** selected-Obsidian-closure Phase B8 generation-layout preflight after Phase B7 PASS  
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
- **Corrected Phase B6 closed schema provenance.** The complete source set is 37 files, and native Termux `glib-compile-schemas` 2.88.2 reproduces the retained aggregate byte-for-byte in default and strict modes.
- **Phase B7 passed read-only.** All 161 retained semantic objects have exactly one primary lifecycle disposition; all 113 ELF objects are fully and disjointly accounted.
- **The minimum CPU immutable payload is explicit.** Materialize 87 external static ELF objects, 4 required NSS/security dynamic objects, and 4 selected font files; generate one GSettings aggregate.
- **The minimum CPU base explicitly excludes 11 Vulkan feature objects.** Five app-local ELF, six world ELF, six app-local data paths, twelve world locale files, nineteen mutable-state paths, five cache paths, and one optional GPU device remain outside immutable selected content.
- **The selected ELF manifest has 91 unique source paths and zero lookup-name collisions.** The 95 copied source objects—91 ELF plus 4 fonts—also have 95 unique hashes.
- **Candidate materialization has not started.** Phase B7 does not prove source identity at copy time, a collision-free combined alias namespace, physical object-store safety, activation, rollback, loader selection, or workload behavior.
- **Phase B8 is read-only.** It rechecks 91 ELF, 4 fonts, 37 schema sources, and the schema compiler; designs content-addressed object identities and generation-local aliases; derives a generation ID; and records activation/rollback contracts.
- **The intended physical model is one content-addressed store plus immutable generation manifests and aliases.** Candidate validation must use an explicit generation path before any `current` pointer change.
- **Atomic activation remains mandatory.** Staging, final generations, and the temporary/current symlink replacement must live under one generation base and one filesystem.
- **Garbage collection remains forbidden until current, previous-generation, and active validation references are defined.**
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
docs/refactor/0091-scoped-graphics-policy-promotion-closure.md
```

## Current focus

### Application-domain/provider architecture

- [x] close retained identity/locality
- [x] partition static/runtime/data sets
- [x] group dynamic graphics and NSS/security roots
- [x] choose typed manifests over one deduplicated static generation
- [x] close locale, selected-font, and schema source/compiler ownership
- [x] pass Phase B7 complete semantic disposition and CPU manifest synthesis
- [ ] run Phase B8 source/alias/generation-layout preflight
- [ ] implement a staging-only materializer and immutable-generation validator
- [ ] validate the explicit candidate generation before activation
- [ ] implement atomic activation and rollback

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
rerun closed graphics gates or Phase B1-B7 without a source trigger;
copy selected bytes directly into a live farm;
activate a partial or unvalidated multi-file generation;
use source basenames, SONAMEs, or lookup names without combined alias analysis;
copy app-local/world ELF, glibc locale, or Vulkan feature roots into the CPU generation;
expand selected fonts by package or directory inertia;
change the promoted launcher before explicit-generation validation;
implement garbage collection before current/previous/active references exist;
start PyMOL by extending the broad farm;
use ambiguous evidence archive names.
```

## Evidence policy

Identity, complete source closure, semantic disposition, content identity, alias namespace, physical materialization, explicit-generation selection, atomic activation, rollback, and workload equivalence are separate claims. Typed capabilities may overlap, but immutable content and activation transitions must remain receipt-owned and complete.

```bash
out=<stage-specific-slug>-$(date +%Y%m%d-%H%M%S)
OUT=<stage output root>/$out
# run stage
tar czf ~/Downloads/$out.tgz $OUT
```
