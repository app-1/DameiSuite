"""UI standard: no gfx font below 11 px in the Damei suites (10 / 10.5 -> 11). Idempotent, backs up first."""
import os, re, shutil
D = r"C:\Dev\DameiAPI\reaper_scripts"
BK = os.path.join(D, "backups_preui")
os.makedirs(BK, exist_ok=True)
FILES = ["Damei_SynthSuite.jsfx", "Damei_MixingSuite.jsfx", "Damei_GuitarSuite.jsfx",
         "Damei_DrumSuite.jsfx", "Damei_BassSuite.jsfx", "Damei_VocalSuite.jsfx",
         "Damei_DevastatorSuite.jsfx", "Damei_AssessmentMatrix.jsfx"]
R = re.compile(r'(gfx_setfont\(\s*\d+\s*,\s*"[^"]*"\s*,\s*)(10(?:\.\d)?|[1-9](?:\.\d)?)(\s*[,)])')
for fn in FILES:
    p = os.path.join(D, fn)
    raw = open(p, encoding="utf-8", newline="").read()
    new, n = R.subn(lambda m: m.group(1) + "11" + m.group(3), raw)
    if n:
        shutil.copyfile(p, os.path.join(BK, fn))
        open(p, "w", encoding="utf-8", newline="").write(new)
    print(fn, n)
