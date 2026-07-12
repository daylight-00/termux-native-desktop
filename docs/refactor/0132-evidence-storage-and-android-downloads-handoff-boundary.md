# 0132 — Evidence Storage and Android Downloads Handoff Boundary

## Status

```text
prior Downloads interpretation:
    INCORRECT

correct storage boundary:
    ACCEPTED

Termux private work state:
    repository experiment work tree or other stage-owned private path

Android-visible Downloads:
    final handoff artifacts only
```

## Corrected rule

`$HOME/Downloads` is the contact point between the Termux user and the Android user/UI. It is not the project's general source, cache, build, extraction, or transaction workspace.

The rule is:

```text
files that must be handed to the external reviewer/user interface:
    $HOME/Downloads

all other persistent or temporary project state:
    an appropriate Termux-private location
    or the repository's ignored stage work tree
```

For this workstream the canonical private workspace is:

```text
experiments/glibc/selected-obsidian-provider-authority/work/
```

It is covered by the repository ignore rule:

```text
experiments/**/work/
```

## Canonical layout

```text
work/
    source/
        external source checkouts

    artifacts/
        exact package artifacts and reusable caches

    receipts/
        unpacked/
            unpacked transaction roots

    tmp/
        transaction-local bundles, clones, and scratch state
```

Final reviewer handoff archives use:

```text
$HOME/Downloads/*.tgz
```

## What belongs in Downloads

Only artifacts intended to cross the Termux/Android-user boundary belong there, for example:

```text
final evidence TGZ requested for upload;
explicitly requested patch or document handoff;
other operator-facing export files.
```

The final handoff archive is a copy/export boundary. It is not the authoritative live workspace.

## What does not belong in Downloads

Do not place the following there by default:

```text
Git source repositories;
raw downloaded package caches;
unpacked receipts;
build trees;
source trees;
package extraction directories;
temporary clones or bundles;
long-lived experiment state;
internal manifests that are already contained in a handoff archive.
```

Android shared storage has different ownership, filesystem, symlink, permission, metadata, and Git safety behavior. Those constraints should not be introduced into normal Termux-private work without a handoff requirement.

## Current provider-authority defaults

Source-recipe evidence:

```text
source checkout:
    work/source/termux-pacman-glibc-packages

unpacked receipt:
    work/receipts/unpacked/...

temporary bundle/clone:
    work/tmp/...

final TGZ handoff:
    $HOME/Downloads/selected-obsidian-provider-authority-n3-source-recipe-evidence-results-<timestamp>.tgz
```

Binary-artifact evidence:

```text
exact .deb cache:
    work/artifacts/n3-exact-debs

unpacked receipt:
    work/receipts/unpacked/...

final TGZ handoff:
    $HOME/Downloads/selected-obsidian-provider-authority-n3-binary-artifact-comparison-results-<timestamp>.tgz
```

## Historical receipts

Receipts already produced in `$PREFIX/tmp` or the private `work/` tree remain valid when their content and transaction guards passed. They do not need to be regenerated solely because the default storage policy was later clarified.

The accepted binary receipt from `20260712-194542` remains valid. Its TGZ was successfully handed off even though the runner initially created it in `work/receipts`; no semantic or identity claim depends on that path.

## Implementation correction

The source and binary runners now enforce:

```text
source/cache/OUT/temp:
    under the private work tree

ARCHIVE:
    under HANDOFF_DIR

HANDOFF_DIR default:
    $HOME/Downloads
```

This keeps shared-storage exposure to the single final compressed archive.

## Generalization

The same principle applies to later project stages:

```text
internal state follows the owning subsystem's Termux-private layout;
repository-local generated state uses ignored work directories;
only explicit exports and reviewer handoffs use Downloads.
```

Do not infer from an archive-delivery rule that all evidence inputs or caches should share the archive's destination.
