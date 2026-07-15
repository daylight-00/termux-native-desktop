# 10. Open Design Questions

> **Lifecycle:** historical system-foundation provenance. Current constitutional authority is [`../constitution/`](../constitution/README.md); current architecture is [`../architecture/`](../architecture/README.md). Interpret this document in its recorded context; any later status, precedence, or execution-order wording below is historical to that context.

Good architecture does not force certainty where evidence is incomplete. This document lists questions that should remain explicit until experiments justify a decision.

## 10.1 Should passive Debian rootfs runtime dependencies remain?

Current practical pattern can use rootfs-hosted:

```text
fonts/fontconfig data
locale data
XDG shared data
```

Options:

### A. Accept passive rootfs provider

Pros:

```text
simple
package-managed source
broad data availability
```

Cons:

```text
runtime filesystem dependency remains broad
harder to define minimal runtime closure
rootfs updates can change behavior
```

### B. Materialize selected data providers

Pros:

```text
explicit closure
portable runtime state
clear provenance/versioning
```

Cons:

```text
selection complexity
update burden
risk of missing dynamic data requirements
```

Decision should be per capability, not one global yes/no.

## 10.2 How much of the shared library pool should be global?

Options:

```text
broad shared farm
manifest-selected shared core/provider set
mostly app-local closures
hybrid tiers
```

A likely target is hybrid:

```text
coherent low-level core
small set of intentionally shared providers
app-local libraries when upstream locality is important
resolved supplemental closure
```

But empirical collision/duplication data should guide the boundary.

## 10.3 What is the canonical world definition format?

Start with Markdown. Later choices:

```text
TOML
YAML
JSON
shell declarations
custom minimal DSL
```

Selection questions:

```text
Can schema be validated?
Can comments explain decisions?
Can shell tooling consume it without heavy runtime dependencies?
Can values remain declarative rather than arbitrary code?
```

Do not choose format before field semantics stabilize.

## 10.4 Should launch composition be generated or interpreted?

### Generate scripts

```text
manifest -> generated launcher
```

Pros: inspectable output, low runtime complexity.

### Interpret at launch

```text
manifest -> runtime composer -> exec
```

Pros: centralized conflict checks and dynamic selection.

A hybrid may work:

```text
generate deterministic launch plan
validate
execute thin runner
```

Measure startup complexity before deciding.

## 10.5 What belongs in world base versus capability provider?

Borderline examples:

```text
DISPLAY
XDG_RUNTIME_DIR
TMPDIR
DBus address policy
GSettings backend
```

Questions:

```text
Is this fundamental to every process in the world?
Is it only needed by desktop GUI consumers?
Is it a bridge endpoint?
Is it application-family behavior?
```

The semantic inventory should resolve each item.

## 10.6 Electron sandbox policy scope

Current environment applies an Electron sandbox setting broadly in the glibc environment.

Open questions:

```text
Is it required for every Electron app?
Only for current packaging topology?
Only for selected versions?
Can a narrower CLI/app policy replace it?
What are the security implications?
```

Do not move it blindly; perform controlled tests.

## 10.7 How should app-local and shared libraries interact?

Need explicit policy for:

```text
$ORIGIN preservation
provider override rules
SONAME collisions
symbol version conflicts
plugin-local dependencies
```

A resolver may need to distinguish:

```text
mandatory app-local
preferred shared
forbidden shared override
fallback candidate
```

This should be based on real app cases.

## 10.8 How should runtime plugin closure be discovered?

Possible evidence sources:

```text
loader diagnostics
strace file opens
/proc maps before/after feature action
plugin metadata scans
application logs
package manifests
```

A robust resolver likely needs both static and dynamic evidence.

Question: how much dynamic trace should become reusable manifest data versus remain test evidence?

## 10.9 What is the right PyMOL acquisition strategy?

Options include:

```text
Conda package environment
source build into controlled prefix
wheel-oriented packaging with native closure
hybrid source + selected binary dependencies
licensed vendor payload adapter
```

Decision criteria:

```text
license/redistribution
ABI target coherence
OpenGL/Qt dependency shape
Python integration
reproducibility
maintenance cost
performance
```

The domain/capability contract should be written before selecting the source strategy.

## 10.10 Should Conda be treated as provider, app domain, or supply source?

Potential roles:

```text
Python runtime provider
scientific native dependency provider
application materialization mechanism
artifact source
```

It can legitimately serve more than one role, but ownership must be explicit to avoid Conda environment variables redefining the entire glibc world.

## 10.11 How should proprietary applications be supported?

A sustainable model may be:

```text
project distributes runtime support and adapter
user provides/downloads licensed artifact
adapter verifies and transforms locally
```

Questions:

```text
What metadata can be distributed?
Can checksums/version selectors be published?
What transformations are license-compatible?
How are updates detected?
```

Legal terms must be checked for each upstream source; technical feasibility is not redistribution permission.

## 10.12 Should a project package manager eventually exist?

Possible future triggers:

```text
many apps/providers
version constraints
shared provider upgrades
file ownership needs
rollback history
remote repository/release distribution
```

Until then, simpler mechanisms may be enough:

```text
manifests
versioned directories
stable symlinks
install/materialize scripts
checksums
promotion records
```

Do not build a package manager because package managers are interesting.

## 10.13 How much host abstraction is desirable?

Current primary target is a specific device and stock Android environment.

Potential future scope:

```text
same SoC family
multiple Adreno generations
multiple Android versions
other Termux package generations
other OEM kernels
```

Generalization should follow evidence. Contracts should include scope metadata so device-specific assumptions remain visible.

## 10.14 How should GPU provider compatibility be expressed?

Potential dimensions:

```text
Mesa source version/commit
build options
KMD support set
libdrm dependency shape
Vulkan loader version
kernel KGSL behavior
Android version/device
WSI path
```

A provider manifest must avoid pretending one “Mesa version” uniquely defines behavior.

## 10.15 Can the broad farm be indexed before it is replaced?

A low-risk intermediate step:

```text
keep current farm semantics
    -> generate manifest of symlink name, target path, package owner, version
    -> detect collisions and ordering
```

This would improve provenance without changing runtime behavior.

Open question: which package ownership query mechanism is easiest and reliable inside the rootfs?

## 10.16 What is the minimum world-purity classifier?

Possible approaches:

```text
path-origin rules
ELF interpreter/ABI metadata
known package provenance
hash manifests
symbol-version signatures
```

A first validator can be conservative and path/provenance based. It should label unknowns rather than claiming certainty.

## 10.17 How should current `architecture.md` and target architecture coexist?

Recommended distinction:

```text
architecture.md
    -> current integrated operational model

system-foundation/
    -> abstract identity, target model, migration strategy
```

As implementation converges, selected target concepts may be promoted into `architecture.md`. Do not prematurely rewrite current-state documentation as future state.

## 10.18 When is refactoring complete?

Not when:

```text
all files moved
all scripts renamed
new manifest parser exists
```

But when:

```text
new apps reuse contracts;
provider selection is deterministic;
world contamination is automatically detected;
rootfs dependencies are intentional and visible;
working behavior survives structural changes;
promotion and rollback are repeatable;
evidence explains why runtime state exists.
```

## 10.19 Decision process for open questions

For each question:

```text
1. write competing hypotheses/options;
2. define decision criteria;
3. design smallest discriminating experiment;
4. collect evidence;
5. record conclusion scope;
6. create decision record only when durable;
7. update contracts and validators together.
```

Open questions are not architecture failures. Hidden open questions are.
