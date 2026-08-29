# 2026-08-29 — spiral-tip exceptional point (idea I2)

Worker journal. `claude` (Claude Opus 5), branch `claude/inscribe-equilateral-triangle-oj15x1`.
Lane files: `problems/inscribed-equilateral-triangle/attacks/spiral-tip-witness/`.
This is a journal: it records the order things happened, including the wrong turns. The claims live
in the lane README, with statuses; nothing here is assumable.

---

## Order of work

1. Read `RULES.md` §0/§1/§2/§3/§5/§6/§7/§9, the problem `README.md` and `RULES.md`, ideation I2/I3,
   `attacks/rotation-continuity/README.md` (§1–§6), `attacks/convex-vertex-criterion/README.md`
   (§0–§2), `attacks/rectifiable-case/README.md`.
2. Re-derived the criterion from scratch on paper (Lemma 1) *before* re-reading Observation R and
   Proposition R, so that the agreement in the lane README §2.2 is a cross-check and not an echo.
3. Designed the construction on paper.
4. Wrote `KILL-CRITERION.md`. **No code had been run at this point.** The file says so, and says
   the honest qualification: it precedes all computation but not all thought, so K1/K2 are bets
   made by someone who already expected them not to fire.
5. Ran the numerics. Four scripts; the third was discarded (see "the instrument was wrong" below).
6. Wrote the lane README.

## The design, and the one moment it was in doubt

