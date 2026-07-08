# Code OSS Remote Development over SSH with Open Remote - SSH

## Experiment Report

**Experiment date:** 2026-06-30  
**Report prepared:** 2026-07-08  
**Client environment:** Native Code - OSS running inside Termux/Android  
**Remote host:** `victor`, an existing Ubuntu x86_64 server  
**Extension under test:** `jeanp413.open-remote-ssh`  
**Installed extension build observed in logs:** `0.1.2-universal`  
**Status at the end of this report:** Connection failure reproduced and root cause narrowed to the remote-server download/version-selection path. A proposed extension upgrade and explicit compatible REH version have not yet been validated in the experiment.

---

## 1. Purpose

The purpose of this experiment was to replace Microsoft's proprietary Remote - SSH extension with an open alternative that can be used from Code - OSS.

The selected candidate was:

```text
jeanp413.open-remote-ssh
```

The intended topology was:

```text
Android / Termux
└── native Code - OSS
    └── Open Remote - SSH
        └── SSH connection
            └── victor
                ├── Ubuntu
                ├── x86_64
                ├── existing Microsoft VS Code remote installation
                │   └── ~/.vscode-server
                └── separate Code OSS / Open Remote - SSH server installation
```

A major constraint was that `victor` already contained a working `~/.vscode-server` installation used by another VS Code Remote - SSH workflow. That installation was not to be deleted or damaged.

The experiment therefore had two goals:

1. establish a working Code - OSS remote development session over SSH; and
2. keep the existing `~/.vscode-server` installation intact.

---

## 2. Environment

### 2.1 Client

The screenshots and extension stack traces show that the Code - OSS client was running directly in the Termux prefix:

```text
/data/data/com.termux/files/home/
```

The Open Remote - SSH extension was installed at:

```text
/data/data/com.termux/files/home/.vscode-oss/extensions/
jeanp413.open-remote-ssh-0.1.2-universal/
```

The SSH identity discovered by the extension was:

```text
/data/data/com.termux/files/home/.ssh/id_rsa
```

Although the filename was `id_rsa`, the key type printed in the log was:

```text
ssh-ed25519
```

The local Code - OSS build exposed the following version metadata to the remote installer:

```text
DISTRO_VERSION="1.122.1"
DISTRO_COMMIT="8761a5560cfd65fdd19ce7e2bd18dab5c0a4d84e"
DISTRO_QUALITY="stable"
```

### 2.2 Remote host

The target host alias was:

```text
victor
```

The installer positively detected:

```text
osReleaseId==ubuntu==
arch==x86_64==
platform==linux==
```

The remote home directory visible in the log was:

```text
/home/hwjang
```

The remote host already had a conventional Microsoft VS Code Server directory:

```text
~/.vscode-server
```

This directory was intentionally preserved.

The Open Remote - SSH installer independently selected:

```text
$HOME/.vscode-server-oss
```

which confirms that the experiment did not require removal of the existing:

```text
$HOME/.vscode-server
```

---

## 3. Initial extension selection

Several broad classes of Remote - SSH replacement were considered:

- a full remote extension-host workflow;
- SSH-mounted remote filesystems;
- SFTP-style file synchronization;
- manually managed remote extension hosts.

`Open Remote - SSH` was selected because the experiment required behavior closest to Remote - SSH rather than only remote file editing.

The selected extension identifier was:

```text
jeanp413.open-remote-ssh
```

---

## 4. Initial configuration

### 4.1 Extension installation

The intended installation command was:

```bash
code-oss --install-extension jeanp413.open-remote-ssh
```

The runtime logs later confirmed that the installed version was:

```text
jeanp413.open-remote-ssh-0.1.2-universal
```

### 4.2 Proposed API enablement

For the Code - OSS client, the proposed API was enabled through the runtime arguments configuration.

The intended `argv.json` entry was:

```json
{
  "enable-proposed-api": [
    "jeanp413.open-remote-ssh"
  ]
}
```

### 4.3 User settings

The user configured the Code - OSS user settings file under the native Termux/Code - OSS configuration path:

```text
/data/data/com.termux/files/home/.config/Code - OSS/User/settings.json
```

The screenshot showed these four configured properties:

```json
{
  "remote.SSH.serverBinaryName": "codium-server",
  "remote.SSH.serverDownloadUrlTemplate": "https://github.com/VSCodium/vscodium/releases/download/${version}${release}/vscodium-reh-${os}-${arch}-${version}${release}.tar.gz",
  "remote.SSH.serverVersion": "latest",
  "remote.SSH.serverValidation": "force"
}
```

The important intended behavior was:

- use a VSCodium-compatible remote extension host;
- name its executable `codium-server`;
- download it from VSCodium release assets;
- resolve the server version using `latest`;
- force validation behavior.

---

## 5. First connection attempt

The user initiated a connection to:

```text
victor
```

The graphical error was:

```text
Could not establish connection to "victor"
```

The UI offered:

```text
Retry
Cancel
Close Remote
```

The Remote - SSH output pane showed an extension-side failure with a stack trace ending inside:

```text
.../.vscode-oss/extensions/
jeanp413.open-remote-ssh-0.1.2-universal/
lib/extension.js
```

At this early stage, several possible causes were considered:

- failed SSH authentication;
- remote command execution restrictions;
- remote package/tool prerequisites;
- server installation directory collision;
- server version mismatch;
- server download failure.

The later logs allowed most of these hypotheses to be eliminated.

---

## 6. Preservation of the existing VS Code Server installation

A key question was whether Open Remote - SSH required deletion of:

```text
~/.vscode-server
```

The answer from the actual installer log is no.

The Open Remote - SSH-generated installer used:

```bash
SERVER_DATA_DIR="$HOME/.vscode-server-oss"
SERVER_DIR="$SERVER_DATA_DIR/bin/$DISTRO_COMMIT"
SERVER_SCRIPT="$SERVER_DIR/bin/$SERVER_APP_NAME"
```

