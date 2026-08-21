# Attack: the hull → triangle relaxation, and why it cannot close Erdős–Oler

**Claim type: neither construction nor optimality — no bound on $s(n)$, upper or lower, is
claimed anywhere in this file.** (Problem [`../../RULES.md`](../RULES.md) §1 asks for that sentence
first.) What is here is one *conditional* lower-bound tool, one *barrier theorem* that says the
route this attack was opened on cannot work, and the exact witness that makes the barrier concrete.
Nothing enters `results/`; nothing here is assumable, including by me
(repo [`RULES.md`](../../../../RULES.md) §3).

- Route: attack **stage 2** of Oler's derivation — the relaxation $A(H)\le A(T)$, $M(H)\le M(T)$ —
  identified as carrying the entire missing unit at $n = T(k)-1$ by
  [`../oler-slack-analysis/`](../oler-slack-analysis/) §3.
- Code: [`experiments/packing-eo-hull-deficit/`](../../../../experiments/packing-eo-hull-deficit/)
  — one command, Python standard library only, exact arithmetic throughout.
- Transcript: [`out/report.txt`](../../../../experiments/packing-eo-hull-deficit/out/report.txt).
- Kill-criterion, written before any computation: [`KILL-CRITERION.md`](./KILL-CRITERION.md).
- Author: `claude` (Claude Opus 5), 2026-08-21.

| What | Status |
|---|---|
| §2 Corner-Deficit Lemma | `sketch` — my derivation; elementary, exactly verified on 12 configurations, **not assumable** |
| §3 Corner-Improved Oler (CIO) | `sketch` — mine; depends on Oler (`cited`) plus convex monotonicity |
| §4 Conditional Erdős–Oler (empty-corner case) | `sketch` — mine, a corollary of §3 |
| §5 Neutrality: a corner cut never outvalues what it displaces | `sketch` — mine, two lines of algebra, exactly checked |
| §6 **Relaxation Barrier** | `sketch` — mine; this is what kills the route |
| §7 The zero-gain witness | `numerical` — an exact, explicit 27-point configuration |
| §8 Steiner-type guess $\mathrm{def}\ge \mu^2/6+\mu/2$ | `refuted` — exact witness |
| §9 Necessary conditions on a $k=7$ counterexample | `sketch` (statements) over `cited` inputs |
| Oler's inequality itself | `cited` — Oler 1961, see [`../oler-lower-bound/`](../oler-lower-bound/) |

---

## 0. Kill-criterion outcome, stated up front

> **K1 (primary).** *"If the corner-deficit machinery turns out to be exactly neutral against the
> triangular lattice — if for every corner cut (or, worse, for every convex $K\subseteq T$) the
> deficit the cut guarantees is at most the number of points the cut region can hold — then no
> bound obtained by relaxing $H$ to a cut region can supply the missing unit, and this route is
> dead as a standalone."*
>
> **MET, in the strongest available form (§6).** Not just corner cuts: for **every** convex
> $K \subseteq T$ and every integer side $a$, $\mathrm{def}(K) \le N(T\setminus K)$. The proof is
> three lines and uses only the lattice's exact tightness in Oler's inequality. §7 gives the
> concrete witness at the first open case: 27 unit-separated points in the triangle of side 6 whose
> corner deficit is exactly $0$ and whose hull is the whole triangle. I stopped there and did not
> re-scope.
>
> **K2 (control).** *Not met* — the lemma reproduces $\mathrm{def}(H) = 1$ exactly on
> $T(k)-\text{apex}$ for $k = 3,4,5,6$ and $0$ exactly on every full lattice $T(k)$, $k \le 6$.
>
> **K3 (control).** *Not met* — no certificate has two points in a corner triangle of side $< 1$.

**What survives the kill:** §3 and §4 are a real, if conditional, strengthening of Oler's triangle
bound, and they are *tight* on exactly the extremal configurations. §9 turns them into explicit
necessary conditions on any counterexample to Erdős–Oler at $k = 7$. §6 says where the missing unit
must come from instead, and it is not from geometry — it is from an integer count.

---

