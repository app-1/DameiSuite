import sys, time, urllib.request
sys.path.append(r"c:\Dev\DameiAPI\scratch")
from ipc_lua import run_lua

def measure_vox(duration=4.0):
    urllib.request.urlopen("http://127.0.0.1:8080/_/SET/POS/28.0;1007")
    t0 = time.time()
    max_pk = -100.0
    samples = []
    while time.time() - t0 < duration:
        time.sleep(0.1)
        r = urllib.request.urlopen("http://127.0.0.1:8080/_/TRACK/4;TRACK/16;1016")
        for line in r.read().decode("utf-8").splitlines():
            p = line.split("\t")
            if len(p) >= 8 and p[0] == "TRACK" and p[1] == "4":
                pl = float(p[6]) / 10.0
                pr = float(p[7]) / 10.0
                pk = max(pl, pr)
                if pk > max_pk: max_pk = pk
                samples.append(pk)
    urllib.request.urlopen("http://127.0.0.1:8080/_/1016")
    avg_pk = sum(samples) / len(samples) if samples else -100.0
    return max_pk, avg_pk

print("Current Vocal State (Track 5 Sovereign ON, Track 4 Empress ON, Fader -3dB):")
pk1, avg1 = measure_vox(4.0)
print(f"  Vocal Max Peak = {pk1:+.2f} dBFS | Avg Peak = {avg1:+.2f} dBFS")

# Now apply Option A:
# Bypass Track 5 FX (Vocal Sovereign)
# Set Track 4 fader to 0.0 dB
# Reload Track 4 Vocal Empress Preset 06
lua_option_a = """
local tr4 = reaper.GetTrack(0, 3) -- Track 4
local tr5 = reaper.GetTrack(0, 4) -- Track 5

-- 1. Bypass Track 5 FX 0 (Vocal Sovereign)
reaper.TrackFX_SetEnabled(tr5, 0, false)

-- 2. Set Track 4 fader to 0.0 dB (D_VOL = 1.0)
reaper.SetMediaTrackInfo_Value(tr4, "D_VOL", 1.0)

-- 3. Set Track 4 Vocal Empress to Preset 06
reaper.TrackFX_SetParam(tr4, 0, 1, 6) -- slider2 = 6

return "OPTION_A_APPLIED"
"""
run_lua(lua_option_a)
time.sleep(1.0)

print("\nUnified Flagship Option A State (Track 5 Bypassed, Track 4 Empress at 0dB Fader, Preset 06):")
pk2, avg2 = measure_vox(4.0)
print(f"  Vocal Max Peak = {pk2:+.2f} dBFS | Avg Peak = {avg2:+.2f} dBFS")
print(f"  Delta = {pk2 - pk1:+.2f} dB")
