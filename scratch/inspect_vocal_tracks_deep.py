import sys
sys.path.append(r"C:\Dev\DameiAPI\scratch")
from ipc_lua import run_lua

lua_code = """
local tracks = {}
for i = 0, reaper.CountTracks(0) - 1 do
    local tr = reaper.GetTrack(0, i)
    local _, name = reaper.GetSetMediaTrackInfo_String(tr, "P_NAME", "", false)
    local num = reaper.GetMediaTrackInfo_Value(tr, "IP_TRACKNUMBER")
    local vol = reaper.GetMediaTrackInfo_Value(tr, "D_VOL")
    local mute = reaper.GetMediaTrackInfo_Value(tr, "B_MUTE")
    local solo = reaper.GetMediaTrackInfo_Value(tr, "I_SOLO")
    local num_items = reaper.CountTrackMediaItems(tr)
    local items = {}
    for it = 0, math.min(num_items - 1, 10) do
        local item = reaper.GetTrackMediaItem(tr, it)
        local pos = reaper.GetMediaItemInfo_Value(item, "D_POSITION")
        local len = reaper.GetMediaItemInfo_Value(item, "D_LENGTH")
        local take = reaper.GetActiveTake(item)
        local take_name = ""
        if take then
            _, take_name = reaper.GetSetMediaItemTakeInfo_String(take, "P_NAME", "", false)
        end
        table.insert(items, {pos = pos, len = len, name = take_name})
    end
    if name:lower():find("vox") or name:lower():find("vocal") or name:lower():find("adlib") or name:lower():find("verb") or (i >= 0 and i <= 10) then
        table.insert(tracks, {idx = i, num = num, name = name, vol = vol, mute = mute, solo = solo, num_items = num_items, items = items})
    end
end
return tracks
"""

res = run_lua(lua_code)
import json, math
for t in res:
    db = 20*math.log10(t['vol']) if t['vol'] > 0.00001 else -150
    print(f"Track {t['num']:2.0f} (idx={t['idx']:2d}): \"{t['name']}\" | vol={db:+.1f}dB, mute={t['mute']}, items={t['num_items']}")
    for it in t['items'][:4]:
        print(f"    Item @ {it['pos']:.2f}s (len={it['len']:.2f}s): {it['name'][:60]}")
