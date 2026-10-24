# build_flagship_bus_suites_v4.py
# Systematically generates Damei_InstrumentalSuite.jsfx and Damei_VocalBus.jsfx
# with strictly confined SIFAM analog meters, 6-band exact ToneBoosters EQ,
# HuggingFace AI Assistant architecture, and rich live visualizations.

import os, shutil

inst_target = r"c:\Dev\DameiSuite\effects\Damei_InstrumentalSuite.jsfx"
inst_reaper = r"C:\Users\pityy\AppData\Roaming\REAPER\Effects\Damei\Damei_InstrumentalSuite.jsfx"

vocal_target = r"c:\Dev\DameiSuite\effects\Damei_VocalBus.jsfx"
vocal_reaper = r"C:\Users\pityy\AppData\Roaming\REAPER\Effects\Damei\Damei_VocalBus.jsfx"

print("Building flagship bus suites v4...")
