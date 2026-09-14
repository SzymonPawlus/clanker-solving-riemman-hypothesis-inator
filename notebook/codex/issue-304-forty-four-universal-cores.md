# Universal rational measures for forty-four primitive cores

Status: `sketch`; exact author audit passed. Independent same-family checking
is in progress, and Claude or human review is required before promotion.

The single-measure argument now covers every one of the forty-four explicitly
listed eight-speed patterns in
[all-forty-four-cores.json](./issue-304/all-forty-four-cores.json). For every
positive integer `c`, adding any six arbitrary positive integer speeds below
`c max(P)` to any listed subsystem `cP` leaves one common rational time at
which all speeds have distance at least `1/15` from an integer.

The patterns have primitive maxima distributed as follows:

| Maximum | Number of explicitly certified patterns |
|---:|---:|
| 18 | 4 |
| 24 | 8 |
| 30 | 8 |
| 36 | 16 |
| 48 | 4 |
| 72 | 4 |

The first twenty certificates are unchanged from the frozen twenty-core
result. The other twenty-four use rational points already good for their
fixed subsystem, including quarter points inside exact good intervals. All
atom weights are positive. Every total lies in `(6,61/10]`; the smallest
total across all forty-four is `60067/10000`.

The [universal rational-measure lemma](./issue-304-twenty-universal-cores.md)
is restated here to make the obligations clear. Atoms `(x_i,z_i)` good for
every speed in `P` are lifted to `(k+x_i)/c` with weight `z_i/c`. An arbitrary
new speed `w` reduces to `n=c/gcd(c,w)`, `q=w/gcd(c,w)`. Its total killed
weight is

```text
sum_i z_i #{0<=k<n: ||q(k+x_i)/n||<1/15} / n.
```

For `n<=30`, all coprime `1<=q<max(P)n` are checked exactly, excluding fixed
speeds only at `n=1`. For `n>=31`, the uniform bound

```text
(61/10) ceil(2n/15)/n <= (61/10)(2n+14)/(15n) <=1
```

controls every column. Hence six new speeds kill weight at most six, while
the total exceeds six. A supported rational time survives them all.
Forbidden arcs remain strict, so equality is a witness. The problem has
fourteen moving speeds and fifteen total runners; all coordinates use the
same time. Only the fixed subsystem is scaled commonly, while the six added
speeds remain arbitrary.

The fresh [author audit](./issue-304/check_forty_four_cores.py) invokes the
exact arithmetic checker on the entire combined manifest. It verified all
primitive atom inequalities, positivity, exact totals, and 433,328 finite
column inequalities. The largest finite load is `9999/10000`. The complete
[audit record](./issue-304/all-forty-four-author-audits.json) binds the
certificate manifest with SHA-256

```text
e8c26ff9ca2b405666ec33a4872f94a8b2897c8164dfa4d462ad3a51a56d23e6.
```

This note claims an unconditional all-scale obstruction for each explicitly
listed pattern, subject to its supplied exact finite checks. The manager's
separate classification shows why this particular collection is useful:
conditionally on a minimal seven-row maximal cover containing both period
two and period three, its primitive pattern belongs to this forty-four-core
list. That classification has its own finite reduction and independent
checks; it is not assumed in proving any of the individual measures here.

Necessity of periods two and three is a separate state-graph attack. The
earliest candidate graph leaves contained small negative rounding artifacts
and were rejected by the helper; replacement nonnegative leaves are being
audited. No rejected graph is used in the present forty-four-core statement.
The supplied core measures were directly checked for positivity and do not
contain that defect.

Clock-confirmed author checkpoint: 2026-09-14 20:42:21 UTC. Research continues
through the requested work cycle; these certificates do not prove the full
`k=14` conjecture or address every possible larger maximal-cover core.
