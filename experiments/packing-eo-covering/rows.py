"""The staggered-row accounting quoted in attacks/eo-covering-construct README §4.

Floats: this is an accounting argument about idealised shapes, not a certificate.
Prints the edge-pentagon optimum, the alternating-gap recursion above it, and the
cumulative comparison against the plain hexagon lattice cut at the boundary.
"""
import math

def pent(s):
    """area of the best diameter-1 pentagon with a flat side of length s on dT"""
    return s*(math.sqrt(1-s*s) + math.sqrt(1-s*s/4))/2

s, A0 = max(((x/2000.0, pent(x/2000.0)) for x in range(1, 1999)), key=lambda t: t[1])
h1, h2 = math.sqrt(1-s*s), math.sqrt(1-s*s/4)
t0 = s*s/(4*(h2-h1))
k = s*s/8

def nxt(t):
    c = 1 - (t/2 + k/t)
    d = c*c - 2*k
    if d < 0: return None, None
    tp = c + math.sqrt(d)
    UL = (t+tp)/2 - k*(1/t + 1/tp)
    return tp, s*(1 + UL)/2

HEX = 3*math.sqrt(3)/8
CUT = HEX - (math.sqrt(3)/2)*0.25/2      # hexagon cut at its two lower vertices

print("edge pentagon: s = %.4f, h1 = %.4f, h2 = %.4f, area = %.4f" % (s, h1, h2, A0))
print("forced gap to row 1: t = %.4f" % t0)
areas = [A0]; t = t0
for r in range(1, 8):
    t, a = nxt(t)
    print("  row %d: gap %.4f  area %.4f" % (r, t, a))
    areas.append(a)
print("regular hexagon %.4f ; hexagon cut at boundary %.4f" % (HEX, CUT))
print("\nrows   plain-lattice   deep-notch")
for r in (1, 2, 3, 4, 7):
    print("%4d %14.3f %12.3f" % (r, CUT + HEX*(r-1), sum(areas[:r])))
