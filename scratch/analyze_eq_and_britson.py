import json

with open(r'c:\Dev\DameiSuite\scratch\tr15_legacy_chain_dump.json') as f:
    data = json.load(f)

print("=== FX 0: Britson Buss ===")
for p in data[0]['params']:
    print(f"  {p['name']:25s} = {p['fmt']} ({p['val']})")

print("\n=== FX 1: TB Equalizer Pro Active Bands ===")
tb = data[1]['params']
for p in tb:
    name = p['name']
    val = p['val']
    fmt = p['fmt']
    if 'gain' in name.lower() and abs(val - 0.5) > 0.001:
        print(f"  {name:25s} = {fmt} ({val})")
    elif 'shape' in name.lower() or 'type' in name.lower() or 'order' in name.lower():
        if val != 0.0:
            print(f"  {name:25s} = {fmt} ({val})")
    elif 'program' in name.lower():
        print(f"  {name:25s} = {fmt} ({val})")

# Print all bands that have non-zero gain or active filter
bands_with_gain = set()
for p in tb:
    if 'gain' in p['name'].lower() and abs(p['val'] - 0.5) > 0.001:
        # extract band number
        digits = ''.join(c for c in p['name'] if c.isdigit())
        if digits:
            bands_with_gain.add(digits)

print("\nBands with active gain adjustments:", sorted(list(bands_with_gain), key=int))
for b in sorted(list(bands_with_gain), key=int):
    print(f"\n--- Band {b} ---")
    for p in tb:
        if p['name'].endswith(b) or p['name'].startswith(f"Band{b}") or p['name'].startswith(f"Type{b}") or p['name'].startswith(f"Frequency{b}") or p['name'].startswith(f"Gain{b}") or p['name'].startswith(f"Q{b}") or p['name'].startswith(f"Order{b}") or p['name'].startswith(f"Shape{b}"):
            if not any(c.isdigit() and c != b for c in p['name'].replace(b, '')):
                print(f"   {p['name']:20s} = {p['fmt']} ({p['val']})")
