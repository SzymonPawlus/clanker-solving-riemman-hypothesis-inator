# Round-4 attack AC: the container-$\vartheta'$ kernel bound — **the claim that dies is "independent of $n$"**

```
claim type:  NEITHER construction nor optimality.  No bound on d(n) or s(n) is asserted
             anywhere in this file, for any n.  This is a measurement of a relaxation and
             an argument about its cost.
status:      `numerical` for every computed number; `sketch` for every argument, including
             every lemma below.  Nothing here is assumable (RULES.md §3), including by me.
author:      claude (Opus 5, convergent role per RULES.md §8 — the model that generated
             proposal AC was Fable 5, and is not this one), 2026-08-24
worker:      r4-theta, branch r4-theta
executes:    proposal AC of ../r3-approaches/README.md
code:        ../../../../experiments/packing-r4-theta/   (one reproduce command)
neighbour:   ../r3-sdpgate/  — the completed negative result on the *coordinate* moment
             hierarchy.  This file deliberately does NOT reuse its verdict; see §5.
```

**Kill-criterion: NOT fired** (and it turned out to be aimed at the wrong quantity — see
[`KILL-CRITERION.md`](./KILL-CRITERION.md)). What replaced it is a cost argument that does
kill the proposal's headline claim.

---

## 1. The verdict in four lines

1. **AC's dominance claim is correct.** $\vartheta'$ really does sit above every
   diameter-cover bound; §2.3 re-derives the required kernel explicitly instead of citing
   the sandwich. So the question "does it beat Oler?" has an a-priori answer, *yes*, and is
   not the interesting question.
2. **AC's headline claim is false.** "An SOS problem in $\sim4$ variables, **independent of
   $n$**" is true of the variable count and false of everything that determines the cost:
   §2.4 forces kernel degree $m \gtrsim \sqrt{2n}$, hence SDP blocks $\sim n^2/6$ and
   scalar variables $\sim n^4$.
3. **`r3-sdpgate`'s ceiling has no analogue here.** $d_2(n) \le \sqrt6$ was *bounded*;
   §2.5 shows $\vartheta'(G_d) = \Theta(d^2)$, so the $\vartheta'$ floor grows like
   $\sqrt n$ — the right order. This family of relaxations is **not** flat.
4. **The cheap measurement found no weakness at all** — over 20 solves at seven values of
   $n$, $\vartheta'$ on a finite witness never reached $n$, and at $n = 16$, $d = \sqrt{129}-3$
   it came back at exactly $\alpha = 15$. That is a null result and **not** evidence for AC:
   the instrument (§3) is one-sided by construction and can only ever detect weakness. §4.4
   says exactly how blunt it is and why.

---

## 2. The formulation, and four lemmas

Repo conventions throughout (`../../RULES.md` §2): $T_d$ is the **closed** equilateral
triangle $A = (0,0)$, $B = (d,0)$, $C = (d/2,\ d\sqrt3/2)$; all inequalities non-strict;
$s = 2\sqrt3 + d$.

### 2.0 The optimisation being solved

Let $G_d$ be the graph with vertex set $T_d$ and $\{x,y\} \in E$ iff $0 < \lVert x-y\rVert
< 2$. An independent set of $G_d$ is exactly a set of points at pairwise distance $\ge 2$,
so $\alpha(G_d)$ is the maximum number of points and

$$d(n) \;=\; \min\{\, d \;:\; \alpha(G_d) \ge n \,\}.$$

**The kernel variable.** A symmetric continuous kernel $Z : T_d \times T_d \to \mathbb{R}$
that is positive semidefinite (every finite Gram matrix $\big(Z(x_i,x_j)\big)$ is psd).

**The constraints.**

$$Z(x,x) \le \lambda - 1 \quad \forall x \in T_d, \qquad\qquad
Z(x,y) \le -1 \quad \forall x \ne y \text{ with } \lVert x - y\rVert \ge 2 .$$

**The value.** $\vartheta'(G_d) = \inf\{\lambda : \text{some } Z \text{ is feasible}\}$.

This is the "prime" variant of Lovász theta — for a finite graph it is the dual of
$\max\{\langle J,B\rangle : B \succeq 0,\ B \ge 0 \text{ entrywise},\ \operatorname{tr}B = 1,\
B_{ij} = 0 \text{ on edges}\}$, and the entrywise $B \ge 0$ is what turns $\vartheta$ into
$\vartheta'$. (Derived in the docstring of `theta_gate.py`; not taken on faith.)

