# 0024 — VS Code GUI Recovery Validation Passed

## Status

The real VS Code GUI workload was launched after the CLI-level ABI incident recovery had already passed strict substrate, provider-relocation, and CLI gates.

The user directly confirmed that the application executed normally.

The GUI recovery gate is therefore recorded as:

```text
VS_CODE_GUI_WORKLOAD_VALID
ABI_INCIDENT_RECOVERY_COMPLETE_FOR_TESTED_VSCODE_WORKLOAD
```

Graphics-provider selection remains a separate evidence claim.

## 1. Display-server state

Before launch, the device reported:

```text
DISPLAY=:1
```

A live Termux:X11 server process was present:

```text
termux-x11 com.termux.x11 :1
```

No `xfce4-session` process was observed at that moment.

This did not prevent the standalone VS Code GUI workload from opening and operating normally.

## 2. Launch command

The application was launched through the promoted public entrypoint:

```text
code --new-window $HOME/termux-native-desktop
```

stdout and stderr were captured under:

```text
$PREFIX/tmp/vscode-gui-recovery-20260710-190109/
```

## 3. Launcher-process behavior

The background shell job associated with the launcher exited after spawning/handing off to the persistent application process set.

After the launcher job reported `Done`, `pgrep` still observed the live VS Code process tree.

Therefore the shell job completion was not application failure.

## 4. Observed process tree

The persistent process set included:

```text
main VS Code process
zygote processes
chrome_crashpad_handler
GPU process
network utility process
renderer process
```

The main process command line included the expected project path:

```text
--new-window $HOME/termux-native-desktop
```

This confirms that the promoted launcher reached the real GUI application workload rather than only completing a CLI metadata path.

## 5. Observed GPU-process state

A live Electron/Chromium GPU process was observed.

Its command line included:

```text
--type=gpu-process
--use-angle=vulkan
--use-gl=angle
--enable-features=...Vulkan
```

The main and utility processes also carried Vulkan/ANGLE-related configuration arguments.

This proves:

```text
GPU process creation
Vulkan/ANGLE launch configuration propagation
application process survival under that configuration
```

It does **not** by itself prove:

```text
which Vulkan ICD JSON was actually opened
which Vulkan physical device/adapter was selected
which Mesa/Turnip shared objects were mapped
whether fallback or alternate provider selection occurred internally
```

Those remain separate graphics-provider-selection claims and require candidate/provider-specific evidence such as loader trace, file-open trace, mapped-object identity, or application diagnostics.

## 6. Renderer and utility process state

A renderer process and a network utility process were observed alive under the same VS Code user-data directory and application payload.

This establishes that the recovered workload progressed beyond the original startup relocation failure into a normal multiprocess Electron application state.

## 7. User-observed workload result

The user reported that VS Code executed normally.

This is accepted as direct GUI workload evidence for:

```text
window creation
visible application startup
normal basic application operation
```

The claim is intentionally bounded. No stronger graphics-backend or long-duration stability claim is inferred solely from successful visible execution.

## 8. Remaining stderr diagnostics

Captured stderr contained:

```text
grep: /proc/version: Permission denied
```

and warnings that several passed Chromium/Electron flags were not in the CLI known-option list:

```text
ignore-gpu-blocklist
enable-features
use-gl
use-angle
disable-gpu-vsync
```

The application nevertheless launched normally and produced a persistent main/GPU/utility/renderer process set.

Therefore these diagnostics are not part of the closed ABI incident.

They remain candidates for later launcher-quality and graphics-configuration cleanup, but should not be mixed into substrate recovery.

## 9. Incident closure conclusion

The full observed recovery chain is now:

```text
broken glibc 2.43 substrate
    -> missing __vsyslog_chk@@GLIBC_2.17
    -> libdbus relocation failure
    -> VS Code startup failure

exact glibc 2.42 recovery artifact
    -> required symbol present

bounded package-managed rollback
    -> glibc only

strict post-recovery validation
    -> core ABI PASS
    -> libdbus relocation PASS
    -> VS Code GPU-path CLI PASS
    -> VS Code CPU-path CLI PASS

real GUI validation
    -> persistent Electron process tree
    -> live GPU process
    -> renderer/utility processes
    -> user-confirmed normal execution
```

The broad farm was not rebuilt during this recovery sequence.

The tested VS Code workload is therefore recovered.

## 10. Next architecture step

The ABI incident recovery workstream is complete for the tested VS Code workload.

Next work should remain separated into:

```text
A. graphics-provider actual-selection evidence
    optional/independent validation track

B. bounded selected D-Bus provider-closure pilot
    architecture discrimination track defined by 0019
```

Do not use the successful recovery as justification to reintroduce:

```text
gl-sync
one global dirty fingerprint
broad-farm lifecycle automation
gl-run as a universal lifecycle gateway
```

The selected-closure pilot should now proceed from the recovered substrate while preserving the broad farm unchanged as control/reference.
