"""Direct independent finite check for the positive-strip residue-15 lemma."""
from fractions import Fraction as F
from hashlib import sha256
from math import gcd
from pathlib import Path
import json

masks={a:sum(1<<j for j in range(15) if (a*j)%15 in (0,14)) for a in range(15)}
assert masks[0]==(1<<15)-1
units={j for j in range(15) if gcd(j,15)==1}
assert len(units)==8
for a in range(1,15):
    unit_hits={j for j in units if masks[a]>>j&1}
    assert len(unit_hits)==int(gcd(a,15)==1)
minimum=15;minimizers=[];cover_count=0
for subset in range(1<<14):
    chosen=[a for a in range(1,15) if subset>>(a-1)&1]
    union=0
    for a in chosen:union|=masks[a]
    if union==(1<<15)-1:
        cover_count+=1
        if len(chosen)<minimum:minimum=len(chosen);minimizers=[chosen]
        elif len(chosen)==minimum:minimizers.append(chosen)
assert minimum==10 and len(minimizers)==8
x=F(2,163);checks=0
for a in range(-80,81):
    if not a:continue
    b=-(a*x.numerator//x.denominator)
    alpha=a*x+b;assert 0<alpha<1
    for j in range(15):
        z=(x+j)/15
        phase=(a*z+F(b,15))%1
        assert phase not in (F(1,15),F(14,15))
        assert (min(phase,1-phase)<F(1,15))==((a*j)%15 in (0,14))
        checks+=1
report=dict(status='sketch support; independent residue and phase checks',
            checker_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
            nonzero_residue_subsets=1<<14,covering_subsets=cover_count,
            minimum_rows_without_zero_residue=minimum,minimal_ten_residue_sets=minimizers,
            literal_affine_phase_checks=checks)
Path(__file__).with_name('helper-affine-residue15-audit.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS minimum',minimum,'rows without slope divisible15;',checks,'literal phases')
