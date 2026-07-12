# 0114 — Debian Baseline Correction, Native-Font Pressure, and Auditor Boundary

## Status

This record corrects the clean-state assumptions in `0113` and narrows the role of this audit stream.

```text
record type:
    CORRECTION / AUDIT PRESSURE

runtime launch:
    NO

package install/remove:
    NO

generation mutation:
    NO

implementation authorization:
    NO
```

## Corrected Debian baseline

The accepted pre-problem Debian state was not a debootstrap/minbase rootfs.

It was:

```text
base:
    debian:trixie-slim

initial maintenance:
    apt upgrade

initial intentional application addition:
    VS Code only
```

The user accepts this state as the clean reference baseline for the present audit.

Therefore the relevant comparison is not:

```text
unknown minbase
    vs
current rootfs
```

It is:

```text
debian:trixie-slim
+ initial apt upgrade
+ VS Code installation and its required dependencies

    vs

later rootfs additions made while attempting to solve the VS Code terminal-font problem
```

The earlier `0113` statements that treated the original base as an unknown minbase are superseded by this record.

## Actual problem boundary

The objection does not apply to:

```text
trixie-slim itself
initial apt upgrade
VS Code installation
VS Code-required dependency closure
```

The suspect boundary begins later, when the VS Code integrated-terminal font issue was mitigated through:

```text
Debian/PRoot font installation
and other rootfs package additions associated with that workaround
```

The exact later package delta remains evidence to be reconstructed, but its architectural status is already under pressure:

```text
accepted baseline:
    trixie-slim + upgrade + VS Code

suspect workaround delta:
    later font and related package additions
```

## Correct philosophical pressure

The governing principle is:

```text
maximum effect from minimum sufficient conditions
```

For the terminal-font problem, the first architectural question should have been:

```text
Can the glibc/Electron application consume a font provider that already exists
in native Termux or Android-visible space through an explicit fontconfig contract?
```

It should not have started with:

```text
Which desktop/font packages can be installed inside the Debian rootfs
until the visible symptom disappears?
```

The later PRoot font installation is therefore treated as **workaround debt**, not as an accepted clean-state dependency.

## Native-font target pressure

This audit does not select or implement one mechanism. It requires the implementation to prove a bounded native-font provider contract.

Candidate provider classes may include:

```text
native Termux-managed font bytes
Android system font bytes visible to the Termux application UID
project-owned selected font bytes acquired from a native source
```

The final choice must be based on evidence, not convenience.

The required behavior is:

```text
VS Code/Obsidian glibc processes
    -> explicit fontconfig configuration
    -> declared native-space font provider
    -> declared cache ownership
    -> no Debian rootfs font package runtime authority
```

The font provider may be referenced or selected/materialized according to the final lifecycle design, but it must not require a persistent PRoot font installation merely to render the integrated terminal.

## Required proof obligations

### Provider identity

```text
exact font file identities
source ownership
version/provenance where applicable
stable path or content-addressed identity
```

### Consumer selection

```text
explicit FONTCONFIG_FILE/FONTCONFIG_PATH or equivalent contract
actual selected family/file evidence
no accidental fallback to rootfs font directories
```

### Required effects

The implementation must define which effects are actually required.

```text
VS Code integrated-terminal monospace rendering
Latin glyph coverage
Korean/CJK coverage if part of the workstation contract
bold/italic variants only when required
UI fallback behavior
```

A font is not required merely because it was installed or mapped once.

### Negative boundary

```text
no rootfs font path in the accepted fontconfig input
no rootfs font file open or map in the required scenarios
no dependency on rootfs fontconfig cache
no broad desktop-font package set by inertia
```

### Clean reconstruction

```text
start from accepted trixie-slim + upgrade + VS Code baseline
leave later PRoot font workaround packages absent
configure the native font provider
reproduce terminal and required application behavior
```

## Pressure on the current four-font selected set

The current selected-generation font set came from Debian rootfs packages:

```text
NotoSansCJK-Regular.ttc
DejaVuMathTeXGyre.ttf
DejaVuSansMono.ttf
DejaVuSansMono-Bold.ttf
```

