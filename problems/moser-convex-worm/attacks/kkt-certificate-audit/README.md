# Clean-room audit of the `0.23518745713` certificate

**Issue:** #202. **Status:** independent exact audit of a `sketch` support
certificate. The convex-area interpretation remains conditional on the
finite-polygon mixed-area/common-fan bridge in Issues #170/#176.

This audit uses only the witness statement from PR #195, not its checker or
tests. It independently reconstructs the exact rational geometry, positive
balanced circuits, equilateral-triangle fan minima, residual segment bounds,
projection-sign cells, concavity argument, and the direct-motion involution.

The audited witness has half-angle parameters

```text
(-43133/53882, -929/49257, 929/49257, 43133/53882)
```

and open-arc edge lengths

```text
(7381/21619, 6857/43238, 6857/43238, 7381/21619).
```

## Verdict

The exact floor

```text
23518745713/100000000000 = 0.23518745713
```

survives this audit. The checker derives, rather than assumes, that the only
positive three-direction circuits are

```text
(0,2,4), (0,3,4), (1,2,4), (1,3,4).
```

It uses the following independently selected rational cover in
`u=tan(phi/2)`:

```text
C: [0, 224348713/1000000000]
A: [224348713/1000000000, 1/3]
S: [1/3, 745974447/1000000000]
B: [745974447/1000000000, 1].
```

No positive residual term crosses a projection wall within its assigned
cell. Each cell formula is therefore a constant plus nonnegative sine widths,
so it is concave and its minimum occurs at an endpoint. All eight endpoint
inequalities are positive in exact `Q(sqrt(3))` arithmetic. Reversal of the
four traversed indices exchanges the crossed circuits `A,D`, preserves the
other data, and covers the second half-turn without introducing a reflection.

## Slack

The certificate is genuinely tight. Non-rigorous decimal diagnostics give:

| location | active bound | margin above target |
|---|---|---:|
| `phi=0` | `C` | about `1.66e-11` |
| first splice | `C` | about `9.14e-12` |
| first splice | `A` | about `6.14e-12` |
| central splice | `S` | about `1.08e-10` |
| central splice | `B` | about `3.27e-11` |

The exact checker prints the limiting `phi=0` margin as
`q+r*sqrt(3)` with rational `q,r`, and proves its sign without floating point.
The tiny splice overlap leaves essentially no room to simplify the cut
denominators. It also shows where any perturbative improvement must act: the
endpoint and both circuit-switch wells must rise together.

Replay:

```text
python problems/moser-convex-worm/attacks/kkt-certificate-audit/audit_exact.py
python -O problems/moser-convex-worm/attacks/kkt-certificate-audit/audit_exact.py
python problems/moser-convex-worm/attacks/kkt-certificate-audit/reconstruct_numeric.py
```

`reconstruct_numeric.py` is reconnaissance only and is not used by the exact
proof. The audit is frozen before an asymmetric or fifth-edge search so that
later exploratory changes cannot obscure its review target.
