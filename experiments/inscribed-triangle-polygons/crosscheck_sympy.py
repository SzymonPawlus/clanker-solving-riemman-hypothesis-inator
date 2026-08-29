"""Independent cross-check of the decider, using sympy's own exact geometry.

The point of this file is NOT to re-run `geom.py`. It re-decides goodness through a completely
different code path:

  * numbers are sympy `Rational`/`sqrt(3)` expressions rather than my (a, b) pairs over Q;
  * segment-segment intersection is `sympy.geometry.Segment2D.intersection`, which I did not
    write, rather than my `seg_intersect`;
  * the only thing shared with `geom.py` is the *reduction* itself and the fixture list.

If the two disagree anywhere, at least one is wrong and the whole experiment is suspect.

    python3 crosscheck_sympy.py [--limit N] [--group G]

Slow by design (sympy's exact geometry is far heavier than the pair arithmetic), so it runs
over the named fixtures, not the pseudorandom ones.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time

import sympy as sp
from sympy.geometry import Point2D, Segment2D

from fixtures import battery
from geom import decide_good, is_simple

HERE = os.path.dirname(os.path.abspath(__file__))
S3 = sp.sqrt(3)


def to_sp(pt):
    """Convert one of my K-points to a sympy Point2D."""
    return Point2D(sp.Rational(pt[0].a) + sp.Rational(pt[0].b) * S3,
                   sp.Rational(pt[1].a) + sp.Rational(pt[1].b) * S3)


def rot(p, o, sigma):
    """Rotate p about o by sigma*60 degrees, in sympy."""
    c = sp.Rational(1, 2)
    s = sigma * S3 / 2
    vx = sp.simplify(p.x - o.x)
    vy = sp.simplify(p.y - o.y)
    return Point2D(sp.simplify(o.x + c * vx - s * vy), sp.simplify(o.y + s * vx + c * vy))


def good_sympy(poly, O):
    """Same reduction, sympy arithmetic and sympy's own segment intersection."""
    n = len(poly)
    segs = [Segment2D(poly[i], poly[(i + 1) % n]) for i in range(n)]
    for sigma in (1, -1):
        rsegs = [Segment2D(rot(poly[i], O, sigma), rot(poly[(i + 1) % n], O, sigma))
                 for i in range(n)]
        for rs in rsegs:
            for s in segs:
                for obj in rs.intersection(s):
                    pts = [obj] if isinstance(obj, Point2D) else [obj.p1, obj.p2]
                    for X in pts:
                        if X != O:                    # exclude the trivial fixed point
                            return True, (sigma, X)
    return False, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0, help="max fixtures (0 = all named ones)")
    ap.add_argument("--group", default=None)
    args = ap.parse_args()

    fxs = [f for f in battery() if f["group"] != "random"]
    if args.group:
        fxs = [f for f in fxs if f["group"] == args.group]
    if args.limit:
        fxs = fxs[:args.limit]

    t0 = time.time()
    rows = []
    disagreements = []
    for f in fxs:
        poly = f["poly"]
        assert is_simple(poly)[0]
        spoly = [to_sp(p) for p in poly]
        for i, V in enumerate(poly):
            mine = decide_good(poly, V)["good"]
            theirs, _ = good_sympy(spoly, spoly[i])
            rows.append({"fixture": f["name"], "vertex": i, "mine": mine, "sympy": theirs})
            if mine != theirs:
                disagreements.append(rows[-1])
                print(f"  DISAGREEMENT {f['name']} vertex {i}: mine={mine} sympy={theirs}")
        print(f"  {f['name']:<44} {len(poly)} vertices  ok  ({time.time()-t0:.1f}s)", flush=True)
        with open(os.path.join(HERE, "out", "crosscheck_sympy.json"), "w") as fh:
            json.dump({"sympy_version": sp.__version__, "python": sys.version.split()[0],
                       "fixtures_checked": len({r['fixture'] for r in rows}),
                       "vertices_checked": len(rows), "disagreements": disagreements,
                       "seconds": round(time.time() - t0, 2), "rows": rows}, fh, indent=1)

    print(f"\n{len(rows)} vertices re-decided with sympy {sp.__version__}; "
          f"{len(disagreements)} disagreements ({time.time()-t0:.1f}s)")
    return 1 if disagreements else 0


if __name__ == "__main__":
    sys.exit(main())
