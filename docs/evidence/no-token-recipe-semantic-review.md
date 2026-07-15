# Seven-root no-token recipe semantic review

## Status

```text
review state: COMPLETE
roots reviewed: 7
confirmed Class A: 7
reclassified Class B: 0
new supplier or runtime evidence collected: 0
provider authority accepted: 0
composition accepted: 0
target population accepted: 0
activation accepted: 0
```

This review closes the package-specific recipe-adaptation question for the seven roots whose earlier token collector found no explicit patch, hook, option, or packaging delta. It does not establish provider authority.

Canonical machine-readable record:

```text
experiments/glibc/selected-obsidian-provider-authority/review/
    no-token-recipe-semantic-review.tsv
```

The provider claim inventory consumes that table through:

```text
experiments/glibc/selected-obsidian-provider-authority/recipe/
    generate-provider-claim-classification.py
```

## Method

For every root, the review bound the exact recipe to:

```text
source repository: termux-pacman/glibc-packages
source commit: fd2ae25e04f3ea26d6c7b4678020814889331d86
recipe tree: canonical root-review row
recipe file manifest: one build.sh blob with exact Git identity
upstream source: exact version, URL and SHA-256 from the pinned recipe
upstream build entrypoint: Meson or release-tarball Autotools/X.Org configuration
```

The review then checked whether `build.sh` introduced any package-specific:

```text
source patch or hook
configure or Meson option
custom build step
install/output transformation
custom path or layout policy
```

Dependency declarations and source/version pins were recorded, but they were not treated as semantic source or producing-process adaptations by themselves.

## Result

| Root | Version | Build system | Result | Package-specific changed boundary |
|---|---:|---|---|---|
| `gpkg/libepoxy` | 1.5.10 | Meson | `CONFIRMED_A` | none; source pin and dependency metadata only |
| `gpkg/libtasn1` | 4.20.0 | Autotools | `CONFIRMED_A` | none; source pin and dependency metadata only |
| `gpkg/libxcomposite` | 0.4.6 | X.Org Autotools | `CONFIRMED_A` | none; source pin and dependency metadata only |
| `gpkg/libxfixes` | 6.0.1 | X.Org Autotools | `CONFIRMED_A` | none; source pin and dependency metadata only |
| `gpkg/libxi` | 1.8.2 | X.Org Autotools | `CONFIRMED_A` | none; source pin and dependency metadata only |
| `gpkg/libxinerama` | 1.1.5 | X.Org Autotools | `CONFIRMED_A` | none; source pin and dependency metadata only |
| `gpkg/pango` | 1.54.0 | Meson | `CONFIRMED_A` | none; source pin and dependency metadata only |

The exact recipe directories contain one `build.sh` each. None declares a patch, custom hook, package-specific build option, custom install step, or output transformation.

## Supplier boundary retained

Class A does not mean the complete producing environment was reconstructed. The project continues to rely on:

```text
the exact authoritative upstream release
upstream Meson or Autotools semantics
the generic Termux glibc cross-build framework
toolchain, prefix and dependency resolution supplied by that framework
```

Those boundaries are intentionally not re-prosecuted as Class C because this review does not claim independent reproduction or bit-equivalent output.

### `libepoxy`

Upstream defaults select GLX and EGL from the detected host platform. The recipe does not override those choices. Feature selection therefore remains supplier-environment-sensitive and must be checked when provider authority and runtime selection are reviewed.

### X.Org roots

The four X.Org recipes use release tarballs with standard X.Org Autotools entrypoints and dependency checks. Their package-specific recipes add no semantic build delta. Capability necessity, consumer binding, conflict/exclusion, and rollback remain separate provider-authority questions.

### `pango`

Upstream Meson auto-selects several optional capabilities from the available dependency set. The recipe adds no option override. The `gobject-introspection` build dependency does not by itself establish GIR output in a cross build without explicit upstream introspection enablement.

The existing concrete-filename drift remains open:

```text
CF-001
CF-002
CF-003
CF-004
```

That drift is a provider-integration and continuity-policy question. It is not evidence of package-specific recipe adaptation and is not closed by this review.

## Claim inventory effect

For these seven roots:

```text
ADAPTATION_SEMANTICS
    Class A confirmed
    AD-006 semantic-review gap closed

PROVIDER_AUTHORITY
    remains Class B and open
    adaptation-classification prerequisite removed
```

The overall inventory remains:

```text
89 claims
36 Class A
49 Class B
 1 conditional Class C
 3 Class D
```

No historical SUP-02 request becomes required. The six T6 requests remain unnecessary and the Pango request remains replaced by bounded semantic and drift-policy review.

## Next bounded tranche

The smallest coherent next tranche is the four-root X.Org provider-authority chain:

```text
gpkg/libxfixes
gpkg/libxcomposite
gpkg/libxi
gpkg/libxinerama
```

That review may use exact artifact/member identities, SONAMEs, package dependency edges, capability necessity, and bounded passive consumer evidence. It must not infer composition, target membership, or activation.

## Stop line

Do not infer from this review that:

- supplier producing-build provenance has been reconstructed;
- generic Termux glibc framework behavior is project-owned;
- any package member is an accepted provider;
- Pango filename drift is resolved;
- the selected runtime composition or target population is complete;
- activation is authorized.