Therefore the two installations are logically separate:

```text
Existing Microsoft VS Code workflow:
    ~/.vscode-server

Open Remote - SSH experiment:
    ~/.vscode-server-oss
```

No evidence in either captured log shows the extension attempting to overwrite or delete:

```text
~/.vscode-server
```

Accordingly, the existing VS Code Server installation should be preserved.

A previously suggested broad cleanup command that included `~/.vscode-server` was corrected and should not be used for this setup.

A safe cleanup target, based strictly on the log, is:

```bash
ssh victor 'rm -rf ~/.vscode-server-oss'
```

Other possible experimental directories may be removed only if they were explicitly created during later tests:

```text
~/.vscodium-server
~/.codium-server
~/.code-oss-remote-server
```

but the confirmed directory used by the observed `0.1.2` installer was:

```text
~/.vscode-server-oss
```

---

## 7. Direct SSH execution check

Because an early UI-side error included wording similar to:

```text
Unable to exec
```

the remote shell path was tested separately.

The diagnostic command proposed for direct execution was:

```bash
ssh -T victor \
  'echo EXEC_OK; uname -s; uname -m; id; echo SHELL=$SHELL; command -v bash; command -v tar; command -v gzip; command -v curl || command -v wget'
```

The user reported that the command completed normally.

The exact stdout from that direct command was not preserved in the conversation, so it is not reconstructed here. The reported result nevertheless established that ordinary SSH remote command execution was working.

This significantly weakened the hypothesis that `victor` had a general `ForceCommand`, shell, or SSH execution restriction.

The captured extension log independently confirms that the remote installer executed far enough to run commands such as:

```text
/usr/bin/uname
```

and to detect:

```text
ubuntu
x86_64
linux
```

Therefore the failure was not at basic SSH login or command dispatch.

---

## 8. First decisive log analysis

The first complete log showed successful progression through:

1. remote authority resolution;
2. identity-key discovery;
3. public-key authentication attempts;
4. remote installation-script execution;
5. remote OS detection;
6. remote architecture detection;
7. server URL construction;
8. attempted `wget` download.

The critical runtime values were:

```bash
DISTRO_VERSION="1.122.1"
DISTRO_COMMIT="8761a5560cfd65fdd19ce7e2bd18dab5c0a4d84e"
DISTRO_QUALITY="stable"
DISTRO_VSCODIUM_RELEASE=""

SERVER_APP_NAME="code-server-oss"
SERVER_DATA_DIR="$HOME/.vscode-server-oss"
```

The script then constructed this URL:

```text
https://github.com/VSCodium/vscodium/releases/download/1.122.1/vscodium-reh-linux-x64-1.122.1.tar.gz
```

The actual `wget` result was:

```text
2026-06-30 14:37:40 ERROR 404: Not Found.
```

The script then emitted:

```text
Error downloading server from https://github.com/VSCodium/vscodium/releases/download/1.122.1/vscodium-reh-linux-x64-1.122.1.tar.gz
```

and returned:

```text
exitCode==1==
```

with correctly detected remote metadata:

```text
osReleaseId==ubuntu==
arch==x86_64==
platform==linux==
```

This is the first conclusive root-cause observation in the experiment.

### Confirmed conclusion

The failure was not caused by:

- failure to reach `victor`;
- inability to authenticate by SSH;
- inability to run the installer script;
- unsupported remote OS;
- unsupported remote architecture;
- collision with the existing `~/.vscode-server`.

The failure occurred because the generated VSCodium REH asset URL returned HTTP 404.

---

## 9. Important configuration/runtime mismatch

The user's `settings.json` requested:

```json
"remote.SSH.serverBinaryName": "codium-server"
```

However, the generated installer continued to use:

```bash
SERVER_APP_NAME="code-server-oss"
```

The settings also requested:

```json
"remote.SSH.serverVersion": "latest"
```

but the installer still used the local Code - OSS version metadata:

```bash
DISTRO_VERSION="1.122.1"
DISTRO_VSCODIUM_RELEASE=""
```

This created the nonexistent URL:

```text
.../releases/download/1.122.1/
vscodium-reh-linux-x64-1.122.1.tar.gz
```

This observation is important because it shows that the intended VSCodium mapping settings did not produce the expected runtime values in the installed `0.1.2` extension.

The logs alone prove the runtime behavior but do not, by themselves, prove exactly why the extension ignored or failed to map those settings. The following possibilities were considered:

- the installed extension version did not support the same setting behavior expected from newer documentation;
- the configuration keys had changed between extension revisions;
- the stable `0.1.2` build had incomplete Code - OSS compatibility;
- version resolution treated the local Code - OSS version as a VSCodium release version.

At the end of this report, these remain implementation-level interpretations of the observed behavior. The directly confirmed fact is that the `0.1.2` runtime used `code-server-oss`, `1.122.1`, and an empty VSCodium release suffix despite the user's settings.

---

## 10. Second connection attempt

A second connection attempt was performed and captured in:

```text
Remote - SSH2.log
```

The result reproduced the same failure.

The second attempt again used:

```bash
DISTRO_VERSION="1.122.1"
DISTRO_VSCODIUM_RELEASE=""
SERVER_APP_NAME="code-server-oss"
SERVER_DATA_DIR="$HOME/.vscode-server-oss"
```

The same URL was generated:

```text
https://github.com/VSCodium/vscodium/releases/download/1.122.1/vscodium-reh-linux-x64-1.122.1.tar.gz
```

The second `wget` failure was:

```text
2026-06-30 14:46:49 ERROR 404: Not Found.
```

The installer result was:

```text
exitCode==1==
listeningOn====
connectionToken====
logFile==/home/hwjang/.vscode-server-oss/.8761a5560cfd65fdd19ce7e2bd18dab5c0a4d84e.log==
osReleaseId==ubuntu==
arch==x86_64==
platform==linux==
tmpDir==/run/user/1014==
```

The extension then surfaced:

