# Attack: a class-counting theorem for coverings — with its headline corollary **refuted**

> ## CORRECTION, 2026-08-22, after review by worker V4
>
> **This file's original headline was false and is withdrawn.** It claimed that $1+2\sqrt3$ is *the
> least $a$ at which fifteen pieces are necessary*, and therefore that it explained the plateau
> four searches had hit. It is not, and it does not.
>
> The 15-point unit triangular lattice (5 per side) lies in $T_4$ with all pairwise distances
> $\ge 1$ — this is just $a_{15} = 4$, which is `cited`. A piece of diameter $<1$ holds at most one
> of those 15 points, so **fifteen pieces are necessary for every $a \ge 4$**, which is $0.4641$
> below the claimed threshold. Theorem N forces only $10$ at $a = 4$, where the truth is $\ge 15$:
> it is five pieces slack there, and its arriving at 15 exactly at $1+2\sqrt3$ is a **coincidence,
> not an explanation**.
>
> The two quantities were conflated. The plateau is about
> $A_{15} = \sup\{a : T_a \text{ is coverable by } 15 \text{ pieces}\}$; Theorem N bounds
> $\min\{a : N(a) \ge 15\}$. Different quantities, and the second says nothing about the first.
>
> **What survives, and it is the useful half:** Theorem N and its four lemmas were reconstructed
> step by step by V4 and confirmed unchanged (§2), and so is the **class structure** they give — for
> $a \ge 1+2\sqrt3$ every covering has at least 3 two-side, 9 one-side and 3 no-side pieces, so a
> 15-piece covering has *exactly* those (§3.1). That is the rigorous replacement for the disputed
> "forced $3+9+3$" claim, and it is what feeds the area budget in §5.1.
>
> Also corrected by the same review: **§5.1's retraction was itself wrong** and the lead it retired
> is live again. See §5.1.
>
> `FINDINGS.md` carried the false headline and has been amended.


**Claim type: NEITHER of the two in problem [`../../RULES.md`](../../RULES.md) §1.** No bound on
$s(16)$ or $a_{16}$ is asserted here, in either direction. What is proved is a statement about
*coverings* — how many pieces of diameter $<1$ a triangle needs, and how they must be arranged.
That constrains the method the campaign's record is built on; it does not move the record. Nothing
enters `results/`.

- Author: `claude` (manager, Claude Opus 5 — convergent role, repo
  [`RULES.md`](../../../../RULES.md) §8: this is a proof plus exact calculation), 2026-08-22
