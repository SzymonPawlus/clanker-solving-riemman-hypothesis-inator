"""Exact checks for the Oler equality-case attack (`attacks/eo-oler-equality`).

One command, Python standard library only, exact arithmetic for every decision.

    python3 run.py            # writes out/report.txt and prints the same text

Normalisation: separation 1, Oler's own.  E finite with pairwise distances >= 1,
P = conv(E), n = |E|, slack(E) = (2/sqrt3) A(P) + M(P)/2 + 1 - n.

Sections
  1  Lemma T  -- the n = 3 case of Oler with its equality classification.
     Decision procedure is exact over Q: with rational sides, 16 A^2 is rational,
     so  (2/sqrt3) A >= 2 - p/2  is decided by one rational comparison.
  2  the algebra of the proof of Lemma T (polynomial identity + the vertex step)
  3  the extremal class: slack of lattice-convex sets, exactly, in Q(sqrt3)
  4  the tau-identity  slack = sum_f tau(f) - sum_{interior e} (len(e) - 1)
  5  Theorem D arithmetic: equilateral hull, no interior points
  6  scope: what an equality theorem does and does not give at k = 7
  7  control: face excess at a perturbed lattice (independent re-derivation of
     eo-boundary-counting W1 -- priority is theirs, this is a control only)
"""

import random
import sys
from fractions import Fraction as F

sys.path.insert(0, "../packing-oler-slack")
from exact import Alg, Ival, sqrt_bounds          # noqa: E402  (read-only import)

OUT = []


def say(s=""):
    OUT.append(s)
    print(s)


def head(t):
    say()
    say("=" * 78)
    say(t)
    say("=" * 78)


# ---------------------------------------------------------------------------
# 1. Lemma T
# ---------------------------------------------------------------------------
# G(x,y,z) = (2/sqrt3) A + (x+y+z)/2 - 2.  Sign decided exactly over Q.
#   16 A^2 = 2(x^2y^2 + y^2z^2 + z^2x^2) - (x^4 + y^4 + z^4) =: Q  (>= 0 iff a
#   triangle, possibly degenerate).   (2/sqrt3) A = sqrt(Q/12).
# So G >= 0  <=>  Q/12 >= (2 - p/2)^2  or  2 - p/2 <= 0 ;
#    G  = 0  <=>  2 - p/2 >= 0  and  Q/12 == (2 - p/2)^2.

def heron_Q(x, y, z):
    return 2 * (x * x * y * y + y * y * z * z + z * z * x * x) - (
        x ** 4 + y ** 4 + z ** 4
    )


def lemmaT_sign(x, y, z):
    """Exact sign of G for a (possibly degenerate) triangle with sides x,y,z."""
    Q = heron_Q(x, y, z)
    assert Q >= 0, "not a triangle"
    r = 2 - F(x + y + z, 2)
    if r < 0:
        return 1
    lhs, rhs = F(Q, 12), r * r
    return (lhs > rhs) - (lhs < rhs)


def is_triangle(x, y, z):
    return heron_Q(x, y, z) >= 0