Its runtime isolation is useful evidence, but its supply origin does not match the newly clarified target philosophy.

Therefore its status is corrected to:

```text
first-generation diagnostic/transition provider:
    VALID AS HISTORICAL EVIDENCE

final clean-state native font provider:
    NOT ACCEPTED YET
```

The successor design must not automatically retain these four files merely because the first generation used them.

It must compare them against a native-source provider and select the minimum set that satisfies the declared effects.

## Pressure on package cleanup

The desired rollback boundary is now clearer.

```text
target retained Debian state:
    trixie-slim
    + initial apt upgrade result
    + VS Code and its required dependency closure

target removed state:
    later font-workaround package delta
    + later related packages that have no independent accepted purpose
```

However, this audit does not authorize a purge command.

Removal remains blocked until evidence distinguishes:

```text
VS Code dependency closure
manual later font additions
automatic dependencies of those later additions
packages independently required by later accepted experiments
generated caches/configuration left by removed packages
```

The purpose of the inventory is now narrow and known: reconstruct the delta **after** the accepted VS Code baseline, not rediscover an unknown rootfs origin.

## Corrected clean-state model

```text
accepted Debian reference state
    debian:trixie-slim
    + initial apt upgrade
    + VS Code dependency closure

native font provider
    outside Debian font-package authority

selected application/runtime providers
    explicit immutable or world-owned contracts

later PRoot font workaround delta
    temporary debt to identify and remove
```

The rootfs may continue to serve as a package/source oracle for other selected ELF capabilities, but it must not become the font authority solely because fonts were installed there during diagnosis.

## Auditor role boundary

The role of this assistant in this project is:

```text
AUDITOR / PRESSURE SOURCE
```

The role includes:

```text
inspect repository decisions and receipts
identify contradictions and hidden assumptions
challenge convenience-based retention
separate proven facts from inference
require minimum-condition and clean-state proof
set stop lines and acceptance pressure
report risks, overclaims, and missing evidence
```

The role excludes:

```text
implementing the font solution
choosing packages or provider paths on behalf of the implementation
running device experiments
installing/removing packages
mutating generations or launchers
turning an audit finding into an implementation without an explicit role change
```

Repository documentation that records audit findings is allowed. Runtime/code implementation is not part of this role.

## Correction to the prior response

The large read-only inventory command proposed after `0113` is withdrawn as an immediate action from the auditor.

The auditor may require evidence categories, but should not advance into an implementation/operation script unless the user explicitly changes the role for that task.

The pressure requirement is therefore expressed as an evidence contract only:

```text
show the package delta after the accepted VS Code baseline;
show which later additions belong to the font workaround;
show whether native fonts can replace the rootfs font authority;
show that cleanup preserves VS Code and accepted workloads;
```

## Revised immediate pressure order

```text
P0. reconstruct the post-VS-Code package/configuration delta;
P1. define native font provider candidates and required effects;
P2. demand a controlled native-font selection experiment from the implementation role;
P3. reject rootfs-font retention unless it outperforms native alternatives under explicit requirements;
P4. after proof, demand a cleanup plan back to the accepted trixie-slim + upgrade + VS Code baseline;
P5. keep pixbuf/icon/MIME work separate from the terminal-font workaround unless evidence joins them.
```

## Stop lines

Do not:

```text
treat the original rootfs as minbase;
question the accepted trixie-slim + upgrade + VS Code baseline without new evidence;
classify all current rootfs packages as suspect;
retain Debian font packages because they are already installed;
retain the four selected Debian fonts by generation inertia;
conflate GTK pixbuf/icon/MIME capability with the earlier VS Code terminal-font workaround;
authorize package purge without reconstructing the post-baseline delta;
implement a native-font solution from the auditor role;
provide operational commands merely because an evidence gap exists.
```

## Final corrected judgment

The core pressure is now narrower and stronger:

```text
The accepted Debian baseline is known.
The later PRoot font workaround is the debt.
The target is a native-space font provider with an explicit glibc fontconfig contract.
The auditor's job is to prevent the workaround from becoming architecture by inertia.
```
