# 0077 — Vulkan Policy Pre-Deploy PASS and Symlink Activation Gap

## Status

The real-device no-mutation pre-deploy receipt passed.

Evidence root:

```text
$PREFIX/tmp/tnd-vulkan-policy-composition/
    promoted-vulkan-policy-predeploy-20260711-154344
```

Repository state:

```text
branch:
    refactor/module-package-layout

head:
    e86dfa1516a6c978c31a81ebb849153c4232aa61
```

Receipt:

```text
gate_failures=0
predeploy.status=PASS
```

Passed gates:

```text
shell_syntax                         PASS
policy_scope_smoke                   PASS
deploy_smoke                         PASS
live_deploy_dry_run                  PASS
baseline_clears_vk_driver_files      PASS
baseline_does_not_export_vk_driver_files PASS
baseline_does_not_export_vk_icd_filenames PASS
profile_exports_vk_driver_files      PASS
profile_exports_vk_icd_filenames     PASS
gl_run_sources_profile               PASS
vscode_sources_profile               PASS
obsidian_app_sources_profile         PASS
dry_run_plans_profile                PASS
dry_run_plans_gl_env                 PASS
dry_run_plans_vscode                 PASS
dry_run_plans_obsidian_app           PASS
```

This authorizes the explicit live deployment step for the scoped policy transaction.

It does not close post-deployment environment or workload gates.

## Dry-run result

The live `tools/deploy --dry-run` plan correctly includes:

```text
$HOME/gl/env
$HOME/gl/bin/gl-run
$HOME/gl/policy/vulkan/freedreno.sh
$HOME/.local/bin/code
$HOME/gl/bin/obsidian
$HOME/gl/bin/obsidian-app
```

and all existing module/package overlay leaves.

The new profile destination is planned as:

```text
$HOME/gl/policy/vulkan/freedreno.sh
    -> repository modules/gl/overlay/home/gl/policy/vulkan/freedreno.sh
```

## Important lifecycle finding

The current live-target inventory exposed a transaction-boundary defect in the repository deployment model.

Before running `tools/deploy`, these existing runtime paths were already symlinks into the mutable checkout:

```text
$HOME/gl/env
$HOME/gl/bin/gl-run
$HOME/.local/bin/code
$HOME/gl/bin/obsidian
$HOME/gl/bin/obsidian-app
```

The new profile path was still:

```text
$HOME/gl/policy/vulkan/freedreno.sh
    ABSENT
```

Therefore the sequence:

```text
git pull
    -> existing symlink targets immediately expose new source contents

tools/deploy
    -> only then creates newly introduced leaf links
```

is not an atomic activation transaction.

For this specific migration, after the pull and before deployment:

```text
gl/env already became provider-neutral
VS Code and Obsidian launchers already required the new profile
gl-run already required the new profile
new profile live leaf was absent
```

Expected temporary behavior in that interval:

```text
VS Code GPU intent:
    profile unavailable
    -> CPU fallback

Obsidian GUI GPU intent:
    profile unavailable
    -> CPU fallback

gl-run:
    profile unavailable
    -> fail closed
```

This is safer than inheriting the incompatible bionic provider, but it is still a partially activated multi-file transaction.

## Immediate recovery/completion

The current transaction should be completed by running:

```text
tools/deploy
```

which creates the missing managed profile leaf and refreshes all managed links coherently to the current checkout.

No desktop-session restart is required for the link installation itself.

Existing already-running processes retain their launch environment and mapped objects; new launches consume the new composition.

## Architectural consequence

The repository currently uses source-linked deployment:

```text
live runtime leaf
    -> mutable checkout source file
```

This gives excellent source transparency and minimal duplication, but `git pull` is also an activation operation for every existing linked leaf.

Therefore:

```text
tools/deploy is not the sole activation boundary
```

for changes to already-linked files.

This matters whenever one transaction:

```text
changes existing consumers
and
adds a new required runtime leaf
```

because the consumer changes activate before the new leaf exists.

## Scope boundary

Do not redesign the whole deployment model before completing and validating the current scoped Vulkan transaction.

The immediate order is:

```text
1. install the missing profile leaf with tools/deploy
2. run a no-GUI live installation receipt
3. validate gl-run and Electron GPU/CPU workloads
4. close the current policy migration
5. then evaluate atomic activation models as a separate lifecycle problem
```

Potential future models include:

```text
immutable release directories plus one active symlink
materialized staged trees with atomic rename
commit-addressed deployment roots
transaction manifests with dependency ordering
```

No model is selected here.

The proven requirement is only:

```text
future multi-file promoted transactions need an activation boundary
stronger than independently mutable checkout symlinks
```

## Added live installation receipt

Added:

```text
experiments/glibc/vulkan-policy-composition/recipe/
    validate-live-vulkan-policy-installation.sh
```

Commit:

```text
da9b6529dca0c5c41651c01f6227880d86c87561
```

The receipt performs no GUI or rendering workload.

It validates:

```text
clean exact-HEAD checkout
all six managed live symlink targets
managed Freedreno ICD readability
baseline clears inherited bionic VK variables
explicit profile sets both variables to the exact glibc ICD
both loader variables are equal
profile implementation variable does not leak
```

Outputs:

```text
repository-root.txt
branch.txt
head.txt
summary.tsv
gates.tsv
baseline-environment.tsv
freedreno-profile-environment.tsv
live-targets.tsv
installation.status
```

## Post-deploy gate sequence

After `tools/deploy`:

```text
1. run live installation receipt
2. require installation.status=PASS
3. run gl-run renderer validation
4. run promoted VS Code GPU CDP identity validation
5. run promoted VS Code CPU policy/argv validation
6. run promoted Obsidian GPU and CPU validations
```

Do not move directly from deploy success to migration closure.

## Current state

```text
ownership audit:
    PASS

pre-deploy source/dry-run receipt:
    PASS

source transaction:
    IMPLEMENTED

existing linked leaves:
    ALREADY EXPOSE CURRENT SOURCE

new Freedreno profile live leaf:
    ABSENT AT CAPTURE TIME

live tools/deploy:
    NEXT IMMEDIATE STEP

live installation receipt:
    AFTER DEPLOY

rendering workload validation:
    BLOCKED ON INSTALLATION RECEIPT

atomic deployment lifecycle issue:
    OPEN, SEPARATE FROM CURRENT POLICY SEMANTICS
```

## Stop line

Do not:

```text
launch a GPU workload before installing the missing profile leaf
restart the whole desktop session merely to install the link
claim tools/deploy is the only activation boundary
redesign deployment before restoring and validating the current transaction
mark scoped Vulkan promotion complete
```

First complete the live leaf installation and run the no-GUI installation receipt.
