# Journal: round-2 cross-examination of three IET claims (2026-08-29)

Role: cross-examiner, same conversation as the three authoring lanes. Branch
`claude/inscribe-equilateral-triangle-oj15x1`. Output:
[`../../problems/inscribed-equilateral-triangle/attacks/round2-cross-review/README.md`](../../problems/inscribed-equilateral-triangle/attacks/round2-cross-review/README.md).

## Framing, read first

Same-model-family examination (Sonnet 5 examining Opus 5). Per `RULES.md` §5 and §8 this cannot
grant `verified:review` — that requires a different model *family*, and Codex was unavailable this
session. Everything below is due diligence, not promotion. I said this plainly in the deliverable
and am repeating it here so the record is unambiguous if this journal is read on its own.

Targets, in the priority order given: Theorem T
(`attacks/rectifiable-case/README.md`), the spiral-tip witness
(`attacks/spiral-tip-witness/README.md`), and the half-density lemma
(`attacks/half-density-obstruction/README.md`).

## Method

For each claim: restate it in my own words first; re-derive every step from definitions rather
than reading the proof and agreeing; attack the standard failure points (JCT applied to something
not shown Jordan, continuity claimed where it fails, nondegeneracy/limits, division by a possibly
zero quantity, the specific step each lane's own brief nominated as weakest); and, for the two
computational claims, re-implement the decision procedure from scratch (own `Fraction`-based
$\mathbb Q(\sqrt3)$ arithmetic, own rotation, own exact segment intersection, no `sympy` geometry
predicates per the standing warning) rather than rerunning the authors' code.

## Theorem T — outcome: survived

Restated it, then rebuilt the whole chain independently: the differentiability estimate and its
angle consequence ($\sin\theta\le1/3$, $\theta<\arcsin(1/3)\approx19.47°$); Lemma 0 (cone
confinement forces macroscopic triangles); Lemma 1 (localisation, pure compactness + injectivity,
no rectifiability used); Corollary 1.1's length bound $8/3\cdot\rho$; the Banach-indicatrix-style
partition inequality (re-derived from the $n$-piece oscillation argument plus Fatou, confirmed
exact, no hidden factor); Lemma 2's $\tfrac23\rho<\rho$ bound (re-derived the Markov-style step
$\int(m^+-1)\ge|\{m^+\ge2\}|$ and confirmed both $8/3$ and $2/3$); the $140°$ angular-separation
claim (re-derived from $\arcsin(1/3)$, got $[141.06°,218.94°]$, confirming the stated bounds with
margin); and Lemma 3 (no-nesting) — the step the lane itself nominated as weakest and asked to be
re-derived rather than read. I did exactly that, working from the bare statement, and landed on
the same case-split (nested case forces $\overline\Omega=\overline{\Omega'}$ hence $J=J'$,
contradiction; externally-tangent sub-case killed by an open positive-measure set at a boundary
point). Could not break any of it.

Specifically checked the dispatcher's requested item — consistency with the spiral-tip witness —
by direct computation rather than trusting either lane: the spiral's chord/arc ratio
$c/\sqrt{1+c^2}$ is a genuine constant strictly less than 1 for every $c>0$, which is stronger than
merely failing to converge to 1 and rules out unit-speed differentiability at the tip outright. So
Theorem T's hypothesis never fires at the spiral tip, and Corollary T3 is not violated. No
collision; confirmed independently.

Found one purely cosmetic gap (not a mathematical error): the file never states that $\delta$ from
differentiability should be shrunk below $L/4$ to keep the parameter window
$(t_0-\delta,t_0+\delta)$ from wrapping around $\mathbb R/L\mathbb Z$ in Lemma 1's compactness
argument. Trivially repaired by using $\min(\delta,L/4)$; (1) holds a fortiori for any smaller
$\delta$. Recorded in the deliverable as a non-load-bearing note, not an objection.

Not checked: the general area-formula fact "$\mathcal H^1(\gamma(A))=|A|$ for injective
arclength-parametrised curves" — standard real analysis, used correctly, but I treated it as
citable rather than re-deriving it from first principles (as the file itself does — it flags this
as removable and not load-bearing for Theorem T proper, only for Corollary T1's a.e. statement).

## Spiral-tip witness — outcome: survived

Re-derived injectivity/Jordanness from the bare definition of $J$ (strict monotonicity of
$e^{-ct}$ forces one point per circle per arm; the two arms differ by exactly $\beta\ne0$ at every
shared radius; the closing arc $B$ lives only at modulus 1, where the arms contribute exactly their
own endpoints) rather than reading the file's homeomorphism argument first. Re-derived the length
integral and got $2\sqrt{1+c^2}/c+\beta$ exactly. Re-derived the chord/arc ratio and got
$c/\sqrt{1+c^2}$ exactly, matching. Checked the universal-cover/shear argument for the interior
(§4.3): confirmed the shear map is a genuine homeomorphism and that the two candidate exterior
pieces actually overlap, which is what licenses invoking JCT correctly (on a curve already shown
Jordan by other means, not smuggled). Re-derived Theorem 1 and the sharpness-at-$\beta=60°$
computation exactly.

Attempted breaks: missing pairing in the disjointness table (none found — $B$'s modulus-1
restriction rules it out structurally); periodicity exploit on a single winding arm (none — radial
coordinate alone determines the parameter by strict monotonicity, and direction is an unbounded,
not mod-360, function of it); rectifiability failing near the tip due to infinite winding (ruled
out — convergence is purely from the exponential radial decay, independent of angular winding; I
also checked the contrast case $\theta(r)=1/r$ genuinely fails rectifiability, confirming §12.1's
claim that rectifiability is a property of the choice and not the mechanism).

Not checked: §10's spiral-similarity corollary (the file's own least-checked line) and the
numerical corner-angle census — both explicitly non-load-bearing for the three headline theorems.

## Half-density obstruction — outcome: survived, plus independent computational confirmation

Re-derived Lemma H (two lines, isometry + measure, no topology) and the sharpness claim
($\sup=\frac12$, not $\frac16$) via the $C_6$ independent-set framing, working it out myself before
reading the file's version, then cross-checked the "angle-blind" claim by independently redoing the
$90°/C_4$ case ($\alpha(C_4)=2\Rightarrow\frac24=\frac12$, not $\frac14$). Re-derived Lemma H'
(strict form via connectedness of the punctured ball) and confirmed it. Re-derived Lemma A
completely independently — this is the same theorem as Theorem T's Lemma 3, and I proved it a
second time from scratch in this file's closure-based notation rather than treating my first
derivation as covering it; it holds.

Then did a genuine independent re-implementation of the pinwheel witness (§6), the most
computationally loaded claim in the batch: rebuilt the 21-vertex polygon from the file's own
generating recipe using nothing but `fractions.Fraction`, wrote my own shoelace area, my own
orientation-sign simplicity test, my own point-to-segment distance, and my own from-scratch
$\mathbb Q(\sqrt3)$ decider (own `E` class for $a+b\sqrt3$, own `rot60`, own exact segment
intersection) — sharing no code with the author. Results: area $=1723/1000$ exactly, matching;
$\varepsilon^2=4/125$ exactly, matching; angle at $O<60°$, matching; and searching from scratch for
equilateral witnesses at $O$ turned up 80 verified triangles, the first of which is *algebraically
identical* to the one the file reports
($Q=(-\tfrac3{13}+\tfrac9{13}\sqrt3,0)$,
$X=(-\tfrac3{26}+\tfrac9{26}\sqrt3,\tfrac{27}{26}-\tfrac3{26}\sqrt3)$,
side$^2=\tfrac{252}{169}-\tfrac{54}{169}\sqrt3$). Scripts are in scratch, not committed anywhere
(this lane owns no `experiments/` directory and I was not asked to add one); the working files were
`/tmp/verify_pinwheel.py` and `/tmp/verify_pinwheel2.py` on the machine of record, reproducible
from the vertex-generating recipe quoted in the deliverable.

This is the strongest single piece of evidence in this review: an independently-written decider,
sharing no code with the author, landing on the exact same witness triangle. It directly discharges
kill-criterion K4 myself rather than accepting the file's claim that it did.

Attempted breaks: hunted for a convex counterexample to §7's vacuity proposition (none — basic
convex geometry, a supporting line always exists); hunted for a closed set achieving equality in
Lemma H' (none — the connectedness argument forbids it structurally, not just numerically).

Not checked in full: the illustrative $C\not\Rightarrow D$ counterexample domain of §5.3 — I
recomputed its claimed density ($0.1228$) and it matches, but did not verify it corresponds to an
actual Jordan curve boundary rather than an abstractly-defined region. Explicitly non-load-bearing
(illustrative only, not one of the three headline results).

## Overall

All three claims survive an honest, adversarial, independent reconstruction — including, in two
cases, a from-scratch computational re-verification that reproduced the authors' exact witnesses.
I looked hard for the kind of smuggled regularity, JCT misuse, or hidden-constant error this
problem's `RULES.md` warns is the dominant failure mode here, and did not find one. All three stay
`sketch` per repo policy: this is not the cross-family review §5 requires, and I said so at the top
of the deliverable and again here. The next useful step is a genuine Codex (or human) review of
these same three files, ideally starting from Theorem T's Lemma 3 and the half-density lane's
pinwheel witness, since those are now the two pieces of this batch with the most independent
scrutiny already on record.
