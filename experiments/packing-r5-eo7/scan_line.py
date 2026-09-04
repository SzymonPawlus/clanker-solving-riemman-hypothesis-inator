"""Float scan of the line-relaxation bound over (phi, h, theta).  STATUS: numerical."""
import math, sys, json
sys.path.insert(0, __import__('os').path.dirname(__file__))
from geometry import line_bound, SQRT3

def scan(a=6.0, nphi=241, nh=241, nth=241, hmax=6.5):
    best = (-1, None)
    hist = {}
    for i in range(nphi):
        phi = (math.pi/3.0) * i / (nphi - 1)
        for jh in range(nh):
            h = SQRT3/2.0 + (hmax - SQRT3/2.0) * jh / (nh - 1)
            for kt in range(nth):
                th = kt / nth
                v = line_bound(phi, h, th, a)
                hist[v] = hist.get(v, 0) + 1
                if v > best[0]:
                    best = (v, (phi, h, th))
    return best, hist

if __name__ == "__main__":
    a = float(sys.argv[1]) if len(sys.argv) > 1 else 6.0
    best, hist = scan(a=a)
    print("a =", a)
    print("max line-relaxation bound =", best[0])
    phi, h, th = best[1]
    print("  at phi = %.9f (deg %.5f), h = %.9f, theta = %.9f" % (phi, math.degrees(phi), h, th))
    print("  h/(sqrt3/2) =", h/(SQRT3/2))
    print("histogram:", dict(sorted(hist.items())))
