# 0023 — CLI-Level ABI Incident Recovery Closed

## Status

The glibc/libdbus ABI incident is closed at the CLI workload level.

The strict recovery rerun completed successfully under:

```bash
set -euo pipefail
```

The current device state is:

```text
SUBSTRATE_RECOVERED
PROVIDER_RELOCATION_VALID
VS_CODE_GPU_CLI_VALID
VS_CODE_CPU_CLI_VALID
CLI_LEVEL_INCIDENT_CLOSED
```

Real GUI validation remains a separate workload gate.

## 1. Containment state

Current package state:

```text
glibc 2.42 aarch64
```

The package is held temporarily:

```text
apt-mark showhold
    glibc
```

This hold is incident containment only. It is not a permanent substrate lifecycle mechanism.

## 2. Strict core ABI gate

The corrected gate passed:

```text
glibc core ABI: PASS (__vsyslog_chk@GLIBC_2.17 exported)
```

This confirms that the active 2.42 substrate exports the ABI symbol required by the active Debian-derived `libdbus-1.so.3`.

## 3. Provider relocation gate

The active provider relocation gate passed:

```text
farm libdbus relocation: PASS
```

Observed resolution included:

```text
libsystemd.so.0 -> $HOME/gl/lib/libsystemd.so.0
libc.so.6      -> $PREFIX/glibc/lib/libc.so.6
libcap.so.2    -> $PREFIX/glibc/lib/libcap.so.2
libm.so.6      -> $PREFIX/glibc/lib/libm.so.6
```

The original undefined-symbol failure did not recur.

No broad-farm rebuild was performed between the failing 2.43 state and the recovered 2.42 state.

This provides direct operational evidence that the incident was caused by substrate ABI regression rather than farm regeneration state.

## 4. VS Code GPU-path CLI gate

The default launcher path completed successfully:

```text
1.127.0
4fe60c8b1cdac1c4c174f2fb180d0d758272d713
arm64
```

The launcher emitted non-fatal diagnostics:

```text
grep: /proc/version: Permission denied
warnings for Chromium/Electron flags that are not in the CLI known-option list
```

These diagnostics did not prevent execution and are outside the closed ABI incident claim.

## 5. VS Code CPU-path CLI gate

The explicit CPU path also completed successfully:

```text
1.127.0
4fe60c8b1cdac1c4c174f2fb180d0d758272d713
arm64
```

This validates that both launcher branches reach the recovered application workload at CLI probe level.

## 6. Strict aggregate gate

The rerun ended with:

```text
===== strict CLI recovery gate =====
PASS
```

Unlike the earlier recovery harness, this rerun used `set -euo pipefail`, and the core ABI gate itself had already been corrected to avoid `readelf | grep -q` SIGPIPE ambiguity.

Therefore the aggregate PASS is authoritative for the tested CLI-level claims.

## 7. Incident conclusion

The evidence chain is now:

```text
active glibc 2.43
    missing __vsyslog_chk@@GLIBC_2.17
        -> libdbus relocation failure
        -> VS Code symbol lookup failure

exact glibc 2.42 artifact
    exports __vsyslog_chk@@GLIBC_2.17

bounded package-managed downgrade
    glibc 2.43 -> 2.42 only

post-recovery
    core ABI gate PASS
    libdbus relocation gate PASS
    VS Code GPU-path CLI PASS
    VS Code CPU-path CLI PASS
```

The broad farm was not rebuilt during recovery.

## 8. What remains open

The following are not part of the closed CLI-level incident claim:

```text
real VS Code GUI interaction
window creation and rendering
actual Vulkan/ANGLE device selection
actual OpenGL/Zink workload validation
Chromium flag-warning cleanup
/proc/version permission diagnostic cleanup
long-term corrected latest substrate adoption
```

These must be tracked independently.

## 9. Next execution order

Proceed in this order:

```text
1. perform real VS Code GUI workload validation
2. preserve that workload evidence separately
3. keep the broad farm unchanged as control/reference
4. begin the bounded selected D-Bus closure pilot defined in 0019
5. do not introduce gl-sync, one global fingerprint, or broad-farm lifecycle machinery by inertia
```

The incident recovery and the selected-closure architecture experiment remain separate workstreams.
