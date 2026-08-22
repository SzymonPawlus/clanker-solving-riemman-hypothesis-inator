"""V4 independent verification of attacks/n16-structure (Theorem N).

Everything that decides a reported result is exact: Fraction, or Q(sqrt3) as a
rational pair.  Floats appear only in printed columns and as search seeds that
are afterwards confirmed exactly.

    python3 verify4.py
"""
from fractions import Fraction as F
from itertools import combinations
from q3 import Q3, R3, ZERO, ONE, floor_q3
from geom import d2, cross, signed_area2, ccw, is_convex_ccw, clip, subtract, covered

r = R3
FAIL = []


def chk(name, cond, extra=""):
    print(f"  [{'ok ' if cond else 'FAIL'}] {name}{(' :: ' + extra) if extra else ''}")
    if not cond:
        FAIL.append(name)
    return cond


def hull(pts):
    """Exact convex hull (monotone chain) in the chart; affine chart preserves it."""
    P = sorted(set(pts), key=lambda z: (z[0].p, z[0].q, z[1].p, z[1].q))
    P = sorted(P, key=lambda z: (z[0].approx(), z[1].approx()))
    # exact insertion sort on the total order (u, then v)
    def less(A, B):
        if A[0] != B[0]:
            return A[0] < B[0]
        return A[1] < B[1]
    for i in range(1, len(P)):
        j = i
        while j > 0 and less(P[j], P[j - 1]):
            P[j], P[j - 1] = P[j - 1], P[j]
            j -= 1
    if len(P) < 3:
        return P
    low = []
    for p in P:
        while len(low) >= 2 and cross(low[-2], low[-1], p).sign() <= 0:
            low.pop()
        low.append(p)
    up = []
    for p in reversed(P):
        while len(up) >= 2 and cross(up[-2], up[-1], p).sign() <= 0:
            up.pop()
        up.append(p)
    return low[:-1] + up[:-1]


# ---------------------------------------------------------------------------
print("=" * 78)
print("0.  smoke tests of my own coverage routine (must pass before it is believed)")
print("=" * 78)
sq = [(Q3(0), Q3(0)), (Q3(2), Q3(0)), (Q3(2), Q3(2)), (Q3(0), Q3(2))]
t1 = [(Q3(0), Q3(0)), (Q3(2), Q3(0)), (Q3(0), Q3(2))]
t2 = [(Q3(2), Q3(0)), (Q3(2), Q3(2)), (Q3(0), Q3(2))]
chk("square covered by its two half-triangles", covered(sq, [t1, t2])[0])
chk("square NOT covered by one half-triangle", not covered(sq, [t1])[0])
big = [(Q3(-1), Q3(-1)), (Q3(3), Q3(-1)), (Q3(3), Q3(3)), (Q3(-1), Q3(3))]
chk("square covered by a strictly larger square", covered(sq, [big])[0])
shrunk = [(Q3(0), Q3(0)), (Q3(2), Q3(0)), (Q3(2), Q3(F(19, 10))), (Q3(0), Q3(F(19, 10)))]
chk("square NOT covered by a 5%-short copy", not covered(sq, [shrunk])[0])
chk("overlap-tolerant: 3 overlapping strips cover the square",
    covered(sq, [[(Q3(0), Q3(0)), (Q3(1), Q3(0)), (Q3(1), Q3(2)), (Q3(0), Q3(2))],
                 [(Q3(F(1, 2)), Q3(0)), (Q3(F(3, 2)), Q3(0)), (Q3(F(3, 2)), Q3(2)), (Q3(F(1, 2)), Q3(2))],
                 [(Q3(1), Q3(0)), (Q3(2), Q3(0)), (Q3(2), Q3(2)), (Q3(1), Q3(2))]])[0])