def lemmaT_scan():
    head("1. Lemma T -- (2/sqrt3) A + p/2 >= 2 for every triangle with sides >= 1")
    say("Decision is exact over Q; no floating point anywhere in this section.")

    violations, equalities = [], []
    checked = 0

    # (a) systematic grid, sides in [1, 4] on a 1/12 lattice
    step = F(1, 12)
    vals = [1 + i * step for i in range(0, 37)]
    for i, x in enumerate(vals):
        for y in vals[i:]:
            for z in vals:
                if z < y:
                    continue
                if not is_triangle(x, y, z):
                    continue
                checked += 1
                s = lemmaT_sign(x, y, z)
                if s < 0:
                    violations.append((x, y, z))
                elif s == 0:
                    equalities.append((x, y, z))
    say(f"(a) grid scan, sides in [1,4] step 1/12 : {checked} triangles checked")

    # (b) random rational sides, including near-degenerate and very obtuse ones
    rng = random.Random(20260821)
    rnd = 0
    for _ in range(200000):
        d = rng.choice([2, 3, 4, 5, 6, 7, 8, 12, 16, 24, 60, 97, 100, 1000])
        x = 1 + F(rng.randrange(0, 6 * d), d)
        y = 1 + F(rng.randrange(0, 6 * d), d)
        z = 1 + F(rng.randrange(0, 6 * d), d)
        if not is_triangle(x, y, z):
            continue
        rnd += 1
        s = lemmaT_sign(x, y, z)
        if s < 0:
            violations.append((x, y, z))
        elif s == 0 and (x, y, z) not in equalities:
            equalities.append((x, y, z))
    say(f"(b) random rational scan             : {rnd} triangles checked")

    # (c) degenerate triangles x = y + z with y, z >= 1 (Q = 0 exactly)
    deg = 0
    for i in range(0, 61):
        for j in range(0, 61):
            y, z = 1 + F(i, 20), 1 + F(j, 20)
            x = y + z
            assert heron_Q(x, y, z) == 0
            deg += 1
            s = lemmaT_sign(x, y, z)
            if s < 0:
                violations.append((x, y, z))
            elif s == 0:
                equalities.append((x, y, z))
    say(f"(c) degenerate (collinear) triangles : {deg} checked")

    # (d) fine scan around the two predicted equality points
    fine = 0
    for a in range(-6, 7):
        for b in range(-6, 7):
            for c in range(-6, 7):
                for base in ((1, 1, 1), (2, 1, 1)):
                    x = base[0] + F(a, 1000)
                    y = base[1] + F(b, 1000)
                    z = base[2] + F(c, 1000)
                    if min(x, y, z) < 1 or not is_triangle(x, y, z):
                        continue
                    fine += 1
                    s = lemmaT_sign(x, y, z)
                    if s < 0:
                        violations.append((x, y, z))
                    elif s == 0:
                        equalities.append((x, y, z))
    say(f"(d) fine scan near (1,1,1),(2,1,1)   : {fine} checked")

    say()
    say(f"VIOLATIONS of Lemma T found : {len(violations)}")
    eqset = sorted({tuple(sorted(t)) for t in equalities})
    say(f"EQUALITY triples found      : {[tuple(str(v) for v in t) for t in eqset]}")
    ok = not violations and eqset == [(F(1), F(1), F(1)), (F(1), F(1), F(2))]
    say(f"K1 (Lemma T + its equality classification) holds on every case checked: {ok}")
    return ok


def lemmaT_algebra():
    head("2. The algebra inside the proof of Lemma T")
    # h(S) = S(S-2)^2 + 3S - 12  ==  (S-3)(S^2 - S + 4)
    def h1(S):
        return S * (S - 2) ** 2 + 3 * S - 12

    def h2(S):
        return (S - 3) * (S * S - S + 4)

    pts = [F(i, 7) for i in range(-20, 40)]
    say(f"(i)  identity  S(S-2)^2 + 3S - 12 = (S-3)(S^2-S+4)  at {len(pts)} "
        f"rational points: {all(h1(S) == h2(S) for S in pts)}")
    say("     degree 3 both sides, so agreement at 4 points already proves it; "
        "the discriminant of S^2-S+4 is -15 < 0, so that factor is positive, "
        "hence h(S) >= 0 for S >= 3 with equality only at S = 3.")

    # (ii) the vertex step: for S in [3,4], min of a*b*c over {a+b+c=S,
    #      each in [4-S, S-2]} is (S-2)^2 (4-S).
    bad = []
    for k in range(0, 41):
        S = 3 + F(k, 40)
        lo, hi = 4 - S, S - 2
        target = (S - 2) ** 2 * (4 - S)
        m = 400
        for i in range(m + 1):
            a = lo + (hi - lo) * F(i, m)
            for j in range(m + 1):
                b = lo + (hi - lo) * F(j, m)
                c = S - a - b
                if c < lo or c > hi:
                    continue
                if a * b * c < target:
                    bad.append((S, a, b, c))
                    break
            if bad:
                break
    say(f"(ii) vertex step, S on a 1/40 grid in [3,4], polytope on a 400-grid: "
        f"{len(bad)} points below (S-2)^2(4-S) -> {'OK' if not bad else bad[:3]}")
    return not bad


