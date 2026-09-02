#!/usr/bin/env python3
"""V6 INDEPENDENT checker for fractional covering certificates (Lemma F).

Written from the Lemma F statement and the certificate field names only.
Deliberately uses a DIFFERENT algorithm from
experiments/packing-n16-fracverify/fracverify.py for the load-bearing check (D):

  fracverify  : carry (region, accumulated weight), split regions against
                pieces, drop regions once acc >= K.
  v6check     : build the ARRANGEMENT of all supporting lines of all piece
                edges together with the three lines of T_N.  Every
                full-dimensional cell of that arrangement inside T_N is bounded
                (T_N's own edges are lines of the arrangement), so every such
                cell has at least one vertex of the arrangement on its boundary.
                The total-weight function W(x) = sum_{i : x in S_i} w_i is
                constant on each open cell, and for x on any lower-dimensional
                face and any full-dim cell C with x in closure(C) we have
                W(x) >= W(C) because every piece is CLOSED.  Hence
                     min_{T_N} W = min over full-dim cells of W(cell),
                and it suffices to evaluate W just inside each sector around
                each arrangement vertex.  Evaluation "just inside" is done
                exactly with a symbolic infinitesimal: a point p + eps*d lies in
                the closed halfplane a.x >= c iff (a.p-c) > 0, or (a.p-c) == 0
                and a.d >= 0.  No sampling, no floats, no area identity.

Everything is fractions.Fraction.  No numpy/scipy anywhere.
"""
import json, os, sys, itertools
from fractions import Fraction as F


# ---------------------------------------------------------------- geometry --
def cross(ax, ay, bx, by):
    return ax * by - ay * bx


def poly_is_convex_ccw(P):
    """True iff P is a strictly-or-weakly convex polygon traversed ccw with
    positive area and no repeated / collinear-backtracking vertices."""
    n = len(P)
    if n < 3:
        return False
    A2 = sum(P[i][0] * P[(i + 1) % n][1] - P[(i + 1) % n][0] * P[i][1]
             for i in range(n))
    if A2 <= 0:
        return False
    for i in range(n):
        a, b, c = P[i], P[(i + 1) % n], P[(i + 2) % n]
        if cross(b[0] - a[0], b[1] - a[1], c[0] - b[0], c[1] - b[1]) < 0:
            return False
        if a == b:
            return False
    return True


def halfplanes(P):
    """Convex ccw polygon -> list of (a, b, c) meaning a*u + b*v >= c."""
    H = []
    n = len(P)
    for i in range(n):
        (x1, y1), (x2, y2) = P[i], P[(i + 1) % n]
        dx, dy = x2 - x1, y2 - y1
        if dx == 0 and dy == 0:
            continue
        # interior is to the LEFT: cross(d, x-p) >= 0  ->  -dy*u + dx*v >= -dy*x1+dx*y1
        a, b = -dy, dx
        c = a * x1 + b * y1
        H.append((a, b, c))
    return H


def sqQ(p, q):
    du, dv = p[0] - q[0], p[1] - q[1]
    return du * du + du * dv + dv * dv


# ------------------------------------------------------------ cert decoding --
def rat(z):
    """Accept int or exact rational string.  REJECT decimal strings and floats
    (problem RULES.md section 2 bans decimal strings in exact fields)."""
    if isinstance(z, bool):
        raise ValueError("bool in exact field")
    if isinstance(z, int):
        return F(z)
    if isinstance(z, float):
        raise ValueError("float in exact field: %r" % (z,))
    if isinstance(z, str):
        if "." in z or "e" in z.lower():
            raise ValueError("decimal string in exact field: %r" % (z,))
        return F(z)
    raise ValueError("bad exact value %r" % (z,))