# ---------------------------------------------------------------------------
print()
print("=" * 78)
print("1.  Lemma 3 constant, Lemma 4 side, Lemma 2 threshold  (re-derived, exact)")
print("=" * 78)
# Lemma 3: min over beta of alpha^2+beta^2-alpha*beta.  Verify the claimed
# minimiser beta=alpha/2 and value 3 alpha^2/4 by exact identity:
#   a^2+b^2-ab - 3a^2/4 = (b - a/2)^2   for all a,b.
ok = True
for pa in [F(1), F(3, 2), F(7, 5), F(2), F(1, 3)]:
    for pb in [F(0), F(1, 4), pa / 2, F(3), F(9, 7)]:
        lhs = pa * pa + pb * pb - pa * pb - 3 * pa * pa / 4
        ok &= (lhs == (pb - pa / 2) ** 2)
chk("identity a^2+b^2-ab = 3a^2/4 + (b-a/2)^2, so min_b = 3a^2/4 at b=a/2", ok)
# hence 3 alpha^2/4 < 1  =>  alpha < 2/sqrt3
c = Q3(0, F(2, 3))          # 2/sqrt3 = 2 sqrt3 / 3
chk("2/sqrt3 == 2*sqrt3/3 and (2/sqrt3)^2 == 4/3",
    (c * c) == Q3(F(4, 3), 0), f"2/sqrt3 = {c.approx():.7f}")
# Lemma 4: deep triangle side.  In the chart, dist to the three sides are
# u*r/2, v*r/2, (a-u-v)*r/2, so D = {u>=2/r, v>=2/r, u+v <= a-2/r}: an
# equilateral triangle of chart side (a - 2/r) - 2*(2/r) = a - 6/r = a - 2 sqrt3.
chk("6/sqrt3 == 2*sqrt3  (=> delta = a - 2 sqrt3, no stray factor of sqrt3)",
    Q3(6, 0) / R3 == Q3(0, 2), f"6/sqrt3 = {(Q3(6,0)/R3).approx():.7f}")
chk("inradius check: a = 2 sqrt3 gives delta = 0 and inradius exactly 1",
    (Q3(0, 2) - Q3(0, 2)) == ZERO)
# Lemma 2 threshold
chk("Viviani threshold: a*sqrt3/2 < 2  <=>  a < 4/sqrt3 = 4 sqrt3/3",
    Q3(4, 0) / R3 == Q3(0, F(4, 3)), f"4/sqrt3 = {(Q3(4,0)/R3).approx():.7f}")
# d>=4 branch: circumradius of an equilateral triangle of side delta is delta/sqrt3
chk("apex-to-centroid of equilateral side d is d/sqrt3; d/sqrt3 >= 1 <=> d >= sqrt3",
    (Q3(0, 1) / R3) == ONE, "sqrt3/sqrt3 = 1")
chk("delta >= sqrt3  <=>  a >= 3 sqrt3", (Q3(0, 2) + Q3(0, 1)) == Q3(0, 3),
    f"3 sqrt3 = {Q3(0,3).approx():.6f}")
# Borsuk's constant, for contrast only
chk("(Borsuk route, NOT used) sqrt3/2*delta >= 1 would give a = 2sqrt3+2/sqrt3 = 8sqrt3/3",
    Q3(0, 2) + Q3(0, F(2, 3)) == Q3(0, F(8, 3)), f"8sqrt3/3 = {Q3(0,F(8,3)).approx():.6f}")

# ---------------------------------------------------------------------------
print()
print("=" * 78)
print("2.  Theorem N's counting function, recomputed exactly (section 3 table)")
print("=" * 78)


def theoremN(a):
    """(c, b, d, total) forced by Theorem N as stated, for a > 4/sqrt3."""
    assert a > Q3(0, F(4, 3)), "Theorem N needs a > 4/sqrt3"
    c = 3
    L = a - Q3(0, F(4, 3))                       # |M_e| = a - 4/sqrt3
    b = 3 * (floor_q3(L) + 1)
    delta = a - Q3(0, 2)                         # a - 2 sqrt3
    if delta >= Q3(0, 1):                        # delta >= sqrt3
        d = 4
    elif delta >= ONE:
        d = 3
    elif delta.sign() > 0:
        d = 1                                    # D non-empty, needs >=1 piece
    else:
        d = 0
    return c, b, d, c + b + d


