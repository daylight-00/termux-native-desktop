# Repository Refactor and Architecture Work Log

This directory is the transaction-level source of truth for migration from the original prototype toward explicit ownership, semantic provider authority, locked supply identity, clean runtime composition, controlled materialization, and activation.

## Working rule

```text
session narrative != authority
repository evidence + current canonical index = authority
```

Historical numbered records remain intact when later audits narrow or supersede their interpretation.

## Current checkout

```text
checkout:
    $HOME/projects/termux-native-desktop

active architecture branch:
    docs/post-graphics-architecture-audit
```

The historical `$HOME/termux-native-desktop` path is evidence only.

## Authority and precedence

Foundation on `main`:

```text
docs/system-foundation/01-essence.md
docs/system-foundation/02-principles-and-invariants.md
docs/system-foundation/03-system-model-v2.md
docs/system-foundation/05-ideal-target-architecture.md
docs/system-foundation/11-architecture-reassessment-and-hard-refactor-decision.md
docs/system-foundation/12-document-consistency-audit-and-execution-order.md
```

Current branch-local chain:

```text
0112 selected passive runtime/map facts
0115 PRoot oracle, supply and baseline lifecycle
0116 controlling provider-authority intervention
0117 intervention execution order
0118-0120 N1/N2 census and read-only receipt
0123 corrected N3 normalization acceptance
0128 source-recipe receipt acceptance
0131 exact binary-artifact receipt acceptance
0132 Termux-private work versus Downloads handoff boundary
0133 bounded priority provider review
0134 exact non-materializing member-lock draft
0135 post-0134 architecture audit and corrections
0136 provider-authority coverage and lock-semantics normalization
0137 world internals, locale and loader lifecycle boundary
0138 application payload, launcher and supplement authority boundary
0139 non-priority generic source-authority boundary
0140 non-priority generic exact-candidate evidence collector
0141 non-priority generic exact-candidate receipt review
0142 non-priority generic artifact/member comparison set
0143 non-priority generic artifact member-inventory collector
0144 non-priority generic artifact member-inventory receipt review
0145 bounded generic recipe binding and drift-target ELF review
0146 generic recipe-binding and drift-target ELF receipt review
0147 generic build-attestation and adaptation review set
```

Precedence:

```text
system-foundation
    -> constitutional intent and invariants

0116
    -> controlling provider-authority intervention

0115 and 0112
    -> oracle/supply lifecycle and accepted bounded runtime facts

0117-0134
    -> evidence transactions and bounded historical decisions

0135
    -> audit correction requirements

0136
    -> current normalized coverage/registry/alias/schema state

0137
    -> current world-internal demand, locale and loader lifecycle boundary

0138
    -> current application identity, launcher supply and release lifecycle boundary

0139
    -> current non-priority generic capability/source-class boundary

0140
    -> canonical 61-row exact-candidate search contract and read-only retained-evidence collector

0141
    -> exact retained receipt review into direct-family, indirect-only and absent classes

0142
    -> exact 34-artifact/44-edge named member-inventory comparison set and explicit static/development exclusions

0143
    -> bounded exact-artifact acquisition and stream-only control/data member-inventory collector implementation

0144
    -> exact device receipt review into exact-member, expected-alias drift and expected-alias-absent classes
```

## Current state

