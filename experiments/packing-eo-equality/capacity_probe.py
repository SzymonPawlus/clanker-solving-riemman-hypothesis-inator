"""Does a *true-capacity* partition/covering bound supply the missing point at
k = 7?  `numerical` probe, prompted by the manager's retraction of the claim
that partition schemes are dead.

The live mechanism: if T(a) can be covered by N sets each of diameter < 1, then
n <= N, because two points of a unit-separated set cannot share a set.  This is
NOT "apply Oler to each piece and sum" (which is dead by the partition identity)
-- it caps each piece by its true capacity, 1.

Cheapest concrete version: a hexagonal cell tiling with cells of circumdiameter
1 - eta < 1.  Count the cells that actually meet T(a), minimised over the
tiling's orientation and translation.  Convexity => exact-enough intersection
test by separating axes.  Floats; this is evidence, not a certificate.
"""
import math

SQ3 = math.sqrt(3.0)


def hexagon(cx, cy, R, phi):
    return [(cx + R * math.cos(phi + k * math.pi / 3),
             cy + R * math.sin(phi + k * math.pi / 3)) for k in range(6)]


def sep_axis(P, Q):
    """True if convex polygons P, Q are separated (no intersection)."""
    for poly in (P, Q):
        m = len(poly)
        for i in range(m):
            x1, y1 = poly[i]
            x2, y2 = poly[(i + 1) % m]
            ax, ay = -(y2 - y1), x2 - x1
            pa = [ax * x + ay * y for x, y in P]
            qa = [ax * x + ay * y for x, y in Q]
            if max(pa) < min(qa) - 1e-12 or max(qa) < min(pa) - 1e-12:
                return True
    return False


def cells_meeting_triangle(a, R, phi, tx, ty):
    """Hexagon cells (circumradius R, orientation phi, lattice offset t) that
    intersect the equilateral triangle of side a."""
    T = [(0.0, 0.0), (a, 0.0), (a / 2, a * SQ3 / 2)]
    # cell centres: triangular lattice of spacing s = sqrt3 * R, rotated by phi
    s = SQ3 * R
    u = (s * math.cos(phi + math.pi / 6), s * math.sin(phi + math.pi / 6))
    v = (s * math.cos(phi + math.pi / 2), s * math.sin(phi + math.pi / 2))
    n = 0
    rng = int(a / s) + 4
    for i in range(-rng, rng + 1):
        for j in range(-rng, rng + 1):
            cx = tx + i * u[0] + j * v[0]
            cy = ty + i * u[1] + j * v[1]
            if cx < -1.5 or cx > a + 1.5 or cy < -1.5 or cy > a * SQ3 / 2 + 1.5:
                continue
            H = hexagon(cx, cy, R, phi)
            if not sep_axis(H, T):
                n += 1
    return n


if __name__ == "__main__":
    lines = []
    def say(s=""):
        lines.append(s); print(s)

    say("Hexagonal-cell covering of T(a) by cells of diameter 1 - eta < 1.")
    say("n <= (number of cells meeting T), minimised over orientation and offset.")
    say("Erdos-Oler k=7 needs n <= 26 for every a < 6.  Oler alone gives 27.")
    say()
    eta = 1e-6
    R = (1 - eta) / 2
    say(f"{'a':>8}{'cell diam':>11}{'min cells':>11}{'area bound':>12}"
        f"{'Oler bound':>12}")
    for a in (5.999, 5.9, 2.0 - 1e-6, 1.999):
        best = 10 ** 9
        for it in range(24):
            phi = math.pi / 3 * it / 24
            for p in range(14):
                for q in range(14):
                    s = SQ3 * R
                    tx = (p / 14) * s * math.cos(phi + math.pi / 6) \
                        + (q / 14) * s * math.cos(phi + math.pi / 2)
                    ty = (p / 14) * s * math.sin(phi + math.pi / 6) \
                        + (q / 14) * s * math.sin(phi + math.pi / 2)
                    c = cells_meeting_triangle(a, R, phi, tx, ty)
                    best = min(best, c)
        area = SQ3 / 4 * a * a
        hexarea = 3 * SQ3 / 2 * R * R
        oler = (a * a + 3 * a + 2) / 2
        say(f"{a:>8}{2*R:>11.6f}{best:>11}{area/hexarea:>12.3f}{oler:>12.4f}")
    say()
    say("'area bound' = area(T)/area(cell): the information-theoretic floor for")
    say("this family of coverings, before any boundary waste.")
    open("out/capacity_probe.txt", "w").write("\n".join(lines) + "\n")
