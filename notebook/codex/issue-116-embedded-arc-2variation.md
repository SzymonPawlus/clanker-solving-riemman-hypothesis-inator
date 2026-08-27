# Embedded-arc winding mass at critical 2-variation

**Status:** `sketch`

This note proves a compactness criterion for the action primitives of smooth
Jordan approximations.  It is not an assumable claim.  In particular, it does
not depend on either PR #115 or PR #118.

## Statement

For a continuous path $c:[a,b]\to\mathbb R^2$, use the convention

\[
 \|c\|_{2\text{-var};[a,b]}^2
 :=\sup_{a=t_0<\cdots<t_m=b}
       \sum_{i=0}^{m-1}|c(t_{i+1})-c(t_i)|^2.
\]

Let $c$ be an injective rectifiable arc, and let $L$ be the closed
rectifiable loop obtained by following $c$ and then the straight chord from
$c(b)$ to $c(a)$.  Then

\[
 \int_{\mathbb R^2}|\operatorname{Ind}(L,z)|\,dz
 \leq {\pi\over4}\|c\|_{2\text{-var};[a,b]}^2. \tag{1}
\]

The injectivity is essential to the proof.  There is no analogous universal
bound for arbitrary smooth closed loops: critical Fourier examples can tend
to zero in 2-variation while their signed areas diverge [Yang, Example 41].

## Excursion decomposition

Write $C=[c(a),c(b)]$ for the endpoint chord and

\[
 U=\{u\in(a,b):c(u)\notin C\}.
\]

The open set $U$ is a countable disjoint union of intervals
$(a_j,b_j)$.  The endpoints of every component map to $C$.  They have
distinct images because $c$ is injective.  The interior of the excursion
$c|_{[a_j,b_j]}$ is disjoint from all of $C$, so it meets the chord segment
$[c(b_j),c(a_j)]$ only at its endpoints.  Consequently

\[
 E_j=c|_{[a_j,b_j]}+[c(b_j),c(a_j)]
\]

is an oriented Jordan loop.  This argument does not require transverse chord
hits.  It also permits intervals and Cantor subsets of the parameter set on
which $c$ lies in $C$.  An excursion need not stay in one half-plane of
the line supporting $C$; it may cross that line outside the finite segment.

Regard rectifiable curves as integral 1-currents.  The excursion currents are
absolutely summable, since

\[
 \mathbf M(E_j)
 \leq \operatorname{len}(c|_{[a_j,b_j]})+|c(b_j)-c(a_j)|
 \leq 2\operatorname{len}(c|_{[a_j,b_j]}),
\]

and the excursion intervals are disjoint.  Thus \(\sum_jE_j\) converges in
mass.  The residual

\[
 R=L-\sum_jE_j
\]

is a compactly supported 1-cycle carried by the line containing $C$.
Every such cycle is zero: integration of a 1-form along that line depends
only on a one-dimensional primitive, and the boundary vanishes.  Hence

\[
 L=\sum_j E_j. \tag{2}
\]

This is where every chord-contained portion of $c$, including a
non-interval contact set, is accounted for.

Let \(\Omega_j\) be the bounded Jordan domain of $E_j$, and let
\(\varepsilon_j\in\{-1,1\}\) be its orientation.  The chord is contained in
the convex hull of its endpoints, so

\[
 \operatorname{diam}(E_j)
 =\operatorname{diam}(c([a_j,b_j])).
\]

For any finite collection of excursions, choose two ordered points in each
interval whose image distance is arbitrarily close to that excursion's
diameter.  Combining all of those points into one partition of $[a,b]$
shows, and monotone passage to the countable family gives,

\[
 \sum_j\operatorname{diam}(E_j)^2
 \leq\|c\|_{2\text{-var};[a,b]}^2. \tag{3}
\]

The isodiametric inequality and (3) imply

\[
 \sum_j|\Omega_j|
 \leq {\pi\over4}\sum_j\operatorname{diam}(E_j)^2
 \leq {\pi\over4}\|c\|_{2\text{-var};[a,b]}^2. \tag{4}
\]

Therefore the oriented fillings
\(\sum_j\varepsilon_j[\Omega_j]\) converge in mass.  By (2), their boundary
is $L$.  A compactly supported planar integral 2-current with boundary
$L$ is unique: the difference of two such fillings is a compactly supported
2-cycle in \(\mathbb R^2\), hence is zero by the constancy theorem.  The
usual index filling of $L$ is consequently

