import os, shutil

effects_src = r"c:\Dev\DameiSuite\effects"
effects_dest = os.path.expandvars(r"%APPDATA%\REAPER\Effects\Damei")
ini_path = os.path.expandvars(r"%APPDATA%\REAPER\reaper-jsfx.ini")

os.makedirs(effects_dest, exist_ok=True)

# 1. Copy CymbalClarity
shutil.copy2(os.path.join(effects_src, "Damei_CymbalClarity.jsfx"), os.path.join(effects_dest, "Damei_CymbalClarity.jsfx"))
print("Copied Damei_CymbalClarity.jsfx")

# 2. Copy RoomSculptor
shutil.copy2(os.path.join(effects_src, "Damei_RoomSculptor.jsfx"), os.path.join(effects_dest, "Damei_RoomSculptor.jsfx"))
print("Copied Damei_RoomSculptor.jsfx")

# 3. Update reaper-jsfx.ini
with open(ini_path, "r", encoding="utf-8", errors="ignore") as f:
    ini_content = f.read()

entries = [
    'NAME Damei/Damei_CymbalClarity.jsfx "JS: Damei Atumpan CymbalClarity (Resonance Tamer & Air Leveller)"\n',
    'NAME Damei/Damei_RoomSculptor.jsfx "JS: Damei Atumpan RoomSculptor (Acoustic Space Inflator & Smash Compressor)"\n'
]

modified = False
for entry in entries:
    fname = entry.split()[1]
    if fname not in ini_content:
        ini_content += entry
        modified = True
        print(f"Registered {fname} in reaper-jsfx.ini")

if modified:
    with open(ini_path, "w", encoding="utf-8") as f:
        f.write(ini_content)
    print("reaper-jsfx.ini updated successfully!")
else:
    print("reaper-jsfx.ini already contains entries.")
