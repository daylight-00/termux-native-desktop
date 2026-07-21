# Selected Obsidian provider composition review

## Decision

```text
composition decision:             REVIEWED_BLOCKED_INCOMPLETE
accepted bounded provider roots:  30
accepted exact members:           40
included members:                 39
deferred members:                  1
selected GTK identity gaps:        3
target manifest allowed:          NO
activation allowed:               NO
```

The accepted-member table is generated at `selected-provider-composition-members.tsv`; remaining selected identities are generated at `selected-provider-composition-gaps.tsv`. The review is non-materializing and does not authorize target paths, aliases, copies, installation, deployment, service operation, or activation.

## Latest bounded tranche

The exact atomic AT-SPI2 core family is included only for the selected GTK 3.24.49 accessibility library-linkage boundary:

```text
libatk-1.0.so.0.25611.1       -> libatk-1.0.so.0
libatk-bridge-2.0.so.0.0.0    -> libatk-bridge-2.0.so.0
libatspi.so.0.0.1             -> libatspi.so.0
```

The bridge directly binds the accepted ATK and AT-SPI sibling SONAMEs. The family remains one atomic lifecycle with its exact GIR/typelib artifacts. Exactly seven activation metadata files stay in the disabled namespace; no service, helper, D-Bus bus, registry daemon, accessibility enablement, target population, or activation authority is accepted.

The exact Class B recipe remains separated from the retained Class C producing record. Approved-supplier publication is absent and not inferred. Ordinary Termux/bionic packages and Debian oracle members remain excluded as provider bytes.

## Remaining gaps

The selected `libgdk-3.so.0.2417.32` and `libgtk-3.so.0.2417.32` pair remains `BLOCKED_NO_TERMUX_GLIBC_PROVIDER_CANDIDATE`. Ordinary bionic GTK does not authorize glibc provider bytes or infer backend, settings, theme, accessibility, input, printing, portal, or service behavior.

Selected `libselinux.so.1` remains `BLOCKED_NO_TERMUX_GLIBC_PROVIDER_CANDIDATE`. Android and ordinary Termux/bionic SELinux libraries are boundary evidence only and do not authorize a cross-world alias, policy loading, relabeling, or glibc compatibility.

All three remaining selected identities lack accepted provider rows. The Class D composition therefore remains incomplete and no target manifest is allowed.

## Production-boundary disposition and next tranche

The next tranche is `GTK3_CORE_ATOMIC_CANDIDATE_PREPARATION`: prepare one exact Class B GTK 3.24.49 recipe candidate and one isolated Class C GDK/GTK pair, or retain a precise source, backend, dependency, pair-atomicity, or service blocker. It does not authorize provider authority, supplier publication, package installation, target population, display/accessibility service activation, deployment, or activation.
