"""Synth Bus Nebula: Ear-Candy Director palettes + patcher (reuses the shared kernel from gen_candy)."""
import gen_candy as gc

SYN_PRODUCERS = ['Jordan Fish', 'Dan Braunstein', 'Buster Odeholm', 'George Lever', 'Zakk Cervini',
                 'Joey Sturgis', 'Mick Gordon', 'Lance Prenc', 'Scott Seigel', 'Jonathan Dolese',
                 'Kel Pinchin', 'Sam Guaiana', 'Forrester Savell', 'Jens Bogren', 'Nolly Getgood',
                 'Will Putney', 'Sam Bassal', 'Henrik Udd']

NAMES_S = ['Arp Throw', 'Reverse Swell', 'Dotted Echo', 'Slapback', 'Plate Tail', 'Filter Rise',
           'Gate Chop', 'Radio Choke', 'Sparkle Air', 'Octave Shimmer', 'Sub-Octave Weight', 'Pitch Dive',
           'Grit Layer', 'Haas Widener', 'Tremolo Pulse', 'Filter Sweep']
HINTS_S = ['last arp phrase thrown ping-pong into the drop', 'reversed synth swell into the drop',
           'dotted echo blooms in gaps after phrases', 'short slap on sparse synth lines',
           'plate tail on big chord ring-outs', 'high-pass rise across the last bar',
           '16th gate chop on the final beat', 'bandpass choke before drops / bridge lo-fi',
           'high-band sparkle in loud choruses', 'octave shimmer late in loud choruses',
           'octave-down weight on breakdowns / peaks', 'pitch dive over the last 0.4 s of a section',
           'parallel grit when energy peaks', 'Haas widen in choruses',
           'tempo-synced tremolo on sparse pads', 'slow filter sweep through verses and builds']

# (tricks, signature, density, gain) in the Synth slider15 order
SYN = [
 (['RISE', 'GHOSTUP', 'BLOOM', 'WIDE', 'CHOP', 'ECHO'], 'RISE', 2, 1.05),
 (['BLOOM', 'ECHO', 'HALL', 'WIDE', 'GHOSTUP', 'BREATH'], 'BLOOM', 1, 0.90),
 (['GHOSTDN', 'DIVE', 'CHOP', 'GRIT', 'TELE'], 'GHOSTDN', 1, 1.00),
 (['BLOOM', 'GHOSTUP', 'SWEEP', 'TREM', 'HALL', 'ECHO'], 'GHOSTUP', 2, 1.05),
 (['RISE', 'CHOP', 'WIDE', 'SLAP', 'BREATH', 'TELE'], 'RISE', 2, 1.00),
 (['CHOP', 'RISE', 'GRIT', 'WIDE', 'THROW', 'TELE'], 'CHOP', 2, 1.00),
 (['GRIT', 'GHOSTDN', 'DIVE', 'CHOP', 'SWEEP', 'TELE'], 'GRIT', 2, 1.00),
 (['GHOSTDN', 'CHOP', 'DIVE', 'GRIT', 'RISE'], 'GHOSTDN', 2, 1.00),
 (['DIVE', 'TELE', 'GRIT', 'GHOSTDN', 'CHOP', 'SWEEP'], 'DIVE', 2, 1.00),
 (['TELE', 'GRIT', 'SWEEP', 'DIVE', 'ECHO', 'TREM'], 'TELE', 2, 1.00),
 (['GHOSTUP', 'BLOOM', 'WIDE', 'SWEEP', 'ECHO', 'RISE'], 'GHOSTUP', 2, 1.00),
 (['RISE', 'THROW', 'WIDE', 'BREATH', 'SLAP', 'CHOP'], 'RISE', 2, 0.95),
 (['BLOOM', 'HALL', 'TREM', 'SWEEP', 'GHOSTUP', 'ECHO'], 'TREM', 2, 1.00),
 (['HALL', 'BLOOM', 'WIDE', 'SWEEP', 'GHOSTDN'], 'HALL', 1, 0.90),
 (['SWEEP', 'ECHO', 'GHOSTUP', 'TREM', 'WIDE', 'BLOOM'], 'SWEEP', 2, 1.00),
 (['GHOSTDN', 'DIVE', 'CHOP', 'GRIT', 'TELE'], 'GRIT', 1, 1.00),
 (['BLOOM', 'RISE', 'SWEEP', 'WIDE', 'GHOSTUP', 'SLAP'], 'WIDE', 2, 1.00),
 (['RISE', 'BLOOM', 'BREATH', 'WIDE', 'ECHO', 'SLAP'], 'BREATH', 1, 0.95),
]

