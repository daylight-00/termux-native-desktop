# Status

> **State:** corrected selected-Obsidian N3 normalization, source-recipe evidence, and exact binary-artifact comparison PASS; priority provider-authority review is active; successor generation and activation remain blocked  
> **Updated:** 2026-07-12

## Working conclusions

- **The project remains architecturally on track.** The prototype, ownership refactor, ABI recovery, selected D-Bus pilot, scoped graphics closure, and first selected-Obsidian generation each answered valid questions without becoming automatic final architecture.
- **Phase B1-B10 evidence remains valid.** The existing selected generation is immutable and unactivated; `current` is absent and the promoted launcher is unchanged.
- **The selected generation is architecture-discrimination evidence, not yet an approved final provider composition.** Its runtime success does not choose source authority.
- **N2 read-only provider evidence is closed.** It preserved 27,279 current glibc-prefix paths, 86 package identities, 958 prefix ELF objects, 161 selected/reference rows, 20 supplemental rows, and two unowned loader-state paths.
- **Corrected N3 normalization is closed.** The 26,419 raw census rows were reduced to a 1,551-row normalized decision surface without accepting provider authority.
- **Source-recipe evidence is closed.** All 28 priority packages map to historical installed-version recipes. Twenty-seven have one matching recipe tree; `libwayland-glibc 1.23.1` has two historical trees.
- **Exact binary supply identity is established for the 28 priority packages.** Twenty-eight indexed `.deb` artifacts totaling 42,864,296 bytes were verified by repository path, size, SHA-256, Package, Version, and Architecture.
- **Every artifact data member matches the installed filesystem.** All 6,016 regular files, 226 symlinks, and 645 directories match; all 462 ELF members are byte-identical to their live counterparts. There are zero missing paths or content, target, or type mismatches.
- **This closes mutable installed-path supply ambiguity for the 28 priority package identities.** It does not prove that all 28 packages belong in the minimum workstation runtime.
- **`libwayland-glibc` older-tree pressure is strong but not cryptographically closed.** The accepted artifact has uniform 2024-11-13 timestamps shortly after the older recipe commit and before the newer tree existed; absence of direct `libm` NEEDED alone does not prove which tree built it.
- **`glibc 2.42` is the observed installed substrate artifact.** The current source repository HEAD contains glibc 2.43 and is not treated as installed provenance.
- **`glibc-runner` remains unproven runtime authority.** Exact artifact identity does not create a minimum-runtime claim.
- **Package boundaries remain distinct from semantic provider boundaries.** Packages can mix runtime libraries, utilities, headers, data, documentation, and maintenance surfaces.
- **Storage follows subsystem ownership.** Source, cache, unpacked receipts, and scratch state use Termux-private or ignored repository `work/` paths. `$HOME/Downloads` is reserved for final files that must cross the Termux/Android-user handoff boundary.
- **Provider authority is now the immediate layer.** Review must combine normalized semantic responsibility, source recipes and patches, exact binary identity, application-local alternatives, minimum profile, and update ownership.
- **Successor composition remains blocked.** No provider choice, runtime profile, update contract, activation, or rollback scope is accepted merely because exact artifacts are reproducible.

## Architecture authority

```text
main/docs/system-foundation/01-essence.md
main/docs/system-foundation/02-principles-and-invariants.md
main/docs/system-foundation/03-system-model-v2.md
main/docs/system-foundation/05-ideal-target-architecture.md
main/docs/system-foundation/11-architecture-reassessment-and-hard-refactor-decision.md
main/docs/system-foundation/12-document-consistency-audit-and-execution-order.md

docs/refactor/0112-selected-obsidian-passive-map-selection-diagnostic-pass-and-contract-decision.md
docs/refactor/0113-clean-state-minimum-condition-and-supply-authority-audit.md
docs/refactor/0114-debian-baseline-correction-native-font-pressure-and-auditor-boundary.md
docs/refactor/0115-proot-oracle-supply-and-baseline-model.md
docs/refactor/0116-end-to-end-architecture-audit-and-provider-authority-intervention.md
docs/refactor/0117-provider-authority-intervention-adoption-and-execution-order.md
docs/refactor/0118-selected-obsidian-provider-authority-census-schema-and-evidence-plan.md
docs/refactor/0119-selected-obsidian-provider-authority-n2-read-only-evidence-collector.md
docs/refactor/0120-selected-obsidian-provider-authority-n2-device-receipt-review.md
docs/refactor/0122-selected-obsidian-provider-authority-n3-receipt-review-and-normalization-correction.md
docs/refactor/0123-selected-obsidian-provider-authority-corrected-n3-receipt-pass-and-source-comparison-entry.md
docs/refactor/0124-selected-obsidian-provider-authority-source-recipe-evidence-collector.md
docs/refactor/0128-selected-obsidian-provider-authority-source-recipe-receipt-pass.md
docs/refactor/0129-selected-obsidian-provider-authority-bounded-binary-artifact-comparison-collector.md
docs/refactor/0131-selected-obsidian-provider-authority-binary-artifact-receipt-pass.md
docs/refactor/0132-evidence-storage-and-android-downloads-handoff-boundary.md
```

