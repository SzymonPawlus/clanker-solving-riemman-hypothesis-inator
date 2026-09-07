# 2026-09-04 — pinning the RH landscape table to primary sources

Issue #260. `problems/riemann-hypothesis/RULES.md` §1.4 names this as one of only four
legitimate contributions in that directory: the Landscape table carried an HTML comment
admitting the proportions and the $10^{13}$ figure were from memory.

Egress was open. arXiv, Crossref, numdam, archive.org, fr.wikisource and academic homepages all
resolved. zbMATH returned 403 for me this session (the earlier worker's note said it was
reachable — it was not, for the query I tried), and I did not attempt JSTOR or Taylor & Francis.

## Method

For each row I wanted two separate things, and I tracked them separately because they fail
separately:

1. **a locator that actually resolves** — I fetched every one; nothing below is from memory;
2. **the source saying what our row says.**

Where (1) succeeded and (2) did not, the row moved to a provisional table rather than getting a
citation stapled to it. Under repo `RULES.md` §3 `cited` is assumable, so a resolved DOI
attached to a misstated theorem is strictly worse than no citation — it launders the misstatement.

Several sources are page scans. `WebFetch` cannot read a PDF, so the pattern that worked was: let
WebFetch save the binary, then `pdftotext -layout` locally and grep the OCR. That is how the
Hadamard, Mossinghoff–Trudgian, Gourdon, Milne and Conrey–Li checks were actually done.

## Per-row verdicts

**Row 1 — $\zeta \ne 0$ on $\Re s = 1$, Hadamard; de la Vallée Poussin (1896).**
Hadamard **verified**, and verified against the scan itself rather than a bibliography: BSMF
**24** (1896), 199–220, DOI `10.24033/bsmf.545`. The OCR gives him stating the target — "il n'a
même pas été établi que la fonction $\zeta$ n'ait pas de zéros sur la droite $\Re(s)=1$. C'est
cette dernière conclusion que je me propose de démontrer" — and closing with the asymptotic for
$\sum_{p<x}\log p$.

Two problems with the row as written:

- **"equivalent to the Prime Number Theorem" is an overstatement of what these papers do.**
  They prove the forward implication and thence PNT. The biconditional is a separate, later,
  standard fact. The mathematics is fine; the *attribution* was not. Demoted to provisional with
  the reason spelled out, because someone building on "equivalent, Hadamard 1896" would be
  building on something no cited source here establishes.
- **de la Vallée Poussin's 1896 half never resolved to a paginated article scan.** The
  archive.org copy is a monograph reprint whose metadata gives no volume or pages. Marked
  provisional.

**Row 2 — classical zero-free region $\sigma > 1 - c/\log|t|$, de la Vallée Poussin.**
**Statement mismatch — a dropped quantifier, and this is the one I would review hardest.**
Mossinghoff–Trudgian (arXiv:1410.3926) §1 state it as: there is a constant $R_0$ with
$\zeta(s)\ne 0$ for $\sigma > 1 - 1/(R_0\log|t|)$, *"where $R_0$ is a particular constant and
$|t|$ is sufficiently large."* Our row had neither the existential on the constant nor the
"$|t|$ large" hypothesis. Without the latter the assertion is not merely imprecise but false as
literally written: $\log|t| \to 0$ as $|t| \to 1$, so the claimed region swallows the whole
half-plane and then some. Both restored.

Also a **wrong-paper attribution by omission**: this is the 1899–1900 memoir (Mém. Couronnés
Acad. Roy. Belgique **59**, 1–74), not the 1896 paper the row above it points at. Their Table 1
credits de la Vallée Poussin with $R_0 = 30.4679$, which I recorded — a named constant is harder
to misremember later than a bare $c$.

