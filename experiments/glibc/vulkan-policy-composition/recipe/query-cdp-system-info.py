#!/data/data/com.termux/files/usr/bin/python
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import socket
import struct
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


class WebSocketProtocolError(RuntimeError):
    pass


def recv_exact(sock: socket.socket, size: int) -> bytes:
    chunks: list[bytes] = []
    remaining = size
    while remaining:
        chunk = sock.recv(remaining)
        if not chunk:
            raise WebSocketProtocolError("unexpected EOF")
        chunks.append(chunk)
        remaining -= len(chunk)
    return b"".join(chunks)


def read_http_headers(sock: socket.socket) -> bytes:
    data = bytearray()
    while b"\r\n\r\n" not in data:
        chunk = sock.recv(4096)
        if not chunk:
            raise WebSocketProtocolError("EOF during websocket handshake")
        data.extend(chunk)
        if len(data) > 65536:
            raise WebSocketProtocolError("oversized websocket handshake")
    return bytes(data)


def websocket_connect(url: str, timeout: float) -> socket.socket:
    parsed = urlparse(url)
    if parsed.scheme != "ws":
        raise ValueError(f"only ws:// URLs are supported: {url}")
    if not parsed.hostname or not parsed.port:
        raise ValueError(f"websocket URL must include host and port: {url}")

    path = parsed.path or "/"
    if parsed.query:
        path += "?" + parsed.query

    sock = socket.create_connection((parsed.hostname, parsed.port), timeout=timeout)
    sock.settimeout(timeout)

    nonce = os.urandom(16)
    key = base64.b64encode(nonce).decode("ascii")
    request = (
        f"GET {path} HTTP/1.1\r\n"
        f"Host: {parsed.hostname}:{parsed.port}\r\n"
        "Upgrade: websocket\r\n"
        "Connection: Upgrade\r\n"
        f"Sec-WebSocket-Key: {key}\r\n"
        "Sec-WebSocket-Version: 13\r\n"
        "\r\n"
    ).encode("ascii")
    sock.sendall(request)

    response = read_http_headers(sock)
    header_block = response.split(b"\r\n\r\n", 1)[0]
    lines = header_block.decode("iso-8859-1").split("\r\n")
    if not lines or " 101 " not in f" {lines[0]} ":
        raise WebSocketProtocolError(
            "websocket handshake failed: " + lines[0] if lines else "empty response"
        )

    headers: dict[str, str] = {}
    for line in lines[1:]:
        if ":" not in line:
            continue
        name, value = line.split(":", 1)
        headers[name.strip().lower()] = value.strip()

    expected = base64.b64encode(
        hashlib.sha1((key + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11").encode("ascii")).digest()
    ).decode("ascii")
    observed = headers.get("sec-websocket-accept")
    if observed != expected:
        raise WebSocketProtocolError(
            f"invalid Sec-WebSocket-Accept: expected={expected!r} observed={observed!r}"
        )

    return sock


def send_frame(sock: socket.socket, opcode: int, payload: bytes) -> None:
    first = 0x80 | (opcode & 0x0F)
    length = len(payload)
    mask_key = os.urandom(4)

    if length < 126:
        header = struct.pack("!BB", first, 0x80 | length)
    elif length <= 0xFFFF:
        header = struct.pack("!BBH", first, 0x80 | 126, length)
    else:
        header = struct.pack("!BBQ", first, 0x80 | 127, length)

    masked = bytes(byte ^ mask_key[index % 4] for index, byte in enumerate(payload))
    sock.sendall(header + mask_key + masked)


def recv_frame(sock: socket.socket) -> tuple[bool, int, bytes]:
    first, second = struct.unpack("!BB", recv_exact(sock, 2))
    fin = bool(first & 0x80)
    opcode = first & 0x0F
    masked = bool(second & 0x80)
    length = second & 0x7F

    if length == 126:
        length = struct.unpack("!H", recv_exact(sock, 2))[0]
    elif length == 127:
        length = struct.unpack("!Q", recv_exact(sock, 8))[0]

    mask_key = recv_exact(sock, 4) if masked else b""
    payload = recv_exact(sock, length)
    if masked:
        payload = bytes(byte ^ mask_key[index % 4] for index, byte in enumerate(payload))

    return fin, opcode, payload


def recv_text_message(sock: socket.socket) -> str:
    fragments: list[bytes] = []
    active_opcode: int | None = None

    while True:
        fin, opcode, payload = recv_frame(sock)

        if opcode == 0x8:
            raise WebSocketProtocolError("server closed websocket")
        if opcode == 0x9:
            send_frame(sock, 0xA, payload)
            continue
        if opcode == 0xA:
            continue

        if opcode in (0x1, 0x2):
            if active_opcode is not None:
                raise WebSocketProtocolError("new data frame during fragmented message")
            active_opcode = opcode
            fragments = [payload]
        elif opcode == 0x0:
            if active_opcode is None:
                raise WebSocketProtocolError("unexpected continuation frame")
            fragments.append(payload)
        else:
            continue

        if fin:
            if active_opcode != 0x1:
                raise WebSocketProtocolError("expected text websocket response")
            return b"".join(fragments).decode("utf-8")


def cdp_call(sock: socket.socket, request_id: int, method: str) -> dict[str, Any]:
    request = {"id": request_id, "method": method}
    send_frame(sock, 0x1, json.dumps(request, separators=(",", ":")).encode("utf-8"))

    while True:
        message = json.loads(recv_text_message(sock))
        if message.get("id") != request_id:
            continue
        if "error" in message:
            raise RuntimeError(f"CDP {method} failed: {message['error']}")
        result = message.get("result")
        if not isinstance(result, dict):
            raise RuntimeError(f"CDP {method} returned no result object")
        return result


def scalar_text(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (str, int, float)):
        return str(value)
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def write_outputs(result: dict[str, Any], out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "system-info.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    gpu = result.get("gpu")
    if not isinstance(gpu, dict):
        raise RuntimeError("SystemInfo.getInfo result has no gpu object")

    devices = gpu.get("devices")
    if not isinstance(devices, list) or not devices:
        raise RuntimeError("SystemInfo.getInfo returned no GPU devices")

    device_columns = [
        "index",
        "primary",
        "vendorId",
        "deviceId",
        "subSysId",
        "revision",
        "vendorString",
        "deviceString",
        "driverVendor",
        "driverVersion",
    ]
    with (out_dir / "gpu-devices.tsv").open("w", encoding="utf-8") as handle:
        handle.write("\t".join(device_columns) + "\n")
        for index, device in enumerate(devices):
            if not isinstance(device, dict):
                continue
            row = {
                "index": index,
                "primary": index == 0,
                **device,
            }
            handle.write("\t".join(scalar_text(row.get(column, "")) for column in device_columns) + "\n")

    aux = gpu.get("auxAttributes")
    if not isinstance(aux, dict):
        aux = {}
    with (out_dir / "gpu-aux-attributes.tsv").open("w", encoding="utf-8") as handle:
        handle.write("key\tvalue\n")
        for key in sorted(aux):
            handle.write(f"{key}\t{scalar_text(aux[key])}\n")

    feature_status = gpu.get("featureStatus")
    if not isinstance(feature_status, dict):
        feature_status = {}
    with (out_dir / "gpu-feature-status.tsv").open("w", encoding="utf-8") as handle:
        handle.write("feature\tstatus\n")
        for key in sorted(feature_status):
            handle.write(f"{key}\t{scalar_text(feature_status[key])}\n")

    command_line = result.get("commandLine", "")
    (out_dir / "browser-command-line.txt").write_text(
        scalar_text(command_line) + "\n", encoding="utf-8"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Query Chromium SystemInfo.getInfo through a browser CDP websocket."
    )
    parser.add_argument("--websocket-url", required=True)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--timeout", type=float, default=10.0)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    sock = websocket_connect(args.websocket_url, args.timeout)
    try:
        result = cdp_call(sock, 1, "SystemInfo.getInfo")
        write_outputs(result, args.out)
        send_frame(sock, 0x8, b"")
    finally:
        sock.close()

    print("CDP SystemInfo.getInfo: PASS")
    print(f"output: {args.out}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"CDP SystemInfo.getInfo: FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
