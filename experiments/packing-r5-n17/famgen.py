"""Independent re-implementation of the r4-famcert four-grain generator,
written from the SPEC IN ITS DOCSTRING ONLY (grain row/abscissa ranges and the
four offsets), not by importing or copying experiments/packing-r4-famcert/generator.py.

Lattice L = {(2i + r, r*sqrt3)}.  Offsets
  g_BL = (0,0)   g_C = (sqrt3, 1)   g_T = (sqrt3, 3)   g_BR = (2 sqrt3, 0)
U = ceil(j/2), M = floor(j/2), par = j mod 2, d = 2j + 2 sqrt3, s = 2j + 4 sqrt3.
"""
from q3 import Q3

OFF = {"BL": (Q3(0, 0), Q3(0, 0)),
       "BR": (Q3(0, 2), Q3(0, 0)),
       "C":  (Q3(0, 1), Q3(1, 0)),
       "T":  (Q3(0, 1), Q3(3, 0))}


def site(name, r, x):
    gx, gy = OFF[name]
    return (Q3(x, 0) + gx, Q3(0, r) + gy)


def labelled(j):
    U = (j + 1) // 2
    M = j // 2
    par = j % 2
    out = []
    for r in range(0, U + 1):
        for x in range(r, 2 * U - r + 1, 2):
            out.append(("BL", r, x, site("BL", r, x)))
    for r in range(0, U + 1):
        for x in range(2 * j - 2 * U + r, 2 * j - r + 1, 2):
            if par == 1 and r == 0 and x == 2 * j - 2 * U:
                continue
            out.append(("BR", r, x, site("BR", r, x)))
    for r in range(par, par + M + 1):
        k = r - par
        for x in range(j - k, j + k + 1, 2):
            out.append(("C", r, x, site("C", r, x)))
    for r in range(U, j + 1):
        for x in range(r, 2 * j - r + 1, 2):
            out.append(("T", r, x, site("T", r, x)))
    return out


def generate(j):
    return [p for (_, _, _, p) in labelled(j)]


def d_of(j):
    return Q3(2 * j, 2)


def s_of(j):
    return Q3(2 * j, 4)


def law_n(j):
    tri = lambda k: k * (k + 1) // 2
    return tri(j + 2) + j // 2 + 1
