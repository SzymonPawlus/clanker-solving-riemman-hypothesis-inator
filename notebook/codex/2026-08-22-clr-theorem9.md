# CLR Theorem 9 source check

Issue: #92

I checked the open-access version of record of Cornuéjols--Liu--Ravi,
*Approximately Packing Dijoins via Nowhere-Zero Flows*, Combinatorica 45
(2025), article 32, DOI 10.1007/s00493-025-00159-x.

The discrepancy is real:

- Theorem 9 is attributed to reference [25] (Schrijver's unpublished note)
  and states the strengthening reformulation of Woodall's conjecture.  The
  paper gives no proof of Theorem 9.
- The paper later says its proof of Theorem 11 is inspired by Schrijver's
  Theorem 9.
- Lemma 2 is the structural lemma stated for a digraph with
  `w in {0,1}^A`; it is immediately followed by, and used in, the proof of
  Theorem 10.
- Independently of that lemma, the introduction explicitly warns that
  weight-zero arcs cannot be removed because zero- and one-weight arcs
  together determine the dicuts.

Therefore the Schrijver-filter conclusion in `tau2-robbins/README.md` remains
supported, but its theorem-level locator was wrong.  I changed the locator to
the introduction, Lemma 2, and the proof of Theorem 10, and explicitly noted
what Theorem 9 actually is.

This is verification-critical literature work.  The source correction must
be independently reviewed by Claude or a human before it can earn
`verified:review` or be used as an independently verified claim.
