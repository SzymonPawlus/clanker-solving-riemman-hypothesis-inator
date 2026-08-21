# Kill-criteria — the ceiling of the 15-piece covering method

**Written before any computation** (repo `RULES.md` §6.2). Worker C4, `claude` (Claude Opus 5),
2026-08-22, branch `claude/circle-equklatetal-problem-sa7tx7`.

## The quantity

$$A_{15}\ :=\ \sup\{\,a>0\ :\ T_a \text{ can be covered by 15 sets of diameter}<1\,\}$$

where $T_a$ is the closed equilateral triangle of side $a$ (separation-1 normalisation, as in
[`../n16-covering/`](../n16-covering/) and [`../eo-covering-bound/`](../eo-covering-bound/) — **not**
the separation-2 convention of `results/`).

The covering route to $a_{16}\ge a$ can never prove more than $a_{16}\ge A_{15}$. Two soft ends are
known to the team:

| | value | why |
|---|---|---|
| best certified covering (repo record) | $a^\star = 4.46335$ | $A_{15}\ge 4.46335$ |
| Melissen–Schuur 16-point packing | $4.6247636$ | $A_{15}\le 4.6247636$ |

**This lane attacks the upper end.** A proof of $A_{15} < 4.6247636$ closes the method for $n=16$.

## Criteria

- **K1 (primary, no-progress).** If the best bound I can prove from ingredients that are either
  *proved here* or `cited` **and independently checkable in this session** is $\ge 4.6247636$, the
  lane has **not** closed the method. Report the number and the reason it stalls; do **not**
  re-scope into constructing coverings (that is another worker's lane), into packing search, or
  into "one more weight function".
- **K2 (circularity — the specific trap in this lane).** No bound may take as an input a published
  or repo value of $s(n)$, $d(n)$, $a_n$, or a covering number, for any $n$. Those quantities
  *contain* the statement being derived (`FINDINGS.md`, "A `cited` input contained the
  conclusion"). Permitted inputs: geometry proved here, the isodiametric inequality, and explicit
  configurations verified here from scratch. If a bound turns out to depend on such a value,
  discard the bound rather than repair it.
  - The one legitimate use of a packing is the *direction* $A_{15}<a$ from an **explicit** 16-point
    1-separated configuration in $T_a$. That is self-certifying and non-circular, but it is a
    packing record claim; per problem `RULES.md` §4 and repo §7 it may only be reported as a
    candidate, never as a result, and it is not what this lane is for.
- **K3 (§7 tripwire, both directions).**
  - If I derive $A_{15} < 4.46335$, that contradicts the repo's exactly certified 15-piece covering
    of $T_{4.46335}$. **That is a bug in my argument, not a refutation of the certificate.** Stop
    and find it.
  - If I derive $A_{15} \ge 4.6247636$ **as a lower bound**, that would refute a published packing.
    Same verdict: bug first.
- **K4 (citation dependence).** If the only route below $4.6247636$ runs through a literature
  statement I cannot obtain and check in this session (network egress to scholarly hosts is blocked
  — [`../eo-literature/`](../eo-literature/)), the resulting number is **conditional**, is reported
  as such, and does **not** license telling the team to stop. A remembered theorem is not a `cited`
  one.
- **K5 (budget).** One hour of unattended compute (repo `RULES.md` §6.6). Every decision in exact
  rational arithmetic; $\pi$ and $\sqrt3$ enter only as certified rational enclosures rounded in
  the direction that **weakens** my conclusion.

## What would count as success

In decreasing order:

1. $A_{15} < 4.6247636$ proved — the method cannot solve $n=16$; the team should stop.
2. A bound below $4.6247636$ that is conditional on a named, unverified citation — the team gets a
   quantified expectation and a specific PDF to fetch.
3. A rigorous bound above $4.6247636$ — the method survives, with the headroom measured.
4. "I could not beat the trivial $5.2163$" — still worth reporting plainly.
