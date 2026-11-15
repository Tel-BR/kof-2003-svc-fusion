-- Runs replay.lua and logs fighter state each frame to PROBE_LOG:
-- "<frame>\t<P1 animation pointer>\t<P1 x>\t<P1 y>\t<P1 health>\t<P2 health>\t<P2 animation pointer>".
-- Defaults are SVC Chaos work-RAM addresses measured in ticket 03; set PROBE_* to override.
-- Frame labels follow replay.lua with REPLAY_OFFSET=1. DUMP_FRAMES and DUMP_OUT, if set,
-- write the 64 KB work RAM at those frames (game data: keep the file under private/).
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
local log = assert(io.open(assert(os.getenv('PROBE_LOG')), 'w'))
local dumps = {}
for f in (os.getenv('DUMP_FRAMES') or ''):gmatch('%d+') do dumps[tonumber(f)] = true end
local dump = os.getenv('DUMP_OUT') and assert(io.open(os.getenv('DUMP_OUT'), 'wb'))
local done = 0
emu.register_frame_done(function()
    local frame = done + 1
    done = done + 1
    if dump and dumps[frame] then
        dump:write(string.pack('>I4', frame), mem:read_range(0x100000, 0x10ffff, 8)) dump:flush()
    end
    if frame >= first then
        log:write(('%d\t%08x\t%04x\t%04x\t%d\t%d\t%08x\n'):format(frame, mem:read_u32(p1 + anim),
            mem:read_u16(p1 + xoff), mem:read_u16(p1 + yoff), mem:read_u8(p1 + hpoff),
            mem:read_u8(p2 + hpoff), mem:read_u32(p2 + anim)))
        log:flush()
    end
end, 'probe')
