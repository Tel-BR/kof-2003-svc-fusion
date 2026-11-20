-- Logs every sound request while the owner plays SVC Chaos with Guile (wayfinder ticket 33).
-- Passive: it only listens (memory taps and the frame callback) and never writes game memory.
-- Run it by hand as -autoboot_script; svc_voice_roles_report.py ("run") sets everything up.
--
-- Environment:
--   VOICE_LOG         output TSV (required). Keep it under private/: it carries game traces.
--   VOICE_SITUATIONS  situations file, one "<id><TAB><label>" per line (optional).
--   VOICE_KEY_NEXT    host key that advances the situation marker (default KEYCODE_0PAD).
--   VOICE_KEY_BACK    host key that goes back one marker (default KEYCODE_DELPAD).
--   VOICE_SHOW_EVERY  frames between reminders of the current situation (default 300, 0 = never).
--   VOICE_TABLE, VOICE_TABLE_ROWS, VOICE_BLOCK_ROW, VOICE_BLOCK_ROWS, VOICE_HELPER_LO,
--   VOICE_HELPER_HI, VOICE_STAGE, VOICE_LATCH   addresses and sizes from research 30 (defaults below).
--   PROBE_P1_OBJECT, PROBE_P2_OBJECT, PROBE_ANIM_OFFSET, PROBE_HEALTH_OFFSET   as in probe.lua.
--
-- Output: tab-separated, one line per event, flushed at once. Lines starting with # are notes.
--   frame  situation  kind  row  slot  word  p1_anim  p1_hp  p2_anim  p2_hp  extra
-- frame      completed frames + 1 (the same label probe.lua uses with REPLAY_OFFSET=1).
-- situation  marker index: 0 before the first key press, then 1, 2, ... as the owner advances.
-- kind       req    word read from the sound table by the helper at 0x00844C..0x0084D6 (a request)
--            reqx   word read from the sound table by other code (kept so nothing is hidden)
--            stage  word written to the sound staging cell (second view of the same requests)
--            cmd    byte written to the 68000 sound latch
--            play   Z80 started an ADPCM-A channel (extra: ch, start, end, last latch byte)
--            playB  Z80 started ADPCM-B (extra: start, end)
--            hp     P1 or P2 health changed
--            mark   the owner moved the situation marker (extra: id)
-- row        sound-table row; slot = row - VOICE_BLOCK_ROW inside Guile's block, else "other".
-- word       the 16-bit sound word (prefix and index) for req, reqx and stage; the byte for cmd.
local machine = manager.machine
local main = machine.devices[':maincpu']
local audio = machine.devices[':audiocpu']
local mem = main.spaces.program
local zio = audio.spaces.io

local function num(name, default) return tonumber(os.getenv(name) or default) end

local TABLE = num('VOICE_TABLE', '0x0A283C')
local TABLE_ROWS = num('VOICE_TABLE_ROWS', '4096')
local BLOCK_ROW = num('VOICE_BLOCK_ROW', '2496')
local BLOCK_ROWS = num('VOICE_BLOCK_ROWS', '80')
local HELPER_LO = num('VOICE_HELPER_LO', '0x00844C')
local HELPER_HI = num('VOICE_HELPER_HI', '0x0084D6')
local STAGE = num('VOICE_STAGE', '0x10C43C')
local LATCH = num('VOICE_LATCH', '0x320000')
local SHOW_EVERY = num('VOICE_SHOW_EVERY', '300')
local KEY_NEXT = os.getenv('VOICE_KEY_NEXT') or 'KEYCODE_0PAD'
local KEY_BACK = os.getenv('VOICE_KEY_BACK') or 'KEYCODE_DELPAD'
local p1 = num('PROBE_P1_OBJECT', '0x10a100')
local p2 = num('PROBE_P2_OBJECT', '0x10a380')
local anim = num('PROBE_ANIM_OFFSET', '0x28')
local hpoff = num('PROBE_HEALTH_OFFSET', '0x139')

