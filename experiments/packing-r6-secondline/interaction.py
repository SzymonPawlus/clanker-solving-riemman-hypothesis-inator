"""(F2) How much is the inter-strip interaction worth?

B(a)  = one-family bound  = max over (phi,h,theta) of sum_j (floor(ell_j) + 1)   [offsets free]
M(a)  = two-family count  = max over unit-separation lattices of |(L+t) cap T(a)| [offsets in AP]

B(a) - M(a) is exactly what the second line family buys, because the ONLY thing the second
family adds to the one-family relaxation is that the per-strip offsets x_j form an arithmetic
progression x_0 + j*beta (mod 1) instead of being free.

STATUS: numerical.
"""
import json, sys
import one_family as OF
import two_family as TF

if __name__ == "__main__":
    aa = [float(x) for x in sys.argv[1:]] or [6.0, 5.999999, 5.99, 5.9, 5.5, 5.0]
    rows = []
    for a in aa:
        B, argB = OF.scan(a, 0.0, cap="floor", hmax=a + 0.6)
        M, infoM = TF.sweep(a, nphi=31, nbeta=6, nh=12, nt=36)
        rows.append({"a": a, "B_one_family": B, "M_two_family": M, "interaction_gain": B - M,
                     "argB_phi_deg": __import__("math").degrees(argB[0]), "argB_h": argB[1],
                     "argM": infoM})
        print(json.dumps({k: v for k, v in rows[-1].items() if k != "argM"}), flush=True)
        json.dump(rows, open("out/interaction.json", "w"), indent=1)
