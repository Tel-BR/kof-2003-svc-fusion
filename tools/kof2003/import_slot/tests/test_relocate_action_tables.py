"""Exercise the relocation command with invented program contents."""
import hashlib
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
TOOL = ROOT / 'tools/kof2003/import_slot/relocate_action_tables.py'
TABLES = (0x706A2, 0x70FE2, 0x71922, 0x72262, 0x72BA2, 0x734E2,
          0x73E22, 0x74762, 0x75C22)
REFERENCES = (0x166C0, 0x28C38, 0x28C46, 0x28C54, 0x28C62,
              0x28C70, 0x28C7E, 0x28C8C, 0x28C9A)


def invented_program():
    data = bytearray(0x900000)
    data[0x44020:0x52A20] = b'\xff' * 0xEA00
    data[0x28CBC:0x28CC0] = (0x750A2).to_bytes(4, 'big')
    for reference in (0x240E6, 0x24D06):
        data[reference:reference + 4] = (0x77B4A).to_bytes(4, 'big')
    for immediate in (0x24100, 0x24D0E):
        data[immediate:immediate + 2] = (148).to_bytes(2, 'big')
    for index, (table, reference) in enumerate(zip(TABLES, REFERENCES)):
        data[reference:reference + 4] = table.to_bytes(4, 'big')
        for fighter in range(37):
            data[table + fighter * 64:table + (fighter + 1) * 64] = bytes([index, fighter]) * 32
    for table, refs in ((0x77A22, (0x24138, 0x27E1A)),
                        (0x77AB6, (0x24156, 0x27E38)),
                        (0xA5F56, (0x3C6E4,)), (0xA5FEA, (0x3C6F6,)),
                        (0xAAFD4, (0x234F0, 0x3C7F0)), (0xB2280, (0x235B0,))):
        for reference in refs:
            data[reference:reference + 4] = table.to_bytes(4, 'big')
    return data


def test_command_relocates_rows_and_keeps_original_program():
    with tempfile.TemporaryDirectory(dir=ROOT / 'private/work') as temp:
        source, dest = Path(temp) / 'input.bin', Path(temp) / 'output.bin'
        data = invented_program()
        source.write_bytes(data)
        digest = hashlib.sha256(data).hexdigest()
        run = subprocess.run([sys.executable, str(TOOL), str(source), str(dest),
                              '--sha256', digest, '--fighter-id', '5'], capture_output=True, text=True)
        assert run.returncode == 0, run.stderr
        assert source.read_bytes() == data
        result = dest.read_bytes()
        for index, (table, reference) in enumerate(zip(TABLES, REFERENCES)):
            relocated = 0x44020 + index * 0x1000
            assert int.from_bytes(result[reference:reference + 4], 'big') == relocated
            assert result[relocated:relocated + 37 * 64] == data[table:table + 37 * 64]
            assert result[relocated + 0x30 * 64:relocated + 0x31 * 64] == bytes([index, 5]) * 32


def test_command_rejects_unexpected_input_without_creating_output():
    with tempfile.TemporaryDirectory(dir=ROOT / 'private/work') as temp:
        source, dest = Path(temp) / 'input.bin', Path(temp) / 'output.bin'
        source.write_bytes(invented_program())
        run = subprocess.run([sys.executable, str(TOOL), str(source), str(dest),
                              '--sha256', '0' * 64, '--fighter-id', '5'], capture_output=True, text=True)
        assert run.returncode != 0
        assert not dest.exists()


def test_command_refuses_a_changed_table_reference():
    with tempfile.TemporaryDirectory(dir=ROOT / 'private/work') as temp:
        source, dest = Path(temp) / 'input.bin', Path(temp) / 'output.bin'
        data = invented_program()
        data[REFERENCES[0]:REFERENCES[0] + 4] = (0x123456).to_bytes(4, 'big')
        source.write_bytes(data)
        run = subprocess.run([sys.executable, str(TOOL), str(source), str(dest),
                              '--sha256', hashlib.sha256(data).hexdigest(),
                              '--fighter-id', '5'], capture_output=True, text=True)
        assert run.returncode != 0
        assert not dest.exists()


def test_command_expands_four_byte_fighter_tables_for_all_readers():
    with tempfile.TemporaryDirectory(dir=ROOT / 'private/work') as temp:
        source, dest = Path(temp) / 'input.bin', Path(temp) / 'output.bin'
        data = invented_program()
        for table, refs in ((0x77A22, (0x24138, 0x27E1A)),
                            (0x77AB6, (0x24156, 0x27E38))):
            for reference in refs:
                data[reference:reference + 4] = table.to_bytes(4, 'big')
            for fighter in range(37):
                data[table + fighter * 4:table + fighter * 4 + 4] = bytes([fighter]) * 4
        source.write_bytes(data)
        run = subprocess.run([sys.executable, str(TOOL), str(source), str(dest),
                              '--sha256', hashlib.sha256(data).hexdigest(),
                              '--fighter-id', '5'], capture_output=True, text=True)
        assert run.returncode == 0, run.stderr
        result = dest.read_bytes()
        for i, (table, refs) in enumerate(((0x77A22, (0x24138, 0x27E1A)),
                                           (0x77AB6, (0x24156, 0x27E38)))):
            new = 0x4D020 + i * 0x100
            assert all(int.from_bytes(result[r:r + 4], 'big') == new for r in refs)
            assert result[new:new + 37 * 4] == data[table:table + 37 * 4]
            assert result[new + 0x30 * 4:new + 0x31 * 4] == bytes([5]) * 4


