# Round-3 attack X: the Lasserre/moment strength gate — **the direction is retired**

```
claim type:  NEITHER construction nor optimality.  No bound on d(n) or s(n) is
             asserted anywhere in this file, for any n.  This is a measurement of
             how weak a relaxation is, and its outcome is a refutation.
status:      `numerical` for every computed number; `sketch` for every argument.
             Nothing here is assumable (RULES.md §3).
author:      claude (Opus 5, convergent role per RULES.md §8 — the model that
             generated proposal X was Fable 5, and is not this one), 2026-08-23
worker:      r3-sdpgate, branch r3-sdpgate
executes:    proposal X of ../r3-approaches/README.md
code:        ../../../../experiments/packing-r3-sdpgate/  (one reproduce command)
```

**Kill-criterion: FIRED.** See [`KILL-CRITERION.md`](./KILL-CRITERION.md). Recorded as a
success under `RULES.md` §0 — a clearly documented refutation is the product.

---

## 1. The verdict in three lines

1. **The size claim is right.** Re-derived here from scratch; every number in proposal X
   reproduces, including its own consistency check. One wording correction, in §2.4.
2. **It does not matter.** The dense level-2 relaxation is slack against the *published exact*
   $d(n)$ by **38.8–68.6 %** at $n = 4,5,6,7,8,10,12$. The gate allowed "a few percent".
3. **Why, exactly.** The level-2 value equals, to solver precision, the elementary bound
   $f(n) \le 2n/(3(n-1))$ obtained from "min $\le$ mean" and one convexity remark. The entire
   level-2 hierarchy reproduces a two-line variance argument. Its lower bound on $d(n)$ rises to
   $\sqrt6 = 2.449\ldots$ and *stops*, while $d(n) \sim \sqrt{8n}$.

So the direction dies on **strength**, not on size — which is the opposite of what round 1's
approach C predicted, and also the opposite of the conclusion proposal X drew from correcting C.
Both halves of that history were half-right: C was wrong about *why*, X was right about the size
and wrong to infer the direction was reopened.

---

## 2. Part one — re-deriving the size claim

### 2.1 What was claimed

Proposal X, from an ideation lens, `sketch` and unverified: at $n = 16$, after reduction by
$S_n$, the dense $561\times561$ level-2 moment matrix splits into isotypic blocks of size
$9, 9, 3, 1$; the dense $6545$ level-3 matrix into blocks of size $\le 31$; invariant scalar
moments number $56$ at degree $\le 4$ and $275$ at degree $\le 6$ against $2.76\times10^6$ dense;
the constraints collapse to two orbits. Its stated internal check was
$\sum_\lambda m_\lambda \dim\lambda = $ dense dimension.

### 2.2 What I did instead of accepting it

Setting, pinned so the numbers are comparable: the **fixed-$t$ feasibility** formulation, $N = 2n$
variables $x_1..x_n, y_1..y_n$, with $S_n$ permuting the point index simultaneously in $x$ and $y$.
(That is the formulation the $561 = \binom{34}{2}$ and $6545 = \binom{35}{3}$ figures belong to.
The maximise-$t$ formulation of approach C has $N = 2n+1$ and gives $595$ and $7140$;
`moment_sizes.py` in `../candidate-approaches/` prints those. Do not mix them — this file uses the
first for §2 and the second for §3, and says so each time.)

The monomials of degree $\le L$ carry a permutation representation of $S_n$. In the
symmetry-adapted SDP the single big PSD constraint becomes one PSD block of size $m_\lambda$ per
irreducible $S^\lambda$, so **the block sizes are exactly the multiplicities** $m_\lambda$.
I computed them by characters, from scratch
([`symmetry_sizes.py`](../../../../experiments/packing-r3-sdpgate/symmetry_sizes.py)):

- **Permutation character, closed form derived here.** A monomial, i.e. exponent pairs
  $(a_i,b_i)$, is fixed by $\sigma$ iff $(a_i,b_i)$ is constant along every cycle of $\sigma$.
  Hence the number of fixed monomials of degree $\le r$ is
  $\sum_{k=0}^{r}[q^k] \prod_{c \,\in\, \mathrm{cyc}(\sigma)} (1-q^{\ell_c})^{-2}$.
