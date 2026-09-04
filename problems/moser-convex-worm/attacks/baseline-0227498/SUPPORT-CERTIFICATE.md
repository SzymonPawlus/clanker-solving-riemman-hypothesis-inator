# Finite support certificate lemma

**Status:** sketch. This is a proposed pruning predicate for later witness
searches. It is not a certified lower bound until independently reviewed and
instantiated with outward interval arithmetic.

## Polygon support lemma

Let \(P=\operatorname{conv}(p_0,\ldots,p_{m-1})\) be a convex polygon listed
counterclockwise, and let a compact convex set \(K\) contain \(P\). For the
edge

\[
 e_i=p_{i+1}-p_i
\]

(indices modulo \(m\)), put \(\ell_i=|e_i|\) and let \(n_i\) be its outward
unit normal. Write

\[
 h_K(n)=\max_{x\in K} n\mathbin\cdot x.
\]

Then

\[
 \operatorname{area}(K)
 \geq \frac12\sum_{i=0}^{m-1}\ell_i h_K(n_i). \tag{S}
\]

Although the support values depend on the origin, their weighted sum does not:
translation by \(z\) adds
\(z\cdot\sum_i\ell_i n_i=0\), since the rotated edge vectors close.

## Proof

Translate both sets arbitrarily. Since \(P\subseteq K\), convexity gives

\[
 K+tP\subseteq K+tK=(1+t)K. \tag{5}
\]

The polygonal Minkowski first-variation identity is

\[
 \operatorname{area}(K+tP)
 =\operatorname{area}(K)
 +t\sum_i\ell_i h_K(n_i)
 +t^2\operatorname{area}(P). \tag{6}
\]

For a polygonal \(K\), (6) follows by attaching, along every edge of \(tP\),
a strip whose length is the corresponding support displacement; the corner
pieces together form a translate and scale of \(tP\). General compact convex
\(K\) follows by Hausdorff approximation with polygons. A checker may instead
take (6) as the standard planar mixed-area identity and verify only its finite
polygon specialization.

By (5), the left side of (6) is at most
\((1+t)^2\operatorname{area}(K)\). Compare the linear coefficients at
\(t=0\) to obtain (S).

The rectangle-width lemma is the centrally symmetric four-edge specialization
of (S).

## Finite certificate predicate

Suppose \(K\) is the convex hull of finitely many placed witness vertices
\(v_0,\ldots,v_{N-1}\). On an interval-search leaf, a certificate records for
each polygon edge \(i\):

1. an exposed-vertex index \(j(i)\);
2. an outward-rounded lower rational \(H_i\);
3. an interval proof that
   \(n_i\cdot v_{j(i)}\geq H_i\) throughout the leaf.

Then

\[
 h_K(n_i)=\max_j n_i\cdot v_j
 \geq n_i\cdot v_{j(i)}\geq H_i,
\]

and the leaf is safely pruned whenever

\[
 \frac12\sum_i\ell_i H_i\geq c. \tag{7}
\]

No hull ordering or claim that \(v_{j(i)}\) is the true maximizer is needed.
Selecting any vertex gives a sound lower bound.

For a centrally symmetric base polygon, pair opposite edges. If their common
length is \(\ell_i\), then

\[
 \ell_i\bigl(h_K(n_i)+h_K(-n_i)\bigr)
 =\ell_i w_K(n_i).
\]

Thus the certificate can record two vertex indices realizing a lower bound on
the width. This is the form used by the square in the baseline proof.

## Exact schema for an independent checker

A future certificate using (7) must expose:

- exact algebraic or rational vertices of the base polygon \(P\), in
  counterclockwise order;
- exact edge lengths and normals, or defining polynomial relations and
  isolating intervals for them;
- the normalized placement-variable box for the leaf;
- for each edge, `vertex_index` and the rational `support_lower`;
- outward interval enclosures for every sine, cosine, product, and dot product;
- the exact rational target \(c\);
- a branch tree whose leaves cover the complete compact placement domain.

An independent checker need only reconstruct the placed vertices, verify the
box cover, recompute every selected dot-product lower bound, and check (7).
The producer's hull code and optimizer are not dependencies.

## Limits

- The base polygon must itself be contained in every \(K\) on the leaf. In a
  witness problem, choose the convex hull of one placed witness as \(P\).
- For a nonsymmetric \(P\), one-sided supports must use a common explicitly
  normalized origin. Widths alone do not determine the sum in (S).
- The predicate may be weak: a failed support bound says nothing about the
  actual area. A checker must retain another sound predicate or subdivide.
- Formula (S) is a lower bound, not generally an exact hull-area formula.
