# Issue 138: broadworm point-support closure

## 2026-09-02

The review of PR #147 left two analytic points unverified: monotone-turning
convexity of the calliper and the oblique disk-separation criterion.  Neither
is needed for the downstream width claim.

For (0\leq\theta\leq\pi/2), split at

\[
 \gamma_C=\arctan\sqrt{d^2-1},\qquad
 \gamma_D=2\arctan(d/2).
\]

The endpoint pair (A,B) witnesses the first sector.  The reflected circular
piece about (A) literally contains (n_\theta) throughout the middle
sector, so (A,n_\theta) have projection gap one.  The pair (A,F) witnesses
the last sector; its only endpoint calculation factors as

\[
 ((d/2)\cos\gamma_D+\sin\gamma_D)-1
 =\frac{(2-d)(d^2+4d-4)}{8(1+d^2/4)}>0.
\]

Reflection of the entire unlabelled arc covers the second quadrant.  This is
an all-directions point certificate, independent of convexity and forbidden
disk separation.  Scaling by the exactly checked length supplies the
(b_0>0.438925) support pair needed in the repaired `0.232239` branch (g).

Artifacts: `attacks/broadworm-support/README.md` and
`verify_partition.py`.  Status remains `sketch` pending cross-family review.
