"""Exact-arithmetic checker for circle-packing certificates.

See `problems/circle-packing-equilateral-triangle/README.md` for the definition of
what a valid packing is. This package only *implements* that check; it is not the
definition.
"""

from .checker import CertificateError, CheckResult, check_certificate, check_file

__all__ = ["CertificateError", "CheckResult", "check_certificate", "check_file"]
