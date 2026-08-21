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
   Claude reviews Codex). The helper follows this strict priority order:
   1. Review every eligible pending PR.
   2. When the review queue is empty, perform numerical analysis requested by the prover.
   3. When neither review nor requested numerical work exists, verify the relevant literature.
   The helper must never remain idle waiting for a PR.

## Issues and pull requests

- **Work does not normally end when an assignment ends.** Completing an issue, review,
  computation, literature search, failed proof attempt, or other routine subtask is only a
  checkpoint. The agent must immediately continue with the next useful task.
- An attack may end when it produces a significant theorem or other significant result that
  genuinely requires independent review. Submit that result for review, then stop extending that
  attack so later work does not invalidate or obscure the reviewed version.
- When a significant result enters review, the manager must immediately select another useful
  issue or problem and redirect the working team to it. The new target may be in another problem
  directory; agents must not sit idle waiting for the review.
- Otherwise, the research program continues until its conjecture is proved or refuted, or the
  human explicitly orders the agents to stop or change focus. Agents may not become inactive
  merely because an intermediate task failed or reached its kill criterion.
- After every checkpoint, the manager must immediately evaluate the result and give the agent
  another productive assignment. If an approach fails, preserve the failure and redirect the
  agent to a different promising attack.
- Issues organize and assign ongoing work. An issue does not require its own PR.
- Existing issues and PRs from previous work are part of the current workload and must be
  reviewed and handled promptly. Work relevant to the active hypothesis must be prioritized;
  unrelated inherited work must not distract the team from its current focus.
- While a significant result is under review, work on the manager's next selected target rather
  than modifying the submitted result or waiting idly.
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
