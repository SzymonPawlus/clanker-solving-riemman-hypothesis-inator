# clanker-solving-riemman-hypothesis-inator

Two LLM agents — Claude and Codex — attacking open mathematical problems under a
machine-checked, cross-reviewed workflow. The name is a joke. The verification is not.

## Layout

```
RULES.md        operating protocol for agents — canonical, human-owned
CLAUDE.md       thin pointer to RULES.md, read automatically by Claude Code
AGENTS.md       thin pointer to RULES.md, read automatically by Codex
problems/       one directory per problem (see problems/README.md)
lean/           Lean 4 + Mathlib project — the verification gate
experiments/    reproducible numerics
notebook/       per-agent append-only journals
```

## How it works

- **Board:** GitHub Issues. Assignment is the lock — it resolves server-side, so claims cannot race.
- **Isolation:** one branch and one PR per issue; no two agents ever write the same file.
- **Review:** cross-model. Claude reviews Codex's PRs and vice versa, because two model families
  have less correlated blind spots than one model reviewing itself.
- **Gate:** Lean-preferred. Prose may merge as `sketch`; nothing reaches a problem's `results/`
  without a `sorry`-free Lean proof.

Agents run autonomously — they open, claim, and close their own issues — subject to the limits in
`RULES.md` §6. Humans can intervene at any point; the `human-hold` label stops an agent
immediately.

## Status

Scaffolding. No mathematical results yet.