## 1. Setup

Oler normalisation throughout: minimum separation **1**, containing equilateral triangle $T$ of
side $a$. (The repo's certificates use separation 2 and side $d = 2a$; the code halves every
coordinate on load. Do not mix them up.)

$E \subseteq T$ finite with pairwise distances $\ge 1$, $n = |E|$, $H = \operatorname{conv}(E)$.
For a convex $K \subseteq T$ write

$$B(K) \;=\; \tfrac{2}{\sqrt3}A(K) + \tfrac12 M(K) + 1, \qquad
\mathrm{def}(K) \;=\; B(T) - B(K) \;=\; \tfrac{2}{\sqrt3}\bigl(A(T)-A(K)\bigr) + \tfrac12\bigl(M(T)-M(K)\bigr),$$

so that $B(T) = \mathrm{Oler}(a) := \tfrac{a^2}{2} + \tfrac{3a}{2} + 1$ and Oler's route is
$n \le B(H) = \mathrm{Oler}(a) - \mathrm{def}(H)$. Note $\mathrm{Oler}(m) = T(m+1)$ for integer
$m$, where $T(k) = k(k+1)/2$ — the lattice count. That coincidence is the whole story below.

**Corner coordinates.** $h_V(x)$ = the coordinate of $x$ along the internal bisector at corner $V$,
so $h_A(x,y) = \tfrac{\sqrt3}{2}x + \tfrac12 y$ for $A = (0,0)$, and cyclically. The level sets of
$h_V$ are parallel to the opposite side, and

$$\Delta_V(t) \;:=\; T \cap \{h_V \le \tfrac{\sqrt3}{2}t\}$$

is the **closed corner triangle at $V$ of side $t$** (equilateral, for $0 \le t \le a$).

**The target.** Erdős–Oler at $k = 7$ is: $n = 27$ forces $a \ge 6$. Oler's bound alone gives only
$a \ge \tfrac{-3+\sqrt{217}}{2} = 5.86546\ldots$, because $\mathrm{Oler}(6) = 28$. The gap to close
is exactly

$$\varepsilon(a) \;:=\; \mathrm{Oler}(a) - 27 \;=\; \tfrac{a^2}{2} + \tfrac{3a}{2} - 26,
\qquad \varepsilon(6) = 1,$$

and any argument must show $\mathrm{def}(H) + \bigl[B(H) - n\bigr] > \varepsilon(a)$ for
$a < 6$ — where the bracket is Oler's own slack on the hull ("stage 1"). This attack was assigned
the first summand.

---

## 2. The Corner-Deficit Lemma — `sketch`

For each corner $V$ put $c_V = \min_{p \in E} h_V(p)$ and $t_V = 2c_V/\sqrt3$, the side of the
largest corner triangle at $V$ free of points of $E$.

> **Lemma 1.** If $t_U + t_V \le a$ for each pair of corners, then
> $$\mathrm{def}(H) \;\ge\; \sum_{V} \frac{t_V^2 + t_V}{2}.$$

**Proof.** By definition every $p \in E$ has $h_V(p) \ge \tfrac{\sqrt3}{2}t_V$, so
$E \subseteq K := T \cap \bigcap_V \{h_V \ge \tfrac{\sqrt3}{2}t_V\}$, and $K$ is convex, hence
$H = \operatorname{conv}(E) \subseteq K \subseteq T$. Area and perimeter are monotone under
inclusion of convex sets (the perimeter half is the step Oler himself uses on p. 154), so
$\mathrm{def}(H) \ge \mathrm{def}(K)$. Under the hypothesis $t_U + t_V \le a$, $K$ is the hexagon
obtained by slicing the three corner triangles off, so

$$A(K) = A(T) - \tfrac{\sqrt3}{4}\sum_V t_V^2, \qquad M(K) = M(T) - \sum_V t_V$$

— each side of $T$ loses $t_U$ and $t_V$ at its two ends and each cut edge contributes $t_V$ back.
Substituting, $\mathrm{def}(K) = \tfrac{2}{\sqrt3}\cdot\tfrac{\sqrt3}{4}\sum t_V^2 + \tfrac12\sum t_V
= \sum_V \tfrac{t_V^2+t_V}{2}$. $\blacksquare$

