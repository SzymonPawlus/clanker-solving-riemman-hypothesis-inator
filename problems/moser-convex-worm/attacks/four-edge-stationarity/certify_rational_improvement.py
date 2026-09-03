#!/usr/bin/env python3
"""Exact certificate for a perturbed symmetric four-edge support witness."""

from dataclasses import dataclass
from fractions import Fraction as Q
from itertools import combinations


def need(ok,msg):
    if not ok: raise ValueError(msg)


def sign(a,b):
    if not b:return (a>0)-(a<0)
    if not a:return (b>0)-(b<0)
    if (a>0)==(b>0):return (a>0)-(a<0)
    z=(a*a>3*b*b)-(a*a<3*b*b)
    return z if a>0 else -z


@dataclass(frozen=True)
class S:
    a:Q=Q(0);b:Q=Q(0)
    def __add__(self,z):z=lift(z);return S(self.a+z.a,self.b+z.b)
    __radd__=__add__
    def __neg__(self):return S(-self.a,-self.b)
    def __sub__(self,z):return self+(-lift(z))
    def __rsub__(self,z):return lift(z)-self
    def __mul__(self,z):
        z=lift(z);return S(self.a*z.a+3*self.b*z.b,self.a*z.b+self.b*z.a)
    __rmul__=__mul__
    def __truediv__(self,z):return S(self.a/Q(z),self.b/Q(z))
    def __lt__(self,z):return sign((self-lift(z)).a,(self-lift(z)).b)<0
    def positive(self):return sign(self.a,self.b)>0
def lift(z):return z if isinstance(z,S) else S(Q(z))


def det(a,b):return a[0]*b[1]-a[1]*b[0]
def dot(a,b):return a[0]*b[0]+a[1]*b[1]
def unit(t):return ((1-t*t)/(1+t*t),2*t/(1+t*t))


TA=Q(1,53);TB=Q(313,391);P=Q(169,495);QINNER=Q(1,2)-P
TARGET=Q(11759,50000) # 0.23518
TRI=((S(),S()),(S(Q(1,2)),S()),(S(Q(1,4)),S(0,Q(1,4))))
TEDGES=((S(1),S()),(S(Q(-1,2)),S(0,Q(1,2))),(S(Q(-1,2)),S(0,Q(-1,2))))


def geometry():
    ca,sa=unit(TA);cb,sb=unit(TB)
    vs=((cb,-sb),(ca,-sa),(ca,sa),(cb,sb),(-Q(1),Q(0)))
    closing=2*P*cb+2*QINNER*ca
    loads=(P,QINNER,QINNER,P,closing)
    need(2*P+2*QINNER==1,'worm length')
    need(all(dot(v,v)==1 for v in vs),'unit vectors')
    need(all(det(vs[i],vs[(i+1)%5])>0 for i in range(5)),'turns')
    need(all(vs[i][0]>0 for i in range(4)) and
         vs[0][1]<vs[1][1]<0<vs[2][1]<vs[3][1],'winding-one order')
    need(all(sum(loads[i]*vs[i][j] for i in range(5))==0 for j in (0,1)),'closure')
    return vs,loads


def allocations(vs,loads):
    ans={}
    for I in combinations(range(5),3):
        i,j,k=I;ray=[det(vs[j],vs[k]),det(vs[k],vs[i]),det(vs[i],vs[j])]
        if all(z<0 for z in ray):ray=[-z for z in ray]
        if not all(z>0 for z in ray):continue
        lam=min(loads[a]/z for a,z in zip(I,ray));x=[Q(0)]*5
        for a,z in zip(I,ray):x[a]=lam*z
        need(all(0<=z<=e for z,e in zip(x,loads)),'capacity')
        need(all(sum(x[i]*vs[i][j] for i in range(5))==0 for j in (0,1)),'allocated balance')
        r=[e-z for e,z in zip(loads,x)]
        need(all(sum(r[i]*vs[i][j] for i in range(5))==0 for j in (0,1)),'residual balance')
        ans[I]=tuple(x)
    need(tuple(ans)==((0,2,4),(0,3,4),(1,2,4),(1,3,4)),'cycles')
    return ans


