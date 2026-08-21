# Attack: Oler slack localisation — where the slack lives, and one dead route

**Claim type: neither. No bound on $s(n)$ — upper or lower — is claimed anywhere in this file.**
Problem [`../../RULES.md`](../RULES.md) §1 asks for that sentence first, and here it is the literal
truth: this attack produces an *identity*, a *measurement*, and a *refutation*. Nothing enters
`results/`; nothing here is assumable, including by me (repo [`RULES.md`](../../../../RULES.md) §3).

- Issue: [#78](https://github.com/SzymonPawlus/clanker-solving-riemman-hypothesis-inator/issues/78)
- Code: [`experiments/packing-oler-slack/`](../../../../experiments/packing-oler-slack/) — one
  command, Python standard library only, exact arithmetic throughout
- Transcript: [`out/report.txt`](../../../../experiments/packing-oler-slack/out/report.txt)
- Author: `claude` (Claude Opus 5 — convergent role, `RULES.md` §8: this is checking and exact
  calculation, not ideation), 2026-08-21

| What | Status |
|---|---|
| §1 the decomposition identity | `sketch` — my derivation; elementary, and verified exactly on 15 configurations, but not cross-examined and **not assumable** |
| §3 the slack atlas numbers | `numerical` — exact computations about specific explicit configurations |
| §4 refutation of face-excess nonnegativity | `refuted` — the hypothesis is false; the witness is exact and needs nothing from §1 |
| §5 the floored-perimeter statement | **bare conjecture**, unproved and not to be attacked here; §5.3 says why |
| Oler's inequality itself | `cited` — Oler 1961, see [`../oler-lower-bound/`](../oler-lower-bound/) |

**Kill-criterion outcome, stated up front** (repo `RULES.md` §6.3):

> **Primary** (issue #78): *"if the face-excess-nonnegativity hypothesis is refuted by an explicit
> configuration verified in exact rational arithmetic, the local/discharging route to a
> floored-perimeter strengthening is dead. Stop there."*
>
> **MET — §4.** The hypothesis is false, by a three-point configuration in exact rational
> coordinates, and the deficit is unbounded. The route is dead and I stopped. §5 records what the
> route was *aiming* at, why it is not being pursued, and what it would imply — no re-scoping.
>
> **Secondary:** *"if the decomposition identity fails on any triangular control ($n = 3, 6, 10$
> must give exactly zero), the identity is wrong."* **Not met** — all three controls give exactly
> zero, with zero excess on every individual face and every boundary edge.

**What to review hardest**, if you are the cross-examiner: §1's face-count step ($F = 2n-b-2$)
and the claim in §2 that the boundary-edge excess is non-negative *always*. Everything downstream
of §2 is arithmetic.

---

## 1. The identity — `sketch`

Throughout, points are at minimum separation **1** (Oler's normalisation; the certificates in this
repo use separation 2, so the code halves every coordinate — see the experiment README).

Let $E$ be a finite, non-collinear point set, $P = \operatorname{conv}(E)$, $n = |E|$. Write $b$
for the number of points of $E$ on $\partial P$ — hull vertices *and* points lying inside a hull
edge — and $i = n - b$ for the rest. Let $\mathcal{T}$ be **any** triangulation of $P$ whose vertex
set is exactly $E$ (so every point is a corner of some triangle; no point is left over and no
extra point is introduced).

> **Identity.**
> $$\underbrace{\tfrac{2}{\sqrt3}A(P) + \tfrac12 M(P) + 1 - n}_{\text{Oler's slack}}
> \;=\; \sum_{f \in \mathcal{T}} \tfrac{2}{\sqrt3}\Bigl(A_f - \tfrac{\sqrt3}{4}\Bigr)
> \;+\; \sum_{e \subset \partial P} \tfrac12\bigl(\ell_e - 1\bigr),$$
> the second sum being over the $b$ boundary edges of $\mathcal{T}$.

Call the two sums the **face excess** and the **boundary-edge excess**. $\sqrt3/4$ is the area of
the unit equilateral triangle and $1$ is the minimum separation, so each term measures one cell's
departure from the extremal lattice cell.

**Proof.** Three ingredients.

1. **Face count: $F = 2n - b - 2$.** Euler for the planar subdivision: $V = n$, faces $F + 1$
   counting the outer one. Every triangle has three sides; interior edges are shared by two
   triangles and boundary edges by one, so $3F = 2\lvert E_{\text{edges}}\rvert - b$, giving
   $\lvert E_{\text{edges}}\rvert = (3F+b)/2$. Then $V - \lvert E_{\text{edges}}\rvert + (F+1) = 2$
   yields $n - F/2 - b/2 = 1$, i.e. $F = 2n - b - 2$.
2. **Areas: $\sum_f A_f = A(P)$**, since $\mathcal{T}$ tiles $P$.
3. **Boundary edge count: $\lvert E_{\text{bd}}\rvert = b$.** The boundary edges of
   $\mathcal{T}$ form a single cycle through the $b$ boundary points, so there are exactly $b$ of
   them. This is the step everything rests on and it is where a reader can silently diverge: if
   $b$ is read as "hull *vertices*" rather than "points of $E$ on $\partial P$", the count is
   wrong wherever a point lies inside a hull edge, and $F = 2n-b-2$ fails with it. (Flagged by an
   independent checker, which got $F = 15$ instead of $9$ on the $T(4)$ lattice under the wrong
   reading. Six of the twelve certificates exercise this case.)
4. **Lengths: $\sum_e \ell_e = M(P)$**, since those $b$ edges subdivide the hull edges, and
   subdividing a segment preserves total length.

Expand the right-hand side with these:
$$\tfrac{2}{\sqrt3}A(P) - \tfrac{F}{2} + \tfrac12 M(P) - \tfrac{b}{2}
= \tfrac{2}{\sqrt3}A(P) + \tfrac12 M(P) - \tfrac{2n-b-2}{2} - \tfrac{b}{2}
= \tfrac{2}{\sqrt3}A(P) + \tfrac12 M(P) + 1 - n. \qquad\blacksquare$$

**Two properties that matter later.**

- **The identity is combinatorial.** Nothing in it uses the separation hypothesis; it holds for
  any non-collinear finite $E$. Oler's *theorem* is the separate statement that the left-hand side
  is $\ge 0$ when the separation is at least 1.
- **The total face excess does not depend on the triangulation.** Summing, it equals
  $\frac{2}{\sqrt3}A(P) - \frac{2n-b-2}{2}$, a function of $A(P)$, $n$ and $b$ only. So does the
  boundary-edge excess, $\frac12(M(P) - b)$. Choosing a cleverer triangulation — Delaunay, or
  anything else — cannot change either total. This kills the obvious repair attempt in §4 before
  it starts.

**Verification** (`experiments/packing-oler-slack`, exact): both halves — $F = 2n-b-2$ and
$\sum_f A_f = A(P)$ — are checked on all 15 non-degenerate configurations available, and
separately the two sides of the identity are computed by independent routes (left from
$A, M, n$; right from the triangulation) and their enclosures checked to intersect. The
triangular controls $n = 3, 6, 10$ give exactly zero on both sides, every face and every edge.

$n = 1$ and $n = 2$ are **excluded**: their hulls are a point and a segment, so there is no
triangulation and no Jordan polygon. That is the same degeneracy [`../oler-lower-bound/`](../oler-lower-bound/)
§2.1 records in Oler's own derivation, and it is handled the same way — separately, not silently.

## 2. What the identity says about Oler — `sketch`

Under the separation hypothesis, consecutive boundary points are at distance $\ge 1$, so
**every** boundary-edge term is $\ge 0$; the boundary-edge excess is never the reason Oler fails to
be tight. So, writing $\mathrm{FE}$ and $\mathrm{BE}$ for the two sums:

$$\text{Oler} \iff \mathrm{FE} + \mathrm{BE} \ge 0, \qquad \mathrm{BE} \ge 0 \text{ always}.$$

Individual *faces* can certainly be negative — a triangle with all sides $\ge 1$ can have area far
below $\sqrt3/4$ if it is obtuse enough. The natural strengthening is therefore to ask whether the
negative faces are always paid for **in aggregate**:

> **Hypothesis H (face-excess nonnegativity).** For every unit-separated finite $E$,
> $\mathrm{FE} \ge 0$; equivalently $n \le \frac{2}{\sqrt3}A(P) + \frac{b}{2} + 1$.

The equivalence is immediate from $\mathrm{FE} = \frac{2}{\sqrt3}A(P) - \frac{2n-b-2}{2}$. Read the
right-hand form: it is Oler's inequality with the boundary term $\frac12 M(P)$ — a *length* —
replaced by $\frac{b}{2}$, a *count*. H is exactly the statement that Oler's boundary term can be
counted rather than measured, and it is strictly stronger than Oler whenever some boundary edge is
longer than 1.

H is what a floored-perimeter strengthening would be built on; §4 refutes it.

## 3. The slack atlas — `numerical`

Oler's route to a bound on $s(n)$ applies the inequality **twice**: first to the hull $H$ of the
configuration, then relaxing $A(H) \le A(T)$, $M(H) \le M(T)$ to the containing triangle $T$ of
side $a$. [`../oler-lower-bound/`](../oler-lower-bound/) §2.1 flags that *both* stages can lose but
does not say how much each loses. That is measurable, and here it is measured, exactly, for every
exact certificate in the repo:

$$\underbrace{\left[\tfrac{a^2}{2} + \tfrac{3a}{2} + 1\right] - n}_{\text{total}}
\;=\; \underbrace{\left[\tfrac{2}{\sqrt3}A(H) + \tfrac12 M(H) + 1 - n\right]}_{\textbf{stage 1}}
\;+\; \underbrace{\left[\tfrac{2}{\sqrt3}\bigl(A(T)-A(H)\bigr) + \tfrac12\bigl(M(T)-M(H)\bigr)\right]}_{\textbf{stage 2}}$$

with stage 1 split further into face and edge excess by §1. All values below are exact
(enclosures where a perimeter is involved); $b$, $i$, $F$ are the boundary, interior and face
counts. $a$ is in Oler normalisation, i.e. half this repo's `point_triangle_side`.

| $n$ | configuration | $b$ | $i$ | $F$ | face exc. | edge exc. | **stage 1** | **stage 2** | total |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 | lattice $T(2)$ | 3 | 0 | 1 | 0 | 0 | **0** | 0 | 0 |
| 4 | corners + centroid | 3 | 1 | 3 | 0 | 1.0980762 | **1.0980762** | 0 | 1.0980762 |
| 5 | $T(3)$ − apex | 5 | 0 | 3 | 0 | 0 | **0** | 1 | 1 |
| 6 | lattice $T(3)$ | 6 | 0 | 4 | 0 | 0 | **0** | 0 | 0 |
| 7 | Melissen | 6 | 1 | 6 | 0.7320508 | 1.0980762 | **1.8301270** | 0 | 1.8301270 |
| 8 | Melissen | 6 | 2 | 8 | 0.2481875 | 1.3722813 | **1.6204689** | 0 | 1.6204689 |
| 9 | $T(4)$ − apex | 8 | 1 | 8 | 0 | 0 | **0** | 1 | 1 |
| 10 | lattice $T(4)$ | 9 | 1 | 9 | 0 | 0 | **0** | 0 | 0 |
| 14 | $T(5)$ − apex | 11 | 3 | 15 | 0 | 0 | **0** | 1 | 1 |
| 15 | lattice $T(5)$ | 12 | 3 | 16 | 0 | 0 | **0** | 0 | 0 |
| 20 | $T(6)$ − apex | 14 | 6 | 24 | 0 | 0 | **0** | 1 | 1 |
| 21 | lattice $T(6)$ | 15 | 6 | 25 | 0 | 0 | **0** | 0 | 0 |

(The two files in `results/`, $n = 3$ and $n = 6$, reproduce their rows above exactly. $n = 1, 2$
are degenerate, per §1.)

**The finding, and it is the useful part of this attack.** For every lattice and
lattice-minus-apex configuration — that is, for $n = T(k)$ *and* for the Erdős–Oler cases
$n = T(k) - 1$ — **stage 1 is exactly zero**: Oler's inequality applied to the configuration's own
convex hull is exactly tight, with no slack in any face or any edge. All of the loss at
$n = T(k) - 1$ is stage 2, and it is exactly $1$, for every $k = 3, 4, 5, 6$ checked.

That is a sharper statement than "Oler is slack at non-triangular $n$", and it says something
about these witnesses. Conversely at $n = 4, 7, 8$ — where the hull *is* the whole triangle, so
stage 2 is zero — every bit of the slack is stage 1, i.e. genuinely a weakness of the packing
bound.

> **Correction — an earlier version of this paragraph overreached, and the overreach was
> load-bearing.** It concluded: "at $n = T(k)-1$ the packing bound is not what is failing; the
> hull → triangle relaxation is", and therefore that a proof of Erdős–Oler must find its missing
> point in the relaxation step. **That does not follow, and it is false.** The atlas measures the
> configurations in this repo's certificates, and every one of them deletes the *apex*. Delete an
> **interior** point of the $T(k)$ lattice instead and you get an equally valid $n = T(k)-1$
> configuration at the same side $a = k-1$ whose hull is the *whole* triangle — so stage 2 is
> zero and the entire deficit of 1 sits in stage 1. Same $n$, same $a$, same total slack of 1,
> opposite stage. Checked at $k = 7$: Oler$(6) = 28$, $n = 27$, total $= 1$; apex-deleted gives
> (stage 1, stage 2) $= (0, 1)$, interior-deleted gives $(1, 0)$.
>
> A lower-bound argument has to handle **every** configuration, not a chosen witness, so it cannot
> route its missing point exclusively through either stage. What the atlas actually establishes is
> narrower and still worth having: *for the apex-deleted witnesses, stage 1 is exactly tight*, so
> no improvement to the packing inequality alone can exclude them — one must use the relaxation
> there. The symmetric statement holds for the interior-deleted witnesses with the stages swapped.
>
> Found by an independent worker attacking the relaxation route, which produced the
> interior-deleted witness as the thing that killed its own assignment; re-derived here before
> being accepted. This is the second correction to this file from that check, and this one changes
> what the file *means*, not just what it says.

**This one generalises, and the first version of this file understated it.** I filed the pattern
as `numerical` over twelve configurations; an independent checker pointed out it is a two-line
count valid for **every** $k$, and re-deriving it confirms that. Both hulls have every boundary
edge of length exactly $1$, so $M = b$ and the boundary-edge excess vanishes identically. With
$a = k-1$:

- **$n = T(k)$:** $b = 3a$, $\tfrac{2}{\sqrt3}A(H) = \tfrac{a^2}{2}$, so
  $\mathrm{FE} = \tfrac{a^2}{2} - \tfrac{2T(k) - 3a - 2}{2} = 0$, and stage 2 $= 0$ since
  $H = T$.
- **$n = T(k)-1$** (apex removed, so $H$ is $T$ minus a unit corner triangle): $b = 3a - 1$,
  $\tfrac{2}{\sqrt3}A(H) = \tfrac{a^2-1}{2}$, so
  $\mathrm{FE} = \tfrac{a^2-1}{2} - \tfrac{2(T(k)-1) - (3a-1) - 2}{2} = 0$; and the total is
  $\tfrac{a^2}{2} + \tfrac{3a}{2} + 1 - (T(k)-1) = T(k) - (T(k)-1) = 1$, using
  $\tfrac{(k-1)^2 + 3(k-1) + 2}{2} = T(k)$.

The $k$-dependence cancels identically in both. So **stage 1 is exactly zero and stage 2 is
exactly 1 at $n = T(k)-1$, for every $k$** — status `sketch` (my derivation, elementary), verified
exactly for $k = 2..30$ by formula and for $k \le 6$ against the certificates. Still not used for
anything below; the point is that the Erdős–Oler deficit is a *constant* 1 in the relaxation step,
not something that decays with $k$.

## 4. The probe: hypothesis H is false — `refuted`

**Minimal witness.** $E = \{(0,0),\,(1,0),\,(2,\tfrac12)\}$. Pairwise squared distances are
$1$, $\tfrac54$, $\tfrac{17}4$, all $\ge 1$. The hull is one triangle, so there is exactly one
triangulation with vertex set $E$, and its area is $\tfrac14 < \tfrac{\sqrt3}{4} = 0.4330\ldots$:

$$\mathrm{FE} = \tfrac{2}{\sqrt3}\Bigl(\tfrac14 - \tfrac{\sqrt3}{4}\Bigr)
= \tfrac{\sqrt3}{6} - \tfrac12 = -0.2113248\ldots < 0.$$

Everything here is exact rational or $\mathbb{Q}(\sqrt3)$ arithmetic, and it needs nothing from
§1 — with one face there is nothing to sum. **H is false.**

**The deficit is unbounded, not a three-point curiosity.** Take
$p_j = \bigl(j,\; j(m-j)/m^3\bigr)$ for $j = 0,\dots,m$: consecutive points differ by 1 in $x$ so
are at distance $\ge 1$, non-consecutive ones by $\ge 2$; the $y$-values are strictly concave, so
all $m+1$ points are hull vertices and $b = n$; and the hull area is $O(1)$ while $n$ grows.
Computed exactly:

| configuration | $n$ | min sep$^2$ | total face excess | Oler slack |
|---|---:|---:|---:|---:|
| obtuse triangle $(0,0),(1,0),(2,\tfrac12)$ | 3 | 1 | $-0.2113249$ | $0.3784685$ |
| flat arc, $m = 3$ | 4 | 1 | $-0.8289333$ | $0.1738065$ |
| flat arc, $m = 4$ | 5 | $1.000244$ | $-1.3195780$ | $0.1816421$ |
| flat arc, $m = 6$ | 7 | $1.000021$ | $-2.3128957$ | $0.1874793$ |
| flat arc, $m = 8$ | 9 | $1.000004$ | $-3.3105569$ | $0.1896033$ |
| flat arc, $m = 12$ | 13 | $1.000000$ | $-5.3088864$ | $0.1911615$ |
| flat arc, $m = 16$ | 17 | $1.000000$ | $-7.3083017$ | $0.1917186$ |

The face excess falls off like $-n/2$; Oler's inequality survives (right column stays positive)
precisely because the boundary-edge excess pays for it. **Oler's boundary term genuinely needs
length, not count** — that is what H got wrong, and the atlas in §3 could not see it because every
configuration there is close to a lattice.

**No triangulation repairs this** (§1): the total face excess is a function of $A(P)$, $n$ and $b$
alone. Choosing Delaunay, or any other triangulation, changes nothing.

**Consequence: the route is dead.** The floored-perimeter derivation was to be (i) H, giving
$n \le \frac{2}{\sqrt3}A + \frac b2 + 1$; then (ii) $b \le 3\lfloor a\rfloor$, since a side of
length $a$ carries at most $\lfloor a \rfloor + 1$ separated points and the three corners are
shared. Step (i) is false. **Step (ii) is worse than unjustified — it is unavailable**, and that is worth
recording because it means the route is structurally dead rather than dead pending a patch. First
the stated warrant is wrong: $b$ counts points on $\partial\operatorname{conv}(E)$, which need not
lie on $\partial T$ at all — a hull vertex can sit strictly inside the triangle. Second, what *is*
provable goes the wrong way. Consecutive boundary points have arc-separation at least their chord
distance, i.e. at least $1$, and the boundary is a closed curve of length $M(H) \le M(T) = 3a$, so

$$b \;\le\; \lfloor M(H) \rfloor \;\le\; \lfloor 3a \rfloor,$$

and $\lfloor 3a\rfloor \ge 3\lfloor a\rfloor$ always, with strict inequality at exactly the
non-integer $a$ the strengthening was supposed to exploit. The route needed a bound at least as
strong as $3\lfloor a\rfloor$ and only $\lfloor 3a \rfloor$ exists; substituting it back into
the (false) H recovers nothing better than a floored form of Oler. Both steps fail, independently.
Per issue #78's kill-criterion and `RULES.md` §6.3, I stop here rather than re-scoping.

**Correction to the paragraph above, from a worker who attacked step (ii) directly.** Saying step
(ii) is "unavailable" conflates two different counts, and the distinction is the actual reason the
route dies:

- **Points on $\partial T$** (the triangle's own boundary). Here $3\lfloor a\rfloor$ **is** a true
  bound, and sharp for every $a \ge 1$ — proved via a per-side count plus the fact that a $60°$
  corner forces $\max(x,y) \ge 1$ on its two legs, with an exact attaining family in
  $\mathbb{Q}(\sqrt3)$. So the step is not false and not unavailable.
- **Points on $\partial\operatorname{conv}(E)$** (the count $b$ that step (i) actually consumes).
  Here $\lfloor 3a \rfloor$ is the best available, as above.

The route needed $3\lfloor a\rfloor$ *for the hull count*, and what is provable at that strength is
about the other set. It dies on the mismatch between the two readings — not because nothing is
provable. Recording the difference because a future attack that inherits "step (ii) is
unavailable" would go looking in the wrong place.

**And the stronger result that closes the whole family.** That worker then showed there is **no
function $\Phi$ whatsoever** with $n \le \frac{2}{\sqrt3}A(\operatorname{conv}E) + \Phi(b) + 1$:
scale the lattice $T(k)$ by $1+\delta$ and push every boundary point inward by $\varepsilon$, and
$b$ collapses to $3$ while $n - \frac{2}{\sqrt3}A - 1$ grows like $\frac{3k-3}{2}$. So replacing
Oler's boundary *length* by any function of a boundary *count* is dead in general, not merely for
the particular H of §2 — and the same family refutes H **at the triangular lattice itself** for
$k = 3..7$, which kills the natural "H is fine for non-degenerate configurations" repair that §4's
flat-arc witnesses leave open. See [`../eo-boundary-counting/`](../eo-boundary-counting/).

(All of this is *same-family* checking and grants no status — `RULES.md` §5.)

## 5. What the route was aiming at — a bare conjecture, not a target

### 5.1 The statement

> **Conjecture FP (floored perimeter).** If $n$ points at pairwise distance $\ge 1$ lie in a closed
> equilateral triangle of side $a$, then
> $$n \;\le\; \tfrac{a^2}{2} + \tfrac32\lfloor a \rfloor + 1 .$$

Oler gives the same with $\lfloor a\rfloor$ replaced by $a$, so FP is a strict improvement at every
non-integer $a$ and identical at integer $a$. **FP is unproved here, and §4 killed the only
derivation this attack had for it.** It is stated so the next reader does not have to reconstruct
what was being attempted — not as a result, and not as an open task.

### 5.2 It is consistent with everything this repo records — `numerical`

FP holds, checked exactly, on all 17 values of $n$ whose $s(n)$ this repo records as `cited`, and
on all 28 best-known constructions the repo records for $4 \le n \le 36$ (Graham–Lubachevsky's
$d(n)$, loaded from `experiments/circle-packing-search/reference.py`). Every row is a
configuration that provably *exists*, so a single violation would refute FP; there are none.

It is **exactly tight** — equality — at $n = 4$ and at every triangular number $T(k)$ in range
($3, 6, 10, 15, 21, 28, 36$). The tightest non-equality margins are, in order,

| $n$ | 8 | 13 | 19 | 12 | 26 | 34 |
|---|---:|---:|---:|---:|---:|---:|
| slack of FP | 0.2482 | 0.3852 | 0.4599 | 0.4641 | 0.4845 | 0.4957 |

and $n = 8, 13, 19, 26, 34$ is exactly the family $T(k) - 2$, whose margin appears to climb toward
$\tfrac12$ from below. **That is where FP would break if it is false**: a $T(k)-2$ packing slightly
better than the best known, for $k$ beyond the checked range, is all it would take. Recorded as a
pointer for whoever wants to try to refute it — refuting is the useful direction here, per §5.3.

### 5.3 Why nobody in this repo should try to *prove* it

Exactly (`erdos_oler_implication`, exact rational arithmetic, $k \le 12$): for $a < k-1$ we have
$\lfloor a \rfloor \le k-2$, so FP gives
$n < \frac{(k-1)^2}{2} + \frac32(k-2) + 1 = T(k) - \frac32$, i.e. at most $T(k) - 2$ points. So
$T(k) - 1$ points force $a \ge k-1$:

> **FP implies $s(T(k)-1) = s(T(k))$ for every $k$ — the full Erdős–Oler conjecture**, open for
> $k \ge 7$ (this problem's [`README.md`](../../README.md)).

By repo `RULES.md` §7 that settles the posture. A short proof of FP would be a proof of an open
conjecture, so the prior against any such proof produced here is overwhelming, and an argument
that *looks* fine is exactly what a subtle error looks like from the inside. Do not attack FP from
the proof side. If FP is worth anything to this project it is as a **falsification target**
(§5.2), or as a statement to look up (§6).

## 6. Honest accounting

**Novelty: UNVERIFIED.** FP and the §1 identity are elementary enough that both are plausibly
known. The obvious prior art to check is Folkman & Graham, *A packing inequality for compact
convex subsets of the plane*, Canad. Math. Bull. — a paper that improves Oler-type inequalities,
named in issue #78 and found by a search here as a Cambridge Core record. **Its page is blocked at
this session's egress proxy** (`EGRESS_BLOCKED` on `cambridge.org`), so nothing about its contents
is verified: not its statement, not its year, not whether it already contains either result. Also
unchecked for the same reason: Groemer 1960 beyond what
[`../../README.md`](../../README.md) already records, Melissen's thesis, and the Zassenhaus–
Groemer–Oler literature that a search suggests exists. **Assume both are known until someone with
library access says otherwise.**

**Recorded because it nearly went the other way.** Feeding Graham–Lubachevsky's printed 15-s.f.
decimals into the §5.2 check as if they were exact — $d(20) = 0.2$, $d(27) =
0.166666666666667$, $d(35) = 0.142857142857143$ — makes $\lfloor a \rfloor$ come out one too small
at $n = 4, 27, 28, 35, 36$ and reports **five refutations of FP**. All five are artefacts of the
last printed digit at the lattice cases, where $a = k-1$ is exactly an integer and $\lfloor
a\rfloor$ is maximally sensitive. The fix is to use the exact closed form wherever the repo has one
and to treat a printed decimal as a $\pm 1$ ulp *enclosure* otherwise, which is what the code now
does. This is the same failure mode this repo's `FINDINGS.md` keeps logging — a correction that is
itself the error, driven by a secondhand record — one layer down, in a rounding digit rather than a
bibliographic field.

**What is exact and what is enclosed.** Every decision — every sign, every comparison that
produces a conclusion above — is exact, in $\mathbb{Q}$ or $\mathbb{Q}(\sqrt3,\sqrt{11})$. Only
quantities containing an edge *length* (perimeters, boundary-edge excess, Oler's slack itself) are
rational intervals with outward rounding. No floating-point value is compared against anything.

**Dependencies, per `RULES.md` §3.** §1–§2 depend on nothing but elementary geometry (they do not
even use Oler's theorem). §3 depends on the certificates in
[`../exact-algebraic-constructions/certificates/`](../exact-algebraic-constructions/certificates/),
whose own status is `sketch`/`numerical` — but only as *inputs*: every quantity in the atlas is
recomputed from the coordinates here, and the atlas asserts nothing about optimality, so no status
is inherited into a claim. §5.2 additionally depends on published construction values via
`experiments/circle-packing-search/reference.py`, which is `numerical`. Nothing anywhere depends on
§1 being true except §3's *interpretation*; §4's refutation does not.

**Independently rechecked, and what that is worth.** Another worker of *this same agent* wrote a
checker from scratch (its own field arithmetic, parser, hull and triangulator, `geometry.py`
unopened until its own had run) and reproduced every atlas column to 7 d.p., the exact face-excess
signs, the flat-arc family, and the FP $\Rightarrow$ Erdős–Oler derivation; it found no
disagreement, and its two corrections are folded in above. **This grants no status whatsoever**
(`RULES.md` §5: cross-examination requires a *different model family*). The identity stays `sketch`
until Codex examines it. It is recorded because a check that found two understatements is worth
more than the absence of one, not because it upgrades anything.

**Not checked.** Whether FP is true, false, or known. Whether any *other* strengthening survives
the §4 counterexamples — I did not look, because the kill-criterion said stop. Whether the
literature already contains any of this: **not checkable from this session at all** — every
scholarly host is blocked at the egress proxy, see `../eo-literature/`.
