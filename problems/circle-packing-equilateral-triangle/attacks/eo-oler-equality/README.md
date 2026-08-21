# Attack: the equality case of Oler's inequality

**Claim type: neither.** No bound on $s(n)$ — upper or lower — is claimed anywhere in this file
(problem [`../../RULES.md`](../RULES.md) §1 asks for that sentence first). What is here is one
proved lemma with its equality classification, one new decomposition identity, one exact
identification of the extremal class, one complete equality theorem in a restricted case, one
**scope result that kills the stated target**, and a `numerical` measurement that answers the
question "would lattice-forcing actually close $k = 7$". Nothing enters `results/`; nothing here
is assumable, including by me (repo [`RULES.md`](../../../../RULES.md) §3).

- Kill-criteria, written before any computation: [`KILL-CRITERION.md`](./KILL-CRITERION.md)
- Code: [`experiments/packing-eo-equality/`](../../../../experiments/packing-eo-equality/) —
  stdlib only, exact arithmetic for every decision except §6, which is labelled `numerical`
- Transcripts: [`out/report.txt`](../../../../experiments/packing-eo-equality/out/report.txt),
  [`out/lattice_probe.txt`](../../../../experiments/packing-eo-equality/out/lattice_probe.txt)
- Journal: [`notebook/claude/2026-08-21-eo-oler-equality.md`](../../../../notebook/claude/2026-08-21-eo-oler-equality.md)
- Author: `claude` (Claude Opus 5 — convergent role, `RULES.md` §8: this is checking and exact
  calculation), 2026-08-21

**Target held: (C), partially.** Not (A), not (B). §5 says why (A) *cannot* be the target the
team wants, and why (B) as stated is not a reduction of Erdős–Oler but a restatement of it.

## Status table

| What | Status |
|---|---|
| **T1 Lemma T** — $\frac{2}{\sqrt3}A+\frac p2\ge 2$ for any triangle with sides $\ge 1$, **with equality exactly at $(1,1,1)$ and the degenerate $(2,1,1)$** | `sketch` (proof in §1; exact scan of over 150 000 triangles found no violation and no third equality triple) |
| **T2 the $\tau$-identity** $\operatorname{slack}=\sum_f\tau(f)-\sum_{e\ \mathrm{int}}(\ell_e-1)$ | `sketch` (my derivation, §2; exactly verified) |
| **T2.1** equality theorem when some triangulation has all interior edges of length $1$ | `sketch` — depends on T1 and T2 only, **not** on Oler |
| **T3 the extremal class** — $E=\Lambda\cap P$ has $\operatorname{slack}=\frac{M(P)-b}2$, zero iff every hull edge is unit | `sketch` over Pick's theorem (`cited`); exactly verified |
| **T4** equality with equilateral hull and no interior points $\Rightarrow a\in\{1,2\}$, $E$ the lattice | `sketch` (complete proof, §4) |
| **S1** an equality theorem excludes exactly one side length at $k=7$ and closes nothing | `sketch` (arithmetic over `cited` Oler) |
| **S2** "deficit $\ge 1$" *is* Erdős–Oler $k=7$, not a reduction of it | `sketch` (one line of monotonicity) |
| **N1** $\max_\Lambda|\Lambda\cap T(a)|=22$ for $a$ across the whole $k=7$ window | `numerical` — grid over orientation, robust over translations; **not** a proof |
| Oler's inequality itself | `cited` — Oler 1961, see [`../oler-lower-bound/`](../oler-lower-bound/) |
| Pick's theorem | `cited` — standard; affine-invariant, applied to $\Lambda$ with covolume $\frac{\sqrt3}2$ |

## Kill-criterion outcomes, stated up front (`RULES.md` §6.3)