- Issue [#97](https://github.com/SzymonPawlus/clanker-solving-riemman-hypothesis-inator/issues/97),
  branch `claude/circle-packing-subagents-9yg5gt`
- Code: [`experiments/packing-n16-structure/`](../../../../experiments/packing-n16-structure/) —
  Python standard library only, exact $\mathbb{Q}(\sqrt3)$ arithmetic in every decision, no seeds,
  no network, runs in under a second

**No kill-criterion file**, and that is deliberate rather than an omission: this lane ran no search
and had nothing to abandon. The theorem was derived first and checked afterwards, which is the
honest order and is stated here so a reviewer can weigh it.

| assertion | status |
|---|---|
| §2 Theorem N (the counting theorem) and its four lemmas | `sketch` — mine, elementary, unreviewed, **not assumable, including by me** |
| §3 the identity $\delta = a - 2\sqrt3 = 1 \iff a = 1+2\sqrt3$ | `sketch` — true, but the **corollary drawn from it is `refuted`**, see the correction above |
| §3.1 the class structure ($\ge 3$ / $\ge 9$ / $\ge 3$, hence exactly $3/9/3$ at 15 pieces) | `sketch` — mine; **this is the part that survives and is used** |
| §4 exact verification against the standing certificate | `numerical` — exact rational/$\mathbb{Q}(\sqrt3)$ computation on one explicit object |
| §5 the counting ceiling $3\sqrt3$ | `sketch` — mine |
| §6 adjudication of the V3/R1 disagreement | `sketch` — mine, with an exact witness |
| the standing record $a_{16}\ge1+2\sqrt3$ | `sketch` — [`../n16-covering-2/`](../n16-covering-2/), unchanged by anything here |

---

## 1. The question this answers

Three independent search methods — a sequential-LP minimax solver, a Tutte-embedding beam search
over 663 single-flip and 3334 depth-two structural neighbours, and a pattern search over thousands
of explicit site layouts — all converge on the same covering side length, $a = 1+2\sqrt3$
([`../n16-covering-2/`](../n16-covering-2/)). A fourth lane's float descent reproduces it again
([`../n16-covering-max/`](../n16-covering-max/) §2). The campaign has recorded that plateau four
times and never explained it.

**I believed I had explained it, and I had not — see the correction at the top of this file.**
$1+2\sqrt3$ is where *Theorem N's counting* first reaches fifteen, but fifteen pieces are already
necessary from $a = 4$ by a much cheaper argument ($a_{15} = 4$, `cited`), so the coincidence
explains nothing. **The plateau remains unexplained.** What §2 does deliver is the class structure
of §3.1, which is a real repair of a claim two audits had flagged, and which §5.1 now shows is
worth something quantitative.

## 2. Theorem N — a lower bound on the number of pieces, by class

Throughout: separation $1$; $T_a$ is the closed equilateral triangle of side $a$; a **piece** is a
set of diameter **strictly** $<1$ (strictness is load-bearing throughout this problem — separation
is non-strict, so a piece of diameter exactly $1$ may contain two admissible points). Suppose
$T_a = \bigcup_i S_i$ with every $\operatorname{diam} S_i < 1$. Classify each piece by **how many
of the three sides of $T_a$ it meets** — $0$, $1$, $2$ or $3$. The classes are disjoint by
construction, so their lower bounds add. That is the whole trick.

**Lemma 1 (reach).** *A piece meeting a side lies strictly within distance $1$ of that side.*
If $q \in S_i \cap e$ then every $x\in S_i$ has $\operatorname{dist}(x,e)\le|xq|\le\operatorname{diam}S_i<1$.

**Lemma 2 (no piece meets three sides, for $a > 4/\sqrt3$).** Suppose $S_i$ meets all three sides,
at $p_1\in AB$, $p_2\in AC$, $p_3\in BC$. By Lemma 1's computation the three distances from $p_1$
to the sides are $0$, $\le|p_1p_2|<1$ and $\le|p_1p_3|<1$, summing to $<2$. Viviani's theorem says
that sum is the height $a\sqrt3/2$ for *every* point of $T_a$. So $a\sqrt3/2<2$, i.e.
$a<4/\sqrt3 = 2.3094\ldots$ — false in our range.

**Lemma 3 (corner reach $2/\sqrt3$).** *If $S_i$ meets two sides, at distances $\alpha$ and $\beta$
from their common apex, then $\alpha<2/\sqrt3$ and $\beta<2/\sqrt3$.* The angle at the apex is
$60^\circ$, so the two footpoints are $\sqrt{\alpha^2+\beta^2-\alpha\beta}$ apart, and this is
$<1$. Minimising $\alpha^2+\beta^2-\alpha\beta$ over $\beta$ gives $\beta=\alpha/2$ and value
$3\alpha^2/4$; hence $3\alpha^2/4<1$, i.e. $\alpha<2/\sqrt3 = 1.1547\ldots$, and symmetrically for
$\beta$. This holds for *every* point of the trace, since the bound was derived from an arbitrary
pair.

**Lemma 4 (the deep triangle).** *Let $D$ be the set of points of $T_a$ at distance $\ge1$ from all
three sides. Then $D$ is an equilateral triangle of side $\delta = a-2\sqrt3$, and every piece
meeting $D$ meets no side of $T_a$.* The first part is the standard inner-parallel triangle (each
side moves in by $1$, shortening the side by $2/\tan 30^\circ = 2\sqrt3$); the second is Lemma 1
contrapositive.

> **Theorem N.** For $a > 4/\sqrt3$, writing $c$, $b$, $d$ for the number of pieces meeting two
> sides, exactly one side, and no side:
> $$c \ \ge\ 3, \qquad b \ \ge\ 3\bigl(\lfloor a - 4/\sqrt3\rfloor + 1\bigr), \qquad
> d \ \ge\ \begin{cases} 3 & \text{if } \delta = a-2\sqrt3 \ \ge\ 1,\\ 4 & \text{if } \delta \ \ge\ \sqrt3,\end{cases}$$
> and the total number of pieces is at least $c+b+d$.

*Proof.* **$c\ge3$:** each apex of $T_a$ lies in some piece, and that piece meets the two sides
through the apex; the three pieces are distinct because the apexes are pairwise $a>1$ apart while
each piece has diameter $<1$.
**$b\ge\ldots$:** fix a side $e$ and let $M_e\subseteq e$ be the closed middle segment obtained by
deleting the open intervals of length $2/\sqrt3$ at each end; $|M_e| = a-4/\sqrt3$. No piece meeting
no side meets $e$; no piece meeting a *different* side meets $e$; and by Lemma 3 no two-side piece
has any trace point in $M_e$. So $M_e$ is covered by the traces of one-side pieces meeting $e$.
Each such trace has diameter $<1$, hence lies in an interval of length $<1$, so their lengths sum to
more than $|M_e|$ and their number is at least $\lfloor|M_e|\rfloor+1$. (Floor-plus-one, **not**
ceiling: at integer $|M_e|$ the ceiling is one too few, because each interval is strictly shorter
than $1$.) One-side pieces meeting different sides are distinct, so the three sides contribute
disjointly.
**$d\ge\ldots$:** by Lemma 4 the pieces covering $D$ meet no side. $D$'s three apexes are pairwise
$\delta$ apart, so if $\delta\ge1$ no piece contains two of them and three pieces are needed. If
moreover $\delta\ge\sqrt3$, add $D$'s centroid: it is at distance $\delta/\sqrt3\ge1$ from each
apex, giving four points pairwise $\ge1$ apart and forcing a fourth piece. $\square$

Note what the last step does **not** use: it needs only that $\delta/\sqrt3$ is the apex-to-centroid
distance. It does not assume that the $\delta/\sqrt3$ partition of $T_\delta$ is optimal, so no
Borsuk-type input is required.

## 3. The threshold identity — what $1+2\sqrt3$ is

$$\delta \ =\ a - 2\sqrt3 \ =\ 1 \qquad\Longleftrightarrow\qquad a \ =\ 1 + 2\sqrt3 .$$

The identity is correct; **the conclusion originally drawn from it is not** (see the correction at
the top). Below $1+2\sqrt3$ the deep triangle has side $<1$ and one piece can swallow it, so
Theorem N forces only $3+9+1 = 13$. At $a = 1+2\sqrt3$ the deep triangle's side reaches exactly
$1$, its three apexes become mutually unswallowable, and Theorem N's forced total jumps by two to
$3+9+3 = 15$.

**But Theorem N is not the binding constraint here.** The cheap bound $N(a) \ge \omega(a)$ — a
piece of diameter $<1$ holds at most one of any set of points at pairwise distance $\ge 1$ —
already gives $N(a) \ge 15$ for all $a \ge a_{15} = 4$, and dominates the table below throughout.
The table records what *this argument* forces, which is strictly less:

| $a$ | | corner | edge | deep | **forced total** | $\delta = a-2\sqrt3$ |
|---|---:|---:|---:|---:|---:|---:|
| $4.30$ | | 3 | 6 | 1 | 10 | $+0.8359$ |
| $1+2\sqrt3-\tfrac1{100}$ | $4.454102$ | 3 | 9 | 1 | 13 | $+0.9900$ |
| $\mathbf{1+2\sqrt3}$ | $\mathbf{4.464102}$ | 3 | 9 | 3 | **15** | $\mathbf{+1.0000}$ |
| $1+2\sqrt3+\tfrac1{100}$ | $4.474102$ | 3 | 9 | 3 | 15 | $+1.0100$ |
| $4.62$ | | 3 | 9 | 3 | 15 | $+1.1559$ |
| $5$ | | 3 | 9 | 3 | 15 | $+1.5359$ |
| $3\sqrt3$ | $5.196152$ | 3 | 9 | 4 | 16 | $+1.7321$ |

### 3.1 What actually survives — the class structure

**Corollary.** For $a \ge 1+2\sqrt3$, if a covering of $T_a$ by diameter-$<1$ pieces uses exactly
$15$ pieces, then it has **exactly** $3$ two-side, $9$ one-side and $3$ no-side pieces, each side is
met by exactly $5$ pieces, and the three no-side pieces cover $D$.

This is the "$3$ corner $+$ $9$ edge $+$ $3$ interior" structure the campaign had been asserting
without a valid proof — see §6 for why the previous derivation failed and how Theorem N avoids it.
It is unaffected by the correction above, because it is a statement about the *composition* of a
15-piece covering, not about the least $a$ at which fifteen are needed. It is also the only part of
this file that anything downstream uses: §5.1 turns it into a quantitative gain in the area budget.

**What is not claimed, and what I claimed wrongly.** Nothing here says fifteen pieces first become
necessary at $1+2\sqrt3$; they are necessary from $a = 4$. Nothing here explains the plateau. The
plateau is about $A_{15}$, the largest $a$ that *is* coverable by 15 pieces, and this file bounds a
different quantity.

## 4. Exact verification against the standing certificate

The 15 polygons were transcribed **from the table printed in
[`../n16-covering-2/README.md`](../n16-covering-2/README.md)**, not from that lane's code, and
checked in exact $\mathbb{Q}(\sqrt3)$ (`structure.py`). Every prediction of §3 holds:

| predicted by Theorem N | found in the record |
|---|---|
| all pieces inside $T_a$ | ✔ |
| max squared diameter | exactly $1$ |
| two-side pieces $=3$ | ✔ (pieces 0, 4, 14) |
| one-side pieces $=9$ | ✔ (1, 2, 3, 5, 8, 9, 11, 12, 13) |
| no-side pieces $=3$ | ✔ (6, 7, 10) |
| three-side pieces $=0$ | ✔ |
| pieces meeting each side $=5$ | ✔, all three sides |
| $\delta = a-2\sqrt3 = 1$ exactly | ✔ |
| the 3 no-side pieces cover $D$ | ✔ (exact residue subtraction, no area identity) |
| no *single* piece covers $D$ | ✔ (control — must fail, and does) |
| two-side traces $<2/\sqrt3$ from the apex | ✔ (all six squared trace lengths exactly $1 < 4/3$) |

The coverage check is by direct residue subtraction — repeatedly clip the residual regions by each
piece's edge half-planes and keep the outside parts — so it assumes no disjointness and uses no
area identity, and therefore survives overlapping pieces. It was smoke-tested first on a square cut
by two triangles (covered) and by one (not covered), and the $\mathbb{Q}(\sqrt3)$ sign routine was
tested on the mixed-sign cases $2-\sqrt3>0$, $1-\sqrt3<0$, $-3+2\sqrt3>0$, $-7+4\sqrt3<0$ where a
naive implementation fails.

## 5. The ceiling — and it is why this does not close the lane

Theorem N cannot force a sixteenth piece until **$a = 3\sqrt3 = 5.196152\ldots$** (where the deep
triangle admits four separated points) or $a = 3+4/\sqrt3 = 5.309401\ldots$ (where a side's middle
needs a fourth piece). Both are far above the best-known packing's $4.6247637$.

So this argument explains the plateau but **cannot break it**, and it says so in a checkable way:
between $1+2\sqrt3$ and $3\sqrt3$, fifteen pieces are necessary and counting has nothing further to
say about whether they are sufficient. Any proof that $A_{15} = 1+2\sqrt3$ must come from a tool
that is not piece-counting — an area or density argument (Lemma S in
[`../n16-covering-limit/`](../n16-covering-limit/), whose own ceiling is $4.836854$), or an
exhaustion over the now-forced $3+9+3$ structure.

### 5.1 I retracted this lead, and the retraction was wrong — it is live again

**First I claimed** that combining Theorem N's forced $3/9/3$ counts with Lemma S's area budget
would sharpen the ceiling on $A_{15}$. **Then I retracted it**, on the grounds that the budget
reproduces [`../n16-covering-limit/`](../n16-covering-limit/)'s published U1 $= 5.039166$ to six
decimals and therefore adds nothing. **Worker V4 refuted the retraction**, and it is right.

The arithmetic in both rows is fine — V4 reproduced $5.039165715$ and $4.920765783$ independently
by rational interval arithmetic. What was wrong was the inference:

- **Row 1 was never evidence of anything.** $3\cdot\tfrac\pi6 + 12\cdot\tfrac\pi4$ uses **no**
  class information that Lemma S lacked, so reproducing U1 from it is an arithmetic check on my own
  code, not an independent confirmation and not a demonstration that the counts are redundant.
- **Row 2's comparison was not like-for-like.** It set my weaker closed-form $f$ against that lane's
  certified slab-LP $f$ and read the difference as "no gain". The actual difference is elsewhere:
  **Lemma S knows only $k_e \ge 3$ and must therefore maximise its budget over every admissible
  $(k_1,k_2,k_3)$, while Theorem N pins them to $3/9/3$.** Held at the *same* capped closed-form
  $f$, Lemma S degenerates back to $5.039166$ where Theorem N gives $4.920766$ — a gain of
  $\mathbf{0.118}$, not zero. And what the forced counts delete is precisely the $k_e = 4$ branch,
  which `n16-covering-limit` itself describes as the branch that "decides everything" for its U2.

So the lead is **un-retired**, and it is now the sharpest thing this lane points at: feed the forced
$3/9/3$ into that lane's *certified* slab-LP $f$ at $\ell = (a-4/\sqrt3)/3$ and see whether it
beats its published U2 $= 4.914308$. V4's envelope estimate is $\approx 4.88$ — **uncertified**, it
did not rerun the LP — and if it holds it is the one place this round could move a published number
rather than a sentence. A worker is on it.

**Recorded in full rather than tidied**, because the sequence — propose, retract on a bad argument,
be corrected — is the substance. The retraction *felt* like rigour; withdrawing a claim usually
does. `FINDINGS.md` has the pattern.

## 6. The V3/R1 disagreement, adjudicated

[`../n16-verification-3/`](../n16-verification-3/) and [`../n16-redteam/`](../n16-redteam/) both
concluded that [`../n16-covering-2/`](../n16-covering-2/)'s forced-structure argument does not
prove its conclusion, **by incompatible routes**, and R1 reports that V3 certified as correct the
sub-step R1 breaks. Problem `RULES.md` §3 requires that a checker disagreement be investigated, not
averaged. Adjudication:

**R1 is right about where it first fails.** Its witness is admissible and I re-derived it exactly:
with $P=(21/20,\,0)$ on $AB$ and $Q=(1/4,\,\sqrt3/4)$ on $AC$, $|PQ|^2 = 331/400 < 1$, so a single
piece may contain both; $P$ is at distance $1.05>1$ from $A$ and $3.414\ldots>1$ from $B$, so $P$
lies in the *middle* of $AB$ as `n16-covering-2` defines it (distance $>1$ from both endpoints).
That is precisely what its $n_1\ge9$ step assumes cannot happen, and the step therefore fails.

**V3's objection is also a real gap, in a later step**, not the same one: the case split over $n_2$
never treats $n_2=4$ or $n_2=5$. Both audits are correct about their own step; neither is wrong.
The appearance of a contradiction comes from each describing the argument as failing "at" one
place.

**Both are repaired at once by Theorem N**, which never splits on $n_2$ and is immune to R1's
witness by construction: it defines the corner zone at $2/\sqrt3 = 1.1547$ rather than at $1$, and
R1's witness has $\alpha = 1.05 < 2/\sqrt3$, so it lies inside the corner zone and leaves the
middle $M_{AB}$ untouched. The $1$ in the original argument was the wrong constant; Lemma 3 gives
the right one.

## 7. What to review hardest

1. **Lemma 3's minimisation.** $\min_\beta(\alpha^2+\beta^2-\alpha\beta) = 3\alpha^2/4$ at
   $\beta=\alpha/2$ is the constant the whole theorem turns on, and getting it wrong is exactly the
   error the original argument made. Re-derive it.
2. **The floor-plus-one in Lemma/Theorem N's edge count.** At integer $|M_e|$ the ceiling is one too
   few. `min_intervals` handles it and is tested at $|M_e| = 1$ and $|M_e| = 3$ exactly; check the
   reasoning, not just the code.
3. **The disjointness of the three classes.** It is the step that lets the bounds add, and it is one
   sentence, which is where this repo's errors live.
4. **Lemma 4's inner-parallel side length** $\delta = a - 2\sqrt3$. The whole of §3 is this identity;
   a factor of $\sqrt3$ here would be the separation-1/separation-2 trap in new clothing.

## 8. Reproduce

```bash
python3 experiments/packing-n16-structure/structure.py
```

Under a second; exact $\mathbb{Q}(\sqrt3)$ in every decision; no floats decide anything (the
`approx()` method is used only to format the printed columns and to seed an integer search that is
then confirmed exactly).

## 9. What this is worth

`sketch`, and not assumable by anyone including me (`RULES.md` §3). Every checker on this lane is
Claude Opus 5; `RULES.md` §5 needs an examiner from a different model family, and problem
`RULES.md` §3 needs Codex to reimplement the check from the problem statement. **The record is
unchanged at $a_{16}\ge1+2\sqrt3$, i.e. $s(16)\ge2+6\sqrt3$.**

After correction, what this file buys is narrower than what it first claimed, and worth stating
exactly:

- **Delivered:** Theorem N and its four lemmas, reconstructed independently by V4 and confirmed; the
  class structure of §3.1, which is a rigorous replacement for a "forced $3+9+3$" claim that two
  audits had shown was not proved; the adjudication in §6; and — via §5.1 — a quantified reason to
  expect the forced counts to sharpen `n16-covering-limit`'s U2.
- **Withdrawn:** the claim that $1+2\sqrt3$ is the least $a$ at which fifteen pieces are necessary,
  and with it the claim to have explained the plateau. **The plateau is still unexplained.**
- **Withdrawn:** §5.1's retraction, which was wrong in the opposite direction.

Three assertions, two of them wrong, both caught by one reviewer in one pass. The theorem survived;
everything I built on top of it did not.
