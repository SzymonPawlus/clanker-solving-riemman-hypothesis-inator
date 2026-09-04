#!/usr/bin/env python3
"""Independent exact red-team of c40527d and a sharper rational floor."""

from dataclasses import dataclass
from fractions import Fraction as Q
from itertools import combinations


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sgn(a, b):
    """Sign of a+b*sqrt(3), exactly."""
    if not b:
        return (a > 0) - (a < 0)
    if not a:
        return (b > 0) - (b < 0)
    if (a > 0) == (b > 0):
        return (a > 0) - (a < 0)
    cmp = (a*a > 3*b*b) - (a*a < 3*b*b)
    return cmp if a > 0 else -cmp


@dataclass(frozen=True)
class R3:
    a: Q = Q(0)
    b: Q = Q(0)
    def __add__(self, z):
        z = lift(z); return R3(self.a+z.a, self.b+z.b)
    __radd__ = __add__
    def __neg__(self): return R3(-self.a, -self.b)
    def __sub__(self, z): return self + (-lift(z))
    def __rsub__(self, z): return lift(z)-self
    def __mul__(self, z):
        z=lift(z); return R3(self.a*z.a+3*self.b*z.b,self.a*z.b+self.b*z.a)
    __rmul__=__mul__
    def __truediv__(self,z): return R3(self.a/Q(z),self.b/Q(z))
    def sign(self): return sgn(self.a,self.b)
    def __lt__(self,z): return (self-z).sign()<0
    def __eq__(self,z):
        try: z=lift(z)
        except Exception: return False
        return self.a==z.a and self.b==z.b
    def __str__(self): return f"{self.a} + ({self.b}) sqrt(3)"


def lift(z): return z if isinstance(z,R3) else R3(Q(z))


def cross(u,v): return u[0]*v[1]-u[1]*v[0]
def dot(u,v): return u[0]*v[0]+u[1]*v[1]
def unit(t): return ((1-t*t)/(1+t*t),2*t/(1+t*t))


TS=(Q(-4,5),Q(-1,72),Q(1,72),Q(4,5))
LS=(Q(163,480),Q(77,480),Q(77,480),Q(163,480))
CHORD=Q(11984563,25510200)
T_OLD=Q(1175341,5000000)
T_NEW=Q(5876707,25000000)  # 0.23506828
Y = R3(Q(-180,25753), Q(25915,103012))


def hull():
    vs=tuple(unit(t) for t in TS)+((Q(-1),Q(0)),)
    loads=LS+(CHORD,)
    require(sum(LS)==1,"open length")
    require(all(dot(v,v)==1 for v in vs),"unit edge")
    require(all(cross(vs[i],vs[(i+1)%5])>0 for i in range(5)),"local turns")
    # Winding guard: first four x coordinates are positive, y coordinates
    # increase strictly, and the fifth direction is pi.  Therefore their
    # unwrapped arguments are -beta,-alpha,alpha,beta,pi, followed by
    # 2pi-beta, giving winding exactly one rather than a star polygon.
    require(all(vs[i][0]>0 for i in range(4)),"direction half-plane")
    require(vs[0][1]<vs[1][1]<0<vs[2][1]<vs[3][1],"unwrapped order")
    require(sum(loads[i]*vs[i][0] for i in range(5))==0 and
            sum(loads[i]*vs[i][1] for i in range(5))==0,"closure")
    return vs,loads


def allocations(vs,loads):
    out={}
    for I in combinations(range(5),3):
        i,j,k=I
        ray=[cross(vs[j],vs[k]),cross(vs[k],vs[i]),cross(vs[i],vs[j])]
        if all(x<0 for x in ray): ray=[-x for x in ray]
        if not all(x>0 for x in ray): continue
        lam=min(loads[a]/x for a,x in zip(I,ray))
        x=[Q(0)]*5
        for a,z in zip(I,ray): x[a]=lam*z
        require(all(0<=z<=ell for z,ell in zip(x,loads)),"capacity")
        require(all(sum(x[i]*vs[i][j] for i in range(5))==0 for j in (0,1)),"balance")
        r=[ell-z for ell,z in zip(loads,x)]
        require(all(sum(r[i]*vs[i][j] for i in range(5))==0 for j in (0,1)),"residual")
        out[I]=tuple(x)
    require(tuple(out)==((0,2,4),(0,3,4),(1,2,4),(1,3,4)),"allocation list")
    return out


TRI=((R3(),R3()),(R3(Q(1,2)),R3()),(R3(Q(1,4)),R3(0,Q(1,4))))
EDGES=((R3(1),R3()),(R3(Q(-1,2)),R3(0,Q(1,2))),
       (R3(Q(-1,2)),R3(0,Q(-1,2))))


