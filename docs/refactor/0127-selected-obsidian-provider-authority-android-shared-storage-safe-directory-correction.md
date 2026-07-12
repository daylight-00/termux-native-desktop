# 0127 — Selected Obsidian Provider-Authority Android Shared-Storage `safe.directory` Correction

## Status

```text
source checkout probe:
    COMPLETE

source checkout corruption:
    NOT OBSERVED

actual failure class:
    GIT DUBIOUS-OWNERSHIP PROTECTION

corrected source wrapper:
    READY_FOR DEVICE EXECUTION

package/runtime/generation/current mutation:
    NONE
```

## Corrected diagnosis

The project checkout and branch topology are normal:

```text
current branch:
    docs/post-graphics-architecture-audit

remote tracking branch:
    origin/docs/post-graphics-architecture-audit
```

The source input's logical path is:

```text
/data/data/com.termux/files/home/Downloads/
    termux-pacman-glibc-packages-source
```

Its physical Android shared-storage path is:

```text
/storage/emulated/0/Download/
    termux-pacman-glibc-packages-source
```

Git refused every query with:

```text
fatal: detected dubious ownership in repository
```

Therefore the earlier origin-only and possible-checkout-damage diagnoses are withdrawn. Git had not yet inspected the repository because ownership protection stopped discovery first.

## Why global configuration is rejected

Git suggested:

```text
git config --global --add safe.directory <path>
```

The evidence workflow does not apply this suggestion because it would persist a broad user-level trust decision outside the transaction.

The wrapper instead supplies:

```text
git -c safe.directory=<canonical physical path> ...
```

for each read-only operation against the source input.

This is command-scoped and leaves global, local, and source-repository configuration unchanged.

## Isolation transfer

A direct local `git clone <shared-storage-path>` is also rejected. Its internal `upload-pack` subprocess does not retain the parent command's scoped `safe.directory` setting.

The corrected transfer is:

```text
source checkout
    -> command-scoped `git bundle create --all`
    -> bundle under $PREFIX/tmp evidence base
    -> clone bundle into an internally owned temporary checkout
    -> set approved origin only on the temporary checkout
    -> run collector against the temporary checkout
    -> remove bundle and temporary checkout on exit
```

No network fetch occurs.

## Preserved guards

The source input must still pass:

```text
HEAD equals:
    fd2ae25e04f3ea26d6c7b4678020814889331d86

non-bare checkout;
full non-shallow history;
clean tracked and untracked state;
git fsck connectivity;
approved or absent persistent origin;
HEAD and refs unchanged after collection.
```

The temporary checkout must also retain the pinned HEAD, full-history state, clean worktree, and fsck connectivity.

## Receipt extension

A passing result records:

```text
origin_mode:
    ISOLATED_SHARED_STORAGE_SAFE_DIRECTORY_BUNDLE_CLONE

safe_directory_scope:
    COMMAND_ONLY

transfer_mode:
    LOCAL_GIT_BUNDLE_ALL_REFS

input_git_config_mutation:
    NO

input_metadata_mutation:
    NO

network_fetch_performed:
    NO
```

## Development reproduction

The ownership failure was independently reproduced with a Git checkout owned by a different account:

```text
plain git rev-parse:
    rejected as dubious ownership

command-scoped safe.directory rev-parse:
    PASS

command-scoped bundle creation:
    PASS

bundle clone into owned storage:
    PASS
```

This validates the corrected mechanism rather than merely suppressing the observed error message.

## Direction decision

Rerun the source-recipe collector after fast-forwarding the project branch. Do not add a global `safe.directory` exception and do not move or recreate the source checkout.
