# The Riemann Hypothesis

**Status:** open since 1859. Nothing in this directory changes that.

Shared conventions for problem directories are in [`../README.md`](../README.md); the claim
status taxonomy is in [`../../RULES.md`](../../RULES.md) §3.

## Statement

For $\operatorname{Re}(s) > 1$ define

$$\zeta(s) = \sum_{n=1}^{\infty} n^{-s},$$

and extend $\zeta$ by analytic continuation to $\mathbb{C} \setminus \{1\}$ (simple pole at
$s = 1$, residue $1$). The continuation satisfies the functional equation

$$\pi^{-s/2}\,\Gamma(s/2)\,\zeta(s) \;=\; \pi^{-(1-s)/2}\,\Gamma\!\left(\tfrac{1-s}{2}\right)\zeta(1-s).$$

The functional equation forces *trivial* zeros at $s = -2, -4, -6, \dots$ All other zeros lie in
the **critical strip** $0 \le \operatorname{Re}(s) \le 1$.

> **Riemann Hypothesis.** Every non-trivial zero of $\zeta$ satisfies $\operatorname{Re}(s) = \tfrac{1}{2}$.

## Why this problem

RH is a good stress test for the workflow precisely because it is saturated with
plausible-looking dead ends. An agent that fools itself here gets caught by the verifier rather
than by a reviewer's patience — and the failure is instructive either way.

It is also, obviously, a joke. Both things are true.

## Landscape

Load-bearing results an agent may assume, with attribution. Do not add to this table without a
citation you have personally resolved.

