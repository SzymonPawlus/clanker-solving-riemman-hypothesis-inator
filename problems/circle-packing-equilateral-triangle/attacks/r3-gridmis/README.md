# Approach W — grid-rounding to a finite independent-set refutation

**This is a lower-bound (optimality-side) attack. It produces no construction and claims no
packing.** What it can produce is a statement of the form "$d(n) > d$", i.e. an optimality-side
bound, backed by a finite, externally checkable refutation.

```
status:  sketch   for Lemma 1 and Proposition 2 (prose, this file, unreviewed)
         numerical for every solver verdict, EXCEPT the DRAT-checked refutations
                   in §5, which are machine-checked refutations of a CNF but still
                   rest on Lemma 1 (sketch) and on the encoder in this directory
author:  claude (Opus 5), worker r3-gridmis, 2026-08-23
issue:   round-3 proposal W, attacks/r3-approaches/README.md §2
code:    experiments/packing-r3-gridmis/
kill:    KILL-CRITERION.md  — FIRED (see §6)
```

**Nothing here is assumable** (`RULES.md` §3). Lemma 1 is a `sketch` by its author; a bound
derived from it is a `sketch` too, no matter how the finite part was checked. The finite part is
in much better shape than the lemma: §5 records refutations whose SAT proofs were verified by
`drat-trim`, an external checker this project did not write.

---

## 0. Summary

| | |
|---|---|
| Target to beat | Oler at $n=16$: $d(16) \ge \sqrt{129}-3 = 8.35782\ldots$ (`sketch`, `attacks/r3-approaches` §0.1) |
| Best $d$ this method refuted at $n=16$ | see §4 — **below** the Oler floor |
| Calibration at $n=12$ ($d(12)=4+2\sqrt3=7.46410\ldots$, `cited`) | refuted $d(12) > 7.0$; never refuted any $d \ge d(12)$ |
| Kill-criterion | **fired** |

The two-sided calibration passed: the method refutes $93.8\%$ of the known $d(12)$ and refutes
nothing above it. The method is *sound* and it *works*; it simply does not reach far enough at
$n = 16$ inside an hour of compute, and §6 quantifies why in a way that does not depend on
solver engineering.

---

## 1. The perturbation lemma

Throughout, $T_d$ is the closed equilateral triangle with $A=(0,0)$, $B=(d,0)$,
$C=(d/2,\,d\sqrt3/2)$ (problem `RULES.md` §2), i.e.

$$T_d \;=\; \Big\{(x,y)\;:\; -y \le 0,\;\; \tfrac{-\sqrt3\,x+y}{2}\le 0,\;\;
\tfrac{\sqrt3\,x+y-\sqrt3\,d}{2}\le 0\Big\}. \tag{1}$$

Each of the three linear forms in (1) is written with a **unit** normal vector:
$(0,-1)$, $(-\tfrac{\sqrt3}{2},\tfrac12)$, $(\tfrac{\sqrt3}{2},\tfrac12)$. That normalisation is
what makes step (ii) of the proof work, so it is not cosmetic.

Let $g>0$ and let

$$L \;=\; \big\{\, i\,(g,0) + j\,(g/2,\; g\sqrt3/2) \;:\; i,j\in\mathbb Z \,\big\}$$

be the triangular lattice of spacing $g$ anchored at the origin.

> **Lemma 1 (grid rounding).**
> Let $n\ge 2$, $d>0$, $g>0$, and let $r$ be any real with
> $$\frac{g}{\sqrt3}\;\le\; r\;<\;1 .$$
> Put $\rho := 2-2r \;(>0)$,
> $$T_d^{(r)} := \Big\{(x,y): -y\le r,\;\; \tfrac{-\sqrt3x+y}{2}\le r,\;\;
>   \tfrac{\sqrt3x+y-\sqrt3 d}{2}\le r\Big\},\qquad V := L\cap T_d^{(r)},$$
> $$G = G(n,d,g,r) := \big(V,\;E\big),\qquad
>   E := \big\{\{u,v\}: u,v\in V,\ u\ne v,\ |u-v| < \rho\big\}.$$
> If $\alpha(G) < n$, then $T_d$ contains no $n$ points with pairwise distances $\ge 2$.
> Equivalently, $d(n) > d$.

