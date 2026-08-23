#!/usr/bin/env python3
"""Independent exact checker for FRACTIONAL covering certificates (Lemma F).

Written from the statement of Lemma F and the certificate's own field names.
It does NOT import, read or adapt `experiments/packing-n16-fractional/fractional.py`
-- problem RULES.md section 3 requires the second checker to be written
independently, and re-running the author's script verifies only determinism.

WHAT IS BEING CHECKED
  Chart e1=(1,0), e2=(1/2,sqrt3/2); Q(u,v) = u^2 + u v + v^2 is the squared
  Euclidean length of u e1 + v e2.  All coordinates are INTEGERS in units of
  1/UNIT of the separation distance, so Q is an exact integer.
  T_N = {u >= 0, v >= 0, u + v <= N}.

  Lemma F: if every piece has diameter < 1, every point of T_N carries total
  incident weight >= 1, and the total weight is < n, then T_N holds no n points
  at pairwise distance >= 1.

  So a certificate is valid iff, with weights w_i/K:
    (A) every piece is contained in T_N;
    (B) max squared diameter Qmax <= (UNIT-1)^2, i.e. diameter <= (UNIT-1)/UNIT < 1;
    (C) sum_i w_i < n*K                                     [budget, strict]
    (D) for every x in T_N,  sum_{i : x in S_i} w_i >= K     [covering]
  and then a_n >= N/sqrt(Qmax) by dilation (N/(UNIT-1) when Qmax=(UNIT-1)^2).

  (D) quantifies over a continuum.  It is discharged EXACTLY, with no sampling
  and no area identity, by carrying a list of (convex region, accumulated
  weight) and splitting each region against each piece in turn; at the end the
  set of regions whose accumulated weight is < K must be empty.
"""
import json
import sys
from fractions import Fraction as F


# ---------- exact convex polygon geometry over the rationals ----------------
def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def area2(p):
    s = 0
    for i in range(len(p)):
        x1, y1 = p[i]
        x2, y2 = p[(i + 1) % len(p)]
        s += x1 * y2 - x2 * y1
    return s


def ccw(p):
    return p if area2(p) > 0 else p[::-1]


def clip(poly, a, b, keep):
    """Part of convex `poly` with keep*cross(a,b,P) >= 0.  Exact."""
    if not poly:
        return []
    out = []
    n = len(poly)
    for i in range(n):
        P, Q = poly[i], poly[(i + 1) % n]
        sp, sq = keep * cross(a, b, P), keep * cross(a, b, Q)
        if sp >= 0:
            out.append(P)
        if (sp > 0 > sq) or (sp < 0 < sq):
            cp, cq = cross(a, b, P), cross(a, b, Q)
            t = F(cp) / F(cp - cq)
            out.append((P[0] + t * (Q[0] - P[0]), P[1] + t * (Q[1] - P[1])))
    ded = []
    for p in out:
        if not ded or p != ded[-1]:
            ded.append(p)
    if len(ded) > 1 and ded[0] == ded[-1]:
        ded.pop()
    return ded if len(ded) >= 3 and area2(ded) != 0 else []


def split(poly, piece):
    """(inside, outside_parts) for convex poly against convex piece."""
    cur, outside = poly, []
    for i in range(len(piece)):
        if not cur:
            break
        A, B = piece[i], piece[(i + 1) % len(piece)]
        o = clip(cur, A, B, -1)
        if o:
            outside.append(o)
        cur = clip(cur, A, B, 1)
    return cur, outside


def sqQ(p, q):
    du, dv = p[0] - q[0], p[1] - q[1]
    return du * du + du * dv + dv * dv


def sqdiam(poly):
    return max(sqQ(poly[i], poly[j])
               for i in range(len(poly)) for j in range(i + 1, len(poly)))


# ---------- certificate decoding -------------------------------------------
def exact(z):
    """Parse an exact field.  Problem RULES.md section 2 bans decimal strings;
    a bare JSON float is worse.  (Bugs C2, found by worker V6.)"""
    if isinstance(z, float):
        raise ValueError(f"bare float {z!r} in an exact field")
    if isinstance(z, str):
        if "." in z or "e" in z.lower():
            raise ValueError(f"decimal string {z!r} in an exact field")
    return F(z)


