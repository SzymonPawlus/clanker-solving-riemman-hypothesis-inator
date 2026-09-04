# Schrijver's counterexample to Edmonds–Giles, written down explicitly

**Issue:** #156. **Status of the mathematical content:** `numerical` (an exact finite
computation on one explicit instance) plus one `cited` locator correction. Nothing here is
`verified:review` or promoted into `results/`.

**What this closes.** Gap **G2** of `attacks/tau2-complete/` — "Schrijver's actual
counterexample instance has never been written down in this repo" — which the whole Schrijver
filter of that attack turns on. That file's author deliberately refused to transcribe the
digraph because their only access to it was an unrendered figure; that was the right call, and
this file does the transcription properly instead of guessing.

**What this is NOT.** This is a *reconstruction of a 1980 published counterexample to
Edmonds–Giles*, a conjecture already known to be false. It is **not** an extraordinary claim,
**not** new, and **not** a counterexample to Woodall's conjecture, which is the unweighted
statement and is untouched by everything below. Conflating the two is the exact confusion
`../../RULES.md` §4 warns about.

Reproduce everything here with one command:

```
python3 experiments/woodall-schrijver/run.py
```

Stdlib only, CPython 3.14.5, no randomness, no seeds, no third-party libraries, exact integer
arithmetic throughout. Runtime ≈ 1 s.

---

## 1. Definitions used

Restated per `../../RULES.md` §4, in my own words, before any argument.

Let $D=(V,A)$ be a digraph and $w:A\to\mathbb Z_{\ge0}$.

* $\delta^+(U)=\{(x,y)\in A: x\in U,\ y\notin U\}$ and $\delta^-(U)=\{(x,y)\in A:x\notin U,\ y\in U\}$.
* $U$ is a **dicut shore** if $\varnothing\neq U\subsetneq V$ and $\boldsymbol{\delta^-(U)=\varnothing}$.
  Its **dicut** is $\delta^+(U)$. The condition is $\delta^-(U)=\varnothing$ — **not**
  $\delta^+(U)\neq\varnothing$, the misreading `../../RULES.md` §4 singles out.
* $\tau_w=\min\{w(\delta^+(U)):U\text{ a dicut shore}\}$, and $\tau_w=+\infty$ when there is no
  dicut shore at all.
* $J\subseteq A$ is a **dijoin** if it meets every dicut.
* A **$w$-packing of dijoins** of size $k$ is a list $J_1,\dots,J_k$ of dijoins with every arc
  $a$ in at most $w(a)$ of them; $\nu_w$ is the largest such $k$. So an arc of weight $0$ lies
  in **no** member of a packing, while still helping to decide *which* vertex sets are dicut
  shores. That asymmetry is the entire mechanism of the counterexample.
* Edmonds–Giles conjectured $\nu_w=\tau_w$. The easy direction $\nu_w\le\tau_w$ is not in
  dispute.

Sanity checks on these definitions, all run in `run.py` Stage 1 with answers derived by hand
first: a directed path ($\tau=\nu=1$), a **directed circuit** (no dicut shore at all, so
$\tau=+\infty$ — the fixture that catches the $\delta^+/\delta^-$ confusion, since under the
wrong reading a circuit would have many "dicuts"), a DAG with two sources, the diamond at
$\tau=2$, the diamond plus a weight-0 arc, and an orientation of $K_{3,3}$ at $\tau=3$.

---

## 2. Provenance — where the instance came from, element by element

The primary source, **A. Schrijver, "A counterexample to a conjecture of Edmonds and Giles",
*Discrete Mathematics* 32 (1980) 213–214**, is behind Elsevier and **I did not read it.** The
digraph below is transcribed from two *secondary* drawings of it, which I read in full:

| Tag | Source | What I read | How |
|---|---|---|---|
| **[ACZ]** | A. Abdi, G. Cornuéjols, M. Zlatin, *On packing dijoins in digraphs and weighted digraphs*, **arXiv:2202.00392v5**, Figure 1 | the digraph, solid = weight 1, dashed = weight 0 | downloaded the arXiv e-print source; the figure is `figures/D1.pdf`, a **vector** PDF. I decompressed its content stream and read the 12 circle centres, 21 line segments, 21 arrowhead triangles and the per-path dash pattern **as coordinates**, applying the CTM stack. Vertices were assigned by nearest-centre snap (max gap 0.0 units), direction by which endpoint the arrowhead sits at (max gap 4.8 units vs. an endpoint separation of ≥ 50), and weight by whether the stroke's dash array was empty. Every arrowhead's dash style matched its segment's. **Not read by eye.** |
| **[HZ]** | *A Min-Max Relation on Dicuts and Dijoins in Weighted Chordal Digraphs*, **arXiv:2501.10918v2**, Figure 1, left panel (`Younger-3+5.jpg`) | the same digraph, **with the arc labels** $1,1',1'',2,2',2'',3,3',3''$ on the nine solid arcs, plus a caption asserting checkable facts about it | rendered the JPEG and read it visually |