> **K1 (primary).** *"If an exactly-verified triangle with all sides $\ge1$ violates
> $\frac2{\sqrt3}A+\frac p2\ge2$, or a third equality triple exists, the base case is false and I
> stop."* — **Not met.** Lemma T is proved in §1 and survived every exact check: no violation, and
> exactly the two predicted equality triples.
>
> **K2 (scope).** *"If the equality characterisation, granted in full, still leaves a non-empty set
> of side lengths $a<6$ at which 27 points are not excluded, target (A) is insufficient; record it
> in the first line, drop to (C), and do not present an equality theorem as closing $k=7$."* —
> **MET, §5.** Granted in full, an equality theorem excludes the single value
> $a^\*=\frac{-3+\sqrt{217}}2$ and nothing else; the open window
> $[a^\*,6)$ survives essentially untouched. I dropped to (C).
>
> **K3 (control).** *"If my candidate extremal class fails to give slack exactly $0$, or some
> lattice-convex set with a long hull edge gives slack $0$, the statement is wrong."* — **Not met**,
> but the *pre-existing* statement of the class was wrong and is corrected in §3: $E\subseteq\Lambda$
> is **not** sufficient for equality. Exact witness: a lattice-convex 4-point set with one hull edge
> of length $\sqrt3$ has slack $\frac{\sqrt3-1}2 = 0.366\ldots \ne 0$.
>
> **K4 (duplication).** Three things I derived independently are already in the repo and are
> **credited, not reclaimed**: see §6.

**What to review hardest**, if you are the cross-examiner: the vertex-minimisation step in the
proof of Lemma T (§1, Step 3) — that is my least-certain step — and the face/edge counts in §2.

