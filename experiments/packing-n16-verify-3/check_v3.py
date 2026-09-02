"""Independent checker (worker V3) for a covering certificate of T_a.

Written from problems/circle-packing-equilateral-triangle/README.md and RULES.md.
Every decision below is exact: Fraction, or Q(sqrt3) as a pair of Fractions.
No floating point enters any accept/reject decision.

WHAT IS CHECKED, and why it is what the pigeonhole needs
-------------------------------------------------------
Claim shape: T_a is covered by k closed sets each of diameter <= D.  If D < 1
then any set of points in T_a with pairwise distances >= 1 has at most one point
per set, so at most k points.  If D = 1 exactly, the covering certifies NOTHING
by itself (two points at distance exactly 1 may share a closed piece), and the
bound must come from a separate limiting argument.

  C1  every listed vertex lies in the closed triangle T_a
  C2  the listed vertices of each piece are in strictly convex position
      (order-independent: exact convex hull uses all of them)
  C3  max over all vertex pairs of each piece of the exact squared distance.
      Since a polygon is contained in the convex hull of its vertices and the
      diameter of a compact set equals that of its convex hull, this max is
      exactly the piece's squared diameter.
  C4  pairwise interior-disjointness: exact convex intersection has zero area
  C5  COVERAGE  T_a \\ union(P_i) = empty, computed by exact halfplane
      subtraction and NOT by any area identity.  Residue parts of zero area are
      discarded; that is sound because union(P_i) is closed, so T_a minus it is
      relatively open in T_a, and a nonempty relatively open subset of T_a has
      positive area.
  C6  area identity, reported as a cross-check only, never as evidence of C5
"""
import sys, json, itertools
from fractions import Fraction as F
from q3f import Q3, q3, ZERO, ONE, parse_exact
from geom import (cross, qform, area2, clip_halfplane, intersect_convex,
                  subtract_convex, point_in_convex, dedup, touches, contained_in)


def hull(points):
    """Exact ccw convex hull (monotone chain).  Returns hull vertices."""
    pts = sorted(set(points), key=lambda P: (P[0].p, P[0].q, P[1].p, P[1].q))
    # exact lexicographic sort by value, not by representation
    pts = list(points)
    pts.sort(key=lambda P: _key(P))
    uniq = []
    for P in pts:
        if not uniq or not (uniq[-1][0] == P[0] and uniq[-1][1] == P[1]):
            uniq.append(P)
    pts = uniq
    if len(pts) < 3:
        return pts
    lower = []
    for P in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], P).sign() <= 0:
            lower.pop()
        lower.append(P)
    upper = []
    for P in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], P).sign() <= 0:
            upper.pop()
        upper.append(P)
    return lower[:-1] + upper[:-1]


class _K:
    __slots__ = ("P",)

    def __init__(self, P):
        self.P = P

    def __lt__(self, o):
        if self.P[0] < o.P[0]:
            return True
        if o.P[0] < self.P[0]:
            return False
        return self.P[1] < o.P[1]


def _key(P):
    return _K(P)


def tri(a):
    return [(ZERO, ZERO), (a, ZERO), (ZERO, a)]