# ---------------------------------------------------------------------------
# exact geometry in Q(sqrt3)
# ---------------------------------------------------------------------------
SQ3 = Alg.sqrt(3)
HALF = Alg.rational(F(1, 2))


def lat(i, j):
    """Point i*(1,0) + j*(1/2, sqrt3/2) of the unit triangular lattice."""
    return (Alg.rational(i) + Alg.rational(F(j, 2)), SQ3 * Alg.rational(F(j, 2)))


def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def d2(p, q):
    dx, dy = p[0] - q[0], p[1] - q[1]
    return dx * dx + dy * dy


def hull(pts):
    """Andrew monotone chain, exact; returns hull VERTICES ccw (no collinear)."""
    P = sorted(set(pts), key=lambda p: (p[0], p[1]))
    if len(P) < 3:
        return P
    def build(seq):
        st = []
        for p in seq:
            while len(st) >= 2 and cross(st[-2], st[-1], p) <= 0:
                st.pop()
            st.append(p)
        return st
    lower = build(P)
    upper = build(reversed(P))
    return lower[:-1] + upper[:-1]


def on_seg(p, a, b):
    if cross(a, b, p) != Alg.rational(0):
        return False
    return (min(a[0], b[0]) <= p[0] <= max(a[0], b[0])
            and min(a[1], b[1]) <= p[1] <= max(a[1], b[1]))


def area2(poly):
    """Twice the signed area, exact in Q(sqrt3)."""
    s = Alg.rational(0)
    for i in range(len(poly)):
        a, b = poly[i], poly[(i + 1) % len(poly)]
        s = s + (a[0] * b[1] - b[0] * a[1])
    return s


def perimeter_ival(poly, prec=80):
    tot = Ival(F(0), F(0))
    for i in range(len(poly)):
        a, b = poly[i], poly[(i + 1) % len(poly)]
        tot = tot + Ival.of(d2(a, b), prec).sqrt(prec)
    return tot


def boundary_points(pts, hv):
    out = []
    for p in pts:
        for i in range(len(hv)):
            if on_seg(p, hv[i], hv[(i + 1) % len(hv)]):
                out.append(p)
                break
    return out


def min_sep2(pts):
    return min(d2(p, q) for i, p in enumerate(pts) for q in pts[i + 1:])


def slack_ival(pts, prec=80):
    """slack = (2/sqrt3)A + M/2 + 1 - n, as a rigorous rational enclosure."""
    hv = hull(pts)
    n = len(pts)
    A2 = area2(hv)                       # 2A, exact
    term_area = A2 / SQ3                 # (2/sqrt3) * A  = (2A)/sqrt3 , exact
    M = perimeter_ival(hv, prec)
    b = len(boundary_points(pts, hv))
    return (Ival.of(term_area, prec) + M * F(1, 2)
            + Ival(F(1 - n), F(1 - n))), b, term_area, M


# ---------------------------------------------------------------------------
# 3. the extremal class
# ---------------------------------------------------------------------------
def tri_lattice(k):
    return [lat(i, j) for j in range(k) for i in range(k - j)]


