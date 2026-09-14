# Independent mathematical audit of the eight-row short-relation reduction

Status: `sketch`, requiring Claude or human review. This is a same-family
mathematical audit, not `verified:review`. The audited author proof has
SHA-256 `956273f2530e02a7bc1557d763dc0c50c171d1c9394b96f401dd4e67e67c34f9`
and is `issue-304-eight-row-short-relations.md` on the prover branch.
No author implementation was read or used.

I reconstructed the displayed proof from its elementary definitions and
found no failed step. Its actual conclusion is a disjunction: an eight-row
maximal-endpoint cover has a reduced period at most 65534, or all speed
ratios fit one of finitely many rational affine templates in one free
parameter. Neither alternative bounds that parameter or solves the
fifteen-runner problem. The proof requires no seven-row classification.

The four sanity filters pass: all eight rows act on the same endpoint
family, the forbidden arcs are strict, only common scaling and reduced
row data are used, and the motivating target is fourteen moving velocities
and fifteen total runners at threshold 1/15. The trapezoid minorant is
zero at the forbidden-arc endpoints, preserving equality as success.

## Independently reconstructed analytic steps

The trapezoid has a plateau of half-width `1/15-1/75` and two ramps of
width `1/75`. Integrating these pieces gives mean `3/25`, and its circle
Lipschitz constant is 75. Its convolution with a nonnegative integral-one
kernel stays in `[0,1]`.

Expanding the finite geometric sum defining the Fejer polynomial gives
coefficients `1-|k|/N` for `|k|<N`. Orthogonality therefore gives

    integral F_N^2 = 1 + 2 sum_{k=1}^{N-1}(1-k/N)^2
                   = (2N^2+1)/(3N).

The bounds `F_N<=N` and `F_N<=1/(4Nt^2)` follow, respectively, from the
triangle inequality and the geometric-sum sine quotient. Squaring these
bounds and splitting the first moment at `1/(2N)` gives two contributions
`1/4` and `1/4-1/(4N^2)`. Dividing by the displayed normalization yields
a first moment below `3/(4N)`. Thus convolution changes the trapezoid by
at most `225/(4N)` uniformly. The kernel is a finite polynomial of degree
`2N-2`, so no infinite Fourier-series interchange is required.

For a sampled product of the two smoothed rows, a Fourier term survives
the M-point average only when `M` divides `m*w_i+n*w_j`. The endpoint
shift contributes a constant unit phase and cannot make a vanishing
geometric sum nonzero. Terms with exactly one nonzero coefficient vanish
under the hypothesis that both reduced periods exceed D. Terms with both
coefficients nonzero vanish by nonresonance. The sole remaining term is
the square of the mean, `9/625`.

Writing the product difference as
`(g_i-f_i)g_j+f_i(g_j-f_j)` bounds it by twice the uniform error, since
all factors lie in `[0,1]`. Because the trapezoid product is bounded above
by the intersection indicator, every nonresonant pair has intersection
density at least beta. The direction of this inequality is correct.

The per-row count is bounded by the number of integers in one residue
class modulo 15 inside `(-h,h)`, at most `ceil((2h-1)/15)`. Coprimality is
needed only with h; divisibility of a by 3 or 5 causes no loss. For h>D
this gives the stated rho. Exact arithmetic with `N=32768`, `D=65534`
reproduces

    rho = 131083/983025,
    beta = 449199/40960000,
    8rho-7beta = 1594490420447/1610588160000 < 1.

At a point lying in s nonempty sets, the induced subgraph of any tree has
at most s-1 edges. Therefore the sum of the eight indicators minus the
seven tree-edge intersection indicators is at least the union indicator.
A connected nonresonance graph would supply such a tree and force union
density below one. Hence it is disconnected. Taking one component against
the others gives a nontrivial partition with a resonance on every cross pair.

## Coefficients, affine elimination, and boundary checks

A resonance with one coefficient zero would force a reduced row period
at most D, so both coefficients are nonzero in the large-period case.
Since every speed ratio is strictly between zero and one,
`|c|<|m|+|n|<=2D`. Choosing one row on each side of the partition expresses
all rows on the opposite side directly in terms of the first. For a row
on the same side, eliminating the opposite reference row produces
denominator `s_0*v_i`, slope numerator `u_i*r_0`, and constant numerator
`s_0*d_i-u_i*c_0`. The first two are nonzero products bounded by D squared;
the last has magnitude strictly below four D squared. No difference of
coefficients is used as a divisor, so the feared zero-denominator gap
does not arise.

The sparse-pair example is also correct. With `M=3m+5`, writing `X=15j+1`
and `y=mX mod15M`, simultaneous danger is equivalent to `0<X<2M` and
`0<y<2M`. The congruence `3y=M-5X mod15M` and these strict ranges force
the literal equality `3y=M-5X`. Substitution gives `y=m-25j` and shows
that j is divisible by three. The exact intersections are therefore
`j=3k` with `0<=k<m/75`. This includes the strict endpoint tie when m is
divisible by 75, which excludes the last candidate index.

The independent arithmetic script checks the kernel normalization at
N=2,...,50 and N=32768 and directly enumerates the sparse-pair intersections
for every m=1,...,500, including all neighboring strict-boundary fixtures.
It also checks the resonance `3w_1+5w_2=7M`. These finite regressions support
the audit; the preceding algebra supplies the unbounded reasoning.

Replay `helper_short_relations_algebra.py --proof PATH --output PATH`.
The hash-bound result is `helper-eight-short-relations-audit.json`.