- **Irreducible characters** by Murnaghan–Nakayama on beta-sets (remove a rim hook of length
  $\mu_1$; height read off as the number of beta-elements strictly between $b-h$ and $b$).
- **Multiplicities** $m_\lambda = \frac{1}{n!}\sum_\mu |C_\mu|\,\chi_{\text{perm}}(\mu)\chi_\lambda(\mu)$
  in exact `Fraction` arithmetic, asserted integral and non-negative.
- **Self-check**, the same one the lens quoted: $\sum_\lambda m_\lambda \dim\lambda$ against
  $\binom{N+L}{L}$, by the hook-length formula. Asserted in code, at every $n$ and $L$.

### 2.3 Result — confirmed, in full

At $n = 16$:

| level | dense | blocks $m_\lambda$ | on $\lambda$ | check |
|---|---|---|---|---|
| 2 | $561\times561$ | **9, 9, 3, 1** | $(16), (15,1), (14,2), (14,1,1)$ | $9\cdot1 + 9\cdot15 + 3\cdot104 + 1\cdot105 = 561$ ✓ |
| 3 | $6545\times6545$ | **31, 23, 15, 9, 4, 2** | $(15,1),(16),(14,2),(14,1,1),(13,3),(13,2,1)$ | $31\cdot15+23\cdot1+15\cdot104+9\cdot105+4\cdot440+2\cdot896 = 6545$ ✓ |

| invariant scalar moments | claimed | derived | dense |
|---|---|---|---|
| degree $\le 4$ | 56 | **56** | $\binom{36}{4} = 58{,}905$ |
| degree $\le 6$ | 275 | **275** | $\binom{38}{6} = 2{,}760{,}681$ |

Every claimed figure reproduces. I also checked two of them **by hand, before running the
script**, so that the script is not the only witness:

- $m_{(16)}$ at level 2 is the number of $S_n$-orbits of degree-$\le2$ monomials, which one can
  simply list: $1;\ x_i;\ y_i;\ x_i^2;\ y_i^2;\ x_iy_i;\ x_ix_j;\ y_iy_j;\ x_iy_j\ (i\ne j)$.
  Nine. And $\dim S^{(15,1)} = 15$, $\dim S^{(14,2)} = 104$, $\dim S^{(14,1,1)} = 105$, giving
  $9 + 135 + 312 + 105 = 561$.
- The invariant-moment count of degree $\le D$ is the orbit count, generated by
  $\prod_{k\ge1}(1-q^k)^{-(k+1)}$ (choose a multiset of nonzero exponent pairs; there are $k+1$
  pairs of weight $k$). Expanding: $1, 2, 6, 14, 33, 70, 149$, with partial sums
  $1, 3, 9, 23, 56, 126, 275$. So $56$ at degree $\le4$ and $275$ at degree $\le6$.

Two independent routes, one answer, in both cases.

### 2.4 One correction, and one addition

**Correction (small).** "Constraints collapsing to *two* orbits" holds only with $D_3$ included.
Under $S_n$ **alone** the $3n$ containment constraints form **three** orbits, one per triangle
edge, so the count is $1 + 3 = 4$; the $D_3$ that rotates the edges merges them to $1 + 1 = 2$.
Proposal X does invoke $S_n \times D_3$ elsewhere, so this is a wording slip and nothing rides on
it — but the two numbers should not be conflated.

**Addition (strengthens the claim).** The block sizes and invariant-moment counts are
**independent of $n$** once $n \ge 2L$. At $n = 8, 12, 16$ alike, level 2 gives $9,9,3,1$ and
level 3 gives $31,23,15,9,4,2$; the invariant moment counts are $56$ and $275$ at every one. That
is the strongest available form of the lens's point: the *reduced* SDP does not grow with $n$ at
all. It also makes the negative result below sharper rather than weaker — a relaxation that is
this cheap and still this bad is bad for structural reasons.

