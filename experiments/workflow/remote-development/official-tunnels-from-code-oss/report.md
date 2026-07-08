# Code - OSS Client to Official VS Code Remote Tunnel: Compatibility Experiment Report

**Experiment date:** 2026-06-30  
**Report scope:** Attempts to connect a native Termux Code - OSS desktop client to a remote machine exposed through the official VS Code Remote Tunnels stack.  
**Remote target name:** `victor`  
**Tunnel ID observed in logs:** `fancy-chair-1xm3l36`  
**Tunnel cluster observed in logs:** `asse`

---

## 1. Objective

The goal of the experiment was specific:

> Keep the remote machine on the official VS Code / `code tunnel` stack, while using Code - OSS as the local desktop client.

The desired architecture was therefore:

```text
Remote machine (victor)
  official VS Code CLI / VS Code Server
  code tunnel
        |
        | Microsoft Remote Tunnels transport
        v
Local machine
  Termux native desktop environment
  Code - OSS client
  Remote - Tunnels extension
```

The experiment did **not** aim to replace the remote server with an OSS-compatible server. It attempted to determine how far an OSS client could progress against the official VS Code Remote Tunnels service and whether configuration or product metadata changes could make that combination work.

The final result was:

> The Code - OSS client successfully discovered the tunnel, started or reused the local tunnel proxy, resolved `tunnel+victor` to a local WebSocket endpoint, opened Management and ExtensionHost sockets, and reached the remote connection negotiation stage. The connection was then consistently rejected with `Connection error: Unauthorized client refused`.

Multiple client-side compatibility obstacles were found and individually removed during the investigation. None of those changes removed the final authorization failure.

---

## 2. Environment and Known-Good Control

### 2.1 Local client environment

The local client was a native Code - OSS installation under Termux:

```text
/data/data/com.termux/files/usr/lib/code-oss/
```

The local configuration directory shown during the experiments was initially:

```text
~/.config/Code - OSS/
```

The experiments also used clean or VS Code-like profiles such as:

```text
~/.config/CodeTunnelTest
~/.config/Code
```

The local machine also contained an Ubuntu proot distribution with a separate official VS Code installation:

```text
/data/data/com.termux/files/usr/var/lib/proot-distro/containers/ubuntu/rootfs/usr/share/code/
```

This became useful later as a source of a working official `code-tunnel` executable path.

### 2.2 Remote server environment

The remote target was:

```text
victor
```

The server used the official VS Code CLI/server tunnel stack. A server installation path observed later was:

```text
/home/hwjang/.vscode/cli/servers/Stable-6928394f91b684055b873eecb8bc281365131f1c/
```

The observed server stable commit was therefore:

```text
6928394f91b684055b873eecb8bc281365131f1c
```

### 2.3 Critical control test: `vscode.dev` worked

A decisive control was performed early in the investigation:

> The same remote tunnel could be opened successfully from `vscode.dev`.

This established that, at that time:

- the remote machine was online;
- the tunnel existed;
- the tunnel account/authentication path was functional;
- the remote official VS Code Server/CLI tunnel setup was functional;
- the failure was specific to the Code - OSS desktop client path, rather than a general server-side tunnel outage.

This control shaped the remainder of the investigation: effort focused on the local Code - OSS product metadata, extension API permissions, tunnel helper availability, profile isolation, and final client/server negotiation.

---

## 3. Initial Symptom

The initial UI showed two user-facing errors:

```text
Could not fetch remote environment
```

and:

```text
Failed to connect to the remote extension host server
(Error: Connection error: Unauthorized client refused)
```

The first screenshot also showed an SSH-oriented remote view and an active remote indicator, which initially caused some ambiguity between Remote-SSH and Remote Tunnels. The objective was later clarified: the server should remain on the official VS Code tunnel stack and the local client should be Code - OSS.

The visible `settings.json` at that stage contained a mixture of SSH-specific and tunnel-specific settings. The screenshot showed entries of the form:

```json
{
  "remote.SSH.serverBinaryName": "codium-server",
  "remote.SSH.serverDownloadUrlTemplate": "...",
  "remote.SSH.serverVersion": "latest",
  "remote.SSH.serverValidation": "force",
  "remote.SSH.showLoginTerminal": true,
  "remote.SSH.useLocalServer": false,
  "remote.SSH.useExecServer": false,
  "remote.tunnels.tunnelCredentialCommand": null
}
```

The SSH settings were not the direct mechanism used by Remote Tunnels, so later tests increasingly isolated the tunnel path from SSH-related extension noise.

---

## 4. Baseline Tunnel Transport Behavior

The earliest detailed tunnel log already showed that the Remote - Tunnels extension could discover and establish the transport tunnel.

From `Remote - Tunnels3.log`:

```text
2026-06-30 15:11:03.785 [info] Resolving tunnel+victor...
2026-06-30 15:11:03.785 [info] Creating new tunnel proxy server
2026-06-30 15:11:09.934 [info] [proxy] Found tunnel (ID=fancy-chair-1xm3l36, Cluster=asse)
2026-06-30 15:11:09.947 [info] Remote resolution completed
2026-06-30 15:11:30.853 [info] [proxy] [connection.0] tunnel connection established
2026-06-30 15:11:31.036 [info] [proxy] Tunnel connection successful
```

The extension then reused a local Unix-domain socket for the tunnel proxy:

```text
2026-06-30 15:11:31.780 [info] Resolving tunnel+victor...
2026-06-30 15:11:31.801 [info] Found running server in /data/data/com.termux/files/usr/tmp/vscode-tunneling-752204387a587e89.sock
2026-06-30 15:11:31.855 [info] Remote resolution completed
```

