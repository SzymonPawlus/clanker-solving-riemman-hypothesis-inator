"""Clean-room rational-atom universal dual audit using direct grid residues."""
from fractions import Fraction as F
from pathlib import Path
from hashlib import sha256
from math import gcd,lcm
import argparse
import json
from helper_p18_dual_check import tail_classes


def direct_count(n,q,x):
    modulus=n*x.denominator
    return sum(15*min(v,modulus-v)<modulus
               for k in range(n)
               for v in [(q*(k*x.denominator+x.numerator))%modulus])


def verify(path,H):
    data=json.loads(Path(path).read_text())
    P=tuple(data['pattern'])
    assert len(P)==8 and P==tuple(sorted(set(P))) and P[0]>0
    if 'atoms' in data:
        atoms=[(F(x),F(z)) for x,z in data['atoms']]
        declared_total=F(data['total'])
    else:
        assert len(data['types'])==len(data['weights'])
        atoms=[(F(15*r+1,15*u),F(z))
               for (u,r),z in zip(data['types'],data['weights'])]
        declared_total=F(data['mass'])
    assert all(0<=x<1 and z>=0 for x,z in atoms)
    S=sum(z for x,z in atoms)
    assert S==declared_total and 6<S<=F(61,10),(S,declared_total)
    # Duplicate locations are harmless; merge them explicitly.
    grouped={}
    for x,z in atoms:grouped[x]=grouped.get(x,F(0))+z
    atoms=sorted((x,z) for x,z in grouped.items() if z)
    for x,z in atoms:
        assert all(direct_count(1,u,x)==0 for u in P),('unsafe atom',x,P)
    denominator=lcm(*(z.denominator for x,z in atoms))
    integer_atoms=[(x,int(z*denominator)) for x,z in atoms]
    count=0
    maximum=F(0)
    maximizers=[]
    for n in range(1,H+1):
        for q in range(1,max(P)*n):
            if gcd(n,q)>1 or (n==1 and q in P):continue
            raw=sum(z*direct_count(n,q,x) for x,z in integer_atoms)
            value=F(raw,n*denominator)
            assert value<=1,(path,n,q,value)
            if value>maximum:maximum,maximizers=value,[(n,q)]
            elif value==maximum:maximizers.append((n,q))
            count+=1
    cutoff,classes=tail_classes(S)
    assert H>=cutoff-1
    # Direct test of uniform lifting at all c<=10, not inferred via quotient.
    lifted_columns=0
    for c in range(1,11):
        for w in range(1,max(P)*c):
            if w in {c*u for u in P}:continue
            g=gcd(c,w)
            n,q=c//g,w//g
            direct=sum(z*direct_count(c,w,x) for x,z in atoms)/c
            reduced=sum(z*direct_count(n,q,x) for x,z in atoms)/n
            assert direct==reduced and direct<=1,(c,w,direct,reduced)
            lifted_columns+=1
    return {'source_file':Path(path).name,'pattern':P,'positive_atoms':len(atoms),
            'total':str(S),'finite_max_n':H,'finite_columns':count,
            'finite_maximum':str(maximum),'maximizers':maximizers,
            'analytic_tail_start':cutoff,'tail_residue_classes':classes,
            'literal_scale_range':[1,10],'literal_lift_columns':lifted_columns,
            'certificate_sha256':sha256(Path(path).read_bytes()).hexdigest()}


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('certificates',nargs='+')
    p.add_argument('--H',type=int,default=30)
    p.add_argument('--output',required=True)
    a=p.parse_args()
    out={'audits':[],'checker_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
         'tail_module_sha256':sha256(Path(__file__).with_name('helper_p18_dual_check.py').read_bytes()).hexdigest()}
    for path in a.certificates:
        result=verify(path,a.H)
        out['audits'].append(result)
        print(result['source_file'],result['total'],result['positive_atoms'],
              result['finite_columns'],result['finite_maximum'],flush=True)
    Path(a.output).write_text(json.dumps(out,indent=2)+'\n')
