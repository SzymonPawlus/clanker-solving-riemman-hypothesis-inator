"""The constant-width test body, exactly: is the disk really not extremal for m/w?

`problems/inscribed-equilateral-triangle/attacks/extremal-size/` §7 reports that the convex
body with support function

        h(theta) = 1 + cos(5 theta)/24                     (call it K)

has width exactly 2 and m(K) ~ 1.714410, i.e. m/w ~ 0.857205, beating the disk's
sqrt3/2 ~ 0.866025 -- and says plainly that the m there is a FLOAT.  This module replaces
that float by an exact inequality.

What has to be proved, and what does not
========================================
w(K) = 2 is exact and needs no computation: h(theta) + h(theta+180) = 2 identically because
cos 5(theta+180) = -cos 5theta.  Convexity is h + h'' = 1 - cos 5theta >= 0.  So the ONLY
quantity in the ratio that needs a computation is m(K), and only from ABOVE: the claim is
m(K)/2 < sqrt3/2, i.e.

        m(K) < sqrt 3,      equivalently      m(K)^2 < 3.

Since every triangle inscribed in the boundary of K is in particular CONTAINED in K,

        m(K)  <=  M(K) := sup{ side of an equilateral triangle contained in K },

so an upper bound on M(K) suffices and no lemma about where a maximal triangle touches the
boundary is needed anywhere.  (That inequality may be strict; nothing below depends on it
being tight.  For orientation only, the float optimum of the containment problem here is
1.71462 against the sibling lane's inscribed float 1.71441.)

The chain, each link exact
==========================
1. **Outer polygon.**  h_K is the support function, so for ANY finite set of nonzero
   rational normals n_j and any rational c_j >= h_K(n_j),
        K subset Q0 = { x : <x,n_j> <= c_j for all j }.
   h_K(n) = |n| + eps*(x^5-10x^3y^2+5xy^4)/(x^2+y^2)^2 with eps = 1/24: the second term is
   exactly rational and only |n| needs a rational upper bound (`lp.sqrt_upper`).

2. **A priori side bound s_ub.**  If T is an equilateral triangle contained in Q0 then its
   minimal width sqrt3*s/2 is at most the width of any slab containing Q0.  The normal set
   is antipodally closed by construction, so for each j the two half planes with normals
   +-n_j give the slab width (c_j + c_{j'})/|n_j|, and s <= 2(c_j+c_{j'})/(sqrt3 |n_j|) is
   computed with a rational lower bound for sqrt3 and for |n_j|.  This step uses Q0, NOT the
   inflated body, so there is no circularity.

3. **Direction sampling.**  Rational directions u_1..u_D in angular order with every
   consecutive gap at most gamma, certified by gap <= tan gap = cross/dot (dot > 0).

4. **Rotation to a sampled direction.**  Every equilateral triangle is t + lambda T(u) for
   T(u) = {0, u, rho u}; let T subset Q0 have side s and direction v, and pick u_k within
   gamma/2 of v.  Rotating T about its centroid by that angle moves each vertex by at most
   2R sin(gamma/4) <= R gamma/2 with R = s/sqrt3 the circumradius, so the rotated triangle,
   which has direction EXACTLY u_k and the same side s, lies in the outer parallel body
        Q_r = { x : <x,n_j> <= c_j + r|n_j| },     r = s_ub * gamma / (2 sqrt3).

5. **An exact LP bound at each sampled direction.**  A half plane contains a triangle iff it
   contains its three vertices, so t + lambda T(u) subset Q_r iff
        <t,n_j> + lambda m_j(u) <= c_j + r|n_j|,   m_j(u) = max(0, <u,n_j>, <rho u,n_j>),
   and weak duality on that 3-variable LP gives, for any nonnegative y supported on a triple
   with sum y_r n_r = 0 and sum y_r m_r = 1, the bound lambda <= sum y_r c_r.  Every entry is
   in Q(sqrt3) and every comparison is exact; floats only propose which triple to try.

   Hence   m(K)^2 <= M(Q0)^2 <= max_k |u_k|^2 * (dual bound at u_k)^2.

Blind spot, stated as one: this bounds m(K) from ABOVE only.  It does not produce an
inscribed triangle of any particular size, so it cannot bound m(K) from below, and it says
nothing about whether 0.857205 is anywhere near the true infimum of m/w over convex bodies.
"""

from __future__ import annotations

import math
import time
from fractions import Fraction as F

from .qs3 import Q3
from . import lp

__all__ = ["run"]

SQRT3_LO = F(17320508075688772, 10 ** 16)      # < sqrt 3, checked exactly below
SQRT3_HI = F(17320508075688773, 10 ** 16)      # > sqrt 3


def _check_sqrt3_brackets():
    assert SQRT3_LO ** 2 < 3 < SQRT3_HI ** 2, "sqrt3 brackets are wrong"