A stale or broken local tunnel socket condition was also observed once:

```text
2026-06-30 15:19:25.610 [info] Resolving tunnel+victor...
2026-06-30 15:19:25.636 [info] Found running server in /data/data/com.termux/files/usr/tmp/vscode-tunneling-752204387a587e89.sock
2026-06-30 15:19:25.706 [info] Remote resolution completed
2026-06-30 15:19:26.188 [error] [proxy] [connection.10] error setting up websocket: Error: CodeError(AsyncPipeFailed(Os { code: 2, kind: NotFound, message: "No such file or directory" }))
```

Immediately afterward, the extension created a fresh proxy server and recovered the transport layer:

```text
2026-06-30 15:19:26.322 [info] Resolving tunnel+victor...
2026-06-30 15:19:26.371 [info] Creating new tunnel proxy server
2026-06-30 15:19:31.699 [info] [proxy] Found tunnel (ID=fancy-chair-1xm3l36, Cluster=asse)
2026-06-30 15:19:31.701 [info] Remote resolution completed
2026-06-30 15:19:39.654 [info] [proxy] [connection.0] tunnel connection established
2026-06-30 15:19:39.868 [info] [proxy] Tunnel connection successful
```

### Interpretation

The baseline logs demonstrated that the main failure was not simply "the tunnel cannot be found." The client repeatedly reached a state where:

```text
Tunnel discovery      OK
Tunnel proxy startup  OK
Tunnel transport      OK
Remote resolution     OK
```

This distinction was important throughout the later tests.

---

## 5. Proposed API Compatibility Problems

The Code - OSS workbench initially refused some proposed APIs required by Microsoft remote extensions.

Observed errors included the equivalent of:

```text
Extension 'ms-vscode.remote-server CANNOT USE these API proposals 'resolvers'
```

and:

```text
Extension 'ms-vscode.remote-explorer CANNOT USE these API proposals 'contribViewsRemote, extensionsAny'
```

A runtime-argument test was therefore performed using proposed API enablement for the relevant extension IDs.

The tested `argv.json` concept was:

```json
{
  "enable-proposed-api": [
    "ms-vscode.remote-server",
    "ms-vscode.remote-explorer"
  ]
}
```

The equivalent direct launch form was also used:

```bash
code-oss \
  --enable-proposed-api ms-vscode.remote-server \
  --enable-proposed-api ms-vscode.remote-explorer
```

### Result

This was useful, because the experiment progressed beyond the initial proposed-API complaints. However, once the tunnel resolver was active, the client still failed later in the connection sequence with:

```text
Connection error: Unauthorized client refused
```

Thus proposed API access was a real compatibility issue, but not the final blocker.

---

## 6. First Detailed Workbench-Level Failure

`Window.log` showed the complete client-side sequence clearly.

First, the tunnel authority resolver returned a local WebSocket endpoint:

```text
2026-06-30 15:54:55.866 [info] [Window] resolveAuthority(tunnel) returned 'WebSocket(127.0.0.1:45971)' after 17948 ms
```

Then the workbench started creating the two remote channels:

```text
2026-06-30 15:54:55.878 [info] [Window] Creating a socket (renderer-Management-5b637586-dc3e-429f-9dbc-9105801fc6b3)...
2026-06-30 15:54:55.887 [info] [Window] Creating a socket (renderer-ExtensionHost-0dd280e9-8d97-4f9f-b976-092ffc355142)...
```

The Management socket itself was created successfully:

```text
2026-06-30 15:55:04.229 [info] [Window] Creating a socket (renderer-Management-5b637586-dc3e-429f-9dbc-9105801fc6b3) was successful after 8351 ms.
```

The rejection occurred during remote connection negotiation:

```text
2026-06-30 15:55:04.850 [error] [Window] [remote-connection][Management   ][5b637…][initial][WebSocket(127.0.0.1:45971)] received error control message when negotiating connection. Error:
2026-06-30 15:55:04.853 [error] [Window] Error: Connection error: Unauthorized client refused
```

The client retried repeatedly. The same behavior was observed for both Management and ExtensionHost channels:

```text
2026-06-30 15:55:05.402 [error] [Window] [remote-connection][ExtensionHost][0dd28…][initial][WebSocket(127.0.0.1:45971)] received error control message when negotiating connection. Error:
2026-06-30 15:55:05.411 [error] [Window] Error: Connection error: Unauthorized client refused
```

This established a very specific boundary:

```text
resolver -> local WebSocket       succeeded
socket creation                   succeeded
initial connection negotiation    rejected
```

---

## 7. Remote Tunnel Service Product Metadata Failure

A separate client service log revealed that the Code - OSS product metadata was incomplete for Remote Tunnel Service operation.

From `Remote Tunnel Service.log`:

```text
2026-06-30 15:54:50.514 [error] Missing 'tunnelApplicationConfig' or 'tunnelApplicationName' in product.json. Remote tunneling is not available.
```

This was an important discovery because it showed that the local Code - OSS package was not fully configured for all tunnel-service paths.

### 7.1 First product metadata patch attempt

The initial approach was to add OSS-style product identifiers, including values such as:

```json
{
  "serverApplicationName": "code-server-oss",
  "serverDataFolderName": ".vscode-server-oss",
  "tunnelApplicationName": "code-tunnel-oss"
}
```

Proposed API allowances were also inserted into `extensionEnabledApiProposals` for the remote extensions.

Despite a successful edit, the user reported that the same Remote Tunnel Service error remained:

