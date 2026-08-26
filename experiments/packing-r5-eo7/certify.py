"""Certified branch-and-bound for the lattice-count bound at side a.

THEOREM SHAPE (see attacks/r5-eo7/README.md for the statement and the proof of the
reduction).  Let Lambda be a lattice in R^2 whose shortest non-zero vector has length
>= 1, let t in R^2, and let a' < a.  Then

    | (Lambda + t)  cap  T(a') |  <=  N(a),

where N(a) is what this program certifies.  For a = 6 the Erdos-Oler k = 7 target is
N(6) <= 26 (since 27 points at side < 6 would refute EO(7)).

REDUCTION (all of it is re-derived in the write-up):
  * rescale by a/a' > 1 so the triangle is T(a) and the lattice separation is r > 1;
  * take v1 a shortest vector, r = |v1|, (v1,v2) Lagrange-reduced, h = covol/r >= r*sqrt(3)/2
    > sqrt(3)/2; Lambda+t lies on lines parallel to v1 spaced h apart, points spaced r
    on each line;
  * a chord of length L carries at most ceil(L) points when the spacing is > 1
    (and at most 1 when L = 0), so the count is at most  sum_j c(ell_j)  where ell_j
    is the chord length of T(a) on line j.

PARAMETERS (3):  phi in [0, pi/6]  (line direction, folded by the D3 symmetry of T),
                 kappa >= 1 with h = kappa*sqrt(3)/2,
                 rho in [0,1]      (see below).

Two regimes.
  R1  no line meets the "rising" side of the chord profile.  Lemma A (symbolic, in the
      write-up) gives  sum <= Delta(a) + 1  with no computation.
  R2  some line does.  Let that line (the topmost one at or below the peak) sit at
      s = d1 - rho*d1.  Then everything is an explicit function of (phi, kappa, rho)
      and this file branch-and-bounds it.

STATUS: numerical (the branch-and-bound), sketch (the reduction).  Not assumable.
"""
import json, os, sys
from fractions import Fraction
from mpmath import iv, mp, mpf

iv.dps = 40
mp.dps = 60

PI = iv.pi
SQ3 = iv.sqrt(3)
PI6 = PI / 6


def _m(q):
    """Exact mpf for a Fraction with a power-of-two denominator (all box endpoints are)."""
    if isinstance(q, Fraction):
        return mpf(q.numerator) / mpf(q.denominator)
    return q


def _c(x_sup):
    """Contribution cap of a chord whose length is at most x_sup, points spaced > 1."""
    if x_sup < 0:
        return 0
    import math
    v = math.ceil(x_sup)
    return max(1, v)


class Box:
    __slots__ = ("phi", "kap", "rho")

    def __init__(self, phi, kap, rho):
        self.phi = phi  # (lo, hi) as mpf
        self.kap = kap
        self.rho = rho

    def widths(self):
        return (float(self.phi[1] - self.phi[0]), float(self.kap[1] - self.kap[0]),
                float(self.rho[1] - self.rho[0]))

    def split(self):
        w = self.widths()
        k = max(range(3), key=lambda i: w[i] / (float(PI6.b), 6.0, 1.0)[i])
        lo, hi = (self.phi, self.kap, self.rho)[k]
        mid = (lo + hi) / 2 if not isinstance(lo, Fraction) else Fraction(lo + hi, 2)
        a = [self.phi, self.kap, self.rho]
        b = [self.phi, self.kap, self.rho]
        a[k] = (lo, mid)
        b[k] = (mid, hi)
        return Box(*a), Box(*b)

    def as_json(self):
        f = lambda t: [float(t[0]), float(t[1])]
        return {"phi": f(self.phi), "kappa": f(self.kap), "rho": f(self.rho)}


# ---------------------------------------------------------------- trig pieces
def _trig(philo, phihi):
    p = iv.mpf([philo, phihi])
    cm = iv.cos(p - PI6)          # cos(phi - pi/6)   in [sqrt3/2, 1]
    cp = iv.cos(p + PI6)          # cos(phi + pi/6)
    s = iv.sin(p)
    c = iv.cos(p)
    c2 = iv.cos(2 * p)
    return p, cm, cp, s, c, c2


def ell_fall(a, philo, phihi, kaplo, kaphi, rholo, rhohi, i):
    """Rigorous upper bound on ell^fall_i = L* - K*h*(1+i) + K*rho*d1 over the box.

    Monotone in kappa (decreasing: h enters with -K(1+i) and +0 elsewhere) and in
    rho (increasing).  So set kappa = kaplo, rho = rhohi and bound over phi.
    """
    if philo == 0:
        # exact slice: L* = a, K = 2/sqrt3, d1 = 0, h = kappa*sqrt3/2
        # => ell = a - kappa*(1+i).   (rho term vanishes because d1 = 0)
        exact = Fraction(a) - kaplo * (1 + i)
        if phihi == 0:
            return float(exact)
    _, cm, cp, s, c, c2 = _trig(philo, phihi)
    kap = iv.mpf([_m(kaplo), _m(kaplo)])
    h = kap * SQ3 / 2
    Lstar = (iv.mpf(a) * SQ3 / 2) / cm
    K = SQ3 / (c2 + iv.mpf(1) / 2)
    d1 = iv.mpf(a) * s
    rho = iv.mpf([_m(rhohi), _m(rhohi)])
    val = Lstar - K * h * (1 + i) + K * rho * d1
    return float(val.b)


