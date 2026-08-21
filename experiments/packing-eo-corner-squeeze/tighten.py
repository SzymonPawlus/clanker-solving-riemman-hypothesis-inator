"""How much sharper would the capacity inputs have to be to close the gap?

Reduce every capacity in the relaxation by tau (never below 1) and find the least
tau that makes the system infeasible.  tau is then a measure, in points, of the
distance between what is known about N(.) and what a proof of Erdos-Oler would need.
"""
import sys, time
from fractions import Fraction as F
import relax as R


def tighten(cons_list, tau, n):
    out = []
    for (nm, mem, lo, hi) in cons_list:
        if nm == "total":
            out.append((nm, mem, lo, hi))
        else:
            out.append((nm, mem, lo, max(1, hi - tau) if hi < n else hi - tau))
    return out


if __name__ == "__main__":
    for k in [int(x) for x in sys.argv[1:]] or [4, 5]:
        a = F(k - 1) - F(1, 100)
        cells, cc, cl, info = R.build(k, a)
        n = info["n"]
        for tau in range(0, 6):
            cl2 = tighten(cl, tau, n)
            cc2 = [max(1, c - tau) for c in cc]
            t = time.time()
            z, nodes = R.feasible(cells, cc2, cl2, n, node_limit=40_000_000)
            v = "FEASIBLE" if isinstance(z, list) else str(z)
            print("k=%d tau=%d -> %s (%d nodes, %.0fs)" % (k, tau, v, nodes, time.time() - t),
                  flush=True)
            if v != "FEASIBLE":
                break
