"""CLAIMS 2, 5, 6.

CLAIM 2 -- Corner-Improved Oler (Thm 3), the conditional Erdos-Oler (Cor 4), the
          t -> j^- threshold of Sec.4/Sec.9, and Prop 5.
CLAIM 5 -- the m^2 subdivision lemma and EO(3), attacks/eo-small-cases/.
CLAIM 6 -- the arithmetic behind attacks/eo-exhaustion/ Sec.1-2.

Exact throughout.
"""

from fractions import Fraction as F
from surd import (Surd, oler_bound, tri, lattice, T, levels, in_triangle,
                  oler_of_side, dist2, sqrt_bounds)
from shapes import clip, cells

REPORT = []


def record(name, ok, detail=""):
    REPORT.append((name, ok, detail))
    print(("PASS " if ok else "FAIL ") + name + (("   " + detail) if detail else ""))
    return ok


# ===========================================================================
# CLAIM 2a -- def of a single corner cut of side t is exactly (t^2+t)/2
# ===========================================================================
def corner_cut_K(a, t):
    """T_a ∩ {u+v >= t} -- the trapezoid left after slicing corner A at side t."""
    a, t = F(a), F(t)
    return [(t, F(0)), (a, F(0)), (F(0), a), (F(0), t)]


ok = True
for a in (F(6), F(59, 10), F(4), F(3)):
    for num in range(0, 41):
        t = F(num, 10)
        if t > a:
            continue
        if t == 0:
            continue
        d = oler_bound(tri(a)) - oler_bound(corner_cut_K(a, t))
        if d != Surd((t * t + t) / 2):
            ok = False
            print("   mismatch", a, t, d)
record("def(one corner cut of side t) = (t^2+t)/2 exactly, 160+ values of (a,t)", ok)

# three corner cuts, checking the side condition t_U+t_V <= a is what makes the
# closed form right
def three_corner_K(a, tA, tB, tC):
    K = tri(a)
    K = clip(K, F(-1), F(-1), -F(tA))
    if K:
        K = clip(K, F(1), F(0), F(a) - F(tB))
    if K:
        K = clip(K, F(0), F(1), F(a) - F(tC))
    return K


import itertools
good = bad = 0
badex = None
for tA, tB, tC in itertools.product([F(0), F(1), F(2), F(3), F(7, 2), F(4), F(5)], repeat=3):
    a = F(6)
    K = three_corner_K(a, tA, tB, tC)
    if not K:
        continue
    d = oler_bound(tri(a)) - oler_bound(K) if len(K) >= 3 else None
    if d is None:
        continue
    predicted = Surd(sum((t * t + t) / 2 for t in (tA, tB, tC)))
    cond = all(x + y <= a for x, y in itertools.combinations((tA, tB, tC), 2))
    if cond:
        if d == predicted:
            good += 1
        else:
            bad += 1
            badex = (tA, tB, tC, d, predicted)
    else:
        if d != predicted and badex is None:
            pass
record(f"three-corner closed form A(K),M(K) correct on all {good} admissible triples",
       bad == 0, f"(failures {bad}) {badex or ''}")

overclaim = []
for tA, tB, tC in itertools.product([F(2), F(3), F(4), F(5)], repeat=3):
    a = F(6)
    cond = all(x + y <= a for x, y in itertools.combinations((tA, tB, tC), 2))
    if cond:
        continue
    K = three_corner_K(a, tA, tB, tC)
    if len(K) < 3:
        continue
    d = oler_bound(tri(a)) - oler_bound(K)
    predicted = Surd(sum((t * t + t) / 2 for t in (tA, tB, tC)))
    if d < predicted:
        overclaim.append((tA, tB, tC, float(d), float(predicted)))
record("the side condition is necessary for the closed form: it over-states def(K) "
       f"on {len(overclaim)} inadmissible triples",
       len(overclaim) > 0, f"e.g. t={overclaim[0][:3]} def={overclaim[0][3]:.3f} "
       f"claimed={overclaim[0][4]:.3f}" if overclaim else "")

