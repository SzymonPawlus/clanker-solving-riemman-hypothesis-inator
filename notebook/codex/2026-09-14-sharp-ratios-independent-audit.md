# Preserved independent audit of the one-through-seven sharp ratios

Status: `sketch`, pending Claude or human approval. Root independently
implemented `check_sharp_ratios.py` from the manager's mathematical prose
and graph data, without reading or importing an author generator/checker.
Helper preserved its bytes as `helper_sharp_ratios_audit.py` and reran it.
This replay preserves root's independent audit; it is not a third
implementation and does not earn `verified:review`.

The candidate sharp largest-killer/anchor ratios for one through seven
rows are `15,15/2,15/4,13/6,11/6,13/12,1/2`. The motivating target is
fourteen moving velocities, fifteen total runners, threshold 1/15. Every
row acts on one common anchor endpoint. The bad inequality is strict;
equality at the ratio bound is allowed and is tested by sharp examples.
Physical periods are preserved separately from minimized residual periods.

The source imports only root's earlier independent common integer
arithmetic, already preserved as `helper_state_graph_audit.py`. It
reconstructs every initial physical unit numerator, every qualifying
child, exact residual normalization, root reachability, and every recorded
representative. Numerators may exceed their periods. An independently
derived necessary prune skips period `h` when

```
r*ceil((2h-1)/15)*L < h*|R|.
```

Indeed, even the entire row then has density less than the required
fraction of the residual. This bound is independent of the numerator and
cannot discard a qualifying child. No author pruning implementation is
imported.

Fresh replay passed all six exclusion graphs: 1,938 states, 516 edges,
and all seven sharp covering/private-index examples. The seven-row graph
alone has 1,264 roots, 1,541 states and 330 edges. The combined run took
4.14 seconds. `helper-sharp-ratios-audit.json` binds the copied checker,
common arithmetic, and each graph by SHA-256. The original root report is
preserved separately as `helper-sharp-ratios-root-audit.json`.

`helper_sharp_negative_fixtures.py` preserves root's separate mutation
script. Its fresh report rejects all five malformed inputs: an omitted
root, an omitted child, an incomplete flag, a lost physical-period bound,
and a representative at forbidden ratio equality. Both original and fresh
negative reports are retained. A successful same-family audit leaves the
theorem candidate at sketch status.

From this notebook directory, with the manager's tracked mathematical data:

```
python3 helper_sharp_ratios_audit.py --common-checker helper_state_graph_audit.py --manager-dir ../../../codex-297-sept14-manager/notebook/codex/issue-297 --output helper-sharp-ratios-audit.json
python3 helper_sharp_negative_fixtures.py --checker helper_sharp_ratios_audit.py --common-checker helper_state_graph_audit.py --graph ../../../codex-297-sept14-manager/notebook/codex/issue-297/upper-anchor-three-ratio-15-4.graph.json --output helper-sharp-negative-fixtures.json
```
