# Oler slack localisation — exact face/edge decomposition

**Question.** Oler's inequality $N \le \frac{2}{\sqrt3}A(P) + \frac12 M(P) + 1$ is tight on
triangular lattices and slack everywhere else we can check. *Where, geometrically, does the slack
sit?* And does the answer suggest a local strengthening?

**Status of everything this produces:** `numerical` at best — it is exact computation, not proof.
The write-up and the derivations live in
[`problems/circle-packing-equilateral-triangle/attacks/oler-slack-analysis/`](../../problems/circle-packing-equilateral-triangle/attacks/oler-slack-analysis/)
and are `sketch`. Nothing here is assumable (repo `RULES.md` §3). Issue
[#78](https://github.com/SzymonPawlus/clanker-solving-riemman-hypothesis-inator/issues/78).

## Reproduce

```bash
python3 run.py            # ~2 seconds, Python 3.11 standard library only
```

No dependencies, no randomness, no seeds, no network: every number is a `fractions.Fraction`
or an element of $\mathbb{Q}(\sqrt3,\sqrt{11})$. Output goes to `out/report.txt` (transcript)
and `out/report.json` (machine-readable). Re-running overwrites both and must reproduce them
byte-for-byte, since nothing in the pipeline is stochastic.

## Method — what is exact and what is enclosed

| File | What it is |
|---|---|
| `exact.py` | `Alg`: exact arithmetic in $\mathbb{Q}(\sqrt3,\sqrt{11})$ on the basis $(1,\sqrt3,\sqrt{11},\sqrt{33})$, with exact sign decisions. `Ival`: rational intervals with outward rounding. |
| `geometry.py` | Exact hull, boundary cycle, triangulation, and the slack decomposition. |
| `run.py` | The six sections listed below. |

**Exact, with no tolerance anywhere:** orientation tests, collinearity, hull, point-in-triangle
location, all areas, the face count, the per-face excess, the total face excess, and every
comparison that decides a *conclusion*. Sign decisions on `Alg` terminate because
$1,\sqrt3,\sqrt{11},\sqrt{33}$ are linearly independent over $\mathbb{Q}$, so a non-zero element
is bounded away from zero.

**Rigorously enclosed, never estimated:** anything containing an edge *length*, i.e. the
perimeter $M(P)$, the boundary-edge excess and hence Oler's slack itself. Square roots of
non-squares leave the field, so those are rational intervals with outward rounding — a reported
interval contains the true value. No floating-point number is ever compared against anything; the
`float` values in the transcript exist to be read.

**Normalisation.** Oler's inequality is stated at minimum separation 1; this problem's
certificates use minimum separation 2 (`problems/circle-packing-equilateral-triangle/RULES.md`
§2). Certificate coordinates are therefore **halved on load**, and the point-triangle side used
here is $a = d/2$. This is the single most likely place for an independent reimplementation to
disagree, so it is stated in the code at every use site.

## What it computes

1. **Controls.** The triangular lattices $n = 3, 6, 10$ must give *exactly* zero: zero excess on
   every face, length exactly 1 on every boundary edge, and slack exactly $[0,0]$. This is the
   secondary kill-criterion of issue #78; if it fails, nothing downstream means anything and the
   script exits non-zero.
2. **Slack atlas.** For every exact certificate in the repo ($n = 1$–$10, 14, 15, 20, 21$, plus
   `results/`): $n$, boundary/interior counts, face count, face excess, boundary-edge excess, and
   a split of the *triangle* bound's slack into **stage 1** (Oler applied to the convex hull) and
   **stage 2** (relaxing the hull to the containing triangle).
3. **The probe.** Is the total face excess $\ge 0$ for unit-separated sets? — the hypothesis a
   floored-perimeter strengthening of Oler would need. Primary kill-criterion.
4. **Consistency** of the floored-perimeter *conclusion* against every $s(n)$ the repo records as
   `cited`.
5. **The same conclusion against every best-known construction**, $n = 4$–$36$, taking
   Graham–Lubachevsky's $d(n)$ from `experiments/circle-packing-search/reference.py` (loaded, not
   retyped, so no digit can be mistranscribed; that tree is read-only to this experiment). Exact
   closed forms are used wherever the repo has one and a printed decimal is used only as a
   $\pm 1$ ulp enclosure — see the note the script prints, which is the reason for that care.
6. **The implication.** Exact rational arithmetic showing that this conclusion would imply the
   full Erdős–Oler conjecture.

## Results

See [`out/report.txt`](out/report.txt) for the transcript, and the attack write-up for what any
of it means. In one line each: the controls pass exactly; the slack of the *hull* bound is
exactly zero for every lattice and lattice-minus-apex configuration in the repo, so all of the
loss there is the hull → triangle relaxation; and the face-excess-nonnegativity hypothesis is
**refuted**, exactly, with a deficit that grows without bound.
