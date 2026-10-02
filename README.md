# termux-native-desktop

Native desktop workstation on a stock, non-root Android phone: Termux, glibc applications and real Adreno GPU acceleration, without PRoot in the normal runtime.

## Highlights

- **Native session** — Termux:X11 + XFCE, no container as the normal execution path
- **glibc applications** — VS Code and Obsidian on a managed glibc application world
- **GPU** — Mesa Turnip + Zink, validated on Adreno 730 with stock Android KGSL
- **Native Python** — disposable `uv`-based base environment
- **Immutable releases** — `tools/deploy` materializes each release behind one stable `current` pointer
- **Evidence first** — experiments and reports are kept next to the code; failed paths stay as records

## Architecture

```text
Termux native host
├── bionic apps and services · uv-base · Termux:X11 bridge
├── glibc applications (VS Code, Obsidian)
│   └── managed glibc substrate + selected compatibility providers
└── graphics: Mesa/Turnip (bionic, glibc) · ANGLE Vulkan · Zink
```

- **PRoot** — dependency solver, library/data warehouse and behavioral oracle; excluded from normal application execution
- **Boundaries** — explicit bridges between the bionic and glibc worlds

## Repository

- `modules/` — project-authored integrations
  - `desktop/` — Termux:X11 + XFCE session launcher
  - `gl/` — glibc application world integration
  - `shell/` — Bash bootstrap
  - `uv-base/` — native base environment
- `packages/` — lifecycle and launch definitions for external payloads (`mesa-glibc`, `gdkpixbuf-glibc`, `obsidian`, `vscode`, `cpython-android-runtime`)
- `experiments/` — evidence, provenance, diagnostics
- `tools/` — deploy and repository check tooling
- `tests/` — repository validation
- `docs/` — guides, decisions, evidence

## Documentation

- [Architecture](docs/architecture.md)
- [Desktop session](docs/desktop-session.md)
- [glibc layer](docs/glibc-layer.md)
- [GPU acceleration](docs/gpu.md)
- [Timeline](docs/timeline.md)
- [Status ledger](STATUS.md) · [Docs index](docs/INDEX.md)

## Development

```sh
tests/run-repository --fast   # or --full
```

- Needs `bash`, `git`, Python ≥ 3.11

## Related

- [python-build-standalone-android](https://github.com/daylight-00/python-build-standalone-android) — redistributable Python builds for Android

## License

- [MIT](LICENSE)
- Third-party recipes and patches keep their upstream licenses