def ell_fall_sup(a, box, i, depth=14):
    """Monotonicity-aware sup of ell^fall_i over the box's phi-range."""
    philo, phihi = box.phi
    kaplo = box.kap[0]
    rhohi = box.rho[1]
    # cheap symbolic caps: ell <= L* <= a, and ell <= (L*-K h) - i*K*h + rho*K*d1
    #                      with L* - K h <= a - 1 (Lemma B) and K*h >= 1.
    cap = min(float(a), float(a) - 1 - i + float(rhohi) * _kd1_sup(a, philo, phihi))
    best = _sup_phi_rec(a, philo, phihi, kaplo, rhohi, i, depth)
    return min(best, cap)


def _kd1_sup(a, philo, phihi):
    _, cm, cp, s, c, c2 = _trig(philo, phihi)
    K = SQ3 / (c2 + iv.mpf(1) / 2)
    return float((K * iv.mpf(a) * s).b)


def _sup_phi_rec(a, philo, phihi, kaplo, rhohi, i, depth):
    if philo == 0 and phihi == 0:
        return float(Fraction(a) - kaplo * (1 + i))
    v = ell_fall(a, philo, phihi, kaplo, kaplo, rhohi, rhohi, i)
    if depth <= 0 or phihi - philo < mpf("1e-12"):
        return v
    # monotonicity test in phi
    d = _dfall_dphi(a, philo, phihi, kaplo, rhohi, i)
    if d.b <= 0:
        return _sup_phi_rec(a, philo, philo, kaplo, rhohi, i, 0)
    if d.a >= 0:
        return _sup_phi_rec(a, phihi, phihi, kaplo, rhohi, i, 0)
    mid = (philo + phihi) / 2
    return max(_sup_phi_rec(a, philo, mid, kaplo, rhohi, i, depth - 1),
               _sup_phi_rec(a, mid, phihi, kaplo, rhohi, i, depth - 1))


def _dfall_dphi(a, philo, phihi, kaplo, rhohi, i):
    p, cm, cp, s, c, c2 = _trig(philo, phihi)
    h = iv.mpf([_m(kaplo), _m(kaplo)]) * SQ3 / 2
    rho = iv.mpf([_m(rhohi), _m(rhohi)])
    A = iv.mpf(a)
    dL = (A * SQ3 / 2) * iv.sin(p - PI6) / (cm ** 2)
    den = c2 + iv.mpf(1) / 2
    dK = SQ3 * 2 * iv.sin(2 * p) / (den ** 2)
    d1 = A * s
    dd1 = A * c
    K = SQ3 / den
    return dL - dK * h * (1 + i) + rho * (dK * d1 + K * dd1)


def ell_rise_sup(a, box, i):
    """Rigorous upper bound on ell^rise_i = L*(1 - rho - i*h/d1) over the box.

    Decreasing in rho and in kappa; for i = 0 also decreasing in phi (L* is).
    Returns None if no such line can exist in the box.
    """
    philo, phihi = box.phi
    kaplo = box.kap[0]
    rholo = box.rho[0]
    _, cm, cp, s, c, c2 = _trig(philo, phihi)
    A = iv.mpf(a)
    Lstar = (A * SQ3 / 2) / cm
    h = iv.mpf([_m(kaplo), _m(kaplo)]) * SQ3 / 2
    d1 = A * s
    if i == 0:
        if philo == 0:
            val = Fraction(a) * (1 - rholo)
            return float(val)
        return float((Lstar * (1 - iv.mpf([_m(rholo), _m(rholo)]))).b)
    # i >= 1 needs i*h <= d1 - rho*d1 <= d1
    if float(d1.b) < i * float(h.a):
        return None
    ratio = h / d1                      # d1 bounded away from 0 here
    val = Lstar * (1 - iv.mpf([_m(rholo), _m(rholo)]) - i * ratio)
    return float(val.b)


def box_bound(a, box, imax=40):
    total = 0
    for i in range(imax):
        u = ell_fall_sup(a, box, i)
        if u < 0:
            break
        total += min(int(a), _c(u))
    for i in range(imax):
        u = ell_rise_sup(a, box, i)
        if u is None or u < 0:
            break
        total += min(int(a), _c(u))
    return total


def bnb(a, target, max_boxes=400000, out=None, minwidth=1e-7):
    """Branch and bound over R2.  Returns (best_certified_bound, stalled_boxes, stats)."""
    kmax = 2 * (a + 1) / (3 ** 0.5) + 1     # h > w_max => at most one line; w <= a
    root = Box((mpf(0), PI6.b), (Fraction(1), Fraction(kmax).limit_denominator(64) + 1),
               (Fraction(0), Fraction(1)))
    stack = [root]
    worst = 0
    stalled = []
    nboxes = 0
    while stack:
        if nboxes >= max_boxes:
            stalled.extend(stack)
            break
        b = stack.pop()
        nboxes += 1
        v = box_bound(a, b)
        if v <= target:
            worst = max(worst, v)
            continue
        w = b.widths()
        if max(float(w[0]), float(w[1]), float(w[2])) < minwidth:
            stalled.append(b)
            worst = max(worst, v)
            continue
        stack.extend(b.split())
    stats = {"a": a, "target": target, "boxes_processed": nboxes,
             "stalled": len(stalled), "worst_certified": worst,
             "R1_lemmaA": a * (a + 1) // 2 + 1}
    if out:
        with open(out, "w") as f:
            json.dump({"stats": stats,
                       "stalled_boxes": [x.as_json() for x in stalled[:200]]}, f, indent=1)
    return worst, stalled, stats


if __name__ == "__main__":
    a = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    target = int(sys.argv[2]) if len(sys.argv) > 2 else 26
    out = sys.argv[3] if len(sys.argv) > 3 else None
    worst, stalled, stats = bnb(a, target, out=out)
    print(json.dumps(stats, indent=1))
