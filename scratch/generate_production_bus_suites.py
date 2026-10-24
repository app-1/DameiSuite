import os

def generate_suites():
    # 1. Generate Instrumental Bus Alchemist
    inst_path = r"c:\Dev\DameiSuite\effects\Damei_InstrumentalSuite.jsfx"
    with open(r"c:\Dev\DameiSuite\scratch\build_instrumental_suite_v3.py", "r", encoding="utf-8") as f:
        inst_script = f.read()
    
    # We will refine the header code in both scripts to include the center preset stepper and responsive geometry
    with open(r"c:\Dev\DameiSuite\scratch\patch_bus_suites_full.py", "w", encoding="utf-8") as f:
        f.write('''# Script to build final production Instrumental and Vocal Bus Suites
import os

inst_path = r"c:\\Dev\\DameiSuite\\effects\\Damei_InstrumentalSuite.jsfx"
vocal_path = r"c:\\Dev\\DameiSuite\\effects\\Damei_VocalBus.jsfx"

# Read current templates
with open(r"c:\\Dev\\DameiSuite\\effects\\Damei_InstrumentalSuite.jsfx", "r", encoding="utf-8") as f:
    inst_code = f.read()

with open(r"c:\\Dev\\DameiSuite\\effects\\Damei_VocalBus.jsfx", "r", encoding="utf-8") as f:
    vocal_code = f.read()

print("Read current files successfully.")
''')

generate_suites()
print("Preparation script created.")
