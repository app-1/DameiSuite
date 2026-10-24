import re

suites = {
    'Guitar': (r'C:\Dev\DameiSuite\effects\Damei_GuitarSuite.jsfx', 'slider23'),
    'Bass': (r'C:\Dev\DameiSuite\effects\Damei_BassSuite.jsfx', 'slider20'),
    'Drum': (r'C:\Dev\DameiSuite\effects\Damei_DrumSuite.jsfx', 'slider25'),
    'Vocal': (r'C:\Dev\DameiSuite\effects\Damei_VocalSuite.jsfx', 'slider18'),
    'Synth': (r'C:\Dev\DameiSuite\effects\Damei_SynthSuite.jsfx', 'slider15'),
    'Mixing': (r'C:\Dev\DameiSuite\effects\Damei_MixingSuite.jsfx', 'slider39'),
}

for name, (path, slider) in suites.items():
    code = open(path, encoding='utf-8').read()
    print(f"=== {name} ({slider}) ===")
    # Find slider declaration
    for line in code.splitlines():
        if line.startswith(slider + ':'):
            print("Declaration:", line[:120])
    # Find gfx_showmenu or preset display
    for i, line in enumerate(code.splitlines()):
        if 'gfx_showmenu' in line or (slider in line and 'gfx_' in line) or 'p_title' in line or 'p_lbl' in line:
            print(f"  Line {i+1}: {line[:120]}")
