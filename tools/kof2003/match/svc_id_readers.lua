-- Listens to SVC Chaos while a recording plays back, for wayfinder ticket 28:
-- which data does the game look up by a fighter's ID, and who reads it.
-- Passive: memory taps and the frame callback only; it never writes game memory.
--
-- What it proved and what it did not (2026-11-20, MAME 0.289). The dumps work and are how
-- the fighter object's ID field was found. The taps do NOT see the game reading work RAM:
-- over a whole recorded match the only hits on the object were the BIOS memory test at
-- boot (the $5555/$AAAA pattern, reader in BIOS space). Debugger watchpoints with
-- -debug -debugger none were no better: the watchpoint is accepted but its printf has
-- nowhere to go. So who reads the ID has to be found another way; the dumps stay useful.
--
-- Environment:
--   ID_LOG          output TSV (required). Keep it under private/: it carries game data.
--   ID_OBJECTS      fighter object bases, comma separated (default SVC's P1 and P2).
--   ID_SPAN         bytes of each object to dump (default 0x300, one object stride).
--   ID_DUMP_FRAMES  frames at which to dump the objects (default 1500,2000,3000,4500).
--   ID_TAP_OFFSETS  object offsets to tap reads on, comma separated (default none).
--   ID_TAP_WIDTH    bytes covered by each tap (default 2, a word).
--   ID_TAP_RAW      how many tapped reads to write one by one before only counting (default 300).
--   LAST_FRAME      stop MAME at this frame, as in playback_shots.lua.
--
-- Output: tab separated, one line per event. Lines starting with # are notes.
--   frame  kind  base  offset  value  extra
-- kind  dump    the object's bytes at that frame; value is hex, offset is the dump's start
--       read    one tapped read, up to ID_TAP_RAW of them; extra carries the reader's PC and
--               the stacked return addresses
--       reader  one line per distinct reader at the end: how often it read that offset and
--               the frame it first did
local machine = manager.machine
local main = machine.devices[':maincpu']
local mem = main.spaces.program

local function list(name, default)
    local out = {}
    for item in (os.getenv(name) or default):gmatch('[^,%s]+') do out[#out + 1] = tonumber(item) end
    return out
end

local function num(name, default) return tonumber(os.getenv(name) or default) end

local OBJECTS = list('ID_OBJECTS', '0x10A100,0x10A380')
local SPAN = num('ID_SPAN', '0x300')
local TAP_WIDTH = num('ID_TAP_WIDTH', '2')
local DUMPS = {}
for _, f in ipairs(list('ID_DUMP_FRAMES', '1500,2000,3000,4500')) do DUMPS[f] = true end
local TAPS = list('ID_TAP_OFFSETS', '')
local RAW = num('ID_TAP_RAW', '300')
local last = num('LAST_FRAME', nil)

local out = assert(io.open(assert(os.getenv('ID_LOG'), 'ID_LOG is not set'), 'w'))
local frame = 0
local taps = {}

local function state(dev, key)
    return dev.state[key] and dev.state[key].value or 0
end

local function stack_word(at)
    local sp = state(main, 'A7')
    if sp == 0 then sp = state(main, 'SP') end
    if sp == 0 then return 0 end
    return mem:read_u32(sp + at)
end

local function emit(kind, base, offset, value, extra)
    out:write(string.format('%d\t%s\t%06X\t%X\t%s\t%s\n', frame, kind, base, offset, value,
        extra or '-'))
end

out:write('# frame\tkind\tbase\toffset\tvalue\textra\n')
out:write(string.format('# objects %d span %X taps %d\n', #OBJECTS, SPAN, #TAPS))

-- Every tapped read is counted per reader; only the first ID_TAP_RAW are written one by one,
-- so a field the engine reads every frame cannot flood the log.
local readers, raw_left = {}, RAW

for _, base in ipairs(OBJECTS) do
    for _, off in ipairs(TAPS) do
        local from = base + off
        taps[#taps + 1] = mem:install_read_tap(from, from + TAP_WIDTH - 1, 'id_read',
            function(addr, data, mask)
                local pc = state(main, 'PC')
                local offset = addr - base
                local key = string.format('%06X\t%X\t%06X', base, offset, pc)
                local seen = readers[key]
                if seen then
                    seen.n = seen.n + 1
                else
                    readers[key] = {n = 1, frame = frame, value = data & 0xffff, mask = mask,
                                    stk = string.format('%06X,%06X,%06X', stack_word(0),
                                                        stack_word(4), stack_word(8))}
                end
                if raw_left > 0 then
                    raw_left = raw_left - 1
                    emit('read', base, offset, string.format('%04X', data & 0xffff),
                        string.format('pc=%06X stk=%06X,%06X,%06X mask=%X', pc, stack_word(0),
                            stack_word(4), stack_word(8), mask))
                end
            end)
    end
end

local function report()
    for key, seen in pairs(readers) do
        out:write(string.format('%d\treader\t%s\t%04X\tn=%d first=%d stk=%s mask=%X\n',
            frame, key, seen.value, seen.n, seen.frame, seen.stk, seen.mask))
    end
end

local function dump()
    for _, base in ipairs(OBJECTS) do
        local bytes = {}
        for i = 0, SPAN - 1 do bytes[#bytes + 1] = string.format('%02X', mem:read_u8(base + i)) end
        emit('dump', base, 0, table.concat(bytes), string.format('span=%X', SPAN))
    end
end

emu.register_frame_done(function()
    if DUMPS[frame] then dump() end
    if last and frame >= last then report() out:flush() out:close() machine:exit() end
    frame = frame + 1
end, 'id_readers')
