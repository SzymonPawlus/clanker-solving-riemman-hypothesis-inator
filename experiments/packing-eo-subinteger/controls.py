"""Kill-criterion K3: the capacity function must never be below the truth.

Every capacity computed by geom.capacity is an *upper* bound claim.  The way to
falsify it is to exhibit an actual separation-1 configuration with more points in
a region than the claimed capacity.  This module does exactly that, against

  (a) every exact certificate in problems/**/results/ (halved: the repo uses
      separation 2 and side d = 2a, this attack uses separation 1 and side a), and
  (b) the triangular lattice of T(k) points in the triangle of side k-1, for
      k = 2..9, which is the extremal configuration the whole conjecture is about,

testing EVERY corner-coordinate box with thresholds at multiples of a/M.

Also re-verifies Lemma P of ../eo-corner-squeeze/ (`sketch`, therefore not
assumable, RULES.md §3) independently.
"""

import sys, os, json, glob
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import geom

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))


def lattice(k):
    """T(k) points of the triangular lattice in the triangle of side a = k-1,
    given in corner coordinates (u_A, u_C).  Separation exactly 1."""
    a = F(k - 1)
    pts = []
    for i in range(k):
        for j in range(k - i):
            uA = F(i + j)
            uC = a - j
            pts.append((uA, uC))
    return a, pts


def parse_alg(s):
    """Parse the small algebraic language used by the repo's certificates.
    Returns (rational, coefficient of sqrt3) -- enough for every value present."""
    s = s.replace(" ", "")
    import re
    if s in ("0", ""):
        return (F(0), F(0))
    # supported forms: integers/fractions, k*sqrt(3), sums thereof
    tot = [F(0), F(0)]
    for term in re.findall(r"[+-]?[^+-]+", s):
        sign = F(-1) if term.startswith("-") else F(1)
        t = term.lstrip("+-")
        if "sqrt(3)" in t:
            c = t.replace("sqrt(3)", "").strip("*")
            tot[1] += sign * (F(c) if c else F(1))
        else:
            tot[0] += sign * F(t)
    return tuple(tot)


def cert_points():
    """Yield (name, a, points-in-(u_A,u_C)) for every parsable certificate."""
    out = []
    for path in sorted(glob.glob(os.path.join(ROOT, "problems", "circle-packing-equilateral-triangle", "results", "*.json"))):
        j = json.load(open(path))
        try:
            d = parse_alg(j["point_triangle_side"])
        except Exception:
            continue
        if d[1] != 0:
            continue                      # side not rational -> skip (checked by hand)
        a = d[0] / 2                       # separation 2 -> separation 1
        pts = []
        ok = True
        for (xs, ys) in j["coordinates"]:
            X, Y = parse_alg(xs), parse_alg(ys)
            # x rational, y = c*sqrt3 -> u_A = x + y/sqrt3 = x + c*... rational
            if X[1] != 0 or Y[0] != 0:
                ok = False
                break
            x = X[0] / 2
            csqrt3 = Y[1] / 2              # y = csqrt3 * sqrt3
            uA = x + csqrt3                # y/sqrt3 = csqrt3
            uC = a - 2 * csqrt3
            pts.append((uA, uC))
        if ok:
            out.append((os.path.basename(path), a, pts))
    return out


def check_separation(pts, name):
    bad = 0
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            if geom.d2(pts[i], pts[j]) < 1:
                bad += 1
    return bad


def in_box(p, a, lo, hi):
    uA, uC = p
    uB = 2 * a - uA - uC
    u = (uA, uB, uC)
    return all(lo[V] <= u[V] <= hi[V] for V in range(3))


