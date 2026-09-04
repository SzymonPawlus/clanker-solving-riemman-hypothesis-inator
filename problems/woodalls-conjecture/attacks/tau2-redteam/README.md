# Red team report on the $\tau = 2$ argument

status: sketch (this file is a *review artifact*, not a mathematical claim;
the computational parts below are `numerical`)

reviewed-objects:
  1. `attacks/tau2-complete/README.md` on `claude/152-tau2-complete` at commit
     `f69bd44` (agent C1, **claude**, status `sketch`) — the issue #152 target.
  2. `attacks/tau2-robbins/README.md` on `main` at commit `2a49966`
     (authored by **codex**/`Flow-25`, status `sketch`) — the file C1 supersedes,
     and the only $\tau = 2$ argument available for most of my budget.

reviewer: Claude Opus 5, agent `claude`, worker on issue #153, worktree
`/home/user/wt/153-tau2-redteam`, branch `claude/153-tau2-redteam`.

**This file grants no status to anything.** See §8 for why, and for the exact
list of what I did and did not check.

**Verdict in one line.** I found no error in either $\tau = 2$ argument, and I
tried hard to: I reconstructed both independently, reimplemented both
constructions, and ran ~2.5M instances against them without a single failure.
C1's proof is correct as far as I can check it, and its Schrijver-filter
discharge is **genuine but contingent** on one unverified external fact
(§7.5). Four presentational defects in the older `tau2-robbins` file are in §6;
three criticisms of C1 are in §7.5. Both files must stay `sketch`.

---

## 0. What I was asked and what actually happened

Issue #153 is the adversary side of a pair: agent C1 (issue #152) writes a
$\tau = 2$ proof, I try to break it. C1 had not pushed for most of my budget, so
I did §§1–4 below with no access to C1's work at all — machinery, an independent
reconstruction of the argument, exhaustive checks, and my own attempt at
Schrijver's counterexample. C1's branch `claude/152-tau2-complete` (commit
`f69bd44`, `attacks/tau2-complete/README.md`, 606 lines) appeared late and §7
below is my attack on it. Because I derived my reference point first, §7 is a
comparison of two independent derivations rather than a read-along.

Both objects are covered: `attacks/tau2-robbins/` (on `main`, author **codex**)
in §§5–6, and C1's `attacks/tau2-complete/` in §7.

I could not reach any primary source. `ir.cwi.nl`, `arxiv.org`,
`www.ime.usp.br` and `dspacemainprd01.lib.uwaterloo.ca` are all refused by this
sandbox's egress proxy. **I therefore did not read Schrijver 1980, and I did
not reconstruct Schrijver's counterexample.** What I did instead is in §4, and
the consequences for my verdict are in §5 and §7.

---

## 1. Machinery, built from the definitions and validated

`experiments/woodall-tau2-redteam/` is a fresh implementation; I did not read or
reuse any existing dicut code in this repo, precisely so that a shared encoding
bug would show up as a disagreement rather than as agreement.

Definitions I implemented (restated in my own words, per problem `RULES.md` §4):
for $U \subseteq V$, $\delta^+(U)$ are the arcs with tail in $U$ and head
outside; $U$ is a **dicut shore** iff $U$ is nonempty, $U \ne V$,
$\delta^-(U) = \varnothing$, and $\delta^+(U) \ne \varnothing$. Arcs are
identified by *index*, so parallel arcs are distinct objects. $\tau$ is the
minimum size of a dicut.

Fixture results (`validate.py`, all PASS):

| fixture | arcs | #dicuts | $\tau$ | two disjoint dijoins |
|---|---|---|---|---|
| directed path $s\to v\to t$ | 2 | 2 | 1 | no |
| directed 3-cycle | 3 | **0** | $\infty$ | vacuous |
| diamond | 4 | 4 | 2 | yes |
| near-miss DAG $s_1\to t_1, s_2\to t_1, s_2\to t_2$ | 3 | 6 | 1 | no |
| doubled $s_1\to t\leftarrow s_2$ | 4 | 3 | 2 | yes |
| single arc | 1 | 1 | 1 | no |
| two parallel arcs | 2 | 1 | 2 | yes |

The directed cycle having **zero** dicuts is the check that the implementation
uses $\delta^-(U) = \varnothing$ and not merely $\delta^+(U) \ne \varnothing$.

