"""Parsing certificate scalars from UNTRUSTED text, with no evaluation of Python.

Why this module exists
----------------------
A certificate is a JSON file that arrives from somewhere else -- another agent, a
pull request, a paper's supplementary material. Its scalar fields are strings like
`"4 + 2*sqrt(3)"`, and the obvious way to turn one into an exact number is sympy's
`parse_expr`. That is unsafe: `parse_expr` tokenises the text and then *evaluates*
it as Python with the default globals, so a certificate containing

    open('/tmp/proof','w').write('executed')

runs that call. The file is written before the checker ever gets to decide the
certificate is malformed, so rejecting afterwards is too late. Review of PR #16
demonstrated exactly this.

The fix is not to filter the input and keep evaluating it -- a denylist of dangerous
spellings is a losing game -- but to remove evaluation from the path entirely.

How this module is safe
-----------------------
`ast.parse(text, mode="eval")` builds a syntax tree without executing anything, and
in `eval` mode it rejects statements (imports, assignments, `exec`) at parse time.
The tree is then walked by `_evaluate` below, which is an interpreter for a grammar
of exactly:

    integer literals, unary + -, binary + - * / **, parentheses,
    and calls to the allowlisted radicals in `_ALLOWED_CALLS`

Every other node type -- `Name`, `Attribute`, `Subscript`, `Lambda`, `ListComp`,
`JoinedStr`, comparisons, boolean and bitwise operators -- falls through to a raise.
There is no `eval`, `exec`, `compile` or `getattr` in this module, so builtins,
attribute access and imports are not merely filtered: there is no code path that
could reach them. Rejection therefore happens *before* any side effect, because
nothing in the input is ever run.

Floats are refused rather than converted. `"10.928"` is exactly the rational
1366/125, so it parses in principle, but the problem's `RULES.md` §2 bans decimal
strings in exact fields precisely because such a value is nearly always truncated
optimiser output wearing an exact value's clothes.

Resource limits
---------------
An allowlisted grammar still lets a hostile certificate ask for a very expensive
number -- `10**10**9` is three tokens. The bounds below cap input size, tree size,
exponent magnitude and the size of any rational, so a malformed certificate fails
fast instead of exhausting memory.

**These are invariants of the value returned, not checks on individual operations.**
The re-review of PR #16 showed why that distinction is the whole guard. Checking only
the exponent syntax being evaluated lets composition escape the cap, because sympy
*simplifies* as it builds:

    (2**(1/10000))**(1/10000)  ->  2**(1/100000000)
    sqrt(sqrt(...sqrt(2)...))  ->  2**(1/1048576)      (20 nested calls, 121 chars)

Each individual exponent was in range; the combined one was not. A root index that
large is not a parser curiosity -- `exact.enclose` computes `scale**q` to bound a
`q`-th root, so such a coordinate turns a 121-character certificate into an
out-of-memory or non-terminating CLI run. Measured on this branch before the fix, a
depth-20 nest under a 256 MiB cap did not finish in 4 s; depth 11 (`q = 2048`, well
inside the old cap of 10,000) took 28 s.

So `_validated` below walks the *simplified* sympy expression after every step and
enforces:

  * every `Rational` (this includes plain integers) fits in `MAX_VALUE_BITS` bits;
  * every surviving `Pow` has a rational exponent `p/q` with `|p| <= MAX_EXPONENT`
    and `q <= MAX_ROOT_INDEX`;
  * the expression tree has at most `MAX_RESULT_NODES` nodes.

Because it runs bottom-up on every intermediate, the first step that breaks the
invariant is the one that is rejected -- nothing expensive is built on top of it.
A rational never survives as a `Pow` (sympy folds `1/10**60` into a single
`Rational`), so `MAX_EXPONENT` constrains only the radicals, which are the terms
that are genuinely expensive downstream.
"""

from __future__ import annotations

import ast

import sympy

__all__ = [
    "UnsafeExpression",
    "parse_scalar",
    "ALLOWED_FUNCTIONS",
    "MAX_SOURCE_LENGTH",
    "MAX_NODES",
    "MAX_EXPONENT",
    "MAX_ROOT_INDEX",
    "MAX_VALUE_BITS",
    "MAX_RESULT_NODES",
]

