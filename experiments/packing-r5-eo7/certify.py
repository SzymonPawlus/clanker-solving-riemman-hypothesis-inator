"""Certified branch-and-bound for the lattice-count bound in T(a).

THEOREM SHAPE (statement + reduction proof: attacks/r5-eo7/README.md).  Let Lambda be a
lattice in R^2 whose shortest non-zero vector has length >= 1, let t in R^2, and let
a' < a with a a positive integer.  Then

    | (Lambda + t) cap T(a') |  <=  N(a),

with N(a) certified here.  For a = 6, Erdos-Oler at k = 7 needs N(6) <= 26, because 27
points at side < 6 would refute EO(7).  THIS IS THE LATTICE CASE ONLY -- real packings
need not be lattice subsets.  See the write-up for the (unproved) forcing hypothesis
that would be needed to reach EO(7).

REDUCTION.  Rescale by a/a' > 1: the triangle becomes T(a) and the lattice separation
becomes r > 1.  Take v1 a shortest vector, r = |v1| >= 1, (v1,v2) Lagrange-reduced,
h = covol/r >= r*sqrt(3)/2 > sqrt(3)/2.  Then Lambda+t lies on lines parallel to v1
spaced h apart, with points spaced exactly r > 1 on each line, so a chord of length
L > 0 carries at most ceil(L) points and a chord of length 0 at most 1.  Hence the
count is at most sum_j c(ell_j) over the chords ell_j of T(a).

CHORD PROFILE.  For phi in [0, pi/3] the vertex projections on n = (-sin,cos) order as
B < A < C; writing s for the level measured from the minimum,
    d1 = a sin(phi),   w = a cos(phi - pi/6),   L* = (a sqrt3/2)/cos(phi - pi/6),
    K  = L*/(w - d1) = sqrt3/(cos 2phi + 1/2)          (independent of a),
    ell(s) = L* s/d1        (0 <= s <= d1, "rising"),
    ell(s) = L* - K(s - d1) (d1 <= s <= w, "falling").
Symbolic facts used as hard caps (proved in the write-up):
    (F1) L* <= a  on [0, pi/6];
    (F2) K h >= 1 whenever h >= sqrt3/2;
    (F3) L* - K h <= a - 1 on [0, pi/6], h >= sqrt3/2, with equality only at
         (phi, h) = (0, sqrt3/2);
    (F4) L* h / d1 >= 3/2 on (0, pi/6], h >= sqrt3/2.

PARAMETERS (3): phi in [0, pi/6] (D3 symmetry of T folds direction space to this),
                kappa >= 1 with h = kappa sqrt3/2,
                rho in [0,1]: the topmost line at level <= d1 sits at s = (1-rho) d1.
Regimes:  R1 = no line at level <= d1  -> Lemma A gives  <= a(a+1)/2 + 1, no computation.
          R2 = otherwise               -> branch and bound below.

STATUS: numerical (the branch-and-bound), sketch (the reduction and F1-F4).  Not assumable.
"""
import json, math, sys
from fractions import Fraction
from mpmath import iv, mp, mpf

iv.dps = 30
mp.dps = 50

PI = iv.pi
SQ3 = iv.sqrt(3)
PI6 = PI / 6


def _m(q):
    if isinstance(q, Fraction):
        return mpf(q.numerator) / mpf(q.denominator)
    return q


def _c(x_sup, cap):
    """Contribution of a chord whose length is at most x_sup (spacing > 1)."""
    if x_sup < 0:
        return 0
    return min(cap, max(1, math.ceil(x_sup)))


