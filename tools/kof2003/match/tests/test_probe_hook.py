"""The probe hook added to a private runtime copy, checked on invented source files (ticket 08)."""
import hashlib
import tempfile
from pathlib import Path

import pytest

from match.probe_hook import prepare

ROOT = Path(__file__).resolve().parents[4]
LOOP = b'    for (;;) {\n        io_set_inputs(&in);\n        run_frame();\n        audio();\n    }\n'
MONITORED = LOOP.replace(b'        run_frame();\n', b'        run_frame();\n#ifdef KOF2003_REHEARSAL_MONITOR\n'
                         b'        kof_rehearsal_monitor(frame, &in);\n#endif\n')


@pytest.fixture
def private_dir():
    with tempfile.TemporaryDirectory(dir=ROOT / 'private' / 'work') as temp:
        yield Path(temp)


def write(folder, data):
    source = folder / 'neogeo.c'
    source.write_bytes(data)
    return source, hashlib.sha256(data).hexdigest()


def test_hook_calls_the_probe_after_each_frame_only_under_its_macro(private_dir):
    source, digest = write(private_dir, LOOP)
    prepare(source, private_dir / 'out.c', digest)
    result = (private_dir / 'out.c').read_bytes()
    assert source.read_bytes() == LOOP
    assert result == LOOP.replace(b'        run_frame();\n', b'        run_frame();\n#ifdef KOF2003_NATIVE_PROBE\n'
                                  b'        extern void kof_native_probe(long);\n'
                                  b'        kof_native_probe(frame);\n#endif\n')


def test_hook_keeps_windows_line_endings(private_dir):
    data = LOOP.replace(b'\n', b'\r\n')
    source, digest = write(private_dir, data)
    prepare(source, private_dir / 'out.c', digest)
    result = (private_dir / 'out.c').read_bytes()
    assert b'kof_native_probe(frame);\r\n#endif\r\n' in result
    assert b'\n' not in result.replace(b'\r\n', b'')


def test_hook_goes_alongside_the_rehearsal_monitor(private_dir):
    source, digest = write(private_dir, MONITORED)
    prepare(source, private_dir / 'out.c', digest)
    result = (private_dir / 'out.c').read_bytes()
    assert b'kof_rehearsal_monitor(frame, &in);' in result
    assert result.index(b'run_frame();') < result.index(b'kof_native_probe(frame);') \
        < result.index(b'kof_rehearsal_monitor(frame, &in);')


def test_wrong_identity_or_second_hook_is_refused(private_dir):
    source, digest = write(private_dir, LOOP)
    with pytest.raises(ValueError, match='SHA-256'):
        prepare(source, private_dir / 'out.c', '0' * 64)
    prepare(source, private_dir / 'once.c', digest)
    hooked = (private_dir / 'once.c').read_bytes()
    with pytest.raises(ValueError, match='frame hook'):
        prepare(private_dir / 'once.c', private_dir / 'twice.c', hashlib.sha256(hooked).hexdigest())


def test_paths_outside_private_are_refused(private_dir, tmp_path):
    source, digest = write(private_dir, LOOP)
    with pytest.raises(ValueError, match='private'):
        prepare(source, tmp_path / 'out.c', digest)


def test_existing_output_is_not_overwritten(private_dir):
    source, digest = write(private_dir, LOOP)
    (private_dir / 'out.c').write_bytes(b'keep')
    with pytest.raises(FileExistsError):
        prepare(source, private_dir / 'out.c', digest)
    assert (private_dir / 'out.c').read_bytes() == b'keep'
