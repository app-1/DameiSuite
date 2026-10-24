import os, glob, re

effects = glob.glob(r'c:\Dev\DameiSuite\effects\*.jsfx')
for ef in sorted(effects):
    name = os.path.basename(ef)
    content = open(ef, 'r', encoding='utf-8').read()
    # strip strings and comments
    code_no_str = re.sub(r'"[^"\\]*(?:\\.[^"\\]*)*"', '', content)
    code_no_com = re.sub(r'//.*', '', code_no_str)
    p_open = code_no_com.count('(')
    p_close = code_no_com.count(')')
    b_open = code_no_com.count('[')
    b_close = code_no_com.count(']')
    c_open = code_no_com.count('{')
    c_close = code_no_com.count('}')
    p_match = 'OK' if p_open == p_close else f'MISMATCH ({p_open} vs {p_close})'
    b_match = 'OK' if b_open == b_close else f'MISMATCH ({b_open} vs {b_close})'
    c_match = 'OK' if c_open == c_close else f'MISMATCH ({c_open} vs {c_close})'
    print(f'{name:32} ( ): {p_match:15} [ ]: {b_match:15} {{ }}: {c_match:15}')