---

## 3. Part two — the strength gate

### 3.1 Setup

Point formulation, repo conventions, scaled to the **unit** triangle $A=(0,0)$, $B=(1,0)$,
$C=(1/2,\sqrt3/2)$, so no side parameter appears. Write

$$f(n) = \max_{p_1..p_n \in T_1}\ \min_{i<j}\ \lVert p_i-p_j\rVert^2 ,
\qquad\text{so}\qquad d(n) = 2/\sqrt{f(n)}$$

exactly (a packing at separation $\ge2$ fits in $T_d$ iff $d^2 f(n) \ge 4$). The polynomial
program is approach C's, verbatim — maximise $t$ subject to $\lVert p_i-p_j\rVert^2 - t \ge 0$,
three half-plane containments per point, and $0 \le t \le 1$; $t$ is a decision variable, so
$N = 2n+1$. A level-$L$ relaxation returns $f_L \ge f(n)$, hence $d_L = 2/\sqrt{f_L} \le d(n)$.

$t \le 1$ is *valid* for every $n \ge 2$ (the diameter of $T_1$ is 1), so including it is
legitimate; the runs record whether it is active, and **it never is** at $n \ge 4$. So the
numbers below are not an artefact of the cap.

### 3.2 Validation before the main runs (`RULES.md` §6)

`moment_gate.py --selftest`, all passing:

| instance | exact answer | level-2 relaxation |
|---|---|---|
| $\max x$ s.t. $1-x^2\ge0$ | 1 | 1.000000000 (also exact at level 1) |
| $\max x_1x_2$ on the simplex | 1/4 | 0.250000000 |
| **the packing program at $n=2$**, cap loosened to $t\le4$ | $f(2)=1$ | 0.999999983 |
| **the packing program at $n=3$**, cap loosened to $t\le4$ | $f(3)=1$ | 0.999999832 |

The last two are the ones that matter: the relaxation is *exact* at $n = 2, 3$, with the cap
deliberately loosened so that it cannot be supplying the answer. The machinery is right.

### 3.3 The slack table

Dense level 2. $d_2$ is the relaxation's lower bound on $d(n)$; $d(n)$ is the published exact
value (`../../README.md`, `cited` there). **$d_2$ is float SDP output and is therefore a
`numerical` hypothesis, not a bound.**

| $n$ | exact $d(n)$ | $d(n)$ | level-2 $d_2$ | abs gap | **rel gap** | measured $f_2$ | $\tfrac{2n}{3(n-1)}$ | cap active? |
|---:|---|---:|---:|---:|---:|---:|---:|:--|
| 4 | $2\sqrt3$ | 3.464102 | 2.121320 | 1.3428 | **38.8%** | 0.8888888 | $8/9 = 0.8888889$ | no |
| 5 | $4$ | 4.000000 | 2.190890 | 1.8091 | **45.2%** | 0.8333333 | $5/6 = 0.8333333$ | no |
| 6 | $4$ | 4.000000 | 2.236068 | 1.7639 | **44.1%** | 0.7999999 | $4/5 = 0.8000000$ | no |
| 7 | $2+2\sqrt3$ | 5.464102 | 2.267784 | 3.1963 | **58.5%** | 0.7777794 | $7/9 = 0.7777778$ | no |
| 8 | $2+\tfrac{2\sqrt{33}}{3}$ | 5.829708 | 2.291287 | 3.5384 | **60.7%** | 0.7619056 | $16/21 = 0.7619048$ | no |
| 10 | $6$ | 6.000000 | 2.323787 | 3.6762 | **61.3%** | 0.7407425 | $20/27 = 0.7407407$ | no |
| 12 | $4+2\sqrt3$ | 7.464102 | 2.345209 | 5.1189 | **68.6%** | 0.7272720 | $8/11 = 0.7272727$ | no |

