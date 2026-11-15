-- Replays a button transition list on MAME's Neo Geo MVS driver.
--
-- Frame numbering follows the native neogeorecomp player: inputs for frame N
-- are applied before frame N runs (frame 0 is the first frame after power-on),
-- and a capture of frame N is taken once frame N has been drawn.
--
-- REPLAY_TRANSITIONS  file of "<frame>\t<button>[+<button>...]" or "<frame>\t-"
-- REPLAY_SHOTS        file of "<frame>\t<png name>" (written under -snapshot_directory)
-- REPLAY_FRAMES       stop after this many frames
-- REPLAY_OFFSET       native frame shown by MAME's first completed frame
--                     (measured: 2 for kof2003 with the Europe MVS v2 BIOS)
local ports = manager.machine.ioport.ports
local fields = {
    up = {':edge:joy:JOY1', 'P1 Up'}, down = {':edge:joy:JOY1', 'P1 Down'},
    left = {':edge:joy:JOY1', 'P1 Left'}, right = {':edge:joy:JOY1', 'P1 Right'},
    a = {':edge:joy:JOY1', 'P1 A'}, b = {':edge:joy:JOY1', 'P1 B'},
    c = {':edge:joy:JOY1', 'P1 C'}, d = {':edge:joy:JOY1', 'P1 D'},
    p2up = {':edge:joy:JOY2', 'P2 Up'}, p2down = {':edge:joy:JOY2', 'P2 Down'},
    p2left = {':edge:joy:JOY2', 'P2 Left'}, p2right = {':edge:joy:JOY2', 'P2 Right'},
    p2a = {':edge:joy:JOY2', 'P2 A'}, p2b = {':edge:joy:JOY2', 'P2 B'},
    p2c = {':edge:joy:JOY2', 'P2 C'}, p2d = {':edge:joy:JOY2', 'P2 D'},
    start = {':edge:joy:START', '1 Player Start'}, start2 = {':edge:joy:START', '2 Players Start'},
    coin = {':AUDIO_COIN', 'Coin 1'}, coin2 = {':AUDIO_COIN', 'Coin 2'},
    service = {':AUDIO_COIN', 'Service 1'},
}

local function field(name)
    local where = assert(fields[name], 'button not available on MAME MVS: ' .. name)
    return assert(ports[where[1]].fields[where[2]], 'missing MAME field ' .. where[2])
end

local function read_pairs(path)
    local rows = {}
    for line in io.lines(path) do
        local frame, value = line:match('^(%d+)\t(.+)$')
        if frame then rows[tonumber(frame)] = value end
    end
    return rows
end

local changes = read_pairs(assert(os.getenv('REPLAY_TRANSITIONS')))
local shots = read_pairs(assert(os.getenv('REPLAY_SHOTS')))
local last = assert(tonumber(os.getenv('REPLAY_FRAMES')))
local screen = manager.machine.screens[':screen']
local held = {}

local function apply(frame)
    local change = changes[frame]
    if not change then return end
    local now = {}
    if change ~= '-' then
        for name in change:gmatch('[^+]+') do now[name] = true end
    end
    for name in pairs(held) do
        if not now[name] then field(name):clear_value() end
    end
    for name in pairs(now) do field(name):set_value(1) end
    held = now
end

-- Measured alignment (ticket 02): when MAME reports frame done for the
-- (n+1)-th time, its screen shows native frame n + OFFSET, and setting the
-- inputs for that same native frame at this point reproduces the native run
-- through coin, start and team selection up to the first in-fight input.
-- OFFSET is 2 for kof2003 with the Europe MVS v2 BIOS. Sprites may still
-- differ by one frame because the two renderers latch them differently.
local offset = tonumber(os.getenv('REPLAY_OFFSET') or '2')
local done = 0
for frame = 0, offset - 1 do apply(frame) end
emu.register_frame_done(function()
    local native_frame = done + offset
    done = done + 1
    if shots[native_frame] then screen:snapshot(shots[native_frame]) end
    if native_frame >= last then manager.machine:exit() return end
    apply(native_frame)
end, 'replay')
