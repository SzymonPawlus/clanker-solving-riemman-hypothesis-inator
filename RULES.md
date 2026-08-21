# Rules

This repository coordinates Claude and Codex agents through GitHub issues and pull requests.
The goal is sustained cooperation on mathematical problems, with independent verification of
important results.

## Roles

The team consists of **four agents**: one human-interface agent plus three working agents with
the roles below. All three worker agents must remain productive:

1. **Manager** — communicates with the human, divides the work, assigns issues, and keeps every
   agent occupied. The manager must monitor progress regularly, assign pending PRs to the
   reviewer, and push the prover toward new, significant results instead of repeatedly proving
   minor facts or remaining stuck on an unproductive path. The manager selects one active
   hypothesis and coordinates all agents around attacking it; it must not scatter work across
   unrelated problems. Changing the active hypothesis must be a deliberate decision based on
   progress, evidence, or human direction.
2. **Prover** — continuously attacks the mathematical problem represented by its assigned issue.
3. **Helper (paper finder / numerical analyst / reviewer)** — supports the prover by checking
   whether results already exist in the literature, performing numerical analysis, verifying
   proposed results, and reviewing pending PRs from the other party (Codex reviews Claude and
   Claude reviews Codex). Reviewing has immediate priority whenever a PR is waiting. When no PR
   needs review, the helper must actively support the prover through literature, computation,
   counterexample searches, or independent checking; it must never remain idle waiting for a PR.

## Issues and pull requests

- **Work does not end when an assignment ends.** Completing an issue, review, computation,
  literature search, proof attempt, or other subtask is only a checkpoint. The agent must
  immediately continue with the next useful task on the active hypothesis.
- The research program continues until the active conjecture is proved or refuted, or the human
  explicitly orders the agents to stop or change focus. Agents may not become inactive merely
  because their current assignment produced a result, failed, or reached its kill criterion.
- After every checkpoint, the manager must immediately evaluate the result and give the agent
  another productive assignment. If an approach fails, preserve the failure and redirect the
  agent to a different promising attack.
- Issues organize and assign ongoing work. An issue does not require its own PR.
- Existing issues and PRs from previous work are part of the current workload and must be
  reviewed and handled promptly. Work relevant to the active hypothesis must be prioritized;
  unrelated inherited work must not distract the team from its current focus.
- Keep agents working on a problem while review is pending; avoid workflows that unnecessarily
  block further investigation.
- Create as few PRs as possible. A PR is required only for significant progress that needs
  verification, such as solving the problem, proving an important new theorem, or finding a
  counterexample.
- Do not create a PR for routine, insignificant, or result-free work.
- Every PR must be independently reviewed by the other party: Codex reviews Claude's work and
  Claude reviews Codex's work.
- Review every PR as soon as possible. Pending review takes priority because delays obstruct
  further progress.
- Every agent must remain productively occupied. The manager is included: it must regularly
  inspect the agents, issues, PRs, and overall direction, then intervene or reassign work when
  progress stalls.
- The human-interface agent is not one of the three worker roles. It communicates with the human
  and relays instructions while the manager runs the research team.
- The manager is responsible for ensuring the reviewer handles pending PRs promptly.

Human instructions override these rules.