`0116` remains the end-to-end intervention authority. `0123`, `0128`, and `0131` close the normalized, source-recipe, and binary-artifact evidence transactions. They do not close semantic provider authority.

## Accepted receipt identities

### Corrected N3 normalization

```text
archive:
    selected-obsidian-provider-authority-n3-normalized-classification-results-20260712-165805.tgz

SHA-256:
    4dd86c4af956b447ed1829d6b5d604f43d10a17e5b3dcb3ddff3e9b48c377a9c
```

### Source-recipe evidence

```text
archive:
    selected-obsidian-provider-authority-n3-source-recipe-evidence-results-20260712-185001.tgz

SHA-256:
    c8160016267f3ff83b348146240f74f808ffbc93374a6f75988231ef22408cdb
```

### Binary-artifact comparison

```text
archive:
    selected-obsidian-provider-authority-n3-binary-artifact-comparison-results-20260712-194542.tgz

SHA-256:
    da16d49acf54cbc8b6824e3974f08fea9ad0d6daf91687f4666d6c48d0b7567f
```

## Current audit pressure

### P0 — preserve accepted state

Do not mutate:

```text
existing selected generation
current pointer
promoted launcher
dpkg package state
ld.so.conf or ld.so.cache
closed graphics decisions
```

### P1 — priority provider-authority review

For each of the 28 priority package identities, decide at object/capability scope:

```text
semantic responsibility
minimum valid scope
relevant source authority
Termux/Android adaptation necessity
application-local alternative
runtime versus research profile
update owner and trigger
locked artifact identity
remaining discriminating evidence
```

Review order:

```text
world and platform boundary:
    glibc
    termux-exec-glibc
    glibc-runner
    X11/XCB packages

generic shared capabilities:
    compression, identity, XML, FFI, numeric, regex, DRM, Wayland, Kerberos

tool and maintenance pressure:
    e2fsprogs-glibc
    gcc-libs-glibc package split
```

### P2 — separate package and object dispositions

A package-level exact artifact receipt may contain:

```text
runtime ELF providers
tools and executables
headers and static files
data and configuration
documentation
maintenance-only surfaces
```

Do not promote the entire package surface when only a bounded capability is required.

### P3 — runtime and research profiles

Maintain separate declarations for:

```text
minimum workstation runtime profile
research/build/maintenance profile
oracle seed and named scenarios
```

### P4 — update domains

Demand distinct contracts for:

```text
world substrate update
platform integration update
generic provider update
application payload update
toolchain update
oracle scenario update
```

### P5 — successor generation

Lift the block only after:

```text
provider authority decisions are complete enough for the selected set
fonts and pixbuf/icon/MIME capabilities are bounded
locked artifact receipts are incorporated into supply contracts
content/provenance/composition/install/validation identities are separated
activation and rollback scopes are honest
```

## Storage and handoff policy

```text
repository ignored work tree:
    source checkouts
    raw artifacts and caches
    unpacked receipts
    temporary transaction state

$HOME/Downloads:
    final handoff archives and explicitly requested exports only
```

The archive destination does not define the workspace destination.

## Current stop lines

Do not:

```text
materialize or activate a successor before provider-authority review closes
treat every $PREFIX/glibc object as world substrate
treat package or repository membership as semantic authority
treat all 86 installed packages or all 28 priority packages as runtime
promote glibc-runner by availability
merge toolchain or maintenance utilities into the minimum runtime profile
replace valid application-local providers without evidence
reopen closed graphics gates
patch RPATH
mutate loader state
create current
```

## Evidence policy

Prototype validity, oracle validity, package-source provenance, exact binary supply identity, semantic provider authority, runtime composition, interactive capability, update compatibility, activation, rollback, and clean reconstruction are separate claims.
