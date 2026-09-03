# 2026-09-02 — Woodall $\tau = 2$: red team (issue #153)

Adversary side of pair C. C1 is issue #152. Full report:
`problems/woodalls-conjecture/attacks/tau2-redteam/README.md`.
Code: `experiments/woodall-tau2-redteam/`.

## Outcome

**No error found in either $\tau = 2$ argument.** That is a negative result and I
want it on the record as one, together with exactly what it is based on, because
"I looked and it seemed fine" is worth nothing here (RULES §0).

What I actually did, in order:

1. Built dicut/dijoin/$\tau$ machinery from the definitions, not from any
   existing repo code — so that a shared encoding bug would surface as a
   disagreement rather than as agreement. Validated on the four fixtures problem
   RULES §4 demands (path, directed cycle with **zero** dicuts, diamond,
   near-miss DAG) plus three more.
2. Derived the reformulation *two disjoint dijoins $\iff$ the dicut hypergraph is
   2-colourable*, which made the exact decision cheap and let me attack lemmas
   rather than only theorems. Solver validated on triangle / 4-cycle / 5-cycle /
   Fano.
3. Reconstructed the $\tau = 2$ argument myself before reading C1's, including a
   self-contained ear-decomposition proof of the Robbins input so that step is
   not a black box. Landed in the same place.
4. Exhaustive: all $3^{12}$ multi-digraphs on 4 vertices, all $2^{20}$ simple
   digraphs on 5, plus 300k random 5-vertex multi-digraphs. 234k instances with
   $\tau = 2$. Checked the theorem *and* the construction (independent DFS
   Robbins orientation + agreement colouring) separately. **0 failures.**
5. Tried to reconstruct Schrijver's Edmonds–Giles counterexample. **Failed** —
   every primary and secondary host is egress-blocked. I did not write down a
   digraph from memory and call it Schrijver's.
6. When C1 pushed, transcribed C1's Theorem R from its *prose* and re-ran C1's
   lemmas on 42772 instances with my machinery. **0 failures.** Rebuilt C1's
   §6.2 demonstration instance detail by detail: every claim confirmed.

## The two things I derived that I did not expect

**Proposition R1 (mine).** No $\{0,1\}$-weighted counterexample has $|S| = 3$.
Dicut shores are the nonempty proper down-sets of the condensation poset; two
distinct minimal elements would already force $|S| \ge 4$, so source and sink are
unique, so some special arc runs $m \to M$ and is present in every cut that
contains any other $m$-tailed special — killing the triangle of traces.

**Proposition R2 (mine).** Along a single maximal chain of down-sets, each
special arc is "on" for an interval, so the traces form an interval hypergraph,
which is 2-colourable whenever all edges have size $\ge 2$. So the obstruction
must combine *incomparable* poset elements. This is why the crown/6-cycle
candidate suggested by the literature snippets gives an **even** trace cycle and
is not itself a counterexample, and it is a structural reason weight-0 arcs are
necessary rather than incidental.

Neither proposition is needed by anyone else's proof; they are search-space
constraints and they explain why my exhaustive sweep over **all** simple DAGs on
$\le 6$ vertices (118166 minimal admissible supports) came back empty, matching
`zero-weight-frontier`'s $\ge 7$-vertex floor.

## The finding that matters

Both arguments discharge the Schrijver filter at the same place — the
colouring-to-packing step — and I confirmed by re-derivation that this is the
*first* place anything fails: Lemma A, Robbins and the crossing lemma are all
weight-blind and survive verbatim.

But that has a sharp consequence, which I derived **before** reading C1 and then
found C1 asserting too: **the argument is a correct proof of Edmonds–Giles for
strictly positive weights at $\tau_w \ge 2$.** I tested the prediction on
1605210 strictly-positive-weight instances with $\tau_w = 2$ — zero without a
packing.

So the whole force of the filter reduces to one external fact: *Schrijver's
instance uses weight-0 arcs.* If it did not, both proofs would be refuted
outright. That fact is currently sourced to a web-search snippet, because nobody
in this repo can open the paper. That is the single load-bearing unverified
input, and it is why I would not promote either file even if I were allowed to.

## Status discipline

I grant nothing. Issue #153 withholds `verified:review` from me. Worth noting
for whoever picks this up: the `tau2-robbins` file was written by **codex**
(`Flow-25`), so a claude review of *that* file is cross-family under RULES §5 —
but C1's `tau2-complete` is claude's own, so same-family, and in any case my
`not-checked` list (Schrijver's instance) is disqualifying on its own. Both stay
`sketch`.

Defects recorded: four against `tau2-robbins` (§6 of the report — the worst is
that Lemma A mixes two incompatible empty-dicut conventions and is false as
stated under the one the repo's code uses; C1 **fixed** this), and three against
C1 (§7.5 — a claimed equivalence with one direction admittedly unproved, an
under-flagged contingency in the filter, and a prior-art attribution gap on the
positive-weight reduction, which `zero-weight-frontier` §1C already had).

## Kill criterion

Issue #153 says: if C1 marks its approach `refuted`, switch to confirming the
refutation. C1 did not; it discharged all three filters and kept the approach.
I independently agree with that decision — the filter analysis is sound, subject
to the contingency above.

## Budget

~1.5h. Three background searches killed at the checkpoint when the coordinator
reassigned instance-hunting to #156.
