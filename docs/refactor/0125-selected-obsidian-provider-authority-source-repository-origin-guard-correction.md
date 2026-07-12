# 0125 — Selected Obsidian Provider-Authority Source Repository Origin-Guard Correction

## Status

```text
first source-recipe evidence execution:
    FAIL DURING SOURCE_REPOSITORY_GUARD

failure cause:
    source checkout has no origin remote

source checkout content judgment:
    NOT REJECTED BY THIS FAILURE

corrected wrapper:
    READY_FOR DEVICE EXECUTION

provider-authority intervention:
    ACTIVE
```

The first execution stopped before package, APT, or recipe analysis because:

```text
git remote get-url origin
    -> rc 128
```

Failure evidence remains at:

```text
$PREFIX/tmp/selected-obsidian-provider-authority/
    selected-obsidian-provider-authority-n3-source-recipe-evidence-20260712-172842
```

The failure proves only that the user-provided source checkout lacks a persistent `origin` remote. It does not prove that the Git object graph is shallow, dirty, incomplete, or unrelated to the approved public repository.

## Independent public pin

The approved public repository was independently inspected at:

```text
repository:
    termux-pacman/glibc-packages

main HEAD:
    fd2ae25e04f3ea26d6c7b4678020814889331d86

subject:
    update pkgs (#380)
```

The corrected wrapper pins the external source input to that exact commit.

## Corrected input guard

The original source checkout must satisfy:

```text
HEAD exactly equals the pinned public commit;
checkout is full and non-shallow;
tracked and untracked state is clean;
git fsck connectivity passes;
refs are hashed before and after collection;
HEAD, refs, and worktree state remain unchanged.
```

Remote handling is now:

```text
approved persistent origin present:
    collector uses the original checkout

origin absent:
    wrapper creates an isolated local clone under the evidence base
    without network fetch and without hardlinks;
    only the temporary clone receives the approved origin URL;
    collector uses that temporary normalized view;
    original source metadata remains untouched;
    temporary view is removed when the wrapper exits

unexpected persistent origin:
    hard failure
```

This preserves the collector's existing strict origin guard without mutating the user-provided source checkout merely to satisfy a metadata label.

## Added receipt evidence

A passing archive now contains:

```text
source-repository-origin-guard.tsv
```

It records:

```text
input and effective source paths;
expected and observed HEAD;
origin handling mode;
persistent origin before collection;
effective approved origin;
input refs SHA-256 before and after;
input metadata mutation = NO;
network fetch performed = NO.
```

## Development validation

The corrected wrapper passed a synthetic transaction where:

```text
input checkout had no remotes;
input HEAD matched the configured pin;
input was full, clean, and fsck-valid;
an isolated local clone was created;
the collector observed the approved origin;
the original checkout remained remote-less and clean;
the temporary clone was removed;
the archive retained the origin-guard receipt.
```

## Read-only boundary

The correction does not:

```text
add or modify a remote in the user-provided source checkout;
fetch source objects from the network;
reset or checkout the source input;
run apt update or package download;
install, upgrade, remove, or build packages;
launch a workload;
mutate the selected generation or current.
```

## Rerun

After fast-forwarding the project branch, run the same command:

```bash
git pull --ff-only

bash \
  experiments/glibc/selected-obsidian-provider-authority/recipe/run-n3-source-recipe-evidence.sh
```

Expected origin mode for the currently observed remote-less input:

```text
SOURCE_REPO_ORIGIN_MODE=ISOLATED_LOCAL_CLONE_APPROVED_ORIGIN
```

If the source checkout HEAD differs from the pinned commit, the wrapper prints both identities and stops. Do not fetch or reset it until that mismatch is reviewed.

## Stop line

Do not:

```text
add origin solely to bypass the guard;
accept an arbitrary remote-less repository;
change the source pin without independent public verification;
continue after a source HEAD mismatch;
perform package, runtime, generation, or current mutation.
```