```text
Error resolving authority
Error: Couldn't install vscode server on remote server, install script returned non-zero exit status
```

The stack trace confirmed the extension version:

```text
/data/data/com.termux/files/home/.vscode-oss/extensions/
jeanp413.open-remote-ssh-0.1.2-universal/
lib/extension.js
```

### Reproducibility result

The second attempt reproduced the first attempt's failure mode exactly:

```text
remote SSH path works
→ installer executes
→ Ubuntu/x86_64 detected
→ VSCodium REH URL constructed
→ HTTP 404
→ installer exitCode 1
→ authority resolution fails
```

This ruled out a transient download or one-off SSH issue.

---

## 11. Failure-chain reconstruction

The complete observed failure chain can be summarized as follows.

```text
Code - OSS on Termux
        |
        | resolves ssh-remote+victor
        v
SSH key discovered
/data/data/com.termux/files/home/.ssh/id_rsa
        |
        v
Public-key authentication attempted
        |
        v
Remote install script launched
        |
        v
uname succeeds
        |
        +--> platform = linux
        +--> arch = x86_64
        +--> osReleaseId = ubuntu
        |
        v
Open Remote - SSH runtime values:
DISTRO_VERSION = 1.122.1
DISTRO_VSCODIUM_RELEASE = ""
SERVER_APP_NAME = code-server-oss
        |
        v
Generated URL:
https://github.com/VSCodium/vscodium/releases/download/1.122.1/
vscodium-reh-linux-x64-1.122.1.tar.gz
        |
        v
wget
        |
        v
HTTP 404 Not Found
        |
        v
Error downloading server
        |
        v
exitCode == 1
        |
        v
Couldn't install vscode server on remote server
        |
        v
Could not establish connection to "victor"
```

---

## 12. Incorrect or superseded hypotheses

### 12.1 "The SSH server cannot execute remote commands"

This was considered because the UI/extension trace included an `Unable to exec`-style message.

However:

- the direct `ssh -T victor '...'` diagnostic reportedly worked;
- the extension's own installation script executed on the remote host;
- `/usr/bin/uname` ran;
- Ubuntu, x86_64, and Linux were correctly detected;
- `wget` ran and received an HTTP response.

Therefore general remote command execution failure is not the primary cause of the captured attempts.

### 12.2 "The existing ~/.vscode-server must be deleted"

This was also rejected.

The captured Open Remote - SSH installer used:

```text
~/.vscode-server-oss
```

not:

```text
~/.vscode-server
```

The existing VS Code server can remain installed.

### 12.3 "The installer never reached the remote host"

Rejected.

The remote host produced platform and OS results and executed `wget`.

### 12.4 "The remote Ubuntu host is unsupported"

Rejected for these attempts.

The installer accepted:

```text
platform==linux==
osReleaseId==ubuntu==
arch==x86_64==
```

and proceeded to the download stage.

---

## 13. Configuration experiments and recommendations considered

Several configuration additions were discussed during debugging.

### 13.1 Explicit remote platform

The following host mapping was considered:

```json
"remote.SSH.remotePlatform": {
  "victor": "linux"
}
```

The captured logs already detected the remote platform correctly as:

```text
platform==linux==
```

Therefore platform detection was not the cause of the observed 404.

### 13.2 Separate server installation path

A separate path was considered:

```json
"remote.SSH.serverInstallPath": {
  "victor": "/home/hwjang/.code-oss-remote-server"
}
```

This is useful as an isolation policy, but the captured `0.1.2` installer instead used:

```text
/home/hwjang/.vscode-server-oss
```

Since this was already separate from `/home/hwjang/.vscode-server`, directory collision was not the observed failure.

### 13.3 `latest` versus `closest` versus explicit version

The experiment started with:

```json
"remote.SSH.serverVersion": "latest"
```

But the actual runtime still generated a URL from:

```text
1.122.1
```

and an empty release suffix.

Therefore simply having `"latest"` in the settings did not prevent the invalid URL in the installed `0.1.2` build.

The next proposed remediation was to use an explicit known VSCodium REH version rather than rely on automatic mapping.

This remediation had not yet been experimentally validated at the time this report was written.

---

## 14. Extension-version finding

The second log conclusively identifies the installed extension as:

```text
jeanp413.open-remote-ssh-0.1.2-universal
```

The debugging process then shifted from the remote host to extension-version/configuration compatibility.

The working hypothesis at the end of the experiment was:

> The stable `0.1.2` extension build is not applying the intended Code - OSS/VSCodium server mapping in the way expected by the configuration, causing the local Code - OSS version `1.122.1` to be inserted directly into a VSCodium REH asset URL.

This hypothesis is consistent with all observed runtime values:

```text
DISTRO_VERSION="1.122.1"
DISTRO_VSCODIUM_RELEASE=""
SERVER_APP_NAME="code-server-oss"
```

and the resulting 404.

However, because the proposed upgrade was not yet run and no successful connection log exists yet, this report does not claim that upgrading alone is already proven to solve the issue.

---

## 15. Proposed next experiment

The next proposed experiment was:

1. keep the existing remote `~/.vscode-server` untouched;
2. upgrade Open Remote - SSH from the observed `0.1.2` build to a newer build with the intended Code - OSS compatibility behavior;
3. configure an explicit VSCodium REH version known to exist;
4. fully restart Code - OSS;
5. remove only the failed OSS-side server directory if needed;
6. reconnect to `victor`;
7. verify the runtime installer values before judging success.

The critical values to inspect in a successful follow-up log are:

```text
SERVER_APP_NAME="codium-server"
```

and a download URL whose release tag and filename correspond to a real VSCodium REH asset.

The follow-up should also verify that the server starts and reports a non-empty listening endpoint:

```text
exitCode==0==
listeningOn==...==
connectionToken==...==
```

No such successful output has yet been captured.

---

## 16. Current conclusions

### Confirmed

