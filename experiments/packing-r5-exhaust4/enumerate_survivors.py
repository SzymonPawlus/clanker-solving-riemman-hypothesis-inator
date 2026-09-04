"""Enumerate every level-L cell profile that survives all sound rules for
   P(n, t, strict).  Writes centroids so the survivors can be inspected.

Usage: python3 enumerate_survivors.py n t strict L out.json [time_limit]
"""
import json, sys
from fractions import Fraction
from eo4.search import Prover
from eo4 import geom

n = int(sys.argv[1]); t = Fraction(sys.argv[2]); strict = sys.argv[3] == "1"
L = int(sys.argv[4]); out = sys.argv[5]
tl = float(sys.argv[6]) if len(sys.argv) > 6 else 600.0

pr = Prover(n, t, strict, L, max_cited=8)
res = pr.run_enumerate(time_limit=tl, checkpoint=out + ".ckpt")
surv = res.pop("survivors")


def centroid(cell, LM):
    vs = geom.verts_at(cell, LM)
    ci = Fraction(sum(v[0] for v in vs), 3)
    cj = Fraction(sum(v[1] for v in vs), 3)
    # cartesian, unit triangle, h = 2^-LM
    h = Fraction(1, 1 << LM)
    return (float(h * (ci + cj / 2)), float(h * cj) * 0.8660254037844386)


res["n_survivors"] = len(surv)
res["survivor_centroids"] = [
    sorted(centroid(c, pr.LM) for c, m in s for _ in range(m)) for s in surv[:400]]
res["survivor_cells"] = [[[list(c), m] for c, m in s] for s in surv[:400]]
with open(out, "w") as f:
    json.dump(res, f, indent=1)
print(json.dumps({k: v for k, v in res.items()
                  if k not in ("survivor_centroids", "survivor_cells")}))
