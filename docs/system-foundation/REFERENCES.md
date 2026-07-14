# System Foundation References

The target architecture is derived primarily from the project’s own experiments and current operational documents, interpreted using standard systems concepts documented in upstream specifications and manuals.

## Project-local source of truth

- [`../PROJECT_CONTEXT.md`](../PROJECT_CONTEXT.md) — motivation, evolution, and project boundary.
- [`../architecture.md`](../architecture.md) — current integrated system model.
- [`../glibc-layer.md`](../glibc-layer.md) — current glibc runtime model and onboarding procedure.
- [`../gpu.md`](../gpu.md) — current GPU build/runtime contract and evidence boundaries.
- [`../desktop-session.md`](../desktop-session.md) — current two-world session contract.
- [`../../STATUS.md`](../../STATUS.md) — current working conclusions and open questions.
- [`../../experiments/README.md`](../../experiments/README.md) — experiment provenance contract.
- [`../../setup/glibc/env`](../../setup/glibc/env) — current shared glibc environment implementation.
- [`../../setup/glibc/bin/gl-farm`](../../setup/glibc/bin/gl-farm) — current Debian library farm materialization.
- [`../../setup/glibc/bin/gl-run`](../../setup/glibc/bin/gl-run) — current glibc OpenGL/Zink capability wrapper.
- [`../../setup/glibc/bin/code`](../../setup/glibc/bin/code) — current VS Code launcher policy.
- [`../../scripts/deploy-gl.sh`](../../scripts/deploy-gl.sh) — current repository-to-live deployment linkage.

## External systems references

- Termux execution environment: <https://github.com/termux/termux-packages/wiki/Termux-execution-environment>
- Android storage model: <https://developer.android.com/training/data-storage>
- Linux kernel documentation: <https://docs.kernel.org/>
- Arm ABI specifications: <https://github.com/ARM-software/abi-aa>
- GNU C Library manual: <https://sourceware.org/glibc/manual/>
- ELF gABI reference: <https://refspecs.linuxfoundation.org/elf/gabi4+/contents.html>
- Mesa documentation: <https://docs.mesa3d.org/>
- Vulkan specification: <https://registry.khronos.org/vulkan/specs/latest/html/vkspec.html>

## Related knowledge set

The systems concepts used by this architecture are developed progressively in [`../knowledge/README.md`](../knowledge/README.md).
