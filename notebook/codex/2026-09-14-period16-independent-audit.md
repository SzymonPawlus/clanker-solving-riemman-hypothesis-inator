# Independent audit: a seven-row cover has smallest period at most 16

Status: `sketch`, requiring Claude/human review. This concerns seven-row
maximal-anchor covers at threshold 1/15, within the fourteen-moving-runner
target. Author implementation was not read.

For h>=92 every reduced row has density at most
(2h+13)/(15h)<1/7, so seven such rows cannot cover. It remains to exclude
smallest period p=17,...,91. Fix its nonempty bad set A of cardinality b.
For another row (h,a), d=gcd(p,h), let N be its bad-set cardinality and let
N_s count its bad residues congruent to s modulo d. Its exact whole-space
charge outside A is

    C = N/h - d/(ph) * sum_(s in A) N_s.

The centered integer interval (-h,h) gives

    N <= ceil((2h-1)/15) <= (2h+13)/15,
    N_s >= floor((2h-1)/(15d)) = ceil(2h/(15d))-1
        >= 2h/(15d)-1.

Hence, for every h>=301,

    C <= min(41/301,
             (2/15)(1-b/p)+(13/15+b)/301).

The independent checker enumerates all distinct nonempty B(h,a) for
2<=h<=300 using literal residues, and for every base with17<=p<=91 selects
the six largest conditional charges among h>=p, excluding the identical
base row. Six virtual tail rows at the displayed upper bound are included
before ranking, allowing all possible numbers of tail rows. Duplicate
residue sets at one period are removed. A nonempty row has fundamental
period h because its nontrivial cyclic orbit could not fit inside an open
arc of length2/15, so there is no omitted cross-period duplicate issue.

The exact computation inspected27,375distinct rows,2,472base patterns and
64,527,128finite candidate comparisons. Every total b/p plus the six
largest charges is strictly below one. The largest value is1574/1581,
attained at p=17 with a=1,14,15,16. Thus p<=16.

Combined with the independently reconstructed greedy-lcm multiplier sets,
any primitive inclusion-minimal seven-row maximal cover has maximal speed
at most16*24*10*8*3*2=184,320. This is not a finite bound for arbitrary
fourteen-speed tuples or for minimal covers having eight or more rows.

Replay `helper_period16_audit.cpp`, redirecting its integer table to a text
file, then run `helper_period16_summary.py` on that file. The summary uses
exact Python fractions and records source/table SHA-256 hashes. The frozen
table and summary are `helper-period16-topcharges.txt` and
`helper-period16-audit.json`.
