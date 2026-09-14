# Independent helper audit, 2026-09-14

Status: `numerical` for finite computations; `sketch` for mathematical arguments.
Issue #301; active target: 14 moving velocities, 15 total runners, threshold 1/15.
Productive cycle started 19:56:45 UTC. No eligible other-party Lonely Runner PR
was open at the first queue check. Author implementations were not inspected.

## Mandatory filters before implementation

1. Quantifiers: the original input is one arbitrary tuple of nonzero integer
   velocities; an endpoint witness must work for every coordinate at one time.
   The present audit only bounds covers of endpoints of one maximal anchor;
   failure to find such a cover is not a reduction of the full problem.
2. Boundaries: at anchor u the endpoint t=(15j+1)/(15u) is successful exactly
   when every centered residue is at least u. Killing uses the strict test
   min(r,15u-r)<u. At u=1,w=1,j=0 the residue equals u and is not killed.
3. Scaling: only one common scaling or gcd normalization is used. In reduced
   rows h=u/gcd(u,w), a=w/gcd(u,w); this is a pairwise change of notation,
   not an assertion of coordinatewise scaling symmetry.
4. Dimension: k=14 moving velocities and k+1=15 total runners throughout.

## Mathematical specification used

For 0<a<h and gcd(a,h)=1, enumerate

    B(h,a)={j in {0,...,h-1}: min(r,15h-r)<h,
            r=a(15j+1) mod 15h}.

An independent faster equivalent enumerates integers e in (-h,h) congruent
to a modulo 15 and solves j=a^(-1)(e-a)/15 modulo h. For a singleton base
{0 mod p}, let d=gcd(p,h). The charge outside the base is

    |B|/h - d #{b in B:d divides b}/(ph).

Only identical residue sets at the same period are deduplicated. Every
nonempty row has fundamental period h: a proper period would force a whole
nontrivial finite cyclic coset into a circular open interval of length 2/15,
whereas the shortest circular arc containing such a coset has length at
least 1/2.

The finite valuation ranking retains the 2-adic and 3-adic redundancy
requirements only; omitting other primes weakens the constraints and so is
safe for an upper bound. Every reported period ceiling remains explicit.

## First bounded checkpoint

At H=200, the independent enumeration found 12,209 distinct nonempty rows
and removed 22 same-period duplicates. Direct residue enumeration agreed
with the faster centered-integer implementation for every reduced pair
through h=60. All seven displayed p=4 valuation-class maxima in the earlier
corrected note were reproduced exactly. The global p=3 bound was 2/3 in
class (e2,e3)=(2,1); the global p=4 bound was 146/195 in class (2,2).
The strict p=4 margin is only 1/780, so exact arithmetic matters.

## Independent semantics for the proposed universal dual

Let P={1,5,6,7,9,11,13,18}, and let D contain its surviving primitive lower
endpoints (u,r). At common scale c, each such type has precisely c lifted
endpoints, indexed j=r+u l for 0<=l<c, at time

    t=(l+(15r+1)/(15u))/c.

Assign each lift weight z(u,r)/c. An additional speed w<18c has g=gcd(c,w),
n=c/g, q=w/g, gcd(n,q)=1, and 0<q<18n. As l runs through c values, its
residue modulo n repeats exactly g times. Its total killed weight is

    (1/n) sum_(u,r) z(u,r) C(n,q,u,r),

where C counts 0<=l<n satisfying the strict forbidden inequality. At n=1,
the q in P are excluded because w is already a fixed speed. For n>1 there
are no such exclusions. Thus a rational z of total S>6 with all column
weights <=1 prohibits any six extra speeds from covering D, at every scale.
This requires no assertion that off-lattice columns lie in the convex hull
of primitive columns.

For each primitive type the n samples form a translated uniform n-point
grid, since gcd(n,q)=1. Hence C<=ceil(2n/15), with the open-arc endpoint
convention. The last n for which 7 ceil(2n/15)>n is 83. To prove this without
an arbitrary cutoff, write n=15m+r, 0<=r<15. The inequality is equivalent to
m>=7 ceil(2r/15)-r; checking these fifteen fixed residue classes shows that
it holds for every n>=84. Consequently S<=7 proves every tail column once
the finitely many 0<q<18n, gcd(n,q)=1, n<=83 are checked exactly.

## Universal P18 certificate audit, 20:01--20:03 UTC

The supplied 24 positive weights have exact total 6011/1000. The independent
direct-integer checker inspected all 38,548 columns with 1<=n<=83 and found
maximum 749/750, attained at both (n,q)=(3,49) and (3,53). It also checked
8,130 literal lifted columns for every c=1,...,30 and every allowed speed
w<18c; these agree exactly with the quotient formula. The exact mass gives
an analytic tail starting at n=25, by the fifteen residue-class inequalities
stored in the JSON audit. The stronger finite range through 83 was retained.

