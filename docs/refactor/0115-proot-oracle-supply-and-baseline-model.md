# 0115 — PRoot Oracle, Supply, and Baseline Model

## Status

This is a top-down correction after rereading the initial knowledge layer, system-foundation documents, durable PRoot decision, rootfs-as-library-pool experiment, and later selected-closure work.

```text
record type:
    ARCHITECTURE AUDIT / BASELINE MODEL CORRECTION

runtime implementation:
    NO

package operation:
    NO

experiment direction:
    PRESSURE ONLY
```

This record supersedes one conclusion in `0114`:

```text
trixie-slim + apt upgrade + VS Code
    is not the final clean-system baseline.
```

It is a valid historical **oracle scenario state**.

## Foundation-derived conclusion

The project documents consistently establish:

```text
PRoot-mediated normal application execution
    -> rejected

Debian PRoot/rootfs in build and supply plane
    -> accepted

oracle behavior
    -> observe and compare

package manager/rootfs state
    -> candidate input and evidence

promoted runtime authority
    -> selected, validated, materialized outside PRoot
```

The initial knowledge layer says an oracle is a known-good reference used to answer questions, and explicitly warns that the oracle is not automatically the architecture to copy.

The system model places Debian PRoot in the Build and Supply Plane, whose responsibility ends before promotion to live runtime.

The ideal target architecture places the Debian rootfs outside the normal execution path:

```text
Supply/Oracle Plane
    -> candidate materialization
    -> validation
    -> promoted runtime
```

Therefore a mutable installed Debian tree must not be treated as the final workstation baseline merely because it existed first or produced useful evidence.

## The conceptual mistake: one word, several baselines

Earlier discussion used `baseline` for incompatible concepts.

They must be separated.

### 1. Native host baseline

The authoritative machine state:

```text
Android kernel/security model
Termux bionic host
Termux:X11/session
explicit native host packages and tools
```

This baseline exists independently of any Debian oracle instance.

### 2. Oracle seed baseline

The reproducible seed from which a Debian reference instance is derived.

Historical seed:

```text
debian:trixie-slim
```

For future reproducibility the seed contract should also identify:

```text
image/archive digest
architecture
repository/snapshot policy
initial package manifest
```

A floating `apt upgrade` is a historical action, not by itself a stable reproducible identity. Its resulting package manifest or repository snapshot must be recorded if exact reconstruction matters.

### 3. Oracle scenario state

A disposable or reconstructible derived state created to answer one question.

Examples:

```text
oracle.vscode-control
    seed
    + upgrade transaction
    + VS Code installation
    + required dependency closure

oracle.font-control
    seed or vscode-control ancestor
    + font packages
    + observed fontconfig behavior

oracle.pixbuf-control
    seed
    + GTK/pixbuf packages
    + loader/cache/icon/MIME behavior
```

These are controlled experiment inputs, not workstation runtime baselines.

### 4. Supply transaction state

A state used to resolve, download, inspect, or extract exact artifacts.

```text
APT metadata
package archives
package ownership/version information
maintainer-script/trigger observations
staged extraction roots
```

Supply transactions can use a Debian rootfs without promoting the installed tree itself.

### 5. Promoted runtime baseline

The actual workstation runtime contract:

```text
native host
+ coherent glibc world substrate
+ explicit capability providers
+ application-local payloads
+ selected/materialized closures
+ bridges
+ mutable application state
```

PRoot process mediation is absent.

The target also removes passive rootfs file authority where a selected/provider contract has been proven.

### 6. Evidence/control baseline

A named oracle receipt against which target behavior is compared.

This may contain VS Code, fonts, GTK, or other packages. Its purpose is observational and comparative.

It must be reconstructible or preserved as evidence, but it does not need to be retained as one permanent shared rootfs.

## Reclassification of the initial VS Code installation

The historical sequence was:

```text
debian:trixie-slim
    -> apt upgrade
    -> VS Code installation
```