```text
repository ownership migration:
    DEPLOYED / RETAINED

ABI incident recovery:
    CLOSED FOR TESTED WORKLOAD

selected D-Bus pilot:
    PASS

scoped graphics-policy transaction:
    CLOSED

first immutable selected generation:
    PUBLISHED / UNACTIVATED

passive startup/topology/survival/maps:
    PASS

priority provider evidence:
    PASS / BOUNDED

exact artifact/member supply:
    STRONG PASS

package-wide runtime inference:
    REJECTED

global identity coverage normalization:
    PASS

canonical supply/object/fragment registries:
    PASS

artifact alias classification:
    PASS

world/locale/loader lifecycle boundary:
    PASS / CLEAN RECONSTRUCTION OPEN

application payload/launcher/supplement boundary:
    PASS / EXACT PAYLOAD AND SUPPLEMENT MEMBERSHIP OPEN

non-priority generic source-class boundary:
    PASS / EXACT OBJECT/SOURCE BINDING OPEN

generic exact-candidate collector:
    READY / DEVICE RECEIPT REVIEWED

generic exact-candidate receipt review:
    PASS / 37 DIRECT FAMILY, 13 INDIRECT ONLY, 11 ABSENT

generic artifact/member comparison set:
    DEFINED / 34 EXACT ARTIFACTS, 44 NAMED EDGES, 15 STATIC/DEV EXCLUSIONS

generic artifact member-inventory collector:
    PASS / 34 EXACT ARTIFACTS VERIFIED, STREAM INVENTORY, NO INSTALL OR FILESYSTEM MATERIALIZATION

generic artifact member-inventory receipt review:
    PASS / 21 EXACT MEMBER+SONAME, 15 EXPECTED-ALIAS DRIFT, 1 EXPECTED-ALIAS ABSENT

generic recipe binding and drift-target ELF receipt review:
    PASS / 37 LINEAGE CANDIDATES, 21 EXACT OBJECT CANDIDATES, 15 SONAME-CONFIRMED DRIFT TARGETS, 1 UNSATISFIED ALIAS; ZERO AUTHORITY ACCEPTANCE

semantic final-provider authority:
    OPEN

application runtime composition:
    NOT REACHED

target-layout schema:
    PASS / SCHEMA ONLY

target-layout population:
    BLOCKED

extraction/materializer:
    BLOCKED

successor materialization:
    BLOCKED

current activation:
    BLOCKED

clean reconstruction:
    NOT PROVEN
```

## Evidence cardinality

```text
semantic-object denominator:
    161

ELF semantic objects:
    113

first-generation content identities:
    96 = 91 selected external ELF + 4 fonts + 1 generated schema

application-local references:
    11

protected-world references:
    18

priority package dispositions:
    28 / 28

bounded priority reviewed objects:
    59 / 59

exact artifacts:
    28

artifact data members compared:
    6,887

member mismatches:
    0

canonical provider objects:
    60 = 59 reviewed + 1 optional exec

reviewed fragment memberships:
    63

optional fragment memberships:
    1

canonical artifact aliases:
    84

legacy fragment alias edges:
    92

legacy lock rows:
    156

non-priority generic provider identities:
    61

target schema fields:
    20

populated target rows:
    0
```

These counts are not interchangeable. The 59-object review is a bounded subset of the 161-row denominator. The 96 first-generation contents are not application-local payload.

## Normalized work products

```text
experiments/glibc/selected-obsidian-provider-authority/review/
    authority-coverage-ledger.tsv
    authority-coverage-ledger/*.tsv
    non-priority-generic-authority-ledger.tsv
    non-priority-generic-authority-ledger/*.tsv
    normalization-codebook.tsv
    world-lifecycle-authority-boundary.tsv
    application-authority-boundary.tsv
    generic-source-authority-boundary.tsv
    unresolved-authority-ledger.tsv

experiments/glibc/selected-obsidian-provider-authority/profiles/
    supply-repository-metadata-registry.tsv
    supply-artifact-registry.tsv
    provider-object-registry.tsv
    provider-object-registry/*.tsv
    provider-fragment-registry.tsv
    provider-fragment-memberships.tsv
    runtime-alias-authority.tsv
    runtime-alias-authority/*.tsv
    target-layout-schema.tsv
    target-layout-invariants.md
```

Large registries use root indexes plus SHA-256-locked partitions. Historical `provider-profile-*` and `member-locks/*.tsv` files remain bounded supply evidence, not materializer input.

## Current semantic corrections

```text
exact Termux artifact supply
    != automatic final generic/platform authority

Termux repository build
    != automatic Termux/Android adaptation

artifact-to-live byte equivalence
    != artifact-to-recipe build binding

fragment membership
    != application composition inclusion

package-provided alias
    != runtime-required alias

artifact mode/path/uid/gid
    != target policy

schema definition
    != target population
```

Specific decisions:

