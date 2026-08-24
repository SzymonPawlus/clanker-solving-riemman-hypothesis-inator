# Kill-criterion for round-4 attack AC (container-$\vartheta'$ kernel bound)

```
worker:  r4-theta, branch r4-theta
status:  every statement below is `sketch` (argument) or `numerical` (computation).
         Nothing here is assumable (RULES.md §3).  No bound on d(n) or s(n) is claimed.
```

## The criterion as assigned

> **If the $\vartheta'$-derived bound does not beat Oler at any $n$ you can compute, record
> the table and STOP.**

## Verdict: **NOT FIRED — and the criterion turned out to be mis-aimed.**

Two separate things went wrong with the criterion, and both are findings rather than excuses.

### 1. The criterion asks for a measurement whose sign my instrument cannot produce

The cheap instrument built here (§3 of [`README.md`](./README.md)) evaluates
$\vartheta'(G_d[W])$ on a **finite** witness $W \subset T_d$. By the ceiling lemma
(§2.2, `sketch`), $\vartheta'(G_d[W]) \le \vartheta'(G_d)$, so the instrument can only ever
show that $\vartheta'$ is **too weak**. It can never show that $\vartheta'$ is strong,
because a value below $n$ is compatible with the continuum value being anything above it.
The measurements came back at the "$\vartheta'$ is strong" end — over 20 solves at seven
values of $n$, $\vartheta'(G_d[W])$ never reached $n$; at every $d$ well below $d(n)$ it sat
on $\alpha(G_d[W])$ to a few thousandths (at $n = 16$, $d = \sqrt{129}-3$: $\alpha = 15$ and
$\vartheta' = 15.0000$, converged), and nowhere did it exceed $\alpha$ by as much as $0.45$.
So **no ceiling was detected and the gate did not fire**.

That is an honest null result, not evidence for AC. §4.4 records exactly how blunt the
instrument is — in particular that the witness *undershoots* $\alpha(G_d)$ precisely at the
$d$ where the gate would need it to overshoot.

### 2. The literal question "does $\vartheta'$ beat Oler" has an a-priori answer, YES

$\vartheta'(G) \le \bar\chi(G)$ — I re-derive the required kernel explicitly in §2.3
rather than citing the sandwich — so the $\vartheta'$ floor is **at least** the floor of
*every* diameter-cover argument, including the covering plateau
$d(16) \ge 2 + 4\sqrt3 = 8.928\ldots$ that PRs #98/#104 record (`sketch`, unmerged, and
therefore **not depended on here** — it is quoted only to locate the question). That is
already above Oler's $\sqrt{129} - 3 = 8.358\ldots$. So proposal AC's dominance claim is
correct, and "beats Oler at $n = 16$" is not the interesting question about AC.

**The interesting question is cost**, and that is where AC breaks.

## What replaces it: the criterion that *did* fire

AC's actual selling point is

> "an SOS problem in a small number of variables (~4), **independent of $n$**".

That is the claim I ended up testing, and it is **false as stated**. §2.4 gives a
rank argument (`sketch`, derived from scratch):

* any feasible kernel $Z$ has $\operatorname{rank} Z \ge \alpha(G_d) - 1$, because the
  images of an independent set are pairwise obtuse vectors, and $\mathbb{R}^r$ holds at
  most $r+1$ of those;
* a kernel of degree $\le m$ in each argument has rank $\le \binom{m+2}{2}$;
* hence $\binom{m+2}{2} \ge \alpha(G_d) - 1 \approx n$, i.e. $m \gtrsim \sqrt{2n}$.

The number of *variables* is 4 for every $n$. The *degree* is not: it grows like
$\sqrt n$, so the Putinar multiplier blocks grow like $\binom{m+4}{4} \sim n^2/6$ and the
scalar variable count like $n^4$. **"Independent of $n$" is true of the wrong quantity.**

So the recommendation in §5 of [`README.md`](./README.md) rests on cost and on the
un-computed SOS side, **not** on a measured slack table — which is exactly the opposite
shape of the `r3-sdpgate` result, and I say so rather than borrowing its verdict.

## What would reopen this

An actual SOS solve of the $n = 16$ instance at $m = 4$ (the minimum the rank bound
allows: $\binom{6}{2} = 15 \ge \alpha - 1 = 14$), on the semialgebraic set
$\{x, y \in T_d,\ \lVert x-y \rVert^2 \ge 4\}$ in 4 variables. The blocks are a
$70 \times 70$ and seven $\sim 35 \times 35$ — small. If that returns
$\lambda < 16$ at some $d > 8.928$, AC has produced something the repo does not have, and
it would then need exact rounding (Dostert–de Laat–Moustrou, arXiv:2001.00256 — abstract
only; **this session could not read the paper**) before it is a bound rather than a float.
I did not get that far and say so in §6.

A cheaper second attempt at *firing* the gate: sharper finite witnesses. Circulant-shaped
point sets have $\vartheta' > \alpha$ by a fractional amount, and a gain of $1$ is all the
gate needs.