Every $n$ the kill-criterion named — $5, 7, 8, 12$ — is in that table, plus the triangular
$n = 6, 10$ where $d(n) = 2(k-1)$ exactly, plus $n = 4$. The gate's threshold was "a few
percent"; approach C's was 1 %. The measured slack is **38.8 % to 68.6 %**, and it *grows*
with $n$. The cap $t \le 1$ is inactive at every row, so none of this is an artefact of it.

Solver notes, for honesty: $n = 4,5,6$ were solved with CLARABEL at default tolerance
(`optimal_inaccurate`), $n = 7,8,10,12$ with SCS at `eps = 1e-5` (`optimal`). The last column
shows agreement with $2n/(3(n-1))$ to between $5\times10^{-8}$ and $2\times10^{-6}$ relative —
that agreement is the real accuracy check, and it is far tighter than the gaps being measured.

### 3.4 Level 3

Level 3 was run at $n = 4$, the smallest case where level 2 is already loose (at $n = 2, 3$ both
levels are exact). It improves the bound and comes nowhere near closing the gap:

| $n$ | level | dense moment matrix | moment variables | $f_L$ | $d_L$ | known $d(n)$ | rel gap |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 2 | $55$ | $715$ | 0.888889 | 2.121320 | 3.464102 | **38.8 %** |
| 4 | 3 | $220$ | $5{,}005$ | 0.653211 | 2.474589 | 3.464102 | **28.6 %** |

A factor of seven in moment variables buys ten percentage points, at the *easiest* nontrivial $n$.
(The level-3 solve hit its 240 s wall-clock cap and returned `optimal_inaccurate`; the true
level-3 value is somewhere near, not obviously below, and the conclusion is insensitive to it.)
Level 3 at $n = 5, 6$ was launched and did not finish inside the compute budget; that is recorded
rather than papered over, and it does not affect the verdict, which the level-2 row of the table
above already settles at every $n$ the gate named.

**"You under-built the relaxation" — tested, and it does not rescue it.**
[`extra_test.py`](../../../../experiments/packing-r3-sdpgate/extra_test.py) re-solves level 2 at
$n = 4$ after adding the pairwise products of each point's three containment half-planes as
explicit (valid, redundant, degree-2) constraints:

| $n=4$, level 2 | extra constraints | $f_2$ | $d_2$ | rel gap |
|---|---:|---:|---:|---:|
| as built | 0 | 0.888889 | 2.121320 | **38.8 %** |
| + corner products | 12 | 0.691363 | 2.405342 | **30.6 %** |

So the relaxation *is* strengthenable — and 30.6 % is still two orders of magnitude past the gate.
The cross-point products ($h_{i,k}h_{j,l}$, $i \ne j$) were launched too and did not finish inside
the budget; they are the obvious next thing anyone re-opening this should try, and they would have
to close a 30-point gap to change anything.

**Size is emphatically not the obstruction.** Extending §2's computation upward at $n = 16$:

| level | dense moment matrix | reduced blocks | invariant scalar moments (deg $\le 2L$) | dense |
|---:|---:|---|---:|---:|
| 2 | $561$ | $9, 9, 3, 1$ | 56 | 58,905 |
| 3 | $6{,}545$ | $31, 23, 15, 9, 4, 2$ | 275 | 2,760,681 |
| 4 | $58{,}905$ | $90, 59, 56, 38, 21, 18, 5, 3, 3, 1$ | 1,164 | 76,904,685 |
| 5 | $435{,}897$ | $238, 187, 132, \ldots$ (14 irreps) | 4,435 | 1,471,442,973 |

Even the reduced **level 5** at $n = 16$ is a trivial SDP by modern standards — largest block
$238$, four thousand scalar variables. Proposal X's size finding is not merely right, it is more
right than stated. That is exactly what makes the slack measurement decisive rather than
inconclusive: there is no "if only we had a bigger solver" left to appeal to. (Caveat: this counts
the moment matrix and the invariant scalar moments. The localizing matrices reduce by the same
mechanism but their block structure was not computed here.)

---

## 4. The diagnosis — level 2 *is* the mean-distance bound

