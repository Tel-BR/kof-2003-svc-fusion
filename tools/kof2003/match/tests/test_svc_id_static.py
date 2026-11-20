"""Static reader inventory for SVC Chaos fighter IDs (wayfinder ticket 28).

The code here is invented 68000 machine code, not game bytes.
"""
import pytest

pytest.importorskip("capstone")

from match.svc_id_static import (  # noqa: E402
    Insn, field_uses, normalise_program, summarise, sweep, table_reads)

# moveq #0,d0 / move.b $1d6(a4),d0 / lea $1e(pc),a0 / add.w d0,d0 / move.w (a0,d0.w),d0 / rts
JUMP_TABLE = bytes.fromhex("7000" "102c01d6" "41fa0016" "d040" "30300000" "4e75")
# moveq #0,d2 / move.b $71(a4),d2 / lea $a65ba.l,a0 / move.b (a0,d2.w),d2 / rts
BYTE_TABLE = bytes.fromhex("7400" "142c0071" "41f9000a65ba" "14302000" "4e75")
# move.b $1d6(a4),d0 / mulu.w #$90,d0 / lea $1000.l,a0 / adda.l d0,a0 / move.l (a0),d1 / rts
ROW_TABLE = bytes.fromhex("102c01d6" "c0fc0090" "41f900001000" "d1c0" "2210" "4e75")


def test_a_program_stored_with_swapped_bytes_is_put_right():
    right = bytes.fromhex("0010f300") + bytes(4)
    swapped = bytes.fromhex("1000" "00f3") + bytes(4)
    assert normalise_program(right) == right
    assert normalise_program(swapped) == right


def test_a_file_that_is_neither_order_is_refused():
    with pytest.raises(ValueError, match="reset vector"):
        normalise_program(bytes.fromhex("deadbeef") + bytes(4))


def test_the_sweep_gives_each_instruction_its_address_width_and_operands():
    insns = sweep(JUMP_TABLE)
    assert [i.address for i in insns] == [0, 2, 6, 10, 12, 16]
    assert insns[1] == Insn(2, 4, "move", "b", ("$1d6(a4)", "d0"))
    assert insns[2].operands == ("$1e(pc)", "a0")


def test_the_sweep_skips_a_word_that_is_not_an_instruction():
    insns = sweep(bytes.fromhex("4e75" "0048" "4e75"))
    assert [i.address for i in insns] == [0, 4]


def test_a_use_of_a_field_is_a_read_a_write_or_a_test():
    code = bytes.fromhex("122c0071" "19410071" "0c2c001a01d6" "082b00060077")
    uses = field_uses(sweep(code), {0x71, 0x77, 0x1D6})
    assert [(u.address, u.field, u.role) for u in uses] == [
        (0, 0x71, "read"), (4, 0x71, "write"), (8, 0x1D6, "test"), (14, 0x77, "test")]
    assert uses[2].immediate == 0x1A


def test_an_absolute_address_is_not_a_field_use_but_an_indexed_displacement_is():
    # move.b $71.w,d0 (absolute address) and move.b $71(a4,d1.w),d0 (8-bit displacement, indexed)
    uses = field_uses(sweep(bytes.fromhex("10380071" "10341071")), {0x71})
    assert [(u.address, u.indexed) for u in uses] == [(4, True)]


def test_a_jump_table_indexed_by_the_id_is_found_with_its_scale():
    insns = sweep(JUMP_TABLE)
    (read,) = table_reads(insns, field_uses(insns, {0x1D6}))
    assert (read.field, read.base, read.scale, read.width) == (0x1D6, 0x1E, 2, "w")
    assert read.site == 2 and read.access == 12 and read.kind == "table"


def test_a_byte_table_at_an_absolute_address_has_scale_one():
    insns = sweep(BYTE_TABLE)
    (read,) = table_reads(insns, field_uses(insns, {0x71}))
    assert (read.base, read.scale, read.width) == (0xA65BA, 1, "b")


def test_a_row_table_reached_by_multiplying_and_adding_to_a_pointer():
    insns = sweep(ROW_TABLE)
    (read,) = table_reads(insns, field_uses(insns, {0x1D6}))
    assert (read.base, read.scale, read.width) == (0x1000, 0x90, "l")


def test_tracking_stops_when_the_register_is_loaded_with_something_else():
    # move.b $71(a4),d0 / moveq #1,d0 / lea $1000.l,a0 / move.b (a0,d0.w),d1 / rts
    code = bytes.fromhex("102c0071" "7001" "41f900001000" "12300000" "4e75")
    insns = sweep(code)
    assert table_reads(insns, field_uses(insns, {0x71})) == []


def test_a_comparison_of_the_loaded_id_with_a_literal_is_an_identity_test():
    # move.b $1d6(a4),d0 / cmpi.b #$13,d0 / beq.b +2 / rts
    code = bytes.fromhex("102c01d6" "0c000013" "6702" "4e75")
    insns = sweep(code)
    (read,) = table_reads(insns, field_uses(insns, {0x1D6}))
    assert (read.kind, read.immediate) == ("identity", 0x13)


def test_a_call_that_receives_the_id_reports_its_table_and_row_size():
    # lea $1000.l,a0 / move.w $70(a4),d0 / moveq #$40,d1 / jsr $2000.l
    code = bytes.fromhex("41f900001000" "302c0070" "7240" "4eb900002000")
    insns = sweep(code)
    (read,) = table_reads(insns, field_uses(insns, {0x70}))
    assert (read.kind, read.base, read.callee, read.argument) == ("call", 0x1000, 0x2000, 0x40)


def test_a_premultiplied_id_word_indexes_with_its_scale_already_applied():
    # lea $1000.l,a0 / move.w $182(a4),d0 / move.l (a0,d0.w),d1
    insns = sweep(bytes.fromhex("41f900001000" "302c0182" "22300000"))
    (read,) = table_reads(insns, field_uses(insns, {0x182}))
    assert (read.base, read.scale, read.width) == (0x1000, 4, "l")


def test_a_field_can_be_limited_to_one_base_register():
    # move.b $2c34(a5),d1 and move.b $2c34(a4),d1
    insns = sweep(bytes.fromhex("122d2c34" "122c2c34"))
    assert [u.address for u in field_uses(insns, {("a5", 0x2C34)})] == [0]
    assert [u.address for u in field_uses(insns, {0x2C34})] == [0, 4]


def test_the_summary_counts_uses_by_field_and_role():
    code = bytes.fromhex("122c0071" "19410071" "0c2c001a01d6")
    uses = field_uses(sweep(code), {0x71, 0x1D6})
    assert summarise(uses) == {(0x71, "read"): 1, (0x71, "write"): 1, (0x1D6, "test"): 1}
