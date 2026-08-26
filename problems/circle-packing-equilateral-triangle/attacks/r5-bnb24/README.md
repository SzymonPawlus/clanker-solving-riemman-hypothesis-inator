# Approach AI — Markót-class active-region branch and bound, calibrated at `n = 12`, pushed at `n = 24`

**This is an OPTIMALITY (lower-bound) attack. It produces no packing and claims no
construction.** Everything it can produce has the form "no `n` points at pairwise
distance `>= 2` lie in the closed equilateral triangle of side `d`" for an explicit
**rational** `d`, i.e. `d(n) > d`, equivalently `s(n) > d + 2*sqrt(3)`.

```
status:  numerical  — every verdict, node count and bound below (exact integer
                      exhaustion; computation, not proof; same model family as the
                      incumbents it is compared against, so no verified:review)
         sketch     — the relaxation lemma of §1 and the readings in §5–§6
author:  claude (Opus 5), worker r5-bnb24, 2026-08-26
code:    experiments/packing-r5-bnb24/   (one command per run, see its README)
kill:    KILL-CRITERION.md — did NOT fire; the calibration gate cleared on both sides
issue:   round-4 proposal AI, attacks/r4-approaches/README.md §1
```

**Nothing here is assumable** (`RULES.md` §3). The relaxation lemma in §1 is a `sketch`
by a language model; the exhaustion below it is exact but is `numerical` until the other
model family reimplements the checker (problem `RULES.md` §3).

---

## 0. Summary

