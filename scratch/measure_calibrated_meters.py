import sys, math, time, urllib.request
sys.path.append(r"C:\Dev\DameiAPI\scratch")
from ipc_lua import run_lua

def req(cmd):
    url = f'http://127.0.0.1:8080/_/{cmd}'
    with urllib.request.urlopen(url) as r:
        return r.read().decode('utf-8')

# Seek to Chorus 1
req('SET/POS/26.0')
req('1007') # Play
time.sleep(2.5) # Let chorus hit

# Sample live Web API meters
res = req('TRACK/0;TRACK/4;TRACK/5;TRACK/15;TRACK/16;TRACK/51;TRACK/69;TRANSPORT')
req('1016') # Stop

print("=== REAPER LIVE MIX METERS (CHORUS 1) ===")
for line in res.strip().splitlines():
    parts = line.split("\t")
    if len(parts) >= 8 and parts[0] == "TRACK":
        t_idx = parts[1]
        t_name = parts[2]
        p1 = float(parts[6]) / 10.0
        p2 = float(parts[7]) / 10.0
        print(f"Track {t_idx:2s} ({t_name:25s}): Peak = {max(p1, p2):+5.1f} dB")