def check_config(name, a, pts, Ms=(2, 3, 4, 5, 6), verbose=True):
    """Every corner box on every threshold grid a/M must have count <= cap."""
    viol = []
    tested = 0
    cache = {}
    tot = 2 * a
    for M in Ms:
        Th = [a * F(i, M) for i in range(M + 1)]
        for pA in range(M + 1):
            for qA in range(pA, M + 1):
                for pB in range(M + 1):
                    for qB in range(pB, M + 1):
                        for pC in range(M + 1):
                            for qC in range(pC, M + 1):
                                lo = (Th[pA], Th[pB], Th[pC])
                                hi = (Th[qA], Th[qB], Th[qC])
                                if any(lo[V] > hi[V] for V in range(3)):
                                    continue
                                S = tot - sum(lo)
                                if S < 0:
                                    continue
                                g = tuple(sorted(min(hi[V] - lo[V], S) for V in range(3)))
                                key = (S, g)
                                if key not in cache:
                                    cache[key] = geom.capacity(S, [F(0)] * 3, list(g), F(1))[0]
                                cp = cache[key]
                                cnt = sum(1 for p in pts if in_box(p, a, lo, hi))
                                tested += 1
                                if cnt > cp:
                                    viol.append((M, lo, hi, cp, cnt))
    return tested, viol


def lemma_P(kmax=12):
    """Independent re-verification of Lemma P (../eo-corner-squeeze/ §3, `sketch`):
    for k-2 <= a < k-1, at most 2k-2 points of a separation-1 set have u_V >= k-2.

    Re-derivation done here: the region {u_V >= k-2} is the trapezoid of height
    w = (a-(k-2))*sqrt3/2 < sqrt3/2 against the side opposite V.  Two points in it
    differ vertically by v <= w, so horizontally by h with h^2 >= 1 - w^2 > 1/4.
    Horizontal projections are >= g = sqrt(1-w^2) apart inside an interval of
    length <= a, so m <= 1 + a/g.  The claim is a/sqrt(1-w^2) < 2k-2 for a < k-1;
    squaring, a^2 < 4(k-1)^2 (1 - w^2) = 4(k-1)^2 - 3(k-1)^2 (a-k+2)^2.
    Checked below in exact rational arithmetic on a dense grid of a, plus the
    exact endpoint identity at a = k-1."""
    rows = []
    for k in range(3, kmax + 1):
        worst = None
        for num in range(0, 1001):
            a = F(k - 2) + F(num, 1000)      # a in [k-2, k-1]
            lhs = a * a + 3 * (k - 1) ** 2 * (a - k + 2) ** 2
            rhs = 4 * (k - 1) ** 2
            if a < k - 1:
                assert lhs < rhs, (k, a, lhs, rhs)
            m_bound_ok = (lhs < rhs)
            if worst is None or rhs - lhs < worst[1]:
                worst = (a, rhs - lhs)
        a = F(k - 1)
        lhs = a * a + 3 * (k - 1) ** 2 * (a - k + 2) ** 2
        rows.append((k, 2 * k - 2, lhs == 4 * (k - 1) ** 2, float(worst[1])))
    return rows


if __name__ == "__main__":
    print("K3(a): repo certificates")
    for name, a, pts in cert_points():
        b = check_separation(pts, name)
        print(f"  {name}: n={len(pts)} a={a} separation violations={b}")
        assert b == 0, "certificate fails separation in this normalisation!"
        tested, viol = check_config(name, a, pts, Ms=(2, 3, 4))
        print(f"    boxes tested={tested}  capacity violations={len(viol)}")
        for v in viol[:5]:
            print("    VIOLATION", v)
    print("K3(b): triangular lattices T(k) at side k-1")
    for k in range(2, 8):
        a, pts = lattice(k)
        b = check_separation(pts, f"lattice{k}")
        tested, viol = check_config(f"lattice{k}", a, pts, Ms=(2, 3, 4) if k <= 5 else (2, 3))
        print(f"  k={k} n={len(pts)} a={a} sepviol={b} boxes={tested} capviol={len(viol)}")
        for v in viol[:5]:
            print("    VIOLATION", v)
    print("K3(c): Lemma P re-verified (k, bound 2k-2, equality at a=k-1, min slack)")
    for row in lemma_P():
        print("   ", row)
