#!/usr/bin/env python3
"""Attack the independent checker before believing it.

Five deliberate corruptions of a KNOWN-GOOD certificate; every one must be
rejected.  A checker that has not been shown to reject is not evidence.
"""
import copy, json, os, sys, tempfile
from fractions import Fraction as F
import fracverify as V

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "..", "packing-n16-fractional", "certs", "cert_n10_N189.json")
base = json.load(open(SRC))


def run(blob, label):
    fd, p = tempfile.mkstemp(suffix=".json")
    with os.fdopen(fd, "w") as f:
        json.dump(blob, f)
    try:
        ok, b, q = V.verify(p, verbose=False)
    finally:
        os.unlink(p)
    print(f"  {'REJECTED' if not ok else '*** ACCEPTED ***':>18}  {label}")
    return not ok


print("baseline must be VALID:")
ok, _, _ = V.verify(SRC, verbose=False)
print(f"  {'VALID' if ok else '*** INVALID ***':>18}  untouched certificate")
allgood = ok

print("corruptions, all must be REJECTED:")

# 1. diameter cap violated: stretch one polygon vertex far away
b1 = copy.deepcopy(base)
k = next(k for k, s in b1["certificate"]["pieces"].items() if s["kind"] == "poly")
b1["certificate"]["pieces"][k]["verts"][0] = ["189", "0"] if b1["certificate"]["pieces"][k]["verts"][0] != ["189", "0"] else ["0", "189"]
allgood &= run(b1, "a piece stretched past the diameter cap")

# 2. containment violated: push a vertex outside T_N
b2 = copy.deepcopy(base)
k = next(iter(b2["certificate"]["pieces"]))
s = b2["certificate"]["pieces"][k]
if s["kind"] == "box":
    s["bounds"] = [-1] + list(s["bounds"][1:])
else:
    s["verts"][0] = ["-1", str(s["verts"][0][1])]
allgood &= run(b2, "a vertex pushed outside T_N")

# 3. covering violated: delete one piece
b3 = copy.deepcopy(base)
k = next(iter(b3["certificate"]["weights"]))
del b3["certificate"]["weights"][k]
allgood &= run(b3, "one piece deleted (leaves a hole)")

# 4. covering violated subtly: halve one weight so its region drops below 1
b4 = copy.deepcopy(base)
k = next(iter(b4["certificate"]["weights"]))
b4["certificate"]["weights"][k] //= 2
allgood &= run(b4, "one weight halved (region falls below weight 1)")

# 5. budget violated: inflate weights past n*K
b5 = copy.deepcopy(base)
K = b5["certificate"]["K"]; nb = b5["certificate"]["budget_points"]
ks = list(b5["certificate"]["weights"])
need = nb * K - sum(b5["certificate"]["weights"].values())
b5["certificate"]["weights"][ks[0]] += need + 1
allgood &= run(b5, "total weight inflated to the budget")

print("\nSELFTEST", "PASS" if allgood else "FAIL")
sys.exit(0 if allgood else 1)