```text
2026-06-30 16:16:22.924 [error] Missing 'tunnelApplicationConfig' or 'tunnelApplicationName' in product.json. Remote tunneling is not available.
```

That raised the possibility of either:

1. another `product.json` being read, or
2. a path in the application requiring a different product identity/configuration combination.

---

## 8. Locating All Relevant `product.json` Files

A recursive inspection was run to find product metadata files and print relevant identity fields.

The observed output was:

```text
== /data/data/com.termux/files/usr/var/lib/proot-distro/containers/ubuntu/rootfs/usr/share/code/resources/app/product.json
nameShort: Code
applicationName: code
dataFolderName: .vscode
serverApplicationName: code-server
serverDataFolderName: .vscode-server
tunnelApplicationName: code-tunnel
urlProtocol: vscode

== /data/data/com.termux/files/usr/lib/code-oss/resources/app/product.json
nameShort: Code - OSS
applicationName: code-oss
dataFolderName: .vscode-oss
serverApplicationName: code-server-oss
serverDataFolderName: .vscode-server-oss
tunnelApplicationName: code-tunnel-oss
urlProtocol: code-oss
```

This confirmed two separate product trees:

### Official VS Code in Ubuntu proot

```text
/data/data/com.termux/files/usr/var/lib/proot-distro/containers/ubuntu/rootfs/usr/share/code/
```

with VS Code identity:

```text
applicationName: code
serverApplicationName: code-server
tunnelApplicationName: code-tunnel
urlProtocol: vscode
```

### Native Termux Code - OSS client

```text
/data/data/com.termux/files/usr/lib/code-oss/
```

with OSS identity:

```text
applicationName: code-oss
serverApplicationName: code-server-oss
tunnelApplicationName: code-tunnel-oss
urlProtocol: code-oss
```

This finding enabled a controlled A/B experiment: make the native Code - OSS client expose VS Code-like product identity values and see whether the failure moved.

---

## 9. VS Code-Like `product.json` Experiment

A backup was made before modifying:

```text
/data/data/com.termux/files/usr/lib/code-oss/resources/app/product.json
```

The experimental identity was changed toward the observed official VS Code values:

```json
{
  "nameShort": "Code",
  "nameLong": "Visual Studio Code",
  "applicationName": "code",
  "serverApplicationName": "code-server",
  "serverDataFolderName": ".vscode-server",
  "tunnelApplicationName": "code-tunnel",
  "urlProtocol": "vscode"
}
```

At one stage `dataFolderName` was deliberately kept unchanged to avoid losing the existing OSS settings and extensions. At a later stage, a stronger VS Code-like test also used:

```json
{
  "dataFolderName": ".vscode"
}
```

An explicit `tunnelApplicationConfig` object was also added during the experiment:

```json
{
  "tunnelApplicationConfig": {
    "editorWebUrl": "https://vscode.dev",
    "webEndpointUrl": "https://main.vscode-cdn.net",
    "extension": {
      "friendlyName": "Remote - Tunnels",
      "extensionId": "ms-vscode.remote-server",
      "startEntry": {
        "helpLink": "https://aka.ms/remote-tunnels",
        "command": "remote-tunnels.connectToTunnel",
        "label": "Connect to Tunnel"
      }
    }
  }
}
```

The proposal lists were expanded in the experimental product metadata. The tested intent was equivalent to:

```json
{
  "extensionEnabledApiProposals": {
    "ms-vscode.remote-server": [
      "resolvers",
      "tunnels",
      "contribViewsWelcome"
    ],
    "ms-vscode.remote-explorer": [
      "contribViewsRemote",
      "extensionsAny",
      "contribViewsWelcome"
    ]
  }
}
```

### Result

The Remote Tunnel Service failure changed. This was a genuine progression.

Instead of reporting missing product metadata, the service now attempted to execute the configured tunnel application and failed because the executable did not exist:

From `Remote Tunnel Service2.log`:

```text
2026-06-30 16:35:16.226 [error] status error(undefined): + Error: spawn /data/data/com.termux/files/usr/lib/code-oss/bin/code-tunnel ENOENT
2026-06-30 16:35:16.236 [error] undefined
```

This proved that the VS Code-like product metadata was being consumed by the running application and that the failure had moved forward to tunnel helper process startup.

---

## 10. Supplying the Missing `code-tunnel` Helper

Because Code - OSS now expected:

```text
/data/data/com.termux/files/usr/lib/code-oss/bin/code-tunnel
```

but the native package did not contain that executable, a wrapper strategy was used.

The wrapper concept was:

```bash
PREFIX="/data/data/com.termux/files/usr"
BIN="$PREFIX/lib/code-oss/bin"

mkdir -p "$BIN"

cat > "$BIN/code-tunnel" <<'SH'
#!/data/data/com.termux/files/usr/bin/sh
exec /data/data/com.termux/files/usr/bin/proot-distro login ubuntu -- /usr/share/code/bin/code-tunnel "$@"
SH

chmod +x "$BIN/code-tunnel"
ln -sf "$BIN/code-tunnel" "$BIN/code-tunnel-oss"
```

The intention was to make the native Code - OSS process launch the official VS Code tunnel helper from the Ubuntu proot environment rather than trying to execute a glibc binary directly in the native Termux environment.

### Result

After this change the Remote Tunnel Service no longer emitted the `ENOENT` failure. The user reported:

```text
2026-06-30 16:42:14.926 [info] No other tunnel running
```

This was another confirmed progression:

```text
Missing tunnel product metadata  -> fixed enough to proceed
Missing code-tunnel executable   -> fixed with wrapper
Remote Tunnel Service startup    -> no longer erroring
```