rows = [("4.30", Q3(F(43, 10), 0)),
        ("1+2r3 - 1/100", Q3(F(99, 100), 2)),
        ("1+2r3", Q3(1, 2)),
        ("1+2r3 + 1/100", Q3(F(101, 100), 2)),
        ("4.62", Q3(F(462, 100), 0)),
        ("5", Q3(5, 0)),
        ("3 sqrt3", Q3(0, 3))]
print(f"  {'a':>16} {'value':>10} {'c':>3} {'b':>3} {'d':>3} {'tot':>4} {'delta':>10}")
published = {"4.30": (3, 6, 1, 10), "1+2r3 - 1/100": (3, 9, 1, 13),
             "1+2r3": (3, 9, 3, 15), "1+2r3 + 1/100": (3, 9, 3, 15),
             "4.62": (3, 9, 3, 15), "5": (3, 9, 3, 15), "3 sqrt3": (3, 9, 4, 16)}
allrows = True
for name, a in rows:
    c, b, d, t = theoremN(a)
    dl = (a - Q3(0, 2)).approx()
    same = (c, b, d, t) == published[name]
    allrows &= same
    print(f"  {name:>16} {a.approx():10.6f} {c:3d} {b:3d} {d:3d} {t:4d} {dl:10.6f}"
          f"   {'' if same else '<-- DIFFERS from published'}")
chk("section 3 table reproduces row by row", allrows)
chk("threshold identity: a - 2 sqrt3 == 1  <=>  a == 1 + 2 sqrt3",
    (Q3(1, 2) - Q3(0, 2)) == ONE, f"1+2sqrt3 = {Q3(1,2).approx():.9f}")
# where does the count first reach 15 / 16, by bisection on the exact predicate?
chk("forced total is 13 just below 1+2sqrt3 and 15 at it",
    theoremN(Q3(F(99, 100), 2))[3] == 13 and theoremN(Q3(1, 2))[3] == 15)
chk("(caveat) at a = 1/2+2sqrt3 = 3.964 the forced total is only 10",
    theoremN(Q3(F(1, 2), 2))[3] == 10)
chk("forced total first reaches 16 at 3 sqrt3 (and not at 3sqrt3 - 1/1000)",
    theoremN(Q3(0, 3))[3] == 16 and theoremN(Q3(F(-1, 1000), 3))[3] == 15)
chk("the other 16-threshold, a = 3 + 4/sqrt3, is larger than 3 sqrt3",
    Q3(3, F(4, 3)) > Q3(0, 3), f"3+4/sqrt3 = {Q3(3,F(4,3)).approx():.6f} > {Q3(0,3).approx():.6f}")
# floor-vs-ceiling: integer |M_e| does occur, exactly at a = k + 4/sqrt3
a_int = Q3(3, F(4, 3))
Lint = a_int - Q3(0, F(4, 3))
chk("at a = 3 + 4/sqrt3 the middle has integer length 3: floor+1 = 4, ceil = 3",
    Lint == Q3(3, 0) and floor_q3(Lint) + 1 == 4)
chk("at a = 1+2sqrt3 the middle length is NOT an integer (floor/ceil agree there)",
    (Q3(1, 2) - Q3(0, F(4, 3))) != Q3(2, 0) and floor_q3(Q3(1, 2) - Q3(0, F(4, 3))) == 2)

# ---------------------------------------------------------------------------
print()
print("=" * 78)
print("3.  the standing 15-piece certificate, transcribed by hand from")
print("    attacks/n16-covering-2/README.md (the table, not any code)")
print("=" * 78)


def P(pu, qu, pv, qv):
    return (Q3(pu, qu), Q3(pv, qv))