# Resource bounds. Generous next to any real certificate: the coordinates in this
# problem are short expressions over small integers and a couple of square roots.
MAX_SOURCE_LENGTH = 4096
MAX_NODES = 512

# Exponent bounds, applied to the *simplified* expression (see `_validated`).
#
# `MAX_ROOT_INDEX` is the algebraic degree the checker is willing to reason about.
# It is the load-bearing one: `exact.enclose` bounds a `q`-th root by computing
# `scale**q` with `scale = 1 << (bits + 8)`, and `is_exactly_zero` computes a
# minimal polynomial of degree `q`, so cost grows superlinearly in `q`. Measured
# end-to-end through the CLI on the n=3 fixture with one coordinate replaced by a
# nest of square roots: q=64 -> 0.53 s, q=256 -> 0.71 s, q=512 -> 1.2 s,
# q=1024 -> 6.0 s, q=2048 -> 28 s, q=4096 -> did not finish in 100 s. 256 keeps the
# whole run inside a second while leaving room for two orders of magnitude more
# degree than a real certificate (square and cube roots) ever asks for.
MAX_ROOT_INDEX = 256
# `MAX_EXPONENT` bounds the numerator. It bites only on radicals, because sympy
# folds a rational power of a rational base into a single `Rational` -- `1/10**60`
# arrives here as one atom, bounded by `MAX_VALUE_BITS` instead. Measured the same
# way, `(1+sqrt(2))**p` costs 0.56 s at p=100, 15 s at p=1000, and did not finish in
# 60 s at p=10000.
MAX_EXPONENT = 128
# 8192 bits is about 2,466 decimal digits: far more than any coordinate in this
# problem needs, and deliberately under CPython's 4,300-digit int-to-str limit, so
# every value that gets past the parser can still be rendered in a failure message.
MAX_VALUE_BITS = 1 << 13
# The simplified expression may not have more nodes than the source could name.
# `MAX_NODES` bounds the syntax tree; this bounds what sympy expanded it into, so a
# short source cannot hand the checker a large tree to walk.
MAX_RESULT_NODES = 512

# The only names a certificate may mention at all. Radicals with a non-square index
# are written as rational powers (`5**(1/3)`), which the grammar already covers.
_ALLOWED_CALLS = {"sqrt": sympy.sqrt}

ALLOWED_FUNCTIONS = frozenset(_ALLOWED_CALLS)


class UnsafeExpression(Exception):
    """The text is not in the allowlisted certificate grammar, so it was not parsed."""


def parse_scalar(text: str) -> sympy.Expr:
    """Exact sympy number for `text`, or `UnsafeExpression`. Nothing is executed."""
    if not isinstance(text, str):
        raise UnsafeExpression(f"expected a string, got {type(text).__name__}")
    if len(text) > MAX_SOURCE_LENGTH:
        raise UnsafeExpression(
            f"expression is {len(text)} characters, over the {MAX_SOURCE_LENGTH} limit"
        )
    try:
        tree = ast.parse(text, mode="eval")
    except (SyntaxError, ValueError) as exc:
        # `mode="eval"` also rejects statements here -- `import os` is a SyntaxError.
        raise UnsafeExpression(f"not a well-formed arithmetic expression: {exc}") from exc
    node_count = sum(1 for _ in ast.walk(tree))
    if node_count > MAX_NODES:
        raise UnsafeExpression(
            f"expression has {node_count} syntax nodes, over the {MAX_NODES} limit"
        )
    try:
        return _evaluate(tree.body)
    except UnsafeExpression:
        raise
    except RecursionError as exc:
        raise UnsafeExpression("expression is nested too deeply to evaluate") from exc
    except (MemoryError, OverflowError, ArithmeticError, ValueError) as exc:
        # The bounds below are meant to reject a hostile expression before it costs
        # anything, but a caller must never see a raw `MemoryError` escape from
        # parsing untrusted text: the contract of this module is that bad input
        # comes back as `UnsafeExpression`, which `checker.parse_exact` turns into a
        # `CertificateError` and the CLI reports as REJECT.
        raise UnsafeExpression(
            f"evaluating this expression exhausted a resource limit "
            f"({type(exc).__name__}); it is rejected rather than computed"
        ) from exc


