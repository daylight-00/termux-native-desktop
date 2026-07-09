# mesa-26.1.4-present-sigbus

Status: **passed** (root cause found; fixed with a build option, zero patches)
Dates: 2026-07-04 → 07-05. First-hand record (this session).

## Question

Fresh vanilla Mesa 26.1.4 (glibc, Turnip/KGSL, zink) enumerates the GPU but
dies at first present. The 26.0.6 backup works. Version regression,
environment, or build configuration?

## Baseline

- 26.0.6 glibc backup (`~/opt/mesa-26-glibc`): zero-copy present verified —
  see experiments/gpu/mesa-glibc-26.0.6.
- bionic 26.1.4 (self-built, msm,kgsl): daily driver, works — see
  experiments/gpu/mesa-bionic-26.1.4.
- Failure signature (strace, evidence/): kgsl ioctls and fd-4 mmaps all
  succeed (one `= -1 ENODEV` ioctl is normal noise), `mesa_shader_cache`
  mmap OK, then thread-stack `mmap(8454144, … MAP_STACK)` → immediate
  `SIGBUS {si_code=BUS_ADRALN, si_addr=0x1}` — a jump through a
  garbage/near-null function pointer in a fresh thread.
- `MESA_VK_WSI_DEBUG=sw` masks it (GPU renders, software present) —
  i.e. the zero-copy present path specifically is broken.
- `TU_DEBUG=startup`: instance created, `/dev/kgsl-3d0` found, autotune
  init — driver bring-up is fine; death is later, at present.

## Procedure — including the wrong turns (they are the lessons)

**Round 1 — patch cargo-culting (failed).** Downloaded the termux-pacman
glibc-packages mesa patchset (gpkg/mesa via GitHub API). Selected by name:
applied `0011/0012 (freedreno-drm KGSL backend)`, `0013-fix-bad-syscall`,
`0015-termux-x11-kgsl`, `fix-for-anon-file`, `meson.build`,
`wsi-termux-x11-v3`; moved to `excluded/`: `0014-HACK-GL_ARB_timer_query`,
`enable-smoothLines`, `virgl-socket-path`. Applied with `git apply --3way`
onto 26.1.4 (patchset tracks ~24.x): **built clean on the first try** —
which was itself a bad sign. Result: vkcube default run now selected
**WSI platform: xlib** and SIGSEGV'd; forced `--wsi xcb` → same
BUS_ADRALN@0x1. Lesson: far-version 3-way merges produce plausible
nonsense silently; a clean apply proves nothing.

**Round 2 — targeted patches from the working bionic set (failed).**
`0007-use-mtx_t-operations-in-turnip` (touches tu_shader.cc) and
`0014-replace-turnip-wait_timestamp_safe-assert` (tu_knl_kgsl.cc), taken
already-rebased from the bionic 26.1.4 backup tree. Built as `-tx` prefix.
Death strace-identical to vanilla (diff of final syscalls = ASLR addresses
only). `0006-wsi-no-pthread_cancel` was staged as the next candidate but
**never tested** — pivoted to bisect (two misses = stop guessing).

**A/B isolation (decisive negative control):** same X server, same vkcube
binary, only the driver swapped via ICD: 26.0.6 backup GOOD, 26.1.4 BAD →
environment, termux-x11, loader all exonerated.

**Round A bisect — turnip-only runner, path-restricted (misleading).**
`git bisect start -- src/vulkan/wsi src/freedreno`, good=26.0.8,
bad=26.1.0(assumed): every step GOOD → "No testable commit found"
(+ a merge-base skip warning). Then 26.1.0 tested manually: **GOOD** —
the bad assumption itself was wrong.

**Round B bisect — turnip-only, no path filter, 26.1.0↔26.1.4:** every
step GOOD again; "converged" on `6dfbc555 VERSION: bump for 26.1.4` —
a one-line version-string commit. Logical impossibility → the insight:
same source at 26.1.4 was GOOD under the runner's config but BAD under the
kit's. **A bisect runner must reproduce the failing CONFIGURATION, not just
the failing version.** Confirmed by hand: 26.1.4 built turnip-only = GOOD.

**NEEDED diff:** full(zink) vs turnip-only turnip ICDs:
full additionally links `libxcb-dri3 / libxcb-present / libxcb-sync` and —
the one that matters — **libdrm**. Interim conclusion "zink breaks turnip"
was falsified by the bionic counter-example (bionic = zink+turnip, works);
reframed as build-graph/linkage (per advisor-session review, which also
pointed at the 26.1.0 relnotes: "meson: Add support for building zink +
Turnip/KGSL", "meson: Fix Turnip libdrm-linking check").

**Round C bisect — full-config runner (correct).** Runner judges by exit
code: 135 (128+SIGBUS(7)) = BAD, 137/124 (killed by timeout = survived) =
GOOD, 125 = build-skip. 26.1.4 reproduced BAD (rc=135). Bisect
good=26.0.8 bad=26.1.4, no path filter → **first bad commit `5d5857af`
"meson: Fix Turnip libdrm-linking check"** (Valentine Burley, MR 40302) —
whose own message says it stops incorrectly forcing a libdrm link when
zink is enabled in a KGSL-only build.

## Evidence — three-way libdrm table (decisive; readelf first-hand)

| build | `readelf -d \| grep libdrm` | result |
|---|---|---|
| 26.0.6 glibc backup | `libdrm.so.2` | works |
| 26.1.4 glibc, kgsl-only + zink | absent | SIGBUS |
| 26.1.4 glibc, **msm,kgsl** + zink | `libdrm.so.2` | works |
| bionic 26.1.4 (msm,kgsl) | `libdrm.so` | works |

Falsified hypothesis, kept for honesty: "unresolved
`tu_GetImageDrmFormatModifierPropertiesEXT` / `tu_SetHdrMetadataEXT`
relocations are the crash" — `readelf -r` shows the SAME zero-valued
R_AARCH64_ABS64 relocations in the WORKING full build. The exact crash
path from missing-libdrm to BUS_ADRALN remains **unproven**; a gdb attempt
failed structurally (bionic gdb cannot load the glibc world:
`libc.so: invalid ELF header`). Left open deliberately.

## Result

`-Dfreedreno-kmds=msm,kgsl` restores the libdrm linkage. Vanilla 26.1.4
then passes everything: vkcube zero-copy (no WSI env vars), VS Code GPU
(webgl2 → ANGLE/Turnip), zink OpenGL 4.6.

## Decision

`docs/decisions/0003-mesa-kmds-msm-kgsl.md`. `packages/mesa-glibc/build.sh` hard-codes msm,kgsl + post-install libdrm check pointing here. Upstream context: kgsl↛libdrm is a 2020 design ("turnip: Only link libdrm in the DRM case, not KGSL", Mesa 20.3); kgsl+X11 is a documented rough edge (24.2 relnotes); ecosystem alternative is the wsi-termux-x11(-only-kgsl) patch family — ours is the patch-free route. Not filed upstream as a new bug (known design; mechanism unproven). Diag runners are preserved under `recipe/`. Narrative: `docs/gpu.md`.

## Artifacts

- `evidence/` — strace captures (see CAPTURE.md), readelf outputs.
- `recipe/bisect-test.sh` and `recipe/bisect-test-full.sh` — preserved bisect judge harnesses.
- Runtime (outside repo, referenced): `~/opt/mesa-26-glibc` (26.0.6 A/B control), `~/gl/opt/mesa-glibc-26.1.4{,-turnip,-full}` (BAD / config proof / FIX), `~/ark/build/termux-packages` (bionic patchset backup).