def decode_piece(spec):
    """-> ccw convex polygon (list of (F,F)) or raise."""
    kind = spec["kind"]
    if kind == "poly":
        P = [(rat(x), rat(y)) for x, y in spec["verts"]]
    elif kind == "box":
        ulo, uhi, vlo, vhi, wlo, whi = (rat(z) for z in spec["bounds"])
        # {ulo<=u<=uhi, vlo<=v<=vhi, wlo<=u+v<=whi}: intersect 6 halfplanes.
        # Build by exact halfplane intersection from scratch (no clipping code
        # shared with the author's checker): enumerate all pairwise line
        # intersections of the 6 boundary lines and keep the feasible ones,
        # then take their convex hull.
        Hs = [(F(1), F(0), ulo), (F(-1), F(0), -uhi),
              (F(0), F(1), vlo), (F(0), F(-1), -vhi),
              (F(1), F(1), wlo), (F(-1), F(-1), -whi)]
        pts = []
        for (a1, b1, c1), (a2, b2, c2) in itertools.combinations(Hs, 2):
            det = a1 * b2 - a2 * b1
            if det == 0:
                continue
            x = (c1 * b2 - c2 * b1) / det
            y = (a1 * c2 - a2 * c1) / det
            if all(a * x + b * y >= c for (a, b, c) in Hs):
                pts.append((x, y))
        P = convex_hull(sorted(set(pts)))
        if len(P) < 3:
            return []
    else:
        raise ValueError("unknown piece kind %r" % kind)
    if not poly_is_convex_ccw(P):
        P = P[::-1]
        if not poly_is_convex_ccw(P):
            raise ValueError("piece is not a convex polygon: %r" % (P,))
    return P


def convex_hull(pts):
    if len(pts) < 3:
        return list(pts)
    def half(ps):
        out = []
        for p in ps:
            while len(out) >= 2 and cross(out[-1][0] - out[-2][0], out[-1][1] - out[-2][1],
                                          p[0] - out[-1][0], p[1] - out[-1][1]) <= 0:
                out.pop()
            out.append(p)
        return out
    lo = half(pts)
    hi = half(pts[::-1])
    return lo[:-1] + hi[:-1]


