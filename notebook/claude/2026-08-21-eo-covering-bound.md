# 2026-08-21 — W2 (Refuter): attacking the covering route from below

Worker W2 on branch `claude/circle-equklatetal-problem-sa7tx7`. Job: kill the covering route to
Erdős–Oler $k=7$ by proving $N^*(a)\ge27$ for $a<6$, or fail and say how close I got.

**Outcome: failed to kill. Floor 25, need 27, gap exactly 2.** Write-up in
`problems/circle-packing-equilateral-triangle/attacks/eo-covering-bound/`.

## What moved

- 20 → **21** by an argument with no search behind it: a piece containing a $60°$ corner lies in
  $B(V,1)$, so its trace on $T_a$ is at most the $\pi/6$ sector, and the three corners are in three
  distinct pieces. Uniform in $a$ over $[5.9,6]$.
- 21 → **25** by exhibiting 25 points at pairwise distance $\ge1$ in $T_a$, $a=5.9833670<6$, as
  exact rationals. Also 22, 23, 24 at smaller $a$.

## The three things I want to remember

**1. Triangular coordinates make this problem rational.** Writing a point as $(u,v)$ for the
Cartesian $(u+v/2,\ v\sqrt3/2)$ turns $T_a$ into $\{u,v\ge0,\ u+v\le a\}$ and the squared distance
into $\Delta u^2+\Delta u\Delta v+\Delta v^2$. No $\mathbb{Q}(\sqrt3)$, no sign tests on surds —
every containment and every distance is a comparison of fractions. `packing-eo-small-cases` built
exact $\mathbb{Q}(\sqrt3)$ machinery for the same job; this is cheaper and I would reach for it
first next time.

**2. The separated-point bound has a ceiling of 26 and I should have said so out loud sooner.**
It reads as the sharp tool — and it is, up to a point — but $m\le26$ for $a<6$ *is* Erdős–Oler at
$k=7$. So the method cannot kill the route however well it is run; a 27th point would refute the
conjecture, not prove it. I wrote that into K2 before computing, which is the only reason I did not
spend the whole session grinding on $n=26$. The kill can only come from a bound that **exceeds** the
largest separated set, i.e. a chromatic-vs-clique gap. Worth generalising: whenever a lower-bound
method's optimum equals the quantity being conjectured, the method is a measuring instrument, not a
proof technique.

**3. The re-check failed first, and it was the re-check that was wrong.** My cartesian
cross-verification rejected all four certificates on the "left edge" test. Cause: I compared $y$
against $\sqrt3 x$ using an interval for $\sqrt3$ on both sides of an identity in which $\sqrt3$
cancels ($\sqrt3x-y=\sqrt3u$), so every point genuinely *on* that edge failed by the width of the
enclosure. Fixed by squaring the half-plane conditions. Two notes: interval arithmetic applied to
an identity manufactures false negatives, and this one failed safe — a spurious rejection, never a
spurious acceptance. Worth keeping the failure direction in mind when choosing how to round.

## Where the search died, and why it is not evidence

$n=26$ is the value that would make the covering requirement exactly tight, and I did not get it.
Every lattice-derived start relaxed to exactly $a=6$: the side-6 lattice is rigid because each edge
carries 7 points spanning length 6, and deleting two points — even a corner, which breaks two edges
at once — does not free it. That is consistent with the two proven cases: the optimal
$\Delta(k)-2$ configuration is a rearrangement, not a truncated lattice ($a_8=1+\sqrt{33}/3$,
$a_{13}\approx3.9712$). Extrapolating $3-a_8\approx0.085$ and $4-a_{13}\approx0.029$ suggests
$6-a_{26}\sim3\times10^{-3}$, so the search had to find a global rearrangement worth a few parts in
a thousand. Mine did not. **My search failing is not evidence that $a_{26}=6$**, and I have written
that into the attack file so nobody reads it that way later.

The cheapest fix is not an idea: Graham–Lubachevsky almost certainly tabulate a 26-point packing,
and re-verifying their *construction* here is not circular (a construction is self-certifying —
what would be circular is using a published *optimal value* $a_{26}$ as a bound). Network egress is
blocked this session, as `eo-literature` already found.

## The tool that could actually kill it, and the shape of its failure

$N^*(a)\ge m+\chi(G_Z)$, where $Z$ is the region free of a separated set $P$ and $G_Z$ joins points
at distance $\ge1$. This beats the separated-point bound exactly when $\chi(G_Z)>\alpha(G_Z)$, and
such gaps exist — five points in pentagram position on a circle of radius $\approx0.6$ give
$C_5$, with $\alpha=2,\chi=3$. So a 24-point configuration whose free region contains an odd cycle
gives $N^*\ge27$ outright, while implying nothing about Erdős–Oler.

I searched 201 configurations (1 full, 25 single deletions, 175 double deletions off the $n=25$
certificate). No gap. The freed regions were not merely bipartite but **edgeless** — deleting points
from a saturated configuration leaves a hole of diameter $<1$. The tension is structural: a gap
needs $Z$ large *and* awkward, but deleting from a tight $P$ makes $Z$ small, while a loose $P$
makes $\alpha(G_Z)$ grow alongside $\chi$. The regime that would work is a $P$ that is locally
maximal but globally poor — every point jammed, the whole configuration far from optimal, one large
connected cavity. I could not think of a way to search for that directly, and that is the honest
open end of this attack.

## Discipline notes

- K1–K4 were written before any computation and all four were evaluated; K1, K3, K4 met, K2 not
  reached. I stopped at the floor rather than re-scoping into constructing coverings (W1's lane).
- The $n=27$ run was a deliberate control. One mid-run float configuration read as 27 separated
  points at $a=5.99998$ — i.e. as a refutation of Erdős–Oler. It is $2\times10^{-5}$ of float noise
  on the side-6 lattice and the exact verifier rejects it. This is why the certificate pipeline
  never divides by the search margin.
- No literature value of $a_n$, $s(n)$ or $d(n)$ is an input to any bound in the attack. Given
  `FINDINGS.md`'s entry on a `cited` input containing the conclusion, that guard was written into
  the kill-criterion file before anything ran.
