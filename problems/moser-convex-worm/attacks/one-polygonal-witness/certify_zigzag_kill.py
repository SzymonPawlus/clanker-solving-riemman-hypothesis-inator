"""Exact Q(sqrt(3)) placement certificate killing the first zigzag candidate."""
from fractions import Fraction as F
import math

SQ3_LO=F(1732050807568877,10**15); SQ3_HI=F(1732050807568878,10**15)
assert SQ3_LO*SQ3_LO < 3 < SQ3_HI*SQ3_HI
class A:
    def __init__(self,a=0,b=0): self.a,self.b=F(a),F(b)
    def __add__(self,o): o=aa(o); return A(self.a+o.a,self.b+o.b)
    __radd__=__add__
    def __neg__(self): return A(-self.a,-self.b)
    def __sub__(self,o): return self+-aa(o)
    def __rsub__(self,o): return aa(o)+-self
    def __mul__(self,o):
        o=aa(o); return A(self.a*o.a+3*self.b*o.b,self.a*o.b+self.b*o.a)
    __rmul__=__mul__
    def bounds(self):
        x0,x1=(SQ3_LO,SQ3_HI) if self.b>=0 else (SQ3_HI,SQ3_LO)
        return self.a+self.b*x0,self.a+self.b*x1
    def mid(self): return float(self.a)+float(self.b)*math.sqrt(3)
def aa(x): return x if isinstance(x,A) else A(x)
def q(x,d=10**7): return F(round(x*d),d)
def ratrot(theta):
    t=q(math.tan(theta/2)); den=1+t*t
    return (1-t*t)/den,2*t/den
def place(poly,tx,ty,theta):
    c,s=ratrot(theta); tx,ty=A(q(tx,10**6)),A(q(ty,10**6))
    return [(x*c-y*s+tx,x*s+y*c+ty) for x,y in poly]
def cross(o,p,q): return (p[0]-o[0])*(q[1]-o[1])-(p[1]-o[1])*(q[0]-o[0])
SEG=[(A(0),A(0)),(A(1),A(0))]
TRI=[(A(0),A(0)),(A(F(1,2)),A(0)),(A(F(1,4)),A(0,F(1,4)))]
SQUARE=[(A(0),A(0)),(A(F(1,3)),A(0)),(A(F(1,3)),A(F(1,3))),(A(0),A(F(1,3)))]
ZIG=[(A(0),A(0)),(A(F(1,4)),A(0)),(A(F(2,5)),A(F(1,5))),
     (A(F(1,5)),A(F(7,20))),(A(F(-1,20)),A(F(7,20)))]
POSE=[0.0001707773998844343,-0.00019926725184776821,5.273255169353027,
      0.09377463766064506,-0.1382205145751953,5.235896053073482,
      0.24224575773303902,-0.3870746355193751,0.37047446722614424]
pts=SEG+place(TRI,*POSE[:3])+place(SQUARE,*POSE[3:6])+place(ZIG,*POSE[6:9])
def approximate_hull(ids):
    ids=sorted(ids,key=lambda i:(pts[i][0].mid(),pts[i][1].mid())); lo=[]; hi=[]
    for i in ids:
        while len(lo)>=2 and cross(pts[lo[-2]],pts[lo[-1]],pts[i]).mid()<=0: lo.pop()
        lo.append(i)
    for i in reversed(ids):
        while len(hi)>=2 and cross(pts[hi[-2]],pts[hi[-1]],pts[i]).mid()<=0: hi.pop()
        hi.append(i)
    return lo[:-1]+hi[:-1]
h=approximate_hull(range(len(pts))); margin=None
for k,i in enumerate(h):
    j=h[(k+1)%len(h)]
    for p in range(len(pts)):
        lo,_=cross(pts[i],pts[j],pts[p]).bounds(); assert lo>=0
        if lo and (margin is None or lo<margin): margin=lo
twice=A(0)
for k,i in enumerate(h):
    j=h[(k+1)%len(h)]; twice+=pts[i][0]*pts[j][1]-pts[j][0]*pts[i][1]
lo,hi=twice.bounds(); assert hi/2 < F(232239,10**6)
print({'hull':h,'area_lower':float(lo/2),'area_upper':float(hi/2),
       'containment_margin':float(margin),'record_threshold':0.232239})
