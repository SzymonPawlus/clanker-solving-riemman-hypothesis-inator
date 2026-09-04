"""Free-vertex descent with perturbation restarts.  FLOATS ONLY."""
import sys, json, math, random, copy
import subdiv
from subdiv import Sub, build

src = sys.argv[1]; out = sys.argv[2]
rounds = int(sys.argv[3]) if len(sys.argv) > 3 else 40
seed = int(sys.argv[4]) if len(sys.argv) > 4 else 0
rng = random.Random(seed)
d = json.load(open(src))
a = d["a"]
if "V" in d:
    V, faces = [list(v) for v in d["V"]], [list(f) for f in d["faces"]]
else:
    V, faces = build(a, [tuple(s) for s in d["sites"]], d["weights"])
S = Sub(a, V, faces)
SCHED = (300., 1500., 8000., 40000.)
best = S.run(ps=SCHED)
bestV = [list(v) for v in S.V]
print("start %.9f  a_max %.6f" % (best, a/best), flush=True)
json.dump({"a": a, "V": bestV, "faces": faces, "max_diam": best, "a_max": a/best}, open(out, "w"))
for r in range(rounds):
    sig = 0.02 * a * (0.3 + rng.random())
    S2 = Sub(a, [list(v) for v in bestV], [list(f) for f in faces])
    for k in range(len(S2.V)):
        c, si = S2.cls[k]
        if c == "pin": continue
        if c == "free":
            S2.V[k][0] += rng.gauss(0, sig); S2.V[k][1] += rng.gauss(0, sig)
        else:
            P, Q = S2.S[si]
            ex, ey = Q[0]-P[0], Q[1]-P[1]; L = math.hypot(ex, ey)
            t = rng.gauss(0, sig)
            S2.V[k][0] += t*ex/L; S2.V[k][1] += t*ey/L
    if not all(subdiv.face_ok(S2.V, f) for f in S2.faces):
        continue
    S2.d = [subdiv.face_diam2(S2.V, f) for f in S2.faces]
    v = S2.run(ps=SCHED)
    if v < best:
        best = v; bestV = [list(x) for x in S2.V]
        json.dump({"a": a, "V": bestV, "faces": faces, "max_diam": best, "a_max": a/best},
                  open(out, "w"))
        print("round %d: %.9f  a_max %.6f  *" % (r, v, a/v), flush=True)
    else:
        print("round %d: %.9f  (best %.9f a_max %.6f)" % (r, v, best, a/best), flush=True)
print("FINAL %.9f  a_max %.6f" % (best, a/best))
