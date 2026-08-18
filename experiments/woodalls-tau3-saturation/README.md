# Exact witness against the tau-saturation structural conjecture

Status: **numerical**. Run:

```bash
python3 experiments/woodalls-tau3-saturation/verify_witness.py
python3 -m unittest discover -s experiments/woodalls-tau3-saturation -v
```

The verifier enumerates every dicut shore from the definition and independently recomputes `tau`
with predecessor bitsets. It checks the displayed minimum dicut, the failed source-to-sink
reachability, and `tau(D+e)>tau(D)` for every missing forward arc `e`.

The witness consists of two forward complete graphs on ordered vertex sets
`(0,2,3,4,8)` and `(1,5,6,7,9)`, plus the cross-arcs `1->2`, `1->4`, and `6->8`. Its unique minimum
dicut has shore `{1,5,6,7,9}` and arcs `{1->2,1->4,6->8}`, so `tau=3`. Sources are `0,1`; sinks
are `8,9`; source `0` cannot reach sink `9`. There are 22 missing forward arcs: adding `0->9`
raises `tau` to 5, and adding any other one raises it to 4.

The explicit finite witness refutes only the proposed structural shortcut. It is not a
counterexample to Woodall's conjecture.