**Why $(t^2+t)/2$ and not something else.** Cutting a corner triangle of side $t$ costs area
quadratically and perimeter linearly, and Oler weights them exactly so that the two contributions
combine into the triangular number $T(t) = (t^2+t)/2$ evaluated at a real argument. §5 is where
that stops being a coincidence.

**Exactly verified** (`run.py` §1) on all 12 non-degenerate exact certificates in the repo: the
containment $E \subseteq K$ and the area identity are checked in exact
$\mathbb{Q}(\sqrt3,\sqrt{11})$, so the lemma is certified without ever evaluating the perimeter.
The lemma is **tight** — equality — on every one of them. In particular $t = (0,0,1)$ and
$\sum(t^2+t)/2 = 1$ for $T(k)-\text{apex}$, $k = 3,4,5,6$, reproducing exactly the "stage 2 = 1"
measured in [`../oler-slack-analysis/`](../oler-slack-analysis/) §3.

## 2.1 Corner occupancy — `sketch`

> **Lemma 2.** A closed equilateral triangle of side $t < 1$ contains at most one point of $E$.

**Proof.** Its diameter is $t < 1$. $\blacksquare$

Trivial, but it is the hinge: it is why $t=1$ is the scale at which corner arguments live, and why
$\Delta_V(1)$ can hold three points (its own vertices) while $\Delta_V(1-\epsilon)$ holds one.

---

## 3. Corner-Improved Oler — `sketch`

Lemma 1 is a statement about $H$ alone and therefore blind to how full the corners are. Coupling
the two is the actual content:

> **Theorem 3 (CIO).** Let $E \subseteq T$ be unit-separated, $n = |E|$. Let $t_A,t_B,t_C \ge 0$
> satisfy $t_U + t_V \le a$ for each pair, and put $m_V = |E \cap \Delta_V(t_V)|$. Then
> $$n \;\le\; \frac{a^2}{2} + \frac{3a}{2} + 1 \;-\; \sum_V\Bigl[\frac{t_V^2+t_V}{2} - m_V\Bigr].$$

