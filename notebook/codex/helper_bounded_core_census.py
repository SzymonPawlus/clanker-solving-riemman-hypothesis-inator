"""Exact bounded core census plus complete safe rational endpoint universes."""
import argparse
from fractions import Fraction as F
from hashlib import sha256
from math import comb,gcd
from pathlib import Path
import json
import subprocess
import tempfile


def core_record(P):
    M=P[-1]
    masks=[{j for j in range(M)
            if min(w*(15*j+1)%(15*M),(-w*(15*j+1))%(15*M))<M}
           for w in P[:-1]]
    assert gcd(*P)==1 and set().union(*masks)==set(range(M))
    private={w:sorted(masks[i]-set().union(*(masks[j] for j in range(len(masks)) if i!=j)))
             for i,w in enumerate(P[:-1])}
    assert all(private.values())
    # Both sides of every strict forbidden arc, with coincident points deduped.
    all_endpoints=sorted({F(15*j+s,15*w)%1 for w in P for j in range(w) for s in(-1,1)})
    safe=[x for x in all_endpoints
          if all(min((w*x)%1,(-w*x)%1)>=F(1,15) for w in P)]
    return {'speeds':P,'private_residues':private,
            'endpoint_universe_size':len(all_endpoints),
            'safe_endpoints':list(map(str,safe)),
            'reduced_periods':[M//gcd(M,w) for w in P[:-1]]}


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--rows',type=int,choices=[7,8],default=8)
    p.add_argument('--min-M',type=int,default=9)
    p.add_argument('--max-M',type=int,default=30)
    p.add_argument('--output',required=True,type=Path)
    a=p.parse_args();assert 2<=a.min_M<=a.max_M<=30
    source=Path(__file__).with_suffix('.cpp')
    with tempfile.TemporaryDirectory(prefix='helper-core-census-') as temp:
        executable=Path(temp)/'census'
        subprocess.run(['c++','-std=c++17','-O3',str(source),'-o',str(executable)],check=True)
        raw=subprocess.check_output([str(executable)],input=f'{a.min_M} {a.max_M} {a.rows}\n',text=True)
    cores=[];summaries=[]
    for line in raw.splitlines():
        tag,*values=line.split();values=list(map(int,values))
        if tag=='C':
            M,*speeds=values;assert len(speeds)==a.rows
            P=tuple(speeds)+(M,)
            assert P==tuple(sorted(set(P)))
            cores.append(core_record(P))
        else:
            assert tag=='S'
            M,subsets,covered,primitive,minimal=values
            assert subsets==comb(M-1,a.rows)
            summaries.append({'M':M,'subsets':subsets,'full_covers':covered,
                              'primitive_full_covers':primitive,
                              'primitive_minimal_covers':minimal})
    assert sum(r['primitive_minimal_covers'] for r in summaries)==len(cores)
    assert len({tuple(c['speeds']) for c in cores})==len(cores)
    result={'status':'numerical; exact bounded enumeration, no unbounded classification',
            'threshold':'1/15','moving_velocities':14,'total_runners':15,
            'fixed_core_size':a.rows+1,'additional_speeds':13-a.rows,
            'row_count':a.rows,'anchor_range':[a.min_M,a.max_M],
            'quotients':'none; every physical subset enumerated',
            'source_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
            'kernel_sha256':sha256(source.read_bytes()).hexdigest(),
            'complete':True,'core_count':len(cores),
            'subsets_checked':sum(r['subsets'] for r in summaries),
            'anchors':summaries,'cores':cores}
    a.output.write_text(json.dumps(result,indent=2)+'\n')
    for r in summaries:print(r['M'],r['subsets'],r['primitive_minimal_covers'])
    print('PASS',len(cores),'cores,',result['subsets_checked'],'literal subsets')
