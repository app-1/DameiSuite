import ctypes
from ctypes import wintypes
from PIL import ImageGrab
import os, time, sys

sys.path.append(r"C:\Dev\DameiAPI\scratch")
from ipc_lua import run_lua

user32 = ctypes.windll.user32
h_winsta = user32.OpenWindowStationW('winsta0', False, 0x0000037F)
user32.SetProcessWindowStation(h_winsta)
h_desktop = user32.OpenDesktopW('default', 0, False, 0x01FF)
user32.SetThreadDesktop(h_desktop)

artifact_dir = r"C:\Users\pityy\.gemini\antigravity-ide\brain\3c9ba815-5b40-4462-b423-397fc6dc8ce3"

def find_window_by_substr(substr):
    found_hwnd = 0
    def enum_cb(hwnd, lparam):
        nonlocal found_hwnd
        if user32.IsWindowVisible(hwnd):
            length = user32.GetWindowTextLengthW(hwnd)
            if length > 0:
                buff = ctypes.create_unicode_buffer(length + 1)
                user32.GetWindowTextW(hwnd, buff, length + 1)
                if substr.lower() in buff.value.lower():
                    found_hwnd = hwnd
                    return False
        return True
    WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)
    user32.EnumWindows(WNDENUMPROC(enum_cb), 0)
    return found_hwnd

def capture_window(hwnd, filename):
    if not hwnd:
        print(f"Skipping {filename}: window not found")
        return None
    rect = wintypes.RECT()
    user32.GetWindowRect(hwnd, ctypes.byref(rect))
    bbox = (rect.left, rect.top, rect.right, rect.bottom)
    user32.ShowWindow(hwnd, 9) # SW_RESTORE
    user32.SetForegroundWindow(hwnd)
    time.sleep(0.5)
    im = ImageGrab.grab(bbox=bbox)
    out_path = os.path.join(artifact_dir, filename)
    im.save(out_path)
    print(f"Captured: {filename} ({im.size[0]}x{im.size[1]})")
    return out_path

# =========================================================================
# 1. SANKOFA ORACLE (Master FX 1) - Reference Library View
# =========================================================================
print("\n--- 1. Capturing Sankofa Oracle Library View ---")
run_lua(r"""
local master = reaper.GetMasterTrack(0)
reaper.TrackFX_SetOffline(master, 1, true)
reaper.TrackFX_SetOffline(master, 1, false)
reaper.TrackFX_SetParam(master, 1, 14, 1.0) -- View 1: Library
reaper.TrackFX_Show(master, 1, 3)
""")
time.sleep(0.8)
oracle_hwnd = find_window_by_substr("Sankofa")
capture_window(oracle_hwnd, "sankofa_library_view_24tracks.png")
run_lua(r"local master = reaper.GetMasterTrack(0); reaper.TrackFX_Show(master, 1, 2)")

# =========================================================================
# 2. DAMEI MIXING SUITE (Master FX 0) - TesseracT & heaving Presets
# =========================================================================
print("\n--- 2. Capturing Mixing Suite Presets ---")
run_lua(r"""
local master = reaper.GetMasterTrack(0)
reaper.TrackFX_SetOffline(master, 0, true)
reaper.TrackFX_SetOffline(master, 0, false)
reaper.TrackFX_SetParam(master, 0, 0, 0.0) -- Tab 0: Overview
reaper.TrackFX_SetParam(master, 0, 38, 22.0) -- Preset 22: Acle Kahney (TesseracT)
reaper.TrackFX_Show(master, 0, 3)
""")
time.sleep(0.8)
mixing_hwnd = find_window_by_substr("Mixing Suite")
capture_window(mixing_hwnd, "mixing_suite_tesseract_preset.png")

run_lua(r"""
local master = reaper.GetMasterTrack(0)
reaper.TrackFX_SetParam(master, 0, 38, 23.0) -- Preset 23: heaving. (carsick)
""")
time.sleep(0.5)
capture_window(mixing_hwnd, "mixing_suite_heaving_preset.png")

