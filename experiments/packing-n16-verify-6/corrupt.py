#!/usr/bin/env python3
"""V6 adversarial battery: corruptions the manager's selftest.py did not try.
Each row is run through BOTH the manager's checker (fracverify) and mine
(v6check).  Disagreement, or an acceptance of something that should be
rejected, is a finding."""
import copy, json, os, sys, tempfile
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "packing-n16-fracverify"))
sys.path.insert(0, HERE)
import fracverify as A          # manager's
import v6check as B             # mine

CD = os.path.join(HERE, "..", "packing-n16-fractional", "certs")

def load(n):
    return json.load(open(os.path.join(CD, n)))

def run(blob, label, expect):
    fd, p = tempfile.mkstemp(suffix=".json")
    with os.fdopen(fd, "w") as f:
        json.dump(blob, f)
    try:
        try:
            oa = A.verify(p, verbose=False)[0]; ra = "accept" if oa else "reject"
        except Exception as e:
            ra = "crash:" + type(e).__name__
        try:
            ob = B.check(p, verbose=False)[0]; rb = "accept" if ob else "reject"
        except Exception as e:
            rb = "crash:" + type(e).__name__
    finally:
        os.unlink(p)
    flag = ""
    if ra != expect and not (expect == "reject" and ra.startswith("crash")):
        flag = "  <-- fracverify DISAGREES with expectation"
    if ra.split(":")[0] != rb.split(":")[0]:
        flag += "  <-- CHECKERS DISAGREE"
    print(f"| {label:<52} | {expect:<6} | {ra:<14} | {rb:<14} |{flag}")
    return flag

flags = []

print(f"| {'corruption':<52} | {'expect':<6} | {'fracverify':<14} | {'v6check':<14} |")
print(f"|{'-'*54}|{'-'*8}|{'-'*16}|{'-'*16}|")

# baselines
for nm in ("cert_n4_N108.json", "cert_n6_N126.json", "cert_n10_N189.json"):
    flags.append(run(load(nm), "BASELINE " + nm, "accept"))

b = load("cert_n4_N108.json")
b10 = load("cert_n10_N189.json")

def poly_key(blob):
    return next(k for k, s in blob["certificate"]["pieces"].items() if s["kind"] == "poly")
def box_key(blob):
    return next(k for k, s in blob["certificate"]["pieces"].items() if s["kind"] == "box")

# A1 non-convex notched polygon (region used must not exceed hull of verts)
x = copy.deepcopy(b); k = poly_key(x)
v = x["certificate"]["pieces"][k]["verts"]
# insert a reflex vertex at the centroid of the first edge, pulled inward
import statistics
cx = sum(F(a) for a, _ in v) / len(v); cy = sum(F(c) for _, c in v) / len(v)
mx = (F(v[0][0]) + F(v[1][0])) / 2; my = (F(v[0][1]) + F(v[1][1])) / 2
nx, ny = (mx + cx) / 2, (my + cy) / 2
x["certificate"]["pieces"][k]["verts"] = [v[0], [str(nx), str(ny)]] + v[1:]
flags.append(run(x, "A1 piece made non-convex (reflex vertex inserted)", "reject"))

# A2 self-intersecting polygon
x = copy.deepcopy(b); k = poly_key(x)
v = x["certificate"]["pieces"][k]["verts"]
v2 = list(v); v2[1], v2[2] = v2[2], v2[1]
x["certificate"]["pieces"][k]["verts"] = v2
flags.append(run(x, "A2 piece vertices reordered (self-intersecting)", "reject"))

# A3 convex piece given clockwise -- must STILL be accepted
x = copy.deepcopy(b); k = poly_key(x)
x["certificate"]["pieces"][k]["verts"] = list(reversed(x["certificate"]["pieces"][k]["verts"]))
flags.append(run(x, "A3 convex piece listed clockwise (benign)", "accept"))

# A4 a collinear extra vertex on an edge -- must STILL be accepted
x = copy.deepcopy(b); k = poly_key(x)
v = x["certificate"]["pieces"][k]["verts"]
mx = (F(v[0][0]) + F(v[1][0])) / 2; my = (F(v[0][1]) + F(v[1][1])) / 2
x["certificate"]["pieces"][k]["verts"] = [v[0], [str(mx), str(my)]] + v[1:]
flags.append(run(x, "A4 collinear extra vertex inserted (benign)", "accept"))

# A5 piece translated by 1/1000 -> positive-area hole
x = copy.deepcopy(b); k = poly_key(x)
x["certificate"]["pieces"][k]["verts"] = [[str(F(a) + F(1, 1000)), c]
                                          for a, c in x["certificate"]["pieces"][k]["verts"]]
