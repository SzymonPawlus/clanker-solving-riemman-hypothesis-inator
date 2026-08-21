# Attack: a 15-piece covering lower bound for $n = 16$

**Claim type: OPTIMALITY / LOWER BOUND** (problem [`../../RULES.md`](../../RULES.md) §1). This
file asserts $s(16) \ge c$ for an explicit $c$ — the hard direction. It makes **no** claim about
any packing being optimal, and nothing here enters `results/`.

- Issue: [#97](https://github.com/SzymonPawlus/clanker-solving-riemman-hypothesis-inator/issues/97)
- Construction and search: `claude` (worker N1), 2026-08-22 — **killed mid-run by a session API
  limit**; it produced the certificate but no write-up.
- Certificate verification and this write-up: `claude` (manager), from the certificate on disk.
- Code: [`experiments/packing-n16-covering/`](../../../../experiments/packing-n16-covering/)
  (search + author's certifier), independent check in
  [`experiments/packing-n16-verify/manager_covering_check.py`](../../../../experiments/packing-n16-verify/manager_covering_check.py)

## The result

> **$a_{16} \ge \dfrac{89267}{20000} = 4.46335$ exactly**, hence
> $$s(16) \;\ge\; 2\cdot\tfrac{89267}{20000} + 2\sqrt3 \;=\; 12.390801615\ldots$$

against the repo's previous best and the standard bound:

| bound on $s(16)$ | value | status |
|---|---|---|
| Oler (1961) | $\ge 11.821918$ | `cited` |
| Lemma L (this repo, 2026-08-21) | $\ge 12.124356$ | `sketch` |
| **this attack** | $\ge \mathbf{12.390802}$ | `sketch` |
| best known packing (Melissen–Schuur 1995) | $\le 12.713629$ | `numerical` |

The open interval for $s(16)$ narrows from $[12.124356,\ 12.713629]$ to
$[12.390802,\ 12.713629]$ — **45.2% of the remaining gap**.

**Status: `sketch`.** Same-family verification only; see "What this is worth" below.

## The mechanism, and the one place it is delicate

> If $T_a$ is covered by 15 sets each of diameter **strictly** less than 1, then 16 points at
> pairwise distance $\ge 1$ cannot lie in $T_a$: two of them would share a piece and be less than
> 1 apart. Hence $a_{16} \ge a$.

**"Strictly" is load-bearing and is exactly where the predecessor of this attack went wrong.**
This problem's `RULES.md` §2 fixes separation as **non-strict**, so a closed piece of diameter
*exactly* 1 may contain two points at distance exactly 1 and the pigeonhole fails. Lemma L's
cells have diameter exactly 1, which is why it needed a scaling repair
([`../n16-verification/`](../n16-verification/) D1, with the witness: $T_{\sqrt3}$ holds four
separated points — three corners and the centroid — while Lemma L covers it with three cells).

This certificate avoids the problem outright: its maximum squared diameter is
$$\frac{2499900001}{2500000000} = 0.9999600004 \;<\; 1,$$
strictly, as an exact rational.

## The certificate

`experiments/packing-n16-covering/sub_s2_cert.json`: 15 convex polygons with exact rational
vertices, in the triangular basis $e_1 = (1,0)$, $e_2 = (1/2,\sqrt3/2)$, where

$$|u e_1 + v e_2|^2 = u^2 + uv + v^2 \quad\text{is \textbf{rational}}, \qquad
T_a = \{u \ge 0,\ v \ge 0,\ u + v \le a\}.$$

With $a$ rational, **every coordinate, every squared diameter and every area is an exact
rational and no square root appears anywhere** — the whole verification is `Fraction`
comparisons. Areas in this basis are $\tfrac{\sqrt3}{2}$ times the $uv$-shoelace area, so even
comparing a sum of areas to the whole triangle needs no irrationals.

## Verification — and one step the author's own argument assumed

Checked twice: by the author's `certify.py`, and independently by
`manager_covering_check.py`, written from the problem statement without using the author's
certifier. Both agree, including on the exact value of the maximum squared diameter.

| check | result |
|---|---|
| exactly 15 faces | ok |
| every vertex satisfies $u,v \ge 0$, $u+v \le a$ (so each convex face $\subseteq T_a$) | ok |
| every face simple and strictly convex | ok |
| max squared diameter over all faces $= \tfrac{2499900001}{2500000000} < 1$ **strictly** | ok |
| face areas sum **exactly** to $\operatorname{area}(T_a)$ | ok |
| all 105 face pairs have interior-disjoint intersection (exact convex clipping) | ok |

**The last row is the one worth pointing at.** The author's certifier argues: the faces lie in
$T_a$ and their areas sum to $|T_a|$, therefore they cover $T_a$. *That inference needs the
interiors to be pairwise disjoint* — without it, an overlap plus a hole of equal area passes the
area test while leaving part of $T_a$ uncovered, and the covering claim fails. The docstring
justifies disjointness by saying the faces "come from a fixed planar subdivision", i.e. it is
inherited from the construction rather than checked. The independent pass verifies it explicitly
by exact convex-polygon intersection: all 105 pairs meet in zero area.

So the covering argument is complete: faces inside $T_a$, pairwise interior-disjoint, areas
summing exactly to $|T_a|$, hence $\bigcup F_i = T_a$ with no sliver (the union is closed and its
complement in $T_a$ is relatively open of measure zero, hence empty).

## Kill-criteria — fixed before computing, and their outcome

See [`KILL-CRITERION.md`](./KILL-CRITERION.md).

- **K1 (no-improvement): did NOT fire.** It required the certified $a^\star$ to exceed
  $5\sqrt3/2 = 4.3301270$; the certificate gives $4.46335$.
- **K3 (§7 tripwire): did NOT fire**, and it is the check that matters most here. Any covering
  claiming $a^\star > 4.62476$ would contradict Melissen–Schuur's explicit 16-point packing and
  would therefore be *wrong*. At $4.46335$ the bound sits comfortably below, consistent with a
  packing that exists.

## What this is worth, stated precisely

- **It is `sketch`, not `verified:review`.** Both checkers are Claude Opus 5. Repo
  `RULES.md` §5 requires an examiner from a **different model family**, and until Codex examines
  it this grants nothing. Two same-family checkers agreeing is close to one checker agreeing with
  itself; what it buys is that the disjointness gap was found, not that the result is certified.
- **Novelty is UNVERIFIED and unverifiable from this session.** Every scholarly host is blocked at
  the egress proxy. A covering/pigeonhole lower bound for circle packing in a triangle is a
  natural idea and may well be published; Melissen–Schuur's own paper on $n = 16,17,18$ has not
  been read here beyond its constructions. **Assume this is known until someone with library
  access says otherwise.**
- **This is not the best this method can do.** The search was killed mid-run by a session limit.
  Its float logs reached max-diameter ratios implying $a^\star \approx 4.4638$ before it died, and
  it was still improving. The certified $4.46335$ is where it happened to have a frozen exact
  certificate, not a converged optimum.
- **The method has a ceiling**, and it is worth knowing before anyone invests more: no covering
  argument of this shape can ever prove more than $a_{16} \le 4.6247636$, since a 16-point packing
  exists there. The remaining headroom is at most $0.161$ in $a$.

## Reproduce

```bash
python3 experiments/packing-n16-verify/manager_covering_check.py
```

Exact rational arithmetic, Python standard library, no seeds, no network, ~1 s. Prints every
check above and the resulting bound.
