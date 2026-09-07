#!/usr/bin/env python3
"""Exact-rational Krawczyk isolation of the symmetric four-edge KKT point."""
from dataclasses import dataclass
from fractions import Fraction as Q
from math import isqrt

N=3
def req(condition,message):
    if not condition:raise RuntimeError(message)

@dataclass(frozen=True)
class I:
    lo:Q;hi:Q
    def __post_init__(s):
        if s.lo>s.hi:raise ValueError('reversed interval')
    def __add__(s,o):o=iv(o);return I(s.lo+o.lo,s.hi+o.hi)
    __radd__=__add__
    def __neg__(s):return I(-s.hi,-s.lo)
    def __sub__(s,o):return s+(-iv(o))
    def __rsub__(s,o):return iv(o)-s
    def __mul__(s,o):
        o=iv(o);z=[s.lo*o.lo,s.lo*o.hi,s.hi*o.lo,s.hi*o.hi];return I(min(z),max(z))
    __rmul__=__mul__
    def inv(s):
        if s.lo<=0<=s.hi:raise ValueError('zero division')
        return I(1/s.hi,1/s.lo) if s.lo>0 else I(1/s.hi,1/s.lo)
    def __truediv__(s,o):return s*iv(o).inv()
    def mid(s):return (s.lo+s.hi)/2
    def interior(s,o):return o.lo<s.lo and s.hi<o.hi
def iv(x):return x if isinstance(x,I) else I(Q(x),Q(x))
def sqrti(x,places=70):
    x=iv(x)
    if x.lo<0:raise ValueError('negative sqrt')
    scale=10**places
    def floorroot(q):return isqrt(q.numerator*scale*scale//q.denominator)
    a=floorroot(x.lo);b=floorroot(x.hi)
    lo=Q(a,scale);hi=Q(b+1,scale)
    if lo*lo>x.lo or hi*hi<x.hi:raise ValueError('sqrt enclosure')
    return I(lo,hi)

@dataclass
class D:
    v:I;g:list;h:list
    @staticmethod
    def const(x):return D(iv(x),[iv(0) for _ in range(N)],[[iv(0) for _ in range(N)] for _ in range(N)])
    @staticmethod
    def var(x,k):
        z=D.const(x);z.g[k]=iv(1);return z
    def __add__(s,o):
        o=dd(o);return D(s.v+o.v,[s.g[i]+o.g[i] for i in range(N)],[[s.h[i][j]+o.h[i][j] for j in range(N)] for i in range(N)])
    __radd__=__add__
    def __neg__(s):return D(-s.v,[-x for x in s.g],[[-x for x in r] for r in s.h])
    def __sub__(s,o):return s+(-dd(o))
    def __rsub__(s,o):return dd(o)-s
    def __mul__(s,o):
        o=dd(o);g=[s.g[i]*o.v+s.v*o.g[i] for i in range(N)]
        h=[[s.h[i][j]*o.v+s.g[i]*o.g[j]+s.g[j]*o.g[i]+s.v*o.h[i][j] for j in range(N)] for i in range(N)]
        return D(s.v*o.v,g,h)
    __rmul__=__mul__
    def unary(s,val,fp,fpp):
        return D(val,[fp*s.g[i] for i in range(N)],[[fp*s.h[i][j]+fpp*s.g[i]*s.g[j] for j in range(N)] for i in range(N)])
    def inv(s):
        val=s.v.inv();return s.unary(val,-val*val,2*val*val*val)
    def __truediv__(s,o):return s*dd(o).inv()
    def sqrt(s):
        val=sqrti(s.v);fp=iv(1)/(2*val);fpp=-iv(1)/(4*val*val*val);return s.unary(val,fp,fpp)
def dd(x):return x if isinstance(x,D) else D.const(x)

def wells(box):
    a,b,p=[D.var(box[i],i) for i in range(3)];q=Q(1,2)-p
    ca=(1-a*a)/(1+a*a);sa=2*a/(1+a*a);cb=(1-b*b)/(1+b*b);sb=2*b/(1+b*b)
    r3=D.const(sqrti(iv(3)));sd=sb*ca-cb*sa
    yo=sb*(ca*r3-sa)/(4*sd);zo=(1-yo*yo).sqrt()
    u=(2*cb+(3+cb*cb).sqrt())/(3*sb);yc=2*u/(1+u*u)
    E=q*ca*r3/4+p*sb/2
    O=q*ca*r3/4+p*(cb*yo+sb*zo)/2
    M=p*sb/4+q*ca*yc
    return E,O,M

def inverse(A):
    n=len(A);B=[list(r)+[Q(i==j) for j in range(n)] for i,r in enumerate(A)]
    for i in range(n):
        k=max(range(i,n),key=lambda z:abs(B[z][i]));B[i],B[k]=B[k],B[i]
        z=B[i][i]
        if not z:raise ValueError('singular midpoint')
        B[i]=[x/z for x in B[i]]
        for k in range(n):
            if k==i:continue
            z=B[k][i];B[k]=[x-z*y for x,y in zip(B[k],B[i])]
    return [r[n:] for r in B]
def matvec(A,x):return [sum((A[i][j]*x[j] for j in range(len(x))),iv(0)) for i in range(len(A))]
def cross(a,b):return [a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]]
def fmt(x):return '[%.17g, %.17g]'%(float(x.lo),float(x.hi))

