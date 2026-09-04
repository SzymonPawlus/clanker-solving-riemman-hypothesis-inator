"""Randomised hunt for a small {0,1}-weighted counterexample to Edmonds-Giles at tau_w = 2.
Status: numerical.  Deterministic given --seed.  Writes hits to hits.json as it goes.
Space: random DAGs on n vertices (arc (i,j), i<j, kept with prob p), random weight-1 subsets;
this is a *sample*, not a census; a hit is verified by the independent full 2-colouring search."""
import argparse, json, random, time
from tau2lib import dicuts, two_colourable_traces


def minimal(masks):
    ms = sorted(set(masks), key=lambda x: bin(x).count("1"))
    out = []
    for m in ms:
        if not any((o & m) == o for o in out):
            out.append(m)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, nargs="+", default=[7, 8])
    ap.add_argument("--seconds", type=float, default=240)
    ap.add_argument("--seed", type=int, default=152)
    ap.add_argument("--weightings", type=int, default=300)
    ap.add_argument("--out", default="hits.json")
    a = ap.parse_args()
    rng = random.Random(a.seed)
    t0 = time.time()
    dags = tried = hits = 0
    found = []
    while time.time() - t0 < a.seconds:
        n = rng.choice(a.n)
        p = rng.uniform(0.3, 0.6)
        arcs = [(i, j) for i in range(n) for j in range(i + 1, n) if rng.random() < p]
        m = len(arcs)
        if m < 6 or m > 18:
            continue
        D = dicuts(n, arcs)
        if 0 in D.values():           # weakly disconnected: tau = 0
            continue
        cuts = list(D.values())
        if any(bin(c).count("1") < 2 for c in cuts):   # singleton dicut: tau_w <= 1 always
            continue
        dags += 1
        mins = minimal(cuts)
        for _ in range(a.weightings):
            q = rng.uniform(0.3, 0.8)
            J = 0
            for i in range(m):
                if rng.random() < q:
                    J |= 1 << i
            traces = [c & J for c in mins]
            if any(bin(t).count("1") < 2 for t in traces):
                continue
            if min(bin(t).count("1") for t in traces) != 2:
                continue                                 # want tau_w exactly 2
            tried += 1
            ones = [i for i in range(m) if (J >> i) & 1]
            idx = {v: k for k, v in enumerate(ones)}
            tr2 = []
            for t in traces:
                x = 0
                for i in ones:
                    if (t >> i) & 1:
                        x |= 1 << idx[i]
                tr2.append(x)
            if two_colourable_traces(tr2, len(ones)) is None:
                hits += 1
                w = [1 if (J >> i) & 1 else 0 for i in range(m)]
                rec = {"n": n, "arcs": arcs, "w": w, "n_weight1": len(ones)}
                found.append(rec)
                with open(a.out, "w") as f:
                    json.dump({"seed": a.seed, "dags": dags, "tau2_instances": tried,
                               "hits": found}, f, indent=1)
                print("HIT", rec, flush=True)
    print(f"done: dags={dags} tau_w=2 instances={tried} hits={hits} in {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()
