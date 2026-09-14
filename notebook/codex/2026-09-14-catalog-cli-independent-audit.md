# Preserved independent black-box audit of the witness catalog interface

Status: exact output validation; no mathematical theorem status promotion.
The underlying universal measure claims remain `sketch` pending Claude or
human review.

Root wrote `helper_catalog_cli_audit.py` after reading the public interface
documentation and the mathematical manifest data. It did not read or
import the solver or its author checker. The helper preserved that checker
unchanged and reran it against the documented command-line interface.

One independently generated fourteen-velocity completion from each of the
204 distinct catalog families passes. The six scales `1`, `2`, `15`, `97`,
`10^100+7`, and `10^1000+239` are cycled across the 204 cases. The test uses
mixed signs, shuffled coordinates, arbitrary additional positive absolute
speeds below the core maximum, and both numeric and decimal-string JSON
input. All returned rational times are checked directly on the original
signed inputs with exact integer remainder inequalities.

All 2,856 original-coordinate inequalities pass. The 204 runs use 485
sampling trials in total and include scales of 1,001 digits. The selected
core membership, common scale, manifest hash, reported minimum distance,
and trial count are also checked. A further signed-repetition fixture
passes. The valid spectrum `{1,...,14}`, whose witness is `1/15`, is
correctly unrecognized by the limited catalog instead of being treated as
a witness from an absent core family.

The fresh report is `helper-catalog-cli-audit.json`; the initial root
report is `helper-catalog-cli-root-audit.json`. They bind the checker,
interface and both unchanged source manifests by SHA-256. The copied
checker is root's independent implementation, not a claim of another
independently authored helper implementation.

Replay `helper_catalog_cli_audit.py --interface PATH/TO/catalog_witness.py
--output PATH`. The public interface takes its catalog from its adjacent
tracked `witness_catalog` directory. The rerun completed in 16.48 seconds.
These successful exact outputs are individually checkable certificates;
this finite test does not certify every possible input or an unbounded
running-time guarantee.
