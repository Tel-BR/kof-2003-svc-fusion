"""Check the PVC byte-write patch using invented private source files (no game or third-party code)."""
import hashlib
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
TOOL = ROOT / 'tools/kof2003/import_slot/pvc_byte_writes.py'

WORD = (b'static void pvc_w16(uint32_t a, uint16_t v) {\n    uint32_t word = o >> 1;\n'
        b'    if (word == 0xff0) pvc_color_unpack();\n    else if (word == 0xff4 || word == 0xff5) pvc_color_pack();\n'
        b'    if (word >= 0xff8) pvc_bank_update();\n}\n\n')
BYTE = (b'static void pvc_w8(uint32_t a, uint8_t v) {\n    s_ram[a] = v;\n    uint32_t word = o >> 1;\n'
        b'    if (word >= 0xff8) pvc_bank_update();\n}\n')


def run(source_bytes, expected=None, destination_exists=False, crlf=False):
    if crlf:
        source_bytes = source_bytes.replace(b'\n', b'\r\n')
    with tempfile.TemporaryDirectory(dir=ROOT / 'private/work') as temp:
        source, dest = Path(temp) / 'input.c', Path(temp) / 'output.c'
        source.write_bytes(source_bytes)
        if destination_exists:
            dest.write_bytes(b'x')
        digest = expected or hashlib.sha256(source_bytes).hexdigest()
        result = subprocess.run([sys.executable, str(TOOL), str(source), str(dest), '--sha256', digest],
                                capture_output=True, text=True)
        return result, source.read_bytes(), (dest.read_bytes() if dest.exists() else None)


def test_byte_handler_gets_the_word_handlers_triggers_and_input_is_untouched():
    data = WORD + BYTE
    result, source_after, patched = run(data)
    assert result.returncode == 0, result.stderr
    assert source_after == data
    tail = patched[patched.index(b'static void pvc_w8('):]
    assert b'if (word == 0xff0) pvc_color_unpack();' in tail
    assert b'else if (word == 0xff4 || word == 0xff5) pvc_color_pack();' in tail
    assert tail.index(b'pvc_color_pack') < tail.index(b'pvc_bank_update')
    assert patched[:patched.index(b'static void pvc_w8(')] == data[:data.index(b'static void pvc_w8(')]


def test_crlf_source_keeps_its_line_endings():
    result, _, patched = run(WORD + BYTE, crlf=True)
    assert result.returncode == 0, result.stderr
    assert b'\n' not in patched.replace(b'\r\n', b'')


def test_refuses_wrong_hash_existing_destination_and_double_application():
    data = WORD + BYTE
    assert run(data, expected='0' * 64)[0].returncode == 1
    assert run(data, destination_exists=True)[0].returncode == 1
    first, _, patched = run(data)
    assert first.returncode == 0
    assert run(patched)[0].returncode == 1


def test_refuses_a_source_without_the_byte_handler():
    assert run(WORD)[0].returncode == 1
