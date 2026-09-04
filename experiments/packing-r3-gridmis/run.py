#!/usr/bin/env python3
"""Single reproduce command for experiments/packing-r3-gridmis.

    cd experiments/packing-r3-gridmis && python3 run.py

Reruns, in order:
  0. randomised soundness tests of Lemma 1 (test_lemma.py, seeds 1/2/3)
  1. tiny known-answer validations (n = 3, 5, 6 against cited d(n))
  2. the two-sided n = 12 calibration (must refute below d(12), never above)
  3. the n = 12 and n = 16 grid/threshold sweeps that fit in the budget
  4. one DRAT-checked refutation end to end (needs `drat-trim` on PATH)

Writes out/reproduce.json and prints a summary table.  Budget ~15 min on 4 cores.
"""
import json, math, os, subprocess, sys, time
from fractions import Fraction as F

from gridmis.lattice import build_graph
from gridmis.mis import decide, verify_independent
from gridmis.satproof import build_cnf, solve_with_proof
from pysat.solvers import Solver

OUT = "out"
os.makedirs(OUT, exist_ok=True)
D12 = 4 + 2 * math.sqrt(3)          # 7.4641016...  cited
OLER16 = math.sqrt(129) - 3         # 8.3578174...  sketch (attacks/r3-approaches §0.1)


def engine(G, n, tb):
    """B&B first (cheap when the root bound suffices), then SAT."""
    res = decide(G.adj, n, time_budget=tb)
    if res[0] == "SAT":
        assert verify_independent(G.adj, res[1])
        return "SAT", "bnb", res[1]
    if res[0] == "UNSAT":
        return "UNSAT", "bnb", None
    cl, _ = build_cnf(G.adj, n)
    s = Solver(name="glucose4", bootstrap_with=cl)
    r = s.solve()
    s.delete()
    return ("SAT" if r else "UNSAT"), "glucose4", None


def row(n, dstr, gstr, tb):
    t = time.time()
    G = build_graph(F(dstr), F(gstr))
    verdict, how, wit = engine(G, n, tb)
    return dict(n=n, d=dstr, g=gstr, d_float=float(F(dstr)), V=G.n_vertices, E=G.n_edges,
                rho_eff=math.sqrt(float(G.rho_eff_sq())),
                scaled_side=2 * (float(F(dstr)) + 2 * math.sqrt(3) * float(G.r))
                / math.sqrt(float(G.rho_eff_sq())),
                verdict=verdict, engine=how, secs=round(time.time() - t, 1))


def main():
    report = {}

    print("== 0. soundness tests ==", flush=True)
    cp = subprocess.run([sys.executable, "test_lemma.py"], capture_output=True, text=True)
    print(cp.stdout.strip())
    report["soundness_tests_pass"] = cp.returncode == 0
    if cp.returncode != 0:
        print("SOUNDNESS TESTS FAILED - stopping"); sys.exit(1)

    print("\n== 1. tiny known-answer validation ==", flush=True)
    tiny = []
    for n, dstr, gstr, expect in [(3, "3/2", "1/4", "UNSAT"), (3, "2", "1/4", "SAT"),
                                  (5, "7/2", "1/4", "SAT"), (6, "4", "1/4", "SAT"),
                                  (6, "3", "1/4", "UNSAT")]:
        r = row(n, dstr, gstr, 30)
        r["expected"] = expect
        r["ok"] = r["verdict"] == expect
        tiny.append(r); print(json.dumps(r), flush=True)
    report["tiny"] = tiny

    print("\n== 2. two-sided control at n=12: must be SAT for every d >= d(12) ==", flush=True)
    ctrl = []
    for gstr in ["1/4", "1/6", "1/8", "1/10"]:
        for dstr in ["7465/1000", "75/10", "8", "9"]:
            r = row(12, dstr, gstr, 60)
            r["control_ok"] = (r["verdict"] == "SAT")
            ctrl.append(r); print(json.dumps(r), flush=True)
    report["control12"] = ctrl
    report["control12_all_sat"] = all(x["control_ok"] for x in ctrl)
    print("two-sided control:", "PASS" if report["control12_all_sat"] else "FAIL", flush=True)

    print("\n== 3a. n=12 threshold sweep ==", flush=True)
    s12 = []
    for gstr, dlist in [("1/4", ["6", "62/10", "64/10"]),
                        ("1/6", ["66/10", "68/10", "7"]),
                        ("1/8", ["68/10", "7", "72/10"])]:
        for dstr in dlist:
            r = row(12, dstr, gstr, 30)
            s12.append(r); print(json.dumps(r), flush=True)
    report["sweep12"] = s12

    print("\n== 3b. n=16 threshold sweep ==", flush=True)
    s16 = []
    for gstr, dlist in [("1/4", ["78/10", "8", "82/10"]),
                        ("1/5", ["78/10", "8"])]:
        for dstr in dlist:
            r = row(16, dstr, gstr, 30)
            s16.append(r); print(json.dumps(r), flush=True)
    report["sweep16"] = s16
    best = max([x["d_float"] for x in s16 if x["verdict"] == "UNSAT"], default=None)
    report["best_d16_refuted"] = best
    report["beats_oler"] = (best is not None and best > OLER16)
    print("best d refuted at n=16: %s   Oler floor %.6f   beats it: %s"
          % (best, OLER16, report["beats_oler"]), flush=True)

    print("\n== 4. DRAT-checked refutation ==", flush=True)
    G = build_graph(F("62/10"), F("1/4"))
    out = solve_with_proof(G.adj, 12, OUT, "reproduce_n12_g1-4_d62-10", timeout=900)
    print(json.dumps({k: v for k, v in out.items() if k != "checker_output"}), flush=True)
    report["drat"] = {k: v for k, v in out.items() if k != "checker_output"}

    with open(os.path.join(OUT, "reproduce.json"), "w") as f:
        json.dump(report, f, indent=1)

    print("\n== SUMMARY ==")
    print("soundness tests            :", "PASS" if report["soundness_tests_pass"] else "FAIL")
    print("tiny known-answer cases    :", "PASS" if all(x["ok"] for x in tiny) else "FAIL")
    print("two-sided control (n=12)   :", "PASS" if report["control12_all_sat"] else "FAIL")
    print("largest d refuted, n=12    :",
          max([x["d_float"] for x in s12 if x["verdict"] == "UNSAT"], default=None),
          " (d(12) = %.6f)" % D12)
    print("largest d refuted, n=16    :", best, " (Oler floor %.6f)" % OLER16)
    print("kill-criterion             :", "FIRED" if not report["beats_oler"] else "not fired")
    print("DRAT verified              :", report["drat"].get("checked"))


if __name__ == "__main__":
    main()