# --------------------------------------------------------------------------- #
# The interpreter. Anything not handled explicitly is rejected.
# --------------------------------------------------------------------------- #

def _evaluate(node: ast.AST) -> sympy.Expr:
    """Evaluate one node and check the resource invariants on the *result*.

    Validating here, rather than at each operator, is what closes the composition
    hole: `_dispatch` may hand back something sympy simplified into a shape no
    individual check saw, and every such shape passes through this one funnel.
    Running bottom-up means the offending step is rejected before anything is built
    on top of it.
    """
    return _validated(_dispatch(node))


def _dispatch(node: ast.AST) -> sympy.Expr:
    if isinstance(node, ast.Constant):
        return _constant(node)
    if isinstance(node, ast.UnaryOp):
        return _unary(node)
    if isinstance(node, ast.BinOp):
        return _binary(node)
    if isinstance(node, ast.Call):
        return _call(node)
    raise UnsafeExpression(
        f"{type(node).__name__} is not allowed in a certificate scalar; the grammar is "
        "integers, + - * / **, parentheses and "
        f"{sorted(ALLOWED_FUNCTIONS)}"
    )


def _constant(node: ast.Constant) -> sympy.Expr:
    value = node.value
    if isinstance(value, float) or isinstance(value, complex):
        raise UnsafeExpression(
            f"decimal literal {value!r}: decimal strings are banned in exact fields "
            "(problem RULES.md §2), because they are almost always truncated optimiser "
            'output. Write the exact expression, e.g. "1366/125" for 10.928'
        )
    if isinstance(value, bool) or not isinstance(value, int):
        raise UnsafeExpression(f"{value!r} is not an integer literal")
    # Bounded like every other value. A literal used to be the one way into the
    # expression that skipped the size check, so `9`*3000 was accepted as a
    # 9,966-bit integer despite the 8,192-bit cap. `_evaluate` would catch it now
    # anyway; checking here keeps the reason specific.
    if value.bit_length() > MAX_VALUE_BITS:
        raise UnsafeExpression(
            f"integer literal of {value.bit_length()} bits exceeds the "
            f"{MAX_VALUE_BITS}-bit limit"
        )
    return sympy.Integer(value)


def _unary(node: ast.UnaryOp) -> sympy.Expr:
    if isinstance(node.op, ast.UAdd):
        return _evaluate(node.operand)
    if isinstance(node.op, ast.USub):
        return -_evaluate(node.operand)
    raise UnsafeExpression(f"unary {type(node.op).__name__} is not allowed")


def _binary(node: ast.BinOp) -> sympy.Expr:
    left = _evaluate(node.left)
    right = _evaluate(node.right)
    op = node.op
    # No result checks here: `_evaluate` validates whatever comes back, so a value
    # that grew past a bound during simplification is caught even when the operator
    # that produced it had no way to see it coming.
    if isinstance(op, ast.Add):
        return left + right
    if isinstance(op, ast.Sub):
        return left - right
    if isinstance(op, ast.Mult):
        return left * right
    if isinstance(op, ast.Div):
        if right == 0:
            raise UnsafeExpression("division by zero")
        return left / right
    if isinstance(op, ast.Pow):
        return _power(left, right)
    raise UnsafeExpression(
        f"operator {type(op).__name__} is not allowed; the grammar is + - * / **"
    )


def _call(node: ast.Call) -> sympy.Expr:
    func = node.func
    if not isinstance(func, ast.Name):
        # Blocks `os.system(...)`, `f()()`, `(lambda: x)()` and every other form
        # where the thing being called is computed rather than named.
        raise UnsafeExpression(
            "only a plain call to an allowlisted function is permitted; "
            f"allowed: {sorted(ALLOWED_FUNCTIONS)}"
        )
    if func.id not in _ALLOWED_CALLS:
        raise UnsafeExpression(
            f"{func.id!r} is not an allowed function; allowed: {sorted(ALLOWED_FUNCTIONS)}"
        )
    if node.keywords:
        raise UnsafeExpression(f"{func.id}() takes no keyword arguments")
    if len(node.args) != 1 or isinstance(node.args[0], ast.Starred):
        raise UnsafeExpression(f"{func.id}() takes exactly one positional argument")
    return _ALLOWED_CALLS[func.id](_evaluate(node.args[0]))


