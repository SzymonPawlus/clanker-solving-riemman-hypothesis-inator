# Issue 165: exact fourth-witness translation elimination

## 2026-09-02

For a polygon base with edge measures \(\ell_e n_e\), allocating each support
direction fractionally among the independently translated witnesses eliminates
translations exactly iff each witness's allocated normal load is zero.  This
gives both a sound support theorem and a kill criterion: one contact cannot
eliminate a planar translation; two contacts must be antipodal.

For the `t=10/13` equal-link arc, the convex hull is an exact isosceles
trapezoid.  Its surface measure splits into a balanced three-normal component
and an antipodal component:

\[
 n_0+n_2+2(69/269)n_3=0,\qquad n_1+n_3=0.
\]

The optimal support allocation therefore has the closed form
\(\max_j C_j+\max_jD_j\).  Together with segment-, square-, and triangle-base
bounds, this removes all six translation coordinates and leaves a finite
three-angle support maximum.  At the reported basin the new bound is about
`0.2349746497` versus hull area `0.2350390775`; exploratory global refinement
found about `0.23464`.  These decimals are diagnostics only.  The next exact
step is an outward interval cover of the three-angle torus.