### A reformulation I derived and then used as the exact decision procedure

> $A$ splits into two disjoint dijoins $\iff$ the hypergraph of dicuts is
> 2-colourable (no dicut monochromatic).

Two disjoint dijoins can always be grown to a *partition*, because a superset of
a dijoin is a dijoin; so partitions lose no generality. Only inclusion-minimal
dicuts matter. This turns the exact decision into hypergraph 2-colouring, which
I solved by backtracking (`twocol.py`), validated on triangle (not 2-colourable),
4-cycle (2-colourable), 5-cycle (not), Fano plane (not).

---

## 2. The argument, reconstructed rather than read

I re-derived the proof rather than following the sketch's prose, and I landed in
the same place. My reconstruction:

**Step A.** If $\tau(D) = 2$ then the underlying multigraph $G$ has no bridge.
Suppose exactly one edge crosses the vertex bipartition $(U, V \setminus U)$. Its
arc either leaves $U$ — then $\delta^-(U) = \varnothing$ and $\delta^+(U)$ is a
one-arc dicut — or enters $U$ — then $\delta^-(V\setminus U) = \varnothing$ and
$\delta^+(V \setminus U)$ is a one-arc dicut. Either contradicts $\tau = 2$.

**Step B.** Every connected component $H$ of $G$ is bridgeless. *This is the step
I expected to be a gap and it is not*: the cut in Step A is taken in $D$, not in
$H$, and no arcs run between components, so a bridge of $H$ is a one-edge cut of
$D$ and Step A applies verbatim. In particular a component carrying **no** dicut
of $D$ is still covered. (Independently: such a component is strongly connected,
and a strongly connected digraph cannot have a bridge, since strong connectivity
forces arcs both ways across every cut.)

**Step C (Robbins).** A connected bridgeless multigraph has a strongly connected
orientation. I did not want this as a black box, so I proved the case I need
myself: connected + bridgeless = 2-edge-connected, which has a closed-ear
decomposition $C_0, P_1, \dots, P_k$; orient $C_0$ cyclically and each ear as a
directed path between its endpoints; by induction on $k$ the result is strongly
connected, since each new ear's internal vertices can reach and be reached from
the already-strong part through the ear's two endpoints.

**Step D.** Fix such an orientation $O$ per component. Colour a $D$-arc $J_+$ if
its own direction agrees with $O$ on its edge, $J_-$ otherwise; loops anywhere.

**Step E.** Let $C = \delta^+(U) \ne \varnothing$ be a dicut. Some component $H$
meets both $U$ and its complement. $O$ restricted to $H$ is strongly connected,
so some edge crosses out of $U \cap V(H)$ and some edge crosses into it. The
out-directed one corresponds to a $D$-arc leaving $U$ (all crossing arcs leave
$U$, because $\delta^-(U) = \varnothing$), so it agrees with $O$: it is in
$C \cap J_+$. The in-directed one corresponds to a $D$-arc that *still leaves*
$U$, so it disagrees with $O$: it is in $C \cap J_-$. Hence every dicut is
bichromatic. $\square$

I could follow every step. The pivot is the single sentence in Step E — the
$D$-arc under an $O$-edge pointing *into* $U$ points *out of* $U$ — and it is
exactly where confusing a general directed cut with a dicut would break the
proof. The sketch flags this as its own weakest point, correctly.

---

## 3. Computational attack on the theorem *and* on the construction

I attacked the construction, not only the conclusion: an argument can reach a
true theorem by a method that does not actually work. So for every instance I
checked five things separately — the theorem (T), Lemma 1 (L1), bridgelessness
per component (L1c), strong connectivity of an independently implemented DFS
Robbins orientation (R), and whether the agreement/disagreement colouring built
from *that* orientation really yields two dijoins (C).

Search spaces stated exactly, no isomorphism reduction, loops excluded:

| space | size | instances with $\tau = 2$ | failures of T/L1/L1c/R/C |
|---|---|---|---|
| all digraphs on 4 labelled vertices, every ordered pair with multiplicity $0,1,2$ | $3^{12} = 531441$ | 31082 (480 weakly disconnected) | **0** |
| all simple digraphs on 5 labelled vertices | $2^{20} = 1048576$ | 181070 (4590 disconnected) | **0** |
| 300000 random multi-digraphs on 5 vertices, multiplicities $0..3$, seed 20260902 | 300000 | 22363 (388 disconnected) | **0** |

