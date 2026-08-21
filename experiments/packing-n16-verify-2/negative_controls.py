#!/usr/bin/env python3
"""
Calibration: corrupt the REAL certificate in each of the ways a bad certificate
could plausibly be bad, and confirm covercheck.py rejects every one.

A checker that has never rejected anything is not evidence.

Corruptions:
  C1  diameter exactly 1        -- scale by mu = 50000/49999 so max diam == 1 exactly.
                                   THIS IS THE LEMMA L FAILURE MODE and must be rejected.
  C2  diameter just over 1      -- scale slightly past the supremum.
  C3  inflated a                -- claim a larger a with the same pieces (leaves a
                                   hole; area identity must fire).
  C4  a hole                    -- delete one piece.
  C5  an overlap                -- duplicate a piece (16 pieces, and two coincide).
  C6  16 pieces                 -- split one piece in two: a legitimate covering,
                                   but with 16 pieces it proves nothing about 16 points.
  C7  piece pushed outside T_a  -- translate one piece off the triangle.
  C8  overlap + equal-area hole -- the exact configuration the area-only argument
                                   lets through: shift one piece so it overlaps a
                                   neighbour; area sum is untouched, covering fails.
  C9  decimal strings           -- RULES.md sec.2 bans them in exact fields.
"""

import json
import os
import sys
import io
import contextlib
from fractions import Fraction as F

import covercheck
from covercheck import rat, check

SRC = "../packing-n16-covering/sub_s2_cert.json"
OUT = "controls"
os.makedirs(OUT, exist_ok=True)

raw = json.load(open(SRC))
a0 = rat(raw["a"])
faces0 = [[(rat(c[0]), rat(c[1])) for c in f] for f in raw["faces_uv"]]


def emit(name, a, faces):
    path = os.path.join(OUT, name + ".json")
    json.dump({"a": [str(a.numerator), str(a.denominator)],
               "faces_uv": [[[str(u), str(v)] for (u, v) in f] for f in faces]},
              open(path, "w"))
    return path


def scaled(mu):
    return mu * a0, [[(mu * u, mu * v) for (u, v) in f] for f in faces0]


controls = []

# C1: max diameter exactly 1
mu = F(50000, 49999)
controls.append(("C1_diam_exactly_1", scaled(mu),
                 "max squared diameter is EXACTLY 1 -- the Lemma L equality case"))

# C2: max diameter just over 1
mu = F(50000, 49999) * F(1000001, 1000000)
controls.append(("C2_diam_over_1", scaled(mu), "max squared diameter > 1"))

# C3: inflated a
controls.append(("C3_inflated_a", (a0 + F(1, 1000), faces0),
                 "a inflated by 1/1000, pieces unchanged -> uncovered strip"))

# C4: a hole (drop a piece)
controls.append(("C4_missing_piece", (a0, faces0[:-1]),
                 "one piece deleted -> 14 pieces and a hole"))

# C5: duplicate a piece
controls.append(("C5_duplicate_piece", (a0, faces0 + [faces0[0]]),
                 "piece 0 duplicated -> 16 pieces, coincident pair"))

# C6: 16 pieces by splitting one (a VALID covering, wrong piece budget)
f = faces0[0]
if len(f) >= 4:
    half1 = f[:3] + [f[0]]           # placeholder, replaced below
# split piece 0 by the diagonal from vertex 0 to vertex 2
p0 = faces0[0]
tri = [p0[0], p0[1], p0[2]]
rest = [p0[0]] + p0[2:]
controls.append(("C6_sixteen_pieces", (a0, [tri, rest] + faces0[1:]),
                 "piece 0 split in two -> 16 pieces; covering is fine, "
                 "pigeonhole against 16 points is not"))

# C7: a piece translated outside T_a
shift = F(1, 2)
moved = [(u - shift, v) for (u, v) in faces0[3]]
controls.append(("C7_outside_T_a", (a0, faces0[:3] + [moved] + faces0[4:]),
                 "one piece translated off the triangle"))

# C8: overlap + equal-area hole (the area-only argument's blind spot)
d = F(1, 100)
slid = [(u + d, v) for (u, v) in faces0[6]]
controls.append(("C8_overlap_plus_hole", (a0, faces0[:6] + [slid] + faces0[7:]),
                 "one piece translated by 1/100: areas still sum exactly to "
                 "|T_a|, but there is now an overlap and an equal-area hole"))

print("#" * 78)
print("# NEGATIVE CONTROLS on the real certificate -- all must be REJECTED")
print("#" * 78)

bad = 0
for name, (a, faces), why in controls:
    path = emit(name, a, faces)
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            ok, _ = check(path, verbose=False)
    except Exception as e:                     # a malformed piece may raise
        ok = False
        buf.write("  raised %s: %s\n" % (type(e).__name__, e))
    txt = buf.getvalue()
    reasons = [ln.strip() for ln in txt.splitlines() if ln.strip().startswith("[FAIL]")]
    status = "REJECTED" if not ok else "*** ACCEPTED -- CHECKER IS BROKEN ***"
    print("\n%-22s %s" % (name, status))
    print("   scenario : %s" % why)
    for r in reasons[:4]:
        print("   caught   : %s" % r[7:].strip()[:110])
    if ok:
        bad += 1

# C9: decimal strings in exact fields (RULES.md sec.2)
dec_ok = False
try:
    rat("4.46335")
except ValueError:
    dec_ok = True
print("\n%-22s %s" % ("C9_decimal_strings",
                      "REJECTED" if dec_ok else "*** ACCEPTED -- CHECKER IS BROKEN ***"))
print("   scenario : decimal string '4.46335' offered where an exact rational is required")
if not dec_ok:
    bad += 1

print("\n" + "=" * 78)
print("controls: %s" % ("ALL REJECTED as required" if bad == 0
                        else "%d LEAKED THROUGH" % bad))
print("=" * 78)
sys.exit(1 if bad else 0)