---

## 11. Tunnel Transport After Helper Fix

After the helper executable issue was removed, the tunnel transport continued to succeed.

From `Remote - Tunnels5.log`:

```text
2026-06-30 16:45:07.423 [info] Resolving tunnel+victor...
2026-06-30 16:45:07.423 [info] Creating new tunnel proxy server
2026-06-30 16:45:13.901 [info] [proxy] Found tunnel (ID=fancy-chair-1xm3l36, Cluster=asse)
2026-06-30 16:45:13.906 [info] Remote resolution completed
2026-06-30 16:45:22.081 [info] [proxy] [connection.0] tunnel connection established
2026-06-30 16:45:22.273 [info] [proxy] Tunnel connection successful
```

The proxy was then reused through:

```text
/data/data/com.termux/files/usr/tmp/vscode-tunneling-588b9fc4c8b130e4.sock
```

For example:

```text
2026-06-30 16:45:23.058 [info] Resolving tunnel+victor...
2026-06-30 16:45:23.075 [info] Found running server in /data/data/com.termux/files/usr/tmp/vscode-tunneling-588b9fc4c8b130e4.sock
2026-06-30 16:45:23.105 [info] Remote resolution completed
```

A later test in `Remote - Tunnels6.log` repeated the same successful transport sequence:

```text
2026-06-30 16:55:29.361 [info] Resolving tunnel+victor...
2026-06-30 16:55:29.361 [info] Creating new tunnel proxy server
2026-06-30 16:55:36.495 [info] [proxy] Found tunnel (ID=fancy-chair-1xm3l36, Cluster=asse)
2026-06-30 16:55:36.512 [info] Remote resolution completed
2026-06-30 16:55:45.302 [info] [proxy] [connection.0] tunnel connection established
2026-06-30 16:55:45.511 [info] [proxy] Tunnel connection successful
```

The corresponding proxy socket was:

```text
/data/data/com.termux/files/usr/tmp/vscode-tunneling-3fb7e984916b486b.sock
```

These repeated successes ruled out the helper-process issue as the cause of the final connection rejection.

---

## 12. Remote-SSH Extension Interference and Clean-Profile Isolation

`Window2.log` revealed unrelated Remote-SSH errors still occurring in the same client environment:

```text
2026-06-30 16:42:02.616 [error] [Window] Extension 'ms-vscode-remote.remote-ssh CANNOT USE these API proposals 'resolvers, tunnels, terminalDataWriteEvent, contribViewsRemote, telemetry, contribRemoteHelp'. You MUST start in extension development mode or use the --enable-proposed-api command line flag
```

The same log also contained:

```text
2026-06-30 16:42:10.246 [error] [Window] [LocalProcess0][resolveAuthority(ssh-remote,1)][3861ms] returned an error {"code":"NotAvailable","message":"Remote - SSH is only supported in Microsoft versions of VS Code","detail":true}
```

and:

```text
2026-06-30 16:42:10.250 [error] [Window] resolveAuthority(ssh-remote) returned an error after 3866 ms Remote - SSH is only supported in Microsoft versions of VS Code
```

Because the objective was Remote Tunnels, these SSH errors were treated as interference/noise rather than as the primary tunnel failure.

### Clean profile experiment

A dedicated tunnel-only extension directory and user data directory were created conceptually as:

```text
~/.config/CodeTunnelTest
~/.vscode-tunnel-test/extensions
```

Only the tunnel-related extensions were copied into the clean extension directory:

```text
ms-vscode.remote-server-...
ms-vscode.remote-explorer-...
```

The client was then launched in the clean profile with the required proposed APIs:

```bash
code-oss \
  --user-data-dir "$HOME/.config/CodeTunnelTest" \
  --extensions-dir "$HOME/.vscode-tunnel-test/extensions" \
  --enable-proposed-api ms-vscode.remote-server \
  --enable-proposed-api ms-vscode.remote-explorer
```

### Result

Removing the Remote-SSH extension noise did not remove the final tunnel failure. The tunnel still resolved to a local WebSocket endpoint and the workbench still received `Unauthorized client refused` during negotiation.

This was valuable because it isolated the problem from the unrelated Microsoft Remote-SSH product check.

---

## 13. Node.js Global `navigator` Compatibility Error

Another independent extension compatibility problem appeared in the workbench logs:

```text
navigator is now a global in nodejs, please see https://aka.ms/vscode-extensions/navigator for additional info on this error.: PendingMigrationError
```

The relevant local setting used in the clean profile was:

```json
{
  "extensions.supportNodeGlobalNavigator": true
}
```

The test profile settings path was:

```text
~/.config/CodeTunnelTest/User/settings.json
```

### Result

The later `Window5.log` no longer showed the `navigator` migration error. However, the final remote connection still failed with the same authorization rejection.

This again separated an extension-runtime compatibility problem from the final client/server authorization problem.

---

## 14. Full VS Code-Like Profile and Product Identity Test

To test whether the server rejection depended on obvious product identity fields, the experiment went further than merely setting `tunnelApplicationName`.

The tested VS Code-like product values included:

```json
{
  "nameShort": "Code",
  "nameLong": "Visual Studio Code",
  "applicationName": "code",
  "dataFolderName": ".vscode",
  "serverApplicationName": "code-server",
  "serverDataFolderName": ".vscode-server",
  "tunnelApplicationName": "code-tunnel",
  "urlProtocol": "vscode"
}
```

The launch profile was also moved toward VS Code-style locations:

```text
~/.config/Code
~/.vscode/extensions
```

A representative launch command was:

```bash
code-oss \
  --user-data-dir "$HOME/.config/Code" \
  --extensions-dir "$HOME/.vscode/extensions" \
  --disable-extension ms-vscode-remote.remote-ssh \
  --enable-proposed-api ms-vscode.remote-server \
  --enable-proposed-api ms-vscode.remote-explorer
```

### Result

The Remote Tunnel Service remained healthy, tunnel resolution succeeded, and socket creation succeeded, but the connection was still rejected with:

```text
Connection error: Unauthorized client refused
```

Therefore, changing the obvious product identity and data-folder identifiers was insufficient.

---

## 15. Commit and Quality Matching Experiment

The remote server path showed the stable VS Code server commit:

```text
Stable-6928394f91b684055b873eecb8bc281365131f1c
```

A final product metadata test set the local Code - OSS product metadata to match that server identity:

```json
{
  "quality": "stable",
  "commit": "6928394f91b684055b873eecb8bc281365131f1c"
}
```

This was combined with the previously tested VS Code-like identity fields.

### Result

The later log still failed in exactly the same way. The representative final sequence from `Remote - Tunnels7.log` / final window capture was:

```text
2026-06-30 17:20:05.652 [info] [Window] Invoking resolveAuthority(tunnel)...
2026-06-30 17:20:19.410 [info] [Window] [LocalProcess0][resolveAuthority(tunnel,1)][13756ms] returned WebSocket(127.0.0.1:37933)
2026-06-30 17:20:19.418 [info] [Window] resolveAuthority(tunnel) returned 'WebSocket(127.0.0.1:37933)' after 13760 ms
2026-06-30 17:20:19.425 [info] [Window] Creating a socket (renderer-Management-f0084272-7213-43dc-99e7-8b5d1634369c)...
2026-06-30 17:20:19.436 [info] [Window] Creating a socket (renderer-ExtensionHost-3ced370e-f490-4ffa-895a-68fc80f11020)...
2026-06-30 17:20:27.768 [info] [Window] Creating a socket (renderer-Management-f0084272-7213-43dc-99e7-8b5d1634369c) was successful after 8345 ms.
2026-06-30 17:20:28.397 [info] [Window] Creating a socket (renderer-ExtensionHost-3ced370e-f490-4ffa-895a-68fc80f11020) was successful after 8962 ms.
2026-06-30 17:20:28.448 [error] [Window] [remote-connection][Management   ][f0084…][initial][WebSocket(127.0.0.1:37933)] received error control message when negotiating connection. Error:
2026-06-30 17:20:28.453 [error] [Window] Error: Connection error: Unauthorized client refused
```

The retry immediately reused the same proxy endpoint and failed again:

```text
2026-06-30 17:20:28.466 [info] [Window] Invoking resolveAuthority(tunnel)...
2026-06-30 17:20:28.531 [info] [Window] [LocalProcess0][resolveAuthority(tunnel,2)][74ms] returned WebSocket(127.0.0.1:37933)
2026-06-30 17:20:28.533 [info] [Window] resolveAuthority(tunnel) returned 'WebSocket(127.0.0.1:37933)' after 77 ms
2026-06-30 17:20:28.951 [error] [Window] [remote-connection][ExtensionHost][3ced3…][initial][WebSocket(127.0.0.1:37933)] received error control message when negotiating connection. Error:
2026-06-30 17:20:28.956 [error] [Window] Error: Connection error: Unauthorized client refused
```

Commit and quality matching therefore did not change the final outcome.

---

## 16. Server-Side Log Investigation

A server-side recursive grep was run for likely authorization-related terms, including variants of:

```text
Unauthorized
refused
client
auth
token
vsda
signature
connection
```

The output did **not** expose an explicit server-side line saying that the Code - OSS client had been rejected for a specific product identifier or native authentication component.

Instead, the server log contained apparently normal connection lifecycle entries such as:

```text
/home/hwjang/.vscode/cli/servers/Stable-6928394f91b684055b873eecb8bc281365131f1c/log.txt:21:[00:42:21] [<unknown>][2673b1a1][ExtensionHostConnection] New connection established.
/home/hwjang/.vscode/cli/servers/Stable-6928394f91b684055b873eecb8bc281365131f1c/log.txt:22:[00:42:21] [<unknown>][3e44437c][ManagementConnection] New connection established.
/home/hwjang/.vscode/cli/servers/Stable-6928394f91b684055b873eecb8bc281365131f1c/log.txt:23:[00:42:21] [<unknown>][2673b1a1][ExtensionHostConnection] <1975> Launched Extension Host Process.
```

A later pair was similar:

```text
/home/hwjang/.vscode/cli/servers/Stable-6928394f91b684055b873eecb8bc281365131f1c/log.txt:28:[00:43:05] [<unknown>][4b20e86a][ExtensionHostConnection] New connection established.
/home/hwjang/.vscode/cli/servers/Stable-6928394f91b684055b873eecb8bc281365131f1c/log.txt:29:[00:43:05] [<unknown>][4b20e86a][ExtensionHostConnection] <2672> Launched Extension Host Process.
/home/hwjang/.vscode/cli/servers/Stable-6928394f91b684055b873eecb8bc281365131f1c/log.txt:30:[00:43:05] [<unknown>][f3801d4e][ManagementConnection] New connection established.
```

And one longer-lived connection showed:

```text
/home/hwjang/.vscode/cli/servers/Stable-6928394f91b684055b873eecb8bc281365131f1c/log.txt:35:[00:44:20] [<unknown>][932895fb][ManagementConnection] New connection established.
/home/hwjang/.vscode/cli/servers/Stable-6928394f91b684055b873eecb8bc281365131f1c/log.txt:36:[00:44:20] [<unknown>][52b9f659][ExtensionHostConnection] New connection established.
/home/hwjang/.vscode/cli/servers/Stable-6928394f91b684055b873eecb8bc281365131f1c/log.txt:37:[00:44:20] [<unknown>][52b9f659][ExtensionHostConnection] <2772> Launched Extension Host Process.
```

The corresponding disconnection lifecycle included:

```text
/home/hwjang/.vscode/cli/servers/Stable-6928394f91b684055b873eecb8bc281365131f1c/log.txt:40:[01:06:55] [<unknown>][932895fb][ManagementConnection] The client has disconnected, will wait for reconnection 3h before disposing...
/home/hwjang/.vscode/cli/servers/Stable-6928394f91b684055b873eecb8bc281365131f1c/log.txt:41:[04:06:28] [<unknown>][52b9f659][ExtensionHostConnection] <2772> Extension Host Process exited with code: 0, signal: null.
/home/hwjang/.vscode/cli/servers/Stable-6928394f91b684055b873eecb8bc281365131f1c/log.txt:42:[04:07:03] [<unknown>][932895fb][ManagementConnection] The reconnection grace time of 3h has expired, so the connection will be disposed.
```

### Important limitation

These server entries do not identify which connection attempt came from `vscode.dev`, the Code - OSS test client, or another client session. Therefore, they show that the server was accepting and managing some tunnel client connections, but they do **not** by themselves prove the internal reason for the Code - OSS rejection.

The final root cause is therefore described conservatively in this report:

> The official VS Code Server/tunnel stack rejected the Code - OSS workbench during initial remote connection negotiation, after transport and socket establishment. The exact internal authorization criterion was not exposed by the collected server logs.

Hypotheses involving product identity, client signature/authentication components, protocol compatibility, or other official-build-specific behavior remain hypotheses unless a more detailed server trace or source-level instrumentation identifies the exact check.

---

## 17. Full Experimental Progression

The progression can be summarized as follows.

| Stage | Initial state | Action | Result |
|---|---|---|---|
| Tunnel discovery | Unknown | Connect to `tunnel+victor` | `Found tunnel` |
| Tunnel transport | Working | Start local proxy | `Tunnel connection successful` |
| Local stale socket | Intermittent failure | New proxy/socket created | Transport recovered |
| Proposed APIs | Blocked | Enable APIs for remote-server and remote-explorer | API gate no longer primary blocker |
| RTS product metadata | Missing | Patch product metadata | Failure moved forward |
| Tunnel executable | Missing | Provide `code-tunnel` wrapper via Ubuntu proot | `ENOENT` removed |
| RTS | Error-free | Re-run | `No other tunnel running` |
| Remote-SSH noise | Present | Clean tunnel-only profile | SSH noise removed |
| Node global `navigator` | PendingMigrationError | `extensions.supportNodeGlobalNavigator=true` | Migration error removed |
| Product identity | OSS | VS Code-like name/app/server/tunnel/url fields | Final rejection unchanged |
| Profile identity | OSS paths | VS Code-like data and extension paths | Final rejection unchanged |
| Commit/quality | OSS client values | Match server stable commit and quality | Final rejection unchanged |
| Transport resolver | Working | Resolve `tunnel+victor` | Local WebSocket returned |
| Workbench sockets | Working | Open Management + ExtensionHost channels | Socket creation succeeded |
| Initial negotiation | Failing | Multiple retries | `Unauthorized client refused` |

---

## 18. Final Technical Conclusion

The experiment reached much farther than a simple unsupported-extension failure.

The verified final connection sequence was:

```text
1. Code - OSS starts the Remote - Tunnels extension.
2. The extension resolves tunnel+victor.
3. A local tunnel proxy is created or reused.
4. The service finds the remote tunnel.
5. The tunnel transport connection succeeds.
6. The resolver returns a local WebSocket endpoint.
7. The workbench creates Management and ExtensionHost sockets successfully.
8. During initial remote connection negotiation, the client receives an error control message.
9. The workbench reports: Connection error: Unauthorized client refused.
```

The following issues were independently identified and fixed or isolated:

```text
- stale local tunnel proxy socket
- missing proposed API permissions
- missing tunnel product metadata
- missing local code-tunnel helper
- Remote-SSH extension interference
- Node.js global navigator migration failure
- OSS-vs-VS-Code product identity differences
- data-folder/profile identity differences
- local product commit/quality mismatch with observed server commit
```

After all of those interventions, the final negotiation rejection remained.

### Strongly supported conclusion

> JSON settings and obvious `product.json` identity fields are not sufficient to make this Code - OSS client connect successfully to the tested official VS Code Remote Tunnel server.

### What was not proven

The experiment did **not** conclusively prove which exact internal authorization mechanism produced the rejection. The collected client logs locate the failure at connection negotiation; the collected server logs do not expose the precise reason.

Therefore, claims such as "the failure is definitely caused by component X" should not be made from this evidence alone.

---

## 19. Recommended Practical Paths

The experiments support the following practical choices.

### Path A: Use the official tunnel client path

The server tunnel was already verified to work through `vscode.dev`.

Architecture:

```text
victor: official VS Code tunnel
client: vscode.dev or another supported official VS Code client
```

### Path B: Preserve Code - OSS locally but change the transport/remote-server pairing

Architecture:

```text
client: Code - OSS
transport: SSH or another port tunnel
remote integration: an OSS-compatible remote server / Open Remote SSH-style workflow
```

