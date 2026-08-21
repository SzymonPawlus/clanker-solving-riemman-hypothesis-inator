"""Freeze a float subdivision of the unit triangle into an EXACT rational certificate.

Exact rational arithmetic decides everything below; the floats only supply a starting
guess for the rounding.  Two steps:

 1. snap: scale the unit-triangle embedding to a rational side A and round every unique
    vertex to a rational, forcing boundary vertices exactly onto their side of T_A.
    Because the faces are index cycles of a fixed planar subdivision, the identity
    sum(shoelace of faces) = shoelace(T_A) holds for ANY rational vertex positions, so
    the area identity survives rounding automatically; convexity and the strict diameter
    bound are then verified, not assumed.
 2. dilate: with the exact max squared diameter D of the snapped certificate, the whole
    configuration may be scaled about the chart origin by any rational mu with
    mu^2 * D < 1 -- convexity, containment in T_{mu*A} and disjointness are all preserved
    by a dilation.  Leaving slack in the diameter throws away bound, so we take mu as
    large as the strict inequality allows.
"""
import json, math, sys
from fractions import Fraction as F
import verify_c1 as V


def snap(uv, A, den):
    """uv: unit-triangle float coords; A: exact rational side; den: rounding denominator"""
    out = []
    for (u, v) in uv:
        U = F(round(u * float(A) * den), den)
        W = F(round(v * float(A) * den), den)
        onu = abs(u) < 1e-9
        onv = abs(v) < 1e-9
        onw = abs(u + v - 1.0) < 1e-9
        if onu: U = F(0)
        if onv: W = F(0)
        if onw:
            if onu:   U, W = F(0), A
            elif onv: U, W = A, F(0)
            else:     W = A - U
        if U < 0: U = F(0)
        if W < 0: W = F(0)
        out.append((U, W))
    return out


def maxdiam2(faces):
    d = F(0)
    for f in faces:
        for i in range(len(f)):
            for j in range(i + 1, len(f)):
                q = V.Q(f[i][0] - f[j][0], f[i][1] - f[j][1])
                if q > d: d = q
    return d


def freeze(src, dst, den=10**9, mden=10**12, verbose=True):
    d = json.load(open(src))
    uv = d["uv"]; faces_idx = d["faces"]
    amax = d["a_max"]
    A = None
    for k in range(60):
        cand = F(int(amax * 10**8) - k * 10, 10**8)
        S = snap(uv, cand, den)
        P = [[S[i] for i in f] for f in faces_idx]
        D = maxdiam2(P)
        if D < 1:
            A = cand; break
    if A is None:
        raise SystemExit("could not snap below diameter 1")
    # dilate: pick the largest a' = k/10^m (small denominator, readable) with
    # (a'/A)^2 * D < 1, i.e. the largest side this configuration still covers strictly.
    A2 = None
    for m in (6, 7, 8, 9, 10, 11, 12):
        den2 = 10 ** m
        k = int(float(A) / math.sqrt(float(D)) * den2) + 2
        while F(k, den2) ** 2 * D >= A * A:
            k -= 1
        cand = F(k, den2)
        if A2 is None or cand > A2:
            A2 = cand
    mu = A2 / A
    P2 = [[(u * mu, w * mu) for (u, w) in f] for f in P]
    D2 = maxdiam2(P2)
    assert D2 < 1
    if verbose:
        print("snapped at a = %s  (max sq diam %.15f)" % (A, float(D)))
        print("dilated by mu = %s  ->  a = %s = %.12f" % (mu, A2, float(A2)))
        print("exact max squared diameter now %.15f  < 1 : %s" % (float(D2), D2 < 1))
    json.dump({"a": [str(A2.numerator), str(A2.denominator)],
               "faces_uv": [[[str(u), str(w)] for (u, w) in f] for f in P2],
               "max_sq_diam": str(D2),
               "source": src},
              open(dst, "w"), indent=1)
    return A2, D2


if __name__ == "__main__":
    freeze(sys.argv[1], sys.argv[2],
           den=int(sys.argv[3]) if len(sys.argv) > 3 else 10**9)