The correct classification depends on purpose.

### Legitimate role

If the installation was used to answer:

```text
Does official VS Code work in ordinary Debian?
Which dependencies and side effects appear?
Which libraries/data/plugins are selected?
What is the known-good process/application behavior?
```

then it was a valid oracle/control transaction.

It is not inherently a philosophical mistake.

### Not an accepted final baseline

It becomes architectural debt when:

```text
the long-lived installed rootfs is treated as the workstation baseline;
its mutable package state is used directly as runtime authority;
its broad dependency closure is copied without selection;
new experiments accumulate permanently in the same state;
clean reconstruction requires remembering that historical tree.
```

Therefore:

```text
VS Code installed in PRoot:
    VALID HISTORICAL ORACLE STATE

VS Code installed in PRoot as final clean runtime/supply baseline:
    REJECTED
```

## Reclassification of the font installation

The later font installation can also have two meanings.

### Valid oracle use

Installing fonts in an isolated reference scenario can legitimately answer:

```text
What does ordinary Debian select?
Which files/families solve the visible problem?
Which fontconfig caches/configs are generated?
Which package owns the observed font?
```

### Invalid architectural promotion

It is not acceptable to conclude:

```text
Debian fonts fixed the reference
    -> persistent PRoot font packages are required by the final workstation
```

The rootfs font state is therefore:

```text
useful control evidence
    but
not final font-provider authority
```

The native-font pressure in `0114` remains valid:

```text
prove an explicit native-space font provider contract
and remove rootfs font authority from the promoted runtime.
```

## The correct PRoot object model

PRoot itself is a mechanism.

The Debian rootfs is an instance.

The architectural objects are:

```text
OracleSeed
OracleScenario
SupplyTransaction
ArtifactReceipt
BehavioralControl
```

Not:

```text
one permanent Debian subsystem
```

A useful conceptual model is:

```text
pinned oracle seed
    |
    +-- disposable vscode-control scenario
    |
    +-- disposable font-control scenario
    |
    +-- disposable pixbuf-control scenario
    |
    +-- supply/download/extraction scenario

scenario outputs
    -> evidence
    -> package/artifact identities
    -> behavioral expectations
    -> selected candidate inputs

selected candidates
    -> materialize
    -> validate
    -> promote outside PRoot
```

The implementation may use copies, snapshots, fresh extraction roots, or reproducible recipes. The architecture does not require one mechanism yet.

The invariant is that scenario state is attributable and disposable rather than silently cumulative.

## Runtime profile versus research profile

The final clean setup should define at least two profiles.

### Workstation runtime profile

Minimum state needed to use the promoted workstation:

```text
native host/session
world substrates
promoted providers and application domains
runtime validators/status
user state
```

Target:

```text
no PRoot process requirement
no Debian rootfs font authority
no broad farm/rootfs runtime authority once replacements are proven
```

A Debian rootfs may be absent entirely from this profile if all required providers have been materialized.

### Research/maintenance profile

Additional state for onboarding, diagnosis, upgrades, and reconstruction:

```text
PRoot tooling
pinned oracle seed recipe
APT/dpkg metadata tooling
scenario recipes
artifact cache or acquisition contract
control validators
```

The research profile may create oracle instances on demand.

It should not require one indefinitely mutated rootfs.

## Minimality criterion

The goal is not the smallest Debian package count inside every oracle scenario.

A control scenario may deliberately install a large application when that maximizes discriminating value.

The clean-state principle is instead:

```text
minimum persistent authority
minimum unexplained accumulated state
minimum promoted dependency surface
```

Therefore:

```text
large disposable oracle scenario:
    can be valid

small but permanently authoritative accidental rootfs dependency:
    can be invalid
```

This is the correct interpretation of maximum effect from minimum sufficient conditions.

## Pressure on the current selected-closure work

The selected-generation direction is correct because it demotes the rootfs from runtime provider to source/evidence input.

