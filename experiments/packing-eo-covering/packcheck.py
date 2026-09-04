"""SELF-CHECK ONLY (not a deliverable): max-min separation of n points in T_1,
so a_n = 1/dmax.  Used to test that my covering bounds a_n >= p*sqrt3/2 are not
contradicted by an explicit packing.  Floats; a contradiction would be a finding
to investigate, not a result."""
import math, random, sys
SQ3 = math.sqrt(3.0)

def inside(p):
    x, y = p
    return y >= 0 and y <= x*SQ3 + 1e-12 and y <= (1-x)*SQ3 + 1e-12

def clamp(p):
    return p   # moves outside the triangle are rejected by the caller

def mind(P):
    m = 1e9
    for i in range(len(P)):
        for j in range(i+1, len(P)):
            d = math.hypot(P[i][0]-P[j][0], P[i][1]-P[j][1])
            if d < m: m = d
    return m

def opt(n, rng, iters=40000):
    P = []
    while len(P) < n:
        x = rng.random(); y = rng.random()*SQ3/2
        if inside((x, y)): P.append((x, y))
    best = mind(P)
    step = 0.05
    for it in range(iters):
        step = 0.05*(1-it/iters)**2 + 1e-5
        k = rng.randrange(n)
        old = P[k]
        cand = (old[0]+rng.gauss(0, step), old[1]+rng.gauss(0, step))
        if not inside(cand):
            continue
        P[k] = cand
        v = mind(P)
        if v >= best: best = v
        else: P[k] = old
    return best, P

if __name__ == "__main__":
    for n in [int(x) for x in sys.argv[1].split(",")]:
        rng = random.Random(n*97+5)
        b = 0.0
        for r in range(int(sys.argv[2])):
            v, P = opt(n, rng)
            b = max(b, v)
        print("n=%2d  best min-sep in T_1 = %.6f  ->  a_%d <= %.6f" % (n, b, n, 1.0/b), flush=True)
