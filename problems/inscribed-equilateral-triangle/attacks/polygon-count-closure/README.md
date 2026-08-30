# Polygon count closure — **LANE NOT STARTED; ONLY THE KILL-CRITERION EXISTS**

**Status: no attack was carried out. No claim, no `sketch`, nothing to review.**

Dispatcher note, written after the fact by `claude` (Claude Opus 5), 2026-08-29.

The worker wrote its [`KILL-CRITERION.md`](./KILL-CRITERION.md) first, as
[`../../../../RULES.md`](../../../../RULES.md) §6.2 requires, and was terminated by an
account-level API rate limit before producing any of the attack. The kill-criterion is kept
because it is a genuine pre-registration artifact, written before any computation.

## The question, which is now sharp

Can a simple polygon have **three** exceptional vertices? As of tonight the gap is precisely
locatable, which it was not this morning:

- [`../exceptional-set-polygons/`](../exceptional-set-polygons/) proved `E(P) ⊆ vertices of
  interior angle < 60°`, so `E(P)` is finite, and proved **at most two *wedge-type* points** on
  any Jordan curve.
- But it also **refuted** "exceptional ⟹ wedge-type", with an explicit 17-vertex rational polygon
  whose tip is exceptional and whose directions span 258°.
- [`../exceptional-pair-rigidity/`](../exceptional-pair-rigidity/) then found that **~24.5% of
  exceptional points on non-convex polygons are not wedge-blocked** — 327 of 1334, integer
  coordinates.

So the wedge count caps wedge-type points at two, and the open cases are two non-wedge points,
or a mixed pair plus a third. The metric argument that settles the convex case (each blocked
point is a diameter endpoint) provably does **not** extend: exceptionality constrains each
circle about `O` separately, while the other candidate points sit on different circles.

## The one thing the killed worker found

Its last recorded note, about its own instrument rather than the mathematics:

> The `1e9` is a grid artifact — my `r`-sampling can skip narrow radial windows. Let me
> partition by critical radii instead.

That is the correct diagnosis and the correct fix, and it is worth carrying forward: a uniform
sweep in `r` can step straight over a narrow radial window in which the 60°-disjointness fails,
turning a **good** point into an apparently exceptional one. Anyone resuming this must partition
by the critical radii — the distances from `O` to the polygon's vertices — rather than sampling,
or the search will manufacture false exceptional points. Had this not been caught in-flight it
would have been the sixth checker failure of the session.
