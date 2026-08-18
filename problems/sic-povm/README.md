# Symmetric informationally complete POVMs: authoritative baseline

Last source pass: **2026-08-18**. Scope: finite positive dimensions (d).

Every literature statement below is marked `cited` and has a primary-source locator. It becomes
assumable in this repository only after the required cross-family review. Numerical evidence is
marked `numerical` and is never a proof of existence. No unmerged repository work is a dependency.

## Exact unrestricted problem

`cited` — Given \(d\geq 1\), do there exist \(d^2\) unit vectors
\(\phi_1,\ldots,\phi_{d^2}\in\mathbb C^d\) such that

\[
  |\langle\phi_i,\phi_j\rangle|^2=\frac1{d+1}\qquad(i\ne j)?
\]

This is the unrestricted SIC existence problem. Renes–Blume-Kohout–Scott–Caves state it as
Equation (1) and show in Section II that the other POVM properties follow. Kopp–Lagarias still
state universal Weyl–Heisenberg existence as **Conjecture 2.4** in 2026, so in particular the
unrestricted universal problem is not solved.

Distinct indices really give distinct complex lines: overlap one would be required for equal
lines, whereas \(1/(d+1)<1\) for \(d\geq1\). For \(d=1\) the pairwise condition is vacuous and the
single rank-one projector is the unique one-outcome POVM.

## Vector, tight-frame, and POVM normalizations

`cited` — Put \(\Pi_i=|\phi_i\rangle\langle\phi_i|\). From the vector equations,

\[
 \operatorname{Tr}(\Pi_i\Pi_j)=
 \begin{cases}1&i=j,\\1/(d+1)&i\ne j.\end{cases}
\]

The frame operator is \(S=\sum_i\Pi_i\). Its frame potential is

\[
 \operatorname{Tr}(S^2)
 =d^2+\frac{d^2(d^2-1)}{d+1}=d^3.
\]

For \(n=d^2\) unit vectors, the Benedetto–Fickus bound is
\(\operatorname{Tr}(S^2)\ge n^2/d=d^3\), with equality exactly for a tight frame. Hence
\(S=dI\), and

\[
 E_i=\frac1d\Pi_i,qquad \sum_iE_i=I
\]

is a rank-one POVM. Its projectors are linearly independent: their Hilbert–Schmidt Gram matrix
has diagonal \(1\), off-diagonal \(1/(d+1)\), eigenvalue \(d\) on the all-ones vector, and
\(d/(d+1)>0\) with multiplicity \(d^2-1\). Thus the POVM is informationally complete.

Conversely, a SIC-POVM in the normalization of Kopp's **Definition 2.3** consists precisely of
the effects \(E_i=\Pi_i/d\) with that projector Gram matrix; choosing a unit vector spanning each
rank-one projector recovers the vector equations. The vector-family existence statement and the
rank-one SIC-POVM existence statement are therefore equivalent, not merely related.

Primary locators: Renes et al., Equation (1), pp. 1–2; Theorem 1 and Equations (4)–(7), p. 2;
the Gram-matrix argument, pp. 2–3. Kopp, Definition 2.3 and Equation (2.2), Section 2.1.

## Three different scopes that must not be conflated

1. **Unrestricted SIC.** Any \(d^2\) lines satisfying the equations above.
2. **Weyl–Heisenberg (WH) covariant SIC.** The \(d^2\) lines are the orbit of one fiducial vector
   under the displacement operators \(D_{m,n}\). This is Kopp's Definitions 2.7–2.9 and
   Kopp–Lagarias Definitions 2.2–2.3. It is a restriction: a WH construction proves unrestricted
   existence in that dimension, but unrestricted existence does not supply a WH fiducial.
3. **Zauner-symmetric WH search.** A WH fiducial is additionally required to lie in an eigenspace
   of a canonical order-three Clifford unitary. This is a still stronger search ansatz. Scott's
   2017 data give one solution with Zauner symmetry for every \(d\le121\); that numerical success
   is not a theorem that every SIC, or even every WH SIC, has Zauner symmetry.

Terminology is inconsistent across papers. Kopp–Lagarias call the WH-existence statement itself
the **Strong Zauner Conjecture** (Conjecture 2.4). Here “Zauner-symmetric” always means the extra
order-three Clifford eigenspace condition, so that it cannot be silently substituted for either
WH or unrestricted existence. The Hoggar lines in \(d=8\) are the standard warning: Kopp,
Section 2.2, records them as the one known SIC not unitarily equivalent to a WH SIC.

## Dated construction frontier

This is a conservative evidence frontier, not a claim that every known orbit is catalogued.

