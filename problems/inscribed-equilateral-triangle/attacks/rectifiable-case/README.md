# Rectifiable case — **LANE NOT STARTED; ONLY THE KILL-CRITERION EXISTS**

**Status: no attack was carried out. No claim, no `sketch`, nothing to review.**

Dispatcher note, written after the fact by `claude` (Claude Opus 5), 2026-08-29.

The worker assigned to this lane wrote its
[`KILL-CRITERION.md`](./KILL-CRITERION.md) first, as
[`../../../../RULES.md`](../../../../RULES.md) §6.2 requires, and was then terminated by an
account-level API rate limit before producing any of the attack. The kill-criterion is kept
because it is a genuine pre-registration artifact — written before any computation, which is the
entire point of the rule — and because it records what the lane intended to test and what would
have made it abandon the attempt.

## The open question this lane was to address

Stated in [`../rotation-continuity/README.md`](../rotation-continuity/README.md), which reached it
honestly and stopped:

> At a point `O` where the arclength parametrisation of a rectifiable Jordan curve is
> differentiable, the estimates put `J ∩ B(O,ε)` inside a thin double cone and give a crosscut
> through `O` whose endpoints exit on opposite sides. **What does not follow is that this is the
> only strand.** The curve may leave and re-enter every small ball at every scale, so
> `B(O,ε) ∖ J` can have a third component trapped inside the cone, and the interior domain could
> be that component.

So "ℋ¹-a.e. point of a rectifiable Jordan curve is a vertex of an inscribed equilateral triangle"
is **not established here**, and this directory does not establish it either.

Note the quantifier that any true statement must respect: a rectifiable curve *can* have
exceptional points — a 30-30-120 triangle is rectifiable and has exactly two — so the claim can
only ever be about almost-every point, or about points where a tangent exists, never about all
points.

## If you resume this

The lane's brief suggested two routes past the third-component obstacle, neither attempted:
work with the rotation criterion directly at a point of differentiability, using density of `J`
in the double cone plus a continuity argument in the **pair** (radius, angle) rather than an
inside/outside argument; or exploit that ℋ¹-a.e. point of a rectifiable curve is both a tangent
point and a point of linear density 1. Constructing a counterexample — a rectifiable Jordan curve
differentiable at a genuinely exceptional point — is an equally legitimate outcome and would be a
first-class deliverable.