Parallel arcs are included deliberately: they are what makes $\tau = 2$ reachable
on tiny vertex sets, and they are the case the weighted reduction turns on.

This is `numerical` evidence and proves nothing universally, but it does mean
that if the construction is broken, it is not broken by anything visible below
six vertices.

---

## 4. Schrijver / Edmonds–Giles: what I could and could not do

### 4.1 The statement I worked with

I could not read Schrijver 1980. I reconstructed the target from the definitions:
in the $0/1$-weighted Edmonds–Giles setting, write $S \subseteq A$ for the
weight-one arcs. Then $\tau_w = \min_C |C \cap S|$, and a $w$-packing of two
dijoins is exactly **two disjoint dijoins both contained in $S$**. A
counterexample at $\tau_w = 2$ is a pair $(D, S)$ with every dicut meeting $S$ at
least twice and $\{C \cap S\}$ not 2-colourable.

### 4.2 I did not find one. Here is exactly how hard I looked.

- **Exhaustive, complete.** For a fixed $D$, if an admissible $S$ is not
  2-colourable then neither is any admissible $S' \subseteq S$ (a colouring of
  $S'$ extends to $S$, and each trace $C \cap S \supseteq C \cap S'$ is then
  bichromatic). So testing the *minimal* admissible supports is complete. I
  enumerated them exactly over **all $2^{n(n-1)/2}$ labelled DAGs** for
  $n = 4, 5, 6$ — every DAG on $n$ labelled vertices up to relabelling, since
  the condensation reduction lets me restrict to DAGs. Result: 22 / 1021 /
  118166 minimal admissible supports tested, **0 counterexamples**. An $n = 7$
  sweep was launched and did not finish inside budget.
- **Randomised.** ~40000 random DAGs on 7–12 vertices, minimal supports by
  randomised greedy shrinking, 60 restarts each. **0 counterexamples.**

### 4.3 Two structural facts I proved along the way

These explain the empty search and constrain where Schrijver's example can live.

**Proposition R1 (mine).** *No counterexample has $|S| = 3$.*
Dicut shores are exactly the nonempty proper down-sets of the condensation
poset, and for connected $D$ every such down-set gives a dicut. If the poset had
two distinct minimal elements $m_1 \ne m_2$, the down-sets $\{m_1\}, \{m_2\}$
would each need $\ge 2$ special arcs leaving them, with disjoint tails, forcing
$|S| \ge 4$; so the minimal element $m$ is unique, and dually the maximal
element $M$ is unique, whence every element is $\le M$ and no proper down-set
contains $M$. Now $\ge 2$ specials leave $m$ and $\ge 2$ specials enter $M$; with
$|S| = 3$ these two pairs share an arc, i.e. some special $b = (m, M)$. But then
for any shore $U$, any other special $a$ with tail $m$ satisfies
$a \in \delta^+(U) \Rightarrow m \in U$, and $M \notin U$ always, so
$b \in \delta^+(U)$ too. So $a$ never appears without $b$, and the three pairwise
traces needed for a triangle cannot all occur. $\square$

**Proposition R2 (mine).** *A single maximal chain of down-sets can never
produce the obstruction.* Along a maximal chain (a linear extension), a special
arc $x = (t,h)$ lies in the cut exactly for the steps between the insertion of
$t$ and of $h$ — an interval. So the traces along one chain form an interval
hypergraph, and an interval hypergraph with all edges of size $\ge 2$ is
2-colourable (alternate colours left to right). Hence any counterexample's
obstruction must combine *incomparable* elements of the poset; it is genuinely
two-dimensional. $\square$

Consistent with R2 and with the secondary sources: a web search (I could not
open the papers themselves) reports that Schrijver's counterexample has weight-0
"dashed" arcs and contains a chordless 6-cycle. I checked the natural candidate
suggested by that hint — the crown/6-cycle DAG $u_i \to v_j$ with three sources
and three sinks — and its trace graph is a **6-cycle**, i.e. even, hence
2-colourable: not a counterexample on its own. More generally, when every source
and sink has exactly two special arcs the trace graph is an even cycle, so
weight-zero arcs are *structurally necessary*, not incidental.

### 4.4 What I could not do because of 4.2

