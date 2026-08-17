# Experiments

Numerical work. Results here carry status `numerical` — evidence about where to look, never a
step in a proof.

One directory per experiment, `<problem-slug>-<what>/`, containing:

- a `README.md` stating the question, the method, and the result,
- the code,
- a single command that reproduces it from scratch.

Pin your dependency versions and any random seeds. An experiment nobody can re-run is an
anecdote.

Use `uv` for Python environments. High-precision zeta work generally wants `mpmath`; state the
precision you used and check that results are stable when you raise it — silently
precision-limited output that looks like a discovery is the standard way to waste a week here.
