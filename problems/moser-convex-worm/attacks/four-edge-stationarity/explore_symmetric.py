#!/usr/bin/env python3
"""Numerical first-variation probe for symmetric four-edge support worms.

All output is numerical and non-assumable.  It searches parameters
(tan(alpha/2), tan(beta/2), outer-edge length p), with inner length 1/2-p.
"""

import math
from itertools import combinations


def cross(a,b): return a[0]*b[1]-a[1]*b[0]
def dot(a,b): return a[0]*b[0]+a[1]*b[1]
def unit(t): return ((1-t*t)/(1+t*t),2*t/(1+t*t))


TRI=((0.,0.),(.5,0.),(.25,math.sqrt(3)/4))
EDGES=((1.,0.),(-.5,math.sqrt(3)/2),(-.5,-math.sqrt(3)/2))


def data(x):
    ta,tb,p=x; q=.5-p
    ca,sa=unit(ta); cb,sb=unit(tb)
    tang=((cb,-sb),(ca,-sa),(ca,sa),(cb,sb),(-1.,0.))
    loads=(p,q,q,p,2*p*cb+2*q*ca)
    if not (0<ta<tb<1 and 0<p<.5 and loads[-1]>0): return None
    return tang,loads


def allocs(tang,loads):
    out=[]
    for I in combinations(range(5),3):
        i,j,k=I
        ray=[cross(tang[j],tang[k]),cross(tang[k],tang[i]),cross(tang[i],tang[j])]
        if all(z<0 for z in ray): ray=[-z for z in ray]
        if not all(z>1e-14 for z in ray): continue
        lam=min(loads[a]/z for a,z in zip(I,ray))
        xx=[0.]*5
        for a,z in zip(I,ray): xx[a]=lam*z
        out.append((I,tuple(xx)))
    return out


def rotate(v,c,s): return (c*v[0]-s*v[1],s*v[0]+c*v[1])


def tri_floor(x,tang):
    normals=tuple((v[1],-v[0]) for v in tang)
    vals=[]
    for amount,n in zip(x,normals):
        if amount<1e-15: continue
        for d in EDGES:
            for eps in (-1,1):
                target=(-eps*n[1],eps*n[0])
                c=dot(d,target); s=cross(d,target)
                total=0.
                for z,m in zip(x,normals):
                    if z:
                        total += z*max(dot(rotate(v,c,s),m) for v in TRI)/2
                vals.append(total)
    return min(vals)


def bounds(x):
    z=data(x)
    if z is None:return None
    tang,loads=z
    ans=[((0.,)*5,0.,('S',))]
    for I,a in allocs(tang,loads): ans.append((a,tri_floor(a,tang),I))
    return tang,loads,ans


def at(phi,package):
    tang,loads,bs=package
    sn,cs=math.sin(phi),math.cos(phi)
    vals=[]
    for a,q,I in bs:
        seg=sum((ell-z)*abs(v[0]*sn-v[1]*cs)/4
                for ell,z,v in zip(loads,a,tang))
        vals.append((q+seg,I))
    return max(vals,key=lambda z:z[0])


def all_at(phi,package):
    tang,loads,bs=package
    sn,cs=math.sin(phi),math.cos(phi)
    return sorted([(q+sum((ell-z)*abs(v[0]*sn-v[1]*cs)/4
                          for ell,z,v in zip(loads,a,tang)),I)
                   for a,q,I in bs],key=lambda z:z[0],reverse=True)


def floor(x,detail=False):
    package=bounds(x)
    if package is None:return -1.
    N=3000
    ys=[at(math.pi*k/N,package)[0] for k in range(N+1)]
    candidates=sorted(range(1,N),key=lambda k:ys[k])[:8]
    best=(min(ys[0],ys[-1]),0.)
    for k in candidates:
        lo,hi=math.pi*(k-1)/N,math.pi*(k+1)/N
        # Golden-section minimization of the nonsmooth maximum works once the
        # grid has isolated a single local basin; dense-grid endpoints remain.
        gr=(math.sqrt(5)-1)/2
        a,b=lo,hi;c=b-gr*(b-a);d=a+gr*(b-a)
        fc,fd=at(c,package)[0],at(d,package)[0]
        for _ in range(90):
            if fc<fd:b,d,fd=d,c,fc;c=b-gr*(b-a);fc=at(c,package)[0]
            else:a,c,fc=c,d,fd;d=a+gr*(b-a);fd=at(d,package)[0]
        phi=(a+b)/2; val=at(phi,package)[0]
        if val<best[0]:best=(val,phi)
    if detail:
        vals=all_at(best[1],package)
        return best,vals,package
    return best[0]


def pattern(start):
    x=list(start); fx=floor(x); steps=[.01,.01,.01]
    print('start',x,fx,floor(x,True)[0])
    for iteration in range(120):
        improved=False
        for i in range(3):
            for sign in (-1,1):
                y=x[:];y[i]+=sign*steps[i];fy=floor(y)
                if fy>fx:
                    x,fx=y,fy;improved=True
                    print(iteration,x,fx)
        if not improved:
            steps=[z/2 for z in steps]
        if max(steps)<2e-9:break
    print('best',x,fx,'steps',steps)
    print('detail',floor(x,True)[:2])
    for i in range(3):
        h=1e-6
        y=x[:];y[i]+=h; z=x[:];z[i]-=h
        print('slope',i,(floor(y)-floor(z))/(2*h))