# Restore mixing suite to Kel Pinchin
run_lua(r"""
local master = reaper.GetMasterTrack(0)
reaper.TrackFX_SetParam(master, 0, 38, 6.0) -- Kel Pinchin
reaper.TrackFX_Show(master, 0, 2)
""")

# =========================================================================
# 3. DAMEI OZONE MASTERING SUITE - TesseracT Preset
# =========================================================================
print("\n--- 3. Capturing Ozone Mastering Suite ---")
run_lua(r"""
local master = reaper.GetMasterTrack(0)
local idx = reaper.TrackFX_AddByName(master, "Damei_OzoneSuite.jsfx", false, -1)
reaper.TrackFX_SetParam(master, idx, 32, 22.0) -- Preset 22: Acle Kahney
reaper.TrackFX_Show(master, idx, 3)
""")
time.sleep(0.8)
ozone_hwnd = find_window_by_substr("Ozone 12")
capture_window(ozone_hwnd, "mastering_suite_ozone_tesseract.png")
run_lua(r"""
local master = reaper.GetMasterTrack(0)
-- Find ozone and remove
local cnt = reaper.TrackFX_GetCount(master)
for i = cnt-1, 0, -1 do
    local ret, name = reaper.TrackFX_GetFXName(master, i)
    if string.find(name:lower(), "ozone") then
        reaper.TrackFX_Delete(master, i)
    end
end
""")

# =========================================================================
# 4. GUITAR SUITE (Track 51 / idx 50) - Producer Matrix & Overview
# =========================================================================
print("\n--- 4. Capturing Guitar Suite ---")
run_lua(r"""
local tr = reaper.GetTrack(0, 50)
reaper.TrackFX_SetOffline(tr, 0, true)
reaper.TrackFX_SetOffline(tr, 0, false)
reaper.TrackFX_SetParam(tr, 0, 0, 5.0) -- Tab 5: Producer Matrix
reaper.TrackFX_SetParam(tr, 0, 22, 17.0) -- Preset 17: Acle Kahney
reaper.TrackFX_Show(tr, 0, 3)
""")
time.sleep(0.8)
gtr_hwnd = find_window_by_substr("Guitar Bus")
capture_window(gtr_hwnd, "guitar_suite_producer_matrix.png")

run_lua(r"""
local tr = reaper.GetTrack(0, 50)
reaper.TrackFX_SetParam(tr, 0, 0, 0.0) -- Tab 0: Overview
""")
time.sleep(0.5)
capture_window(gtr_hwnd, "guitar_suite_tesseract_overview.png")

run_lua(r"""
local tr = reaper.GetTrack(0, 50)
reaper.TrackFX_SetParam(tr, 0, 22, 5.0) -- Restore Kel Pinchin
reaper.TrackFX_Show(tr, 0, 2)
""")

# =========================================================================
# 5. BASS SUITE (Track 69 / idx 68) - Producer Matrix
# =========================================================================
print("\n--- 5. Capturing Bass Suite ---")
run_lua(r"""
local tr = reaper.GetTrack(0, 68)
reaper.TrackFX_SetOffline(tr, 0, true)
reaper.TrackFX_SetOffline(tr, 0, false)
reaper.TrackFX_SetParam(tr, 0, 0, 6.0) -- Tab 6: Producer Matrix
reaper.TrackFX_SetParam(tr, 0, 19, 17.0) -- Preset 17: Acle Kahney
reaper.TrackFX_Show(tr, 0, 3)
""")
time.sleep(0.8)
bass_hwnd = find_window_by_substr("Bass Bus")
capture_window(bass_hwnd, "bass_suite_producer_matrix.png")
run_lua(r"""
local tr = reaper.GetTrack(0, 68)
reaper.TrackFX_SetParam(tr, 0, 19, 5.0) -- Restore Kel Pinchin
reaper.TrackFX_SetParam(tr, 0, 0, 0.0)
reaper.TrackFX_Show(tr, 0, 2)
""")

