# Less-mainstream open problems in mathematics

**Online status check:** 18 August 2026. Each entry was rechecked against the linked source; inaccessible publisher pages were cross-checked through their indexed abstract or an open manuscript copy.

**Purpose:** a starting list for serious research triage, not a claim that any item is easy. The list avoids the usual headline problems (RH, P vs NP, Navier--Stokes, Goldbach, Collatz, twin primes, etc.) and favors problems with a crisp statement, active partial progress, and an attack that can be scoped into a finite project.

## How this list was selected

I required a recent research paper, survey, journal page, or maintained expert source that still treats the problem as open. I excluded problems for which a recent proof claim looked likely to have become accepted, and I did not count numerical verification as proof. “First attack” below means a realistic *research subproject*—usually a restricted class, exact finite census, stability statement, or equivalence—not a promise that the full conjecture is approachable.

The sources are deliberately placed with each entry so that status can be rechecked before substantial work begins. Preprints are identified as such.

---

## 1. Caccetta--Häggkvist conjecture

- **Area:** extremal directed graph theory.
- **Statement:** Every loopless simple digraph on $n$ vertices with minimum out-degree at least $r$ contains a directed cycle of length at most $\lceil n/r\rceil$.
- **Why it matters:** It is the cleanest general proposed relation between local outward expansion and directed girth. The triangle case already captures a major obstruction in oriented graph theory.
- **What is known / first attack:** The conjecture is known for small fixed $r$, vertex-transitive/Cayley cases, and various forbidden-subgraph or density regimes, but even the sharp minimum-outdegree-$n/3$ triangle case is open. A useful entry project is an exact census of minimal triangle-free oriented graphs near the $n/3$ threshold, with independently checkable certificates, followed by extraction of unavoidable local configurations rather than merely extending a brute-force bound.
- **Open-status check (2026-08-18):** Chen, Guo and Huang, *Short rainbow cycles in edge-colored graphs*, Discrete Mathematics 349 (2026), which explicitly says the conjecture remains open: [open-access paper](https://www.diva-portal.org/smash/get/diva2%3A2016769/FULLTEXT01.pdf). See also Nathanson’s additive-number-theory formulation: [arXiv:math/0603469](https://arxiv.org/abs/math/0603469).

## 2. Graceful Tree Conjecture

- **Area:** graph labeling / additive combinatorics.
- **Statement:** If a tree has $m$ edges, can its vertices always be injectively labeled by $0,1,\ldots,m$ so that the absolute differences across the edges are exactly $1,2,\ldots,m$?
- **Why it matters:** A very elementary labeling condition hides difficult global arithmetic constraints and connects to cyclic graph decompositions and design theory.
- **What is known / first attack:** Many tree families are graceful. A 2025 preprint proves that every sufficiently large $n$-vertex tree has a labeling realizing at least $(1-\varepsilon)n$ distinct edge differences. A plausible project is to make that asymptotic argument quantitative for a controlled family (bounded pathwidth, bounded number of branch vertices, or a prescribed degree sequence), or to build a proof-producing SAT/CP census that identifies the smallest unresolved structural motifs.
- **Open-status check (2026-08-18):** Letzter, Pokrovskiy and Williams, *On the gracesize of trees* (2025 preprint): [arXiv:2511.11331](https://arxiv.org/abs/2511.11331). The maintained graph-labeling survey also lists current classes and open cases: [Gallian, Dynamic Survey of Graph Labeling](https://www.combinatorics.org/files/Surveys/ds6/ds6v27-2024.pdf).

## 3. Frankl’s union-closed sets conjecture

- **Area:** extremal set theory / information theory.
- **Statement:** Every finite union-closed family ​\(\mathcal F\ne\{\varnothing\}\) has an element contained in at least half of the members of \(\mathcal F\).
- **Why it matters:** The statement is local and finite, but the best general methods are global—entropy, coupling, lattice structure, and Boolean-function techniques.
- **What is known / first attack:** The breakthrough entropy method gives a universal frequency bounded away from zero; the cited peer-reviewed refinement reaches $(3-\sqrt5)/2\approx0.381966$, still short of $1/2$. Realistic projects include optimizing the finite-support measure problem behind the entropy bound, proving the conjecture for another natural Horn-function or lattice class, or performing a proof-certified census under a structural restriction suggested by minimal-counterexample theory.
- **Open-status check (2026-08-18):** Alweiss, Huang and Sellke, *Improved Lower Bound for Frankl’s Union-Closed Sets Conjecture*, Electronic Journal of Combinatorics 31 (2024): [paper](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v31i3p35/pdf/). Lozin and Zamaraev give the Horn-Boolean viewpoint and new verified classes: [peer-reviewed repository record](https://wrap.warwick.ac.uk/id/eprint/180696/).

## 4. The $1/3$--$2/3$ conjecture for posets

- **Area:** order theory / probabilistic combinatorics.
- **Statement:** Every finite poset that is not a chain contains incomparable elements $x,y$ such that a uniformly random linear extension puts $x$ before $y$ with probability in $[1/3,2/3]$.
- **Why it matters:** It says every partially completed comparison sort has a next comparison that removes at least one third of the remaining possibilities. The constants are sharp.
- **What is known / first attack:** The conjecture holds for numerous structured classes and, according to a July 2026 preprint, for all posets through 14 elements. A strong finite project would independently certify that census, classify equality/near-equality cases, or prove the conjecture for a narrowly defined class not covered by width-two, height-two, semiorder, or $N$-free results.
- **Open-status check (2026-08-18):** Gupta, *Balance Constants, Majority Cycles, and the Gold Partition Conjecture through Fourteen Elements* (2026 preprint), whose result implies the $1/3$--$2/3$ conjecture through order 14: [arXiv:2607.23926](https://arxiv.org/abs/2607.23926). For a class proof, see Zaguia’s $N$-free case: [EJC paper](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v19i2p29/pdf/).

## 5. Lonely Runner Conjecture

- **Area:** Diophantine approximation / discrete geometry.
- **Statement:** For $n\ge2$ runners moving at distinct constant speeds around a unit circle, each runner is, at some time, at circular distance at least $1/n$ from every other runner. Equivalently, after making one runner stationary, suitable integer multiples are simultaneously far from integers.
- **Why it matters:** It joins a child-friendly dynamical picture to simultaneous Diophantine approximation, zonotopes, view-obstruction, and finite computation.
- **What is known / first attack:** The conjecture was proved for nine runners in a December 2025 preprint, using a bounded minimal-counterexample search. The next concrete target is ten runners: independently formalize the reduction to a finite search, improve the size bound, and emit exact rational certificates rather than relying on floating point.
- **Open-status check (2026-08-18):** Rosenfeld, *The lonely runner conjecture holds for nine runners* (2025 preprint): [arXiv:2512.01912](https://arxiv.org/abs/2512.01912). Perarnau and Serra’s recent survey gives the broader map: [arXiv:2409.20160](https://arxiv.org/abs/2409.20160).

## 6. Komlós discrepancy conjecture

- **Area:** discrepancy theory / convex geometry.
- **Statement:** There is an absolute constant $C$ such that for any vectors $v_1,\ldots,v_n\in\mathbb R^d$ with $\|v_i\|_2\le1$, one can choose signs $\varepsilon_i\in\{-1,1\}$ satisfying
  \[
  \left\|\sum_i \varepsilon_i v_i\right\|_\infty\le C.
  \]
- **Why it matters:** It is a canonical vector-balancing problem with consequences for randomized rounding, numerical integration, and combinatorial discrepancy.
- **What is known / first attack:** General bounds remain dimension-dependent, while random and smoothed models often achieve constant or smaller discrepancy. A tractable project is to isolate the weakest pseudorandomness condition on a matrix under which a constructive constant bound follows, or to test whether partial-coloring algorithms certify new structured matrix classes.
- **Open-status check (2026-08-18):** Aigner-Horev, Hefetz and Trushkin, *Smoothed Analysis of the Komlós Conjecture: Rademacher Noise*: [arXiv:2307.06285](https://arxiv.org/abs/2307.06285).

## 7. Log-rank conjecture

- **Area:** communication complexity / matrix theory.
- **Statement:** For every Boolean matrix $M$, its deterministic communication complexity is bounded by a fixed polynomial in $\log \operatorname{rank}_{\mathbb R}(M)$. Equivalently, a low-rank Boolean matrix should admit a quasi-polynomial-size partition into monochromatic rectangles.
- **Why it matters:** It asks whether an algebraic measure of a communication problem controls its exact combinatorial complexity; it is a central bridge between theoretical CS and additive/matrix combinatorics.
- **What is known / first attack:** The best general bounds are far from polylogarithmic. A 2025 reformulation reduces the problem to converting signed rectangle decompositions into positive ones with quasi-polynomial blowup. That conversion on restricted support graphs, bounded sign-rank patterns, or tensor products is a plausible entry point.
- **Open-status check (2026-08-18):** Hambardzumyan, Lovett and Shirley, *The Log-Rank Conjecture: New Equivalent Formulations* (2025 preprint): [arXiv:2510.02583](https://arxiv.org/abs/2510.02583).

## 8. Andrews--Curtis conjecture

- **Area:** combinatorial group theory / low-dimensional topology.
- **Statement:** Every balanced presentation of the trivial group can be transformed to the standard trivial presentation using Nielsen moves on relators, conjugating relators, and inversion.
- **Why it matters:** It connects elementary-looking transformations of words in free groups to handle decompositions of 4-manifolds. Candidate counterexamples can be explored computationally, but proving non-equivalence requires genuine invariants.
- **What is known / first attack:** A July 2026 preprint reports machine-checkable verification for rank-two presentations through total relator length 12 and reduces length 13 to the still-open Akbulut--Kirby presentation $AK(3)$. The natural next project is independent certificate checking, better canonicalization of the move graph, or an invariant that separates a bounded candidate from the trivial orbit.
- **Open-status check (2026-08-18):** *Machine-checkable equivalence certificates at the length-14 Andrews--Curtis frontier* (2026 preprint): [arXiv:2607.23611](https://arxiv.org/abs/2607.23611). For the algebraic action formulation, see *Andrews--Curtis groups*: [journal version](https://gcc.episciences.org/15972).

## 9. Toeplitz’s square-peg problem for arbitrary Jordan curves

- **Area:** plane topology / symplectic and discrete geometry.
- **Statement:** Does every simple closed continuous curve in the plane contain four distinct points that are the vertices of a nondegenerate square?
- **Why it matters:** Smooth curves yield to configuration-space and symplectic methods, but passing to arbitrary continuous curves allows inscribed squares to collapse in limits; this is a clean test of how geometry survives weak regularity.
- **What is known / first attack:** The smooth case is stronger than solved: every prescribed rectangle shape occurs. Many nonsmooth classes are also known, but general Jordan curves remain open. A realistic target is a compactness theorem preventing collapse under one new quantitative regularity condition, or a verified polygonal approximation result with a uniform lower bound on square side length.
- **Open-status check (2026-08-18):** Wright, *Every Jordan Curve Contains All Vertices of Uncountably Many Rhombi* (accepted 2025), still states Toeplitz’s assertion as a conjecture: [DOI page](https://www.tandfonline.com/doi/abs/10.1080/00029890.2025.2556357). Greene and Lobb’s smooth rectangular-peg theorem: [arXiv:2005.09193](https://arxiv.org/abs/2005.09193).

## 10. Hadwiger--Boltyanski illumination conjecture

- **Area:** convex and discrete geometry.
- **Statement:** Every convex body in $\mathbb R^d$ can be illuminated by at most $2^d$ exterior directions (equivalently, covered by at most $2^d$ smaller positive homothetic copies), with equality only for affine cubes.
- **Why it matters:** It translates between boundary visibility and covering geometry and remains wide open already in low dimensions above the plane.
- **What is known / first attack:** The planar case and many symmetric or structured classes are known. Suitable first projects include exact illumination of one narrowly specified polytope family, stability near the cube, or improving a dimension-specific bound using John position plus a computer-certified spherical covering.
- **Open-status check (2026-08-18):** Arman, Bondarenko and Prymak, *On Hadwiger’s covering problem in small dimensions* (2025), says the conjecture is wide open: [open-access article](https://doi.org/10.4153/S0008439525000384). Recent special-class progress: [arXiv:2407.11331](https://arxiv.org/abs/2407.11331).

## 11. Symmetric Mahler conjecture in dimension $d\ge4$

- **Area:** convex geometry / asymptotic geometric analysis.
- **Statement:** For every centrally symmetric convex body $K\subset\mathbb R^d$,
  \[
  \operatorname{vol}(K)\operatorname{vol}(K^\circ)\ge \frac{4^d}{d!},
  \]
  with equality conjecturally attained by cubes and, more generally, Hanner polytopes.
- **Why it matters:** The volume product is affine-invariant and sits at the intersection of convexity, Banach-space geometry, symplectic geometry, and functional inequalities.
- **What is known / first attack:** The symmetric conjecture is known in dimensions at most three and for important special classes such as unconditional bodies. Workable subprojects include local stability near a Hanner polytope, a new symmetry class in dimension four, or exact polyhedral minimization under a fixed combinatorial type.
- **Open-status check (2026-08-18):** A 2025 paper on symplectically self-polar bodies explicitly notes the symmetric case remains open: [Springer article](https://link.springer.com/article/10.1007/s40316-025-00251-0). The 3D proof and stability result are in [arXiv:1904.10765](https://arxiv.org/abs/1904.10765). Note that the *non-symmetric* dimension-three case was separately claimed solved in May 2026: [arXiv:2605.09334](https://arxiv.org/abs/2605.09334).

## 12. Birkhoff conjecture for convex billiards

- **Area:** Hamiltonian dynamics / geometry.
- **Statement:** In a standard smooth formulation, if a neighborhood of the boundary of a strictly convex planar billiard table is foliated by caustics, must the boundary be an ellipse? (There are stronger and weaker formulations, so assumptions must always be stated.)
- **Why it matters:** Ellipses are the model integrable billiards. The conjecture is a rigidity problem asking whether integrability forces classical geometry.
- **What is known / first attack:** Local versions near ellipses and several polynomial/global-integrability variants are known. A plausible project is to settle one missing rational caustic order under a symmetry condition, sharpen a perturbative estimate, or rigorously explore low-degree polynomial first integrals and extract an algebraic obstruction.
- **Open-status check (2026-08-18):** The 2026 multi-author problem list *Open problems in billiards and quantitative symplectic geometry* treats billiard rigidity questions as open: [arXiv:2602.12896](https://arxiv.org/abs/2602.12896). For the classical formulation and related variants, see Bialy, Fierobe, Glutsyuk, Levi, Plakhov and Tabachnikov: [arXiv:2110.10750](https://arxiv.org/abs/2110.10750).

## 13. Brennan’s conjecture

- **Area:** geometric function theory / complex analysis.
- **Statement:** If \(\Omega\subsetneq\mathbb C\) is simply connected and \(\phi:\Omega\to\mathbb D\) is conformal, then
  \[
  \int_\Omega |\phi'(z)|^p\,dA(z)<\infty
  \qquad\text{for every }\frac43<p<4.
  \]
- **Why it matters:** It asks for the sharp universal integrability range of conformal distortion and connects to integral-means spectra, quasiconformal maps, and Sobolev composition operators.
- **What is known / first attack:** Substantial proper subranges and special domains are known, but the endpoint-near-$4$ regime remains out of reach. A realistic target is a new domain class (for example, controlled basin boundaries, quasidisks with a quantitative parameter, or finitely generated slit geometries), coupled with sharp numerical stress tests to identify the extremal boundary shape.
- **Open-status check (2026-08-18):** Baranov and Kayumov (2023/24) state the conjecture and its open status: [Math-Net journal page](https://www.mathnet.ru/php/archive.phtml?jrnid=sm&option_lang=eng&paperid=9889&wshow=paper). A 2026 special-domain attack is [arXiv:2604.12240](https://arxiv.org/abs/2604.12240).

## 14. Iwaniec’s Beurling--Ahlfors norm conjecture

- **Area:** harmonic analysis / quasiconformal geometry / martingales.
- **Statement:** For $1<p<\infty$, the Beurling--Ahlfors transform $B$ on $L^p(\mathbb C)$ should satisfy
  \[
  \|B\|_{L^p\to L^p}=p^*-1,
  \qquad p^*=\max\!\left(p,\frac{p}{p-1}\right).
  \]
- **Why it matters:** The conjectured sharp constant mirrors Burkholder’s martingale-transform constant and would sharpen major distortion estimates for quasiconformal maps.
- **What is known / first attack:** Sharp lower bounds are understood, while known upper bounds miss the conjectured constant. Entry projects can focus on radial/finite-angular-mode functions, finite-dimensional Bellman-function ansätze, or exact optimization for truncated martingale models that preserve enough structure to say something rigorous about $B$.
- **Open-status check (2026-08-18):** Dragičević and Volberg, *Special martingale transforms, queen beds, and the Ahlfors--Beurling operator* (published online 2025; journal issue 2026): [journal page](https://www.sciencedirect.com/science/article/abs/pii/S0723086925000696). A recent paper explicitly discussing the conjectural norm is available here: [manuscript](https://citeseerx.ist.psu.edu/document?doi=ed063c2906995bdaadd7b4ca2d623bbfa50cf7cf&repid=rep1&type=pdf).

## 15. Lehmer’s totient problem

- **Area:** elementary and computational number theory.
- **Statement:** Is there a composite integer $n$ such that $\varphi(n)\mid n-1$? Lehmer conjectured that no such composite exists.
- **Why it matters:** Any solution would be an exceptionally constrained square-free odd Carmichael number with many prime factors. The problem combines elementary congruences with global multiplicative structure.
- **What is known / first attack:** Strong lower bounds on the number of prime factors and on the size of a hypothetical solution are known. A credible project is not a blind integer search: improve a conditional lower bound for a fixed smallest prime factor, encode the prime-factor constraints as an exact covering/constraint problem, or independently certify a substantially enlarged search region.
- **Open-status check (2026-08-18):** MathWorld’s maintained entry (updated in 2026) summarizes the problem and constraints: [Lehmer’s Totient Problem](https://mathworld.wolfram.com/LehmersTotientProblem.html). A 2025 journal paper still treats the conjecture as open: [article PDF](https://reference-global.com/download/article/10.2478/awutm-2025-0005.pdf).

## 16. Rokhlin’s multiple-mixing problem

- **Area:** ergodic theory / probability-preserving dynamics.
- **Statement:** If an invertible measure-preserving transformation is strongly mixing (two-fold mixing), must it be mixing of order three—and hence of all orders?
- **Why it matters:** For $\mathbb Z^d$-actions with $d\ge2$, mixing need not imply higher-order mixing, but no analogous counterexample is known for a single $\mathbb Z$-action. The problem probes what pairwise asymptotic independence really controls.
- **What is known / first attack:** Positive answers are known for important classes including Gaussian, Poisson, algebraic, and several rank-one or shearing systems under extra hypotheses. A useful first attack is to prove 3-mixing for a sharply delimited construction class, or to translate a proposed counterexample into explicit joining constraints and rule it out.
- **Open-status check (2026-08-18):** Ryzhikov, *Multiple mixing, 75 years of Rokhlin’s problem* (2024 survey/preprint): [arXiv:2411.07234](https://arxiv.org/abs/2411.07234). A 2026 dynamics paper still describes Rokhlin’s question in this form: [Cambridge journal page](https://www.cambridge.org/core/journals/ergodic-theory-and-dynamical-systems/article/on-mixing-flows-on-finitearea-translation-surfaces/E5C54801CDE68E0F0D25777398AAD1C1).

## 17. Planar self-avoiding walk scaling limit

- **Area:** probability / statistical mechanics.
- **Statement:** After the correct spatial rescaling, does the uniform self-avoiding walk on a two-dimensional lattice converge to Schramm--Loewner evolution \(\mathrm{SLE}_{8/3}\)? Even existence and conformal invariance of the Euclidean-lattice scaling limit are open.
- **Why it matters:** This would rigorously connect a basic polymer model to conformal random geometry and prove predicted critical exponents such as the $4/3$ fractal dimension.
- **What is known / first attack:** High-dimensional behavior is accessible via lace expansion, and the corresponding statement has been proved on certain random planar maps, but \(\mathbb Z^2\) remains resistant. A realistic project is a rigorous finite-domain observable estimate, a special strip/half-plane limit, or certified Monte Carlo tests designed to distinguish correction-to-scaling hypotheses rather than merely reproduce the expected exponent.
- **Open-status check (2026-08-18):** Slade’s expert survey explicitly says existence and conformal invariance of the two-dimensional scaling limit remain open: [survey PDF](https://personal.math.ubc.ca/~slade/spa_proceedings.pdf). The original Lawler--Schramm--Werner scaling-limit conjectures are in [arXiv:math/0204277](https://arxiv.org/abs/math/0204277); the random-quadrangulation analogue is recorded in the peer-reviewed Cambridge repository: [Gwynne--Miller](https://www.repository.cam.ac.uk/items/4f501335-0a82-4f37-bce6-2eaa44f32666).

## 18. Existence of SIC-POVMs in every dimension

- **Area:** algebraic geometry / finite frames / quantum information.
- **Statement:** For every integer $d\ge2$, do there exist $d^2$ unit vectors $v_1,\ldots,v_{d^2}\in\mathbb C^d$ such that
  \[
  |\langle v_i,v_j\rangle|^2=\frac{1}{d+1}\quad(i\ne j)?
  \]
  Equivalently, does a symmetric informationally complete rank-one quantum measurement exist in every dimension?
- **Why it matters:** SICs are optimal equiangular tight frames for quantum tomography and unexpectedly connect finite group actions to real quadratic fields and explicit class-field theory.
- **What is known / first attack:** Exact and numerical solutions exist in many dimensions, overwhelmingly with Weyl--Heisenberg covariance, but there is no uniform proof. Good projects include exact algebraic certification in a new dimension, proving existence for an infinite arithmetic subfamily under a stated number-theoretic hypothesis, or independently verifying the current benchmark dimension gaps.
- **Open-status check (2026-08-18):** Kopp and Lagarias, *SIC-POVMs and orders of real quadratic fields*, Journal of Number Theory (online July 2026), explicitly lists all-dimensional existence as unsolved: [journal page](https://www.sciencedirect.com/science/article/pii/S0022314X26001241). The basic existence statement is also formalized as an open problem by DeepMind: [formal-conjectures page](https://google-deepmind.github.io/formal-conjectures/doc/FormalConjectures/OpenQuantumProblems/23.html).

---

## A practical way to choose one

For a computation-first project, the best candidates here are **Lonely Runner (ten runners)**, **Andrews--Curtis (certificate checking and the $AK(3)$ frontier)**, **the $1/3$--$2/3$ conjecture (independent order-14 census)**, or **Caccetta--Häggkvist (minimal near-threshold oriented graphs)**. For proof-first restricted cases, **Graceful Trees**, **Illumination**, **Birkhoff billiards**, and **SIC-POVMs** have natural class-by-class programs. For analysis-heavy work, **Komlós**, **Brennan**, and **Beurling--Ahlfors** offer sharp quantitative intermediate targets.

Before opening a project, recheck the newest version of the cited source, search its citations, write down an exact deliverable and kill criterion, and distinguish rigorously among **theorem**, **conditional theorem**, **computer-assisted theorem**, and **numerical evidence**.
