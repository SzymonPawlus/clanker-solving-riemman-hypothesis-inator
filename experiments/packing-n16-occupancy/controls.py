"""K0 validation controls for the occupancy engine (see KILL-CRITERION.md).

Each control certifies a_n >= a for a about 3-5 % below the known (cited) a_n,
and must FAIL to certify just above a_n, where an explicit packing exists.
Capacity table is capped at n-1 throughout (circularity guard).

Known values used only as *test oracles* here (never as engine inputs):
a_4 = sqrt(3), a_6 = 2, a_7 = 1 + sqrt(3), a_10 = 3   (cited, problem README).

Run:  python3 controls.py        (~8 min, single core, deterministic)
"""
from fractions import Fraction as F
import collections
import time
import occ


def build_hex(a, t):
    best = None
    m0 = int(float(a / t))
    cands = [((a - t * m) / 3 % t,) * 2 for m in (m0 - 1, m0, m0 + 1)]
    cands += [(F(0), F(0)), (t / 2, t / 2)]
    for off in cands:
        pcs = occ.merge_pass(occ.hex_cover(a, t, off[0], off[1]))
        if best is None or len(pcs) < len(best):
            best = pcs
    return best


def run(name, n, a, pieces, expect_certified, time_cap_total, pattern_cap):
    t0 = time.time()
    r = occ.run_occupancy(
        a, pieces, n, cap_max_index=occ.CAP_MAX_INDEX_FOR(n),
        floor_diam2=1e-4, node_cap=2000000,
        time_cap_per_pattern=pattern_cap, time_cap_total=time_cap_total,
        out_path="out/ctl-%s.json" % name, label="control " + name)
    got = r.get("all_refuted")
    c = collections.Counter(p["status"] for p in r["patterns"])
    print("[%s] a=%s expect certified=%s got=%s %s (%.1fs)" %
          (name, a, expect_certified, got, dict(c), time.time() - t0))
    assert got == expect_certified, "CONTROL FAILED: " + name
    return r


if __name__ == "__main__":
    t = F(6, 7)
    # n=4, window (a_3, a_4): pure pair pruning + refinement, no capacity.
    run("n4-lo", 4, F(165, 100), occ.subdiv_cover(F(165, 100), 1), True, 240, 120)
    run("n4-hi", 4, F(175, 100), occ.subdiv_cover(F(175, 100), 1), False, 240, 120)
    # n=6 on a fine subdivision: exercises clique enumeration.
    run("n6-lo", 6, F(19, 10), occ.subdiv_cover(F(19, 10), 2), True, 240, 60)
    run("n6-hi", 6, F(41, 20), occ.subdiv_cover(F(41, 20), 2), False, 240, 60)
    # n=7, window (a_6, a_7): root capacity cannot fire -> the decisive one.
    run("n7-lo", 7, F(26, 10), build_hex(F(26, 10), t), True, 240, 120)
    run("n7-hi", 7, F(28, 10), build_hex(F(28, 10), t), False, 240, 120)
    # n=10 with a deliberately fine cover: full pipeline in certify direction.
    run("n10-lo", 10, F(57, 20), occ.merge_pass(
        occ.hex_cover(F(57, 20), F(4, 5), F(2, 5), F(2, 5))), True, 420, 120)
    run("n10-hi", 10, F(61, 20), build_hex(F(61, 20), t), False, 240, 120)
    print("ALL CONTROLS PASSED")
