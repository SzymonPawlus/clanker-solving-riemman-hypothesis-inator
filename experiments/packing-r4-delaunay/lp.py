"""The LP gate for the Euler-localised Delaunay-scoring family (proposal AB).

READ THE FRAMEWORK SECTION OF ../../problems/circle-packing-equilateral-triangle/
attacks/r4-delaunay/README.md FIRST.  In brief:

A *localised score* is a pair (sigma, tau) plus constants (c_A, c_L) >= 0 with

  (D) domination / telescoping-compatibility, pointwise over the shape space:
          sigma(f) <= c_A * area(f) - 1/2      for every triangle with sides >= 1
          tau(l)   <= c_L * l        - 1/2      for every l >= 1
  (V) validity, globally:
          sum_faces sigma(f) + sum_{boundary edges} tau(l_e)  >=  0
      for every finite non-collinear unit-separated E and every triangulation
      of conv(E) with vertex set E.

Given (D) and (V), Euler (F = 2n - b - 2, i.e. n - 1 = (F+b)/2) telescopes to

          n  <=  1 + c_A*A(conv E) + c_L*M(conv E)
             <=  1 + c_A*(sqrt3/4)a^2 + 3*c_L*a       inside T_a.

Oler is the member sigma(f) = (2/sqrt3)area(f) - 1/2, tau(l) = (l-1)/2,
(c_A, c_L) = (2/sqrt3, 1/2), giving n <= 1 + a^2/2 + 3a/2.

WHAT THE LPs DO.  Both LPs below impose only NECESSARY conditions on a member,
so their optimum is an OPTIMISTIC estimate of what the family can prove: the
true best bound from the family is at least as weak as the LP's answer.  Hence
"the LP does not beat Oler" is a meaningful negative, while "the LP beats Oler"
would only be a lead.

  reduced_lp : variables (c_A, c_L).  Constraint per library configuration K:
               c_A*A(K) + c_L*M(K) + 1 >= n(K).   [necessary: apply (D)+(V) to K]
  score_lp   : variables sigma_s for every distinct face shape in the library,
               tau_t for every distinct boundary edge length, plus (c_A, c_L).
               Constraints (D) per shape/length and (V) per configuration.
               This is the family as literally stated -- one free score value
               per shape -- and it is the honest test of whether NONLINEARITY
               buys anything.

Objective in both: minimise  B(a) = 1 + c_A*(sqrt3/4)*a^2 + 3*c_L*a.

Status of every number produced here: `numerical`.  An LP optimum from a float
solver is not a bound.
"""

import math

import numpy as np
from scipy.optimize import linprog

SQRT3 = math.sqrt(3.0)
BIG = 1e6


# ---------------------------------------------------------------- reduced LP

def reduced_lp(cfgs, a):
    """min 1 + c_A*(sqrt3/4)a^2 + 3 c_L a  s.t.  c_A A_K + c_L M_K >= n_K - 1."""
    c = np.array([(SQRT3 / 4.0) * a * a, 3.0 * a])
    A_ub, b_ub = [], []
    for k in cfgs:
        A_ub.append([-float(k.area_up), -float(k.perim_up)])
        b_ub.append(-(k.n - 1))
    res = linprog(c, A_ub=np.array(A_ub), b_ub=np.array(b_ub),
                  bounds=[(0, BIG), (0, BIG)], method="highs")
    assert res.status == 0, res.message
    return 1.0 + res.fun, res.x


# ------------------------------------------------------------------ full LP

def _shape_tables(cfgs):
    """Distinct face shapes (keyed by exact sorted squared side lengths) with
    their exact area, and distinct boundary-edge squared lengths with an upper
    bound on the length."""
    shapes, edges = {}, {}
    for k in cfgs:
        for key, area in k.face_shapes:
            # a shape key determines the triangle up to congruence, so the area
            # is a function of the key; assert that rather than assume it.
            if key in shapes:
                assert shapes[key] == area, "shape key collision"
            else:
                shapes[key] = area
        for i in range(k.b):
            key = k.bedge_len2[i]
            L = k.bedge_len_up[i]
            edges[key] = max(edges.get(key, L), L)
    return shapes, edges


def score_lp(cfgs, a, return_solution=False):
    """The family as literally stated: one free score value per face shape."""
    from framework import kfloat
    shapes, edges = _shape_tables(cfgs)
    slist, elist = list(shapes), list(edges)
    si = {s: i for i, s in enumerate(slist)}
    ei = {e: len(slist) + i for i, e in enumerate(elist)}
    IA, IL = len(slist) + len(elist), len(slist) + len(elist) + 1
    nv = IL + 1

    c = np.zeros(nv)
    c[IA] = (SQRT3 / 4.0) * a * a
    c[IL] = 3.0 * a

    A_ub, b_ub = [], []
    # (D) sigma_s - c_A * area(s) <= -1/2
    for s in slist:
        row = np.zeros(nv)
        row[si[s]] = 1.0
        row[IA] = -float(kfloat(shapes[s]))
        A_ub.append(row)
        b_ub.append(-0.5)
    # (D) tau_t - c_L * l_t <= -1/2
    for e in elist:
        row = np.zeros(nv)
        row[ei[e]] = 1.0
        row[IL] = -float(edges[e])
        A_ub.append(row)
        b_ub.append(-0.5)
    # (V) -sum sigma - sum tau <= 0
    for k in cfgs:
        row = np.zeros(nv)
        for key, _ in k.face_shapes:
            row[si[key]] -= 1.0
        for i in range(k.b):
            row[ei[k.bedge_len2[i]]] -= 1.0
        A_ub.append(row)
        b_ub.append(0.0)

    bounds = [(-BIG, BIG)] * (len(slist) + len(elist)) + [(0, BIG), (0, BIG)]
    res = linprog(c, A_ub=np.array(A_ub), b_ub=np.array(b_ub),
                  bounds=bounds, method="highs")
    assert res.status == 0, res.message
    val = 1.0 + res.fun
    if not return_solution:
        return val, (res.x[IA], res.x[IL])
    # report how far the optimal sigma is from the linear (Oler-type) member
    cA = res.x[IA]
    dev = max(abs(res.x[si[s]] - (cA * float(kfloat(shapes[s])) - 0.5))
              for s in slist)
    return val, (res.x[IA], res.x[IL]), dev, (len(slist), len(elist))


# ------------------------------------------------------------------- driver

def threshold_a(bound_fn, n_target, lo=0.0, hi=60.0, iters=200):
    """Largest a at which the family can still certify 'fewer than n_target
    points fit', i.e. sup{a : B(a) < n_target}.  B is increasing in a."""
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        if bound_fn(mid) < n_target:
            lo = mid
        else:
            hi = mid
    return lo


def oler_d(n):
    """Oler's own answer in this repo's normalisation: d >= sqrt(8n+1) - 3."""
    return math.sqrt(8.0 * n + 1.0) - 3.0
