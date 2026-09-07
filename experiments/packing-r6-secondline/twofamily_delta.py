"""(F3 + the assignment's target) delta-robustness of the TWO-family count.

Hypothesis (H2-delta).  Every p in P is within delta of a line of family 1 (unit normal n1,
spacing h1) AND within delta of a line of family 2 (unit normal n2, spacing h2).  Let L be
the lattice of intersection points of the two families.

Step 1 (injectivity).  p - pi(p) lies in the parallelogram P_delta = {x : |x.n1| <= delta,
|x.n2| <= delta}, whose diameter is 4 delta / |sin(angle(n1,n2))|.  If that is < 1 then two
distinct points of P cannot share an intersection, so p -> pi(p) is injective.

Step 2 (containment).  pi(p) in T(a) (+) P_delta.  Pushing edge e of T(a) outward by w_e
turns it into a triangle of side a + (2/sqrt3) * (w_1 + w_2 + w_3).  Here
w_e = h_{P_delta}(m_e) = delta * (|c1| + |c2|) where m_e = c1 n1 + c2 n2 is the outward unit
edge normal resolved in the two family normals.  So

    |P|  <=  M( a + Gamma * delta ),      Gamma = (2/sqrt3) * sum_e (|c1^e| + |c2^e|).

Since |c1| + |c2| >= |c1 n1 + c2 n2| = 1 for every edge, Gamma >= 2 sqrt3 = 3.4641, with
equality impossible (only two of the three edge normals can be parallel to n1 or n2).
So the two-family delta-window is  eta / Gamma  <  eta / (2 sqrt3) = 0.2887 * eta,
against the one-family window of (sqrt3/2) * eta = 0.8660 * eta.

STATUS: sketch (the derivation) + numerical (the constants).
"""
import json, math
import os as _os
import sys as _sys

_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import _deps

_deps.require('twofamily_delta.py')   # fail fast, before the numpy import below

import numpy as np

SQRT3 = math.sqrt(3.0)
# outward unit normals of T(a): edge AB, edge AC, edge BC
M_EDGES = np.array([[0.0, -1.0], [-SQRT3 / 2, 0.5], [SQRT3 / 2, 0.5]])


def gamma(phi, psi):
    """Gamma for family-1 line direction angle phi and family-2 line direction angle psi."""
    n1 = np.array([-math.sin(phi), math.cos(phi)])
    n2 = np.array([-math.sin(psi), math.cos(psi)])
    A = np.array([n1, n2]).T                       # columns n1, n2
    if abs(np.linalg.det(A)) < 1e-12:
        return float("inf"), 0.0
    C = np.linalg.solve(A, M_EDGES.T)              # (2, 3): rows c1, c2
    return (2.0 / SQRT3) * float(np.abs(C).sum()), abs(float(np.linalg.det(A)))


if __name__ == "__main__":
    out = {}
    # (i) the extremal lattice found by the two-family sweep: phi = 29.333 deg, hexagonal
    for name, phid in (("extremal_M22_phi29.33", 29.333333333333332),
                       ("aligned_phi0", 0.0), ("phi15", 15.0), ("phi30", 30.0)):
        phi = math.radians(phid)
        g, s = gamma(phi, phi + math.pi / 3.0)     # hexagonal: families 60 deg apart
        out[name] = {"phi_deg": phid, "Gamma": g, "abs_sin_angle": s,
                     "two_family_window_over_eta": 1.0 / g,
                     "injectivity_needs_delta_lt": s / 4.0}
    # (ii) the best (smallest) Gamma over all hexagonal orientations
    best = min(((gamma(math.radians(d), math.radians(d) + math.pi / 3)[0], d)
                for d in np.linspace(0, 60, 6001)))
    out["min_Gamma_over_hexagonal_orientations"] = {"Gamma": best[0], "phi_deg": best[1],
                                                    "window_over_eta": 1.0 / best[0]}
    # (iii) the best Gamma over ALL pairs of directions (not only 60 deg apart)
    bb = None
    for d1 in np.linspace(0, 60, 241):
        for d2 in np.linspace(0, 180, 721):
            g, s = gamma(math.radians(d1), math.radians(d2))
            if s < 0.4:          # angle too shallow: injectivity fails for useful delta
                continue
            if bb is None or g < bb[0]:
                bb = (g, d1, d2, s)
    out["min_Gamma_over_all_direction_pairs"] = {"Gamma": bb[0], "phi1_deg": bb[1],
                                                 "phi2_deg": bb[2], "abs_sin": bb[3],
                                                 "window_over_eta": 1.0 / bb[0]}
    out["one_family_window_over_eta"] = SQRT3 / 2
    out["isotropic_floor_Gamma"] = 2 * SQRT3
    print(json.dumps(out, indent=1))
    json.dump(out, open("out/twofamily_delta.json", "w"), indent=1)