**How a feasible solution becomes a lower bound on $d(n)$.**

> **Lemma 1 (soundness).** $\alpha(G_d) \le \vartheta'(G_d)$. Hence
> $$\vartheta'(G_d) < n \;\Longrightarrow\; \alpha(G_d) < n \;\Longrightarrow\; d(n) > d .$$

*Proof (`sketch`, re-derived here, no citation used).* Let $S$ be independent, $|S| = m$,
and $Z$ feasible with value $\lambda$. Positive semidefiniteness gives
$\sum_{x,y \in S} Z(x,y) \ge 0$. The $m$ diagonal terms are each $\le \lambda - 1$ and the
$m(m-1)$ off-diagonal terms are each $\le -1$ (every off-diagonal pair of $S$ is a
non-edge), so $0 \le m(\lambda - 1) - m(m-1)$, i.e. $\lambda \ge m$. $\square$

So the **best floor this method can ever produce** is

$$d_{\vartheta'}(n) \;:=\; \sup\{\, d : \vartheta'(G_d) < n \,\} \;\le\; d(n).$$

### 2.1 What "compute it" would mean

Restricting to kernels $Z(x,y) = v_m(x)^{\mathsf T} C\, v_m(y)$ with $C \succeq 0$ and
$v_m$ the vector of monomials of degree $\le m$ in two variables turns the two constraint
families into polynomial non-negativity conditions on

$$\{x \in T_d\} \subset \mathbb{R}^2 \qquad\text{and}\qquad
\Sigma_d := \{(x,y) : x \in T_d,\ y \in T_d,\ \lVert x-y\rVert^2 \ge 4\} \subset \mathbb{R}^4,$$

each discharged by a Putinar SOS certificate. **Four variables**, as AC says — $\Sigma_d$
carries seven defining inequalities (three half-planes per point, one separation). That is
the object AC proposes to solve. I did not solve it; §2.4 is about what it would cost, and
§6 says plainly that not solving it is the main gap in this file.

### 2.2 The ceiling lemma — why a negative result here needs no SOS at all

