# Erdős–Oler: the hull → triangle relaxation, exactly

**Everything here is `numerical` at best** — exact computation about explicit objects, not proof.
The derivations and their statuses live in
[`problems/circle-packing-equilateral-triangle/attacks/eo-hull-deficit/`](../../problems/circle-packing-equilateral-triangle/attacks/eo-hull-deficit/)
and are `sketch`. Nothing here is assumable (repo `RULES.md` §3).

## Reproduce

```bash
python3 run.py            # ~2 seconds, Python 3.11 standard library only
```

No dependencies, no randomness, no seeds, no network. Output goes to `out/report.txt` and is
reproduced byte-for-byte on a re-run. Exit status is non-zero if any check fails.

## Normalisation — the single most likely source of disagreement

Oler's inequality is stated at minimum separation **1**; this problem's certificates use minimum
separation **2** and side $d = 2a$ (`problems/circle-packing-equilateral-triangle/RULES.md` §2).
**Every certificate coordinate is halved on load**, and $a = d/2$ throughout.

Triangle placement is the repo's: $A=(0,0)$, $B=(a,0)$, $C=(a/2, a\sqrt3/2)$. The *bisector
coordinate* at a corner is $h_A(x,y) = \tfrac{\sqrt3}{2}x + \tfrac12 y$ (and cyclically), so the
corner triangle $\Delta_A(t) = T \cap \{h_A \le \tfrac{\sqrt3}{2}t\}$ is equilateral of side $t$.

## What is exact and what is enclosed

`Alg` (exact $\mathbb{Q}(\sqrt3,\sqrt{11})$) and `Ival` (outward-rounded rational intervals) are
**imported** from [`../packing-oler-slack/exact.py`](../packing-oler-slack/exact.py), which is
read-only to this experiment. `geom.py` here is new: convex hull, shoelace area, half-plane
clipping, lattice generation, and the cited table of optimal separations.

- **Exact, no tolerance:** orientation and hull, all areas, containment tests, corner-triangle
  membership, lattice-point counts, the neutrality comparisons, and every comparison that decides
  a conclusion in §§1–3, 5–7.
- **Rigorously enclosed:** anything containing an edge *length* — perimeters, and therefore
  $\mathrm{def}(K)$ itself. The corner-deficit lemma of §1 is nevertheless certified **without**
  the enclosure, via the exact containment $E \subseteq K$ plus an exact area identity; the
  $\mathrm{def}(H)$ column is reported for information only.
- No floating-point value is ever compared against anything; the floats in the transcript are
  there to be read.

`max_points_in_triangle(t)` is exact for rational $t \le 4$: it uses the `cited` optimal values
$a(n)$ for $n \le 15$ from this problem's README, and Oler's inequality caps $N(4)$ at $15$, so no
larger $n$ can enter that range.

## Sections

1. **Corner-deficit lemma** on every exact certificate in the repo.
2. **Corner-occupancy lemma** (kill-criterion K3 control).
3. **Neutrality**: $(t^2+t)/2 \le T(\lfloor t\rfloor+1) \le N(t)$, equality iff $t \in \mathbb{Z}$.
4. **The barrier** at $a = 6$: $\mathrm{def}(K) \le N(T\setminus K)$ on corner cuts, triple corner
   cuts and 90 arbitrary half-plane cuts.
5. Necessary conditions forced on a hypothetical $n = 27$, $a < 6$ configuration.
6. **The witness**: lattice $T(7)$ minus one *interior* point — 27 points, $a = 6$, corner deficit
   exactly $0$. This is why the route buys nothing unconditionally.
7. A Steiner-type alternative bound, refuted by an exact witness.
