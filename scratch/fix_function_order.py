import re, shutil

# 1. Fix Damei_InstrumentalSuite.jsfx
with open(r"c:\Dev\DameiSuite\scratch\upgrade_instrumental_suite.py", "r", encoding="utf-8") as f:
    text = f.read()

p1 = text.find('function apply_producer_preset(idx)')
p2 = text.find('function update_filters()')
p3 = text.find('update_filters();\n\n@slider')

apply_fn = text[p1:p2]
update_fn = text[p2:p3]

new_text = text[:p1] + update_fn + "\n\n" + apply_fn + text[p3:]

with open(r"c:\Dev\DameiSuite\scratch\upgrade_instrumental_suite.py", "w", encoding="utf-8") as f:
    f.write(new_text)

# 2. Fix Damei_VocalBus.jsfx
with open(r"c:\Dev\DameiSuite\scratch\upgrade_vocal_bus.py", "r", encoding="utf-8") as f:
    text_v = f.read()

vp1 = text_v.find('function apply_producer_preset(idx)')
vp2 = text_v.find('function update_vocal_filters()')
vp3 = text_v.find('update_vocal_filters();\n\n@slider')

v_apply_fn = text_v[vp1:vp2]
v_update_fn = text_v[vp2:vp3]

new_text_v = text_v[:vp1] + v_update_fn + "\n\n" + v_apply_fn + text_v[vp3:]

with open(r"c:\Dev\DameiSuite\scratch\upgrade_vocal_bus.py", "w", encoding="utf-8") as f:
    f.write(new_text_v)

print("Both builder scripts updated with update_filters declared BEFORE apply_producer_preset.")