1. Code - OSS on native Termux can launch the Open Remote - SSH resolver.
2. The extension discovers and uses the Termux SSH identity.
3. The SSH path to `victor` is functional.
4. The remote installation script executes on `victor`.
5. `victor` is detected as Ubuntu, Linux, x86_64.
6. The existing `~/.vscode-server` does not need to be removed.
7. The observed Open Remote - SSH installer uses `~/.vscode-server-oss`.
8. The captured connection failures occur at VSCodium REH download time.
9. Both captured attempts generate the same invalid URL based on `1.122.1`.
10. Both captured attempts fail with HTTP 404.
11. The installed extension version in the captured failure is `0.1.2-universal`.
12. The user settings requesting `codium-server` and `latest` do not appear in the generated runtime installer values of the captured attempts.

### Not yet confirmed

1. Whether upgrading Open Remote - SSH fixes the configuration mapping.
2. Whether an explicit compatible VSCodium REH version produces a working server.
3. Whether `codium-server` starts successfully on `victor` after download.
4. Whether local Code - OSS and the selected remote extension host are protocol-compatible in the final configuration.
5. Whether remote extensions, terminal integration, debugging, and reconnection all work after initial connection.

---

## 17. Recommended state-preserving cleanup

Because the existing Microsoft VS Code remote environment must be preserved:

### Do not remove

```bash
~/.vscode-server
```

### Confirmed experiment directory that may be removed before retry

```bash
ssh victor 'rm -rf ~/.vscode-server-oss'
```

### Verify before removing any other directory

```bash
ssh victor 'ls -la ~ | grep -E "vscode|codium|code-oss"'
```

The cleanup policy should remain conservative until a successful Open Remote - SSH installation is established.

---

## 18. Reproduction recipe for the captured failure

The observed failure can be reproduced conceptually with the following setup.

### Client

```text
Code - OSS version metadata:
1.122.1
commit:
8761a5560cfd65fdd19ce7e2bd18dab5c0a4d84e
```

### Extension

```text
jeanp413.open-remote-ssh-0.1.2-universal
```

### Settings used by the user

```json
{
  "remote.SSH.serverBinaryName": "codium-server",
  "remote.SSH.serverDownloadUrlTemplate": "https://github.com/VSCodium/vscodium/releases/download/${version}${release}/vscodium-reh-${os}-${arch}-${version}${release}.tar.gz",
  "remote.SSH.serverVersion": "latest",
  "remote.SSH.serverValidation": "force"
}
```

### Connection action

```text
Remote-SSH: Connect to Host...
victor
```

### Observed generated installer state

```bash
DISTRO_VERSION="1.122.1"
DISTRO_COMMIT="8761a5560cfd65fdd19ce7e2bd18dab5c0a4d84e"
DISTRO_QUALITY="stable"
DISTRO_VSCODIUM_RELEASE=""

SERVER_APP_NAME="code-server-oss"
SERVER_DATA_DIR="$HOME/.vscode-server-oss"
```

### Observed generated URL

```text
https://github.com/VSCodium/vscodium/releases/download/1.122.1/vscodium-reh-linux-x64-1.122.1.tar.gz
```

### Observed result

```text
ERROR 404: Not Found.
```

followed by:

```text
Error downloading server from https://github.com/VSCodium/vscodium/releases/download/1.122.1/vscodium-reh-linux-x64-1.122.1.tar.gz
```

and:

```text
exitCode==1==
```

Finally:

```text
Error resolving authority
Error: Couldn't install vscode server on remote server, install script returned non-zero exit status
```

---

# Appendix A — First captured Remote - SSH log

The following is preserved verbatim from the uploaded `Remote - SSH.log`.