**The two drawings agree arc for arc**, and they are by different author groups. [HZ]'s labels
are what let me state the instance in a form a reader can check against the literature.

A third source, **G. Cornuéjols, S. Liu, R. Ravi, arXiv:2311.04337v2, Figure 2**
(`SCO-fig1-black-note.jpeg`) — the figure `attacks/tau2-complete/` could not resolve — turns out
**not to be this digraph at all.** It is CLR's *translation* of Schrijver's example into
strongly-connected-orientation language: an undirected graph carrying a 2-SCO
($x_e=1$ solid, $x_e=2$ dashed, $0$ on the undrawn reverses of the dashed arcs) that does not
decompose into two SCOs. Same underlying 12-vertex two-hexagon skeleton, different object and
different weights. Anyone chasing G2 through CLR Figure 2 would have transcribed the wrong
thing; that is worth recording.

### Locator correction

Crossref returns **pages 213–214** for Schrijver 1980 (two deposited records,
`10.1016/0012-365x(80)90057-6` and `10.1016/0012-365x(80)90255-1`, agreeing on
*Discrete Mathematics*, vol. 32, 1980, 213–214). `attacks/tau2-complete/README.md` §8 already
says 213–214 and is **right**; `problems/woodalls-conjecture/README.md` says **213–215** and is
**wrong**. I have not edited that file — it is outside this attack's ownership and open PRs may
touch it.

---

## 3. The instance

Twelve vertices: an outer hexagon `TL TR R BR BL L` (clockwise from top-left) and an inner
hexagon `tl tr r br bl l` in the same six cyclic positions. Twenty-one arcs.

**Weight 1 (drawn solid) — nine arcs, in three families of three:**

| label | arc | | label | arc | | label | arc |
|---|---|---|---|---|---|---|---|
| `1`   | `l  → TL` | | `2`   | `tr → R`  | | `3`   | `br → BL` |
| `1'`  | `TR → TL` | | `2'`  | `BR → R`  | | `3'`  | `L  → BL` |
| `1''` | `l  → bl` | | `2''` | `tr → tl` | | `3''` | `br → r`  |

**Weight 0 (drawn dashed) — twelve arcs:**

| | | |
|---|---|---|
| outer hexagon | `L → TL`, `TR → R`, `BR → BL` | |
| inner hexagon | `l → tl`, `tr → r`, `br → bl` | |
| radial spokes (inner → outer) | `tl → TL`, `tr → TR`, `r → R`, `br → BR`, `bl → BL`, `l → L` | |

The machine-readable form is `experiments/woodall-schrijver/instance.py`.

The instance has an order-3 automorphism preserving weights,
`TL→R→BL→TL`, `TR→BR→L→TR`, `tl→r→bl→tl`, `tr→br→l→tr`,
which carries family $1\to2\to3\to1$. This is **checked in code**, and it is a real constraint
on the transcription: a single mis-read arrowhead would almost certainly break it.

---

## 4. Verification

Two checkers, written to be structurally different rather than two copies of one idea:

* **`checker_a.py`** enumerates all $2^{n}$ vertex subsets and tests $\delta^-(U)=\varnothing$
  directly; finds $\nu_w$ by a recursive branch-and-prune over arcs that handles general
  integer $w$.
* **`checker_b.py`** instead uses the equivalent characterisation "$U$ is closed under
  in-neighbours", i.e. $U$ is a union of ancestor-sets, and enumerates those by a worklist over
  down-sets whose cost is proportional to the number of down-sets, not to $2^n$; finds $\nu_w$
  (for $w\in\{0,1\}$) by a flat `itertools.product` over all assignments of the weight-1 arcs to
  $\{$member 1,…,member $k$, unused$\}$ with **no pruning at all**. It uses sets of names, not
  bitmasks.

They agree on $\tau_w$, on $\nu_w$, and on the number of dicut shores, on every fixture and on
Schrijver's instance.

### Result

$$\tau_w = 2, \qquad \nu_w = 1, \qquad \nu_w < \tau_w .$$