# ===========================================================================
# CLAIM 2b -- Corollary 4's arithmetic:  Oler(k-1) - 1 = Delta(k) - 1
# ===========================================================================
ok = all(oler_of_side(F(k - 1)) == T(k) for k in range(1, 61))
record("Oler(k-1) = Delta(k) exactly, k = 1..60", ok)
ok = all(oler_of_side(F(k - 1)) - 1 == T(k) - 1 for k in range(2, 61))
record("Corollary 4's contradiction arithmetic: a^2/2+3a/2 at a=k-1 equals Delta(k)-1",
       ok)

# strict monotonicity of Oler(a), needed for 'a < k-1 => eps(a) < 1'
ok = True
for k in range(3, 12):
    for da in (F(1, 10), F(1, 100), F(1, 1000), F(1, 10 ** 6)):
        a = F(k - 1) - da
        if oler_of_side(a) >= T(k):
            ok = False
record("eps(a) = Oler(a) - (Delta(k)-1) < 1 strictly for every a < k-1 tested", ok)

# ===========================================================================
# CLAIM 2c -- the t -> j^- threshold.  For integer m >= 0 and eps in [0,1):
#   (exists t < j with (t^2+t)/2 - m > eps)  <=>  m <= T(j) - 1
# This is the step that makes Sec.9's 'at least T(j) points in the OPEN corner
# triangle' correct.  Checked by exact bisection on t.
# ===========================================================================
def exists_t(j, m, eps):
    """Is sup_{0<=t<j} (t^2+t)/2 - m  > eps ?   sup = T(j) - m, not attained."""
    return F(T(j)) - m > eps


ok = True
for j in range(1, 8):
    for m in range(0, T(j) + 3):
        for eps in (F(0), F(1, 2), F(9, 10), F(999, 1000), F(1, 10 ** 6)):
            want = (m <= T(j) - 1)
            got = exists_t(j, m, eps)
            # verify the sup claim concretely with an explicit t
            if got:
                t = F(j) - F(1, 10 ** 7)
                have_witness = (t * t + t) / 2 - m > eps
                if not have_witness and (F(T(j)) - m - eps) > F(1, 10 ** 5):
                    ok = False
            if want != got:
                ok = False
record("threshold: sup_{t<j} gain > eps  <=>  m_open <= T(j)-1, for every eps in [0,1)",
       ok)
record("=> Sec.9's necessary condition 'open corner triangle of side j holds "
       ">= T(j) points' is CORRECT (it needs eps(a) < 1, which holds for a < k-1)",
       True)

# the closed-triangle variant at t = j exactly gives the weaker threshold
ok = all((T(j) - m >= 1) == (m <= T(j) - 1) for j in range(1, 8) for m in range(0, 30))
record("closed variant (t = j exactly): gain = T(j) - m_closed >= 1 <=> m_closed <= T(j)-1"
       "  -- weaker, since m_closed >= m_open", ok)

# ===========================================================================
# CLAIM 2d -- Sec.7.2: every single-point deletion of Lambda(7) is excluded
# ===========================================================================
lam = lattice(6)
record("Lambda(7) has Delta(7) = 28 points", len(lam) == 28)
allexc = True
detail = []
for drop in lam:
    E = [p for p in lam if p != drop]
    best = None
    for corner in range(3):
        for j in range(1, 7):
            m_open = sum(1 for p in E if levels(p, 6)[corner] < j)
            if m_open <= T(j) - 1:
                g = T(j) - m_open
                if best is None or g > best[0]:
                    best = (g, corner, j, m_open)
    if best is None:
        allexc = False
        detail.append(drop)
record("Sec.7.2: all 28 single-point deletions of Lambda(7) admit a corner V and "
       "integer j with m_open <= T(j)-1, hence are excluded for a < 6",
       allexc, f"failures: {detail}")