def lattice_convex_cases():
    head("3. The extremal class: slack of lattice-convex sets (exact)")
    say("A set is *lattice-convex* here if E = Lambda ∩ conv(E) for the unit")
    say("triangular lattice Lambda.  Prediction (Theorem 3): slack = (M - b)/2,")
    say("so slack = 0 iff every hull edge between consecutive points has length 1.")
    say()
    cases = []
    for k in (2, 3, 4, 5, 7):
        cases.append((f"T({k}) lattice, n={k*(k+1)//2}", tri_lattice(k), True))
    cases.append(("unit rhombus (2 faces)", [lat(0, 0), lat(1, 0), lat(0, 1), lat(1, 1)], True))
    cases.append(("unit hexagon + centre",
                  [lat(0, 0), lat(1, 0), lat(0, 1), lat(-1, 1), lat(-1, 0),
                   lat(0, -1), lat(1, -1)], True))
    cases.append(("unit trapezoid (T(3) minus a corner)",
                  [lat(0, 0), lat(1, 0), lat(2, 0), lat(0, 1), lat(1, 1)], True))
    # a lattice polygon with one PRIMITIVE edge of length sqrt3 > 1
    cases.append(("lattice triangle with a sqrt3 edge",
                  [lat(0, 0), lat(1, 0), lat(2, 0), lat(1, 1)], True))
    # not lattice-convex: an interior lattice point deleted
    t4 = tri_lattice(4)
    cases.append(("T(4) minus its interior point (NOT lattice-convex)",
                  [p for p in t4 if p != lat(1, 1)], False))
    t7 = tri_lattice(7)
    cases.append(("T(7) minus an interior point, n=27 (NOT lattice-convex)",
                  [p for p in t7 if p != lat(2, 2)], False))
    cases.append(("T(7) minus its apex, n=27", [p for p in t7 if p != lat(0, 6)], True))

    say(f"{'configuration':<44}{'n':>3}{'b':>4}  {'min sep^2':>10}  "
        f"{'slack (enclosure)':>26}  lat-cvx")
    rows = []
    for name, pts, latcvx in cases:
        sl, b, ta, M = slack_ival(pts, prec=60)
        n = len(pts)
        ms = min_sep2(pts)
        pred = (M - Ival(F(b), F(b))) * F(1, 2)
        agrees = (sl.lo <= pred.hi and pred.lo <= sl.hi)
        rows.append((name, n, b, sl, pred, agrees, latcvx))
        say(f"{name:<44}{n:>3}{b:>4}  {ms.float():>10.6f}  "
            f"[{sl.lo.__float__():.9f}, {sl.hi.__float__():.9f}]  {latcvx}")
    say()
    say("Check slack == (M - b)/2 exactly (i.e. face excess == 0) for the")
    say("lattice-convex rows -- this is Pick's theorem in disguise:")
    for name, n, b, sl, pred, agrees, latcvx in rows:
        if latcvx:
            say(f"  {name:<44} (M-b)/2 in [{float(pred.lo):.9f}, "
                f"{float(pred.hi):.9f}]  agrees: {agrees}")
    say()
    say("Note the n = 27 row 'T(7) minus its apex': slack is exactly 0 at a")
    say("non-triangular n.  Equality in Oler therefore does NOT by itself force")
    say("n to be triangular; that conclusion needs the extra hypothesis that the")
    say("hull is the whole containing triangle.")
    say()
    say("Rows where slack is exactly 0 must be exactly the unit-edge ones:")
    for name, n, b, sl, pred, agrees, latcvx in rows:
        zero = sl.lo <= 0 <= sl.hi
        say(f"  {name:<44} slack could be 0: {zero}")
    return rows


