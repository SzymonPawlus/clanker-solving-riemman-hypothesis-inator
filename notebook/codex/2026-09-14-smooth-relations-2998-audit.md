# Independent analytic audit of the 2,998 relation window

Status: `sketch`; same-family mathematical audit, requiring Claude or human
review. The manager's proof is
`2026-09-14-lonely-runner-smooth-relations-2998.md`. No author checker or
generator was read or used.

The analytic improvement passes my independent reconstruction. The bound
is D=2998, with affine slope and denominator coefficients at most 8,988,004
in absolute value and constant coefficient below 35,952,016. These are
finite coefficient bounds with one unbounded rational parameter; no bound
for the maximal speed follows. The result remains an eight-row endpoint
cover reduction in the fourteen-moving/fifteen-total runner target at
threshold 1/15, with one common endpoint family and only common scaling.
The cosine minorant vanishes at the strict forbidden-arc endpoints.

## The Taylor estimate is valid across every join

On either ramp the derivative is a signed sine of amplitude
`pi/(2 epsilon)`. At each end of a ramp it is zero, agreeing with the
derivative on the constant plateau or zero interval. Near the origin the
function is constant, and near the circle's opposite join it is zero.
Thus the real periodic lift has a continuous first derivative everywhere.
Its derivative has Lipschitz constant `L=pi^2/(2 epsilon^2)` on each smooth
piece. Subdividing any real interval at its finitely many joins and adding
the bounds proves the same Lipschitz constant globally.

Integrating the difference of first derivatives along the interval from
x to x-y therefore gives

    |f(x-y)-f(x)+y f'(x)| <= integral_0^|y| Ls ds = L y^2/2.

This argument requires no second derivative at a join. The concern that
the raised cosine is not globally C2 is consequently harmless here.

## Second moment and uniform convolution error

The squared-Fejer normalization is independently the sum of squares of
its finite triangular Fourier coefficients, `(2N^2+1)/(3N)`. Using
`F_N<=N` below `1/(2N)` and `F_N<=1/(4Nt^2)` above that point gives raw
second moment

    1/(12N) + 1/(4N) - 1/(4N^2)
      = 1/(3N) - 1/(4N^2).

Dividing by the normalization bounds the normalized second moment by
`1/(2N^2)`. The kernel is even, so the integral of its linear Taylor term
is exactly zero. The remainder bound above therefore yields convolution
error at most `L/(4N^2)`, exactly the factor used by the manager. The
finite Fourier degree remains `2N-2`.

The ramp integral is epsilon/2 on each side. Hence the mean of the
minorant is `2/15-epsilon`, equal to `11/100` for epsilon=7/300. With
N=1500, twice the uniform error is strictly below 1/490 using pi squared
below ten. A self-contained bound for that last elementary constant is

    integral_0^1 x^4(1-x)^4/(1+x^2) dx = 22/7-pi > 0.

Polynomial division verifies the identity, and `(22/7)^2=484/49<10`.
This also avoids treating a rounded value of pi as an exact input.

## Fourier averaging, tree inequality, and coefficients

Under row periods greater than D, every one-coordinate nonconstant
Fourier term vanishes on the M-point endpoint grid. For a nonresonant
pair every two-coordinate nonconstant term also vanishes, leaving the
square of the mean. The endpoint offset changes only a constant unit
phase, not the vanishing geometric sum. Product replacement costs at
most twice the uniform error, so the lower bound on the exact forbidden
intersection is beta, with the correct inequality direction.

The independently calculated constants are

    beta = 4929/490000,
    rho = 2/15 + 13/(15*2999),
    8rho-7beta = 628885787/629790000 < 1,
    gap = 904213/629790000.

The pointwise tree inequality follows by counting at most s-1 tree edges
among s active vertices, so a connected nonresonance graph contradicts
full coverage. Every cross-pair in a partition of its components is
resonant. The large individual periods exclude zero coefficients. The
same product-based affine elimination as in the earlier audit uses two
nonzero products as its slope and denominator coefficients, never a
possibly vanishing difference. Squaring D and multiplying by four gives
the claimed exact bounds.

The bibliography is also consistent: Cambridge's publisher record gives
David Hunter, Journal of Applied Probability 13(3), September 1976,
pages 597–603, DOI 10.2307/3212481, and describes graph-theoretic union
bounds selected by spanning trees. This audit uses the displayed
pointwise proof; the paywalled article was not used as a proof dependency.
[Publisher record](https://www.cambridge.org/core/journals/journal-of-applied-probability/article/abs/an-upper-bound-for-the-probability-of-a-union/092D711504BA968EF0D1D903A2685D60)

The independent exact-arithmetic script is `helper_smooth_relations_algebra.py`;
its hash-bound report is `helper-smooth-relations-2998-audit.json`. It checks
the normalization and moment algebra at N=2,...,100 and N=1500, all stated
rational constants, and the polynomial identity for the pi bound. These
checks support the preceding analytic reconstruction and do not replace it.
