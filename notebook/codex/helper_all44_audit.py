"""Audit only the author's normalized mathematical data, by literal grids.

Uses the independent helper inventory, and never reads the author's checker.
All decisions are integer or rational; the C++ kernel enumerates every k.
"""
import argparse
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from math import gcd, lcm
from pathlib import Path
import json
import subprocess
import tempfile


def digest(path):
    return sha256(Path(path).read_bytes()).hexdigest()


def bad(n,q,x):
    modulus=n*x.denominator
    return sum(15*min(r,modulus-r)<modulus for k in range(n)
               for r in [(q*(k*x.denominator+x.numerator))%modulus])


def audit(manifest, inventory, executable, output):
    source=Path(__file__).parent
    data=json.loads(manifest.read_text())
    expected=json.loads(inventory.read_text())
    cores=[tuple(c['speeds']) for c in expected['cores']]
    actual=[tuple(c['pattern']) for c in data['cases']]
    assert len(cores)==len(set(cores))==len(actual)==len(set(actual))==44
    assert set(cores)==set(actual), (set(cores)-set(actual),set(actual)-set(cores))
    assert data['threshold']=='1/15' and data['max_extra_speeds']==6
    assert F(data['total_upper_bound'])==F(61,10)
    # Endpoint equalities are accepted, while the center of a forbidden arc is bad.
    assert bad(1,1,F(1,15))==bad(1,1,F(14,15))==0
    assert bad(1,1,F(0))==1
    # For n=15k+r, increasing k adds 28 to the inequality's slack.
    tail=[]
    for r in range(15):
        k=(31-r+14)//15
        n=15*k+r
        hits=(2*n+14)//15
        slack=10*n-61*hits
        assert n>=31 and slack>=0
        tail.append({'residue':r,'first_n':n,'ceil_2n_over_15':hits,
                     'slack_10n_minus_61ceil':slack,'slack_step_per_15':28})
    result={'status':'sketch; independent Claude or human review required',
            'scope':'44 specified primitive cores, every common positive integer scale, six additional positive speeds below scaled maximum',
            'dimension':{'moving_velocities':14,'total_runners':15,'threshold':'1/15'},
            'manifest_sha256':digest(manifest),'inventory_sha256':digest(inventory),
            'checker_sha256':digest(__file__),
            'kernel_sha256':digest(source/'helper_all44_grid.cpp'),
            'core_inventory_matches':True,'tail_first_n':31,
            'tail_residue_classes':tail,'audits':[]}
    for case in data['cases']:
        P=tuple(case['pattern']);M=P[-1]
        assert P==tuple(sorted(set(P))) and P[0]>0 and gcd(*P)==1
        assert all(type(v) is int for v in P) and M<=10**6
        # Direct physical rows independently confirm full coverage and minimality.
        rows=[{j for j in range(M) if bad(1,w,F(15*j+1,15*M))}
              for w in P[:-1]]
        assert set().union(*rows)==set(range(M))
        assert all(rows[i]-set().union(*(rows[j] for j in range(7) if j!=i))
                   for i in range(7))
        atoms=[(F(x),F(z)) for x,z in case['atoms']]
        assert atoms and all(0<=x<1 and z>=0 for x,z in atoms)
        assert all(not bad(1,v,x) for x,z in atoms for v in P)
        total=sum(z for x,z in atoms)
        assert total==F(case['total']) and 6<total<=F(61,10)
        D=lcm(*(z.denominator for x,z in atoms))
        # These explicit bounds make all kernel sums/products safe: grid products
        # use signed 128 bits, sums <=30*61*10^12/10 use signed 64 bits.
        assert D<=10**12 and all(x.denominator<=10**12 for x,z in atoms)
        assert len(atoms)<=10**6
        entries=[(x.numerator,x.denominator,int(z*D)) for x,z in atoms]
        assert sum(z for a,b,z in entries)<=61*10**12//10
        payload=f'{M} {D} {len(entries)}\n'+ ' '.join(map(str,P))+'\n'
        payload+=''.join(f'{a} {b} {z}\n' for a,b,z in entries)
        text=subprocess.check_output([str(executable)],input=payload,text=True)
        fields=list(map(int,text.split()))
        count,topnum,topden,lifted,nmax=fields[:5]
        pairs=fields[5:]
        assert len(pairs)==2*nmax and topden>0
        expected_count=sum(1 for n in range(1,31) for q in range(1,M*n)
                           if gcd(n,q)==1 and not(n==1 and q in P))
        assert count==expected_count
        record={'tag':case['tag'],'pattern':P,'atoms':len(atoms),
                'positive_atoms':sum(z>0 for x,z in atoms),'total':str(total),
                'finite_columns':count,'finite_max_n':30,
                'finite_maximum':str(F(topnum,topden)),
                'maximizers':list(zip(pairs[::2],pairs[1::2])),
                'literal_scale_range':[1,10],'literal_lift_columns':lifted}
        result['audits'].append(record)
        output.write_text(json.dumps(result,indent=2)+'\n')
        print(case['tag'],count,str(total),str(F(topnum,topden)),flush=True)
    result['complete']=True
    result['case_count']=len(result['audits'])
    result['finite_columns']=sum(c['finite_columns'] for c in result['audits'])
    result['literal_lift_columns']=sum(c['literal_lift_columns'] for c in result['audits'])
    result['maximum_bad_mass']=str(max(F(c['finite_maximum']) for c in result['audits']))
    result['maxima_histogram']=dict(sorted(Counter(P[-1] for P in cores).items()))
    output.write_text(json.dumps(result,indent=2)+'\n')
    print('PASS',result['case_count'],'cores;',result['finite_columns'],'columns;',
          result['literal_lift_columns'],'literal lifts; maximum',result['maximum_bad_mass'])


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('manifest',type=Path)
    p.add_argument('--cores',type=Path,default=Path(__file__).with_name('helper-fortyfour-primitive-cores.json'))
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args()
    with tempfile.TemporaryDirectory(prefix='helper-all44-') as temp:
        executable=Path(temp)/'grid'
        subprocess.run(['c++','-std=c++17','-O3',str(Path(__file__).with_name('helper_all44_grid.cpp')),
                        '-o',str(executable)],check=True)
        audit(a.manifest,a.cores,executable,a.output)
