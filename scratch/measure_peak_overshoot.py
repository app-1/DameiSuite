import sys, time, urllib.request, json
sys.path.append(r"c:\Dev\DameiAPI\scratch")
from ipc_lua import run_lua

def set_tr16_state(use_suite_only):
    lua = f"""
    local tr = reaper.GetTrack(0, 15) -- Track 16 (0-indexed 15)
    for i = 0, 4 do
        reaper.TrackFX_SetEnabled(tr, i, {str(not use_suite_only).lower()})
    end
    reaper.TrackFX_SetEnabled(tr, 5, {str(use_suite_only).lower()})
    return true
    """
    run_lua(lua)

def measure_peaks_over_window(duration_sec=4.0):
    # Set play position to 28.0 (chorus entry) and start playback
    urllib.request.urlopen("http://127.0.0.1:8080/_/SET/POS/28.0;1007")
    t0 = time.time()
    max_peak_l = -100.0
    max_peak_r = -100.0
    samples = []
    while time.time() - t0 < duration_sec:
        time.sleep(0.1)
        r = urllib.request.urlopen("http://127.0.0.1:8080/_/TRACK/16;1016")
        lines = r.read().decode("utf-8").strip().splitlines()
        for l in lines:
            p = l.split("\t")
            if len(p) >= 8 and p[0] == "TRACK" and p[1] == "16":
                pl = float(p[6]) / 10.0
                pr = float(p[7]) / 10.0
                if pl > max_peak_l: max_peak_l = pl
                if pr > max_peak_r: max_peak_r = pr
                samples.append(max(pl, pr))
    urllib.request.urlopen("http://127.0.0.1:8080/_/1016") # Stop
    avg_peak = sum(samples) / len(samples) if samples else -100.0
    return {
        "max_peak": max(max_peak_l, max_peak_r),
        "max_peak_l": max_peak_l,
        "max_peak_r": max_peak_r,
        "avg_peak": avg_peak
    }

print("Testing Condition A: Legacy Chain (Britson + TB EQ + DeeGain + Bass Manager + BUSTERse)...")
set_tr16_state(use_suite_only=False)
time.sleep(0.5)
res_legacy = measure_peaks_over_window(5.0)

print("Testing Condition B: Damei Instrumental Bus Alchemist...")
set_tr16_state(use_suite_only=True)
time.sleep(0.5)
res_suite = measure_peaks_over_window(5.0)

print("\n================== INSTRUMENTAL BUS PEAK CAPTURE AUDIT ==================")
print(f"Condition A (Legacy Chain) : Max Peak = {res_legacy['max_peak']:+.2f} dBFS | Avg Peak = {res_legacy['avg_peak']:+.2f} dBFS")
print(f"Condition B (Damei Suite)  : Max Peak = {res_suite['max_peak']:+.2f} dBFS | Avg Peak = {res_suite['avg_peak']:+.2f} dBFS")
delta_peak = res_suite['max_peak'] - res_legacy['max_peak']
print(f"Peak Delta (Overshoot)     : {delta_peak:+.2f} dB")
if delta_peak > 0.5:
    print(f"-> CONFIRMED: Damei Suite allows {delta_peak:+.2f} dB transient overshoot compared to legacy chain!")
