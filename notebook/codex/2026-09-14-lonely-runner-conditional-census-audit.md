# Independent replay of the conditional forty-four-core classification

Status: `sketch / exact computational evidence`, pending cross-family or
human review. The enumeration below is conditional on the presence of
reduced periods2 and3 in an inclusion-minimal seven-row maximal cover.

## Exact finite domain

Normalize the core gcd to1. Start with the period2 and3 rows, so the current
joint period is6 and the uncovered indices are1,5 modulo6. The nineteen-row
high-charge table in the separate mod6 note forces some third row with
period in{5,10,12,18,20,24,30}. Thus the joint period after three choices
belongs to{12,18,24,30,60}.

The residual-fiber count gives the exact multiplier sets
E4={1,2,3,4,8}, E3={1,2,3}, E2={1,2}, E1={1}. Multiplying the five possible
third joint periods by these sets gives exactly37 possible primitive maxima:

```
12,18,24,30,36,48,54,60,72,90,96,108,120,144,162,180,192,
216,240,270,288,324,360,384,432,480,540,576,720,768,864,
960,1080,1152,1440,1920,2880.
```

Every period is a divisor of M. At a state of joint period L with p rows
remaining, the final ratio M/L must lie in the product E1...Ep. This is an
exact necessary condition because every joint-period update multiplies L
by its selected row's n=h/gcd(h,L).

## Completeness of the independent enumeration

For each candidate M, the manager implementation directly materializes the
strict bad-index set of every physical speed1,...,M−1 using integer residues
modulo15M. It begins with M/2 and M/3. At a nonempty residual, any completing
set of p rows has at least one row covering at least1/p of that residual.
The search branches over **every** available physical speed meeting that
gain requirement and the necessary remaining lcm-product requirement.

There is no increasing-speed constraint: such an ordering could be
incompatible with selecting a high-gain row first. Memoization identifies
only an identical unordered set of already selected physical speeds, which
has identical covered indices and identical available speeds.

The alternative period3 speed2M/3 is restored after enumeration. It has the
same bad-index set and the same gcd with M as M/3; the two cannot both occur
in an inclusion-minimal cover. No other equal row sets are collapsed in the
manager implementation. Every completed tuple is checked directly for gcd1
and a private bad index for each of the seven killer rows.

This ordering is complete for all inclusion-minimal seven-row covers under
the two period assumptions: the residual cannot become empty before all
seven rows are chosen, and a high-gain completing row always exists at each
step. The search has no node or time cap.

## Result and independent comparison

All37 candidate maxima completed in2127 manager search states. Exactly44
primitive cores were found, distributed as follows:

| Primitive maximum | Number of cores |
| --- | --- |
| 18 | 4 |
| 24 | 8 |
| 30 | 8 |
| 36 | 16 |
| 48 | 4 |
| 72 | 4 |

The independently written helper enumeration completed in1673 states and
returned exactly the same44 physical speed tuples. Its code was not read
before the manager implementation was complete. The full tuple set, a
private-residue certificate for every row, and hashes binding the code and
comparison input are in `issue-297/independent-conditional-census.json`.

This is an unbounded **conditional** classification because its37-anchor
domain has been derived for arbitrary scales; it is not merely a search up
to2880 without a reduction. Presence of period2 and period3 has not been
proved here. The computation does not cover minimal maximal-anchor covers
with eight or more rows. None of these results is a counterexample to the
Lonely Runner Conjecture.

Replay the manager implementation with
`python3 notebook/codex/issue-297/independent_conditional_census.py` from this
worktree. It writes a fresh report under `/tmp` and prints a short row for
each completed maximum. The original report is preserved separately.

