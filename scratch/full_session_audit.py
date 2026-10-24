import sys, time, urllib.request
sys.path.append(r"c:\Dev\DameiAPI\scratch")
from ipc_lua import run_lua

def full_session_audit():
    urllib.request.urlopen("http://127.0.0.1:8080/_/SET/POS/28.0;1007")
    time.sleep(3.0)
    
    # Query main tracks: Master, VOX (4), STEMS (12), INST BUSS (16), DRUMS (17), SYNTHS (41), GUITAR (52), BASS (70)
    track_ids = [0, 4, 16, 17, 41, 52, 70] # 1-based display indices
    cmd = ";".join([f"TRACK/{t}" for t in track_ids]) + ";1016"
    r = urllib.request.urlopen(f"http://127.0.0.1:8080/_/{cmd}")
    lines = r.read().decode("utf-8").strip().splitlines()
    urllib.request.urlopen("http://127.0.0.1:8080/_/1016") # Stop
    
    out = {}
    for l in lines:
        p = l.split("\t")
        if len(p) >= 8 and p[0] == "TRACK":
            t_idx = p[1]
            name = p[2]
            pl = float(p[6]) / 10.0
            pr = float(p[7]) / 10.0
            out[f"Tr {t_idx:2s} ({name:20s})"] = max(pl, pr)
    return out

res = full_session_audit()
print("\n================== FULL SESSION LIVE MIX AUDIT ==================")
for k, v in res.items():
    print(f"{k:32s} : {v:+6.2f} dBFS Peak")