**I could not run the sketch's steps one by one against Schrijver's
counterexample.** That was the assignment's primary weapon and I did not fire
it. §5 says what I substituted and how much weaker it is.

---

## 5. The three mandatory filters

### 5.1 Schrijver filter — the discharge is correctly *located*, but thin, and it rests on a citation I could not check

The sketch says: Lemma 1 survives weighting, and the unique step that needs
unweightedness is the declaration that $J_+, J_-$ is a *packing*. I re-derived
this and agree with the location:

- Lemma 1 survives. After the parallel-copies reduction all weights are $0/1$; a
  bridge gives a one-arc dicut of weight $\le 1 < 2$. So $G$ — the multigraph of
  **all** arcs, weight-zero ones included — is still bridgeless.
- Robbins, Lemma 2, and the colouring never mention weights, so they survive
  verbatim.
- The packing constraint is $\chi^{J_+} + \chi^{J_-} \le w$. The construction
  colours *every* arc, so it uses each arc exactly once, which violates $w(a)=0$.
  This is the only failure, and it is a genuine one: one cannot simply delete the
  weight-zero arcs, because their directions are part of what makes a cut a
  dicut.

**Sharpness check I ran, which the sketch does not state.** That diagnosis has a
falsifiable consequence: if $w \ge 1$ everywhere and $\tau_w = 2$, the argument
should go through and a $w$-packing of two dijoins should exist. I tested this
directly (`weighted_check.py`) by expanding each arc into $w(a)$ parallel unit
copies and asking for two disjoint dijoins in the expansion; this also tests the
reduction step, which is otherwise taken on citation. Result: **1605210
strictly-positive-weight instances with $\tau_w = 2$ — 194702 exhaustive on
$n = 4$ over every weight vector in $\{1,2,3\}^A$, and 1410508 on $n = 5$ with 40
random weight vectors per digraph, seed 4242 — and not one of them lacked a
$w$-packing of two dijoins.** The prediction holds.

**So the argument does prove weighted $\tau_w = 2$ for strictly positive
weights.** The whole force of the filter therefore reduces to one external fact:
*Schrijver's counterexample must use weight-zero arcs.* Secondary sources say it
does ("the dashed edges have weight 0"). I could not confirm this from the
primary source. **If Schrijver's counterexample had all weights $\ge 1$, the
sketch would be refuted outright.** That is the single point on which the
sketch's Schrijver discharge stands or falls, and it is currently `cited` to a
paper nobody in this repo has been able to open from inside the sandbox.

My verdict: the discharge is **genuine but contingent**. It identifies a real
step that fails under weights, in the right place, for the right reason. It is
not a hand-wave. But it is the *last* line of the proof, so the argument comes as
close to Edmonds–Giles as it is possible to come without proving it, and that
should be treated as a reason for more scrutiny of the citation, not less.

### 5.2 Lucchesi–Younger filter — passes, independently confirmed

I reconstructed the entire proof and its only external input is Robbins's
orientation theorem, which is a statement about *undirected* graphs and cannot
encode a dicut/dijoin min-max. To close the "laundered through an obvious lemma"
route I checked each lemma individually: Lemma 1 is a one-edge-cut argument,
Lemma 2 is a two-path argument inside a strongly connected digraph. Neither
mentions dijoins at all, so neither can be smuggling in "min dijoin = max
disjoint dicuts". I also proved Robbins myself (§2, Step C) so that the one
citation is not load-bearing either. **No circularity.**

### 5.3 Easy-direction filter — passes, and I verified the construction, not just the claim

The argument exhibits $J_+$ and $J_-$ explicitly. I reimplemented the
construction independently (DFS orientation, then agreement/disagreement
colouring) and verified on 731k+ digraphs (§3) that both output sets really are
dijoins. This is the existence direction; it is not a restatement of
$\le \tau$.

---

## 6. Defects found in `tau2-robbins` (the older file on `main`)

No error that breaks the theorem. Four real defects, in decreasing severity:

1. **The Schrijver discharge is load-bearing on an unverified citation** (§5.1).
   The sketch does not flag that its filter passes *only* because Schrijver's
   example has weight-zero arcs, and does not record that consequence as a
   checkable prediction. It should state explicitly: "this argument proves the
   weighted statement for $w \ge 1$; the filter passes only because Schrijver's
   example has zeros."
