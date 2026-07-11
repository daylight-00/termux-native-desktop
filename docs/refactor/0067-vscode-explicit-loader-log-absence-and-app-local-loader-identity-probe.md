# 0067 — VS Code Explicit Loader-Log Absence and App-Local Loader Identity Probe

## Status

The corrected dual-stream loader summarizer has been run against the existing VS Code explicit-Freedreno control evidence.

Result:

```text
launch.stdout:
    0 bytes
    loader signal lines: 0
    selected driver lines: 0

launch.stderr:
    713 bytes
    loader signal lines: 2
    selected driver lines: 0
```

The aggregate loader-selection parser still reports:

```text
loader_version_lines          0
icd_manifest_lines            0
physical_device_sort_lines    0
driver_removal_lines          0
selected_driver_lines         0
llvmpipe_lines                0
turnip_lines                  0
gfxstream_lines               0
lvp_lines                     0
```

Therefore the corrected observer result is:

```text
selected-provider evidence from VK_LOADER_DEBUG:
    NOT OBSERVED IN CAPTURED STDOUT OR STDERR
```

This is not evidence that Vulkan did not run.

The same control independently proves that the VS Code GPU process maps:

```text
app-local libEGL.so
app-local libGLESv2.so
app-local libvulkan.so.1
provider-store libvulkan_freedreno.so
/dev/kgsl-3d0
```

The remaining question is why the app-local Vulkan-facing path did not emit desktop-loader debug output into the captured streams.

## Evidence root

```text
$PREFIX/tmp/tnd-vulkan-policy-composition/vscode-explicit-adopted-20260711-134601
```

No new workload run was performed for this result.

## Corrected observer interpretation

The dual-stream correction established that the original empty selection summary was not caused only by reading stderr instead of stdout.

Observed:

```text
stdout bytes:
    0

stdout loader signals:
    0

stderr selected-driver lines:
    0
```

The two broad-pattern matches in stderr are not sufficient to classify provider selection. The parser deliberately distinguishes:

```text
broad signal pattern match
```

from:

```text
Using "<device>" with driver: "<path>"
```

and the second category is empty.

The next probe records the exact two broad-pattern lines so that launcher environment echo output can be separated from true loader diagnostics.

## Why the result remains an observer question

The control already passed:

```text
causal main adoption
Electron topology
60-second survival
final process map capture
GPU -> provider-store Freedreno relation
GPU -> KGSL relation
```

Therefore the unresolved question is narrower:

```text
what is the identity and debug behavior of
$HOME/gl/apps/vscode/libvulkan.so.1
in this Electron/ANGLE control?
```

The runtime payload is external and not tracked in Git. The package integration documentation already treats the live VS Code payload under `$HOME/gl/apps/vscode` as an external application payload whose complete source identity and checksum provenance still need a future package-completion pass.

That makes direct device identity capture the correct next evidence step.

## New bounded identity probe

Added:

```text
experiments/glibc/vulkan-policy-composition/recipe/
    probe-vscode-app-local-vulkan-loader.sh
```

Commit:

```text
88ecb7f5fb7c4d675e358a29f55c40fb9f6e9def
```

The probe is read-only with respect to runtime state.

It records:

```text
1. exact path and resolved path
2. byte size
3. SHA-256
4. ELF build ID
5. SONAME
6. presence of VK_LOADER_DEBUG string
7. presence of Vulkan Loader Version string
8. comparison with available farm/prefix/rootfs libvulkan.so.1 candidates
9. Vulkan loader entry-point symbols
10. exact broad-pattern lines from the stored control stdout/stderr
```

Outputs:

```text
candidate-identities.tsv
app-comparisons.tsv
app-local-dynamic-section.txt
app-local-notes.txt
app-local-dynamic-symbols.txt
app-local-loader-debug-strings.txt
app-local-loader-entrypoints.txt
control-observer-signal-lines.tsv
```

## Evidence questions

The next probe answers four bounded questions.

### Q1 — Is the app-local libvulkan a byte-identical copy of another known loader candidate?

Possible outcomes:

```text
same SHA / same build ID
    -> app-local path is a relocated copy or alias-equivalent object

different SHA / different build ID
    -> consumer-local loader identity is distinct
```

### Q2 — Does the app-local object contain desktop-loader debug capability markers?

The probe records strings such as:

```text
VK_LOADER_DEBUG
Vulkan Loader Version
[Vulkan Loader]
```

String presence is supporting identity evidence, not a complete behavioral proof.

### Q3 — Does the app-local object expose the expected Vulkan loader-facing entry points?

The probe records symbol-table lines for:

```text
vkGetInstanceProcAddr
vkCreateInstance
vkEnumerateInstanceExtensionProperties
vkEnumerateInstanceLayerProperties
```

This distinguishes a loader-shaped object from an arbitrary Vulkan-related support library.

### Q4 — What exactly were the two stderr broad-pattern matches?

The stored evidence is rescanned and the exact matching lines are recorded with stream identity and line number.

This prevents launcher policy echo text from being misclassified as loader diagnostics.

## Decision boundary after the identity probe

### Outcome A — app-local object is the same as a known desktop loader and contains debug markers

Then the next question is process/stream propagation or loader initialization behavior inside Electron/ANGLE.

Use one bounded consumer-specific observation probe before any invasive tracing.

### Outcome B — app-local object differs from the known glibc/rootfs desktop loaders

Then treat the app-local loader as a distinct consumer-local component.

Do not assume that environment/debug behavior from the standalone desktop loader applies unchanged.

Investigate its provenance and behavior contract before designing selection evidence.

### Outcome C — app-local object lacks desktop-loader debug markers but maps the explicit ICD

Then `VK_LOADER_DEBUG` is not a valid selection observer for this consumer-local path.

Use an alternative bounded consumer-level evidence source rather than repeating the same environment-only experiment.

## Current gate state

```text
VS Code explicit control workload:
    PASS

GPU process -> Freedreno:
    PASS

GPU process -> KGSL:
    PASS

VK_LOADER_DEBUG selection output:
    ABSENT FROM CAPTURED STREAMS

app-local Vulkan loader identity:
    NEXT BOUNDED GATE

loader-selected provider identity:
    OPEN

VS Code implicit-discovery control:
    BLOCKED UNTIL EXPLICIT INTERPRETATION IS CLOSED OR THE CLAIM BOUNDARY IS DELIBERATELY REVISED
```

## Stop line

Do not yet:

```text
rerun the 60-second control blindly
run the implicit-discovery VS Code control
change the promoted VS Code launcher
change shared gl/env
add global Vulkan policy
add invasive tracing
infer selected provider solely from map presence
```

First identify the actual consumer-local Vulkan loader object and its observer capabilities.