flags.append(run(x, "A5 one piece translated by 1/1000", "reject"))

# A6 piece shrunk by pulling ONE vertex in by 1/1000
x = copy.deepcopy(b); k = poly_key(x)
v = x["certificate"]["pieces"][k]["verts"]
cx = sum(F(a) for a, _ in v) / len(v); cy = sum(F(c) for _, c in v) / len(v)
v[0] = [str(F(v[0][0]) + (cx - F(v[0][0])) / 1000), str(F(v[0][1]) + (cy - F(v[0][1])) / 1000)]
flags.append(run(x, "A6 one vertex pulled inward by 1/1000", "reject"))

# A7 box: whi set to 0 (fracverify builds its w-clip from two coincident points)
x = copy.deepcopy(b10); k = box_key(x)
bd = list(x["certificate"]["pieces"][k]["bounds"]); bd[5] = 0
x["certificate"]["pieces"][k]["bounds"] = bd
flags.append(run(x, "A7 box upper s-bound set to 0 (degenerate piece)", "reject"))

# A8 box: wlo set negative (constraint direction flips in a 2-point encoding)
x = copy.deepcopy(b10); k = box_key(x)
bd = list(x["certificate"]["pieces"][k]["bounds"]); bd[4] = -5
x["certificate"]["pieces"][k]["bounds"] = bd
flags.append(run(x, "A8 box lower s-bound set to -5 (widened piece)", "accept"))

# A9 decimal string coordinates (banned by problem RULES.md section 2)
x = copy.deepcopy(b); k = poly_key(x)
x["certificate"]["pieces"][k]["verts"] = [[str(float(F(a))), str(float(F(c)))]
                                          for a, c in x["certificate"]["pieces"][k]["verts"]]
flags.append(run(x, "A9 coordinates as decimal strings (RULES 2 ban)", "reject"))

# A10 bare floats in exact fields
x = copy.deepcopy(b); k = poly_key(x)
x["certificate"]["pieces"][k]["verts"] = [[float(F(a)), float(F(c))]
                                          for a, c in x["certificate"]["pieces"][k]["verts"]]
flags.append(run(x, "A10 coordinates as bare JSON floats (RULES 2 ban)", "reject"))

# A11 negative weight on one piece, compensated elsewhere
x = copy.deepcopy(b)
ks = list(x["certificate"]["weights"])
x["certificate"]["weights"][ks[0]] = -65536
x["certificate"]["weights"][ks[1]] = 3 * 65536
flags.append(run(x, "A11 a negative weight (compensated in total)", "reject"))

# A12 N_units inflated by 1 (leaves an uncovered strip)
x = copy.deepcopy(b); x["certificate"]["N_units"] = 109
flags.append(run(x, "A12 N_units 108 -> 109 (uncovered strip)", "reject"))

# A13 K doubled without doubling weights
x = copy.deepcopy(b); x["certificate"]["K"] = 2 * 65536
flags.append(run(x, "A13 K doubled, weights unchanged", "reject"))

# A14 unit inflated to 1/1000 -- diameter cap becomes vacuous
x = copy.deepcopy(b); x["certificate"]["unit"] = "1/1000"
flags.append(run(x, "A14 unit 1/64 -> 1/1000 (cap made vacuous)", "accept"))

# A15 unit deflated to 1/63 -- cap now violated
x = copy.deepcopy(b); x["certificate"]["unit"] = "1/63"
flags.append(run(x, "A15 unit 1/64 -> 1/63 (Qmax exceeds separation)", "reject"))

# A16 weighted piece with no spec
x = copy.deepcopy(b); x["certificate"]["weights"]["999999"] = 65536
flags.append(run(x, "A16 weight on a piece with no spec", "reject"))

# A17 two pieces' weights swapped (n10 has unequal weights)
x = copy.deepcopy(b10)
ks = sorted(x["certificate"]["weights"])
w = x["certificate"]["weights"]
a0, a1 = ks[0], ks[-1]
w[a0], w[a1] = w[a1], w[a0]
flags.append(run(x, "A17 two weights swapped (n10)", "reject"))

# A18 budget lowered from 4 to 3
x = copy.deepcopy(b); x["certificate"]["budget_points"] = 3
flags.append(run(x, "A18 budget 4 -> 3 (weight no longer under budget)", "reject"))

print()
n = sum(1 for f in flags if f)
print("FLAGGED ROWS:", n)
