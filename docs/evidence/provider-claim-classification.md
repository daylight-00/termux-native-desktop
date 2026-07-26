# Provider claim classification under ADR 0005

The exact `libpixman-1.so.0.46.4` is additionally accepted as a bounded Cairo prerequisite. The exact `libgraphite2.so.3.2.1` is accepted as a bounded HarfBuzz Graphite-shaping prerequisite. These outside-inventory prerequisites do not widen complete composition, target, or activation authority.

## Status

```text
classification: COMPLETE / REVIEWED BOUNDED INVENTORY
roots: 28
objects: 37
claims: 95
Class A: 36
Class B: 52
Class C: 4
Class D: 3
provider authority claims: 31
provider reviews accepted: 24
provider authority still open: 7
composition accepted: 0
target rows accepted: 0
activation accepted: 0
```

The generator is `experiments/glibc/selected-obsidian-provider-authority/recipe/generate-provider-claim-classification.py`; canonical outputs are the provider claim, SUP-02 disposition and metadata TSVs.

## Claim separation

Each root retains separate artifact-identity, adaptation-semantics and provider-authority claims. OJ-001 required identity, producing provenance, composition, target population and activation remain separate global/object claims.

## Latest claim additions

The exact GTK 3.24.49 production result adds:

```text
PCC-GTK3-CORE-PRODUCING  Class C
    exact independently reproduced atomic package and GDK/GTK member record

PCC-GTK3-CORE-PROVIDER   Class B
    exact atomic two-member provider decision for selected GTK core library linkage
```

The Class C row retains source, recipe, patch, package, ELF, GIR/typelib, dependency, loader and protected-state evidence. The Class B row accepts only `libgdk-3.so.0.2417.32` and `libgtk-3.so.0.2417.32` plus their SONAME aliases. It does not authorize package-wide tools, modules, schemas, printing, display/service operation, target population, deployment or activation.

## SUP-02 disposition

```text
STILL_NECESSARY: 0
NARROWED:       14
REPLACED:        7
UNNECESSARY:     7
```

All requests remain historical. None is required now without a new explicit Class C reclassification or recorded escalation trigger.

## Current authority state

Twenty-one provider roots inside the fixed 28-root inventory remain accepted. Three exact project-produced roots outside that inventory—libXdamage, atomic AT-SPI2/ATK, and atomic GTK 3 core—have separate bounded provider decisions. Exact Pixman and Graphite2 remain bounded prerequisites outside the claim inventory.

The selected composition has one unresolved identity, `libselinux.so.1`. The next review is direct-consumer necessity and security semantics only. Target population and activation remain blocked.

## Stop line

Do not combine artifact identity, adaptation, producing provenance, provider authority, composition, target population or activation; do not infer package-wide or execution authority from the GTK build; and do not authorize libSELinux production from the remaining gap alone.
