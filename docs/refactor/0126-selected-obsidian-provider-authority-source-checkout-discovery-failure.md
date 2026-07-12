# 0126 — Selected Obsidian Provider-Authority Source Checkout Discovery Failure

## Status

```text
source-recipe evidence rerun:
    FAIL BEFORE SOURCE HEAD RESOLUTION

observed failure:
    git -C <source-path> rev-parse HEAD
        -> non-zero

prior origin-only diagnosis:
    WITHDRAWN

source checkout probe:
    AVAILABLE

package/runtime/generation/current mutation:
    NONE
```

The second execution showed that the earlier `remote get-url origin` failure must not be interpreted merely as a missing remote. The same path now fails to resolve `HEAD`, which means Git cannot currently treat it as a valid ordinary checkout.

Possible classes include:

```text
broken .git file pointing to a missing gitdir;
incomplete or damaged .git directory;
source archive or copied worktree carrying stale Git metadata;
wrong directory level;
bare or otherwise non-worktree repository layout;
missing HEAD or referenced object.
```

No class is accepted until the read-only probe reports the actual Git discovery state.

## Probe

```text
experiments/glibc/selected-obsidian-provider-authority/recipe/
    probe-n3-source-repository.sh
```

The probe records without mutation:

```text
source path type;
.git marker type;
first gitfile line when .git is a file;
absolute git directory resolution;
worktree top-level resolution;
HEAD resolution;
bare/non-bare state;
shallow state;
clean-status command result;
configured remotes;
stdout, stderr, and return code for each Git query.
```

The probe does not run fetch, clone, reset, checkout, clean, or package operations.

## Execution

```bash
git pull --ff-only

bash \
  experiments/glibc/selected-obsidian-provider-authority/recipe/probe-n3-source-repository.sh
```

The complete terminal output is the next required evidence.

## Direction decision

Do not recreate, delete, fetch, reset, or repair the source path before the probe output is reviewed. The directory is external evidence input; even a broken checkout should first be classified so the workflow records why replacement is justified.