> **Lemma 2 (ceiling).** For every **finite** $W \subset T_d$,
> $\ \vartheta'(G_d[W]) \le \vartheta'(G_d)$.
> Consequently, if some finite $W$ has $\vartheta'(G_d[W]) \ge n$, then
> $d_{\vartheta'}(n) \le d$.

*Proof (`sketch`).* A feasible kernel $Z$ for $G_d$ restricts to the matrix
$\big(Z(w,w')\big)_{w,w' \in W}$, which is psd, has diagonal $\le \lambda - 1$, and has
every non-adjacent off-diagonal entry $\le -1$ — the constraints of $G_d[W]$ are a
*subset* of those of $G_d$. So every $\lambda$ feasible for $G_d$ is feasible for
$G_d[W]$. $\square$

This is the whole instrument. **Finite subgraphs give upper bounds on the $\vartheta'$
floor**, against *every* kernel of *every* degree, with no SOS machinery — and finite
$\vartheta'$ is one ordinary SDP. It is the cheapest possible refutation device for this
family. It is also strictly **one-sided**: a grid value *below* $n$ says nothing, because
the grid only lower-bounds $\vartheta'(G_d)$.

### 2.3 AC's dominance claim, checked

> **Lemma 3.** If $T_d$ can be covered by $N$ sets each of diameter $< 2$, then
> $\vartheta'(G_d) \le N$.

*Proof (`sketch`, explicit kernel rather than the cited sandwich).* Each covering set is a
clique of $G_d$; let $c(x)$ be the index of a set containing $x$. Put
$\phi(x) = \sqrt N\, e_{c(x)} - \tfrac{1}{\sqrt N}\mathbf 1 \in \mathbb{R}^N$ and
$Z(x,y) = \langle \phi(x), \phi(y)\rangle$, which is psd by construction. Then
$Z(x,y) = -2 + 1 = -1$ when $c(x) \ne c(y)$ — in particular for every non-adjacent pair,
since non-adjacent points cannot share a clique — and $Z(x,x) = N - 1$. So $\lambda = N$
is feasible. $\square$

So the $\vartheta'$ floor is at least the floor of every diameter-cover argument. **AC is
right about this**, and it is why "does $\vartheta'$ beat Oler?" is not a real gate: the
covering plateau recorded in PRs #98/#104 ($d(16) \ge 2 + 4\sqrt3 = 8.9282\ldots$,
`sketch`, unmerged, **not used as a dependency here** — quoted only to locate the
question) already exceeds Oler's $\sqrt{129} - 3 = 8.3578\ldots$, and Lemma 3 hands that
same floor to $\vartheta'$ for free.

### 2.4 The rank obstruction — where "independent of $n$" dies

> **Lemma 4 (rank).** Every feasible kernel has $\operatorname{rank} Z \ge \alpha(G_d) - 1$.
> If $Z$ has degree $\le m$ in each argument, then
> $$\binom{m+2}{2} \;\ge\; \alpha(G_d) - 1 .$$

*Proof (`sketch`).* Write $Z(x,y) = \langle \phi(x), \phi(y)\rangle$ with $\phi$ into
$\mathbb{R}^r$, $r = \operatorname{rank} Z$. For an independent set $S$, the vectors
$\{\phi(x)\}_{x \in S}$ have pairwise inner products $\le -1 < 0$. In $\mathbb{R}^r$ at
most $r+1$ vectors can be pairwise strictly obtuse (classical), so
$\alpha(G_d) \le r + 1$. For a kernel of bidegree $\le (m,m)$ one may take
$\phi(x) = C^{1/2} v_m(x)$, so $r \le \dim v_m = \binom{m+2}{2}$. $\square$

Since $\alpha(G_d) \approx d^2/8 \approx n$ near $d = d(n)$, and $d(n) \approx \sqrt{8n}$:

$$\binom{m+2}{2} \gtrsim n \qquad\Longrightarrow\qquad m \;\gtrsim\; \sqrt{2n}\, .$$

The number of *variables* is 4 for every $n$. The *degree* is not, and the SOS problem's
size is set by the degree. Concretely, with $m$ the least degree Lemma 4 permits and the
Putinar multiplier blocks indexed by monomials of degree $\le m$ in **4** variables:

| $n$ | $\alpha - 1$ | least $m$ with $\binom{m+2}{2} \ge \alpha-1$ | multiplier block $\binom{m+4}{4}$ | scalar vars $\sim \binom{m+4}{4}^2$ |
|---:|---:|---:|---:|---:|
| 8 | 7 | 3 | 35 | $\sim 6\times10^2$ |
| 16 | 15 | 4 | 70 | $\sim 5\times10^3$ |
| 21 | 20 | 5 | 126 | $\sim 1.6\times10^4$ |
| 34 | 33 | 7 | 330 | $\sim 1.1\times10^5$ |
| 100 | 99 | 13 | 2380 | $\sim 5.7\times10^6$ |

Growth $\binom{m+4}{4} \sim m^4/24 \sim n^2/6$, so scalar variables $\sim n^4$. That is far
better than the $2n$-variable coordinate hierarchy of `r3-sdpgate` — but it is emphatically
**not** independent of $n$, and the claim that it is was AC's whole reason to exist. (The
lemma constrains *polynomial* kernels. A non-polynomial kernel can have large rank cheaply;
the lemma is about the SOS route AC proposes, and only that.)

At $n = 16$ the required instance is small — a $70 \times 70$ block and seven $\sim
35 \times 35$ ones — which is why §6 lists "actually solve it" as the honest next step
rather than a formality.

### 2.5 No `r3-sdpgate` ceiling: $\vartheta'$ is $\Theta(d^2)$

`r3-sdpgate` died because $d_2(n) = \sqrt{6(n-1)/n}$ is **bounded** by $\sqrt6$ while
$d(n)$ grows. Nothing of the sort happens here:

* **Below:** $\vartheta'(G_d) \ge \alpha(G_d) \ge \Delta(\lfloor d/2\rfloor + 1) = \Omega(d^2)$
  (the triangular lattice packing, `cited` at $d = 2(k-1)$).
* **Above:** cover $T_d$ by regular hexagons of circumradius $\rho < 1$ (diameter $2\rho < 2$,
  area $\tfrac{3\sqrt3}{2}\rho^2$) from the hexagonal tiling; Lemma 3 then gives
  $\vartheta'(G_d) \le \frac{\sqrt3 d^2/4}{(3\sqrt3/2)\rho^2} + O(d) \to \frac{d^2}{6} + O(d)$.

