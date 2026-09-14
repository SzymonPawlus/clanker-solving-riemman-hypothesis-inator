# Lonely Runner: 14 September sustained work cycle

Status: session record; no mathematical result is promoted by this file.

The user requested an attack under the repository rules lasting at least one hour.
The session began at 2026-09-14 19:55:08 UTC. The active campaign inherited from
issue #297 is Lonely Runner with fourteen moving velocities, fifteen total
runners, and separation at least 1/15. Root acts as the human interface.

## Workers and isolation

- Manager: issue #297, branch `codex/297-sept14-manager`, worktree
  `/tmp/codex-297-sept14-manager`; productive cycle began 19:56:26 UTC.
- Prover: a separate issue and worktree are being established; structural attack
  on the current maximal-anchor and transferred-burden program.
- Helper: issue #301, branch `codex/301-sept14-helper`, worktree
  `/tmp/codex-301-sept14-helper`; productive cycle began 19:56:45 UTC.

The existing root checkout and unrelated untracked files are preserved. The
human-owned `RULES.md` and `AGENTS.md` are not edited. Pending Codex PRs #300,
#302, and #303 are frozen; same-model checking cannot supply their required
Claude or human approval. Routine exploratory work does not justify a PR.

## Initial evidence and direction

The previous all-anchor proof contains acknowledged finite-tail gaps. The helper
is auditing the corrected p=3 and p=4 classifications from the mathematical
definitions, without reading earlier checker code. The prover is seeking a
structural argument for the scaled eight-speed subsystem, beyond further
individual linear-programming certificates. The manager checks progress and
redirects failed or completed approaches within the same hypothesis.

