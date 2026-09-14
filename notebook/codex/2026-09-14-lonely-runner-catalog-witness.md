# Executable witnesses for the 204 explicit scaled-core families

Status: ordinary exact-output tooling backed by mathematical certificates
still marked `sketch`; cross-family or human review remains required for
those universal certificate claims. The tool never promotes their status.

`issue-297/catalog_witness.py` recognizes a scaled copy of any of the frozen
44 eight-speed cores or 160 nine-speed cores inside a fourteen-velocity input,
then extracts one common rational time. It accepts arbitrary nonzero integer
velocities, including signs and repetitions. A recognized core must include
the largest absolute input speed. Consequently every additional distinct
absolute speed is strictly below the scaled core maximum, exactly as required
by the phase certificates.

The two unchanged source manifests are copied under `issue-297/witness_catalog/`
and checked against their frozen SHA-256 values. The first comes from prover
`fd602d4`; the second from prover `2cc5bc8`. This makes the interface portable
without another worktree or a temporary certificate file. It also verifies
the primitive pattern, positivity, exact declared mass, and safety of every
support atom before recognition.

For each recognized family, the scale is determined exactly as
M/max(primitive core), then every scaled core speed is checked for membership
in the input's absolute spectrum. If several families match, the tool uses
the largest conditional success lower bound 1-r/W, where r is the actual
number of additional distinct absolute speeds and W is the certificate mass.
The existing exact randomized lift sampler chooses a primitive atom according
to its rational weight and an integer lift index uniformly from the full
scale. Its cost does not involve listing all scale-many lifts.

Most importantly, a reported `witness` is directly checked on all fourteen
original signed inputs. For the returned reduced rational t=A/B, each input
must satisfy the integer inequality

    15 min(v_i A mod B, -v_i A mod B) >= B.

Thus a successfully returned time has a directly checkable exact certificate,
even though the universal runtime/existence argument still depends on the
review status of the underlying measures. Endpoint equality is accepted.

## Use

Supply a JSON list of exactly fourteen velocities, or an object with a
`velocities` list. Decimal strings are accepted, so very large integers do
not depend on another program's floating-point JSON behavior. For example:

    python3 notebook/codex/issue-297/catalog_witness.py \
      --input input.json --output witness.json --seed 7

Without `--seed`, sampling uses the operating system's random source.
The default cap is 100,000 trials, adjustable with `--max-trials`.
Exit status zero means a directly verified witness. Status 2 means the input
was not recognized among these 204 explicit families; it does not imply that
no witness exists. Status 3 means the sampling cap was reached and likewise
makes no infeasibility claim. Status 4 means invalid input. The output records
the selected primitive core, scale, source hash, and exact rational time.

A portable 1,001-digit-scale example and its output are stored in
`issue-297/catalog-witness-1001digit-input.json` and
`issue-297/catalog-witness-1001digit-result.json`.

## Checks and scope

The replay script `issue-297/check_catalog_witness.py` tests one completion
from each of all 204 families, alternating scales 97 and 10^1000+239, with
arbitrary off-lattice additional speeds and mixed signs. All 204 produced
rational witnesses in a total of 415 trials. Every output was checked again
by direct numerator/remainder arithmetic.

Additional fixtures cover a witness attaining equality 1/15, an unrecognized
spectrum, a deliberately forced trial limit, zero/length/Boolean/floating
input rejection, legal signs and repetitions, and an altered catalog hash.
The exact report binds the interface and replay script by SHA-256.

This interface recognizes only the explicitly listed core families. It does
not claim a complete classification of eight-row covers, test every possible
fourteen-speed tuple, or prove the full Lonely Runner Conjecture.