# ---------------------------------------------------------------------------
# 4. the tau-identity
# ---------------------------------------------------------------------------
def tau_check():
    head("4. The tau-identity:  slack = sum_f tau(f) - sum_{interior e} (len e - 1)")
    say("tau(f) = (2/sqrt3)A_f + p_f/2 - 2 >= 0 is exactly Lemma T's defect.")
    say("Verified on explicitly given triangulations (faces listed by hand).")

    def up(i, j):
        return (lat(i, j), lat(i + 1, j), lat(i, j + 1))

    def down(i, j):
        return (lat(i + 1, j), lat(i + 1, j + 1), lat(i, j + 1))

    def lattice_faces(k):
        fs = []
        for j in range(k - 1):
            for i in range(k - 1 - j):
                fs.append(up(i, j))
                if i + j < k - 2:
                    fs.append(down(i, j))
        return fs

    cases = [
        ("single unit triangle", [lat(0, 0), lat(1, 0), lat(0, 1)], [up(0, 0)]),
        ("unit rhombus", [lat(0, 0), lat(1, 0), lat(0, 1), lat(1, 1)],
         [up(0, 0), (lat(1, 0), lat(1, 1), lat(0, 1))]),
    ]
    for k in (3, 4, 5):
        cases.append((f"T({k}) lattice", tri_lattice(k), lattice_faces(k)))
    # a non-lattice control: the refutation witness of oler-slack-analysis §4
    w = [(Alg.rational(0), Alg.rational(0)), (Alg.rational(1), Alg.rational(0)),
         (Alg.rational(2), Alg.rational(F(1, 2)))]
    cases.append(("witness (0,0),(1,0),(2,1/2)", w, [tuple(w)]))
    # a non-lattice 4-point control
    q = [(Alg.rational(0), Alg.rational(0)), (Alg.rational(F(3, 2)), Alg.rational(0)),
         (Alg.rational(F(11, 4)), Alg.rational(F(1, 2))),
         (Alg.rational(F(1, 2)), SQ3)]
    cases.append(("generic 4-point set", q,
                  [(q[0], q[1], q[3]), (q[1], q[2], q[3])]))

    prec = 70
    allok = True
    for name, pts, faces in cases:
        n = len(pts)
        hv = hull(pts)
        b = len(boundary_points(pts, hv))
        # face count control  F = 2n - b - 2
        Fcount = len(faces)
        ok_F = (Fcount == 2 * n - b - 2)
        # areas sum to A(P)
        tot2 = Alg.rational(0)
        for f in faces:
            a2 = area2(list(f))
            tot2 = tot2 + (a2 if a2.sign() > 0 else -a2)
        ok_A = (tot2 == area2(hv) or tot2 == -area2(hv))
        # tau sum
        tau = Ival(F(0), F(0))
        for f in faces:
            a2 = area2(list(f))
            a2 = a2 if a2.sign() > 0 else -a2
            per = perimeter_ival(list(f), prec)
            tau = tau + Ival.of(a2 / SQ3, prec) + per * F(1, 2) - Ival(F(2), F(2))
        # interior edges
        edges = {}
        for f in faces:
            for i in range(3):
                e = tuple(sorted([f[i], f[(i + 1) % 3]], key=lambda p: (p[0], p[1])))
                edges[e] = edges.get(e, 0) + 1
        inter = [e for e, c in edges.items() if c == 2]
        bd = [e for e, c in edges.items() if c == 1]
        Lint = Ival(F(0), F(0))
        for e in inter:
            Lint = Lint + Ival.of(d2(*e), prec).sqrt(prec) - Ival(F(1), F(1))
        rhs = tau - Lint
        sl, _, _, _ = slack_ival(pts, prec)
        agrees = (sl.lo <= rhs.hi and rhs.lo <= sl.hi)
        ok_Eint = (len(inter) == 3 * n - 2 * b - 3) and (len(bd) == b)
        allok = allok and ok_F and ok_A and agrees and ok_Eint
        say(f"{name:<30} n={n:>2} b={b:>2} F={Fcount:>2} "
            f"F=2n-b-2:{str(ok_F):>5} areas:{str(ok_A):>5} "
            f"|E_int|=3n-2b-3:{str(ok_Eint):>5} identity:{str(agrees):>5}")
        say(f"{'':30}   slack in [{float(sl.lo):.9f},{float(sl.hi):.9f}]  "
            f"sum tau - sum(len-1) in [{float(rhs.lo):.9f},{float(rhs.hi):.9f}]")
    say(f"tau-identity holds on every case checked: {allok}")
    return allok


