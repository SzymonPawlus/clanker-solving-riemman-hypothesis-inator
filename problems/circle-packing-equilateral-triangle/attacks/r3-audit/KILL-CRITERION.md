# Kill-criterion — R3-Z novelty and corrections audit

```
status: sketch (this is a process record, not a mathematical claim)
author: claude (Opus 5), worker r3-audit, 2026-08-23
```

## The criterion as assigned

Proposal Z states it, and the worker brief repeats it:

> Not applicable in the usual sense — this is an audit, and its negative outcome ("still cannot
> read it") is itself the deliverable. It ends when every lead is either resolved or recorded as
> blocked with the specific host and the specific question a human should answer.

`RULES.md` §6.2–6.3 asks an attack to name what observation would make it stop. For a literature
audit the honest answer is that **there is no observation that refutes it** — an audit cannot be
falsified by its own findings, only completed. So the termination condition replaces it, and the
condition is a checklist, not an inequality.

## Did it fire?

**No — because it cannot.** The audit ran to its **termination condition** instead: every lead is
now either resolved or recorded as blocked with a named host and a named question.

This is the outcome proposal Z predicted and pre-registered as a success (`RULES.md` §0: "a
clearly documented refutation is a success"). It is reported as one. The negative half — one
central question that this session provably cannot answer — is the deliverable, not a shortfall.

## Termination checklist

| Lead | Disposition | Evidence tier | Blocked host | Question |
|---|---|---|---|---|
| Gáspár–Tarnai n = 16 triangle density row | **BLOCKED, unread** | (iii) abstract via search only | `pp.bme.hu:443`, 403 on CONNECT | Q1 (§1.1) |
| Gáspár–Tarnai "heuristic": theorem or not | **BLOCKED**, both readings recorded, snippet tally 4–1 for "heuristic" | (iii) | `pp.bme.hu:443` | Q2 |
| Nurmela–Östergård method = approach I | **RESOLVED** at tier (iii); flagged as uncited prior art | (iii) | body paywalled (Springer, not probed) | Q3 to confirm |
| Amore N = 400 for the equilateral triangle | **RESOLVED** at tier (ii)/(iii); substance confirmed | (ii)/(iii) | `arxiv.org`, EGRESS_BLOCKED | — |
| Issue #13's actual framing | **RESOLVED**, tier (i) on the issue text; triage mischaracterised it | (i) | — | — |
| Triage §0.1 (Oler floor) | **RESOLVED — confirmed**, and strengthened | `numerical` | — | — |
| Triage §Z.1 (0.7559 calibration) | **RESOLVED — confirmed** exactly; conversion derived | `numerical` | — | — |
| Triage §0.2 (Q(√3) family) | **RESOLVED — partially refuted**: n = 27 missed | `numerical` | — | — |
| Payan body, k = 6 / n = 20 | **BLOCKED**, unchanged from `../../README.md` | (ii) | ScienceDirect (not re-probed) | Q4 |

Every row is terminal for this session. Nine leads, four blocked with a named host and a named
question, five resolved, of which one refutes the thing it was checking.

## The one thing that would reopen this attack

A human returning **one PDF** — Gáspár & Tarnai, *Per. Polytechnica Ser. Civ. Eng.* 44:1 (2000)
13–32 — or even a photograph of the equilateral-triangle table's n = 16 row. Everything in §2 of
the write-up collapses to a yes or a no against the threshold **0.755901213657**, which is
re-derived and exact.

Until then the standing instruction is unchanged and binding: **assume the Gáspár–Tarnai bound is
known, and claim no novelty for the n = 16 lower bound.**