def piece_polygon(spec):
    """Decode one piece to a ccw integer polygon in the (u,v) chart."""
    if spec["kind"] == "poly":
        # vertices may be integers or exact rationals like "107/2"
        return ccw([(exact(x), exact(y)) for x, y in spec["verts"]])
    if spec["kind"] == "box":
        ulo, uhi, vlo, vhi, wlo, whi = spec["bounds"]
        # {ulo<=u<=uhi, vlo<=v<=vhi, wlo<=u+v<=whi} -- clip the u,v box by w
        ulo, uhi, vlo, vhi, wlo, whi = (exact(z) for z in (ulo, uhi, vlo, vhi, wlo, whi))
        poly = ccw([(ulo, vlo), (uhi, vlo), (uhi, vhi), (ulo, vhi)])
        # The u+v bounds MUST NOT be clipped against the point pair
        # ((c,0),(0,c)): that cross product carries a factor of c, so the
        # inequality flips for c < 0 and vanishes for c = 0.  (Bug C1, found
        # by worker V6; gen_family emits w-bounds down to -126.)
        # Use the direction-fixed pair (c,0),(c-1,1): then
        #   cross((c,0),(c-1,1),P) = c - (Pu+Pv),
        # whose sign is independent of the sign of c.
        for c, keep in ((whi, 1), (wlo, -1)):
            poly = clip(poly, (c, F(0)), (c - 1, F(1)), keep)
            if not poly:
                return []
        return poly
    raise ValueError("unknown piece kind: " + spec["kind"])


# ---------- the four checks -------------------------------------------------
def verify(path, verbose=True):
    blob = json.load(open(path))
    cert = blob["certificate"]
    N = int(cert["N_units"])
    K = int(cert["K"])
    budget = int(cert["budget_points"])
    weights = {k: int(v) for k, v in cert["weights"].items()}
    specs = cert["pieces"]
    unit = cert["unit"]
    UNIT = F(unit).denominator if isinstance(unit, str) else int(round(1 / unit))
    cap = (UNIT - 1) ** 2

    fails = []
    missing = [k for k in weights if k not in specs]
    if missing:
        fails.append(f"weights reference {len(missing)} piece(s) with no spec: {missing[:5]}")
    polys = {}
    for k in weights:
        if k not in specs:
            continue
        try:
            polys[k] = piece_polygon(specs[k])
        except ValueError as e:
            fails.append(f"piece {k}: {e}")
    if not polys:
        return False, 0.0, 0

    # (A) containment in T_N
    for k, P in polys.items():
        if not P:
            fails.append(f"piece {k} decoded empty")
            continue
        for (u, v) in P:
            if u < 0 or v < 0 or u + v > N:
                fails.append(f"piece {k} vertex ({u},{v}) outside T_{N}")

    # (B) strict diameter
    qmax = max(sqdiam(P) for P in polys.values() if P)
    if qmax > cap:
        fails.append(f"max squared diameter {qmax} > cap {cap}")

    # (C) budget, strictly below n*K
    tot = sum(weights.values())
    if not tot < budget * K:
        fails.append(f"total weight {tot}/{K} not < budget {budget}")

    # (D) covering, exactly, by region splitting with accumulated weight
    T = ccw([(F(0), F(0)), (F(N), F(0)), (F(0), F(N))])
    regions = [(T, 0)]
    order = sorted(weights, key=lambda k: -weights[k])
    for k in order:
        P, w = polys[k], weights[k]
        if not P:
            continue
        nxt = []
        for (R, acc) in regions:
            if acc >= K:
                continue                      # already satisfied, drop
            inside, outside = split(R, P)
            if inside:
                nxt.append((inside, acc + w))
            for o in outside:
                nxt.append((o, acc))
        regions = [(R, a) for (R, a) in nxt if a < K]
        if not regions:
            break
    if regions:
        fails.append(f"covering FAILS: {len(regions)} region(s) with weight < 1")

    ok = not fails
    bound_sq = F(N * N, qmax)
    if verbose:
        print(f"--- {os.path.basename(path)}")
        print(f"    N={N} unit=1/{UNIT} budget={budget} pieces_in_support={len(polys)}")
        print(f"    (A) containment in T_N                : {'ok' if not any('outside' in f for f in fails) else 'FAIL'}")
        print(f"    (B) max squared diameter {qmax} <= {cap}   : {'ok' if qmax <= cap else 'FAIL'}")
        print(f"    (C) total weight {tot}/{K} = {tot/K:.9f} < {budget} : {'ok' if tot < budget*K else 'FAIL'}")
        print(f"    (D) covering, exact region split       : {'ok' if not any('covering' in f for f in fails) else 'FAIL'}")
        print(f"    => bound a_n >= N/sqrt(qmax) = sqrt({bound_sq}) = {float(bound_sq)**0.5:.10f}")
        print(f"    VERDICT: {'VALID' if ok else 'INVALID'}")
        for f in fails:
            print("      !", f)
    return ok, float(bound_sq) ** 0.5, qmax


import os

if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        d = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "..", "packing-n16-fractional", "certs")
        args = [os.path.join(d, f) for f in sorted(os.listdir(d))
                if f.startswith("cert_")]
    allok = True
    for p in args:
        ok, b, q = verify(p)
        allok &= ok
    print("\nALL CERTIFICATES VALID" if allok else "\nSOME CERTIFICATE INVALID")
