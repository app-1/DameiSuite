import sys, time
sys.path.append(r'c:\Dev\DameiAPI\scratch')
from ipc_lua import run_lua

play_and_read = """
local tr = reaper.GetTrack(0, 14)
reaper.TrackFX_SetParam(tr, 5, 1, 6)
reaper.SetEditCurPos(52.683, false, false)
reaper.CSurf_OnPlay()

local t0 = reaper.time_precise()
while reaper.time_precise() - t0 < 1.0 do end

reaper.gmem_attach('DameiMixMetering')

local glue_gr = reaper.gmem_read(10)
local inst_rms = reaper.gmem_read(11)
local inst_pk = reaper.gmem_read(12)
local inst_w = reaper.gmem_read(13)
local pocket_dip = reaper.gmem_read(14)

local inst_active = reaper.gmem_read(940)
local inst_preset = reaper.gmem_read(941)
local inst_crest = reaper.gmem_read(944)
local sub_mono_r = reaper.gmem_read(946)
local rel_mst = reaper.gmem_read(948)
local rel_vox = reaper.gmem_read(949)
local heartbeat = reaper.gmem_read(955)

local mix_active = reaper.gmem_read(1000)
local num_suites = reaper.gmem_read(1001)
local mix_pb_in  = reaper.gmem_read(1040)

local mst_rms = reaper.gmem_read(800)
local vox_rms = reaper.gmem_read(883)
local drm_rms = reaper.gmem_read(823)
local gtr_rms = reaper.gmem_read(843)
local bas_rms = reaper.gmem_read(863)

reaper.CSurf_OnStop()

local res = '=== DAMEI ECOSYSTEM LIVE AUDIT ===' .. '\\n' ..
  'Inst Active: ' .. tostring(inst_active) .. ' | Preset: ' .. tostring(inst_preset) .. '\\n' ..
  'Inst RMS: ' .. string.format('%.2f', inst_rms) .. ' dBFS | Crest: ' .. string.format('%.2f', inst_crest) .. ' dB\\n' ..
  'Inst Width: ' .. string.format('%.2f', inst_w) .. 'x | Sub-Mono Ratio: ' .. string.format('%.2f', sub_mono_r) .. ' dB\\n' ..
  'Glue GR: ' .. string.format('%.2f', glue_gr) .. ' dB | Pocket Notch: ' .. string.format('%.2f', pocket_dip) .. ' dB\\n' ..
  'Inst vs Master: ' .. string.format('%.2f', rel_mst) .. ' dB | Inst vs Vocal: ' .. string.format('%.2f', rel_vox) .. ' dB\\n' ..
  'Mix Active: ' .. tostring(mix_active) .. ' | Suites: ' .. tostring(num_suites) .. ' | Inst Present: ' .. tostring(mix_pb_in) .. '\\n' ..
  'Master RMS: ' .. string.format('%.2f', mst_rms) .. ' | Vocal RMS: ' .. string.format('%.2f', vox_rms) .. '\\n' ..
  'Heartbeat Age: ' .. string.format('%.3f', reaper.time_precise() - heartbeat) .. 's'

return res
"""

print(run_lua(play_and_read))
