"""n = 16 occupancy runs.  Usage: python3 run16.py <a_num> <a_den> <total_s>

Builds a clipped-hexagon cover of T_a (t = 6/7, several offsets, greedy exact
merging), verifies it exactly, saves it, then runs the occupancy exhaustion
with the capacity table capped at index 15 (CIRCULARITY GUARD: nothing about
n = 16 is an input; 4.6247636 is a comparison target only, never used here).
"""
import sys, json, time
from fractions import Fraction as F
import occ

def build_cover(a, t):
    best = None
    m0 = int(float(a / t))
    cands = [((a - t * m) / 3 % t,) * 2 for m in (m0 - 1, m0, m0 + 1)]
    cands += [(F(0), F(0)), (t / 2, t / 2), (t / 3, t / 3)]
    for off in cands:
        pcs = occ.merge_pass(occ.hex_cover(a, t, off[0], off[1]))
        if best is None or len(pcs) < len(best[0]):
            best = (pcs, off)
    return best

if __name__ == "__main__":
    num, den, total_s = int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3])
    a = F(num, den)
    assert a < F(462, 100), "K3 tripwire guard: refuse to run at a >= 4.62"
    t = F(6, 7)
    pcs, off = build_cover(a, t)
    tag = "%d_%d" % (num, den)
    with open("out/n16-cover-%s.json" % tag, "w") as fh:
        json.dump({"a": [str(num), str(den)], "t": str(t),
                   "offset": [str(off[0]), str(off[1])],
                   "pieces": [[[str(u), str(v)] for (u, v) in p]
                              for p in pcs]}, fh)
    print("a = %s = %.6f, N = %d pieces, offset %s" %
          (a, float(a), len(pcs), off))
    r = occ.run_occupancy(a, pcs, 16, cap_max_index=15,
                          floor_diam2=4e-4, node_cap=5000000,
                          time_cap_per_pattern=total_s,
                          time_cap_total=total_s,
                          out_path="out/n16-a%s.json" % tag,
                          label="n16 occupancy a=%s" % a)
    import collections
    print(collections.Counter(p["status"] for p in r["patterns"]))
