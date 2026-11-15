-- Saves captures while MAME plays back an .inp recording (-playback). SHOT_FRAMES lists
-- frame counts with the same numbering as log_inputs.lua; LAST_FRAME stops MAME.
local shots = {}
for f in (os.getenv('SHOT_FRAMES') or ''):gmatch('%d+') do shots[tonumber(f)] = true end
local last = tonumber(os.getenv('LAST_FRAME'))
local screen = manager.machine.screens[':screen']
local done = 0
emu.register_frame_done(function()
    if shots[done] then screen:snapshot(('f%05d.png'):format(done)) end
    if last and done >= last then manager.machine:exit() end
    done = done + 1
end, 'shots')