def check(a, faces, name="cert", verbose=True, max_nodes=200000):
    """Returns (ok, report dict).  a: Q3 side; faces: list of vertex lists."""
    rep = {"name": name, "a": (str(a.p), str(a.q)), "n_faces": len(faces)}
    errs = []
    T = tri(a)

    # ---- C1 containment of every vertex in the closed triangle -----------
    for i, f in enumerate(faces):
        for (u, v) in f:
            if u.sign() < 0 or v.sign() < 0 or (u + v > a):
                errs.append(f"C1 face {i}: vertex ({float(u):.6f},{float(v):.6f}) outside T_a")
    rep["C1_all_vertices_in_T_a"] = not errs

    # ---- C2 strict convexity, order-independent --------------------------
    polys = []
    order_matches = True
    for i, f in enumerate(faces):
        h = hull(f)
        if len(h) != len(f):
            errs.append(f"C2 face {i}: {len(f)} listed vertices but hull has {len(h)}"
                        " (a listed vertex is redundant / not strictly convex)")
            polys.append(h)
            continue
        polys.append(h)
        # is the listed cyclic order (up to rotation/reflection) the hull order?
        fl = list(f)
        rot = None
        for s in range(len(h)):
            if all(h[(s + t) % len(h)][0] == fl[t][0] and h[(s + t) % len(h)][1] == fl[t][1]
                   for t in range(len(h))):
                rot = s
        if rot is None:
            order_matches = False
    rep["C2_all_faces_strictly_convex"] = all("C2" not in e for e in errs)
    rep["C2_listed_order_is_ccw_cyclic"] = order_matches

    # ---- C3 exact squared diameters --------------------------------------
    diam2 = []
    for i, P in enumerate(polys):
        m = ZERO
        for X, Y in itertools.combinations(P, 2):
            d = qform(X, Y)
            if d > m:
                m = d
        diam2.append(m)
    mx = max(diam2, key=lambda z: (float(z)))
    # exact max
    mx = diam2[0]
    for d in diam2[1:]:
        if d > mx:
            mx = d
    rep["C3_max_squared_diameter"] = f"{mx.p} + {mx.q} sqrt3  (= {float(mx):.15f})"
    rep["C3_strictly_below_1"] = bool(mx < ONE)
    rep["C3_exactly_1"] = bool(mx == ONE)
    if mx > ONE:
        errs.append(f"C3: a piece has squared diameter {float(mx)} > 1")

    # ---- C4 pairwise interior disjointness -------------------------------
    overlaps = []
    for i, j in itertools.combinations(range(len(polys)), 2):
        I = intersect_convex(polys[i], polys[j])
        if len(I) >= 3 and area2(I).sign() != 0:
            overlaps.append((i, j, float(area2(I)) / 2))
    rep["C4_pairwise_interior_disjoint"] = not overlaps
    rep["C4_overlaps"] = overlaps

    # ---- C5 COVERAGE, no area shortcut -----------------------------------
    # Depth-first exact residue search.  Invariant: every element (Q, j) of the
    # stack is a closed convex polygon Q such that
    #     Q \\ union_{i} P_i  ==  Q \\ union_{i >= j} P_i
    # (pieces with index < j provably do not meet Q in positive area).
    # Q is split by the first piece that meets it; parts of zero area are
    # dropped, which is sound because union(P_i) is closed, so T_a minus it is
    # relatively open in T_a and a nonempty relatively open subset of T_a has
    # positive area.
    stack = [(T, 0)]
    uncovered = []
    nodes = 0
    peak = 1
    while stack:
        Qp, j = stack.pop()
        nodes += 1
        peak = max(peak, len(stack) + 1)
        if nodes > max_nodes:
            errs.append(f"C5: node budget {max_nodes} exhausted -- INCONCLUSIVE")
            uncovered = None
            break
        while j < len(polys) and not touches(Qp, polys[j]):
            j += 1
        if j == len(polys):
            uncovered.append(Qp)
            continue
        if contained_in(Qp, polys[j]):
            continue
        for part in subtract_convex(Qp, polys[j]):
            stack.append((part, j + 1))
    rep["C5_nodes"] = nodes
    rep["C5_peak_stack"] = peak
    if uncovered is None:
        rep["C5_covered"] = None
    else:
        rep["C5_uncovered_parts"] = len(uncovered)
        rep["C5_covered"] = (len(uncovered) == 0)
        if uncovered:
            wit = uncovered[0]
            cx = sum((V[0] for V in wit), ZERO) / q3(len(wit))
            cy = sum((V[1] for V in wit), ZERO) / q3(len(wit))
            rep["C5_witness_uncovered_point"] = (float(cx), float(cy))
            rep["C5_uncovered_area_chart"] = float(
                sum((area2(p) for p in uncovered), ZERO)) / 2
            errs.append(f"C5: {len(uncovered)} uncovered part(s), e.g. near "
                        f"({float(cx):.6f},{float(cy):.6f})")

    # ---- C6 area identity (cross-check only) -----------------------------
    tot = ZERO
    for P in polys:
        tot = tot + area2(P)
    tA = area2(T)
    rep["C6_area_sum_equals_T_a"] = bool(tot == tA)
    rep["C6_areas_chart"] = (f"{tot.p}+{tot.q}r3", f"{tA.p}+{tA.q}r3")

    rep["errors"] = errs
    ok = not errs
    rep["VERDICT"] = "PASS" if ok else "FAIL"
    if verbose:
        for k, v in rep.items():
            print(f"  {k}: {v}")
    return ok, rep


def _int(t):
    s = str(t).strip()
    if '.' in s:
        raise ValueError('decimal string in exact field')
    return int(s)


def load_json_cert(path):
    """Load a certificate written as JSON.  Exact fields only."""
    with open(path) as fh:
        raw = fh.read()
    D = json.loads(raw)
    # NOTE: this repo has no pinned JSON schema for covering certificates.
    # experiments/packing-n16-covering-2/cert_rational.json writes "a" as
    # [numerator, denominator] -- a RATIONAL pair -- while its coordinates are
    # plain "p/q" strings.  A [p, q] pair meaning p + q*sqrt3 is indistinguishable
    # from it.  Honour the a_is_ratio flag; default to the ratio reading.
    if isinstance(D["a"], list) and D.get("a_encoding", "ratio") == "ratio":
        a = Q3(F(_int(D["a"][0]), _int(D["a"][1])), 0)
    else:
        a = parse_exact(D["a"])
    faces = [[(parse_exact(c[0]), parse_exact(c[1])) for c in f] for f in D["faces_uv"]]
    return a, faces


if __name__ == "__main__":
    if len(sys.argv) > 1:
        a, faces = load_json_cert(sys.argv[1])
        print(f"=== {sys.argv[1]} : a = {float(a):.15f}")
        ok, _ = check(a, faces, name=sys.argv[1])
    else:
        import cert_v3
        a, faces = cert_v3.A_SIDE, cert_v3.faces()
        print(f"=== V3 transcription of n16-covering-2, a = 1+2sqrt3 = {float(a):.15f}")
        ok, _ = check(a, faces, name="n16-covering-2 (V3 transcription)")
    print("PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)
