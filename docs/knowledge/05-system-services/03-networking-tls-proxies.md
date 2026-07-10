# 12. Networking, DNS, TLS, Proxies, and Transport Fallbacks

Networking problems are often described too broadly as “the internet is broken.” A useful systems model separates endpoint discovery, routing, transport, encryption, proxy mediation, and application protocol.

## 12.1 Socket as a file descriptor-backed kernel object

A network client begins conceptually with:

```text
socket()
    -> fd
    -> connect()
    -> send/recv or read/write
```

The fd refers to a kernel socket object. This fits the same Unix descriptor model used for files, pipes, terminals, and devices.

## 12.2 Address and port

An endpoint such as:

```text
192.0.2.10:443
```

contains two different pieces of information:

```text
IP address
    -> network host/interface destination

port
    -> transport endpoint on that host
```

The “building and room number” analogy is imperfect but useful at beginner level.

## 12.3 Server lifecycle

A TCP server commonly follows a pattern like:

```text
socket
    -> bind(address, port)
    -> listen
    -> accept connections
```

A client:

```text
socket
    -> connect(server address, port)
```

The kernel TCP stack maintains connection state for each side.

## 12.4 `localhost`

`127.0.0.1` is an IPv4 loopback address.

Conceptually:

```text
client process
    -> kernel network stack
    -> loopback route
    -> local listening socket
    -> server process
```

No external Wi-Fi path is required.

But localhost is relative to network namespace context. Separate network namespaces can have separate loopback interfaces and routing tables.

## 12.5 Unix socket versus TCP loopback

Both can support local IPC, but they use different namespaces and transports.

```text
Unix socket
    -> local socket address, often pathname-based

TCP loopback
    -> IP stack, address + port
```

This distinction can help diagnose path-view problems between environments sharing a kernel.

## 12.6 DNS

DNS maps names to information such as IP addresses.

A simplified connection path:

```text
application hostname
    -> resolver
    -> DNS query/configuration
    -> address result
    -> TCP/UDP transport attempt
```

A successful DNS lookup does not prove that the target TCP endpoint or TLS connection will work.

## 12.7 Resolver stack differences matter

A glibc process and a bionic process can use the same network kernel while differing in resolver integration and filesystem configuration assumptions.

Therefore a relocated glibc application needs more than `libc.so.6`; name resolution must be tested in the actual target environment.

The lesson generalizes:

```text
kernel network availability
    !=
userspace resolver configuration correctness
```

## 12.8 TCP

TCP provides a reliable ordered byte-stream abstraction between endpoints.

Key beginner-level properties:

```text
ordered bytes
retransmission/reliability machinery
flow control
congestion control
```

Application write boundaries are not message boundaries.

```text
write("hello")
write("world")
```

can be read as:

```text
"helloworld"
```

or in several chunks. Higher-level protocols define framing.

## 12.9 UDP

UDP provides datagram-oriented transport without TCP’s connection/reliability semantics.

Simplified contrast:

```text
TCP -> ordered byte stream
UDP -> individual datagrams
```

Applications choosing UDP must account for the reliability/order behavior their protocol needs.

## 12.10 Routing and interfaces

The kernel chooses an output path according to routing state.

```text
destination address
    -> route lookup
    -> output interface / next hop
    -> transmission path
```

Possible interfaces include:

```text
loopback
Wi-Fi
cellular-related interfaces
VPN/tunnel interfaces
virtual interfaces
```

A timeout can therefore arise below the application protocol layer.

## 12.11 HTTP and HTTPS layering

A simplified HTTPS path:

```text
DNS
    -> TCP connection
    -> TLS handshake
    -> HTTP exchange
```

Failure classes differ:

```text
name resolution failure
connection refusal
connection timeout
TLS certificate validation error
HTTP authorization/application error
```

Debug from lower layers upward.

## 12.12 TLS and trust stores

TLS provides encrypted and integrity-protected transport plus peer authentication mechanisms.

A client needs trust material and policy for certificate validation.

Therefore a relocated application can have:

```text
ELF load success
DNS success
TCP success
TLS handshake failure due to trust-store path
```

CA certificates are part of an end-to-end runtime capability even though `ldd` will not list them.

## 12.13 Multiple TLS stacks in one application family

Complex applications may use several networking implementations:

```text
Chromium network stack
Node.js HTTP/TLS stack
native extension library
Git subprocess
Python helper
```

Each can interpret proxy and CA settings differently. “curl works” proves only that curl’s stack and configuration work.

## 12.14 Forward proxy

A forward proxy sits between a client and destination.

```text
client
    -> proxy
    -> destination server
```

For plain HTTP, the proxy can understand HTTP request semantics directly.

For HTTPS, a common forward-proxy flow uses HTTP `CONNECT` to request a byte tunnel to a destination host/port.

```text
client -> CONNECT destination:443 -> proxy
proxy  -> TCP connection -> destination
client <-> encrypted TLS bytes <-> destination through tunnel
```

A basic CONNECT tunnel need not decrypt application TLS content.

## 12.15 SOCKS

SOCKS is a general connection-proxy protocol rather than an HTTP-semantic proxy.

Conceptually:

```text
client asks SOCKS proxy:
connect me to host X, port Y
```

DNS resolution placement can differ by client/proxy mode, which matters when direct local DNS is broken but proxy-side resolution works.

## 12.16 Proxy environment variables

Common conventions include:

```text
HTTP_PROXY / http_proxy
HTTPS_PROXY / https_proxy
ALL_PROXY
NO_PROXY
```

Not every program or library honors every variable identically. Setting a variable does not force arbitrary applications to use it.

`NO_PROXY` prevents local endpoints such as `localhost` from being sent through an external proxy path where inappropriate.

## 12.17 WebSocket

WebSocket begins with an HTTP-based handshake/upgrade flow and then provides a persistent bidirectional message-framed channel.

Conceptually:

```text
HTTP connection
    -> upgrade handshake
    -> persistent WebSocket session
    <-> bidirectional frames
```

`wss://` adds TLS under the WebSocket protocol.

## 12.18 Why WebSocket can fail while HTTPS works

A network path may permit ordinary HTTPS request/response traffic but fail for:

```text
upgrade semantics
long-lived connection behavior
proxy tunneling
specific client proxy implementation
intermediary timeout policy
```

Therefore:

```text
HTTPS works
    !=
WebSocket works
```

A client can fall back from WebSocket to HTTPS transport and remain partially or fully usable.

## 12.19 The Codex + tinyproxy lesson

The project observed a useful control experiment:

```text
preferred WebSocket path
    -> disconnect/failure

HTTPS fallback
    -> available

local tinyproxy path
    -> usable behavior restored
```

The disciplined conclusion is not “WebSocket is broken on Termux.”

The result narrows the failure toward the original transport/proxy path and away from a total application or authentication failure. Exact mechanism requires transport logs or packet-level evidence.

## 12.20 Diagnostic ladder

For a network feature failure, investigate:

```text
1. Can the process create/connect sockets?
2. Does DNS resolution work?
3. Is the route/interface path valid?
4. Does TCP connect?
5. Is a proxy involved?
6. Does TLS handshake and verification succeed?
7. Does HTTP work?
8. Does WebSocket upgrade/session work?
9. Does the application protocol work?
```

Do not change WebSocket flags when DNS is the proven failure layer; do not rewrite DNS configuration when only the persistent transport fails.

## References

- RFC 9293, TCP: <https://www.rfc-editor.org/rfc/rfc9293.html>
- RFC 9110, HTTP semantics: <https://www.rfc-editor.org/rfc/rfc9110.html>
- RFC 8446, TLS 1.3: <https://www.rfc-editor.org/rfc/rfc8446.html>
- RFC 6455, WebSocket protocol: <https://www.rfc-editor.org/rfc/rfc6455.html>
- RFC 1928, SOCKS v5: <https://www.rfc-editor.org/rfc/rfc1928.html>