**Proof.** We prove the contrapositive. Suppose $p_1,\dots,p_n \in T_d$ satisfy
$|p_i-p_j|\ge 2$ for all $i\ne j$.

*(i) Covering radius: each $p_i$ has a lattice point within $g/\sqrt3$.*
$L$ is the vertex set of the standard triangulation of the plane into equilateral triangles of
side $g$ (each lattice cell being a translate of the triangle with vertices $0$, $(g,0)$,
$(g/2,g\sqrt3/2)$, or its reflection). Every point of the plane lies in at least one closed cell
$\Delta$. For an equilateral triangle $\Delta$ of side $g$, the function
$z\mapsto \min_{w\in \mathrm{vert}(\Delta)} |z-w|$ is maximised over $\Delta$ at the circumcentre,
with value the circumradius $g/\sqrt3$ — for an acute triangle the max–min-vertex-distance point
is the circumcentre, and an equilateral triangle is acute. Hence for each $i$ there is a vertex
$v_i$ of a cell containing $p_i$ with
$$|p_i - v_i| \;\le\; \frac{g}{\sqrt3} \;\le\; r. \tag{2}$$
(If several lattice points are nearest, fix one arbitrarily; the argument uses only (2).)

*(ii) Trap (b): $v_i$ need not lie in $T_d$, but it does lie in $T_d^{(r)}$.*
Write the three constraints of (1) as $\langle a_k, z\rangle \le b_k$, $k=1,2,3$, with
$|a_k| = 1$ as noted above. For $p\in T_d$ and $|v-p|\le r$, Cauchy–Schwarz gives
$$\langle a_k, v\rangle \;=\; \langle a_k, p\rangle + \langle a_k, v-p\rangle
  \;\le\; b_k + |a_k|\,|v-p| \;\le\; b_k + r .$$
So $v_i \in T_d^{(r)}$, and since $v_i\in L$, $v_i \in V$. This is exactly why the vertex set is
the *relaxed* triangle and not $L\cap T_d$: taking $V = L\cap T_d$ would make the lemma **false**,
because a point of $T_d$ near a corner or an edge can round to a lattice point outside $T_d$ and
the constructed set would then not be a subset of $V$.

Geometrically, relaxing all three half-planes of $T_d$ by $r$ raises the inradius from
$d/(2\sqrt3)$ to $d/(2\sqrt3)+r$, so
$$T_d^{(r)} \;=\; \text{the equilateral triangle concentric with } T_d \text{ of side } d+2\sqrt3\,r, \tag{3}$$
which is how the vertex count is estimated in §6. (For a *triangle*, unlike a general convex
body, the relaxed-half-plane set is exactly a scaled copy; it is strictly larger than the outer
parallel body $T_d \oplus rB$, whose corners are rounded. Using the larger set is sound — a
larger $V$ can only increase $\alpha(G)$ — and it is what keeps every test rational, see §2.)

*(iii) Trap (a): the $v_i$ are automatically distinct, and pairwise non-adjacent.*
For $i\ne j$, the triangle inequality and (2) give
$$|v_i - v_j| \;\ge\; |p_i-p_j| \;-\; |p_i-v_i| \;-\; |p_j-v_j| \;\ge\; 2 - 2r \;=\; \rho \;>\;0. \tag{4}$$
Because $\rho>0$, (4) forces $v_i \ne v_j$: two distinct packing points can never collapse onto
one lattice vertex. So $\{v_1,\dots,v_n\}$ has exactly $n$ elements. And by (4) again, no two of
them are within $\rho$, so no pair is an edge of $G$.

