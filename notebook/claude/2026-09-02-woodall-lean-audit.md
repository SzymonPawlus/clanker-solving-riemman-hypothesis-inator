# 2026-09-02 — Woodall Lean faithfulness audit (issue #151, adversary side of pair B)

Worktree `/home/user/wt/151-lean-audit`, branch `claude/151-lean-audit`. Model: Fable 5.1.

## Order of work (matters for an adversarial audit)

1. 07:33 Read RULES.md, CLAUDE.md, Woodall README/RULES, RH RULES §4, lean/README.md, issues
   #150/#151. B1's branch `claude/150-lean-foundations` did not exist on the remote.
2. Wrote `experiments/woodall-lean-crosscheck/prose_model.py` from README.md alone, without
   opening the other `experiments/woodall*` checkers. Fixtures pass: path τ=1; 3-cycle has no
   dicut; diamond τ=2 with two disjoint dijoins; near-miss DAG τ=1; `0→1,0→1` has τ=2.
3. Committed `attacks/lean-foundations-audit/hypotheses.md` (20 drift hypotheses H1–H20 and
   three prose ambiguities P1–P3) at f16bc5f **before** reading any Lean.
4. Found the older branch `claude/76-lean-woodall` (PR #79, closed by Codex on 2026-08-21).
   Modelled its `Basic.lean` literally (`lean_model_76.py`) and swept it: 13,615 labelled
   digraphs, n≤4, ≤6 arcs, multiplicity ≤2.
5. Polled for B1's branch in the background while writing up.

## Prose-model observations (findings against README.md, not against any Lean)

- P1: README does not say whether `∅` is a dicut of a disconnected digraph. Literal reading:
  yes, τ=0, no dijoin exists. Survey reading: dicuts nonempty. They differ on exactly the
  273 simple digraphs in the sweep whose underlying graph is disconnected, and on no
  weakly-connected one.
- P2: τ is undefined when there is no dicut. The easy-direction prose proof needs a minimum
  dicut to exist; any Lean `τ : ℕ` must pick a convention or avoid defining τ.

## Branch-76 Lean, literal model vs prose (sweep results)

- Simple digraphs, literal-README reading: **0 disagreements** on dicuts, τ, max packing.
- Parallel arcs: `arcs : Finset (V × V)` collapses them. 2,086 of 13,615 digraphs change τ;
  smallest witness `0→1, 0→1` (prose τ=2, Lean τ=1). Codex's review of #79 caught this.
- Empty dicut permitted, documented as deliberate: matches literal README, differs from the
  survey on the 273 disconnected simple digraphs.
- H1, H3, H4, H7, H10, H12 checked against the source: none fire. `IsDicutSide` requires
  `S ≠ ∅ ∧ S ≠ univ ∧ inn S = ∅`; `HasPacking` has `i ≠ j → Disjoint`; the easy direction is
  stated against *every* dicut, which is the stronger, correct form.
