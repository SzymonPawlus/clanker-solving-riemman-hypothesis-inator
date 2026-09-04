#!/usr/bin/env python3
"""
Adversarial tests for check_v5.py.  A checker that has never rejected anything
has not been tested.  Each corruption below is a deliberate, quantified defect;
the checker must reject it (or, for the inflation case, report it correctly).

Usage: python3 attack_v5.py [certificate.json]
Exit 0 iff every corruption behaves as required.
"""

import copy
import json
import os
import sys
import tempfile
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check_v5 import check, Q3, SQRT3, dec, containment_q3   # noqa: E402

CERT = (sys.argv[1] if len(sys.argv) > 1 else
        "problems/circle-packing-equilateral-triangle/attacks/n16-upper-2/"
        "n16-certificate.json")

base = json.load(open(CERT))
D = Fraction(base["side_length"].split("+")[0].strip())
PTS = [(Fraction(x), Fraction(y)) for x, y in base["coordinates"]]


def run(cert):
    fd, p = tempfile.mkstemp(suffix=".json")
    with os.fdopen(fd, "w") as f:
        json.dump(cert, f)
    try:
        try:
            log, fail, stats = check(p, verbose=False)
        except Exception as e:                      # parse errors etc.
            return ["EXCEPTION: " + type(e).__name__ + ": " + str(e)], {}
        return fail, stats
    finally:
        os.unlink(p)


def fr(q):
    return f"{q.numerator}/{q.denominator}"


results = []


def record(name, defect, fail, must_fail_gate=None, note=""):
    if must_fail_gate is None:
        ok = True
    else:
        ok = any(must_fail_gate in f for f in fail)
    results.append((name, defect, "rejected: " + "; ".join(fail) if fail else "ACCEPTED",
                    "OK" if ok else "*** CHECKER MISSED IT ***", note))
    return ok


# ---------------------------------------------------------------- 0. control
fail, stats = run(base)
record("0  unmodified certificate", "none", fail, None,
       "must be ACCEPTED" if not fail else "*** control failed ***")
control_clean = not fail

# ------------------------------------------- 1. pair overlapping by ~1e-12
i, j = stats["min_pair"]
t = Fraction(1) - Fraction(1, 2 * 10 ** 12)          # shrink the gap vector
c = copy.deepcopy(base)
px, py = PTS[i]
qx, qy = PTS[j]
nx, ny = px + (qx - px) * t, py + (qy - py) * t
c["coordinates"][j] = [fr(nx), fr(ny)]
sq = (nx - px) ** 2 + (ny - py) ** 2
overlap = 2 - Fraction(sq)                            # ~ depth, in dist^2 units
fail, _ = run(c)
record(f"1  pair ({i},{j}) pushed into overlap",
       f"dist^2 = 4 {dec(Q3(Fraction(sq) - 4, 0), 16)}, i.e. distance short of 2 by ~1.0e-12",
       fail, "G2.1")

# ------------------------------------- 2. point outside edge AB by 1e-12 (y<0)
k = min(range(16), key=lambda t_: PTS[t_][1])
c = copy.deepcopy(base)
c["coordinates"][k] = [fr(PTS[k][0]), fr(PTS[k][1] - Fraction(1, 10 ** 12))]
fail, _ = run(c)
record(f"2  point {k} pushed below edge AB (y = 0)",
       f"y = {dec(Q3(PTS[k][1] - Fraction(1, 10**12), 0), 16)} < 0, outside by ~1.0e-12",
       fail, "G3.1")

# ------------------- 3. point outside the SLANTED edge AC by 1e-12 (perp. dist)
# clearance to AC, as a perpendicular distance, is (sqrt3*x - y)/2.
# raising y by delta reduces (sqrt3*x - y) by delta, i.e. perp clearance by delta/2.
clr_ac = [(SQRT3 * Q3(x, 0) - Q3(y, 0)) for x, y in PTS]
k = min(range(16), key=lambda t_: float(clr_ac[t_]))
need = clr_ac[k]                                     # sqrt3*x - y, a Q(sqrt3) number
# choose a rational delta > need + 2e-12 : delta = ceil(need*10^30)/10^30 + 2e-12
approx = Fraction(int(float(need) * 10 ** 24) + 1, 10 ** 24)
delta = approx + Fraction(2, 10 ** 12)
c = copy.deepcopy(base)
c["coordinates"][k] = [fr(PTS[k][0]), fr(PTS[k][1] + delta)]
resid = SQRT3 * Q3(PTS[k][0], 0) - Q3(PTS[k][1] + delta, 0)
fail, _ = run(c)
record(f"3  point {k} pushed across the SLANTED edge AC",
       f"sqrt3*x - y = {dec(resid, 16)} < 0; perpendicular distance outside ~1.0e-12",
       fail, "G3.1")

# ------------------- 4. point outside the SLANTED edge BC by 1e-12 (perp. dist)
clr_bc = [(SQRT3 * (Q3(D, 0) - Q3(x, 0)) - Q3(y, 0)) for x, y in PTS]
k = min(range(16), key=lambda t_: float(clr_bc[t_]))
need = clr_bc[k]
approx = Fraction(int(float(need) * 10 ** 24) + 1, 10 ** 24)
delta = approx + Fraction(2, 10 ** 12)
c = copy.deepcopy(base)
c["coordinates"][k] = [fr(PTS[k][0]), fr(PTS[k][1] + delta)]
resid = SQRT3 * (Q3(D, 0) - Q3(PTS[k][0], 0)) - Q3(PTS[k][1] + delta, 0)
fail, _ = run(c)
record(f"4  point {k} pushed across the SLANTED edge BC",
       f"sqrt3*(d-x) - y = {dec(resid, 16)} < 0; perpendicular distance outside ~1.0e-12",
       fail, "G3.1")

