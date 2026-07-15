
# Architecture documentation

This is the canonical router for the current integrated system model and component contracts.

| Question | Read |
|---|---|
| How is the whole system composed? | [`../architecture.md`](../architecture.md) |
| How is the glibc application world bounded and operated? | [`../glibc-layer.md`](../glibc-layer.md) |
| How are graphics providers and acceptance evidence composed? | [`../gpu.md`](../gpu.md) |
| How does the Termux:X11 desktop session work? | [`../desktop-session.md`](../desktop-session.md) |
| Which project-owned physical modules implement capabilities? | [`../../modules/README.md`](../../modules/README.md) |
| Which external payload/provider lifecycle belongs to a package? | [`../../packages/README.md`](../../packages/README.md) |
| Where is Mesa workspace/provider ownership defined? | [`../../packages/mesa-glibc/README.md`](../../packages/mesa-glibc/README.md) |

Architecture documents must distinguish current validated realization from target semantics and historical implementation. Current paths can be replaceable even when their behavior is accepted.

Top-down constitutional sources are routed through [`../constitution/README.md`](../constitution/README.md). Architecture does not silently redefine those invariants.
