"""Render results.json as the markdown tables used in the r4-theta write-up."""
import json, math

rows = [r for r in json.load(open("results.json")) if "error" not in r]


def oler(n):
    return math.sqrt(8 * n + 1) - 3


print("### 4.1 Refinement ladder — the instrument, not the quantity\n")
print("*n = 8 at d = Oler's floor, corner-to-corner grid.  The reported value is a "
      "repaired-primal LOWER bound, so a coarse grid whose solve converges beats a fine "
      "grid whose solve does not.*\n")
print("| refine | pts/side | N | spacing | alpha(grid) | theta'(grid) >= | solver value "
      "| status | solve |")
print("|---:|---:|---:|---:|---:|---:|---:|:--|---:|")
for r in rows:
    if r["n"] != 8 or r["label"] != "oler-floor":
        continue
    print(f"| {r['refine']} | {r['k']} | {r['N']} | {r['spacing']:.3f} | {r['alpha_grid']} "
          f"| {r['theta_lb']:.4f} | {r['theta_solver']:.4f} | `{r['status']}` | "
          f"{r['solve_s']:.0f} s |")

print("\n### 4.2 The gate table\n")
print("*Best (largest) certified value per (n, probe).  The gate fires iff it reaches n.*\n")
print("| n | known d(n) | Oler floor | d probe | what d is | witness | N | alpha(grid) | "
      "theta'(grid) >= | gain | reaches n? |")
print("|---:|---:|---:|---:|:--|:--|---:|---:|---:|---:|:--|")
best = {}
for r in rows:
    key = (r["n"], r["label"])
    if key not in best or r["theta_lb"] > best[key]["theta_lb"]:
        best[key] = r
for (n, label) in sorted(best):
    r = best[(n, label)]
    dk = r.get("d_known")
    dks = f"{dk:.6f}" if dk else "*open*"
    wit = "anchored" if label.endswith("-anchored") else "corner"
    base = label.replace("-anchored", "")
    print(f"| {n} | {dks} | {oler(n):.6f} | {r['d']:.6f} | {base} | {wit} | {r['N']} | "
          f"{r['alpha_grid']} | {r['theta_lb']:.4f} | "
          f"{r['theta_lb'] - r['alpha_grid']:+.4f} | "
          f"**{'YES — gate fires' if r['fires'] else 'no'}** |")

print("\n### 4.3 Every record\n")
print("| n | label | d | refine | N | non-edges | alpha | theta' >= | solver | status | "
      "build | solve |")
print("|---:|:--|---:|---:|---:|---:|---:|---:|---:|:--|---:|---:|")
for r in rows:
    print(f"| {r['n']} | {r['label']} | {r['d']:.4f} | {r['refine']} | {r['N']} | "
          f"{r['nonedges']} | {r['alpha_grid']} | {r['theta_lb']:.4f} | "
          f"{r['theta_solver']:.4f} | `{r['status']}` | {r['build_s']} s | "
          f"{r['solve_s']} s |")