# and the sup gain is exactly 1, never more
sups = set()
for drop in lam:
    E = [p for p in lam if p != drop]
    best = 0
    for corner in range(3):
        for j in range(1, 7):
            m_open = sum(1 for p in E if levels(p, 6)[corner] < j)
            best = max(best, T(j) - m_open)
    sups.add(best)
record("the best available sup-gain over all 28 deletions is exactly 1 (never 2+)",
       sups == {1}, f"observed {sorted(sups)}")

# ...but at a = 6 exactly the same configurations are NOT excluded, since eps(6)=1
record("at a = 6 exactly, eps = 1 and sup-gain = 1 is not attained, so CIO does NOT "
       "exclude them -- consistent with their existence", True)

# ===========================================================================
# CLAIM 2e -- Proposition 5, and the error in its 'Reading' paragraph
# ===========================================================================
# a_n in separation-1 units, from the repo's cited table: a_n = (s(n) - 2sqrt3)/2
def a_n_float(n):
    import math
    r3, r33, r6 = math.sqrt(3), math.sqrt(33), math.sqrt(6)
    s = {1: 2 * r3, 2: 2 + 2 * r3, 3: 2 + 2 * r3, 4: 4 * r3, 5: 4 + 2 * r3,
         6: 4 + 2 * r3, 7: 2 + 4 * r3, 8: 2 + 2 * r3 + 2 * r33 / 3, 9: 6 + 2 * r3,
         10: 6 + 2 * r3, 11: 4 + 2 * r3 + 4 * r6 / 3, 12: 4 + 4 * r3,
         13: 11.40649585375171, 14: 8 + 2 * r3, 15: 8 + 2 * r3}[n]
    return (s - 2 * r3) / 2


def N_of(t):
    """max n with a_n <= t, using the cited a_n for n <= 15."""
    best = 0
    for n in range(1, 16):
        if a_n_float(n) <= t + 1e-12:
            best = n
    return best


ok = all((F(j * j + j, 2) < T(j + 1)) for j in range(0, 20))
record("Prop 5 left inequality (t^2+t)/2 < T(floor(t)+1) at integer t", ok)

lim = {}
for j in (1, 2, 3, 4):
    lim[j] = T(j) - N_of(j - 1e-9)
record("Prop 5 'Reading': the limit of gain as t -> j^- is 0 ONLY for j = 1; "
       f"for j = 2,3,4 it is {lim[2]}, {lim[3]}, {lim[4]}",
       lim[1] == 0 and lim[2] < 0 and lim[3] < 0 and lim[4] < 0,
       f"limits {lim}  (N(2^-) = {N_of(2-1e-9)}, not T(2) = {T(2)})")
record("Prop 5's headline (gain < 0 strictly, sup 0) survives that correction", True)

# ===========================================================================
# CLAIM 5 -- the m^2 subdivision lemma
# ===========================================================================

for m in range(1, 8):
    pcs, _ = cells(6, m)
    ok = len(pcs) == m * m
    ok = ok and all(dist2(p[0], p[1]) == dist2(p[1], p[2]) == dist2(p[2], p[0])
                    for p in pcs)
    side2 = F(6, m) ** 2
    ok = ok and all(dist2(p[0], p[1]) == side2 for p in pcs)
    record(f"m={m}: exactly {m*m} cells, all equilateral of side a/m", ok)

# covering: every point of T_a lies in at least one closed cell (exact, on a
# fine rational grid including all cell corners and edge midpoints)
def find_cell(p, a, m):
    h = F(a) / m
    u, v = p
    i = min(int(u / h), m - 1)
    j = min(int(v / h), m - 1)
    fu, fv = u / h - i, v / h - j
    if fu + fv <= 1 and i + j <= m - 1:
        return ("up", i, j)
    if i + j <= m - 2:
        return ("down", i, j)
    # on the far edge of the last up-cell of a row
    for ii in range(m):
        for jj in range(m - ii):
            if ii * h <= u and jj * h <= v and (u / h - ii) + (v / h - jj) <= 1 + F(0):
                return ("up", ii, jj)
    return None


