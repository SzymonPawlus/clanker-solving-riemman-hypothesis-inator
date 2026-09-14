# Sharp upward ratio for a six-row endpoint cover

Status: `sketch / exact finite certificate`, pending independent cross-family
or human review. This is a new attack, separate from the frozen maximal-
anchor seven-row classification.

## Statement

Let u>0 be an integer anchor and let at most six positive integer speeds
cover all of its lower endpoints (15j+1)/(15u), j modulo u, with strict
forbidden distance <1/15. Some killer speed is at least 13u/12.

The ratio is sharp: at u=12, speeds {4,5,6,7,11,13} cover every endpoint.
Private endpoint indices for these six speeds are respectively 3,7,2,5,1,11.
Their maximum is exactly 13u/12. This is an endpoint-cover theorem, not a
counterexample to Lonely Runner.

Consequently, in an arbitrary fourteen-speed tuple of maximum M, every
anchor u>12M/13 requires at least seven killer rows if all its endpoints are
covered. The strict inequality on u is needed because of the sharp example.

The ambient target remains fourteen moving velocities, fifteen total
runners, at threshold 1/15. Every row acts on one common endpoint family.
All danger tests are strict and equality 1/15 is safe. Signs may be removed
and common gcd normalization is valid; no coordinatewise scaling is used.

## Finite reduction, including nonmaximal anchors

Assume for contradiction all killers satisfy w<13u/12. Reduced row data are
h=u/gcd(u,w), a=w/gcd(u,w), with gcd(a,h)=1 and now

    0<a<13h/12.

Numerators greater than h must be included. Their bad set is the literal
modular set B(h,a)={j mod h: min(s,15h-s)<h}, s=a(15j+1) mod15h.
When h=1, a is a positive integer below 13/12, hence a=1, whose distance at
an anchor endpoint is exactly 1/15; this row is empty. More generally an
h=1 row kills all endpoints only if a is divisible by 15. No such row occurs
under this ratio bound.

For h>=2, the centered integer interval (-h,h) has 2h-1 integers. Only one
residue class modulo 15 can represent a bad phase, so every row has at most
ceil((2h-1)/15) bad indices. This holds for every numerator a, including
a>h. For h>=27, (2h+13)/(15h)<1/6. At h=25,26 the exact ceiling is four,
also less than h/6. Therefore a six-row cover must contain a row of reduced
period p<=24. All nonempty possibilities have 2<=p<=24.

Choose a row with smallest physical reduced period p. Enumerate every
integer 0<a<13p/12 coprime to p, take its complement, and allow five more
rows, each of physical reduced period at least p. Equal initial bad sets
may be identified because only existence of a covering completion is sought.
The exact minimal period of the residual set may be smaller than p; the
lower bound p on later physical row periods is retained separately.

At a state (p,r,L,R), r is the number of remaining rows and R is a nonempty
periodic residual set. For any new row h,a, put n=h/gcd(h,L). Its conditional
hit fraction on each L-fiber is at most ceil(2n/15)/n. Some completing row
must hit at least 1/r of the residual, so n lies in E_r. For r<=5 these sets
are E5={1,2,3,4,5,8,9,10}, E4={1,2,3,4,8}, E3={1,2,3}, E2={1,2}, E1={1}.
The bound (15-2r)n<=14r proves the table is exhaustive.

Enumerate each h>=p dividing Ln with h/gcd(h,L)=n, and all coprime
0<a<13h/12. Lift the row and residual to Ln and keep precisely those rows
satisfying r*hits>=n*|R|. Subtract its bad set, reduce to the exact smallest
residual period, retain the physical lower period bound p, and decrement r.
Every hypothetical cover supplies one retained child. Induction on r makes
the resulting finite state enumeration complete.

## Frozen certificate

The completed graph has 169 distinct initial row-set roots, 279 states,
151 distinct child edges, and largest residual period 180. No empty
residual occurs. It exhausts every initial p=2,...,24 with no resource cap
reached. The graph is `issue-297/upper-anchor-six-ratio-13-12.graph.json`;
its summary is `issue-297/upper-anchor-six-ratio-13-12.json`. Both are bound
to the generator `issue-297/upper_anchor_six_search.py` by recorded SHA-256.

The JSON state is (minimum_period,remaining,period,missing_hex). Every child
records a representative [h,a] and its full next state. The graph records
all roots, the strict ratio bound, and explicit completion/cover-found
fields. An independent checker must reconstruct every allowed initial
numerator, every exact child state, and every representative row; compare
complete root/child sets; check nonempty residuals and decreasing r; and
reject incomplete graphs. Equality in 12a<13h is excluded exactly by
integer arithmetic.

This certificate supports the sharp theorem subject to independent review.
It gives a new all-anchor necessary condition; it does not exclude covers
by seven or more rows in the high-anchor band or solve the fifteen-runner
case.
