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

artifact_dir = r"C:\Users\pityy\.gemini\antigravity-ide\brain\3153c891-2778-44c6-b1f5-163098ac889d"
os.makedirs(artifact_dir, exist_ok=True)

# 1. Open FX floating window in REAPER
open_lua = """
local tr = reaper.GetTrack(0, 14)
reaper.TrackFX_Show(tr, 5, 3) -- show floating window
return "FX window opened"
"""
print(run_lua(open_lua))
time.sleep(1.0)

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

hwnd = find_window_by_substr("Instrumental Bus") or find_window_by_substr("Harmonic Crucible") or find_window_by_substr("Damei")
print(f"Found window HWND: {hwnd}")

if hwnd:
    rect = wintypes.RECT()
    user32.GetWindowRect(hwnd, ctypes.byref(rect))
    user32.ShowWindow(hwnd, 9) # SW_RESTORE
    user32.SetForegroundWindow(hwnd)
    time.sleep(0.5)

    tabs = [
        (0, "inst_tab0_overview.png"),
        (1, "inst_tab1_tonal_eq.png"),
        (2, "inst_tab2_bus_glue.png"),
        (3, "inst_tab3_crucible.png"),
        (4, "inst_tab4_stereo.png"),
        (5, "inst_tab5_pocket.png"),
        (6, "inst_tab6_producer_matrix.png"),
        (7, "inst_tab7_ear_candy.png"),
    ]

    for tab_idx, filename in tabs:
        # Switch tab in REAPER
        run_lua(f"""
        local tr = reaper.GetTrack(0, 14)
        reaper.TrackFX_SetParam(tr, 5, 0, {tab_idx})
        """)
        time.sleep(0.4)
        user32.GetWindowRect(hwnd, ctypes.byref(rect))
        bbox = (rect.left, rect.top, rect.right, rect.bottom)
        im = ImageGrab.grab(bbox=bbox)
        out_path = os.path.join(artifact_dir, filename)
        im.save(out_path)
        print(f"Captured Tab {tab_idx} -> {out_path} ({im.size[0]}x{im.size[1]})")

print("All screenshots completed.")