**Row 3 — infinitely many zeros on the line, Hardy (1914).** **Provisional.** The bibliographic
record is solid — C. R. Acad. Sci. Paris **158** (1914), 1012–1014, confirmed independently in
the tome 158 table of contents on fr.wikisource ("Sur les zéros de la fonction ζ(s) de Riemann ;
par M. G.-H. Hardy — 1012") and in Ivić's bibliography. But I could not open the three-page note
itself. The attribution is not in doubt; the point of the flag is that I did not do for Hardy
what I did for Hadamard, and the table should not pretend otherwise.

**Row 4 — positive proportion, Levinson (1974) and Conrey (1989).** Both **verified** via
Crossref. Levinson, Adv. Math. **13** (1974) no. 4, 383–436; Conrey, Crelle **399** (1989), 1–26.
Both titles literally assert the row's content.

Two things worth recording:

- The row said "a positive proportion of zeros lie on the line". These are **asymptotic
  densities** — $\liminf_T N_0(T)/N(T)$ — not a statement about any fixed set of zeros. Made
  explicit. This is the density-stated-as-absolute failure mode and the row was one careless
  reading away from it.
- **Ivić's printed bibliography gives Levinson as "Adv. Math. 18 (1975), 383–346".** Wrong
  volume, wrong year, and the page range is *inverted*. I had gone to a respected monograph's
  bibliography precisely as a trustworthy shortcut, and it was wrong in three places at once.
  Recorded the correction in a footnote. The general lesson is unpleasant and worth keeping: a
  secondary bibliography is not a primary source, however good the book.

**Row 5 — first $\sim 10^{13}$ zeros, Gourdon (2004).** Locator **verified** and the statement
matches exactly — §3: "verifying that until the $10^{13}$-th zero, all zeros of the Riemann Zeta
function lie on the critical line". But it is an **unrefereed PDF on a personal website**, never
published. §3 defines `cited` as "established in the literature"; this is not that. Moved to
provisional as `numerical`-with-a-reference. Also credited Patrick Demichel per the
acknowledgments (he managed the distributed computation; Gourdon is sole author).

**Row 6 — function fields / Weil conjectures, "Weil; Deligne (1974)".** **Conflation of two
theorems**, now split. Weil's is RH for *curves* over finite fields — announced in C. R. **210**
(1940), 592–594, with the complete proof in the 1948 monograph (Milne's survey is explicit that
the 1940 note is an announcement). Deligne's is the RH part of the Weil conjectures for
*nonsingular projective varieties*, Publ. Math. IHÉS **43** (1974), 273–307,
DOI `10.1007/BF02684373` — Milne's Theorem 5.1, eigenvalues of Frobenius on $H^r$ having all
conjugates of absolute value $q^{r/2}$. The row's actual assertion, that the analogue **is** a
theorem, is correct in both cases.

**Equivalences.** Lagarias (`10.2307/2695443`), Li (`10.1006/jnth.1997.2137`) and the Beurling
half of Nyman–Beurling (`10.1073/pnas.41.5.312`) all resolved. Nyman's 1950 Uppsala thesis did
not. Robin is **provisional**: no DOI or scan, and secondary listings disagree on the page range
(187–213 twice on arXiv, but 187–182 and 187–217 elsewhere). **Weil's explicit-formula positivity
criterion is unresolved** — I found no locator and did not invent one.

I deliberately **did not restate any of the criteria**. Robin's is $\sigma(n) < e^{\gamma} n
\log\log n$ above a threshold, and a criterion of that shape is one keystroke from being
inverted or having its threshold shifted; since RH `RULES.md` §2 gives no credit for restating
equivalences anyway, citing the name and the locator is all upside.

**de Branges.** "The most-cited failed approach" is a sociological superlative I have no way to
check, and I removed it rather than leave an unfalsifiable claim sitting in a table of assumable
results. What is citable is Conrey–Li (`10.1155/S1073792800000489`, arXiv:math/9812166), quoted
from the preprint: they "give examples showing that de Branges' positivity conditions, which
imply the generalized Riemann hypothesis, are not satisfied" for $\zeta$ and $L(s,\chi_4)$.
Note their abstract says only that they "indicate its difficulty" — the body is stronger than the
abstract, and it is still narrower than "the programme failed". Wording tracks the body.

## Kill-criterion

Stated in #260: if egress were unavailable, stop and leave the table alone rather than pin
citations from memory. Egress was available, so it did not fire. The second half — demote rather
than rewrite a row whose source says something weaker — fired **four times** (rows 1, 3, 5, and
the de Branges sentence), and each time I demoted.

## What I did not do

No new rows. No approaches to RH (§2). No restatement of RH. No `results/` file — this work
produces citations for an existing README, not a new claim, and inventing a claim file to hold
them would be manufacturing work.

## Honest assessment

The output is a table split roughly five verified / four-plus provisional, which per RH
`RULES.md` §0 is the success condition. The failure mode I was most worried about in myself was
the pull toward closing the last few gaps by writing down a citation I "knew" — Weil 1952 and
Nyman 1950 both sat right at that edge, where I could recall a plausible-looking reference and
nothing would visibly break. They are marked unresolved.

The weakest thing I am handing over is that four rows rest on a **secondary** source read
carefully rather than on the primary read directly: the zero-free region statement via
Mossinghoff–Trudgian, the Weil announcement/proof split via Milne, Hardy via a table of
contents. Those are good secondary sources and I flagged each. But the Levinson episode above is
the reason to be uneasy about exactly that pattern — a monograph bibliography I trusted was
wrong in three fields simultaneously. The reviewer's time is best spent on row 2's quantifiers
and on whether the verified/provisional line is drawn in the right place.