**Proof.** Let $K$ be the hexagon of Lemma 1's proof, built from the *given* $t_V$ (not from the
configuration), and let $E' = E \setminus \bigcup_V \Delta_V(t_V) \subseteq K$. Then
$|E'| \ge n - \sum_V m_V$. Oler's inequality applied to $E'$, followed by monotonicity
$\operatorname{conv}(E') \subseteq K$, gives $|E'| \le B(K) = \mathrm{Oler}(a) - \sum_V
\tfrac{t_V^2+t_V}{2}$. Combine. $\blacksquare$

**Degenerate $E'$** — Oler's theorem needs a Jordan polygon, so $|E'| \le 2$ or collinear $E'$ must
be handled separately, exactly as [`../oler-lower-bound/`](../oler-lower-bound/) §2.2 does for the
original derivation. All cases give the same bound, elementarily: for $|E'| = 0,1$ use
$B(K) \ge 1$; for $|E'| = 2$ use that a convex set has perimeter $\ge 2\,\mathrm{diam}$, so
$M(K)\ge 2$ and $B(K)\ge 2$; for $m \ge 3$ collinear points the segment they span has length
$\ge m-1$ and lies in $K$, so $M(K) \ge 2(m-1)$ and $B(K) \ge m$.

**Dependencies.** Oler's inequality (`cited`), convex monotonicity of area and perimeter
(elementary; Oler asserts the perimeter half in the same paragraph). The rest is arithmetic. The
theorem itself is `sketch` and **not assumable**, per `RULES.md` §3.

**Sanity.** $t_V = 0$ for all $V$ recovers Oler exactly. The $T(k)-\text{apex}$ configurations give
$t = (0,0,1)$, $m = (0,0,0)$ and hence $n \le \mathrm{Oler}(a) - 1$, which at $a = k-1$ reads
$T(k)-1 \le T(k)-1$: tight.

---

## 4. What CIO buys: a conditional Erdős–Oler — `sketch`

> **Corollary 4.** Let $n = T(k)-1$ points be unit-separated in $T$ of side $a$. If **some** corner
> $V$ has $\Delta_V(1) \cap E = \varnothing$ — an empty closed unit corner triangle — then
> $a \ge k-1$. That is, Erdős–Oler holds for every such configuration, for **every** $k$.

**Proof.** For $a < 1$ the triangle has diameter $< 1$ and holds at most one point, so the claim is
vacuous for $n \ge 2$; assume $a \ge 1$. Apply Theorem 3 with $t_V = 1$ at that corner and $t = 0$
at the other two (admissible since $1 + 0 \le a$), and $m_V = 0$: $n \le \mathrm{Oler}(a) - 1 = \tfrac{a^2}{2}+\tfrac{3a}{2}$. If
$a < k-1$ then $\tfrac{a^2}{2}+\tfrac{3a}{2} < \tfrac{(k-1)^2}{2} + \tfrac{3(k-1)}{2} = T(k)-1 = n$,
a contradiction. $\blacksquare$

More generally, any corner and any $t$ with $\tfrac{t^2+t}{2} - m_V \ge 1$ does the same job; and
letting $t \to j^-$ for an integer $j$, the condition reads *"the open corner triangle of side $j$
holds at most $T(j)-1$ points"* — one fewer than the lattice puts there.

This is the positive residue of the attack. It reduces Erdős–Oler to configurations in which every
corner is **at least as densely occupied as the lattice, at every integer scale**. §9 spells that
out for $k=7$. It is a genuine restriction — but §6 explains why it is also the end of the road.

---

## 5. Neutrality: a corner cut never outvalues what it displaces — `sketch`

Write $N(t)$ for the maximum number of unit-separated points in a closed equilateral triangle of
side $t$, and define the **gain** of a corner cut of side $t$ as
$\mathrm{gain}(t) = \tfrac{t^2+t}{2} - N(t)$: what CIO wins minus the worst case of what it must
give away.

> **Proposition 5.** For all $t \ge 0$, $\;\tfrac{t^2+t}{2} < T(\lfloor t\rfloor + 1) \le N(t)$.
> Hence $\mathrm{gain}(t) < 0$ **strictly**, for every $t$. Its supremum over $t$ is $0$,
> approached as $t \to j^-$ for a positive integer $j$.

**Proof.** The right inequality is the lattice construction: $T(m+1)$ points at separation 1 fit in
the triangle of side $m$, and $m = \lfloor t \rfloor \le t$. For the left, write $t = m+f$ with
$m = \lfloor t\rfloor$, $f \in [0,1)$:
$$\tfrac{t^2+t}{2} - T(m+1) = \tfrac{(m+f)^2 + (m+f) - (m^2+3m+2)}{2} = \tfrac{(f-1)(2m+f+2)}{2} < 0,$$
since $f - 1 < 0$ and $2m+f+2 > 0$. For the supremum, let $t \to j^-$: then
$\lfloor t\rfloor + 1 = j$ and $\tfrac{t^2+t}{2} \to T(j)$, so the difference tends to $0$.
$\blacksquare$

Checked exactly on 32 rational $t$ against both $T(\lfloor t\rfloor+1)$ and the `cited` values of
$N(t)$ for $t \le 4$ (`run.py` §3); the largest difference on that grid is $-0.1797$, at
$t = 7/8$, i.e. just below $1$.

**Reading.** Break-even is approached only from below, at $t \to j^-$: cutting a corner triangle of
side just under $1$ gains just under $1$ and displaces the $1$ lattice point inside it; side just
under $2$ gains just under $3$ and displaces $T(2) = 3$; side just under $j$ gains just under $T(j)$
and displaces $T(j)$. Anywhere else — in particular at $t = j$ *exactly*, where the closed corner
triangle suddenly swallows a whole extra lattice row — the cut is a strict loss. There is no free
lunch anywhere and the best case is exactly break-even. Since Erdős–Oler is precisely about
configurations one point short of the lattice, break-even is exactly not enough.

---

## 6. The Relaxation Barrier — `sketch`. This is the kill.

Proposition 5 is about corner cuts. The same thing is true of **every** convex cut, and for a
sharper reason.

> **Theorem 6 (Barrier).** Let $m \ge 1$ be an integer and $T$ the equilateral triangle of side
> $m$. Then for **every** convex $K \subseteq T$,
> $$\mathrm{def}(K) \;\le\; \bigl|\Lambda \cap (T\setminus K)\bigr| \;\le\; N(T \setminus K),$$
> where $\Lambda \subset T$ is the triangular lattice with $T(m+1)$ points at separation 1.

**Proof.** $\Lambda \cap K$ is unit-separated with $\operatorname{conv}(\Lambda\cap K) \subseteq K$,
so $|\Lambda \cap K| \le B(K) = \mathrm{Oler}(m) - \mathrm{def}(K)$ (degenerate cases as in §3).
But $|\Lambda \cap K| = |\Lambda| - |\Lambda \cap (T\setminus K)| = \mathrm{Oler}(m) -
|\Lambda\cap(T\setminus K)|$, using $|\Lambda| = T(m+1) = \mathrm{Oler}(m)$. Subtract.
$\blacksquare$

**What it says.** Any argument of the shape *"cut a region $R = T\setminus K$ out of $T$, charge the
points it may contain, and apply Oler to what is left"* yields
$n \le \mathrm{Oler}(a) - [\mathrm{def}(K) - N(R)]$, and the bracket is $\le 0$ at every integer
$a$. **At integer side length, no convex-cut relaxation of Oler's inequality improves Oler's
inequality by anything at all.** Corner cuts, strips, inverted middle triangles, arbitrary
half-planes: all exactly neutral or worse, because the lattice certifies tightness of the cut
bound at the same time as it certifies tightness of the original.

Checked exactly at $a = 6$ (`run.py` §4) on 8 single-corner cuts, 6 triple-corner cuts and 90
arbitrary half-plane cuts with rational normals. Largest observed gain: $0$, attained exactly when the removed
region $T \setminus K$ is an *open* corner triangle of integer side (and, trivially, when $K = T$).

**And for $a<6$, where the target actually lives.** Fix $a \le 6$, embed $T_a \subseteq T_6$ and let
$K \subseteq T_a$ be convex. Since $\mathrm{def}_a(K) = \mathrm{Oler}(a) - B(K)$, we get
$\mathrm{def}_a(K) = \mathrm{def}_6(K) - [\mathrm{Oler}(6)-\mathrm{Oler}(a)]$, so by Theorem 6

$$\underbrace{\mathrm{def}_a(K) - N(T_a\setminus K)}_{\text{gain in } T_a}
\;\le\; \underbrace{\bigl[N(T_6\setminus K) - N(T_a\setminus K)\bigr]}_{\text{a difference of integer counts}}
\;-\; \bigl[\mathrm{Oler}(6)-\mathrm{Oler}(a)\bigr].$$

For $a \to 6^-$ the subtracted term vanishes and the required gain tends to $\varepsilon(6) = 1$.
So **every last bit of the missing unit must come from the cut region's capacity dropping when the
triangle shrinks** — a strictly integer-valued, $\lfloor a \rfloor$-flavoured statement — and
**none of it can come from the area/perimeter deficit**, which is continuous in $a$ and pinned by
Theorem 6. That is the precise sense in which this route is dead: it is not that the relaxation is
weak, it is that the relaxation is *exactly* as strong as Oler and no stronger.

It also explains, after the fact, why the conjecture that
[`../oler-slack-analysis/`](../oler-slack-analysis/) §5 arrived at has $\lfloor a\rfloor$ in it. The
floor is not decoration; by Theorem 6 it is the only place a strengthening can live.

---

## 7. The witness: the corner route buys zero unconditionally — `numerical`

Theorem 6 quantifies over all convex $K$ at once. Here is the concrete version of the same
thing, at the first open case, in a single explicit configuration.

> Take the triangular lattice $T(7)$ in the triangle of side $a = 6$ — 28 points at separation
> exactly 1 — and delete one **interior** point, e.g. $(\tfrac32, \tfrac{\sqrt3}{2})$. The result
> is a unit-separated $E$ with $n = 27$, $a = 6$.

Verified exactly (`run.py` §6): separation $\ge 1$ on all $\binom{27}{2}$ pairs, containment in $T$,
and

- all three corners of $T$ are occupied, so $t_A = t_B = t_C = 0$ and the corner deficit is $0$;
- $H = \operatorname{conv}(E) = T$ exactly (equality of areas in exact arithmetic), so
  $\mathrm{def}(H) = 0$;
- the entire slack $\mathrm{Oler}(6) - 27 = 1$ sits in **stage 1**, Oler's inequality on the hull.

So no inequality of the form $\mathrm{def}(H) \ge f(a,n)$ with $f(6,27) > 0$ can hold, and CIO's
corner gains are all $0$ here. The route closes **exactly $0$** of the missing $1.0$
unconditionally. What it closes conditionally is all of it (§4) — on the complementary class.

The witness also relocates the problem one final time, sharpening
[`../oler-slack-analysis/`](../oler-slack-analysis/) §3's finding. That attack measured that at
$n = T(k)-1$ *the known extremal configuration* puts all its slack in stage 2. What is true in
general is the opposite: a counterexample would be free to put all of it in stage 1, and the above
shows a 27-point configuration doing exactly that already exists at $a = 6$. **Erdős–Oler is a
statement about stage 1 — about Oler's inequality applied to a hull that is the whole triangle.**

---

## 8. A Steiner-type alternative, refuted

The manager's brief suggested a support-function/Steiner-type route relating $A(T)-A(H)$ to
$M(T)-M(H)$. The natural such bound, with $\mu = M(T)-M(H)$, is

$$\mathrm{def}(K) \;\ge\; \frac{\mu^2}{6} + \frac{\mu}{2},$$

which is *exactly tight* for three equal corner cuts ($\mu = 3t$, both sides $\tfrac{3(t^2+t)}{2}$)
— which is what makes it tempting, and it does hold for shallow cuts.

**It is false.** `refuted`, by an exact witness (`run.py` §7): take $a = 6$ and $K$ the triangle of
side $6-u$ obtained by slicing a strip off one side, for which $\mathrm{def}(K) = au - \tfrac{u^2}{2}
+ \tfrac{3u}{2}$ and $\mu = 3u$. At $u = 4$: $\mathrm{def} = 22$ against a claimed $30$; at $u = 6$
($K$ a point): $27$ against $63$. The three-corner-cut family is extremal only for small $\mu$;
deep cuts are much cheaper per unit of perimeter. Any correct Steiner-type statement here needs a
$\mu$-dependent regime split — and by Theorem 6 it would buy nothing anyway.

---

## 9. Necessary conditions on a $k = 7$ counterexample — `sketch`

Kept because it is the usable residue, and because a later exhaustion-style attack can consume it
directly. Suppose, for contradiction, that 27 unit-separated points lie in $T$ of side $a < 6$; put
$\varepsilon = \varepsilon(a) = \tfrac{a^2}{2}+\tfrac{3a}{2}-26 \in [0,1)$. Theorem 3 says

$$\sum_V \Bigl[\frac{t_V^2+t_V}{2} - m_V\Bigr] \;\le\; \varepsilon \qquad
\text{for all admissible } (t_A,t_B,t_C).$$

**Headline form.** Taking one corner at a time, $t_V \to j^-$ for an integer $j \le a$ and $t = 0$
elsewhere, Corollary 4 read contrapositively gives: *for every corner $V$ and every integer
$1 \le j \le 5$, the open corner triangle $\Delta_V(j)^\circ$ contains at least $T(j)$ points of
$E$* — at least as many as the lattice puts there. So $\ge 1$ point within side 1 of each corner,
$\ge 3$ within side 2, $\ge 6$ within side 3, $\ge 10$ within side 4, $\ge 15$ within side 5.

**Sharper, using all three corners at once.** Taking $t_A=t_B=t_C=t$ (admissible for $t \le a/2$)
gives $\sum_V m_V \ge \tfrac{3(t^2+t)}{2} - \varepsilon$, so $\sum_V m_V > c$ for every $t$ with
$\tfrac{3(t^2+t)}{2} - \varepsilon > c$. Two instances, both exact:

1. **Every corner is occupied.** With $t^\ast(a)$ the root of $\tfrac{t^2+t}{2} = \tfrac{2+\varepsilon}{3}$,
   each $\Delta_V(t^\ast)$ contains a point of $E$ — and by Lemma 2 exactly one, since
   $t^\ast(a) < 1$ for $a < 6$. Values: $t^\ast(5.9) = 0.8241\ldots$, $t^\ast(5.99) = 0.9832\ldots$,
   $t^\ast(5.999) = 0.99833\ldots$
2. **The corners are lattice-dense at scale 2.** With $t^+(a)$ the root of
   $\tfrac{t^2+t}{2} = \tfrac{8+\varepsilon}{3}$, the three triangles $\Delta_V(t^+)$ contain at
   least 9 points between them. Values: $t^+(5.9) = 1.8986\ldots$, $t^+(5.99) = 1.9899\ldots$,
   $t^+(5.999) = 1.99900\ldots$

In one sentence: **every corner must be at least as occupied as the lattice, at every integer
scale.** And by Proposition 5 that requirement is never self-contradictory — the "need" column never exceeds the "available" column in `run.py` §5,
at any $a$ or $t$ tested, which is exactly what Theorem 6 predicts must happen.

---

## 10. Honest accounting

**What I am least sure of.** Theorem 3's handling of the region $K$ when the $t_V$ are not those of
the configuration but chosen freely: the step $|E'| \ge n - \sum_V m_V$ is fine even if the corner
triangles overlap (it is an inclusion–exclusion inequality in the safe direction), but the closed
forms for $A(K)$ and $M(K)$ **require** $t_U + t_V \le a$ for each pair, and without that hypothesis
the theorem is *false*, not merely unproven — the formula would subtract overlapping corner
triangles twice. Every use above respects the hypothesis; a reader reusing Theorem 3 must check it.
The second-least-sure step is the degenerate-$E'$ case analysis in §3, which I wrote out rather than
inherited.

**Novelty: UNVERIFIED, and I would assume not.** Theorem 6 is three lines from Oler's inequality
and the lattice; anyone who has thought about why the Erdős–Oler conjecture is hard has probably
noticed it. Corollary 4 is the kind of statement Payan's $k=5,6$ proof would open with. The prior
art to check is Payan (1997) — whose body this repo has never obtained, see
[`../../README.md`](../../README.md) — and Folkman–Graham, already flagged as unreachable at this
session's proxy in [`../oler-slack-analysis/`](../oler-slack-analysis/) §6. **Assume all of §§2–6 is
known until someone with library access says otherwise.**

**What is not claimed.** Nothing here bounds $s(n)$ for any $n$. Corollary 4 is conditional on a
hypothesis that no configuration is known to satisfy at the interesting $a$, and is `sketch`, so it
is not assumable even by me. The Erdős–Oler conjecture is untouched.

**Not checked.** Whether Theorem 6's converse-flavoured question has an answer — i.e. what the
largest $n$ is that fits in $T(a)$ for $a$ slightly below an integer, which is the counting
statement §6 says everything now depends on. Whether the same barrier applies to *non-convex* cut
regions (it does not obviously; but a non-convex $K$ breaks the monotonicity step that makes the
cut usable in the first place). Whether stage-1 stability — a quantitative version of "equality in
Oler forces a lattice" — is reachable; that is the question [`../oler-lower-bound/`](../oler-lower-bound/)
§5.2 already names, and §7 above is a second, independent reason to want it.

**Next agent on this route: don't take this route.** Take §7 seriously — the target is a *stability*
theorem for Oler's inequality on a hull equal to the whole triangle, or the integer counting
statement isolated in §6. Both are harder than what was tried here, and both are where the unit
actually is.
