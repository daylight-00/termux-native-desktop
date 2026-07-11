# 0076 — Scoped Vulkan Policy Promotion Candidate

## Status

The exact-HEAD promoted Vulkan policy ownership audit passed.

Audit evidence root:

```text
$PREFIX/tmp/tnd-vulkan-policy-composition/
    promoted-vulkan-policy-ownership-v2-20260711-152652
```

Audited repository state:

```text
branch:
    refactor/module-package-layout

head:
    cd9f0369ff6054cff0e12291ea31446b28569d1b
```

Receipt:

```text
promoted_policy_reference_count=23
promoted_files_with_any_scanned_token=8
known_contract_failures=0
audit.status=PASS
```

The audit closes the static ownership-inventory gate and unblocks a promoted source transaction.

The transaction has now been implemented in the repository, but it has not yet been deployed to the live Termux paths.

## Audit classification

### Bionic desktop producer

```text
modules/desktop/overlay/home/.local/bin/startxfce-x11
```

is the bionic session producer.

It:

```text
exports the bionic Freedreno ICD through both VK variables
exports MESA_LOADER_DRIVER_OVERRIDE=zink for bionic GL clients
removes all client graphics overrides from the termux-x11 server process
```

This producer is correct for the bionic world and is not changed by the glibc policy migration.

The session script already states the ABI boundary explicitly:

```text
glibc launchers must replace or clear the inherited bionic Vulkan policy
before a glibc process can use it
```

### Glibc shared producer before the transaction

```text
modules/gl/overlay/home/gl/env
```

previously combined:

```text
inherited bionic-policy sanitation
and
explicit glibc Freedreno provider selection
```

by exporting both glibc ICD variables globally to every glibc launcher.

The audit confirms that this shared side effect fed multiple semantically different consumer classes.

### Direct glibc consumers

```text
modules/gl/overlay/home/gl/bin/gl-run
packages/vscode/launcher/code
packages/obsidian/launcher/obsidian-app
```

have direct provider-policy requirements.

Their requirements differ:

```text
gl-run:
    explicit Freedreno required
    Zink bridge required

VS Code GPU branch:
    explicit Freedreno required
    ANGLE Vulkan feature mode required

Obsidian GUI GPU branch:
    explicit Freedreno required
    ANGLE Vulkan feature mode required
```

### Provider-neutral glibc consumer

```text
packages/obsidian/launcher/obsidian
```

sources the shared glibc baseline but does not itself need to select a Vulkan provider. It bridges the registered Obsidian CLI and may communicate with an existing GUI process.

It should retain ABI sanitation without inheriting explicit provider selection.

### Non-runtime occurrence

```text
packages/mesa-glibc/build.sh
```

contains an operator-facing example that prints both explicit loader variables. It is not a promoted runtime-policy producer or application launch consumer.

The occurrence remains valid because explicit provider diagnostics still need both variables.

### Integrated documentation

The audit found current-provider assumptions in:

```text
docs/architecture.md
docs/desktop-session.md
docs/gpu.md
```

These documents required synchronized updates with the source transaction.

## Promoted semantic split

The transaction implements four separate responsibilities.

```text
1. bionic session provider policy
2. glibc ABI-boundary sanitation
3. explicit glibc Vulkan provider selection
4. consumer feature or bridge mode
```

### 1. Bionic session provider policy

Owner remains:

```text
modules/desktop/overlay/home/.local/bin/startxfce-x11
```

No source change was made.

### 2. Glibc ABI-boundary sanitation

Owner:

```text
modules/gl/overlay/home/gl/env
```

New contract:

```text
clear inherited VK_ICD_FILENAMES
clear inherited VK_DRIVER_FILES
never select a glibc Vulkan provider globally
```

The shared baseline still owns:

```text
DISPLAY/runtime directory
data/font/locale paths
Electron baseline policy
TLS paths
DBus sanitation
no LD_LIBRARY_PATH policy
```

### 3. Explicit glibc hardware-provider profile

New source-only semantic object:

```text
modules/gl/overlay/home/gl/policy/vulkan/freedreno.sh
```

Live path after deployment:

```text
$HOME/gl/policy/vulkan/freedreno.sh
```

Contract:

```text
source gl/env first

if the managed glibc Freedreno ICD is readable:
    export VK_ICD_FILENAMES=<glibc Freedreno ICD>
    export VK_DRIVER_FILES=<glibc Freedreno ICD>
    return success

otherwise:
    clear both variables
    return failure
```

The profile does not:

```text
discover providers
build or update Mesa
promote provider bytes
modify loader configuration
set Zink mode
set application GPU flags
```

It only applies one explicit provider-selection policy to the current launch composition.

### 4. Consumer composition

#### gl-run

New composition:

```text
source gl/env
source explicit Freedreno profile or fail
set MESA_LOADER_DRIVER_OVERRIDE=zink
execute target
```

`gl-run` remains a narrow OpenGL launch bridge. It does not become a provider manager.

#### VS Code

New composition:

```text
source gl/env

GL_GPU=1 and profile available:
    source explicit Freedreno profile
    enable ANGLE Vulkan flags

GL_GPU=0 or profile unavailable:
    keep both VK variables absent
    pass --disable-gpu
```

The launch flags are now represented as an array rather than one space-separated string, preserving argument boundaries.

#### Obsidian GUI

The GUI launcher now uses the same policy/feature split as VS Code.

