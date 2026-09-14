"""Clean-room exact charge audit from the mathematical specification.

No imports of repository checker code. Every computation is bounded by H.
"""
from fractions import Fraction as F
from math import gcd
from collections import defaultdict
import argparse
import json


def row(h, a):
    inv = pow(a, -1, h)
    first = -h + 1 + ((a + h - 1) % 15)
    return tuple(sorted((inv * ((e-a)//15)) % h
                        for e in range(first, h, 15)))


def direct_row(h, a):
    return tuple(j for j in range(h)
                 if min(a*(15*j+1) % (15*h),
                        (-a*(15*j+1)) % (15*h)) < h)


def valuation(h, prime):
    result = 0
    while h % prime == 0:
        h //= prime
        result += 1
    return result


def rows_through(H):
    result = []
    duplicates = 0
    for h in range(2,H+1):
        seen = set()
        for a in range(1,h):
            if gcd(a,h) != 1:
                continue
            B = row(h,a)
            if h <= 60:
                assert B == direct_row(h,a), (h,a,B,direct_row(h,a))
            if not B:
                continue
            if B in seen:
                duplicates += 1
                continue
            seen.add(B)
            result.append((h,a,B,valuation(h,2),valuation(h,3)))
    return result, duplicates


def charge(p,h,B):
    d=gcd(p,h)
    return F(len(B),h) - F(d*sum(b%d == 0 for b in B),p*h)


def rank(p,rows):
    candidates=[]
    for h,a,B,e2,e3 in rows:
        if h < p or (h==p and B==(0,)):
            continue
        C=charge(p,h,B)
        if C:
            candidates.append((C,h,a,B,e2,e3))
    max2=max(r[4] for r in candidates)
    max3=max(r[5] for r in candidates)
    answer=[]
    for E2 in range(valuation(p,2),max2+1):
        for E3 in range(valuation(p,3),max3+1):
            need2=0 if E2==0 else 2-int(valuation(p,2)==E2)
            need3=0 if E3==0 else 2-int(valuation(p,3)==E3)
            groups=defaultdict(list)
            for r in candidates:
                if r[4] <= E2 and r[5] <= E3:
                    groups[(int(E2>0 and r[4]==E2),
                            int(E3>0 and r[5]==E3))].append(r)
            shortlist=[]
            for key, rs in groups.items():
                for r in sorted(rs, reverse=True)[:5]:
                    shortlist.append((key,r))
            dp={(0,0,0):(F(0),())}
            for (f2,f3), r in shortlist:
                for (n,n2,n3),(score,selection) in list(dp.items()):
                    if n==5:
                        continue
                    key=(n+1,min(need2,n2+f2),min(need3,n3+f3))
                    val=(score+r[0],selection+(r,))
                    if key not in dp or val[0]>dp[key][0]:
                        dp[key]=val
            if (5,need2,need3) in dp:
                score,selection=dp[(5,need2,need3)]
                answer.append({'E2':E2,'E3':E3,'score':str(score),
                    'rows':[{'h':r[1],'a':r[2], 'charge':str(r[0]),
                             'B':r[3]} for r in selection]})
    answer.sort(key=lambda x:F(x['score']),reverse=True)
    return answer


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--H',type=int,default=200)
    parser.add_argument('--output')
    args=parser.parse_args()
    assert direct_row(1,1)==(), 'threshold equality must survive'
    rows,duplicates=rows_through(args.H)
    out={'H':args.H, 'distinct_nonempty_rows':len(rows),
         'same_period_duplicates_removed':duplicates,
         'p3':rank(3,rows),'p4':rank(4,rows)}
    text=json.dumps(out,indent=2)
    if args.output:
        with open(args.output,'w') as f:f.write(text+'\n')
    print(json.dumps({k:out[k] for k in ('H','distinct_nonempty_rows',
                                      'same_period_duplicates_removed')}))
    for p in (3,4):
        print('p',p)
        for rec in out['p'+str(p)][:12]:
            print(rec['E2'],rec['E3'],rec['score'],
                  [(r['h'],r['a'],r['charge']) for r in rec['rows']])


if __name__=='__main__':main()
