# Code OSS client -> official VS Code Remote Tunnel

**Status:** unsuccessful for the target architecture; transport path deeply validated  
**Experiment date:** 2026-06-30  
**Provenance:** first-hand session report (`report.md`)

## Question

Can a native Termux Code OSS desktop client connect to a remote machine that remains on the official VS Code `code tunnel` / server stack?

## Control

The same remote tunnel worked from `vscode.dev`, establishing that the remote machine, tunnel, and account path were operational during the investigation.

## Result

The Code OSS path progressed through:

```text
tunnel discovery
  -> local proxy startup
  -> remote authority resolution
  -> local WebSocket endpoint
  -> Management socket
  -> ExtensionHost socket
  -> initial remote negotiation
  -> Unauthorized client refused
```

The final rejection remained after fixing or testing several client-side metadata, proposed-API, tunnel-helper, profile, and identity hypotheses.

## Decision

Treat the official-tunnel/Code-OSS combination as unsuccessful for the tested architecture. The experiment is valuable because it demonstrates that the failure occurs beyond basic tunnel transport and socket establishment rather than at the first visible UI error.

See [`report.md`](report.md).
