# Eight-row covers: a relation window of 2,998

Status: `sketch`, requiring independent cross-family or human review. This
is a new self-contained improvement of the prover's frozen 65,534-window
argument at `7bbc832`; that earlier version remains unchanged. No novelty
claim is made for smoothing or the spanning-tree union inequality.

## Statement

Suppose eight positive integer speeds w_i<M cover every lower endpoint
 t_j=(j+1/15)/M, j=0,...,M-1, of the maximal anchor M by the strict condition
||w_i t_j||<1/15. Put D=2998. Then either some reduced row period
M/gcd(M,w_i) is at most D, or there is a nontrivial partition A,B of the
rows such that every cross-pair satisfies

    m w_i+n w_j=cM,
    0<|m|,|n|<=D, |c|<2D.

In the latter case, after choosing x=w_0/M, every other speed ratio has form

    w_i/M=(P_i/Q_i)x+R_i/Q_i,
    0<|P_i|,|Q_i|<=8,988,004, |R_i|<35,952,016.

These integer coefficients range over a finite set. The common rational
parameter x remains unbounded; this is a finite collection of affine
relations, not a finite bound for M or a completed eight-core census.

The motivating target is fourteen moving velocities, fifteen total runners,
at 1/15. Every row is evaluated at the same endpoint family. Equality at
1/15 is safe throughout. Only common scaling and exact integer relations
are used. This result does not assume any seven-row classification and does
not prove that an eight-row cover has period two or three.

## A minorant with a bounded second derivative

Let delta=1/15 and epsilon=7/300. For the circle distance d=||t||, define

    f(t)=1                              when d<=delta-epsilon,
         [1+cos(pi(d-delta+epsilon)/epsilon)]/2
                                          when delta-epsilon<=d<=delta,
         0                              when d>=delta.

The definitions agree at each boundary. The periodic function f is C1, its
first derivative is Lipschitz, and

    0<=f<=1_{||t||<1/15},
    integral f=2delta-epsilon=11/100,
    |f'(s)-f'(t)| <= L |s-t|, L=pi^2/(2epsilon^2),

where the last inequality is on the real periodic lift. It follows from the
piecewise second derivative bound and continuity of the first derivative;
no second derivative at a joining point is needed. In particular,

    |f(x-y)-f(x)+y f'(x)| <= L y^2/2.

The minorant vanishes at the strict forbidden-arc endpoints.

## Squared Fejer kernel: exact second moment

For integer N>=2 define

    F_N(t)=(1/N)|sum_{k=0}^{N-1}exp(2pi i k t)|^2,
    A_N=integral F_N^2=(2N^2+1)/(3N),
    K_N=F_N^2/A_N.

The normalization follows by expanding the finite Fourier coefficients
1-|k|/N for |k|<N and summing their squares. Thus K_N is even, nonnegative,
has integral one, and has degree 2N-2. For 0<|t|<=1/2,

    F_N(t)<=min(N,1/(4N t^2)).

The first bound follows from the finite sum and the second from
|sin(pi t)|>=2|t| and the geometric-sum expression. Split at a=1/(2N):

    integral_{-1/2}^{1/2} t^2 F_N(t)^2 dt
      <=2N^2 integral_0^a t^2 dt
          +(1/(8N^2)) integral_a^(1/2) t^(-2) dt
       =1/(12N)+1/(4N)-1/(4N^2)
       <=1/(3N).

Since A_N>=2N/3, the normalized second moment is at most 1/(2N^2).
Convolve g=f*K_N. The linear Taylor term cancels because K_N is even, so

    ||g-f||_infinity <= L/(4N^2)=pi^2/(8epsilon^2 N^2)=eta.

Moreover 0<=g<=1, its mean is alpha=11/100, and its Fourier degree is at
most 2N-2. This second-moment argument replaces the first-moment Lipschitz
estimate in the earlier frozen version.

Take N=1500, so D=2998. The elementary inequality pi^2<10 gives

    2eta <10/(4epsilon^2 N^2)=1/490.

All remaining constants are rational.

## Finite Fourier averages and the tree contradiction

Assume every row period exceeds D. Call a pair nonresonant if no nonzero
integer pair (m,n), |m|,|n|<=D, satisfies m w_i+n w_j=0 modulo M.
The finite Fourier expansion and geometric-sum identity imply

    (1/M)sum_{j=0}^{M-1} g(w_i t_j)g(w_j t_j)=alpha^2

for each such pair. The endpoint shift contributes only a unit phase to a
nonconstant term and does not affect its vanishing. Since f,g lie in [0,1],
their products differ by at most 2eta. The exact bad-set intersection
density is therefore at least

    beta=alpha^2-1/490=4929/490000.

A reduced row of period h has at most ceil((2h-1)/15) bad residues, because
its centered strict phase representatives are one class modulo 15 in the
2h-1 integers from -h+1 to h-1. Hence its density is at most

    rho=2/15+13/[15(D+1)].

If the graph of nonresonant pairs is connected, choose any spanning tree T.
At a point belonging to s>0 of the eight bad sets, its induced subgraph in
T has at most s-1 edges. Consequently, pointwise,

    1_union <=sum_i 1_{B_i}-sum_{ij in T}1_{B_i intersection B_j}.

Averaging gives the exact strict upper bound

    |union|/M <=8rho-7beta
       =628885787/629790000 <1.

Its positive slack is 904213/629790000. Thus the graph is disconnected.
Partition it into nonempty components A,B. Every cross-pair is resonant.
Neither resonance coefficient is zero, since that would force an individual
row period at most D. Since 0<w_i<M, the integer c satisfies
|c|<|m|+|n|<=2D. This proves the first assertion.

The tree inequality is established literature: David Hunter, “An upper bound
for the probability of a union,” Journal of Applied Probability 13(3),
597–603 (1976), [DOI 10.2307/3212481](https://doi.org/10.2307/3212481).
The pointwise proof above makes this use self-contained.

## Elimination gives a finite set of affine templates

Choose w_0 in A and v in B. A row in B directly has a nonzero-coefficient
relation with w_0. For any other row w_i in A, choose the two cross-relations

    r_0 w_0+s_0 v=c_0 M,
    u_i v+v_i w_i=d_i M.

Every displayed speed coefficient is nonzero and at most D in magnitude;
|c_0|,|d_i|<2D. Eliminating v gives

    s_0 v_i w_i=u_i r_0 w_0+(s_0 d_i-u_i c_0)M.

Both the denominator coefficient s_0 v_i and parameter coefficient u_i r_0
are nonzero and bounded by D^2=8,988,004. The remaining coefficient has
magnitude below 4D^2=35,952,016. Direct cross-relations satisfy these same
bounds. This proves the finite-template statement without dividing by a
possibly vanishing difference of coefficients.

`issue-297/check_smooth_relations_2998.py` checks the exact normalization,
second-moment algebra, rational constants, and positive tree gap. These
arithmetic checks do not replace independent review of the analytic proof.
