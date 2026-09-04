"""The four-grain staircase construction, re-transcribed from the SPEC.

CONSTRUCTION (upper bound) only.  Emitting points claims nothing; only the exact
checker's verdict does, and even then only  s(n) <= s.

Source of the spec: the docstring of experiments/packing-r4-famcert/generator.py
(read as a specification, not as code to import).  Nothing here imports famcert.

--------------------------------------------------------------------------
NORMAL FORM used throughout this directory
--------------------------------------------------------------------------
Every point of the configuration is written

        p = ( x + a*sqrt3 ,  b + r*sqrt3 )        with x, r, a, b integers,

where (a, b) is a per-grain constant "seam offset" and (r, x) are lattice
coordinates of the separation-2 triangular lattice L = {(x, r*sqrt3) : x = r mod 2}.
The four grains use

        BL: (a,b) = (0,0)     BR: (2,0)     C: (1,1)     T: (1,3)

and every point of every grain satisfies  x = r (mod 2).

Squared distance in this normal form is exact and j-free:

  p1 - p2 = (dx + da*sqrt3, db + dr*sqrt3)
  |p1-p2|^2 = (dx^2 + 3 da^2 + db^2 + 3 dr^2) + 2*sqrt3*(dx*da + db*dr).

--------------------------------------------------------------------------
GRAIN SHAPES (with U = ceil(j/2), M = floor(j/2), par = j mod 2, U+M = j,
U-M = par, 2U = j+par, 2M = j-par)
--------------------------------------------------------------------------
  BL   r in [0, U],           x in [r, 2U-r]            step 2   (upward)
  BR   r in [0, U],           x in [2M+r, 2j-r]         step 2   (upward)
       MINUS the single site (r,x) = (0, 2M) when j is odd
  C    r in [par, par+M],     x in [j-k, j+k], k = r-par step 2   (INVERTED)
  T    r in [U, j],           x in [r, 2j-r]            step 2   (upward)

n(j) = |BL|+|BR|+|C|+|T| = 2*Delta(U+1) + 2*Delta(M+1) - par
     = Delta(j+2) + floor(j/2) + 1.
"""
from q3 import E, SQ3

GRAINS = ("BL", "BR", "C", "T")
OFFSET = {"BL": (0, 0), "BR": (2, 0), "C": (1, 1), "T": (1, 3)}


def tri(k):
    return k * (k + 1) // 2


def UMp(j):
    return (j + 1) // 2, j // 2, j % 2


def lattice_sites(j):
    """{grain: [(r, x), ...]} -- integer lattice coordinates, deterministic order."""
    U, M, par = UMp(j)
    g = {k: [] for k in GRAINS}
    for r in range(0, U + 1):
        for x in range(r, 2 * U - r + 1, 2):
            g["BL"].append((r, x))
    for r in range(0, U + 1):
        for x in range(2 * M + r, 2 * j - r + 1, 2):
            if par == 1 and r == 0 and x == 2 * M:
                continue
            g["BR"].append((r, x))
    for r in range(par, par + M + 1):
        k = r - par
        for x in range(j - k, j + k + 1, 2):
            g["C"].append((r, x))
    for r in range(U, j + 1):
        for x in range(r, 2 * j - r + 1, 2):
            g["T"].append((r, x))
    return g


def embed(name, r, x, offset=None):
    a, b = OFFSET[name] if offset is None else offset[name]
    return (E(x, a), E(b, r))


def points(j, offset=None):
    g = lattice_sites(j)
    return [embed(nm, r, x, offset) for nm in GRAINS for (r, x) in g[nm]]


def labelled(j, offset=None):
    g = lattice_sites(j)
    return [(nm, r, x, embed(nm, r, x, offset)) for nm in GRAINS for (r, x) in g[nm]]


def n_of(j):
    return tri(j + 2) + j // 2 + 1


def d_of(j):
    return E(2 * j, 2)       # d = 2j + 2 sqrt3


def s_of(j):
    return E(2 * j, 4)       # s = d + 2 sqrt3 = 2j + 4 sqrt3


if __name__ == "__main__":
    for j in range(0, 13):
        g = lattice_sites(j)
        tot = sum(len(v) for v in g.values())
        U, M, par = UMp(j)
        assert tot == n_of(j), (j, tot, n_of(j))
        assert len(g["BL"]) == tri(U + 1) and len(g["BR"]) == tri(U + 1) - par
        assert len(g["C"]) == tri(M + 1) and len(g["T"]) == tri(M + 1)
        print("j=%2d  n=%3d  s=%-14s  |BL|=%d |BR|=%d |C|=%d |T|=%d"
              % (j, tot, s_of(j).s(), len(g["BL"]), len(g["BR"]), len(g["C"]), len(g["T"])))
    print("counts match n(j) = Delta(j+2) + floor(j/2) + 1 for j = 0..12")