```text
[Info  - 05:37:37.545] Resolving ssh remote authority 'ssh-remote+victor' (attempt #1)
[Trace  - 05:37:37.748] Identity keys:
/data/data/com.termux/files/home/.ssh/id_rsa ssh-ed25519 SHA256:k7R+E+GX2GEfqm5RYfbivdLZ4ZdFhBpvxUbVrp4nNo8=
[Trace  - 05:37:37.816] Identity keys:
/data/data/com.termux/files/home/.ssh/id_rsa ssh-ed25519 SHA256:k7R+E+GX2GEfqm5RYfbivdLZ4ZdFhBpvxUbVrp4nNo8=
[Info  - 05:37:38.308] Trying no-auth authentication
[Info  - 05:37:38.451] Trying publickey authentication: /data/data/com.termux/files/home/.ssh/id_rsa ssh-ed25519 SHA256:k7R+E+GX2GEfqm5RYfbivdLZ4ZdFhBpvxUbVrp4nNo8=
[Info  - 05:37:39.378] Trying no-auth authentication
[Info  - 05:37:39.535] Trying publickey authentication: /data/data/com.termux/files/home/.ssh/id_rsa ssh-ed25519 SHA256:k7R+E+GX2GEfqm5RYfbivdLZ4ZdFhBpvxUbVrp4nNo8=
[Trace  - 05:37:40.405] Server install command:

# Server installation script

TMP_DIR="${XDG_RUNTIME_DIR:-"/tmp"}"

DISTRO_VERSION="1.122.1"
DISTRO_COMMIT="8761a5560cfd65fdd19ce7e2bd18dab5c0a4d84e"
DISTRO_QUALITY="stable"
DISTRO_VSCODIUM_RELEASE=""

SERVER_APP_NAME="code-server-oss"
SERVER_INITIAL_EXTENSIONS=""
SERVER_LISTEN_FLAG="--port=0"
SERVER_DATA_DIR="$HOME/.vscode-server-oss"
SERVER_DATA_DIR_FLAG=""
SERVER_DIR="$SERVER_DATA_DIR/bin/$DISTRO_COMMIT"
SERVER_SCRIPT="$SERVER_DIR/bin/$SERVER_APP_NAME"
SERVER_LOGFILE="$SERVER_DATA_DIR/.$DISTRO_COMMIT.log"
SERVER_PIDFILE="$SERVER_DATA_DIR/.$DISTRO_COMMIT.pid"
SERVER_TOKENFILE="$SERVER_DATA_DIR/.$DISTRO_COMMIT.token"
SERVER_ARCH=
SERVER_CONNECTION_TOKEN=
SERVER_DOWNLOAD_URL=

LISTENING_ON=
OS_RELEASE_ID=
ARCH=
PLATFORM=

# Mimic output from logs of remote-ssh extension
print_install_results_and_exit() {
    echo "67b8f767d13008f0405cb2eb: start"
    echo "exitCode==$1=="
    echo "listeningOn==$LISTENING_ON=="
    echo "connectionToken==$SERVER_CONNECTION_TOKEN=="
    echo "logFile==$SERVER_LOGFILE=="
    echo "osReleaseId==$OS_RELEASE_ID=="
    echo "arch==$ARCH=="
    echo "platform==$PLATFORM=="
    echo "tmpDir==$TMP_DIR=="
    
    echo "67b8f767d13008f0405cb2eb: end"
    exit 0
}

# Check if platform is supported
if ! command -v uname; then
    echo "Error 'uname' command not found, could not get platform/arch data."
    print_install_results_and_exit 1
fi

KERNEL="$(uname -s)"
case $KERNEL in
    Darwin)
        PLATFORM="darwin"
        ;;
    Linux)
        PLATFORM="linux"
        ;;
    FreeBSD)
        PLATFORM="freebsd"
        ;;
    DragonFly)
        PLATFORM="dragonfly"
        ;;
    "")
        echo "Error uname -s yields empty result"
        print_install_results_and_exit 1
        ;;
    *)
        echo "Error platform not supported: $KERNEL"
        print_install_results_and_exit 1
        ;;
esac

# Check machine architecture
ARCH="$(uname -m)"
case $ARCH in
    x86_64 | amd64)
        SERVER_ARCH="x64"
        ;;
    armv7l | armv8l)
        SERVER_ARCH="armhf"
        ;;
    arm64 | aarch64)
        SERVER_ARCH="arm64"
        ;;
    ppc64le)
        SERVER_ARCH="ppc64le"
        ;;
    riscv64)
        SERVER_ARCH="riscv64"
        ;;
    loongarch64)
        SERVER_ARCH="loong64"
        ;;
    s390x)
        SERVER_ARCH="s390x"
        ;;
    *)
        echo "Error architecture not supported: $ARCH"
        print_install_results_and_exit 1
        ;;
esac

# https://www.freedesktop.org/software/systemd/man/os-release.html
OS_RELEASE_ID="$(grep -i '^ID=' /etc/os-release 2>/dev/null | sed 's/^ID=//gi' | sed 's/"//g')"
if [[ -z $OS_RELEASE_ID ]]; then
    OS_RELEASE_ID="$(grep -i '^ID=' /usr/lib/os-release 2>/dev/null | sed 's/^ID=//gi' | sed 's/"//g')"
    if [[ -z $OS_RELEASE_ID ]]; then
        OS_RELEASE_ID="unknown"
    fi
fi

# Create installation folder
if [[ ! -d $SERVER_DIR ]]; then
    mkdir -p $SERVER_DIR
    if (( $? > 0 )); then
        echo "Error creating server install directory"
        print_install_results_and_exit 1
    fi
fi

# adjust platform for vscodium download, if needed
if [[ $OS_RELEASE_ID = alpine ]]; then
    PLATFORM=$OS_RELEASE_ID
fi

SERVER_DOWNLOAD_URL="$(echo "https://github.com/VSCodium/vscodium/releases/download/\${version}\${release}/vscodium-reh-\${os}-\${arch}-\${version}\${release}.tar.gz" | sed "s/\${quality}/$DISTRO_QUALITY/g" | sed "s/\${version}/$DISTRO_VERSION/g" | sed "s/\${commit}/$DISTRO_COMMIT/g" | sed "s/\${os}/$PLATFORM/g" | sed "s/\${arch}/$SERVER_ARCH/g" | sed "s/\${release}/$DISTRO_VSCODIUM_RELEASE/g")"

# Check if server script is already installed
if [[ ! -f $SERVER_SCRIPT ]]; then
    case "$PLATFORM" in
        darwin | linux | alpine | freebsd )
            ;;
        *)
            echo "Error '$PLATFORM' needs manual installation of remote extension host"
            print_install_results_and_exit 1
            ;;
    esac

    pushd $SERVER_DIR > /dev/null

    if command -v wget >/dev/null 2>&1; then
        wget --tries=3 --timeout=10 --continue --no-verbose -O vscode-server.tar.gz $SERVER_DOWNLOAD_URL
    elif command -v curl >/dev/null 2>&1; then
        curl --retry 3 --connect-timeout 10 --location --show-error --silent --output vscode-server.tar.gz $SERVER_DOWNLOAD_URL
    elif command -v fetch >/dev/null 2>&1; then
        fetch --retry --timeout=10 --quiet --output=vscode-server.tar.gz $SERVER_DOWNLOAD_URL
    else
        echo "Error no tool to download server binary"
        print_install_results_and_exit 1
    fi

    if (( $? > 0 )); then
        echo "Error downloading server from $SERVER_DOWNLOAD_URL"
        rm -rf vscode-server.tar.gz
        print_install_results_and_exit 1
    fi

    tar -xf vscode-server.tar.gz --strip-components 1
    if (( $? > 0 )); then
        echo "Error while extracting server contents"
        rm -rf vscode-server.tar.gz
        print_install_results_and_exit 1
    fi

    if [[ ! -f $SERVER_SCRIPT ]]; then
        rm -rf $SERVER_DIR/*
        echo "Error server contents are corrupted"
        print_install_results_and_exit 1
    fi

    rm -f vscode-server.tar.gz

    popd > /dev/null
else
    echo "Server script already installed in $SERVER_SCRIPT"
fi

# Try to find if server is already running
if [[ -f $SERVER_PIDFILE ]]; then
    SERVER_PID="$(cat $SERVER_PIDFILE)"
    SERVER_RUNNING_PROCESS="$(ps -o pid,args -p $SERVER_PID | grep $SERVER_SCRIPT)"
else
    SERVER_RUNNING_PROCESS="$(ps -o pid,args -A | grep $SERVER_SCRIPT | grep -v grep)"
fi

if [[ -z $SERVER_RUNNING_PROCESS ]]; then
    if [[ -f $SERVER_LOGFILE ]]; then
        rm $SERVER_LOGFILE
    fi
    if [[ -f $SERVER_TOKENFILE ]]; then
        rm $SERVER_TOKENFILE
    fi

    touch $SERVER_TOKENFILE
    chmod 600 $SERVER_TOKENFILE
    SERVER_CONNECTION_TOKEN="031d89ce-e570-416d-831b-12e3d8460d19"
    echo $SERVER_CONNECTION_TOKEN > $SERVER_TOKENFILE

    $SERVER_SCRIPT --start-server --host=127.0.0.1 $SERVER_LISTEN_FLAG $SERVER_DATA_DIR_FLAG $SERVER_INITIAL_EXTENSIONS --connection-token-file $SERVER_TOKENFILE --telemetry-level off --enable-remote-auto-shutdown --accept-server-license-terms &> $SERVER_LOGFILE &
    echo $! > $SERVER_PIDFILE
else
    echo "Server script is already running $SERVER_SCRIPT"
fi

if [[ -f $SERVER_TOKENFILE ]]; then
    SERVER_CONNECTION_TOKEN="$(cat $SERVER_TOKENFILE)"
else
    echo "Error server token file not found $SERVER_TOKENFILE"
    print_install_results_and_exit 1
fi

if [[ -f $SERVER_LOGFILE ]]; then
    for i in {1..5}; do
        LISTENING_ON="$(cat $SERVER_LOGFILE | grep -E 'Extension host agent listening on .+' | sed 's/Extension host agent listening on //')"
        if [[ -n $LISTENING_ON ]]; then
            break
        fi
        sleep 0.5
    done

    if [[ -z $LISTENING_ON ]]; then
        echo "Error server did not start successfully"
        print_install_results_and_exit 1
    fi
else
    echo "Error server log file not found $SERVER_LOGFILE"
    print_install_results_and_exit 1
fi

# Finish server setup
print_install_results_and_exit 0

[Trace  - 05:37:41.251] Server install command stderr:
https://github.com/VSCodium/vscodium/releases/download/1.122.1/vscodium-reh-linux-x64-1.122.1.tar.gz:
2026-06-30 14:37:40 ERROR 404: Not Found.

[Trace  - 05:37:41.251] Server install command stdout:
/usr/bin/uname
Error downloading server from https://github.com/VSCodium/vscodium/releases/download/1.122.1/vscodium-reh-linux-x64-1.122.1.tar.gz
67b8f767d13008f0405cb2eb: start
exitCode==1==
listeningOn====
connectionToken====
logFile==/home/hwjang/.vscode-server-oss/.8761a5560cfd65fdd19ce7e2bd18dab5c0a4d84e.log==
osReleaseId==ubuntu==
arch==x86_64==
platform==linux==
tmpDir==/run/user/1014==
67b8f767d13008f0405cb2eb: end

[Error  - 05:37:41.257] Error resolving authority
Error: Couldn't install vscode server on remote server, install script returned non-zero exit status
    at t.installCodeServer (/data/data/com.termux/files/home/.vscode-oss/extensions/jeanp413.open-remote-ssh-0.1.2-universal/lib/extension.js:1:430127)
    at process.processTicksAndRejections (node:internal/process/task_queues:103:5)
    at async /data/data/com.termux/files/home/.vscode-oss/extensions/jeanp413.open-remote-ssh-0.1.2-universal/lib/extension.js:1:391641

```