# ------------------------------------------------------------------ checker --
def check(path, verbose=True):
    blob = json.load(open(path))
    c = blob["certificate"]
    N = rat(c["N_units"])
    K = rat(c["K"])
    budget = rat(c["budget_points"])
    unit = c["unit"]
    UNIT = F(unit).denominator if isinstance(unit, str) else F(unit).denominator
    weights = {k: rat(v) for k, v in c["weights"].items()}
    fails = []

    if any(w < 0 for w in weights.values()):
        fails.append("negative weight present")

    polys = {}
    for k in weights:
        if k not in c["pieces"]:
            fails.append("weighted piece %s has no spec" % k)
            continue
        polys[k] = decode_piece(c["pieces"][k])

    # (A) each piece inside T_N = {u>=0, v>=0, u+v<=N}
    for k, P in polys.items():
        if not P:
            fails.append("piece %s empty" % k)
            continue
        for (u, v) in P:
            if u < 0 or v < 0 or u + v > N:
                fails.append("piece %s vertex (%s,%s) outside T_%s" % (k, u, v, N))

    # (B) diameter strictly below the separation: Qmax < UNIT^2
    qmax = max((max(sqQ(P[i], P[j]) for i in range(len(P)) for j in range(i))
                for P in polys.values() if P), default=F(0))
    if not qmax < UNIT * UNIT:
        fails.append("Qmax %s not < UNIT^2 %s (pieces not smaller than separation)"
                     % (qmax, UNIT * UNIT))

    # (C) budget: total weight strictly below budget*K
    tot = sum(weights.values())
    if not tot < budget * K:
        fails.append("total weight %s not < %s" % (tot, budget * K))

    # (D) covering: min over T_N of sum of weights of containing pieces >= K
    TN = [(F(0), F(0)), (N, F(0)), (F(0), N)]
    HT = halfplanes(TN)
    PH = {k: halfplanes(P) for k, P in polys.items() if P}

    lines = list(HT)
    for k in PH:
        lines.extend(PH[k])
    # dedupe lines up to scaling
    uniq = {}
    for (a, b, cc) in lines:
        g = a if a != 0 else b
        key = (a / g, b / g, cc / g)
        uniq[key] = (a, b, cc)
    lines = list(uniq.values())

    verts = set()
    for (a1, b1, c1), (a2, b2, c2) in itertools.combinations(lines, 2):
        det = a1 * b2 - a2 * b1
        if det == 0:
            continue
        x = (c1 * b2 - c2 * b1) / det
        y = (a1 * c2 - a2 * c1) / det
        if all(a * x + b * y >= cc for (a, b, cc) in HT):   # inside closed T_N
            verts.add((x, y))

    worst = None
    for p in sorted(verts):
        # directions: for every line through p, both unit-ish direction vectors
        dirs = []
        for (a, b, cc) in lines:
            if a * p[0] + b * p[1] == cc:
                dirs.append((b, -a))
                dirs.append((-b, a))
        if not dirs:
            dirs = [(F(1), F(0)), (F(-1), F(0)), (F(0), F(1)), (F(0), F(-1))]
        # sort by angle exactly
        def keyf(d):
            x, y = d
            if y > 0 or (y == 0 and x > 0):
                h = 0
            else:
                h = 1
            return (h, F(0))
        def angle_cmp(d1, d2):
            return None
        # bucket-sort by half plane then by cross product
        upper = [d for d in dirs if d[1] > 0 or (d[1] == 0 and d[0] > 0)]
        lower = [d for d in dirs if not (d[1] > 0 or (d[1] == 0 and d[0] > 0))]
        import functools
        def cmp(d1, d2):
            cr = cross(d1[0], d1[1], d2[0], d2[1])
            return -1 if cr > 0 else (1 if cr < 0 else 0)
        upper.sort(key=functools.cmp_to_key(cmp))
        lower.sort(key=functools.cmp_to_key(cmp))
        order = upper + lower
        # dedupe by direction
        ded = []
        for d in order:
            if ded and cross(ded[-1][0], ded[-1][1], d[0], d[1]) == 0 and \
               (d[0] * ded[-1][0] + d[1] * ded[-1][1]) > 0:
                continue
            ded.append(d)
        order = ded
        probes = []
        m = len(order)
        for i in range(m):
            d1, d2 = order[i], order[(i + 1) % m]
            if cross(d1[0], d1[1], d2[0], d2[1]) > 0:
                probes.append((d1[0] + d2[0], d1[1] + d2[1]))
            elif m == 1:
                probes.append((-d1[0], -d1[1]))
        if not probes:
            probes = list(order)
        for d in probes:
            if not inside_eps(p, d, HT):
                continue
            w = sum(weights[k] for k in PH if inside_eps(p, d, PH[k]))
            if worst is None or w < worst[0]:
                worst = (w, p, d)
    if worst is None:
        fails.append("no probe points found (arrangement construction failed)")
    elif worst[0] < K:
        fails.append("covering FAILS: weight %s/%s < 1 near %s dir %s"
                     % (worst[0], K, worst[1], worst[2]))

    ok = not fails
    if verbose:
        print("--- %s" % os.path.basename(path))
        print("    N=%s unit=1/%s K=%s budget=%s pieces=%d lines=%d arr.verts=%d"
              % (N, UNIT, K, budget, len(polys), len(lines), len(verts)))
        print("    (A) containment            : %s" % ok_str(fails, "outside"))
        print("    (B) Qmax=%s < UNIT^2=%s : %s" % (qmax, UNIT * UNIT, ok_str(fails, "Qmax")))
        print("    (C) total weight %s < %s : %s" % (tot, budget * K, ok_str(fails, "total weight")))
        print("    (D) min incident weight    : %s  (%s)"
              % (worst[0] if worst else None, ok_str(fails, "covering")))
        if qmax > 0:
            print("    => a_%s >= %s/sqrt(%s) = %.12f"
                  % (budget, N, qmax, float(N) / float(qmax) ** 0.5))
        print("    VERDICT: %s" % ("VALID" if ok else "INVALID"))
        for f in fails:
            print("      !", f)
    return ok, fails


def ok_str(fails, needle):
    return "FAIL" if any(needle in f for f in fails) else "ok"


def inside_eps(p, d, H):
    """Is p + eps*d in the closed region {a.x >= c} for all small eps > 0?"""
    for (a, b, c) in H:
        s = a * p[0] + b * p[1] - c
        if s < 0:
            return False
        if s == 0 and a * d[0] + b * d[1] < 0:
            return False
    return True


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        d = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "..", "packing-n16-fractional", "certs")
        args = [os.path.join(d, f) for f in sorted(os.listdir(d))
                if f.startswith("cert_")]
    allok = True
    for p in args:
        try:
            ok, _ = check(p)
        except Exception as e:
            print("--- %s\n    EXCEPTION: %s: %s" % (os.path.basename(p), type(e).__name__, e))
            ok = False
        allok &= ok
    print("\nALL VALID" if allok else "\nSOME INVALID")
