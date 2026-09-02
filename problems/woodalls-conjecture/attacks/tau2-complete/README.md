# Minimum dicut size two: a complete write-up of the two-dijoin partition

```
status:        sketch            (cross-family review not available this session; see §10)
target-status: verified:review
author:        claude (Fable 5.1), 2026-09-02, issue #152; adversary issue #153
supersedes:    attacks/tau2-robbins/README.md — by reference, not edited.  Same core idea
               (Robbins orientation + agreement colouring); this file adds the condensation
               step, a full proof of the orientation theorem for multigraphs, explicit edge-
               case conventions, a sharper Schrijver-filter analysis, and machine checks.
kill-criterion: KILL-CRITERION.md (stated first, accounted for in §9)
checks:        experiments/woodall-tau2-checks/  (all `numerical`; evidence, never a step)
depends-on:    nothing external is load-bearing.  Robbins's theorem is re-proved in full
               (Theorem R); it is cited for attribution only (§8, gap G1).
```

**What this is.** A self-contained proof that a finite digraph whose dicuts all have at least
two arcs (in particular, one with minimum dicut size exactly 2) has its arc set partitioned
into two dijoins. Every step is written so that a reader can check it without reconstructing
anything. The reader this is written for is an adversary who will try to weight-generalise it;
§6.2 tells that reader exactly where the argument dies under weights and why.

**What this is not.** It is not `verified:review`. Nobody from another model family has
reconstructed it. Per `RULES.md` §3 it is not assumable — not by its author, not by anyone —
until that happens. §10 lists what has and has not been independently checked.

---

## 0. Reading guide

| § | Content | Status of content |
|---|---|---|
| 1 | Definitions, in my own words, with the conventions fixed | definitions |
| 2 | Sanity checks: path, cycle, diamond, near-miss DAG | worked examples, machine-checked |
| 3 | Statement of the theorem | — |
| 4 | Reduction to the condensation, with proof, and why it is legitimate | proof |
| 5 | The proof: Lemma A (bridgeless), Theorem R (strong orientation), Lemma B (crossing both ways), the construction, and a table of where each hypothesis is used | proof |
| 6 | The three mandatory filters, each with its outcome; §6.2 is the decisive Schrijver filter | analysis |
| 7 | The steps I am least sure of, named, for the adversary | honesty |
| 8 | Dependencies and stated gaps | honesty |
| 9 | Kill-criterion accounting | bookkeeping |
| 10 | Checked / not checked | status discipline |

---

## 1. Definitions (own words) and conventions

Throughout, $D=(V,A)$ is a **finite digraph**. Loops and parallel arcs are allowed, and so are
antiparallel arcs ($x\to y$ together with $y\to x$). Each arc is an individual object; two
parallel arcs are two arcs. An arc $a$ has a tail $t(a)$ and a head $h(a)$.

**Cuts.** For $U\subseteq V$ write
$$\delta^+(U)=\{a\in A:\ t(a)\in U,\ h(a)\notin U\},\qquad
  \delta^-(U)=\{a\in A:\ t(a)\notin U,\ h(a)\in U\}=\delta^+(V\setminus U).$$
Loops lie in no $\delta^\pm(U)$.

**Dicut.** A *dicut* is a set of the form $\delta^+(U)$ where $U$ is a **nonempty proper**
subset of $V$ (so $V\setminus U$ is also nonempty) **and $\delta^-(U)=\varnothing$**. In words:
some arc set that is *all* the arcs crossing the vertex partition $\{U,V\setminus U\}$, and they
all point the same way (out of $U$). $U$ is called the *shore*. The condition is
$\delta^-(U)=\varnothing$; it is *not* "$\delta^+(U)\neq\varnothing$". (Problem `RULES.md` §4
warns this is the standard misreading; the checker in `experiments/woodall-tau2-checks/`
implements exactly the condition above.)

**Convention on the empty dicut.** If $D$ is not weakly connected, taking $U$ to be a union of
weak components gives $\delta^+(U)=\delta^-(U)=\varnothing$, so $\varnothing$ is a dicut. I keep
this convention; it makes $\tau=0$ for weakly disconnected digraphs, and then no dijoin exists
at all (nothing meets $\varnothing$). The theorem below is stated for $\tau\ge 2$, so it never
sees that case, and §3 remarks how to read it under the other convention.

**$\tau(D)$** is the minimum $|C|$ over dicuts $C$. If $D$ has no dicut at all (equivalently,
$D$ is strongly connected — see Proposition 4.1(iv)), set $\tau(D)=+\infty$.

**Dijoin.** A *dijoin* is a set $J\subseteq A$ with $J\cap C\neq\varnothing$ for every dicut
$C$. Supersets of dijoins are dijoins. If there are no dicuts, every arc set (including
$\varnothing$) is a dijoin.

**Two disjoint dijoins ⇔ a 2-colouring.** $A$ is partitioned into two dijoins iff there is a
map $c:A\to\{\text{red},\text{blue}\}$ such that **every dicut contains an arc of each colour**.
(Given such $c$ the colour classes are disjoint dijoins covering $A$; given disjoint dijoins
$J_1,J_2$, colour $J_1$ red and everything else blue — $A\setminus J_1\supseteq J_2$ is a
dijoin because supersets of dijoins are dijoins.) The proof produces such a colouring.