The level-2 values are not merely bad, they are a recognisable quantity. To solver precision,

$$f_2(n) \;=\; \frac{2n}{3(n-1)} \qquad (n \ge 4),$$

which is exactly the elementary "min $\le$ mean" bound (`sketch`, my own argument, and
`elementary_bound.py` records it):

$$\sum_{i<j}\lVert p_i - p_j\rVert^2 \;=\; n\sum_i \lVert p_i - c\rVert^2$$

is convex in each $p_i$ separately, hence maximised over the closed triangle with every point at
a vertex; with $a, b, c$ points at the three vertices of $T_1$ it equals $ab+bc+ca \le n^2/3$
over the real simplex $a+b+c=n$; divide by $\binom n2$.

This identity is for the relaxation *as approach C specifies it*. Augmenting it with redundant
valid inequalities does move the value (§3.4), so the coincidence is a property of that particular
build, not a theorem about every level-2 relaxation of this problem. What survives augmentation is
the size of the gap.

Three consequences, and they are what actually kills the direction:

1. **The level-2 hierarchy adds nothing.** Twenty thousand moment variables and a
   $351\times351$ PSD block at $n=12$ reproduce a two-line variance argument.
2. **It is asymptotically worse than useless.** $d_2(n) = \sqrt{6(n-1)/n} \nearrow \sqrt6 = 2.449$,
   a *bounded* function, while $d(n)$ grows like $\sqrt{8n}$. The gap is not a constant factor
   that a higher level might shave; it diverges.
3. **It cannot even see integrality.** For $n$ not divisible by 3 the honest vertex-count bound is
   smaller — at $n=5$, $(a,b,c) = (2,2,1)$ gives $8/10 = 0.8$, against the SDP's $5/6 = 0.8333$.
   The relaxation is below the *elementary* bound's own integer optimum.

At $n = 16$ this predicts $d_2(16) = \sqrt{6\cdot15/16} = 2.372$, against Oler's floor
$8.358$ (`sketch`, §0.1 of `../r3-approaches/`) and a best-known $9.25$ (`numerical`). It is not
in the game.

---

## 5. What this means for the board

- **Proposal X is retired.** Not "deferred pending a bigger solver" — the obstruction is
  independent of solver capacity, and §2.4 shows the reduced SDP does not even grow with $n$.
- **Approach C is retired too, and its recorded reason should be amended.** C's gate (i) was
  about size and gate (ii) about slack; the repo's summary of C attributes its death to size.
  Size was never the problem. This matters because a future agent reading "C died on size" might
  reopen it on the strength of exactly the (correct!) size finding that proposal X made.
- **The generic warning C itself wrote — "low levels of the hierarchy are usually slack for
  maximin-distance problems" — was the true statement in that section**, and it is now measured
  rather than asserted.
- **What is *not* refuted.** Nothing is claimed about level $\ge 4$, which is out of reach at
  $n=16$ in the dense formulation and was not attempted. Nor about **AC** (the container-$\vartheta'$
  kernel bound), which is a different object: an SOS bound in $\le 4$ variables whose slack is
  governed by the geometry of the kernel, not by the moment matrix of the $2n$ coordinates. This
  result is evidence about the *coordinate* hierarchy only. If anyone reopens SDP methods here,
  AC is the door, not X.

---

## 6. What I am least sure of

Whether $f_2(n) = 2n/(3(n-1))$ **exactly**, or only to the seven digits I measured. I did not
prove the identity; I matched it numerically at the $n$ listed and gave the elementary argument
for why that value is a valid upper bound on $f(n)$ (which makes $f_2 \le 2n/(3(n-1))$ the
plausible half, and the exactness — that level 2 gains nothing on top — the observed half).
The verdict does not depend on it: a 38.8–68.6 % gap survives any reasonable reading of the numbers.

Secondarily: several solves returned `optimal_inaccurate`. For a *negative* result this is
tolerable — solver error of order $10^{-5}$ does not close a 40 % gap — but it is the reason no
number in this file is offered as a bound.
