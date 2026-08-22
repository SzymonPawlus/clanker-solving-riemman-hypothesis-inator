# Red-team audit of the $n=16$ campaign

**Claim type: neither construction nor optimality** (problem [`../../RULES.md`](../../RULES.md)
§1 asks for that sentence first). Nothing here bounds $s(16)$ in either direction. This is an
adversarial audit of the argument chain the campaign is standing on, of its *scope statements*
rather than only its arithmetic, and of its status graph. Nothing enters `results/`.

- Auditor: `claude` (Claude Opus 5), worker **R1**, 2026-08-22, issue
  [#97](https://github.com/SzymonPawlus/clanker-solving-riemman-hypothesis-inator/issues/97)
- Code: [`experiments/packing-n16-redteam/`](../../../../experiments/packing-n16-redteam/) —
  Python standard library only, exact $\mathbb{Q}(\sqrt3)$ arithmetic for every decision on the
  certificate; `decimal` at 40 digits for the comparison arithmetic
- Journal: [`notebook/claude/2026-08-22-n16-redteam.md`](../../../../notebook/claude/2026-08-22-n16-redteam.md)

> ## THIS GRANTS NO STATUS
>
> I am Claude Opus 5 and so is every author audited here. Repo
> [`RULES.md`](../../../../RULES.md) §5 requires an examiner from a **different model family**.
> Everything below — including everything I confirm — stays `sketch` and stays non-assumable,
> including by me. Confirmation here buys error-finding, not certification.

---

## 0. Verdict

**No blocking finding.** The headline chain is short, and I could not break it:

$$a_{16}\ \ge\ 1+2\sqrt3 = 4.464101615137754\ldots,\qquad
s(16)\ \ge\ 2+6\sqrt3 = 12.392304845413264\ldots$$

I re-derived the certificate **by hand-transcribing the polygon table out of
[`../n16-covering-2/README.md`](../n16-covering-2/README.md)** (not from the author's code) into
my own exact $\mathbb{Q}(\sqrt3)$ checker, and it passes every check including the ones that
matter. All four headline numbers reproduce. The separation-1 / separation-2 conversion — the
standing trap on this problem, and the one that produced a broadcast error on 2026-08-21 — is
**correct in every write-up in the campaign**, and correct in the live `n16-occupancy` capacity
table too.

What I did find is eleven scope and arithmetic corrections, and they are the same shape as every
entry in [`FINDINGS.md`](../../../../FINDINGS.md): *the arithmetic is right and the sentence after
it is one step too broad*. Two of them (the forced structure, and "the lane is exhausted")
currently tell the next worker to stop looking in the place most likely to still contain
something.

---

## 1. Findings

| severity | what | witness | where |
|---|---|---|---|
| **correction** | **"The coarse structure is forced … So the layout is 3 corner + 9 edge + 3 interior" is not proved.** The counting gives only $n_2\ge3$, $I\le n_2$, $n_1+2n_2\ge15$. The step used to exclude $n_2=6$ ("the middle $a-2$ of each side still needs $\ge3$ **more** pieces") assumes a two-side piece cannot reach a side's middle — it can. And $n_2\in\{4,5,7\}$ is never considered at all. | (a) the segment from $p=(\tfrac{21}{20},0)$ on $AB$ to $q=(\tfrac14,\tfrac{\sqrt3}4)$ on $AC$ has $\lvert pq\rvert^2=\tfrac{331}{400}$, i.e. $\lvert pq\rvert=0.909670<1$; it meets **both** sides and $p$ lies in $m_{AB}$ ($1.05>1$ from $A$, $3.414>1$ from $B$). So $M_{AB}$ and the two-side pieces are **not** disjoint. (b) $(n_1,n_2,I)=(7,4,4)$ satisfies every proved constraint. | [`../n16-covering-2/`](../n16-covering-2/) §"Why this is where the family stops" 1; [`../n16-dual/`](../n16-dual/) §"The structure of the optimum" ("That type is **forced**", then substitutes the *observed* $B_2=3$) |
| **correction** | **The Reuleaux-triangle row is false.** "A piece covering a length-$\ell\le D$ chunk of a side — **no penalty**, area up to $\tfrac{\pi-\sqrt3}2 D^2$ — put the Reuleaux triangle of width $D$ with its base on that side". A Reuleaux triangle's boundary contains no segment, so inside a closed half-plane it meets the boundary line in **exactly one point**; it cannot contain a chunk of positive length. | The correct cap at $\ell=D$ is $f(1)=\tfrac\pi3-\tfrac{\sqrt3}4=0.6141848$, computed exactly by the sibling lane [`../n16-covering-limit/`](../n16-covering-limit/) §3, which explicitly says the extremal set is the two-arc lens and "*not* a Reuleaux triangle". So an edge piece with a full-length trace is **below** the hexagon figure $3\sqrt3/8=0.6495191$, not $108\%$ of it. The standing certificate obeys this: its three trace-$1$ edge pieces have area $0.5669873$ each (`areas_traces.py`). | [`../n16-shapes/`](../n16-shapes/) §5 table, row 3; propagated into §5's "area forbids nothing" justification and §7's "**where the money is**: 1. the edge collar … a single boundary piece can reach $0.7048$ ($108\%$)" |
| **correction** | **Arithmetic slip.** "$\tfrac{\sqrt3}{4}a^2 \le 3\cdot\tfrac{\pi}{6} + 12\cdot\tfrac{3\sqrt3}{8} = 9.36499 \Rightarrow a \le 4.65194$". The stated budget gives $a\le4.6505482$. $4.65194$ corresponds to a per-piece cap of $0.6499862$, not $3\sqrt3/8=0.6495191$. | exact: $\tfrac{\sqrt3}4\cdot4.65194^2 = 9.370729 \neq 9.365025$; $\sqrt{4\cdot9.365025/\sqrt3}=4.6505482$ (`arith.py`) | [`../n16-dual/`](../n16-dual/) §"How much room is left" |
| **correction** | **"provably not tight" at $m=8$ is not proved.** What exists is an optimiser plateau at $2.97779$ from two solvers. $A_8\le a_9=3$ *is* proved (by the same pigeonhole, run backwards); $A_8<3$ is not — a sup need not be attained, and no quantitative gap was derived. | the file's own correct caveat, two paragraphs later: "the control does **not** license a claim that $4.464$ is the end of the road" | [`../n16-dual/`](../n16-dual/) §"Controls" |
| **correction** | **"the covering family … shown to be exhausted" / "Why this is where the family stops".** Three optimiser findings, all `sketch`, none of which bounds the family. The campaign's own triage document forbade exactly this inference in advance. | [`../approaches-round-2/`](../approaches-round-2/) §L (2026-08-18): "*a search that fails to find an $(n-1)$-cell cover does not prove that none exists* … report only 'certified lower estimate of $m$' and 'failed-search upper **impression**', never '$m(16)=$'". And [`../n16-shapes/`](../n16-shapes/) §7.2 says the opposite of the same day: "the plateau may be a property of that topology and not of the problem … 3/12/0 is **not** excluded by anything proved here" | [`../n16-covering-2/`](../n16-covering-2/), result section and §"Why this is where the family stops" |
| **correction** | **"Overlapping pieces buy nothing here"** (section heading) and "that closed a whole line of attack in two minutes" — the convex-relaxation argument is valid, but only **at one fixed combinatorial structure**, which the section's own last sentence says and the heading does not. The independent measurement in the sibling lane also does not establish it: there, the overlapping runs beat the convex-partition controls by $5\times10^{-5}$, *inside* the run-to-run spread of $3.7\times10^{-5}$. | [`../n16-covering-2/`](../n16-covering-2/) §2, last sentence ("at this structure"); [`../n16-shapes/`](../n16-shapes/) §6.3 ("**overlap is not demonstrated to help**") | [`../n16-covering-2/`](../n16-covering-2/) §"Why this is where the family stops" 2 |
| note | **Repo-internal prior art, uncited by all four lanes.** The dilation/limit repair that is this round's substantive content, and "pigeonhole needs a *cover*, not a partition — overlap is harmless", were both written down four days earlier, along with the target quantity ($m(n)$, the separation-2 form of $A_{15}$) that the lanes rediscovered. | [`../approaches-round-2/`](../approaches-round-2/) §J: "*for every $\lambda<1$, scaling by $\lambda$ carries it to a cover of $T_{\lambda d^*}$ by $n-1$ cells of diameter $\le2\lambda<2$, which by pigeonhole excludes $n$ points for every $d<d^*$. Hence $d(n)\ge d^*$ from **one** finite certificate*"; §L defines $m(n)$ and sets the threshold "$>8$", which $2(1+2\sqrt3)=8.9282$ clears | indexing, not mathematics — the same failure `FINDINGS.md` records for the Groemer equality clause |
| note | **External prior art: the *method* is published, and this repo already holds the citation.** Melissen (1993) proved $n=4,\dots,12$ "using only partitions and direct applications of Dirichlet's pigeon-hole principle" — stated in Tedeschi & Mackey (AJUR 2021), which [`../../README.md`](../../README.md) records as **read in full**. `FINDINGS.md` says the same ("Melissen uses hand-designed dissections plus pigeonhole"). So "novelty unverified" understates the position for the *method*; what is genuinely unchecked is only whether the specific 15-piece value at $n=16$ is published. | web search (§5); repo's own `cited` material | all four lanes' novelty sections |
| note | **Egress is more open than the campaign records.** Direct HTTPS to scholarly hosts *is* blocked (gateway answers 403 to `CONNECT`; confirmed for `ris.utwente.nl`, `link.springer.com`, `combinatorics.org`, `zbmath.org`), and `WebFetch` is blocked by the same proxy. But the **`WebSearch` tool works in this session** and returns literature summaries. Four lanes say novelty is "unverifiable from this session"; that is true of full texts, not of search. | §5 below | all four lanes |
| note | **"(verified)" on a number no certificate file supports.** [`../n16-covering/`](../n16-covering/)'s superseded banner reports $a_{16}\ge\frac{139503175473}{31250000000}=4.464101615136$ "(verified)", with the closed form $1+2\sqrt3$ as the thing merely "claimed". But the only strict rational certificate on disk is `cert_rational.json` at $a=\frac{446410161513599}{10^{14}}=4.46410161513599$, whose dilation gains $\approx2\times10^{-24}$ — it does **not** reach $4.464101615136$. That rational is a *consequence* of the closed-form limit argument, not an independent check of it, so the banner inverts its own dependency. "(verified)" is also not one of `RULES.md` §3's statuses. | `cert_rational.json`: `max_sq_diam` $=\frac{199282032302597545822661932801}{199282032302598438642984960000}$, so $a/\sqrt\Delta - a < 10^{-23}$ | [`../n16-covering/`](../n16-covering/) banner |
| note | **The §7 tripwire is rounded the wrong way.** Three kill-criteria fire at $a^\star>4.6247636$, but the published packing sits at $a=1/0.216227269309782=4.6247635795$. A certificate in $(4.6247635795,\,4.6247636]$ would pass the tripwire while being wrong. [`../n16-verification/`](../n16-verification/) uses the sharper figure; the three lanes do not. | $1/0.216227269309782 = 4.62476357950639$ | `n16-covering`, `n16-covering-2`, `n16-dual` kill-criteria |
| note | **The isodiametric inequality is carried as `cited` with no specific reference.** `RULES.md` §3 defines `cited` as "established in the literature, **with a specific reference**". It is the only imported mathematics in the whole ceiling lane. | [`../eo-covering-bound/`](../eo-covering-bound/) status table: "`cited` — standard" | inherited by `n16-covering-limit` U0/U2 and `n16-dual` |
| note | **Internal contradiction in a verdict box.** "*No bound derived from the structure lemma of §2 can ever prove $A_{15}\le 4.836854$*" — the §4 table says the opposite and is right: Lemma S can prove $A_{15}\le4.836854$ and nothing *smaller*. | §4 table row X1 vs the verdict box | [`../n16-covering-limit/`](../n16-covering-limit/) |

**None of these changes any number in the lower-bound chain.** The two that would change what the
next worker does are the first and the fifth: between them they retire the "3+9+3 is forced" and
"the family is exhausted" reasons for abandoning the 15-piece lane, and `n16-shapes` §7.2's
topology enumeration (3/10/2, 3/11/1, and — corrected — the $n_2\ge4$ families) is back on the
table. Note that $I\ge1$ *is* proved (the incentre sits at distance $a/(2\sqrt3)=1.289>1$ from
every side, so no boundary piece reaches it), which does kill 3/12/0.

---

## 2. The dependency graph of the $n=16$ lower bound

Edges point from dependency to dependent. Statuses are as the files themselves declare them.

```
  [reduction  s(n) = 2 sqrt3 + d(n),  a = d/2]            cited (problem README, elementary)
                  |
                  v
  [15 convex polygons over Q(sqrt3) at a = 1+2 sqrt3]     numerical (finite exact computation)
   - all in T_a, strictly convex, pairwise interior-disjoint
   - areas sum exactly to area(T_a)
   - max squared diameter EXACTLY 1
                  |
                  v
  [dilation by mu<1  =>  15 pieces of diameter mu<1        sketch  <-- the only prose step
   covering T_{mu a}, for every mu<1]
                  |
                  v
  [pigeonhole: T_b has no 16 points at pairwise            sketch
   distance >=1, for every b < 1+2 sqrt3]
                  |
                  v
  [ {b : 16 separated points fit in T_b} is upward         sketch
    closed  =>  a_16 >= 1+2 sqrt3 ]
                  |
                  v
  [ s(16) >= 2 + 6 sqrt3 ]                                 sketch     <-- HEADLINE
```

Everything to the side of that chain, and **not** in it:

| node | status as declared | actually an input to the bound? |
|---|---|---|
| Oler (1961), $s(16)\ge11.821918$ | `cited` | **no** — comparison row only |
| Lemma L, $a_{16}\ge5\sqrt3/2$ (`eo-covering-construct`, `n16-verification`) | `sketch` | **no** — superseded, not used |
| `n16-covering`'s certificate, $446335/99998$ | `sketch` | **no** — only sets `n16-covering-2`'s K1 threshold |
| `n16-shapes` §6.3 certificate, $4.463841021$ | `numerical` | **no** — weaker, independent |
| `n16-dual`'s certificate, $4.4640971380$ | `sketch` | **no** — weaker, independent |
| isodiametric (Bieberbach) | `cited` (no reference) | **no** — used only in the *ceiling* lane |
| Melissen–Schuur $a_{16}\le4.6247636$ | `numerical`, uncertified in-repo | **no** — tripwire and comparison only |
| $a_n$, $n\le15$, from the `cited` table | `cited` | **no** in the covering lanes; **yes** in the live `n16-occupancy` lane, correctly guarded (§4) |
| Theorem SI, Lemmas S and C (`n16-shapes`) | `sketch` | **no** — they justify a *restriction* being harmless, they do not enter the bound |
| Lemma S / $A_{15}\le4.914308$ (`n16-covering-limit`) | `sketch` | **no** — an obstruction to the method, in the opposite direction |

**Cap check (`RULES.md` §3).** The chain's weakest dependency is the certificate itself, and the
headline is declared `sketch` everywhere it appears. I found **no** step anywhere in the campaign
that treats the headline, or any predecessor's `sketch`, as assumable: the three superseded
certificates are never used as premises, only as thresholds and comparison rows, and every lane
re-certifies from scratch. The live `n16-occupancy` lane names it `sketch` in its K1. That is the
thing this campaign got right, and it is worth saying as plainly as the corrections above.

---

## 3. What I checked and found **sound**

Confirming a step is as useful as breaking one. All of the following I re-derived or recomputed
myself; where it says *exact*, every decision was a `Fraction` or $\mathbb{Q}(\sqrt3)$ sign test.

### 3.1 The certificate (`check_cov2.py`, `areas_traces.py`)

Polygons **hand-transcribed from the write-up's own table**, so this also checks that the
published table is the object the code verifies (it is — the table matches `exact_1p2r3.py`'s
`P`/`FACES` vertex-for-vertex).

| check | result |
|---|---|
| exactly 15 pieces | ok |
| every vertex in $T_a$, $a=1+2\sqrt3$ ($u,v\ge0$, $u+v\le a$) | ok |
| every piece simple, **strictly** convex, ccw | ok |
| max squared diameter over all vertex pairs of all pieces | **exactly 1**, and **every one** of the 15 is exactly 1 |
| all $\binom{15}2=105$ pairs interior-disjoint (exact Sutherland–Hodgman clipping) | ok, 0 overlapping pairs |
| areas sum exactly to $\operatorname{area}(T_a)$ | ok — $\sum 2\cdot$shoelace $=13+4\sqrt3=a^2$ exactly |
| 1891-point rational grid probe, offsets coprime to the certificate's denominators | ok, 0 uncovered |
| per-piece areas | $3\times\tfrac12$ exactly (corners), $0.5669873$–$0.6160254$ (edges), $0.5849365$–$0.5891016$ (interior) — reproduces the write-up's table |
| side division $1,\sqrt3-1,1,\sqrt3-1,1$ | ok, recovered independently from the traces |

### 3.2 The four headline numbers (`arith.py`, 40-digit `decimal`)

All four reproduce.

| | claimed | recomputed |
|---|---|---|
| Oler, $a_{16}\ge\frac{-3+\sqrt{129}}2$ | $4.178908$, $s\ge11.821918$ | $4.1789083458$, $s\ge11.8219183067$ |
| record, $a_{16}\ge1+2\sqrt3$ | $4.464101615137754$ | $4.4641016151377546$ |
| record, $s(16)\ge2+6\sqrt3$ | $12.392304845413264$ | $12.3923048454132638$ |
| upper, $s(16)\le12.713629 \Rightarrow a_{16}\le4.6247636$ | $4.6247636$ | $4.6247636924$ from the rounded $s$; $4.6247635795$ from G–L's $d(16)=0.216227269309782$ |

Sanity: $a_{15}=4 \le 1+2\sqrt3 \le 4.6247636 \le a_{16}^{\text{upper}}$, and $a_{22}\ge3\sqrt3=5.196152$ (Lemma L at $p=6$) against the best-known $1/0.179396908611866=5.5742$. Nothing overshoots.

### 3.3 The separation-1 / separation-2 conversion — the standing trap — in **every** write-up

$s=2a+2\sqrt3$ throughout ($d=s-2\sqrt3$ at separation 2, $a=d/2$ at separation 1). Checked at 40
digits for `n16-covering` ($12.3909801527$), `n16-covering-2` ($12.392304845$), `n16-dual`
($12.3922958911$), `n16-shapes` ($12.39178366$), Lemma L ($7\sqrt3=12.1243557$), Oler
($11.8219183$) and the upper bound. **Every one is right.** The `n16-verification` control table's
conversions of the `cited` $a_n$ ($n=4,7,11$) are right. The live `n16-occupancy` capacity table
($a_2=1$, $a_4=\sqrt3$, $a_5=2$, $a_7=1+\sqrt3$, $a_8=1+\sqrt{33}/3$, $a_9=3$,
$a_{11}=2+2\sqrt6/3$, $a_{12}=2+\sqrt3$, $a_{14}=4$) is right. The trap did not fire in this
campaign.

### 3.4 The strictness / equality-case argument — **sound**, and sharp on the case that breaks the naive version

This was the thing I most expected to break, and it does not.

- The **false** principle is "$T_a$ covered by $N$ sets of diameter $\le1$ $\Rightarrow$ $T_a$ has
  at most $N$ points at pairwise distance $\ge1$". Witness on the record: $T_{\sqrt3}$, three
  kites, diameters exactly $1$ (corner-to-centroid $=1$, corner-to-midpoint $=\sqrt3/2$,
  centroid-to-midpoint $=1/2$), and four separated points.
- The principle actually used is different and is a **theorem**: if $T_{a_0}=\bigcup_1^N S_i$ with
  $\operatorname{diam}S_i\le1$, then for every $\mu<1$ the dilation about the corner-anchored
  origin gives $T_{\mu a_0}=\bigcup\mu S_i$ with $\operatorname{diam}\mu S_i\le\mu<1$, so no
  $N+1$ separated points fit in $T_b$ for any $b<a_0$. The feasible set
  $\{b: N{+}1 \text{ separated points fit in } T_b\}$ is upward closed (because
  $T_b\subseteq T_{b'}$ for $b\le b'$ at the fixed placement), so its infimum is $\ge a_0$, i.e.
  $a_{N+1}\ge a_0$ — **with equality included**, and with no compactness needed.
- On the witness above it returns $a_4\ge\sqrt3$, and $a_4=\sqrt3$ exactly. The argument is
  **sharp on the configuration that kills the naive one**, which is the right test and is the one
  the write-up nominates.
- Nothing in the campaign claims $T_{1+2\sqrt3}$ itself holds no 16 separated points, which would
  be the over-reach. I checked every occurrence.

### 3.5 Circularity (`FINDINGS.md`'s top entry) — clean in the covering lanes

- No table of known $a_n$ / $d(n)$ / $s(n)$ appears anywhere in
  `experiments/packing-n16-{covering,covering-2,shapes,dual,limit}/`. Grepped.
- $4.6247636$ appears in the code only as `CEILING` in tripwire assertions and in reporting
  lines — never on the left of an inequality that produces a bound. Checked every occurrence in
  `experiments/`.
- The live `n16-occupancy` lane is the one where the failure mode is real (it uses `cited` $a_k$
  as capacity inputs). Its guard is a named constant, `CAP_MAX_INDEX_FOR(n) = n-1`, enforced at
  the table lookup; at $n=16$ the largest usable entry is $a_{14}=4$ and the whole triangle is
  $4.46>4$, so no whole-region prune is available and the conclusion cannot be fed back in. The
  guard is real, not decorative.

### 3.6 Individual lemmas re-derived

| statement | verdict |
|---|---|
| **Theorem SI** (`n16-shapes` §3): covering by $N$ sets of diameter $<1$ $\iff$ by $N$ convex polygons $\iff$ partition into $N$ sets | **sound**. $D=\max_i\operatorname{diam}S_i<1$ needs finiteness — used correctly; the regular hexagon of inradius $\varepsilon$ has diameter $4\varepsilon/\sqrt3$ — correct; $\operatorname{diam}(Q\oplus E)\le\operatorname{diam}Q+\operatorname{diam}E$ — correct; $\operatorname{diam}\operatorname{conv}=\operatorname{diam}$ at a vertex pair — correct. It is **not** a limiting statement and does not lose an $\varepsilon$ of side length, as claimed. The scope sentences around it are right too: it leaves overlap open and says so. |
| **Lemma S** (`n16-shapes` §2): $\operatorname{diam}$ of the $60^\circ$ sector of radius $r$ is exactly $r$ | **sound**. $\rho_1^2+\rho_2^2-\rho_1\rho_2$ is separately convex, so maximised at a corner of $[0,r]^2$; the $61^\circ$ control is the right control. |
| **Lemma C** (`n16-shapes` §2): a piece of diameter $\le D$ containing a corner has area $\le\pi D^2/6$ | **sound**. |
| polygonal-sector areas $A_n=\tfrac n2\sin\frac{60^\circ}{n}r^2$ | **sound**, all seven values reproduce. |
| **Lemma S** (`n16-covering-limit` §2): the corner/edge/interior structure inequality | **sound in every step I checked**: (a) $B(V,1)\cap T_a$ is the unit $60^\circ$ sector for $a\ge2$; (b) $\sqrt{s^2-st+t^2}$ on $s,t\ge1$ is minimised only at $(1,1)$ with value $1$, so no piece meets two side-middles; (c) $\sum\ell_i\ge a-2$ and $\lvert M_e\rvert\ge3$; (d) $f$ non-increasing by convexity, Jensen in the right direction. |
| $f(1)=\tfrac\pi3-\tfrac{\sqrt3}4=0.6141848$ exactly, extremal set the two-arc lens | **sound**, and it is the witness against `n16-shapes` §5 (finding 2). Independent consistency check: the standing certificate's three trace-$1$ edge pieces have area $0.5669873<f(1)$, and its trace-$0.732$ pieces have $0.6160254$ — the certificate satisfies a bound derived in a different lane by a different route. |
| the **Kershner-density refutation** (`n16-covering-limit` §5) | **sound, and correctly scoped**. Regular hexagons of diameter $1$ do tile the plane with density $1$ and area $3\sqrt3/8$ each, so a circle-covering density constant cannot bound them. The file then says the *conclusion* $3\sqrt3/8$ may still be true and is open here — which is the right amount of caution, and is what the corner-deficit and boundary-counting closures also do. |
| Fejes Tóth hexagon bound $\Rightarrow15A_6=10.124715$, $a\le4.8355$ | arithmetic **reproduces** ($4.8354966$ against $4.835498$ stated; the difference is a deliberate upward rounding of $A_6$, which weakens the author's own conclusion — correct practice, not an error). Same for X2 ($4.7258037$ vs $4.725804$). |
| area ceilings U0 $=5.2160321$, U1 $=5.0391657$, hexagon $=4.7434165$, and the gap arithmetic $0.481320$, $0.377761$, $0.103559$, $95.06\%$, $51/64/83\%$ | all **reproduce** exactly |
| `n16-dual`'s $m=3$ control, $866025399/500000000=1.7320507980<\sqrt3$ | **sound** and is the sharpest control in the campaign |

---

## 4. What I could not check, and why

- **Whether $1+2\sqrt3$ is optimal for 15 pieces.** Not claimed by anyone, and I did not attempt a
  search — that is another worker's lane and duplicating it would be manufactured work. My
  finding is only that the *reasons given* for believing it is optimal do not support the weight
  placed on them.
- **The literature, beyond search summaries.** `WebSearch` works; `WebFetch` and direct HTTPS do
  not (403 at the gateway on `CONNECT`). I could not read Melissen–Schuur (1995), Melissen (1993),
  Melissen's thesis, or Graham–Lubachevsky, so I cannot say whether a 15-piece covering giving
  $1+2\sqrt3$ at $n=16$ is published. **Assume it is until someone with library access says
  otherwise.** What search did establish — that the partition-plus-pigeonhole *method* is the
  published standard for these proofs — is in §5.
- **The other lanes' code**, beyond the greps reported in §3.5 and the certificate data. I
  re-derived from write-ups and data, not from their implementations; that is deliberate, but it
  means a bug living only in a script that produced a number I did not recompute would be
  invisible to me.
- **`n16-covering-limit` §3's slab LP and its rational dual certificates.** I checked the two
  closed-form endpoints ($f(1)$ exactly, and the explicit disk lower bound's form) and the shape
  of the argument, not the 128-slab LPs or their dual repair. Nothing in the lower-bound chain
  depends on them.
- **The live lanes** `n16-covering-max`, `n16-mixed-capacity`, `n16-verification-3`, and
  `n16-occupancy`'s results: no write-up existed at the close of this pass. I audited
  `n16-occupancy`'s kill-criterion and its capacity table and circularity guard only (both sound,
  §3.3 and §3.5).
- **Anything about $n\ne16$.** The earlier `eo-*` closures (corner-deficit, boundary-counting,
  hull-deficit) were read for their scope statements only. Each carries explicit hedges, names its
  own near-miss, and records the circular result its author caught — I found nothing to add and
  did not re-derive them.

---

## 5. Novelty, honestly scoped

**Assume this is known.** Two things sharpen the campaign's own wording.

1. **The method is published, and this repo already holds the citation.** Melissen (1993) proved
   the optimal placements of $4$ through $12$ points in an equilateral triangle *"using only
   partitions and direct applications of Dirichlet's pigeon-hole principle"* — reported in
   Tedeschi & Mackey, *On Packing Thirteen Points in an Equilateral Triangle*, AJUR **18**(2)
   (2021) 3–12, which [`../../README.md`](../../README.md) records as **read in full, open
   access**. `FINDINGS.md` says the same thing in its Oler entry. So "novelty unverified" is
   weaker than what is known: partition + pigeonhole *is* the standard published technique for
   exactly this problem, and the only open novelty question is the specific 15-piece configuration
   and the value $1+2\sqrt3$ at $n=16$.
2. **What still needs checking, and where.** (i) Does Melissen–Schuur (1995), *Packing 16, 17 or 18
   circles in an equilateral triangle*, Discrete Math. **145**, 333–342, contain any **lower**
   bound for $n=16$, or only constructions? (ii) Does Melissen's 1997 Utrecht thesis *Packing and
   covering with circles* record the best pigeonhole/partition bound for $n=16$? (iii) Is the
   auxiliary quantity — least maximum diameter of a $15$-piece partition of an equilateral
   triangle — tabulated anywhere? It is a natural Borsuk-flavoured problem and $\delta(3)=1/\sqrt3$
   is certainly classical. (iv) Melissen, *Loosest circle coverings of an equilateral triangle*,
   Math. Mag. (1997), surfaced in search and has not been looked at by anyone here.
   None of (i)–(iv) is answerable without a library; all four are one PDF each.

**Egress, stated precisely, because four files state it too broadly.** The agent proxy answers
`403` to `CONNECT` for scholarly hosts (verified this session for `ris.utwente.nl`,
`link.springer.com`, `www.combinatorics.org`, `zbmath.org`), and `WebFetch` fails with
`EGRESS_BLOCKED` on the same hosts. **`WebSearch` is not blocked** and returned the Melissen
pigeonhole sentence above. "Unverifiable from this session" should read "full texts are
unreachable; search summaries are not".

---

## 6. Reproduce

```bash
python3 experiments/packing-n16-redteam/check_cov2.py     # exact Q(sqrt3) re-verification, ~10 s
python3 experiments/packing-n16-redteam/areas_traces.py   # per-piece areas and traces vs f(l)
python3 experiments/packing-n16-redteam/arith.py          # 40-digit checks of every quoted number
python3 experiments/packing-n16-redteam/cmp_code.py       # my table transcription vs exact_1p2r3.py
```

Python standard library only (`fractions`, `decimal`, `itertools`). No seeds, no tolerances, no
network, no float in any decision. `check_cov2.py` exits non-zero on any failure.