Three sibling fixed subsystems passed the same independent checks:

| Fixed primitive speeds | Total weight | Maximum finite column |
| --- | --- | --- |
| 1,5,6,9,11,13,14,18 | 6019/1000 | 999/1000 at (1,15) |
| 1,5,7,9,11,12,13,18 | 1507/250 | 999/1000 at (1,4) |
| 1,5,9,11,12,13,14,18 | 759/125 | 999/1000 at (1,4),(1,15) |

Each of these had 38,548 finite columns and 8,130 literal scale fixtures,
and each exact-mass tail starts at n=25. These internal checks are all from
the Codex family and do not constitute Claude/human review.

## A simpler complete tail closure for smallest periods 3 and 4

This argument concerns an inclusion-minimal cover of a maximal anchor by
six rows, whose smallest reduced period is p=3 or p=4. The base row is
{0 modulo p}. It does not presume the earlier seven-row theorem.

For another row, put d=gcd(p,h), and count

    N = #{e in (-h,h): e=a modulo 15},
    S = #{e in (-h,h): e=a modulo 15d}.

Because gcd(a,d)=1, the condition j=0 modulo d is exactly e=a modulo 15d.
The conditional charge is C=(N-(d/p)S)/h. Elementary counts of points in
an open interval give N<2h/15+1 and S>=2h/(15d)-1. Hence

    C < 2(p-1)/(15p) + (1+d/p)/h
      <= 2(p-1)/(15p) + 2/h.

At p=3 this is below 1/10 whenever h>180. At p=4 it is below 7/60 whenever
h>120. The finite enumeration below also checks that the four largest
distinct charges are respectively

    p=3: 1/6,2/15,2/15,2/15; sum=17/30,
    p=4: 1/6,1/6,3/20,3/20; sum=19/30.

The tail bounds are smaller than these leaders, so these are global leader
bounds, not merely finite rankings. A five-row sum capable of reaching the
remaining mass (2/3 or 3/4) must give every selected row at least 1/10 or
7/60 respectively. Therefore every threatening row has h<=180 or h<=120.
This proves the finite reduction without infinitely many valuation cases.

The clean-room enumeration then gives the exact counts:

| p | Period ceiling | Rows above threshold | Threatening five-tuples | After 2/3-adic redundancy | After full lcm redundancy |
| --- | --- | --- | --- | --- | --- |
| 3 | 180 | 125 | 682 | 4 | 4 |
| 4 | 120 | 46 | 285 | 0 | 0 |

A threatening tuple has conditional-charge sum at least the complement
mass. Identical residue sets are removed before selecting distinct rows.
The 2/3-adic sieve requires that every positive maximal exponent among the
base and five chosen periods occurs at least twice; full redundancy tests
that each period divides the lcm of the others. These are necessary by the
private-prime-power peeling argument, independently reconstructed below.

All four p=3 survivors have periods 4,5,10,10,60, with numerators 1,1,7,9
for the first four and numerator 17,19,23,29 for period 60. Each has charge
exactly 2/3 and leaves exactly 13 residues uncovered modulo 60. The complete
residue lists are in `helper-smallest-period-audit.json`. Thus no six-row
cover can have smallest period 3 or 4. This is a finite-computation-backed
sketch until cross-family review, despite the complete tail reduction.

For the peeling implication, let h be one period, L the lcm of the others,
and q=gcd(h,L). If h does not divide L, m=h/q>=2. In a residue class modulo
L missed by all other rows, the h-residues range over a complete coset of
q modulo h. Multiplication by a transforms their phases into a translated
uniform m-point grid. No such grid fits inside the forbidden circular open
arc of length 2/15: its shortest containing arc has length 1-1/m>=1/2.
Therefore at least one compatible residue also survives the selected row,
contradicting a cover. Every inclusion-minimal cover must be lcm-redundant.

## Generic rational supports and constructive extraction

All sixteen further M=24/M=30 support certificates passed an independent
direct-grid audit. For each positive rational atom x and each primitive
speed u, the check was exactly 15*min(u*num(x) modulo den(x), its negative
residue)>=den(x). Every reduced extra-speed column with n<=30 was then
enumerated: 6,664 columns per M=24 family and 8,332 per M=30 family. The
uniform-lift identity was separately checked by direct enumeration for all
c=1,...,10. Every exact weight total lies in (6,61/10], and the exact-total
tail starts at n=25 in each case. Full source hashes, totals, maxima and
maximizers are stored in `helper-generic-dual-audit.json`.

The three subsequent new primitive-core certificates likewise passed:
totals 3037/500,759/125,152/25 and finite maxima 499/500,997/1000,1997/2000.
Their checker counts were 10,000,13,336,10,000 columns respectively.