def system(X):
    W=wells(X[:3]);le,lO=X[3],X[4];lm=iv(1)-le-lO
    F=[W[0].v-W[1].v,W[0].v-W[2].v]
    F += [le*W[0].g[k]+lO*W[1].g[k]+lm*W[2].g[k] for k in range(3)]
    J=[[iv(0) for _ in range(5)] for _ in range(5)]
    for j in range(3):J[0][j]=W[0].g[j]-W[1].g[j];J[1][j]=W[0].g[j]-W[2].g[j]
    for k in range(3):
        for j in range(3):J[k+2][j]=le*W[0].h[k][j]+lO*W[1].h[k][j]+lm*W[2].h[k][j]
        J[k+2][3]=W[0].g[k]-W[2].g[k];J[k+2][4]=W[1].g[k]-W[2].g[k]
    return F,J,W

def certify():
    centers=[Q(18860263338563645,10**18),Q(8005085184891370,10**16),Q(34141264634940915,10**17),Q(4908466867025911,10**16),Q(4374218430906998,10**16)]
    radii=[Q(1,10**14),Q(1,10**14),Q(1,10**14),Q(1,10**13),Q(1,10**13)]
    X=[I(c-r,c+r) for c,r in zip(centers,radii)];x0=[I(c,c) for c in centers]
    F0,J0,_=system(x0);_,JX,W=system(X)
    C=inverse([[J0[i][j].mid() for j in range(5)] for i in range(5)])
    base=[iv(centers[i])-z for i,z in enumerate(matvec(C,F0))]
    R=[[iv(Q(i==j))-sum((iv(C[i][k])*JX[k][j] for k in range(5)),iv(0)) for j in range(5)] for i in range(5)]
    delta=[I(-r,r) for r in radii];K=[base[i]+z for i,z in enumerate(matvec(R,delta))]
    if not all(K[i].interior(X[i]) for i in range(5)):
        raise RuntimeError('Krawczyk inclusion fails: '+repr([(float(X[i].lo),float(X[i].hi),float(K[i].lo),float(K[i].hi)) for i in range(5)]))
    lm=iv(1)-X[3]-X[4];req(X[3].lo>0 and X[4].lo>0 and lm.lo>0,'multiplier positivity')
    L=W[0].v;req(L.lo>Q(23518745713,10**11) and L.hi<Q(23518745716,10**11),'value isolation')
    d1=[W[0].g[i]-W[1].g[i] for i in range(3)];d2=[W[0].g[i]-W[2].g[i] for i in range(3)]
    tangent=cross(d1,d2)
    req(any(t.lo>0 or t.hi<0 for t in tangent),'constraint gradients may be dependent')
    H=[[X[3]*W[0].h[i][j]+X[4]*W[1].h[i][j]+lm*W[2].h[i][j] for j in range(3)] for i in range(3)]
    curvature=sum((tangent[i]*H[i][j]*tangent[j] for i in range(3) for j in range(3)),iv(0))
    req(curvature.hi<0,'weighted constrained curvature is not negative')
    return X,K,lm,L,tangent,curvature
if __name__=='__main__':
    X,K,lm,L,tangent,curvature=certify()
    print('PASS unique KKT root by Krawczyk inclusion')
    print('box',*[fmt(x) for x in X],sep='\n  ')
    print('Krawczyk image',*[fmt(x) for x in K],sep='\n  ')
    print('lambdaM',fmt(lm));print('well interval',fmt(L))
    print('constraint tangent',*[fmt(x) for x in tangent],sep='\n  ')
    print('weighted tangent curvature',fmt(curvature))