The brief's framing — a spiral arm whose radius is strictly monotone, so equal radii force equal
parameters — makes the *arm* trivial. The whole question is the closing arc. I spent the first
half hour on the wrong version of that question ("where can the closing arc go so it is far from
the arm?"), which has no answer, before noticing the right one:

> The closing arc has to reach `O`, and `O` is the accumulation point of the arm. So it has to get
> there *through* the complement of the arm near `O`.

Pass to `w = log z`: the arm's preimage in the universal cover of the punctured disc is a family of
parallel lines, permuted transitively by the deck transformation, so the complement downstairs is a
single spiralling channel. Conclusion: the complement is connected — the arc *can* reach `O` — but
it must itself wind infinitely. **The closing arc is forced to be a second spiral tip.** That was
the moment the construction became obvious: if the second arm has to be a spiral anyway, make it a
*congruent* one, `C = e^{i beta} S`, so the two arms sit a constant angle apart on every circle.

Then the criterion becomes bookkeeping on one circle at a time, and

  at radius r, the directions of J are exactly { tau(r), tau(r) + beta },  tau(r) = -ln r / c,

which is the only computation in the lane. Everything else follows from `beta < 60 deg`.

The general lemma that fell out (README §3, "Lemma 2") is the thing I actually think is worth
keeping: **the wedge test is the special case of a per-circle wedge that does not rotate.** Letting
it rotate with the radius lets the union of the wedges be all of `S^1` while every individual wedge
stays under 60 degrees. That reframing is what makes "full direction set, still exceptional"
unsurprising in retrospect, which is the sign it is the right statement.

## Things I got wrong or nearly got wrong

**(a) The instrument was wrong, and it nearly refuted my own corollary.** My first detector for
"do `J` and `rho_alpha(J)` meet?" counted *proper* segment crossings (strict orientation sign
changes both ways). For `|alpha| < beta` the theory predicts they meet — and they do, but along a
**tangential overlap of two arcs of the same unit circle**, which a strict crossing test is
designed not to report. The count was also unstable under refinement: 5 crossings at 720 samples
per turn, 0 at 360. I had written "theory: GOOD" next to a printed `0` before I understood why.

Had I taken that at face value I would have recorded a false refutation of Corollary 5 in a file
whose whole point is exceptional-point bookkeeping. What saved it was that the disagreement was
between two things I had derived, not between a derivation and an expectation — §0's actual
mechanism, working. Replaced by a distance-based detector, which shows the predicted transition at
`|alpha| = beta`. Recorded in the lane README §8.1 item 5 and §11 (K5) rather than quietly fixed.

**(b) Nearly claimed rectifiability without computing it.** The kill-criterion explicitly says the
arm's length is an integral, not a picture. It is `sqrt(1+c^2)/c` per arm — finite — and the same
integral gives the much better fact that **arclength from the tip is exactly proportional to the
radius**, `r = c s / sqrt(1+c^2)`. So the chord/arc ratio at `O` is a constant in `(0,1)` and the
tangent fails to exist purely by winding. That is a sharper statement than "not differentiable" and
I would not have found it if I had asserted finiteness instead of integrating.

**(c) Almost picked a pitch that makes the corner count ambiguous.** The interior angle at the
outer corner `P0` is `arctan(c)`, which is below 60 degrees for `c < sqrt 3`. That does not make
`P0` exceptional — the wedge test needs the *whole* curve in the cone, and here the curve wraps all
the way round — but it would have made the `|E(J)| = 1` story rest entirely on numerics. Choosing
`c = 2` puts both corner angles above 60 degrees. I still ran `c = 0.3` and `c = 1` deliberately, as
the stress test for K6: if the small-`c` corners had come out exceptional, three exceptional points
would contradict Meyerson and, per §7, the first suspect would have been me. They came out good.

**(d) Did not run the polygon control, and said so.** Every exceptional point of a polygon is
wedge-type; the rotating-wedge mechanism needs infinitely many direction changes in every
neighbourhood. So `experiments/inscribed-triangle-polygons/` cannot see this and agreement with it
would have meant nothing. Faking that check would have been easy and worthless. Related: truncating
the spiral at any positive radius **removes `O` from the curve**, so this exceptional point is not a
limit of exceptional points of the truncations — an approximation argument cannot reach it.

## Status discipline notes

- Everything produced is `sketch` or `numerical`. I cannot grant `verified:review` to my own work
  and did not.
- I deliberately did **not** import Observation R (`attacks/rotation-continuity`) or Proposition R
  (`attacks/convex-vertex-criterion`); both are `sketch`, and a `sketch` may not rest on a `sketch`.
  Lemma 1 is re-derived. The agreement between the three is reported as decorrelation, worth
  something socially and nothing logically.
- Meyerson's bound is used only as a consistency check *on* the output, never as an input — it is
  `cited`* (provisional, P2, no source text read) in the problem README as of today.
- K7 (is this already Meyerson's or Schwartz's own example?) is **unresolved and unresolvable from
  this session**: no scholarly host is reachable. "Not found" is not evidence of novelty. The lane
  claims none.

## Files owned by this worker

- `problems/inscribed-equilateral-triangle/attacks/spiral-tip-witness/README.md`
- `problems/inscribed-equilateral-triangle/attacks/spiral-tip-witness/KILL-CRITERION.md`
- this file

Ran no git command; the dispatcher commits.

---

## The script

`numpy` only, deterministic, no seeds, no `sympy` geometry predicates (the repo found
`Segment2D.intersection` wrong on 3 of 176 boundary cases today, witnesses off-segment by ~1e-16);
segment predicates below are reimplemented from orientation sign tests. Written to the session
scratchpad, reproduced here in full because this lane owns no `experiments/` directory.

Run as `python3 spiral.py` (part A) and `python3 spiral4.py out.txt` (part B).

### Part A — embeddedness, radial normal form, and the main claim

```python
import numpy as np, math

def build(c, beta, rmin=1e-9, per_turn=720):
    """J = {0} u S u e^{i beta} S u arc(1 -> e^{i beta}),  S = {e^{-c t} e^{i t}: t>=0},
    truncated at |z| = rmin and closed to the origin by two straight segments.
    NOTE: this truncation is a DIFFERENT curve from J -- it has no spiral tip. It is used
    only to cross-check the finite part of the picture."""
    tmax = -math.log(rmin)/c
    n = max(64, int(per_turn*tmax/(2*math.pi)))
    t = np.linspace(0.0, tmax, n)
    S = np.exp(-c*t)*np.exp(1j*t)
    C = np.exp(1j*beta)*S
    narc = max(16, int(per_turn*beta/(2*math.pi)))
    arc = np.exp(1j*np.linspace(0.0, beta, narc))
    pts = np.concatenate([[0j], S[::-1], arc[1:-1], C, [0j]])
    return np.stack([pts.real, pts.imag], axis=1)

def cross(o, a, b):                      # 2x2 orientation determinant, broadcast
    return (a[...,0]-o[...,0])*(b[...,1]-o[...,1]) - (a[...,1]-o[...,1])*(b[...,0]-o[...,0])

def proper_crossings(A, B):              # strict sign changes on both sides
    p1=A[:-1][:,None,:]; p2=A[1:][:,None,:]; q1=B[:-1][None,:,:]; q2=B[1:][None,:,:]
    d1=cross(q1,q2,p1); d2=cross(q1,q2,p2); d3=cross(p1,p2,q1); d4=cross(p1,p2,q2)
    return np.argwhere((d1*d2<0)&(d3*d4<0))

def self_crossings(A):                   # K4: all pairs, non-adjacent only
    n=len(A)-1
    return [(int(i),int(j)) for i,j in proper_crossings(A,A)
            if not (i==j or (i+1)%n==j%n or (j+1)%n==i%n)]

def rot(P, X, ang):
    z=(P[:,0]-X[0])+1j*(P[:,1]-X[1]); w=z*np.exp(1j*ang)
    return np.stack([w.real+X[0], w.imag+X[1]], axis=1)
```

Checks driven from these: `self_crossings(A)` (K4); the radial normal form, by comparing each
vertex's argument against `{tau(r), tau(r)+beta}` with `tau(r) = -log(r)/c`; and the main claim,
`proper_crossings(A, rot(A, [0,0], pi/3))` together with the scale-invariant separation
`min_p dist(rho(p), J) / |p|`.

The symbolic sanity check of Lemma 1 (part (a) of the run) uses `sympy` **algebra only**:

```python
import sympy as sp
r, th = sp.symbols('r theta', positive=True)
P = sp.Matrix([r*sp.cos(th),            r*sp.sin(th)])
Q = sp.Matrix([r*sp.cos(th+sp.pi/3),    r*sp.sin(th+sp.pi/3)])
# |OP| = |OQ| = |PQ| = r ; and cos(angle POQ) = (s^2+s^2-s^2)/(2 s^2) = 1/2
```

### Part B — the distance detector (replaces the crossing counter; see "the instrument was wrong")

```python
def seg_pt_dist(A, P, chunk=256):        # min distance from each point of P to polyline A
    a=A[:-1]; b=A[1:]; ab=b-a; L2=(ab**2).sum(1); L2[L2==0]=1e-300
    out=np.empty(len(P))
    for s in range(0,len(P),chunk):
        p=P[s:s+chunk][:,None,:]
        u=np.clip(((p-a[None])*ab[None]).sum(2)/L2[None],0,1)
        proj=a[None]+u[:,:,None]*ab[None]
        out[s:s+chunk]=np.sqrt(((p-proj)**2).sum(2)).min(1)
    return out

def gap(A, X, ang, sub=1, floor=1e-3):   # 0 <=> rho_X,ang(J) meets J away from X
    R=rot(A,X,ang)[::sub]
    d=np.linalg.norm(R-X,axis=1)
    keep=d > floor*np.max(np.linalg.norm(A-X,axis=1))
    return float(np.min(seg_pt_dist(A,R[keep])/d[keep]))
```

`gap` is normalised by `|p - X|`, which makes it scale-invariant — necessary, because the tip germ
is self-similar under `z -> e^{-2 pi c} z` and an unnormalised distance would go to zero near `O`
for trivial reasons.

## Results as run

Parameter sets: `(c, beta) = (2, 30 deg)`, `(0.3, 30 deg)`, `(1, 55 deg)`; truncation radii
`1e-3` to `1e-9`, i.e. 1.3 to 7.3 turns; 950 to 15888 segments.

| check | result |
|---|---|
| Lemma 1 symbolically | `|OP| = |OQ| = |PQ| = r`; `cos(angle POQ) = 1/2`. K1 not met |
| K4 embeddedness, all pairs non-adjacent | **0** crossings in every run (5 runs) |
| radial normal form | max deviation from `{tau(r), tau(r)+beta}` = `9.8e-15` |
| `J` vs `rho_(O,60)(J)`, proper crossings | **0** in every run |
| `min_p dist(rho_60(p), J)/|p|` | `0.4117` (c=2), `0.1402` (c=0.3), `0.0613` (c=1, beta=55) |
| `J` vs `rho_(O,90)(J)` | **0** crossings — the square-test remark |
| Corollary 5 transition | gap positive exactly for `beta < |alpha| < 360 - beta` |
| exceptional census | see lane README §10 |

The `0.0613` for `beta = 55 deg` against `0.4117` for `beta = 30 deg` is the quantitative form of
README §5.4: the construction degenerates as `beta -> 60 deg`, where the closing arc's own endpoints
become an inscribed equilateral triangle with `O`.

## What I would tell the next worker

1. The lane's transferable object is **Lemma 2**, not the spiral. "Per-circle wedge, allowed to
   rotate" is the right generality; the log spiral is one way to realise it and §12.1 of the lane
   README gives the general form.
2. The open question I could not answer (README §12.3): the rotating wedge is a *mechanism*, not a
   classification. `Theta_J(r) = {0, 100, 200}` degrees avoids 60-degree pairs without lying in any
   small arc, so there is at least room for a third mechanism. What can `{Theta_J(r)}` look like at
   an exceptional point of a Jordan curve? That is where I would go next, and it is also the frame
   in which one would ask why the sharp bound is **two**. Nothing here explains the two.
3. Do not try to formalise Proposition 4 (Jordanness) in Lean — it needs the Jordan curve theorem
   for the interior, which Mathlib does not have. Lemmas 1–3 and Theorem 1, with the word "Jordan"
   deleted, are the reachable target and carry the entire mathematical content.
