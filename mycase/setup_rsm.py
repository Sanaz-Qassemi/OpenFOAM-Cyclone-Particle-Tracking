import os, re

# Find latest reconstructed time folder
times = [d for d in os.listdir('.') if re.match(r'^\d+(\.\d+)?$', d) and d != '0']
latest_t = sorted(times, key=float)[-1]

# Read ASCII template from 0/k.air
with open(os.path.join('0', 'k.air'), 'r', errors='ignore') as f:
    k_text = f.read()

m_int = re.search(r'internalField\s+uniform\s+([0-9.eE+-]+);', k_text)
k_val = float(m_int.group(1)) if m_int else 0.5
r_diag = (2.0 / 3.0) * k_val

bf_start = k_text.find('boundaryField')
bf_text = k_text[bf_start:]

r_header = f"""FoamFile
{{
    format      ascii;
    class       volSymmTensorField;
    location    "{latest_t}";
    object      R.air;
}}

dimensions      [0 2 -2 0 0 0 0];

internalField   uniform ({r_diag:.6f} 0 0 {r_diag:.6f} 0 {r_diag:.6f});

"""

bf_r = re.sub(r'value\s+uniform\s+[0-9.eE+-]+;', f'value           uniform ({r_diag:.6f} 0 0 {r_diag:.6f} 0 {r_diag:.6f});', bf_text)

with open(os.path.join(latest_t, 'R.air'), 'w') as f:
    f.write(r_header + bf_r)

with open(os.path.join('0', 'R.air'), 'w') as f:
    f.write(r_header.replace(f'"{latest_t}"', '"0"') + bf_r)

print(f"Successfully generated ASCII R.air in {latest_t}/ and 0/")
