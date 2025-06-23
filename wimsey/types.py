from dataclasses import dataclass
from typing import TypeAlias, Any, Callable

import narwhals.stable.v1 as nw


@dataclass
class MagicExpr:
    """
    Special Wimsey object for special data such as column names that aren't possible via
    expressions directly.
    """

    expr_name: str


schema = MagicExpr("schema")


@dataclass
class Result:
    name: str
    success: bool
    unexpected: Any = None


GeneratedTest: TypeAlias = tuple[nw.Expr | MagicExpr, Callable[[Any], Result]]
