"""Types (mostly data based) for use in Wimsey module."""

from dataclasses import dataclass
from typing import Any, Callable, TypeAlias

import narwhals.stable.v1 as nw


@dataclass
class MagicExpr:
    """Type for use in place of nw.Expr.

    Special Wimsey object for special data such as column names that aren't
    possible via expressions directly.
    """

    expr_name: str


schema = MagicExpr("schema")


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


GeneratedTest: TypeAlias = tuple[nw.Expr | MagicExpr, Callable[[Any], Result]]
