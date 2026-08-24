"""Single reproduce command for everything in this directory.

    python3 run_all.py

Order matters: the closed forms are checked against the published table, then the
checker is validated on solved instances and negative controls, then the float ->
Q(sqrt 3) snap is shown, then the certificates are emitted, then the emitted JSON
files are re-parsed from disk and re-verified independently of the in-memory
configuration.
"""
import json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))


def run(script):
    print("\n" + "=" * 72)
    print("$ python3 %s" % script)
    print("=" * 72)
    rc = subprocess.call([sys.executable, os.path.join(HERE, script)], cwd=HERE)
    if rc != 0:
        raise SystemExit("%s failed with exit code %d" % (script, rc))


def parse_q3(s):
    """Parse an exact 'a + b*sqrt(3)' string back into Q3. Rejects decimals."""
    from fractions import Fraction as F
    from qsqrt3 import Q3
    if re.search(r"\d\.\d", s):
        raise ValueError("decimal string in an exact field: %r" % s)
    a, b = F(0), F(0)
    for term in re.findall(r"[+-]?\s*[^+-]+", s.replace(" ", "")):
        t = term.strip()
        if not t:
            continue
        sign = F(-1) if t.startswith("-") else F(1)
        t = t.lstrip("+-")
        if "sqrt(3)" in t:
            c = t.replace("*sqrt(3)", "").replace("sqrt(3)", "")
            b += sign * (F(c) if c else F(1))
        else:
            a += sign * F(t)
    return Q3(a, b)


def reverify_from_disk():
    print("\n" + "=" * 72)
    print("re-verifying the emitted certificate FILES, parsed back from disk")
    print("=" * 72)
    sys.path.insert(0, HERE)
    from qsqrt3 import Q3
    from check import check
    ok = True
    for n in (17, 24, 31):
        path = os.path.join(HERE, "certificates", "n%03d-r3-qsqrt3.json" % n)
        with open(path) as fh:
            c = json.load(fh)
        s = parse_q3(c["side_length"])
        d = s - Q3(0, 2)
        pts = [(parse_q3(x), parse_q3(y)) for x, y in c["coordinates"]]
        rep = check(c["n"], d, pts, verbose=False)
        good = rep["ok"] and rep["tight"] and c["claim"] == "construction" \
            and c["status"] == "numerical" and rep["s_exact"] == c["side_length"]
        ok &= good
        print("  %s  n=%2d  s <= %-16s  feasible=%s  tight=%s  contacts=%d  status=%s"
              % ("PASS" if good else "FAIL", n, c["side_length"], rep["ok"],
                 rep["tight"], rep["n_contacts"], c["status"]))
    if not ok:
        raise SystemExit("a certificate file failed re-verification")
    print("\nAll three certificate files re-verify from disk, exactly and tight.")
    print("Claim established: s(17) <= 6+4sqrt3, s(24) <= 8+4sqrt3, s(31) <= 10+4sqrt3.")
    print("These are CONSTRUCTIONS (upper bounds), status `numerical`.")
    print("NO optimality is claimed; n = 17, 24, 31 are all open.")


if __name__ == "__main__":
    run("verify_closed_forms.py")
    run("validate.py")
    run("snap.py")
    run("rattler.py")
    run("emit.py")
    reverify_from_disk()
