# Branch-and-bound lower bounds for circle packing in an equilateral triangle

**Claim kind:** *optimality / lower bound* (problem `RULES.md` §1), and **only a
one-sided bound**. This directory produces statements of the form

> no `n` points at mutual distance `>= 2` lie in the closed equilateral triangle of side
> `d`, for one explicit **rational** `d`

i.e. `d(n) > d`, equivalently `s(n) > d + 2*sqrt(3)`.

**Status:** `numerical`. The computation is a finite exhaustion in exact integer
arithmetic, so it is not "numerical" in the sense of being approximate — there is no
tolerance anywhere in the pruning. It is `numerical` in this repo's sense: a computational
claim that has not yet been independently reimplemented. Problem `RULES.md` §3 requires
the *other* agent to write a checker from the problem statement, not to rerun this one.
Until that happens nothing here may be built on.

Issue: [#28](https://github.com/SzymonPawlus/clanker-solving-riemman-hypothesis-inator/issues/28).

---

## This is not an optimality proof, and cannot be turned into one by shrinking epsilon

The issue was retitled for this reason and the correction is repeated here because it is
the easiest thing in this directory to get wrong.

Ruling out a packing at one fixed side `d* - eps` proves `d(n) > d* - eps`. It does **not**
prove `d(n) >= d*`. Combined with a construction giving `d(n) <= d*` the deliverable is an
**enclosure**

```
d* - eps  <  d(n)  <=  d*
```

of width `eps`, and every run is a separate finite exhaustion at a separate side length,
so shrinking `eps` narrows the enclosure and never closes it. There is no limiting run.

This matches what the precedent actually delivers: Markót & Csendes describe the unit
square `n = 28..30` as solved "within very tight tolerance values", and Markót (2021)
reports high-precision *enclosures*.

**What exact closure would additionally require, and what is not done here:**

1. **Interval isolation of all global optimizers.** A validated interval-Newton /
   fixed-point argument showing that every global optimizer lies in a proven-unique small
   box, for *every* optimizer, not for the one an optimiser happened to converge to.
   Nothing in this directory does that: it never locates an optimizer at all, it only
   refutes side lengths.
2. **A separately certified algebraic identification of the objective value.** Even with
   all optimizers isolated, the exact value `d(n) = 4 + 2*sqrt(3)` (or whatever it is)
   needs a structural/algebraic argument. A numerical enclosure that happens to bracket a
   recognisable constant is not that argument.

Neither follows from the exhaustion. If a future write-up in this repo concludes
`d(16) = d*`, it is not resting on this code.

---

## The reduction, and the exact search space

By the reduction in the problem `README.md`, packing `n` unit circles into an equilateral
triangle of side `s` is equivalent to placing `n` points at pairwise distance `>= 2` in
the equilateral triangle of side `d = s - 2*sqrt(3)`. The container placement is the one
fixed by problem `RULES.md` §2:

```
A = (0, 0),   B = (d, 0),   C = (d/2, d*sqrt(3)/2)
```

closed triangle, non-strict inequalities throughout (points may sit on an edge, distances
may be exactly 2).

**The search space is the full configuration space** `T(d)^n`, subject to nothing but the
`C(n,2)` distance constraints and containment. In particular:

* no symmetry is *assumed* of the configuration — the only symmetry used is a sound
  quotient of the search (below);
* no contact graph, no rigidity assumption, no restriction to locally maximal packings;
* no discretisation of the point positions. Points range over the continuum. The
  *subdivision* is a discretisation of the search, not of the feasible set: cells are
  closed and cover their parent, so a configuration cannot fall between cells.

Concretely the tree is over **cell configurations**: a node is a multiset of subdivision
cells with multiplicities summing to `n`, meaning "there is a packing with this many of
its points in each of these cells". The root is `n` points in `T(d)` itself.

### Subdivision

Each equilateral triangle splits into four congruent equilateral triangles of half the
side. All vertices produced lie on the lattice spanned by `u = (h, 0)` and
`v = (h/2, h*sqrt(3)/2)` with `h = d/2^L`, so a level-`L` cell is `(orientation, i, j)`
with `i, j` integers:

* `up(i,j)` has vertices `(i,j)`, `(i+1,j)`, `(i,j+1)`
* `down(i,j)` has vertices `(i+1,j)`, `(i,j+1)`, `(i+1,j+1)`

Children of `up(i,j)`: `up(2i,2j)`, `up(2i+1,2j)`, `up(2i,2j+1)`, `down(2i,2j)`.
Children of `down(i,j)`: `down(2i+1,2j)`, `down(2i,2j+1)`, `down(2i+1,2j+1)`,
`up(2i+1,2j+1)`. `tests/test_lattice.py::test_children_cover_the_parent` checks the cover
by sampling the parent.

### Branching

Take a cell of minimal level (largest cell) and split it; distribute its `k` points over
the four children in all `C(k+3,3)` ways. Since the children are closed and cover the
parent, every real configuration consistent with the parent node is consistent with at
least one child node. Cells are kept in FIFO order inside a node, which makes "a cell of
minimal level" always the front cell.

### Pruning — two rules, both one-sided

1. **Pair test.** Two occupied cells `X != Y` whose *maximum* separation is `< 2` cannot
   hold two points at distance `>= 2`. A cell with multiplicity `>= 2` gets the same test
   against itself (its maximum internal separation is its side). The maximum of squared
   distance over a product of convex polygons is attained at a vertex pair, so scanning
   the nine vertex pairs is exact.
2. **Capacity test.** A cell of side `a` holds at most `cap(a)` points at mutual distance
   `>= 2`, where `cap` is read off the *cited* optimal values `d(k)`, `k <= 15`, from the
   problem `README.md`. `--max-cited K` restricts which `d(k)` may be used;
   `--max-cited 2` reduces the rule to "a cell of side `< 2` holds at most one point",
   which is the trivial two-point case and makes a run depend on no literature at all.

Both fire only when infeasibility is certain, so no node that could contain a packing is
ever discarded.

### Symmetry

The three level-1 corner cells are permuted by the symmetry group `D3` of the triangle,
whose action on the corners is the full `S3`. Every configuration therefore has an image
whose three corner multiplicities are non-increasing, so the search imposes that at the
root split only — worth up to a factor 6. No deeper symmetry reduction is attempted; the
usual point-relabelling symmetry is already quotiented out by representing a node as a
multiset rather than an ordered tuple.

### Termination and the three outcomes

Splitting always increases the total level, so with a cap `max_level` the tree is finite.

| outcome | meaning |
|---|---|
| `proved` | every branch pruned. No `n` points at mutual distance `>= 2` in `T(d)`; hence `d(n) > d`. |
| `unresolved` | a node survived with every cell already at `max_level`. **Nothing is proved** — the resolution was too coarse. A witness node is reported. |
| `timeout` | wall-clock or node budget exhausted. **Nothing is proved.** The remaining frontier is checkpointed and `--resume` continues from it. |

---

## Arithmetic: what is exact, and the floating-point model

**The geometry is exact integer arithmetic. No floating point is involved in any pruning
decision.** For a lattice displacement `a*u + b*v`,

```
|a*u + b*v|^2 = (d/2^L)^2 * (a^2 + a*b + b^2)
```

because `|u| = |v| = d/2^L` and `u . v = (d/2^L)^2 / 2`. With `d = p/q` an exact rational,
the pair test is the integer comparison

```
p^2 * (a^2 + a*b + b^2)  >=  4^(L+1) * q^2
```

between Python arbitrary-precision integers. No rounding, no tolerance, no epsilon. This
is why `--d` must be a rational: the theorem produced is about that rational side length.

Floating point enters in exactly one place: the *cited constants* `d(k)` are algebraic
(they involve `sqrt(3)`, `sqrt(6)`, `sqrt(33)`), and the capacity rule has to compare them
against a rational cell side. `cpbnb/interval.py` encloses them in outward-rounded
binary64 intervals, and the comparison is then done exactly in `fractions.Fraction`
against the interval endpoint. The floating-point model:

* Python `float` is IEEE-754 binary64.
* `+ - * /` and `math.sqrt` are correctly rounded, in round-to-nearest-ties-to-even, which
  CPython never changes.
* Hence for the true result `t` of one such operation,
  `nextafter(fl(t), -inf) <= t <= nextafter(fl(t), +inf)`, and every operation in
  `Interval` pushes each endpoint one ulp outward with `math.nextafter`. Widening is
  applied unconditionally, including where the result is exact and the widening is merely
  wasteful.

The comparison is one-sided: `capacity` returns a bound only when `lo(d(k)) > side` holds
in exact rational arithmetic. If an enclosure were too wide to decide, the answer is
"no bound", which loses pruning but never soundness.

So the rigour of a `proved` verdict rests on:

* **integer arithmetic** (unconditionally exact) for the pair test and the branching;
* **outward-rounded binary64** plus exact rational comparison for the capacity test — and
  the capacity test can be switched off entirely with `--max-cited 2`;
* the **cited** values `d(k)`, `k <= 15`, when `--max-cited` is above 2. Per repo
  `RULES.md` §3 a claim is capped at its weakest dependency, so a run with
  `--max-cited 15` is capped at `cited`; a run with `--max-cited 2` depends on no external
  claim at all;
* **the enumeration logic being correct**, which is the actual weak link and the thing a
  reviewer should attack. See "What I am least sure of".

---

## Results

All runs below: single CPU core, CPython 3.14.5, x86-64 Linux, no parallelism inside a
run. The search is deterministic — no randomness, no seeds — so `(n, d, max_level,
max_cited, symmetry)` fixes the node count bit-for-bit; only wall-clock varies. Machine
was running several searches concurrently, so the seconds column is an upper bound on
single-run time.

### n = 12 — the mandatory validation (repo `RULES.md` §6)

Known: `s(12) = 4 + 4*sqrt(3) = 10.92820323...`, so `d(12) = 4 + 2*sqrt(3) = 7.46410161...`
(Melissen 1993, `cited`). All runs use `--max-cited 2`, i.e. **no literature input** — with
`--max-cited 11` the cited `d(11) = 7.2659...` would settle every `d < 7.2659` in zero
nodes and the run would test nothing.

| `d` | `eps = d(12) - d` | max level | outcome | nodes | seconds |
|---|---|---|---|---|---|
| 5.0 | 2.4641 | 4 | **proved** | 3 190 | 0.09 |
| 5.5 | 1.9641 | 4 | **proved** | 4 238 | 0.10 |
| 6.0 | 1.4641 | 5 | **proved** | 4 238 | 0.10 |
| 6.2 | 1.2641 | 5 | **proved** | 7 288 806 | 41 |
| 6.4 | 1.0641 | 5 | **proved** | 7 675 792 | 35 |
| 6.5 | 0.9641 | 5 | **proved** | 7 675 792 | 38 |
| 6.6 | 0.8641 | 6 | **proved** | 7 675 792 | 40 |
| 6.8 | 0.6641 | 6 | **proved** | 7 675 980 | 34 |
| 6.9 | 0.5641 | 6 | **proved** | 7 675 980 | 36 |
| **6.95** | **0.5141** | 6 | **proved** | 7 675 980 | 31 |
| 6.99 | 0.4741 | 6 | timeout | 2.3e7 | 90 |
| 7.0 | 0.4641 | 6 | timeout | 2.4e8 | 1 200 |
| 7.1 | 0.3641 | 6 | timeout | 2.0e8 | 900 |
| 7.2 | 0.2641 | 7 | timeout | 2.4e8 | 1 200 |
| 7.3 (`--max-cited 11`) | 0.1641 | 8 | timeout | 2.4e8 | 1 200 |

The frontier is sharp: everything up to `d = 6.95` closes in about half a minute and
7 676 thousand nodes, and `d = 6.99` does not close in 2.3e7 nodes. Node counts repeat
across neighbouring `d` because the integer compatibility relation between level-5 and
level-6 cells is coarse and does not change over those ranges.

**The validation, stated as a number:** the exhaustion certifies

```
d(12) > 139/20 = 6.95    and therefore    s(12) > 6.95 + 2*sqrt(3) = 10.41410161...
```

against the true `s(12) = 10.92820323...`. The certified bound is 95.3 % of the true value
(93.1 % in `d`). It is *correct* — it does not contradict the known optimum, and it is on
the right side of it — and it is *weak*: the method as implemented does not come close to
reproducing `d(12)` itself, and the honest reading of the table is that the cost explodes
somewhere around `eps ~ 0.5`.

**The negative controls matter more than the positive ones.** A bug that over-prunes shows
up as a *false* `proved` at a side length where a packing exists, and that is the failure
that would invalidate every bound here. `tests/test_search.py` checks:

* the search does not report `proved` at `d = 2, 2*sqrt(3)+, 4, d(7)+, 6, 7.4642, 8` for
  the corresponding `n` (all feasible);
* directly, and independently of the tree walk, that **neither prune rule ever fires** on
  the cells containing four explicit optimal packings — the triangular-lattice optima for
  `n = 3, 6, 10, 15` at `d = 2, 4, 6, 8` — at every level from 0 to 7
  (`test_known_packings_survive_every_level`). This is the strongest soundness evidence in
  the directory.

### n = 16 — the target

Best known: `s(16) ~ 12.7136`, `d(16) ~ 9.2495` (Melissen & Schuur 1995; the numeric value
here is this repo's own optimiser output in `experiments/circle-packing-search/out/n16.json`,
status `numerical`). Optimality is open. Note `d(16) >= d(15) = 8` holds trivially, since
16 points contain 15 — **so any certified bound at or below 8 is not new information.**

| `d` | `--max-cited` | max level | outcome | nodes | seconds |
|---|---|---|---|---|---|
| 6.0 | 2 | 4 | **proved** | 1 908 | 0.17 |
| 7.0 | 2 | 5 | **proved** | 5 677 | 0.20 |
| 7.5 | 2 | 5 | **proved** | 5 677 | 0.20 |
| 7.9 | 2 | 5 | **proved** | 5 677 | 0.20 |
| 7.99 | 2 | 5 | **proved** | 5 677 | 0.20 |
| **7.999** | 2 | 6 | **proved** | 5 677 | 0.20 |
| 8.0 | 2 | 6 | timeout | 5.2e7 | 900 |
| 8.001 | 2 | 6 | timeout | 2.4e6 | 90 |
| 8.001 | 15 | 6 | timeout | 2.2e7 | 90 |
| 8.01 | 15 | 6 | timeout | 2.2e7 | 90 |
| 8.05 | 15 | 5 | timeout | 2.1e8 | 1 200 |
| 8.05 | 15 | 7 | timeout | 2.2e7 | 90 |
| 8.3 | 15 | 6 | timeout | 2.2e8 | 1 200 |
| 8.5 | 15 | 6 | timeout | 2.2e8 | 1 200 |
| 8.8 | 15 | 7 | timeout | 2.1e8 | 1 200 |

**The n = 16 outcome is a negative one, and it is the honest headline.** Within the
budget the search certifies `d(16) > 7.999` (`s(16) > 11.4631...`) — which is *weaker than
the free bound* `d(16) >= d(15) = 8`, since 16 points contain 15. Nothing at or above 8
closed, in fourteen attempts spanning `d = 8.0 .. 8.8` and levels 5 to 7. The enclosure
this directory can currently assemble for `n = 16` is therefore

```
8 (cited, free)  <=  d(16)  <=  9.2495 (best known construction, numerical)
```

**with no contribution from the search.** The `d < 8` runs are cheap for a structural
reason worth recording, and the cliff sits exactly at 8: for `d < 8` the level-2 cells have
side `d/4 < 2`, so each holds at most one point and 16 points are forced into the 16
level-2 cells one apiece — a completely determined configuration that the pair test kills
in 5 677 nodes. At `d = 8` the side is exactly 2, the forcing disappears, and the search
must work at level 3 or deeper where it chooses 16 cells out of 64. The node count crosses
four orders of magnitude between `d = 7.999` and `d = 8.001`.

### Why it stops where it stops

The binding constraint is resolution, and it is predictable in advance. At cell size `h`,
a set of pairwise-compatible cells exists whenever `n` points at mutual distance `>= 2 - h`
fit in `T(d)`, i.e. whenever `d >= d(n) * (2 - h)/2`. So no proof is possible at all unless

```
h  <  2 * (1 - d/d(n))          equivalently     2^L  >  d / (2 * (1 - d/d(n)))
```

which for `n = 12`, `eps = 0.5` needs `L >= 6`, and for `n = 16` a bound of `d = 8.5`
needs `L >= 6` and `d = 8.8` needs `L >= 7`. Every `timeout` row above was run at a level
that satisfies this, so the failures are cost, not resolution. The measured rate is
`~2.4e5` nodes/second in CPython on one core. The observed jump — `7.7e6` nodes at
`eps = 0.51` for `n = 12`, and `> 2.4e8` without closing at `eps = 0.46` — is at least a
factor 30 for a 10 % reduction in `eps`; extrapolating that, `n = 12` at `eps = 0.2` is
somewhere in `1e10`–`1e12` nodes, i.e. `1e5`–`1e7` CPU-seconds, and `n = 16` above
`d = 8.5` is further away again. That is consistent with the precedent (Markót & Csendes needed 21–53 hours
of 2005 CPU for the square cases) and it is the honest estimate to budget against: this
implementation is between three and six orders of magnitude short of a tight `n = 16`
enclosure, and closing that gap is an engineering problem (a compiled inner loop, better
bounds, parallel subtrees), not a change of method.

The issue's own kill-criterion — "validation `n = 12` does not close within ~1e8 boxes /
~10 h: abandon or redesign" — is **not** met: `n = 12` closes in 7.7e6 nodes at
`eps = 0.51`. It is the *tight* regime that is out of reach, which the issue anticipated
by allowing "a weaker rigorous lower bound by stopping the subdivision early".

---

## What is proved, and what is not

**Proved** (modulo the implementation being correct, and `cited` `d(k)` where
`--max-cited > 2`):

* `d(12) > 139/20`, i.e. `s(12) > 139/20 + 2*sqrt(3) = 10.41410161...`
  (`--max-cited 2`, so this depends on no cited claim).
* `d(16) > 7999/1000`, i.e. `s(16) > 7999/1000 + 2*sqrt(3) = 11.46310161...`
  (`--max-cited 2`; and weaker than the free `d(16) >= 8`).
* the same for every other `proved` row of the tables above.

**Not proved, and not approached:**

* `d(16) = d*` or `d(16) >= d*` for the Melissen–Schuur value — see the second section.
* any statement about where the optimizers are.
* any improvement on `d(16) >= 8`, which is free from `d(15) = 8`.
* anything at all from a `timeout` or `unresolved` run. Those rows are budget records, not
  weak theorems.

---

## How this composes with the exact checker (`experiments/circle-packing-checker`, PR #16)

They are the two halves of an enclosure and they do not overlap:

| | direction | input | output |
|---|---|---|---|
| `circle-packing-checker` | **upper** bound `s(n) <= c` | a certificate: `n` exact/interval coordinates in the schema of problem `RULES.md` §2 | accept/reject, plus whether the certificate is *tight* |
| `circle-packing-bnb` (here) | **lower** bound `s(n) > c` | `n` and one exact rational `d` | `proved` / `unresolved` / `timeout` |

An enclosure `c_lo < s(n) <= c_hi` is assembled by pairing a `proved` run here at
`d = c_lo - 2*sqrt(3)` with a checker-accepted certificate at `c_hi`. **This directory
emits no packing certificate and cannot feed the checker** — a lower-bound proof has no
coordinates in it, so there is deliberately no shared file format. Its JSON output records
`n`, the exact rational `d` as a string, the verdict, the search parameters and the node
counts, which is what a reviewer re-deriving the bound needs.

The one convention they must agree on is the reduction and the container placement, and
both take it from the same place: problem `README.md` for `s = 2*sqrt(3) + d`, and problem
`RULES.md` §2 for `A = (0,0)`, `B = (d,0)`, `C = (d/2, d*sqrt(3)/2)` with closed
containment and non-strict inequalities. `--d` here is the point-formulation side `d`,
**not** `s`; the CLI prints both.

---

## What I am least sure of

In descending order of how much damage it would do:

1. **The branching is exhaustive.** Everything rests on "children are closed and cover the
   parent, so no configuration falls through". The cover is checked by sampling
   (`test_children_cover_the_parent`), which is evidence, not proof; a reviewer should
   re-derive the two child sets from the vertex formulas by hand. A wrong child set is the
   one bug that would produce false `proved` verdicts everywhere and still pass most tests.
2. **The `D3` symmetry restriction.** The argument is that `D3` acts on the corners as the
   full `S3`, so every configuration has an image with non-increasing corner
   multiplicities, and that boundary points do not break this because the search ranges
   over *all* assignments of points to closed cells. `--no-symmetry` disables it and is
   tested to give the same verdicts on the small cases — but only on the small cases.
3. **The capacity table.** `d(k) = s(k) - 2*sqrt(3)` transcription from the problem
   `README.md`, and the `cited` status of those `s(k)`. `--max-cited 2` removes this
   dependency entirely, and the headline `n = 12` numbers were produced with
   `--max-cited 2` for that reason.
4. **The FIFO invariant** ("the front cell always has minimal level"). It holds because
   every appended child is exactly one level deeper than the cell it replaced. If it were
   violated, `max_level` would stop the search early and the effect would be *unsound*
   only in the direction of a wrong `unresolved`, not a wrong `proved` — but it would also
   silently change what `max_level` means.
5. **`math.sqrt` correct rounding.** Assumed, not checked at runtime. It is IEEE-754
   mandated and true on every mainstream platform; it only affects the capacity rule.

---

## Reproducibility

```
./run.sh          # environment, cited constants, full test suite, the short n = 12 run
./run.sh full     # additionally the long n = 12 and n = 16 searches (hours)
```

`uv` is the only prerequisite; `pyproject.toml` pins the interpreter range and pytest.
Direct use:

```
uv run python -m cpbnb prove --n 12 --d 6.8 --max-level 6 --max-cited 2 \
    --checkpoint out/ck.json --out out/result.json --time-limit 3600
uv run python -m cpbnb prove --n 12 --d 6.8 --max-level 6 --max-cited 2 --resume out/ck.json
uv run python -m cpbnb sweep --n 12 --target 7.4642 --epsilons 1.0 0.8 0.6 --max-level 7
uv run python -m cpbnb validate
uv run python -m cpbnb constants
```

**Determinism.** There is no randomness anywhere in the search, so there is no seed to
pin: `(n, d, max_level, max_cited, symmetry)` determines the node count exactly. Versions
recorded in every output JSON under `meta`. The results above were produced on CPython
3.14.5, x86-64 Linux; the tests are the part that must reproduce, and they use no
platform-dependent arithmetic beyond IEEE-754 binary64.

**Checkpointing.** `--checkpoint` writes `{schema, status, parameters, nodes, elapsed,
frontier, frontier_count, frontier_digest}` every 200 000 nodes and on exit, via an atomic
rename. On `timeout` the frontier is the complete remaining DFS stack, so `--resume`
continues an interrupted exhaustion with no loss and no double counting. A killed run
therefore still leaves a resumable state on disk (repo `RULES.md` §6).

**Resume is a soundness boundary, and is validated as one.** A resume replaces the root
node — "the `n` points are somewhere in the container" — with a frontier *asserted* to
cover every branch the interrupted run had not yet refuted. If that assertion is false the
exhaustion closes over a strict subset of the configuration space and reports `proved` for
a theorem it never proved. Codex found exactly this in review of this PR: `load_frontier`
discarded the checkpoint's parameters, so resuming the n = 12 frontier under `--n 2 --d 2`
printed `d(2) > 2`, which the two vertices of a side-2 triangle refute. `--resume` now
fails closed, exiting non-zero without running, unless:

- the checkpoint's `n`, `d`, `max_level`, `max_cited` and `symmetry` all equal the ones the
  run was invoked with (`d` compared as an exact rational, so `5.3` and `53/10` match).
  `max_cited` matters for provenance as much as for arithmetic: resuming a
  literature-pruned frontier under `--max-cited 2` would report a run that "depends on no
  literature" while standing on cited values;
- its `status` is one that carries a frontier. A finished (`proved`/`unresolved`)
  checkpoint stores none, and used to load as an empty frontier and silently start a
  *fresh* search — answering a question the user had not asked;
- the frontier is non-empty. An empty search stack is reported as `proved` without
  examining a single configuration, which is the classic vacuous proof;
- `frontier_count` and the SHA-256 `frontier_digest` match the frontier, catching
  truncation and hand-editing;
- every node is structurally a node of *this* search: at least one cell, each a genuine
  cell of the subdivision at level ≤ `max_level` (so a subset of the container, not an
  arbitrary lattice triangle elsewhere), cells distinct, multiplicities positive and
  **summing to exactly `n`**, and a minimal-level leading cell. A node summing to fewer
  than `n` points describes a smaller configuration that the search may legitimately
  refute while saying nothing about `n`.

`Prover.run` re-applies the structural checks to any `initial_stack` it is handed, so a
caller reaching past `load_frontier` cannot inject a node the loader would have rejected.

**What resume validation does not buy.** It cannot establish the property a resume really
needs — that the frontier *covers* what the interrupted run had not refuted. A checkpoint
with half its nodes deleted is internally consistent, and with its digest recomputed would
still yield a false `proved`. The digest reduces this to deliberate forgery rather than
accident, truncation or misuse, which is as far as a file-based checkpoint can go. So a
resumed `proved` is only as trustworthy as the file it resumed from; `prove` records
`resumed_from` in its output and says so under the PROVED banner, and a result that must
stand on its own should come from an uninterrupted run. Checkpoints in `out/` predate these
fields (schema 0) and are deliberately **not** resumable: their frontiers can be truncated
undetectably. They remain valid records of the runs that produced them.

**Files.** `cpbnb/interval.py` (outward-rounded intervals), `cpbnb/lattice.py` (exact
integer subdivision geometry), `cpbnb/caps.py` (cited `d(k)` and the capacity rule),
`cpbnb/search.py` (the branch and bound, including checkpoint validation),
`cpbnb/__main__.py` (CLI), `tests/` (70 tests, of which `tests/test_checkpoint.py` is the
regression net for the false-proof-by-resume class),
`out/` (run logs, results and checkpoints). Nothing in this PR touches
`problems/**/results/`.

**Compute actually used.** About 45 minutes of wall clock, with up to twelve searches
running concurrently on a 24-core machine, so roughly 3.9 CPU-hours in total. Repo
`RULES.md` §6.6 sets the budget as "one hour unattended per task"; this run stayed inside
that as wall clock and exceeded it as CPU time, which is stated here rather than rounded
down. Every long run was time-limited in advance, checkpointed, and reaped — no background
job outlived the session.
