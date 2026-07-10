# 0022 — glibc 2.42 Recovery and Core-Gate False Negative

## Status

The active device performed the previously simulated bounded package-managed downgrade:

```text
glibc 2.43 -> 2.42
```

The package transaction completed successfully and the active libc identity matched the exact preserved 2.42 artifact.

One regression gate, `modules/gl/tests/core-abi.sh`, reported a false negative because of its shell pipeline structure. Provider relocation and VS Code CLI workload probes passed.

## 1. Preserved recovery artifact

The exact artifact was copied to persistent project state:

```text
$HOME/.local/state/termux-native-desktop/artifacts/glibc/glibc_2.42_aarch64.deb
```

Verified SHA-256:

```text
59e47a50b77ba9c0c1cc7cd0dafbb1558528cb544a740858faad0263e8b9b27f
```

## 2. Pre-recovery identity

```text
package:
    glibc 2.43 aarch64

libc SHA-256:
    e9e6d07732a00aa3c56ca8ca0a3ec9cf4a6c310ea3cad5ba5638f2cb21ac9d56

libc Build ID:
    44a096e6462274ee2203500197c7aa1adf5ef9a5

APT mark:
    auto
```

## 3. Local-artifact simulation

The preserved local `.deb` was simulated immediately before installation.

Operation set:

```text
Inst glibc [2.43] (2.42 ... local-deb [aarch64])
Conf glibc (2.42 ... local-deb [aarch64])
```

No removal operation was present.

## 4. Package-managed recovery transaction

APT/dpkg performed:

```text
dpkg: warning: downgrading glibc from 2.43 to 2.42
Unpacking glibc (2.42) over (2.43)
Setting up glibc (2.42)
```

The package retained its previous automatic-install mark.

## 5. Post-recovery substrate identity

```text
package:
    glibc 2.42 aarch64

libc SHA-256:
    665384fb6018e1a41ce21e542c6e7b4ee67850ec7292ce90329623b25a673834

libc Build ID:
    0b0a4cdb97355daecdb91d2915f61215924104c8
```

These identities exactly match the previously inspected 2.42 artifact.

## 6. Provider relocation validation

The independent active provider relocation gate passed:

```text
farm libdbus relocation: PASS
```

This is important because the original incident reproduced as:

```text
undefined symbol: __vsyslog_chk, version GLIBC_2.17
```

in this exact `libdbus` relocation path.

After substrate rollback, the undefined-symbol failure disappeared without rebuilding or changing the broad farm.

This directly validates that the incident boundary was substrate ABI, not provider farm generation.

## 7. VS Code CLI recovery validation

The VS Code CLI workload probe passed:

```text
1.127.0
4fe60c8b1cdac1c4c174f2fb180d0d758272d713
arm64
```

The CPU-path CLI probe also passed with the same identity output.

Non-fatal diagnostics remained:

```text
grep: /proc/version: Permission denied
warnings that several Chromium/Electron flags are not in the CLI known-option list
```

These are separate from the resolved ABI incident because execution continued and the workload identity probe completed successfully.

## 8. Core ABI gate false negative

The original gate used:

```bash
set -euo pipefail

if readelf --dyn-syms --wide "$LIBC" \
    | grep -qE '<symbol-pattern>'; then
    ...
fi
```

The active libc identity is byte-for-byte the same SHA-256 and Build ID as the previously inspected 2.42 artifact that showed:

```text
__vsyslog_chk@@GLIBC_2.17
```

Yet the script printed FAIL.

The failure mechanism is the interaction of:

```text
pipefail
+
grep -q early exit after match
+
producer readelf receiving SIGPIPE
```

Under `pipefail`, the producer's non-zero pipeline status can make the complete condition false even though `grep` found the symbol.

The test is changed to:

```text
readelf -> temporary complete symbol table file
grep -q -> regular file
```

This preserves both claims:

```text
readelf itself completed successfully
symbol pattern is present
```

without a short-circuit pipeline ambiguity.

## 9. Incident containment

The device applied:

```text
apt-mark hold glibc
```

Current APT policy after recovery:

```text
Installed: 2.42
Candidate: 2.43
```

The hold is classified only as temporary incident containment. It is not the architecture's substrate lifecycle mechanism.

## 10. Current recovery assessment

Evidence supports:

```text
SUBSTRATE_RECOVERED
PROVIDER_RELOCATION_VALID
VS_CODE_CLI_VALID
CORE_ABI_GATE_SCRIPT_FIXED_PENDING_RERUN
```

The remaining immediate action is to sync the fixed test and rerun:

```text
modules/gl/tests/core-abi.sh
modules/gl/tests/farm-libdbus-relocation.sh
code --version
```

After those pass together, the CLI-level incident recovery can be recorded as closed. Real GUI validation remains a separate workload gate.
