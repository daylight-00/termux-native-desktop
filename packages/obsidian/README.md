# Obsidian package integration

This package owns workstation-specific integration for the extracted Obsidian arm64 AppImage payload.

## Current promoted launchers

```text
packages/obsidian/launcher/obsidian
packages/obsidian/launcher/obsidian-app
```

`tools/deploy` currently exposes them at:

```text
$HOME/gl/bin/obsidian
$HOME/gl/bin/obsidian-app
```

These public paths are current integration adapters, not permanent architecture identities.

## Current GUI contract

The GUI launcher:

- sources the current graphics-policy-neutral glibc baseline;
- uses the external payload under `$HOME/gl/apps/obsidian`;
- configures AppDir data/schema paths;
- avoids upstream AppRun library-path injection;
- owns the application GPU/CPU feature-mode decision;
- when `GL_GPU=1`, applies the explicit managed glibc Freedreno provider and validated ANGLE Vulkan argv;
- when `GL_GPU=0`, retains a provider/bridge-neutral baseline and passes exact `--disable-gpu`;
- fails closed to the sanitized CPU path if the managed provider profile is unavailable.

The CLI launcher bridges the Obsidian-registered user CLI through the glibc boundary. It does not select a graphics provider or OpenGL bridge.

## Graphics-policy validation state

```text
Obsidian GPU branch:
    PASS

Obsidian CPU branch:
    PASS

scoped graphics-policy transaction:
    CLOSED
```

Canonical records:

```text
docs/refactor/0088-obsidian-user-data-authority-and-cdp-path-false-negative.md
docs/refactor/0089-current-obsidian-gpu-environment-and-primary-identity-pass.md
docs/refactor/0090-current-obsidian-cpu-policy-and-survival-pass.md
docs/refactor/0091-scoped-graphics-policy-promotion-closure.md
```

Accepted semantic contract:

```text
application owns feature mode
hardware provider is explicit and consumer-scoped
ANGLE Vulkan branch owns no Zink/Gallium override
CPU branch owns exact --disable-gpu
validation uses receipt-local application state
selected hardware GPU requires correlated evidence
```

The `GL_GPU` variable, launcher paths, and current provider-profile path are implementations of that contract, not immutable object names.

## Application-state authority

Canonical validation does not use the normal profile.

```text
XDG_CONFIG_HOME=<receipt-local config root>
actual Obsidian user data=<config root>/obsidian
```

The first CDP attempt is retained as evidence that a generic Chromium user-data argument did not define Obsidian's actual configuration authority.

Normal vaults, plugins, locks, and long-duration user behavior remain outside promotion evidence.

## Runtime payload

```text
$HOME/gl/apps/obsidian
```

is an external extracted payload and is not tracked in Git.

AppImage acquisition/extraction provenance remains under:

```text
experiments/glibc/obsidian-appimage/
```

The exact current repository launcher sources are bounded by `docs/refactor/0138-selected-obsidian-application-payload-launcher-and-supplement-authority-boundary.md`. The historical Obsidian 1.12.7 arm64 AppImage behavior is accepted, but exact upstream payload supply remains open.

A package-completion pass still needs to promote:

```text
exact upstream release locator and source filename
source size and SHA-256
checksum/signature policy and immutable retention
complete extraction/adaptation receipt and tree manifest
application-version trigger
canonical package-level validators
mutable-state migration and release rollback policy
named application-domain supplement membership
```

## Selected application-domain closure remains open

Graphics validation does not close the selected Obsidian application-domain pilot.

The parent question remains:

```text
Can Obsidian consume selected external provider bytes
while preserving valid AppDir/$ORIGIN locality,
protected substrate ownership,
and control/candidate workload equivalence?
```

Current canonical pilot:

```text
experiments/glibc/selected-obsidian-closure/README.md
```

Remaining work includes:

```text
locality-shadowing analysis
non-graphics static/runtime closure agreement
provider/data capability grouping
candidate materialization
actual candidate-selection proof
control/candidate equivalence
```

Do not treat the package as a reason to expand the broad farm or merge app-local and external provider bytes.

## Current ownership caveat

The launcher still inherits some non-graphics policy from the transitional world baseline, including Electron-family/security behavior.

The highest-priority future split is to move Electron-family policy such as sandbox handling to explicit family/application ownership once the packaging/version assumptions and security consequences are validated.

## Revalidation triggers

Rerun only affected package gates when:

```text
launcher changes
Obsidian/Electron version changes
application-state authority changes
GPU/CPU argv policy changes
provider profile or graphics composition changes
selected-device evidence logic changes materially
```

Documentation-only changes do not require runtime reruns unless they invalidate an existing evidence interpretation.