def rot(p,c,s): return (c*p[0]-s*p[1],s*p[0]+c*p[1])


def tri_value(x,vs,c,s):
    ns=tuple((R3(v[1]),R3(-v[0])) for v in vs)
    total=R3()
    for amount,n in zip(x,ns):
        if not amount: continue
        vals=[dot(rot(p,c,s),n) for p in TRI]
        h=vals[0]
        for z in vals[1:]:
            if h<z: h=z
        total += amount*h
    return total/2


def tri_floor(x,vs):
    vals=[]
    for amount,v in zip(x,vs):
        if not amount: continue
        n=(Q(v[1]),Q(-v[0]))
        for d in EDGES:
            for eps in (-1,1):
                target=(R3(-eps*n[1]),R3(eps*n[0]))
                c=dot(d,target); s=cross(d,target)
                require(c*c+s*s==1,"switch rotation")
                vals.append(tri_value(x,vs,c,s))
    floor=vals[0]
    for z in vals[1:]:
        if z<floor: floor=z
    # Fixed supports between exhaustive switches give a nonnegative sinusoid;
    # f''=-f<=0, so this boundary minimum covers every direct orientation.
    return floor


def coeff(residual,vs,u):
    """Regenerate P sin(phi)+K cos(phi) from signs at rational half-angle u."""
    sn,cs=2*u/(1+u*u),(1-u*u)/(1+u*u)
    p=k=Q(0)
    for r,v in zip(residual,vs):
        raw=v[0]*sn-v[1]*cs
        if not r: continue
        require(raw!=0,"sample at projection crossing")
        e=1 if raw>0 else -1
        p += r*e*v[0]/4
        k += r*e*(-v[1])/4
    return p,k


def value(q,p,k,u):
    return q+p*(2*u/(1+u*u))+k*((1-u*u)/(1+u*u))


def qscale_interval(q, lo, hi):
    return (q*lo,q*hi) if q>=0 else (q*hi,q*lo)


def algebraic_bottleneck(vs,loads,xs,q,got):
    """Isolate and prove the exact global envelope minimum at A=C."""
    rlo=Q(1732050807568877293527446341505,10**30)
    rhi=Q(1732050807568877293527446341506,10**30)
    require(rlo*rlo<3<rhi*rhi,"sqrt3 bracket")
    ylo=Y.a+Y.b*rlo; yhi=Y.a+Y.b*rhi
    require(Q(144,5185)<ylo<yhi<Q(3,5),"bottleneck angular range")
    clo=Q(903424551805033647756928048264,10**30)
    chi=Q(903424551805033647756928048265,10**30)
    require(clo*clo < 1-yhi*yhi and chi*chi > 1-ylo*ylo,
            "cosine bracket")

    def at_star(name,x):
        tri=q[x] if x is not None else R3()
        tri_lo=tri.a+tri.b*(rlo if tri.b>=0 else rhi)
        tri_hi=tri.a+tri.b*(rhi if tri.b>=0 else rlo)
        alloc=(Q(0),)*5 if x is None else xs[x]
        sl=sh=Q(0)
        for ell,z,v in zip(loads,alloc,vs):
            ry=qscale_interval(v[0],ylo,yhi)
            rc=qscale_interval(-v[1],clo,chi)
            lo,hi=ry[0]+rc[0],ry[1]+rc[1]
            require(not (lo<=0<=hi),f"unresolved bottleneck sign {name}")
            al,ah=(lo,hi) if lo>0 else (-hi,-lo)
            sl+=(ell-z)*al/4; sh+=(ell-z)*ah/4
        return tri_lo+sl,tri_hi+sh

    intervals={
      'S':at_star('S',None),'A':at_star('A',(0,2,4)),
      'B':at_star('B',(0,3,4)),'C':at_star('C',(1,2,4)),
      'D':at_star('D',(1,3,4))}
    # The exact A-C difference has no cosine term and vanishes at Y.
    qa,qc=q[(0,2,4)],q[(1,2,4)]
    pa,pc=got['A'][0],got['C'][0]
    require(qa-qc+(pa-pc)*Y==R3(),"A/C crossing identity")
    Llo,Lhi=intervals['C']
    require(intervals['A'][0]<=Lhi and intervals['A'][1]>=Llo,
            "A/C interval disagreement")
    require(all(intervals[n][1]<Llo for n in ('S','B','D')),
            "another bound exceeds bottleneck")

    # Exact global lower bound at L*: concavity on these four intervals and
    # endpoint comparisons.  Values at the rational endpoints are exact
    # Q(sqrt3); compare their rigorous rational lower enclosures with Lhi.
    qs={'C':qc,'A':qa,'S':R3(),'B':q[(0,3,4)]}
    rational_endpoints={'C':Q(0),'A':Q(1,3),'S0':Q(1,3),
                        'S1':Q(3,4),'B0':Q(3,4),'B1':Q(1)}
    for tag,u in rational_endpoints.items():
        name=tag[0]
        p,k=got[name]
        z=value(qs[name],p,k,u)
        lower=z.a+z.b*(rlo if z.b>=0 else rhi)
        require(lower>Lhi,f"endpoint does not exceed algebraic bottleneck: {tag}")
    # At phi*, all five values are <= L*, with A=C=L*.  Conversely the
    # four concave pieces C,A,S,B have both endpoints >=L*, proving their
    # maximum is >=L* everywhere. Thus L* is the exact envelope minimum.
    require(Llo>T_NEW,"isolated bottleneck does not beat rational theorem")
    return intervals,(Llo,Lhi)


