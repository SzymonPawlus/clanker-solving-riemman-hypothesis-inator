"""Exact bounded decision driver and literal validation of found speed sets."""
import argparse
from hashlib import sha256
from math import gcd
from pathlib import Path
import json
import subprocess
import tempfile


def verified_cover(M,speeds,forbidden):
    P=sorted(set(speeds))+[M]
    assert len(P)==len(speeds)+1
    g=gcd(*P);P=[v//g for v in P];N=P[-1]
    masks={w:{j for j in range(N)
              if min(w*(15*j+1)%(15*N),(-w*(15*j+1))%(15*N))<N}
           for w in P[:-1]}
    assert set().union(*masks.values())==set(range(N))
    # Remove any redundant choices; the decision solver is for at most eight.
    for w in list(masks):
        if set().union(*(b for v,b in masks.items() if v!=w))==set(range(N)):
            del masks[w]
    P=sorted(masks)+[N];g=gcd(*P)
    if g>1:return verified_cover(N,[w for w in P[:-1]],forbidden)
    private={w:sorted(b-set().union(*(bb for v,bb in masks.items() if v!=w)))
             for w,b in masks.items()}
    assert all(private.values())
    periods=[N//gcd(N,w) for w in P[:-1]]
    assert not(set(periods)&set(forbidden))
    return {'primitive_speeds':P,'private_residues':private,'reduced_periods':periods}


def one(exe,M,slots,forbidden,seconds):
    raw=subprocess.check_output([str(exe)],input=f'{M} {slots} {int(2 in forbidden)} {int(3 in forbidden)} {seconds}\n',text=True).split()
    actual,complete,found,nodes,hits,prunes,cached=map(int,raw[:7]);elapsed=float(raw[7]);size=int(raw[8]);speeds=list(map(int,raw[9:]))
    assert actual==M and len(speeds)==size and bool(found)==bool(size)
    assert not found or complete
    return {'M':M,'complete':bool(complete),'nodes':nodes,'cache_hits':hits,
            'gain_prunes':prunes,'cached_failures':cached,'elapsed_seconds':elapsed,
            'cover':verified_cover(M,speeds,forbidden) if found else None}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--first',type=int,default=241)
    p.add_argument('--last',type=int,default=400);p.add_argument('--seconds',type=int,default=10)
    p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    assert 9<=a.first<=a.last<=512
    source=Path(__file__).with_suffix('.cpp')
    with tempfile.TemporaryDirectory(prefix='helper-no23-memo-') as tmp:
        exe=Path(tmp)/'memo'
        subprocess.run(['c++','-std=c++17','-O3',str(source),'-o',str(exe)],check=True)
        fixtures=[one(exe,18,7,(),10),one(exe,20,8,(),10),one(exe,30,8,(2,3),10)]
        assert fixtures[0]['cover'] and fixtures[1]['cover']
        assert fixtures[2]['complete'] and not fixtures[2]['cover']
        report={'status':'numerical; exact bounded decision only','range':[a.first,a.last],
                'max_rows':8,'forbidden_periods':[2,3],'seconds_cap_per_anchor':a.seconds,
                'source_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
                'kernel_sha256':sha256(source.read_bytes()).hexdigest(),
                'fixtures':fixtures,'anchors':[]}
        for M in range(a.first,a.last+1):
            rec=one(exe,M,8,(2,3),a.seconds);report['anchors'].append(rec)
            a.output.write_text(json.dumps(report,indent=2)+'\n')
            print(M,rec['complete'],rec['nodes'],rec['elapsed_seconds'],bool(rec['cover']),flush=True)
            if rec['cover']:break
        report['incomplete_anchors']=[r['M'] for r in report['anchors'] if not r['complete']]
        report['completed_anchors']=sum(r['complete'] for r in report['anchors'])
        report['covers_found']=sum(r['cover'] is not None for r in report['anchors'])
        a.output.write_text(json.dumps(report,indent=2)+'\n')
