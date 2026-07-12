#!/usr/bin/env python3
from __future__ import annotations

import hashlib
from pathlib import Path

EXPECTED_SOURCE_SHA256 = "7b0df03c95d471e7cb9ccdd9be00345ee40b8546f5478e374516ee56c7f04089"
PARTS_DIR = Path(__file__).with_name("collect-n3-binary-artifact-comparison.parts")
parts = sorted(PARTS_DIR.glob("*.part"))
if [part.name for part in parts] != [f"{index:03d}.part" for index in range(7)]:
    raise SystemExit(f"collector source parts are missing or unexpected: {PARTS_DIR}")
source = b"".join(part.read_bytes() for part in parts)
actual = hashlib.sha256(source).hexdigest()
if actual != EXPECTED_SOURCE_SHA256:
    raise SystemExit(f"collector source SHA-256 mismatch: {actual} != {EXPECTED_SOURCE_SHA256}")
namespace = {
    "__name__": "__main__",
    "__file__": str(Path(__file__).resolve()),
    "__package__": None,
    "__cached__": None,
}
exec(compile(source, f"{Path(__file__).resolve()}:assembled", "exec"), namespace)
