#!/usr/bin/env python3
"""Exact rational witness near the symmetric four-edge KKT point."""
from dataclasses import dataclass
from fractions import Fraction as F
from itertools import combinations

def req(x,m):
    if not x: raise ValueError(m)
def sg(a,b):
    if not b:return (a>0)-(a<0)
    if not a:return (b>0)-(b<0)
    if (a>0)==(b>0):return (a>0)-(a<0)
    z=(a*a>3*b*b)-(a*a<3*b*b);return z if a>0 else -z
@dataclass(frozen=True)
class R:
    a:F=F(0);b:F=F(0)
    def __add__(s,o):o=rr(o);return R(s.a+o.a,s.b+o.b)
    __radd__=__add__
    def __neg__(s):return R(-s.a,-s.b)
    def __sub__(s,o):return s+(-rr(o))
    def __rsub__(s,o):return rr(o)-s
    def __mul__(s,o):o=rr(o);return R(s.a*o.a+3*s.b*o.b,s.a*o.b+s.b*o.a)
    __rmul__=__mul__
    def __truediv__(s,o):return R(s.a/F(o),s.b/F(o))
    def __lt__(s,o):z=s-rr(o);return sg(z.a,z.b)<0
    def pos(s):return sg(s.a,s.b)>0
def rr(x):return x if isinstance(x,R) else R(F(x))
def dot(a,b):return a[0]*b[0]+a[1]*b[1]
def det(a,b):return a[0]*b[1]-a[1]*b[0]
def unit(t):return ((1-t*t)/(1+t*t),2*t/(1+t*t))

TA=F(929,49257); TB=F(43133,53882); P=F(7381,21619); Q=F(1,2)-P
TARGET=F(23518745713,10**11)
TRI=((R(),R()),(R(F(1,2)),R()),(R(F(1,4)),R(0,F(1,4))))
ED=((R(1),R()),(R(F(-1,2)),R(0,F(1,2))),(R(F(-1,2)),R(0,F(-1,2))))

def data():
    ca,sa=unit(TA);cb,sb=unit(TB)
    v=((cb,-sb),(ca,-sa),(ca,sa),(cb,sb),(-F(1),F(0)))
    L=(P,Q,Q,P,2*P*cb+2*Q*ca)
    req(2*P+2*Q==1,'length');req(all(dot(x,x)==1 for x in v),'unit')
    req(all(det(v[i],v[(i+1)%5])>0 for i in range(5)),'turn')
    req(all(v[i][0]>0 for i in range(4)) and v[0][1]<v[1][1]<0<v[2][1]<v[3][1],'winding')
    req(all(sum(L[i]*v[i][j] for i in range(5))==0 for j in (0,1)),'closure')
    return v,L
def alloc(v,L):
    A={}
    for I in combinations(range(5),3):
        i,j,k=I;z=[det(v[j],v[k]),det(v[k],v[i]),det(v[i],v[j])]
        if all(x<0 for x in z):z=[-x for x in z]
        if not all(x>0 for x in z):continue
        h=min(L[a]/x for a,x in zip(I,z));q=[F(0)]*5
        for a,x in zip(I,z):q[a]=h*x
        req(all(0<=x<=y for x,y in zip(q,L)),'cap')
        req(all(sum(q[i]*v[i][j] for i in range(5))==0 for j in (0,1)),'bal')
        r=[y-x for x,y in zip(q,L)];req(all(sum(r[i]*v[i][j] for i in range(5))==0 for j in (0,1)),'res')
        A[I]=tuple(q)
    req(tuple(A)==((0,2,4),(0,3,4),(1,2,4),(1,3,4)),'allocations');return A
def rot(x,c,s):return (c*x[0]-s*x[1],s*x[0]+c*x[1])
def tv(q,v,c,s):
    z=R()
    for w,x in zip(q,v):
        if not w:continue
        n=(R(x[1]),R(-x[0]));vals=[dot(rot(y,c,s),n) for y in TRI];h=vals[0]
        for y in vals[1:]:
            if h<y:h=y
        z+=w*h
    return z/2
def tf(q,v):
    V=[]
    for w,x in zip(q,v):
        if not w:continue
        n=(x[1],-x[0])
        for d in ED:
            for e in (-1,1):
                y=(R(-e*n[1]),R(e*n[0]));c=dot(d,y);s=det(d,y);req(c*c+s*s==R(1),'rot');V.append(tv(q,v,c,s))
    m=V[0]
    for x in V[1:]:
        if x<m:m=x
    return m
def formula(q,v,L,sample,lo,hi):
    sn,cs=2*sample/(1+sample*sample),(1-sample*sample)/(1+sample*sample);a=b=F(0)
    for w,l,x in zip(q,L,v):
        if w==l:continue
        raw=x[0]*sn-x[1]*cs;req(raw!=0,'sample');e=1 if raw>0 else -1
        for u in (lo,hi):
            se,ce=2*u/(1+u*u),(1-u*u)/(1+u*u);z=x[0]*se-x[1]*ce
            req(z==0 or (z>0)==(raw>0),'sign cell')
        a+=(l-w)*e*x[0]/4;b+=(l-w)*e*(-x[1])/4
    return a,b
def val(q,a,b,u):return q+a*2*u/(1+u*u)+b*(1-u*u)/(1+u*u)
def verify():
    v,L=data();A=alloc(v,L);zero=(F(0),)*5
    N={'C':A[(1,2,4)],'A':A[(0,2,4)],'S':zero,'B':A[(0,3,4)]}
    QF={n:(R() if n=='S' else tf(q,v)) for n,q in N.items()}
    cuts=(F(0),F(1422669,6341329),F(1,3),F(1363695,1828072),F(1))
    samples={'C':F(1,10),'A':F(1,3),'S':F(1,3),'B':F(4,5)}; margins=[]
    for n,lo,hi in zip(('C','A','S','B'),cuts,cuts[1:]):
        a,b=formula(N[n],v,L,samples[n],lo,hi);req(a>=0 and b>=0,'concavity')
        for u in (lo,hi):
            m=val(QF[n],a,b,u)-TARGET;req(m.pos(),f'endpoint {n} {u}');margins.append(m)
    mu=(3,2,1,0,4);aset=set(A.values())
    req(all(L[i]==L[mu[i]] and v[mu[i]]==(v[i][0],-v[i][1]) for i in range(5)),'mirror')
    req({tuple(q[mu[i]] for i in range(5)) for q in aset}==aset,'mirror alloc')
    req(tf(A[(1,3,4)],v)==QF['A'],'mirror triangle')
    return L,QF,margins
if __name__=='__main__':
    L,QF,M=verify();print('parameters',TA,TB,P,Q);print('closing',L[-1]);print('triangle floors',QF);print('PASS floor >',TARGET)
