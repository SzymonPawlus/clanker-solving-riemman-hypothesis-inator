"""Exact primitive-core census conditional on reduced periods two and three.

Uses independently audited greedy multiplier sets, explicit phase masks,
minimality preservation, and the necessary final-lcm=normalized-anchor test.
"""
from math import gcd,lcm
from pathlib import Path
from hashlib import sha256
from time import perf_counter
import json,argparse

E={1:{1},2:{1,2},3:{1,2,3},4:{1,2,3,4,8},
   5:{1,2,3,4,5,8,9,10}}
FUTURE={0:{1}}
for r in range(1,6):FUTURE[r]={a*b for a in E[r] for b in FUTURE[r-1]}


def audit_anchor(M,seconds):
    start=perf_counter()
    assert M%6==0
    full=(1<<M)-1
    columns=[]
    for w in range(1,M):
        mask=sum(1<<j for j in range(M)
            if min(w*(15*j+1)%(15*M),(-w*(15*j+1))%(15*M))<M)
        columns.append((w,M//gcd(M,w),mask))
    columns.sort(key=lambda x:(-x[2].bit_count(),x[0]))
    index={w:i for i,(w,h,mask) in enumerate(columns)}
    i2,i3=index[M//2],index[M//3]
    mask2,mask3=columns[i2][2],columns[i3][2]
    chosen=(i2,i3)
    private=(mask2&~mask3,mask3&~mask2)
    available=((1<<len(columns))-1)^(1<<i2)^(1<<i3)
    seen=set();certificates=[];nodes=0;lcm_prunes=0;gain_prunes=0

    def walk(covered,L,available,chosen,private):
        nonlocal nodes,lcm_prunes,gain_prunes
        nodes+=1
        if nodes%10000==0 and perf_counter()-start>seconds:raise TimeoutError
        r=7-len(chosen)
        if M%L or M//L not in FUTURE[r]:
            lcm_prunes+=1;return
        if covered==full:
            if r or L!=M:return
            assert all(private)
            for third_speed in (M//3,2*M//3):
                speeds=tuple(sorted(third_speed if i==i3 else columns[i][0]
                                    for i in chosen))+(M,)
                assert speeds not in seen
                seen.add(speeds)
                cert={third_speed if i==i3 else columns[i][0]:
                      [j for j in range(M) if mask>>j&1]
                      for i,mask in zip(chosen,private)}
                certificates.append({'speeds':speeds,'private_residues':cert})
            return
        if not r:return
        missing=full^covered
        threshold=(missing.bit_count()+r-1)//r
        options=[]
        filtered=available
        gains=[]
        bits=available
        while bits:
            bit=bits&-bits;bits-=bit;i=bit.bit_length()-1
            w,h,mask=columns[i]
            gain=(mask&missing).bit_count()
            if not gain or any(not(old&~mask) for old in private):
                filtered&=~bit;continue
            gains.append(gain)
            n=h//gcd(h,L)
            if gain>=threshold and n in E[r] and M//lcm(L,h) in FUTURE[r-1]:
                options.append((gain,i))
        if sum(sorted(gains,reverse=True)[:r])<missing.bit_count():
            gain_prunes+=1;return
        # Covers partition by the first selected eligible high-gain row.
        # Earlier alternatives are removed only in later sibling branches.
        options.sort(reverse=True)
        for gain,i in options:
            bit=1<<i
            filtered&=~bit
            w,h,mask=columns[i]
            next_private=tuple(old&~mask for old in private)+(mask&~covered,)
            walk(covered|mask,lcm(L,h),filtered,chosen+(i,),next_private)

    complete=True
    try:walk(mask2|mask3,6,available,chosen,private)
    except TimeoutError:complete=False
    return {'M':M,'complete':complete,'elapsed_seconds':perf_counter()-start,
            'nodes':nodes,'lcm_prunes':lcm_prunes,'gain_prunes':gain_prunes,
            'primitive_count':len(certificates),
            'primitive_certificates':sorted(certificates,key=lambda rec:rec['speeds'])}


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--anchors',default='12,18,24,30,36,48,54,60,72,90,96,108,120,144,162,180,192,216,240,270,288,324,360,384,432,480,540,576,720,768,864,960,1080,1152,1440,1920,2880')
    parser.add_argument('--seconds',type=float,default=90)
    parser.add_argument('--output',required=True)
    a=parser.parse_args()
    out={'checker_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
         'per_anchor_seconds_cap':a.seconds,'anchors':[]}
    for M in map(int,a.anchors.split(',')):
        rec=audit_anchor(M,a.seconds)
        out['anchors'].append(rec)
        Path(a.output).write_text(json.dumps(out,indent=2)+'\n')
        print(json.dumps({k:v for k,v in rec.items() if k!='primitive_certificates'}),flush=True)
