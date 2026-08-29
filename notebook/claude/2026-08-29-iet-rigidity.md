# 2026-08-29 — exceptional-pair rigidity (idea I5)

Worker journal. `claude` (Claude Opus 5), branch `claude/inscribe-equilateral-triangle-oj15x1`.
Lane files: `problems/inscribed-equilateral-triangle/attacks/exceptional-pair-rigidity/`.
This is a journal: it records the order things happened, including the wrong turns and the
things I nearly reported too strongly. The claims live in the lane README, with statuses; nothing
here is assumable.

---

## Order of work

1. Read `RULES.md` §0/§3/§7 (and §1/§2/§5/§6 for the protocol), the problem `README.md` and its
   `RULES.md` in full, `attacks/ideation-round-1/README.md` §I5,
   `attacks/convex-vertex-criterion/README.md` in full, and the two experiment READMEs. Skimmed
   `attacks/spiral-tip-witness/README.md` §4 and §10 for the mixed-pair claim and the curve's
   definition.
2. Did the mathematics on paper, before writing anything and before running anything. This is where
   the whole lane came from and it took about half the session; see below.
3. Wrote `KILL-CRITERION.md`. **No code had been run at this point**, which the file says, together
   with the honest qualification that it does not precede all *thought* — I already believed the
   convex answer was "the pair is the diameter", so K1 is a weak bet and K2–K7 are the real ones.
4. Built the exact machinery: `q3.py` (arithmetic in $\mathbb{Q}(\sqrt3)$ with a hand-written sign
   algorithm), `decide.py` (decider 1: rotation + exact segment intersection), `geom.py`
   (simplicity, hull, exact "angle $< 60°$"), `sweep.py` (decider 2: direction-space sweep),
   `controls.py`, `census.py`, `climb.py`, `verify_ce.py`, `verify2.py`.
5. Controls first, census second, hill-climb third, verification of every counterexample last.
6. Wrote the lane README, then corrected three overstatements in it (below).

## The mathematics, in the order it actually arrived

**The first thing I tried was the wrong shape of question.** I started on "what convex shapes have
exactly two points of opening $< 60°$", which is the brief's question 1 read literally, and got a
useless answer within ten minutes: *every* triangle with two angles below $60°$ qualifies, and so
do lens-shaped bodies, so the family is huge and boring. The $30$–$30$–$120$ triangle is not
special as a shape. That could have been the lane's whole output and it would have been a thin one.

**The turn was to ask what the two points do to the *metric* rather than to the shape.** Writing
$d = |O_1O_2|$ and looking at a third point $Z$, the two cone conditions give
$\angle ZO_1O_2 \le 60°$ and $\angle ZO_2O_1 \le 60°$, hence $\angle O_1ZO_2 \ge 60°$, hence
$|O_1Z| \le d$ by "larger angle opposite longer side". So *every point is within $d$ of each of the
two*. That is one line and it is the whole engine.

**Then the law of cosines closed it, and the reason it closes is pretty.** For any $X,Y$ at
distances $a,b \le d$ from $O_1$ with $\angle XO_1Y \le 60°$,
$|XY|^2 = a^2+b^2-2ab\cos\gamma \le a^2+b^2-ab \le d^2$, because $\max(a^2+b^2-ab)$ on $[0,d]^2$ is
$d^2$ at the corners. So $\operatorname{diam} = d$. The step that needs $\gamma \le 60°$ is
$\cos\gamma \ge \tfrac12$, and the equality configuration $a=b=d$, $\gamma = 60°$ **is an
equilateral triangle of side $d$ inscribed in the set**. That coincidence — the failure case of the
diameter inequality is exactly an inscribed equilateral triangle — is what makes the uniqueness
statement (W2) work, and it is the moment I believed the lane had something.

**Realising the hypotheses were much weaker than convexity.** Having written the proof for a convex
body I noticed it never uses convexity: it uses only that two named points each see the whole set
inside a $60°$ cone. So W0/W1/W2 are statements about an arbitrary subset of the plane with budget
**none**, and convexity enters only later, to prove that on a convex curve *exceptional implies
blocked*. That reframing is the reason the lane has a falsifiable prediction to test on non-convex
polygons at all (§7.5), and it is the single best thing in the file.

**Re-deriving the convex criterion, and getting a shorter proof by accident.** `RULES.md` §3 means
I could not use `convex-vertex-criterion`'s Theorem B, so I re-derived it. Setting
$h(\theta) = r(\theta) - r(\theta-60°)$ on $(60°,\alpha)$, either $h$ vanishes (done by the IVT) or
it has constant sign, and each sign pushes the witness onto one of the two extreme rays via upper
semicontinuity. That is three cases decided by one sign, where the other lane has an $A/B/C$ split.
I wrote mine before re-reading theirs; when I did re-read, the conclusions matched exactly, so K2
did not fire. I record this as a cross-check and not as confirmation: two Opus workers agreeing is
worth very little (`RULES.md` §8).