---

# Appendix B — Second captured Remote - SSH log

The following is preserved verbatim from the uploaded `Remote - SSH2.log`.

```text
[Info  - 05:46:45.868] Resolving ssh remote authority 'ssh-remote+victor' (attempt #1)
[Trace  - 05:46:46.77] Identity keys:
/data/data/com.termux/files/home/.ssh/id_rsa ssh-ed25519 SHA256:k7R+E+GX2GEfqm5RYfbivdLZ4ZdFhBpvxUbVrp4nNo8=
[Trace  - 05:46:46.119] Identity keys:
/data/data/com.termux/files/home/.ssh/id_rsa ssh-ed25519 SHA256:k7R+E+GX2GEfqm5RYfbivdLZ4ZdFhBpvxUbVrp4nNo8=
[Info  - 05:46:46.629] Trying no-auth authentication
[Info  - 05:46:46.783] Trying publickey authentication: /data/data/com.termux/files/home/.ssh/id_rsa ssh-ed25519 SHA256:k7R+E+GX2GEfqm5RYfbivdLZ4ZdFhBpvxUbVrp4nNo8=
[Info  - 05:46:47.970] Trying no-auth authentication
[Info  - 05:46:48.217] Trying publickey authentication: /data/data/com.termux/files/home/.ssh/id_rsa ssh-ed25519 SHA256:k7R+E+GX2GEfqm5RYfbivdLZ4ZdFhBpvxUbVrp4nNo8=
[Trace  - 05:46:49.20] Server install command:

# Server installation script

TMP_DIR="${XDG_RUNTIME_DIR:-"/tmp"}"

DISTRO_VERSION="1.122.1"
DISTRO_COMMIT="8761a5560cfd65fdd19ce7e2bd18dab5c0a4d84e"
DISTRO_QUALITY="stable"
DISTRO_VSCODIUM_RELEASE=""

SERVER_APP_NAME="code-server-oss"
SERVER_INITIAL_EXTENSIONS=""
SERVER_LISTEN_FLAG="--port=0"
SERVER_DATA_DIR="$HOME/.vscode-server-oss"
SERVER_DATA_DIR_FLAG=""
SERVER_DIR="$SERVER_DATA_DIR/bin/$DISTRO_COMMIT"
SERVER_SCRIPT="$SERVER_DIR/bin/$SERVER_APP_NAME"
SERVER_LOGFILE="$SERVER_DATA_DIR/.$DISTRO_COMMIT.log"
SERVER_PIDFILE="$SERVER_DATA_DIR/.$DISTRO_COMMIT.pid"
SERVER_TOKENFILE="$SERVER_DATA_DIR/.$DISTRO_COMMIT.token"
SERVER_ARCH=
SERVER_CONNECTION_TOKEN=
SERVER_DOWNLOAD_URL=

LISTENING_ON=
OS_RELEASE_ID=
ARCH=
PLATFORM=

# Mimic output from logs of remote-ssh extension
print_install_results_and_exit() {
    echo "20ab25639b243e3640ac6e43: start"
    echo "exitCode==$1=="
    echo "listeningOn==$LISTENING_ON=="
    echo "connectionToken==$SERVER_CONNECTION_TOKEN=="
    echo "logFile==$SERVER_LOGFILE=="
    echo "osReleaseId==$OS_RELEASE_ID=="
    echo "arch==$ARCH=="
    echo "platform==$PLATFORM=="
    echo "tmpDir==$TMP_DIR=="
    
    echo "20ab25639b243e3640ac6e43: end"
    exit 0
}

# Check if platform is supported
if ! command -v uname; then
    echo "Error 'uname' command not found, could not get platform/arch data."
    print_install_results_and_exit 1
fi

KERNEL="$(uname -s)"
case $KERNEL in
    Darwin)
        PLATFORM="darwin"
        ;;
    Linux)
        PLATFORM="linux"
        ;;
    FreeBSD)
        PLATFORM="freebsd"
        ;;
    DragonFly)
        PLATFORM="dragonfly"
        ;;
    "")
        echo "Error uname -s yields empty result"
        print_install_results_and_exit 1
        ;;
    *)
        echo "Error platform not supported: $KERNEL"
        print_install_results_and_exit 1
        ;;
esac

# Check machine architecture
ARCH="$(uname -m)"
case $ARCH in
    x86_64 | amd64)
        SERVER_ARCH="x64"
        ;;
    armv7l | armv8l)
        SERVER_ARCH="armhf"
        ;;
    arm64 | aarch64)
        SERVER_ARCH="arm64"
        ;;
    ppc64le)
        SERVER_ARCH="ppc64le"
        ;;
    riscv64)
        SERVER_ARCH="riscv64"
        ;;
    loongarch64)
        SERVER_ARCH="loong64"
        ;;
    s390x)
        SERVER_ARCH="s390x"
        ;;
    *)
        echo "Error architecture not supported: $ARCH"
        print_install_results_and_exit 1
        ;;
esac

# https://www.freedesktop.org/software/systemd/man/os-release.html
OS_RELEASE_ID="$(grep -i '^ID=' /etc/os-release 2>/dev/null | sed 's/^ID=//gi' | sed 's/"//g')"
if [[ -z $OS_RELEASE_ID ]]; then
    OS_RELEASE_ID="$(grep -i '^ID=' /usr/lib/os-release 2>/dev/null | sed 's/^ID=//gi' | sed 's/"//g')"
    if [[ -z $OS_RELEASE_ID ]]; then
        OS_RELEASE_ID="unknown"
    fi
fi

# Create installation folder
if [[ ! -d $SERVER_DIR ]]; then
    mkdir -p $SERVER_DIR
    if (( $? > 0 )); then
        echo "Error creating server install directory"
        print_install_results_and_exit 1
    fi
fi

# adjust platform for vscodium download, if needed
if [[ $OS_RELEASE_ID = alpine ]]; then
    PLATFORM=$OS_RELEASE_ID
fi

SERVER_DOWNLOAD_URL="$(echo "https://github.com/VSCodium/vscodium/releases/download/\${version}\${release}/vscodium-reh-\${os}-\${arch}-\${version}\${release}.tar.gz" | sed "s/\${quality}/$DISTRO_QUALITY/g" | sed "s/\${version}/$DISTRO_VERSION/g" | sed "s/\${commit}/$DISTRO_COMMIT/g" | sed "s/\${os}/$PLATFORM/g" | sed "s/\${arch}/$SERVER_ARCH/g" | sed "s/\${release}/$DISTRO_VSCODIUM_RELEASE/g")"

# Check if server script is already installed
if [[ ! -f $SERVER_SCRIPT ]]; then
    case "$PLATFORM" in
        darwin | linux | alpine | freebsd )
            ;;
        *)
            echo "Error '$PLATFORM' needs manual installation of remote extension host"
            print_install_results_and_exit 1
            ;;
    esac

    pushd $SERVER_DIR > /dev/null

    if command -v wget >/dev/null 2>&1; then
        wget --tries=3 --timeout=10 --continue --no-verbose -O vscode-server.tar.gz $SERVER_DOWNLOAD_URL
    elif command -v curl >/dev/null 2>&1; then
        curl --retry 3 --connect-timeout 10 --location --show-error --silent --output vscode-server.tar.gz $SERVER_DOWNLOAD_URL
    elif command -v fetch >/dev/null 2>&1; then
        fetch --retry --timeout=10 --quiet --output=vscode-server.tar.gz $SERVER_DOWNLOAD_URL
    else
        echo "Error no tool to download server binary"
        print_install_results_and_exit 1
    fi

    if (( $? > 0 )); then
        echo "Error downloading server from $SERVER_DOWNLOAD_URL"
        rm -rf vscode-server.tar.gz
        print_install_results_and_exit 1
    fi

    tar -xf vscode-server.tar.gz --strip-components 1
    if (( $? > 0 )); then
        echo "Error while extracting server contents"
        rm -rf vscode-server.tar.gz
        print_install_results_and_exit 1
    fi

    if [[ ! -f $SERVER_SCRIPT ]]; then
        rm -rf $SERVER_DIR/*
        echo "Error server contents are corrupted"
        print_install_results_and_exit 1
    fi

    rm -f vscode-server.tar.gz

    popd > /dev/null
else
    echo "Server script already installed in $SERVER_SCRIPT"
fi

# Try to find if server is already running
if [[ -f $SERVER_PIDFILE ]]; then
    SERVER_PID="$(cat $SERVER_PIDFILE)"
    SERVER_RUNNING_PROCESS="$(ps -o pid,args -p $SERVER_PID | grep $SERVER_SCRIPT)"
else
    SERVER_RUNNING_PROCESS="$(ps -o pid,args -A | grep $SERVER_SCRIPT | grep -v grep)"
fi

if [[ -z $SERVER_RUNNING_PROCESS ]]; then
    if [[ -f $SERVER_LOGFILE ]]; then
        rm $SERVER_LOGFILE
    fi
    if [[ -f $SERVER_TOKENFILE ]]; then
        rm $SERVER_TOKENFILE
    fi

    touch $SERVER_TOKENFILE
    chmod 600 $SERVER_TOKENFILE
    SERVER_CONNECTION_TOKEN="6583e79f-7915-4212-9488-1ec521fa3196"
    echo $SERVER_CONNECTION_TOKEN > $SERVER_TOKENFILE

    $SERVER_SCRIPT --start-server --host=127.0.0.1 $SERVER_LISTEN_FLAG $SERVER_DATA_DIR_FLAG $SERVER_INITIAL_EXTENSIONS --connection-token-file $SERVER_TOKENFILE --telemetry-level off --enable-remote-auto-shutdown --accept-server-license-terms &> $SERVER_LOGFILE &
    echo $! > $SERVER_PIDFILE
else
    echo "Server script is already running $SERVER_SCRIPT"
fi

if [[ -f $SERVER_TOKENFILE ]]; then
    SERVER_CONNECTION_TOKEN="$(cat $SERVER_TOKENFILE)"
else
    echo "Error server token file not found $SERVER_TOKENFILE"
    print_install_results_and_exit 1
fi

if [[ -f $SERVER_LOGFILE ]]; then
    for i in {1..5}; do
        LISTENING_ON="$(cat $SERVER_LOGFILE | grep -E 'Extension host agent listening on .+' | sed 's/Extension host agent listening on //')"
        if [[ -n $LISTENING_ON ]]; then
            break
        fi
        sleep 0.5
    done

    if [[ -z $LISTENING_ON ]]; then
        echo "Error server did not start successfully"
        print_install_results_and_exit 1
    fi
else
    echo "Error server log file not found $SERVER_LOGFILE"
    print_install_results_and_exit 1
fi

# Finish server setup
print_install_results_and_exit 0

[Trace  - 05:46:49.409] Server install command stderr:
https://github.com/VSCodium/vscodium/releases/download/1.122.1/vscodium-reh-linux-x64-1.122.1.tar.gz:
2026-06-30 14:46:49 ERROR 404: Not Found.

[Trace  - 05:46:49.410] Server install command stdout:
/usr/bin/uname
Error downloading server from https://github.com/VSCodium/vscodium/releases/download/1.122.1/vscodium-reh-linux-x64-1.122.1.tar.gz
20ab25639b243e3640ac6e43: start
exitCode==1==
listeningOn====
connectionToken====
logFile==/home/hwjang/.vscode-server-oss/.8761a5560cfd65fdd19ce7e2bd18dab5c0a4d84e.log==
osReleaseId==ubuntu==
arch==x86_64==
platform==linux==
tmpDir==/run/user/1014==
20ab25639b243e3640ac6e43: end

[Error  - 05:46:49.417] Error resolving authority
Error: Couldn't install vscode server on remote server, install script returned non-zero exit status
    at t.installCodeServer (/data/data/com.termux/files/home/.vscode-oss/extensions/jeanp413.open-remote-ssh-0.1.2-universal/lib/extension.js:1:430127)
    at process.processTicksAndRejections (node:internal/process/task_queues:103:5)
    at async /data/data/com.termux/files/home/.vscode-oss/extensions/jeanp413.open-remote-ssh-0.1.2-universal/lib/extension.js:1:391641

```

