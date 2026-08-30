# inscribed-triangle-maximiser — the exact **largest** inscribed equilateral triangle

**Status: `numerical`.** Exact arithmetic in $K=\mathbb{Q}(\sqrt3)$ makes **each individual
fixture's answer certain** — there is no tolerance anywhere and every reported triangle is
re-checked by verifiers that know nothing about how it was found. That is not a general claim
about polygons, still less about Jordan curves. Nothing here is a proof step and nothing here
may be built on (`../../RULES.md` §3; this problem's
[`RULES.md`](../../problems/inscribed-equilateral-triangle/RULES.md) §6.4). Blind spots are in
[§7](#7-what-would-make-this-wrong-blind-spots-not-reassurances), and one of them is
load-bearing for the global maximum.

```
regularity budget:
  §1-§4 (the polygon maximisers):  polygonal, simple, vertices in Q(sqrt3).
  §5 (the constant-width body):    convex; the body is smooth-ish (h + h'' = 0 at five
                                   points) but NOTHING below uses that -- the bound uses
                                   only that h is a support function, i.e. convexity.
What breaks first if you drop convexity in §5: the outer polygon Q0 stops containing the
body at all, and with it every inequality in that section.
```

- Lane: exact maximiser. Author `claude` (Claude Opus 5), 2026-08-30, branch
  `claude/inscribe-equilateral-triangle-oj15x1`. Issue linkage is the dispatcher's to record.
- Journal: [`../../notebook/claude/2026-08-30-iet-maximiser.md`](../../notebook/claude/2026-08-30-iet-maximiser.md).
- **This directory previously contained unvalidated, never-run code and a README claiming
  nothing** (see [§8](#8-what-happened-to-the-previous-contents)). The mathematics of that code
  survived validation; one control-flow defect in its LP module did not, and is documented.

## Why the lane exists

Both committed deciders — [`../inscribed-triangle-polygons/`](../inscribed-triangle-polygons/)
and [`../inscribed-triangle-angular/`](../inscribed-triangle-angular/) — answer *is there an
inscribed equilateral triangle with a vertex at $O$?* and **short-circuit at the first
witness**. Neither maximises. The gap had already produced a reporting error: the 30-30-120
control's $120°$ apex is recorded with witness side$^2=1/3$, while the true maximum there is
$4/9$ — both correct, different questions.

## 1. What is computed, exactly

For a simple polygon $P$ with vertices in $K$ and $O\in\partial P$:

$$\mathrm{maxside}^2(O)=\max\{\,s^2:\ (O,X,Y)\ \text{a nondegenerate equilateral triangle
with}\ X,Y\in\partial P,\ s=|OX|\,\}$$

exactly, in $K$, together with a maximiser $(X,Y)$. Sides are never taken: everything is
side$^2$, which stays in $K$. Nondegeneracy ($s>0$,
[`RULES.md`](../../problems/inscribed-equilateral-triangle/RULES.md) §2) is imposed on every
candidate before it is scored, never checked afterwards.

## 2. Two independent maximisers, on purpose

| | `iet/maximiser.py` — direction space | `iet/pairmax.py` — edge-pair space |
|---|---|---|
| parametrised by | the **direction** $v$ of the ray from $O$ | the **position** $t$ of one vertex along an edge |
| candidate set | vertex directions $V-O$, $\rho^{-1}(V-O)$, and $\pm M_{ef}$ for all ordered edge pairs, from $\mathrm{cross}(v,M_{ef})=0$ | endpoints of the feasible $t$-interval of each ordered edge pair and each chirality |
| optimality argument | on an arc the side$^2$ is $k_e^2/(|b-a|^2\sin^2 t)$, and $|\sin|$ is concave, so the max sits at an arc endpoint | side$^2(t)=|P(t)-O|^2$ is a **convex** quadratic, so its max over a closed interval sits at an endpoint |
| cost | $O(n^3)$ | $O(n^2)$ |
| scorer | rebuilds both radial scale sets from scratch at each candidate | re-checks each candidate with `verify_triangle` |

They share the field arithmetic (`iet/qs3.py`) and the vector helpers, and nothing else: a
different parametrisation, a different candidate set, a different optimality argument. The
second exists because *six checkers failed in this session against zero mathematical errors of
that kind*, so agreement between two implementations is worth more than either alone.

## 3. Validation — external answers first, self-consistency second

| control | expected | got | source of the expectation |
|---|---|---|---|
| equilateral triangle, side 1 | $1$ at every vertex | $1$ | it inscribes itself |
| **unit square** | $\sec 15° = \sqrt6-\sqrt2 = 1.03527618\ldots$ | side$^2 = 8-4\sqrt3$ **exactly**, at all four corners | **classical**: the largest equilateral triangle in a unit square |
| 30-30-120 wedge witness | max side$^2=4/9$ at the $120°$ apex; **no** triangle at either $30°$ apex | exactly that | the brief's target; the $30°$ apexes are the §3.1 wedge test |
| 30-30-120, base midpoint | the one arc component in the committed battery | max side$^2=1/3$ | hand analysis in the angular lane's README §4 |

$8-4\sqrt3=1.0717967\ldots$ and $\sqrt{8-4\sqrt3}=1.03527618\ldots=\sec15°$ to every digit
checked. **The square is the check that matters**: it is a number from outside this project,
and it is the maximum, not a witness.

## 4. Cross-check against both committed deciders — 2 270 boundary points, zero disagreements

Every one of the sibling lane's 190 committed fixtures, at every vertex and every recorded
edge sample:

| compared | count | disagreements |
|---|---|---|
| this lane vs `inscribed-triangle-polygons` (`good`) | 2 270 | **0** |
| this lane vs `inscribed-triangle-angular` (`good`) | 2 270 | **0** |
| this lane's two maximisers (`side²`, exactly) | 2 270 | **0** |
| maximiser's triangle rejected by the polygons lane's verifier | 2 270 | **0** |
| maximiser's triangle rejected by the angular lane's verifier | 2 270 | **0** |
| vs the fixture's recorded `good` flag | 1 487 | **0** |

So: every triangle reported here is accepted by both committed verifiers, and every $O$ either
decider calls good yields a **positive** maximum here (and conversely). **No disagreement was
found, so there is nothing to adjudicate** — the weaker of the two available outcomes.

## 5. Global maximum over $O$ — say which of the two it is

**It is exact per $O$, and exact globally only modulo one `sketch` of mine.**

`iet/maximiser.py` proves (**Lemma V**, its module docstring, status **`sketch`** — my own,
unreviewed) that a *global* maximiser has at least one vertex at a **vertex of the polygon**,
by showing that a triangle with all three vertices in relative interiors of edges sits in a
one-parameter family $s(t)=K/(|\alpha|\cos(t-t_0))$ whose only critical point is a *minimum*
of $s$. Given Lemma V, $\max_{O\in\partial P}$ is the max over the finitely many vertices, and
is therefore exact. **Without Lemma V, what is exact is the per-$O$ maximum, plus a sample over
$O$.** The two are not blurred anywhere in `out/global.json`, which records both.

The sample is a genuine attempt to refute Lemma V, not a confirmation of it: 8 613 rational
interior edge points across the 190 fixtures, each solved exactly.

| | |
|---|---|
| sampled edge points solved exactly | 8 613 |
| points beating their polygon's vertex maximum | **0** |
| fixtures where the best sampled point ties the vertex maximum | 4 |
| fixtures where it is strictly below | 185 |

A single violation would have refuted Lemma V, which is what the sweep is for. None appeared.
That is evidence, not a proof, and Lemma V stays `sketch`.

## 6. The constant-width body — the disk really is not extremal, now exactly

[`../../problems/inscribed-equilateral-triangle/attacks/extremal-size/`](../../problems/inscribed-equilateral-triangle/attacks/extremal-size/)
§7 reports the convex body $K$ with support function $h(\theta)=1+\tfrac1{24}\cos5\theta$ as
beating the disk for $m/w$: $w=2$ exactly, $m\approx1.714410$, ratio $\approx0.857205$ against
the disk's $\sqrt3/2\approx0.866025$ — and says plainly that its $m$ is a **float**. This lane
replaces the float by an exact inequality.

**Only an upper bound on $m$ is needed, and only convexity is used.** $w(K)=2$ is exact and
needs no computation ($h(\theta)+h(\theta+180°)=2$ identically). Every triangle inscribed in
$\partial K$ is in particular *contained* in $K$, so $m(K)\le M(K):=\sup\{$side of an
equilateral triangle contained in $K\}$, and no lemma about where a maximal triangle touches
the boundary is needed anywhere.

The chain (`iet/cw.py`, full derivation in its docstring), each link exact:

1. $K\subseteq Q_0$, an outer polygon of $J=192$ rational half planes, because $h_K$ is the
   support function and each offset is a rational **upper** bound on it — $h_K(n)=|n|+
   \varepsilon(x^5-10x^3y^2+5xy^4)/(x^2+y^2)^2$, whose second term is exactly rational.
2. An a priori side bound $s\le 2.3095 < 12/5$ for triangles in $Q_0$, from an antipodal pair
   of half planes (a slab of width $W$ admits only $s\le 2W/\sqrt3$).
3. $D=3600$ rational directions with every consecutive gap $\le\gamma$, certified by
   $\gamma\le\tan\gamma=\mathrm{cross}/\mathrm{dot}$; here $\gamma\le 582134689/333332813958
   \approx1.7464\cdot10^{-3}$.
4. Rotating a triangle of side $s$ about its centroid onto the nearest sampled direction moves
   each vertex by $\le s\gamma/(2\sqrt3)$, so it lands in the outer parallel body $Q_r$,
   $r\approx1.2099\cdot10^{-3}$.
5. At each sampled direction, containment is a 3-variable LP and **weak duality** on a triple
   of constraints with $y\ge0$ gives an exact bound. Floats only propose which triple to try;
   every returned number is re-derived in $K$ and rejected unless $y\ge0$ holds exactly.

**Result.**

$$m(K)^2\ \le\ M(Q_0)^2\ \le\ \frac{368394053}{125000000}=2.947152424\ <\ 3,$$

hence $m(K)\le 1.7167273$ and

$$\frac{m(K)}{w(K)}\ \le\ 0.85836363\ <\ \frac{\sqrt3}{2}=0.86602540 .$$

**The disk is not extremal for $m/w$ among convex bodies — exactly, no floating point in the
inequality.** That *confirms and upgrades* `extremal-size`'s headline rather than refuting it;
the refutation would have been the more valuable outcome and did not occur. The exact
$\mathbb{Q}(\sqrt3)$ value of the bound is in `out/cw.json`; the displayed rational is a
certified rounding of it.

**The LP chain is checked against three bodies whose answers are known**, and in each the bound
must not fall below the truth:

| body | truth | bound (at the test's coarse $D=300$) |
|---|---|---|
| unit disk | $\sqrt3=1.7320508$ | $1.7404875$ |
| unit square | $\sec15°=1.0352762$ | $1.0393187$ |
| near-equilateral triangle | $\approx1$ | $1.0080626$ |

The disk row is the sharpest test available: it is the body the whole `extremal-size` question
is normalised against, and its $M$ is $\sqrt3$ exactly.

## 7. What would make this wrong (blind spots, not reassurances)

1. **Lemma V is a `sketch`.** The global maximum over $O$ is exact *given* it. Its Case 2 (two
   of the three vertices on one edge line) is argued more loosely than Case 1. If it is false,
   every per-$O$ number here stands and every *global* number becomes "the max over the
   vertices and 8 613 sampled edge points".
2. **The $m\le M$ step is an inequality, not an identity.** §6 bounds the *contained* problem.
   If $M(K)$ were much larger than $m(K)$ the bound would still be sound but could be too weak
   to settle anything; here it is not, but the method can never *certify* $m$ from below, and
   this lane produces **no lower bound on $m(K)$ at all** for the constant-width body.
3. **§6 does not say $0.857205$ is the answer**, or that it is near the infimum of $m/w$ over
   convex bodies. It says one specific body beats the disk.
4. **The direction sampling in §6 is exhaustive only through the rotation argument** of step 4.
   If that argument is wrong, the bound is a statement about 3 600 directions and nothing more.
   It is stated in full in `iet/cw.py` so it can be attacked.
5. **Polygons are the most regular curves there are.** §§1–5 say nothing about non-polygonal
   Jordan curves ([`RULES.md`](../../problems/inscribed-equilateral-triangle/RULES.md) §3.3).
6. **No new fixtures were generated.** The battery is the sibling lane's 190, chosen by its
   author; 182 of them are convex. Agreement on it is mostly a convex check.
7. **numpy is used**, in `_best_t` and in the residual ranking of `iet/lp.py`, purely to
   *propose* an LP basis. A wrong proposal loosens the bound; it cannot make it invalid,
   because `dual_bound` re-derives the certificate in $K$ and rejects it unless $y\ge0$ holds
   exactly. No sympy, and no library geometry predicate, anywhere.

## 8. What happened to the previous contents

The files here were written by a worker terminated mid-task by a rate limit, were swept into an
unrelated commit, and had never been run. Treated as unvalidated on resumption, per the
handover:

- `qs3.py`, `maximiser.py`, `siblings.py`: **mathematics validated** — the candidate-set
  argument and the scale-set algebra are correct and reproduce all four controls. Kept.
- `lp.py`: the LP *derivation* was correct; its `lambda_upper_at` ranked candidate constraints
  by $(c_j-\langle t,n_j\rangle)/m_j$ and so **could never propose a constraint with $m_j=0$** —
  which are ordinary walls of the polytope and do sit in the optimal basis. On the very
  direction attaining the maximum it therefore found no valid triple at all and returned
  `None`. Fixed by ranking on the residual; the fix is commented at the site. `dual_bound` also
  carried a dead `if False else` assignment, removed. This is the same shape of defect the
  sibling lane hit yesterday: right algebra, broken control flow.
- `pairmax.py`, `cw.py`, `run.py`, `run.sh`, `tests/`, this README: new.

## Reproducing

```sh
sh run.sh          # everything, ~4 minutes, deterministic
```

Pinned: **CPython 3.11.15**, **numpy 2.4.6**, otherwise standard library (`fractions`, `math`,
`json`, `unittest`). No randomness is used anywhere in this lane (`SEED = 20260830` is recorded
in the outputs for form; every generator is deterministic). Stages:

```sh
python3 -m unittest discover -s tests -q   # 19 tests, ~12 s
python3 run.py validate                    # the hand-known answers,        ~2 s
python3 run.py fixtures                    # 190 fixtures / 2270 points,    ~70 s
python3 run.py global                      # vertices vs 8613 edge samples, ~101 s
python3 run.py cw 192 3600                 # the constant-width bound,      ~55 s
```

| file | what |
|---|---|
| `iet/qs3.py` | exact $\mathbb{Q}(\sqrt3)$; its own integer-triple representation, independent of both sibling lanes |
| `iet/maximiser.py` | the direction-space maximiser, `verify_triangle`, `global_max`, Lemma V |
| `iet/pairmax.py` | the independent edge-pair maximiser |
| `iet/lp.py` | exact weak-duality bound for the containment LP |
| `iet/cw.py` | the constant-width chain: outer polygon, $s_{ub}$, $\gamma$, inflation, bound |
| `iet/siblings.py` | read-only adapters onto the two committed lanes; imports them, writes nothing |
| `run.py`, `run.sh` | drivers; every stage checkpoints into `out/` |
| `tests/` | 19 tests |
| `out/` | `validate.json`, `fixtures.json`, `global.json`, `cw.json` and their logs |
