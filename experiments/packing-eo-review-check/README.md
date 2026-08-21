# `packing-eo-review-check` — independent re-check of the Oler-slack attack

**Claim kind: neither.** No bound on $s(n)$ is claimed here. This directory is a *review
artifact*: a second, independently written implementation used to cross-examine
[`problems/circle-packing-equilateral-triangle/attacks/oler-slack-analysis/`](../../problems/circle-packing-equilateral-triangle/attacks/oler-slack-analysis/)
and its code in [`../packing-oler-slack/`](../packing-oler-slack/). Status: `numerical`.
Nothing here is assumable (repo `RULES.md` §3).

- Reviewer: `claude` (Claude Opus 5), 2026-08-21. Findings write-up:
  [`../../problems/circle-packing-equilateral-triangle/attacks/eo-review-notes/README.md`](../../problems/circle-packing-equilateral-triangle/attacks/eo-review-notes/README.md)
- Reviewing my own agent's work, so per repo `RULES.md` §5 this **cannot** grant
  `verified:review` — that needs Codex. It is an adversarial same-family check, and it is
  labelled as one.

## Provenance — why a second implementation exists at all

The problem's [`RULES.md`](../../problems/circle-packing-equilateral-triangle/RULES.md) §3 says the
reviewer of a computational claim "writes a checker independently, from the problem statement — not
by reading, importing, or adapting the author's code", and that "a second agent running the first
agent's script verifies nothing except that the script is deterministic".

So: `../packing-oler-slack/{geometry,exact,run}.py` were **not opened** before `field.py`,
`triangulate.py` and `check.py` existed and ran. The only inputs used were

- the problem statement and conventions in the problem `README.md` / `RULES.md` §2,
- the *statements* (not the derivations, not the code) in the attack's `README.md`,
- the certificate JSONs in
  [`../../problems/circle-packing-equilateral-triangle/attacks/exact-algebraic-constructions/certificates/`](../../problems/circle-packing-equilateral-triangle/attacks/exact-algebraic-constructions/certificates/).

The two implementations share no line of code and differ in method: the author derives the face
count from Euler's formula, whereas `triangulate.py` **builds an actual triangulation** and counts
the triangles it produced, so $F = 2n-b-2$ is an output here rather than an input.

## Reproducing

```bash
cd experiments/packing-eo-review-check && python3 check.py
```

Python 3.11, standard library only (`fractions`, `math`, `json`, `re`). No seeds, no randomness,
no floating-point decision anywhere. Runtime ≈ 40 s. Saved transcript:
[`out/review-check.txt`](out/review-check.txt).

## Arithmetic

`field.py` implements $\mathbb{Q}(\sqrt3,\sqrt{11})$ as a 4-dimensional $\mathbb{Q}$-vector space
with basis $(1,\sqrt3,\sqrt{11},\sqrt{33})$ — the field the certificates actually live in. Because
3, 11 and 33 are distinct squarefree integers the basis is $\mathbb{Q}$-linearly independent, so
an element is zero **iff** all four coordinates vanish. That is what makes `sign()` total: zero is
decided algebraically, and a nonzero value is separated from 0 by interval refinement that provably
terminates. Every orientation test, collinearity test and separation test in the hull code goes
through it.

Two useful consequences for this particular review:

- $2/\sqrt3 = \tfrac{2}{3}\sqrt3$ lies **inside** the field, so areas and the whole face excess are
  exact field elements, never intervals.
- Lengths are not. `Iv` is an outward-rounded rational interval type used for perimeters. Where a
  squared edge length happens to be a perfect square in the field, `exact_sqrt` recovers the exact
  length — which is what upgrades the "edge excess is exactly 0" finding from an enclosure to an
  identity on every lattice configuration.

**Normalisation.** Certificates use separation 2 (problem `RULES.md` §2); Oler's inequality and the
attack use separation 1. `load_cert` therefore halves every coordinate *and* halves
`point_triangle_side`. Getting this wrong scales the area by 4 and the perimeter by 2, so it would
be loud rather than subtle — but it is the single most likely place for two checkers to disagree,
and it is pinned here explicitly.

## What is checked

| | |
|---|---|
| **Certificates** | all $\binom n2$ squared separations $\ge 1$ after halving, exactly |
| **Claim 1 (identity)** | an explicit triangulation with vertex set exactly $E$ is *constructed* for each of the 12 non-degenerate certificates; its triangle count is compared with $2n-b-2$, its per-face excess summed and compared with $\frac{2}{\sqrt3}A-\frac F2$, and both sides of the identity compared |
| **Claim 2 (atlas)** | $b$, $i$, $F$, face excess, edge excess, stage 1, stage 2 and the total recomputed from coordinates; stage 1 + stage 2 = total asserted; exact-zero tested exactly |
| **Claim 3 (refutation of H)** | the 3-point witness and the flat-arc family recomputed, including their separations |
| **Claim 4 (FP ⇒ Erdős–Oler)** | the implication re-derived symbolically over $\mathbb{Q}$ for $3\le k\le 20$, asserting the supremum is exactly $T(k)-\tfrac32$ |
| **bonus** | closed forms for $T(k)$ and $T(k)-1$ checked for $3\le k\le 12$, showing stage 1 = 0 and stage 2 = 1 are not special to $k\le6$ |

Known-answer controls, run first in effect: the triangular cases $n = 3, 6, 10, 15, 21$ must give
exactly zero on every column (repo `RULES.md` §6, "validate on a tiny instance first"). They do.

## Result

Every published number reproduces. No disagreement was found. Details, including two places where
the write-up understates what it has, are in the findings file linked above.

## Limitations

- `triangulate.py` builds **one** triangulation per configuration by ear-clipping the boundary
  cycle and then inserting interior points. It does not enumerate all triangulations. The
  triangulation-independence of the totals is an argument, not something searched over here — but
  since the constructed triangulation is an arbitrary one and its face-excess sum matches the
  closed form exactly, the argument is at least exercised.
- Lengths for $n = 7$ and $n = 8$ are genuine intervals (the perimeters are irrational and not in
  the field). Widths are below $10^{-38}$; every *decision* in this file is still exact, because
  no conclusion depends on comparing those intervals against anything.
- This checks the attack's arithmetic and its two derivations. It does not check the literature
  question the attack flags in its §6 (whether the identity and Conjecture FP are already known);
  scholarly hosts are blocked at this session's egress proxy, exactly as the attack reports.
