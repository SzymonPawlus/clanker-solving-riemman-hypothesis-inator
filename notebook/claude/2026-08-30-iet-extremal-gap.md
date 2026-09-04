# 2026-08-30 — IET, closing the two gaps in `extremal-size` Theorem C

Worker journal for `claude`, branch `claude/inscribe-equilateral-triangle-oj15x1`.
Lane: [`../../problems/inscribed-equilateral-triangle/attacks/extremal-gap-closure/`](../../problems/inscribed-equilateral-triangle/attacks/extremal-gap-closure/).
Files owned: that lane's `README.md` and `KILL-CRITERION.md`, and this file. Nothing else was
written. No git command was run (the dispatcher commits).

**Deliberate clash.** A concurrent lane (`attacks/extremal-refutation-hunt/`) is trying to refute
the bound I am trying to prove. I did not open its directory, did not `ls` it beyond the parent
listing that showed its name, and did not coordinate. If we disagree, that disagreement is the
product.

---

## 0. Order of work (so the §6.2 discipline is auditable)

1. Read `RULES.md` (§0, §1, §2, §3, §5, §7, §9), the problem `README.md` header and `RULES.md`
   in full, `attacks/extremal-size/README.md` §§1–7 and the result table,
   `attacks/round3-cross-review/README.md` head + Lane 3 verdicts + "strongest objections".
2. Pencil work on both gaps. **No code.**
3. Wrote `KILL-CRITERION.md`.
4. Only then wrote and ran the exact checker.
5. Wrote the lane README; re-extracted the embedded copy of the checker from the README and ran
   *that*, to confirm the version a reader gets is the version that produced the recorded output.

---

## 1. Gap 2 first, as instructed — and it fell quickly

The brief's hint was right, but not for the reason I expected. The sub-interval
$[-90°+\varepsilon,\,30°-\varepsilon]$ does work, and it lets you delete three separate claims
that `extremal-size` §6 Step 1 makes and does not prove: the continuous-bijection-onto
$\partial K\setminus\{A\}$ claim, the values $R(\pm90°)=0$, and continuity on the *closed*
interval. But when I wrote out what the sub-interval needs to make $g(a)>0>g(b)$, it needs
$R(90°-\varepsilon)<\sqrt3\,r$ for some $\varepsilon$, i.e. $R$ small near the tangent
directions — which is the endpoint statement wearing a hat.

So I proved the underlying fact instead (Lemma E). The proof is three lines and turns on noticing
what strict convexity says about a *supporting line*, not about the boundary: $K\cap H$ is convex
and inside $\partial K$, so it is a single point. Then any subsequential limit of
$A+R(\theta_n)u(\theta_n)$ with $\theta_n\to90°$ lies in $K\cap H=\{A\}$, so $R\to0$.

I also had to re-derive interior continuity (Lemma C) because I am not allowed to assume the
other lane's `sketch`, and the only nontrivial part is that the *open* segment from $A$ to the
far boundary point is interior — which needed the "$W = \{(1-\lambda)x+\lambda p_0\}$ is open"
trick plus an IVT in $\lambda$ to land the auxiliary point inside the incircle chord. That was
the fiddliest half-page of the day and is one of the two places I would look first for my own
error.

**Honest accounting, recorded in the lane README per KILL-CRITERION K3:** the sub-interval fix is
a real improvement to the write-up and removes three unproved claims, but it does not remove a
hypothesis. Presenting it as if it did would have been the exact kind of laundering §0 warns
about.

## 2. Then Gap 1, where the sky fell in

I went to check the smoothing $K_n=K+\tfrac1nD$ and stopped at the word "strictly".

$K+\varepsilon D$ is the **outer parallel body**. For a square it is a *rounded* square — and a
rounded square has four dead-flat sides. Minkowski summation with a disk kills corners, not
flats. The clean statement is $F(A+B,u)=F(A,u)+F(B,u)$ for faces, and $F(D,u)$ is always a
single point, so $F(K+\varepsilon D,u)$ is a translate of $F(K,u)$:

> $K+\varepsilon D$ is strictly convex **iff** $K$ is.

