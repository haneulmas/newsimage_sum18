"""Check the committed PNG and two dependency-free, network-denied entry runs."""

import ast
import hashlib
import json
import os
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
import zlib


ROOT = Path(__file__).resolve().parents[1]
SIGNATURE = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1_048_576
TARGET_BYTES = 400_000

AUDITED_RUN = """
import runpy
import sys

attempts = []

def audit(event, args):
    if event.startswith(("socket.", "subprocess.", "urllib.")) or event in (
        "os.system", "os.exec", "os.spawn", "os.posix_spawn", "pty.spawn"
    ):
        attempts.append(event)
        raise RuntimeError("Entry attempted a forbidden operation: " + event)

sys.addaudithook(audit)
runpy.run_path(sys.argv[1], run_name="__main__")
assert not attempts, attempts
assert not any(name == "PIL" or name.startswith("PIL.") for name in sys.modules)
"""


def check_png(data):
    assert len(data) <= MAX_BYTES, "PNG exceeds 1 MiB"
    assert len(data) < TARGET_BYTES, "PNG misses the under-400 KB target"
    assert data[:8] == SIGNATURE, "Invalid PNG signature"
    chunks = []
    offset = 8
    while offset < len(data):
        assert offset + 12 <= len(data), "Truncated PNG chunk"
        length = struct.unpack_from(">I", data, offset)[0]
        end = offset + length + 12
        assert end <= len(data), "Truncated PNG payload"
        kind = data[offset + 4:offset + 8]
        payload = data[offset + 8:end - 4]
        crc = struct.unpack_from(">I", data, end - 4)[0]
        assert crc == zlib.crc32(kind + payload) & 0xFFFFFFFF, "PNG CRC mismatch"
        chunks.append((kind, payload))
        offset = end
    assert [kind for kind, _ in chunks] == [b"IHDR", b"PLTE", b"IDAT", b"IEND"], (
        "Unexpected PNG chunks, metadata or trailing image data"
    )
    assert len(chunks[0][1]) == 13, "Invalid IHDR length"
    width, height, depth, color, compression, filtering, interlace = struct.unpack(
        ">IIBBBBB", chunks[0][1]
    )
    assert (width, height) == (1024, 1024), "Expected a 1024-square canvas"
    assert (depth, color, compression, filtering, interlace) == (8, 3, 0, 0, 0), (
        "Expected non-interlaced 8-bit indexed PNG"
    )
    palette = chunks[1][1]
    assert 0 < len(palette) <= 768 and len(palette) % 3 == 0, "Invalid palette"
    assert chunks[2][1], "Missing compressed image data"
    assert not chunks[3][1], "Invalid IEND payload"
    expected = height * (width + 1)
    inflater = zlib.decompressobj()
    pixels = inflater.decompress(chunks[2][1], expected + 1)
    assert inflater.eof and not inflater.unused_data and not inflater.unconsumed_tail, (
        "Incomplete zlib image stream or trailing compressed data"
    )
    assert len(pixels) == expected, "Incorrect decompressed image length"
    for row in range(height):
        start = row * (width + 1)
        assert pixels[start] == 0, "Expected deterministic unfiltered scanlines"
        assert max(pixels[start + 1:start + width + 1]) < len(palette) // 3, (
            "Pixel references a missing palette entry"
        )
    return {
        "format": "PNG",
        "width": width,
        "height": height,
        "bytes": len(data),
        "paletteEntries": len(palette) // 3,
        "chunks": [kind.decode("ascii") for kind, _ in chunks],
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def check_entry_source(path):
    tree = ast.parse(path.read_text(encoding="utf-8"))
    allowed = {"os", "pathlib", "shutil"}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            assert all(item.name in allowed for item in node.names), "Unexpected runtime import"
        elif isinstance(node, ast.ImportFrom):
            assert node.level == 0 and node.module in allowed, "Unexpected runtime import"
    literals = {node.value for node in ast.walk(tree)
                if isinstance(node, ast.Constant) and isinstance(node.value, str)}
    assert {"MAKEFUN_OUTPUT_DIR", "/output", "entry.png"} <= literals, "Missing output contract"


def main():
    entry = ROOT / "main.py"
    check_entry_source(entry)
    reference = (ROOT / "assets" / "entry.png").read_bytes()
    metrics = check_png(reference)
    runs = []
    with tempfile.TemporaryDirectory(prefix="global-ledger-verify-") as temporary:
        scratch = Path(temporary)
        for number in (1, 2):
            output = scratch / ("run " + str(number)) / "new output"
            result = subprocess.run(
                [sys.executable, "-I", "-S", "-B", "-c", AUDITED_RUN, str(entry)],
                cwd=scratch,
                env={**os.environ, "MAKEFUN_OUTPUT_DIR": str(output)},
                capture_output=True,
                text=True,
                timeout=30,
                check=False,
            )
            assert result.returncode == 0, result.stderr
            assert not result.stdout and not result.stderr, "Unexpected runtime console output"
            assert sorted(item.name for item in output.iterdir()) == ["entry.png"], (
                "Entry wrote unexpected output files"
            )
            image = (output / "entry.png").read_bytes()
            assert image == reference, "Output differs from the committed PNG"
            runs.append({"run": number, "sha256": check_png(image)["sha256"],
                         "forbiddenOperations": 0})
    assert not scratch.exists(), "Temporary verification files remain"
    print(json.dumps({"status": "PASS", "python": sys.version.split()[0],
                      "asset": metrics, "runs": runs}, indent=2))


if __name__ == "__main__":
    main()
