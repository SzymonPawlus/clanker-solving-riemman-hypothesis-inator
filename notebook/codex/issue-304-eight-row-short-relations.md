# Eight-row covers force bounded integer relations or a small period

Status: `sketch`; a new self-contained analytic reduction for independent
review. It does not prove minimum period at most three, does not classify
eight-row covers, and does not assume the earlier seven-row results.

## Statement and endpoint convention

Suppose eight positive integer speeds `w_i<M` cover every lower endpoint
`t_j=(j+1/15)/M`, `0<=j<M`, of the maximal anchor `M`. A row is bad exactly
when `||w_i*t_j||<1/15`; equality is success. This concerns one common time
in the fourteen-moving/fifteen-total-runner attack. Signs and repeated
absolute values cause no issue; only common scaling is used.

Put `D=65534`. Then either:

1. some row has reduced period `M/gcd(M,w_i)<=D`; or
2. the eight rows admit a nontrivial partition `A,B` such that every
   cross-pair `i in A,j in B` has integers `m,n,c` with

   ```text
   0<|m|,|n|<=D, |c|<2D,
   m*w_i+n*w_j=c*M.
   ```

In case 2 all eight speed ratios belong to a finite collection of rational
affine templates in one free parameter. More explicitly, one can choose
`x=w_0/M` so every other speed satisfies

```text
w_i/M = (P_i/Q_i)*x + R_i/Q_i,
0<|P_i|,|Q_i|<=D^2, |R_i|<4D^2.
```

The parameter `x` remains an arbitrary rational in `(0,1)` obeying all
speed-range constraints. Thus this is a finite relational reduction, not
a finite bound for `M`. Small periods need their own further analysis.

## Nonnegative smoothing with an explicit finite Fourier degree

Set `delta=1/15`, `epsilon=1/75`. On the circle define the trapezoid `f` to
equal one when `||t||<=delta-epsilon`, decrease linearly to zero at
`||t||=delta`, and vanish outside. It satisfies

```text
0<=f<=1_{||t||<1/15}, integral f = 2delta-epsilon = 3/25,
|f(x)-f(y)| <= 75 ||x-y||.
```

In particular, the minorant is zero at both forbidden-arc endpoints; no
closed-arc replacement is hidden in the argument.

For an integer `N>=2`, define the Fejer polynomial directly by

```text
F_N(t)=(1/N)|sum_{k=0}^{N-1} exp(2pi*i*k*t)|^2
      =sum_{|k|<N}(1-|k|/N) exp(2pi*i*k*t).
```

Squaring and taking its constant coefficient gives the exact identity

```text
A_N=integral F_N^2 = (2N^2+1)/(3N) >=2N/3.
```

Let `K_N=F_N^2/A_N`. This polynomial is nonnegative, has integral one, and
has degree `2N-2`. For `0<|t|<=1/2`, the elementary geometric-sum formula
and `sin(pi|t|)>=2|t|` give

```text
F_N(t) <= min(N,1/(4N t^2)).
```

The sine inequality follows from concavity of sine between zero and
`pi/2`. Splitting the moment integral at `1/(2N)` gives

```text
integral ||t|| F_N(t)^2 dt
 <=2 integral_0^(1/(2N)) t N^2 dt
   +2 integral_(1/(2N))^(1/2) [1/(16N^2 t^3)] dt
 =1/2-1/(4N^2) <1/2.
```

Consequently `integral ||t|| K_N(t) dt <=3/(4N)`. The convolution
`g=f*K_N` is a real trigonometric polynomial of degree at most `2N-2`,
has mean `3/25`, lies in `[0,1]`, and satisfies the uniform error bound

```text
||g-f||_infinity <=225/(4N)=eta.
```

All facts about the kernel used here follow from the displayed finite sum,
orthogonality of integer exponentials, and the elementary integral bound.

## Exact endpoint averages and a spanning-tree bound

Take `N=32768`, so the polynomial degree is `D=65534`. Assume all reduced
row periods exceed `D`. Call a pair nonresonant when there is no nonzero
integer pair `(m,n)` with `|m|,|n|<=D` and
`m*w_i+n*w_j` divisible by `M`.

