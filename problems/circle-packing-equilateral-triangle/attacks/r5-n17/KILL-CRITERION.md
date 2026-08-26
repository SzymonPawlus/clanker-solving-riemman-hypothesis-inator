# Kill-criterion — r5-n17 (audit of the `n = 17` cert/generator disagreement)

## As stated in the assignment

This lane is an audit, so a clean "explained, benign, here is the reason" is a complete result and
there is no ordinary kill. One trigger was stated, and it is the loud one:

> If **either** configuration is actually infeasible, not tight, or misreported, STOP and report
> that immediately and loudly — it would invalidate a merged sibling result and possibly the
> certificate schema's interpretation, and it must not be buried in a longer write-up.

## Verdict: **did not fire**

Checked with a checker written from the problem statement (not from either author's code) and
validated first on four proven optima (`n = 3, 4, 6, 10`) and five negative controls:

| `n` | configuration | pairs | feasible | min sq dist | tight |
|---:|---|--:|:--|:--|:--|
| 17 | `r3-qsqrt3` certificate | 136 | yes | exactly 4 | yes, `d_min = 6 + 2√3` |
| 17 | famcert generator `j = 3` | 136 | yes | exactly 4 | yes, `d_min = 6 + 2√3` |
| 24 | `r3-qsqrt3` certificate | 276 | yes | exactly 4 | yes, `d_min = 8 + 2√3` |
| 24 | famcert generator `j = 4` | 276 | yes | exactly 4 | yes, `d_min = 8 + 2√3` |
| 31 | `r3-qsqrt3` certificate | 465 | yes | exactly 4 | yes, `d_min = 10 + 2√3` |
| 31 | famcert generator `j = 5` | 465 | yes | exactly 4 | yes, `d_min = 10 + 2√3` |

Additionally the famcert generator re-verifies feasible and tight at `j = 6, 7` (`n = 40, 49`),
with contact counts 84 and 106, matching that lane's Gate-2 table.

**Nothing is misreported in a load-bearing way.** The `12/17`, `30/31` and `24/24` overlap figures
in `attacks/r4-famcert/README.md` §1 are all confirmed independently, as are the contact/boundary/
rattler counts in `attacks/r3-qsqrt3/README.md` §2. One **wording** narrowing is recorded in
README §4.2 — the `n = 31` rattler is on wall `AB` in the committed certificate, not strictly
interior as that README's prose implies — which changes no number in either table but does change
what a rattler-census script will report. It is a definitional clarification, not a defect, and it
is not grounds for firing this trigger.

## Scope of the non-firing

Not firing means both point sets are exactly what they claim to be. It does **not** mean:

- that `6 + 4√3`, `8 + 4√3`, `10 + 4√3` are optimal (nothing here touches lower bounds);
- that these are the only packings at those side lengths (only two were compared);
- that any of this is assumable — `numerical`, same model family as both authors, so problem
  `RULES.md` §3's independent cross-family checker is still owed and nothing is promoted.
