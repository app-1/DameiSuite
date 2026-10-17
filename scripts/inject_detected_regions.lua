-- ==============================================================================
-- DAMEI HUGGINGFACE AI SONG REGION INJECTOR
-- Generated automatically from HuggingFace CLAP Model Analysis
-- Target File: HexGyal.wav
-- Duration: 108.95s
-- ==============================================================================

reaper.Undo_BeginBlock()

-- 1. Clear existing Damei structural regions to prevent timeline duplicates
local num_markers, num_regions = reaper.CountProjectMarkers(0)
for i = num_markers + num_regions - 1, 0, -1 do
  local retval, isrgn, pos, rgnend, name, idx = reaper.EnumProjectMarkers(i)
  if retval and isrgn then
    local n = name:lower()
    if n:find('chorus') or n:find('verse') or n:find('intro') or n:find('bridge') or n:find('outro') or n:find('pre') then
      reaper.DeleteProjectMarker(0, idx, true)
    end
  end
end

-- 2. Inject detected sections with color coding
local col_intro = reaper.ColorToNative(255, 215, 60) | 0x1000000
reaper.AddProjectMarker2(0, true, 0.00, 14.00, 'Intro', -1, col_intro)
local col_verse_1 = reaper.ColorToNative(30, 200, 255) | 0x1000000
reaper.AddProjectMarker2(0, true, 14.00, 28.00, 'Verse 1', -1, col_verse_1)
local col_chorus_1 = reaper.ColorToNative(40, 240, 110) | 0x1000000
reaper.AddProjectMarker2(0, true, 28.00, 44.00, 'Chorus 1', -1, col_chorus_1)
local col_bridge_1 = reaper.ColorToNative(218, 112, 214) | 0x1000000
reaper.AddProjectMarker2(0, true, 44.00, 60.00, 'Bridge 1', -1, col_bridge_1)
local col_chorus_2 = reaper.ColorToNative(40, 240, 110) | 0x1000000
reaper.AddProjectMarker2(0, true, 60.00, 68.00, 'Chorus 2', -1, col_chorus_2)
local col_verse_2 = reaper.ColorToNative(30, 200, 255) | 0x1000000
reaper.AddProjectMarker2(0, true, 68.00, 78.00, 'Verse 2', -1, col_verse_2)
local col_bridge_2 = reaper.ColorToNative(218, 112, 214) | 0x1000000
reaper.AddProjectMarker2(0, true, 78.00, 92.00, 'Bridge 2', -1, col_bridge_2)
local col_chorus_3 = reaper.ColorToNative(40, 240, 110) | 0x1000000
reaper.AddProjectMarker2(0, true, 92.00, 98.00, 'Chorus 3', -1, col_chorus_3)
local col_outro = reaper.ColorToNative(130, 140, 155) | 0x1000000
reaper.AddProjectMarker2(0, true, 98.00, 108.95, 'Outro', -1, col_outro)

reaper.Undo_EndBlock('Inject Damei AI Song Structure Regions', -1)
reaper.UpdateTimeline()
reaper.ShowConsoleMsg('[Damei AI] Injected 9 structural regions into REAPER timeline!\n')