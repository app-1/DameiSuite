import sys, urllib.request, time
sys.path.append(r"C:\Dev\DameiAPI\scratch")
from ipc_lua import run_lua

# Set Track 15 fader to 0.90 (-0.9 dB)
run_lua("""
local tr15 = reaper.GetTrack(0, 14)
reaper.SetMediaTrackInfo_Value(tr15, "D_VOL", 0.90)
""")

def req(cmd):
    url = f'http://127.0.0.1:8080/_/{cmd}'
    with urllib.request.urlopen(url) as r: return r.read().decode('utf-8')

req('SET/POS/26.0;1007')

max_peaks = {}
t0 = time.time()
while time.time() - t0 < 4.0:
    res = req('TRACK/0;TRACK/4;TRACK/15;TRACK/16;TRACK/51;TRACK/69')
    for l in res.strip().splitlines():
        parts = l.split('\t')
        if len(parts) >= 8 and parts[0] == 'TRACK':
            t_name = parts[2]
            p = max(float(parts[6]), float(parts[7])) / 10.0
            if t_name not in max_peaks or p > max_peaks[t_name]:
                max_peaks[t_name] = p
    time.sleep(0.2)

req('1016')

print("=== REAPER CHORUS 1 PEAKS (Track 15 fader @ -0.9 dB) ===")
for name, val in max_peaks.items():
    print(f"  {name:25s}: {val:+5.1f} dB")