def test_command_expands_fighter_pointer_tables():
    with tempfile.TemporaryDirectory(dir=ROOT / 'private/work') as temp:
        source, dest = Path(temp) / 'input.bin', Path(temp) / 'output.bin'
        data = invented_program()
        for table, refs in ((0xA5F56, (0x3C6E4,)), (0xA5FEA, (0x3C6F6,)),
                            (0xAAFD4, (0x234F0, 0x3C7F0)), (0xB2280, (0x235B0,))):
            for reference in refs:
                data[reference:reference + 4] = table.to_bytes(4, 'big')
            for fighter in range(37):
                data[table + fighter * 4:table + fighter * 4 + 4] = bytes([fighter]) * 4
        source.write_bytes(data)
        run = subprocess.run([sys.executable, str(TOOL), str(source), str(dest),
                              '--sha256', hashlib.sha256(data).hexdigest(),
                              '--fighter-id', '5'], capture_output=True, text=True)
        assert run.returncode == 0, run.stderr
        result = dest.read_bytes()
        for i, (table, refs) in enumerate(((0xA5F56, (0x3C6E4,)), (0xA5FEA, (0x3C6F6,)),
                                           (0xAAFD4, (0x234F0, 0x3C7F0)), (0xB2280, (0x235B0,)))):
            new = 0x4D220 + i * 0x100
            assert all(int.from_bytes(result[r:r + 4], 'big') == new for r in refs)
            assert result[new:new + 37 * 4] == data[table:table + 37 * 4]
            assert result[new + 0x30 * 4:new + 0x31 * 4] == bytes([5]) * 4


def test_command_preserves_overlapping_last_eighty_byte_row():
    with tempfile.TemporaryDirectory(dir=ROOT / 'private/work') as temp:
        source, dest = Path(temp) / 'input.bin', Path(temp) / 'output.bin'
        data = invented_program()
        source.write_bytes(data)
        run = subprocess.run([sys.executable, str(TOOL), str(source), str(dest),
                              '--sha256', hashlib.sha256(data).hexdigest(),
                              '--fighter-id', '5'], capture_output=True, text=True)
        assert run.returncode == 0, run.stderr
        result = dest.read_bytes()
        assert int.from_bytes(result[0x28CBC:0x28CC0], 'big') == 0x4D620
        assert result[0x4D620:0x4D620 + 37 * 80] == data[0x750A2:0x750A2 + 37 * 80]
        assert result[0x4D620 + 0x30 * 80:0x4D620 + 0x31 * 80] == data[0x750A2 + 5 * 80:0x750A2 + 6 * 80]


def test_command_expands_pair_matrix_in_both_dimensions():
    with tempfile.TemporaryDirectory(dir=ROOT / 'private/work') as temp:
        source, dest = Path(temp) / 'input.bin', Path(temp) / 'output.bin'
        data = invented_program()
        for row in range(64):
            for col in range(37):
                off = 0x77B4A + row * 148 + col * 4
                data[off:off + 4] = bytes([row, col, row, col])
        source.write_bytes(data)
        run = subprocess.run([sys.executable, str(TOOL), str(source), str(dest),
                              '--sha256', hashlib.sha256(data).hexdigest(),
                              '--fighter-id', '5'], capture_output=True, text=True)
        assert run.returncode == 0, run.stderr
        result = dest.read_bytes()
        assert all(int.from_bytes(result[r:r + 4], 'big') == 0x4EA20 for r in (0x240E6, 0x24D06))
        assert all(int.from_bytes(result[r:r + 2], 'big') == 256 for r in (0x24100, 0x24D0E))
        for row, col in ((0, 0), (36, 36), (0x30, 7), (7, 0x30), (0x30, 0x30)):
            oldrow, oldcol = (5 if row == 0x30 else row), (5 if col == 0x30 else col)
            actual = 0x4EA20 + row * 256 + col * 4
            expected = 0x77B4A + oldrow * 148 + oldcol * 4
            assert result[actual:actual + 4] == data[expected:expected + 4]


def test_command_clones_fighter_entries_in_existing_large_directories():
    with tempfile.TemporaryDirectory(dir=ROOT / 'private/work') as temp:
        source, dest = Path(temp) / 'input.bin', Path(temp) / 'output.bin'
        data = invented_program()
        for base, width in ((0x704A2, 4), (0x6090A, 2), (0x6098A, 2),
                            (0x60A0A, 2), (0x60A8A, 2), (0x7DC28, 2),
                            (0x200000, 4), (0x380000, 4)):
            data[base + 5 * width:base + 6 * width] = b'\x71' * width
            data[base + 0x30 * width:base + 0x31 * width] = b'\x24' * width
        source.write_bytes(data)
        run = subprocess.run([sys.executable, str(TOOL), str(source), str(dest),
                              '--sha256', hashlib.sha256(data).hexdigest(),
                              '--fighter-id', '5'], capture_output=True, text=True)
        assert run.returncode == 0, run.stderr
        result = dest.read_bytes()
        for base, width in ((0x704A2, 4), (0x6090A, 2), (0x6098A, 2),
                            (0x60A0A, 2), (0x60A8A, 2), (0x7DC28, 2),
                            (0x200000, 4), (0x380000, 4)):
            assert result[base + 0x30 * width:base + 0x31 * width] == b'\x71' * width
            assert result[base:base + 37 * width] == data[base:base + 37 * width]
