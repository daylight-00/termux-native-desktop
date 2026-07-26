# libSELinux provider evidence blocker — superseded by consumer reselection

The historical review correctly found no approved Termux-glibc `libselinux.so.1` package or pinned recipe and correctly rejected Android/bionic SELinux bytes as a different ABI and policy world.

`LIBSELINUX-CONSUMER-NECESSITY-001` supersedes the active blocker with `DEPENDENCY_ELIMINATION_OR_RESELECTION`. Debian oracle `libmount1:arm64 2.41-5` carried optional SELinux-enabled libmount functionality. The selected exact `libmount-glibc 2.40.2-1` replacement has no `libselinux.so.1` `DT_NEEDED` entry and no imported SELinux symbols, and the v101 GTK candidate completed without a provider.

```text
historical blocker state: SUPERSEDED_DEPENDENCY_ELIMINATED_BY_CONSUMER_RESELECTION
provider authority:       NOT REQUIRED
provider build:           NOT AUTHORIZED
policy mutation:          BLOCKED
target / activation:      BLOCKED
```

The historical blocker remains evidence that cross-world substitution was never acceptable. Canonical current evidence is `docs/evidence/libselinux-direct-consumer-necessity-review.md`.