def local_crossing(x, pair, bracket):
    package=bounds(x)
    if package is None:return None
    tang,loads,bs=package
    table={I:(a,q) for a,q,I in bs}
    def one(phi,I):
        a,q=table[I];sn,cs=math.sin(phi),math.cos(phi)
        return q+sum((ell-z)*abs(v[0]*sn-v[1]*cs)/4
                     for ell,z,v in zip(loads,a,tang))
    lo,hi=bracket
    def d(phi):return one(phi,pair[0])-one(phi,pair[1])
    if d(lo)*d(hi)>0:return None
    for _ in range(90):
        mid=(lo+hi)/2
        if d(lo)*d(mid)<=0:hi=mid
        else:lo=mid
    phi=(lo+hi)/2
    return one(phi,pair[0]),phi


def wells(x):
    ta,tb,_=x
    alpha,beta=2*math.atan(ta),2*math.atan(tb)
    outer=local_crossing(x,((0,2,4),(1,2,4)),(alpha,beta))
    center=local_crossing(x,(('S',),(0,3,4)),(alpha,math.pi/2))
    if outer is None or center is None:return (-1.,None,None)
    endpoint=(at(0.,bounds(x))[0],0.)
    return min(endpoint[0],outer[0],center[0]),endpoint,outer,center


def nelder(start):
    n=3
    simplex=[list(start)]
    for i,h in enumerate((.001,.003,.002)):
        y=list(start);y[i]+=h;simplex.append(y)
    score=lambda x:wells(x)[0]
    for it in range(250):
        simplex.sort(key=score,reverse=True)
        vals=[score(x) for x in simplex]
        centroid=[sum(simplex[j][i] for j in range(n))/n for i in range(n)]
        worst=simplex[-1]
        refl=[centroid[i]+(centroid[i]-worst[i]) for i in range(n)]
        fr=score(refl)
        if vals[0]>=fr>vals[-2]:simplex[-1]=refl
        elif fr>vals[0]:
            exp=[centroid[i]+2*(refl[i]-centroid[i]) for i in range(n)]
            simplex[-1]=exp if score(exp)>fr else refl
        else:
            con=[centroid[i]+.5*(worst[i]-centroid[i]) for i in range(n)]
            if score(con)>vals[-1]:simplex[-1]=con
            else:
                best=simplex[0]
                simplex=[best]+[[best[i]+.5*(x[i]-best[i]) for i in range(n)]
                                for x in simplex[1:]]
        spread=max(abs(score(x)-score(simplex[0])) for x in simplex)
        if it%20==0:print('NM',it,simplex[0],score(simplex[0]),wells(simplex[0]))
        if spread<1e-14 and max(max(abs(x[i]-simplex[0][i]) for i in range(n))
                               for x in simplex)<1e-9:break
    simplex.sort(key=score,reverse=True)
    print('NM BEST',simplex[0],score(simplex[0]),wells(simplex[0]))
    first_variation(simplex[0])


def first_variation(x):
    """Numerical KKT/equioscillation diagnostic for the three active wells."""
    grads=[]
    for well_index in range(3):
        g=[]
        for i in range(3):
            h=2e-6
            xp=list(x);xm=list(x);xp[i]+=h;xm[i]-=h
            # wells tuple is (minimum, endpoint, outer, center)
            g.append((wells(xp)[well_index+1][0]-wells(xm)[well_index+1][0])/(2*h))
        grads.append(g)
    # Solve lambda0(g0-g2)+lambda1(g1-g2)=-g2 in coordinates 0,1,
    # put lambda2=1-lambda0-lambda1, then report the unused residual.
    a,b=grads[0][0]-grads[2][0],grads[1][0]-grads[2][0]
    c,d=grads[0][1]-grads[2][1],grads[1][1]-grads[2][1]
    e,f=-grads[2][0],-grads[2][1]
    den=a*d-b*c
    l0=(e*d-b*f)/den;l1=(a*f-e*c)/den;l2=1-l0-l1
    residual=[sum(l*g[i] for l,g in zip((l0,l1,l2),grads)) for i in range(3)]
    det=(grads[0][0]*(grads[1][1]*grads[2][2]-grads[1][2]*grads[2][1])
         -grads[0][1]*(grads[1][0]*grads[2][2]-grads[1][2]*grads[2][0])
         +grads[0][2]*(grads[1][0]*grads[2][1]-grads[1][1]*grads[2][0]))
    print('well gradients endpoint/outer/center',grads)
    print('KKT lambda',l0,l1,l2,'residual',residual,'gradient determinant',det)


if __name__=='__main__':
    pattern((1/72,4/5,163/480))
    nelder((.01514276,.79998,.34149816))