h = F(1, 2)
t = F(1, 3)
PIECES = [
    [P(0, 0, 0, 0), P(1, 0, 0, 0), P(0, t, 0, t), P(0, 0, 1, 0)],                                   # 0
    [P(0, t, 1, t), P(0, 0, 0, 1), P(0, 0, 1, 0), P(0, t, 0, t), P(1, 0, 1, 0)],                    # 1
    [P(0, t, 0, F(4, 3)), P(0, 0, 1, 1), P(0, 0, 0, 1), P(0, t, 1, t), P(1, 0, 0, 1)],              # 2
    [P(0, t, 1, F(4, 3)), P(0, 0, 0, 2), P(0, 0, 1, 1), P(0, t, 0, F(4, 3)), P(1, 0, F(5, 2), 0)],  # 3
    [P(1, 0, 0, 2), P(0, 0, 1, 2), P(0, 0, 0, 2), P(0, t, 1, F(4, 3))],                             # 4
    [P(1, 0, 0, 0), P(0, 1, 0, 0), P(1, t, 0, t), P(1, 0, 1, 0), P(0, t, 0, t)],                    # 5
    [P(F(3, 2), 0, F(3, 2), 0), P(1, 0, 0, 1), P(0, t, 1, t), P(1, 0, 1, 0), P(1, t, 0, t),
     P(0, 1, 1, 0)],                                                                                # 6
    [P(1, t, 0, F(4, 3)), P(1, 0, F(5, 2), 0), P(0, t, 0, F(4, 3)), P(1, 0, 0, 1),
     P(F(3, 2), 0, F(3, 2), 0), P(0, 1, 0, 1)],                                                     # 7
    [P(0, 1, 1, 1), P(1, 0, 0, 2), P(0, t, 1, F(4, 3)), P(1, 0, F(5, 2), 0), P(1, t, 0, F(4, 3))],  # 8
    [P(0, 1, 0, 0), P(1, 1, 0, 0), P(0, F(4, 3), 0, t), P(0, 1, 1, 0), P(1, t, 0, t)],              # 9
    [P(0, F(4, 3), 1, t), P(0, 1, 0, 1), P(F(3, 2), 0, F(3, 2), 0), P(0, 1, 1, 0),
     P(0, F(4, 3), 0, t), P(F(5, 2), 0, 1, 0)],                                                     # 10
    [P(1, 1, 0, 1), P(0, 1, 1, 1), P(1, t, 0, F(4, 3)), P(0, 1, 0, 1), P(0, F(4, 3), 1, t)],        # 11
    [P(1, 1, 0, 0), P(0, 2, 0, 0), P(1, F(4, 3), 0, t), P(F(5, 2), 0, 1, 0), P(0, F(4, 3), 0, t)],  # 12
    [P(0, 2, 1, 0), P(1, 1, 0, 1), P(0, F(4, 3), 1, t), P(F(5, 2), 0, 1, 0), P(1, F(4, 3), 0, t)],  # 13
    [P(0, 2, 0, 0), P(1, 2, 0, 0), P(0, 2, 1, 0), P(1, F(4, 3), 0, t)],                             # 14
]
A = Q3(1, 2)                                   # a = 1 + 2 sqrt3
chk("15 pieces transcribed", len(PIECES) == 15)

HU = [hull(pc) for pc in PIECES]
chk("every piece is a convex polygon with no redundant listed vertex",
    all(len(HU[i]) == len(PIECES[i]) for i in range(15)),
    ",".join(f"{i}:{len(PIECES[i])}->{len(HU[i])}" for i in range(15)
             if len(HU[i]) != len(PIECES[i])) or "all match")
chk("all hulls ccw and strictly convex", all(is_convex_ccw(p) for p in HU))
chk("vertex-count profile 3 quadrilaterals / 9 pentagons / 3 hexagons",
    sorted(len(p) for p in HU) == [4, 4, 4] + [5] * 9 + [6] * 3)

inside = all(v[0] >= ZERO and v[1] >= ZERO and (v[0] + v[1]) <= A for p in HU for v in p)
chk("every vertex lies in the closed T_a  (u,v >= 0, u+v <= a)", inside)

