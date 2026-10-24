import sys, time, urllib.request
sys.path.append(r"c:\Dev\DameiAPI\scratch")
from ipc_lua import run_lua

def set_state(use_suite_only):
    lua = f"""
    local tr15 = reaper.GetTrack(0, 14)
    -- FX 0..4 legacy
    for i = 0, 4 do
        reaper.TrackFX_SetEnabled(tr15, i, {str(not use_suite_only).lower()})
    end
    -- FX 5 Damei Suite
    reaper.TrackFX_SetEnabled(tr15, 5, {str(use_suite_only).lower()})
    return true
    """
    run_lua(lua)

def measure():
    urllib.request.urlopen("http://127.0.0.1:8080/_/SET/POS/26.0;1007")
    time.sleep(2.5)
    r = urllib.request.urlopen("http://127.0.0.1:8080/_/TRACK/4;TRACK/15;TRACK/16;TRACK/40;TRACK/51;TRACK/69;1016")
    lines = r.read().decode("utf-8").strip().splitlines()
    urllib.request.urlopen("http://127.0.0.1:8080/_/1016")
    peaks = {}
    for l in lines:
        p = l.split("\t")
        if len(p) >= 8 and p[0] == "TRACK":
            t_idx = p[1]
            t_name = p[2]
            peak = max(float(p[6]), float(p[7])) / 10.0
            peaks[f"Tr {t_idx:2s} ({t_name:20s})"] = peak
    return peaks

print("Measuring CONDITION A: Legacy Chain (FX 0..4 ON, Suite BYPASSED)...")
set_state(use_suite_only=False)
res_legacy = measure()

print("Measuring CONDITION B: Damei Suite Only (FX 0..4 BYPASSED, Suite ON)...")
set_state(use_suite_only=True)
res_suite = measure()

print("\n==================== FORENSIC MIX LEVEL COMPARISON ====================")
hdr = f"{'Track':30s} | {'Legacy Chain':14s} | {'Damei Suite':14s} | {'Delta':8s}"
print(hdr)
print("-" * len(hdr))
for k in res_legacy:
    v_leg = res_legacy[k]
    v_sui = res_suite.get(k, 0.0)
    diff = v_sui - v_leg
    print(f"{k:30s} | {v_leg:+6.1f} dBFS      | {v_sui:+6.1f} dBFS      | {diff:+5.1f} dB")

# Keep Suite Only active as requested by the user
set_state(use_suite_only=True)
print("\n[STATUS] Track 15 switched to Damei Instrumental Bus Alchemist ONLY (Legacy chain bypassed).")
