"""Exact exclusion of <=6 maximal-anchor killers containing periods 2,3.

Four filters: endpoint-cover subproblem for k14/15total; common endpoint
index for every row; strict danger/equality safe; only periodic lifts.
No candidate period or numerical tolerance cutoff is used.
"""
from math import gcd,isqrt,lcm
from functools import lru_cache
from pathlib import Path
import json,hashlib

@lru_cache(None)
def divisors(m):
 return tuple(d for d in range(1,m+1) if m%d==0)
@lru_cache(None)
def mask(h,a):
 return sum(1<<j for j in range(h) if min(a*(15*j+1)%(15*h),15*h-a*(15*j+1)%(15*h))<h)
def lift(B,h,L):
 return B*(((1<<L)-1)//((1<<h)-1))
def minimal(L,R):
 for D in divisors(L):
  S=R&((1<<D)-1)
  if lift(S,D,L)==R:return D,S
 raise AssertionError
E={p:tuple(n for n in range(1,1+14*p//(15-2*p)) if p*((2*n+14)//15)>=n) for p in range(1,5)}
graph={}
def visit(p,L,R):
 key=(p,L,hex(R))
 if key in graph:return
 assert R,'A cover has been found'
 graph[key]={'remaining':p,'period':L,'missing_hex':hex(R),'children':[]}
 if p==0:return
 found={}
 for n in E[p]:
  T=L*n;S=lift(R,L,T)
  for h in divisors(T):
   if h<=1 or h//gcd(h,L)!=n:continue
   for a in range(1,h):
    if gcd(a,h)!=1:continue
    B=lift(mask(h,a),h,T)
    hits=(S&B).bit_count()
    if p*hits<n*R.bit_count():continue
    D,Q=minimal(T,S&~B)
    found.setdefault((p-1,D,hex(Q)),(h,a))
 for child,row in sorted(found.items()):
  graph[key]['children'].append({'row':row,'state':child})
  visit(child[0],child[1],int(child[2],16))

if __name__=='__main__':
 assert mask(2,1)==1 and mask(3,1)==1 and mask(3,2)==1
 assert not mask(16,1)&2 # phase16/240=1/15 is safe
 visit(4,6,34)
 data={'status':'sketch; exact complete DAG','scope':'at most six maximal-anchor killers with reduced periods two and three','root':[4,6,'0x22'],'states':list(graph.values()),'count':len(graph),'edges':sum(len(s['children']) for s in graph.values()),'largest_period':max(s['period'] for s in graph.values()),'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
 output=Path(__file__).with_name('six-with-two-three-excluded.json')
 output.write_text(json.dumps(data,indent=2)+'\n')
 print(json.dumps({k:v for k,v in data.items() if k!='states'}))