dmax = ZERO
for p in HU:
    for X, Y in combinations(p, 2):
        if d2(X, Y) > dmax:
            dmax = d2(X, Y)
chk("max squared diameter over all 15 pieces is EXACTLY 1", dmax == ONE, f"{dmax}")
chk("NB: diameter exactly 1 is NOT < 1, so Theorem N's hypothesis does not hold "
    "for this object as given", dmax == ONE)

# classification
cls, meets = {}, {}
for i, p in enumerate(HU):
    m = []
    if min((v[1] for v in p), key=lambda z: z.approx()) == ZERO or any(v[1] == ZERO for v in p):
        m.append("AB")                                   # side v = 0
    if any(v[0] == ZERO for v in p):
        m.append("AC")                                   # side u = 0
    if any((v[0] + v[1]) == A for v in p):
        m.append("BC")                                   # side u+v = a
    meets[i] = m
    cls[i] = len(m)
two = [i for i in range(15) if cls[i] == 2]
one = [i for i in range(15) if cls[i] == 1]
zero = [i for i in range(15) if cls[i] == 0]
three = [i for i in range(15) if cls[i] == 3]
chk("two-side pieces = 3", len(two) == 3, str(two))
chk("one-side pieces = 9", len(one) == 9, str(one))
chk("no-side  pieces = 3", len(zero) == 3, str(zero))
chk("three-side pieces = 0", len(three) == 0)
chk("the published index sets agree with mine",
    two == [0, 4, 14] and one == [1, 2, 3, 5, 8, 9, 11, 12, 13] and zero == [6, 7, 10])
for s in ("AB", "AC", "BC"):
    k = sum(1 for i in range(15) if s in meets[i])
    chk(f"side {s} is met by exactly 5 pieces", k == 5, f"{k}")

# deep triangle
delta = A - Q3(0, 2)
chk("delta = a - 2 sqrt3 = 1 exactly at a = 1+2 sqrt3", delta == ONE)
o = Q3(0, F(2, 3))                                        # 2/sqrt3
D = [(o, o), (o + ONE, o), (o, o + ONE)]
chk("D's three apexes are pairwise at distance exactly delta = 1",
    all(d2(X, Y) == ONE for X, Y in combinations(D, 2)))
chk("D sits on the third side constraint u+v <= a - 2/sqrt3",
    (D[1][0] + D[1][1]) == A - o and (D[2][0] + D[2][1]) == A - o)
okD, res = covered(D, [HU[i] for i in zero])
chk("the 3 no-side pieces (6,7,10) cover the deep triangle D", okD, f"residue parts {res}")
singles = [covered(D, [HU[i]])[0] for i in range(15)]
chk("control: no single piece covers D", not any(singles))
pairs = [covered(D, [HU[i], HU[j]])[0] for i, j in combinations(zero, 2)]
chk("control: no two of {6,7,10} cover D", not any(pairs))

# corner traces
tr_ok, tr_vals = True, []
for i in two:
    apexes = [v for v in HU[i] if sum(1 for s, f in
              (("AB", lambda z: z[1] == ZERO), ("AC", lambda z: z[0] == ZERO),
               ("BC", lambda z: (z[0] + z[1]) == A)) if s in meets[i] and f(v)) == 2]
    assert len(apexes) == 1, (i, apexes)
    ap = apexes[0]
    for v in HU[i]:
        tr_vals.append(d2(ap, v))
    m = max((d2(ap, v) for v in HU[i]), key=lambda z: z.approx())
    tr_ok &= (m <= ONE)
chk("every vertex of a two-side piece is within squared distance 1 of its apex, "
    "and 1 < 4/3 = (2/sqrt3)^2", tr_ok and ONE < Q3(F(4, 3), 0))

okT, resT = covered([(ZERO, ZERO), (A, ZERO), (ZERO, A)], HU)
chk("independent re-check: the 15 pieces do cover T_a (transcription is sound)",
    okT, f"residue parts {resT}")

