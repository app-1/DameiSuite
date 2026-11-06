import os

paths = [
    r"c:\Dev\DameiSuite\effects\Damei_DrumAssessment.jsfx",
    os.path.expandvars(r"%APPDATA%\REAPER\Effects\Damei\Damei_DrumAssessment.jsfx")
]

for p in paths:
    if os.path.exists(p):
        with open(p, "rb") as f:
            raw = f.read()
        
        # Replace common broken utf-8 sequences
        clean = raw.replace(b"\xef\xbf\xbd?\xef\xbf\xbd", b">> ")
        clean = clean.replace(b"\xc3\xa2\xe2\x80\xa2", b">> ")
        clean = clean.replace(b"\xe2\x80\xa2", b">> ")
        
        # Decode as utf-8 ignore
        text = clean.decode("utf-8", errors="ignore")
        # Replace any leftover ? or 
        text = text.replace("?", ">> ")
        text = text.replace("", ">")
        
        with open(p, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Cleaned typography in {p}")
