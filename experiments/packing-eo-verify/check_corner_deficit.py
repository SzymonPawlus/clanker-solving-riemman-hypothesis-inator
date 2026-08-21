"""CLAIM 3 -- the Corner-Deficit Lemma of attacks/eo-hull-deficit/ Sec. 2.

    Lemma 1.  t_V = the side of the largest corner triangle at V free of points of
    E (i.e. t_V = min_{p in E} level_V(p)).  If t_U + t_V <= a for each pair of
    corners, then  def(H) >= sum_V (t_V^2 + t_V)/2,  where H = conv(E) and
    def(K) = B(T_a) - B(K).

Three things are tested:
  (i)  the lemma on random exact configurations satisfying the side condition;
  (ii) whether the side condition is *necessary* -- i.e. whether dropping it
       produces counterexamples (it does; explicit witnesses below);
  (iii) behaviour exactly at the boundary t_U + t_V = a.

Exact throughout; no separation hypothesis is used or needed.
"""

import random
from fractions import Fraction as F
from surd import (Surd, oler_bound, hull_oler_bound, tri, levels, in_triangle,
                  oler_of_side)

REPORT = []


def record(name, ok, detail=""):
    REPORT.append((name, ok, detail))
    print(("PASS " if ok else "FAIL ") + name + (("   " + detail) if detail else ""))
    return ok


def tvec(E, a):
    """(t_A, t_B, t_C) -- the largest point-free corner triangle side at each corner."""
    return tuple(min(levels(p, a)[i] for p in E) for i in range(3))


def deficit(E, a):
    return oler_bound(tri(a)) - hull_oler_bound(E)


def rhs(t):
    return Surd(sum((x * x + x) / 2 for x in t))


def side_condition(t, a):
    return all(t[i] + t[j] <= F(a) for i in range(3) for j in range(3) if i < j)


# ---------------------------------------------------------------------------
# (i) randomised exact test
# ---------------------------------------------------------------------------
random.seed(20260821)
sat = viol = 0
fail_sat = []
fail_viol = []
for trial in range(4000):
    a = random.choice([F(2), F(3), F(4), F(6), F(27, 10), F(59, 10)])
    n = random.randint(1, 7)
    E = []
    while len(E) < n:
        den = random.choice([1, 2, 3, 4, 6, 8, 12])
        u = F(random.randint(0, int(a) * den), den)
        v = F(random.randint(0, int(a) * den), den)
        p = (u, v)
        if in_triangle(p, a) and p not in E:
            E.append(p)
    t = tvec(E, a)
    ok = deficit(E, a) >= rhs(t)
    if side_condition(t, a):
        sat += 1
        if not ok:
            fail_sat.append((a, E, t))
    else:
        viol += 1
        if not ok:
            fail_viol.append((a, E, t))

record(f"Lemma 1 holds on all {sat} random configurations satisfying t_U+t_V<=a",
       not fail_sat, f"(failures: {len(fail_sat)})")
record(f"the side condition is NOT vacuous: {viol} random configurations violate it, "
       f"{len(fail_viol)} of those break the lemma",
       len(fail_viol) > 0,
       f"first witness: a={fail_viol[0][0]} E={fail_viol[0][1]} t={fail_viol[0][2]}"
       if fail_viol else "")

# ---------------------------------------------------------------------------
# (ii) explicit minimal witnesses that the side condition is load-bearing
# ---------------------------------------------------------------------------
for a in (F(2), F(3), F(4), F(6)):
    apex = (F(0), F(a))                    # corner C; t_A = t_B = a, t_C = 0
    E = [apex]
    t = tvec(E, a)
    d = deficit(E, a)
    r = rhs(t)
    record(f"WITNESS a={a}: E={{apex}}, t={t} violates t_A+t_B<=a and the lemma is FALSE",
           (not side_condition(t, a)) and (d < r),
           f"def(H) = {float(d):.4f} < RHS = {float(r):.4f}")