**Underlying multigraph.** $G(D)$ has vertex set $V$ and, for each non-loop arc $a$, one
undirected edge $e_a=\{t(a),h(a)\}$. Parallel and antiparallel arcs give parallel edges. An
*orientation* $O$ of $G(D)$ assigns to each edge $e_a$ one of its two directions, written
$O(e_a)\in\{(t(a),h(a)),(h(a),t(a))\}$; note that this is chosen **per edge**, so two parallel
edges may be oriented oppositely. $O$ is *strongly connected* if the resulting digraph
$(V,\{O(e_a)\})$ has a directed path from every vertex to every other.

A *bridge* of a multigraph $G$ is an edge $e$ such that $G-e$ has more connected components than
$G$. A loop is never a bridge; an edge with a parallel twin is never a bridge.

---

## 2. Sanity checks on the definitions

All four are executed in `experiments/woodall-tau2-checks/test_tau2.py` (`numerical`).

1. **Directed path** $s\to v\to t$. Shores with no entering arc: $\{s\}$ and $\{s,v\}$ (the
   set $\{s,t\}$ has $v\to t$ entering it; $\{v\}$ has $s\to v$ entering). Dicuts:
   $\{s\to v\}$ and $\{v\to t\}$, both of size 1, so $\tau=1$. A single dijoin must contain
   both arcs. Two disjoint dijoins do not exist — consistent with the theorem's hypothesis
   failing.
2. **Directed cycle** $v_0\to v_1\to\cdots\to v_{k-1}\to v_0$. Any nonempty proper $U$ contains
   some $v_i$ with $v_{i-1}\notin U$ (indices mod $k$), so $v_{i-1}\to v_i\in\delta^-(U)$.
   **No dicuts**, $\tau=+\infty$; every arc set is a dijoin; the theorem is trivially true.
   The checker confirms the dicut list is empty — the standard bug (testing
   $\delta^+(U)\ne\varnothing$ instead of $\delta^-(U)=\varnothing$) would report dicuts here.
3. **Diamond** $s\to x,\ s\to y,\ x\to t,\ y\to t$. Dicut shores: $\{s\}$, $\{s,x\}$, $\{s,y\}$,
   $\{s,x,y\}$. Dicuts: $\{sx,sy\}$, $\{sy,xt\}$, $\{sx,yt\}$, $\{xt,yt\}$; $\tau=2$. The
   colouring red $=\{sx,xt\}$, blue $=\{sy,yt\}$ (the two $s$–$t$ paths) meets every dicut in
   both colours. §5.5 shows this is exactly what the construction produces.
4. **Near-miss DAG** $s_1\to t_1,\ s_2\to t_1,\ s_2\to t_2$. The shore $\{s_1\}$ has no entering
   arc and $\delta^+(\{s_1\})=\{s_1t_1\}$: a dicut of size 1, so $\tau=1$ and the theorem does
   not apply. (Its other dicut shores are $\{s_2\}$, $\{s_1,s_2\}$, $\{s_2,t_2\}$,
   $\{s_1,s_2,t_2\}$, $\{s_1,s_2,t_1\}$.) Replacing every arc by two parallel copies gives
   $\tau=2$, and colouring one copy of each pair red and the other blue is a valid partition —
   and is also what the construction produces, since a strong orientation of a doubled path
   must orient each pair oppositely.

---

## 3. Statement

> **Theorem.** Let $D=(V,A)$ be a finite digraph in which every dicut has at least two arcs,
> i.e. $\tau(D)\ge 2$ (including $\tau(D)=+\infty$). Then $A$ can be partitioned into two
> dijoins. In particular this holds when $\tau(D)=2$, which is the existence direction of
> Woodall's conjecture for $\tau=2$.

