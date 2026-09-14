# Independent conditional forty-four-core census by residual recursion

Status: `sketch`; independent implementation within the Codex family only.
Claude or human review is required.

Root wrote `helper_direct_core_census.py` from the literal row definition and
the complete high-gain branching argument. It did not read either author's
census implementation or import the earlier 37-anchor reduction. Its only
arithmetic dependency is root's previously independent
`helper_state_graph_audit.py`. The helper preserved these exact bytes and
reran the complete census. This is root's independent implementation, not
another independently authored helper implementation.

The result is 438 residual states, 1,069 qualifying physical row edges and
22 distinct five-row suffix sets. Restoring each of the two physical
period-3 numerators gives exactly 44 primitive cores. The largest residual
period visited is 360. Every returned core is rechecked with literal
integer masks for full coverage, gcd one and a private endpoint for every
row. The output equals the previously tracked forty-four-core inventory
exactly: maxima 18,24,30,36,48,72 with counts 4,8,8,16,4,4.

## Completeness argument

The statement is conditional: seven smaller positive integer speeds form
an inclusion-minimal cover of the maximal lower endpoints, and reduced
periods 2 and 3 occur. The target remains fourteen moving velocities and
fifteen total runners, with one common time family and threshold 1/15.
All bad sets are strict; equality is safe. No coordinatewise scaling or
phase translation is used.

The reduced period-2 row is `(2,1)`. Either period-3 row `(3,1)` or `(3,2)`
has the same bad mask. A minimal cover cannot contain both identical
period-3 masks. Select the period-2 row and one period-3 row first. Their
remaining indices are precisely `{1,5}` modulo six, and five rows remain.

For any state with r remaining slots and exact periodic residual R modulo
L, some row in any completing family covers at least a fraction 1/r of R.
Writing `n=h/gcd(h,L)`, the open arc bound requires
`r ceil(2n/15)>=n`, so n belongs to the finite exact set E_r. Enumerating
every such n, every h dividing Ln with `h/gcd(h,L)=n`, and every physical
unit numerator `1<=a<h` therefore includes a possible next row from every
completion. The code retains precisely the rows meeting the direct integer
gain test. Subtracting the row and replacing the residue set by its true
period preserves the identical infinite subset of indices.

Induction on r proves that this recurrence returns every completing set
with at most r rows: a completing family supplies a high-gain first row,
then its remaining members appear in the recursively enumerated suffix.
Memoization merges only equal residual states. The actual physical `(h,a)`
pairs are retained in every returned suffix set, so equal residual children
do not lose distinct physical speed families. Every empty residual returns
the newly selected row as a completed suffix. All returned suffixes have
exactly five rows; a shorter one would trigger the explicit failure check.

For a physical row family, put `M=lcm(h_1,...,h_7)` and `w_i=M*a_i/h_i`.
Since `gcd(a_i,h_i)=1`, `gcd(M,w_i)=M/h_i`. Hence

    gcd(M,w_1,...,w_7)=M/lcm(h_1,...,h_7)=1.

Conversely, in any primitive normalized physical core, the same identity
forces its actual maximal speed to equal that lcm. Thus the recurrence's
reconstruction neither misses a possible primitive maximal speed nor
introduces an unsupported normalization. All numerators are between zero
and h, so every reconstructed speed is strictly between zero and M.
Restoring both period-3 numerators supplies every physical choice.

This establishes the completeness obligation without assuming a finite
list of possible maximal speeds. It still does not establish necessity of
periods 2 and 3; those remain separate graph-certificate obligations.

## Reproduction

Run `helper_direct_core_census.py --common-checker helper_state_graph_audit.py
--expected-inventory helper-fortyfour-primitive-cores.json --output PATH`.
The expected inventory is used only for final exact comparison, after the
full candidate set has independently been generated. The fresh report is
`helper-direct-census-audit.json`; the original root output is preserved as
`helper-direct-census-root-audit.json`. Both bind source and inventory hashes.
