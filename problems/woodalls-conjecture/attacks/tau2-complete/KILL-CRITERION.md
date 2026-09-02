# Kill-criterion for `tau2-complete` (issue #152)

Stated before the write-up was produced, per `RULES.md` §6.2; accounted for at the end of
`README.md` §9.

**K1 — Schrijver filter (decisive).** The write-up must name one step of the proof that is
*false* once arcs carry weights in `{0,1}` (weight-0 arcs kept, packing required to avoid them),
and it must show that step failing. If no such step can be exhibited, the argument would prove
the Edmonds–Giles conjecture, which Schrijver refuted at exactly `tau = 2`; the approach is then
`refuted`, the write-up records where the weighted version would go through, and work stops.

**K2 — Lucchesi–Younger filter.** If any step turns out to rely on "min dijoin = max disjoint
dicuts" (or on a lemma equivalent to it) in the direction being proved, the approach is `refuted`.

**K3 — Easy direction.** If the argument only shows that at most two disjoint dijoins exist, it
is not an attack and is `refuted`.

**K4 — Elementary step fails.** If any of the four internal lemmas (condensation
correspondence, bridgelessness, ear-by-ear strong orientation, both-directions crossing) fails
on a machine-checked instance in `experiments/woodall-tau2-checks/`, the write-up stops and
records the failing instance.

**K5 — Budget.** One hour of compute. Anything not finished by then is reported as partial.

## Outcome

See `README.md` §9. K1 discharged (the step is the *colouring-to-packing* step, §6.2), K2 and
K3 discharged (§6.3, §6.4), K4 did not fire (all checks in `experiments/woodall-tau2-checks/`
pass), K5 not reached for the proof itself; the search for Schrijver's *own* instance was budget-
limited and is reported as such (§6.2, gap G2).