#### Obsidian CLI

The CLI launcher remains unchanged. Because `gl/env` is now provider-neutral, it receives sanitation without provider selection.

## Source commits

Explicit provider profile:

```text
0c90178318171fe2be1ee361b0aafe8e603bd537
```

Provider-neutral glibc baseline:

```text
fab6f417885259490266afb5c87e996984f9185b
```

Consumer migration:

```text
72ab3ef36cf092714c1648b07617ae1331d54418  gl-run
050f1e370d06a060d15280bee7921cf3998da8f6  VS Code
cfc0a71da8d5b01802047246ed6706cb47a3c44e  Obsidian GUI
```

Repository tests:

```text
273198118ac1fcdcac6e19f26150e4064037ed07  policy-scope smoke
d7e8fe515ea6cd8dc87adc7e503bf0001ac7c820  deploy profile coverage
```

Integrated documentation:

```text
8871de11d0ac24f41e819fb5b6235b3c13c2314  gl module
0bc499a223b86b473c8f3eff4b40b31a586ee8e0  VS Code package
eb45bcc447b2276d66e6f296e3f7b876808f882e  Obsidian package
eb869c8499136ef61e7acb2d5f8cd013dad5ac10  architecture
cf5d375b15eff7f6f22a23cb3dde88c14e924f47  desktop session
8b05ae64a1dc929754240b820a52cb614263eeb3  GPU guide
4197fec8e594d7a1a88d7e33f1e69da8c101b667  glibc layer guide
```

The superseded first audit helper was removed from the current tree:

```text
d5d95e014f6a0fd85a098bc573f4cce3fd3a3799
```

Pre-deploy receipt helper:

```text
36c522272f96fb69678327c7576d457eb68ff64e
```

## Repository smoke tests

Added:

```text
tests/repository/vulkan-policy-scope-smoke.sh
```

The test uses isolated fake consumers and a fake readable ICD manifest. It verifies:

```text
VS Code CPU mode:
    inherited bionic VK variables removed
    --disable-gpu present
    ANGLE Vulkan flag absent

VS Code GPU mode:
    both variables point to the glibc profile ICD
    ANGLE Vulkan flag present
    --disable-gpu absent

Obsidian CPU/GPU modes:
    same policy split

Obsidian CLI:
    inherited bionic policy removed
    no explicit provider selected

gl-run:
    explicit profile applied
    Zink override applied

missing provider:
    Electron launcher falls back to CPU mode
    gl-run fails closed
```

Added deploy-smoke coverage verifies that:

```text
$HOME/gl/policy/vulkan/freedreno.sh
```

is installed as a managed leaf symlink by `tools/deploy`.

## Assistant-side sandbox result

The changed source and test contents were reconstructed in an isolated local sandbox.

Observed:

```text
vulkan policy scope smoke: PASS
deploy smoke test: PASS
```

This validates shell behavior and repository deployment mechanics in a generic Linux sandbox.

It does not replace authoritative validation on the real Termux/Android device.

## Added pre-deploy gate

Added:

```text
experiments/glibc/vulkan-policy-composition/recipe/
    validate-promoted-vulkan-policy-transaction.sh
```

The gate performs no deployment.

It requires:

```text
clean tracked working tree
exact branch/HEAD receipt
```

It runs:

```text
shell syntax checks
policy-scope repository smoke
deploy repository smoke
live tools/deploy --dry-run
source-contract checks
dry-run target checks
current live-target inventory
```

Outputs:

```text
repository-root.txt
branch.txt
head.txt
summary.tsv
gates.tsv
current-live-targets.tsv
shell-syntax.log
policy-scope-smoke.log
deploy-smoke.log
live-deploy-dry-run.log
predeploy.status
```

A PASS means the source transaction and dry-run plan are ready for a separate explicit live deployment step.

It does not deploy or launch applications.

## Required real-device sequence

```text
1. sync exact branch
2. run pre-deploy gate
3. inspect all gates and live target state
4. if PASS, run tools/deploy
5. validate live baseline/profile environment contracts
6. validate gl-run renderer
7. validate VS Code GPU primary identity
8. validate VS Code CPU environment/argv behavior
9. validate Obsidian GPU and CPU controls
10. only then mark the migration promoted and closed
```

## Rollback model

The live files are managed symlinks into the checkout.

Before deployment, the old checkout commit remains the rollback reference.

A rollback must restore a coherent set:

```text
gl/env
gl-run
VS Code launcher
Obsidian GUI launcher
provider profile presence/absence
integrated docs are repository state only
```

Do not roll back only `gl/env` while leaving migrated launchers, or vice versa. The baseline and consumers form one transaction.

## Current gate state

```text
exact-HEAD ownership audit:
    PASS

VS Code provider/device causal evidence:
    PASS

promoted source transaction:
    IMPLEMENTED IN REPOSITORY

repository policy-scope smoke:
    PASS IN ASSISTANT SANDBOX

repository deploy smoke:
    PASS IN ASSISTANT SANDBOX

real-device pre-deploy gate:
    NEXT

live tools/deploy:
    NOT RUN

live GPU/CPU workload validation:
    NOT RUN
```

## Stop line

Do not yet:

```text
run tools/deploy without the pre-deploy receipt
restart the desktop session
change startxfce-x11
remove the bionic session provider policy
remove historical experiment evidence
mark the migration complete
```

First run the no-mutation pre-deploy gate on the real checkout.
