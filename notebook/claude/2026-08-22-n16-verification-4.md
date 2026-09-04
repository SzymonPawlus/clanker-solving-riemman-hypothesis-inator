# 2026-08-22 — V4, verification of `n16-structure` (Theorem N)

Issue #97, branch `claude/circle-packing-subagents-9yg5gt`. Role: verification (repo `RULES.md` §8,
convergent). Author under review: the campaign manager, Claude Opus 5, same family as me — so the
most this can be is an independent same-family reconstruction, and I said so in the deliverable
before saying anything else.

## What I did

Wrote my own $\mathbb{Q}(\sqrt3)$ layer, my own exact convex geometry (hull, half-plane clipping,
residue subtraction), and my own transcription of the 15 polygons from `n16-covering-2`'s printed
table. Never opened `experiments/packing-n16-structure/` except to `grep` it for the string
`Borsuk`. 61 exact checks, all pass, under 2 s.

Order of work: re-derived the five lemmas on paper first, *then* wrote code to confirm the
constants. That ordering mattered — the algebra told me where to look, and two of the three findings
are about sentences, not numbers.

## What I found

**Theorem N is correct.** Every lemma reconstructs. Lemma 3's constant $2/\sqrt3$ is right and the
minimisation is an exact identity ($\alpha^2+\beta^2-\alpha\beta = \frac34\alpha^2 +
(\beta-\frac\alpha2)^2$), the quantifier really does extend to every trace point (though the
write-up's stated reason for it is not the reason), $\delta = a-2\sqrt3$ survives two independent
derivations, Viviani's direction is right, the $d\ge4$ branch is plain pigeonhole with no Borsuk
residue anywhere in the lane, and floor-plus-one is right including at the one threshold where it
actually bites ($a = 3+4/\sqrt3$). §4's twelve predictions all reproduce from my own transcription
and my own checker.

**The headline corollary is false.** "$1+2\sqrt3$ is the least $a$ at which fifteen pieces are
necessary" — the 15-point unit triangular lattice sits inside $T_4$, each piece of diameter $<1$
holds at most one of its points, so 15 pieces are necessary for every $a\ge4$. That is $0.46$ below
the claimed threshold, and it makes Theorem N 5 pieces slack at $a=4$. So the coincidence of two
constants remains a coincidence: the searches converge on $A_{15} = \sup\{a$ coverable$\}$, and
Theorem N bounds $\min\{a: N(a)\ge15\}$, which is a different quantity.

**§5.1's retraction does not hold.** Its arithmetic reproduces to the digit; the inference doesn't.
Lemma S maximises over $(k_1,k_2,k_3)$ because it only knows $k_e\ge3$; Theorem N pins $3/9/3$.
Hold $f$ fixed and Lemma S degenerates to U1 $=5.039166$ while Theorem N gives $4.920766$.

## What I want to remember

The two errors are the same error, and it is the one `FINDINGS.md` logged yesterday: a correct
theorem read one step too broadly. "Theorem N forces 15 at $1+2\sqrt3$" → "15 are necessary at
$1+2\sqrt3$". "My budget reproduces U1" → "so the combination buys nothing". In both the qualifier
was present in the paragraph above and absent from the bolded sentence. **I should read the bolded
sentences first, not last** — they are where the quantifier goes missing, precisely because that is
where the author is compressing.

Second thing worth keeping: my first corruption test *passed*, and the test was wrong, not the
checker. I had moved a shared vertex outward, which grows the union and cannot break a covering. A
corruption suite proves nothing until each corruption is checked to be one.

Third: the strongest tool I used all session was the elementary one — 15 lattice points in a
triangle of side 4. I reached for it only at step 9, after an hour of exact arithmetic on the
author's own terms. Asking "what does the *truth* look like near this threshold" is cheaper than
checking a derivation line by line, and it is the question that actually found something.

## Left for someone else

- The combination §5.1 retired: Theorem N's forced $3/9/3$ fed into `n16-covering-limit`'s certified
  slab-LP $f$ at $\ell=(a-4/\sqrt3)/3$. My envelope estimate puts it near $4.88$ against U2's
  $4.914308$. Uncertified — I did not rerun that lane's LP.
- Whether the concave envelope $\hat f$ differs from $f$ on that interval. Both the author's row 2
  and my reproduction use $f$, so neither is a certified bound.
- `FINDINGS.md` carries the false headline and is human/manager-owned; I flagged it, I did not touch
  it.
