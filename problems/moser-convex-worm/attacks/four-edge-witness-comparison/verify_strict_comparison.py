#!/usr/bin/env python3
"""Independent exact comparison of the PR #191 and PR #192 witnesses."""

from dataclasses import dataclass
from fractions import Fraction as F


@dataclass(frozen=True)
class Q3:
    a: F = F(0)
    b: F = F(0)
    def __add__(self, z):
        z = lift(z); return Q3(self.a+z.a, self.b+z.b)
    __radd__ = __add__
    def __sub__(self, z):
        z = lift(z); return Q3(self.a-z.a, self.b-z.b)
    def __rsub__(self, z): return lift(z)-self
    def __mul__(self, z):
        z = lift(z)
        return Q3(self.a*z.a+3*self.b*z.b, self.a*z.b+self.b*z.a)
    __rmul__ = __mul__
    def __truediv__(self, z):
        z = lift(z); d=z.a*z.a-3*z.b*z.b
        return Q3((self.a*z.a-3*self.b*z.b)/d,
                  (self.b*z.a-self.a*z.b)/d)
    def __neg__(self): return Q3(-self.a,-self.b)
    def sign(self):
        if not self.b: return (self.a>0)-(self.a<0)
        if not self.a: return (self.b>0)-(self.b<0)
        if self.a > 0 and self.b > 0: return 1
        if self.a < 0 and self.b < 0: return -1
        # Opposite signs: compare |a| with sqrt(3)|b| without approximation.
        s = (self.a*self.a > 3*self.b*self.b) - (self.a*self.a < 3*self.b*self.b)
        return s if self.a > 0 else -s
    def __lt__(self,z): return (self-lift(z)).sign() < 0
    def __le__(self,z): return (self-lift(z)).sign() <= 0
    def __gt__(self,z): return (self-lift(z)).sign() > 0
    def __ge__(self,z): return (self-lift(z)).sign() >= 0


def lift(z): return z if isinstance(z,Q3) else Q3(F(z),F(0))
SQ3 = Q3(0,1)

def require(condition, message):
    if not condition:
        raise ArithmeticError(message)


def unit(t): return ((1-t*t)/(1+t*t), 2*t/(1+t*t))
def cross(v,w): return v[0]*w[1]-v[1]*w[0]
def dot(v,w): return v[0]*w[0]+v[1]*w[1]


def tau(vec, x, support):
    vals=[]
    for i in support:
        total=Q3()
        for j in support:
            qx, qy = cross(vec[i],vec[j]), -dot(vec[i],vec[j])
            candidates=(Q3(), lift(qx)/2, (lift(qx)+SQ3*qy)/4)
            total += x[j]*max(candidates)
        vals.append(total/2)
    return min(vals)


def witness(tb,ta,p):
    q=F(1,2)-p
    cb,sb=unit(tb); ca,sa=unit(ta)
    vec=[(cb,-sb),(ca,-sa),(ca,sa),(cb,sb),(F(-1),F(0))]
    R=2*(p*cb+q*ca); L=[p,q,q,p,R]
    z=q*sa/sb
    alloc={
        "S":[F(0)]*5,
        "C":[F(0),q,q,F(0),2*q*ca],
        "B":[p,F(0),F(0),p,2*p*cb],
        "A":[z,F(0),q,F(0),z*cb+q*ca],
    }
    floors={"S":Q3()}
    for name,support in (("C",(1,2,4)),("B",(0,3,4)),("A",(0,2,4))):
        floors[name]=tau(vec,alloc[name],support)
    return vec,L,alloc,floors


def at_u(W,name,u):
    vec,L,alloc,floors=W
    cp=(1-u*u)/(1+u*u); sp=2*u/(1+u*u)
    residual=F(0)
    for v,l,x in zip(vec,L,alloc[name]):
        residual += (l-x)*abs(v[1]*cp-v[0]*sp)
    return floors[name]+residual/4


def stable_signs(W,name,a,b):
    vec,L,alloc,_=W
    for v,l,x in zip(vec,L,alloc[name]):
        if l == x: continue
        def s(u): return v[1]*(1-u*u)-v[0]*2*u
        require(s(a)*s(b) >= 0, f"projection wall in {name} interval")


T=F(117593,500000)             # 0.235186
W191=witness(F(313,391),F(1,53),F(169,495))
W192=witness(F(19999,25000),F(3,200),F(683,2000))

# Each named residual formula is concave on its interval.  Exact endpoint
# values therefore bound the complete first quadrant from below.
cover=(("C",F(0),F(4487,20000)),
       ("A",F(4487,20000),F(1,3)),
       ("S",F(1,3),F(74597,100000)),
       ("B",F(74597,100000),F(1)))
for name,a,b in cover:
    stable_signs(W191,name,a,b)
    require(at_u(W191,name,a) > T, f"low left endpoint for {name}")
    require(at_u(W191,name,b) > T, f"low right endpoint for {name}")

# The full envelope of W192 is at most any one of its point values.  At phi=0
# its maximum is C (checked exactly), and that value is below T.
v192=[at_u(W192,name,F(0)) for name in ("S","C","A","B")]
require(max(v192) == v192[1], "C is not active for W192 at phi=0")
require(v192[1] < T, "W192 phi=0 value did not fall below threshold")

print("PASS: floor(W191) > 117593/500000 > floor(W192)")
print("W191 endpoint margins (exact signs):")
for name,a,b in cover:
    print(name,(at_u(W191,name,a)-T).sign(),(at_u(W191,name,b)-T).sign())