Therefore $\{v_1,\dots,v_n\}$ is an independent set of size $n$ in $G$, i.e. $\alpha(G)\ge n$.
Contrapositive: $\alpha(G)<n$ implies no such $p_1,\dots,p_n$ exist. $\blacksquare$

**Where the hypothesis $r<1$ is used.** Only in (4), and there it is essential. It is the *whole*
content of "trap (a)": the collapse of two packing points onto one lattice vertex is not a case
to be handled separately, it is a case that the hypothesis $\rho>0$ excludes. With $r=g/\sqrt3$
the hypothesis reads $g<\sqrt3$, which every grid used here satisfies by a wide margin.

**Where the unit normalisation is used.** Only in (ii). If the constraints of (1) were written
with un-normalised normals the relaxation constant would be wrong by the normal's length, and the
vertex set could be too small — an unsound direction.

**Any single lattice works, and the choice is free.** Lemma 1 holds for every $g$, every $r$ in
range, and (by the same proof, which never uses the anchoring) every translate/rotation of $L$.
So a refutation at *one* grid suffices; different grids give logically independent arguments.

---

## 2. Exactness — no floating point in the soundness-critical comparisons

Index a lattice point by the integer pair $(a,j)$ with $a = 2i+j$ (so $a\equiv j \bmod 2$):
$$x = \frac{g\,a}{2},\qquad y = \frac{g\,j\sqrt3}{2}.$$
Then $x\in\mathbb Q$ and $y\in\sqrt3\,\mathbb Q$ whenever $g\in\mathbb Q$, and

$$|v-v'|^2 \;=\; \frac{g^2}{4}\Big(\Delta a^2 + 3\,\Delta j^2\Big) \;\in\; \mathbb Q. \tag{5}$$

Take $d,g,r\in\mathbb Q$ with $3r^2 \ge g^2$ (this is exactly $r\ge g/\sqrt3$). Then:

* **Edge test.** $|v-v'| < \rho \iff g^2(\Delta a^2+3\Delta j^2) < 4\rho^2$ — a rational comparison.
* **Containment tests.** Substituting the coordinates into the three relaxed constraints and
  clearing $\sqrt3$ by squaring (legitimate because in each case both sides are known to be
  $\ge 0$ before squaring):
  * $y\ge -r$: automatic if $j\ge0$, else $3g^2j^2 \le 4r^2$;
  * $\tfrac{\sqrt3x-y}{2}\ge -r$: automatic if $a\ge j$, else $3g^2(j-a)^2 \le 16r^2$;
  * $\tfrac{\sqrt3(d-x)-y}{2}\ge -r$: with $t := d-\tfrac{g(a+j)}{2}\in\mathbb Q$, automatic if
    $t\ge0$, else $3t^2 \le 4r^2$.

All of these are comparisons of exact rationals, implemented with `fractions.Fraction` and
Python integers in `experiments/packing-r3-gridmis/gridmis/lattice.py`. `covering_radius_bound`
returns a rational $r \ge g/\sqrt3$ by an exact integer-`isqrt` ceiling, and asserts $3r^2\ge g^2$
before returning; **rounding $r$ up is the safe direction** (a larger $r$ only shrinks $\rho$ and
enlarges $V$, both of which weaken the conclusion). No float ever enters a decision.

### 2.1 A free tightening: the distance spectrum is discrete

By (5) the distances realised in $L$ are $\tfrac g2\sqrt Q$ for integers
$Q = \Delta a^2 + 3\Delta j^2$ with $\Delta a\equiv \Delta j \pmod 2$. So $E$ depends on $\rho$
only through
$$Q_{\max} \;=\; \max\{\,Q \in \mathbb Z_{\ge 0} \;:\; Q < 4\rho^2/g^2\,\},$$
and the independent sets of $G$ are *exactly* the subsets of $V$ with pairwise distance
$\ge \rho_{\mathrm{eff}} := \tfrac g2 \sqrt{Q_{\mathrm{next}}}$, where $Q_{\mathrm{next}}$ is the
least representable value exceeding $Q_{\max}$. Always $\rho_{\mathrm{eff}} \ge \rho$, and the
gain is real but small: e.g. at $g=1/4$, $\rho = 1.71132$ but $\rho_{\mathrm{eff}} = \sqrt3 =
1.73205$. This costs nothing and is reported by the code.