TIPS_S = [
 ["Electronic lift: filter rise across the pre-chorus bar.",
  "Octave shimmer on the synth hook, late in loud choruses.",
  "Gate chop on the last beat, then a wide open drop.",
  "Reverse swell blends under the chorus entry. Barely there."],
 ["Dreamy and wide: reverse swell into each chorus.",
  "Dotted echo blooms only in the gaps between synth phrases.",
  "Plate tail on big chord ring-outs; sparkle air on the hook.",
  "Keep verses close and dry so the chorus feels huge."],
 ["Dark weight: sub-octave shadow under breakdown synths.",
  "Pitch dive over the last 0.4 s before a heavy drop.",
  "Gate chop on the final beat, then silence, then impact.",
  "No wash: keep ambience out of the heavy parts."],
 ["Ritual atmosphere: octave shimmer late in big sections.",
  "Slow filter sweep and gentle tremolo on the pad layers.",
  "Reverse swell plus long plate tail into the biggest hook.",
  "Dotted echo blooms in the gaps, never over the vocal."],
 ["Pop-punk lift: filter rise into the chorus, short and bright.",
  "Gate chop before the drop, snap back to full range.",
  "Haas widener opens the chorus synths for gloss.",
  "Short slapback on sparse verse synths."],
 ["Electronicore energy: gate chop on the last beat.",
  "Filter rise on the pre-chorus; arp throw into the drop.",
  "Grit layer when the synth peaks above the section average.",
  "Widener on the chorus lead; verses stay tight."],
 ["Industrial grit: parallel grit layer when the synth peaks.",
  "Sub-octave weight and pitch dive on the heavy hits.",
  "Gate chop before the drop; slow sweep through the build.",
  "Radio choke on the last bar, fully open on the downbeat."],
 ["Aggressive and tight: sub-octave weight on breakdown hits.",
  "Gate chop on the final beat, dry everywhere else.",
  "Pitch dive tails at section ends, short and mean.",
  "Grit layer at riff peaks keeps the synths hostile."],
 ["Dark and hostile: pitch dive on the last 0.4 s of a section.",
  "Radio choke before the drop; lo-fi texture on the bridge.",
  "Grit layer at peaks, sub-octave weight on heavy hits.",
  "Slow filter sweep through the build for cold tension."],
 ["Gothic grit: radio choke on the bridge for lo-fi texture.",
  "Slow filter sweep and tremolo pulse on the pads.",
  "Grit layer at peaks; dotted echo at riff stops.",
  "Pitch dive into the drop, very short."],
 ["Ethereal tech: octave shimmer rises late in big choruses.",
  "Reverse swell into the hook plus dotted echo in the gaps.",
  "Haas widener gives the synth lead a halo.",
  "Slow filter sweep on the clean pads."],
 ["Melodic hardcore: filter rise into the chorus.",
  "Arp throw into the drop, slapback on sparse parts.",
  "Widener opens the chorus; breath air for sheen.",
  "Gate chop before the heaviest section."],
 ["Progressive space: tremolo pulse and slow sweep on the pads.",
  "Reverse swell into the big sections, very long and soft.",
  "Plate tail on ring-outs; octave shimmer very late.",
  "Dotted echo blooms between phrases, never over the groove."],
 ["Dense and natural: plate tail on big ring-outs only.",
  "Haas widener in choruses for size, nothing flashy.",
  "One reverse swell into the biggest section.",
  "Slow filter sweep in verses adds quiet movement."],
 ["Hypnotic motion: slow filter sweep through every section.",
  "Dotted echo in the gaps; octave shimmer late and quiet.",
  "Tremolo pulse on pads for polyrhythmic shimmer.",
  "Widener on the lead for width, never on the sub."],
 ["Brutal precision: pitch dive and gate chop before the hit.",
  "Sub-octave weight under breakdown synths, dry elsewhere.",
  "Radio choke before the drop; no ambience.",
  "Grit layer only when the synth peaks."],
 ["Oceanic build: reverse swell and filter rise into the chorus.",
  "Slow sweep through the verse; widener on the chorus.",
  "Octave shimmer late in loud sections.",
  "Short slapback on sparse parts."],
 ["Alt-rock polish: filter rise into the chorus, widener on top.",
  "Reverse swell into the hook, dotted echo in the gaps.",
  "Breath air makes the chorus synths glossy.",
  "Short slapback on sparse verse parts."],
]
for r in TIPS_S:
    assert len(r) == 4 and all(len(x) <= 66 for x in r), r