def analytic():
    vs,loads=hull(); xs=allocations(vs,loads)
    q={I:tri_floor(x,vs) for I,x in xs.items()}
    expected={
      (0,2,4):R3(Q(231,414800),Q(399091,19910400)),
      (0,3,4):R3(Q(163,1968)),
      (1,2,4):R3(0,Q(399091,9955200)),
      (1,3,4):R3(Q(231,414800),Q(399091,19910400))}
    require(q==expected,"triangle floors")

    zero=tuple(Q(0) for _ in loads)
    named={'S':zero,'A':xs[(0,2,4)],'B':xs[(0,3,4)],'C':xs[(1,2,4)]}
    # Samples lie strictly inside the claimed validity ranges and determine
    # absolute-value signs; crossings removed by zero residuals cause no gap.
    samples={'C':Q(1,10),'A':Q(1,3),'S':Q(1,3),'B':Q(4,5)}
    got={}
    for name,x in named.items():
        r=tuple(ell-z for ell,z in zip(loads,x))
        got[name]=coeff(r,vs,samples[name])
    expected_coeff={
      'C':(Q(489,13120),Q(163,984)),
      'A':(Q(29833549,255102000),Q(163,984)),
      'S':(Q(40331857,204081600),Q(163,984)),
      'B':(Q(399091,2488800),Q(0))}
    require(got==expected_coeff,"sinusoidal coefficients")

    qs={'C':q[(1,2,4)],'A':q[(0,2,4)],'S':R3(),'B':q[(0,3,4)]}
    cuts=(Q(0),Q(157,697),Q(1,3),Q(3,4),Q(1))
    names=('C','A','S','B')
    old_margins=[]
    for name,lo,hi in zip(names,cuts,cuts[1:]):
        p,k=got[name]
        for u in (lo,hi):
            margin=value(qs[name],p,k,u)-T_OLD
            require(margin.sign()>0,f"old endpoint {name},{u}")
            old_margins.append((name,u,margin))
    # All coefficients are nonnegative, so each sinusoid is nonnegative and
    # concave on its stated subinterval of [0,pi/2]. Endpoint checks suffice.

    mirror=(3,2,1,0,4)
    require(all(loads[i]==loads[mirror[i]] for i in range(5)),"mirror loads")
    require(all(vs[mirror[i]]==(vs[i][0],-vs[i][1]) for i in range(5)),"mirror directions")
    aset=set(xs.values())
    require({tuple(x[mirror[i]] for i in range(5)) for x in aset}==aset,"mirror allocations")

    # Stronger rational theorem: a much closer rational cut to the exact C/A
    # crossing retains positive endpoint margins at 0.23506828.
    sharp=Q(17183,76284)
    sharp_cuts=(Q(0),sharp,Q(1,3),Q(3,4),Q(1))
    sharp_margins=[]
    for name,lo,hi in zip(names,sharp_cuts,sharp_cuts[1:]):
        p,k=got[name]
        for u in (lo,hi):
            margin=value(qs[name],p,k,u)-T_NEW
            require(margin.sign()>0,f"sharp endpoint {name},{u}: {margin}")
            sharp_margins.append((name,u,margin))
    bottleneck=algebraic_bottleneck(vs,loads,xs,q,got)
    return q,got,old_margins,sharp_margins,bottleneck


if __name__=='__main__':
    q,got,old,sharp,bottleneck=analytic()
    print('triangle floors')
    for x in q.items(): print(x)
    print('regenerated coefficients',got)
    print('old endpoint margins')
    for x in old: print(x)
    print('sharper endpoint margins')
    for x in sharp: print(x)
    print('bottleneck intervals',bottleneck)
    print('PASS: full direct-motion envelope >= 5876707/25000000')