---

## 3. What is a proof here and what is not

This distinction is the point of the whole approach, so it is stated bluntly.

| Artifact | What it establishes | Trust base |
|---|---|---|
| Lemma 1 | $\alpha(G)<n \Rightarrow d(n)>d$ | **prose by a language model — `sketch`, not assumable** |
| the graph $G$ | that the CNF/graph really is $G(n,d,g,r)$ | `gridmis/lattice.py` (exact rationals) — audit target |
| a **witness** independent set of size $n$ | $\alpha(G)\ge n$: the method *cannot* refute this $d$ | self-certifying; re-checked exactly by `verify_independent` |
| `mis.decide` returning `UNSAT` | $\alpha(G)<n$ | my branch-and-bound being complete and bug-free — **solver output, not a proof** |
| glucose4 returning `UNSAT` | $\alpha(G)<n$ | the SAT solver — **solver output, not a proof** |
| a DRAT proof accepted by `drat-trim` | the CNF is unsatisfiable | the encoder (`satproof.build_cnf`, ~20 lines) and `drat-trim`, **not** the SAT solver |

Only the last row is a machine-checked refutation. It still does not make $d(n)>d$ assumable,
because Lemma 1 above it is a `sketch` (`RULES.md` §3: a claim is capped at its weakest
dependency). What it does buy is that the *finite* half of the argument no longer rests on
anybody's search code.

The exact-independence bound used for pruning inside `mis.decide` is the greedy clique-partition
bound: a partition of the candidate set into $k$ cliques of $G$ certifies at most $k$ of its
vertices can be in an independent set. That is sound, so exhausting the search is a complete
refutation *if the implementation is correct*. It agreed with glucose4 on every instance where
both ran (§4), which is a cross-check between two independent search procedures, not a proof.

---

## 4. Results

Every number below is a **verdict about $\alpha(G)$**, and Lemma 1 (a `sketch`) is what converts it
into a statement about $d(n)$. `UNSAT` = no independent set of size $n$ = the method refutes that
$d$; `SAT` = an independent set of size $n$ exists = the method **cannot** refute that $d$ (and
says nothing about whether a packing exists there).

### 4.1 Two-sided calibration at $n = 12$, where $d(12) = 4+2\sqrt3 = 7.464102\ldots$ (`cited`)

**Upper side — the control that matters.** The method must never refute a $d \ge d(12)$, since a
packing demonstrably exists there. All **25** instances at
$d \in \{7.465,\; 7.5,\; 7.6,\; 8.0,\; 9.0\}$ and $g \in \{\tfrac14,\tfrac16,\tfrac18,\tfrac1{10},\tfrac1{12}\}$
— up to $5\,995$ vertices — returned `SAT`, and every witness was re-verified exactly with
`verify_independent`. **0 false refutations.** (`out/control12.json`.)

This is a check on the *implementation*, not on the lemma: if Lemma 1 is true then `SAT` here is
forced, so a single `UNSAT` above $d(12)$ would have meant a bug or a broken lemma. There was none.

**A second, sharper control at $n = 15$.** $d(15) = 8$ *exactly* ($n = \Delta(5)$, Oler, `cited`),
and the optimal configuration is the triangular arrangement with points at the corners and on the
edges — the case that stresses the boundary trap of Lemma 1 hardest, because points sitting exactly
on $\partial T_d$ are precisely the ones that can round outward. All 16 instances at
$d \in \{8.0,\,8.1,\,8.5,\,9.0\}$, $g \in \{\tfrac14,\tfrac15,\tfrac16,\tfrac18\}$ returned `SAT`
with an exactly verified witness, including $d = 8.0$ on the nose. (`out/control15.json`.) Since
$d(16) \ge d(15) = 8$ is free, this also confirms that nothing at $n = 16$ below $d = 8$ is
interesting.

