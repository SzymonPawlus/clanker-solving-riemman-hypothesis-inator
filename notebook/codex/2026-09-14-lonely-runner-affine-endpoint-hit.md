# Exact endpoint hits for affine-template lifts

Status: `sketch`, independently derived by the manager after the prover's
composite-lift suggestion. This is a separate extension; the frozen prime-lift
criterion is unchanged. The frontier remains fourteen moving speeds, fifteen
total runners, at 1/15. An eight-row anchor cover alone is not a counterexample
to that conjecture.

Let M,q be positive integers with gcd(q,M)=1. Put

    G(M,q)={q(15j+1)/(15M) mod1: 0<=j<M}.

For a reduced rational endpoint u/v in [0,1), including 0/1, the exact criterion is

    u/v belongs to G(M,q)
    iff v divides 15M and (15M/v)u is congruent to q modulo15.

Necessity follows by multiplying an equality modulo one by 15M. For sufficiency,
write T=(15M/v)u. The congruence makes (T-q)/15 an integer. There is exactly one
j modulo M solving qj=(T-q)/15 modulo M, because gcd(q,M)=1. Multiplication by15
then gives q(15j+1)=T modulo15M. No division by a nonunit modulo15 is used.

Now let a_i,b_i be integers, a_i nonzero, and suppose for some open interval I
all physical ratios a_i*x+b_i lie strictly between zero and one. Define the
strict forbidden sets on the z-circle by

    B_i={z: ||a_i*z+b_i/15||<1/15}.

Every endpoint of B_i has reduced denominator dividing 15|a_i|. If the union
of the B_i covers every open cell in their endpoint arrangement, its remaining
safe points can only be endpoints. For x=q/M in I the physical speeds
w_i=a_i*q+b_i*M satisfy

    w_i*(15j+1)/(15M) = a_i*z_j+b_i/15 modulo1.

Thus if G(M,q) avoids all endpoints, the physical rows cover every lower anchor
endpoint exactly. Equality at the forbidden boundary is safe throughout this
argument; it is the proved grid avoidance that removes such equalities.

Take M=15p, where p is prime and p>max(5,|a_i|), and gcd(q,15p)=1. Suppose no
a_i is divisible by15. A grid-hit endpoint denominator v would have to divide
225p and make T=(225p/v)u coprime to15, since T=q modulo15. Reducedness of u/v
therefore forces v to contain both9 and25. But v divides15|a_i|, which cannot
contain both these factors unless15 divides a_i. Contradiction. Hence every
endpoint is avoided.

The additional restriction that every slope is divisible by3 or5 is unnecessary
for avoidance. If that restriction holds and no slope is divisible by15, then
the individual reduced periods are exactly5p or3p:

    M/gcd(M,w_i)=15p/gcd(15,a_i).

If gcd(a_1,...,a_s)=1, the physical anchor-plus-speeds tuple is primitive.
For every sufficiently large prime p there are eligible q with q/(15p) in I:
any long enough integer interval contains an integer coprime to15, and at most
the fourteen integers p,2p,...,14p must additionally be avoided. This gives
arbitrarily large primitive physical covers if a qualifying affine cell cover
is actually found. No such eight-row template is asserted here.

## Stronger power-of-three lift, proposed by the root agent

The root agent independently proposed the simpler choice M=3^n, which works
for every fixed integer-affine open-cell cover. Let s=max_i v_3(|a_i|), choose
n>s and q not divisible by3. Every sampled phase has reduced denominator with
3-adic valuation exactly n+1, because neither q nor15j+1 is divisible by3.
Every affine endpoint has denominator of valuation at most s+1. Hence the grid
avoids every endpoint, and open-cell coverage becomes an exact physical cover.
The reduced periods are3^(n-v_3(|a_i|)), tending to infinity with n. Dividing
the entire anchor-plus-speed tuple by its common gcd does not change any of
these reduced periods. An integer q not divisible by3 exists in any open
interval MI once its length exceeds3. This removes the prime condition and
the assumption that no slope is divisible by15. It also removes every
bad-fifteenth-point requirement from the open-cell discovery search.

This conclusion still requires a single actual finite affine open-cell cover
with a nonempty physical strip. It does not assert that such a template exists,
nor that all possible large physical covers have this integer-affine form.

The independent arithmetic fixture script `issue-297/check_affine_endpoint_hit.py`
compares the criterion against literal rational grid membership and tests
composite endpoint avoidance. It is finite validation of the stated algebra,
not an exhaustive template search or a finite reduction of all fourteen-tuples.
