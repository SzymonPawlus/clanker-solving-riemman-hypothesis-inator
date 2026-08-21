"""How many points of a unit triangular lattice fit in an equilateral triangle
of side a < 6?  `numerical` evidence only -- a grid search over the lattice's
orientation and translation relative to the triangle.  Nothing here is a proof:
a grid can miss the maximum.  Run: python3 lattice_probe.py

Why it matters: if a 27-point unit-separated configuration in T(a), a < 6, could
be forced to lie in SOME unit triangular lattice, Erdos-Oler k=7 would follow
from  max_{Lambda} |Lambda ∩ T(a)| <= 26  for a < 6.  This measures that max.
"""
import math

SQ3 = math.sqrt(3.0)


def count(a, theta, tx, ty, margin):
    """Lattice points (unit triangular lattice) inside T(a) rotated by theta and
    translated by (tx,ty), counted with an outward `margin` (so an upper bound)."""
    c, s = math.cos(theta), math.sin(theta)
    # triangle vertices, rotated then translated
    V = [(0.0, 0.0), (a, 0.0), (a / 2, a * SQ3 / 2)]
    V = [(c * x - s * y + tx, s * x + c * y + ty) for x, y in V]
    xs = [p[0] for p in V]
    ys = [p[1] for p in V]
    # lattice: i*(1,0) + j*(1/2, sqrt3/2)
    jlo = int(math.floor((min(ys) - 1) / (SQ3 / 2)))
    jhi = int(math.ceil((max(ys) + 1) / (SQ3 / 2)))
    # edge half-plane tests, oriented ccw
    E = []
    for k in range(3):
        (x1, y1), (x2, y2) = V[k], V[(k + 1) % 3]
        ex, ey = x2 - x1, y2 - y1
        L = math.hypot(ex, ey)
        E.append((x1, y1, ex / L, ey / L))
    n = 0
    for j in range(jlo, jhi + 1):
        y = j * SQ3 / 2
        ilo = int(math.floor(min(xs) - 1 - j * 0.5))
        ihi = int(math.ceil(max(xs) + 1 - j * 0.5))
        for i in range(ilo, ihi + 1):
            x = i + j * 0.5
            ok = True
            for (x1, y1, ux, uy) in E:
                if ux * (y - y1) - uy * (x - x1) < -margin:
                    ok = False
                    break
            if ok:
                n += 1
    return n


def sweep(a, nth, ntr, margin):
    best, arg = 0, None
    for it in range(nth):
        th = math.pi / 3 * it / nth
        for p in range(ntr):
            for q in range(ntr):
                tx = p / ntr + 0.5 * (q / ntr)
                ty = (q / ntr) * SQ3 / 2
                m = count(a, th, tx, ty, margin)
                if m > best:
                    best, arg = m, (th, tx, ty)
    return best, arg


if __name__ == "__main__":
    lines = []
    def say(s=""):
        lines.append(s); print(s)

    say("Grid search: max |Lambda ∩ T(a)| over lattice orientation and translation.")
    say("margin = outward tolerance, so the reported count is an UPPER bound on")
    say("the true count for the exact triangle (conservative).")
    say()
    say(f"{'a':>10}{'theta steps':>13}{'transl grid':>13}{'margin':>10}{'max count':>11}")
    for a, nth, ntr, mg in ((6.0, 60, 30, 1e-9),
                            (5.999, 60, 30, 1e-9),
                            (5.999, 120, 60, 1e-9),
                            (5.99, 120, 60, 1e-9),
                            (5.9, 120, 60, 1e-9),
                            (5.87, 120, 60, 1e-9)):
        best, arg = sweep(a, nth, ntr, mg)
        say(f"{a:>10}{nth:>13}{ntr:>13}{mg:>10.0e}{best:>11}")
    open("out/lattice_probe.txt", "w").write("\n".join(lines) + "\n")