**Lower side — how far down it reaches.** Largest $d$ refuted at each grid:

| $g$ | $\rho$ | $\rho_{\mathrm{eff}}$ | $\lvert V\rvert$ | $\lvert E\rvert$ | largest $d$ refuted | $d / d(12)$ | engine, time |
|---|---|---|---|---|---|---|---|
| $1/4$ | 1.71132 | 1.73205 | 351 | 18 960 | **6.2** | 0.831 | B&B, 24 nodes, 0.05 s |
| $1/5$ | 1.76906 | 1.77764 | 630 | 59 607 | **6.8** | 0.911 | B&B, 72 458 nodes, 3.9 s |
| $1/6$ | 1.80755 | 1.83333 | 903 | 129 090 | **6.8** | 0.911 | B&B, 1 979 nodes, 0.5 s |
| $1/8$ | 1.85566 | 1.86665 | 1 653 | 438 324 | **7.0** | 0.938 | glucose4, 115 s |
| $1/10$ | 1.88453 | 1.90000 | 2 278 | 932 097 | $\ge 6.6$ | — | B&B; not pushed further |

So: **$d(12) > 7.0$**, i.e. $93.8\%$ of the true value, is refuted. Gate 1 of the kill-criterion
passes on both sides.

### 4.2 Push at $n = 16$

The bar is Oler: $d(16) \ge \sqrt{129}-3 = 8.357817\ldots$ (`sketch`, `attacks/r3-approaches` §0.1).

| $g$ | $\lvert V\rvert$ | $\lvert E\rvert$ | clauses | largest $d$ refuted | solve time | first `SAT` |
|---|---|---|---|---|---|---|
| $1/4$ | 561 | 33 177 | 54 288 | **8.0** | 17 s | $8.2$ (witness) |
| $1/5$ | 903 | 91 674 | 135 393 | **8.1** | 77 s | — (8.2 not decided in budget) |
| $1/6$ | 1 225 | 186 483 | 253 262 | **8.0** | 157 s | — (8.1 not decided in budget) |

**Largest $d$ refuted at $n = 16$: $d = 8.1$** (grid $g = 1/5$, 903 vertices, glucose4, 77 s).
Under Lemma 1 that reads $d(16) > 8.1$, equivalently $s(16) > 2\sqrt3 + 8.1 = 11.5641$ — which is
**below** Oler's $8.3578$ / $11.8219$ and therefore adds nothing to the board. **The
kill-criterion has fired** (`KILL-CRITERION.md`).

Solve time roughly doubles per $+0.1$ in $d$ at fixed $g$ near the top of each grid's range, and
roughly doubles per grid refinement step at fixed $d$; the two compound.

### 4.3 Cross-checks

- The exhaustive branch and bound (`gridmis/mis.py`) and glucose4 **agreed on every instance
  where both terminated** — two independently written search procedures, one of them not written
  by this project.
- glucose4 is decisively the stronger of the two at the hard end: $n=12$, $g=1/8$, $d=7.0$ was
  `UNKNOWN` to the B&B after $10^6$ nodes and `UNSAT` to glucose4 in 115 s. Reported reach would
  have been one grid level too pessimistic on the B&B alone.
- Randomised end-to-end tests of Lemma 1 (§ `experiments/.../test_lemma.py`): 1 199 random
  feasible point sets snapped, 0 violations of any of the three conclusions.

## 5. DRAT-checked refutations

These are the only artifacts here where the *finite* step does not rest on trusting a search
procedure. The CNF is emitted by `satproof.build_cnf` (one variable per vertex, one binary clause
per edge, one `pysat` cardinality constraint), glucose4 emits a DRAT proof, and `drat-trim` —
built from Marijn Heule's published source, not written by this project — validates it.

