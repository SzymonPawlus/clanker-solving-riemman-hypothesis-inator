"""Exact Q(sqrt 3) configurations for n = 17, 24, 31.

CONSTRUCTION (upper bound) only. Nothing here claims optimality.

Coordinates are in the point formulation of
problems/circle-packing-equilateral-triangle/README.md: n points at pairwise
distance >= 2 in the closed equilateral triangle A=(0,0), B=(d,0),
C=(d/2, d*sqrt(3)/2), with s = d + 2*sqrt(3).

Each configuration was obtained by snapping the float output of
experiments/circle-packing-ls (LS billiard + SLSQP polish) to the nearest
element of Q(sqrt 3); the snap residual is recorded in the README.  Rattlers
(points with slack in every constraint) were placed by an exact lattice search
over the rattler's free region, so their exact positions differ from the
optimiser's float positions.  That is legitimate: a rattler has a
positive-measure free region and any point of it gives an equally valid packing.
"""
from fractions import Fraction as F
from qsqrt3 import Q3

def _p(ax, bx, ay, by):
    return (Q3(ax, bx), Q3(ay, by))

# --- n = 17,  d = 6 + 2 sqrt(3),  s = 6 + 4 sqrt(3) -------------------------
D17 = Q3(6, 2)
P17 = [
    _p(4, 2, 0, 0),    # 0   on AB
    _p(4, 0, 0, 0),    # 1   on AB
    _p(3, 0, 0, 1),    # 2
    _p(6, 2, 0, 0),    # 3   corner B
    _p(3, 1, 3, 3),    # 4   corner C
    _p(3, 1, 3, 1),    # 5
    _p(3, 1, 1, 1),    # 6
    _p(5, 1, 1, 1),    # 7
    _p(4, 1, 1, 0),    # 8
    _p(2, 1, 3, 2),    # 9   on AC
    _p(2, 0, 0, 0),    # 10  on AB
    _p(0, 0, 0, 0),    # 11  corner A
    _p(1, 0, 0, 1),    # 12  on AC
    (Q3(F(5, 2)), Q3(4)),   # 13  RATTLER, placed exactly (see module docstring)
    _p(5, 2, 0, 1),    # 14  on BC
    _p(5, 1, 3, 1),    # 15
    _p(4, 1, 3, 2),    # 16  on BC
]

# --- n = 24,  d = 8 + 2 sqrt(3),  s = 8 + 4 sqrt(3) -------------------------
D24 = Q3(8, 2)
P24 = [
    _p(5, 1, 3, 3),    # 0
    _p(4, 1, 1, 2),    # 1
    _p(6, 1, 1, 2),    # 2
    _p(0, 0, 0, 0),    # 3   corner A
    _p(4, 1, 3, 2),    # 4
    _p(4, 1, 3, 4),    # 5
    _p(3, 0, 0, 1),    # 6
    _p(5, 1, 1, 1),    # 7
    _p(1, 0, 0, 1),    # 8   on AC
    _p(5, 2, 0, 1),    # 9
    _p(4, 2, 0, 0),    # 10  on AB
    _p(6, 2, 0, 2),    # 11
    _p(2, 1, 3, 2),    # 12  on AC
    _p(3, 1, 3, 3),    # 13
    _p(2, 0, 0, 2),    # 14
    _p(4, 0, 0, 0),    # 15  on AB
    _p(3, 1, 1, 1),    # 16
    _p(4, 1, 1, 0),    # 17
    _p(8, 2, 0, 0),    # 18  corner B
    _p(2, 1, 1, 2),    # 19
    _p(6, 2, 0, 0),    # 20  on AB
    _p(6, 1, 3, 2),    # 21
    _p(2, 0, 0, 0),    # 22  on AB
    _p(7, 2, 0, 1),    # 23
]

# --- n = 31,  d = 10 + 2 sqrt(3), s = 10 + 4 sqrt(3) ------------------------
D31 = Q3(10, 2)
P31 = [
    _p(6, 1, 3, 4),    # 0
    _p(3, 0, 0, 3),    # 1
    _p(5, 2, 0, 1),    # 2
    _p(7, 1, 3, 3),    # 3
    _p(4, 0, 0, 2),    # 4
    _p(1, 0, 0, 1),    # 5   on AC
    _p(4, 1, 3, 4),    # 6
    _p(2, 0, 0, 2),    # 7
    _p(7, 2, 0, 1),    # 8
    _p(5, 1, 3, 3),    # 9
    _p(7, 2, 0, 3),    # 10
    _p(3, 0, 0, 1),    # 11
    _p(5, 0, 0, 1),    # 12
    (Q3(7), Q3(0)),    # 13  RATTLER, placed exactly (see module docstring)
    _p(6, 2, 0, 2),    # 14
    _p(7, 1, 1, 3),    # 15
    _p(5, 1, 1, 3),    # 16
    _p(5, 1, 1, 1),    # 17
    _p(10, 2, 0, 0),   # 18  corner B
    _p(3, 1, 3, 3),    # 19
    _p(8, 2, 0, 2),    # 20
    _p(9, 2, 0, 1),    # 21  on BC
    _p(6, 2, 0, 0),    # 22  on AB
    _p(4, 0, 0, 0),    # 23  on AB
    _p(8, 2, 0, 0),    # 24  on AB
    _p(0, 0, 0, 0),    # 25  corner A
    _p(6, 1, 1, 2),    # 26
    _p(3, 1, 1, 3),    # 27
    _p(4, 1, 1, 2),    # 28
    _p(5, 1, 3, 5),    # 29  corner C
    _p(2, 0, 0, 0),    # 30  on AB
]
