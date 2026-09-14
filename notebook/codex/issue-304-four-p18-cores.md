# All four recorded eighteen-speed cores have an obstruction at every scale

Status: `sketch`; exact author certificates and same-family clean-room audit
pass. Claude or human review is still required for `verified:review`.

The proof in [the universal-phase note](./issue-304-universal-phase-dual.md)
applies to all four fixed eight-speed patterns below. For every integer
`c>=1`, appending any six arbitrary positive speeds below `18c` to `cP`
leaves a common time at which every speed has distance at least `1/15` from
the nearest integer. Thus each row excludes an infinite family of potential
fourteen-moving-runner counterexamples (fifteen runners in total).

| Fixed pattern P | Number of atoms | Exact total weight | Maximum finite load |
|---|---:|---:|---:|
| 1,5,6,7,9,11,13,18 | 24 | 6011/1000 | 749/750 |
| 1,5,6,9,11,13,14,18 | 26 | 6019/1000 | 999/1000 |
| 1,5,7,9,11,12,13,18 | 26 | 1507/250 | 999/1000 |
| 1,5,9,11,12,13,14,18 | 30 | 759/125 | 999/1000 |

For each pattern all positive atom weights are at exact lower endpoints
already allowed by the fixed pattern. Each total lies strictly between six
and `61/10`. For every reduced denominator `1<=n<=30`, the exact author
checker enumerates all `1<=q<18n` with `gcd(n,q)=1`, excluding fixed speeds
only for `n=1`, and proves the displayed load bound. For all `n>=31`,

```text
T ceil(2n/15)/n <= (61/10)(2n+14)/(15n) <= 1,
```

where the last inequality is precisely `854<=28n`. Hence no unbounded
classification or unproved finite-reduction hypothesis is hidden in this
statement. The finite counts concern a complete set of exceptional
denominators; the scaling integer itself is unrestricted.

The complete certificate set is:

- [first pattern](./issue-304/p18-weights.tsv), SHA-256
  `55d7522ab04f86aa7882d059cba8d49c1b72810b0d43698691ae50c3130f483b`;
- [6,14 pattern](./issue-304/p18-6-14-weights.tsv);
- [12,7 pattern](./issue-304/p18-12-7-weights.tsv);
- [12,14 pattern](./issue-304/p18-12-14-weights.tsv).

[The author checker](./issue-304/check_certificates.py) verifies positivity,
allowedness of every atom, the exact total, every finite column, and strict
boundary fixtures with only the Python standard library. Its generated
[audit manifest](./issue-304/p18-author-audits.json) binds each table to its
SHA-256 and lists the maximum for every finite denominator. This checker
shares the author's interval-count derivation and is not an independent
review. The helper separately derived direct residue enumeration without
reading the author checker and passed all four tables through `n=83`, plus
actual arbitrary-speed lifts at every scale `c<=30`.

No claim is made here that these four patterns exhaust all maximal covers,
or that every fourteen-speed tuple contains one. The infinite obstruction
for each explicitly listed subsystem is unconditional subject only to the
finite arithmetic certificate checks supplied here.
