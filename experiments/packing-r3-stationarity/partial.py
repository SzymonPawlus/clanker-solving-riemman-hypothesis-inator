"""Rigorous PARTIAL support counts.

Any subset of the admissible graphs gives a valid LOWER bound on the total number of
admissible support classes, because supports built on non-isomorphic loaded graphs are
never isomorphic.  This script walks the geng stream for a given m, counts support
classes exactly for the first `maxgraphs` admissible graphs (or until `deadline`
seconds), and reports the partial sum together with how much of the stream it covered.
"""
from __future__ import annotations

import sys
import time

from support_enum import Quad, graph_admissible, wall_capacity
from fastcount import automorphisms, count_labellings, geng_stream


def main():
    d = Quad(int(sys.argv[1]), int(sys.argv[2]))
    m = int(sys.argv[3])
    maxgraphs = int(sys.argv[4])
    deadline = float(sys.argv[5])
    cap = wall_capacity(d)
    ca = not (d - Quad(2)).sign() > 0
    t0 = time.time()
    seen = adm = nsup = 0
    for G in geng_stream(m):
        seen += 1
        if not graph_admissible(G):
            continue
        adm += 1
        nsup += count_labellings(G, cap, ca, automorphisms(G), True)
        if adm >= maxgraphs or time.time() - t0 > deadline:
            break
        if adm % 20 == 0:
            print(f"  ... m={m} adm={adm} partial_supports={nsup} "
                  f"({time.time()-t0:.0f}s)", flush=True)
    print(f"m={m} cap={cap} graphs_scanned={seen} admissible_used={adm} "
          f"PARTIAL_supports>={nsup} secs={time.time()-t0:.1f}", flush=True)


if __name__ == "__main__":
    main()
