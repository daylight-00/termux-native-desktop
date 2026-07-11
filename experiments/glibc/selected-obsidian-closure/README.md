# Selected Obsidian AppDir Closure Pilot

## Status

```text
PHASE_B1_B8_CLOSED
PHASE_B9_PASS
PASSIVE_B10_TOPOLOGY_PASS
PASSIVE_B10_100_SECOND_SURVIVAL_PASS
PASSIVE_B10_MAPS_CAPTURE_PASS
PASSIVE_B10_MAPPED_IDENTITY_FAIL
INTERACTIVE_VAULT_OPEN_CAPABILITY_OPEN
CPU_MAP_CONTRACT_DIAGNOSTIC_NEXT
```

The immutable generation remains published but unactivated.

## Passive B10 receipt

```text
selected-obsidian-phase-b10-passive-short-runtime-cpu-validation-20260712-015859
```

```text
archive SHA-256:
    86330e210a0171fd1bf059eec600cc92eac963b0e468538be77b8819214905af

captured head:
    3b7cc1f4f33852f273bda77d681d035a5c3be668

operator input:
    NONE

analysis.status:
    FAIL

failure stage:
    mapped_identity

topology / survival / maps:
    PASS / PASS / PASS

current before / after:
    ABSENT / ABSENT
```

Stable process topology:

```text
main       1
zygote     3
utility    1
renderer   1
GPU        0
```

## Map result

```text
unique mapped regular objects:
    143

selected object-store identities:
    93 / 96

expected app-local references:
    11 / 11

expected protected-world references:
    18 / 18
```

Selected content by kind:

```text
ELF:
    89 / 91 mapped from selected objects

fonts:
    3 / 4 mapped

GSettings aggregate:
    1 / 1 mapped
```

Missing selected objects:

```text
libXdmcp.so.6.0.0
DejaVuSansMono-Bold.ttf
libXau.so.6.0.0
```

The font is demand-unmapped and must not be treated as a loader failure.

The two ELF source paths were mapped from the world prefix instead:

```text
$PREFIX/glibc/lib/libXdmcp.so.6.0.0
$PREFIX/glibc/lib/libXau.so.6.0.0
```

Four selected copied consumers retain absolute DT_RPATH:

```text
libxcb-render.so.0.0.0
libXrandr.so.2.2.0
libXrender.so.1.3.0
libxcb-shm.so.0.0.0

DT_RPATH:
    $PREFIX/glibc/lib
```

Additional CPU-map exceptions:

```text
excluded semantic mapping:
    $PREFIX/glibc/lib/libX11-xcb.so.1.0.0

unmodelled app-local mapping:
    $HOME/gl/apps/obsidian/libvk_swiftshader.so
```

Clean negative boundaries:

```text
broad farm:
    0

rootfs provider:
    0

current:
    0
```

## Next stage

Recipe:

```text
recipe/analyze-passive-map-selection-diagnostic.py
```

This is read-only. It consumes the retained B1/B2 graph, B9 generation receipt, and passive B10 maps receipt.

It will:

```text
rehash all 96 selected objects;
rehash mapped source substitutes;
record selected map state by content kind;
record four absolute-RPATH selected consumers;
join retained edges to bypassed providers;
record libX11-xcb and libvk_swiftshader identities;
separate demand-loaded data from required selected ELF;
perform no launch and no mutation.
```

Expected next state:

```text
READY_FOR_CPU_MAP_CONTRACT_REDESIGN
```

## Canonical command

```bash
cd "$HOME/projects/termux-native-desktop"

rm -rf \
  experiments/glibc/selected-obsidian-closure/recipe/__pycache__

git fetch origin
git merge --ff-only origin/docs/post-graphics-architecture-audit

B1_OUT="$PREFIX/tmp/selected-obsidian-closure/selected-obsidian-phase-b1-retained-control-locality-20260711-192919"
B2_OUT="$PREFIX/tmp/selected-obsidian-closure/selected-obsidian-phase-b2-static-runtime-closure-20260711-195310"
B9_OUT="$PREFIX/tmp/selected-obsidian-closure/selected-obsidian-phase-b9-generation-publication-corrected-20260712-003136"
B10_OUT="$PREFIX/tmp/selected-obsidian-closure/selected-obsidian-phase-b10-passive-short-runtime-cpu-validation-20260712-015859"

out="selected-obsidian-passive-map-selection-diagnostic-$(date +%Y%m%d-%H%M%S)"
OUT="$PREFIX/tmp/selected-obsidian-closure/$out"

if B1_OUT="$B1_OUT" \
   B2_OUT="$B2_OUT" \
   B9_OUT="$B9_OUT" \
   B10_OUT="$B10_OUT" \
   OUT="$OUT" \
   python \
     experiments/glibc/selected-obsidian-closure/recipe/analyze-passive-map-selection-diagnostic.py
then
  analysis_rc=0
else
  analysis_rc=$?
fi

printf '\n===== analysis exit status =====\n'
printf '%s\n' "$analysis_rc"

for f in \
  "$OUT/analysis.status" \
  "$OUT/failure-stage.txt" \
  "$OUT/next-state.txt" \
  "$OUT/summary.tsv" \
  "$OUT/input-verification.tsv" \
  "$OUT/selected-map-state.tsv" \
  "$OUT/selected-rpath-consumers.tsv" \
  "$OUT/rpath-provider-edges.tsv" \
  "$OUT/cpu-map-exceptions.tsv" \
  "$OUT/mapped-path-classification.tsv" \
  "$OUT/live-identity-verification.tsv" \
  "$OUT/claim-boundary.txt"
do
  [ -e "$f" ] || continue
  printf '\n===== %s =====\n' "$f"
  cat "$f"
done

tar czf ~/Downloads/$out.tgz $OUT
```

## Stop line

Do not:

```text
claim overall B10 PASS;
activate current;
mutate or patch the existing generation;
change RPATH before the diagnostic;
classify demand-unmapped fonts as loader failures;
ignore graphics-related mappings in CPU mode;
proceed to atomic activation.
```
