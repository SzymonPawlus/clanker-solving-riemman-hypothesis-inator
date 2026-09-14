# Independent audit of the greedy lcm finite reduction

Status: `sketch`, no cross-family review. Active threshold 1/15, fourteen
moving velocities and fifteen total runners. This is a theorem about
inclusion-minimal seven-row covers of maximal-anchor lower endpoints,
not a finite reduction of the full fourteen-speed Lonely Runner problem.

The argument below was reconstructed from the manager's mathematical
specification, without reading a search or checker implementation.

## Conditional grid count

Let selected row periods have lcm L. Their uncovered set is a union of
residue classes modulo L. Fix one such class j=s modulo L, and consider a
further reduced row (h,a), gcd(h,a)=1, 0<a<h. Put d=gcd(h,L) and n=h/d.
In one common period lcm(h,L), that class has n compatible lifts, which
we may write j=s+Lk for 0<=k<n. The row phases are

    a(15s+1)/(15h) + (a L/d) k/n   modulo one.

Both gcd(a,n)=1 and gcd(L/d,n)=1 hold, so these phases form a translated
uniform n-point grid. An open arc of length 2/15 contains at most
ceil(2n/15) points of such a grid. Consequently the row covers at most
ceil(2n/15)/n of each uncovered class, and therefore of their union.
Equality remains safe on the Lonely Runner side: the arc is strictly open.

Suppose r remaining rows cover the nonempty residual set. Averaging their
incidence counts shows that at least one has conditional coverage at least
1/r. It follows that one row has

    n in E_r = {n>=1: r ceil(2n/15)>=n}.

Adding that row changes the selected lcm from L to exactly L*n.

## Exact finite multiplier sets

For n=15m+s, 0<=s<15, the condition is

    (15-2r)m <= r ceil(2s/15)-s.

For r<=7 the left coefficient is positive; the fifteen inequalities give
a complete, analytic enumeration, with no assumed numerical cutoff:

    E1 = {1}
    E2 = {1,2}
    E3 = {1,2,3}
    E4 = {1,2,3,4,8}
    E5 = {1,2,3,4,5,8,9,10}
    E6 = {1,2,3,4,5,6,8,9,10,11,12,16,17,18,23,24}.

The generic E7 has maximum 98, not 91. In particular n=98 satisfies
7 ceil(196/15)=98. This distinction does not invalidate the manager's
bound, because the first unconditioned row has a stronger exact count.

## The first-row improvement and normalized anchor

Some row in any seven-row cover has unconditional density at least 1/7.
The centered residue count is at most ceil((2h-1)/15), and

    ceil((2h-1)/15) <= (2h+13)/15.

Thus h/7 <= (2h+13)/15 gives h<=91. This argument uses the integer
centered progression before any conditioning, and cannot simply be
substituted for the generic E7 bound.

Choose such a first row and then use the conditional averaging step with
r=6,5,4,3,2,1. Inclusion-minimality ensures that the residual set stays
nonempty before the final row: otherwise the already chosen proper subset
would itself cover the anchor. Hence all seven row periods are selected,
and their lcm satisfies

    L_final <= 91*24*10*8*3*2*1 = 1,048,320.

For maximal anchor M and speeds w1,...,w7, the reduced periods are
hi=M/gcd(M,wi). Prime valuations give the exact identity

    lcm(h1,...,h7) = M/gcd(M,w1,...,w7).

After dividing all eight speeds by their common gcd, the maximal anchor is
therefore at most 1,048,320. A separate proof that some row period is at
most 16 would allow choosing it first, giving 16*24*10*8*3*2=184,320;
that optional premise is not used in the unconditional bound here.

The minimality hypothesis matters. Arbitrary redundant rows could lower
the gcd of an already covered subsystem and increase the normalized anchor
without contributing anything to its cover. Likewise this bound concerns
seven-row cores only; a maximal anchor covered minimally by eight or more
of the thirteen other velocities has not been reduced to this box.
