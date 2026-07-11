# 0079 — Promoted gl-run Validator Prerequisite and Parser False Negatives

## Status

The first promoted `gl-run` renderer validation did not reach the build or OpenGL workload.

Observed terminal error:

```text
missing GLX probe build helper:
    experiments/glibc/vulkan-policy-composition/recipe/
        build-glx-renderer-probe.sh
```

No evidence files such as:

```text
summary.tsv
gates.tsv
renderer.stdout
renderer.stderr
validation.status
build.log
```

were created because the validator exited before creating its evidence directory.

Classification:

```text
promoted gl-run runtime:
    NOT TESTED

GLX probe build:
    NOT RUN

OpenGL context:
    NOT CREATED

renderer identity:
    NOT OBSERVED

failure class:
    VALIDATOR PREREQUISITE FALSE NEGATIVE
```

This is not evidence against the scoped Vulkan policy transaction, `gl-run`, Zink, Turnip, or the GLX consumer.

## Root cause 1 — executable-bit assumption

The validator invoked the historical helper with:

```text
bash "$BUILD_HELPER"
```

but checked it with:

```text
[ -x "$BUILD_HELPER" ]
```

Those contracts are inconsistent.

A shell source artifact passed explicitly to `bash` needs to be a readable regular file; it does not need its executable mode bit set.

The helper exists in the refactor branch at:

```text
experiments/glibc/vulkan-policy-composition/recipe/
    build-glx-renderer-probe.sh
```

The `-x` check therefore mislabeled a present non-executable source file as missing.

Correct contract:

```text
build helper:
    regular file required

promoted gl-run public entry point:
    executable required
```

## Root cause 2 — identity parser delimiter

Review of the GLX consumer source found a second latent false negative.

The consumer prints:

```text
GL_VENDOR=<value>
GL_RENDERER=<value>
GL_VERSION=<value>
```

The initial validator attempted to parse:

```text
GL_VENDOR: <value>
GL_RENDERER: <value>
GL_VERSION: <value>
```

using `": "` as the delimiter.

Even after the prerequisite check was bypassed, the validator would therefore have produced empty identity fields and failed:

```text
gl_vendor_present
gl_renderer_present
gl_version_present
renderer_is_zink
renderer_is_turnip_adreno
```

without reflecting the actual workload output.

The parser now consumes the first `=` delimiter and preserves the remaining value.

## Correction

Updated:

```text
experiments/glibc/vulkan-policy-composition/recipe/
    validate-promoted-gl-run-renderer.sh
```

Correction commit:

```text
b07f1b3fdc9a3addb29e4f3674539893cdec7b4e
```

Changes:

```text
build helper check:
    -x -> -f

GLX source check:
    added explicit -f prerequisite

identity parser:
    colon-delimited -> equals-delimited

receipt behavior:
    create evidence directory before prerequisite checks
    record prerequisite states in prerequisites.tsv
    write validation.status=FAIL for prerequisite failure
```

## Evidence hygiene

The failed evidence-root pathname from the first run may remain as an absent or empty path.

It must not be interpreted as a failed graphics workload because:

```text
no binary was built
no gl-run process executed
no GLX context was attempted
no renderer output existed
```

The corrected rerun must use a fresh evidence root so that the valid receipt cannot be confused with the pre-workload failure.

## Current gate state

```text
live scoped Vulkan installation:
    PASS

first promoted gl-run validator invocation:
    INVALID PRE-WORKLOAD FAILURE

corrected validator:
    READY

promoted gl-run renderer:
    RERUN REQUIRED

promoted VS Code GPU identity:
    BLOCKED ON VALID GL-RUN RECEIPT
```

## Stop line

Do not:

```text
patch executable bits manually in the live checkout
run the historical helper directly as an executable
reuse the failed evidence-root pathname
classify the result as a Zink or Turnip failure
proceed to the VS Code workload before a valid GLX receipt
```

Sync the correction and rerun the corrected validator with a new output root.
