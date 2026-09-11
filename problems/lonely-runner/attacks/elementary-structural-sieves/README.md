# Elementary structural sieves at the fifteen-runner frontier

```
status:         sketch
target-status:  verified:review
author:         codex (@Flow-25), 2026-09-11, issue #297
scope:          k moving integer velocities at threshold 1/(k+1), specialized to k=14
depends-on:     elementary Haar measure on R/Z only; no finite-case preprint is assumed
kill-criterion: a counterexample to either displayed implication, or discovery that an identical
                result already appears in a cited primary source (then retain only the attribution)
```

## Outcome

Two exact sufficient conditions remove structured families without invoking any finite-reduction
theorem:

1. if there are at most \(\lfloor(k+1)/2\rfloor\) distinct absolute velocities, the instance has
   a witness; and
2. if some integer \(q\), \(2\leq q\leq k+1\), divides none of the velocities, then \(t=1/q\) is
   a witness.

For the current target \(k=14\), these prove every instance with at most seven distinct absolute
speeds, and every instance for which some \(q\in\{2,\ldots,15\}\) divides no coordinate.  Both
statements allow repetitions and arbitrary signs.

These are elementary baseline sieves, not claims of novelty.  Their value is as proved,
implementation-independent rejection rules for a later exact campaign.

## 1. Sparse absolute spectra

Let \(A=\{|v_i|:1\leq i\leq k\}\) and put \(d=|A|\).  Work on the circle
\(\mathbb T=\mathbb R/\mathbb Z\) with normalized Haar measure \(\mu\).  For \(a\in A\), define

\[
 B_a=\{t\in\mathbb T:\lVert at\rVert<1/(k+1)\}.
\]

Multiplication by the nonzero integer \(a\) preserves Haar measure, and the open arc
\(\{x:\lVert x\rVert<1/(k+1)\}\) has measure \(2/(k+1)\).  Hence

\[
 \mu\!\left(\bigcup_{a\in A}B_a\right)
 \leq \sum_{a\in A}\mu(B_a)=\frac{2d}{k+1}.
\]

If \(2d<k+1\), the union has measure less than one.  A point outside it is a common witness.

The equality case \(2d=k+1\) also works.  When \(d=1\), equality forces \(k=1\), and
\(t=1/(2a)\) is a witness directly.  When \(d\geq2\), all the sets \(B_a\) contain the common open
neighborhood

\[
 \{t\bmod1: |t|<1/((k+1)\max A)\}
\]

of zero.  This neighborhood has positive measure, so the union bound is strict: for example,
pointwise one may subtract \((d-1)\mathbf 1_{\cap_a B_a}\) from
\(\sum_a\mathbf 1_{B_a}\).  Therefore the union again has measure less than one.

We have proved:

> **Sparse-spectrum theorem.** Every nonzero integer \(k\)-tuple with at most
> \(\lfloor(k+1)/2\rfloor\) distinct absolute coordinate values satisfies the Lonely Runner
> inequality at threshold \(1/(k+1)\).

At \(k=14\), \(2d\leq14<15\), so only the strict union-bound case is needed.  In particular,
seven positive speeds may occur with arbitrary multiplicities among all fourteen coordinates.

### Exact-witness corollary

The proof gives existence on the circle.  It can also be made into a rational certificate.  Each
boundary point of each forbidden set has the form

\[
  \frac{(k+1)j\pm1}{(k+1)a}\pmod1
  \qquad(0\leq j<a).
\]

The finite union of open arcs is not the whole circle.  If its complement has an interval, a
boundary point of that interval is one of the displayed rationals and lies in the complement; if
the complement is finite, its points are already boundaries.  Thus some rational endpoint is a
witness.  This observation gives a finite exact certificate search without changing the proof's
quantifiers.

## 2. Modular-denominator sieve

Suppose \(2\leq q\leq k+1\) and \(q\nmid v_i\) for every \(i\).  Take \(t=1/q\).  The residue of
each \(v_i\) modulo \(q\) is nonzero, so

