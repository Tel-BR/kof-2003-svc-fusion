-- Runs replay.lua and logs fighter state each frame to PROBE_LOG:
-- "<frame>\t<P1 animation pointer>\t<P1 x>\t<P1 y>\t<P1 health>\t<P2 health>\t<P2 animation pointer>".
-- Defaults are SVC Chaos work-RAM addresses measured in ticket 03; set PROBE_* to override.
-- With PROBE_ADDRESSES ("0xADDRESS:SIZE[,...]", SIZE 1, 2 or 4) it logs those addresses instead,
-- "<frame>\t<hex>\t<hex>...", the format of the native player's probe (match/probe_log.py).
-- Frame labels are replay.lua's native frame numbers (REPLAY_OFFSET, default 2; mame_run.py
-- passes 1 for SVC Chaos). DUMP_FRAMES and DUMP_OUT, if set, write the 64 KB work RAM at those
-- frames (game data: keep the file under private/).
dofile(assert(os.getenv('REPLAY_LUA')))
local mem = manager.machine.devices[':maincpu'].spaces.program
local function addr(name, default) return tonumber(os.getenv(name) or default) end
local p1 = addr('PROBE_P1_OBJECT', '0x10a100')
local p2 = addr('PROBE_P2_OBJECT', '0x10a380')
local anim = addr('PROBE_ANIM_OFFSET', '0x28')
local xoff = addr('PROBE_X_OFFSET', '0x18')
local yoff = addr('PROBE_Y_OFFSET', '0x1c')
local hpoff = addr('PROBE_HEALTH_OFFSET', '0x139')
local first = tonumber(os.getenv('PROBE_FIRST') or '0')
local offset = tonumber(os.getenv('REPLAY_OFFSET') or '2')
local function parse_addresses(text)
    local probes = {}
    for item in (text .. ','):gmatch('([^,]*),') do
        local hex, size = item:match('^%s*0[xX](%x+):(%d)%s*$')
        assert(hex and #hex <= 6, 'PROBE_ADDRESSES: expected 0xADDRESS:SIZE, got "' .. item .. '"')
        local address = tonumber(hex, 16)
        size = tonumber(size)
        assert(size == 1 or size == 2 or size == 4, 'PROBE_ADDRESSES: size must be 1, 2 or 4')
        assert(size == 1 or address % 2 == 0, 'PROBE_ADDRESSES: odd address for a word read')
        probes[#probes + 1] = {address, size}
    end
    assert(#probes <= 16, 'PROBE_ADDRESSES: at most 16 addresses')
    return probes
end
local probes = os.getenv('PROBE_ADDRESSES') and parse_addresses(os.getenv('PROBE_ADDRESSES'))
local readers = {[1] = 'read_u8', [2] = 'read_u16', [4] = 'read_u32'}
local function line(frame)
    if not probes then
        return ('%d\t%08x\t%04x\t%04x\t%d\t%d\t%08x\n'):format(frame, mem:read_u32(p1 + anim),
            mem:read_u16(p1 + xoff), mem:read_u16(p1 + yoff), mem:read_u8(p1 + hpoff),
            mem:read_u8(p2 + hpoff), mem:read_u32(p2 + anim))
    end
    local fields = {tostring(frame)}
    for _, probe in ipairs(probes) do
        local value = mem[readers[probe[2]]](mem, probe[1])
        fields[#fields + 1] = ('%0' .. (2 * probe[2]) .. 'x'):format(value)
    end
    return table.concat(fields, '\t') .. '\n'
end
local log = assert(io.open(assert(os.getenv('PROBE_LOG')), 'w'))
local dumps = {}
for f in (os.getenv('DUMP_FRAMES') or ''):gmatch('%d+') do dumps[tonumber(f)] = true end
local dump = os.getenv('DUMP_OUT') and assert(io.open(os.getenv('DUMP_OUT'), 'wb'))
local done = 0
emu.register_frame_done(function()
    local frame = done + offset
    done = done + 1
    if dump and dumps[frame] then
        dump:write(string.pack('>I4', frame), mem:read_range(0x100000, 0x10ffff, 8)) dump:flush()
    end
    if frame >= first then
        log:write(line(frame))
        log:flush()
    end
end, 'probe')