def a_priori_side_bound(hps, J=None):
    """Exact rational upper bound on the side of any equilateral triangle inside Q0.

    Uses any ANTIPODAL pair of normals in the list: those two half planes bound a slab of
    width (c_j + c_j')/|n_j| containing Q0, and an equilateral triangle of side s inside a
    slab of width W has sqrt3 s/2 <= W.  Works for any half-plane family that contains at
    least one antipodal pair; the sampled families built here always do.
    """
    index = {(n[0], n[1]): j for j, (n, c, clo, nrm) in enumerate(hps)}
    best = None
    for j, (n, c, clo, nrm) in enumerate(hps):
        k = index.get((-n[0], -n[1]))
        if k is None:
            continue
        c2 = hps[k][1]
        q = F(n[0]) ** 2 + F(n[1]) ** 2
        nlo = lp.sqrt_lower(q)                     # <= |n|
        w_ub = (F(c) + F(c2)) / nlo                # >= the slab width
        s = 2 * w_ub / SQRT3_LO                    # >= 2W/sqrt3
        if best is None or s < best:
            best = s
    assert best is not None, "no antipodal pair of normals: cannot bound the side a priori"
    return best


def run(J=192, D=2400, eps=F(1, 24), s_ub=F(12, 5), progress=None, hps=None):
    """`hps=None` uses the constant-width body; pass a half-plane family to bound the
    largest equilateral triangle contained in any other convex body (used by the tests,
    where the answer is known: the disk gives sqrt3 and the unit square sec 15 degrees)."""
    _check_sqrt3_brackets()
    t0 = time.time()
    if hps is None:
        hps = lp.outer_halfplanes(J, eps=eps)
    s_apriori = a_priori_side_bound(hps)
    assert s_apriori <= s_ub, ("the a priori bound %s exceeds the assumed s_ub %s"
                               % (float(s_apriori), float(s_ub)))
    dirs = lp.sample_directions(D)
    gamma = lp.max_gap_tan(dirs)                    # >= the true max angular gap
    r = s_ub * gamma / (2 * SQRT3_LO)               # >= s_ub*gamma/(2 sqrt3)
    hps_r = lp.inflate(hps, r)

    best2 = None
    best_i = None
    recs = []
    for i, u in enumerate(dirs):
        lam, lam_float = lp.lambda_upper_at(hps_r, u)
        if lam is None:
            raise AssertionError("no exact dual certificate at direction %d" % i)
        u2 = Q3.of(F(u[0]) ** 2 + F(u[1]) ** 2)
        s2 = lam * lam * u2
        # The exact Q(sqrt3) certificates carry several-hundred-digit integers; keeping all
        # D of them makes a multi-megabyte artifact for no gain, so only the running record
        # holder's exact value is kept (it is the only one the bound is read off) and the
        # rest are recorded as floats for the profile.
        recs.append({"i": i, "side_ub_display": float(s2) ** 0.5,
                     "lambda_float": lam_float})
        if best2 is None or (s2 - best2).sgn() > 0:
            best2, best_i = s2, i
            recs[-1]["lambda_ub_exact"] = lam.pair()
            recs[-1]["side2_ub_exact"] = s2.pair()
        if progress and i % progress == 0:
            print("      dir %5d/%d  running side_ub <= %.9f  (%.0fs)"
                  % (i, D, float(best2) ** 0.5, time.time() - t0), flush=True)

    # A clean rational UPPER bound for the reported side^2 = a + b sqrt3, so that the final
    # inequality can be read without expanding a 400-digit fraction: bound sqrt3 above when
    # b > 0 and below when b < 0, then round outward to 1/10^9.
    a_part = F(best2.a, best2.c)
    b_part = F(best2.b, best2.c)
    s2_rat = a_part + b_part * (SQRT3_HI if b_part > 0 else SQRT3_LO)
    s2_rat = lp._round_up(s2_rat, 10 ** 9)

    three = Q3.of(3)
    proves = (best2 - three).sgn() < 0
    out = {
        "J": J, "D": D, "eps": str(eps), "s_ub": str(s_ub),
        "s_apriori_bound": str(s_apriori), "gamma_upper": str(gamma),
        "gamma_upper_display": float(gamma), "r_inflation": str(r),
        "r_display": float(r),
        "side2_upper_bound": best2.pair(),
        "side2_upper_rational": str(s2_rat),
        "side2_upper_rational_display": float(s2_rat),
        "side2_rational_lt_3": bool(s2_rat < 3),
        "side2_upper_display": float(best2),
        "side_upper_display": float(best2) ** 0.5,
        "argmax_direction": best_i,
        "three_minus_side2": (three - best2).pair(),
        "three_minus_side2_display": float(three - best2),
        "m_over_w_upper_display": float(best2) ** 0.5 / 2,
        "disk_ratio_display": math.sqrt(3) / 2,
        "proves_disk_not_extremal": bool(proves),
        "seconds": time.time() - t0,
        "per_direction": recs,
    }
    return out
