import math, sys, time, random
from pysat.solvers import Cadical195
S3=math.sqrt(3)
A=(0,0); B=(3,0); C=(1.5,1.5*S3); CORN=[A,B,C]
def d(p,q): return math.hypot(p[0]-q[0],p[1]-q[1])
def inT(p):
    x,y=p
    return y>=-1e-12 and y<=S3*x+1e-12 and y<=S3*(3-x)+1e-12
def inU(p,eps):
    return inT(p) and all(d(p,V)>=1+eps for V in CORN)

def boundary_U(nseg, narc, eps):
    """points just inside U along its boundary: 3 straight segments + 3 arcs"""
    pts=[]
    # straight parts: on each side, between the two points at distance 1 from the ends
    sides=[(A,B),(B,C),(C,A)]
    for (P,Qq) in sides:
        ux=((Qq[0]-P[0])/3,(Qq[1]-P[1])/3)
        for t in range(nseg+1):
            s=1+t/nseg          # arclength from P in [1,2]
            q=(P[0]+ux[0]*s, P[1]+ux[1]*s)
            # nudge inward (towards centroid) a touch so it is strictly in U
            pts.append(q)
    # arcs: circle of radius 1+eps about each corner, inside T
    for V in CORN:
        others=[W for W in CORN if W!=V]
        a1=math.atan2(others[0][1]-V[1], others[0][0]-V[0])
        a2=math.atan2(others[1][1]-V[1], others[1][0]-V[0])
        # take the short way round (60 degrees)
        da=(a2-a1+math.pi)%(2*math.pi)-math.pi
        for t in range(narc+1):
            th=a1+da*t/narc
            pts.append((V[0]+(1+eps)*math.cos(th), V[1]+(1+eps)*math.sin(th)))
    return [p for p in pts if inT(p)]

def interior(N, eps):
    pts=[]
    for j in range(N+1):
        for i in range(N+1-j):
            x=3*(2*i+j)/(2*N); y=3*S3*j/(2*N)
            pts.append((x,y))
    return pts

def colour(pts,k,verbose=True):
    n=len(pts)
    E=[(i,j) for i in range(n) for j in range(i+1,n) if d(pts[i],pts[j])>1]
    s=Cadical195(); var=lambda p,c: p*k+c+1
    for p in range(n): s.add_clause([var(p,c) for c in range(k)])
    for i,j in E:
        for c in range(k): s.add_clause([-var(i,c),-var(j,c)])
    t0=time.time(); r=s.solve(); dt=time.time()-t0
    mod=None
    if r:
        m=set(x for x in s.get_model() if x>0)
        mod=[next(c for c in range(k) if var(p,c) in m) for p in range(n)]
    s.delete()
    if verbose: print(f"  |P|={n} edges={len(E)} k={k} -> {'SAT' if r else 'UNSAT'} ({dt:.2f}s)",flush=True)
    return r, mod

if __name__=="__main__":
    eps=float(sys.argv[1]) if len(sys.argv)>1 else 0.01
    for (ns,na,N) in [(2,2,4),(4,4,6),(6,6,8),(10,10,10),(16,16,14),(24,24,18),(32,32,24)]:
        pts=list({(round(p[0],9),round(p[1],9)) for p in
                  CORN + boundary_U(ns,na,eps) + [p for p in interior(N,eps) if inT(p)]})
        print(f"ns={ns} na={na} N={N}:")
        r,_=colour(pts,8)
        if not r:
            print("*** UNSAT (floats) ***"); break
