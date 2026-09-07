#!/usr/bin/env python3
"""Clean-room exact audit of PR #195's finite support certificate."""
from dataclasses import dataclass
from fractions import Fraction as F
from itertools import combinations

def need(ok,msg):
    if not ok: raise ArithmeticError(msg)

@dataclass(frozen=True)
class S3:
    q:F=F(0); r:F=F(0)             # q+r*sqrt(3)
    def __add__(self,z): z=cast(z); return S3(self.q+z.q,self.r+z.r)
    __radd__=__add__
    def __neg__(self): return S3(-self.q,-self.r)
    def __sub__(self,z): return self+-cast(z)
    def __rsub__(self,z): return cast(z)-self
    def __mul__(self,z):
        z=cast(z); return S3(self.q*z.q+3*self.r*z.r,self.q*z.r+self.r*z.q)
    __rmul__=__mul__
    def __truediv__(self,z):
        z=cast(z); d=z.q*z.q-3*z.r*z.r
        return S3((self.q*z.q-3*self.r*z.r)/d,(self.r*z.q-self.q*z.r)/d)
    def sign(self):
        if self.r==0: return (self.q>0)-(self.q<0)
        if self.q==0: return (self.r>0)-(self.r<0)
        if (self.q>0)==(self.r>0): return 1 if self.q>0 else -1
        cmp=(self.q*self.q>3*self.r*self.r)-(self.q*self.q<3*self.r*self.r)
        return cmp if self.q>0 else -cmp
    def __lt__(self,z): return (self-cast(z)).sign()<0
    def __le__(self,z): return (self-cast(z)).sign()<=0
    def __gt__(self,z): return (self-cast(z)).sign()>0

def cast(z): return z if isinstance(z,S3) else S3(F(z))
rt3=S3(0,1)
def unit(t): return ((1-t*t)/(1+t*t),2*t/(1+t*t))
def det(a,b): return a[0]*b[1]-a[1]*b[0]
def dot(a,b): return a[0]*b[0]+a[1]*b[1]

tb,ta,p=F(43133,53882),F(929,49257),F(7381,21619)
q=F(1,2)-p
cb,sb=unit(tb); ca,sa=unit(ta)
v=((cb,-sb),(ca,-sa),(ca,sa),(cb,sb),(F(-1),F(0)))
L=(p,q,q,p,2*(p*cb+q*ca))
need(p>0 and q>0 and 2*p+2*q==1,"open arc is not positive unit length")
need(all(dot(w,w)==1 for w in v),"non-unit tangent")
need(sum(L[i]*v[i][0] for i in range(5))==0 and
     sum(L[i]*v[i][1] for i in range(5))==0,"surface does not close")
need(all(det(v[i],v[(i+1)%5])>0 for i in range(5)),"not strict winding-one")

# Enumerate rather than assume the positive three-direction circuits.
circuits={}
for I in combinations(range(5),3):
    i,j,k=I; raw=(det(v[j],v[k]),det(v[k],v[i]),det(v[i],v[j]))
    if all(a>0 for a in raw) or all(a<0 for a in raw):
        r=tuple(abs(a) for a in raw); scale=min(L[a]/b for a,b in zip(I,r))
        x=[F(0)]*5
        for a,b in zip(I,r): x[a]=scale*b
        need(all(F(0)<=x[a]<=L[a] for a in range(5)),"capacity failure")
        need(sum(x[a]*v[a][0] for a in range(5))==0 and
             sum(x[a]*v[a][1] for a in range(5))==0,"balance failure")
        circuits[I]=tuple(x)
need(set(circuits)=={(0,2,4),(0,3,4),(1,2,4),(1,3,4)},
     "unexpected positive-circuit list")

def triangle_floor(I,x):
    values=[]
    for i in I:
        total=S3()
        for j in I:
            qx,qy=det(v[i],v[j]),-dot(v[i],v[j])
            total += x[j]*max(S3(),cast(qx)/2,(cast(qx)+rt3*qy)/4)
        values.append(total/2)
    return min(values)

zero=(F(0),)*5
loads={"S":zero,"C":circuits[(1,2,4)],"A":circuits[(0,2,4)],
       "D":circuits[(1,3,4)],"B":circuits[(0,3,4)]}
tau={"S":S3()}
for name,I in (("C",(1,2,4)),("A",(0,2,4)),("D",(1,3,4)),("B",(0,3,4))):
    tau[name]=triangle_floor(I,loads[name])

def value(name,u):
    co=(1-u*u)/(1+u*u); si=2*u/(1+u*u)
    residual=F(0)
    for w,l,x in zip(v,L,loads[name]): residual+=(l-x)*abs(w[1]*co-w[0]*si)
    return tau[name]+residual/4

def no_wall(name,a,b):
    for w,l,x in zip(v,L,loads[name]):
        if l==x: continue
        f=lambda u:w[1]*(1-u*u)-2*w[0]*u
        need(f(a)*f(b)>=0,f"{name} residual crosses a projection wall")

target=F(23518745713,100000000000)
cells=(("C",F(0),F(224348713,1000000000)),
       ("A",F(224348713,1000000000),F(1,3)),
       ("S",F(1,3),F(745974447,1000000000)),
       ("B",F(745974447,1000000000),F(1)))
for name,a,b in cells:
    no_wall(name,a,b)
    need(value(name,a)>target,f"{name} left endpoint misses target")
    need(value(name,b)>target,f"{name} right endpoint misses target")

# Exact reflection-free half-turn involution: reverse traversed indices and
# reflect the angle parameter about pi/2; A and D exchange.
rev=(3,2,1,0,4)
need(all(L[i]==L[rev[i]] for i in range(5)),"length reversal fails")
need(tau["A"]==tau["D"],"crossed triangle constants do not mirror")
need(all(loads["D"][rev[i]]==loads["A"][i] for i in range(5)),
     "crossed allocation does not mirror")

margin=value("C",F(0))-target
need(margin>0,"headline endpoint margin is nonpositive")
print("PASS: independent exact audit of 0.23518745713")
print("limiting phi=0 margin = q + r*sqrt(3)")
print("q =",margin.q)
print("r =",margin.r)
print("positive circuits:",sorted(circuits))