class Box:
    __slots__ = ("phi", "kap", "rho")

    def __init__(self, phi, kap, rho):
        self.phi, self.kap, self.rho = phi, kap, rho

    def widths(self):
        return (float(self.phi[1] - self.phi[0]), float(self.kap[1] - self.kap[0]),
                float(self.rho[1] - self.rho[0]))

    def split(self):
        w = self.widths()
        k = max(range(3), key=lambda i: w[i] / (float(PI6.b), 6.0, 1.0)[i])
        parts = [self.phi, self.kap, self.rho]
        lo, hi = parts[k]
        mid = Fraction(lo + hi, 2) if isinstance(lo, Fraction) else (lo + hi) / 2
        A = list(parts); B = list(parts)
        A[k] = (lo, mid); B[k] = (mid, hi)
        return Box(*A), Box(*B)

    def as_json(self):
        f = lambda t: [float(t[0]), float(t[1])]
        return {"phi": f(self.phi), "kappa": f(self.kap), "rho": f(self.rho)}


def _pieces(a, plo, phi_, kaplo, rho):
    """Interval quantities on phi in [plo, phi_], at kappa = kaplo, rho = rho."""
    p = iv.mpf([plo, phi_])
    cm = iv.cos(p - PI6)
    s = iv.sin(p)
    c = iv.cos(p)
    c2 = iv.cos(2 * p)
    A = iv.mpf(a)
    Lstar = (A * SQ3 / 2) / cm
    K = SQ3 / (c2 + iv.mpf(1) / 2)
    h = iv.mpf([_m(kaplo), _m(kaplo)]) * SQ3 / 2
    d1 = A * s
    return p, cm, s, c, c2, Lstar, K, h, d1


def _fall0(a, plo, phi_, kaplo, rhohi):
    """Interval for ell^fall_0 = L* - K h + rho K d1 on phi in [plo, phi_]."""
    if plo == 0 and phi_ == 0:                      # exact slice: d1 = 0, L* = a, K h = kappa
        v = float(Fraction(a) - kaplo)
        return iv.mpf([v, v])
    _, _, _, _, _, Ls, K, h, d1 = _pieces(a, plo, phi_, kaplo, rhohi)
    return Ls - K * h + iv.mpf([_m(rhohi), _m(rhohi)]) * K * d1


def _dfall0(a, plo, phi_, kaplo, rhohi):
    p, cm, s, c, c2, Ls, K, h, d1 = _pieces(a, plo, phi_, kaplo, rhohi)
    A = iv.mpf(a)
    dL = (A * SQ3 / 2) * iv.sin(p - PI6) / (cm ** 2)
    den = c2 + iv.mpf(1) / 2
    dK = SQ3 * 2 * iv.sin(2 * p) / (den ** 2)
    rho = iv.mpf([_m(rhohi), _m(rhohi)])
    return dL - dK * h + rho * (dK * d1 + K * A * c)


def _sup_fall0(a, box, depth=8):
    """Monotonicity-aware rigorous sup of ell^fall_0 over the box."""
    kaplo, rhohi = box.kap[0], box.rho[1]

    def rec(plo, phi_, d):
        if plo == phi_:
            return float(_fall0(a, plo, phi_, kaplo, rhohi).b)
        v = float(_fall0(a, plo, phi_, kaplo, rhohi).b)
        if d <= 0:
            return v
        g = _dfall0(a, plo, phi_, kaplo, rhohi)
        if g.b <= 0:
            return float(_fall0(a, plo, plo, kaplo, rhohi).b)
        if g.a >= 0:
            return float(_fall0(a, phi_, phi_, kaplo, rhohi).b)
        mid = (plo + phi_) / 2
        return max(rec(plo, mid, d - 1), rec(mid, phi_, d - 1))

    v = rec(box.phi[0], box.phi[1], depth)
    return min(v, float(a) - 1 + float(rhohi) * _kd1_sup(a, box))


def _kd1_sup(a, box):
    p = iv.mpf([box.phi[0], box.phi[1]])
    K = SQ3 / (iv.cos(2 * p) + iv.mpf(1) / 2)
    return float((K * iv.mpf(a) * iv.sin(p)).b)


def _sup_rise0(a, box):
    """ell^rise_0 = L*(1-rho); decreasing in phi and in rho, so sup at (phi_lo, rho_lo)."""
    plo, rholo = box.phi[0], box.rho[0]
    if plo == 0:
        return float(Fraction(a) * (1 - rholo))
    Ls = (iv.mpf(a) * SQ3 / 2) / iv.cos(iv.mpf([plo, plo]) - PI6)
    return float((Ls * (1 - iv.mpf([_m(rholo), _m(rholo)]))).b)


