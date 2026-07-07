# Status

## Working conclusions
- proot runtime rejected: measured I/O cost (VS Code)
- glibc layer viable: patchelf + Termux-glibc core + Debian rootfs farm
- GPU: Mesa 26.1.4 vanilla works iff -Dfreedreno-kmds=msm,kgsl (kgsl-only drops libdrm -> present SIGBUS)
- Electron (VS Code, Obsidian) fully working w/ ANGLE-Vulkan zero-copy
- Zink OpenGL 4.6 available (gl-run)

## Current focus
- [ ] repo restructure + first push
- [ ] docs backfill (background/timeline, decisions/)
- [ ] PyMOL pilot (glibc + Qt + zink)
