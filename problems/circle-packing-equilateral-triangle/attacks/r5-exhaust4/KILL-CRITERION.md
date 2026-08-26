# Kill-criterion — r5-exhaust4 (round-4 proposal AF)

## Stated in advance (from the assignment)

> If the exhaustion cannot be pushed past $a > 2.95$ — i.e. the "measured-cheap" part turns out
> not to be cheap — record how far it got, the cost scaling, and the specific configurations that
> survive, and STOP. AF itself states a ceiling at $k = 6$ in advance; if you find the ceiling is
> much lower (e.g. the method stalls well above 2.95 even at $k = 4$), **that is the finding**.

## Verdict: **fired — but in the opposite direction from the one anticipated, and the finding is stronger than a stall**

The cheap half was cheap and was over-delivered; the endgame half is not expensive but
**impossible**, and that is now a theorem rather than a measurement.

### 1. The "measured-cheap" half did not fire

$a > 2.95$ was reached in 108 s / 569 301 nodes and then passed: $a > 2.97$ in 112 s / 680 793
nodes and **$a > 2.99$ in 387 s / 1 275 604 nodes**, i.e. $d(9) > 5.98$ — better than the repo's
previous best of 5.9. $a = 2.999$ timed out at 600 s with 26 live branches and proves nothing. The cost is close to flat over that interval, so the
trigger condition ("turns out not to be cheap") is false. This half is an **independent
reproduction** of `attacks/eo-exhaustion/` §4's $k=4$ row, obtained with code written from the
problem statement, not from theirs.

### 2. The endgame half fired, and the ceiling is $k = 3$, not $k = 6$

AF pre-declared a ceiling at $k = 6$. The real ceiling is $k = 3$, and it is provable rather than
measured:

* **Theorem 2** (`README.md` §4): for every level $L \ge 2$ there is an explicit node — the nine
  cells containing the $\Delta(4)$ lattice minus one point — that no rule in the family (pair,
  capacity, Oler-hull, strict or closed) refutes. So the exhaustion **cannot terminate at any
  resolution and under any compute budget**. The Oler-hull bound at that node converges to exactly
  $9$ from above, with a deficit $\Theta(2^{-L})$ that is always positive.
* **Proposition 3** (`README.md` §4.4): the dyadic pigeonhole closes EO($k$) iff $k^2-5k+4<0$, i.e.
  iff $k \le 3$. At $k = 3$ it closes in one node; at $k = 4$ refinement makes the count
  monotonically *worse*, and the coarsest bound misses by exactly the $+1$.

### 3. Consequence for the board

Combined with `attacks/eo-exhaustion/` §1.1 (finitely many fixed-rational-side refutations never
imply EO($k$) — re-derived here independently), the dyadic-cell route is closed **on both
branches**:

| branch | terminates? | proves EO(4)? |
|---|---|---|
| fixed rational side $a<3$ | yes, cheaply | **no** — monotonicity + finiteness (`eo-exhaustion` §1.1) |
| uniform in $a$ (strict, $t=1/3$) | **no, at any level** — Theorem 2 | would, if it terminated |

So **the mechanised-Melissen route via dyadic cell exhaustion is not viable**, which is what the
assignment says would be the valuable negative. It is a *narrow* negative and the write-up says so:
it does not touch non-dyadic partitions (§6), and in particular it does not touch the covering
question that the sibling lane attacks by a different mechanism.

### 4. What was not done

No attempt was made to mechanise a rigidity/uniqueness theorem or a 1-D chain lemma. Theorem 2
says a cell exhaustion cannot supply either, and the assignment's discipline is to stop when the
criterion fires rather than re-scope. `README.md` §6 records precisely what such an argument would
have to look like, including the observation — which I could not find recorded in the repo — that
**no triangle has capacity exactly 2** (because $a(2)=a(3)$), so any partition-and-capacity closure
must use non-triangular pieces.
