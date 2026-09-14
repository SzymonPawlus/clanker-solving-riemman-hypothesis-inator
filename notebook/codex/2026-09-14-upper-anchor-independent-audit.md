# Preserved independent audit of the sharp six-killer ratio

Status: `sketch`; independent implementation within the Codex family only.
Claude or human review is required.

The root worker independently reconstructed the manager's mathematical
specification for the candidate sharp theorem: if at most six positive
integer speeds cover every lower endpoint of anchor u at threshold 1/15,
one killer is at least `13u/12`. Root read only the prose specification and
JSON graph, not the author's generator. The helper preserved the root
checker and its negative-fixture script unchanged and reran both.

The graph SHA-256 is
`17d8cb6916e455d94723dad2ed8d466d81df52e4743bcde2fdbeeb488128d4a3`.
The replay passes all 169 initial roots, 279 states and 151 distinct child
edges, regenerating 210 qualifying physical rows. The largest residual
period is 180. The report binds the upper-anchor checker and the earlier
independent common arithmetic module by SHA-256.

The copied checker independently checks the initial reduced-period bound
of 24 and enumerates all coprime numerators under the strict inequality
`12a<13h`, including allowed numerators greater than h. Every state retains
the lower bound on the physical period even when its residual mask is
compressed to a smaller period. All roots, child states and representative
rows are regenerated and compared exactly. Equality at distance 1/15 is
safe throughout; the target remains fourteen moving velocities and fifteen
total runners, and all rows act on one common endpoint family.

It also directly checks sharpness: for anchor 12 the six speeds
`{4,5,6,7,11,13}` cover all lower endpoints, with a private endpoint for
every speed. The maximum speed is exactly `13*12/12=13`. This is a sharp
endpoint-cover example, not a counterexample to Lonely Runner.

All five malformed-graph fixtures are rejected: an omitted root, an omitted
child, an incomplete graph, a lost physical-period lower bound, and the
forbidden ratio equality represented by `(h,a)=(12,13)`.

The preserved files are `helper_upper_anchor_audit.py`,
`helper_upper_anchor_negative_fixtures.py`, `helper-upper-anchor-root-audit.json`,
`helper-upper-anchor-combined-audit.json`, and
`helper-upper-anchor-negative-fixtures.json`. Replay the first script with
`--common-checker helper_state_graph_audit.py`, the manager's tracked
`upper-anchor-six-ratio-13-12.graph.json` via `--graph`, and `--output PATH`.
The negative-fixture script additionally takes the upper checker via
`--checker`. This preserves root's independent implementation, not a claim
of another independently authored helper checker.
