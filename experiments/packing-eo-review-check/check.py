"""Independent re-check of the Oler-slack attack's four claims.

Written from the problem statement + the attack's README statements only.
experiments/packing-oler-slack/{geometry,exact,run}.py were NOT read before
this file existed (problem RULES.md section 3).

Run:  python3 check.py
"""

import glob
import json
import os
import re
import sys
from fractions import Fraction as F

from field import Alg, Iv

CERTS = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "..", "problems", "circle-packing-equilateral-triangle",
    "attacks", "exact-algebraic-constructions", "certificates",
)

TWO_OVER_R3 = Alg(0, F(2, 3))          # 2/sqrt3 = 2*sqrt3/3, stays in the field
R3_OVER_4 = Alg(0, F(1, 4))            # sqrt3/4, area of the unit equilateral


# --------------------------------------------------------------------------
# expression parser:  numbers, sqrt(k), + - * / ( )
# --------------------------------------------------------------------------
def parse(expr):
    toks = re.findall(r"sqrt|\d+|[+\-*/()]", expr.replace(" ", ""))
    pos = [0]

    def peek():
        return toks[pos[0]] if pos[0] < len(toks) else None

    def eat(t=None):
        v = toks[pos[0]]
        assert t is None or v == t, f"expected {t}, got {v}"
        pos[0] += 1
        return v

    def atom():
        t = peek()
        if t == "(":
            eat("(")
            v = expression()
            eat(")")
            return v
        if t == "sqrt":
            eat("sqrt")
            eat("(")
            k = int(eat())
            eat(")")
            return Alg.sqrt(k)
        if t == "-":
            eat("-")
            return -atom()
        if t == "+":
            eat("+")
            return atom()
        return Alg(F(int(eat())))

    def term():
        v = atom()
        while peek() in ("*", "/"):
            op = eat()
            v = v * atom() if op == "*" else v / atom()
        return v

    def expression():
        v = term()
        while peek() in ("+", "-"):
            op = eat()
            v = v + term() if op == "+" else v - term()
        return v

    v = expression()
    assert pos[0] == len(toks), f"trailing tokens in {expr!r}"
    return v


