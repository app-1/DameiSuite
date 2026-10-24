import sys, time, urllib.request
sys.path.append(r"c:\Dev\DameiAPI\scratch")
from ipc_lua import run_lua

def test_settings(thresh_db, trim_db):
    lua = f"""
    local tr = reaper.GetTrack(0, 15) -- Track 16
    reaper.TrackFX_SetParam(tr, 5, 11, {thresh_db}) -- slider12 is param 11 (0-indexed)
    reaper.TrackFX_SetParam(tr, 5, 3, {trim_db})    -- slider4 is param 3 (0-indexed)
    return true
    """
    run_lua(lua)
    time.sleep(0.3)
    
    # Measure
    urllib.request.urlopen("http://127.0.0.1:8080/_/SET/POS/28.0;1007")
    t0 = time.time()
    max_p = -100.0
    while time.time() - t0 < 4.0:
        time.sleep(0.1)
        r = urllib.request.urlopen("http://127.0.0.1:8080/_/TRACK/16;1016")
        for line in r.read().decode("utf-8").splitlines():
            p = line.split("\t")
            if len(p) >= 8 and p[0] == "TRACK" and p[1] == "16":
                pl = float(p[6]) / 10.0
                pr = float(p[7]) / 10.0
                if max(pl, pr) > max_p: max_p = max(pl, pr)
    urllib.request.urlopen("http://127.0.0.1:8080/_/1016")
    return max_p

print("Legacy Chain reference max peak: -3.80 dBFS")
for trim in [-1.5, -1.8, -2.0]:
    for thresh in [-9.0, -10.5, -12.0]:
        pk = test_settings(thresh, trim)
        delta = pk - (-3.80)
        print(f"Thresh={thresh:5.1f} dB, Trim={trim:4.1f} dB -> Max Peak={pk:+5.2f} dBFS (Delta={delta:+5.2f} dB)")