The missing step is to demote the installed rootfs from permanent **supply authority** as well.

Target:

```text
oracle/supply scenario
    -> locked artifacts and receipts
    -> selected content generation
    -> runtime composition
```

Not:

```text
current mutable rootfs absolute path
    -> forever required for materialization
```

This does not require eliminating Debian as an artifact source. It requires making the source transaction explicit and reproducible.

## Pressure on cleanup language

The cleanup target is no longer:

```text
restore one accepted long-lived rootfs baseline
```

It is:

```text
stop depending on the accumulated rootfs as authority;
preserve/reconstruct useful oracle scenarios;
remove obsolete persistent scenario state when safe;
prove the runtime profile independently.
```

The current long-lived rootfs can be:

```text
preserved temporarily as historical evidence;
exported/archived if needed;
replaced later by reproducible scenario recipes;
recreated from the seed;
or deleted when no longer authoritative.
```

Manual package-by-package rollback is not automatically superior to recreating the appropriate oracle scenario from a pinned seed.

## Evidence obligations

The implementation/research session should eventually provide:

### Oracle seed identity

```text
exact trixie-slim source/archive identity
architecture
initial package manifest
repository/snapshot context
```

### Scenario receipts

For VS Code, fonts, pixbuf, and future controls:

```text
parent seed/scenario identity
requested packages/artifacts
resolved package/version set
transaction logs
resulting package manifest
question answered
outputs retained
scenario disposal/recreation policy
```

### Supply receipts

```text
exact package/artifact hashes
origin/version/signature information
selected extracted paths
maintainer-script/trigger relevance
```

### Runtime independence

```text
no PRoot mediation
no undeclared rootfs paths
no broad scenario-state authority
```

## Revised baseline vocabulary

Use these terms in future records:

```text
host baseline
oracle seed
oracle scenario
supply transaction
behavioral control
promoted runtime composition
runtime profile
research profile
```

Avoid unqualified:

```text
Debian baseline
clean rootfs baseline
```

because those phrases collapse different authorities and lifecycles.

## Revised audit pressure order

```text
P0. stop treating the current accumulated rootfs as one clean baseline;
P1. identify the oracle seed and historical scenario lineage;
P2. separate VS Code, font, pixbuf, and supply roles conceptually;
P3. preserve only the evidence/artifacts needed to reconstruct each scenario;
P4. prove the native font provider against a named font-control scenario;
P5. make selected-generation synthesis consume locked supply receipts;
P6. prove a workstation runtime profile with no rootfs font authority;
P7. decide whether the long-lived rootfs should be archived, reset, or removed;
P8. reproduce oracle scenarios on demand rather than accumulating one mutable system.
```

## Stop lines

Do not:

```text
call trixie-slim + upgrade + VS Code the final clean-system baseline;
call installing VS Code in an oracle inherently wrong;
confuse a valid control installation with runtime promotion;
use one accumulated rootfs for every experiment without scenario attribution;
make package-count minimalism the primary oracle criterion;
retain PRoot font authority because it is already present;
remove useful oracle evidence before scenario lineage/artifacts are preserved;
require the workstation runtime profile to retain PRoot unless a promoted capability still proves that need;
turn this audit into an implementation choice among snapshot/copy/container mechanisms.
```

## Auditor boundary

The assistant remains an auditor and source of top-down pressure.

This record defines object classes, proof obligations, and stop lines. It does not choose or implement the oracle-instance mechanism, execute package transactions, or operate the device.

## Final judgment

PRoot should be treated as:

> **A disposable and reproducible oracle/supply mechanism that produces evidence and candidate artifacts, not a persistent Debian subsystem and not a promoted workstation baseline.**

The VS Code installation was a valid historical oracle scenario when used as a known-good control.

The font installation was also potentially valid as a diagnostic oracle scenario.

The mistake would be allowing either scenario's accumulated installed state to become permanent runtime or supply authority by inertia.
