import sys, urllib.request, time
sys.path.append(r"C:\Dev\DameiAPI\scratch")
from ipc_lua import run_lua

# Mute tracks 6, 7, 8, 9, 10 (0-indexed 5, 6, 7, 8, 9)
run_lua("""
for t = 5, 9 do
    local tr = reaper.GetTrack(0, t)
    reaper.SetMediaTrackInfo_Value(tr, "B_MUTE", 1)
end
local tr5 = reaper.GetTrack(0, 4)
reaper.SetMediaTrackInfo_Value(tr5, "B_MUTE", 0)
""")

def req(cmd):
    url = f'http://127.0.0.1:8080/_/{cmd}'
    with urllib.request.urlopen(url) as r: return r.read().decode('utf-8')

req('SET/POS/27.0;1007')
time.sleep(2.0)
res = req('TRACK/4;TRACK/5;1016')
for l in res.strip().splitlines():
    p = l.split('\t')
    if len(p) >= 8 and p[0] == 'TRACK':
        print(f"Track {p[1]} ({p[2]}): {max(float(p[6]), float(p[7]))/10.0:+.1f} dB")

# Unmute tracks 6, 7, 9, 10 (keep 8 muted as it was originally)
run_lua("""
reaper.SetMediaTrackInfo_Value(reaper.GetTrack(0, 5), "B_MUTE", 0)
reaper.SetMediaTrackInfo_Value(reaper.GetTrack(0, 6), "B_MUTE", 0)
reaper.SetMediaTrackInfo_Value(reaper.GetTrack(0, 7), "B_MUTE", 1) -- -1VoxLeft originally muted
reaper.SetMediaTrackInfo_Value(reaper.GetTrack(0, 8), "B_MUTE", 0)
reaper.SetMediaTrackInfo_Value(reaper.GetTrack(0, 9), "B_MUTE", 0)
""")
