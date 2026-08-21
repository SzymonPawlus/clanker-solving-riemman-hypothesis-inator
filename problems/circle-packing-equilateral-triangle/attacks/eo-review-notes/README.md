# Review notes: adversarial re-check of `oler-slack-analysis`

**Claim type: neither.** No bound on $s(n)$ is asserted or relied on here. This file records a
review, not a result.

- Target: [`../oler-slack-analysis/README.md`](../oler-slack-analysis/README.md) and
  [`experiments/packing-oler-slack/`](../../../../experiments/packing-oler-slack/), issue
  [#78](https://github.com/SzymonPawlus/clanker-solving-riemman-hypothesis-inator/issues/78)
- Reviewer: `claude` (Claude Opus 5), 2026-08-21 — reviewer role
- Independent checker written for this review:
  [`experiments/packing-eo-review-check/`](../../../../experiments/packing-eo-review-check/);
  transcript
  [`out/review-check.txt`](../../../../experiments/packing-eo-review-check/out/review-check.txt)

> ## Status this review can and cannot grant
>
> The attack's author is `claude`, and so am I. Repo [`RULES.md`](../../../../RULES.md) §5 is
> explicit that `verified:review` requires **a different model family**, and that "a model checking
> output from its own family is close to checking itself". **This review therefore grants nothing.**
> Every status in the attack stays exactly where its author put it: the identity `sketch`, the atlas
> `numerical`, the refutation `refuted`, Conjecture FP a bare conjecture. If the identity is ever to
> be built on, Codex has to examine it.
>
> What this *is*: a second, independently written implementation and a second derivation, run
> adversarially, as the problem's [`RULES.md`](../RULES.md) §3 asks of any computational claim. It
> is worth something — it would have caught an arithmetic error, a normalisation error or a wrong
> hull count — and it is worth strictly less than cross-family examination.

## Summary

| # | Claim | Verdict |
|---|---|---|
| 1 | the decomposition identity | **confirmed** — re-derived independently, and checked against a *constructed* triangulation on all 12 non-degenerate certificates |
| 2 | the slack atlas; stage 1 exactly 0 and stage 2 exactly 1 on lattice / lattice-minus-apex | **confirmed** — every published column reproduces; and it is *exact*, not enclosed |
| 3 | refutation of face-excess nonnegativity (H) | **confirmed** — trivially, and the unbounded family reproduces to 7 d.p. |
| 4 | FP ⇒ Erdős–Oler | **confirmed** — re-derived from scratch, same landing point, $\sup = T(k)-\tfrac32$ exactly |

**No disagreement was found anywhere.** Two places where the write-up *understates* what it has are
in §5 and §6 below; one is a claim that can be promoted from `numerical` to a two-line proof, the
other closes off a repair the write-up leaves open.

Method note: the checker shares no code with the author's. It was written before
`packing-oler-slack/geometry.py` was opened. The two differ in approach — the author derives
$F$ from Euler's formula and fans the strict hull vertices; mine *builds* a triangulation by
ear-clipping the full boundary cycle and reports the triangle count as an output, so $F = 2n-b-2$
is a prediction being tested rather than an assumption being used.

## 1. Claim 1 — the identity. Confirmed.

Restated in my own words: for finite non-collinear $E$ with $|E| = n$, $P = \operatorname{conv}E$,
$b$ points of $E$ on $\partial P$, and **any** triangulation $\mathcal T$ of $P$ with vertex set
exactly $E$,
$$\tfrac{2}{\sqrt3}A(P)+\tfrac12 M(P)+1-n=\sum_{f}\tfrac{2}{\sqrt3}\bigl(A_f-\tfrac{\sqrt3}{4}\bigr)+\sum_{e\subset\partial P}\tfrac12(\ell_e-1).$$

Re-derived without reading the write-up's proof, and I land in the same place. Expanding the right
side gives $\frac{2}{\sqrt3}A - \frac F2 + \frac12 M - \frac b2$, which equals the left side iff
$F = 2n-b-2$. So the identity **is** the face count, and everything else in it is bookkeeping.

**The face-count step, which the write-up flags as the thing to review hardest.** It is right.
Counting triangle sides, each interior edge is shared and each boundary edge is not, so
$3F = 2E_{\text{int}} + E_{\text{bd}} = 2E - E_{\text{bd}}$; Euler on $V-E+(F+1)=2$ with $V=n$ then
gives $F = 2n - E_{\text{bd}} - 2$. This is the classical $2i+b-2$ with $i = n-b$.

**Where the write-up's proof is thin — presentational, not an error.** The step it actually flags is
not the step that carries the weight. The whole derivation reduces to
$$E_{\text{bd}} = b,$$
i.e. *the number of boundary edges of $\mathcal T$ equals the number of points of $E$ on $\partial P$*,
and that equation is never stated, only used (it appears as the bare symbol $b$ inside
"$3F = 2|E_{\text{edges}}| - b$"). It is true, and for a reason worth one sentence: $P$ is convex,
so $\partial P$ is a single cycle; every point of $E$ on $\partial P$ is a vertex of $\mathcal T$
by hypothesis; and no boundary edge can skip a point $p$ lying in the relative interior of a hull
edge $[u,w]$, because $\{u,w\}$ as an edge would contain the vertex $p$ in its interior, which no
simplicial complex permits. Hence the cycle has exactly $b$ vertices and $b$ edges.

That is exactly the point where a reader who takes $b$ to mean "hull vertices" gets a different
answer. The write-up *defines* $b$ correctly ("hull vertices **and** points lying inside a hull
edge") and never slips, but a proof whose load-bearing step is unstated is one bad reading away
from being wrong. **Recommend adding that sentence**, and it is the only change I would ask for in
§1.

**Empirical confirmation.** The gap matters in practice: 6 of the 12 certificates have points
interior to a hull edge. On the $T(4)$ lattice, $n = 10$, there are 3 strict hull vertices and 6
edge-interior points. Using the correct $b = 9$ gives $F = 9$; using "hull vertices" $b = 3$ would
give $F = 15$. My triangulator **built 9 triangles**. Across all 12 configurations the constructed
triangle count matched $2n-b-2$ every time, and the summed per-face excess matched the closed form
$\frac{2}{\sqrt3}A-\frac F2$ *exactly in the field*, not merely to within an enclosure.

The two secondary properties also check out. Triangulation-independence is immediate once the totals
are $\frac{2}{\sqrt3}A(P)-\frac{2n-b-2}{2}$ and $\frac12(M(P)-b)$. And §2's "boundary-edge excess is
always $\ge 0$" is true for the stated reason and is genuinely trivial — boundary edges join
*distinct* points of $E$, so $\ell_e\ge1$ by hypothesis. Listing it alongside the face count as
"review hardest" over-weights it.

## 2. Claim 2 — the atlas. Confirmed, and exactly.

Recomputed $b$, $i$, $F$, face excess, edge excess, stage 1, stage 2 and the total from the
certificate coordinates, halved to Oler normalisation. Every one of the 12 rows reproduces the
published table to the printed 7 decimal places, and $\text{stage 1}+\text{stage 2}=\text{total}$
holds inside the enclosures for all of them. All certificates independently pass the separation
test ($\min_{p\ne q}d^2\ge1$ after halving).

The exactness claim survives a sharper test than the write-up applies. Face excess is an *exact*
field element throughout (because $2/\sqrt3 = \frac23\sqrt3$ stays in $\mathbb Q(\sqrt3,\sqrt{11})$),
and where every hull edge length is a perfect square in the field the perimeter is exact too. On all
nine lattice / lattice-minus-apex configurations:

| $n$ | 3 | 5 | 6 | 9 | 10 | 14 | 15 | 20 | 21 |
|---|---|---|---|---|---|---|---|---|---|
| face excess | $0$ | $0$ | $0$ | $0$ | $0$ | $0$ | $0$ | $0$ | $0$ |
| $M$ (exact) | 3 | 5 | 6 | 8 | 9 | 11 | 12 | 14 | 15 |
| $b$ | 3 | 5 | 6 | 8 | 9 | 11 | 12 | 14 | 15 |
| total | 0 | 1 | 0 | 1 | 0 | 1 | 0 | 1 | 0 |

$M = b$ **exactly**, so the edge excess is exactly $0$ and stage 1 is exactly $0$ — not "zero to
within $10^{-38}$". The four $T(k)-1$ cases have total exactly $1 \in \mathbb Q$, so stage 2 is
exactly 1. The finding is as sharp as advertised.

## 3. Claim 3 — H is false. Confirmed.

The witness needs nothing: $\{(0,0),(1,0),(2,\frac12)\}$ has squared separations $1,\frac54,\frac{17}4$,
one face of area $\frac14$, and $\mathrm{FE} = \frac{2}{\sqrt3}(\frac14-\frac{\sqrt3}4) =
\frac{\sqrt3}6-\frac12$, whose sign my exact sign test returns as $-1$. Oler's slack itself stays
positive ($0.3784685$), as claimed.

The flat-arc family reproduces exactly, including the separations, which are the part most likely to
be wrong in a family like this:

| $m$ | 3 | 4 | 6 | 8 | 12 | 16 |
|---|---|---|---|---|---|---|
| face excess | $-0.8289333$ | $-1.3195780$ | $-2.3128957$ | $-3.3105569$ | $-5.3088864$ | $-7.3083017$ |
| Oler slack | $0.1738065$ | $0.1816421$ | $0.1874793$ | $0.1896033$ | $0.1911615$ | $0.1917186$ |

all matching the published table, with $b = n$ confirmed for every one and $\min d^2 \ge 1$ verified
exactly rather than by eye. The kill-criterion in issue #78 is properly met and the write-up stops,
which is what §6.3 asks.

## 4. Claim 4 — FP ⇒ Erdős–Oler. Confirmed.

Derived independently. If $a<k-1$ then $\lfloor a\rfloor\le k-2$, so FP gives
$$n\;<\;\tfrac{(k-1)^2}{2}+\tfrac32(k-2)+1\;=\;\tfrac{k^2+k-5}{2}+1\;=\;T(k)-\tfrac32,$$
hence $n\le T(k)-2$ for integer $n$. So $T(k)-1$ points cannot fit below $a = k-1$; the lattice
$T(k)$ minus one point fits *at* $a = k-1$; therefore $s(T(k)-1)=s(T(k))$. Same landing point as the
write-up. Checked symbolically over $\mathbb Q$ for $3\le k\le20$, asserting the supremum is exactly
$T(k)-\frac32$ in every case — it is.

Two things I attacked and could not break:

- **Strictness.** The chain needs $a^2/2 < (k-1)^2/2$ strictly, which holds since $a<k-1$; the
  floor term is only $\le$. Fine.
- **The other side.** The argument needs $T(k)$ points to *not* fit below $a = k-1$ either, or the
  conclusion is not an equality. FP at integer $a$ *is* Oler, and Oler gives
  $(a+1)(a+2)\ge k(k+1)$, i.e. $a\ge k-1$. So FP alone suffices; no extra dependency is smuggled in.

Small-$a$ sanity: FP at $a=\tfrac12$ gives $n\le1$ (correct — two separated points do not fit),
at $a=1$ gives $n\le3=T(2)$ (tight), at $a=1.9$ gives $n\le4$ (correct, since $n=5$ needs $a=2$).

The write-up's §5.3 posture is right, and it is the right reading of `RULES.md` §7: FP implies an
open conjecture, so a short proof of FP is overwhelmingly likely to be a mistake, and FP should be
treated as a falsification target. Nothing downstream depends on FP, so this costs nothing.

## 5. Understatement 1 — claim 2 is a theorem, not a measurement

The write-up files "stage 1 = 0 at $T(k)$ and $T(k)-1$" as `numerical`, "checked for $k\le6$",
and lists "whether it holds for all $k$" under *not checked*. It holds for all $k$, by counting,
and the proof is two lines. In Oler normalisation the lattice $T(k)$ has side $a = k-1$ and
$$b=3(k-1),\quad A=\tfrac{\sqrt3}{4}(k-1)^2,\quad M=3(k-1),$$
so $\mathrm{FE}=\frac{(k-1)^2}{2}-\frac{2T(k)-3(k-1)-2}{2}=0$ and $\mathrm{BE}=\frac{M-b}{2}=0$.
Deleting the apex turns the hull into a trapezoid with
$$b=3(k-1)-1,\quad A=\tfrac{\sqrt3}{4}\bigl((k-1)^2-1\bigr),\quad M=(k-1)+2(k-2)+1=3(k-1)-1=b,$$
so again $\mathrm{FE}=\mathrm{BE}=0$, and the total
$\frac{(k-1)^2}{2}+\frac32(k-1)+1-(T(k)-1)$ is identically $1$. Verified symbolically over
$\mathbb Q$ for $3\le k\le12$ in the checker; the algebra above is general.

So the sentence "the deficit is exactly 1, for every $k=3,4,5,6$ checked" can be "for every $k$",
and the *interpretation* the write-up draws from it — that at $n=T(k)-1$ the loss is entirely the
hull → triangle relaxation — becomes a statement about the whole family rather than four data
points. That strengthens the attack's most useful output. It does not change any status: it is
still elementary, still uncited, still `sketch` until Codex looks at it.

## 6. Understatement 2 — step (ii) of the dead route is not merely unjustified, it is unrepairable

The write-up refutes H (step (i)) and separately notes that step (ii), $b\le3\lfloor a\rfloor$, "is
separately unjustified" because a hull vertex may sit strictly inside $T$. Correct. But the
situation is worse than "unjustified", and saying so closes the route properly rather than leaving a
repair dangling for the next reader.

The bound that *is* available is
$$b\;\le\;M(\operatorname{conv}E)\;\le\;M(T)\;=\;3a\quad\Longrightarrow\quad b\le\lfloor 3a\rfloor,$$
the first step because the $b$ boundary edges each have length $\ge1$, the second by monotonicity of
perimeter under inclusion of convex sets. And $\lfloor3a\rfloor\ge3\lfloor a\rfloor$ always, strictly
whenever the fractional part of $a$ is $\ge\frac13$ (at $a=3.5$: 10 versus 9). So the true bound is
**weaker** than the one step (ii) needs, in exactly the non-integer range where FP is supposed to
improve on Oler.

Worse, feeding the true bound into H gives $n\le\frac{a^2}{2}+\frac{3a}{2}+1$ — which is Oler again.
So even if H had been true, H plus the only boundary bound actually available would have re-derived
Oler and nothing more. The route does not fail "twice over" in the sense of two independent patches
being needed; its second failure is structural. **Recommend saying that in §4**, since a reader who
repairs H would otherwise try step (ii) next.

## 7. Nothing else to report

Things I attacked and found sound: the halving convention (a factor-4 area error would have been
loud in every row, and was not there); the exclusion of $n=1,2$ as degenerate; the internal
consistency of §3 with §5.2 — the $n=8$ FP margin $0.2482$ is *the same number* as the $n=8$ face
excess, which is not a coincidence but the case $b = 6 = 3\lfloor a\rfloor$ with stage 2 $=0$, and it
being equal is evidence both sections were computed correctly; the identification of
$\{8,13,19,26,34\}$ as $T(k)-2$ (and the correct exclusion of the $n=12$ row from that family); and
the write-up's own §6 honesty note about the Graham–Lubachevsky printed decimals, which is the
right diagnosis of a real trap.

**not-checked.** The literature question — whether the identity or FP are known (Folkman–Graham,
Groemer, Melissen). Scholarly egress is blocked in my session too, so the attack's "assume both are
known until someone with library access says otherwise" stands unchallenged and unconfirmed. Also
not checked: §5.2's sweep over the 28 best-known constructions, which depends on
`experiments/circle-packing-search/reference.py`; I re-derived the implication FP ⇒ Erdős–Oler but
did not re-verify that table of published values.