This changes the transport and remote integration model rather than trying to make the official Remote Tunnels server accept the Code - OSS workbench.

---

# Appendix A. Commands Used or Proposed During the Investigation

This appendix preserves the main command inputs used during the experiment. Some commands were diagnostic; others were A/B compatibility tests. They are recorded as experiment history, not as a recommended final configuration.

## A.1 Minimal tunnel-oriented settings cleanup

```json
{
  "remote.SSH.showLoginTerminal": true,
  "remote.SSH.useLocalServer": false,
  "remote.SSH.useExecServer": false
}
```

The tunnel credential override was removed from the test configuration:

```json
"remote.tunnels.tunnelCredentialCommand": null
```

## A.2 Clear local tunnel proxy sockets

```bash
pkill -f 'code-oss|Code - OSS|vscode-tunneling|remote-server' 2>/dev/null || true

rm -f /data/data/com.termux/files/usr/tmp/vscode-tunneling-*.sock
rm -f "$TMPDIR"/vscode-tunneling-*.sock 2>/dev/null || true
```

## A.3 Proposed API runtime configuration

```json
{
  "enable-proposed-api": [
    "ms-vscode.remote-server",
    "ms-vscode.remote-explorer"
  ]
}
```

Direct launch equivalent:

```bash
code-oss \
  --enable-proposed-api ms-vscode.remote-server \
  --enable-proposed-api ms-vscode.remote-explorer
```

## A.4 Search for product metadata files

The diagnostic intent was to recursively find `product.json` files and print fields including:

```text
nameShort
applicationName
dataFolderName
serverApplicationName
serverDataFolderName
tunnelApplicationName
urlProtocol
```

The observed output is preserved in Section 8.

## A.5 Backup and patch local product file

Primary local product file:

```bash
PRODUCT="/data/data/com.termux/files/usr/lib/code-oss/resources/app/product.json"
cp "$PRODUCT" "$PRODUCT.bak.$(date +%s)"
```

## A.6 VS Code-like product identity test

```python
# Experimental values applied to the local Code - OSS product metadata.
d["nameShort"] = "Code"
d["nameLong"] = "Visual Studio Code"
d["applicationName"] = "code"
d["dataFolderName"] = ".vscode"
d["serverApplicationName"] = "code-server"
d["serverDataFolderName"] = ".vscode-server"
d["tunnelApplicationName"] = "code-tunnel"
d["urlProtocol"] = "vscode"
```

## A.7 Explicit tunnel application configuration test

```python
d["tunnelApplicationConfig"] = {
    "editorWebUrl": "https://vscode.dev",
    "webEndpointUrl": "https://main.vscode-cdn.net",
    "extension": {
        "friendlyName": "Remote - Tunnels",
        "extensionId": "ms-vscode.remote-server",
        "startEntry": {
            "helpLink": "https://aka.ms/remote-tunnels",
            "command": "remote-tunnels.connectToTunnel",
            "label": "Connect to Tunnel"
        }
    }
}
```

## A.8 `code-tunnel` wrapper experiment

```bash
PREFIX="/data/data/com.termux/files/usr"
BIN="$PREFIX/lib/code-oss/bin"

mkdir -p "$BIN"

cat > "$BIN/code-tunnel" <<'SH'
#!/data/data/com.termux/files/usr/bin/sh
exec /data/data/com.termux/files/usr/bin/proot-distro login ubuntu -- /usr/share/code/bin/code-tunnel "$@"
SH

chmod +x "$BIN/code-tunnel"
ln -sf "$BIN/code-tunnel" "$BIN/code-tunnel-oss"
```

## A.9 Clean tunnel-only profile setup

```bash
rm -rf "$HOME/.config/CodeTunnelTest" "$HOME/.vscode-tunnel-test"
mkdir -p "$HOME/.vscode-tunnel-test/extensions"
```

The tunnel-related extensions were copied from the normal extension directories into the clean directory, then the client was started with:

```bash
code-oss \
  --user-data-dir "$HOME/.config/CodeTunnelTest" \
  --extensions-dir "$HOME/.vscode-tunnel-test/extensions" \
  --enable-proposed-api ms-vscode.remote-server \
  --enable-proposed-api ms-vscode.remote-explorer
```

## A.10 Node global navigator workaround test

```bash
mkdir -p "$HOME/.config/CodeTunnelTest/User"

cat > "$HOME/.config/CodeTunnelTest/User/settings.json" <<'JSON'
{
  "extensions.supportNodeGlobalNavigator": true
}
JSON
```

## A.11 Commit/quality identity test

Observed server stable commit:

```text
6928394f91b684055b873eecb8bc281365131f1c
```

Experimental product metadata:

```python
d["quality"] = "stable"
d["commit"] = "6928394f91b684055b873eecb8bc281365131f1c"
```

## A.12 Server-side log search

A representative diagnostic search was:

```bash
grep -RniE "Unauthorized|refused|client|auth|token|vsda|signature|connection" \
  ~/.vscode-server ~/.vscode-cli ~/.vscode 2>/dev/null | tail -200
```

Recent log discovery:

```bash
find ~/.vscode-server ~/.vscode-cli ~/.vscode \
  -type f \( -name "*.log" -o -name "server-main.log" \) \
  -printf "%T@ %p\n" 2>/dev/null | sort -n | tail -30
```

Observed recent remote log files included paths such as:

