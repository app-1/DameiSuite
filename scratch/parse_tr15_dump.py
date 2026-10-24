import json

with open(r'c:\Dev\DameiSuite\scratch\tr15_legacy_chain_dump.json') as f:
    data = json.load(f)

for fx in data:
    idx = fx['fx_idx']
    name = fx['fx_name']
    print("=" * 60)
    print(f"FX {idx}: {name} (Enabled: {fx['enabled']})")
    print("=" * 60)
    
    if idx == 0: # Britson Buss
        for p in fx['params']:
            print(f"  {p['name']:25s} = {p['fmt']} ({p['val']})")
            
    elif idx == 1: # TB Equalizer Pro
        # Program name and non-zero parameters
        for p in fx['params']:
            val = p['val']
            pname = p['name']
            if pname == 'Program':
                print(f"  PRESET/PROGRAM: {p['fmt']} ({val})")
            elif val != 0.0 and val != 0.5 and val != 1.0:
                print(f"  {pname:25s} = {p['fmt']} ({val})")
            elif any(k in pname.lower() for k in ['gain', 'freq', 'q', 'type', 'order', 'solo', 'mute']) and val != 0.0:
                print(f"  {pname:25s} = {p['fmt']} ({val})")
                
    elif idx == 2: # DeeGain
        for p in fx['params']:
            print(f"  {p['name']:25s} = {p['fmt']} ({p['val']})")
            
    elif idx == 3: # Bass Manager
        for p in fx['params']:
            print(f"  {p['name']:25s} = {p['fmt']} ({p['val']})")
            
    elif idx == 4: # BUSTERse
        for p in fx['params']:
            print(f"  {p['name']:25s} = {p['fmt']} ({p['val']})")