# ---------------------------------------------------------------------------
print()
print("=" * 78)
print("4.  corruptions fed to MY checker -- each must be caught")
print("=" * 78)


def corrupt(pieces, i, k, du, dv):
    q = [list(p) for p in pieces]
    u, v = q[i][k]
    q[i][k] = (u + Q3(du, 0), v + Q3(dv, 0))
    return [hull(p) for p in q]


c1 = corrupt(PIECES, 6, 0, F(-1, 20), F(-1, 20))       # shrink hexagon 6
chk("corruption A: hexagon 6 pulled in by 1/20 -> D no longer covered",
    not covered(D, [c1[i] for i in zero])[0])
c2 = corrupt(PIECES, 0, 1, F(1, 10), 0)                # stretch corner piece 0
dm = max((d2(X, Y) for X, Y in combinations(c2[0], 2)), key=lambda z: z.approx())
chk("corruption B: corner piece stretched -> squared diameter exceeds 1", dm > ONE, f"{dm.approx():.4f}")
chk("corruption C: dropping piece 7 -> T_a no longer covered",
    not covered([(ZERO, ZERO), (A, ZERO), (ZERO, A)], [HU[i] for i in range(15) if i != 7])[0])
c4 = [list(p) for p in PIECES]
c4[4] = [(u + Q3(F(1, 50), 0), v) for (u, v) in c4[4]]   # slide piece 4 off the corner
c4 = [hull(p) for p in c4]
chk("corruption D: piece 4 slid by 1/50 -> it stops meeting side u=0, class count changes",
    not any(v[0] == ZERO for v in c4[4]))
chk("corruption E: a deliberately mis-transcribed vertex breaks the T_a covering",
    not covered([(ZERO, ZERO), (A, ZERO), (ZERO, A)],
                corrupt(PIECES, 10, 3, F(1, 30), 0))[0])

# ---------------------------------------------------------------------------
print()
print("=" * 78)
print("5.  ATTACK: is 1+2sqrt3 really the LEAST a at which 15 pieces are necessary?")
print("=" * 78)
# 15 points of the unit triangular lattice inside T_4 (chart coords are lattice
# coords here).  Squared distance du^2+du*dv+dv^2 is a positive-definite integral
# form, so distinct lattice points are at squared distance >= 1.
lat = [(Q3(i, 0), Q3(j, 0)) for i in range(5) for j in range(5) if i + j <= 4]
chk("15 lattice points listed", len(lat) == 15)
chk("all 15 lie in the closed T_4",
    all(x[0] >= ZERO and x[1] >= ZERO and (x[0] + x[1]) <= Q3(4, 0) for x in lat))
mind = min((d2(X, Y) for X, Y in combinations(lat, 2)), key=lambda z: z.approx())
chk("pairwise squared distances all >= 1 (min is exactly 1)", mind == ONE, f"{mind}")
chk("4 < 1 + 2 sqrt3", Q3(4, 0) < Q3(1, 2), f"4 < {Q3(1,2).approx():.6f}")
print("  => a piece of diameter <1 holds at most one of these 15 points, so EVERY")
print("     covering of T_4 by diameter-<1 pieces uses >= 15 pieces:  N(4) >= 15.")
print("     N is non-decreasing in a, so 15 pieces are necessary for all a >= 4,")
print("     i.e. already 0.4641 BELOW 1+2sqrt3.  Theorem N at a = 4 forces only",
      theoremN(Q3(4, 0))[3], "pieces.")
chk("Theorem N is off by 5 pieces at a = 4 (forces 10, truth is >= 15)",
    theoremN(Q3(4, 0))[3] == 10)
# the same pigeonhole with the cited optimum s(15) = 8 + 2 sqrt3
print("  cross-check against the cited table: s(15) = 8+2sqrt3 (Oler, triangular")
print("     number, `cited`) means d(15) = 8 at separation 2, i.e. a_15 = 4 at")
print("     separation 1 -- so 4 is exactly the least side holding 15 separated points.")