---

# Appendix C — Important commands used or proposed during diagnosis

## Direct SSH execution validation

```bash
ssh -T victor \
  'echo EXEC_OK; uname -s; uname -m; id; echo SHELL=$SHELL; command -v bash; command -v tar; command -v gzip; command -v curl || command -v wget'
```

The user reported that this test completed normally. Its exact stdout was not preserved.

## Remote home check

```bash
ssh victor 'echo $HOME'
```

The logs independently show the effective remote home path as:

```text
/home/hwjang
```

## Conservative cleanup

```bash
ssh victor 'rm -rf ~/.vscode-server-oss'
```

## Inspection before any broader cleanup

```bash
ssh victor 'ls -la ~ | grep -E "vscode|codium|code-oss"'
```

## Directory that must be preserved

```text
~/.vscode-server
```

---

# Appendix D — Diagnostic lessons from the experiment

1. A top-level Remote - SSH UI error is not sufficient to identify the real failure stage.
2. The generated remote install script is the most valuable artifact for distinguishing:
   - authentication failures,
   - remote execution failures,
   - platform detection failures,
   - dependency failures,
   - download failures,
   - extraction failures,
   - server startup failures.
3. The presence of a working existing `~/.vscode-server` does not imply it must be reused or removed.
4. For Code - OSS forks, local editor versions and remote extension-host release versions should not be assumed to map one-to-one.
5. Always inspect the final expanded download URL rather than only the URL template.
6. The runtime values embedded in the generated installer are more authoritative than the intended settings when debugging actual behavior.
7. Repeating the connection attempt and comparing logs is useful for separating deterministic configuration failures from transient network failures.
8. In this experiment, two attempts produced the same deterministic 404, making a transient network explanation unlikely.