\[
 \operatorname{Ind}(L,\cdot)
 =\sum_j\varepsilon_j\mathbf1_{\Omega_j}\quad\text{a.e.}
\]

Taking absolute values, using the triangle inequality, and then (4) proves
(1).  Nested or overlapping lobe interiors cause no problem: the current
identity is signed, while the estimate uses
\(|\sum_j\varepsilon_j\mathbf1_{\Omega_j}|
 \leq\sum_j\mathbf1_{\Omega_j}\).

## Uniform local criterion for action primitives

Let $c_n:\mathbb R/\mathbb Z\to\mathbb R^2$ be smooth parametrized Jordan
curves.  Suppose their images lie in a fixed ball $B(0,R)$, they have a
common parameter modulus

\[
 |c_n(t)-c_n(s)|\leq\omega(\delta)
 \quad (|t-s|\leq\delta),
\]

and their local 2-variations have the uniform modulus

\[
 \nu(\delta):=
 \sup_n\sup_{|t-s|\leq\delta}
 \|c_n\|_{2\text{-var};[s,t]}\longrightarrow0. \tag{5}
\]

Intervals are understood on a lifted period, with length at most $1/2$.
For the chord-closed subarc $L_{n;s,t}$, (1) gives the explicit absolute
winding-mass estimate

\[
 \eta(\delta):=
 \sup_n\sup_{|t-s|\leq\delta}
 \int|\operatorname{Ind}(L_{n;s,t},z)|\,dz
 \leq {\pi\over4}\nu(\delta)^2. \tag{6}
\]

Set \(\lambda_0=(x\,dy-y\,dx)/2\) and anchor the smooth action primitives by

\[
 F_n(t)=\int_0^t c_n^*\lambda_0.
\]

Generalized Green's formula for a closed rectifiable planar loop says

\[
 \int_{L_{n;s,t}}\lambda_0
 =\int_{\mathbb R^2}\operatorname{Ind}(L_{n;s,t},z)\,dz.
\]

The straight chord from $c_n(t)$ to $c_n(s)$ has action
\(\det(c_n(t),c_n(s))/2\), of absolute value at most
\(R\omega(\delta)/2\).  Equations (6) and Green's formula therefore give

\[
 |F_n(t)-F_n(s)|
 \leq {\pi\over4}\nu(\delta)^2
       +{R\over2}\omega(\delta). \tag{7}
\]

Independently of the possibly nonminimal supplied modulus \(\omega\), the
actual endpoint distance is at most \(\nu(\delta)\) by the two-point
partition.  The right side may therefore be replaced directly by
\(\pi\nu(\delta)^2/4+R\nu(\delta)/2\).

Formula (7) is a common modulus of continuity.  Covering $[0,1]$ by a fixed
finite number of sufficiently short intervals and using $F_n(0)=0$ also gives
a common uniform bound there.  Arzelà--Ascoli supplies a subsequence converging
uniformly on $[0,1]$ to a continuous function $F$.  In particular the period
actions $A_n:=F_n(1)$ converge to $A:=F(1)$.  The primitives themselves live
on the lifted real parameter and need not be periodic; their identity

\[
 F_n(k+r)=kA_n+F_n(r)\qquad(k\in\mathbb Z,\ 0\leq r<1)
\]

then promotes convergence on $[0,1]$ to local-uniform convergence on
\(\mathbb R\), with the analogous identity for the limit.  Thus (5), rather
than a pointwise bound on chord-closure indices, is sufficient for the
primitive compactness step.

This conclusion is only a compactness statement.  It does not assert that
arbitrary uniformly convergent smooth Jordan approximations satisfy (5), nor
does it by itself prove the square-peg conjecture.

## References

- J. Cufí and J. Verdera, *A general form of Green Formula and Cauchy
  Integral Theorem*, Proc. Amer. Math. Soc. **143** (2015), 1661--1669,
  arXiv:1306.6832 (generalized Green formula).
- D. Yang, *Notes on area operator, geometric 2-rough paths and Young
  integral when \(p^{-1}+q^{-1}=1\)*, arXiv:1204.0112v1, especially
  Examples 41--42 (failure of an unrestricted critical 2-variation area
  bound).
