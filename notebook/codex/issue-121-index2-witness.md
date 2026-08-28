# Square Peg #121: a zero-area Jordan curve of variation index two

Status: `sketch`.

This note gives an explicit planar Jordan parametrization in the
Wiener--Yang class `C^(0,2-var)` which is nonrectifiable and has infinite
`p`-variation for every `p<2`.  It is a regularity witness only and does not
use frozen PRs #115, #118, or #119.

The construction proves **analytic strictness only**: the critical class
contains zero-image-area, nonrectifiable curves outside every finite
`p`-variation class with `p<2`.  It does not prove that this curve lies
outside Stromquist's or Asano--Ike's locally monotone class.  Its graph and
polygonal-closing geometry may well be locally monotone after a harmless
choice of closing arc; that separate classification is not audited here.
A non-locally-monotone critical witness would require an additional
construction, such as the spiral-strip program, and is not claimed.

## 1. Explicit triangular-wave graph

For `k>=1`, set

```text
I_k=[2^(-k-1),2^(-k)],       ell_k=|I_k|=2^(-k-1),
e_k=2^(-k),                  r_k=exp(-k^2),
N_k=ceil(e_k/(2r_k^2)).                                  (1)
```

Divide `I_k` into `2N_k` equal subintervals, with nodes

```text
x_(k,j)=2^(-k-1)+j ell_k/(2N_k),   0<=j<=2N_k.            (2)
```

Define the continuous piecewise-linear function `f:[0,1]->[0,infinity)` by

```text
f(x_(k,j)) = 0   if j is even,
f(x_(k,j)) = r_k if j is odd,                              (3)
```

affinely on the intervening subintervals, and put `f=0` on `[1/2,1]` and
at `0`.  Adjacent blocks agree at their zero endpoints.  Since `r_k->0`,
`f` is continuous at the only accumulation point `0`.

Let

```text
gamma(t)=(t,f(t)),       0<=t<=1.                          (4)
```

The first coordinate makes `gamma` injective.

## 2. Exact block estimates

On `I_k`, the total variation of the scalar function is

```text
Var_1(f;I_k)=2N_k r_k.                                    (5)
```

For any partition of `I_k`, all scalar increments have magnitude at most
`r_k`, so

```text
sum |Delta f|^2
 <= r_k sum |Delta f|
 <= r_k Var_1(f;I_k)
 = 2N_k r_k^2.                                            (6)
```

The defining extrema partition attains the last expression.  From (1),

```text
e_k <= 2N_k r_k^2 < e_k+2r_k^2 <= 2e_k.                  (7)
```

For the vector graph, Minkowski's inequality for variation seminorms and
the monotonicity of the first coordinate give

```text
||gamma||_(2-var;I_k)
 <= ||id||_(2-var;I_k)+||f||_(2-var;I_k)
 = ell_k+(2N_k r_k^2)^(1/2),
```

and hence

```text
||gamma||_(2-var;I_k)^2 <= 2ell_k^2+4e_k <= C e_k.        (8)
```

For every fixed `p<2`, the extrema partition instead gives

```text
||gamma||_(p-var;I_k)^p
 >= 2N_k r_k^p
 >= e_k r_k^(p-2)
 = 2^(-k) exp((2-p)k^2) -> infinity.                      (9)
```

The length of the graph on the same block is at least

```text
2N_k r_k >= e_k/r_k = 2^(-k)exp(k^2) -> infinity.         (10)
```

Each individual block has finite length; (10) says that these finite block
lengths are unbounded, which already forces the full graph to have infinite
length.

## 3. The global tail estimate

Nonnegativity is the useful feature of this construction.  If `a,b>=0`,

```text
|a-b|^2 <= a^2+b^2.                                       (11)
```

Thus, when a scalar partition increment crosses one or more block
boundaries, inserting the intervening zero endpoints does not decrease its
squared-increment sum.  After inserting all such endpoints, (6)--(7) give

```text
||f||_(2-var;[0,2^(-K)])^2
 <= sum_(k>=K) 2N_k r_k^2
 <= 2 sum_(k>=K)e_k -> 0.                                 (12)
```

The same argument also handles a partition whose first or last point lies
inside a block: only the relevant partial block variation is used, and it is
bounded by the full term in (6).

For the vector graph, Minkowski and monotonicity of `t` yield

