# 0052 — GLX Map Runtime Anonymous Memory Classification

## Status

The software-intent Zink/Llvmpipe graph exposed one enrichment-classification gap:

```text
/memfd:allocation
```

The original enrichment classified it as:

```text
path_class=OTHER
package=UNKNOWN
version=UNKNOWN
```

This classification was misleading because the mapping is not a package-provenance object and should not contribute to an unresolved provider set.

## Correction

The GLX map enrichment now classifies only the narrow observed pattern:

```text
/memfd:allocation*
```

as:

```text
path_class=RUNTIME_ANON_MEMORY
package=RUNTIME_MEMORY
version=NOT_APPLICABLE
state=RUNTIME_ANONYMOUS_MAPPING
```

Identity fields are:

```text
sha256=NOT_APPLICABLE
build_id=NOT_APPLICABLE
soname=NOT_APPLICABLE
```

The correction intentionally does not assign semantic ownership to every possible `/memfd:*` name.

## Why the narrow pattern matters

A memfd mapping can represent different runtime purposes depending on producer and use. The current evidence establishes only that:

```text
/memfd:allocation
```

is a non-filesystem anonymous runtime mapping captured in the passing software control.

The current evidence does not establish:

```text
which component created it
what exact allocation purpose it serves
whether every memfd mapping should share one semantic class
```

Therefore the classifier uses a narrow evidence-backed pattern instead of a broad `/memfd:*` rule.

## Architecture consequence

The provider graph must distinguish:

```text
filesystem provider objects
package-owned support objects
device nodes
runtime caches
runtime anonymous memory mappings
```

A runtime mapping that appears in `/proc/<pid>/maps` is not automatically a provider closure member.

This correction preserves the principle:

```text
mapped object presence
    !=
package provenance
    !=
selected provider role
```

## Validation

Re-run enrichment for the software evidence root:

```bash
MAP_OUT="$PREFIX/tmp/tnd-vulkan-policy-composition/implicit-software-maps-20260711-025042" \
bash \
    experiments/glibc/vulkan-policy-composition/recipe/enrich-glx-probe-maps.sh
```

Then verify:

```bash
grep -F '/memfd:allocation' \
    "$PREFIX/tmp/tnd-vulkan-policy-composition/implicit-software-maps-20260711-025042/mapped-provider-identities.tsv"
```

Expected class/state:

```text
RUNTIME_ANON_MEMORY
RUNTIME_ANONYMOUS_MAPPING
```

The package summary should no longer contain:

```text
OTHER UNKNOWN UNKNOWN 1
```

for this observed mapping.
