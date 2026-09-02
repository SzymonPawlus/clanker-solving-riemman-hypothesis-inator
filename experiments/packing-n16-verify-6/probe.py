import itertools, random, sys, os, json, copy, tempfile
from fractions import Fraction as F
sys.path.insert(0,'../packing-n16-fracverify'); sys.path.insert(0,'.')
import fracverify as A, v6check as B

# --- (1) can intersection-of-edge-halfplanes escape the vertex hull? --------
def hp(P):
    H=[]
    n=len(P)
    for i in range(n):
        (x1,y1),(x2,y2)=P[i],P[(i+1)%n]
        dx,dy=x2-x1,y2-y1
        if dx==0 and dy==0: continue
        H.append((-dy,dx,-dy*x1+dx*y1))
    return H
def inhull(p,Hh):
    return all(a*p[0]+b*p[1]>=c-F(0) for a,b,c in Hh)
random.seed(7)
bad=0; tried=0
for _ in range(200000):
    m=random.choice([4,5,6])
    P=[(F(random.randint(-4,4)),F(random.randint(-4,4))) for _ in range(m)]
    if len(set(P))<m: continue
    # area2
    A2=sum(P[i][0]*P[(i+1)%m][1]-P[(i+1)%m][0]*P[i][1] for i in range(m))
    if A2==0: continue
    if A2<0: P=P[::-1]
    tried+=1
    H=hp(P)
    # hull of vertices
    pts=sorted(set(P))
    def half(ps):
        out=[]
        for p in ps:
            while len(out)>=2:
                (ax,ay),(bx,by)=out[-2],out[-1]
                if (bx-ax)*(p[1]-by)-(by-ay)*(p[0]-bx)<=0: out.pop()
                else: break
            out.append(p)
        return out
    hl=half(pts)[:-1]+half(pts[::-1])[:-1]
    if len(hl)<3: continue
    Hh=hp(hl)
    # vertices of intersection-of-H: all pairwise line meets that satisfy H
    esc=None
    for (a1,b1,c1),(a2,b2,c2) in itertools.combinations(H,2):
        det=a1*b2-a2*b1
        if det==0: continue
        x=(c1*b2-c2*b1)/det; y=(a1*c2-a2*c1)/det
        if all(a*x+b*y>=c for a,b,c in H) and not inhull((x,y),Hh):
            esc=(x,y); break
    if esc:
        bad+=1
        if bad<=3: print("ESCAPE:",P,"point outside hull:",esc)
print(f"(1) non-convex probe: {tried} polygons, {bad} where halfplane-intersection escapes the vertex hull")

# --- (2) a genuine weight reallocation on n10 ------------------------------
CD='../packing-n16-fractional/certs/'
def run(blob,label):
    fd,p=tempfile.mkstemp(suffix='.json'); os.close(fd); json.dump(blob,open(p,'w'))
    try:
        try: ra='accept' if A.verify(p,verbose=False)[0] else 'reject'
        except Exception as e: ra='crash:'+type(e).__name__
        try: rb='accept' if B.check(p,verbose=False)[0] else 'reject'
        except Exception as e: rb='crash:'+type(e).__name__
    finally: os.unlink(p)
    print(f"| {label:<52} | reject | {ra:<14} | {rb:<14} |")
b10=json.load(open(CD+'cert_n10_N189.json'))
x=copy.deepcopy(b10); w=x['certificate']['weights']; ks=sorted(w)
w[ks[0]]-=30000; w[ks[1]]+=30000
run(x,"A19 30000/65536 of weight moved between 2 pieces")
x=copy.deepcopy(b10); w=x['certificate']['weights']; ks=sorted(w)
w[ks[3]]-=1
run(x,"A20 one weight reduced by 1/65536 (n10, tight cover)")
b4=json.load(open(CD+'cert_n4_N108.json'))
x=copy.deepcopy(b4); w=x['certificate']['weights']; ks=sorted(w)
w[ks[0]]-=1
run(x,"A21 one weight reduced by 1/65536 (n4)")

# --- (3) box sign bug, isolated -------------------------------------------
print()
print("(3) fracverify box decoder vs. the documented semantics {ulo<=u<=uhi, vlo<=v<=vhi, wlo<=u+v<=whi}")
for bd in ([0,4,0,4,0,4],[0,4,0,4,-3,4],[0,4,0,4,2,0],[0,4,0,4,3,6],[-2,2,-2,2,-1,1]):
    spec={"kind":"box","bounds":bd}
    got=A.piece_polygon(spec)
    # ground truth by brute force over a fine rational grid
    ulo,uhi,vlo,vhi,wlo,whi=bd
    truth=[(F(u,4),F(v,4)) for u in range(-12,20) for v in range(-12,20)
           if ulo<=F(u,4)<=uhi and vlo<=F(v,4)<=vhi and wlo<=F(u,4)+F(v,4)<=whi]
    # is every truth point inside the decoded polygon?
    if got:
        H=hp([(F(a),F(b)) for a,b in got])
        okin=all(all(a*p[0]+b*p[1]>=c for a,b,c in H) for p in truth)
        # and does the decoded polygon contain points that are NOT in truth?
        extra=[(F(u,4),F(v,4)) for u in range(-12,20) for v in range(-12,20)
               if all(a*F(u,4)+b*F(v,4)>=c for a,b,c in H)
               and not (ulo<=F(u,4)<=uhi and vlo<=F(v,4)<=vhi and wlo<=F(u,4)+F(v,4)<=whi)]
    else:
        okin = (len(truth)==0); extra=[]
    verdict = "OK" if (okin and not extra) else ("LOSES points" if not okin else "GAINS points")
    print(f"   bounds={bd!s:<22} decoded={'empty' if not got else str(len(got))+'-gon':<8} "
          f"truth_pts={len(truth):<4} -> {verdict}"
          + ("" if okin else "  (decoded region MISSES part of the box)")
          + (f"  (+{len(extra)} spurious)" if extra else ""))
