"""Render results_p1.json: the best gain per family, and the gain-vs-criticality picture."""
import json, os, collections, math

HERE = os.path.dirname(os.path.abspath(__file__))
R = [r for r in json.load(open(os.path.join(HERE, "results_p1.json"))) if "gain" in r]
conv = [r for r in R if r["status"] == "optimal"]

print(f"{len(R)} solves, {len(conv)} converged (`optimal`).\n")

print("## Best gain per family (converged solves only)\n")
print("| family | best gain | witness | N | alpha | theta' >= | chi-bar_f | alpha/(n-1) |")
print("|---|---:|:--|---:|---:|---:|---:|---:|")
best = {}
for r in conv:
    f = r["family"]
    if f not in best or r["gain"] > best[f]["gain"]:
        best[f] = r
for f, r in sorted(best.items(), key=lambda kv: -kv[1]["gain"]):
    chi = r.get("chi_bar_f")
    print(f"| `{f}` | **{r['gain']:+.4f}** | `{r['tag']}` | {r['N']} | {r['alpha']} | "
          f"{r['theta_lb']:.4f} | {'%.4f' % chi if chi else '—'} | "
          f"{r['alpha']/(r['n']-1):.2f} |")

print("\n## The tension: gain only appears on witnesses far from critical\n")
print("A witness fires the gate at n only if theta' >= n, and alpha(W) <= alpha(G_d) = n-1,")
print("so it needs gain >= 1 AT alpha(W) = n-1.  Bucketing by criticality alpha/(n-1):\n")
print("| alpha/(n-1) | solves | max gain | mean gain | max theta'/alpha |")
print("|---|---:|---:|---:|---:|")
buckets = collections.defaultdict(list)
for r in conv:
    c = r["alpha"] / (r["n"] - 1)
    key = min(int(c * 5), 4)
    buckets[key].append(r)
for k in sorted(buckets):
    b = buckets[k]
    lo, hi = k / 5, (k + 1) / 5
    lab = f"{lo:.1f}–{hi:.1f}" if k < 4 else "0.8–1.0"
    g = [r["gain"] for r in b]
    rat = [r["theta_lb"] / max(r["alpha"], 1) for r in b]
    print(f"| {lab} | {len(b)} | {max(g):+.4f} | {sum(g)/len(g):+.4f} | {max(rat):.4f} |")

crit = [r for r in conv if r["alpha"] == r["n"] - 1]
print(f"\n**Critical witnesses (alpha = n-1) in the sweep: {len(crit)}.  "
      f"Max gain over them: {max(r['gain'] for r in crit):+.6f}.**")

print("\n## Ring family: theta' against the proved ceiling m/(t+1) - floor(m/(t+1))\n")
print("| m | R/inradius | alpha | theta' >= | chi-bar_f = m/(t+1) | gain | ceiling | ratio |")
print("|---:|---:|---:|---:|---:|---:|---:|---:|")
rings = [r for r in conv if r["family"] == "R-ring" and "chi_bar_f" in r]
rings.sort(key=lambda r: -r["gain"])
seen = set()
for r in rings[:14]:
    key = (r["params"]["m"], round(r["theta_lb"], 4))
    if key in seen:
        continue
    seen.add(key)
    ceil = r["chi_bar_f"] - r["alpha"]
    print(f"| {r['params']['m']} | {r['tag'].split('/R')[-1]} | {r['alpha']} | "
          f"{r['theta_lb']:.4f} | {r['chi_bar_f']:.4f} | {r['gain']:+.4f} | "
          f"{ceil:.4f} | {r['gain']/ceil:.2f} |")

viol = [r for r in conv if "chi_bar_f" in r and r["theta_lb"] > r["chi_bar_f"] + 1e-6]
print(f"\nSandwich alpha <= theta' <= chi-bar_f violated on {len(viol)} of "
      f"{len([r for r in conv if 'chi_bar_f' in r])} solves where chi-bar_f was computed.")
gmax = max(conv, key=lambda r: r["gain"])
print(f"\n**Best gain anywhere in the sweep: {gmax['gain']:+.4f} "
      f"(`{gmax['tag']}`, N={gmax['N']}, alpha={gmax['alpha']}, "
      f"theta' >= {gmax['theta_lb']:.4f}).  Firing needs +1.**")
fired = [r for r in R if r.get("reaches_n")]
print(f"**Witnesses reaching theta' >= n: {len(fired)}.**")
