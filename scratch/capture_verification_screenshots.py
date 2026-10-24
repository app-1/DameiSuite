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

# 1. Capture Sankofa Oracle
print("Opening Sankofa Oracle...")
show_oracle = """
local master = reaper.GetMasterTrack(0)
reaper.TrackFX_Show(master, 1, 3) -- show floating window
return "Oracle shown"
"""
run_lua(show_oracle)
time.sleep(1.0)

hwnd_oracle = find_window_by_substr("Sankofa Oracle") or find_window_by_substr("Assessment")
print(f"Sankofa Oracle HWND: {hwnd_oracle}")
if hwnd_oracle:
    rect = wintypes.RECT()
    user32.GetWindowRect(hwnd_oracle, ctypes.byref(rect))
    user32.ShowWindow(hwnd_oracle, 9)
    user32.SetForegroundWindow(hwnd_oracle)
    time.sleep(0.5)
    bbox = (rect.left, rect.top, rect.right, rect.bottom)
    img = ImageGrab.grab(bbox=bbox, all_screens=True)
    out_path = os.path.join(artifact_dir, "sankofa_oracle_connected.png")
    img.save(out_path)
    print(f"Saved: {out_path}")

# 2. Capture Instrumental Bus Conclave
print("Opening Instrumental Bus Conclave...")
show_inst = """
local master = reaper.GetMasterTrack(0)
reaper.TrackFX_Show(master, 1, 2) -- hide oracle
local tr = reaper.GetTrack(0, 14)
reaper.TrackFX_Show(tr, 5, 3) -- show floating window
return "Inst shown"
"""
run_lua(show_inst)
time.sleep(1.0)

hwnd_inst = find_window_by_substr("Instrumental Bus") or find_window_by_substr("Conclave") or find_window_by_substr("Damei")
print(f"Instrumental Bus HWND: {hwnd_inst}")
if hwnd_inst:
    rect = wintypes.RECT()
    user32.GetWindowRect(hwnd_inst, ctypes.byref(rect))
    user32.ShowWindow(hwnd_inst, 9)
    user32.SetForegroundWindow(hwnd_inst)
    time.sleep(0.5)

    tabs = [
        (0, "inst_tab0_formatted.png"),
        (5, "inst_tab5_formatted.png"),
        (6, "inst_tab6_formatted.png"),
    ]

    for tab_idx, filename in tabs:
        set_tab_lua = f"""
        local tr = reaper.GetTrack(0, 14)
        reaper.TrackFX_SetParam(tr, 5, 0, {tab_idx})
        return "Tab {tab_idx} active"
        """
        run_lua(set_tab_lua)
        time.sleep(0.5)
        bbox = (rect.left, rect.top, rect.right, rect.bottom)
        img = ImageGrab.grab(bbox=bbox, all_screens=True)
        out_path = os.path.join(artifact_dir, filename)
        img.save(out_path)
        print(f"Captured Tab {tab_idx} -> {out_path}")

print("All screenshots successfully captured!")
