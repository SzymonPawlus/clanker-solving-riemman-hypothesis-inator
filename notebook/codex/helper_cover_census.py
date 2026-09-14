"""Independent exhaustive minimal seven-row maximal-anchor cover census.

Each search branches on one uncovered residue. Branches partition covers
according to the first available row covering that residue, so no cover is
lost or counted twice. A timeout is explicitly incomplete, never no-cover.
"""
from math import gcd
from functools import reduce
from itertools import combinations
from pathlib import Path
from hashlib import sha256
from time import perf_counter
import argparse,json


def census(M,seconds):
    start=perf_counter()
    full=(1<<M)-1
    columns=[]
    for w in range(1,M):
        mask=sum(1<<j for j in range(M)
                 if min(w*(15*j+1)%(15*M),(-w*(15*j+1))%(15*M))<M)
        if mask:columns.append((w,mask))
    # Reorder for search only. Each column still represents one actual speed.
    columns.sort(key=lambda item:(-item[1].bit_count(),item[0]))
    coverers=[sum(1<<i for i,(_,mask) in enumerate(columns) if mask>>r&1)
              for r in range(M)]
    nodes=0
    primitive=[]
    all_count=0
    without_half=0
    without_period_three=0
    smaller=[]
    seen=set()

    def walk(covered,available,chosen,private):
        nonlocal nodes,all_count,without_half,without_period_three
        nodes+=1
        if nodes%10000==0 and perf_counter()-start>seconds:raise TimeoutError
        if covered==full:
            speeds=tuple(sorted(columns[i][0] for i in chosen))
            if len(chosen)<7:
                smaller.append(speeds)
                return
            masks=[columns[i][1] for i in chosen]
            private=[]
            for i,mask in enumerate(masks):
                other=0
                for j,mask2 in enumerate(masks):
                    if j!=i:other|=mask2
                private.append(mask&~other)
            if not all(private):return
            assert speeds not in seen,speeds
            seen.add(speeds)
            all_count+=1
            without_half+=int(M%2!=0 or M//2 not in speeds)
            without_period_three+=int(not any(M//gcd(M,w)==3 for w in speeds))
            if reduce(gcd,speeds+(M,))==1:
                private_by_speed={columns[i][0]:[r for r in range(M) if mask>>r&1]
                                  for i,mask in zip(chosen,private)}
                primitive.append({'speeds':speeds+(M,),
                                  'private_residues':private_by_speed,
                                  'reduced_periods':[M//gcd(M,w) for w in speeds]})
            return
        slots=7-len(chosen)
        if not slots or available.bit_count()<slots:return
        missing=full^covered
        gains=[]
        union=covered
        bits=available
        while bits:
            bit=bits&-bits;bits-=bit;i=bit.bit_length()-1
            gain=(columns[i][1]&missing).bit_count()
            if gain:gains.append(gain);union|=columns[i][1]
        if union!=full or sum(sorted(gains,reverse=True)[:slots])<missing.bit_count():return
        best_options=None
        remain=missing
        while remain:
            bit=remain&-remain;remain-=bit;r=bit.bit_length()-1
            options=available&coverers[r]
            if not options:return
            if best_options is None or options.bit_count()<best_options.bit_count():
                best_options=options
        options=best_options
        branch_available=available
        while options:
            bit=options&-options;options-=bit
            branch_available &= ~bit
            i=bit.bit_length()-1
            next_private=tuple(mask&~columns[i][1] for mask in private)
            # Once a selected row has no private residue among the selected
            # rows, adding further rows can never restore minimality.
            if not all(next_private):continue
            next_private+=(columns[i][1]&~covered,)
            walk(covered|columns[i][1],branch_available,chosen+(i,),next_private)

    complete=True
    try:walk(0,(1<<len(columns))-1,(),())
    except TimeoutError:complete=False
    primitive.sort(key=lambda rec:rec['speeds'])
    return {'M':M,'complete':complete,'elapsed_seconds':perf_counter()-start,
            'search_nodes':nodes,'nonempty_columns':len(columns),
            'minimal_seven_covers':all_count,'primitive_seven_covers':len(primitive),
            'covers_without_half_speed':without_half,
            'covers_without_period_three':without_period_three,
            'primitive_certificates':primitive,'covers_with_fewer_than_seven':smaller}


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--anchors',required=True)
    p.add_argument('--seconds',type=float,default=60)
    p.add_argument('--output',required=True)
    a=p.parse_args()
    anchors=list(map(int,a.anchors.split(',')))
    out={'checker_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),'anchors':[]}
    for M in anchors:
        record=census(M,a.seconds)
        out['anchors'].append(record)
        Path(a.output).write_text(json.dumps(out,indent=2)+'\n')
        print(json.dumps({k:v for k,v in record.items()
                          if k not in ('primitive_certificates','covers_with_fewer_than_seven')}),flush=True)
