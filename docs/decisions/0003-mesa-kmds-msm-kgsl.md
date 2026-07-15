# 0003 — Mesa is built with -Dfreedreno-kmds=msm,kgsl (never kgsl alone)

Date: 2026-07-05

## Status

Accepted for the validated Mesa build scope.

## Decision
All glibc Mesa builds include the msm KMD alongside kgsl, even though only
kgsl is used at runtime (/dev/kgsl-3d0, stock Android kernel).

## Context
Upstream commit 5d5857af (26.1.x) stops linking libdrm in KGSL-only zink
builds — by design (dates to Mesa 20.3: "Only link libdrm in the DRM case").
Without libdrm the x11 present path dies (SIGBUS BUS_ADRALN@0x1). Including
msm makes libdrm a hard dependency again; the msm backend is inert at
runtime. This matches the bionic Termux package config, which is why bionic
never showed the bug. Evidence: three-way NEEDED table in
experiments/gpu/mesa-26.1.4-present-sigbus.

## Consequences
- build-mesa.sh hard-codes msm,kgsl and warns post-install if libdrm is
  missing from the turnip ICD.
- Watch upstream for a proper kgsl+zink+x11 fix that would remove the need.
- Exact crash mechanism intentionally left unproven (glibc gdb required).
