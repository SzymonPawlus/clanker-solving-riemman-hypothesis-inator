# 2026-09-04 — Groemer 1960 read in full; his Satz *is* Oler, on the right region (#96)

Worker journal, issue #96, branch `claude/96-groemer-oler`.

## What I was asked, and what the blocker was

#96 claimed that Groemer's Satz, applied to $K = H \oplus B_1$, reduces to Oler's inequality, and
that Groemer therefore supplies the equality characterisation `attacks/oler-lower-bound/` §5.2
records as missing. The issue explicitly forbade acting on it, because the equality clause was
known here only through a one-sentence transcription and pp. 286–293 were unread. Egress was the
blocker.

## Egress: open, and the recorded locator was the wrong one

This is worth writing down because the repo's memory of "GDZ is blocked" was only half the story.
GDZ is reachable. What is *not* reachable is the locator the README recorded:

- `http://gdz.sub.uni-goettingen.de/dms/resolveppn/?PPN=GDZPPN002389444` — resolves, but lands on
  the Mathematische Zeitschrift **search portal**, not the article. Easy to mistake for a block.
- `https://gdz.sub.uni-goettingen.de/id/GDZPPN002389444` — 404.
- `https://gdz.sub.uni-goettingen.de/mets/PPN266833020_0073` — 404.

What works: the **volume** PPN `PPN266833020_0073`, then its IIIF presentation manifest, then the
logical range `LOG_0047` (Groemer's article, 10 canvases), then the IIIF image API at
`https://images.sub.uni-goettingen.de/iiif/image/gdz:PPN266833020_0073:000003NN/full/1800,/0/default.jpg`
for `NN = 299…308`. The manifest labels its own canvases with printed page numbers, so the
299↔285 mapping is the library's, not my guess.

Two general lessons, both of which cost me time:

1. **No OCR is installed** (`tesseract`, `ocrmypdf` both absent), but that does not matter — the
   `Read` tool renders a page image and I read the German myself. For a scanned primary source
   that is the whole pipeline: IIIF image → `Read`. Worth remembering; it makes a lot of "blocked,
   scan only" literature actually readable.
2. `sympy` is not in the system python. `pip install --break-system-packages` works.

## What the source says

All ten pages read. The equality clause is printed on p. 285 as running italics and has **three
labelled cases**, not the two-and-a-parenthetical the README carried. Full German transcription is
in `attacks/groemer-oler-equivalence/` §2.

The load-bearing question — does the clause carry a hypothesis lost in transcription? — is
**answered, and the answer is yes, but harmlessly.** Case a) (the triangle case, the one everything
here rests on) was transcribed faithfully. Case b) was not: the README said "or degenerates to a
segment", where Groemer requires $H$ to decompose into segments of length 2 **with every endpoint a
centre**. A segment hull alone is not an equality case — centres at $0, 2, 5$ are a counterexample.
The paraphrase erred toward being *more permissive* than the source, so nothing built on case a) is
affected, but it is exactly the class of error the issue was worried about, and it was real.

Also settled: p. 294's "Dies ergibt Teil a) des Satzes" — the README left open whether this pointed
at an unread part of the paper. It does not. "Teil a)" is case a) of the equality clause; b) and c)
are dispatched two sentences earlier. The equality characterisation is genuinely proved in both
directions (Hilfssatz 1 carries the biconditional; p. 290 tracks the equality condition explicitly).

## The derivation

Redone from scratch, not read off the issue. `attacks/groemer-oler-equivalence/derive.py`, exact
sympy throughout. Every $\pi$ does cancel ($1 - 2\varkappa = \sqrt3 - 1$ against $\lambda$), giving
$n \le \tfrac{\sqrt3}{6}A + \tfrac14 M + 1$ at separation 2, which rescales to Oler exactly.

I was told to check the direction of every inequality, and the two places it could have gone wrong:

- **The reduction on p. 287** is $\overline F - \varkappa\overline U \le F - \varkappa U$ — the
  functional is *smallest* on the hull, so proving the Satz for $B = C$ gives it for all $B$. Right
  way round; had it been the other way, applying the Satz to $K$ would prove nothing.
- **The rescaling** is a *shrink* by $1/2$ (separation 2 → 1), so $A = 4A'$, $M = 2M'$. The script
  asserts both that this reproduces Oler and that the inverted substitution does **not** — a
  regression guard, so a future flip cannot pass silently. I did not want to rely on my own care
  here, given the repo's history.

Independent corroboration that I did not just algebra-manipulate myself into agreement: the Satz is
**exactly tight** ($\texttt{simplify}(\cdot) = 0$, not small) on triangular-lattice packings for
$k = 1..7$ at Groemer's own scale. That is Groemer's case a) firing where the clause says it should.

## Where I disagreed with the issue

#96 said the reduction is to "Oler's inequality **verbatim**". It is not, quite. Oler's CMB
statement is for an arbitrary **Jordan polygon** $\pi$ with vertices in $E$; $\pi$ need not be
convex. Steiner and $H \oplus B_1$ both need convexity, so what comes out is Oler **specialised to
$\pi = \mathrm{conv}(E)$**. Costs this repo nothing — `oler-lower-bound/` §1.2 says every
application there takes $\pi = H$ — but the gap is real and I did not want it laundered by a word.

## #44

Already closed, and its finding stands: Oler's Acta paper contains no equality characterisation.
That was a correct negative result and I changed nothing about it. What was wrong was the wider
claim §5.2 invited — that the theorem is missing from the *literature*. It is not.

I deliberately did **not** promote (R2). Groemer's case a) gives "hull decomposes into unit
equilateral triangles, all vertices are points of $E$"; getting from there to "$E$ lies in a
triangular lattice" needs two more steps (every point of $E$ is a vertex — circumradius
$1/\sqrt3 < 1$; and edge-to-edge unit-equilateral triangulation ⇒ lattice subset). Both are mine.
Writing them out looked temptingly short, which is precisely why I stopped and isolated them in
§4.3 instead. A one-hour session that ends with a correctly-scoped `sketch` beats one that ends
with a laundered assumption.

## State

Two files corrected (problem README's Groemer section; `oler-lower-bound/` §5.2), one new attack
directory. PR opened, `tier:verification-critical`, review requested from Flow-25. The derivation
is `sketch` and stays `sketch` until a cross-family examiner reconstructs it — which, per §5, is
not something I can grant myself no matter how clean the sympy output looked.
