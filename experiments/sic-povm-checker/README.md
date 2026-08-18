# Exact SIC-family checker, certificate version 1

Status: tooling / `numerical`. Acceptance by this author-written checker does not
grant a verified claim. Issue: #67, parent program #65.

The checker verifies the finite vector-family definition: a dimension `d`
certificate contains exactly `d^2` normalized vectors in `C^d`, and every
distinct squared overlap is exactly `1/(d+1)`. If `povm_weights` is supplied, it
also verifies that the weighted rank-one projectors sum exactly to the identity.

Version 1 deliberately supports only `1 <= d <= 3` and the fixed field
`Q(sqrt(2),sqrt(3),i)`. A scalar is an array of eight bounded rational strings in
the basis

```text
[1, sqrt(2), sqrt(3), sqrt(6), i, i*sqrt(2), i*sqrt(3), i*sqrt(6)].
```

Only canonical integer and fraction strings are accepted. Decimal strings,
expressions, floats, duplicate JSON keys, unknown fields, oversized files and
oversized integers are rejected. No evaluator or general symbolic parser exists.

Required top-level fields are `certificate_version: 1`, `claim: "sic-family"`,
`status: "numerical"`, `dimension`, `field`, and `vectors`. The optional
`povm_weights` list has exactly `d^2` nonnegative rational scalars (encoded in
the same eight-slot basis). Restricting weights to rationals avoids pretending
that arbitrary complex coefficients define positive POVM effects.

Run:

```bash
python3 -m unittest discover -s tests -v
python3 siccheck.py certificate.json
```

The tests independently spell out tetrahedral (`d=2`) and Hesse (`d=3`) vector
families and include parser, resource, geometry, overlap and completeness negative
controls. Durable fixture files belong to child issue #68, not this checker.