**Normalisation.** Separation $1$ throughout (Oler's own). $E$ finite with pairwise distances
$\ge1$, $P=\operatorname{conv}(E)$, $n=|E|$, $b=|E\cap\partial P|$, $A,M$ area and perimeter,
$$\operatorname{slack}(E)\;=\;\tfrac2{\sqrt3}A(P)+\tfrac12M(P)+1-n\;\ge\;0\quad(\text{Oler, }`cited`).$$
The repo's certificates use separation $2$ and side $d=2a$; **nothing in this file reads them**, so
there is no conversion anywhere and no opportunity for the normalisation slip that has caught other
workers today.

---

## 1. Lemma T — the base case, with its equality classification

Every equality induction for Oler has to start at a single triangle, and nothing in this repo
states that case. Here it is, proved.

> **Theorem T1.** Let $x,y,z\ge1$ be the side lengths of a triangle (degenerate allowed), $A$ its
> area and $p=x+y+z$. Then
> $$\tfrac2{\sqrt3}A+\tfrac p2\;\ge\;2,$$
> with equality **iff** $(x,y,z)$ is a permutation of $(1,1,1)$ or of $(2,1,1)$.
>
> Equivalently: $n=3$ points at mutual distance $\ge1$ satisfy Oler's inequality, and equality
> holds exactly for the unit equilateral triangle and for three collinear points at consecutive
> spacing $1$.

*Proof.* Put $\alpha=y+z-x,\ \beta=z+x-y,\ \gamma=x+y-z$, all $\ge0$, and $S:=\alpha+\beta+\gamma=p$.
Heron's formula is $16A^2=S\alpha\beta\gamma$. From $x,y,z\ge1$ we get $S\ge3$.

**Step 1 ($S\ge4$).** Then $\frac p2\ge2$ and $A\ge0$, so the inequality holds. Equality forces
$A=0$ and $S=4$: a degenerate triangle whose longest side equals the sum of the other two, so the
longest side is $S/2=2$ and the remaining two sum to $2$ with each $\ge1$, i.e. both are $1$. That
is $(2,1,1)$, and it does give equality: $0+\frac42=2$.

**Step 2 ($3\le S<4$).** Now $2-\frac p2=\frac{4-S}2>0$ and the claim
$\frac2{\sqrt3}A\ge\frac{4-S}2$ has both sides $\ge0$, so it is *equivalent* to its square,
$\frac43A^2\ge\frac{(4-S)^2}4$, i.e. $\frac{16}3A^2\ge(4-S)^2$, i.e.
$$\tfrac13\,S\,\alpha\beta\gamma\;\ge\;(4-S)^2. \tag{$*$}$$
The constraint $x\ge1$ reads $\beta+\gamma\ge2$, i.e. $\alpha\le S-2$; likewise for $\beta,\gamma$.
Hence also $\alpha=S-\beta-\gamma\ge S-2(S-2)=4-S$, and symmetrically. So
$(\alpha,\beta,\gamma)\in\Delta_S:=\{\alpha+\beta+\gamma=S,\ 4-S\le\alpha,\beta,\gamma\le S-2\}$.

**Step 3 (the minimum of the product over $\Delta_S$).** For $S\in[3,4]$, $\Delta_S$ is the triangle
whose vertices are the permutations of $(S-2,\,S-2,\,4-S)$. *(A vertex needs two coordinates at
their bounds. $(S-2,S-2,4-S)$ is feasible because $4-S\le S-2\iff S\ge3$. The other candidate,
$(4-S,4-S,3S-8)$, needs $3S-8\le S-2\iff S\le3$, so it exists only in the degenerate case $S=3$,
where $\Delta_3=\{(1,1,1)\}$.)* The minimum of $\alpha\beta\gamma$ over the compact set $\Delta_S$
is attained at a vertex: at a minimiser, if two coordinates $\beta,\gamma$ are both strictly inside
their bounds, then with $\alpha$ fixed the map $\beta\mapsto\beta(S-\alpha-\beta)$ is a downward
parabola, hence concave, so its minimum on the feasible interval is at an endpoint — moving there
does not increase the product and reduces the number of free coordinates. Iterating leaves at most
one free coordinate, i.e. a vertex. Therefore
$\min_{\Delta_S}\alpha\beta\gamma=(S-2)^2(4-S)$.

**Step 4 (the resulting one-variable inequality).** $(*)$ now follows from
$\frac13S(S-2)^2(4-S)\ge(4-S)^2$. For $S<4$ divide by $4-S>0$:
$$\tfrac13S(S-2)^2\ge4-S\iff S(S-2)^2+3S-12\ge0\iff (S-3)(S^2-S+4)\ge0 .$$
The identity in the last step is a polynomial identity (both sides expand to
$S^3-4S^2+7S-12$), and $S^2-S+4$ has discriminant $-15<0$, so it is strictly positive. Hence the
inequality holds for all $S\ge3$, **strictly** for $S>3$.

**Equality in Step 2** therefore forces $S=3$, and $S=3$ with $x,y,z\ge1$ forces $x=y=z=1$; the
unit equilateral triangle does give equality, $\frac2{\sqrt3}\cdot\frac{\sqrt3}4+\frac32=2$. $\square$

**Exact verification** (`run.py` §1–§2, all decisions over $\mathbb Q$: with rational sides,
$16A^2$ is rational, so $\frac2{\sqrt3}A\ge2-\frac p2$ is decided by one rational comparison and
never by a floating-point one):

| scan | triangles checked | violations | equality triples |
|---|---:|---:|---|
| grid, sides in $[1,4]$, step $1/12$ | 7 761 | 0 | $(1,1,1)$ |
| random rationals, sides in $[1,7]$, seed 20260821 | 142 714 | 0 | — |
| degenerate $x=y+z$, $y,z\in[1,4]$ step $1/20$ | 3 721 | 0 | $(1,1,2)$ |
| fine scan, $\pm 6/1000$ around $(1,1,1)$ and $(2,1,1)$ | 924 | 0 | — |

Total equality triples found: exactly $\{(1,1,1),(1,1,2)\}$. The polynomial identity and the
vertex step of Step 3 are separately re-checked in code.

**Both equality cases are unit-lattice configurations** — the unit equilateral triangle is a face
of the triangular lattice, and $(2,1,1)$ is three consecutive points of a lattice line. That is the
first evidence, from inside a proof rather than from examples, for the shape of the general
characterisation.

---

## 2. The $\tau$-identity, and one equality theorem it does prove

The decomposition already in the repo ([`../oler-slack-analysis/`](../oler-slack-analysis/) §1,
`sketch`) splits the slack into a face part and a boundary-edge part. I re-derived its ingredients
independently (they are elementary, and per the brief I was not entitled to assume them) and then
recombined them differently, so that **Lemma T is what does the work**.

Let $E$ be finite and non-collinear, $P=\operatorname{conv}(E)$, and let $\mathcal T$ be any
triangulation of $P$ whose vertex set is exactly $E$. Write $L_{\mathrm{int}}$ for the total length
of interior edges and, for a face $f$,
$$\tau(f)\;:=\;\tfrac2{\sqrt3}A_f+\tfrac{p_f}2-2\;\ge\;0\quad\text{(Lemma T)} .$$

> **Theorem T2.**
> $$\operatorname{slack}(E)\;=\;\sum_{f\in\mathcal T}\tau(f)\;-\;\sum_{e\ \text{interior}}(\ell_e-1).$$

*Proof.* Three counts, all for the planar subdivision with $V=n$, $F$ triangles and the outer face.
Each triangle has three sides, interior edges lie in two triangles and boundary edges in one, so
$3F=2|\mathcal E|-b$ and $|\mathcal E|=\frac{3F+b}2$; Euler's $V-|\mathcal E|+(F+1)=2$ then gives
$$F=2n-b-2,\qquad |\mathcal E_{\mathrm{int}}|=|\mathcal E|-b=\tfrac{3F-b}2=3n-2b-3 .$$
(The face count agrees with `oler-slack-analysis` §1, which states it first; $b$ counts **all**
points of $E$ on $\partial P$, not hull vertices — that is the reading the count needs.) Also
$\sum_fA_f=A(P)$ and $\sum_fp_f=M(P)+2L_{\mathrm{int}}$. Hence
$$\sum_f\tau(f)=\tfrac2{\sqrt3}A(P)+\tfrac{M(P)}2+L_{\mathrm{int}}-2(2n-b-2),$$
and subtracting $\operatorname{slack}(E)=\frac2{\sqrt3}A(P)+\frac{M(P)}2+1-n$ leaves
$L_{\mathrm{int}}-(3n-2b-3)=\sum_{e\ \mathrm{int}}(\ell_e-1)$. $\square$

Verified exactly (`run.py` §4) on seven configurations with hand-given triangulations — the unit
triangle, the unit rhombus, $T(3),T(4),T(5)$, the three-point witness of
`oler-slack-analysis` §4, and a generic 4-point set — with $F=2n-b-2$,
$|\mathcal E_{\mathrm{int}}|=3n-2b-3$, $\sum A_f=A(P)$ and both sides of the identity checked
independently.

Both correction terms are non-negative, so T2 gives an **upper** bound on the slack,
$\operatorname{slack}\le\sum_f\tau(f)$ — the wrong direction to prove Oler, which is exactly why
Oler's own proof is not a local one. But it does give an equality theorem outright in a class where
the correction vanishes:

> **Corollary T2.1.** If $E$ admits a triangulation in which **every interior edge has length
> exactly $1$**, then $\operatorname{slack}(E)=\sum_f\tau(f)\ge0$ — an independent proof of Oler's
> inequality for that class, using nothing from Oler — and $\operatorname{slack}(E)=0$ iff every
> face is a unit equilateral triangle, i.e. iff $E$ is a subset of a unit triangular lattice whose
> hull is tiled by unit equilateral faces.

*Proof.* The identity plus $\tau\ge0$ (Lemma T). At equality every $\tau(f)=0$, so by Lemma T's
classification each face is a unit equilateral triangle or the degenerate triple $(2,1,1)$; a face
of a triangulation is non-degenerate, so every face is unit equilateral. Adjacent unit equilateral
faces share an edge, so the lattice generated by one face contains the vertices of its neighbours;
the dual graph of a triangulation is connected, so all of $E$ lies in that one lattice. $\square$

This is a real, checkable instance of the equality characterisation, and its hypothesis is
verifiable on a given configuration. It is not enough for (C): the hypothesis "all interior edges
are unit" is close to assuming the conclusion.

---

## 3. The extremal class, exactly — and a correction to `oler-lower-bound` §5.2

[`../oler-lower-bound/`](../oler-lower-bound/) §5.2 states the missing rigidity as

> **(R2)** equality in Oler's inequality for $(H,E)$ forces $E\subseteq\Lambda$ for some triangular
> lattice $\Lambda$ of minimal distance exactly $1$.

**That condition is necessary but not sufficient, so it is not the equality characterisation.**
The exact statement is:

> **Theorem T3.** Let $\Lambda$ be a unit triangular lattice, $P$ a convex lattice polygon and
> $E=\Lambda\cap P$ (so $P=\operatorname{conv}(E)$). Then
> $$\operatorname{slack}(E)\;=\;\tfrac12\bigl(M(P)-b\bigr)\;\ge\;0,$$
> with equality **iff** every one of the $b$ edges into which $\Lambda$ subdivides $\partial P$ has
> length exactly $1$ — equivalently, iff $P$ is tiled by unit equilateral lattice triangles.

*Proof.* Pick's theorem is affine-invariant, so for $\Lambda$ with covolume $\frac{\sqrt3}2$,
$|\Lambda\cap P|=\frac2{\sqrt3}A(P)+\frac b2+1$ with $b$ the number of lattice points on $\partial P$.
Substituting $n=|\Lambda\cap P|$ into the definition of the slack gives $\frac12(M(P)-b)$. The $b$
boundary lattice points cut $\partial P$ into exactly $b$ segments, each a lattice vector and hence
of length $\ge1$, so $M(P)\ge b$ with equality iff each is a minimal vector. $\square$

So the correct target class is: **$E=\Lambda\cap P$ with $P$ tiled by unit equilateral lattice
triangles** — three conditions, of which (R2) is one. Exactly verified (`run.py` §3, all values
exact in $\mathbb Q(\sqrt3)$ with rigorous rational enclosures for perimeters):

| configuration | $n$ | $b$ | slack (exact) |
|---|---:|---:|---|
| $T(k)$ lattice, $k=2,3,4,5,7$ | 3,6,10,15,28 | 3,6,9,12,18 | $0$ |
| unit rhombus | 4 | 4 | $0$ |
| unit hexagon + centre | 7 | 6 | $0$ |
| unit trapezoid | 5 | 5 | $0$ |
| $T(7)$ minus its apex | **27** | 17 | $0$ |
| **lattice triangle with one $\sqrt3$ edge** | 4 | 4 | $\tfrac{\sqrt3-1}2=0.366025\ldots$ |
| $T(4)$ minus its interior point | 9 | 9 | $1$ |
| $T(7)$ minus an interior point | 27 | 18 | $1$ |

Two things to read off, both load-bearing for anyone continuing this route.

1. **The $\sqrt3$-edge row is the counterexample to (R2) as stated.** Its four points lie in
   $\Lambda$, it is lattice-convex, and its slack is strictly positive. "Equality $\Rightarrow$
   $E\subseteq\Lambda$" is true as far as it goes but cannot be the characterisation, because the
   converse fails.
2. **Equality does not force $n$ to be triangular.** $T(7)$ minus its apex has $n=27$ and slack
   exactly $0$. The triangularity conclusion in `oler-lower-bound` §5.2 comes from the *additional*
   hypothesis that the hull is the whole containing triangle (their (R1), stage-2 equality), not
   from equality in Oler. A reader who takes "equality $\Rightarrow$ $n$ triangular" out of that
   section will be wrong.

---

## 4. Theorem T4 — the equality characterisation in a case where it is complete

This is the (C)-shaped statement I can actually prove: the hull is the whole equilateral triangle,
and there are no interior points.

> **Theorem T4.** Let $E$ be unit-separated with $P=\operatorname{conv}(E)$ an equilateral triangle
> $T$ of side $a$, let every point of $E$ lie on $\partial T$, and let $\operatorname{slack}(E)=0$.
> Then $a\in\{1,2\}$ and $E=\Lambda\cap T$ for a unit triangular lattice: either the three corners
> of a unit triangle ($n=3$), or the three corners and three edge midpoints of a side-2 triangle
> ($n=6$, the $T(3)$ lattice).

*Proof.* $P$ is a non-degenerate triangle whose vertices lie in $E$, so $n\ge3$ and the three
corners of $T$ belong to $E$. With $A(T)=\frac{\sqrt3}4a^2$ and $M(T)=3a$, the hypothesis
$\operatorname{slack}(E)=0$ reads
$$n=\tfrac{a^2+3a+2}2 . \tag{4.1}$$
A side of $T$ is a segment of length $a$; points on it are $\ge1$ apart, so it carries at most
$\lfloor a\rfloor+1$ of them. Summing over the three sides counts each corner twice, and all three
corners are occupied, so $n+3\le3(\lfloor a\rfloor+1)$, i.e.
$$n\;\le\;3\lfloor a\rfloor\;\le\;3a . \tag{4.2}$$
Combining, $a^2+3a+2\le6a$, i.e. $a^2-3a+2\le0$, i.e. $1\le a\le2$.

*Case $a\in[1,2)$.* Then $\lfloor a\rfloor=1$ and (4.2) gives $n\le3$, so by (4.1)
$a^2+3a-4\le0$, i.e. $(a+4)(a-1)\le0$, i.e. $a\le1$. So $a=1$, $n=3$: three points at mutual
distance $\ge1$ that are the corners of a side-1 triangle, i.e. a unit equilateral triangle.

*Case $a=2$.* Then (4.1) gives $n=6$ and (4.2) gives $n\le3\lfloor a\rfloor=6$, so **every**
inequality used is an equality: each side carries exactly $3$ points, and three points at mutual
distance $\ge1$ on a segment of length $2$ must be its endpoints and its midpoint. So $E$ is the
three corners plus the three midpoints — the $T(3)$ lattice. $\square$

Both conclusions are lattice-convex with unit hull edges, as T3 predicts. The arithmetic (the
roots of $a^2-3a+2$ and $a^2+3a-4$, and a grid check that no other $a\in[1,3]$ admits an integer
$n$ satisfying both constraints) is verified in `run.py` §5.

**Where T4 stops, and it is worth being precise about it.** Allow interior points and the argument
dies immediately: (4.1) and (4.2) give $i=n-b\ge\frac{a^2-3a+2}2$, and there is no matching upper
bound on $i$ — bounding the interior points by applying Oler to their own hull is exactly the
partition-and-count identity that
[`../oler-slack-analysis/`](../oler-slack-analysis/) and the partition route already killed. The
natural local repair (show the face excess is non-negative once the hull is an equilateral triangle
with all corners occupied) is **false**; see §6.

---

## 5. Scope — what an equality theorem does at $k=7$, and what (B) really is

This is the part of the attack that changes what should be attempted next, and it is why K2 fired.

**S1. An equality theorem excludes exactly one side length.** Oler gives
$27\le\frac{a^2+3a+2}2$, so $a\ge a^\*=\frac{-3+\sqrt{217}}2$, exactly bracketed in code as
$5.865459931<a^\*<5.865459932$; `../eo-boundary-counting/` §2 (O1) records the same window
$[a^\*,6)$ first. At $a=a^\*$ the slack of a 27-point configuration is exactly $0$, so an equality
characterisation excludes it. For **every** $a\in(a^\*,6)$ the slack is strictly positive:

| $a$ | Oler RHS | slack at $n=27$ |
|---|---|---|
| $a^\*$ | $27.000000$ | $0$ |
| $a^\*+0.01$ | $27.073705$ | $0.073705$ |
| $a^\*+0.05$ | $27.369523$ | $0.369523$ |
| $a^\*+0.13$ | $27.965960$ | $0.965960$ |

An equality statement — *any* equality statement, however strong — says nothing at a configuration
with positive slack. So target (A) improves the $k=7$ bound from $a\ge a^\*$ to $a>a^\*$ and
stops. **In points, which is the unit that matters (`../eo-boundary-counting/` §2): the required
gain is $1$ and an equality theorem delivers $0^+$.**

**S2. "Deficit $\ge1$" is not a reduction of Erdős–Oler; it is Erdős–Oler.** The natural
quantitative target — *for every unit-separated $E$ with $|E|=T(k)-1$ inside an equilateral
triangle of side $a$, the deficit $\frac{a^2+3a+2}2-|E|$ is at least $1$* — is **equivalent** to
Erdős–Oler at $k$, because $a\mapsto\frac{a^2+3a+2}2$ is strictly increasing on $a>0$ and equals
exactly $T(k)$ at $a=k-1$ (verified exactly for $k=2,\dots,10$ in `run.py` §6). So the deficit
reaches $1$ iff $a\ge k-1$. There is nothing to prove *from* it and no partial credit *in* it.

What is genuinely intermediate is the **$\varepsilon$-scale**: a theorem "deficit $\ge\varepsilon$
at $n=27$" gives $d(27)\ge a_\varepsilon$ with $a_\varepsilon=\frac{-3+\sqrt{217+8\varepsilon}}2$,
and Erdős–Oler $k=7$ is exactly $\varepsilon=1$ (note $\sqrt{225}=15$, $a_1=6$ — the algebra
collapses there too). Progress on this route should be reported as a value of $\varepsilon$:

| $\varepsilon$ | $0$ | $0.25$ | $0.5$ | $0.75$ | $1$ |
|---|---|---|---|---|---|
| $a_\varepsilon$ | $5.86546$ | $5.89923$ | $5.93290$ | $5.96650$ | $6$ |

Everything in this repo so far, including this file, sits at $\varepsilon=0$.

---

## 6. What I refuted, and what I only re-derived (`RULES.md` §6.1)

**Already in the repo; credited, not reclaimed.** Before finding them I derived, independently:
the $k=7$ window $[a^\*,6)$ (**O1**, `../eo-boundary-counting/` §2); the failure of face-excess
non-negativity at near-extremal lattice configurations (**W1**, same file §4); and the observation
that the total face and boundary-edge excesses depend only on $(A,M,n,b)$ (`../oler-slack-analysis/`
§1). Priority is theirs. My W1 re-derivation uses a *different* construction — push the three
**corner** points of the $T(k)$ lattice outward along the bisectors, instead of pushing the edge
points inward — and reaches the same conclusion, which is worth recording as independent
confirmation of a load-bearing refutation. Exactly verified (`run.py` §7; separations never
decrease, so $\min\mathrm{sep}^2=1$ throughout):

| $k$ | $\delta$ | $n$ | $a$ | $b$ | face excess | total slack |
|---:|---:|---:|---:|---:|---:|---:|
| 3 | $1/100$ | 6 | 2.01 | 3 | $-1.479950$ | $0.0350500$ |
| 7 | $1/100$ | 28 | 6.01 | 3 | $-7.439950$ | $0.0750500$ |
| 7 | $1/1000$ | 28 | 6.001 | 3 | $-7.494000$ | $0.0075005$ |

**What is new here, and it bears directly on the brief.** The brief proposes that the
slack decomposition makes the equality characterisation concrete, via
*equality $\iff$ every face excess and every boundary-edge excess vanishes*. **That equivalence is
not derivable from the identity.** The identity gives $\operatorname{slack}=\mathrm{FE}+\mathrm{BE}$
with $\mathrm{BE}\ge0$; concluding that both vanish needs $\mathrm{FE}\ge0$, which is precisely the
refuted hypothesis H. Worse, the table above shows the split is **discontinuous** at the extremal
configurations: along that family $\operatorname{slack}\to0$ while
$(\mathrm{FE},\mathrm{BE})\to\bigl(-\tfrac{3(k-2)}2,+\tfrac{3(k-2)}2\bigr)$ — at $k=7$, $(-7.5,+7.5)$
— with the hull an equilateral triangle and all three of its corners occupied. Consequences:

- the equality characterisation cannot be obtained from the slack identity;
- **no stability version of the identity exists**, so the identity is not a route to (B) either;
- and it is not repaired by restricting to "hull $=T$, all corners occupied", which was the natural
  next hypothesis and is the one I tested first.

Whether $\mathrm{FE}=\mathrm{BE}=0$ holds at *exact* equality is untouched by any of this; it is
simply not a consequence of the decomposition.

---

## 7. Would lattice-forcing at side $<k-1$ actually close $k=7$? — `numerical`

The manager's closing question. The answer is **yes, with an enormous margin**, which relocates the
whole difficulty into proving the forcing.

Suppose one could show that a 27-point unit-separated configuration in $T(a)$, $a<6$, must lie in
*some* unit triangular lattice $\Lambda$ (any orientation, any translation). Then $27\le
\max_\Lambda|\Lambda\cap T(a)|$, and a grid search over the lattice's orientation and translation
(`lattice_probe.py`) gives:

| $a$ | translation-robust? | $\max_\Lambda|\Lambda\cap T(a)|$ |
|---|---|---:|
| $6$ (exactly) | — | $28$ |
| $5.9993$ (effective) | yes | $22$ |
| $5.99,\ 5.9,\ 5.87$ | grid only | $22$ |

The count is monotone in $a$, and the robust row is computed with an outward margin $\mu$ that
enlarges the triangle to side $a+2\sqrt3\,\mu$ and exceeds half the translation-grid spacing, so
the tabulated maximum dominates **every** translation, not just gridded ones; only the orientation
is sampled (120 values over the $60^\circ$ period). So the evidence is that
$\max_\Lambda|\Lambda\cap T(a)|=22$ throughout the open window $[a^\*,6)$, jumping to $28$ exactly
at $a=6$.

$22<27$ by five points. So lattice-forcing would close $k=7$ with room to spare — one would not
even need the sharp count, only $\le26$. **Status `numerical`**: a grid can miss a maximum, and the
orientation is sampled, not covered; this is evidence about a quantity, not a theorem. But it is
enough to say where the difficulty is: **all of it is in the forcing, none of it in the counting
afterwards.** And by §5, the forcing has to hold up to deficit $1$, not merely at deficit $0$ —
which is why an equality theorem does not deliver it.

---

## 8. Honest accounting

**Target held: (C), partially.** What is proved: Lemma T with its equality classification (T1), the
$\tau$-identity and the equality theorem it yields under a unit-interior-edge hypothesis (T2,
T2.1), the exact extremal class and the correction to (R2) (T3), and the equality characterisation
for an equilateral hull with no interior points (T4). What is **not** proved: (A), (B), or (C) in
the form the brief asked for — equality with an equilateral hull and interior points allowed
remains open, and §4 says exactly where it breaks.

**The kill-criterion fired**: K2. An equality theorem, granted in full, does not close $k=7$;
it moves $\varepsilon$ from $0$ to $0^+$ on the scale of §5, where the conjecture is
$\varepsilon=1$. I have not re-scoped the target to survive that; I dropped from (A) to (C) and
said so in the first line.

**My least-certain step** is Step 3 in the proof of Lemma T — the claim that
$\min_{\Delta_S}\alpha\beta\gamma$ is attained at a vertex of $\Delta_S$, and that for
$S\in(3,4)$ the only vertices are the permutations of $(S-2,S-2,4-S)$. The concavity argument is
routine and the conclusion is checked exactly on a grid, but it is the one place where a
plausible-looking sentence is carrying real weight. Second least certain: the claim in T2.1 that
unit equilateral faces glue into a single lattice, which is an induction over the dual graph that I
have not written out in full.

**Nothing here may be built on.** T1–T4 are `sketch` (`RULES.md` §3), N1 is `numerical`, and the
whole file is capped at `sketch` regardless of how elementary the individual steps look.

### Reusable outputs

- **Lemma T** — the $n=3$ case of Oler with its equality classification, proved and exactly
  checked. This is the base case any equality induction needs and the repo did not have it.
- **The extremal class**, stated exactly (T3), replacing the incomplete (R2) of
  `oler-lower-bound` §5.2 as the target of the hard direction.
- **The $\varepsilon$-scale** (§5) as the honest way to report progress on this route, together
  with the fact that the $\varepsilon=1$ statement *is* the conjecture.
- **The lattice count 22** across the $k=7$ window (`numerical`), which says the counting half of a
  lattice-forcing argument is free.

### Open follow-ups this surfaced (not claimed here)

1. Does equality force $\mathrm{FE}=\mathrm{BE}=0$? Not a consequence of the decomposition (§6);
   an independent question, and the natural next thing to try to settle *or refute*.
2. Make N1 a theorem: $\max_\Lambda|\Lambda\cap T(a)|\le26$ for $a<6$ is a 3-parameter problem
   (orientation + translation) with piecewise-constant objective, so an exact certified search
   looks reachable. That converts the counting half of §7 from `numerical` to proved and would be
   worth having in advance of any forcing argument.
3. A quantitative Lemma T — a lower bound on $\tau(f)$ in terms of the face's departure from unit
   equilateral — is what a metric discharging proof would need (`../eo-boundary-counting/` §7
   argues discharging must be metric). Lemma T's proof gives $\tau$ as an explicit algebraic
   function of $S$ and the shape, so this is a concrete calculus problem rather than a search for a
   new idea.
