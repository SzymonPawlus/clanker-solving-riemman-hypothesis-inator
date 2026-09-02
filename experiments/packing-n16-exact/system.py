"""The n=16 contact system, in sheared coordinates where everything is rational.

CONSTRUCTION only. Nothing here is an optimality claim.

Coordinate convention (problem RULES.md 2 is unchanged; this is only a change of *chart*):
the certificate triangle is A=(0,0), B=(d,0), C=(d/2, d*sqrt(3)/2) in ordinary (x,y).
Write y = sqrt(3) * Y, x = X.  Then

    A=(0,0)  B=(d,0)  C=(d/2, d/2)          in (X,Y)
    squared distance = (dX)^2 + 3*(dY)^2
    edge AB: Y = 0        edge AC: Y = X        edge BC: Y = d - X
    containment: Y >= 0, Y <= X, Y <= d - X
    x + y/sqrt(3) = X + Y        (so d_min = max_i (X_i + Y_i))

Every coefficient is then rational in (d, t, u) and the whole contact system is a polynomial
system over Q.  Conversion back is x = X, y = sqrt(3)*Y.

Contact graph read off the float hypothesis (experiments/circle-packing-search/out/n16.json);
see analyze_float.py.  Point 4 is a RATTLER and is excluded from the rigid system.
"""

# Labels follow the ordering of unit_triangle_points in out/n16.json.
CONTACTS = [
    (0, 10), (0, 12), (10, 12),          # apex triangle
    (7, 8), (7, 13), (8, 13), (3, 8),    # corner-B lattice patch
    (2, 3), (2, 10), (1, 2), (1, 5), (1, 12),
    (2, 15), (3, 15), (9, 15), (9, 13), (9, 11),
    (5, 14), (6, 14), (11, 14),
]
# 20 contacts among the 15 rigid points.  (8,13) and (10,12) are *consequences* of the corner
# geometry (see attack README), so 18 of them are independent -> 31 independent equations for
# 31 unknowns (30 coordinates + d).

ON_AB = [11, 13]          # Y = 0
ON_AC = [5, 12]           # Y = X
ON_BC = [3, 8, 10]        # Y = d - X
CORNERS = {6: "A", 7: "B", 0: "C"}
INTERIOR = [1, 2, 9, 14, 15]
RATTLER = [4]


def free_symbols_layout():
    """Which unknowns survive after the corner points are solved in closed form."""
    return ["d", "t", "u", "X1", "Y1", "X2", "Y2", "X9", "Y9", "X14", "Y14", "X15", "Y15"]


def points(d, t, u, X1, Y1, X2, Y2, X9, Y9, X14, Y14, X15, Y15):
    """All 15 rigid points in (X,Y), given the 13 unknowns.

    Six of them are forced in closed form by the corner geometry:
      13 = (d-2, 0)          on AB at distance 2 from B
       8 = (d-1, 1)          on BC at distance 2 from B      (|8-13| = 2 then holds automatically)
       3 = (d-2, 2)          on BC at distance 4 from B, forced by |3-8| = 2
      12 = (d/2-1, d/2-1)    on AC at distance 2 from C
      10 = (d/2+1, d/2-1)    on BC at distance 2 from C      (|10-12| = 2 then holds automatically)
    """
    d2 = d / 2
    return {
        6: (0 * d, 0 * d),
        7: (d, 0 * d),
        0: (d2, d2),
        13: (d - 2, 0 * d),
        8: (d - 1, 0 * d + 1),
        3: (d - 2, 0 * d + 2),
        12: (d2 - 1, d2 - 1),
        10: (d2 + 1, d2 - 1),
        5: (t, t),
        11: (u, 0 * u),
        1: (X1, Y1), 2: (X2, Y2), 9: (X9, Y9), 14: (X14, Y14), 15: (X15, Y15),
    }


#: the 13 independent contact equations left after the six closed-form points above
REMAINING = [(6, 14), (11, 14), (5, 14),
             (1, 5), (1, 12), (1, 2), (2, 3), (2, 10),
             (2, 15), (3, 15), (9, 15), (9, 13), (9, 11)]


def residuals(vals):
    """The 13 remaining contact equations, as (Xi-Xj)^2 + 3(Yi-Yj)^2 - 4."""
    P = points(*vals)
    out = []
    for (i, j) in REMAINING:
        dx = P[i][0] - P[j][0]
        dy = P[i][1] - P[j][1]
        out.append(dx * dx + 3 * dy * dy - 4)
    return out