| claim (given Lemma 1) | $\lvert V\rvert$ | vars | clauses | DRAT lines | check time | `drat-trim` |
|---|---|---|---|---|---|---|
| $\alpha(G(12,\,d=6.2,\,g=\tfrac14)) < 12$, so $d(12) > 6.2$ | 351 | 2 236 | 29 513 | 63 481 | 1.1 s | `s VERIFIED` |
| $\alpha(G(12,\,d=6.8,\,g=\tfrac16)) < 12$, so $d(12) > 6.8$ | 903 | 6 331 | 172 805 | 560 380 | 6.9 s | `s VERIFIED` |
| $\alpha(G(12,\,d=7.0,\,g=\tfrac18)) < 12$, so $d(12) > 7.0$ | 1 653 | 12 268 | 541 252 | 1 734 314 | 101 s | `s VERIFIED` |
| $\alpha(G(16,\,d=8.0,\,g=\tfrac14)) < 16$, so $d(16) > 8.0$ | 561 | 3 727 | 54 288 | 503 079 | 18.7 s | `s VERIFIED` |

All four headline refutations therefore have an externally checked finite certificate, including
the $n=12$ calibration record ($93.8\%$ of the true $d(12)$) and an $n=16$ refutation. The proof
files are 5 MB, 75 MB, 319 MB and 49 MB respectively; they are regenerable with
`python3 proofs.py` and are `.gitignore`d, with the `drat-trim` transcripts kept in
`out/proofs.log`.

Files: `experiments/packing-r3-gridmis/out/*.cnf`, `*.drat`, index in `out/proofs.json`.

**What this does and does not buy.** It removes the SAT solver from the trust base; it does not
remove Lemma 1 (`sketch`), the encoder, or `drat-trim` itself (unverified software — an LRAT
proof checked by the verified `cake_lpr` would be the honest upgrade). Under `RULES.md` §3 the
resulting statement about $d(12)$ is capped at `sketch`, and it is anyway weaker than the `cited`
exact value. The proofs are here as *evidence the pipeline produces real certificates*, which was
the point of proposal W, not as new mathematics.

Two practical notes for anyone reusing this: `pysat` omits the terminating empty clause from
`get_proof()`, so a final `0` line must be appended or `drat-trim` reports "no conflict"; and
`cadical153`'s proof through `pysat` did **not** validate here ("conflict claimed, but not
detected") while `glucose3`, `glucose4` and `lingeling` all did.

## 6. The ceiling, quantified

### 6.1 Cost grows quadratically, the gap closes linearly

By (3), $V \subseteq T_{d+2\sqrt3 r} = T_{d+2g}$ when $r = g/\sqrt3$, and the triangular lattice
of spacing $g$ has density $2/(\sqrt3 g^2)$, so

$$\lvert V\rvert \;\approx\; \frac{\sqrt3}{4}(d+2g)^2 \cdot \frac{2}{\sqrt3\,g^2}
  \;=\; \frac{(d+2g)^2}{2g^2},
\qquad
\lvert E\rvert \;\approx\; \frac{\pi\rho^2}{\sqrt3\,g^2}\,\lvert V\rvert \;=\; \Theta(g^{-4}).$$

(At $n=16$, $d=8.1$, $g=1/5$ the formula gives $8.5^2/(2\cdot\tfrac1{25}) = 903.1$ vertices against 903 measured.)

Meanwhile the "scaled side" of the discretised problem — the side, in standard separation-2 units,
of the triangle the discrete problem actually lives in —

$$D_{\mathrm{sc}}(d,g) \;:=\; \frac{2\,(d+2g)}{\rho_{\mathrm{eff}}}
 \;=\; d \;+\; g\Big(\frac{d}{\sqrt3}+2\Big) \;+\; O(g^2)$$

exceeds $d$ by only $\Theta(g)$. So closing a gap $\epsilon := d(n) - d$ needs $g = \Theta(\epsilon)$
and therefore

$$\boxed{\ \lvert V\rvert = \Theta(\epsilon^{-2}),\qquad \lvert E\rvert = \Theta(\epsilon^{-4}).\ }$$