assert len(TIPS_S) == len(SYN) == len(SYN_PRODUCERS) == 18


def patch_synth():
    P = gc.DIR + r'\Damei_SynthSuite.jsfx'
    t, crlf = gc.rd(P)
    assert 'EAR-CANDY DIRECTOR BEGIN' not in t, 'already patched; restore backup first'
    sfx = dict(DIR='slider28', SUB='slider29', MASK='slider30', FOLLOW='slider31', PROD='slider15')
    kern = gc.kernel(sfx, NAMES_S, TIPS_S, SYN, 0xFFFF, 's', prods=SYN_PRODUCERS, hints=HINTS_S)
    gui = gc.GUI_TEMPLATE.replace('min(16, ', 'min(17, ').replace('(dg_pbi + 16) % 17', '(dg_pbi + 17) % 18') \
        .replace('(dg_pbi + 1) % 17', '(dg_pbi + 1) % 18')
    for k, v in sfx.items():
        gui = gui.replace('@@%s@@' % k, v)
    assert '% 17' not in gui

    defmask = gc.mask_of(SYN[0][0])
    t = gc.sub1(t, 'slider1:0<0,5,1{Nebula', 'slider1:0<0,6,1{Nebula')
    t = gc.sub1(t, ',Producer Matrix & Bridge Codex}>', ',Producer Matrix & Bridge Codex,Ear-Candy Director}>')
    t = gc.sub1(t, 'slider27:1<0,1,1{Off,On}>-Matrix Trim (applies Assessment Matrix auto-correct lane)\n',
                'slider27:1<0,1,1{Off,On}>-Matrix Trim (applies Assessment Matrix auto-correct lane)\n'
                'slider28:1<0,1,1{Classic (Off),Ear-Candy Director (Region + Energy Aware)}>-Ear-Candy Director\n'
                'slider29:40<0,100,1>-Ear-Candy Amount (%%)\n'
                'slider30:%d<0,65535,1>-Ear-Candy Trick Palette (bitmask)\n'
                'slider31:1<0,1,1{Manual Palette,Follow Producer Preset}>-Ear-Candy Palette Follows Producer\n' % defmask)
    t = gc.sub1(t, 'function apply_synth_preset(p_idx) (\n  slider15 = p_idx;\n',
                kern + '\nfunction apply_synth_preset(p_idx) (\n  slider15 = p_idx;\n  dk_preset_changed(p_idx);\n')
    t = gc.sub1(t, '// ===== MATRIX TRIM END =====\n\n@slider\n',
                '// ===== MATRIX TRIM END =====\n\ndk_boot = 0;\n\n@slider\n')
    t = gc.sub1(t, '  mtrim_block();\n\n@sample',
                '  (slider28 == 1) ? ( dk_block(); ) : ( dk_off(); );\n\n  mtrim_block();\n\n@sample')
    t = gc.sub1(t, 'spl0 = out_l;\nspl1 = out_r;\n\n// Metering & Scope Buffers',
                '// Ear-Candy Director (region + energy aware producer tricks)\n'
                '(slider28 == 1) ? ( dk_process(); );\n\n'
                'spl0 = out_l;\nspl1 = out_r;\n\n// Metering & Scope Buffers')
    t = gc.sub1(t, 'num_tabs = 6;', 'num_tabs = 7;')
    t = gc.sub1(t, 't_label = "PRODUCER CODEX";',
                'ti == 5 ? t_label = "PRODUCER CODEX" :\nt_label = "EAR-CANDY";')
    # gui function + tab 6 body before the Tab-5 banner
    a = t.index('// TAB 5: PRODUCER CODEX')
    a = t.rfind('// ====', 0, a)
    t = t[:a] + gui + '\nslider1 == 6 ? (\n  dk_gui(p_x, p_y, p_w, p_h, 1.00, 0.72, 0.02);\n);\n\n' + t[a:]
    gc.wr(P, t, crlf)
    print('synth ok')
