"""Check my hand-transcription of the README polygon table against the author's code."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, "/home/user/clanker-solving-riemman-hypothesis-inator/experiments/packing-n16-covering-2")
from check_cov2 import FACES as MINE
import importlib.util
spec = importlib.util.spec_from_file_location("ex", "/home/user/clanker-solving-riemman-hypothesis-inator/experiments/packing-n16-covering-2/exact_1p2r3.py")
ex = importlib.util.module_from_spec(spec)
sys.modules["ex"]=ex
spec.loader.exec_module.__self__ if False else None
try:
    spec.loader.exec_module(ex)
except SystemExit:
    pass
theirs = [[ex.P[k] for k in f] for f in ex.FACES]
def norm(poly):
    # canonical: set of (p,q) pairs for u and v as floats rounded
    return sorted((round(float(u),12), round(float(v),12)) for u,v in poly)
ok=True
for i,(a,b) in enumerate(zip(MINE, theirs)):
    if norm(a)!=norm(b):
        ok=False; print("MISMATCH face",i); print("  mine ", norm(a)); print("  theirs", norm(b))
print("faces compared:", len(MINE), len(theirs))
print("hand-transcription matches the author's code:", ok and len(MINE)==len(theirs))
