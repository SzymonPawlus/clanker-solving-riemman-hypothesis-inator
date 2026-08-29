# Kill-criterion — `extremal-size`

**Written before any computation in this lane.** Nothing in this file was revised after a
number came back; the outcomes are recorded in [`README.md`](./README.md) §10, which says
which of K1–K6 fired. (`../../../../RULES.md` §6.2, this problem's
[`RULES.md`](../../RULES.md) §6.)

- Lane: **quantitative / extremal** — idea **I6** of
  [`../ideation-round-1/README.md`](../ideation-round-1/README.md).
- Author: `claude` (Claude Opus 5), 2026-08-29, branch
  `claude/inscribe-equilateral-triangle-oj15x1`.
- Files this lane owns: this file, `README.md`, and
  `notebook/claude/2026-08-29-iet-extremal.md`. Nothing else.

---

## The question this lane was dispatched on

For a Jordan curve $J$ write

$$m(J) \;=\; \sup\{\,s : \text{some nondegenerate equilateral triangle of side } s
\text{ has all three vertices on } J\,\},$$

and, for a scale-1-homogeneous normalising functional $N$ (diameter, perimeter,
$\sqrt{\text{area}}$, width of the convex hull, inradius of the interior, …), ask for

$$\mu_N \;=\; \inf\{\, m(J)/N(J) \;:\; J \text{ a Jordan curve},\ N(J) > 0 \,\}.$$

The dispatch brief named diameter first and explicitly required the normalisation to be
checked for degeneracy **before** any optimisation. That is K1, and it is the criterion most
likely to fire.

---

## Kill conditions

**K1 — the normalisation is degenerate.** If $\mu_N = 0$ for the normalisation under
consideration, the extremal question *for that $N$* is empty and no amount of computation
makes it interesting. On firing: **record the witness, state $\mu_N = 0$ as the answer, and
move to the next normalisation** rather than optimising inside an empty problem. A degenerate
normalisation is a result (`../../../../RULES.md` §0), not a failure — but it must be reported
as "the question as posed is empty", never quietly replaced by a different question with the
same name.

**K2 — every normalisation is degenerate.** If K1 fires for *every* candidate $N$ that is
bounded above by a constant times the diameter, and also for the local-thickness candidates
(inradius), then there is no quantitative theorem of this shape for general Jordan curves at
all. On firing: write that up and **stop the general-curve half of the lane**. Do not invent
an exotic functional to keep the lane alive; that is re-scoping an attack to survive its own
falsification (`../../../../RULES.md` §6.3).

**K3 — the surviving question is already the convex one, and the convex constant resists.**
If the only non-degenerate formulation is the convex one (I6's conjecture), and one exact
computation session over convex polygons neither beats the best hand candidate nor produces a
plausible closed form, **park it with the numbers reported** and an honest interval. I6's own
kill says the same thing about the general half; this is its convex twin.

**K4 — a claimed lower bound survives the square substitution.** If any lower-bound argument I
produce still reads correctly with "square" for "equilateral triangle" *including its
existence content*, it is wrong (this problem's [`RULES.md`](../../RULES.md) §3.2). On firing:
mark the argument `refuted`, name the step that transferred, and do not repair it in place.
Note the asymmetry that makes this criterion sharp here: **upper** bounds on $m$ (witnesses)
transfer to squares harmlessly because they assert no existence, while **lower** bounds do
not. So K4 is a filter on the lower-bound half only, and an upper-bound witness passing the
square test proves nothing about the lower-bound half.

**K5 — the lower bound is built on a `sketch`.** The dispatch brief points at Theorem T of
[`../rectifiable-case/`](../rectifiable-case/), which is `sketch` and therefore not assumable,
including by me (`../../../../RULES.md` §3). If a lower bound cannot be re-derived from scratch
without it, the bound does not exist. On firing: state the bound as *conditional on a
re-derivation not performed*, i.e. do not state it.

**K6 — the exact constant appears to be in reach.** This is a *stop-and-flag* criterion, not a
stop-and-abandon one. If at any point it looks as though the exact value of $\mu_N$ for
**general** Jordan curves has been determined, `../../../../RULES.md` §7 applies: report as
"this appears to show", name the least-trusted step, do not announce, and hand it to review.
The base rate says the likeliest explanations are a smuggled regularity hypothesis (this
problem's [`RULES.md`](../../RULES.md) §1) or a normalisation that is not what I think it is.

---

## What would *not* kill the lane

- A gap between the lower and upper bound. An interval with a clean witness at the top and a
  clean argument at the bottom is the expected deliverable, not a failure.
- Failing to find the constant in the literature. That is "not found", never "open"
  (this problem's [`RULES.md`](../../RULES.md) §6.1).
- The extremal shape not being recognisable in closed form. Report the numbers.

## Compute budget

One hour unattended (`../../../../RULES.md` §6.6). Search may use floating point; **no reported
decision may**, and no `sympy` geometry predicate is used anywhere (this problem's
[`RULES.md`](../../RULES.md) §5 — sympy was wrong on 3 of 176 boundary cases here). This lane
owns no file under `experiments/`, so anything it computes is scratch: any script it relies on
is reproduced verbatim in `README.md` so that the numbers are checkable, and the numbers are
reported as *search output*, not as committed `numerical` results.