# =========================================================================
# 6. DRUM SUITE (Track 16 / idx 15) - Producer Matrix
# =========================================================================
print("\n--- 6. Capturing Drum Suite ---")
run_lua(r"""
local tr = reaper.GetTrack(0, 15)
reaper.TrackFX_SetOffline(tr, 0, true)
reaper.TrackFX_SetOffline(tr, 0, false)
reaper.TrackFX_SetParam(tr, 0, 0, 6.0) -- Tab 6: Producer Matrix
reaper.TrackFX_SetParam(tr, 0, 24, 17.0) -- Preset 17: Acle Kahney
reaper.TrackFX_Show(tr, 0, 3)
""")
time.sleep(0.8)
drum_hwnd = find_window_by_substr("Drum Bus")
capture_window(drum_hwnd, "drum_suite_producer_matrix.png")
run_lua(r"""
local tr = reaper.GetTrack(0, 15)
reaper.TrackFX_SetParam(tr, 0, 24, 5.0) -- Restore Kel Pinchin
reaper.TrackFX_SetParam(tr, 0, 0, 0.0)
reaper.TrackFX_Show(tr, 0, 2)
""")

# =========================================================================
# 7. VOCAL SUITE (Track 4 / idx 3) - Producer Matrix
# =========================================================================
print("\n--- 7. Capturing Vocal Suite ---")
run_lua(r"""
local tr = reaper.GetTrack(0, 3)
reaper.TrackFX_SetOffline(tr, 0, true)
reaper.TrackFX_SetOffline(tr, 0, false)
reaper.TrackFX_SetParam(tr, 0, 0, 5.0) -- Tab 5: Producer Matrix
reaper.TrackFX_SetParam(tr, 0, 17, 17.0) -- Preset 17: Acle Kahney
reaper.TrackFX_Show(tr, 0, 3)
""")
time.sleep(0.8)
vox_hwnd = find_window_by_substr("Vocal Sovereign")
capture_window(vox_hwnd, "vocal_suite_producer_matrix.png")
run_lua(r"""
local tr = reaper.GetTrack(0, 3)
reaper.TrackFX_SetParam(tr, 0, 17, 5.0) -- Restore Kel Pinchin
reaper.TrackFX_SetParam(tr, 0, 0, 0.0)
reaper.TrackFX_Show(tr, 0, 2)
""")

# =========================================================================
# 8. SYNTH SUITE (Track 40 / idx 39) - Producer Matrix & Codex
# =========================================================================
print("\n--- 8. Capturing Synth Suite ---")
run_lua(r"""
local tr = reaper.GetTrack(0, 39)
reaper.TrackFX_SetOffline(tr, 0, true)
reaper.TrackFX_SetOffline(tr, 0, false)
reaper.TrackFX_SetParam(tr, 0, 0, 6.0) -- Tab 6: Producer Matrix
reaper.TrackFX_SetParam(tr, 0, 14, 18.0) -- Preset 18: Acle Kahney
reaper.TrackFX_Show(tr, 0, 3)
""")
time.sleep(0.8)
syn_hwnd = find_window_by_substr("Synth Bus")
capture_window(syn_hwnd, "synth_suite_producer_matrix.png")
run_lua(r"""
local tr = reaper.GetTrack(0, 39)
reaper.TrackFX_SetParam(tr, 0, 14, 10.0) -- Restore Kel Pinchin
reaper.TrackFX_SetParam(tr, 0, 0, 0.0)
reaper.TrackFX_Show(tr, 0, 2)
""")

# Final check: restore Sankofa to View 0 (Assessment Matrix)
run_lua(r"""
local master = reaper.GetMasterTrack(0)
reaper.TrackFX_SetParam(master, 1, 14, 0.0)
""")
print("\nAll suites successfully captured and restored!")