At $n = 16$ the required $\epsilon$ to clear Oler is $9.2495 - 8.3578 = 0.892$ against the
best-known $d(16) \approx 9.2495$ (`numerical` — and if the true $d(16)$ is smaller, everything
below gets worse). Fitting the measured refutation thresholds gives $g \approx 1/7$, i.e.
$\lvert V\rvert \approx 1\,800$, $\lvert E\rvert \approx 4\times10^5$, roughly $6\times10^5$
clauses. The measured solve times at $n=16$ (17 s at 561 vertices, 77 s at 903, 157 s at 1 225,
and no decision at all one step beyond each) put that firmly outside an hour on 4 cores. **That
is where it bites.**

### 6.2 The deeper reason, which instance size understates

The size blow-up is not the real obstruction. This is:

> An independent set in $G$ is exactly a $\rho_{\mathrm{eff}}$-separated $n$-point set inside
> $T_{d+2g}$ **restricted to the lattice**. Rescaling by $2/\rho_{\mathrm{eff}}$, it is an
> $n$-point packing at separation 2 in a triangle of side $D_{\mathrm{sc}}(d,g)$, drawn from a
> lattice of spacing $2g/\rho_{\mathrm{eff}}$. As $g \to 0$ the lattice restriction disappears and
> $D_{\mathrm{sc}} \to d$, so **the discrete instance converges to the original continuous
> problem.**

The only thing making the discrete problem easier than the continuous one is the lattice
restriction, and refining the grid is precisely the act of throwing that advantage away. Measured
"lattice gain" $D_{\mathrm{sc}}/d(n)$ at the best refuted $d$:

| | $g=1/4$ | $g=1/5$ | $g=1/6$ | $g=1/8$ |
|---|---|---|---|---|
| $n = 12$ ($d(12) = 7.4641$, `cited`) | 1.036 | 1.085 | 1.042 | 1.041 |
| $n = 16$ (vs best-known $9.2495$, `numerical`) | 1.061 | 1.034 | 0.983 | — |

It is worth a few percent and it does not grow as $g \to 0$. (These are *lower* bounds on the
gain each grid can deliver: the $n=16$ rows, and $g=1/10$ at $n=12$, were truncated by the compute
budget before their thresholds were located, which is why the $g=1/6$ entry at $n=16$ sits below 1.
The honest reading is "a few percent, flat", not "it collapses".) A refutation near $d(n)$ therefore asks a general-purpose CDCL solver — which
knows nothing about the geometry — to settle an instance arbitrarily close to the open problem
itself, on a graph with $\Theta(\epsilon^{-2})$ vertices. There is no reason that should be easier
than the continuous problem, and the measurements say it is not.

**Corollary for the board.** This is a *different* wall from the three already diagnosed. It is
not wall 2 (counting/covering): no partition of the container is used, and the clique-partition
bound is only a pruning device, not the argument. It is not wall 1 (interval B&B losing forcing at
$d = 8$): the branching object here is discrete from the start. It is a **resolution-complexity**
wall — the finite certificate exists and is checkable, it is just super-polynomially large in the
precision demanded.

### 6.3 What would have to change

Three concrete levers, none of which fits an hour:

1. **Symmetry.** When $d/g \in \mathbb Z$ the whole configuration carries the triangle's order-6
   symmetry group; symmetry breaking is worth a constant, maybe 6.
2. **Geometry inside the search.** The encoding here is deliberately trivial so that the encoder
   is auditable by eye. A solver that knew about rows, or that carried an area/Oler bound on the
   remaining region as a propagator, would be a different (and much less auditable) object — and
   that is approach A/I, which has its own recorded wall.
3. **A better lemma.** The $2r$ loss in (4) is worst-case: it assumes both endpoints displace by
   the full covering radius in opposite directions. Averaging over lattice offsets, or a
   displacement bound that depends on the pair's lattice direction, would improve the constant —
   but only the constant, not the $\Theta(\epsilon^{-2})$ scaling.