So $\tfrac{d^2}{8}(1-o(1)) \le \vartheta'(G_d) \le \tfrac{d^2}{6}(1+o(1))$, and therefore

$$\sqrt{6n} - O(1) \;\le\; d_{\vartheta'}(n) \;\le\; d(n) .$$

Both ends are $\Theta(\sqrt n)$: **the relaxation is not flat.** The repo now has one
structurally flat convex relaxation (`r3-sdpgate`) and one structurally sound but expensive
one (this), and they should not be filed under the same heading.

For orientation against Oler's $\sqrt{8n+1}-3 \approx 2.828\sqrt n - 3$: the *guaranteed*
end $\sqrt{6n} = 2.449\sqrt n$ crosses below Oler around $n \approx 60$, so the covering-
inherited part of $\vartheta'$ stops helping asymptotically. Whether $\vartheta'$ itself
does is the open question this file does not answer.

---

## 3. The instrument, and its validation (`RULES.md` §6)

`theta_gate.py --selftest`, all passing before any measurement was taken:

| test | expected | got |
|---|---|---|
| $\vartheta'(K_5)$ | 1 | 1.000000 |
| $\vartheta'(\overline{K_6})$ | 6 | 6.000000 |
| $\vartheta'(C_5)$ | $\sqrt5$ | 2.236068 |
| $\vartheta'(\text{Petersen})$ | 4 | 4.000000 |
| $\alpha \le \vartheta' \le \bar\chi_f$ on 6 random graphs | sandwich holds | holds, 6/6 |
| corner grid $\alpha$ in $T_{2(k-1)}$, $k = 3,4,5,6$ | $\Delta(k) = 6,10,15,21$ | exact match |
| corner grid $\alpha$ in $T_6, T_8$ on **refined** grids (55, 91, 153 pts) | $10$, $15$ | exact match |
| anchored grid $\alpha$ in $T_6, T_8, T_{10}$ (190–325 pts) | $10$, $15$, $21$ | exact match |

The geometry rows are the ones that matter: they check the conflict graph, the triangle
placement and the non-strict distance convention against the `cited` exact values at the
triangular numbers, on grids finer than the packing itself, where an off-by-one in the
adjacency test would show up immediately. The $C_5$ row matters for a different reason: it
is the smallest witness that this code *can* see $\vartheta' > \alpha$, which is what §4
reports it failing to see geometrically.

**Adjacency is decided exactly, not by tolerance.** On the $k$-per-side triangular grid with
spacing $h = d/(k-1)$, two lattice points differing by $(a,b)$ are at squared distance
$h^2(a^2+ab+b^2)$, so the test "$< 4$" is the integer-versus-algebraic comparison
$a^2+ab+b^2 < 4(k-1)^2/d^2$, resolved symbolically in `sympy`. Exact ties occur (they are
exactly the pairs at distance $2$, e.g. whenever $d = 2(k-1)$) and are resolved as
**non**-edges, per the non-strict convention.

**Two families of witness $W$ were used.** The *corner-to-corner* grid above, and — after
the first battery exposed the defect described in §4.4 — a *lattice-anchored* grid of
spacing exactly $2/r$ anchored at the corner $A$, which contains the triangular packing and
whose adjacency test degenerates to the pure integer comparison $a^2+ab+b^2 < r^2$. Both are
admissible in Lemma 2 (any finite $W$ is), and the anchored one is the sharper instrument.

**Every reported $\vartheta'$ is a repaired-primal lower bound, not solver output.** The
solver's $B$ is symmetrised, zeroed on edges, clipped to be entrywise non-negative, shifted
by $tI$ to restore positive semidefiniteness, and rescaled to unit trace; the objective is
then evaluated at that exactly-feasible point. Solver inaccuracy can only make this number
*smaller*, never invalid — which is the direction Lemma 2 needs. (It is still `numerical`:
the eigenvalue and the sum are float64. A fully rigorous version would round $B$ to
rationals and certify positive semidefiniteness exactly; not done.)

---

## 4. The measurements

All values `numerical`. Every $\vartheta'$ entry is a **repaired-primal lower bound** on
$\vartheta'(G_d[W])$, hence (Lemma 2) a lower bound on $\vartheta'(G_d)$. The gate fires at a
row iff that value reaches $n$.

### 4.1 Refinement ladder — the instrument, not the quantity

*n = 8 at d = Oler's floor, corner-to-corner grid.  The reported value is a repaired-primal LOWER bound, so a coarse grid whose solve converges beats a fine grid whose solve does not.*

| refine | pts/side | N | spacing | alpha(grid) | theta'(grid) >= | solver value | status | solve |
|---:|---:|---:|---:|---:|---:|---:|:--|---:|
| 4 | 11 | 66 | 0.506 | 6 | 5.9997 | 6.0001 | `optimal` | 1 s |
| 6 | 16 | 136 | 0.337 | 6 | 5.9550 | 6.0076 | `optimal` | 41 s |
| 8 | 21 | 231 | 0.253 | 6 | 5.5738 | 6.1219 | `optimal_inaccurate` | 80 s |
| 10 | 26 | 351 | 0.202 | 6 | 4.9987 | 6.2704 | `optimal_inaccurate` | 81 s |

### 4.2 The gate table

*Best (largest) certified value per (n, probe).  The gate fires iff it reaches n.*

*`gain` is theta' minus alpha on the same witness.  theta' >= alpha always (Lemma 1), so a NEGATIVE gain means only that the repaired-primal bound fell short of the truth because the solve did not converge inside its cap — read those rows as "at least alpha".*

| n | known d(n) | Oler floor | d probe | what d is | witness | N | alpha(grid) | theta'(grid) >= | gain | reaches n? |
|---:|---:|---:|---:|:--|:--|---:|---:|---:|---:|:--|
| 3 | 2.000000 | 2.000000 | 1.990000 | just-below-d(n) | corner | 28 | 1 | 1.0000 | +0.0000 | **no** |
| 6 | 4.000000 | 4.000000 | 3.990000 | just-below-d(n) | corner | 91 | 4 | 3.9971 | -0.0029 | **no** |
| 8 | 5.829708 | 5.062258 | 5.819708 | just-below-d(n) | corner | 171 | 7 | 7.3368 | +0.3368 | **no** |
| 8 | 5.829708 | 5.062258 | 5.819708 | just-below-d(n) | anchored | 171 | 7 | 7.3368 | +0.3368 | **no** |
| 8 | 5.829708 | 5.062258 | 5.062258 | oler-floor | corner | 66 | 6 | 5.9997 | -0.0003 | **no** |
| 8 | 5.829708 | 5.062258 | 5.062258 | oler-floor | anchored | 136 | 6 | 5.9550 | -0.0450 | **no** |
| 10 | 6.000000 | 6.000000 | 5.990000 | just-below-d(n) | corner | 190 | 7 | 7.3150 | +0.3150 | **no** |
| 12 | 7.464102 | 6.848858 | 7.454102 | just-below-d(n) | corner | 276 | 11 | 9.9881 | -1.0119 | **no** |
| 12 | 7.464102 | 6.848858 | 7.454102 | just-below-d(n) | anchored | 276 | 11 | 10.0900 | -0.9100 | **no** |
| 12 | 7.464102 | 6.848858 | 6.848858 | oler-floor | corner | 253 | 10 | 9.9488 | -0.0512 | **no** |
| 12 | 7.464102 | 6.848858 | 6.848858 | oler-floor | anchored | 231 | 10 | 9.8698 | -0.1302 | **no** |
| 15 | 8.000000 | 8.000000 | 7.990000 | just-below-d(n) | corner | 153 | 10 | 10.4471 | +0.4471 | **no** |
| 16 | *open* | 8.357817 | 8.357817 | oler-floor | corner | 351 | 15 | 13.6627 | -1.3373 | **no** |
| 16 | *open* | 8.357817 | 8.357817 | oler-floor | anchored | 153 | 15 | 14.9999 | -0.0001 | **no** |
| 21 | 10.000000 | 10.000000 | 9.990000 | just-below-d(n) | corner | 231 | 15 | 14.3735 | -0.6265 | **no** |

### 4.3 Every record

| n | label | d | refine | N | non-edges | alpha | theta' >= | solver | status | build | solve |
|---:|:--|---:|---:|---:|---:|---:|---:|---:|:--|---:|---:|
| 8 | oler-floor | 5.0623 | 4 | 66 | 1134 | 6 | 5.9997 | 6.0001 | `optimal` | 1.3 s | 0.7 s |
| 8 | oler-floor | 5.0623 | 6 | 136 | 4620 | 6 | 5.9550 | 6.0076 | `optimal` | 2.3 s | 40.7 s |
| 12 | oler-floor | 6.8489 | 6 | 253 | 20700 | 10 | 9.9488 | 10.0089 | `optimal` | 5.6 s | 22.7 s |
| 16 | oler-floor | 8.3578 | 6 | 351 | 46515 | 15 | 13.6627 | 15.0886 | `optimal_inaccurate` | 8.1 s | 80.4 s |
| 8 | just-below-d(n) | 5.8197 | 6 | 171 | 8385 | 7 | 7.3368 | 7.3642 | `optimal` | 1.5 s | 29.5 s |
| 3 | just-below-d(n) | 1.9900 | 6 | 28 | 0 | 1 | 1.0000 | 1.0000 | `optimal` | 0.0 s | 0.0 s |
| 6 | just-below-d(n) | 3.9900 | 6 | 91 | 1386 | 4 | 3.9971 | 4.0014 | `optimal` | 0.0 s | 5.2 s |
| 10 | just-below-d(n) | 5.9900 | 6 | 190 | 10647 | 7 | 7.3150 | 7.3662 | `optimal` | 0.1 s | 50.4 s |
| 15 | just-below-d(n) | 7.9900 | 4 | 153 | 8463 | 10 | 10.4471 | 10.4940 | `optimal` | 0.2 s | 16.9 s |
| 21 | just-below-d(n) | 9.9900 | 4 | 231 | 21420 | 15 | 14.3735 | 15.0685 | `optimal_inaccurate` | 0.3 s | 80.6 s |
| 12 | just-below-d(n) | 7.4541 | 6 | 276 | 26775 | 11 | 9.9881 | 11.0438 | `optimal_inaccurate` | 2.4 s | 80.5 s |
| 8 | oler-floor | 5.0623 | 8 | 231 | 12636 | 6 | 5.5738 | 6.1219 | `optimal_inaccurate` | 4.1 s | 80.3 s |
| 8 | oler-floor | 5.0623 | 10 | 351 | 27828 | 6 | 4.9987 | 6.2704 | `optimal_inaccurate` | 7.4 s | 81.0 s |
| 16 | oler-floor | 8.3578 | 4 | 171 | 10920 | 11 | 10.8898 | 11.1470 | `optimal_inaccurate` | 4.2 s | 80.3 s |
| 8 | oler-floor-anchored | 5.0623 | 6 | 136 | 4620 | 6 | 5.9550 | 6.0076 | `optimal` | 0.1 s | 41.1 s |
| 12 | oler-floor-anchored | 6.8489 | 6 | 231 | 17580 | 10 | 9.8698 | 10.0090 | `optimal` | 0.3 s | 64.7 s |
| 16 | oler-floor-anchored | 8.3578 | 4 | 153 | 8736 | 15 | 14.9999 | 15.0000 | `optimal` | 0.1 s | 3.3 s |
| 16 | oler-floor-anchored | 8.3578 | 6 | 351 | 46515 | 15 | 13.7869 | 15.0760 | `optimal_inaccurate` | 0.6 s | 90.8 s |
| 8 | just-below-d(n)-anchored | 5.8197 | 6 | 171 | 8385 | 7 | 7.3368 | 7.3642 | `optimal` | 0.3 s | 29.1 s |
| 12 | just-below-d(n)-anchored | 7.4541 | 6 | 276 | 26775 | 11 | 10.0900 | 11.0381 | `optimal_inaccurate` | 0.4 s | 90.6 s |

*(Generated by `make_table.py` from `results.json`; not hand-typed.)*

### 4.4 How blunt the instrument is, and why the null result is weak evidence

Two things limit it, and they compound:

1. **A grid cannot represent a packing at a generic $d$.** The corner-to-corner grid has
   spacing $d/(k-1)$, incommensurate with the packing distance 2, so it contains **no** pair
   at distance exactly 2. At $d = 7.99$ the container holds 14 points but the grid witness
   found $\alpha = 10$. The lattice-anchored grid (spacing exactly $2/r$) repairs this at
   $d$ that are multiples of 2 — it reproduces $\Delta(k)$ exactly at $d = 2(k-1)$, which is
   the self-test in §3 — but just *below* a critical $d$ the optimal configuration is not on
   any lattice, and the anchored grid still undershoots. So the witness undershoots
   $\alpha(G_d)$ precisely where the gate needs it to overshoot.
2. **The gap that would have to be crossed is $\ge 1$, and the observed gaps are $< 1/2$.**
   Where the witness does reproduce $\alpha(G_d)$ — at $d$ well below $d(n)$, i.e. the
   `oler-floor` rows — the measured $\vartheta'$ sits *on* $\alpha$ to within a few
   thousandths. The cleanest instance is the one that matters most: at $n = 16$,
   $d = \sqrt{129}-3$, the anchored 153-point witness has $\alpha = 15$, which is exactly
   $\alpha(G_d)$ here (since $d(15) = 8 \le d < d(16)$), and its $\vartheta'$ came back
   $15.0000$ in a converged 3-second solve. Where $\vartheta'$ does exceed $\alpha$ it does
   so by at most $+0.447$ (the $n = 15$ row). Firing the gate from $\alpha = n-1$ requires a
   gain of a full $1$, and nothing here got close.

So the honest reading of §4 is **"no ceiling detected by this instrument"**, not
"$\vartheta'$ is strong". A sharper witness is the obvious next attempt: circulant-shaped
point sets have $\vartheta' > \alpha$ by a fractional amount ($C_5$ in the §3 self-test is
the smallest instance of exactly that), so rings of equally spaced points, or a
ring-augmented grid, could plausibly buy the missing unit. Not attempted here.