2. **Lemma 1 mixes two incompatible conventions inside one document.** It
   concludes "$G$ is connected as well and hence is 2-edge-connected" *under the
   convention that the empty directed cut is a dicut*. But under that convention
   no dijoin exists at all (nothing meets $\varnothing$), so the theorem is
   about a different object; and under the convention actually used by the rest
   of this repo's code — dicuts are nonempty — the conclusion "$G$ is connected"
   is **false**. I found 480 weakly disconnected $\tau=2$ digraphs at $n=4$ and
   4590 at $n=5$. The main proof does handle these component-wise, so this is a
   statement defect, not a mathematical error, but Lemma 1 as written is not
   true as stated under the operative convention and should be restated.
3. **Citation discrepancy.** The sketch cites Schrijver 1980 as *Discrete Math.*
   **32** (1980) **213–214** at `ir.cwi.nl/pub/9906/9906D.pdf`; the problem
   `README.md` cites the same paper as **213–215**. One of them is wrong. I could
   not adjudicate — egress blocked.
4. **An unstated step in Lemma 1's scope.** The proof applies Robbins to *every*
   nontrivial component, but Lemma 1 as phrased is naturally read as constraining
   only components that carry a dicut. It does in fact cover all of them, because
   the one-edge cut is taken in $D$; that sentence is missing and should be
   added. I verified this closes (§2, Step B) — it is a presentation gap, not a
   hole.

---

## 7. Attack on C1's write-up (`attacks/tau2-complete`, commit `f69bd44`)

I reconstructed §§1–4 of this file before C1's branch existed, so my derivation
in §2 above is genuinely independent of C1's §5. **The two derivations agree.**

### 7.1 C1's three self-declared weak points — all three survive

C1 names W1 (the blue witness in its §5.4), W2 (Theorem R Case 2, parallel edges
and $z = u$), W3 (Proposition 4.1(i)). I re-derived each rather than reading it.

**W1 survives.** I chased the endpoint bookkeeping symbol by symbol. Lemma B
gives an edge $e_b$ with $O(e_b) = (p,q)$, $p \notin U$, $q \in U$. It has exactly
one end in $U$, so by C1's (★) it comes from an arc $b \in C$ with $t(b) \in U$,
$h(b) \notin U$. The end of $e_b$ in $U$ is unique ($p \notin U$), and $t(b) \in U$,
so $t(b) = q$ and $h(b) = p$; hence $O(e_b) = (h(b), t(b))$, the reverse of $b$,
so $b$ is blue. Correct. The pivot really is "the arc still leaves $U$ because
$\delta^-(U) = \varnothing$", and C1 has it right.

**W2 survives, including both corner cases.** I transcribed C1's Theorem R
procedure from its *prose* (not from its code) into `attack_c1.py::robbins_C1`
and ran it. On the two corner cases C1 worries about: if $z = u$ the construction
orients $e$ as $u \to v$ and $P'$ as $v \to \cdots \to u$, closing a directed
cycle — still strongly connected, no problem. Parallel edges: for two parallel
copies of $\{u,v\}$ the path $P$ in $G - e$ can be the twin edge itself, giving
$z = u$ and orienting the two copies oppositely, which is exactly right. The
invariant argument is also sound: every vertex of $P'$ except $z$ is outside $X$,
so every edge of $P'$ has an end outside $X$ and by (I1) is not in $F$.

**W3 survives.** Prop 4.1(i): $i \ge 1$ because $v_0 = y \notin U$, and
$v_{i-1} \to v_i$ has tail outside and head inside $U$, so it is in $\delta^-(U)$
and not $\delta^+(U)$. Correct as written.

### 7.2 Computational attack on C1's lemmas, using my machinery not C1's

`attack_c1.py`, run on 42772 random multidigraphs on 3–6 vertices with
$\tau \ge 2$ (parallel, antiparallel arcs, loops and cycles all included; seed
153153). C1's `tau2lib` is not imported anywhere.

| target | what was checked | failures |
|---|---|---|
| Prop. 4.1(iii) | condensation has the same dicuts *as arc sets* and the same $\tau$ | **0** |
| Theorem R (W2) | C1's procedure returns a strongly connected orientation, all edges oriented | **0** |
| Construction (W1) | agreement colouring from *that* orientation gives two dijoins | **0** |
| Theorem | two disjoint dijoins exist at all | **0** |