## Where the computation changed my mind

I expected the polygon census to *support* a general rigidity statement. It did the opposite, and
the shape of the disagreement was informative.

- **Convex population: no exceptions at all.** $331/331$ pairs are the unique diameter pair,
  $1\,186/1\,186$ exceptional points are diameter endpoints, $10\,164$ convex vertices agree with
  my re-derived criterion. So the theorem is not wrong.
- **Non-convex population: exceptions, and I found them within the first 200 polygons.** One pair
  with $|O_1O_2| < \operatorname{diam}$. My first reaction was that the decider was broken — five
  checkers have failed in this session — so I built the second decider (direction space, different
  degeneracies) before believing anything, ran both on the fixture, and added a float direction
  sweep as a third instrument. All three agree, and the inequality $10018 < 10954$ is between
  integers. Then a targeted hunt found thirty more in four minutes, including a **five-vertex**
  integer pentagon, which is the version a reviewer can check by hand.
- **The counterexamples are all of one kind.** Every failing pair has at least one point that is
  *not* wedge-blocked. That is precisely what W1 requires, so the theorem's prediction survived the
  data that killed the conjecture. Sorting the $610$ pairs by blockedness and finding $537/537$
  both-blocked pairs on the diameter — on curves that are not convex — is the most reassuring number
  in the lane, and I only thought to compute it because the theorem had been stated with a
  hypothesis weaker than convexity.

**The surprise I did not expect and nearly under-reported:** about a quarter of the exceptional
points on non-convex polygons are not wedge-blocked at all, with hull openings up to $103.7°$.
Until now the repo's only non-wedge exceptional point was the transcendental spiral tip. These are
integer-coordinate and common. I think that is the most useful thing in this lane for whoever works
next, more than the rigidity theorem.

## Things I nearly got wrong, and one I did

1. **A false floor.** The first two censuses gave minimum ratio $\approx 0.95$ and I started
   drafting "there appears to be a floor near $0.95$". A ten-minute hill-climb took it to $0.724$.
   The "floor" was an artefact of sampling random polygons rather than searching for small ratios.
   Deleted before it reached the README; the README now says explicitly that I found no floor and
   that a plateau of a local search is evidence about the search.
2. **A non-reproducible seed.** `random.Random(SEED + hash(kind) % 1000)` — `hash` on a `str` is
   salted per process, so my first two census runs were not reproducible. Caught it when two runs
   of "the same" configuration gave different minima. Fixed to an explicit per-generator offset and
   re-ran everything; the numbers in the README are from the re-run.
3. **Three overstatements in the first draft of the README**, all fixed: (a) "every good verdict in
   the census is re-verified" — it is not, only the controls and the counterexamples are, and the
   README now states exactly which $287$ points were cross-checked by both deciders; (b) a garbled
   sentence about $1/\sqrt3$; (c) "every exceptional vertex had interior angle $<60°$, max
   $59.90°$" — the maximum was over the non-blocked subset only, and for blocked vertices the bound
   is automatic.
4. **An empirical regularity that is false.** Every exceptional point in the census is a hull
   vertex. I nearly wrote that down as a conjecture. The spiral tip refutes it — the curve meets
   every direction from its tip, so the tip is interior to the convex hull — and I re-derived that
   in two lines from the curve's *definition* rather than importing the other lane's theorem.

## Compute

About $50$ minutes total, inside the `RULES.md` §6.6 hour: controls (seconds), convex census
$46$s, star census $131$s, spiky census $122$s, targeted hunt $240$s, hill-climb $420 + 330$s,
verification runs a few minutes. Every stage wrote its records to JSON before printing. Two
background jobs were killed early by my own bad launch (`nohup ... &` inside a wrapper that exits);
noticed because the log files were empty, relaunched properly, nothing orphaned.

**Not committed.** All of it ran in a scratch directory: `experiments/` belongs to other workers on
this issue and `RULES.md` §2 forbids me writing there. So §7 of the lane README does *not* meet
`RULES.md` §4's one-command-reproducibility bar and says so. The three counterexample polygons are
printed in full in the README, which is the part that actually needs to be independently
re-decidable — and per the problem's `RULES.md` §3.3 the reviewer should re-decide them with their
own checker rather than rerun mine.

## What I would do next

1. **Characterise the non-wedge exceptional points on polygons.** They are common, exact, and
   nobody has looked at them. The question "what replaces the wedge test" is the real open problem
   this lane bumped into.
2. **Push the ratio down properly.** A better search (or a construction) would settle whether
   $|O_1O_2|/\operatorname{diam}$ has any positive floor at all for $|E| = 2$. My guess, worth
   little, is that it does not.
3. **Formalise W0 in Lean.** It is the law of cosines plus a maximum of $a^2+b^2-ab$ on a square;
   this problem's `RULES.md` §6.3 says elementary fragments are the best available Lean targets
   here, and W0 is more elementary than the wedge test it generalises.
