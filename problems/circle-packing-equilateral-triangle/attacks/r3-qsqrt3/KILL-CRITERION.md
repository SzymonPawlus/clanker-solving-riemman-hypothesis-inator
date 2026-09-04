# Kill-criterion — approach Y (`r3-qsqrt3`)

```
status: numerical
author: claude (Opus 5), worker r3-qsqrt3, 2026-08-23
```

## As assigned

> If the exact contact system at $n = 17$ is inconsistent over $\mathbb{Q}(\sqrt3)$ — i.e. the
> conjectured closed form $s(17) = 6 + 4\sqrt3$ is **not** attained by the contact structure the
> optimiser actually finds — stop and report that as the finding. It would mean the table's
> $n = 17$ row is not what it appears to be. Do not force a fit.
>
> Secondary: if the system is consistent but the certificate cannot be made tight, deliver the
> honest untight upper bound and say which it is.

## Verdict: **did not fire.**

Both branches were tested and both came back negative (i.e. favourable).

### Branch 1 — consistency over $\mathbb{Q}(\sqrt3)$

The contact structure the optimiser finds at $n = 17$ **is** attained at $d = 6 + 2\sqrt3$. 16 of
the 17 points snap to $\mathbb{Q}(\sqrt3)$ with numerators $\le 10$ and residuals $\le 3.6\times
10^{-15}$, against a *proven* separation of $4.6\times10^{-3}$ between distinct lattice values at
the search height (`snap.py`). At those exact coordinates all 136 squared separations are $\ge 4$
in exact arithmetic, with minimum **exactly** 4, and all 17 containments hold in the closed
triangle. No fit was forced: nothing was adjusted to make the check pass, and the one point that
does not snap was *not* coerced — see below.

The same held at $n = 24$ (24/24 snap, no rattler) and $n = 31$ (30/31 snap).

### Branch 2 — tightness

The certificate is tight, so the fallback was not needed. The exact minimal enclosing side
$d_{\min} = \max_i (x_i + y_i\sqrt3/3)$ was computed in exact arithmetic and equals the declared
$d$ in all three cases — it was not asserted, and it is not the $\approx 10^{-11}$-inflated value
the repo's existing generator produces.

## The one thing that could have looked like the kill-criterion firing, and did not

At $n = 17$ and $n = 31$, exactly one coordinate pair each **fails to snap**, with residual
$\approx 3\times10^{-3}$ — three orders of magnitude above every other residual and above the
proven lattice separation. Taken at face value that is the kill-criterion's signature: a point of
the optimiser's configuration that is not in $\mathbb{Q}(\sqrt3)$.

It is not, and the reason is checkable rather than a judgement call. In both cases the flagged
point is a **rattler**: at the optimiser's own float position its nearest neighbour is at distance
$2.300$ ($n = 17$) and $2.134$ ($n = 31$), and it has strict slack in all three wall constraints
(smallest wall slack $0.110$ at $n = 17$, $0.166$ at $n = 31$). A rattler's free region is open
and of positive measure, so it has no determined position at all — the optimiser's float value for
it is an artifact of where the dynamics happened to stop, and there is nothing there to snap to.
Problem `RULES.md` §5 is explicit that rattlers are normal and are not to be "fixed".

The distinction that matters: the flagged point was **not** rounded into place to rescue the fit.
It was replaced by an independently chosen exact point of its free region — $(5/2, 4)$ at
$n = 17$ (clearance $2.322$), $(7, 0)$ at $n = 31$ (clearance $2.268$, sitting exactly on edge
$AB$, which the closed-triangle convention permits) — and that replacement is then verified
exactly along with everything else, by the same check as every other point. Had the flagged point been a *contact* point, this move would have been
illegitimate and the criterion would have fired.

## Residual risk this leaves

If a flagged point were in fact a contact point whose true coordinates have larger height in
$\mathbb{Q}(\sqrt3)$, or lie outside $\mathbb{Q}(\sqrt3)$ entirely, then the certificate would
still be a valid construction (the exact check does not care where the coordinates came from),
but the configuration would not be the published one and the claim "this reproduces the published
packing" would be wrong. The clearance measurements above are what rule that out. They are float
measurements of *strict* inequalities with margins of $0.30$ (separation) and $0.11$ (wall) at
$n = 17$, and $0.13$ and $0.17$ at $n = 31$ — comfortably above float noise at $10^{-15}$, but
stated numerically so a reviewer can re-measure them rather than take them.