Stating it for $\tau\ge 2$ rather than $\tau=2$ costs nothing (the proof only ever uses "no
dicut of size $\le 1$") and removes a convention dependency: a reader who does *not* count the
empty set as a dicut can apply the theorem to each weak component of $D$ separately (each has
$\tau\ge 2$ under that convention, since a dicut of a component is a dicut of $D$), and the
union of the per-component partitions is a partition of $A$ into two dijoins of $D$ because
every nonempty dicut of $D$ **contains** a nonempty dicut of a single component. (Nonempty
dicut $\delta^+(U)$: some component $H$ meets both $U$ and $V\setminus U$, since otherwise no
arc crosses $U$; then $\delta^-_H(U\cap V(H))\subseteq\delta^-(U)=\varnothing$, so
$\delta^+_H(U\cap V(H))$ is a dicut of $H$ contained in $\delta^+(U)$, and it is nonempty
because $H$ is connected; both colours meet it, hence meet $\delta^+(U)$.)

---

## 4. Reduction to the condensation

Two vertices are *strongly equivalent* if each reaches the other by a directed path (the
empty path counts, so every vertex is equivalent to itself). The classes are the *strong
components*. Let $\pi:V\to V'$ send each vertex to its component. The **condensation**
$D'=(V',A')$ has vertex set $V'$ and arc set
$A'=\{a\in A:\ \pi(t(a))\ne\pi(h(a))\}$, where the arc $a\in A'$ now has tail $\pi(t(a))$ and
head $\pi(h(a))$. I deliberately keep the *same arc objects*, so that "the same arc set" makes
sense across $D$ and $D'$.

> **Proposition 4.1.**
> (i) If $U$ is a dicut shore of $D$ then $U=\pi^{-1}(\pi(U))$, i.e. $U$ is a union of strong
> components.
> (ii) $U'\mapsto\pi^{-1}(U')$ is a bijection from the dicut shores of $D'$ onto the dicut
> shores of $D$, and it preserves the dicut: $\delta^+_D(\pi^{-1}(U'))=\delta^+_{D'}(U')$ as arc
> sets.
> (iii) Consequently $D$ and $D'$ have exactly the same dicuts (as arc sets), $\tau(D)=\tau(D')$,
> and $J\subseteq A$ is a dijoin of $D$ iff $J\cap A'$ is a dijoin of $D'$.
> (iv) $D'$ is acyclic. In particular $D$ has no dicut iff $D'$ has one vertex iff $D$ is
> strongly connected (when $V\neq\varnothing$).

*Proof.* (i) Let $\delta^-_D(U)=\varnothing$, $x\in U$, and $y$ strongly equivalent to $x$.
There is a directed path $y=v_0\to v_1\to\cdots\to v_k=x$. If $y\notin U$, let $i$ be the least
index with $v_i\in U$ (it exists, $v_k=x\in U$; and $i\ge 1$). Then $v_{i-1}\to v_i$ has tail
outside $U$ and head inside: it is in $\delta^-_D(U)$, contradiction. So $y\in U$.

(ii) Let $U'$ be a nonempty proper subset of $V'$ and $U=\pi^{-1}(U')$; then $U$ is nonempty
and proper. An arc $a$ with both ends in one component is never in $\delta^\pm_D(U)$ because
$U$ is a union of components. For $a\in A'$: $t(a)\in U\iff\pi(t(a))\in U'$ and the same for
heads. Hence $\delta^-_D(U)=\delta^-_{D'}(U')$ and $\delta^+_D(U)=\delta^+_{D'}(U')$ as arc sets;
in particular $U$ is a dicut shore of $D$ iff $U'$ is one of $D'$. Injectivity of
$U'\mapsto\pi^{-1}(U')$ is clear ($\pi$ is onto). Surjectivity: by (i) every dicut shore $U$
of $D$ equals $\pi^{-1}(\pi(U))$, and $\pi(U)$ is nonempty and proper ($U$ proper and a union
of components), so $U$ is the image of $U'=\pi(U)$.

(iii) "Same dicuts" and $\tau(D)=\tau(D')$ are immediate from (ii). Every dicut of $D$ is a
subset of $A'$ (it consists of arcs crossing a union of components), so $J$ meets it iff
$J\cap A'$ does.

(iv) A directed cycle $C_1\to C_2\to\cdots\to C_k\to C_1$ in $D'$ ($k\ge 2$, and $k=1$ is
impossible because arcs inside a component are not in $A'$) gives, for consecutive
components, an arc from a vertex of $C_i$ to a vertex of $C_{i+1}$; concatenating these arcs
with directed paths inside each component (which exist by strong equivalence) shows that a
vertex of $C_1$ reaches a vertex of $C_2$ and vice versa, so $C_1=C_2$, contradiction. For the
last sentence: if $|V'|\ge 2$, an acyclic digraph has a vertex $v'$ with no entering arc (walk
backwards; finiteness), and $\{v'\}$ is a dicut shore of $D'$, hence $D'$ has a dicut; if
$|V'|=1$, $V'$ has no nonempty proper subset and there is no dicut. $\square$

**Why the reduction is legitimate.** By (iii), a partition of $A'$ into two dijoins of $D'$
extends to a partition of $A$ into two dijoins of $D$ by placing each arc of $A\setminus A'$ in
either part (arbitrarily): every dicut of $D$ is a dicut of $D'$ and is met by both parts
already. And $\tau(D')=\tau(D)\ge2$. So it suffices to prove the theorem for $D'$, a DAG.

**A remark the adversary should note.** Nothing in §5 uses acyclicity. The reduction is
included because the issue asks for it and because it is what the experiments enumerate; the
proof of §5 applied directly to $D$ is equally valid, and the experiments check the
construction on digraphs with cycles as well.

---

## 5. The proof

From here $D=(V,A)$ satisfies $\tau(D)\ge 2$, and $G=G(D)$ is its underlying multigraph.
If $|V|=1$ there is no dicut and any partition works; assume $|V|\ge2$.

### 5.1 Lemma A — $G$ is connected and bridgeless

> **Lemma A.** If $\tau(D)\ge 2$ then $G$ is connected and has no bridge.

*Proof.* Connected: if not, let $U$ be the vertex set of one connected component of $G$; $U$
is nonempty and proper, no arc has exactly one end in $U$, so $\delta^-(U)=\varnothing$ and
$\delta^+(U)=\varnothing$ is a dicut of size $0<2$. Contradiction.

Bridgeless: suppose $e_a=\{u,v\}$ (the edge of a non-loop arc $a$) is a bridge, and let $U$ be
the vertex set of the component of $G-e_a$ containing $u$. Then $v\notin U$ (otherwise $u,v$
are joined in $G-e_a$ and $e_a$ is not a bridge). Any edge of $G$ other than $e_a$ with exactly
one end in $U$ would join $U$ to the rest inside $G-e_a$, contradicting that $U$ is a
component of $G-e_a$. So $a$ is the **only** arc of $D$ with exactly one end in $U$. Two
cases:
* $t(a)\in U$: then $\delta^-(U)=\varnothing$ and $\delta^+(U)=\{a\}$ is a dicut of size 1.
* $h(a)\in U$: then $\delta^+(U)=\varnothing=\delta^-(V\setminus U)$ and
  $\delta^+(V\setminus U)=\delta^-(U)=\{a\}$ is a dicut of size 1.

Both contradict $\tau(D)\ge 2$. $\square$

(This is the **only** place the hypothesis $\tau\ge 2$ is used; see the table in §5.5.)

### 5.2 Theorem R — connected bridgeless multigraphs have strong orientations

This is Robbins's theorem [R]. Because the standard statement is for graphs and I could not
access the paper this session (§8, G1), and because parallel edges are essential here (they
arise from parallel/antiparallel arcs and from the condensation), I give a complete proof for
multigraphs. Nothing below depends on [R] beyond attribution.

> **Theorem R.** Every connected multigraph $G$ without bridges has a strongly connected
> orientation.

*Proof.* Loops may be oriented arbitrarily and are irrelevant to strong connectivity; ignore
them. If $G$ has one vertex, the empty orientation is strongly connected. Otherwise every
vertex is incident with an edge.

Maintain a vertex set $X\subseteq V$ and an oriented edge set $F\subseteq E(G)$ with the
invariants

* (I1) every edge of $F$ has both ends in $X$;
* (I2) the digraph $(X,F)$ with the chosen orientation is strongly connected.

Start with $X=\{x_0\}$ for any vertex $x_0$ and $F=\varnothing$; (I1), (I2) hold. While
$F\ne E(G)$:

*Choose an edge.* There is an edge $e\notin F$ with at least one end in $X$: if $X=V$, any
$e\notin F$ works; if $X\ne V$, connectivity of $G$ gives an edge between $X$ and $V\setminus X$,
which is not in $F$ by (I1). Write $e=\{u,v\}$ with $u\in X$.

*Case 1: $v\in X$.* Orient $e$ either way and add it to $F$. (I1) holds; (I2) holds because
adding an arc between two vertices of a strongly connected digraph keeps it strongly
connected. This case covers parallel edges: a second copy of an already-oriented edge is
just another edge with both ends in $X$.

*Case 2: $v\notin X$.* Since $e$ is not a bridge, $G-e$ is connected, so there is a path $P$ in
$G-e$ from $v$ to $u$. Let $z$ be the first vertex of $P$ (walking from $v$) that lies in $X$;
it exists because $u\in X$. Let $P'$ be the sub-path of $P$ from $v$ to $z$. Every vertex of
$P'$ other than $z$ lies outside $X$, so by (I1) no edge of $P'$ is in $F$; also $P'$ does not
use $e$. Orient $e$ as $u\to v$ and orient the edges of $P'$ along $P'$ from $v$ towards $z$;
add $e$ and $E(P')$ to $F$, and add $V(P')$ to $X$. (I1) holds by construction. (I2): every old
vertex reaches every old vertex as before; a new vertex $y\in V(P')\setminus\{z\}$ is reached
from $u$ along $u\to v\to\cdots\to y$ and reaches $z$ along $P'$; since $u,z$ are old vertices,
all pairs are connected.

Each iteration enlarges $F$, so the loop ends with $F=E(G)$; then $X=V$ because every vertex is
incident with some edge and (I1). The final orientation is strongly connected by (I2). $\square$

The procedure is implemented verbatim in `tau2lib.robbins_orientation`, and the tests check
strong connectivity of its output on every instance they touch.

### 5.3 Lemma B — a strong orientation crosses every cut in both directions

> **Lemma B.** Let $O$ be a strongly connected orientation of a multigraph on $V$ and
> $\varnothing\neq U\subsetneq V$. Then some edge is oriented by $O$ from $U$ to $V\setminus U$
> and some edge is oriented by $O$ from $V\setminus U$ to $U$.

*Proof.* Pick $u\in U$, $v\notin U$. A directed $u\to v$ path in $O$ starts inside $U$ and ends
outside, so it has a first arc whose tail is in $U$ and whose head is not: an edge oriented
out of $U$. A directed $v\to u$ path likewise has a first arc with tail outside $U$ and head
inside: an edge oriented into $U$. $\square$

### 5.4 The construction and its verification

Let $O$ be a strongly connected orientation of $G$, which exists by Lemma A and Theorem R.
Define, for every non-loop arc $a$,

$$a\in J_1\ (\text{red})\iff O(e_a)=(t(a),h(a))\quad(\text{$a$ agrees with $O$}),\qquad
  a\in J_2\ (\text{blue})\iff O(e_a)=(h(a),t(a))\quad(\text{$a$ disagrees}).$$

Put loops in $J_1$. Since $O(e_a)$ is exactly one of the two directions, $\{J_1,J_2\}$ is a
partition of $A$.

> **Claim.** Every dicut of $D$ contains a red arc and a blue arc. Hence $J_1$ and $J_2$ are
> disjoint dijoins with $J_1\cup J_2=A$, proving the Theorem.

*Proof.* Let $C=\delta^+(U)$ be a dicut, so $U$ is nonempty and proper and
$\delta^-(U)=\varnothing$. Observe first:

> (★) every edge of $G$ with exactly one end in $U$ is $e_a$ for an arc $a$ with $t(a)\in U$ and
> $h(a)\notin U$, i.e. $a\in C$.

Indeed such an edge comes from an arc $a$ with exactly one end in $U$; then
$a\in\delta^+(U)\cup\delta^-(U)=\delta^+(U)=C$ because $\delta^-(U)=\varnothing$.

*Red arc.* By Lemma B there is an edge $e_a$ oriented by $O$ out of $U$: $O(e_a)=(p,q)$ with
$p\in U$, $q\notin U$. By (★), $a\in C$ and $t(a)\in U$, $h(a)\notin U$. The two ends of $e_a$ are
$\{p,q\}=\{t(a),h(a)\}$, and the one in $U$ is $p=t(a)$; so $O(e_a)=(t(a),h(a))$: $a$ agrees
with $O$ and is red. Thus $a\in C\cap J_1$.

*Blue arc.* By Lemma B there is an edge $e_b$ oriented by $O$ into $U$: $O(e_b)=(p,q)$ with
$p\notin U$, $q\in U$. By (★), $b\in C$ with $t(b)\in U$, $h(b)\notin U$. Now the end of $e_b$ in
$U$ is $q$, so $q=t(b)$ and $p=h(b)$: $O(e_b)=(h(b),t(b))$, which is the direction *opposite*
to $b$. So $b$ is blue and $b\in C\cap J_2$. $\square$

Note what the blue step is doing: the *orientation* $O$ crosses into $U$, but the *arc* $b$
still leaves $U$ — because $C$ is a dicut and no arc of $D$ enters $U$. For a general directed
cut (with arcs both ways) this would be false, and that is the step a confusion of "cut" with
"dicut" would break. This is (W1) in §7.

### 5.5 Where each hypothesis is used, and a worked instance

| Step | Uses $\tau\ge2$? | Uses finiteness? | Uses unit weights / that every arc may be used? | Uses acyclicity? |
|---|---|---|---|---|
| Prop. 4.1 (condensation) | no | yes (paths, minimal index) | no | no (it *produces* it) |
| Lemma A | **yes — only here** | no | no (see §6.2: holds verbatim under weights) | no |
| Theorem R | no | yes (termination) | no | no |
| Lemma B | no | no | no | no |
| Construction 5.4 | no | no | **yes — every arc is coloured and both colour classes are used as dijoins** | no |

**Worked instance: the diamond** ($s\to x,\ s\to y,\ x\to t,\ y\to t$). $G$ is the 4-cycle
$s{-}x{-}t{-}y{-}s$, connected and bridgeless. Theorem R's procedure from $x_0=s$: pick
$e=\{s,x\}$, $v=x\notin X$; path in $G-e$ from $x$ to $s$: $x,t,y,s$; $z=s$; orient
$s\to x\to t\to y\to s$. All edges are now in $F$; $O$ is the directed 4-cycle. Colouring:
$sx$ agrees (red), $xt$ agrees (red), $yt$ disagrees ($O$ has $t\to y$; blue), $sy$ disagrees
($O$ has $y\to s$; blue). Red $=\{sx,xt\}$, blue $=\{sy,yt\}$: the two $s$–$t$ paths, and each
of the four dicuts listed in §2.3 contains one of each. (`test_tau2.py::test_diamond_split`.)

**Worked instance with parallel arcs and a cycle:** `test_tau2.py::test_condensation_random`
and `test_random_multidigraphs` run the whole pipeline — condensation, Lemma A check, Theorem
R, colouring, and an independent brute-force verification that both classes meet every dicut —
on 3 000 seeded random multidigraphs (parallel, antiparallel, loops, cycles) with $\tau\ge2$,
and on **all** simple digraphs on $\le4$ vertices and all multidigraphs on 3 vertices with
arc multiplicity $\le 2$. Zero failures. `numerical`; evidence only.

---

## 6. The three mandatory filters (problem `RULES.md` §1)

### 6.1 The weighted statement, precisely

Let $w:A\to\mathbb Z_{\ge0}$. Put $\tau_w=\min\{w(C): C\text{ a dicut}\}$. A **$w$-packing** of
dijoins is a family $J_1,\dots,J_k$ of dijoins such that every arc $a$ lies in at most $w(a)$
of them. The Edmonds–Giles conjecture asserted that a $w$-packing of size $\tau_w$ always
exists [EG]; Schrijver [S80] gave a counterexample with $w\in\{0,1\}^A$ and $\tau_w=2$. (Locator
status: §8, G2/G4.)

Two standard reductions, both proved here so they are not dependencies:

* **Positive weights are multidigraphs.** Replace each arc $a$ with $w(a)\ge1$ by $w(a)$
  parallel copies of weight 1 (and keep the arcs of weight 0 with weight 0). Dicut shores are
  unchanged (the copies cross exactly the cuts $a$ crossed, in the same direction), the weight
  of every dicut is unchanged, and a $w$-packing of the original corresponds to a family of
  dijoins in the expansion in which each copy is used at most once (spread the $\le w(a)$
  dijoins containing $a$ over its copies) and conversely (collapse copies). So for
  **strictly positive** weights the weighted statement at $\tau_w=2$ is exactly the Theorem
  for multidigraphs, which §5 proves. **The proof above is a correct proof of Edmonds–Giles
  for strictly positive weights at $\tau_w\ge2$.** That is not in tension with anything known:
  Schrijver's example needs weight-0 arcs (Cornuéjols–Liu–Ravi make this remark in their §1
  per `attacks/tau2-robbins`, and it is forced by the argument just given).
* **So the only genuinely weighted regime is $w(a)=0$**, and WLOG $w\in\{0,1\}^A$. Write
  $S=w^{-1}(1)$ (the usable arcs) and $Z=w^{-1}(0)$. A $w$-packing of size 2 is a pair of
  disjoint dijoins **both contained in $S$**. In colouring language: a 2-colouring of $S$ (not
  of $A$) such that every dicut $C$ has both colours among $C\cap S$.

### 6.2 Schrijver filter — outcome: **passes; the failing step is the construction of §5.4**

Run the proof on a $\{0,1\}$-weighted instance $(D,w)$ with $\tau_w=2$, step by step.

1. **Condensation (Prop. 4.1).** Goes through unchanged; weights ride along on the arcs of
   $A'$. Not the failing step.
2. **Lemma A.** *Holds verbatim.* $\tau_w=2$ means every dicut contains at least two arcs of
   $S$, hence at least two arcs; so $\tau(D)\ge2$ in the unweighted sense and Lemma A applies:
   $G$ is connected and bridgeless. **Lemma A is not the step that needs unit weights.**
   (`attacks/tau2-robbins` originally claimed a "weight-2 bridge" here; `FINDINGS.md` records
   that this was wrong, and the corrected version of that file agrees with the present
   analysis.)
3. **Theorem R and Lemma B.** Statements about the multigraph $G$ and about $O$ alone; weights
   do not appear. Not the failing step.
4. **Construction 5.4 — THIS IS THE STEP.** It colours **every** arc of $A$, and its
   correctness proof needs the colour classes $J_1,J_2\subseteq A$ *as they are*: the red
   witness and the blue witness handed to us by Lemma B are *arbitrary* crossing edges of $G$,
   with no control over whether they come from arcs of $S$ or of $Z$. Under $w\equiv1$ that is
   fine because every arc may be used, and the sentence "$J_1,J_2$ partition $A$, hence they
   are a packing" is true. Under weights, a packing must satisfy
   $\chi^{J_1}+\chi^{J_2}\le w$, i.e. $J_1,J_2\subseteq S$. The only candidate the construction
   offers is $(J_1\cap S,\ J_2\cap S)$, and the proof of the Claim gives **no** reason for these
   to be dijoins: if for some dicut $C$ every arc of $C\cap S$ agrees with $O$ (so the blue
   witnesses of $C$ all lie in $Z$), then $J_2\cap S$ misses $C$. The step "both colour classes
   meet every dicut" is simply false for $J_2\cap S$ in that situation.

   **Why weights genuinely break it, not just the bookkeeping.** One might hope to repair the
   step. The three obvious repairs each fail, and the failure of the third *is* Schrijver's
   theorem:

   * *Delete $Z$ and apply the Theorem to $D-Z$.* Deleting an arc that **enters** a shore $U$
     can turn $U$ into a dicut shore of $D-Z$ that was not one in $D$; that new dicut may have
     $\le1$ arc of $S$, so $\tau(D-Z)\le1$ and the Theorem does not apply. Conversely, if
     $\tau(D-Z)\ge2$ then the Theorem *does* give a packing (dicuts of $D$ restrict to dicuts
     of $D-Z$: $\delta^-_{D-Z}(U)\subseteq\delta^-_D(U)=\varnothing$ and
     $\delta^+_{D-Z}(U)=C\cap S$), so every counterexample must have a shore $U$ with
     $\delta^-_D(U)\subseteq Z$, $\delta^-_D(U)\ne\varnothing$ and $|\delta^+_D(U)\cap S|\le1$.
     This is the precise sense in which weight-0 arcs "shape the dicut family" and cannot be
     removed.
   * *Contract $Z$.* Contracting $a=(x,y)$ destroys every dicut whose shore separates $x$ from
     $y$; a dijoin of $D/a$ can miss such a dicut of $D$. So dijoins do not transfer back.
   * *Choose $O$ cleverly.* The construction would work under weights iff $G$ has a strongly
     connected orientation $O$ such that **for every dicut shore $U$, some $S$-arc agrees with
     $O$ across $U$ and some $S$-arc disagrees** — call this an *$S$-witnessed* strong
     orientation. Its existence for all $\{0,1\}$-instances with $\tau_w=2$ is *equivalent* to
     the weighted statement at $\tau_w=2$ (given such $O$, colour $S$ by agreement; given a
     packing $J_1\sqcup J_2\subseteq S$, one still has to produce $O$ — this direction is not
     needed for the point being made). Schrijver's example shows no such $O$ exists in
     general. So there is no repair inside this proof strategy: the very *object* the proof
     builds (a strong orientation of the weight-blind multigraph $G$) does not carry enough
     information.

   **Mechanical demonstration that the step, as written, fails under weights**
   (`test_tau2.py::test_schrijver_filter_step_fails`, `numerical`). Take the diamond plus one
   weight-0 arc $x\to y$, with the four diamond arcs of weight 1. Dicut shores: $\{s\}$,
   $\{s,x\}$, $\{s,x,y\}$ (the shore $\{s,y\}$ is no longer a dicut shore: $x\to y$ enters it).
   $\tau_w=2$. The orientation $O=\{s\to x,\ x\to y,\ y\to s,\ y\to t,\ t\to x\}$ is strongly
   connected. The agreement colouring gives $sx$ red, $sy$ blue, $xt$ blue, $yt$ red, and the
   weight-0 arc $xy$ red. For the dicut $C=\delta^+(\{s,x\})=\{sy,\ xt,\ xy\}$: red $\cap\,C$
   $=\{xy\}\subseteq Z$, so $J_1\cap S=\{sx,yt\}$ **misses $C$** — the construction's output is
   not a $w$-packing. (On this instance another strong orientation happens to work, and a
   $w$-packing $\{sx,xt\},\{sy,yt\}$ exists; the instance shows the *step* failing, not the
   *statement*. The statement fails on Schrijver's instance, where every $O$ fails.)

   **Walking the proof against Schrijver's own instance — stated gap G2.** The issue asks for
   Schrijver's counterexample to be reconstructed and the proof walked against it. I could not
   do this honestly this session: every host carrying the paper or a figure of it
   (`ir.cwi.nl`, `dl.acm.org`, `ime.usp.br`, `arxiv.org`, `en.wikipedia.org`,
   `lemon.cs.elte.hu`, `openproblemgarden.org`, `researchgate.net`, `andrew.cmu.edu`,
   `uwaterloo.ca`) is blocked by the egress proxy; only search-result snippets were
   reachable. Those snippets (unverified against any paper) say: weight-1 ("solid") arcs and
   weight-0 ("dashed") arcs, minimum dicut weight 2, no packing of two dijoins inside the solid
   arcs, solid arcs labelled $1,1',1'',2,\dots$ with six minimal dicuts of weight 2 such as
   $D_1\supseteq\{1,1'\}$, $D_2\supseteq\{1,1''\}$, a chordless cycle of length 6 in the
   underlying graph, and Younger's generalisation to "a ring of length $4k+2$ with $2k+1$ solid
   paths". Rather than write down a digraph from memory and call it Schrijver's, I searched
   for **a** $\{0,1\}$-weighted counterexample with my own checker (`numerical`, all in
   `experiments/woodall-tau2-checks/`): a seeded random hunt over DAGs on 7–8 vertices
   (410 237 instances with $\tau_w=2$) and on 9–11 vertices (1 059 705 instances), an
   exhaustive pass over the symmetric "6-ring of weight-0 arcs plus three solid 3-arc paths"
   family (1 536 instances), a wider ring family with independent path orientations and path
   lengths 2–4 on all six endpoint matchings (803 528 instances: lengths 2 and 3 complete,
   length 4 cut off at the budget), and a shore-lattice construction with three out-star
   gadgets (32 768 configurations). **None produced a counterexample.** Together with the repo's earlier
   census (`attacks/zero-weight-frontier`: none on $\le6$ condensation vertices) this says
   the phenomenon is rarer and/or larger than the families I tried; it does not say anything
   about Woodall. The walk-through above is therefore against the *general* $\{0,1\}$ instance
   and against the diamond-plus-zero-arc instance, and the claim "on Schrijver's instance every
   strong orientation fails" is a *consequence* of Schrijver's theorem (any $S$-witnessed $O$
   would give a packing), not something I have executed. The checker
   `tau2lib.two_packing_within` is ready to run on the instance the moment someone with
   access transcribes it; that transcription is the missing artefact.

**Filter outcome.** The proof contains a step — the colouring-to-packing step of §5.4 — that
is genuinely false under $\{0,1\}$ weights, for a structural reason (the orientation is
weight-blind), and no step earlier than it fails. The kill-criterion K1 is not met.

### 6.3 Lucchesi–Younger filter — outcome: **passes**

The Lucchesi–Younger theorem says the minimum size of a dijoin equals the maximum number of
pairwise disjoint dicuts. It is not used. Inventory of every non-definitional fact used in §4–5:
Proposition 4.1 (paths and components), Lemma A (a bridge gives a one-arc dicut), Theorem R (ear
construction), Lemma B (first arc of a path). None mentions a dijoin; none is a min–max
statement; none has a proof that hides one (each proof is written out above). The word
"dijoin" appears in the argument only in the final Claim, where the two sets are shown to be
dijoins directly from the definition. There is no step of the form "there exists a dijoin of
size $\le k$" or "there exist $k$ disjoint dicuts". I also checked that Theorem R is not LY in
disguise: it concerns undirected graphs and has no notion of dicut.

### 6.4 Easy-direction filter — outcome: **passes**

The trivial direction ("at most $\tau$ disjoint dijoins, since each must use an arc of a
minimum dicut") is never stated or used. The proof *exhibits* $J_1,J_2$ and proves from the
definition that each meets every dicut; it produces a partition of $A$, which is stronger than
existence of two disjoint dijoins.

---

## 7. What to attack: the steps I am least sure of (named, as required)

In decreasing order of my own uncertainty:

* **(W1) The blue witness in §5.4.** The bookkeeping "$O(e_b)$ enters $U$, but $b$ leaves $U$
  because $\delta^-(U)=\varnothing$, hence $b$ disagrees" is the heart of the proof and the
  place where a cut/dicut confusion would silently break it. I have written it with explicit
  endpoints; please re-derive it rather than read it.
* **(W2) Theorem R, Case 2.** The claims that $P'$ uses no edge of $F$, that $P'$ avoids $e$,
  and that the enlarged digraph is strongly connected. Parallel edges and the possibility
  $z=u$ are the corner cases; I believe they are covered but this is the longest argument.
* **(W3) Proposition 4.1(i).** The "first vertex of the path inside $U$" argument, in
  particular that the index $i$ is $\ge1$ and that the arc found is in $\delta^-(U)$ and not
  $\delta^+(U)$.
* **(W4) Conventions.** The empty-dicut convention, $\tau=+\infty$, and the per-component
  remark in §3. A reader using a different convention should check §3's paragraph rather than
  assume it.
* **(W5) The Schrijver analysis.** The claim that Lemma A holds verbatim under weights is a
  short argument and I believe it; the claim that the three "repairs" fail is argued but the
  third one relies on Schrijver's theorem, whose instance I could not verify (G2). I do **not**
  claim that no other proof strategy could be repaired — only that *this* proof's step 5.4
  fails and that the failure is structural.

Things I am *not* worried about but which are load-bearing: Lemma B (two lines), Lemma A
(the bridge case split).

---

## 8. Dependencies and stated gaps

Nothing external is load-bearing: Proposition 4.1, Lemmas A and B and Theorem R are proved in
full above. Attributions and locators, with their verification status this session:

* **[R]** H. E. Robbins, "A theorem on graphs, with an application to a problem of traffic
  control", *Amer. Math. Monthly* 46 (1939), 281–283. Statement: a connected graph has a
  strongly connected orientation iff it has no bridge. **Gap G1:** locator taken from
  `attacks/tau2-robbins` and memory; the paper was not reachable this session, so I did not
  confirm the page numbers or that Robbins states the multigraph form. This is why Theorem R
  is proved here rather than cited. Status of [R] in this file: `cited` for attribution only.
* **[S80]** A. Schrijver, "A counterexample to a conjecture of Edmonds and Giles", *Discrete
  Math.* 32 (1980), 213–214 (the problem README says 213–215). **Gap G2:** not reachable; the
  instance was not transcribed; the only content I have is the search snippets quoted in §6.2.
  Everything said about the instance is flagged as unverified.
* **[EG]** J. Edmonds and R. Giles, "A min-max relation for submodular functions on graphs",
  *Annals of Discrete Math.* 1 (1977), 185–204. **Gap G4:** from memory; not reachable; used
  only to name the conjecture, not in any step.
* **[CLR]** G. Cornuéjols, S. Liu, R. Ravi, "Approximately packing dijoins via nowhere-zero
  flows", *Combinatorica* 45 (2025), art. 32. `attacks/tau2-robbins` cites its Corollary 2 for
  the $\tau=2$ folklore and its Proposition 1 for the agreement-colouring idea, and its §1 for
  the weight-0 remark. **Gap G3:** I could not open the paper; these locators are inherited,
  not re-verified. The result here is folklore (search snippets confirm the phrase "folklore"
  but not the attribution chain), and I claim no novelty.
* **[F]** P. Feofiloff, *Woodall's conjecture on packing dijoins: a survey* (2005). Not
  reachable; not used.

---

## 9. Kill-criterion accounting (`KILL-CRITERION.md`)

* **K1 (Schrijver):** discharged in §6.2 — the failing step is §5.4, and Lemma A explicitly is
  *not* it. Not met.
* **K2 (LY):** discharged in §6.3. Not met.
* **K3 (easy direction):** discharged in §6.4. Not met.
* **K4 (an elementary step fails on a machine-checked instance):** did not fire; all tests in
  `experiments/woodall-tau2-checks/` pass (fixtures, exhaustive small cases, seeded random
  multidigraphs, condensation correspondence, Theorem R output strong on every instance).
* **K5 (budget):** the proof and checks finished inside the hour. The search for a
  $\{0,1\}$-weighted counterexample was stopped at the budget and is reported with exact counts
  in the experiment README; it is not part of the proof.

---

## 10. Checked / not checked (status discipline, `RULES.md` §3 and §5)

```
status: sketch
examined-by: nobody from another model family (not available this session)
depends-on: nothing assumable; [R] cited for attribution only, re-proved as Theorem R
checked (by the author, numerically, experiments/woodall-tau2-checks/):
  - definitions on the four §2 fixtures
  - Prop. 4.1 dicut correspondence on seeded random digraphs with cycles
  - Lemma A (connected + bridgeless) on every tau >= 2 instance touched
  - Theorem R's procedure returns a strongly connected orientation on every instance touched
  - the §5.4 colouring meets every dicut in both colours: all simple digraphs on <= 4 vertices,
    all 3-vertex multidigraphs with multiplicity <= 2, 3000 seeded random multidigraphs
  - the §6.2 mechanical failure of step 5.4 under a weight-0 arc
not-checked:
  - any step by an independent reader (this is what verified:review requires)
  - Schrijver's actual instance (G2); the locators [R], [S80], [EG], [CLR] (G1, G3, G4)
```

Nothing in this file may be built on. Its author will not build on it either.

---

## Sources

See §8 for verification status of each.

1. H. E. Robbins, *Amer. Math. Monthly* 46 (1939), 281–283.
2. A. Schrijver, *Discrete Math.* 32 (1980), 213–214/215.
3. J. Edmonds, R. Giles, *Annals of Discrete Math.* 1 (1977), 185–204.
4. G. Cornuéjols, S. Liu, R. Ravi, *Combinatorica* 45 (2025), art. 32, arXiv:2311.04337.
5. `attacks/tau2-robbins/README.md` (this repo) — the sketch this file supersedes.
6. `attacks/zero-weight-frontier/README.md` and `experiments/woodall-zeroweight-census/` (this
   repo) — the census cited in §6.2, `numerical`.
