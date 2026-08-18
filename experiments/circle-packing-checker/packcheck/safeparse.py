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
exponent magnitude and the size of any intermediate rational, so a malformed
certificate fails fast instead of exhausting memory.
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
    "MAX_VALUE_BITS",
]

# Resource bounds. Generous next to any real certificate: the coordinates in this
# problem are short expressions over small integers and a couple of square roots.
MAX_SOURCE_LENGTH = 4096
MAX_NODES = 512
MAX_EXPONENT = 10_000
# 8192 bits is about 2,466 decimal digits: far more than any coordinate in this
# problem needs, and deliberately under CPython's 4,300-digit int-to-str limit, so
# every value that gets past the parser can still be rendered in a failure message.
MAX_VALUE_BITS = 1 << 13

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
    return _evaluate(tree.body)


# --------------------------------------------------------------------------- #
# The interpreter. Anything not handled explicitly is rejected.
# --------------------------------------------------------------------------- #

def _evaluate(node: ast.AST) -> sympy.Expr:
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
    if isinstance(op, ast.Add):
        return _bounded(left + right)
    if isinstance(op, ast.Sub):
        return _bounded(left - right)
    if isinstance(op, ast.Mult):
        return _bounded(left * right)
    if isinstance(op, ast.Div):
        if right == 0:
            raise UnsafeExpression("division by zero")
        return _bounded(left / right)
    if isinstance(op, ast.Pow):
        return _bounded(_power(left, right))
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
    if abs(p) > MAX_EXPONENT or q > MAX_EXPONENT:
        raise UnsafeExpression(
            f"exponent {sympy.sstr(exponent)} exceeds the {MAX_EXPONENT} limit"
        )
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


def _bounded(expr: sympy.Expr) -> sympy.Expr:
    """Pass `expr` through, rejecting a rational that has grown past the size limit.

    Applied to every intermediate, so repeated squaring cannot escape the bound.
    """
    if expr.is_Rational:
        if max(abs(int(expr.p)), int(expr.q)).bit_length() > MAX_VALUE_BITS:
            raise UnsafeExpression(
                f"intermediate value exceeds the {MAX_VALUE_BITS}-bit limit"
            )
    return expr
