
# Decision index

Decision records preserve durable choices and their lifecycle. Current state remains under `docs/current/`.

## Status meanings

```text
proposed
    explicit review surface; no authority effect

accepted
    binding current decision

superseded
    replaced for current use; retained as provenance

rejected
    considered and not adopted

historical
    past decision context without current force
```

| Decision | Status | Current meaning |
|---|---|---|
| [`0001-no-proot-runtime.md`](0001-no-proot-runtime.md) | accepted | PRoot is excluded from normal application execution and retained for bounded oracle/supply/control roles. |
| [`0002-glibc-core-from-termux-glibc-repo.md`](0002-glibc-core-from-termux-glibc-repo.md) | superseded | Its protected glibc/X11 observations remain evidence; broad “everything else from Debian” ownership is replaced by role- and provider-specific authority. |
| [`0003-mesa-kmds-msm-kgsl.md`](0003-mesa-kmds-msm-kgsl.md) | accepted / scoped | The validated project Mesa build retains `msm,kgsl`; KGSL is the Android runtime device interface. |
| [`0004-single-main-and-immutable-release-deployment.md`](0004-single-main-and-immutable-release-deployment.md) | accepted | `main` is the long-lived integration branch and runtime deployment uses immutable releases plus explicit activation. |
| [`0005-proportional-assurance-depth.md`](0005-proportional-assurance-depth.md) | accepted | Assurance follows the exact claim, implementation class, changed boundary, and risk; blanket supplier producing-build reconstruction is not the default. |

ADR 0005 is binding evidence policy but has no automatic provider, composition, population, or activation effect. A proposed decision must never be cited as accepted policy. A superseded record remains useful historical evidence but must not be applied as current universal policy.