```text
||gamma||_(2-var;[0,2^(-K)])
 <= 2^(-K)+||f||_(2-var;[0,2^(-K)]) -> 0.                 (13)
```

## 4. Yang fine-mesh vanishing

We verify the fixed-base fine-mesh definition directly.  For a partition
`D={0=t_0<...<t_m=1}`, let

```text
mesh(D)=max_i(t_(i+1)-t_i),
w_2(f,delta)^2
 = sup_(mesh(D)<=delta) sum_i |f(t_(i+1))-f(t_i)|^2.       (14)
```

Given `epsilon>0`, choose `K` so that the tail in (12) is less than
`epsilon^2/4`.  Insert the zero endpoint `2^(-K)` into any fine partition;
by (11) this does not decrease the scalar squared sum across that endpoint.
On `[2^(-K),1]`, the function is a finite piecewise-linear path.  If its
Lipschitz constant and total variation are `L_K,V_K`, respectively, then a
partition of mesh at most `delta` contributes at most

```text
(max |Delta f|) sum |Delta f| <= L_K delta V_K.            (15)
```

Choose `delta` so this is below `epsilon^2/4`.  Equations (12) and (15)
prove

```text
w_2(f,delta) -> 0.                                        (16)
```

For the graph, every partition of mesh at most `delta` satisfies

```text
sum |Delta gamma|^2
 = sum (Delta t)^2+sum (Delta f)^2
 <= delta sum Delta t+w_2(f,delta)^2
 = delta+w_2(f,delta)^2.                                  (17)
```

Therefore `gamma` has vanishing 2-variation in the exact Wiener--Yang mesh
sense.  In particular it has finite 2-variation.  Equivalently, one may
truncate the waves with `k>=K`; the resulting finite polygonal paths have
bounded variation and converge to `gamma` in 2-variation by (12)--(13).

## 5. Closing the graph to a Jordan curve

Let `A=(0,0)` and `B=(1,0)`.  Close the graph from `B` back to `A` by the
three-segment polygonal arc

```text
B -> (1,-1) -> (0,-1) -> A.                               (18)
```

For an explicit period-one parametrization `c:[0,1]->R^2`, set

```text
c(s)=gamma(2s),                         0<=s<=1/2,
c(s)=(1,-6(s-1/2)),                     1/2<=s<=2/3,
c(s)=(1-6(s-2/3),-1),                   2/3<=s<=5/6,
c(s)=(0,-1+6(s-5/6)),                   5/6<=s<=1.         (19)
```

The formulas agree at their endpoints and `c(0)=c(1)=A`.  On `[0,1)`, the
map is injective: the graph is injective, lies in `y>=0`, and meets the
closing arc in `y<=0` only at `A,B`; the vertical closing segments have
`x=0` or `x=1`, which the graph meets only at the corresponding endpoint.
Thus (19), periodically extended, is a Jordan parametrization.

Vanishing 2-variation is invariant under the increasing linear
reparametrization of the graph half.  The closing half is a finite
piecewise-linear path, hence has vanishing 2-variation.  Splitting a
fine-mesh partition at the four fixed seams in (19), with the elementary
`|u+v|^2<=2(|u|^2+|v|^2)` cost at each inserted seam, combines (17) with
the finite Lipschitz estimates to show directly that

```text
c in C^(0,2-var).                                         (20)
```

## 6. Remaining properties

For every `p<2`, a block-extrema partition from (9), transported into the
first half of (19) and extended to the full period, proves

```text
||c||_(p-var)=infinity.                                   (21)
```

Equation (10) proves that `c` is nonrectifiable.

Finally, the graph of the continuous function `f` has planar Lebesgue
measure zero: it is closed and every vertical section is a singleton, so
Fubini's theorem applies.  The three closing segments also have planar
measure zero.  Hence

```text
Lebesgue_measure_2(c(S^1))=0.                              (22)
```

Equations (20)--(22) give a zero-area, nonrectifiable Jordan embedding of
variation index exactly two.

## 7. Scope

This is an elementary construction, but it remains `sketch` pending an
independent check of the global block-boundary refinement in (12), the exact
Yang quantifiers in (14)--(17), and the four-seam periodic assembly in (19).
It establishes no Square Peg existence claim by itself and no separation
from the known locally monotone class.
