"""Refine the honeycomb alignment for T_a and dump the hexagon centres."""
import math, json, sys
from honeycomb import count, area
from search import triangle, clip
SQ3 = math.sqrt(3.0)

def centres(a, th, ox, oy):
    tri = triangle(a)
    c, s = math.cos(th), math.sin(th)
    def rot(p): return (c*p[0]-s*p[1], s*p[0]+c*p[1])
    g1 = rot((0.75, SQ3/4)); g2 = rot((0.75, -SQ3/4))
    hexv = [rot((0.5*math.cos(k*math.pi/3), 0.5*math.sin(k*math.pi/3))) for k in range(6)]
    R = int(a/0.4)+4
    out = []
    for i in range(-R, R+1):
        for j in range(-R, R+1):
            cx = ox + i*g1[0] + j*g2[0]; cy = oy + i*g1[1] + j*g2[1]
            poly = [(cx+vx, cy+vy) for vx, vy in hexv]
            p = poly
            for k in range(3):
                x1, y1 = tri[k]; x2, y2 = tri[(k+1)%3]
                nx, ny = (y2-y1), -(x2-x1)
                x3, y3 = tri[(k+2)%3]
                cc = nx*x1+ny*y1
                if nx*x3+ny*y3 > cc: nx, ny, cc = -nx, -ny, -cc
                p = clip(p, nx, ny, cc)
                if not p: break
            if p and area(p) > 1e-12:
                out.append((cx, cy, area(p)))
    return out

def refine(a, th0, span, ox0, oy0, ospan, K=30):
    best = (10**9, None)
    for ti in range(K+1):
        th = th0 + span*(2.0*ti/K - 1.0)
        for oi in range(K+1):
            for oj in range(K+1):
                ox = ox0 + ospan*(2.0*oi/K - 1.0)
                oy = oy0 + ospan*(2.0*oj/K - 1.0)
                n, tot = count(a, th, ox, oy)
                if n < best[0]:
                    best = (n, (th, ox, oy))
    return best

if __name__ == "__main__":
    a = float(sys.argv[1])
    n, par = refine(a, math.pi/6, 0.06, 0.4286, 0.2474, 0.10, K=16)
    print("refined near theta=pi/6:", n, par)
    n2, par2 = refine(a, 0.0, 0.06, 0.0, 0.0, 0.38, K=16)
    print("refined near theta=0   :", n2, par2)
    if n2 < n: n, par = n2, par2
    cs = centres(a, *par)
    print("centres:", len(cs), "min clipped area %.4f" % min(c[2] for c in cs))
    json.dump({"a": a, "n": len(cs), "theta": par[0], "off": par[1:],
               "centres": [[c[0], c[1]] for c in cs],
               "clipped_area": [c[2] for c in cs]},
              open("hex_a%g.json" % a, "w"))
