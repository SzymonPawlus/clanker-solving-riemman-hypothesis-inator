# 2026-08-21 — `eo-epsilon`: trying to get the Erdős–Oler deficit off zero

Worker W3, branch `claude/circle-equklatetal-problem-sa7tx7`. Brief: prove deficit
$\ge\varepsilon$ for *any* explicit $\varepsilon>0$ at $k=7$ ($n=27$, side $a<6$, separation 1),
via the brief's three-step programme: quantify Lemma T, force a face far from both equality
shapes, control the interior-edge correction.

**Outcome: explicit $\varepsilon=0$. Non-explicit $\varepsilon_7>0$.** Write-up:
[`problems/circle-packing-equilateral-triangle/attacks/eo-epsilon/`](../../problems/circle-packing-equilateral-triangle/attacks/eo-epsilon/).

## Order of work

1. Wrote [`KILL-CRITERION.md`](../../problems/circle-packing-equilateral-triangle/attacks/eo-epsilon/KILL-CRITERION.md)
   before any computation. K3 was written as "if a face-shape bound can be shown to yield
   nothing stronger than the target, step 1 is vacuous — say so and report $\varepsilon=0$". I
   expected it to fire, and it did.
2. Re-derived Lemma T and T2 (they are `sketch`, so not assumable). Both survive. Step 3 of
   Lemma T — its author's flagged step — I can reproduce: the concavity argument is exact and
   the vertex enumeration is complete. Recorded in §5 of the attack.
3. Proved Theorem Q, the quantitative Lemma T. It is genuinely sharp near the equality shapes
   (ratio $0.98$ at $(1,1,1.1)$).
4. Then established that it is useless — Proposition V. That is the real content.
5. Separately, noticed that Groemer 1960 applied to the *hull of the circles* is Oler verbatim,
   which makes the equality characterisation `cited` and gives Theorem E.

## The thing I got wrong first

Eight checks failed on the first run of `verify.py`. All eight were my harness, not the maths:
two adversarial scans generated triangles with a side $<1$ (outside Lemma T's hypothesis), the
square-scan started at $k=1$ where $4k^2+4k-7=1$ really is a square (with $a=-1$), and the
"$\sqrt3$-edge" witness I typed was the wrong quadrilateral. Recorded in the write-up §6 rather
than silently fixed: a scan that reports a violation of a correct lemma is evidence about the
scan.

## Why step 1 is vacuous, in one line

T2 is an *identity*: $\operatorname{slack}=\sum_f\tau(f)-\sum_{\mathrm{int}}(\ell_e-1)$. So a
lower bound $\tau\ge\Psi$ gives $\operatorname{slack}\ge\sum\Psi-\sum(\ell_e-1)$, and the
sharpest legal $\Psi$ — namely $\tau$ — returns the target statement unchanged. Sharpening the
face bound moves the derived inequality *towards* the target and never past it. So no
quantitative Lemma T, at any sharpness, can produce $\varepsilon>0$; all the content has to be
an independent handle on the interior-edge sum, and a handle strong enough is equivalent to the
target. The even-redistribution repair is exactly the already-refuted face-excess hypothesis.

Everything I tried inside the decomposition ended the same way — I would derive something that
looked like an improvement and it would turn out to be the same identity rearranged. Three of
those are written up in §6 so nobody repeats them.

## The Groemer observation

`../../problems/circle-packing-equilateral-triangle/attacks/eo-literature/` §3 left open whether
Groemer 1960 contains "a form of the same result Oler proved", and flagged that the README's
`sketch` table shows Groemer *slack* where Oler is tight. Applying Groemer's inequality to
$K=H\oplus B_1$ (the convex hull of the circles) and substituting Steiner's $F=A+M+\pi$,
$U=M+2\pi$ makes every $\pi$ cancel and yields Oler exactly. So: same inequality, applied to
different regions in the two places — which is what that file guessed. More importantly Groemer
*states an equality condition*, so Oler's equality characterisation is `cited` and the repo has
been treating it as missing (`oler-lower-bound` §5.2's (R2); most of `eo-oler-equality`).

Caveat I want on the record: only p. 285 and p. 294 of the Groemer scan have been read in this
repo. I am relying on a transcribed one-sentence equality clause. That is my least-certain step
and the first thing a cross-examiner should attack.

## Theorem E, and why it is not the answer

From the equality case: $\operatorname{def}(a,n)=0$ forces $P=T(a)$ *and* Oler-equality, hence
$T(a)$ tiled by unit triangles, hence $a\in\mathbb Z$ and $n$ triangular. Since $d(n)$ is
attained, $d(n)>a^*_n$ strictly for non-triangular $n$ — so $\varepsilon_k>0$ for every $k\ge2$,
including $k=7$. But the last step is a compactness contradiction with no modulus. Under K4 I
report it as non-explicit and the explicit $\varepsilon$ as $0$; the brief already classified
this as the $0^+$ that does not count, and it is right. What is new is that the $0^+$ costs
nothing — it does not need an equality theorem to be proved first.

## What I would do next, if this were continued

Not step 1. Either (a) a genuine stability theorem for Oler — "slack $<\varepsilon$ implies
Hausdorff-close to a lattice-tiled configuration", which is the only thing that converts Theorem
E into an explicit $\varepsilon$ — or (b) turn `eo-oler-equality` §7's N1 into a theorem
(certified 3-parameter search, piecewise-constant objective), which is the counting half that
(a) would then need. (a) is the hard half and I have no idea how to start it from Groemer's
statement alone; his proof pages are unread.