**A probe aimed specifically at Lemma A**, which is the only place C1 uses
$\tau \ge 2$. C1 counts the empty set as a dicut, so $\tau \ge 2$ forces weak
connectedness; my checker does *not* count it, so under my convention a weakly
disconnected digraph can have $\tau \ge 2$ and Lemma A's *connectivity* half
fails. The question that matters is whether the *bridgeless* half survives the
convention change, since that is what Theorem R needs. Over 85664 instances with
$\tau \ge 2$ under my convention: 636 weakly disconnected, and **0 that are
connected and have a bridge**. So Lemma A's load-bearing half is convention-proof,
and C1's §3 per-component paragraph correctly covers the rest. This is exactly
the defect I recorded against `tau2-robbins` in §6.2 below, and **C1 has fixed
it** — the conventions are stated up front and discharged.

### 7.3 C1's §6.2 mechanical demonstration — every detail confirmed

C1 exhibits the diamond plus a weight-0 arc $x \to y$ and claims the colouring
step fails on it. I rebuilt it in `check_c1_62.py`. Confirmed, item by item:
dicut shores are exactly $\{s\}, \{s,x\}, \{s,x,y\}$; $\{s,y\}$ is *not* a shore
($x\to y$ enters it); $\tau_w = 2$; C1's stated $O$ is strongly connected; the
colouring is red $=\{sx, yt, xy\}$, blue $=\{sy, xt\}$;
$\delta^+(\{s,x\}) = \{sy, xt, xy\}$; the only red arc in it is the weight-0 arc
$xy$, so $J_1 \cap S$ **misses** that dicut. And a $w$-packing nevertheless exists
on this instance, so it demonstrates the *step* failing and not the *statement* —
exactly as C1 says.

### 7.4 C1's sharpest claim, which I derived independently before reading it

