"""Independent all-scale audit of the 160 nine-speed core measures.

Only the author's mathematical JSON is read. The previously frozen independent
literal-grid kernel is reused unchanged. It checks n<=30 (including the required
n<=14) and reads the eight smaller core speeds; the maximal core speed is outside
q<M at n=1, so omitting it from that exclusion list is exact.
"""
import argparse
from fractions import Fraction as F
from hashlib import sha256
from math import gcd,lcm
from pathlib import Path
import json
import subprocess
import tempfile


def digest(path):
    return sha256(Path(path).read_bytes()).hexdigest()


def main(manifest,inventory,output):
    source=Path(__file__).parent
    data=json.loads(manifest.read_text())
    census=json.loads(inventory.read_text())
    assert census['complete'] is True and census['row_count']==8
    expected=[tuple(c['speeds']) for c in census['cores']]
    actual=[tuple(c['pattern']) for c in data['cases']]
    assert len(expected)==len(set(expected))==len(actual)==len(set(actual))==160
    assert set(expected)==set(actual)
    assert data['fixed_speeds']==9 and data['extra_speeds']==5
    assert F(data['mass_cap'])==F(51,10) and data['tail_starts']==15
    assert 51*(2*15+14)<=150*15  # Tail slack increases by 48 per n.
    result={'status':'sketch; independent Claude or human review required',
            'manifest_sha256':digest(manifest),'inventory_sha256':digest(inventory),
            'checker_sha256':digest(__file__),'kernel_sha256':digest(source/'helper_all44_grid.cpp'),
            'scope':'160 specified nine-speed cores, every positive integer scale, five additional positive speeds below scaled maximum',
            'moving_velocities':14,'total_runners':15,'threshold':'1/15',
            'tail':{'first_n':15,'slack_150n_minus_51times_2nplus14':6,'slack_step':48},
            'audits':[]}
    with tempfile.TemporaryDirectory(prefix='helper-eight-phase-') as tmp:
        exe=Path(tmp)/'grid'
        subprocess.run(['c++','-std=c++17','-O3',str(source/'helper_all44_grid.cpp'),'-o',str(exe)],check=True)
        for i,case in enumerate(data['cases'],1):
            P=tuple(case['pattern']);M=P[-1]
            assert len(P)==9 and all(type(v) is int for v in P)
            assert P==tuple(sorted(set(P))) and P[0]>0 and gcd(*P)==1 and M<=10**6
            atoms=[(F(x),F(z)) for x,z in case['atoms']]
            assert atoms and all(0<=x<1 and z>0 for x,z in atoms)
            total=sum(z for x,z in atoms)
            assert total==F(case['total']) and 5<total<=F(51,10)
            for x,z in atoms:
                for v in P:
                    residue=(v*x.numerator)%x.denominator
                    assert 15*min(residue,x.denominator-residue)>=x.denominator
            D=lcm(*(z.denominator for x,z in atoms))
            assert D<=10**12 and all(x.denominator<=10**12 for x,z in atoms)
            assert len(atoms)<=10**6
            entries=[(x.numerator,x.denominator,int(z*D)) for x,z in atoms]
            assert sum(z for a,b,z in entries)<=51*10**12//10
            payload=f'{M} {D} {len(entries)}\n'+' '.join(map(str,P[:-1]))+'\n'
            payload+=''.join(f'{a} {b} {z}\n' for a,b,z in entries)
            fields=list(map(int,subprocess.check_output([str(exe)],input=payload,text=True).split()))
            count,num,den,lifted,nmax=fields[:5];pairs=fields[5:]
            assert len(pairs)==2*nmax and den>0
            def columns(H):
                return sum(1 for n in range(1,H+1) for q in range(1,M*n)
                           if gcd(n,q)==1 and not(n==1 and q in P))
            assert count==columns(30)
            record={'index':i,'pattern':P,'total':str(total),'positive_atoms':len(atoms),
                    'required_columns_n_to14':columns(14),
                    'checked_columns_n_to30':count,'finite_maximum':str(F(num,den)),
                    'maximizers':list(zip(pairs[::2],pairs[1::2])),
                    'literal_lift_scale_range':[1,10],'literal_lift_columns':lifted}
            result['audits'].append(record)
            output.write_text(json.dumps(result,indent=2)+'\n')
            if i%10==0:print(i,'cores checked',flush=True)
    result.update(complete=True,core_count=160,
                  positive_atoms=sum(r['positive_atoms'] for r in result['audits']),
                  required_columns_n_to14=sum(r['required_columns_n_to14'] for r in result['audits']),
                  checked_columns_n_to30=sum(r['checked_columns_n_to30'] for r in result['audits']),
                  literal_lift_columns=sum(r['literal_lift_columns'] for r in result['audits']),
                  least_mass=str(min(F(r['total']) for r in result['audits'])),
                  maximum_bad_mass=str(max(F(r['finite_maximum']) for r in result['audits'])))
    output.write_text(json.dumps(result,indent=2)+'\n')
    print({k:v for k,v in result.items() if k not in ('audits','tail')},flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('manifest',type=Path)
    p.add_argument('--inventory',type=Path,default=Path(__file__).with_name('helper-eight-core-to30.json'))
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();main(a.manifest,a.inventory,a.output)