```text
/home/hwjang/.vscode-server/data/logs/20260630T153928/remoteagent.log
/home/hwjang/.vscode-server/data/logs/20260630T154159/remoteagent.log
/home/hwjang/.vscode-server/data/logs/20260630T155503/remoteagent.log
/home/hwjang/.vscode-server/data/logs/20260630T160912/remoteagent.log
/home/hwjang/.vscode-server/data/logs/20260630T161426/remoteagent.log
/home/hwjang/.vscode-server/data/logs/20260630T163659/remoteagent.log
/home/hwjang/.vscode-server/data/logs/20260630T164521/remoteagent.log
/home/hwjang/.vscode-server/data/logs/20260630T165545/remoteagent.log
/home/hwjang/.vscode-server/data/logs/20260630T170620/remoteagent.log
```

---

# Appendix B. Key Evidence Excerpts by Log File

## B.1 `Remote Tunnel Service.log`

```text
2026-06-30 15:54:50.514 [error] Missing 'tunnelApplicationConfig' or 'tunnelApplicationName' in product.json. Remote tunneling is not available.
```

## B.2 `Remote Tunnel Service2.log`

```text
2026-06-30 16:35:16.226 [error] status error(undefined): + Error: spawn /data/data/com.termux/files/usr/lib/code-oss/bin/code-tunnel ENOENT
2026-06-30 16:35:16.236 [error] undefined
```

## B.3 RTS after helper fix

User-observed result:

```text
2026-06-30 16:42:14.926 [info] No other tunnel running
```

## B.4 `Remote - Tunnels4.log`

```text
2026-06-30 15:54:48.745 [info] Resolving tunnel+victor...
2026-06-30 15:54:48.745 [info] Creating new tunnel proxy server
2026-06-30 15:54:55.736 [info] [proxy] Found tunnel (ID=fancy-chair-1xm3l36, Cluster=asse)
2026-06-30 15:54:55.748 [info] Remote resolution completed
2026-06-30 15:55:03.984 [info] [proxy] [connection.0] tunnel connection established
2026-06-30 15:55:04.194 [info] [proxy] Tunnel connection successful
```

## B.5 `Remote - Tunnels5.log`

```text
2026-06-30 16:45:07.423 [info] Resolving tunnel+victor...
2026-06-30 16:45:07.423 [info] Creating new tunnel proxy server
2026-06-30 16:45:13.901 [info] [proxy] Found tunnel (ID=fancy-chair-1xm3l36, Cluster=asse)
2026-06-30 16:45:13.906 [info] Remote resolution completed
2026-06-30 16:45:22.081 [info] [proxy] [connection.0] tunnel connection established
2026-06-30 16:45:22.273 [info] [proxy] Tunnel connection successful
```

## B.6 `Remote - Tunnels6.log`

```text
2026-06-30 16:55:29.361 [info] Resolving tunnel+victor...
2026-06-30 16:55:29.361 [info] Creating new tunnel proxy server
2026-06-30 16:55:36.495 [info] [proxy] Found tunnel (ID=fancy-chair-1xm3l36, Cluster=asse)
2026-06-30 16:55:36.512 [info] Remote resolution completed
2026-06-30 16:55:45.302 [info] [proxy] [connection.0] tunnel connection established
2026-06-30 16:55:45.511 [info] [proxy] Tunnel connection successful
```

## B.7 Final workbench negotiation failure

```text
2026-06-30 17:20:19.418 [info] [Window] resolveAuthority(tunnel) returned 'WebSocket(127.0.0.1:37933)' after 13760 ms
2026-06-30 17:20:19.425 [info] [Window] Creating a socket (renderer-Management-f0084272-7213-43dc-99e7-8b5d1634369c)...
2026-06-30 17:20:19.436 [info] [Window] Creating a socket (renderer-ExtensionHost-3ced370e-f490-4ffa-895a-68fc80f11020)...
2026-06-30 17:20:27.768 [info] [Window] Creating a socket (renderer-Management-f0084272-7213-43dc-99e7-8b5d1634369c) was successful after 8345 ms.
2026-06-30 17:20:28.397 [info] [Window] Creating a socket (renderer-ExtensionHost-3ced370e-f490-4ffa-895a-68fc80f11020) was successful after 8962 ms.
2026-06-30 17:20:28.448 [error] [Window] [remote-connection][Management   ][f0084…][initial][WebSocket(127.0.0.1:37933)] received error control message when negotiating connection. Error:
2026-06-30 17:20:28.453 [error] [Window] Error: Connection error: Unauthorized client refused
```

---

## 20. Reproducibility Notes

1. The experiment involved several stateful changes to the local Code - OSS installation, including `product.json` edits and a helper wrapper in the installation tree. Backups should be retained before reproducing any such test.
2. The exact tunnel ID, cluster, local proxy socket names, local WebSocket ports, process IDs, and timestamps are expected to vary across runs.
3. The server-side successful connection entries cannot be unambiguously mapped to a particular client type from the provided logs alone.
4. The fact that `vscode.dev` worked is the strongest control that the server tunnel itself was operational.
5. The final `Unauthorized client refused` condition was reproducible across multiple local configurations after the tunnel transport layer was confirmed healthy.

---

## 21. Final Result Statement

**Experiment result:** unsuccessful for the original target architecture.

The tested combination:

```text
Official VS Code Remote Tunnel server
        +
Native Termux Code - OSS desktop client
        +
Remote - Tunnels extension
```

could be made to progress through tunnel discovery, proxy startup, remote authority resolution, WebSocket endpoint creation, and Management/ExtensionHost socket creation. It still failed at initial remote connection negotiation with:

```text
Connection error: Unauthorized client refused
```

The experiment therefore demonstrates that the observed failure is deeper than a missing JSON setting, missing proposed API flag, missing tunnel application name, missing tunnel helper executable, or obvious product identity mismatch.