# --------------------------------------------------------------------------
# exact planar geometry
# --------------------------------------------------------------------------
def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def dist2(p, q):
    return (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2


def hull_vertices(pts):
    """Monotone chain, strict turns only -> extreme points, CCW order."""
    P = sorted(range(len(pts)), key=lambda i: (
        pts[i][0].approx(30), pts[i][1].approx(30)))
    # resolve the float sort exactly
    P = _exact_sort(pts, P)

    def build(idxs):
        st = []
        for i in idxs:
            while len(st) >= 2 and cross(pts[st[-2]], pts[st[-1]], pts[i]).sign() <= 0:
                st.pop()
            st.append(i)
        return st

    lo = build(P)
    hi = build(P[::-1])
    return lo[:-1] + hi[:-1]


def _exact_sort(pts, order):
    import functools

    def cmp(i, j):
        d = (pts[i][0] - pts[j][0]).sign()
        if d:
            return d
        return (pts[i][1] - pts[j][1]).sign()

    return sorted(order, key=functools.cmp_to_key(cmp))


def on_segment(p, a, b):
    """p strictly between a and b, collinear (a,b distinct)."""
    if cross(a, b, p).sign() != 0:
        return False
    # strictly inside the bounding box along the segment direction
    dx, dy = b[0] - a[0], b[1] - a[1]
    t_num = (p[0] - a[0]) * dx + (p[1] - a[1]) * dy
    len2 = dx * dx + dy * dy
    return t_num.sign() > 0 and (len2 - t_num).sign() > 0


def boundary_count(pts, hull):
    """b = hull vertices + points lying in the interior of a hull edge."""
    b = set(hull)
    h = len(hull)
    for i in range(len(pts)):
        if i in b:
            continue
        for k in range(h):
            if on_segment(pts[i], pts[hull[k]], pts[hull[(k + 1) % h]]):
                b.add(i)
                break
    return b


def shoelace_area(pts, hull):
    s = Alg(0)
    h = len(hull)
    for k in range(h):
        p, q = pts[hull[k]], pts[hull[(k + 1) % h]]
        s = s + (p[0] * q[1] - q[0] * p[1])
    a = s * Alg(F(1, 2))
    return a if a.sign() >= 0 else -a


def exact_sqrt(x):
    """If sqrt(x) happens to lie in Q(sqrt3,sqrt11), return it; else None.

    Enough for lattice edges, whose squared lengths are rational squares.  It
    turns the write-up's 'edge excess is exactly 0' from an enclosure into an
    identity.
    """
    for basis in (Alg(1), Alg(0, 1), Alg(0, 0, 1), Alg(0, 0, 0, 1)):
        sq = basis * basis                       # 1, 3, 11 or 33
        r = x / sq
        if any(c != 0 for c in r.c[1:]):
            continue
        q = r.c[0]
        if q < 0:
            continue
        num, den = q.numerator, q.denominator
        rn, rd = _isqrt_exact(num), _isqrt_exact(den)
        if rn is not None and rd is not None:
            cand = Alg(F(rn, rd)) * basis
            if (cand * cand - x).is_zero():
                return cand
    return None


def _isqrt_exact(m):
    from math import isqrt
    r = isqrt(m)
    return r if r * r == m else None


def perimeter(pts, hull):
    """Total boundary length: exact if every edge length is, else an interval."""
    tot = Iv(0)
    ex = Alg(0)
    all_exact = True
    h = len(hull)
    for k in range(h):
        p, q = pts[hull[k]], pts[hull[(k + 1) % h]]
        d2 = dist2(p, q)
        tot = tot + Iv.of(d2).sqrt()
        e = exact_sqrt(d2)
        if e is None:
            all_exact = False
        else:
            ex = ex + e
    tot.exact = ex if all_exact else None
    return tot


# --------------------------------------------------------------------------
# the four quantities under review
# --------------------------------------------------------------------------
def analyse(pts, a_side=None):
    """pts already in Oler normalisation (min separation 1)."""
    n = len(pts)
    hull = hull_vertices(pts)
    bset = boundary_count(pts, hull)
    b, i = len(bset), n - len(bset)
    Fc = 2 * n - b - 2

    A = shoelace_area(pts, hull)
    M = perimeter(pts, hull)

    face_exc = TWO_OVER_R3 * A - Alg(F(Fc, 2))          # exact, in the field
    edge_exc = (M - Iv(b)) * Iv(F(1, 2))                # interval
    stage1 = Iv.of(face_exc) + edge_exc

    out = dict(n=n, b=b, i=i, F=Fc, A=A, M=M,
               face_exc=face_exc, edge_exc=edge_exc, stage1=stage1,
               hull=hull, min_sep2=min(dist2(pts[p], pts[q])
                                       for p in range(n) for q in range(p + 1, n)))
    if a_side is not None:
        a = a_side
        total = a * a * Alg(F(1, 2)) + a * Alg(F(3, 2)) + Alg(1) - Alg(n)
        A_T = R3_OVER_4 * a * a
        M_T = Alg(3) * a
        stage2 = Iv.of(TWO_OVER_R3 * (A_T - A)) + (Iv.of(M_T) - M) * Iv(F(1, 2))
        out.update(a=a, total=total, stage2=stage2,
                   residual=Iv.of(total) - stage1 - stage2)
    return out


def load_cert(path):
    d = json.load(open(path))
    half = Alg(F(1, 2))
    pts = [(parse(x) * half, parse(y) * half) for x, y in d["coordinates"]]
    a = parse(d["point_triangle_side"]) * half
    return d, pts, a


# --------------------------------------------------------------------------
def main():
    print("=" * 78)
    print("INDEPENDENT REVIEW CHECKER  (claude, reviewer role)")
    print("field: Q(sqrt3,sqrt11); areas/face-excess EXACT, lengths enclosed")
    print("=" * 78)

    # ---------------- CLAIM 2: the slack atlas -------------------------
    print("\n### CLAIM 2 -- slack atlas recomputed from certificate coordinates\n")
    hdr = f"{'n':>3} {'b':>3} {'i':>3} {'F':>3} {'faceExc':>13} {'edgeExc':>13} " \
          f"{'stage1':>13} {'stage2':>13} {'total':>10} {'sep2>=1':>7}"
    print(hdr)
    print("-" * len(hdr))
    rows = {}
    for path in sorted(glob.glob(os.path.join(CERTS, "*.json"))):
        d, pts, a = load_cert(path)
        if len(pts) < 3:
            print(f"{len(pts):>3}  (degenerate hull -- skipped, as the write-up says)")
            continue
        r = analyse(pts, a)
        rows[r["n"]] = r
        ok = "yes" if r["min_sep2"] >= Alg(1) else "NO"
        print(f"{r['n']:>3} {r['b']:>3} {r['i']:>3} {r['F']:>3} "
              f"{r['face_exc'].approx():>13.7f} {r['edge_exc'].mid():>13.7f} "
              f"{r['stage1'].mid():>13.7f} {r['stage2'].mid():>13.7f} "
              f"{r['total'].approx():>10.7f} {ok:>7}")
        assert r["residual"].lo <= 0 <= r["residual"].hi, "stage1+stage2 != total"

    # exactness of the "stage 1 is exactly zero" finding
    print("\nstage-1 exact-zero test -- EXACT, not an enclosure:")
    for n, r in sorted(rows.items()):
        fe0 = r["face_exc"].is_zero()
        Mex = r["M"].exact
        if Mex is None:
            mtxt, be0 = "M irrational (interval only)", False
        else:
            be0 = (Mex - Alg(r["b"])).is_zero()
            mtxt = f"M = {Mex} exactly, b = {r['b']}, M-b = {(Mex - Alg(r['b']))}"
        tag = "EXACTLY 0" if (fe0 and be0) else ("faceExc=0 only" if fe0 else "-")
        print(f"  n={n:>3}: face_exc==0 -> {str(fe0):<5}  {mtxt:<46} => stage1 {tag}")

    # ---------------- CLAIM 1: the identity -----------------------------
    print("\n### CLAIM 1 -- identity, checked via an explicit triangulation\n")
    from triangulate import triangulate
    for n, r in sorted(rows.items()):
        d, pts, a = load_cert(_cert_path(n))
        tris = triangulate(pts)
        rhs_face = Alg(0)
        for (x, y, z) in tris:
            Af = _tri_area(pts[x], pts[y], pts[z])
            rhs_face = rhs_face + TWO_OVER_R3 * (Af - R3_OVER_4)
        lhs = Iv.of(TWO_OVER_R3 * r["A"]) + r["M"] * Iv(F(1, 2)) + Iv(1) - Iv(n)
        rhs = Iv.of(rhs_face) + r["edge_exc"]
        agree = (lhs - rhs).lo <= 0 <= (lhs - rhs).hi
        fcount_ok = len(tris) == r["F"]
        print(f"  n={n:>3}: triangles built={len(tris):>3}  2n-b-2={r['F']:>3}  "
              f"{'MATCH' if fcount_ok else 'MISMATCH':<8} "
              f"faceExc(triangulated)={rhs_face.approx():+.7f} vs "
              f"formula {r['face_exc'].approx():+.7f}  "
              f"identity={'holds' if agree else 'FAILS'}")
        assert fcount_ok and agree and (rhs_face - r["face_exc"]).is_zero()

    # ---------------- CLAIM 3: refutation of H --------------------------
    print("\n### CLAIM 3 -- hypothesis H (face excess >= 0) refuted\n")
    wit = [(Alg(0), Alg(0)), (Alg(1), Alg(0)), (Alg(2), Alg(F(1, 2)))]
    r = analyse(wit)
    print(f"  witness {{(0,0),(1,0),(2,1/2)}}: min sep^2 = {r['min_sep2']} "
          f"(>=1? {r['min_sep2'] >= Alg(1)})")
    print(f"  area = {r['A']}  = {r['A'].approx():.7f}   "
          f"(sqrt3/4 = {R3_OVER_4.approx():.7f})")
    print(f"  face excess = {r['face_exc']} = {r['face_exc'].approx():.7f}  "
          f"sign = {r['face_exc'].sign():+d}")
    print(f"  Oler slack  = {r['stage1'].mid():+.7f}  (still >= 0: "
          f"{r['stage1'].lo > 0})")
    assert r["face_exc"].sign() < 0

    print("\n  flat-arc family p_j = (j, j(m-j)/m^3):")
    print(f"  {'m':>3} {'n':>3} {'b':>3} {'minsep2':>12} {'faceExc':>13} {'olerSlack':>13}")
    for m in (3, 4, 6, 8, 12, 16):
        pts = [(Alg(F(j)), Alg(F(j * (m - j), m ** 3))) for j in range(m + 1)]
        r = analyse(pts)
        print(f"  {m:>3} {r['n']:>3} {r['b']:>3} {r['min_sep2'].approx():>12.6f} "
              f"{r['face_exc'].approx():>13.7f} {r['stage1'].mid():>13.7f}")
        assert r["min_sep2"] >= Alg(1), "flat arc violates separation!"
        assert r["b"] == r["n"], "flat arc should be all-boundary"

    # ---------------- CLAIM 4: FP => Erdos-Oler -------------------------
    print("\n### CLAIM 4 -- FP implies Erdos-Oler, re-derived exactly\n")
    print("  For a < k-1 we get floor(a) <= k-2, so FP bounds n by")
    print("  a^2/2 + (3/2)(k-2) + 1 < (k-1)^2/2 + (3/2)(k-2) + 1.")
    print(f"  {'k':>3} {'T(k)':>5} {'bound at a->(k-1)^-':>20} {'=> n <=':>8} "
          f"{'T(k)-1 excluded?':>18}")
    for k in range(3, 21):
        Tk = F(k * (k + 1), 2)
        sup = F(k - 1) ** 2 / 2 + F(3, 2) * (k - 2) + 1
        import math
        nmax = math.ceil(sup) - 1 if sup == int(sup) else math.floor(sup)
        excl = nmax <= Tk - 2
        print(f"  {k:>3} {int(Tk):>5} {str(sup):>20} {nmax:>8} "
              f"{('yes' if excl else 'NO'):>18}")
        assert sup == Tk - F(3, 2), f"k={k}: sup should be T(k)-3/2"
        assert excl
    print("\n  => T(k)-1 points force a >= k-1 for every k; the lattice T(k)")
    print("     minus one point realises a = k-1, so s(T(k)-1) = s(T(k)).")

    # ---------------- general-k version of the atlas finding ------------
    print("\n### BONUS -- the 'stage 1 = 0, stage 2 = 1' finding, proved for all k\n")
    for k in range(3, 13):
        Tk = F(k * (k + 1), 2)
        # lattice T(k): b = 3(k-1), A = (sqrt3/4)(k-1)^2, M = 3(k-1)
        b = 3 * (k - 1)
        fe = F(k - 1) ** 2 / 2 - F(2 * int(Tk) - b - 2, 2)
        be = F(3 * (k - 1) - b, 2)
        tot_lat = F(k - 1) ** 2 / 2 + F(3, 2) * (k - 1) + 1 - Tk
        # T(k) minus apex
        n2 = int(Tk) - 1
        b2 = 3 * (k - 1) - 1
        A2 = (F(k - 1) ** 2 - 1) / 2          # already multiplied by 2/sqrt3
        fe2 = A2 - F(2 * n2 - b2 - 2, 2)
        M2 = (k - 1) + 2 * (k - 2) + 1
        be2 = F(M2 - b2, 2)
        tot2 = F(k - 1) ** 2 / 2 + F(3, 2) * (k - 1) + 1 - n2
        print(f"  k={k:>3}: T(k)  faceExc={fe} edgeExc={be} total={tot_lat}   |   "
              f"T(k)-1  faceExc={fe2} edgeExc={be2} stage2={tot2}")
        assert fe == 0 and be == 0 and tot_lat == 0
        assert fe2 == 0 and be2 == 0 and tot2 == 1

    print("\nAll assertions passed.")


def _cert_path(n):
    return os.path.join(CERTS, f"n{n:03d}-exact.json")


def _tri_area(p, q, r):
    s = (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
    a = s * Alg(F(1, 2))
    return a if a.sign() >= 0 else -a


if __name__ == "__main__":
    main()
