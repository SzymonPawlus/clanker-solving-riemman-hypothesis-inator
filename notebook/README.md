# Notebook

Per-agent working journals. One directory per agent, and **an agent writes only its own**
(`RULES.md` §2) — this is what keeps the two of them off each other's files.

```
notebook/claude/    claude only
notebook/codex/     codex only
```

One file per attempt, named `YYYY-MM-DD-<slug>.md`. Append-only: correct a past entry by writing
a new one that supersedes it, never by rewriting history. The point is a record of what was
believed and when, including the parts that turned out wrong.

Journals are scratch space. Nothing here is citable regardless of how confident it reads — only
`cited` and `verified` claims may be built on, and those live in a problem's `results/`.
