#!/usr/bin/env python3
"""Worker F3 (issue #97): seeded-family runs for the fractional covering lane.

WHY THIS FILE EXISTS.  F2's sweep at N=281/282 returned LP values 17.67/17.75
against budget 16 -- but 281/63 = 4.4603 < 1+2*sqrt3 = A_15, so a 15-piece
cover of T_281 by diameter-63-unit sets EXISTS in the continuum, and F2's
generated family cannot express it.  The sweep therefore tested the family,
not the relaxation.  This driver restores family adequacy by seeding the
family with a grid-rationalised version of the record's own 15-piece cover
(attacks/n16-covering-2, exact vertices over Q(sqrt3)), plus small lattice
translates of the rationalised pieces (translation preserves the diameter),
all clipped to T_N.  Kill-criteria: F2's KILL-CRITERION.md, K1-K4, plus the
F3 addendum A1-A4 fixed there before this file was run.

CIRCULARITY (addendum A3).  The seed is the record's 15-piece *covering* --
a `sketch` covering construction, NOT anything derived from a 16-point
packing.  It is an input to the piece FAMILY only, never to the bound: the
bound comes from Lemma F plus the exact verifier, and a wrong seed can only
raise the LP value, never certify anything false.  The only n=16-specific
constant remains the pigeonhole budget EXCLUDE_POINTS = 16.

All decisions that enter a certificate are exact (int/Fraction); floats are
used only to place candidate lattice points for the rationalisation search.
"""

import math
import sys
from fractions import Fraction as F

import fractional as fr

# ---------------------------------------------------------------------------
# exact seed data over Q(sqrt3): numbers are (a, b) meaning a + b*sqrt3.
# Source: attacks/n16-covering-2 (exact_1p2r3.py).  Transcribed here and
# re-verified exactly by selfcheck_seed() below before any use.
# ---------------------------------------------------------------------------

def q3(a, b=0):
    return (F(a), F(b))

T3 = F(1, 3)   # coefficient sqrt3/3
A15_Q3 = q3(1, 2)  # 1 + 2*sqrt3, the side of the seed cover

VERTS = {
    0: (q3(0), q3(0)),      30: (q3(1, 2), q3(0)),  14: (q3(0), q3(1, 2)),
    1: (q3(1), q3(0)),      15: (q3(0, 1), q3(0)),  22: (q3(1, 1), q3(0)),
    27: (q3(0, 2), q3(0)),
    3: (q3(0), q3(1)),      5: (q3(0), q3(0, 1)),   8: (q3(0), q3(1, 1)),
    11: (q3(0), q3(0, 2)),
    13: (q3(1), q3(0, 2)),  21: (q3(0, 1), q3(1, 1)),
    26: (q3(1, 1), q3(0, 1)), 29: (q3(0, 2), q3(1)),
    2: (q3(0, T3), q3(0, T3)),      4: (q3(0, T3), q3(1, T3)),
    7: (q3(0, T3), q3(0, 4 * T3)),  10: (q3(0, T3), q3(1, 4 * T3)),
    9: (q3(1), q3(0, 1)),           16: (q3(1, T3), q3(0, T3)),
    18: (q3(0, 1), q3(1)),          19: (q3(1, T3), q3(0, 4 * T3)),
    20: (q3(0, 1), q3(0, 1)),       23: (q3(0, 4 * T3), q3(0, T3)),
    24: (q3(0, 4 * T3), q3(1, T3)), 28: (q3(1, 4 * T3), q3(0, T3)),
    # the four rattlers, at the rational points the record parks them at
    6: (q3(1), q3(1)),      12: (q3(1), q3(F(5, 2))),
    17: (q3(F(3, 2)), q3(F(3, 2))), 25: (q3(F(5, 2)), q3(1)),
}

FACES = [[0, 1, 2, 3], [4, 5, 3, 2, 6], [7, 8, 5, 4, 9], [10, 11, 8, 7, 12],
         [13, 14, 11, 10], [1, 15, 16, 6, 2], [17, 9, 4, 6, 16, 18],
         [19, 12, 7, 9, 17, 20], [21, 13, 10, 12, 19], [15, 22, 23, 18, 16],
         [24, 20, 17, 18, 23, 25], [26, 21, 19, 20, 24], [22, 27, 28, 25, 23],
         [29, 26, 24, 25, 28], [27, 30, 29, 28]]


# ---- exact Q(sqrt3) helpers ------------------------------------------------

def q3_add(x, y):
    return (x[0] + y[0], x[1] + y[1])


