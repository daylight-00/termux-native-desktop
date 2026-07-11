# Selected Obsidian AppDir Closure Pilot

## Status

```text
ACTIVE_ARCHITECTURE_DISCRIMINATION
PHASE_B1_B8_CLOSED
PHASE_B9_PASS
PHASE_B10_SHORT_PATH_TOPOLOGY_PASS
PHASE_B10_PREVIOUS_FAILURE_INTERACTION_TRIGGERED
PIXBUF_ICON_MIME_INVENTORY_PASS
PASSIVE_NO_INPUT_B10_NEXT
INTERACTIVE_VAULT_OPEN_CAPABILITY_OPEN
```

The immutable generation exists and remains unactivated.

## Closed generation

```text
generation ID:
    obsidian-cpu-435ac66d15de2e9a3188

content objects:
    96

content bytes:
    70,897,301

generation aliases:
    175

staged/final validation:
    1851 / 1851 PASS

current:
    ABSENT
```

## Corrected Phase B10 interpretation

The short-runtime run displayed the Obsidian initial window and formed the required CPU topology.

```text
main:
    1

renderer:
    1

zygote:
    3

utility:
    1

GPU process:
    0
```

The operator then clicked the vault-open control. The fatal GTK icon/pixbuf chain occurred after that interaction.

Therefore:

```text
passive idle initial-window survival:
    OPEN / previous run was perturbed

interactive vault-open capability:
    FAIL / GTK file-chooser path
```

The capture scripts do not record mouse input. The click timing is operator evidence and is documented separately from machine evidence.

## Pixbuf/icon/MIME inventory

Authoritative receipt:

```text
selected-obsidian-gtk-pixbuf-runtime-capability-inventory-20260712-014314
```

Archive SHA-256:

```text
e9f5fc256dbbe74e6b060fb8ebfde8745959321d20a58f8d7bd4181d19be3be6
```

Result:

```text
analysis.status:
    PASS

next-state:
    READY_FOR_CONTROLLED_PIXBUF_RUNTIME_DIAGNOSTIC

loader caches:
    1

loader modules:
    12

cache references:
    12

written /usr module paths present natively:
    0

rootfs-prefixed modules present:
    12

icon-theme indexes:
    2

MIME database files:
    5

paths absent from B9 semantic manifest:
    20
```

The rootfs cache is generated and references FHS absolute `/usr/lib/...` paths. It cannot be used unchanged in the native namespace. A later diagnostic must create a receipt-local relocated cache.

The inventory does not prove that all twelve modules, both icon themes, or all five MIME files belong in the final generation.

## Claim split

### Passive explicit-generation B10

```text
operator action:
    observe only

forbidden:
    click Open vault
    click Create vault
    interact with any GUI control

required:
    topology PASS
    100-second survival PASS
    maps capture PASS
    exact immutable mapped-identity analysis PASS
```

Wrapper:

```text
recipe/run-passive-explicit-generation-cpu-validation.sh
```

### Interactive vault-open capability

```text
operator action:
    click the vault-open control once

required capability:
    GTK file chooser
    pixbuf loader registry
    icon-theme data
    MIME data

current result:
    FAIL
```

This will be tested only after the passive claim is closed.

## Canonical passive command

```bash
cd "$HOME/projects/termux-native-desktop"

rm -rf \
  experiments/glibc/selected-obsidian-closure/recipe/__pycache__

git fetch origin
git merge --ff-only origin/docs/post-graphics-architecture-audit

B9_OUT="$PREFIX/tmp/selected-obsidian-closure/selected-obsidian-phase-b9-generation-publication-corrected-20260712-003136"

out="selected-obsidian-phase-b10-passive-short-runtime-cpu-validation-$(date +%Y%m%d-%H%M%S)"
OUT="$PREFIX/tmp/selected-obsidian-closure/$out"

if B9_OUT="$B9_OUT" \
   OUT="$OUT" \
   bash \
     experiments/glibc/selected-obsidian-closure/recipe/run-passive-explicit-generation-cpu-validation.sh
then
  analysis_rc=0
else
  analysis_rc=$?
fi

printf '\n===== analysis exit status =====\n'
printf '%s\n' "$analysis_rc"

for f in \
  "$OUT/interaction-contract.tsv" \
  "$OUT/analysis.status" \
  "$OUT/failure-stage.txt" \
  "$OUT/next-state.txt" \
  "$OUT/summary.tsv" \
  "$OUT/runtime-root-contract.tsv" \
  "$OUT/runtime-snapshot.tsv" \
  "$OUT/runtime-cleanup.status" \
  "$OUT/capture-exit-status.txt" \
  "$OUT/process-contract.tsv" \
  "$OUT/missing-expected-mapped-paths.tsv" \
  "$OUT/unexpected-mapped-paths.tsv" \
  "$OUT/mapped-identity-verification.tsv" \
  "$OUT/mapped-path-classification.tsv" \
  "$OUT/current-state-before.tsv" \
  "$OUT/current-state-after.tsv" \
  "$OUT/capture/class-counts.tsv" \
  "$OUT/capture/processes.tsv" \
  "$OUT/capture/launch.stdout" \
  "$OUT/capture/launch.stderr" \
  "$OUT/claim-boundary.txt"
do
  [ -e "$f" ] || continue
  printf '\n===== %s =====\n' "$f"
  cat "$f"
done

tar czf ~/Downloads/$out.tgz $OUT
```

## Operator instruction

During this passive run:

```text
Do not click anything in the Obsidian window.
Do not open or create a vault.
Observe only until the terminal reports completion.
```

## Expected PASS state

```text
analysis.status:
    PASS

next-state:
    READY_FOR_ATOMIC_ACTIVATION_IMPLEMENTATION
```

That next-state applies only to the passive runtime/identity claim. The interactive vault-open capability must still close before practical promotion.

## Stop line

Do not:

```text
rerun Phase B1-B9;
interact with the GUI during the passive run;
mutate the immutable generation;
copy all inventory paths wholesale;
use the rootfs loaders.cache unchanged;
create current;
change the promoted launcher;
claim practical Obsidian usability from passive PASS alone.
```
