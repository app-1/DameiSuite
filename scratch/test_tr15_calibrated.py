import sys, urllib.request, time
sys.path.append(r"C:\Dev\DameiAPI\scratch")
from ipc_lua import run_lua

# Set Track 15 fader to -1.4 dB (0.851138)
run_lua("""
local tr15 = reaper.GetTrack(0, 14)
reaper.SetMediaTrackInfo_Value(tr15, "D_VOL", 0.851138)
""")

def req(cmd):
    url = f'http://127.0.0.1:8080/_/{cmd}'
    with urllib.request.urlopen(url) as r: return r.read().decode('utf-8')

req('SET/POS/26.0;1007')
time.sleep(2.5)
res = req('TRACK/4;TRACK/15;TRACK/16;TRACK/51;TRACK/69;1016')

print("=== REAPER LIVE MIX METERS (INSTRUMENTAL BUS CALIBRATED TO -4.9 dB) ===")
for l in res.strip().splitlines():
    parts = l.split('\t')
    if len(parts) >= 8 and parts[0] == 'TRACK':
        p = max(float(parts[6]), float(parts[7])) / 10.0
        print(f"Track {parts[1]:2s} ({parts[2]:25s}): Peak = {p:+5.1f} dB")