\[
 \left\lVert\frac{v_i}{q}\right\rVert
 =\frac{\min(r_i,q-r_i)}q\geq\frac1q\geq\frac1{k+1},
 \qquad r_i\in\{1,\ldots,q-1\}.
\]

This proves the second sieve, including both endpoints.  A primitive instance surviving it must,
for every \(q\in\{2,\ldots,k+1\}\), contain at least one coordinate divisible by \(q\).  That
necessary divisibility hitting condition is safe to use as a cheap pre-filter.  It is not by
itself a finite bound: one coordinate can cover many values of \(q\).

For \(k=14\), the particularly simple choice \(q=15\) says that any vector with no coordinate
divisible by 15 has the explicit witness \(t=1/15\).  More generally, any normalized box with
\(\max_i|v_i|\leq14\) is closed immediately by the same witness.

### Divisibility-chain corollary

Suppose the distinct absolute speeds are totally ordered by divisibility, and let \(M\) be the
largest.  Then a value \(q\) divides some speed in the chain if and only if \(q\mid M\).  The
modular sieve therefore proves the instance whenever

\[
  \operatorname{lcm}(2,3,\ldots,k+1)\nmid M.
\]

At \(k=14\), that least common multiple is

\[
 \operatorname{lcm}(2,\ldots,15)=360360.
\]

Thus every divisibility-chain instance whose largest normalized absolute speed is not a multiple
of \(360360\) has an explicit modular witness.  In particular, a chain consisting only of powers
of one prime is dispatched by any different prime at most 15.  This corollary is only a sieve:
chains with \(360360\mid M\) remain, so it is not advertised as a proof of the whole chain class.

## 3. Mandatory-filter audit

- **Quantifiers:** both proofs choose one time common to all coordinates.  Signs and repetitions
  were retained, then collapsed only because they define identical forbidden sets.
- **Boundary:** forbidden sets use `<`; both conclusions use `>=`.  The modular witnesses often
  attain equality, so changing this convention would invalidate the sieve.
- **Scaling:** neither proof performs coordinatewise scaling.  The divisibility hitting condition
  may be applied after common-gcd normalization, but it is not claimed to be invariant under
  arbitrary common rescaling.
- **Dimension:** the active specialization is \(k=14\), fifteen total runners, threshold \(1/15\).

## 4. Exact sanity checks

An independent temporary `fractions.Fraction` endpoint sweep checked every nonempty subset of
\(\{1,\ldots,10\}\) of size at most seven at \(k=14\): 967 spectra, each with a rational endpoint
witness.  It also checked the modular implication for every seven-element subset of
\(\{1,\ldots,15\}\) to which some \(q\in\{2,\ldots,15\}\) applies.  These bounded checks are
`numerical` evidence only; the proofs above do not depend on them.

Hand-checkable endpoint fixtures include:

| absolute spectrum | exact witness | minimum distance |
|---|---:|---:|
| \(\{1\}\) | \(1/15\) | \(1/15\) |
| \(\{1,2,3,4,5,6,7\}\) | \(1/15\) | \(1/15\) |
| \(\{8,9,10,11,12,13,14\}\) | \(1/120\) | \(1/15\) |

The last fixture is deliberately not certified by the \(q=15\) shortcut at the displayed time;
it exercises the general rational-endpoint claim.

## 5. Limits and next step

The sparse theorem says nothing once eight or more distinct absolute speeds remain at \(k=14\).
The modular sieve says nothing when the coordinates collectively contain a multiple of every
\(q\leq15\); for a divisibility chain this first occurs when \(360360\) divides its maximum.
Neither condition makes the full integer search finite, and neither proves the fifteen-runner
case.

The next useful structural question is whether the divisibility hitting condition, combined with
the finite-reduction bounds from the cited papers, forces a small enumerable family.  That step
must wait until those bounds and their hypotheses have been reconstructed from the primary source.