---

## 5. What this means for the board

- **AC is not the same kind of object as `r3-sdpgate`'s proposal X, and the sdpgate verdict
  must not be extended to it.** X died because its value saturated; $\vartheta'$ does not
  saturate (§2.5). Anyone reading "SDP methods are dead here" as a blanket statement will be
  reading something this file does not say.
- **AC's dominance claim survives** (§2.3) and is worth keeping on the board as a fact about
  the *ordering* of methods: any diameter-cover floor the covering campaign produces is
  automatically a $\vartheta'$ floor.
- **AC's cost claim does not survive** (§2.4). The proposal should be re-recorded as
  "4-variable SOS with degree growing like $\sqrt n$", which is a materially different and
  much less attractive proposition than "size independent of $n$".
- **What is *not* refuted.** The $n = 16$ SOS instance itself. It is small (§2.4), it was
  never run, and it is the only thing that would turn any of this into a number.
- **A reusable tool.** Lemma 2 plus `theta_gate.py` is a cheap, general refutation device
  for *any* $\vartheta$-family proposal on this problem: build a finite witness, solve one
  SDP, and either the method is provably capped below the target or it is not.

---

## 6. What I am least sure of

**The thing I did not do.** I never solved the SOS problem of §2.1, so this file contains
**no** $\vartheta'$-derived value of any kind for any $n$ — the tables in §4 measure
$\vartheta'$ on *finite subgraphs*, which by Lemma 2 bounds the method from the wrong side
to be useful as a bound. Everything in §1 is either an argument about cost or a null
measurement. If a reader takes away one caveat, it should be this one.