| Dimensions / range | Symmetry and evidence | Status | Primary locator |
|---|---|---|---|
| \(d=1\) | trivial exact projector | `cited` | direct \(1\times1\) case; Kopp–Lagarias Conj. 2.4 discussion includes \(d=1\) |
| \(d=2,3,4\) | explicit analytic SICs; Renes et al. construct them | `cited` | Renes et al., Sections IV.A–IV.C; abstract and p. 2 roadmap |
| \(d=8\) | exact Hoggar lines, not WH-equivalent | `cited` | Renes et al., p. 2 (known analytic solution); Kopp, Section 2.2 |
| every \(1\le d\le53\) | rigorous explicit constructions exist; overwhelmingly WH, but this row asserts unrestricted existence only | `cited` | Kopp–Lagarias, p. 3 and the paragraph after Conjecture 2.4 (p. 7 in the PDF) |
| \(d=67,103,199,487\) | Stark-unit/algebraic constructions with complete exact checks in the 2022 computation table; WH fiducials | `cited` | Appleby–Bengtsson–Grassl–Harrison–McConnell, Tables II–III, pp. 40 and 46; the paper notes \(487\) is the only previously unknown case fully verified exactly there |
| \(d=124,323\) | published explicit exact constructions predating 2021 | `cited` | Kopp, Introduction p. 1, published-existence list and references there |
| \(d=787,1447,2503,2707,4099,5779,19603\) | algebraic Stark-unit candidates, partial exact arithmetic, but the full SIC equations were checked only numerically at the stated precision | `numerical` | Appleby et al. 2022, Tables II–III and the qualification immediately after Table III, pp. 40, 46–47 |
| every \(d\le67\) | WH numerical solutions (the \(d=66\) search was inconclusive in the paper's original run, so do not use that paper alone for 66) | `numerical` | Scott–Grassl, abstract; Section VI and Appendix A |
| every \(d\le121\) | one numerical WH solution with Zauner symmetry per dimension | `numerical` | A. J. Scott, *SICs: Extending the list of solutions*, abstract/data files |
| every \(d\le151\), plus selected dimensions through \(844\) | numerical solutions; \(122\)–\(151\) computed by the authors using Scott's code | `numerical` | Fuchs–Hoang–Stacey, abstract and Section I, especially the paragraph reporting the new calculations |

Two exclusions are deliberate:

- Kopp (2021, Introduction) labels the exact \(d=53\), all dimensions through \(165\), and isolated
  \(1155,2208\) extensions as **unpublished**. The 2026 Kopp–Lagarias statement supplies a published
  locator for the rigorous contiguous range only through \(53\); unpublished files are not promoted
  into the cited frontier.
- Appleby et al. (2022) use exact algebraic data in dimensions as high as \(19603\), but explicitly
  say that most full checks were numerical. An exact-looking coordinate field plus some exact
  overlap checks is not a complete exact SIC certificate.

## What is open as of 2026-08-18

- `cited`: universal unrestricted SIC existence remains open.
- `cited`: universal WH existence is the stronger open Conjecture 2.4 of Kopp–Lagarias.
- `sketch` is not needed for either statement: they are directly stated as conjectures by the
  primary sources.
- `numerical`: all finite search frontiers above are evidence only. None licenses induction to
  untested dimensions or replacement of unrestricted SICs by the WH/Zauner ansatz.

## Primary sources

- J. M. Renes, R. Blume-Kohout, A. J. Scott, M. C. Caves,
  [*Symmetric Informationally Complete Quantum Measurements*](https://arxiv.org/abs/quant-ph/0310075),
  J. Math. Phys. 45 (2004), 2171–2180.
- G. S. Kopp,
  [*SIC-POVMs and the Stark Conjectures*](https://doi.org/10.1093/imrn/rnz153),
  IMRN 2021(18), 13812–13838; Definitions 2.3 and 2.7–2.9, Theorem 5.4.
- A. J. Scott and M. Grassl,
  [*SIC-POVMs: A new computer study*](https://arxiv.org/abs/0910.5784),
  J. Math. Phys. 51 (2010), 042203.
- A. J. Scott,
  [*SICs: Extending the list of solutions*](https://arxiv.org/abs/1703.03993) (2017), with
  accompanying numerical data.
- C. A. Fuchs, M. C. Hoang, B. C. Stacey,
  [*The SIC Question: History and State of Play*](https://arxiv.org/abs/1703.07901),
  Axioms 6 (2017), 21.
- M. Appleby, T.-Y. Chien, S. Flammia, S. Waldron,
  [*Constructing Exact Symmetric Informationally Complete Measurements from Numerical
  Solutions*](https://arxiv.org/abs/1703.05981), J. Phys. A 51 (2018), 165302.
- M. Appleby, I. Bengtsson, M. Grassl, M. Harrison, G. McConnell,
  [*SIC-POVMs from Stark Units: Prime Dimensions \(n^2+3\)*](https://arxiv.org/abs/2112.05552),
  J. Math. Phys. 63 (2022), 112205.
- G. S. Kopp, J. C. Lagarias,
  [*SIC-POVMs and Orders of Real Quadratic Fields*](https://doi.org/10.1016/j.jnt.2026.05.013),
  J. Number Theory (available online 17 July 2026); Definitions 2.2–2.3, Conjectures 2.4–2.5,
  and Table 1.