def rot(v,c,s):return (c*v[0]-s*v[1],s*v[0]+c*v[1])
def tri_value(x,vs,c,s):
    total=S()
    for z,v in zip(x,vs):
        if not z:continue
        n=(S(v[1]),S(-v[0]));vals=[dot(rot(p,c,s),n) for p in TRI];h=vals[0]
        for w in vals[1:]:
            if h<w:h=w
        total+=z*h
    return total/2
def tri_floor(x,vs):
    vals=[]
    for z,v in zip(x,vs):
        if not z:continue
        n=(Q(v[1]),Q(-v[0]))
        for d in TEDGES:
            for e in (-1,1):
                target=(S(-e*n[1]),S(e*n[0]));c=dot(d,target);s=det(d,target)
                need(c*c+s*s==S(1),'rotation');vals.append(tri_value(x,vs,c,s))
    m=vals[0]
    for z in vals[1:]:
        if z<m:m=z
    # These exhaust all support switches; fixed-support cells are concave.
    return m


def coefficients(x,vs,loads,u,lo,hi):
    sn,cs=2*u/(1+u*u),(1-u*u)/(1+u*u);a=b=Q(0)
    for z,e,v in zip(x,loads,vs):
        r=e-z
        if not r:continue
        raw=v[0]*sn-v[1]*cs;need(raw!=0,'sign sample')
        sg=1 if raw>0 else -1
        for endpoint in (lo,hi):
            se,ce=2*endpoint/(1+endpoint*endpoint),(1-endpoint*endpoint)/(1+endpoint*endpoint)
            endpoint_raw=v[0]*se-v[1]*ce
            need(endpoint_raw==0 or (endpoint_raw>0)==(raw>0),'projection sign cell')
        a+=r*sg*v[0]/4;b+=r*sg*(-v[1])/4
    return a,b
def value(q,a,b,u):return q+a*(2*u/(1+u*u))+b*((1-u*u)/(1+u*u))


def main():
    vs,loads=geometry();xs=allocations(vs,loads);zero=(Q(0),)*5
    named={'C':xs[(1,2,4)],'A':xs[(0,2,4)],'S':zero,'B':xs[(0,3,4)]}
    qs={n:(S() if n=='S' else tri_floor(x,vs)) for n,x in named.items()}
    samples={'C':Q(1,10),'A':Q(1,3),'S':Q(1,3),'B':Q(4,5)}
    # Rational cuts bracket the numerical A/C and S/B crossings. Every
    # coefficient is nonnegative, so each formula is concave on its cell.
    cuts=(Q(0),Q(22435,100000),Q(1,3),Q(74597,100000),Q(1))
    ranges={n:(lo,hi) for n,lo,hi in zip(('C','A','S','B'),cuts,cuts[1:])}
    coeff={n:coefficients(x,vs,loads,samples[n],*ranges[n]) for n,x in named.items()}
    margins=[]
    for n,lo,hi in zip(('C','A','S','B'),cuts,cuts[1:]):
        a,b=coeff[n];need(a>=0 and b>=0,'concavity coefficients')
        for u in (lo,hi):
            margin=value(qs[n],a,b,u)-TARGET
            need(margin.positive(),f'endpoint {n} {u}')
            margins.append((n,u,margin))
    mirror=(3,2,1,0,4);aset=set(xs.values())
    need(all(loads[i]==loads[mirror[i]] and
             vs[mirror[i]]==(vs[i][0],-vs[i][1]) for i in range(5)),'mirror data')
    need({tuple(x[mirror[i]] for i in range(5)) for x in aset}==aset,'mirror allocations')
    need(tri_floor(xs[(1,3,4)],vs)==qs['A'],'mirrored triangle floor')
    print('half angles',TA,TB,'outer/inner lengths',P,QINNER)
    print('closing chord',loads[-1]);print('triangle floors',qs);print('coefficients',coeff)
    print('endpoint margins');[print(x) for x in margins]
    print('PASS: complete direct-motion support floor >',TARGET)


if __name__=='__main__':main()
