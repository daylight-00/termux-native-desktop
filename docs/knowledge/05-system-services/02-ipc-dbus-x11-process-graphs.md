# 11. IPC, D-Bus, X11, Wayland, and Process Graphs

A desktop application rarely operates as one isolated process. It communicates with display servers, buses, helpers, child processes, and services. This chapter treats those interactions as explicit runtime graphs.

## 11.1 IPC: processes exchanging information

Common inter-process communication mechanisms include:

```text
pipes
FIFOs
Unix domain sockets
TCP/UDP sockets
shared memory
signals
file descriptor passing
```

The choice of mechanism affects naming, visibility, security, buffering, and lifecycle.

## 11.2 Pipes

A pipe is a kernel buffer connecting a write endpoint and read endpoint.

```text
producer
    -> write fd
    -> kernel pipe buffer
    -> read fd
    -> consumer
```

Pipes are excellent for parent/child and shell-pipeline communication but do not provide the same addressing/discovery model as a socket service.

## 11.3 Unix domain sockets

A Unix socket is a local IPC endpoint. Filesystem-named Unix sockets can use pathnames such as:

```text
/tmp/service.sock
```

The path is an endpoint name, not a regular data file. Copying the pathname object does not recreate the listening server.

A local client/server relationship:

```text
client process
    -> connect(socket address)
    -> kernel socket object
    -> listening server process
```

If two environments have incompatible path views, a server can exist but be unreachable because the client resolves a different socket path.

## 11.4 Shared kernel does not imply shared pathname view

Termux native and PRoot Debian processes use the same underlying kernel, but PRoot can present translated path views.

Therefore IPC reasoning needs two questions:

```text
Are both processes using the same kernel transport?
Do they resolve/reach the same endpoint address?
```

This is why local TCP loopback can sometimes be an effective control experiment when a Unix socket pathname is hidden or mismatched.

## 11.5 D-Bus is a protocol and service ecosystem

D-Bus should not be reduced to `libdbus-1.so`.

A complete relationship can involve:

```text
application
    -> D-Bus client library
    -> bus address
    -> socket transport
    -> bus daemon/broker
    -> destination service
```

There are common concepts of session and system buses, but the exact environment determines which buses exist and which services are available.

`DBUS_SESSION_BUS_ADDRESS` is an endpoint description. A shared library dependency on `libdbus` does not prove that a bus daemon is present or reachable.

## 11.6 `libsystemd` does not imply systemd PID 1

A library can provide APIs used by an application without the full service manager being the init system.

Therefore:

```text
DT_NEEDED libsystemd.so
```

must not be interpreted as:

```text
systemd must be PID 1
```

The runtime requirement must be discovered at the API/feature level.

## 11.7 X11 is a client/server protocol

An X11 application is a client.

```text
X11 app
    -> X11 client libraries
    -> X11 protocol transport
    -> X server
    -> display/input integration
```

In this project:

```text
bionic XFCE/native apps ----┐
                            ├--> Termux:X11 :1
patched glibc apps ---------┘
```

The two ABI worlds can share one display protocol while keeping separate client-library stacks.

This is a central example of a good bridge boundary.

## 11.8 `DISPLAY`

`DISPLAY` is not a library path. It tells X11 clients where the display server endpoint is.

Conceptually:

```text
DISPLAY=:1
    -> local display number
    -> client library derives transport endpoint
    -> connect to X server
```

The exact socket layout matters. The project found that Termux-aware glibc X11/xcb libraries are load-bearing because client transport behavior must match Termux:X11’s local endpoint arrangement.

## 11.9 Wayland mental model

A Wayland application communicates with a compositor/server endpoint, commonly discovered through variables such as:

```text
XDG_RUNTIME_DIR
WAYLAND_DISPLAY
```

Conceptually:

```text
Wayland client
    -> Unix socket
    -> compositor
    -> display/input coordination
```

Although the current project centers Termux:X11, the same lesson applies: environment variables describe protocol endpoints and runtime directories, not merely decorative configuration.

## 11.10 Runtime directories

`XDG_RUNTIME_DIR` is intended for per-user runtime objects such as sockets and transient state.

A good runtime directory contract considers:

```text
ownership
permissions
lifecycle
which process world uses it
```

The project intentionally keeps separate runtime-directory policy for bionic session processes and glibc applications. Unifying them merely because they run on one phone would erase a useful boundary.

## 11.11 Electron and Chromium process graphs

A simplified graph:

```text
browser/main process
    ├── renderer process
    ├── renderer process
    ├── GPU process
    ├── utility process
    └── crash/helper process
```

IPC channels connect these processes using OS primitives.

Therefore a launcher must be treated as constructing a **process-family runtime contract**. Environment, file descriptors, proxy variables, library policy, and GPU policy can be inherited by children.

## 11.12 Environment inheritance

A process receives an environment at execution. Child processes normally inherit a copy unless the parent modifies the environment used for spawning.

This creates both power and risk:

```text
launcher sets DISPLAY
    -> children can reach X server

launcher exports wrong LD_LIBRARY_PATH
    -> helpers may load incompatible libraries
```

A strong design rule is to set policy at the smallest scope that needs it.

## 11.13 Launchers as contract assemblers

A launcher is not just a convenience alias. It can compose:

```text
entrypoint
PATH policy
loader/runtime policy
DISPLAY endpoint
XDG runtime location
GPU provider selection
TLS trust path
shim path
feature flags
sandbox policy
```

But a launcher becomes a maintenance problem if it silently accumulates unrelated policies. The project should separate base world policy, capability-provider selection, and application-family policy conceptually even when implemented through shell scripts initially.

## 11.14 Service availability versus client library availability

A recurring failure pattern:

```text
client library loads
    -> application calls API
    -> expected service socket absent
    -> runtime failure
```

Examples:

```text
D-Bus client without reachable bus
X11 client without display server
proxy-aware client without proxy listener
plugin loader without plugin directory
```

This is why the IPC/process graphs are separate from the ELF graph.

## 11.15 Project connection: URL opening

A desktop app may invoke an `xdg-open`-like interface.

In the project, a shim can bridge from the glibc application world to Termux/Android intent behavior.

Conceptually:

```text
glibc application
    -> xdg-open command contract
    -> project shim
    -> Termux/Android integration
```

This is an example of an explicit bridge: the foreign app consumes a familiar interface while the shim translates into host-native behavior.

## 11.16 A graph-based debugging method

For any IPC failure, draw:

```text
client process
    -> client library
    -> address discovery
    -> transport type
    -> endpoint path/address
    -> server process
    -> server state
```

Then verify each edge.

For X11:

```text
app process
    -> correct libX11/libxcb world?
    -> DISPLAY value?
    -> derived socket path?
    -> socket visible/reachable?
    -> Termux:X11 process alive?
```

This is more reliable than repeatedly changing unrelated environment variables.

## References

- D-Bus specification: <https://dbus.freedesktop.org/doc/dbus-specification.html>
- X.Org documentation: <https://www.x.org/wiki/Documentation/>
- Wayland documentation: <https://wayland.freedesktop.org/docs/html/>
- Project desktop-session guide: [`../../desktop-session.md`](../../desktop-session.md)
- Project architecture: [`../../architecture.md`](../../architecture.md)
