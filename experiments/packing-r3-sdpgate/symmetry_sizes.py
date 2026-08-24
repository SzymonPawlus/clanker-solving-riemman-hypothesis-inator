#!/usr/bin/env python3
"""Independent re-derivation of the S_n-isotypic size claim for the moment
relaxation of the equilateral-triangle point-packing problem (round-3 proposal X).

STATUS OF WHAT THIS PRODUCES: `numerical` (exact integer arithmetic, but it is a
computation, not a proof).  It makes no claim about d(n) or s(n) whatsoever --
it counts dimensions of linear-algebra objects.

Setting.  Fixed-t feasibility formulation: variables x_0..x_{n-1}, y_0..y_{n-1}
(N = 2n).  S_n acts by permuting the point index i simultaneously in x and y.
The order-L moment matrix is indexed by the monomials of degree <= L in those
N variables, which is a permutation module for S_n.  Under the S_n-invariant
(symmetry-adapted) reformulation, that single big PSD constraint splits into one
PSD block of size m_lambda for every irreducible S^lambda occurring, where
m_lambda is the multiplicity of S^lambda in the permutation module.  So the
"block sizes" of the reduced SDP are exactly those multiplicities.

Method (fully independent of any prior script in this repo):
  * character of the permutation module, evaluated on a cycle type mu:
    a monomial (exponent pairs (a_i, b_i)) is fixed by a permutation iff the
    pair (a_i, b_i) is constant along every cycle.  So the number of fixed
    monomials of degree <= r is the sum of the coefficients of q^0..q^r in
    prod_{cycles c} 1/(1 - q^{len(c)})^2.
  * irreducible characters by Murnaghan-Nakayama via beta-sets.
  * m_lambda = (1/n!) sum_mu |C_mu| chi_perm(mu) chi_lambda(mu)  -- exact
    Fraction arithmetic, asserted integral.
  * internal check: sum_lambda m_lambda * dim(lambda) == C(N + r, r).

Run:  python3 symmetry_sizes.py
"""

from __future__ import annotations

from fractions import Fraction
from functools import lru_cache
from math import comb, factorial


# ----------------------------------------------------------------- partitions
def partitions(n, maxpart=None):
    if maxpart is None:
        maxpart = n
    if n == 0:
        yield ()
        return
    for k in range(min(n, maxpart), 0, -1):
        for rest in partitions(n - k, k):
            yield (k,) + rest


def class_size(mu, n):
    """Size of the S_n conjugacy class of cycle type mu."""
    z = 1
    counts = {}
    for p in mu:
        counts[p] = counts.get(p, 0) + 1
    for p, m in counts.items():
        z *= (p ** m) * factorial(m)
    return factorial(n) // z


def hook_dim(lam):
    """dim S^lambda by the hook length formula."""
    n = sum(lam)
    conj = [sum(1 for r in lam if r > c) for c in range(lam[0])]
    prod = 1
    for i, row in enumerate(lam):
        for j in range(row):
            prod *= (row - j) + (conj[j] - i) - 1
    return factorial(n) // prod


# ------------------------------------------------- Murnaghan-Nakayama (beta set)
def beta_set(lam):
    k = len(lam)
    return tuple(sorted((lam[i] + (k - 1 - i) for i in range(k)), reverse=True))


def beta_to_partition(bs):
    bs = sorted(bs, reverse=True)
    k = len(bs)
    lam = [bs[i] - (k - 1 - i) for i in range(k)]
    return tuple(p for p in lam if p > 0)


@lru_cache(maxsize=None)
def mn_char(bs, mu):
    """chi_lambda(mu), lambda given by its beta-set `bs` (tuple, descending)."""
    if not mu:
        return 1
    h = mu[0]
    rest = mu[1:]
    s = set(bs)
    total = 0
    for b in bs:
        nb = b - h
        if nb < 0 or nb in s:
            continue
        # height = number of beta-elements strictly between nb and b
        ht = sum(1 for c in bs if nb < c < b)
        new = tuple(sorted((s - {b}) | {nb}, reverse=True))
        total += (-1) ** ht * mn_char(new, rest)
    return total


