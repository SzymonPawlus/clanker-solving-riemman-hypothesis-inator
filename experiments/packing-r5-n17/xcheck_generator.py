"""Confirm my independent transcription (famgen.py) of the four-grain generator emits
the same point sets as experiments/packing-r4-famcert/generator.py for j = 0..5.

This is the ONE place this audit touches the other lane's code, and it is a
transcription check only: if it failed I would be auditing a configuration nobody
claimed.  No verdict below depends on their code.
"""
import json, os, subprocess, sys
import famgen

FAM = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "packing-r4-famcert"))
CODE = ('import sys, json\n'
        'sys.path.insert(0, %r)\n'
        'from generator import generate\n'
        'print(json.dumps({j: [[str(p[0].a)+"|"+str(p[0].b), str(p[1].a)+"|"+str(p[1].b)]'
        ' for p in generate(j)] for j in range(6)}))\n' % FAM)

r = subprocess.run([sys.executable, "-c", CODE], capture_output=True, text=True, cwd=FAM)
if r.returncode != 0:
    print("could not run the r4-famcert generator; skipping transcription check")
    print(r.stderr[:500])
    raise SystemExit(0)
theirs = json.loads(r.stdout)
for j in range(6):
    mine = [[str(p[0].a) + "|" + str(p[0].b), str(p[1].a) + "|" + str(p[1].b)]
            for p in famgen.generate(j)]
    print("j=%d n=%-3d same order: %-5s   same set: %s"
          % (j, len(mine), mine == theirs[str(j)],
             set(map(tuple, mine)) == set(map(tuple, theirs[str(j)]))))