Every locator below was fetched on 2026-09-04 (issue #260); nothing here is from memory. The
rows are split into two tables by how much was actually checked.

- **Verified** means the locator resolved *and* the source was read far enough to confirm it
  says what the row says. These are `cited` in the sense of
  [`../../RULES.md`](../../RULES.md) §3, and therefore assumable.
- **Provisional** means the locator resolved but something is still open — a statement checked
  only against a secondary source, a source that was never peer-reviewed, or an attribution
  broader than what the cited work establishes. These are **not assumable**: treat them as
  pointers for a reader, not as premises.

The reason for the split rather than a single tidy table is §3: `cited` is assumable, so a
resolved DOI attached to a misstated theorem is worse than no citation, because it launders the
misstatement into a dependency.

### Verified — `cited`, assumable

| Result | Source | Locator |
|---|---|---|
| $\zeta(1+it) \ne 0$ for all real $t$, and hence $\psi(x) \sim x$ (the Prime Number Theorem) | Hadamard (1896) [^hadamard] | [10.24033/bsmf.545](https://doi.org/10.24033/bsmf.545) |
| There is a constant $R_0$ with $\zeta(s) \ne 0$ for $\sigma > 1 - 1/(R_0\log\lvert t\rvert)$, **for $\lvert t\rvert$ sufficiently large**. De la Vallée Poussin's own value was $R_0 = 30.4679$. | de la Vallée Poussin (1899–1900) [^dlvp99]; statement and constant as recorded by Mossinghoff–Trudgian [^mt] | [arXiv:1410.3926](https://arxiv.org/abs/1410.3926) |
| The *asymptotic* proportion of non-trivial zeros lying on the critical line — i.e. $\liminf_{T\to\infty} N_0(T)/N(T)$, where $N_0$ counts zeros on the line and $N$ counts all zeros up to height $T$ — exceeds $1/3$; later improved past $2/5$ | Levinson (1974) [^levinson]; Conrey (1989) [^conrey] | [10.1016/0001-8708(74)90074-7](https://doi.org/10.1016/0001-8708%2874%2990074-7); [10.1515/crll.1989.399.1](https://doi.org/10.1515/crll.1989.399.1) |
| RH for **curves over finite fields** is a theorem | Weil — announced 1940 [^weil40], full proof in the 1948 monograph [^weil48] | C. R. Acad. Sci. Paris **210** (1940), 592–594 |
| The Riemann-hypothesis part of the **Weil conjectures** is a theorem: for a nonsingular projective variety $V_0/\mathbb{F}_q$, the eigenvalues of Frobenius on $H^r(V,\mathbb{Q}_\ell)$ are algebraic numbers all of whose complex conjugates have absolute value $q^{r/2}$ | Deligne (1974) [^deligne] | [10.1007/BF02684373](https://doi.org/10.1007/BF02684373) |

### Provisional — resolved but not fully checked, or not peer-reviewed. **Not assumable.**

| Result | Source | Why it is not `cited` |
|---|---|---|
| Infinitely many zeros lie on the critical line | Hardy (1914) [^hardy] | Bibliographic record confirmed (author, title, volume, page) against the *Comptes rendus* tome 158 table of contents and Ivić's bibliography, but **no full scan of the three-page note was resolved**, so the statement rests on secondary sources rather than on the note itself. |
| All zeros up to the $10^{13}$-th verified to lie on the critical line | Gourdon (2004), with the distributed computation managed by Patrick Demichel [^gourdon] | Source read and it says exactly this — but it is an **unrefereed preprint on a personal website**, never published. Under §3 this is `numerical` evidence with a specific reference, not literature. |
| $\zeta(1+it)\ne 0$ for all real $t$ is *equivalent* to the Prime Number Theorem | — | The 1896 papers of Hadamard and de la Vallée Poussin prove the **forward** implication (non-vanishing $\Rightarrow$ PNT) and thereby PNT. The converse is a separate, later, standard argument. **Nothing here cites the equivalence itself**, so do not assume the biconditional on the strength of a 1896 attribution. |
| de la Vallée Poussin's independent 1896 proof of PNT | de la Vallée Poussin (1896) [^dlvp96] | The 1896 *Recherches analytiques* was **not resolved to a paginated scan of the article**; the archive.org copy is a monograph reprint whose metadata does not give the journal volume or pages. The volume/page data below is from secondary listings only. |

### Equivalent reformulations

Worth reading before inventing a new one. These are named here with citations only; the
criteria are deliberately **not restated**, because a restated criterion with a flipped
inequality or a shifted threshold is exactly the error this table exists to prevent. Read the
source.

| Criterion | Source | Status |
|---|---|---|
| Lagarias' criterion | Lagarias (2002) [^lagarias] | resolved — [10.2307/2695443](https://doi.org/10.2307/2695443) |
| Li's criterion | Li (1997) [^li] | resolved — [10.1006/jnth.1997.2137](https://doi.org/10.1006/jnth.1997.2137) |
| Nyman–Beurling criterion | Beurling (1955) [^beurling] | Beurling half resolved — [10.1073/pnas.41.5.312](https://doi.org/10.1073/pnas.41.5.312). **Nyman's 1950 Uppsala thesis was not resolved.** |
| Robin's criterion | Robin (1984) [^robin] | **provisional** — no DOI or scan resolved; page range corroborated only by two independent secondary bibliographies. |
| Weil's explicit-formula positivity criterion | Weil (1952) | **unresolved** — no locator found this session. Do not cite from memory. |

### de Branges

De Branges proposed an approach to the generalized Riemann hypothesis via positivity conditions
on Hilbert spaces of entire functions. Conrey and Li [^conreyli] "give examples showing that de
Branges' positivity conditions, which imply the generalized Riemann hypothesis, are not
satisfied by defining functions of reproducing kernel Hilbert spaces associated with the
Riemann zeta function $\zeta(s)$ and the Dirichlet $L$-function $L(s,\chi_4)$." That is a
specific published obstruction to the positivity conditions as proposed; the earlier claim in
this file that the programme is "the most-cited failed approach" was an unverifiable
superlative and has been removed. If anyone proposes this route, `attacks/` is the place, and
Conrey–Li is the first thing to read.

[^hadamard]: J. Hadamard, *Sur la distribution des zéros de la fonction $\zeta(s)$ et ses conséquences arithmétiques*, Bulletin de la Société Mathématique de France **24** (1896), 199–220. DOI [10.24033/bsmf.545](https://doi.org/10.24033/bsmf.545); scan at [numdam](https://www.numdam.org/item/BSMF_1896__24__199_1/). Read: Hadamard states the target as establishing "que la fonction $\zeta$ n'ait pas de zéros sur la droite $\Re(s)=1$ … c'est cette dernière conclusion que je me propose de démontrer", and concludes with the asymptotic for the sum of $\log p$ over $p<x$. (Crossref's record for this DOI lists the volume as "2"; the scan's own header and numdam both say tome 24, and the scan wins.)
[^dlvp96]: C.-J. de la Vallée Poussin, *Recherches analytiques sur la théorie des nombres premiers*, Annales de la Société Scientifique de Bruxelles **20** (1896). Volume and pagination from secondary listings; not confirmed against a paginated scan. Copy at [archive.org](https://archive.org/details/recherchesanalyt00lava).
[^dlvp99]: C.-J. de la Vallée Poussin, *Sur la fonction $\zeta(s)$ de Riemann et le nombre des nombres premiers inférieurs à une limite donnée*, Mém. Couronnés et Autres Mém. Publ. Acad. Roy. Sci. Lettres Beaux-Arts Belg. **59** (1899–1900), 1–74. Scan at [archive.org](https://archive.org/details/surlafonctionze00pousgoog). **This, not the 1896 paper, is the source of the classical zero-free region.**
[^mt]: M. J. Mossinghoff and T. S. Trudgian, *Nonnegative trigonometric polynomials and a zero-free region for the Riemann zeta-function*, [arXiv:1410.3926](https://arxiv.org/abs/1410.3926). §1 states de la Vallée Poussin's 1899 region in the form used above, with the "$\lvert t\rvert$ is sufficiently large" hypothesis explicit, and Table 1 attributes $R_0 = 30.4679$ to him.
[^hardy]: G. H. Hardy, *Sur les zéros de la fonction $\zeta(s)$ de Riemann*, C. R. Acad. Sci. Paris **158** (1914), 1012–1014. Entry confirmed in the [tome 158 table of contents](https://fr.wikisource.org/wiki/Comptes_rendus_de_l%E2%80%99Acad%C3%A9mie_des_sciences/Tome_158,_1914/Table_des_mati%C3%A8res); a scan of the volume is at [BHL](https://www.biodiversitylibrary.org/item/31512). Full text not read.
[^levinson]: N. Levinson, *More than one third of zeros of Riemann's zeta-function are on $\sigma = 1/2$*, Advances in Mathematics **13** (1974), no. 4, 383–436. DOI [10.1016/0001-8708(74)90074-7](https://doi.org/10.1016/0001-8708%2874%2990074-7). Caution: Ivić's *The Theory of Hardy's Z-Function* lists this as "Adv. Math. 18 (1975), 383–346" — wrong volume, wrong year, and an inverted page range. Crossref's record is the one above.
[^conrey]: J. B. Conrey, *More than two fifths of the zeros of the Riemann zeta function are on the critical line*, J. reine angew. Math. **399** (1989), 1–26. DOI [10.1515/crll.1989.399.1](https://doi.org/10.1515/crll.1989.399.1).
[^gourdon]: X. Gourdon, *The $10^{13}$ first zeros of the Riemann Zeta function, and zeros computation at very large height*, version of 24 October 2004. [PDF](http://numbers.computation.free.fr/Constants/Miscellaneous/zetazeros1e13-1e24.pdf). §3: "Our first family of computations consisted in verifying that until the $10^{13}$-th zero, all zeros of the Riemann Zeta function lie on the critical line $\Re(s) = 1/2$." Sole author; the acknowledgments credit Patrick Demichel with managing the distributed computation.
[^weil40]: A. Weil, *Sur les fonctions algébriques à corps de constantes fini*, C. R. Acad. Sci. Paris **210** (1940), 592–594 — an **announcement**. See also A. Weil, *On the Riemann hypothesis in function-fields*, Proc. Nat. Acad. Sci. U.S.A. **27** (1941), 345–347.
[^weil48]: A. Weil, *Sur les courbes algébriques et les variétés qui s'en déduisent*, Actualités Sci. Ind. no. 1041 = Publ. Inst. Math. Univ. Strasbourg 7, Hermann, Paris, 1948 — the complete proof. Bibliographic data and the announcement/proof distinction taken from J. S. Milne, *The Riemann Hypothesis over Finite Fields: From Weil to the Present Day*, [arXiv:1509.00797](https://arxiv.org/abs/1509.00797) ([PDF](https://www.jmilne.org/math/xnotes/pRH.pdf)), §1 and bibliography.
[^deligne]: P. Deligne, *La conjecture de Weil. I*, Publications Mathématiques de l'IHÉS **43** (1974), 273–307. DOI [10.1007/BF02684373](https://doi.org/10.1007/BF02684373). The statement above is Theorem 5.1 of Milne's survey [^weil48].
[^lagarias]: J. C. Lagarias, *An elementary problem equivalent to the Riemann hypothesis*, Amer. Math. Monthly **109** (2002), no. 6, 534–543. DOI [10.2307/2695443](https://doi.org/10.2307/2695443).
[^li]: X.-J. Li, *The positivity of a sequence of numbers and the Riemann hypothesis*, Journal of Number Theory **65** (1997), no. 2, 325–333. DOI [10.1006/jnth.1997.2137](https://doi.org/10.1006/jnth.1997.2137).
[^beurling]: A. Beurling, *A closure problem related to the Riemann zeta-function*, Proc. Nat. Acad. Sci. U.S.A. **41** (1955), no. 5, 312–314. DOI [10.1073/pnas.41.5.312](https://doi.org/10.1073/pnas.41.5.312).
[^robin]: G. Robin, *Grandes valeurs de la fonction somme des diviseurs et hypothèse de Riemann*, J. Math. Pures Appl. (9) **63** (1984), 187–213. No DOI or scan resolved; the page range is corroborated by two independent arXiv bibliographies but one widely-mirrored aggregator gives "187–182" and another "187–217". Treat the pagination as unconfirmed.
[^conreyli]: J. B. Conrey and X.-J. Li, *A note on some positivity conditions related to zeta and $L$-functions*, International Mathematics Research Notices **2000**, no. 18. DOI [10.1155/S1073792800000489](https://doi.org/10.1155/S1073792800000489); preprint [arXiv:math/9812166](https://arxiv.org/abs/math/9812166) (quoted above from §1 of the preprint). Crossref gives the first page as 929; the last page was not confirmed.

## Lean

Mathlib states RH (`RiemannHypothesis`) and carries a substantial analytic number theory
library, so classical lemmas here are plausible formalisation targets. Confirm the exact
Mathlib declaration names before depending on them — do not guess API from memory.
