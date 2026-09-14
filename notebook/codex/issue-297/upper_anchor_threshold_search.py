"""Exploratory exact bounded-row covering search with speeds below R*anchor.

Common lower endpoints at threshold1/15; strict arcs; only reduced ratios
and periodic lifts. k14,15total. A time/node cap means incomplete evidence.
"""
from math import gcd,lcm,isqrt
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
import time,json,argparse,hashlib
E={p:tuple(n for n in range(1,1+14*p//(15-2*p)) if p*((2*n+14)//15)>=n) for p in range(1,7)}
@lru_cache(None)
def divisors(m):
 out=[]
 for d in range(1,isqrt(m)+1):
  if m%d==0:
   out.append(d)
   if d*d!=m:out.append(m//d)
 return tuple(sorted(out))
def lift(B,h,T):return B*(((1<<T)-1)//((1<<h)-1))
def reduce_state(T,S):
 for L in divisors(T):
  R=S&((1<<L)-1)
  if lift(R,L,T)==S:return L,R
 raise AssertionError

def search(bound,seconds,limit,output,number_rows=5):
 assert 0<bound<=15
 started=time.monotonic();nodes=0;maxL=0;memo={};graphs={};roots_all=[];found=None;aborted=False
 @lru_cache(None)
 def rows(h):
  candidates={}
  for a in range(1,(bound.numerator*h-1)//bound.denominator+1):
   if gcd(a,h)>1:continue
   lo=-((h-1+a)//15);hi=(h-1-a)//15;inv=pow(a,-1,h)
   B=sum(1<<((inv*k)%h) for k in range(lo,hi+1))
   if B:candidates.setdefault(B,a)
  return tuple((a,B) for B,a in candidates.items())
 def visit(p,r,L,R,path):
  nonlocal nodes,maxL,found
  if not R:found=path;return True
  if not r:return False
  key=(p,r,L,R)
  if key in memo:return memo[key]
  nodes+=1;maxL=max(maxL,L)
  if nodes>limit or time.monotonic()-started>seconds:raise TimeoutError
  if nodes%1000==0:print(json.dumps({'nodes':nodes,'base_minimum':p,'max_period':maxL,'elapsed':round(time.monotonic()-started,2)}),flush=True)
  nxt={};need=R.bit_count()
  record={'minimum_period':p,'remaining':r,'period':L,'missing_hex':hex(R),'children':[]}
  graphs[key]=record
  for n in E[r]:
   T=L*n;S=lift(R,L,T)
   for h in divisors(T):
    if h<p or h//gcd(h,L)!=n:continue
    for a,B in rows(h):
     H=(S&lift(B,h,T)).bit_count()
     if r*H<n*need:continue
     Q=reduce_state(T,S&~lift(B,h,T))
     nxt.setdefault(Q,((h,a),Fraction(H,n*need)))
  for (K,Q),((h,a),gain) in sorted(nxt.items(),key=lambda z:(-z[1][1],z[0][0],z[1][0])):
   record['children'].append({'row':[h,a],'state':[p,r-1,K,hex(Q)]})
   if visit(p,r-1,K,Q,path+[(h,a)]):memo[key]=True;return True
  memo[key]=False;return False
 reports=[]
 try:
  for p in range(2,1+13*number_rows//(15-2*number_rows)):
   before=nodes;roots=0
   for a,B in rows(p):
    roots+=1;L,R=reduce_state(p,((1<<p)-1)^B)
    roots_all.append({'row':[p,a],'state':[p,number_rows-1,L,hex(R)]})
    if visit(p,number_rows-1,L,R,[(p,a)]):break
   reports.append({'minimum_period':p,'roots':roots,'states':nodes-before})
   print(json.dumps(reports[-1]),flush=True)
   if found:break
 except TimeoutError:aborted=True
 if found:
  M=lcm(*(h for h,a in found));speeds=sorted(M*a//h for h,a in found)
  assert all(any(min(w*(15*j+1)%(15*M),15*M-w*(15*j+1)%(15*M))<M for w in speeds) for j in range(M))
  witness={'anchor':M,'killers':speeds,'largest_ratio':str(Fraction(max(speeds),M)),'reduced_rows':found}
 else:witness=None
 result={'status':'numerical/exact exploratory search','number_rows':number_rows,'ratio_bound_strict':str(bound),'complete':not aborted,'cover_found':witness,'nodes':nodes,'maximum_residual_period':maxL,'reports':reports,'elapsed_seconds':time.monotonic()-started}
 if output:
  report_path=Path(output);graph_path=report_path.with_suffix('.graph.json')
  graph_path.write_text(json.dumps({'number_rows':number_rows,'ratio_bound_strict':str(bound),'minimum_period_bound':13*number_rows//(15-2*number_rows),'roots':roots_all,'complete':not aborted,'cover_found':witness,'states':list(graphs.values())},sort_keys=True,separators=(',',':'))+'\n')
  result['graph_file']=graph_path.name;result['graph_sha256']=hashlib.sha256(graph_path.read_bytes()).hexdigest();result['code_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest();result['edges']=sum(len(s['children']) for s in graphs.values());result['roots']=len(roots_all)
  report_path.write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result),flush=True)
 return result
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--rows',type=int,default=5,choices=range(2,8));parser.add_argument('--ratio',default='3/2');parser.add_argument('--seconds',type=int,default=120);parser.add_argument('--limit',type=int,default=1000000);parser.add_argument('--output');ns=parser.parse_args()
 search(Fraction(ns.ratio),ns.seconds,ns.limit,ns.output,ns.rows)
