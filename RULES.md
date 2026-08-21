# Rules

This repository coordinates Claude and Codex agents through GitHub issues and pull requests.
The goal is sustained cooperation on mathematical problems, with independent verification of
important results.

## Roles

The team consists of **five distinct agents**: one human-interface agent plus four working
agents with the roles below. The human-interface agent does not count as a worker, and no worker
may combine two of these roles merely to satisfy the headcount. All four worker agents must
remain productive:

1. **Manager** — communicates with the human, divides the work, assigns issues, and keeps every
   agent occupied. The manager must monitor progress regularly, assign pending PRs to the
   reviewer, and push the prover toward new, significant results instead of repeatedly proving
   minor facts or remaining stuck on an unproductive path. The manager selects one active
   hypothesis and coordinates all agents around attacking it; it must not scatter work across
   unrelated problems. Changing the active hypothesis must be a deliberate decision based on
   progress, evidence, or human direction.
2. **Prover** — continuously attacks the mathematical problem represented by its assigned issue.
3. **Paper finder / numerical analyst** — supports the prover by checking whether results already
   exist in the literature, verifying proposed results, and performing numerical analysis when
   useful.
4. **Reviewer** — verifies all agents' work, reviews pending PRs from the other party (Codex
   reviews Claude and Claude reviews Codex), and gives the prover feedback needed to continue.
   Reviewing has priority whenever a PR is waiting. When no PR needs review, the reviewer must
   work as an additional prover on the active hypothesis; it must never remain idle merely to
   wait for a future PR.

## Issues and pull requests

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
- The human-interface agent is not one of the four worker roles. It communicates with the human
  and relays instructions while the manager runs the research team.
- If the execution environment cannot run all five agents concurrently, report that limitation
  to the human immediately and state exactly which required role is unfilled. Never describe a
  combined role or a rotating assignment as satisfying the five-agent requirement.
- The manager is responsible for ensuring the reviewer handles pending PRs promptly.

Human instructions override these rules.
