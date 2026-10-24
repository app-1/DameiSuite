import re, glob, os
roots = [r'c:\Dev\DameiSuite', r'c:\Dev\DameiAPI', os.path.expandvars(r'%APPDATA%\REAPER\Effects'), os.path.expandvars(r'%APPDATA%\REAPER\Scripts')]
used = set()
for r in roots:
    for ext in ('jsfx', 'lua', 'py', 'js'):
        for f in glob.glob(os.path.join(r, '**', '*.' + ext), recursive=True):
            if 'backup' in f.lower() or 'scratch' in f.lower():
                continue
            try:
                txt = open(f, encoding='utf-8', errors='ignore').read()
            except Exception:
                continue
            for m in re.finditer(r'gmem(?:_read|_write)?\s*[\[\(]\s*(\d{1,5})', txt):
                used.add(int(m.group(1)))
            for m in re.finditer(r'gmem\[\s*(\d+)\s*\+', txt):
                used.add(int(m.group(1)))
print('max used:', max(used))
above = sorted(k for k in used if k >= 1167)
print('used >=1167:', above)
for lo in range(1200, 5000, 100):
    if not any(lo <= k < lo + 100 for k in used):
        print('free 100-block starts at', lo)
        break