```text
glibc reviewed world set:
    current Termux/Android-adapted world authority; six reviewed core objects are bounded, internals are demand-gated and clean reconstruction remains open

locale and loader state:
    twelve glibc-coupled locale members are referenced world data; ld.so.conf is composition-derived policy input; ld.so.cache is derived mutable state

libxcb:
    explicit socket-prefix adaptation proven; final platform source provisional

libxshmfence:
    explicit Termux shm-directory policy proven; final provider provisional

other reviewed X11 objects:
    generic Termux supply; platform-versus-generic provisional

libcap.so.2:
    platform-or-generic provisional; exact supply accepted

libxcb-render.so.0 and libxcb-shm.so.0:
    remain base-fragment pressure due passive mapped/direct consumers

glibc-runner:
    research/build/maintenance only

termux-exec-glibc:
    optional; minimum-runtime necessity unproven

non-priority generic source classes:
    60 Debian-rootfs oracle identities + 1 local graphics-experiment identity; oracle/reference only, exact candidate artifacts and source bindings open

generic exact-candidate evidence:
    bounded receipt reviewed: 37 direct apt+recipe family candidates, 13 indirect-only rows, 11 retained gaps; all remain candidate-only

generic artifact/member comparison set:
    34 exact indexed artifacts, 44 named member-search edges, 15 explicit static/development exclusions; no download or extraction performed

generic artifact member-inventory collector:
    34 exact artifacts verified and inventoried without install or filesystem extraction

generic artifact member-inventory receipt review:
    21 exact concrete member+expected SONAME observations, 15 expected SONAME aliases with different concrete targets, and 1 absent expected alias; no authority acceptance or target population

generic recipe binding and drift-target ELF collector:
    37 pinned family/version/tree recipe candidates across 28 roots; all 34 cached artifacts and 15 target ELFs verified read-only

generic recipe binding and drift-target ELF receipt review:
    37 lineage candidates confirmed; 20 material-delta, 8 configuration/packaging-delta and 9 no-explicit-token semantic-review rows; 15 concrete filename drifts remain unaccepted and libjpeg.so.62 remains unsatisfied

generic build-attestation and adaptation review set:
    16 evidence requirements, 28 root work units and 37 object work units defined; 36 objects are collection-eligible, libjpeg.so.62 is correction-blocked, and all acceptance remains zero

generic build-attestation and adaptation evidence collector:
    read-only foundation revalidation plus local recipe/file/signal, root-object and artifact/member evidence collection implemented; external provenance, semantic/policy review and every acceptance remain open
```

## Living authority issues

```text
AUTH-001 world clean reconstruction, acquisition, named internals and successor validation
AUTH-002 optional Termux exec necessity
AUTH-003 GTK/GLib/font/device/Wayland provider composition
AUTH-004 printing capability/provider
AUTH-005 graphics/X11/XCB provider composition
AUTH-006 libwayland artifact-to-recipe binding
AUTH-007 supply/alias/target population contract
AUTH-008 remaining data capabilities; locale/loader lifecycle bounded
AUTH-009 non-priority generic capabilities; bounded evidence collector implemented for the 16-requirement 28-root/37-object review set; production receipt review, external provenance, semantic/policy evidence, libjpeg.so.62 correction and all final bindings open
AUTH-010 exact application payload supply, named supplements and release execution; launcher source boundary bounded
```

## Current next state

```text
CLOSE_GLOBAL_WORLD_APPLICATION_GENERIC_AND_DATA_AUTHORITY_GAPS
```

Active task:

```text
RUN_BOUNDED_GENERIC_BUILD_ATTESTATION_AND_ADAPTATION_EVIDENCE_COLLECTOR
```

Required order:

```text
1. world internals, locale and loader-state lifecycle boundary: PASS / remaining evidence explicit;
2. application identity/launcher lifecycle boundary: PASS / exact payload supply and named supplement membership OPEN;
3. non-priority generic capability/source-class boundary: PASS / build-attestation/adaptation review set DEFINED as 16 requirements, 28 roots and 37 objects; bounded read-only evidence collector IMPLEMENTED and production receipt NEXT;
4. decide conditional graphics, GTK/Wayland, printing and optional-exec policy only after owning candidate sets are explicit;
5. close fonts, pixbuf/icon/MIME and generated-schema authority;
6. define ApplicationRuntimeComposition only after owning authorities are accepted;
7. populate target rows only after composition acceptance;
8. perform intervention-lift audit before extraction/materializer implementation.
```

## Stop line

Do not:

```text
treat 59/59 as global completion;
call first-generation contents application-local payload;
consume provider fragments or historical lock files as deployable profiles;
treat exact Termux supply as final provider authority;
copy artifact aliases, paths or modes into a runtime target;
populate target rows;
write extraction/materializer code;
install/remove/upgrade/downgrade packages;
run maintainer scripts;
materialize or activate a successor;
create or change current;
mutate launcher, loader state or RPATH;
reopen closed graphics gates.
```
