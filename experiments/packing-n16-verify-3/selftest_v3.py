"""Adversarial self-test of V3's checker: every corruption below MUST be
rejected.  A checker that has not been shown to reject bad input has not been
shown to do anything (problem RULES.md s0).
"""
from fractions import Fraction as F
import copy, io, contextlib
from q3f import Q3, q3, ZERO, ONE, parse_exact
from geom import area2
from check_v3 import check, hull
import cert_v3

A = cert_v3.A_SIDE
BASE = cert_v3.faces()


import time, sys


def run(faces, a=A, max_nodes=60000):
    t0 = time.time()
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        ok, rep = check(a, faces, verbose=True, max_nodes=max_nodes)
    print(f"    [{time.time()-t0:6.1f}s] nodes={rep.get('C5_nodes')} "
          f"covered={rep.get('C5_covered')}", file=sys.stderr, flush=True)
    return ok, rep


def shift(f, du, dv):
    return [(u + du, v + dv) for (u, v) in f]


def scale_about_centroid(f, k):
    n = q3(len(f))
    cu = sum((p[0] for p in f), ZERO) / n
    cv = sum((p[1] for p in f), ZERO) / n
    return [(cu + k * (u - cu), cv + k * (v - cv)) for (u, v) in f]


results = []


def case(name, faces, a=A, expect_field=None):
    print("  running:", name, file=sys.stderr, flush=True)
    ok, rep = run(faces, a)
    rejected = not ok
    results.append((name, rejected, rep.get("errors", [])[:2], rep))
    return rep


# --- (0) the honest certificate passes ---------------------------------
ok0, rep0 = run(BASE)
results.append(("[control] unmodified certificate is ACCEPTED", ok0, [], rep0))

# --- (1) a piece dilated until squared diameter exceeds 1 ---------------
f = [list(x) for x in BASE]
f[6] = scale_about_centroid(BASE[6], q3(F(1001, 1000)))
r = case("(1) piece 6 dilated 1.001x: squared diameter exceeds 1", f)

# --- (2) EQUAL-AREA OVERLAP + HOLE: passes the area identity ------------
f = [list(x) for x in BASE]
f[6] = shift(BASE[6], q3(F(1, 100)), ZERO)
r = case("(2) interior piece translated: equal-area overlap + hole", f)
AREA_TRICK = r["C6_area_sum_equals_T_a"]

# --- (3) a vertex just outside T_a --------------------------------------
f = [list(x) for x in BASE]
g = list(BASE[14])
u, v = g[1]                       # the corner (a, 0)
g[1] = (u + q3(F(1, 10 ** 6)), v)
f[14] = g
case("(3) one vertex 1e-6 outside T_a", f)

# --- (4) a piece deleted ------------------------------------------------
f = [BASE[i] for i in range(15) if i != 7]
case("(4) piece 7 deleted (14 pieces)", f)

# --- (5) a piece shrunk: genuine sliver hole ----------------------------
f = [list(x) for x in BASE]
f[10] = scale_about_centroid(BASE[10], q3(F(999, 1000)))
case("(5) piece 10 shrunk 0.999x: sliver hole", f)

# --- (6) a listed vertex that is not a hull vertex ----------------------
f = [list(x) for x in BASE]
g = list(BASE[0])
mid = ((g[0][0] + g[1][0]) / q3(2), (g[0][1] + g[1][1]) / q3(2))
f[0] = [g[0], mid, g[1], g[2], g[3]]
case("(6) piece 0 given a collinear extra vertex (not strictly convex)", f)

# --- (7) decimal string in an exact field -------------------------------
try:
    parse_exact("4.464101615137754")
    dec_ok = False
except ValueError:
    dec_ok = True
results.append(("(7) decimal string '4.4641...' in an exact field is REJECTED",
                dec_ok, [], {}))

try:
    parse_exact(["0.5773502691896258", "0"])
    dec2 = False
except ValueError:
    dec2 = True
results.append(("(8) decimal string inside a Q(sqrt3) pair is REJECTED", dec2, [], {}))

# --- (9) the honest certificate must NOT be reported as strict ----------
strict_claimed = rep0["C3_strictly_below_1"]
results.append(("(9) checker refuses to call the a=1+2sqrt3 certificate "
                "strictly-sub-diameter-1", (not strict_claimed), [], {}))

# --- (10) an inflated side length a (containment alone would pass) ------
#   claim the same 15 pieces cover T_a for a larger a: coverage must fail
big = A + q3(F(1, 1000))
ok, rep = run(BASE, big)
results.append(("(10) same pieces claimed to cover a larger T_a", (not ok),
                rep.get("errors", [])[:1], rep))

print("=" * 78)
print("V3 checker self-test: 10 corruptions + 1 control")
print("=" * 78)
allgood = True
for name, good, errs, _ in results:
    mark = "ok  " if good else "FAIL"
    if not good:
        allgood = False
    print(f"[{mark}] {name}")
    for e in errs:
        print(f"        -> {e}")
print()
print(f"corruption (2) passed the area identity while failing coverage: "
      f"{AREA_TRICK}  <-- this is why the area shortcut is void")
print()
print("ALL SELF-TESTS PASS" if allgood else "SELF-TEST FAILURE")
