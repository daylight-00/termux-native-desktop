# Status

> **State:** active experiment and architecture hard-refactor preparation  
> **Updated:** 2026-07-10

## Working conclusions

- **The project is a native-first heterogeneous userspace composition system.** Android/Termux bionic remains the authoritative host; coherent foreign application domains are composed beside it through explicit bridges and ABI-appropriate capability providers.
- **No PRoot-mediated normal application runtime.** PRoot remains useful as a dependency solver, artifact/library warehouse, behavioral oracle, and debugging control. Selected passive rootfs data dependencies still exist and must be modeled explicitly rather than confused with PRoot process execution.
- **The glibc application world is viable for real desktop applications.** Official VS Code, extracted Obsidian, glibc Miniforge/Conda workloads, Zink OpenGL, and ANGLE-Vulkan paths have produced validated evidence under their recorded scopes.
- **Process ABI purity remains load-bearing.** Bionic and glibc processes may share kernel services and protocol bridges, but low-level runtime/library worlds must not be accidentally mixed.
- **Provider selection must be intentional and evidenced.** Configuration intent alone is insufficient; validation should capture actual selected or mapped provider identity.
- **The repository ownership refactor remains accepted.** The `refactor/module-package-layout` branch successfully separated application launchers, package lifecycles, experiment harnesses, shell/uv-base ownership, and deployment tooling. That ownership work should be kept and continued.
- **`modules/gl` is not accepted as a final semantic object.** It still groups world substrate/base policy, shared-library materialization, graphics capability policy, passive data policy, URL integration, and target-toolchain integration. Further lifecycle authority must not be added to that umbrella before semantic decomposition.
- **The current broad farm is transitional.** It remains useful as a research compatibility pool, control/reference mechanism, dependency-discovery aid, and migration baseline. It is not established as the permanent production provider architecture.
- **The post-refactor libdbus failure is a substrate/provider ABI incident, not a farm-generation problem.** The recorded active Debian-derived `libdbus-1.so.3` requires `__vsyslog_chk@GLIBC_2.17`, while the recorded installed Termux glibc 2.43 core does not export it. Rebuilding the same farm cannot repair a broken substrate ABI.
- **Substrate and provider lifecycles are independent.** Provider rollback does not restore an independently replaced glibc substrate. Real rollback claims must identify which bytes and which lifecycle domain are actually restored.
- **The concrete `0014` lifecycle implementation plan is paused.** Keep candidate-before-active-mutation, layered validation, receipts, and candidate→validate→promote principles; do not yet implement pacman-hook architecture, `gl-run` auto-sync, one global dirty fingerprint, or generational broad-farm activation.
- **Package-manager choice is below architecture.** The target is a backend-neutral glibc substrate supply adapter. Installing or switching pacman merely for hooks is rejected; pacman remains acceptable only if real device evidence establishes it as the chosen narrow substrate backend.
- **Minimum manipulation, maximum effect is an active design rule.** Preserve validated semantics, evidence, provenance, and rollback ability—not command names, facades, or directories merely because they already exist.

## Current architecture authority

Read in this order for current direction:

```text
docs/system-foundation/11-architecture-reassessment-and-hard-refactor-decision.md
    -> architectural rationale and decisions

docs/system-foundation/12-document-consistency-audit-and-execution-order.md
    -> cross-document consistency, settled/open matrix, and execution order

refactor/module-package-layout:docs/refactor/0015-architecture-reassessment-and-hard-refactor-direction.md
    -> branch-specific implementation consequence

refactor/module-package-layout:docs/refactor/0016-next-session-handoff.md
    -> operational entrypoint for the next development session
```

Earlier foundation and refactor documents remain valuable as evidence, analysis, and historical migration reasoning. Where tactics conflict, the precedence above applies.

## Current execution order

1. **Recover and freeze the ABI incident evidence.** Repair or replace the broken substrate, then run the core ABI regression gate, libdbus relocation regression gate, and VS Code real workload gate. Preserve identities and outputs.
2. **Reconcile main foundation and refactor-branch context deliberately.** The branches diverged after the recovered baseline; absence of a main-only document from the refactor branch does not make it architecturally irrelevant.
3. **Inventory and hard-split the current `gl` umbrella semantically.** Assign every file, environment variable, helper, and path assumption to a world, provider, bridge, toolchain, application family, specific application, validation owner, or supply adapter before physical movement.
4. **Establish actual substrate authority from the device.** Capture package database ownership, current update path, exact previous-artifact availability, real rollback ability, and install/config semantics before selecting a backend.
5. **Pilot one bounded selected shared-provider closure.** Keep the broad farm as a control; materialize selected provider bytes with provenance and validate the candidate in a context that proves actual candidate selection.
6. **Implement only the minimum lifecycle the corrected objects need.** Observe → receipt → candidate materialize → candidate validate → promote → rollback. Hooks remain optional optimizations.
7. **Use PyMOL as architecture proof.** Compose world, Python runtime, X11, OpenGL, font, and native-extension ABI contracts instead of copying legacy launcher/global-environment patterns.

## Implementation stop line

Until semantic inventory and substrate-authority evidence are complete, do not add architecture-changing implementation for:

```text
gl-sync
gl-status
gl-run auto-sync
pacman hooks as lifecycle authority
single global compatibility fingerprint
generational broad-farm activation
new global gl environment policy
```

Allowed work includes read-only inspection, identity capture, incident recovery, regression validation, semantic inventory, human-readable contracts, documentation reconciliation, and small discriminating experiments.

## Other open questions

- Hardware video decoding remains unresolved across the investigated MediaCodec/Vulkan, VA-API/V4L2, FFmpeg/mpv, and Chromium paths.
- Native Dawn WebGPU exposure remains unresolved: conventional Chromium/Electron GPU acceleration works, but the dedicated WebGPU investigation did not expose Turnip as the desired native WebGPU adapter.
- The exact long-term shared-library boundary remains open. The likely model is hybrid, but evidence must decide which providers are shared, app-local, or supplemental selected closure.
- Passive rootfs-backed fonts, locale, schemas, and shared data must be decided per capability.
- The exact glibc substrate backend remains open until device authority evidence is captured.
- A proper kgsl+Zink+X11 solution that removes the practical need for the `msm` backend remains worth watching upstream; the current `msm,kgsl` build is a validated local policy under its recorded scope.

## Evidence policy

A passing screenshot is not enough by itself. Claims stay at the strongest level directly supported by available evidence. Configuration does not prove provider selection, a generation name does not prove immutable bytes, and a provider rollback does not imply substrate rollback. Successful default-WSI presentation and ANGLE-Vulkan rendering remain recorded only at the scope actually demonstrated; complete end-to-end zero-copy presentation is not claimed without instrumentation that proves it.