# ---------------------------------------------------------------------------
# 5. Theorem D arithmetic
# ---------------------------------------------------------------------------
def theoremD():
    head("5. Theorem D: equilateral hull, no interior points -- the arithmetic")
    say("Equality gives n = (a^2+3a+2)/2 ; boundary-only gives n <= 3*floor(a).")
    say("Hence a^2 + 3a + 2 <= 6*floor(a) <= 6a, i.e. a^2 - 3a + 2 <= 0, i.e.")
    say("1 <= a <= 2.  Roots of a^2-3a+2 are exactly 1 and 2:")
    say(f"  a=1: {1 - 3 + 2 == 0}    a=2: {4 - 6 + 2 == 0}")
    say("Sub-case a in [1,2): floor(a)=1 so n <= 3, and n = (a^2+3a+2)/2 >= 3")
    say("  with equality at a=1 only (a^2+3a-4 = (a+4)(a-1)):")
    for a in (F(1), F(3, 2), F(19, 10)):
        say(f"    a={a}: n_eq=(a^2+3a+2)/2={(a*a+3*a+2)/2}  bound 3*floor(a)=3 "
            f"-> feasible: {(a*a+3*a+2)/2 <= 3}")
    say("Sub-case a=2: n = 6 = 3*floor(2), so the boundary bound is tight, so")
    say("  every side carries exactly 3 points at spacing exactly 1.")
    say("A grid check that no other a in [1,3] can satisfy both constraints:")
    bad = []
    for i in range(100, 301):
        a = F(i, 100)
        n_eq = (a * a + 3 * a + 2) / 2
        if n_eq.denominator == 1 and n_eq <= 3 * (a.numerator // a.denominator):
            bad.append((a, n_eq))
    say(f"  integer-n solutions of the joint constraint on a 1/100 grid in [1,3]: {bad}")
    return True


# ---------------------------------------------------------------------------
# 6. scope at k = 7
# ---------------------------------------------------------------------------
def scope():
    head("6. Scope: what an equality theorem gives at k = 7 (control on O1)")
    say("Oler RHS at a = k-1 is exactly T(k):")
    for k in range(2, 11):
        a = k - 1
        rhs = F(a * a + 3 * a + 2, 2)
        say(f"  k={k:>2}  a={a:>2}  RHS={rhs}  T(k)={k*(k+1)//2}  "
            f"equal: {rhs == k * (k + 1) // 2}")
    say()
    say("27 points force a^2 + 3a - 52 >= 0.  a* = (-3 + sqrt217)/2, bracketed")
    lo, hi = sqrt_bounds(F(217), 12)
    alo, ahi = (lo - 3) / 2, (hi - 3) / 2
    say(f"  a* in [{float(alo):.9f}, {float(ahi):.9f}]")
    say(f"  check RHS(a*) = 27 exactly: a*^2 + 3a* + 2 = 52 + 2 = 54, 54/2 = 27")
    say(f"  window width 6 - a* in [{float(6 - ahi):.9f}, {float(6 - alo):.9f}]")
    say()
    say("An equality theorem excludes ONLY the single side length a = a*, where")
    say("slack is exactly 0.  For a in (a*, 6) Oler's RHS is strictly between 27")
    say("and 28, so 27 points are permitted with strictly positive slack and no")
    say("equality statement of any kind applies.  Numbers:")
    for t in (0, 1, 2, 5, 10, 13):
        a = alo + F(t, 100)
        rhs = (a * a + 3 * a + 2) / 2
        say(f"  a={float(a):.6f}  Oler RHS={float(rhs):.6f}  "
            f"slack at n=27 = {float(rhs - 27):.6f}")
    say()
    say("The epsilon-scale: a theorem 'deficit >= eps at n=27' gives")
    say("d(27) >= a_eps = (-3 + sqrt(217 + 8 eps))/2.  Erdos-Oler k=7 is eps = 1.")
    for e in (F(0), F(1, 4), F(1, 2), F(3, 4), F(1)):
        lo, hi = sqrt_bounds(F(217) + 8 * e, 12)
        say(f"  eps={str(e):>4}  a_eps in [{float((lo-3)/2):.9f}, "
            f"{float((hi-3)/2):.9f}]")
    say()
    say("So: to exclude n=27 for every a<6 one needs the deficit to reach 1,")
    say("not 0+.  Deficit >= 1 at a<6 is *literally equivalent* to Erdos-Oler")
    say("k=7, since RHS is strictly increasing in a and RHS(6) = 28 = 27 + 1.")


# ---------------------------------------------------------------------------
# 7. control: perturbed lattice (re-derivation of W1; priority: eo-boundary-counting)
# ---------------------------------------------------------------------------
def perturbed_lattice_control():
    head("7. Control: face excess at a lattice whose corners are pushed out")
    say("Independent re-derivation of eo-boundary-counting §4 (W1) by a different")
    say("construction (move the three CORNERS outward rather than the edges in).")
    say("Priority is theirs; this is a control on my own reasoning, not a claim.")
    say()
    say("Construction: T(k) lattice, side a0=k-1, centroid g.  Replace each of the")
    say("three corner points c by g + lam*(c-g), lam = 1 + delta/a0.  Every other")
    say("point stays.  Hull becomes the equilateral triangle of side a0+delta and")
    say("b drops to 3.")
    say()
    say(f"{'k':>3}{'delta':>9}{'n':>4}{'a':>10}{'b':>4}  {'min sep^2':>11}  "
        f"{'face excess FE':>16}  {'total slack':>24}")
    for delta, k in ((F(1, 5), 3), (F(1, 5), 7), (F(1, 100), 3),
                     (F(1, 100), 7), (F(1, 1000), 7)):
        a0 = k - 1
        pts = tri_lattice(k)
        gx = sum((p[0] for p in pts[1:]), pts[0][0]) / Alg.rational(len(pts))
        gy = sum((p[1] for p in pts[1:]), pts[0][1]) / Alg.rational(len(pts))
        corners = {lat(0, 0), lat(a0, 0), lat(0, a0)}
        lam = Alg.rational(1 + F(delta, a0))
        newpts = []
        for p in pts:
            if p in corners:
                newpts.append((gx + lam * (p[0] - gx), gy + lam * (p[1] - gy)))
            else:
                newpts.append(p)
        hv = hull(newpts)
        b = len(boundary_points(newpts, hv))
        n = len(newpts)
        A2 = area2(hv)
        term = A2 / SQ3                      # (2/sqrt3) A
        FE = term - Alg.rational(F(2 * n - b - 2, 2))
        sl, _, _, _ = slack_ival(newpts, 60)
        say(f"{k:>3}{float(delta):>9.4f}{n:>4}{float(a0 + delta):>10.4f}{b:>4}  "
            f"{min_sep2(newpts).float():>11.6f}  {FE.float():>16.6f}  "
            f"[{float(sl.lo):>11.7f},{float(sl.hi):>11.7f}]")
    say()
    say("FE is negative and grows like -3(k-2)/2 while the TOTAL Oler slack stays")
    say("O(delta).  So face-excess nonnegativity fails on configurations that are")
    say("arbitrarily close to Oler-extremal, with the hull an equilateral triangle")
    say("and all three of its corners occupied.  Same conclusion as W1.")


def main():
    ok1 = lemmaT_scan()
    ok2 = lemmaT_algebra()
    lattice_convex_cases()
    ok4 = tau_check()
    theoremD()
    scope()
    perturbed_lattice_control()
    head("Summary")
    say(f"K1  Lemma T + equality classification survived every exact check : {ok1}")
    say(f"    proof algebra (identity + vertex step) checked               : {ok2}")
    say(f"K3  tau-identity reproduced exactly                              : {ok4}")
    with open("out/report.txt", "w") as fh:
        fh.write("\n".join(OUT) + "\n")


if __name__ == "__main__":
    main()
