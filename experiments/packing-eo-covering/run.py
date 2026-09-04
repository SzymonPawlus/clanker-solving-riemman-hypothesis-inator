"""Reproduce every EXACT claim of attacks/eo-covering-construct in one command.

    python3 experiments/packing-eo-covering/run.py

Python standard library only.  All arithmetic exact (Fractions / Q(sqrt3));
no float decides anything here.  Exits non-zero if any check fails.
"""
import json, os, sys
from fractions import Fraction as F
from exact import Q3, q3, verify, voronoi_cells, power_cells_exact, diam2, triangle, shoelace2
from build28 import build

HERE = os.path.dirname(os.path.abspath(__file__))
fails = 0

def check(name, cond):
    global fails
    print("  [%s] %s" % ("ok" if cond else "FAIL", name))
    if not cond: fails += 1

print("normalisation assertions (separation 1, side a, corners (0,0),(a,0),(a/2,a*sqrt3/2))")
check("basis: |e1|^2 = 1", diam2([(q3(0), q3(0)), (q3(1), q3(0))]) == q3(1))
check("basis: |e2|^2 = 1", diam2([(q3(0), q3(0)), (q3(0), q3(1))]) == q3(1))
check("basis: |e1-e2|^2 = 1", diam2([(q3(1), q3(0)), (q3(0), q3(1))]) == q3(1))
check("T_a area: shoelace(T_6)=36", shoelace2(triangle(6)) == q3(36))

print("\n1. sanity: the k=3 medial subdivision of T_2 (4 cells, diameter exactly 1)")
med = [[(q3(0), q3(0)), (q3(1), q3(0)), (q3(0), q3(1))],
       [(q3(1), q3(0)), (q3(2), q3(0)), (q3(1), q3(1))],
       [(q3(0), q3(1)), (q3(1), q3(1)), (q3(0), q3(2))],
       [(q3(1), q3(0)), (q3(1), q3(1)), (q3(0), q3(1))]]
ok, w = verify(med, 2, verbose=False)
check("T_2 = 4 cells, max diam^2 = %s" % w, ok and w == q3(1))

print("\n2. LATTICE LEMMA:  T_a splits into Delta(p) cells of diameter <= 1 for a = p*sqrt3/2")
print("   p  cells   a=p*sqrt3/2   max diam^2")
for p in range(2, 11):
    a = Q3(0, F(p, 2))
    sites, _ = build(a=a, m=p-1)
    cells = voronoi_cells(sites, a)
    ok, w = verify(cells, a, verbose=False)
    print("   %2d  %4d   %10.6f    %s" % (p, len(sites), a.approx(), w))
    check("p=%d: Delta(%d)=%d cells, all diam^2 <= 1" % (p, p, p*(p+1)//2),
          ok and w <= q3(1) and len(sites) == p*(p+1)//2)

print("\n3. the case that matters: 28 cells for T_a, a <= 7*sqrt3/2 = 6.0622 (need 26 at a=6)")
a = Q3(0, F(7, 2))
sites, _ = build(a=a, m=6)
cells = voronoi_cells(sites, a)
ok, w = verify(cells, a, verbose=False)
check("28 cells partition T_{7sqrt3/2}, max diam^2 = %s" % w, ok and w == q3(1))
sites6, _ = build(a=q3(6), m=6)
cells6 = voronoi_cells(sites6, q3(6))
ok6, w6 = verify(cells6, 6, verbose=False)
check("28 cells partition T_6, max diam^2 = %s" % w6, ok6 and w6 <= q3(1))
check("a = 7sqrt3/2 is sharp for this scheme: fails at a = 6.07",
      not verify(voronoi_cells(build(a=q3(F(607, 100)), m=6)[0], q3(F(607, 100))),
                 q3(F(607, 100)), verbose=False, report=False)[0])

print("\n4. search certificates (power diagrams, rational sites/weights)")
for fn, want in (("cert26.json", 26), ("cert27.json", 27), ("cert28opt.json", 28)):
    d = json.load(open(os.path.join(HERE, fn)))
    a = F(int(d["a"][0]), int(d["a"][1]))
    S = [(q3(F(u)), q3(F(v))) for u, v in d["sites"]]
    W = [F(x) for x in d["weights"]]
    cs = [c for c in power_cells_exact(S, W, q3(a)) if c]
    ok, w = verify(cs, q3(a), verbose=False)
    check("%s: %d cells partition T_{%s} (=%.6f), max diam^2 ~ %.9f"
          % (fn, len(cs), a, float(a), w.approx()), ok and len(cs) == want and w <= q3(1))

print("\n%s" % ("ALL EXACT CHECKS PASSED" if fails == 0 else "%d CHECK(S) FAILED" % fails))
sys.exit(1 if fails else 0)