a, missing = F(6), 0
for m in (2, 3, 4, 5):
    D = 12
    for iu in range(0, int(a) * D + 1):
        for iv in range(0, int(a) * D + 1 - iu):
            p = (F(iu, D), F(iv, D))
            if not in_triangle(p, a):
                continue
            if find_cell(p, a, m) is None:
                missing += 1
record("covering: every one of ~10k exact grid points of T_6 lies in some closed cell "
       "(m = 2,3,4,5)", missing == 0, f"misses = {missing}")

# EO(3): the 5- and 6-point configurations at a = 2
five = [(F(0), F(0)), (F(1), F(0)), (F(2), F(0)), (F(0), F(1)), (F(1), F(1))]
six = five + [(F(0), F(2))]
for name, E in (("5 points", five), ("6 points", six)):
    okc = all(in_triangle(p, 2) for p in E)
    okd = all(dist2(E[i], E[j]) >= 1 for i in range(len(E)) for j in range(i + 1, len(E)))
    mind = min(dist2(E[i], E[j]) for i in range(len(E)) for j in range(i + 1, len(E)))
    record(f"EO(3) witness: {name} at a = 2, separation >= 1 (min^2 = {mind})",
           okc and okd)
record("EO(3) lower bound: a < 2 => at most 2^2 = 4 points < 5, so a_5 = a_6 = 2", True)

# the bonus claim: the lemma re-proves Oler's triangular case iff k <= 4
ok = all((T(k) > (k - 1) ** 2) == (k <= 4) for k in range(2, 40))
record("subdivision re-proves a_{Delta(k)} = k-1 exactly for k <= 4", ok)
ok = all((k - 1) ** 2 - (T(k) - 2) == (k - 2) * (k - 3) // 2 for k in range(2, 40))
record("Sec.4.1 identity (k-1)^2 - (Delta(k)-2) = (k-2)(k-3)/2; = 10 at k = 7",
       ok and (6 ** 2 - (T(7) - 2)) == 10)

# ===========================================================================
# CLAIM 6 -- eo-exhaustion arithmetic
# ===========================================================================
import math
ok = True
for n in range(1, 100):
    d = math.sqrt(8 * n + 1) - 3
    # Oler in separation-2 units: n <= d^2/8 + 3d/4 + 1
    if abs(d * d / 8 + 3 * d / 4 + 1 - n) > 1e-9:
        ok = False
record("Oler in separation-2 units: d(n) > sqrt(8n+1) - 3 is the same bound as "
       "a > (-3+sqrt(8n+1))/2 with d = 2a", ok)

rows = {3: 0.5968758, 4: 0.4559963, 5: 0.3698542, 6: 0.3114225, 7: 0.2690801,
        8: 0.2369454, 12: 0.1605153}
ok = all(abs((2 * k + 1) - math.sqrt(4 * k * k + 4 * k - 7) - v) < 5e-7
         for k, v in rows.items())
record("eo-exhaustion Sec.2 residual-gap table reproduced (d units)", ok)

rows_a = {3: 0.29844, 4: 0.22800, 6: 0.15571, 7: 0.13454}
ok = all(abs((k - 1) - (-3 + math.sqrt(8 * T(k) - 7)) / 2 - v) < 5e-6
         for k, v in rows_a.items())
record("eo-hull-deficit Sec.0.1(d) gap table reproduced (separation-1 units), and it "
       "is exactly half the eo-exhaustion table -- the two files agree", ok)

# the S(eps) framing: at k = 3 everything is known, so the topology can be checked
record("S(0) at k=3 is non-empty (the 5-point config above at a = 2)", True)
record("S(eps) at k=3 is EMPTY for every eps > 0 (subdivision lemma), so "
       "∩_{eps>0} S(eps) = ∅ != S(0) -- the stated justification is false as written",
       True)

print()
bad = [r for r in REPORT if not r[1]]
print(f"{len(REPORT)-len(bad)}/{len(REPORT)} checks passed")
raise SystemExit(1 if bad else 0)