def q3_sub(x, y):
    return (x[0] - y[0], x[1] - y[1])


def q3_mul(x, y):
    return (x[0] * y[0] + 3 * x[1] * y[1], x[0] * y[1] + x[1] * y[0])


def q3_sign(x):
    a, b = x
    if a == 0 and b == 0:
        return 0
    if a >= 0 and b >= 0:
        return 1
    if a <= 0 and b <= 0:
        return -1
    d = a * a - 3 * b * b          # sign of (a-b*sqrt3)*(a+b*sqrt3)
    if a > 0:                      # a>0, b<0
        return 1 if d > 0 else (-1 if d < 0 else 0)
    return -1 if d > 0 else (1 if d < 0 else 0)


def q3_float(x):
    return float(x[0]) + float(x[1]) * math.sqrt(3.0)


def selfcheck_seed():
    """Exact checks on the transcribed seed, in Q(sqrt3):
       (i) every face has squared diameter EXACTLY 1;
       (ii) every vertex lies in T_{1+2 sqrt3};
       (iii) shoelace areas of the faces sum to the shoelace area of T_A
             (a transcription check on the tiling, not a coverage proof --
             the load-bearing verification happens on the integer object).
    """
    one = q3(1)
    for fi, face in enumerate(FACES):
        m = q3(0)
        vs = [VERTS[k] for k in face]
        for i in range(len(vs)):
            for j in range(i + 1, len(vs)):
                du = q3_sub(vs[i][0], vs[j][0])
                dv = q3_sub(vs[i][1], vs[j][1])
                d2 = q3_add(q3_add(q3_mul(du, du), q3_mul(du, dv)),
                            q3_mul(dv, dv))
                if q3_sign(q3_sub(d2, m)) > 0:
                    m = d2
        assert m == one, f"face {fi}: exact diam^2 = {m}, not 1"
    for k, (u, v) in VERTS.items():
        assert q3_sign(u) >= 0 and q3_sign(v) >= 0, f"vertex {k} negative"
        assert q3_sign(q3_sub(A15_Q3, q3_add(u, v))) >= 0, \
            f"vertex {k} outside T_A"
    tot = q3(0)
    for face in FACES:
        vs = [VERTS[k] for k in face]
        s = q3(0)
        for i in range(len(vs)):
            (x1, y1), (x2, y2) = vs[i], vs[(i + 1) % len(vs)]
            s = q3_add(s, q3_sub(q3_mul(x1, y2), q3_mul(x2, y1)))
        assert q3_sign(s) > 0, "face not ccw"
        tot = q3_add(tot, s)
    # shoelace of T_A with vertices (0,0),(A,0),(0,A) is A^2
    assert tot == q3_mul(A15_Q3, A15_Q3), f"area sum {tot} != A^2"
    return True


# ---------------------------------------------------------------------------
# grid rationalisation: integer-vertex versions of the 15 faces at side N
# ---------------------------------------------------------------------------

def poly_area2_int(vs):
    s = 0
    for i in range(len(vs)):
        x1, y1 = vs[i]
        x2, y2 = vs[(i + 1) % len(vs)]
        s += x1 * y2 - x2 * y1
    return s


def max_pair_q(vs):
    m = 0
    for i in range(len(vs)):
        for j in range(i + 1, len(vs)):
            m = max(m, fr.Q(vs[i][0] - vs[j][0], vs[i][1] - vs[j][1]))
    return m


def best_int_face(pts_float, cap=fr.QMAX_ALLOWED):
    """Choose one lattice point near each float vertex (floor/ceil in each
    coordinate) so that the max pairwise Q is <= cap, maximising the shoelace
    area among feasible choices; on failure, shrink toward the centroid and
    retry.  Exhaustive over <= 4^6 combinations per face.  Exact feasibility
    (integer Q); floats only propose candidates."""
    cx = sum(p[0] for p in pts_float) / len(pts_float)
    cy = sum(p[1] for p in pts_float) / len(pts_float)
    for lam in [1.0, 0.999, 0.998, 0.997, 0.996, 0.995, 0.993, 0.991,
                0.989, 0.986, 0.983, 0.980]:
        pts = [(cx + lam * (x - cx), cy + lam * (y - cy))
               for x, y in pts_float]
        cands = [sorted({(math.floor(x), math.floor(y)),
                         (math.floor(x), math.ceil(y)),
                         (math.ceil(x), math.floor(y)),
                         (math.ceil(x), math.ceil(y))}) for x, y in pts]
        best = None
        def rec(i, chosen):
            nonlocal best
            if i == len(cands):
                if max_pair_q(chosen) <= cap:
                    a = poly_area2_int(chosen)
                    if best is None or a > best[0]:
                        best = (a, list(chosen))
                return
            for c in cands[i]:
                ok = all(fr.Q(c[0] - d[0], c[1] - d[1]) <= cap
                         for d in chosen)
                if ok:
                    chosen.append(c)
                    rec(i + 1, chosen)
                    chosen.pop()
        rec(0, [])
        if best is not None:
            hull = fr.hull_int(best[1])
            if hull is not None:
                return hull, lam
    return None, None