So this is a counterexample to Edmonds–Giles. The instance has 127 dicut shores. The nine
weight-1 arcs *do* together form a single dijoin, so $\nu_w=1$ exactly, not $0$.

### Why there is no packing of size 2 — an argument you can check by hand

With $w\in\{0,1\}$, every member of a packing is a subset of $S=\{$the nine weight-1 arcs$\}$
and the members are disjoint. So a $w$-packing of size 2 is exactly a 2-colouring of $S$ with
**no monochromatic trace** $C\cap S$, $C$ a dicut. It suffices to look at the inclusion-wise
minimal traces, since any trace containing a bichromatic trace is bichromatic. Computation
gives 127 distinct traces, of which exactly **ten** are minimal:

$$\{1,1'\},\ \{1,1''\},\ \{2,2'\},\ \{2,2''\},\ \{3,3'\},\ \{3,3''\},$$
$$\{1,2,3\},\ \{1',2'',3\},\ \{1'',2,3'\},\ \{1,2',3''\}.$$

The two-element traces force $c(1')=c(1'')=\lnot c(1)$, and likewise inside the 2- and
3-families. Writing $x=c(1)$, $y=c(2)$, $z=c(3)$, the four three-element traces read
$(x,y,z)$, $(\lnot x,\lnot y,z)$, $(\lnot x,y,\lnot z)$, $(x,\lnot y,\lnot z)$ and so forbid
respectively

$$x=y=z,\qquad x=y\neq z,\qquad x=z\neq y,\qquad y=z\neq x .$$

Every triple in $\{0,1\}^3$ has either all three coordinates equal or exactly two equal, so it
falls under one of those four patterns. **No colouring survives**, hence $\nu_w=1$. This needs
no search, and `run.py` checks the eight cases symbolically as well.

### Independent confirmation that the transcription is right

[HZ]'s Figure 1 caption asserts, of Schrijver's instance: *"Among all minimal dicuts, six have
weight 2 such as $D_1\supseteq\{1,1'\}$ and $D_2\supseteq\{1,1''\}$, and four have weight 3
such as $D_3\supseteq\{1,2,3\}$ and $D_4\supseteq\{1',2'',3\}$."*

My computed list of minimal traces is **six of size 2 and four of size 3, containing exactly the
four sets the caption names.** That is a strong check: it depends on essentially every arc, and
it was produced from [ACZ]'s vector coordinates while the assertion comes from [HZ]'s prose.

One caveat, stated because it matters. Read literally as "minimal *as arc sets*", the caption is
false — there are 49 of those, of weights 2, 3, 4 and 5 (also printed by `run.py`). The reading
that matches is "minimal among the traces on the weight-1 arcs", which is what
$D_i\supseteq\{\dots\}$ (a dicut *containing* the listed weight-1 arcs) says, and is also the
only object the dijoin question depends on. I am confident in this reading but it is a reading.

Two further published assertions also check out: the weight-1 arcs form exactly **three** weakly
connected components (the "three $a_i$–$b_i$ paths" of CLR Figure 2's caption, and the snippet
hint recorded in issue #156), and the underlying undirected graph has a **chordless 6-cycle**
([HZ] §5: *"Schrijver's counterexample has a chordless cycle of length 6, [so] this is best
possible"*). A structural guess of mine — that the underlying graph is "two hexagons plus
spokes" and so has no short cycles — was **wrong**: it has six triangles, each closed by one of
the three long weight-1 arcs. Recorded because it is exactly the kind of eyeballed claim that
must be machine-checked, and the check caught it.

---

## 5. The {0,1}-weighted question issue #156 actually asks

**Is Schrijver's instance {0,1}-weighted?** **Yes** — verified above, weights are $1$ on nine
arcs and $0$ on twelve. Issue #156 was drafted on the assumption that egress was blocked and
that the instance would have to be *constructed* rather than fetched; that assumption is no
longer true, and the answer to the first half of the question is simply that Schrijver's own
example already has the required form, on **12 vertices**.

**Does an explicit {0,1}-weighted counterexample exist at the 7-vertex frontier?**
**I do not know, and I did not settle it.** What I did is below, stated as a failed search.

### The failed search

Search space, stated exactly (`../../RULES.md` §2). For each $n$ the space is

> all pairs $(D,w)$ where $D$ is a **simple DAG** on the labelled vertex set $\{0,\dots,n-1\}$
> with every arc going from a lower to a higher index, and $w:A(D)\to\{0,1\}$,

enumerated by putting each of the $\binom n2$ ordered pairs $i<j$ independently into one of three
states — no arc, a weight-0 arc, a weight-1 arc — giving exactly $3^{\binom n2}$ instances, every
one of which was tested. Every labelled simple DAG on $n$ vertices occurs at least once (relabel
by any topological order); isomorphic copies are revisited, which costs time but omits nothing.

Restricting to DAGs is **without loss of generality**: dicut shores are exactly the vertex sets
closed under in-neighbours, hence unions of strongly connected components, so the dicuts of $D$
are those of its condensation and arcs inside a component lie in no dicut and are useless in a
dijoin. Restricting to **simple** DAGs is **not** without loss of generality — contracting
components can create parallel arcs, and two parallel weight-1 arcs behave like one arc of
weight 2, outside $\{0,1\}$. So the search covers exactly the $\{0,1\}$-weighted instances whose
condensation is simple. (That is the same restriction `attacks/zero-weight-frontier/` works
under.)

| $n$ | instances tested | with an empty dicut ($\tau_w=0$) | with $\tau_w\ge2$ | counterexamples | time |
|---|---|---|---|---|---|
| 2 | 3 | 1 | 0 | **0** | <0.1 s |
| 3 | 27 | 7 | 1 | **0** | <0.1 s |
| 4 | 729 | 105 | 46 | **0** | <0.1 s |
| 5 | 59 049 | 3 801 | 6 441 | **0** | <0.1 s |
| 6 | 14 348 907 | 366 699 | 2 577 230 | **0** | 20.3 s |
| 7 | 10 460 353 203 | — | — | **not run** | ≈ 4.1 h estimated |

(The $n=6$ row is reproduced by `python3 experiments/woodall-schrijver/search.py 6`; `run.py`
runs $n\le5$ so that the single command stays fast. The $n=7$ estimate is the measured rate at
$n=6$, 1414 ns/instance, times $3^{21}$; $n=7$ was **not attempted** — it does not fit the
one-hour budget in this implementation.)

**What this does and does not show.** It shows that no $\{0,1\}$-weighted counterexample to
Edmonds–Giles exists in that stated space at $n\le6$. It is **not** evidence that none exists at
$n=7$: $n=7$ is 729 times larger than $n=6$ and I searched **none** of it. Reporting "I searched
up to 6 and found nothing, therefore 7 is the frontier / therefore none exists" would be the
absence-of-evidence error this repo makes most often, and I am not making it. The $\ge7$-vertex
floor asserted by `attacks/zero-weight-frontier/` is **independently re-derived here only up to
$n\le6$** — i.e. I confirmed the "no counterexample at $n\le6$" half, and did not test whether 7
is achievable.

Note also that this search says nothing whatever about Woodall's conjecture, which is the
unweighted statement.

---

## 6. Mandatory filters (`../../RULES.md` §1)

Run, with outcomes:

1. **Schrijver filter** — not applicable in the usual direction: this attack proves no general
   statement, it *exhibits* the object the filter is named after. Nothing here would prove the
   weighted version of anything, because nothing here is proved for all digraphs.
2. **Lucchesi–Younger filter** — not used, in either direction. No step of this file invokes it.
3. **Easy-direction filter** — the file asserts $\nu_w<\tau_w$ on one instance, which is a
   statement in the *hard* direction's failure, established by exhaustive computation. The easy
   direction $\nu_w\le\tau_w$ is checked as an assertion in every fixture, not assumed silently.

## 7. What I am least sure of

* **The transcription rests on secondary sources.** I did not read Schrijver 1980. If both
  [ACZ] Figure 1 and [HZ] Figure 1 reproduce the same *error*, I have faithfully transcribed
  that error. I consider this unlikely — different author groups, and the instance passes four
  independently published assertions about it plus a symmetry check — but it is the load-bearing
  assumption, and no amount of computation on my side can remove it.
* **The [HZ] caption's "minimal dicut"** is read as "minimal trace on the weight-1 arcs" (§4).
  Under the literal reading the caption's counts are wrong; under mine they are exactly right.
  I believe the reading is correct but it is an interpretation, not something I read stated.
* **The $\tau_w=2,\ \nu_w=1$ computation itself** I am *not* worried about: two structurally
  different checkers agree, the fixtures pin the definitions, and §4's colouring argument
  reproduces $\nu_w=1$ by hand with no search at all. That last item is what I would ask a
  reviewer to check first, since it is short and it makes the exhaustive searches redundant.
* **The 12-vertex count is Schrijver's, not a minimum.** Nothing here shows 12 is optimal.