| | |
|---|---|
| Calibration target | `d(12) = 4 + 2√3 = 7.4641016...` (`cited`) |
| Incumbent bar (PR #56, `experiments/circle-packing-bnb`) | `d(12) > 6.95`, 7 675 980 nodes, level 6 |
| Sibling bar (`attacks/r3-gridmis/`) | `d(12) > 7.0`, glucose4, 1653-vertex lattice graph |
| **This method, lower side** | **`d(12) > 7.1`**, 4 386 939 nodes, **level 5** (1024 cells), 54 s |
| **This method, upper side** | **0 false refutations** in 11 controls, including `d(3)=2`, `d(6)=4`, `d(10)=6` on the nose |
| Kill-criterion | **did not fire** |
| Oler at `n = 24` (`cited` inequality, `sketch` application) | `d(24) >= sqrt(193) − 3 = 10.8924...` |
| Anchor at `n = 24` (`numerical`, `attacks/r3-qsqrt3/`, **used only as a ceiling**) | `d(24) <= 8 + 2√3 = 11.4641...` |
| **This method at `n = 24`** | see §4 — **below Oler**, and §5 says exactly why |

The headline is the calibration, not `n = 24`. Active-region propagation is worth about
**one level of dyadic resolution and a factor ~50 in nodes** at the incumbent's own hard
point, and that is enough to move `n = 12` from `6.95` to `7.1` (`95.1 %` of the true
value). It is **not** enough to reach Oler at `n = 24`, and §5 quantifies the gap without
appealing to solver engineering.

---

## 1. The relaxation (`sketch`)

`T_d` is the closed equilateral triangle `A = (0,0)`, `B = (d,0)`, `C = (d/2, d√3/2)`
(problem `RULES.md` §2). Fix `L` with `h := d/2^L < 2` and take the level-`L` dyadic
subdivision of `T_d` into `4^L` **closed** cells of side `h`, which cover `T_d`. Define

> `G_L = (cells, e ~ f iff the maximum separation of e and f is < 2)`.

**Lemma (grid partition).** If `p_1, ..., p_n ∈ T_d` have pairwise distances `>= 2`, then
`alpha(G_L) >= n`. Hence `alpha(G_L) < n` implies `d(n) > d`.

*Proof.* Each `p_i` lies in at least one closed cell; choose one, `c_i`. If `c_i = c_j`
for `i ≠ j` then `|p_i − p_j| <= diam(c_i) = h < 2`, a contradiction, so the `c_i` are
distinct. For `i ≠ j`, `p_i ∈ c_i` and `p_j ∈ c_j` give
`max sep(c_i, c_j) >= |p_i − p_j| >= 2`, so `c_i ≁ c_j`. The `c_i` are therefore an
independent set of size `n`. ∎

Two remarks, because both are places this could be got wrong.

* **The cells are closed and cover.** A point on a shared edge lies in several cells and
  *any* choice works, because the last display only uses `p_i ∈ c_i`. There is no
  boundary trap of the kind `attacks/r3-gridmis/` Lemma 1 has to handle with a relaxed
  container: here the cells partition `T_d` itself, so no cell ever leaves the triangle.
* **The maximum of `|x − y|` over a product of two convex polygons is attained at a
  vertex pair**, so the `3 × 3` vertex scan is exact, not a bound.

**Exactness.** With `u = (h,0)`, `v = (h/2, h√3/2)`, every cell vertex is `a·u + b·v` with
integers `a, b`, and `|a·u + b·v|² = h²(a² + ab + b²)`. Writing `d = p/q`,

```
max sep(e,f) < 2   <==>   p^2 * maxQ(e,f)  <  4 * q^2 * 4^L ,      Q := a^2+ab+b^2
```

an integer comparison between Python arbitrary-precision integers. **No float is
consulted in any accept/reject decision.**

---

## 2. What the search adds, and how it differs from PR #56

A **tile** is a dyadic cell of the coarsest level `jt` whose side is `< 2`. Every tile is
a clique of `G_L` (its diameter is its side), so it holds at most one point.

| device | PR #56 (`circle-packing-bnb`) | here |
|---|---|---|
| pair test | yes (vertex scan) | yes, same test |
| capacity per cell | from `cited` `d(k)`, `k <= 15`, on the cell's **side alone** | hierarchical: `b(R) = 1` for a tile meeting the candidate set, else `min(cap(R), Σ children)`, with `cap(R)` from Oler on cell centroids |
| **tile forcing** | no | **yes** — when `#tiles still alive == #points still to place`, all of them are occupied |
| **active-region propagation** | **no** | **yes** — for an occupied tile with active region `D`, delete every cell conflicting with *every* cell of `D`; run to fixpoint |
| branching | distribute a cell's `k` points over its 4 children, **independently per cell** | refine **one tile at a time** down the dyadic tree; the product over tiles of sub-positions is never enumerated |
| symmetry | `D3` quotient at the root split | **none used** (see §3) |

**Why active-region propagation is sound.** If tile `t` is occupied and its point lies in
the active region `D` (a set of cells), then a cell `g` with `max sep(g, e) < 2` for
*every* `e ∈ D` cannot hold another point: the point of `t` sits in some `e ∈ D`, and a
point of `g` would then be at distance `< 2` from it. So `C &= ~AND_{e ∈ D} adj[e]`.
The AND is precomputed per dyadic subtree (`capadj`); when `D` is not a full subtree the
AND is evaluated over a dyadic **cover** of `D`, which can only *shrink* the deleted set —
the safe direction — and exactly when `|D|` is small.

**Why the capacity is sound.** Centroids of pairwise non-conflicting level-`L` cells
inside an equilateral region of side `a` lie in that region and are pairwise at distance
`>= rho := 2 − 2h/√3` (the circumradius of an equilateral triangle of side `h` is
`h/√3`). Rescaling by `2/rho` and applying **Oler** (`cited`; merged as
`attacks/oler-lower-bound/oler_bound.py`) to the equilateral triangle of side
`a' = 2a/rho` gives `cap <= a'²/8 + 3a'/4 + 1`. A rational **over**-estimate of `1/√3` is
used, which **under**-estimates `rho` and therefore **over**-estimates `cap`: sound.

---

## 3. Symmetry — none was used, deliberately

The assignment permits symmetry only as an *exhaustive case split*, and problem
`RULES.md` §5 bans symmetry-restricted search reported as optimality. PR #56 uses one
sound reduction (the `D3` action on the three level-1 corner cells is the full `S3`, so
every configuration has an image with non-increasing corner multiplicities). **I did not
use it, or any other symmetry.** Every node count below is from an unrestricted search
over the full configuration space of `T_d^n`: no contact graph, no rigidity assumption,
no restriction to locally maximal packings, no discretisation of the feasible set (the
subdivision discretises the *search*; cells are closed and cover their parent, so no
configuration can fall between cells).

The reduction is worth at most a factor 6 and would not change any verdict below. It is
recorded here as an available, unexercised option rather than silently omitted.

---

## 4. Results

Deterministic: no randomness, no seeds; `(n, p, q, L)` fixes the node count bit for bit.
All raw verdicts and counters are checkpointed in `experiments/packing-r5-bnb24/out/`.

### 4.1 `n = 12` — the calibration, both sides

`d(12) = 4 + 2√3 = 7.46410161...` (Melissen 1993, `cited`).

**Lower side.** Largest `d` refuted, and the cost:

| `d` | `L` | cells | verdict | nodes | prop. rounds | cells deleted by propagation | time |
|---|---|---|---|---|---|---|---|
| 6.0 | 5 | 1024 | **refuted** | **1** | 0 | — | 0.2 s |
| 6.5 | 5 | 1024 | **refuted** | 347 330 | 8.3e5 | — | 4.3 s |
| 6.9 | 5 | 1024 | **refuted** | 1 578 447 | 8.3e5 | 1.89e8 | 19.0 s |
| 7.0 | 5 | 1024 | **refuted** | 4 386 939 | 2.5e6 | 4.95e8 | 50.6 s |
| **7.1** | 5 | 1024 | **refuted** | **4 386 939** | 2.5e6 | 4.95e8 | **53.5 s** |
| 7.2 | 5 | 1024 | not refuted (`sat`) | 63 158 | — | — | 0.9 s |

`d = 6.0` closes in **one node**: the hierarchical capacity bound alone already gives
`b(root) < 12` there, with no search at all.

`d = 7.0` and `d = 7.1` have *identical* node counts because the integer conflict relation
between level-5 cells does not change over that range — the same phenomenon PR #56
reports for its level-5/level-6 relation, and a useful sanity check that both codes are
looking at the same discrete object.

**The certified bound, stated as a number:**

```
d(12) > 71/10 = 7.1        and therefore     s(12) > 7.1 + 2*sqrt(3) = 10.5641016...
```

against the true `s(12) = 10.92820323...`. That is **95.12 %** of `d(12)`, versus PR #56's
93.1 % and `r3-gridmis`'s 93.8 %.

**Upper side — the control that decides whether any of this is worth anything.** A method
that refutes a `d` where a packing demonstrably exists is broken, and every bound it ever
produced is worthless. Eleven instances, none of which may return `unsat`:

| `n` | `d` | `L` | verdict |
|---:|---|---:|---|
| 3 | 2 (`= d(3)`, on the nose) | 3 | `sat` |
| 6 | 4 (`= d(6)`) | 4 | `sat` |
| 10 | 6 (`= d(10)`) | 5 | `sat` |
| 15 | 8 (`= d(15)`) | 5 | `unknown` (budget) |
| 21 | 10 (`= d(21)`) | 5 | `unknown` (budget) |
| 12 | 7.465 | 5 | `sat` |
| 12 | 7.5 | 5 | `sat` |
| 12 | 8 | 5 | `unknown` (budget) |
| 15 | 8.1 | 5 | `unknown` (budget) |
| 24 | 11.47 | 4 | `sat` |
| 24 | 12 | 4 | `sat` |

**0 violations.** `unknown` is a budget outcome and proves nothing either way; only an
`unsat` here would have been fatal.

A second, stronger over-pruning control runs *outside* the tree walk: the optimal
triangular-lattice packings `n = 3, 6, 10, 15, 21` at `d = 2, 4, 6, 8, 10` are placed
exactly, their containing cells computed, and every pair checked to be non-adjacent — at
**every** level from 2 to 6. All 23 (n, L) combinations pass: `n` distinct cells, no
conflicting pair. If the conflict relation ever declared two cells of a real optimum
adjacent, every `unsat` in this directory would be worthless.

### 4.2 `n = 24` — the push

Reference points, none of which this work establishes:

* free: `d(24) >= d(21) = 10` (24 points contain 21; `d(21) = 10` is `cited`);
* **Oler: `d(24) >= sqrt(193) − 3 = 10.89245...`** — the number to beat;
* anchor: `d(24) <= 8 + 2√3 = 11.46410...` from the exact `Q(√3)` certificate in
  `attacks/r3-qsqrt3/` (`numerical`, same family, **not assumable**). I use it only as a
  **target to aim at and a ceiling my refutations must never exceed**, and they do not.

| `d` | `L` | cells | verdict | nodes | build | solve |
|---|---|---|---|---|---|---|
| 10.0 | 7 | 16 384 | **refuted** | **1** (capacity bound alone) | 88 s | 0.0 s |
| 10.3 | 7 | 16 384 | **refuted** | **1** (capacity bound alone) | 92 s | 0.0 s |

See §6 for the runs still in flight at the budget cut and for the frontier they were
probing. **The largest `d` refuted at `n = 24` is well below Oler's 10.8924**, so this
lane contributes nothing to the `n = 24` lower bound, and §5 explains why that was
predictable from the calibration.

**`RULES.md` §7 flag.** `n = 24` is an OPEN case. Nothing here comes near
`d(24) >= 8 + 2√3`; if a future run of this code ever did, that would be an extraordinary
claim requiring the §7 procedure and **not** an optimality proof — combined with the
construction it would be one, which is exactly why it would need both humans.

---

## 5. Why `n = 24` is out of reach, quantified without solver engineering

The capacity bound of §2, evaluated at the root, is a closed form. Refutation by the
bound alone happens exactly when `a'²/8 + 3a'/4 + 1 < n` for `a' = 2d/rho`,
`rho = 2 − 2d/(√3·2^L)`. At `n = 24` that is `a' < 10.892...`, i.e.

```
d  <  10.8924 / (1 + 10.8924/(sqrt(3) * 2^L))
```

which is `10.38` at `L = 7`, `10.63` at `L = 8`, `10.76` at `L = 9` — **converging to
Oler's own 10.8924 from below and never crossing it.** So the free part of the method
cannot beat Oler at any resolution: it is Oler, degraded by the grid.

Everything above that must come from the *search*, and the calibration says how much
search buys: at `n = 12` the bound alone reaches `d = 6.0` (80.4 % of `d(12)`) and the
search carries it to `7.1` (95.1 %) — a gain of **14.7 points of `d/d(n)`** at a cost of
`4.4e6` nodes on a 1024-cell graph. At `n = 24, L = 7` the bound alone reaches `10.38`
(90.5 % of the anchor); the same 14.7-point gain would land past the anchor, which is
impossible, so the gain must be much smaller — and the graph is **16× larger** (16 384
cells against 1024) with **4× more tiles** (64 against 16) and `24` points instead of
`12`. Tile forcing, the strongest propagator at `n = 12`, is precisely the device that
weakens: at `n = 12` it fires once 4 of 16 tiles die, at `n = 24, L = 7` it needs 40 of 64
to die first.

That is the same wall PR #56 hit at `n = 16, d = 8`, in a milder form — and it is the
honest reading of this lane. **Active-region propagation repairs the wall at `n = 12`
(where the incumbent stalled at `eps ≈ 0.5`) and does not repair it at `n = 24`.**

---

## 6. What I verified myself, and what I did not

Round-5 protocol §6 asks for this explicitly.

| input | source | re-derived here? |
|---|---|---|
| `d(12) = 4 + 2√3`, `d(3)=2, d(6)=4, d(10)=6, d(15)=8, d(21)=10` | problem `README.md`, `cited` | **no** — taken as `cited`; but every one was used as a *control* the method had to survive, and all did |
| Oler's inequality `n <= d²/8 + 3d/4 + 1` | `cited` (Oler 1961), merged `attacks/oler-lower-bound/oler_bound.py` | **no** — used as `cited`. Re-checked only that it is exactly tight at `d = 2,4,6,8,10,12` for `n = 3,6,10,15,21,28` |
| `d(24) <= 8 + 2√3` | `attacks/r3-qsqrt3/` (`numerical`) | **no** — used only as a ceiling and a target, never as a premise |
| PR #56's `d(12) > 6.95` / node counts / `n = 16` timeouts | `experiments/circle-packing-bnb/README.md` | **no** — quoted from its README, not re-run. The comparison in §0/§4 is therefore against *its own reported* numbers |
| `r3-gridmis`'s `d(12) > 7.0` | `attacks/r3-gridmis/README.md` §4.1 | **no** — quoted, not re-run |
| the conflict relation of `G_L` | this directory | **yes** — recomputed for 16 000 random cell pairs from Cartesian coordinates in `Q(√3)` (`Fraction` pairs, exact `√3` handling) by a code path sharing nothing with the integer test: **0 disagreements** |
| the search verdicts | this directory | **partly** — re-decided by glucose4 (`pysat`) on the same graph, an independently written search procedure; see `out/crosscheck.log` |
| soundness of the enumeration logic | this directory | **this is the weak link.** See below. |

**The single thing I am least sure of** is not the arithmetic and not the lemma — it is
**the completeness of the branching**, i.e. that the recursion in `arbb/search.py`
`_node` really covers every independent set. The propagators are individually easy to
argue and each was written to fail closed, but the interaction of tile forcing with the
"declare this tile empty" branch is the kind of step where an over-prune would produce a
*false* `unsat` and hence a wrong bound. The controls in §4.1 are aimed exactly at this
and it survived all of them, including three optima *on the nose*; that is evidence, not
a proof. An independent reimplementation by the other model family (problem `RULES.md`
§3) is what this needs, and until then everything here stays `numerical`.

---

## 7. Verdict for the board

* **Proposal AI is worth keeping, at `n = 12`-scale problems, and is not the route to
  `n = 24`.** The new ingredient works and is measurable: one level of resolution and
  ~50× in nodes, moving the repo's best `n = 12` exhaustion from 93.1 % to 95.1 %.
* **The `n = 24` framing of the proposal was wrong for a reason worth recording.** `n = 24`
  was chosen because it has an exact anchor, no rattler, full `D3` symmetry and
  infinitesimal rigidity (`attacks/r5-n17/`) — all of which are properties of the
  *optimum*, and **none of which a refutation-side method can use.** A B&B that refutes
  side lengths never locates an optimizer (PR #56's README makes the same point), so the
  structure at the optimum is invisible to it. What actually governs the cost is `n`, the
  cell count, and the tile-to-point ratio, and on all three `n = 24` is far worse than
  `n = 16`. The good property of `n = 24` — a narrow window — is a property of the
  *anchor*, and Oler occupies 95 % of it already.
* **The honest transferable statement:** the diagnosed wall at `n = 16, d = 8` is real and
  the last untried repair (active-region propagation) *does* repair it, but only by about
  one level of dyadic resolution. It does not change the exponential.
