-- Records the owner's inputs while playing in MAME (-autoboot_script), one line per change.
-- Output: INPUT_LOG; read it with match.session.read_log. Do not use MAME's soft reset (F3)
-- while recording: the reset is not in the .inp recording and it corrupts this log.
-- Logs Player 1 and system inputs whenever they change, by completed frame.
-- Line format: "<frames done>\t<button>[+<button>...]" or "<frames done>\t-".
local names = {
    [':edge:joy:JOY1'] = {['P1 Up']='up', ['P1 Down']='down', ['P1 Left']='left', ['P1 Right']='right',
        ['P1 A']='a', ['P1 B']='b', ['P1 C']='c', ['P1 D']='d'},
    [':edge:joy:START'] = {['1 Player Start']='start'},
    [':AUDIO_COIN'] = {['Coin 1']='coin'},
}
local watched = {}
for tag, map in pairs(names) do
    local port = manager.machine.ioport.ports[tag]
    for fname, short in pairs(map) do
        local f = port and port.fields[fname]
        if f then watched[#watched + 1] = {port = port, field = f, name = short} end
    end
end
local log = assert(io.open(assert(os.getenv('INPUT_LOG')), 'w'))
local last, done = nil, 0
emu.register_frame_done(function()
    local held = {}
    for _, w in ipairs(watched) do
        local v = w.port:read() & w.field.mask
        if v ~= (w.field.defvalue & w.field.mask) then held[#held + 1] = w.name end
    end
    table.sort(held)
    local now = #held > 0 and table.concat(held, '+') or '-'
    if now ~= last then log:write(done, '\t', now, '\n') log:flush() last = now end
    done = done + 1
end, 'input-log')
