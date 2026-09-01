#!/usr/bin/env python3
"""Strict interval convex-cycle and shoelace checker for one pose box."""

import json
import sys
from fractions import Fraction as Q
from pathlib import Path


class Reject(ValueError): pass


class I:
    def __init__(self, lo, hi=None):
        self.lo, self.hi = Q(lo), Q(lo if hi is None else hi)
        if self.lo > self.hi: raise Reject("reversed interval")
    def __add__(self, o): o=iv(o); return I(self.lo+o.lo,self.hi+o.hi)
    __radd__=__add__
    def __neg__(self): return I(-self.hi,-self.lo)
    def __sub__(self,o): return self+-iv(o)
    def __mul__(self,o):
        o=iv(o); v=(self.lo*o.lo,self.lo*o.hi,self.hi*o.lo,self.hi*o.hi)
        return I(min(v),max(v))
    __rmul__=__mul__
    def __truediv__(self,o):
        o=iv(o)
        if o.lo<=0<=o.hi: raise Reject("division interval contains zero")
        return self*I(1/o.hi,1/o.lo)


def iv(x): return x if isinstance(x,I) else I(x)
def strict_object(pairs):
    out={}
    for k,v in pairs:
        if k in out: raise Reject(f"duplicate JSON field: {k}")
        out[k]=v
    return out
def rat(x,label,decimal=False):
    if not isinstance(x,str): raise Reject(f"{label} must be a string")
    try: q=Q(x)
    except (ValueError,ZeroDivisionError) as e: raise Reject(f"bad rational {label}") from e
    if not decimal and str(q)!=x: raise Reject(f"noncanonical rational {label}")
    return q
def cross(a,b): return a[0]*b[1]-a[1]*b[0]
def sub(a,b): return a[0]-b[0],a[1]-b[1]


def rotation(t,eps):
    den=I(1)+t*t
    return eps*(I(1)-t*t)/den, eps*2*t/den


def transform(local,pose,eps):
    tx,ty,t=pose; c,s=rotation(t,eps); x,y=local
    return tx+c*x-s*y,ty+s*x+c*y


def check(path):
    d=json.loads(Path(path).read_text(),object_pairs_hook=strict_object)
    fields={"schema_version","claim_scope","target_rational","box_radius",
            "half_angle_epsilon","pose_centers","selected_cycle"}
    if not isinstance(d,dict) or set(d)!=fields: raise Reject("unknown or missing field")
    if d["schema_version"]!="moser-five-cycle-box-v1": raise Reject("schema")
    if d["claim_scope"]!="single_pose_box_area_prune_only": raise Reject("scope escalation")
    target=rat(d["target_rational"],"target")
    radius=rat(d["box_radius"],"radius")
    eps=rat(d["half_angle_epsilon"],"epsilon")
    if eps!=-1 or radius<=0: raise Reject("wrong chart or radius")
    centers=d["pose_centers"]
    if not isinstance(centers,dict) or set(centers)!={"triangle","square","rational_arc_v2"}:
        raise Reject("incomplete nine-variable pose")
    poses={}
    for name,raw in centers.items():
        if not isinstance(raw,list) or len(raw)!=3: raise Reject("pose must have tx,ty,t")
        poses[name]=tuple(I(rat(v,f"{name} center",True)-radius,
                             rat(v,f"{name} center",True)+radius) for v in raw)

    square=[(Q(0),Q(0)),(Q(1,3),Q(0)),(Q(1,3),Q(1,3)),(Q(0),Q(1,3))]
    arc=[(Q(0),Q(0)),(Q(1,3),Q(0)),(Q(338,807),Q(260,807)),
         (Q(9361,72361),Q(105820,217083))]
    points={"segment.P0":(I(0),I(0)),"segment.P1":(I(1),I(0))}
    for i,p in enumerate(square): points[f"square.P{i}"]=transform(p,poses["square"],eps)
    for i,p in enumerate(arc): points[f"rational_arc_v2.P{i}"]=transform(p,poses["rational_arc_v2"],eps)
    expected=["segment.P0","square.P2","segment.P1","square.P0","rational_arc_v2.P2"]
    if d["selected_cycle"]!=expected: raise Reject("untrusted cycle label")
    cycle=[points[k] for k in expected]; n=len(cycle)

    # Strong convex-order guard: every non-edge cycle vertex is strictly left
    # of every directed edge. This implies simplicity and CCW convex order.
    for i in range(n):
        edge=sub(cycle[(i+1)%n],cycle[i])
        for j in range(n):
            if j in (i,(i+1)%n): continue
            turn=cross(edge,sub(cycle[j],cycle[i]))
            if turn.lo<=0: raise Reject(f"convex-order guard uncertain at edge {i}, point {j}")

    twice=I(0)
    for i in range(n): twice+=cross(cycle[i],cycle[(i+1)%n])
    if twice.lo<=0: raise Reject("shoelace sign uncertain")
    if twice.lo/2<target: raise Reject("area lower endpoint does not clear target")
    return twice.lo/2


def main():
    try: lower=check(sys.argv[1])
    except (IndexError,OSError,json.JSONDecodeError,Reject) as e:
        print(f"REJECT: {e}",file=sys.stderr); return 1
    print(f"PASS strict five-cycle leaf; area_lower={lower}"); return 0
if __name__=="__main__": raise SystemExit(main())