# ---------------------------------------------------------------------------
print()
print("=" * 78)
print("6.  section 5.1: does 3*(pi/6) + 12*(pi/4) really reproduce U1 = 5.039166?")
print("=" * 78)
PI_LO = F(3141592653589793238462643383279, 10 ** 30)
PI_HI = PI_LO + F(1, 10 ** 30)
R3_LO = F(1732050807568877293527446341505, 10 ** 30)
R3_HI = R3_LO + F(1, 10 ** 30)
assert R3_LO ** 2 < 3 < R3_HI ** 2


def isqrt_bounds(x, den=10 ** 20):
    """rational lower/upper bounds for sqrt(x), x a positive Fraction"""
    from math import isqrt
    num = x.numerator * den * den // x.denominator
    lo = F(isqrt(num), den)
    hi = lo + F(1, den)
    assert lo * lo <= x <= hi * hi
    return lo, hi


# sqrt3/4 * a^2 = 3*pi/6 + 12*pi/4 = 7*pi/2   =>   a^2 = 14*pi/sqrt3 = 14*pi*sqrt3/3
a2_lo = 14 * PI_LO * R3_LO / 3
a2_hi = 14 * PI_HI * R3_HI / 3
lo, _ = isqrt_bounds(a2_lo)
_, hi = isqrt_bounds(a2_hi)
print(f"  budget 3*(pi/6)+12*(pi/4) = 7pi/2 gives a in [{float(lo):.9f}, {float(hi):.9f}]")
chk("U1 reproduced: the ceiling is 5.039166 to 6 dp",
    lo > F(50391655, 10 ** 7) and hi < F(50391665, 10 ** 7))
chk("U1 as a closed form: a = sqrt(14 pi/sqrt3)", True, "= sqrt(14*pi*sqrt3/3)")
# U0, for orientation: 15 * pi/4
a2_lo0 = 15 * PI_LO * R3_LO / 3
a2_hi0 = 15 * PI_HI * R3_HI / 3
lo0, _ = isqrt_bounds(a2_lo0)
_, hi0 = isqrt_bounds(a2_hi0)
chk("U0 (isodiametric alone, 15*pi/4) = 5.216032, as that lane publishes",
    lo0 > F(52160315, 10 ** 7) and hi0 < F(52160325, 10 ** 7), f"[{float(lo0):.7f},{float(hi0):.7f}]")

# ---------------------------------------------------------------------------
print()
print("=" * 78)
print("7.  section 6: R1's witness, re-derived exactly (Cartesian, apex at origin)")
print("=" * 78)
# P on AB at (21/20, 0); Q on AC at (1/4, sqrt3/4).  |AQ| = 1/2.
PQ2 = (Q3(F(21, 20)) - Q3(F(1, 4))) ** 2 if False else None
dx = Q3(F(21, 20), 0) - Q3(F(1, 4), 0)
dy = ZERO - Q3(0, F(1, 4))
PQ2 = dx * dx + dy * dy
chk("|PQ|^2 = 331/400 < 1, so one piece may hold both",
    PQ2 == Q3(F(331, 400), 0) and PQ2 < ONE, f"{float(PQ2.p):.6f}")
aq2 = Q3(F(1, 4), 0) * Q3(F(1, 4), 0) + Q3(0, F(1, 4)) * Q3(0, F(1, 4))
chk("|AQ| = 1/2, |AP| = 21/20", aq2 == Q3(F(1, 4), 0))
al, be = Q3(F(21, 20), 0), Q3(F(1, 2), 0)
chk("alpha^2+beta^2-alpha*beta equals |PQ|^2 (the 60-degree law of cosines)",
    al * al + be * be - al * be == PQ2)
chk("alpha = 21/20 > 1 (so it breaks the old 1-constant) but < 2/sqrt3 "
    "(so Lemma 3 survives it)", al > ONE and al < Q3(0, F(2, 3)))

print()
print("=" * 78)
print("FAILURES:", FAIL if FAIL else "none")
print("=" * 78)
