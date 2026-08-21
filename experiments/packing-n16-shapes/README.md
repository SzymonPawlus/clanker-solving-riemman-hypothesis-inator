# packing-n16-shapes

Code for [`problems/circle-packing-equilateral-triangle/attacks/n16-shapes/`](../../problems/circle-packing-equilateral-triangle/attacks/n16-shapes/README.md).
Python standard library only. Exact `Fraction` arithmetic in every decision; the search stage is
float and decides nothing.

| file | what |
|---|---|
| `geom.py` | exact rational geometry in the triangular basis $e_1=(1,0)$, $e_2=(1/2,\sqrt3/2)$: squared distances, areas, convexity, half-plane clipping, **convex-minus-convex difference**, hulls |
| `controls.py` | controls for Lemma S, Lemma C, $\operatorname{diam}\operatorname{conv}=\operatorname{diam}$, the Minkowski-sum diameter bound, the $n$-chord sector areas, and the claim that the standing certificate's corner cells are the $n=2$ sector polygon |
| `audit.py` | exact re-derivation and loss decomposition of the standing record certificate (`../packing-n16-covering/sub_s2_cert.json`, read-only) |
| `tri_group.py` | the search representation: a triangulation of $T_a$ whose triangles are **grouped**, each group's piece being the convex hull of its triangles — coverage automatic, overlap free |
| `seed.py`, `refine.py` | build the seed from the standing certificate; insert extra corner arc vertices (the move a convex partition cannot make) |
| `drive.py` | perturbation-restart descent (floats, seeded, checkpoints to JSON) |
| `certify.py` | float config -> exact rational certificate, verified as it is produced |
| `verify.py` | **independent re-verification of a certificate from the problem statement alone** |

Reproduce the result (a few seconds, no network, no seeds):

```bash
python3 controls.py
python3 audit.py
python3 verify.py best_ref_cert.json
```

`best_ref_cert.json` is the frozen certificate: 15 convex polygons with exact rational vertices,
max squared diameter $9997800121/10^{10} < 1$, covering $T_{89267/20000}$ (verified by exact
polygon difference, **not** by an area identity — the pieces overlap), hence
$a_{16} \ge 4463841021/10^9$.