def seed_polys(N, radius=6, verbose=True):
    """Integer-vertex rationalisations of the 15 faces at scale
    mu = min(N/A15, 63) grid units per separation unit, plus all lattice
    translates within max(|a|,|b|,|a+b|) <= radius, clipped to T_N.
    Every returned piece passes the exact diameter cap."""
    selfcheck_seed()
    A15f = 1 + 2 * math.sqrt(3.0)
    mu = min(N / A15f, 63.0)
    bases = []
    for fi, face in enumerate(FACES):
        pts = [(q3_float(VERTS[k][0]) * mu, q3_float(VERTS[k][1]) * mu)
               for k in face]
        hull, lam = best_int_face(pts)
        assert hull is not None, f"face {fi}: no feasible rationalisation"
        q = max_pair_q(hull)
        assert q <= fr.QMAX_ALLOWED
        if verbose:
            print(f"  seed face {fi:2d}: lam={lam:.3f} verts={len(hull)} "
                  f"diam2={q}")
        bases.append(hull)
    shifts = [(a, b) for a in range(-radius, radius + 1)
              for b in range(-radius, radius + 1)
              if max(abs(a), abs(b), abs(a + b)) <= radius]
    out, seen = [], set()
    for base in bases:
        for (a, b) in shifts:
            vs = [(F(x + a), F(y + b)) for x, y in base]
            for (Ah, Bh, Ch) in ((-1, 0, 0), (0, -1, 0), (1, 1, N)):
                vs = fr.clip_halfplane(vs, F(Ah), F(Bh), F(Ch))
                if not vs:
                    break
            if not vs:
                continue
            vs = fr.clean_convex_ccw(vs)
            if not vs:
                continue
            p = fr.Poly(vs, tag=f"seed+{a},{b}")
            if p.diam2_upper() > fr.QMAX_ALLOWED:
                continue        # cannot happen (translation+clip), but exact
            key = tuple(sorted((str(x), str(y)) for x, y in p.vertsF))
            if key in seen:
                continue
            seen.add(key)
            out.append(p)
    if verbose:
        print(f"  seeds: {len(bases)} base faces -> {len(out)} "
              f"translated/clipped pieces (radius {radius})")
    return out


# ---------------------------------------------------------------------------
# drivers
# ---------------------------------------------------------------------------

def run(N, radius=6, with_family=True, label=None):
    # CIRCULARITY GUARD: the only n=16-specific input is this budget.
    EXCLUDE_POINTS = 16
    seeds = seed_polys(N, radius=radius)
    pieces = list(seeds)
    if with_family:
        pieces = fr.gen_family(N, step_bulk=4, step_edge=4) + pieces
    r = fr.run_case(label or f"n16seed", EXCLUDE_POINTS, N, pieces=pieces,
                    r_bulk=3, fine_band=8, corner_rad=75, lp_time=600)
    print(f"  n16 seeded N={N}: {r['status']} lp={r.get('lp_value')} "
          f"total={r.get('total_weight')} bound={r.get('bound_decimal_lower')}")
    if r.get("TRIPWIRE"):
        print("  TRIPWIRE HIT -- stopping per KILL-CRITERION K3")
    return r


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "check"
    if cmd == "check":
        selfcheck_seed()
        print("seed selfcheck: all 15 faces diam^2 == 1 exactly; vertices in "
              "T_A; areas tile: OK")
    elif cmd == "gate":
        run(281, label="n16seed")
    elif cmd == "run":
        N = int(sys.argv[2])
        rad = int(sys.argv[3]) if len(sys.argv) > 3 else 6
        run(N, radius=rad, label="n16seed")
    elif cmd == "sweep":
        for N in [int(x) for x in sys.argv[2:]]:
            r = run(N, label="n16seed")
            if r.get("TRIPWIRE"):
                break
    else:
        print("usage: seeded.py check | gate | run <N> [radius] | sweep N...")
