"""Types (mostly data based) for use in Wimsey module."""

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, TypeAlias

import narwhals as nw_unstable
import narwhals.stable.v1 as nw_1
import narwhals.stable.v2 as nw_2


@dataclass
class _MagicExpr:
    """Type for use in place of nw.Expr.

    Special Wimsey object for special data such as column names that aren't
    possible via expressions directly.
    """

    expr_name: str


_schema = _MagicExpr("schema")


class DataValidationError(Exception):
    """Exception class for raising against invalid data."""


@dataclass
class Result:
    """Dataclass for storing test result information."""

    name: str
    success: bool
    unexpected: Any = None


@dataclass
class FinalResult:
    """Dataclass for storing test result information."""

    success: bool
    results: list[Result]


NwExpr: TypeAlias = nw_unstable.Expr | nw_1.Expr | nw_2.Expr

GeneratedTest: TypeAlias = tuple[NwExpr | _MagicExpr, Callable[[Any], Result]]