The parenthetical justification in `extremal-size` ("needs parallel segments in $\partial A$ and
$\partial B$") is also wrong on its own terms — a segment is needed in only one summand.

This is the first genuine mathematical error I have found in that lane, and it is in the step both
the lane itself and the round-3 examiner flagged as weakest. Neither of them caught *this*; the
examiner recorded it as "plausible, standard technique, did not independently prove the limit
step". The limit step is in fact fine (Lemma L0 below). The bug was one word earlier, in a clause
that reads like boilerplate. Worth remembering: the round-3 review checked the hard-looking half
of Step 0 and took the easy-looking half on trust, and the easy-looking half was the broken one.

**Repair.** I wanted a strictly convex outer approximation with $K\subseteq K_n$ (the limit step
needs that inclusion). Two candidates:

- **Ball hull** $\bigcap\{D(x,\rho):K\subseteq D(x,\rho)\}$ — geometric, obviously strictly
  convex, but proving $\to K$ in Hausdorff takes a paragraph.
- **Gauge smoothing** $\{(1-\varepsilon)\gamma_K^2+\varepsilon|x|^2/b^2\le1\}$ — strictly convex
  because $|x|^2$ is strictly convex and $\gamma_K^2$ is convex, and the two inclusions
  $K\subseteq K_\varepsilon\subseteq(1-\varepsilon)^{-1/2}K$ are one line each and hand you
  Hausdorff convergence *and* $r(K_n)\ge r$ for free.

Took the second. The scaling by $b^2$ (with $K\subseteq D(0,b)$) is what makes
$\varepsilon|x|^2/b^2\le\varepsilon\gamma^2$ and hence $K\subseteq K_\varepsilon$; without it the
inclusion can go the wrong way, which would have broken Lemma L0. That is a place I nearly
slipped.

## 3. Is the reduction load-bearing, or was I patching a formality?

This is the question I am glad I asked, because I first convinced myself it was a formality.

Attempt: choose the contact point $A$ so that $K\cap H_A=\{A\}$ and skip the reduction. Killed
immediately by polygons — the incircle of a polygon touches *sides*, so $K\cap H_A$ is a whole
edge at every contact point. Then I tried to show the sign condition holds anyway, and found the
long thin rectangle flips *both* signs (so the IVT still fires, just with the opposite
orientation), which made me suspect the condition is robust. It is not.

The witness: take a unit disk and pull one boundary point out to a spike,
$K_M=\operatorname{conv}(D((0,1),1)\cup\{(M,0)\})$, with $A=(0,0)$ the contact point at the base
of the spike. The spike makes $R(90°)=M$ huge while $R(-90°)=0$: maximally asymmetric flat, which
is exactly what the symmetric cases could not produce. For $M>4/\sqrt3$ both endpoint values of
$g$ are positive. And at $M=100$ the whole function $g$ is positive on $[-90°,30°]$, so the zero
set is empty.

I checked $M=3$ first with pencil-and-decimal and got a sign change near $\theta=-20°$, which
nearly made me abandon the witness. The threshold is $M^2/(M^2+1)>\cos^2(30°-\arctan(1/M))$;
$M=3$ is on the wrong side of it and $M=100$ is well clear. Getting that right was worth the
half hour — a witness that fails at the first value you try is exactly the situation where it is
tempting to conclude the phenomenon is not real.

**Bonus finding, which I did not expect.** At that same $A$ there *is* an inscribed equilateral
triangle of side $\approx2.283$: its second vertex sits in the *interior* of the boundary segment
$[(0,0),(M,0)]$, not at the far intersection of its ray. So a ray from $A$ can meet $\partial K$
in a continuum, and `extremal-size` Step 2's "**iff**" is false. Only the "if" is used, so the
theorem is unharmed — but the stated equivalence would be a landmine for anyone reusing it, and
it is in the correction-request list.

The four-case analysis proving $Z=\emptyset$ for $M=100$ is exact (the trig inputs are
$\arctan x<x$ and $\cos x\le1-x^2/2+x^4/24$, with margins of order $0.2$, so nothing rests on a
decimal). I wrote the checker afterwards as a net for algebra slips, not as the decision.

## 4. Ten minutes on replacing the approach (KILL-CRITERION K4)

The containment route dies for a one-sentence reason: *inscribed is a boundary condition*.
$D(O,r)\subseteq K$ gives a contained equilateral triangle of side $\sqrt3\,r$, and dilating it
to reach $\partial K$ lands its three vertices at three different times. `refuted`, recorded.

The one follow-up attempt paid off. Shooting three rays from $O$ at mutual $120°$ gives
$|P_iP_j|^2=\rho_i^2+\rho_j^2+\rho_i\rho_j\ge3r^2$ **automatically** — the size half of the
theorem is free, and all the difficulty is existence. That reframing is worth having on the
record: it says the bound $\sqrt3\,r$ is not the delicate part.

It also gives a **completely independent proof** for 3-fold symmetric bodies (the set of inball
centres is convex and rotation-invariant, so its centroid is the symmetry centre), with no limits
and no IVT. Disk, equilateral triangle, Reuleaux triangle, regular $3k$-gons. That is my main
independent confirmation that Theorem C is not simply false — I would rather have a gap-free
proof of a special case than another sample of the general one.

I stopped there, per K4. The equation count ($\rho(\varphi)=\rho(\varphi+120°)=\rho(\varphi+240°)$
is two equations in one unknown, and the $120°$ structure forces the three-way equality — no
weaker configuration is equilateral) says the route cannot be pushed further without a genuinely
new idea.

## 5. On a limit-free proof, and why I do not have one

I spent a while on parametrising $\partial K$ by a weakly-monotone angle function $\theta(\sigma)$
with $d(\sigma)=|p(\sigma)-A|$, so that flat pieces become plateaux of $\theta$ on which $d$ is
strictly monotone, and asking for $\Gamma\cap(\Gamma+(60°,0))\ne\emptyset$. This is the honest
set-valued version of the radial function, and it is *not* a fix: "starts below, ends above" for
the shifted curve is literally the same sign condition, and $K_{100}$ breaks it. Recorded in the
lane README's open-problems section so the next worker does not spend the same hours. A limit-free
proof needs a different mechanism, not a better parametrisation.

## 6. Self-assessment — where I think I am most likely to be wrong

In order:

1. **Lemma C's interior-continuity proof.** The $W$-is-open + IVT-in-$\lambda$ step is the least
   routine thing I wrote and the easiest to have botched. The statement is certainly true; the
   proof is mine and unchecked.
2. **Lemma S's inclusions.** I want $K\subseteq K_\varepsilon$, and it comes from
   $|x|/b\le\gamma(x)$, which is the *lower* bound on the gauge. I checked the direction twice
   because getting it backwards would silently break Lemma L0 and I would not notice — Lemma L0
   would still "prove" something, just not about $\partial K$.
3. **The claim that $K_M\cap\{x<0\}$ is exactly the disk**, which is what makes $R(-30°)=\sqrt3$
   exact. It rests on both tangent points from $(M,0)$ having $x\ge0$, which I computed by
   reflecting $(0,0)$ in the line through $(M,0)$ and the centre. CHECK 4's independent hull
   oracle covers the formula but only at rational directions, and $-30°$ is not one of them.
4. Least worried about Step 3, Lemma E and Lemma L0 — each is a short argument with one idea.

Nothing here is `verified:review` and I granted none. Six checkers reportedly failed this session
against zero errors of that kind; mine agreed with hand computation on every value I had computed
by hand *first* ($R(30°)\approx2.283$ at $M=100$, $R(+30)=-18/13+24/13\sqrt3\approx1.813$ at
$M=3$, the $M=3$ crossing near $\tan\theta\approx-0.36$), which is the only reason I trust it at
all.

## 7. Protocol notes

- Regularity budget declared at the top of the lane README: **convex**, with the sentence on what
  breaks (and a second sentence on what breaks if you keep convexity but drop *strict* convexity,
  since that is this lane's whole subject).
- All three §3 filters run and reported in the lane README §7. The square contrast is the
  strongest of the three here: the non-transfer is a clean equation count (three points and one
  equation vs four points and two), plus Step 3's angle arithmetic being specific to $60°$.
- Nondegeneracy (§2): every triangle exhibited has an explicit positive side; the limit passage
  carries the uniform bound $\sqrt3\,r$ established before the limit. That part of the original
  Step 0 was done correctly and I said so.
- No `experiments/` file created (not my lane's files), so the checker is embedded verbatim in the
  lane README and is reproducible with `python3` from stdlib alone.
- No dependence on `experiments/inscribed-triangle-maximiser/` (unvalidated, mid-write) and none
  on `extremal-refutation-hunt/` (unread by design).
