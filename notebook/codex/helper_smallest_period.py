"""Finite threatening-tuple audit after explicit p3/p4 analytic tails.

The only shared local module is the helper's own clean-room row definition.
"""
from fractions import Fraction as F
from math import lcm
from itertools import combinations
from pathlib import Path
from hashlib import sha256
import json
from helper_charge_audit import rows_through,charge


def redundant(periods):
    return all(lcm(*(periods[:i]+periods[i+1:]))%h==0
               for i,h in enumerate(periods))


def check(p,H):
    rows,_=rows_through(H)
    candidates=[]
    for h,a,B,*_ in rows:
        if h<p or (h==p and B==(0,)):continue
        C=charge(p,h,B)
        if C:candidates.append((C,h,a,B))
    candidates.sort(reverse=True)
    leaders=candidates[:4]
    goal=F(p-1,p)
    cutoff=goal-sum(r[0] for r in leaders)
    assert cutoff==(F(1,10) if p==3 else F(7,60))
    candidates=[r for r in candidates if r[0]>=cutoff]
    counts={'threatening_charge_tuples':0,
            'two_three_redundant':0,'fully_redundant':0}
    survivors=[]
    visited=0

    def dfs(start,chosen,score):
        nonlocal visited
        visited+=1
        need=5-len(chosen)
        if not need:
            if score<goal:return
            counts['threatening_charge_tuples']+=1
            periods=[p]+[r[1] for r in chosen]
            for prime in (2,3):
                vals=[]
                for h in periods:
                    e=0
                    while h%prime==0:h//=prime;e+=1
                    vals.append(e)
                if max(vals)>0 and vals.count(max(vals))<2:return
            counts['two_three_redundant']+=1
            if not redundant(periods):return
            counts['fully_redundant']+=1
            L=lcm(*periods)
            assert L<=10000000,L
            missed=[j for j in range(L) if j%p and
                    all(j%h not in B for _,h,_,B in chosen)]
            assert missed,(p,chosen)
            survivors.append({'charge':str(score),'lcm':L,'missed':missed,
                'rows':[{'h':h,'a':a,'B':B,'charge':str(C)}
                        for C,h,a,B in chosen]})
            return
        for i in range(start,len(candidates)-need+1):
            upper=score+sum(candidates[j][0] for j in range(i,i+need))
            if upper<goal:break
            dfs(i+1,chosen+[candidates[i]],score+candidates[i][0])

    dfs(0,[],F(0))
    return {'smallest_period':p,'finite_period_ceiling':H,
            'nonempty_distinct_candidate_rows':len(rows),
            'four_leaders':[{'h':h,'a':a,'charge':str(C)}
                            for C,h,a,B in leaders],
            'minimum_threatening_charge':str(cutoff),
            'rows_above_cutoff':len(candidates),'dfs_nodes':visited,
            'counts':counts,'survivors':survivors}


if __name__=='__main__':
    out={'p3':check(3,180),'p4':check(4,120),
         'checker_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
         'row_module_sha256':sha256(Path(__file__).with_name('helper_charge_audit.py').read_bytes()).hexdigest()}
    Path(__file__).with_name('helper-smallest-period-audit.json').write_text(
        json.dumps(out,indent=2)+'\n')
    for key,rec in out.items():
        if isinstance(rec,dict):
            print(key,json.dumps({k:v for k,v in rec.items() if k!='survivors'}))
            for s in rec['survivors']:
                print('remaining',[(r['h'],r['a']) for r in s['rows']],
                      s['charge'],len(s['missed']))
