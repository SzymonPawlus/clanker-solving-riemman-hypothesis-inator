#!/bin/sh
# Reproduces every number in attacks/r5-exhaust4/README.md.  ~12 min, one core.
set -e
cd "$(dirname "$0")"
mkdir -p out

echo "=== 0. subdivision test (children closed, covering, contained) ==="
python3 - <<'PY'
import random
from eo4 import geom
def inside(pt, v):
    def cr(o,a,b): return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
    s=[cr(v[i],v[(i+1)%3],pt) for i in range(3)]
    return all(x>=0 for x in s) or all(x<=0 for x in s)
random.seed(20260824); bad=0
for cell in [(0,0,0,0),(1,0,1,0),(1,1,0,0),(2,1,1,1),(3,0,2,3)]:
    ks=geom.children(cell); pv=[(a*2,b*2) for a,b in geom.cell_vertices(cell)]
    for k in ks:
        for w in geom.cell_vertices(k):
            if not inside(w,pv): bad+=1
    for _ in range(3000):
        r1,r2=random.random(),random.random()
        if r1+r2>1: r1,r2=1-r1,1-r2
        p=(pv[0][0]+r1*(pv[1][0]-pv[0][0])+r2*(pv[2][0]-pv[0][0]),
           pv[0][1]+r1*(pv[1][1]-pv[0][1])+r2*(pv[2][1]-pv[0][1]))
        if not any(inside(p,geom.cell_vertices(k)) for k in ks): bad+=1
assert bad==0, bad
print("children cover and are contained: OK")
PY

echo "=== 1. validation ladder ==="
python3 -m eo4 --n 3  --t 1    --strict --max-level 4 --max-cited 4
python3 -m eo4 --n 6  --t 1/2  --strict --max-level 3 --max-cited 4
python3 -m eo4 --n 10 --t 1/3  --strict --max-level 3 --max-cited 4
python3 -m eo4 --n 15 --t 1/4  --strict --max-level 3 --max-cited 4
python3 -m eo4 --n 5  --t 1/2  --strict --max-level 4 --max-cited 4
echo "--- negative controls (must NOT prove) ---"
python3 -m eo4 --n 9  --t 3/10 --max-level 5
python3 -m eo4 --n 9  --t 1/3  --max-level 6

echo "=== 2. fixed rational sides: how far down in a ==="
python3 -m eo4 --n 9 --t 20/59    --max-level  8 --time-limit 900 --out out/closed-a2.95.json
python3 -m eo4 --n 9 --t 100/297  --max-level  9 --time-limit 900 --out out/closed-a2.97.json
python3 -m eo4 --n 9 --t 100/299  --max-level 12 --time-limit 900 --out out/closed-a2.99.json
python3 -m eo4 --n 9 --t 200/599   --max-level 13 --time-limit 900 --out out/closed-a2.995.json
python3 -m eo4 --n 9 --t 1000/2999 --max-level 15 --time-limit 900 --out out/closed-a2.999.json

echo "=== 3. the uniform (strict) target, which provably never closes ==="
for L in 3 4 5 6; do
  python3 -m eo4 --n 9 --t 1/3 --strict --max-level $L --time-limit 300 --out out/strict-n9-L$L.json
done

echo "=== 4. why it never closes: the Delta(4)-lattice-minus-one node ==="
python3 nontermination.py 12 out/nontermination.json

echo "=== 5. survivor localisation ==="
for L in 3 4 5 6; do python3 analyse.py 9 1/3 1 $L out/an-n9-L$L.json 900; done
