"""Post-processing: rigorous certification of the sieve's output.

1. Coverage check: the per-segment checkpoints must tile [5041, N) exactly.
2. Every flagged candidate n is re-decided with certified interval
   arithmetic, using sigma(n) recomputed INDEPENDENTLY of the sieve by
   factorization (and cross-checked against the sieve's value).
3. Near-miss catalogue: for the top segment argmaxes of sigma(n)/n, output
   certified enclosures of the Robin ratio sigma(n)/(e^gamma n log log n).

Exit codes: 0 = all candidates certified 'holds'; 3 = an 'undecided'
(kill K3); 4 = a certified violation for n > 5040 — per RULES.md section 7
this is overwhelmingly a bug and triggers the extraordinary-claim protocol,
NOT an announcement.
"""
import csv
import sys
from robin_core import sigma_exact, factorize, robin_decide, ratio_enclosure

TOP_K = 40

def main(ckpt="checkpoints"):
    # --- 1. coverage ---
    segs = []
    with open(f"{ckpt}/segments.csv") as f:
        for row in csv.reader(f):
            L, R, bn, bs, chk, nfl = map(int, row)
            segs.append((L, R, bn, bs, nfl))
    segs.sort()
    assert segs[0][0] == 5041, "coverage must start at 5041"
    for (L1, R1, *_), (L2, *_ ) in zip(segs, segs[1:]):
        assert R1 == L2, f"coverage gap: [{L1},{R1}) then {L2}"
    N = segs[-1][1]
    print(f"coverage: contiguous [5041, {N}) in {len(segs)} segments")

    # --- 2. certify all flagged candidates ---
    cands = []
    with open(f"{ckpt}/candidates.txt") as f:
        for line in f:
            n, s = map(int, line.split())
            cands.append((n, s))
    verdicts = {"holds": 0, "violates": 0, "undecided": 0}
    bad = []
    for n, s_sieve in cands:
        s = sigma_exact(n)                     # independent recomputation
        assert s == s_sieve, f"sieve/factorization sigma mismatch at {n}: {s_sieve} vs {s}"
        v, lo, hi = robin_decide(n, s)
        verdicts[v] += 1
        if v != "holds":
            bad.append((n, s, v))
    print(f"candidates flagged by conservative filter: {len(cands)}")
    print(f"certified verdicts: {verdicts}")
    if verdicts["violates"]:
        print("!!! certified violation above 5040 — per RULES.md §7 this is")
        print("!!! overwhelmingly a bug. extraordinary-claim protocol applies.")
        print("!!! offending n:", [b[0] for b in bad if b[2] == "violates"])
        return 4
    if verdicts["undecided"]:
        print("kill K3: undecided candidates:", [b[0] for b in bad])
        return 3

    # --- 3. near-miss catalogue ---
    # Rank BOTH the per-segment argmaxes of sigma(n)/n AND every flagged
    # candidate.  The latter matters in the first segment, where log log n
    # varies enough that the argmax of sigma(n)/n (a large abundant number)
    # is not the argmax of the Robin ratio (a small one like 10080).
    argmaxes = sorted({(bn, bs) for (_, _, bn, bs, _) in segs} | set(cands))
    scored = []
    for bn, bs in argmaxes:
        assert sigma_exact(bn) == bs, f"argmax sigma mismatch at {bn}"
        lo, hi = ratio_enclosure(bn, bs)
        scored.append((lo, hi, bn, bs))
    scored.sort(reverse=True)
    with open(f"{ckpt}/near_misses.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["n", "sigma", "ratio_lo", "ratio_hi", "factorization"])
        for lo, hi, bn, bs in scored[:TOP_K]:
            fac = " * ".join(f"{p}^{e}" if e > 1 else f"{p}"
                             for p, e in sorted(factorize(bn).items()))
            w.writerow([bn, bs, f"{lo:.12f}", f"{hi:.12f}", fac])
    print(f"top {min(TOP_K, len(scored))} near-misses -> {ckpt}/near_misses.csv")
    top = scored[0]
    print(f"largest certified Robin ratio among per-segment argmaxes: "
          f"n={top[2]}, ratio in [{top[0]:.12f}, {top[1]:.12f}]")
    print(f"RESULT: sigma(n) < e^gamma * n * log log n certified for all "
          f"5041 <= n < {N}")
    return 0

if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
