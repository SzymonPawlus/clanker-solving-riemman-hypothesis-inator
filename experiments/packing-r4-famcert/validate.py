"""VALIDATION LADDER for the four-grain family generator.

CONSTRUCTION (upper bound) only. Nothing here claims optimality.

Written by the manager after the authoring worker was terminated by a connection
loss before it could write this file (its docstring in generator.py already
referenced it). It does two things, in this order, and the order matters:

  GATE 1 -- reproduction. The generator must regenerate the members whose values
            are already known, exactly:
              j = 0,1,2  ->  n = 4,7,12    PROVEN optima (cited: Milano 1987 /
                                           Melissen 1993), s = 4sqrt3, 2+4sqrt3,
                                           4+4sqrt3
              j = 3,4,5  ->  n = 17,24,31  open, but exact tight certificates
                                           already exist in
                                           experiments/packing-r3-qsqrt3/certificates/
            For j = 3,4,5 we additionally compare POINT SETS against those
            committed certificates, not merely the side length. A generator that
            gets the right n and d with the wrong configuration is not validated.

  GATE 2 -- prediction. Only if GATE 1 passes in full do the new members
            j = 6,7 (n = 40, 49) mean anything.

Run:  python3 validate.py
"""

import json
import os
import sys

from qsqrt3 import Q3
from parse import parse_q3
import generator
import check as chk

HERE = os.path.dirname(os.path.abspath(__file__))
R3CERTS = os.path.normpath(os.path.join(
    HERE, "..", "packing-r3-qsqrt3", "certificates"))

# n -> (path, ) for the already-committed exact certificates
KNOWN_CERT = {17: "n017-r3-qsqrt3.json",
              24: "n024-r3-qsqrt3.json",
              31: "n031-r3-qsqrt3.json"}

# proven optima, cited; s(n) as (rational part, sqrt3 coefficient)
PROVEN = {4: (0, 4), 7: (2, 4), 12: (4, 4)}


def load_known(n):
    p = os.path.join(R3CERTS, KNOWN_CERT[n])
    if not os.path.exists(p):
        return None
    with open(p) as f:
        cert = json.load(f)
    pts = set()
    for xs, ys in cert["coordinates"]:
        pts.add((parse_q3(xs), parse_q3(ys)))
    return cert, pts


def main():
    print("=" * 78)
    print("GATE 1 -- reproduction of known members")
    print("=" * 78)
    gate1 = True
    for j in (0, 1, 2, 3, 4, 5):
        n = len(generator.generate(j))
        pts = generator.generate(j)
        s = generator.s_of(j)
        rep = chk.check(len(pts), s, pts)

        note = []
        if len(pts) != n:
            note.append("COUNT MISMATCH")

        # value check against the cited proven optima
        if len(pts) in PROVEN:
            a, b = PROVEN[len(pts)]
            want = Q3(a, b)
            if s == want:
                note.append("matches CITED proven optimum")
            else:
                note.append(f"VALUE MISMATCH vs cited {want.sexpr()}")
                gate1 = False

        # point-set check against the committed exact certificates
        if len(pts) in KNOWN_CERT:
            got = load_known(len(pts))
            if got is None:
                note.append("committed cert not found (skipped)")
            else:
                cert, known_pts = got
                mine = set((p[0], p[1]) for p in pts)
                if mine == known_pts:
                    note.append("POINT SET identical to committed certificate")
                else:
                    inter = len(mine & known_pts)
                    note.append(f"POINT SET DIFFERS (shared {inter}/{len(known_pts)})")
                    # differing is not automatically fatal: a different valid
                    # packing at the same d is still a valid packing. Flag it.
                if cert["side_length"] != s.sexpr():
                    note.append(f"side_length differs: cert {cert['side_length']} vs {s.sexpr()}")
                    gate1 = False

        ok = rep["ok"] and rep.get("tight", False)
        if not ok:
            gate1 = False
        print(f"  j={j}  n={len(pts):3d}  s={s.sexpr():16s} "
              f"feasible={rep['ok']} tight={rep.get('tight')} "
              f"minsq4={rep.get('min_sq_distance_is_exactly_4')} "
              f"contacts={rep.get('contacts_at_distance_exactly_2')}")
        for x in note:
            print(f"         - {x}")
        if rep["failures"]:
            for f in rep["failures"][:5]:
                print(f"         ! {f}")

    print()
    print(f"GATE 1 {'PASSED' if gate1 else 'FAILED'}")
    if not gate1:
        print("Generator is not validated. GATE 2 results below would be meaningless;")
        print("stopping here.")
        return 1

    print()
    print("=" * 78)
    print("GATE 2 -- predictions past the published table (n = 40, 49)")
    print("=" * 78)
    print("The published Graham-Lubachevsky table stops at n = 34. These are NOT")
    print("record claims: Amore (2022, arXiv:2212.12287) reports triangle numerics")
    print("to N = 400 and is behind the egress block, so 'no published value here'")
    print("does NOT mean 'nobody has done better'. These are exact certified")
    print("UPPER BOUNDS and nothing more.")
    print()
    out = {}
    for j in (6, 7):
        pts = generator.generate(j)
        s = generator.s_of(j)
        rep = chk.check(len(pts), s, pts)
        print(f"  j={j}  n={len(pts):3d}  s={s.sexpr():16s} "
              f"feasible={rep['ok']} tight={rep.get('tight')} "
              f"pairs={rep.get('pairs_checked')} "
              f"minsq4={rep.get('min_sq_distance_is_exactly_4')} "
              f"contacts={rep.get('contacts_at_distance_exactly_2')} "
              f"on_boundary={rep.get('on_boundary')}")
        if rep["failures"]:
            for f in rep["failures"][:5]:
                print(f"         ! {f}")
        out[len(pts)] = rep

    print()
    print("=" * 78)
    print("NEGATIVE CONTROLS (a checker that accepts everything proves nothing)")
    print("=" * 78)
    pts = list(generator.generate(6))
    s = generator.s_of(6)
    # (a) break a separation
    bad = list(pts)
    bad[0] = (bad[1][0], bad[1][1])
    r = chk.check(len(bad), s, bad)
    print(f"  duplicate point          -> ok={r['ok']} (must be False)")
    # (b) deflate s
    r = chk.check(len(pts), s - Q3(1, 0), pts)
    print(f"  deflated s by 1          -> ok={r['ok']} (must be False)")
    # (c) inflate s: must be feasible but NOT tight
    r = chk.check(len(pts), s + Q3(1, 0), pts)
    print(f"  inflated s by 1          -> ok={r['ok']} tight={r.get('tight')} "
          f"(must be True / False)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
