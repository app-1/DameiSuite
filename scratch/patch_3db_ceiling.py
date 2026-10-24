import os, shutil

src_file = r'effects/Damei_InstrumentalSuite.jsfx'
reaper_file = r'C:\Users\pityy\AppData\Roaming\REAPER\Effects\Damei\Damei_InstrumentalSuite.jsfx'

with open(src_file, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update slider5 definition
old_s5 = 'slider5:0<0,1,1{Free Output, -6.0 dBTP Strict Pre-Master Lock}>-Headroom Guardian Mode'
new_s5 = 'slider5:0<0,2,1{-3.0 dBTP Staging Lock (Legacy Parity), -6.0 dBTP Pre-Master Lock, Free Uncapped Pass}>-Headroom Guardian Mode'
assert old_s5 in text, "Could not find old_s5"
text = text.replace(old_s5, new_s5, 1)

# 2. Update Peak Catcher threshold in audio loop
old_lim = '''  // Analog Soft-Diode Peak Catcher
  lim_th = 0.98; // -0.18 dBFS
  abs(final_l) > lim_th ? (
    final_l = sign(final_l) * (lim_th + (abs(final_l) - lim_th) / (1.0 + sqr(abs(final_l) - lim_th)));
  );
  abs(final_r) > lim_th ? (
    final_r = sign(final_r) * (lim_th + (abs(final_r) - lim_th) / (1.0 + sqr(abs(final_r) - lim_th)));
  );'''

new_lim = '''  // Analog Soft-Diode Peak Catcher (Strict -3.0 dBTP Legacy Ceiling Lock)
  lim_th = slider5 == 1 ? 0.501187 : (slider5 == 2 ? 0.98 : 0.707946); // 0 = -3.0 dBTP, 1 = -6.0 dBTP, 2 = Free Pass
  abs(final_l) > lim_th ? (
    final_l = sign(final_l) * (lim_th + (abs(final_l) - lim_th) / (1.0 + sqr((abs(final_l) - lim_th) * 4.0)));
  );
  abs(final_r) > lim_th ? (
    final_r = sign(final_r) * (lim_th + (abs(final_r) - lim_th) / (1.0 + sqr((abs(final_r) - lim_th) * 4.0)));
  );'''
assert old_lim in text, "Could not find old_lim"
text = text.replace(old_lim, new_lim, 1)

# 3. Update top banner readout (line 1491)
old_hdr_pill = 'slider5 ? gfx_drawstr("STRICT -6.0 dBTP") : gfx_drawstr("FREE CREST PASS");'
new_hdr_pill = 'slider5 == 1 ? gfx_drawstr("STRICT -6.0 dBTP") : (slider5 == 2 ? gfx_drawstr("FREE CREST PASS") : gfx_drawstr("-3.0 dBTP CEILING LOCK"));'
assert old_hdr_pill in text, "Could not find old_hdr_pill"
text = text.replace(old_hdr_pill, new_hdr_pill, 1)

# 4. Update Tab 5 Ceiling Guardian text
old_t5_guard = 'slider5 ? "-6.0 dBTP Strict" : "Free Crest Pass"'
new_t5_guard = 'slider5 == 1 ? "-6.0 dBTP Strict" : (slider5 == 2 ? "Free Crest Pass" : "-3.0 dBTP Strict Lock")'
assert old_t5_guard in text, "Could not find old_t5_guard"
text = text.replace(old_t5_guard, new_t5_guard, 1)

with open(src_file, 'w', encoding='utf-8') as f:
    f.write(text)

shutil.copy2(src_file, reaper_file)
print("Successfully patched -3.0 dBTP ceiling guardian into Instrumental Suite!")
