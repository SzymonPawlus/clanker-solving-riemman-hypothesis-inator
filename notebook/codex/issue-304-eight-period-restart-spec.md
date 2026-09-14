# Restart specification for the incomplete eight-row residual graphs

Status: incomplete exact exploration. No graph in this checkpoint proves
the absence of an eight-row cover. A closed cached subgraph is not the same
as a closed root. No mathematical conclusion is based on timeout or on the
absence of an encountered candidate.

## Mathematical domain and complete children

For a fixed proposed minimum row period `p`, the roots are every distinct
complement of `B(p,a)` with `gcd(p,a)=1`, with seven further rows allowed.
All selected later rows have actual reduced period at least `p`. The bad
row is defined by the strict integer inequality

```text
B(h,a)={j mod h : min(a(15j+1) mod15h, -a(15j+1) mod15h)<h}.
```

There are fourteen moving velocities and fifteen total runners in the
surrounding problem. All rows concern the same maximal lower endpoint;
equality at distance `1/15` is allowed, and only common gcd normalization
is used.

At state `(r,L,R)`, generate every divisor `d|L`, every positive integer
`n` with `r ceil(2n/15)>=n` and `gcd(n,L/d)=1`, and every reduced numerator
of `h=dn>=p`. A completing set of `r` rows has at least one row with
`r*hits>=n*|R|` after lifting to `Ln`, so every such high-gain row must be
included. Remove its hits, reduce the residual indicator to its true period,
and decrement `r`. Only exactly equal resulting residual states are
identified. Numerators with the same conditional counts are not silently
identified before constructing their actual child sets.

For `r<=7`, the inequality implies `n<=14r/(15-2r)<=98`. In particular,
`E7` has 56 values and maximum 98. The smaller sets are the same `E1,...,E6`
as in the frozen seven-row specification. If every root and descendant
were eventually closed, this would be an unbounded exclusion for that
fixed minimum period `p`. The current files do not satisfy that condition.

## Caps, resume, and certificate interpretation

`eight_period_states.py` uses exact scalar integer arithmetic. Its optional
resume mode reads a completed earlier capped run and recursively retains
only nodes whose entire descendant graph is already closed. It never
reuses an open node or a branch depending on an open node as an exclusion.
Every remaining root and edge is regenerated. Reuse occurs only inside the
same fixed-`p` file; the state identifier need not encode `p` because files
with different minimum periods are not mixed.

Caps on time, state count, and current residual period create explicit
`open` nodes. Parent nodes still record all their generated child states.
After the run has ended, every closed subgraph can therefore be replayed
independently. A file written during a running process is a progress save,
not a complete root certificate; use the final process checkpoint before
attempting a restart or an exhaustiveness conclusion.

`eight_period_states_fast.py` batches the same hit counts in signed 64-bit
integer arrays, then reconstructs each actual lifted child using ordinary
integer sets. It does not use floating point. The campaign caps the current
residual period at 50,000 or less and `n<=98`, so `h<=4,900,000`; even the
largest products used in those arrays are below `h^2<2.5*10^13`, safely
inside signed 64-bit range. Before use, 24 varied states were compared
against the scalar implementation, with exactly equal complete child lists.
This is author regression testing, not independent verification.

An independent graph audit must reconstruct every root, every physical
reduced row, every high-gain child, the actual period minimization, and the
full set of child targets. The supplied generators must not be read or
translated when implementing that independent audit. No dual weights are
used in this campaign.

## Capped passes preserved during this cycle

- Minimum period four: 300-second scalar pass followed by a 600-second
  scalar continuation; final checkpoint has 2,577 states, 373 open nodes,
  2,202 closed subgraphs, and zero closed roots.
- Minimum period five: 300-second scalar pass followed by a 240-second
  integer-vectorized continuation; the continuation finished with 2,759
  states and 351 open nodes.
- Minimum period six: 300-second scalar pass, then a separate 240-second
  vectorized continuation; final checkpoint has 3,569 states and 298 open
  nodes.
- Minimum period seven: one 300-second vectorized pass; 1,047 states,
  248 open nodes, 796 closed subgraphs, and zero closed roots.
- Minimum period eight: one 300-second vectorized pass; 2,503 states and
  408 open nodes.
- Minimum period nine: a separate 300-second vectorized pass; 1,076 states
  and 313 open nodes.

The per-file hashes, actual root counts, closed-subgraph counts, and source
hashes are recorded in the checkpoint manifest. Final follow-up work should
first inspect those counts, preserve the frozen graphs, and select an
explicit restart or a stronger pruning argument. A larger search by itself
does not resolve the unbounded minimum-period proposal.

All six capped runs have ended. The final machine-readable inventory is
`issue-304/eight-period-final-checkpoint.json`: 13,531 recorded states,
1,991 open nodes, no closed roots, and no encountered covering tuple.
Every edge references a saved state with one fewer remaining row. These
integrity checks do not substitute for independent complete-child replay.