# ----------------------------------------------- permutation-module characters
def fixed_monomials(mu, max_degree):
    """# monomials of degree <= max_degree in x_1..x_n, y_1..y_n fixed by a
    permutation of cycle type mu."""
    r = max_degree
    poly = [0] * (r + 1)
    poly[0] = 1
    for l in mu:
        # multiply by 1/(1-q^l)^2 = sum_{m>=0} (m+1) q^{l m}
        factor = [0] * (r + 1)
        m = 0
        while l * m <= r:
            factor[l * m] = m + 1
            m += 1
        new = [0] * (r + 1)
        for i, a in enumerate(poly):
            if a == 0:
                continue
            for j in range(0, r + 1 - i):
                if factor[j]:
                    new[i + j] += a * factor[j]
        poly = new
    return sum(poly)


def multiplicities(n, max_degree):
    """Return {lambda: m_lambda} for the degree-<=max_degree monomial module."""
    nf = factorial(n)
    parts = list(partitions(n))
    data = [(mu, class_size(mu, n), fixed_monomials(mu, max_degree)) for mu in parts]
    out = {}
    for lam in parts:
        bs = beta_set(lam)
        acc = Fraction(0)
        for mu, cs, fp in data:
            if fp == 0:
                continue
            acc += Fraction(cs * fp * mn_char(bs, mu), nf)
        assert acc.denominator == 1, (lam, acc)
        m = int(acc)
        assert m >= 0
        if m:
            out[lam] = m
    return out


def orbit_count(n, max_degree):
    """Burnside: # S_n-orbits on monomials of degree <= max_degree (= # invariant
    scalar moment variables of that degree)."""
    nf = factorial(n)
    tot = 0
    for mu in partitions(n):
        tot += class_size(mu, n) * fixed_monomials(mu, max_degree)
    assert tot % nf == 0
    return tot // nf


# ------------------------------------------------------------------- reporting
def report(n, levels=(2, 3)):
    N = 2 * n
    print(f"=== n = {n} points, N = 2n = {N} variables (fixed-t formulation) ===")
    for L in levels:
        dense = comb(N + L, L)
        mult = multiplicities(n, L)
        check = sum(m * hook_dim(lam) for lam, m in mult.items())
        blocks = sorted(mult.values(), reverse=True)
        print(f"\n  level L = {L}: dense order-{L} moment matrix {dense} x {dense}")
        print(f"    isotypic blocks (multiplicities m_lambda), largest first: {blocks}")
        for lam, m in sorted(mult.items(), key=lambda kv: -kv[1]):
            print(f"      lambda = {lam!s:<24} dim = {hook_dim(lam):>7}   m = {m}")
        print(f"    check  sum_lambda m_lambda * dim(lambda) = {check}"
              f"   (dense = {dense})  -> {'OK' if check == dense else 'MISMATCH'}")
        assert check == dense
        deg = 2 * L
        inv = orbit_count(n, deg)
        print(f"    invariant scalar moments, degree <= {deg}: {inv}"
              f"   (dense C({N}+{deg},{deg}) = {comb(N + deg, deg):,})")
    # constraint orbits
    print(f"\n  constraint orbits at n = {n}:")
    print(f"    pairwise separation ||p_i-p_j||^2 >= t : C({n},2) = {comb(n,2)}"
          f" constraints, 1 S_n-orbit")
    print(f"    containment (3 half-planes per point)  : 3n = {3*n}"
          f" constraints, 3 S_n-orbits (one per triangle edge),")
    print(f"                                             1 orbit under S_n x D_3")
    print(f"    TOTAL: 4 orbits under S_n alone; 2 orbits under S_n x D_3")


if __name__ == "__main__":
    for n in (5, 7, 8, 12, 16):
        report(n, levels=(2, 3) if n <= 16 else (2,))
        print()
