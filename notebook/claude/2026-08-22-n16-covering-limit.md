# 2026-08-22 — worker C4 — the ceiling of the 15-piece covering method ($n=16$)

Lane: prove an **upper** bound on $A_{15}=\sup\{a: T_a$ coverable by 15 sets of diameter $<1\}$.
Three other workers are pushing the lower end ($4.46335$ today); the absolute ceiling is
$4.6247636$, where a 16-point packing exists. If $A_{15}<4.6247636$, the method can never do
$n=16$ and the team should stop.

Write-up: `problems/circle-packing-equilateral-triangle/attacks/n16-covering-limit/`.
Code: `experiments/packing-n16-limit/`. Kill-criteria written before computing.

## Outcome

**Proved $A_{15}\le 4.914308$.** Does not close the method. But the more useful output is the
ceiling: **no bound derivable from my structure lemma can beat $4.836854$**, and even lending the
coverer the two strongest results I could think of but not verify (Fejes Tóth's hexagon bound,
Graham's biggest little hexagon) only moves that to $4.7258$, still above $4.6247636$. K1 fired; I
stopped.

## What actually decided it, and I should have seen it in five minutes

The one-line arithmetic I did *after* building the machinery, and should have done before:

$$\frac{\operatorname{area}(T_{4.6247636})}{15}=0.617431=95.06\%\ \text{of}\ \frac{3\sqrt3}{8}=0.649519,$$

the area of a regular hexagon of diameter 1 — a shape that **tiles the plane with zero waste**.
So killing the method means proving that 15 pieces cannot reach 95% of perfect hexagonal
efficiency. Per-piece area caps cannot express that: the sharp per-piece cap is $\pi/4$ (a disk of
diameter 1 sits in the interior and attains it), $15\pi/4=11.78$ against a target of $9.26$, and
every boundary correction I proved recovers 21% of that gap. Even assuming the ideal density
constant $3\sqrt3/8$ per piece, the residual deficit needed is $0.4813$ while the entire
three-corner effect is worth $0.3778$.

**Lesson for the next lane of this shape: compute the required per-piece average against the ideal
tiling constant first.** It is one line and it prices the whole attack.

## The correction I did not expect to be making

My briefing asserted that diameter-1 sets "cannot cover at density better than the hexagonal
$2\pi/\sqrt{27}$", giving $3\sqrt3/8$ per piece and $a\le4.74342$. That is Kershner's constant for
**congruent circles**. Regular hexagons of diameter 1 tile the plane — density exactly 1 — so the
argument does not transfer to arbitrary diameter-1 sets. The arithmetic
$(\pi/4)/(2\pi/\sqrt{27})=3\sqrt3/8$ happens to land on the hexagon's area, which is what makes it
look right. The citable analogue (Fejes Tóth's hexagon bound + Graham's $A_6=0.674981$) is
*weaker*: $a\le4.835498$.

This is the `FINDINGS.md` pattern again — a correct theorem (Kershner) read one step too broadly
(circles → arbitrary sets) — and it arrived in a *dispatch instruction*, which is the delivery
mechanism the 2026-08-21 entry flagged as the expensive one. I nearly built the whole attack on
top of it; what caught it was asking "what is the extremal set?" instead of "what is the constant?"

## Method notes worth reusing

- **The trace bound $f(\ell)$.** A piece meeting an edge in a trace of diameter $\ell$ has
  $\operatorname{area}\le f(\ell)$, and $f$ is genuinely computable: slice the piece horizontally,
  and the two cross distances give $w(y)+w(y')\le2\sqrt{1-(y-y')^2}$, which with
  $w(y)\le2\sqrt{1-y^2}-\ell$ is a **linear** program in the slice widths. Solve numerically, then
  re-derive the value from a rational dual certificate — cheap, and no float touches a decision.
  $f(1)=\pi/3-\sqrt3/4$ comes out exactly, because at $\ell=1$ the admissible region *is*
  $B(A,1)\cap B(B,1)\cap\{y\ge0\}$. (I first wrote "Reuleaux triangle" here and had to correct
  it: that shape bulges on all three sides, has area $(\pi-\sqrt3)/2=0.7048$, and does not have a
  straight side to sit on the edge. The *code* had the right number throughout; the prose gloss on
  it was wrong — the `FINDINGS.md` shape exactly.)
- **Bounding your own method from below.** Feeding a certified *lower* bound on $f$ — here an
  explicit unit-diameter disk cut by the edge line — back into the lemma exhibits a budget the
  lemma cannot refute, and that is the lemma's ceiling. This turned "I could not beat X" into "no
  one can beat X with this lemma", which is the difference between a null result and a decision.
- **Pitfall (mine, twice):** `pkill -f foo.py` from a shell whose own command line contains
  `foo.py` kills the shell. Exit code 144, no output, looks like the script crashed.
- **Pitfall:** exact-rational Newton for $\sqrt{\cdot}$ doubles denominators every step and hangs
  by iteration 30. Use `math.isqrt` on a scaled integer: $\lfloor\sqrt{xS^2}\rfloor/S$ is a
  certified lower bound by construction, and $+1/S$ an upper one.

## What I did not do

- No packing search, no 16-point configuration hunt (K2: that direction is a record claim, not this
  lane's job, and the sharp separated-point tool *is* the conclusion).
- Did not try to prove Fejes Tóth's hexagon bound myself. A route exists for the restricted case of
  a convex polygonal **tiling** — Euler gives an average side count and the maximal-area $k$-gon of
  diameter 1 is concave in $k$ around 6 — but the boundary cells of a finite region carry extra
  sides (I get average $\le 6+E_b/n$, i.e. $6.4$ for 15 cells), so it does not close, and it would
  only bound tilings rather than coverings. Recorded in case someone wants it; it does not reach
  $4.6247636$ either way, per the ceiling table.
