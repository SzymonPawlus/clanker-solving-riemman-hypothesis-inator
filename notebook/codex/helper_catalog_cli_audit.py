"""Independent black-box check of all204 documented catalog CLI families.

The solver and its author checker are neither read nor imported. Inputs are
generated here; returned rational times are checked directly on original
signed velocities using integer arithmetic.
"""
import argparse
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
import random
import subprocess
import sys
import tempfile
import time


p=argparse.ArgumentParser()
p.add_argument('--interface',type=Path,required=True)
p.add_argument('--output',type=Path,required=True)
a=p.parse_args()
interface=a.interface.resolve()
catalog=interface.parent/'witness_catalog'
patterns=[]
source_hashes={}
for name in ('all-forty-four-cores.json','eight-core-phase-to30.json'):
    raw=(catalog/name).read_bytes()
    source_hashes[name]=sha256(raw).hexdigest()
    patterns.extend(tuple(c['pattern']) for c in json.loads(raw)['cases'])
assert len(patterns)==len(set(patterns))==204
patterns_set=set(patterns)
rng=random.Random(9202614)
scales=(1,2,15,97,10**100+7,10**1000+239)
records=[]
started=time.monotonic()
with tempfile.TemporaryDirectory() as td:
    td=Path(td)
    ip,op=td/'input.json',td/'output.json'
    for index,P in enumerate(patterns):
        c=scales[index%len(scales)]
        M=c*max(P)
        values={c*v for v in P}
        while len(values)<14:
            values.add(rng.randrange(1,M))
        values=[-v if i%3==0 else v for i,v in enumerate(sorted(values))]
        rng.shuffle(values)
        payload=[str(v) for v in values] if index%2 else {'velocities':values}
        ip.write_text(json.dumps(payload))
        proc=subprocess.run([sys.executable,str(interface),'--input',str(ip),'--output',str(op),
                             '--seed',str(31*index+5),'--max-trials','10000'],
                            capture_output=True,text=True,timeout=20)
        assert proc.returncode==0,(index,proc.returncode,proc.stderr)
        result=json.loads(op.read_text())
        assert result['status']=='witness'
        t=Fraction(result['time'])
        assert 0<=t<1
        num,den=t.numerator,t.denominator
        distances=[Fraction(min(v*num%den,-v*num%den),den) for v in values]
        assert all(15*d.numerator>=d.denominator for d in distances),(index,values,result)
        assert Fraction(result['minimum_distance'])==min(distances)
        chosen=tuple(result['primitive_core'])
        assert chosen in patterns_set
        scale=int(result['scale'])
        assert scale>0 and max(chosen)*scale==max(map(abs,values))
        assert all(scale*v in {abs(w) for w in values} for v in chosen)
        assert source_hashes[result['source_manifest']]==result['source_sha256']
        assert 1<=result['trials']<=10000
        records.append(dict(pattern=list(P),scale_digits=len(str(c)),
                            trials=result['trials'],minimum_distance=str(min(distances))))
        if (index+1)%34==0:
            print(f'{index+1}/204 documented CLI families independently verified',flush=True)
    # This vector already has the obvious witness1/15 but is outside the
    # listed core families; an unrecognized result must not assert failure.
    ip.write_text(json.dumps(list(range(1,15))))
    proc=subprocess.run([sys.executable,str(interface),'--input',str(ip),'--output',str(op)],
                        capture_output=True,text=True,timeout=20)
    assert proc.returncode==2
    unrecognized=json.loads(op.read_text())
    assert unrecognized['status']!='witness'
    # Repeated speeds and opposite signs add no constraint; this recognized
    # eight-speed core is padded to fourteen original coordinates.
    P=patterns[0]
    values=list(P)+[-P[0],P[0],-P[1],P[1],-P[2],P[2]]
    assert len(values)==14
    ip.write_text(json.dumps(values))
    proc=subprocess.run([sys.executable,str(interface),'--input',str(ip),'--output',str(op),'--seed','19'],
                        capture_output=True,text=True,timeout=20)
    assert proc.returncode==0
    t=Fraction(json.loads(op.read_text())['time'])
    assert all(15*min(v*t.numerator%t.denominator,-v*t.numerator%t.denominator)>=t.denominator for v in values)
report=dict(status='PASS; independently checked exact outputs, no theorem status promotion',
            black_box_family_cases=len(records),original_coordinate_inequalities=14*len(records),
            total_trials=sum(r['trials'] for r in records),
            maximum_scale_digits=max(r['scale_digits'] for r in records),
            extra_checks=['unrecognized valid spectrum','signed repeated inputs'],
            interface_sha256=sha256(interface.read_bytes()).hexdigest(),
            checker_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
            source_hashes=source_hashes,elapsed_seconds=time.monotonic()-started,cases=records)
a.output.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='cases'}),flush=True)