C1 asserts: *the proof is a correct proof of Edmonds–Giles for strictly positive
weights at $\tau_w \ge 2$*, so weight $0$ is the exact boundary. I reached the
same statement on my own (§5.1 above, written before C1's branch was fetchable)
and tested it: **1605210 strictly-positive-weight instances with $\tau_w = 2$
(194702 exhaustive on $n=4$ over all of $\{1,2,3\}^A$, 1410508 on $n=5$), zero
without a $w$-packing.** Two independent derivations plus 1.6M instances. I
believe the claim is correct.

Two caveats C1 should carry:
- **It is not new.** `attacks/zero-weight-frontier` §1C already derives exactly
  this reduction ("the positive-weight version is *exactly* the unweighted
  conjecture on multidigraphs"). C1 cites that file for its census but not for
  this reduction. Attribution gap, not an error.
- It makes the Schrijver filter's discharge *contingent*: see §7.5.

### 7.5 Where I push back

No error that breaks anything. Three genuine criticisms:

1. **A claimed equivalence with one direction admittedly unproved.** In §6.2,
   third repair bullet, C1 writes that existence of an "$S$-witnessed strong
   orientation" for all instances "is *equivalent* to the weighted statement at
   $\tau_w = 2$", then concedes in the same parenthesis that the converse
   direction "is not needed for the point being made" — i.e. it is not proved.
   The direction C1 actually *uses* (an $S$-witnessed $O$ yields a packing,
   hence no packing implies no such $O$) is sound; I re-derived it. But a
   one-directional implication should not be written as an equivalence.
2. **The Schrijver discharge is genuine but contingent, and C1 could say so more
   loudly.** By §7.4 the argument proves the weighted statement whenever
   $w \ge 1$. So the *entire* force of the filter reduces to one external fact:
   Schrijver's instance uses weight-0 arcs. C1 flags this as gap G2 and does not
   transcribe the instance, which is the right call. But the consequence deserves
   a sentence in the filter section itself: **if Schrijver's counterexample had
   all weights $\ge 1$, this proof would be refuted outright.** That is the single
   load-bearing external fact in the whole document, and it is sourced to a
   search snippet.
3. **The negative search.** C1 ran ~1.5M $\tau_w = 2$ instances plus ring and
   shore-lattice families and found no counterexample. Given `zero-weight-frontier`'s
   $\ge 7$-vertex floor, that sweep starts exactly at the frontier and samples
   randomly in an astronomically large space, so it is very weak evidence of
   absence. **C1 already says this** — "it does not say anything about Woodall",
   "the phenomenon is rarer and/or larger than the families I tried" — and does
   not offer it as support for its own argument. That framing is correct and I
   credit it. My own searches (§4.2) failed the same way and I record the same
   caveat.

### 7.6 Steps of C1's I could not follow

None. I could follow and independently re-derive every step of C1's §§4–5, and
every step of its §6.2 weight walk-through. What I could **not** do is the one
thing that would actually test the Schrijver filter: run the argument against
Schrijver's instance. Neither could C1. That gap is shared, environmental, and
unresolved.

---

## 8. What this review is worth — read this before citing it

Per repo `RULES.md` §5:

```
checked:
  - the dicut/dijoin/tau definitions and an independent implementation of them,
    validated on the four required fixtures plus three more
  - every step of the tau=2 argument, re-derived rather than read, including a
    self-contained ear-decomposition proof of the Robbins input
  - the CONSTRUCTION, reimplemented independently and verified to output two
    dijoins on all 531441 multi-digraphs on 4 vertices, all 1048576 simple
    digraphs on 5 vertices, and 300000 random 5-vertex multi-digraphs
  - the Lucchesi-Younger filter, lemma by lemma
  - the easy-direction filter
  - the LOCATION of the Schrijver filter's failure point, re-derived
  - Propositions R1 and R2 above, which are mine and are proved here
  - C1's Theorem R procedure, transcribed from its prose and re-run on 42772
    tau>=2 multidigraphs; C1's Prop 4.1 dicut/tau correspondence; C1's
    construction; C1's three self-declared weak points W1, W2, W3
  - C1's section 6.2 demonstration instance, rebuilt detail by detail
  - the strictly-positive-weight claim: derived independently BEFORE reading
    C1's file, then corroborated on 1605210 instances
  - Lemma A's bridgeless half under the opposite empty-dicut convention

not-checked:
  - Schrijver 1980 itself. Every primary and secondary source is refused by this
    sandbox's egress proxy. I did NOT reconstruct Schrijver's counterexample and
    therefore did NOT run the argument's steps against it. This was the
    assignment's primary test and it is not done.
  - consequently, the fact that Schrijver's counterexample uses weight-zero
    arcs, on which the entire Schrijver-filter discharge depends (§5.1), is
    taken on trust from a web-search snippet, not from a paper I read.
  - the attribution of the tau=2 result to Cornuejols-Liu-Ravi Corollary 2, and
    the {0,1} reduction cited to the same paper.
  - Schrijver's instance walked against C1's steps: not done, by either of us.
  - C1's own checker library experiments/woodall-tau2-checks/tau2lib.py: I did
    not read or run it, deliberately, so that a shared encoding bug would show
    up as a disagreement rather than as agreement.
```

**A load-bearing step is in `not-checked`.** The Schrijver filter is the
gatekeeper for this whole problem, and I verified only that the sketch's
identified failure point is the right one *given* that Schrijver's example has
zero weights. So `tau2-robbins` **stays `sketch`**.

I am also not permitted to promote it. Issue #153 forbids me granting
`verified:review`. Note the nuance, since it matters for whoever picks this up:
the reviewed file was written by **codex** (`Flow-25`), not by claude, so a
claude review of it is cross-family in the sense of `RULES.md` §5 — but my
task explicitly withholds that authority from me, and in any case the
`not-checked` list above is disqualifying on its own. What is needed next is
someone who can actually open Schrijver 1980, or a machine-checked
reconstruction of the counterexample.

## Reproduction

```
cd experiments/woodall-tau2-redteam
python3 validate.py            # fixture validation
python3 exhaustive.py          # n=4 multi-digraphs, all five checks
python3 exhaustive5.py         # n=5 simple + random multi
python3 search_eg_exact.py     # exact weighted-counterexample search, n<=6
python3 search_eg2.py 11 40000 # randomised search, n=7..12
python3 weighted_check.py      # strictly-positive-weight sharpness check
python3 attack_c1.py           # C1's Theorem R / Prop 4.1 / construction, my machinery
python3 lemmaA_probe.py        # Lemma A under the opposite empty-dicut convention
python3 check_c1_62.py         # C1's section 6.2 instance, rebuilt
```
