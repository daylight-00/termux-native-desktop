# Bounded libcloudproviders provider authority

> Decision: `ACCEPTED_BOUNDED_PROVIDER`
>
> Scope: exact `libcloudproviders.so.0.3.6` for GTK 3.24.49 `GtkPlacesSidebar` cloud-provider account integration only.

## Exact coordinates

```text
recipe root:    gpkg/libcloudproviders
recipe tree:    ca7597d86cb1610e64f209ff2b84c3ea13c4357a
build blob:     cb073e2018c70bbf92596433da4fda7b8e023c55
artifact:       libcloudproviders-glibc 0.3.6
artifact SHA:   62b4d4f5263a7750f56e4655fdf91011ec5dc2e137f4e73a08506ddbaa64c1ae
member:         libcloudproviders.so.0.3.6
member SHA:     54dea7e30b9e02f5626a374e5b62e5e975684a426a940f525a18eb4ce9e4f030
SONAME:         libcloudproviders.so.0
selected row:   selected:b912b41387c558b52895
```

## Class B adaptation boundary

The only package-specific configuration delta is `-Dvapigen=false`. It disables Vala binding generation. It does not patch the C implementation, change the C shared-library ABI or SONAME, change the DBus client API, or change GTK's C consumer path. This is accepted as a bounded build-surface reduction, not as producing-build equivalence.

## Consumer binding

GTK 3.24.49 declares cloudproviders support as optional and disabled by default, while the selected Debian `libgtk-3-0t64 3.24.49-3` runtime directly depends on `libcloudproviders0`. GTK's `GtkPlacesSidebar` and sidebar rows include and call collector, provider and account APIs when `HAVE_CLOUDPROVIDERS` is enabled. This closes the selected-build feature and consumer binding without a device probe.

Accepted capability:

```text
GtkPlacesSidebar cloud-provider account collection
account name, status, status-details, icon and URI integration
```

## Dependency and service boundary

The exact library is a DBus client-side runtime provider. This decision does not accept or require the existence of a session bus, cloud-provider server implementations, configured accounts, or service activation. Absence of those services means the optional integration has no accounts to display; it does not create an alternate library provider. GLib/GIO remain accepted dependencies. DBus library/session/service authority remains separate.

## Exclusions

- Vala, GIR/introspection, headers, pkg-config, documentation and development surfaces;
- cloud-provider servers, services, accounts and service activation;
- Debian oracle bytes as target authority;
- complete GTK composition, target paths, target population, deployment or activation;
- producing-build equivalence.

## Update and rollback

Re-review on artifact/member/version/SHA/SONAME, recipe tree or build-script blob, `vapigen` configuration, GTK tag/package dependency/API call surface, DBus client contract, or candidate multiplicity changes. Before materialization revoke this row; after a future immutable generation, roll back the selector to the previous generation.

## Authority effect

The exact member is accepted only for the selected GTK 3.24.49 PlacesSidebar cloud-account integration. Composition remains incomplete and target population and activation remain blocked.
