"""Independent unbounded conditional census from literal residual recursion.

No author census or period-maximum reduction is read or imported. The only
import is root's previously independent generic integer row arithmetic.
"""
import argparse
from functools import lru_cache
from hashlib import sha256
import importlib.util
import json
from math import gcd, lcm
from pathlib import Path
import time


def run(common, expected_path):
    node_count = physical_edges = 0
    largest_period = 0

    @lru_cache(None)
    def completions(r,L,R):
        nonlocal node_count, physical_edges, largest_period
        node_count += 1
        largest_period = max(largest_period,L)
        assert R
        if r == 0:
            return frozenset()
        families = set()
        for n in common.admissible_growth(r):
            T=L*n
            lifted=common.lift(R,L,T)
            for h in common.divisors(T):
                if h<2 or h//gcd(h,L)!=n:
                    continue
                for a,B in common.rows(h):
                    killed=lifted & common.lift(B,h,T)
                    if r*killed.bit_count()<lifted.bit_count():
                        continue
                    physical_edges += 1
                    rest=lifted^killed
                    if not rest:
                        families.add(frozenset(((h,a),)))
                    else:
                        D,compressed=common.normalize(T,rest)
                        for suffix in completions(r-1,D,compressed):
                            assert (h,a) not in suffix
                            families.add(suffix | {(h,a)})
        return frozenset(families)

    tails = completions(5,6,34)
    patterns={}
    for suffix in tails:
        assert len(suffix)==5, 'a cover with fewer than seven total rows was found'
        for three_a in (1,2):
            physical=suffix | {(2,1),(3,three_a)}
            assert len(physical)==7
            M=lcm(*(h for h,a in physical))
            speeds=tuple(sorted(M*a//h for h,a in physical))
            assert len(set(speeds))==7 and all(0<w<M for w in speeds)
            core=speeds+(M,)
            assert gcd(*core)==1
            masks={w:sum(1<<j for j in range(M)
                         if min(w*(15*j+1)%(15*M),15*M-w*(15*j+1)%(15*M))<M)
                   for w in speeds}
            union=0
            for B in masks.values(): union |= B
            assert union==(1<<M)-1
            private={}
            for w,B in masks.items():
                other=0
                for v,C in masks.items():
                    if v!=w: other |= C
                witness=B & ~other
                assert witness, ('nonminimal returned core',core,w)
                private[w]=(witness & -witness).bit_length()-1
            patterns[core]=dict(speeds=list(core),private_endpoint=private,
                                reduced_rows=[list(row) for row in sorted(physical)])
    expected=json.loads(expected_path.read_text())
    expected_set={tuple(case['speeds']) for case in expected['cores']}
    assert len(expected_set)==len(expected['cores'])
    assert set(patterns)==expected_set, ('census mismatch',set(patterns)-expected_set,expected_set-set(patterns))
    bymaximum={}
    for core in patterns:
        bymaximum[str(core[-1])]=bymaximum.get(str(core[-1]),0)+1
    return dict(status='PASS; independent same-family census, sketch pending cross-family review',
                root=dict(remaining=5,period=6,residual=[1,5],fixed_rows=[[2,1],[3,'1 or 2']]),
                states=node_count,qualifying_physical_edges=physical_edges,
                largest_residual_period=largest_period,distinct_suffix_row_sets=len(tails),
                primitive_core_count=len(patterns),counts_by_maximum=bymaximum,
                expected_inventory_sha256=sha256(expected_path.read_bytes()).hexdigest(),
                cores=[patterns[c] for c in sorted(patterns)])


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--common-checker',type=Path,required=True)
    p.add_argument('--expected-inventory',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args()
    spec=importlib.util.spec_from_file_location('independent_common',a.common_checker)
    common=importlib.util.module_from_spec(spec);spec.loader.exec_module(common)
    started=time.monotonic()
    report=run(common,a.expected_inventory)
    report['elapsed_seconds']=time.monotonic()-started
    report['checker_sha256']=sha256(Path(__file__).read_bytes()).hexdigest()
    report['common_checker_sha256']=sha256(a.common_checker.read_bytes()).hexdigest()
    a.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='cores'}),flush=True)


if __name__=='__main__': main()
