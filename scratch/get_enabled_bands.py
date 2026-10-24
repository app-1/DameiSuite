import json

with open(r'c:\Dev\DameiSuite\scratch\tr15_legacy_chain_dump.json') as f:
    data = json.load(f)

# 1. Britson Buss
print("================== BRITSON BUSS ==================")
for p in data[0]['params']:
    print(f"  {p['name']:25s} = {p['fmt']} ({p['val']})")

# 2. TB Equalizer Pro
print("\n================== TB EQUALIZER PRO ==================")
tb = data[1]['params']
enabled_bands = []
for p in tb:
    if p['name'].startswith('Enable') and p['val'] == 1.0:
        b = p['name'].replace('Enable', '')
        enabled_bands.append(b)

print(f"Enabled Bands: {enabled_bands}")
for b in enabled_bands:
    print(f"\n--- Band {b} ---")
    for p in tb:
        if p['name'].endswith(b) and any(k in p['name'].lower() for k in ['freq', 'gain', 'q', 'type', 'order']):
            print(f"   {p['name']:20s} = {p['fmt']} ({p['val']})")

# Also check output gain or dynamics on TB Equalizer
for p in tb[:15]:
    print(f"  GLOBAL: {p['name']:20s} = {p['fmt']} ({p['val']})")

# 3. DeeGain
print("\n================== DEEGAIN ==================")
for p in data[2]['params']:
    print(f"  {p['name']:25s} = {p['fmt']} ({p['val']})")

# 4. Bass Manager
print("\n================== BASS MANAGER ==================")
for p in data[3]['params']:
    print(f"  {p['name']:25s} = {p['fmt']} ({p['val']})")

# 5. BUSTERse
print("\n================== BUSTERse ==================")
for p in data[4]['params']:
    print(f"  {p['name']:25s} = {p['fmt']} ({p['val']})")
