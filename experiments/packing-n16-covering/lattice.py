"""Lemma L, p=5, re-derived independently and verified exactly in Q(sqrt3).

Construction (own implementation; the scheme is from attacks/eo-covering-construct §2):
sites of the triangular lattice of spacing g = sqrt3/2, arranged as Delta(p),
centred in T_a; cells = Voronoi cells clipped to T_a.
"""
from fractions import Fraction as F
from exact import q3, Q3, SQ3, voronoi_cells, verify, diam2, shoelace2, triangle

def lattice_sites(p, a):
    a = q3(a)
    g = Q3(0, F(1, 2))          # sqrt3/2
    u0 = (a - g*(p-1)) * F(1, 3)
    return [(u0 + g*i, u0 + g*j) for i in range(p) for j in range(p-i)]

def build(p, a):
    return voronoi_cells(lattice_sites(p, a), q3(a))

def classify(p):
    """corner / edge / interior label for each site in the same order as lattice_sites"""
    lab = []
    for i in range(p):
        for j in range(p-i):
            k = p-1-i-j
            zeros = (i == 0) + (j == 0) + (k == 0)
            lab.append("corner" if zeros == 2 else ("edge" if zeros == 1 else "interior"))
    return lab

if __name__ == "__main__":
    p = 5
    a0 = Q3(0, F(5, 2))         # 5*sqrt3/2
    cells = build(p, a0)
    print("p = 5, a0 = 5*sqrt3/2 = %.9f" % a0.approx())
    ok, worst = verify(cells, a0)
    lab = classify(p)
    tot = q3(0)
    byl = {}
    for c, L in zip(cells, lab):
        s = shoelace2(c)
        if s.sign() < 0: s = -s
        # true area = (sqrt3/4)*s
        A = (s * Q3(0, F(1, 4))).approx()
        byl.setdefault(L, []).append(A)
        tot = tot + s
    print()
    for L in ("corner", "edge", "interior"):
        v = sorted(byl[L])
        print("%-9s n=%2d  area %.6f .. %.6f   sum %.6f" % (L, len(v), v[0], v[-1], sum(v)))
    print("total area      %.9f   (sqrt3/4*a0^2 = %.9f)"
          % ((tot*Q3(0, F(1,4))).approx(), 3**0.5/4*a0.approx()**2))
    print("mean cell area  %.6f   hexagon ceiling 3*sqrt3/8 = %.6f" %
          ((tot*Q3(0, F(1,4))).approx()/15, 3*3**0.5/8))
    assert ok
