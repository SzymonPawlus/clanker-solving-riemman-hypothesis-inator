# Attack: exact algebraic constructions (certified upper bounds)

**Claim type: CONSTRUCTION only.** Every statement in this file is of the form
$s(n) \le c$, witnessed by an explicit packing whose feasibility is verified in exact arithmetic.
**No statement here is an optimality claim.** A feasible packing says nothing whatever about
whether some other packing does better, and nothing below should be read, cited, or built on as
if it did. Problem [`../../RULES.md`](../RULES.md) §1 requires this sentence first; it is not
boilerplate, it is the thing that goes wrong.

- Issue: [#74](https://github.com/SzymonPawlus/clanker-solving-riemman-hypothesis-inator/issues/74)
- Code: [`experiments/packing-exact-algebraic/`](../../../../experiments/packing-exact-algebraic/)
- Certificates: [`certificates/`](./certificates/)
- Author: `claude` (Claude Opus 5), 2026-08-19
- Status of the closed forms: **`sketch`**. Status of the search that suggested them:
  **`numerical`**. Neither is assumable, including by me (repo `RULES.md` §3).

## The gap this addresses

The repo could already *find* good configurations — `attacks/multistart-nlp-search` does that.
What it could not do for most $n$ was hand over coordinates that are exact algebraic numbers.
Optimiser output is a float configuration that is always slightly infeasible; the missing step is
**exactification**: identify the contact graph, solve the resulting algebraic system exactly, and
then certify feasibility with no tolerance anywhere.

Before this, `results/` held exact certificates for $n = 3$ and $n = 6$ only.

## What was produced

Exact, tight, machine-checked certificates for **14 values of $n$**:

$$n \in \{1,2,3,4,5,6,7,8,9,10,14,15,20,21\}.$$

Every one is *tight* in the sense of `RULES.md` §2 — the exact minimal enclosing side of the point
set equals the declared $d$ — so none of them is an inflated bound wearing a certificate.

| $n$ | exact $s$ (this construction, upper bound) | published value | field |
|---:|---|---|---|
| 1 | $2\sqrt3$ | $2\sqrt3$ | $\mathbb{Q}(\sqrt3)$ |
| 2 | $2 + 2\sqrt3$ | $2 + 2\sqrt3$ | $\mathbb{Q}(\sqrt3)$ |
| 3 | $2 + 2\sqrt3$ | $2 + 2\sqrt3$ | $\mathbb{Q}(\sqrt3)$ |
| 4 | $4\sqrt3$ | $4\sqrt3$ | $\mathbb{Q}(\sqrt3)$ |
| 5 | $4 + 2\sqrt3$ | $4 + 2\sqrt3$ | $\mathbb{Q}(\sqrt3)$ |
| 6 | $4 + 2\sqrt3$ | $4 + 2\sqrt3$ | $\mathbb{Q}(\sqrt3)$ |
| 7 | $2 + 4\sqrt3$ | $2 + 4\sqrt3$ | $\mathbb{Q}(\sqrt3)$ |
| 8 | $2 + 2\sqrt3 + \tfrac{2\sqrt{33}}{3}$ | $2 + 2\sqrt3 + \tfrac{2\sqrt{33}}{3}$ | $\mathbb{Q}(\sqrt3,\sqrt{11})$ |
| 9 | $6 + 2\sqrt3$ | $6 + 2\sqrt3$ | $\mathbb{Q}(\sqrt3)$ |
| 10 | $6 + 2\sqrt3$ | $6 + 2\sqrt3$ | $\mathbb{Q}(\sqrt3)$ |
| 14 | $8 + 2\sqrt3$ | $8 + 2\sqrt3$ | $\mathbb{Q}(\sqrt3)$ |
| 15 | $8 + 2\sqrt3$ | $8 + 2\sqrt3$ | $\mathbb{Q}(\sqrt3)$ |
| 20 | $10 + 2\sqrt3$ | $10 + 2\sqrt3$ | $\mathbb{Q}(\sqrt3)$ |
| 21 | $10 + 2\sqrt3$ | $10 + 2\sqrt3$ | $\mathbb{Q}(\sqrt3)$ |

The "published value" column is the `cited` table in [`../../README.md`](../README.md). It is the
**target** these constructions were checked against, never an output of this work. Matching it is
a successful reproduction (`RULES.md` §4), and it is the whole result: **no row beats anything.**

Read the table correctly. For these $n$ the literature separately proves the matching *lower*
bound, so the true $s(n)$ is known — but that fact is `cited` and comes from Oler, Melissen and
Payan, not from this directory. What this directory contributes is the upper half, in exact form,
independently of those papers.

## Validation gate (repo `RULES.md` §6)

The kill-criterion on issue #74 was: if the pipeline cannot recover the published exact $s(n)$ for
$n = 2,3,4,5,6$, abandon it. **Not met** — all five are recovered exactly, and `test_exact.py`
asserts that gate by name so it cannot quietly rot. The secondary stop (a $d$ coming out *smaller*
than a published optimum, which would contradict a `cited` result and therefore indicate a bug)
was never triggered: every value matches exactly.

## The constructions

Point formulation throughout: $n$ points at pairwise distance $\ge 2$ in the closed triangle
$A=(0,0)$, $B=(d,0)$, $C=(d/2, d\sqrt3/2)$, with $s = d + 2\sqrt3$.

### Triangular lattice $T(k)$ — $n = k(k+1)/2$, $d = 2(k-1)$

Row $r$ (bottom row $r = 0$) holds $k - r$ points at $(2j + r,\; r\sqrt3)$ for $j = 0,\dots,k-1-r$.
Containment reduces to $0 \le j \le k-1-r$ and separation is the lattice minimum $2$. Covers
$n = 1, 3, 6, 10, 15, 21$.

### Lattice minus the apex — $n = k(k+1)/2 - 1$, same $d$

Delete the apex point $(k-1, (k-1)\sqrt3)$. Tightness survives because $x + y/\sqrt3 = 2j + 2r$ is
maximised at $2(k-1) = d$ by the rightmost point of *every* row, not only the apex. Covers
$n = 2, 5, 9, 14, 20$.

This is the configuration side of the Erdős–Oler conjecture. **We assert only that it is feasible
at this $d$.** That $s(\Delta(k)-1) = s(\Delta(k))$ — i.e. that nothing smaller works — is the
`cited` (and for $n=20$, qualified) part, and is not touched here.

### $n = 4$ — $d = 2\sqrt3$

Three corners plus the centroid $(\sqrt3, 1)$. The centroid sits at distance $d/\sqrt3 = 2$ from
each corner, so all three of its contacts are exact; the corner-corner distances are $2\sqrt3$.

### $n = 7$ — $d = 2 + 2\sqrt3$

Three corners; $(1,\sqrt3)$ at distance $2$ from $A$ along $AC$ and its mirror $(1+2\sqrt3,\sqrt3)$
on $BC$; and $(d/2, d/2) = (1+\sqrt3,\,1+\sqrt3)$, which is at distance exactly $2$ from both of
those *and* from the apex. That is the rigid part.

The seventh point is a **rattler** — the optimiser leaves it with no contacts at all, free to move
in a region near the bottom edge. `RULES.md` §5 says rattlers are normal and must not be "fixed",
so it is placed at the exact, symmetric point $(d/2, 0) = (1+\sqrt3,\,0)$, whose nearest neighbours
are at distance $1+\sqrt3 \approx 2.73$ and $\sqrt6 \approx 2.45$. Any point in the rattler's cell
would do; this one is merely the tidiest to write down.

### $n = 8$ — $d = 2 + \tfrac{2\sqrt{33}}{3}$

This is the one that needed actual solving, and the only one leaving $\mathbb{Q}(\sqrt3)$. The
optimiser returns a mirror-symmetric configuration with contact graph: bottom row of three at
$(0,0)$, $(d/2,0)$, $(d,0)$; a symmetric pair at height $h$ each touching two of the bottom row; a
symmetric pair on the edges $AC$, $BC$; and the apex.

Write the edge points as $(u, \sqrt3 u)$ and $(d-u, \sqrt3 u)$. Their mutual distance is $d - 2u$,
and their distance to the apex is also $d - 2u$ (the displacement to the apex is parallel to an
edge). So the three contacts among the top trio collapse to a single equation
$$d - 2u = 2 \quad\Longrightarrow\quad u = \tfrac{d-2}{2}.$$
The pair at height $h$ is equidistant from $(0,0)$ and $(d/2,0)$, hence at $x = d/4$ with
$$h^2 = 4 - \tfrac{d^2}{16},$$
and its contact with the edge point $(u, \sqrt3 u)$ gives, using $d/4 - u = (4-d)/4$,
$$\frac{(4-d)^2}{16} + \Bigl(h - \frac{\sqrt3\,(d-2)}{2}\Bigr)^{2} = 4 .$$
The system has the spurious root $d = 2$ and the root
$$\boxed{\,d = 2 + \frac{2\sqrt{33}}{3},\qquad h = \frac{\sqrt{11}}{2} - \frac{\sqrt3}{6}\,}$$
whence $s = 2 + 2\sqrt3 + \tfrac{2\sqrt{33}}{3}$, the published value. Pleasantly,
$\sqrt3\,u = \sqrt3\cdot\tfrac{\sqrt{33}}{3} = \sqrt{11}$ exactly, so the edge pair sits at height
$\sqrt{11}$ and the apex at $\sqrt3 + \sqrt{11}$.

sympy was used to solve that quadratic system while deriving it. **The certificate does not depend
on sympy**: the closed form is re-verified from scratch by the standard-library checker, which
confirms all $28$ squared distances are $\ge 4$ and that $d_{\min} = d$ exactly.

## What is NOT here, and why

- **$n = 11, 12, 13$.** Attempted, not delivered. The multi-start search did not converge within
  the 60-minute budget on shared CPUs for $n \ge 11$ (the $n \le 8$ sweep alone took the first
  run), so there was no reliable contact graph to exactify. These have known closed forms in
  `../../README.md` ($4 + 2\sqrt3 + \tfrac{4\sqrt6}{3}$, $4+4\sqrt3$,
  $4 + \tfrac{2\sqrt6}{3} + \tfrac{10\sqrt3}{3}$) and are the obvious next targets: the method
  clearly works, it just needs the configurations. Recorded as unfinished, not as impossible.
- **$16 \le n \le 34$.** Out of scope here; no record is approached, let alone claimed.
- **Anything in `results/`.** Nothing in this attack was written to `problems/**/results/`.
  Promotion needs the cross-family independent-checker review of `RULES.md` §3, which this PR does
  not have. Until then these are `sketch` constructions in `attacks/`, which is where they belong.

## Honest accounting of what could still be wrong

- The **conventions** could be misread. Everything rests on the placement $A=(0,0)$, $B=(d,0)$,
  $C=(d/2,d\sqrt3/2)$ and on `side_length` meaning $s$ rather than $d$. If the containment
  inequalities were derived with the wrong orientation, every certificate would be wrong together
  and the tests would not notice, because the tests use the same derivation. **This is the single
  most valuable thing for a reviewer to re-derive independently.**
- The **exactness argument** rests on linear independence of $\sqrt{\text{distinct squarefree}}$
  over $\mathbb{Q}$. That is standard, but it is what makes the syntactic zero-test sound, so it
  is load-bearing and worth stating out loud rather than burying in a docstring.
- The **rattler placement** for $n = 7$ is a choice, not a derivation. It is verified feasible
  exactly, so the certificate stands regardless, but do not read $(d/2, 0)$ as canonical.
- **$n = 8$'s derivation assumes the contact graph** read off a float solution. If that graph were
  misread, the algebra would produce some *other* exact configuration — but the checker verifies
  the result unconditionally, so the worst case is a valid certificate for a worse $d$, not a false
  one. Since the resulting $d$ matches the published value, that did not happen.