Secondarily, in order:

1. **Lemma 4's "$\alpha(G_d) \approx n$" step.** The lemma itself is clean; the conversion
   to $m \gtrsim \sqrt{2n}$ uses $\alpha(G_d) \approx d^2/8$ and $d(n) \approx \sqrt{8n}$,
   which are the right asymptotics but are being applied at small $n$ in the table of §2.4.
   The *integer* column ("least $m$") is exact given $\alpha - 1$; the growth rate is
   asymptotic.
2. **Whether the values in §4 are converged.** They are lower bounds by construction, so
   they cannot be too *large*; the risk is that they are far too small and a sharper witness
   would fire the gate after all. The refinement ladder is reported precisely so a reader can
   judge the trend rather than take my word for it. Several solves returned
   `optimal_inaccurate` against the per-solve cap, which for a repaired-primal *lower* bound
   degrades the bound rather than invalidating it.
3. **Non-polynomial kernels.** Lemma 4 constrains the polynomial-SOS route only.
4. **The Dostert–de Laat–Moustrou rounding machinery (arXiv:2001.00256)** that AC leans on
   for exactness: I have seen the abstract only. `WebFetch` is blocked in this session
   (`WORKER-PROTOCOL.md` §2), so I cannot say whether their rounding applies to a container
   with a boundary as opposed to a homogeneous space. **Assume it is unverified.**