# a non-degenerate hull version: three points clustered near one corner
a = F(6)
E = [(F(0), F(6)), (F(1), F(5)), (F(0), F(5))]
t = tvec(E, a)
d, r = deficit(E, a), rhs(t)
record("WITNESS a=6: 3-point full-dimensional hull near the apex, side condition "
       "violated, lemma FALSE",
       (not side_condition(t, a)) and (d < r),
       f"t={t}  def(H)={float(d):.4f} < RHS={float(r):.4f}")

# ---------------------------------------------------------------------------
# (iii) exactly at the boundary of the side condition
# ---------------------------------------------------------------------------
for a in (F(2), F(4), F(6)):
    h = a / 2
    E = [(h, F(0)), (F(0), h), (h, h)]     # the medial triangle's vertices
    t = tvec(E, a)
    d, r = deficit(E, a), rhs(t)
    record(f"BOUNDARY a={a}: medial triangle, t=({h},{h},{h}) with t_U+t_V = a exactly",
           side_condition(t, a) and d == r,
           f"def(H) = {float(d):.6f}  RHS = {float(r):.6f}  equal={d == r}")

# The extremal family with t = (s,s,s): E = the vertices of the hexagon/triangle
#   K(s) = {u+v >= s, u <= a-s, v <= a-s} inside T_a.
# For s <= a/2 this K is a hexagon (side condition holds, with equality at s=a/2);
# for a/2 < s <= 2a/3 it is a triangle and the side condition fails.  These are the
# *worst* configurations for the lemma at a given t, since H = K is as large as
# possible, so they decide sufficiency at and beyond the boundary.
def extremal_E(a, s):
    a, s = F(a), F(s)
    if s <= a / 2:
        return [(s, F(0)), (a - s, F(0)), (a - s, s), (s, a - s),
                (F(0), a - s), (F(0), s)]
    return [(a - s, 2 * s - a), (2 * s - a, a - s), (a - s, a - s)]


a = F(6)
for s in (F(29, 10), F(299, 100), F(2999, 1000), F(3)):
    E = extremal_E(a, s)
    t = tvec(E, a)
    d, r = deficit(E, a), rhs(t)
    record(f"AT/INSIDE BOUNDARY a=6, t=({float(s):.4f})^3, sum of a pair = "
           f"{float(2*s):.4f} <= 6",
           t == (s, s, s) and side_condition(t, a) and d >= r,
           f"def-RHS = {float(d - r):.9f}")

for s in (F(3001, 1000), F(301, 100), F(31, 10), F(33, 10), F(7, 2), F(4)):
    E = extremal_E(a, s)
    t = tvec(E, a)
    d, r = deficit(E, a), rhs(t)
    broke = d < r
    record(f"JUST OUTSIDE a=6, t=({float(s):.4f})^3, pair sum {float(2*s):.4f} > 6 "
           f"-> lemma {'FAILS' if broke else 'still holds'}",
           t == (s, s, s) and not side_condition(t, a),
           f"def-RHS = {float(d - r):.9f}")

# ---------------------------------------------------------------------------
# (iv) the k=7 sanity value quoted in Sec. 2: T(k) minus the apex gives
#      t = (0,0,1) and sum (t^2+t)/2 = 1
# ---------------------------------------------------------------------------
for k in (3, 4, 5, 6, 7):
    a = F(k - 1)
    E = [(F(i), F(j)) for i in range(k) for j in range(k - i) if (i, j) != (0, k - 1)]
    t = tvec(E, a)
    d = deficit(E, a)
    record(f"lattice T({k}) minus apex at a={a}: t={t}, sum(t^2+t)/2 = "
           f"{float(rhs(t)):.4f}, def(H) = {float(d):.4f}",
           t == (F(0), F(0), F(1)) and d == rhs(t) and d == Surd(1))

print()
bad = [r for r in REPORT if not r[1]]
print(f"{len(REPORT)-len(bad)}/{len(REPORT)} checks passed")
raise SystemExit(1 if bad else 0)
