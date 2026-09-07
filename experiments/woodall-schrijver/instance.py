"""Schrijver's counterexample to the Edmonds-Giles conjecture, as an explicit
{0,1}-weighted digraph.

Transcribed 2026-09-04 from two independent published drawings of the same
instance (see ../../problems/woodalls-conjecture/attacks/schrijver-instance/README.md
for the provenance and the exact locators):

  [ACZ]  A. Abdi, G. Cornuejols, M. Zlatin, "On packing dijoins in digraphs and
         weighted digraphs", arXiv:2202.00392v5, Figure 1 (source file
         `figures/D1.pdf`, read as vector path data, not by eye).
  [HZ]   arXiv:2501.10918v2, "A Min-Max Relation on Dicuts and Dijoins in
         Weighted Chordal Digraphs", Figure 1 left panel (`Younger-3+5.jpg`),
         which carries the arc labels 1,1',1'',2,2',2'',3,3',3''.

The two drawings agree arc-for-arc.  NOTE: this is a transcription of a
*secondary* rendering.  Schrijver, Discrete Math. 32 (1980) 213-214, the
primary source, was NOT read (Elsevier paywall).

Layout.  Twelve vertices: an outer hexagon TL,TR,R,BR,BL,L (clockwise from top
left) and an inner hexagon tl,tr,r,br,bl,l in the same cyclic positions.
Twenty-one arcs:

  * 3 solid outer-hexagon arcs, 3 solid inner-hexagon arcs, 3 solid "long"
    arcs from an inner vertex to a non-corresponding outer vertex  (weight 1)
  * 3 dashed outer-hexagon arcs, 3 dashed inner-hexagon arcs,
    6 dashed radial spokes (inner -> outer)                        (weight 0)

The instance has an order-3 rotational automorphism
  TL->R->BL->TL, TR->BR->L->TR, tl->r->bl->tl, tr->br->l->tr
which maps arc family 1 -> 2 -> 3 -> 1.
"""

VERTICES = ("TL", "TR", "R", "BR", "BL", "L", "tl", "tr", "r", "br", "bl", "l")

# (tail, head, weight, label-in-[HZ] or "" for the unlabelled weight-0 arcs)
ARCS = (
    # --- weight 1 (drawn solid) -------------------------------------------
    ("l", "TL", 1, "1"),
    ("TR", "TL", 1, "1'"),
    ("l", "bl", 1, "1''"),
    ("tr", "R", 1, "2"),
    ("BR", "R", 1, "2'"),
    ("tr", "tl", 1, "2''"),
    ("br", "BL", 1, "3"),
    ("L", "BL", 1, "3'"),
    ("br", "r", 1, "3''"),
    # --- weight 0 (drawn dashed) ------------------------------------------
    ("L", "TL", 0, ""),      # outer hexagon
    ("TR", "R", 0, ""),      # outer hexagon
    ("BR", "BL", 0, ""),     # outer hexagon
    ("l", "tl", 0, ""),      # inner hexagon
    ("tr", "r", 0, ""),      # inner hexagon
    ("br", "bl", 0, ""),     # inner hexagon
    ("tl", "TL", 0, ""),     # spoke
    ("tr", "TR", 0, ""),     # spoke
    ("r", "R", 0, ""),       # spoke
    ("br", "BR", 0, ""),     # spoke
    ("bl", "BL", 0, ""),     # spoke
    ("l", "L", 0, ""),       # spoke
)

SCHRIJVER = (VERTICES, tuple((t, h, w) for (t, h, w, _) in ARCS))


def rotation(v):
    """The order-3 automorphism, used only as a self-check on the transcription."""
    return {"TL": "R", "R": "BL", "BL": "TL",
            "TR": "BR", "BR": "L", "L": "TR",
            "tl": "r", "r": "bl", "bl": "tl",
            "tr": "br", "br": "l", "l": "tr"}[v]
