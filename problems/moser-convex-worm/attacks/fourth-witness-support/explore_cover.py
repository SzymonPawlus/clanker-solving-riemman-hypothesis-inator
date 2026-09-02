#!/usr/bin/env python3
"""Numerical portfolio scan for Issue 167. Never a proof predicate."""
import math

c, s = 69 / 269, 260 / 269
phi = math.atan2(s, c)
RAW = {
    "S": [(0, 0), (1, 0)],
    "T": [(0, 0), (.5, 0), (.25, math.sqrt(3) / 4)],
    "Q": [(0, 0), (1/3, 0), (1/3, 1/3), (0, 1/3)],
    "W": [(0, 0), (1/3, 0), (338/807, 260/807),
          (9361/72361, 105820/217083)],
}

def rotate(points, angle):
    ca, sa = math.cos(angle), math.sin(angle)
    return [(ca*x-sa*y, sa*x+ca*y) for x, y in points]

def support(points, angle):
    ca, sa = math.cos(angle), math.sin(angle)
    return max(ca*x + sa*y for x, y in points)

def width(points, angle):
    ca, sa = math.cos(angle), math.sin(angle)
    values = [ca*x + sa*y for x, y in points]
    return max(values) - min(values)

def portfolio(alpha, beta, gamma):
    ps = {k: rotate(RAW[k], a) for k, a in
          {"S": 0, "T": beta, "Q": alpha, "W": gamma}.items()}
    bs = max(width(p, math.pi/2) / 2 for p in ps.values())
    bq = (max(width(p, alpha) for p in ps.values()) +
          max(width(p, alpha+math.pi/2) for p in ps.values())) / 6
    tn = [beta-math.pi/2, beta+math.pi/6, beta+5*math.pi/6]
    bt = max(sum(support(p, n) for n in tn) / 4 for p in ps.values())
    wn = [gamma-math.pi/2, gamma+phi-math.pi/2,
          gamma+2*phi-math.pi/2, gamma+phi+math.pi/2]
    cv = [(support(p, wn[0])+support(p, wn[2])+
           2*c*support(p, wn[3]))/6 for p in ps.values()]
    dv = [(support(p, wn[1])+support(p, wn[3]))/6 for p in ps.values()]
    bw = max(cv) + max(dv)
    return max(bs, bq, bt, bw), (bs, bq, bt, bw)

def main():
    dims = (24, 32, 128)
    best = (1.0, None)
    low = []
    for ia in range(dims[0]):
        a = (ia+.5)*math.pi/(2*dims[0])
        for ib in range(dims[1]):
            b = (ib+.5)*2*math.pi/(3*dims[1])
            for ig in range(dims[2]):
                g = (ig+.5)*2*math.pi/dims[2]
                value, pieces = portfolio(a, b, g)
                if value < best[0]:
                    best = (value, (ia, ib, ig, a, b, g, pieces))
                if value < .235:
                    low.append((value, ia, ib, ig))
    print("grid", dims, "minimum", best)
    print("cells below .235", len(low))
    print("lowest cells", sorted(low)[:20])

if __name__ == "__main__":
    main()