An independent witness extractor was implemented without inspecting the
manager's implementation. For a rational safe primitive atom x=A/B, scale c,
extra speed w, and integer interval L<=j<R, set

    D=cB, a=wB, b=w(BL+A), N=R-L, K=ceil(D/15).

The strict bad residues are exactly [0,K) and [D-K+1,D). Write
F(N,a,b,D)=sum_(0<=j<N) floor((aj+b)/D). Then the bad count is

    N + F(N,a,b-(D-K+1),D) - F(N,a,b-K,D).

This handles denominators not divisible by 15, including equality cases.
The floor sum is computed by an independent lattice-point reciprocity:
first remove signed quotient parts of a,b modulo D; with 0<a<D,0<=b<D and
J=floor((a(N-1)+b)/D), the remaining sum is

    NJ - F(J,D,D-b+a-1,a).

The modulus decreases, giving a Euclidean algorithm. For each atom define
the signed score N minus the sum of six bad counts. The dual certificate
implies that some full fiber has positive score. The scores add over
disjoint intervals, so repeatedly retaining a positive half reaches one
index with score one and therefore no forbidden coordinate. Its one common
witness time is (j+x)/c, checked again by exact integer inequalities.

Independent fixtures passed: 124,930 signed floor-sum cases, 20,000 endpoint
interval cases, 50,004 generic rational interval cases, and 100 complete
endpoint-family witnesses at scales 1,...,100. Sixteen generic supports
were also exercised at c=37 and c=10^100+267 with six arbitrary extras;
every final time was checked exactly against all fourteen velocities.
The huge-scale cases required 332 bisections, roughly half a second each.
These tests support the implementation; the argument above supplies the
arbitrary-scale semantics, still awaiting cross-family review.

## Primitive-cover completeness counterexamples and bounded census

The inherited suggestion that every minimal seven-row maximal cover is a
scaled one of the twenty M=18/24/30 cores is false. The primitive vectors

    (2,12,15,18,26,28,33,36),
    (2,11,13,16,20,24,28,48)

each have gcd one. Direct strict-residue checks show that their seven
nonmaximal speeds cover every maximal-anchor lower endpoint, and every row
has a private residue. The first vector's private sets, in increasing speed
order, are {17,35}, {3,15,21,33}, {7,31}, {2,8,10,16,20,26,28,34},
{11,29}, {5,23}, {13,25}. Neither is a Lonely Runner counterexample.

An independent exhaustive search subsequently enumerated every minimal
seven-row cover among the actual speed subsets W of {1,...,M-1}, |W|=7,
for every 8<=M<=120. No symmetry quotient was used in the search; afterwards
gcd(W union {M})=1 identifies primitive covers. Common scaling preserves
the exact residue pattern by lifting, justifying this terminology. There
is no claimed reduction of unbounded velocities to this bounded domain.

Exactly 44 primitive covers occur, at the following anchors:

| M | All minimal seven-row covers | Primitive covers |
| --- | --- | --- |
| 18 | 4 | 4 |
| 24 | 8 | 8 |
| 30 | 8 | 8 |
| 36 | 20 | 16 |
| 48 | 12 | 4 |
| 54 | 4 | 0 |
| 60 | 8 | 0 |
| 72 | 32 | 4 |
| 90 | 12 | 0 |
| 96 | 12 | 0 |
| 108 | 20 | 0 |
| 120 | 16 | 0 |

All other anchors in the stated domain have zero such covers. The search
branches on an uncovered residue and partitions possible covers according
to the first available chosen row covering it. Earlier alternatives are
removed only within later sibling branches. The union of remaining rows
and the sum of the largest remaining new-coverage counts provide necessary
pruning conditions. Final covers are accepted only if all seven rows have
private residues. Every primitive output carries these direct certificates.
Explicit time caps report incomplete rather than negative; none of the
8<=M<=120 runs hit its cap. An unpruned subset enumeration is additionally
cross-checking the first four nonzero anchor counts.

## Primary literature context checked during the census

[Gonçalves--Ramos, *Bounds for the Lonely Runner Problems Via Linear
Programming*](https://doi.org/10.1007/s00574-021-00272-7), §1.1 and Theorem 1,
already develops LP bounds through sign-constrained trigonometric
polynomials. Its sections 2--3 prove these bounds and discuss refinements.
This is relevant precedent for computational LP certificates.

[Kravitz, *Barely lonely runners and very lonely
runners*](https://arxiv.org/html/1912.06034), §4, describes the pre-jump:
adding multiples of 1/g preserves the positions of g-divisible speeds while
moving the other runners. Theorem 7.2 uses this grid to move a further
runner away from zero. The present uniform-lift construction is a weighted
finite-atom use of that established mechanism. Neither source inspected
here directly supplies the specific core certificates being checked, but
this limited literature check does not establish novelty of the method or
of every restricted family.