def _kh_lo(a, box):
    p = iv.mpf([box.phi[0], box.phi[1]])
    K = SQ3 / (iv.cos(2 * p) + iv.mpf(1) / 2)
    h = iv.mpf([_m(box.kap[0]), _m(box.kap[0])]) * SQ3 / 2
    return max(1.0, float((K * h).a))            # (F2)


def _risestep_lo(a, box):
    """Lower bound on L* h / d1 (the drop between consecutive rising chords)."""
    p = iv.mpf([box.phi[0], box.phi[1]])
    Ls = (iv.mpf(a) * SQ3 / 2) / iv.cos(p - PI6)
    h = iv.mpf([_m(box.kap[0]), _m(box.kap[0])]) * SQ3 / 2
    d1 = iv.mpf(a) * iv.sin(p)
    if float(d1.a) <= 0:
        return None                              # no i >= 1 rising line possible here
    return max(1.5, float((Ls * h / d1).a))      # (F4)


def _nrise_max(a, box):
    """Max number of rising lines: they sit at s = (1-rho)d1 - i h >= 0."""
    d1hi = float(a) * math.sin(float(box.phi[1]))
    hlo = float(box.kap[0]) * math.sqrt(3) / 2
    return int(math.floor(d1hi / hlo)) + 1


def box_bound(a, box):
    cap = int(a)                                  # (F1): every chord is <= L* <= a
    tot = 0
    f0 = _sup_fall0(a, box)
    step = _kh_lo(a, box)
    i = 0
    while True:
        u = f0 - i * step
        if u < 0:
            break
        tot += _c(u, cap)
        i += 1
        if i > 4 * a:
            break
    r0 = _sup_rise0(a, box)
    nr = _nrise_max(a, box)
    rs = _risestep_lo(a, box)
    for i in range(nr):
        u = r0 if i == 0 else (None if rs is None else r0 - i * rs)
        if u is None or u < 0:
            break
        tot += _c(u, cap)
    return tot


def bnb(a, target, max_boxes=2000000, out=None, minwidth=1e-9, progress=20000):
    kmax = Fraction(math.ceil(2 * (a + 1) / math.sqrt(3)) + 1)
    root = Box((mpf(0), PI6.b), (Fraction(1), kmax), (Fraction(0), Fraction(1)))
    stack = [root]
    worst = 0
    stalled = []
    n = 0
    while stack:
        if n >= max_boxes:
            stalled.extend(stack)
            break
        b = stack.pop()
        n += 1
        if progress and n % progress == 0:
            print(json.dumps({"boxes": n, "stack": len(stack), "worst": worst,
                              "stalled": len(stalled)}), flush=True)
            if out:
                json.dump({"partial": True, "boxes": n, "worst": worst,
                           "stalled": len(stalled)}, open(out + ".progress", "w"))
        v = box_bound(a, b)
        if v <= target:
            worst = max(worst, v)
            continue
        if max(b.widths()) < minwidth:
            stalled.append(b); worst = max(worst, v)
            continue
        stack.extend(b.split())
    stats = {"a": a, "target": target, "boxes_processed": n, "stalled": len(stalled),
             "worst_certified_R2": worst, "R1_lemmaA": a * (a + 1) // 2 + 1,
             "certified_overall": max(worst, a * (a + 1) // 2 + 1) if not stalled else None}
    if out:
        json.dump({"stats": stats, "stalled_boxes": [x.as_json() for x in stalled[:200]]},
                  open(out, "w"), indent=1)
    return worst, stalled, stats


if __name__ == "__main__":
    a = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    target = int(sys.argv[2]) if len(sys.argv) > 2 else 26
    out = sys.argv[3] if len(sys.argv) > 3 else None
    worst, stalled, stats = bnb(a, target, out=out)
    print(json.dumps(stats, indent=1))
