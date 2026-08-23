# Kill-criteria — `n16-budget`

Fixed **before any computation**, worker B1, 2026-08-22. Stated so that the outcome is
falsifiable rather than negotiable afterwards.

The lane recomputes the area budget of `../n16-covering-limit/`'s **Lemma S** with the per-side
piece counts **pinned to `(k_1,k_2,k_3) = (3,3,3)`** by Theorem N of `../n16-structure/`, using
that lane's *certified slab-LP* upper bound on `f`, independently reimplemented here.

## B1 — the point of the lane (primary)

If the pinned bound does **not** come out below the published **U2 = 4.914308**, the lead of
`../n16-structure/` §5.1 is dead: report that, say which branch was binding at the optimum, and
stop. Do not go looking for a third ingredient to rescue it.

## B2 — the tripwire that outranks everything

Any bound on `A_15` that lands **at or below `1 + 2*sqrt(3) = 4.4641016...`** is a **bug in my
argument**, never a result: `../n16-covering-2/`'s 15-piece covering certifies `A_15 >= 1+2*sqrt3`.
Asserted in code; the run must fail loudly rather than print such a number.

## B3 — the pinned ceiling must not be crossed

Exhibiting a certified **lower** bound `f_lo <= f` gives a budget Lemma S cannot refute, hence a
ceiling `X1'` on what the *pinned* lemma can ever prove. If the certified upper-bound computation
returns a value **below** `X1'`, one of the two is wrong; stop and find out which, rather than
publishing the smaller number. (`X1 = 4.836854` of `../n16-covering-limit/` is **not** the relevant
comparison: it was computed under the unpinned maximisation over `(k_e)`, which is a strictly
weaker hypothesis, so the pinned bound is *expected* to fall below it. Crossing `X1` is therefore
not by itself an inconsistency — crossing `X1'` is.)

## B4 — circularity

No value of `s(16)`, `d(16)`, `a_16`, no published or repo packing, and no covering number is an
input to any bound. The only imported mathematics is the isodiametric (Bieberbach) inequality.
`4.6247637` appears only as a comparison target. If any bound turns out to need such an input,
the bound is withdrawn, not relabelled.

## B5 — status honesty

The result depends on Theorem N, which is `sketch`. By `RULES.md` §3 the result is therefore
`sketch` too, however exact the arithmetic. If I catch myself writing it up as anything stronger,
that is the failure this criterion exists to catch.

## B6 — budget

45 minutes wall clock, <= 1 core for long runs. Over budget: report the partial grid and the
bound implied by it (a coarser `f` grid still yields a *valid* bound, only a weaker one).
