"""Single reproduce command for everything in this directory.

    python3 run_all.py

Order matters: the closed forms are checked against the published table, then the
checker is validated on solved instances and negative controls, then the float ->
Q(sqrt 3) snap is shown, then the certificates are emitted, then the emitted JSON
files are re-parsed from disk and re-verified independently of the in-memory
configuration.
"""
import importlib.util, json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))


def run(script):
    print("\n" + "=" * 72)
    print("$ python3 %s" % script)
    print("=" * 72)
    sys.stdout.flush()   # parent stdout is block-buffered when redirected; the
                         # child writes straight to the fd, so flush or the
                         # section headers land after the output they label.
    rc = subprocess.call([sys.executable, os.path.join(HERE, script)], cwd=HERE)
    if rc != 0:
        raise SystemExit("%s failed with exit code %d" % (script, rc))


def run_optional(script, module, what):
    """Run a NON-load-bearing diagnostic, skipping it if its dependency is absent.

    The exact certificate pipeline is stdlib-only.  `pyproject.toml` therefore
    declares `dependencies = []`, and this function is what makes that honest:
    a missing optional dependency must not stop the pipeline that does the real
    work.  Returns True if it ran, False if it was skipped.
    """
    print("\n" + "=" * 72)
    if importlib.util.find_spec(module) is None:
        print("SKIPPED (optional): python3 %s" % script)
        print("=" * 72)
        print("  `%s` is not installed, so this diagnostic did not run." % module)
        print("  What was skipped: %s" % what)
        print("  It is NOT load-bearing -- it compares a published FLOAT table against")
        print("  the closed forms.  Every exact check below runs on stdlib")
        print("  fractions.Fraction alone and is unaffected.")
        print("  To run it too:  pip install mpmath>=1.3.0  (tested with 1.3.0)")
        sys.stdout.flush()
        return False
    run(script)
    return True


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
    ran_closed_forms = run_optional(
        "verify_closed_forms.py", "mpmath",
        "agreement of the published Graham-Lubachevsky m(n) floats with "
        "6+4sqrt3, 8+4sqrt3, 10+4sqrt3 to 15 s.f.")
    run("validate.py")
    run("snap.py")
    run("rattler.py")
    run("emit.py")
    reverify_from_disk()
    if not ran_closed_forms:
        print("\nNOTE: the optional mpmath diagnostic was skipped (see the top of this")
        print("log). Nothing above depended on it: the certificates are exact and were")
        print("checked with stdlib Fraction arithmetic only.")
