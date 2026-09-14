# Explicit closure of the at-most-six-row obligation

Status: `sketch / exact complete certificate`, pending independent cross-family
or human review. This is separate from the frozen seven-row census.

The period-two and period-three necessity statements concern covers by at most
seven rows. They do not alone imply that a cover needs seven rows. The
conditional forty-four-core census only records inclusion-minimal covers with
exactly seven rows and must not silently supply this missing assertion.

Here the remaining exact obligation is excluded directly: the odd residues
not divisible by three cannot be covered by four further maximal-anchor
rows. Start at (remaining,L,R)=(4,6,{1,5}). For every state, enumerate every
physical reduced row (h,a), 0<a<h and gcd(a,h)=1, satisfying
n=h/gcd(h,L) in E_remaining and the exact high-gain inequality. Use

    B(h,a)={j modulo h: min(a(15j+1) mod15h,
                           15h-a(15j+1) mod15h)<h}.

The multiplier sets are E4={1,2,3,4,8}, E3={1,2,3}, E2={1,2}, E1={1}.
They follow from the equally spaced grid bound and the finite tail inequality
(15-2r)n<=14r. At each step lift to lcm(L,h), subtract the selected bad set,
reduce to the exact smallest residual period, and decrement the number of
rows remaining. Any completion must contain a high-gain row, so induction
on the remaining count makes this enumeration complete. Every row period
is included by enumerating h|Ln with h/gcd(h,L)=n. There is no empirical
period cutoff and no assumption that the primitive maximum is small.

Exactly 25 states and 43 distinct child edges arise, with maximum residual
period 72. The state counts by rows remaining are 1,7,15,2 for 4,3,2,1.
No empty residual occurs and all terminal child lists are empty. At the root,
the seven distinct children have representative rows

    (12,5), (12,7), (12,11), (18,1), (24,5), (24,7), (24,1).

The full graph is `issue-297/six-with-two-three-excluded.json`, with generator
`issue-297/exclude_six_with_two_three.py`. The generator uses the direct
modular bad-set definition, rather than the centered-integer implementation
used in the earlier period-three graph. It records its SHA-256 in the
certificate. An independent graph audit must regenerate all distinct
children, check every representative, and verify reachability and strict
remaining-count descent.

Thus a maximal-anchor cover containing periods two and three requires at
least seven rows, conditional on the exact finite certificate's validation.
Together with the separate necessities of periods two and three in any cover
by at most seven rows, this closes the lower-bound gap without relying on the
older charge-ranking proof with its acknowledged tail issues.

All rows share the same endpoint index and threshold. The ambient target is
fourteen moving velocities, fifteen total runners, at 1/15. The danger
inequality is strict; the sanity fixture (h,a,j)=(16,1,1) has distance exactly
1/15 and is safe. Only common normalization and periodic lifts are used.
This result does not treat minimal maximal-anchor covers of eight or more
rows or claim the full Lonely Runner Conjecture.
