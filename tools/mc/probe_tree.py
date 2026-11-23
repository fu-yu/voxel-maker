"""Grow trees on the local check server and print where their logs and leaves are.
Usage: python3 -I tools/mc/probe_tree.py <feature> <count> <radius> <height> [x0]
  e.g. python3 -I tools/mc/probe_tree.py minecraft:mega_spruce 3 7 32
Needs the server in the dev environment running with RCON (see tools/mc/README.md).
Each layer is printed from the top: rows run along z, '#' is a log, 'o' a leaf, '.' empty."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rcon import Rcon
r = Rcon(); feat = sys.argv[1]; n = int(sys.argv[2]); R = int(sys.argv[3]); H = int(sys.argv[4])
X0 = int(sys.argv[5]) if len(sys.argv) > 5 else 60000
Z = X0; Y = -60
for k in range(n):
    x = X0 + k * (2 * R + 12)
    r.cmd(f'forceload add {x-R-2} {Z-R-2} {x+R+2} {Z+R+2}')
    print(r.cmd(f'place feature {feat} {x} {Y} {Z}')[:80])
    rows = []
    for dy in range(H):
        lay = []
        for dz in range(-R, R + 1):
            s = ''
            for dx in range(-R, R + 1):
                p = f'{x+dx} {Y+dy} {Z+dz}'
                if 'passed' in r.cmd(f'execute if block {p} #minecraft:logs'): s += '#'
                elif 'passed' in r.cmd(f'execute if block {p} #minecraft:leaves'): s += 'o'
                else: s += '.'
            lay.append(s)
        rows.append(lay)
    while rows and all(set(l) == {'.'} for l in rows[-1]): rows.pop()
    print(f'--- tree {k}: height {len(rows)}')
    for dy in reversed(range(len(rows))): print(f'{dy:2d} ' + ' '.join(rows[dy]))