For a nonresonant pair, expand `g(w_i*t_j)g(w_j*t_j)` into its finite
Fourier sum and average over `j=0,...,M-1`. Every nonconstant term vanishes
by the geometric-sum identity. The shift `1/(15M)` only contributes a
unit phase to such a term and does not affect its vanishing. Thus

```text
(1/M)sum_j g(w_i*t_j)g(w_j*t_j) = (3/25)^2.
```

Since `f,g` both lie in `[0,1]`, replacing their product changes it by at
most `2eta`. The exact intersection density of the two bad row sets is
therefore at least

```text
beta=9/625-225/(2N)=449199/40960000.
```

A reduced row of period `h` contains at most `ceil((2h-1)/15)` residues:
write its centered residues as `a+15k` in the strict integer interval
`-h<a+15k<h`. Therefore every row here has density at most

```text
rho=2/15+13/[15(D+1)]=131083/983025.
```

If the graph of nonresonant pairs were connected, choose a spanning tree
with seven edges. For arbitrary finite sets `B_1,...,B_8` and a tree `T`,

```text
1_(union B_i) <= sum_i 1_(B_i) - sum_{ij in T} 1_(B_i intersection B_j).
```

Indeed, at a point belonging to `s>0` sets, the induced subgraph of a tree
has at most `s-1` edges. Averaging this inequality gives

```text
|union B_i|/M <=8rho-7beta
 =1594490420447/1610588160000 <1.
```

The positive gap is `16097739553/1610588160000`. This contradicts full
endpoint coverage. Hence the nonresonant graph is disconnected, and all
cross-pairs of a partition into its components are resonant.

In such a resonance, neither coefficient can be zero: otherwise a reduced
row period would be at most `D`. The speed range gives
`|c|<|m|+|n|<=2D`. This proves the partition assertion.

## Finite affine templates without dividing by a possibly zero coefficient

Choose `w_0` on one side and `v` on the other. Every row `w_i` opposite
`w_0` directly satisfies `r_i*w_0+s_i*w_i=c_i*M`, with both coefficients
nonzero and bounded by `D`. This gives the required template immediately.

For a row `w_i` on the same side as `w_0`, use

```text
r_0*w_0+s_0*v=c_0*M,
u_i*v+v_i*w_i=d_i*M.
```

Both `s_0` and `v_i` are nonzero. Eliminating `v` gives

```text
s_0*v_i*w_i = u_i*r_0*w_0 + (s_0*d_i-u_i*c_0)*M.
```

The denominator coefficient and the coefficient of `w_0` are nonzero,
bounded by `D^2`; the remaining integer coefficient has magnitude less
than `4D^2`. There is no division by a cancellation-prone difference of
coefficients and no extra rank hypothesis. The collection of integer
triples with these bounds is finite, while their shared parameter is
unbounded. Further work must analyze those templates or improve this very
large bound; no minimum-period-three theorem follows here.

## Why a uniform pair-overlap shortcut fails

For any positive integer `m`, take

```text
M=3m+5, w_1=2m+5=M-m, w_2=3m+4=M-1.
```

The exact common bad indices are `j=3k` with `0<=k<m/75`, so their number
is `ceil(m/75)`. To check this, write `X=15j+1`. A speed `M-b` kills the
endpoint precisely when `0<bX mod15M<2M`. The row with `b=1` forces
`X<2M`. If `y=mX mod15M` is also in `(0,2M)`, then
`3y=M-5X mod15M`; the stated ranges force `3y=M-5X`, hence `X<M/5`.
The congruence for `y` then forces `j` divisible by three. These conditions
are also sufficient. For `m=75t+1` both row periods equal `M=225t+8`,
while their intersection density is `(t+1)/(225t+8)`, tending to `1/225`.
Thus even arbitrarily large individual periods permit sparse pair
intersections. The resonance here is `3w_1+5w_2=7M`, exactly the kind the
nonresonant argument deliberately separates.
