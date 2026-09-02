"""Per-piece Euclidean areas and boundary traces of the a=1+2sqrt3 certificate,
cross-checked against the half-plane cap f(l) (n16-covering-limit sec.3)."""
import sys, math, itertools
sys.path.insert(0, __file__.rsplit('/',1)[0])
from q3 import Q3, q3, R
from check_cov2 import FACES, a, shoelace2, sq

def eucl_area(P):
    return q3(0.0) if False else (shoelace2(P))   # 2*uv-area

print("a =", a, "=", float(a))
tot=0.0
rows=[]
for i,P in enumerate(FACES):
    A2 = shoelace2(P)                     # 2 * uv-area
    area = float(A2)*math.sqrt(3)/4.0     # Euclidean area
    tot += area
    # boundary traces: which sides of T_a the piece meets, and trace length
    traces={}
    for name, test in (("AB(v=0)", lambda u,v: v==q3(0)),
                       ("CA(u=0)", lambda u,v: u==q3(0)),
                       ("BC(u+v=a)", lambda u,v: (u+v)==a)):
        pts=[(u,v) for (u,v) in P if test(u,v)]
        if len(pts)>=2:
            m=q3(0)
            for X,Y in itertools.combinations(pts,2):
                d=sq(X[0]-Y[0],X[1]-Y[1])
                if d>m: m=d
            traces[name]=math.sqrt(float(m))
        elif len(pts)==1:
            traces[name]=0.0
    rows.append((i,area,traces,len(P)))

for i,area,traces,nv in rows:
    kind = "corner" if len([t for t in traces if traces[t]>0])>=2 else ("edge" if traces else "interior")
    tr = ", ".join(f"{k}:{v:.6f}" for k,v in traces.items())
    print(f"piece {i:2d}  nv={nv}  area={area:.7f}   {kind:8s}  traces[{tr}]")
print(f"total area = {tot:.7f}   area(T_a) = {float(a)**2*math.sqrt(3)/4:.7f}")

f1 = math.pi/3 - math.sqrt(3)/4
print()
print(f"f(1)  = pi/3 - sqrt3/4 = {f1:.7f}   (max area of a diam<=1 set in a half-plane")
print( "                                    containing two boundary points 1 apart)")
print(f"3sqrt3/8 = {3*math.sqrt(3)/8:.7f}     (regular hexagon of diameter 1)")
print(f"(pi-sqrt3)/2 = {(math.pi-math.sqrt(3))/2:.7f}  (Reuleaux triangle of width 1)")
print(f"pi/4 = {math.pi/4:.7f}, pi/6 = {math.pi/6:.7f}")
print()
viol=0
for i,area,traces,nv in rows:
    lmax = max(traces.values()) if traces else 0.0
    if lmax > 0.999999 and area > f1 + 1e-12:
        print(f"  !! piece {i} has trace {lmax:.6f} and area {area:.7f} > f(1)={f1:.7f}")
        viol+=1
print("pieces with trace ~1 exceeding f(1):", viol)
# slice upper bound for f(l)
def f_slice(l): return math.pi/2 - math.asin(l/2) - (l/2)*math.sqrt(1-l*l/4)
for l in (math.sqrt(3)-1, 1.0):
    print(f"  slice upper bound f({l:.6f}) <= {f_slice(l):.7f}")
