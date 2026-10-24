import re, glob, os
used = {}
for f in glob.glob(r'c:\Dev\DameiSuite\effects\*.jsfx') + glob.glob(r'c:\Dev\DameiSuite\scripts\*.lua'):
    txt = open(f, encoding='utf-8', errors='ignore').read()
    for m in re.finditer(r'gmem(?:_read|_write)?[\[\(]\s*(\d{2,4})', txt):
        used.setdefault(int(m.group(1)), set()).add(os.path.basename(f))
for lo, hi in [(800, 899), (1000, 1199)]:
    print(f'--- {lo}-{hi}')
    for k in sorted(used):
        if lo <= k <= hi:
            print(k, sorted(used[k])[:4])