# --------------------------------------------------------------------------- #
# Resource bounds
# --------------------------------------------------------------------------- #

def _power(base: sympy.Expr, exponent: sympy.Expr) -> sympy.Expr:
    """`base ** exponent`, refusing exponents that are irrational or expensive."""
    if not exponent.is_Rational:
        raise UnsafeExpression(f"exponent {sympy.sstr(exponent)} is not rational")
    p, q = int(exponent.p), int(exponent.q)
    # A pre-check, not the guarantee. `_validated` enforces the same two caps on the
    # simplified result; this only stops sympy from *materialising* something absurd
    # (`sqrt(2)**10**9` evaluates eagerly to a half-billion-bit integer) on the way
    # there. Both checks are needed: this one cannot see composition, and the other
    # runs too late to prevent the work.
    _check_exponent(p, q, f"exponent {sympy.sstr(exponent)}")
    if base == 0 and p < 0:
        raise UnsafeExpression("division by zero: 0 raised to a negative power")
    if base.is_Rational:
        # Bound the result before computing it: `10**10000` is cheap to write and
        # expensive to materialise.
        magnitude = max(abs(int(base.p)), int(base.q)).bit_length()
        if magnitude * abs(p) > MAX_VALUE_BITS:
            # The base itself may be far too large to render, so report sizes only.
            raise UnsafeExpression(
                f"a {magnitude}-bit base raised to the power {sympy.sstr(exponent)} "
                f"would exceed the {MAX_VALUE_BITS}-bit intermediate limit"
            )
    return base**exponent


def _check_exponent(p: int, q: int, what: str) -> None:
    """Reject a rational exponent `p/q` outside the caps."""
    if abs(p) > MAX_EXPONENT:
        raise UnsafeExpression(
            f"{what} has numerator {p}, over the {MAX_EXPONENT} limit"
        )
    if q > MAX_ROOT_INDEX:
        raise UnsafeExpression(
            f"{what} is a root of index {q}, over the {MAX_ROOT_INDEX} limit; "
            "bounding such a root exactly costs more than this checker will spend"
        )


def _validated(expr: sympy.Expr) -> sympy.Expr:
    """Enforce the resource bounds on `expr` as it actually is, post-simplification.

    This is the guarantee the rest of the module rests on: whatever `parse_scalar`
    returns satisfies these bounds, regardless of which sequence of individually
    legal operations produced it. Checking the operations alone is not enough,
    because sympy rewrites as it builds -- `sqrt(sqrt(2))` is not two square roots
    to the checker downstream, it is `2**(1/4)`, and twenty of them are `2**(1/2**20)`.
    """
    nodes = 0
    for sub in sympy.preorder_traversal(expr):
        nodes += 1
        if nodes > MAX_RESULT_NODES:
            raise UnsafeExpression(
                f"the simplified expression has more than {MAX_RESULT_NODES} nodes"
            )
        if sub.is_Float:
            # Not reachable from the grammar, which has no float literal; a second
            # gate so that no future rewrite can leak inexact arithmetic in here.
            raise UnsafeExpression(f"floating-point value {sub} in an exact field")
        if sub.is_Rational:
            bits = max(abs(int(sub.p)), int(sub.q)).bit_length()
            if bits > MAX_VALUE_BITS:
                # The value may be far too large to render, so report the size only.
                raise UnsafeExpression(
                    f"a {bits}-bit rational exceeds the {MAX_VALUE_BITS}-bit limit"
                )
        elif sub.is_Pow:
            exponent = sub.exp
            if not exponent.is_Rational:
                raise UnsafeExpression(
                    f"exponent {sympy.sstr(exponent)} is not rational"
                )
            _check_exponent(
                int(exponent.p),
                int(exponent.q),
                f"the simplified exponent {sympy.sstr(exponent)}",
            )
    return expr