# --------------------------------- 5. side_length INFLATED (must still be caught
#     as untight, not as infeasible -- an inflated s is feasible but overclaims)
c = copy.deepcopy(base)
c["side_length"] = f"{(D + Fraction(1,1000)).numerator}/{(D + Fraction(1,1000)).denominator} + 2*sqrt(3)"
fail, st = run(c)
ok = (not fail) and (not st["tight"]) and st["gap"].cmp(Fraction(9, 10000)) > 0
results.append(("5  side_length inflated by 1e-3",
                "d -> d + 1/1000 (still feasible, but a worse bound than claimed)",
                f"accepted as feasible; tight={st['tight']}, d - d_min = {dec(st['gap'], 8)}",
                "OK" if ok else "*** inflation not reported ***",
                "tightness gate is what catches this, per RULES.md s2"))

# --------------------------------- 6. side_length DEFLATED below d_min
c = copy.deepcopy(base)
dd = D - Fraction(1, 10 ** 12)
c["side_length"] = f"{dd.numerator}/{dd.denominator} + 2*sqrt(3)"
fail, _ = run(c)
record("6  side_length deflated below the minimal enclosing value",
       "d -> d - 1e-12 < d_min: the configuration no longer fits",
       fail, "G")

# --------------------------------- 7. a coordinate as a truncated decimal string
c = copy.deepcopy(base)
c["coordinates"][0] = ["6.27666889895201295", c["coordinates"][0][1]]
fail, _ = run(c)
record("7  coordinate written as a decimal string",
       '"6.27666889895201295" -- exactly rational, but banned by RULES.md s2',
       fail, "G0.4")

# --------------------------------- 8. scientific-notation coordinate
c = copy.deepcopy(base)
c["coordinates"][2] = ["4.6248e-14", c["coordinates"][2][1]]
fail, _ = run(c)
record("8  coordinate in scientific notation", '"4.6248e-14"', fail, "G0.4")

# --------------------------------- 9. side_length as a decimal string
c = copy.deepcopy(base)
c["side_length"] = "12.71362877415147"
fail, _ = run(c)
record("9  side_length as a decimal string", '"12.71362877415147"', fail, "")

# --------------------------- 10. the separation-1/separation-2 trap (FINDINGS.md)
# halve everything: a legitimate separation-1 packing, illegal at separation 2.
c = copy.deepcopy(base)
c["coordinates"] = [[fr(x / 2), fr(y / 2)] for x, y in PTS]
hd = D / 2
c["side_length"] = f"{hd.numerator}/{hd.denominator} + 2*sqrt(3)"
fail, _ = run(c)
record("10 whole packing rescaled to separation 1",
       "all coordinates and d halved: valid at separation 1, illegal at separation 2",
       fail, "G2.1", "guards the standing separation-1/2 trap")

# --------------------------- 11. coordinate_type lies about the encoding
c = copy.deepcopy(base)
c["coordinate_type"] = "interval"
fail, _ = run(c)
record("11 coordinate_type says 'interval', payload is bare rationals",
       "declared type does not match the encoding", fail, "G0.5")

# --------------------------- 12. rigid motion: the whole packing translated
c = copy.deepcopy(base)
c["coordinates"] = [[fr(x + Fraction(1, 10)), fr(y)] for x, y in PTS]
fail, _ = run(c)
record("12 whole packing translated by (0.1, 0)",
       "RULES.md s2: checkers do NOT search over rigid motions", fail, "G3.1")

# --------------------------- 13. does the slanted-edge test actually discriminate?
# a checker with the classic sign slip -- 3x^2 >= y^2 with the x >= 0 guard dropped
def slipped(x, y, d):
    return (y >= 0) and (3 * x * x >= y * y) and (3 * (d - x) ** 2 >= y * y)


k = min(range(16), key=lambda t_: float(clr_ac[t_]))
xx, yy = PTS[k]
xx = -xx - Fraction(1, 10 ** 6)          # mirror across x = 0: genuinely outside AC
slip_accepts = slipped(xx, yy, D)
truth = containment_q3(Q3(xx, 0), Q3(yy, 0), D)[0]
results.append(("13 discrimination of the sign-slip mutant",
                "x -> -x - 1e-6 (outside edge AC); guard 'x >= 0' dropped from the "
                "squared encoding",
                f"mutant accepts = {slip_accepts}; exact Q(sqrt3) truth = {truth}",
                "OK" if (slip_accepts and not truth) else "*** test does not discriminate ***",
                "confirms the squaring step is a real failure mode, and that the "
                "guard is what stops it"))

# ------------------------------------------------------------------ report
w = [max(len(r[i]) for r in results) for i in range(5)]
print("\n=== corruption-rejection table (V5, independent checker) ===\n")
hdr = ("corruption", "defect", "checker response", "outcome", "note")
print("| " + " | ".join(h.ljust(w[i]) for i, h in enumerate(hdr)) + " |")
print("|" + "|".join("-" * (w[i] + 2) for i in range(5)) + "|")
for r in results:
    print("| " + " | ".join(str(r[i]).ljust(w[i]) for i in range(5)) + " |")

bad = [r[0] for r in results if r[3] != "OK"] + ([] if control_clean else ["control"])
print("\nALL CORRUPTIONS HANDLED AS REQUIRED" if not bad else f"\nPROBLEMS: {bad}")
sys.exit(1 if bad else 0)