Fresh primary-source inspection on 14 September confirms that
[Allikvere's preprint](https://arxiv.org/abs/2609.02604) is still v1, dated
2 September 2026, and claims fourteen total runners. Its proof is not an
assumption of this cycle. The
[Sungkawichai–Trakulthongchai source](https://arxiv.org/abs/2604.23906) has a v2
dated 1 September. A separate
[restricted congruence-family claim](https://jaigp.org/paper/95), dated
5 September, was located; it does not assert the full fifteen-runner case and
has not been independently checked here.

## Checkpoints

Further entries below will state bounded domains, exact findings, limitations,
and the actual completion time. Waiting will not be counted as productive work.

### First all-scale certificate (about 20:03 UTC)

The prover, now on issue #304 and branch `codex/304-sept14-prover` in
`/tmp/codex-304-sept14-prover`, found the missing threshold distinction in the
earlier notes: excluding six completion speeds only requires a dual mass
strictly greater than six, not the optimal value seven.

Its 24 positive rational endpoint weights have total `6011/1000`. For
`P={1,5,6,7,9,11,13,18}`, they certify a candidate theorem: every fourteen-speed
tuple containing `cP` and six additional positive speeds below `18c` has a
common time with all distances at least `1/15`, for every positive integer c.
The finite certificate does not assume the earlier seven-row classification.

The helper independently enumerated all 38,548 admissible reduced columns with
denominator at most 83 from integer-grid semantics. The maximum bad weight was
`749/750`, attained at reduced pairs `(3,49)` and `(3,53)`. A further 8,130
actual columns at scales 1 through 30 agreed with the reduction. An analytic
tail bound handles unbounded denominators. These are same-model independent
implementation checks, not the required Claude/human approval; status remains
`sketch` pending that review.

The team continues on related primitive patterns and a constructive extraction
of a rational witness at arbitrarily large scales. The first candidate is to
be frozen so subsequent work cannot silently change the reviewed object.

### Twenty core patterns (20:07--20:08 UTC)

All four primitive cores with maximum 18 passed independent checks. The
prover froze this first version at commit `f253029` and pushed branch
`codex/304-sept14-prover`. No new PR was opened because the inherited board
already exceeds the review cap (26 assigned awaiting-review claims versus
the stated maximum six). Existing unrelated work is not mass-closed or
unassigned to conceal the drift.

Endpoint-only measures failed for ten of the twenty recorded primitive
cores at maxima 18, 24, and 30. Including rational interior times already
safe for the fixed core produced candidate measures above six for all ten.
Thus there are now candidates for all twenty patterns, with the additional
independent audits still underway at this checkpoint.

After that candidate is frozen, the next attack is the unbounded
classification of seven-row maximal-anchor covers. It remains a separate
open obligation; the twenty-core special-case theorem does not assume it.
The manager is also deriving and testing deterministic rational witness
extraction using exact interval counts and bisection, avoiding enumeration
of all c fibers when c is large.

### Classification refuted (20:09--20:10 UTC)

The manager found the primitive core
`{2,12,15,18,26,28,33,36}`. Its seven speeds below 36 cover all 36 lower
endpoints of the maximal speed, and every row is essential. Its gcd is one,
so it cannot be a scaling of one of the previously recorded cores with
maximum 18, 24, or 30. The helper and root independently checked the direct
integer residues. For example, private endpoint indices include 17 for
speed 2, 3 for speed 12, 7 for speed 15, 2 for speed 18, 11 for speed 26,
5 for speed 28, and 13 for speed 33.

This refutes the prior proposal that *every* seven-row maximal cover belongs
to those twenty scaled patterns. It does not refute Lonely Runner, nor does
it by itself refute the weaker proposed divisibility criterion for which
maximal speeds admit some seven-row cover. The twenty-core theorem remains
valid within its stated scope; the helper has now independently checked all
twenty certificates, including their exact tail bounds.

### A finite replacement for the false classification (20:19--20:23 UTC)

The manager derived a self-contained candidate reduction for an
inclusion-minimal cover of a maximal anchor by exactly seven smaller speeds.
After gcd normalization, the maximal speed is at most `1,048,320`.

The proof chooses rows greedily. If the current uncovered set has period L
and a candidate row has period h, then on each residual class its new factor
`n=h/gcd(h,L)` can kill at most `ceil(2n/15)/n` of the class. With p rows left,
some row must kill at least `1/p` of the residual. The possible factors have
maxima 24, 10, 8, 3, 2, and 1 for p=6 through 1. The first row uses the
sharper integer count `ceil((2h-1)/15)/h`, giving h at most 91. Their product
is the stated bound. The last joint period equals the normalized maximal
speed. Inclusion-minimality is essential to this statement.

Retaining the exact allowed-factor sets, instead of only their maxima,
gives 4,324 possible products; requiring seven distinct smaller positive
speeds removes maxima 2 through 7, leaving 4,318 candidates. Root and manager
independently regenerated the same product counts. Of the refined list,
1,746 candidates fall outside the earlier proposed divisibility criterion.
These are candidates, not assertions that covers exist.

The manager reports exact finite regression checks on 9,879 reduced rows,
1,727,083 conditional residue classes, and 817 endpoint ties. In particular,
the proof does not assume reduced numerators are coprime to 15. The new
reduction remains a `sketch` pending the required cross-model review.

### Stronger reduction and conditional classification (20:25--20:36 UTC)

The prover's new exact argument shows that any maximal-anchor cover by at
most seven rows has a reduced period at most 16. Its finite obligation has
2,472 base cases, with largest upper bound `1574/1581<1`; the helper
independently reproduced the result using 64,527,128 direct charge
comparisons and the analytic tail. Starting the period-growth argument with
that row improves the normalized maximal-speed bound to `184,320`.
The refined necessary product domain has 1,326 values, of which 530 are
outside the previously proposed divisibility condition. The twenty-core
certificate version is frozen at `83043de`, and the small-period reduction
at `2acd3bc`, on the prover branch.

For covers that explicitly contain periods 2 and 3, a separate argument
reduces the primitive candidates to 37 maximal speeds, all at most 2,880.
The helper's complete enumeration found exactly 44 primitive speed cores.
The manager's fresh enumeration used all physical speeds, allowed the greedy
choices in every order, and independently obtained the same 44 tuples:
2,127 search nodes versus the helper's 1,673, with no cap reached. Each
output was checked for full coverage, gcd one, and a private residue for
every row. Thus the conditional classification has two independent
implementations within the Codex family. The universal necessity of
periods 2 and 3 is still open; no unconditional 44-pattern classification
is claimed.

### Independent replay and service interruption

At 20:46:45 UTC, root completed a clean-export replay of the saved manager,
prover, and helper commits. Passing checks included the classification
falsifier, greedy period reduction, conditional divisibility, both
conditional 44-core enumerations, both period-16 implementations, the
twenty-core rational measures, and both deterministic witness constructors.
The two period-16 implementations again gave `1574/1581`; the independent
C++ checker performed 64,527,128 charge comparisons.

The helper's first portable wrapper depended on untracked individual
certificate files. This packaging defect was caught before handoff and is
being replaced with a wrapper consuming the committed normalized manifest.
The helper's push was also rejected by automatic approval review over
unverified destination/payload authorization. Root then verified the exact
repository as `PUBLIC` with account permission `WRITE`; the helper was
instructed to reconsider the same authorized push using that new evidence.
No rejected action was bypassed.

The service subsequently stopped the workers with a usage-limit error.
The user requested continuation. The temporary worktrees disappeared across
the interrupted turn, but the repository retained all three committed
branch heads. Root confirmed the objects and restored them on 14 September
at about 21:19 UTC in persistent paths under `.worktrees/`:

- Manager: `codex-297-sept14-manager`, head `f4a213c`.
- Helper: `codex-301-sept14-helper`, head `3565d72`.
- Prover: `codex-304-sept14-prover`, head `fd602d4`.

The service interruption is not counted as productive time. A fresh
continuous worker cycle is now underway, targeted through at least
22:21 UTC. The manager resumed at 21:19:50 UTC; all three roles were
re-established. Lost untracked state-graph claims are not assumed: the
graphs must be regenerated and independently checked. The committed
forty-four-core measure manifest survived and is the helper's first audit
target in this resumed cycle.

### Resumed structural closure and portable replay (21:26--21:32 UTC)

The helper independently checked all 44 committed rational measures:
433,328 reduced columns and 82,280 literal lifted columns, maximum bad
mass `9999/10000`, positive total mass greater than six for every core,
and the analytic tail for all remaining scales. The certificate inventory
matches the independent conditional 44-core enumeration exactly. Commit
`10d8a6d` repairs the tracked-only replay and saves the audit. The earlier
push restriction was resolved using the newly verified public repository
and WRITE permission; the helper reports a successful push.

Root exported only tracked files from helper `10d8a6d`, prover `764d6e1`,
and manager `9e7bf4b` into persistent replay directories. The complete
helper wrapper passed there: all 44 measures, the period-16 bound, and the
37-anchor conditional census. The randomized witness checker also passed
its fixed 1,001-digit-scale case, directly verifying all 14 coordinates.

The new exact residual-state graphs remove both proposed structural gaps:
the prover excludes every minimum period 3 through 16 in a seven-row
cover without period 2, and the manager excludes a seven-row cover with
period 2 but without period 3. Root wrote a separate checker from the
mathematical prose and graph format, without reading either generator.
It enumerates every unit numerator through the direct strict modular
inequality, reconstructs every admissible child, checks all roots and
representative rows, and verifies complete graph reachability. All 15
graphs passed in 81 seconds. The no-period-3 graph has 1,093 states and
2,022 edges, with SHA-256
`7c9bda49bc14b1f866699af207e09f333c5fb81fad74e995c5d591104742a18b`.

A composition audit caught an additional gap: the earlier conditional
seven-row census did not itself rule out covers with fewer rows. A separate
manager graph starting with four rows left and residual `{1,5}` modulo six
now excludes those cases. Root independently checked all 25 states and
43 edges; its graph SHA-256 is
`a0ca6e78d93b638c52caf68db9aba30ce884636f006ab87b673b8632325452c6`.
The independent checker also rejected deliberate omitted-edge, invalid-row,
missing-root, incomplete-campaign, unexpected-dual, and duplicate-residue
mutations. Helper will preserve the checker and a fresh combined report.

All components and their proposed composition remain `sketch` pending the
required Claude or human review. This does not prove the full k=14 case.
The manager has redirected the working team to minimal eight-row maximal
covers, first small primitive maxima, whose nine fixed speeds leave five
arbitrary extra speeds to handle. The requested continuous cycle continues.

### Further certificates and a shorter independent census

Helper commits `5d5341e` and `58db4ce` preserve and rerun root's independent
graph checkers. The first checks 2,580 states and 3,610 edges across the
sixteen structural graphs. The second checks the manager's new sharp
upper-anchor theorem: a cover by at most six speeds forces a speed at least
`13/12` of the anchor. Its complete graph has 169 roots, 279 states, and
151 edges. At anchor 12, killers `{4,5,6,7,11,13}` attain equality; direct
strict-residue checks establish coverage and a private endpoint for each.
Five rejection fixtures catch omitted roots/children, incomplete graphs,
loss of the physical-period restriction, and accidental inclusion of the
forbidden ratio equality. Manager commit `b48cb08` preserves the theorem,
graph, and separate at-most-six-row exclusion.

The next bounded census found 160 primitive minimal eight-row covers with
maximum at most 30. Prover `2cc5bc8` supplies a universal rational measure
for each corresponding nine-speed pattern: total mass greater than five,
surviving five arbitrary added smaller speeds at every common scale.
Helper `b3015d8` records a separate successful exact audit. This is an
all-scale theorem for explicit patterns, not an unbounded classification
of eight-row covers. Four patterns at maximum 24 lack period two.

Root then rebuilt the conditional seven-row census directly from residual
states, without either author's census code or the 37-maximum reduction.
Start with period-two and period-three rows, residual `{1,5}` modulo six,
and five rows left. Recursively enumerate every qualifying physical row
using the proved finite multiplier sets; retain all completing row sets,
even when their residual states coincide. For each completion, the primitive
maximum is the lcm of its physical reduced periods. This takes 438 states
and 1,069 qualifying physical edges, and produces exactly 22 suffix sets.
Restoring the two physical period-three numerators gives exactly the same
44 primitive cores. Each is checked directly for coverage, gcd one, and
private residues; all suffixes have exactly five rows. The run completed in
0.105 seconds. Helper is preserving this shorter independent route.

The central proposed-result review map is on
[issue 297](https://github.com/SzymonPawlus/clanker-solving-riemman-hypothesis-inator/issues/297#issuecomment-5671154299).
The review queue remains over the user-stated cap, so the significant
branches are pushed and linked there without opening more PRs or merging
our own work. All claims remain sketches pending Claude or human review.

A possible next inequality based on a spanning tree of pair intersections
was checked against its primary literature attribution: David Hunter,
[An upper bound for the probability of a union](https://www.cambridge.org/core/journals/journal-of-applied-probability/article/abs/an-upper-bound-for-the-probability-of-a-union/092D711504BA968EF0D1D903A2685D60),
Journal of Applied Probability 13(3), 597--603 (1976). The general tree bound
is established literature, not a novelty claim of this project. Its desired
specialization to the remaining endpoint covers has not been proved.

### Executable outputs and the unbounded eight-row attack (through 22:14 UTC)

Manager `6ffcf6f` bundles the two unchanged measure manifests into a
204-family recognizer and rational witness extractor. Root replayed the
tracked-only export and independently tested its public command interface,
without reading/importing the solver or its author checker. All 204 fresh
completions passed at scales 1, 2, 15, 97, and scales with 101 and 1,001
digits. Root directly checked 2,856 inequalities on the original signed
inputs; the runs used 485 total sampling trials. Valid but unrecognized
inputs and signed repetitions were checked separately. Helper `e580afd`
preserves this independent test and its fresh replay. Recognition outside
the explicit catalog remains unsupported; a missing match or trial cap is
never a no-witness result.

The tree-intersection route now has a self-contained analytic candidate.
Prover `7bbc832` gives a finite Fourier smoothing argument. Manager
`7701daa` improves its relation window from 65,534 to 2,998 using a C1
cosine ramp and a second-moment bound for a squared Fejer kernel. Either
an eight-row cover has a reduced period at most 2,998, or its speed ratios
belong to finitely many rational affine templates in one free parameter.
The parameter remains unbounded. Helper `a127660` independently checked
the analytic argument and exact positive gap `904213/629790000`.

Manager `5626836` freezes a self-contained sharp endpoint-cover ratio
table for one through seven killers:

| Number of killers | Necessary largest-killer / anchor ratio |
|---:|---:|
| 1 | 15 |
| 2 | 15/2 |
| 3 | 15/4 |
| 4 | 13/6 |
| 5 | 11/6 |
| 6 | 13/12 |
| 7 | 1/2 |

Every equality has a directly checked example and private endpoint for
each row. Root's new independent checker reconstructed all six exclusion
graphs: 1,938 states and 516 edges. The seven-row exclusion alone has
1,264 roots and 1,541 states and uses only the elementary period-91 bound,
not the earlier period-16 result or 44-core classification. Five damaged
certificate fixtures were rejected. Helper is preserving this final audit.

The exact bounded search for eight-row covers with neither period two nor
period three is fully complete at every maximum from 9 through 400;
helper `1570bcf` closes every earlier capped anchor. It finds no such cover
in that domain. The direct unbounded state searches with fixed minimum
period four and higher still have open/capped states and do not support
an exclusion theorem. Prover `fa4eb0b` preserves their initial checkpoint
and the exact scope of the affine discovery experiments.

Root also derived a conditional affine-template grid lemma. Every original
constraint, including the pivot row, must remain in the normalized circle
model. The helper sharpened the orbit argument under primitive gcd one to
`gcd(M,B*w_0)=gcd(M,L)`. A positive interval of safe phases then forces the
finite bound `M<15*L^2*P/B`, with the template integers defined in the proof.
Empty or isolated-point safe sets are deliberately left separate.

For the isolated-point case, root proposed a simpler lifting mechanism:
take `M=3^n` and choose the parameter numerator coprime to three. Sampled
phases then retain a denominator with 3-adic valuation `n+1`, while every
fixed safe endpoint has bounded valuation. Thus a suitable template covering
every open cell would yield arbitrarily large primitive eight-row covers
after common gcd normalization. Both manager and prover independently
checked the argument. No such template has been found; this is a conditional
lifting lemma, not a counterexample. The prover is freezing it separately
from the earlier prime-lift version.

All theorem statements in this section remain `sketch`. These same-family
audits do not supply Claude/human approval or prove the full k=14 conjecture.

### Closing review checkpoint

Helper `f63f875` preserves the independent sharp-ratio replay and rejection
fixtures. Helper `b5b5c16` freezes the strengthened affine-grid bound and the
complete exact slope-24 chamber decisions. Helper `f50cd22` expands the
open-cell search through slope magnitude 40: all 490 chambers, 8,456 search
states, no cover and no incomplete case. This is still a bounded template
family, not every rational-affine template.

Prover `c7145bc` freezes the pure power-of-three lifting lemma, with explicit
conditions for distinctness and minimality, and preserves open state-graph
checkpoints. The independent helper audit includes 1,102 general grids,
539,980 exact endpoint-hit decisions, 30 power-of-three fixtures, 46,213
boundary separations, 58,806 sample-valuation checks, and 3,960 original/
normalized coordinate identities. None of these fixtures is advertised as
an actual eight-row cell-cover template.

The manager independently confirmed that an integer-affine eight-row
open-cell cover in a common physical strip must have distinct absolute
slopes. Equal signed slopes give an identical constraint; opposite slopes
have intercepts summing to one. Their arc union has measure 1/5, and the
common open intersection with the other rows makes the total union measure
strictly below one. The integer intercept and common-strip hypotheses are
essential; this does not authorize a general shifted-runner shortcut.

A fresh board read at 22:17 UTC found 33 awaiting-review issues in total,
26 assigned to Codex, against the six-claim cap. The six open other-party
PRs all concern other problems; no eligible Lonely Runner PR appeared.
No new PR, claim promotion, own merge, or human-owned rule edit occurred.
One later manager push was briefly rejected by automatic approval review;
fresh PUBLIC/WRITE destination checks and the user-provided publication
instruction resolved it. Manager `4b611b9` is safely pushed, and no
publication blocker remains.

### Final sustained-cycle handoff — 22:24:45 UTC

The fresh manager cycle ran from 21:19:50 through 22:21:32 UTC before
final publication: 61 minutes 42 seconds. The prover separately recorded
21:20:17 through 22:21:36: 61 minutes 19 seconds. The helper also passed
the 22:21 checkpoint while completing the final structural audit. Root's
closing clock read 22:24:45 UTC. This satisfies the requested fresh hour
after the earlier interrupted work; the interrupted interval is not needed
to reach the duration.

Final research heads are manager `6dc67e2`, prover `ae75126`, and helper
`02c57bc`, all pushed. The helper will additionally preserve this exact
closing session-log snapshot in a final bookkeeping commit. The central
review handoff is:

https://github.com/SzymonPawlus/clanker-solving-riemman-hypothesis-inator/issues/297#issuecomment-5671610589

Helper `02c57bc` proves a useful necessary condition directly from the
common positive strip: an integer-affine open-cell cover using fewer than
ten rows must contain a slope divisible by fifteen. At the fifteen common
points `(x+j)/15`, a row is bad exactly when `a_i*j` is 0 or 14 modulo 15.
Without a multiple-of-fifteen slope, eight unit indices require eight unit
slopes, while indices three and five require two additional, distinct
nonunit slopes. Root and manager independently checked this proof. The
helper also checked all 16,384 residue subsets and 2,400 literal phase
inequalities. This is a necessary condition only; no qualifying continuous
cover template was found. It applies to slopes under the stated template
hypotheses, not directly to arbitrary original runner velocities.

Prover `ae75126` closes every running experiment and preserves the six
incomplete minimum-period graphs for periods four through nine. They have
13,531 states and 1,991 open nodes in total. The respective open counts are
373, 351, 298, 248, 408, and 313. Every root remains unclosed. Their restart
instructions permit reuse only of fully closed subgraphs. These are useful
checkpoints, not exclusion proofs.

The review package contains the proposed forty-four-core classification
and its independent exact replays, 204 explicit all-scale families with an
executable rational-witness tool, sharp cover-ratio candidates for one
through seven rows, and the analytic and affine reductions. Exact bounded
negative searches are explicitly distinguished from unbounded claims.
No proof of the full fifteen-runner conjecture has been obtained; minimal
maximum-anchor covers needing eight through thirteen rows remain open.
All theorem candidates remain `sketch` pending Claude or human review.
No own PR was merged, no extra claim was opened beyond the existing queue,
and no human-owned rule file was edited.