local out = assert(io.open(assert(os.getenv('VOICE_LOG'), 'VOICE_LOG is not set'), 'w'))
local frame = 1
local sit = 0

local function state(dev, key)
    return dev.state[key] and dev.state[key].value or 0
end

-- Situations file: "<id><TAB><label>" per line; blank lines and # lines are skipped.
local situations = {}
local sfile = os.getenv('VOICE_SITUATIONS')
local f = sfile and io.open(sfile, 'r')
if f then
    for line in f:lines() do
        line = line:gsub('\r$', '')
        if line:match('%S') and not line:match('^%s*#') then
            local id, label = line:match('^([^\t]*)\t?(.*)$')
            situations[#situations + 1] = {id = id, label = label ~= '' and label or id}
        end
    end
    f:close()
end

local function note(text)
    out:write('#', text, '\n')
    out:flush()
end

local function context()
    return string.format('%08X\t%d\t%08X\t%d', mem:read_u32(p1 + anim), mem:read_u8(p1 + hpoff),
        mem:read_u32(p2 + anim), mem:read_u8(p2 + hpoff))
end

local function emit(kind, row, slot, word, extra)
    out:write(string.format('%d\t%d\t%s\t%s\t%s\t%s\t%s\t%s\n', frame, sit, kind, row, slot, word,
        context(), extra or ''))
    out:flush()
end

local ok_version, version = pcall(emu.app_version)
note(string.format('voice-roles log; mame=%s; table=%06X rows=%d block_row=%d block_rows=%d; sits=%d',
    ok_version and version or '?', TABLE, TABLE_ROWS, BLOCK_ROW, BLOCK_ROWS, #situations))
note('frame\tsit\tkind\trow\tslot\tword\tp1_anim\tp1_hp\tp2_anim\tp2_hp\textra')

local function stack_word(offset)
    local sp = state(main, 'A7')
    if sp == 0 then sp = state(main, 'SP') end
    return mem:read_u32(sp + offset)
end

-- Handles must stay referenced or MAME removes the taps.
voice_roles_handles = {}
local function keep(handle) voice_roles_handles[#voice_roles_handles + 1] = handle end

-- Sound table: the helpers read one word at TABLE + 2 x row.
keep(mem:install_read_tap(TABLE, TABLE + 2 * TABLE_ROWS - 1, 'voice_table', function(addr, data, mask)
    local row = (addr - TABLE) // 2
    local pc = state(main, 'PC')
    local kind = (pc >= HELPER_LO and pc <= HELPER_HI) and 'req' or 'reqx'
    local slot = (row >= BLOCK_ROW and row < BLOCK_ROW + BLOCK_ROWS) and tostring(row - BLOCK_ROW) or 'other'
    local word = (mask & 0xffff) == 0xffff and string.format('%04X', data & 0xffff) or '----'
    emit(kind, row, slot, word, string.format('pc=%06X a4=%06X stk=%06X,%06X,%06X mask=%X', pc,
        state(main, 'A4'), stack_word(8), stack_word(12), stack_word(16), mask))
end))

-- Staging cell: the same words, seen where they are queued (catches a request that skips the table).
keep(mem:install_write_tap(STAGE, STAGE + 3, 'voice_stage', function(addr, data, mask)
    if (mask & 0xffff) ~= 0xffff then return end
    emit('stage', '-', '-', string.format('%04X', data & 0xffff),
        string.format('addr=%06X pc=%06X', addr, state(main, 'PC')))
end))

-- Sound latch: the byte the 68000 sends to the Z80.
keep(mem:install_write_tap(LATCH, LATCH + 1, 'voice_latch', function(addr, data, mask)
    if (mask & 0xff00) == 0 then return end
    emit('cmd', '-', '-', string.format('%02X', (data >> 8) & 0xff), string.format('pc=%06X', state(main, 'PC')))
end))

-- Z80 side: which sample range the chip really starts (same decoding as the research 26 capture).
local last_latch = 0
keep(zio:install_read_tap(0, 0xffff, 'voice_latch_in', function(addr, data, _)
    if (addr & 0xff) == 0 then last_latch = data end
end))
local regs, porta, portb = {}, 0, 0
keep(zio:install_write_tap(0, 0xffff, 'voice_ym', function(addr, data, _)
    local low = addr & 0xff
    if low == 4 then
        porta = data
    elseif low == 6 then
        portb = data
    elseif low == 5 then
        regs[porta] = data
        if porta == 0x10 and (data & 0x80) ~= 0 then
            local start = ((regs[0x13] or 0) << 8 | (regs[0x12] or 0)) << 8
            local ending = (((regs[0x15] or 0) << 8 | (regs[0x14] or 0)) << 8) | 0xff
            emit('playB', '-', '-', '-', string.format('start=%06X end=%06X latch=%02X', start, ending, last_latch))
        end
    elseif low == 7 then
        regs[0x100 | portb] = data
        if portb == 0 and (data & 0x80) == 0 then
            for c = 0, 5 do
                if (data & (1 << c)) ~= 0 then
                    local start = ((regs[0x118 + c] or 0) << 8 | (regs[0x110 + c] or 0)) << 8
                    local ending = (((regs[0x128 + c] or 0) << 8 | (regs[0x120 + c] or 0)) << 8) | 0xff
                    emit('play', '-', '-', '-', string.format('ch=%d start=%06X end=%06X latch=%02X',
                        c, start, ending, last_latch))
                end
            end
        end
    end
end))

-- Owner-driven situation marker.
local input = machine.input
local function key_code(token)
    local ok, code = pcall(input.code_from_token, input, token)
    if not ok then note('key ' .. token .. ' not accepted: ' .. tostring(code)) return nil end
    return code
end
local code_next, code_back = key_code(KEY_NEXT), key_code(KEY_BACK)
local function pressed(code)
    if code == nil then return false end
    local ok, value = pcall(input.code_pressed, input, code)
    return ok and value or false
end

local function describe()
    local total = #situations
    if sit == 0 then return string.format('[0/%d] before the first marker', total) end
    local s = situations[sit]
    if s then return string.format('[%d/%d] %s', sit, total, s.label) end
    return string.format('[%d] marker %d', sit, sit)
end

local function show(text)
    pcall(machine.popmessage, machine, text or describe())
end

local function move_marker(step)
    local target = sit + step
    if target < 0 or (#situations > 0 and target > #situations) then
        show(describe() .. (target < 0 and ' (first)' or ' (last)'))
        return
    end
    sit = target
    local s = situations[sit]
    emit('mark', '-', '-', '-', 'id=' .. (s and s.id or ('marker' .. sit)))
    show()
end

local was_next, was_back = false, false
local last_p1, last_p2 = mem:read_u8(p1 + hpoff), mem:read_u8(p2 + hpoff)
emu.register_frame_done(function()
    local now_next, now_back = pressed(code_next), pressed(code_back)
    if now_next and not was_next then move_marker(1) end
    if now_back and not was_back then move_marker(-1) end
    was_next, was_back = now_next, now_back
    local h1, h2 = mem:read_u8(p1 + hpoff), mem:read_u8(p2 + hpoff)
    if h1 ~= last_p1 or h2 ~= last_p2 then
        emit('hp', '-', '-', '-', string.format('p1=%d p2=%d', h1, h2))
        last_p1, last_p2 = h1, h2
    end
    if frame == 120 then
        show(string.format('Voice roles: %s = next situation, %s = back', KEY_NEXT, KEY_BACK))
    elseif SHOW_EVERY > 0 and frame % SHOW_EVERY == 0 then
        show()
    end
    frame = frame + 1
end, 'voice roles')
