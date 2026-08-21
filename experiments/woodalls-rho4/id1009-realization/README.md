# Exact ACZ realization of ID1009

Status: `numerical`, submitted for independent review in issue #88.

The 16 sink supports

```text
018 018 08B 08B 119 22B 236 245
33B 357 44A 467 559 66A 779 9AA
```

give every source `0,...,B` degree four. For a source shore `X`, let `y(X)` be
the number of sink supports contained in `X`. The checker exhausts all 4,094
nonempty proper shores, verifies

```text
4|X| - 3y(X) >= 3,
```

and finds equality only at `X=2345679AB`. It then checks all 70 active
four-subsets against the exact M1 rule

```text
|Q intersect X| >= 1 + y(X) - |X|
```

for every proper shore. The resulting 32 bases are exactly catalogue entry
`1009_8_4_32`.

Run:

```bash
python experiments/woodalls-rho4/id1009-realization/verify.py
```

The committed [`output.json`](output.json) is the expected deterministic output.

## Consequence and scope

ID1009 is the concrete rank-four Hall obstruction used in issue #88. This
certificate proves that it is realizable as an ACZ M1 restriction at
`tau=3, rho=4`. It refutes the attempted routes “every ACZ M1 restriction is
strongly base orderable” and “ID1009 is globally nonrealizable.” It does **not**
refute Woodall's conjecture or the full tau-three partition conclusion.

The JSON-sink digest in the certificate hashes the ordered JSON array of integer
triples and is
`619d9a5d6cc817715cb16d3be275f2a9fc66994bf4a69e826cb6c729a6f4d52f`.
An independent prover audit used a different canonical-support serialization,
giving `34d89be3f72b69ea77884286dc0958a0f41ecebda804a9dbf10c51e7868f514f`,
and hashed its larger audit payload as
`8163656d896268ee3b3f4e2282646bf150a1b852092d7632f2aae092a2ad21c7`.
These digest values are intentionally not interchangeable.

## Mandatory Woodall filters

- **Schrijver:** passed. The consequence is only for the unweighted ACZ M1
  setting; it does not assert the false weighted Edmonds--Giles statement.
- **Lucchesi--Younger:** passed. No dicut/dijoin duality is used.
- **Easy direction:** passed. This is a finite M1-realizability certificate, not
  a claim that the trivial upper bound supplies a dijoin packing.
