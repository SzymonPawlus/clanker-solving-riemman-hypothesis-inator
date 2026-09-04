"""Reduced refutation: 5 colours on dense point sets strictly inside U."""
import math, sys, time
from explore import S3, A, B, C, CORN, d, inT, boundary_U, colour

def inU(p, eps):
    return inT(p) and all(d(p, V) > 1 + eps for V in CORN)

def dense(N, eps):
    pts = []
    for j in range(N + 1):
        for i in range(N + 1 - j):
            p = (3 * (2 * i + j) / (2 * N), 3 * S3 * j / (2 * N))
            if inU(p, eps):
                pts.append(p)
    return pts

if __name__ == "__main__":
    eps = float(sys.argv[1]) if len(sys.argv) > 1 else 0.005
    for (nb, N) in [(12, 10), (24, 16), (36, 24), (48, 32), (64, 40), (80, 50), (100, 60)]:
        pts = list({(round(p[0], 9), round(p[1], 9)) for p in
                    [q for q in boundary_U(nb, nb, eps) if inU(q, eps * 0.5)] + dense(N, eps)})
        print(f"nb={nb} N={N}:", flush=True)
        r, _ = colour(pts, 5)
        if not r:
            print("*** UNSAT: no 5-cover of U, hence no 8-cover of T(3) ***"); break
