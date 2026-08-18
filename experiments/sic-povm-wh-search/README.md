# Bounded Weyl--Heisenberg SIC search pilot

This experiment uses the convention of Appleby, *SIC-POVMs and the Extended
Clifford Group*, J. Math. Phys. 46, 052107 (2005),
[arXiv:quant-ph/0412001](https://arxiv.org/abs/quant-ph/0412001):

\[
X|a\rangle=|a+1\rangle,\quad Z|a\rangle=\omega^a|a\rangle,
\quad D_{p,q}=\tau^{pq}X^pZ^q,
\]

where \(\omega=e^{2\pi i/d}\) and \(\tau=-e^{\pi i/d}\).  It minimizes the
squared residuals
\(|\langle\psi|D_{p,q}|\psi\rangle|^2-1/(d+1)\) for all nonzero `(p,q)`.

`search.py` uses vectorized displacement actions and an analytic gradient.
`evaluate.py` is intentionally separate and constructs every displacement
matrix entry-by-entry. The two paths are compared at every completed start.

Run with the pinned dependencies:

```sh
PYTHONPATH=/tmp/codex69deps python3 search.py --phase calibrate --output results/calibration
PYTHONPATH=/tmp/codex69deps python3 search.py --phase target --output results/d56
```

The first command is a mandatory gate: both `d=4` and `d=5` must reach maximum
absolute residual below `1e-12` within five minutes. The target phase has ten
pinned seeds and a 45-minute total cap. A failed bounded search is numerical
evidence only and says nothing about existence or nonexistence.
