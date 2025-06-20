from dataclasses import dataclass


@dataclass
class MagicExpr:
    """
    Special Wimsey object for special data such as column names that aren't possible via
    expressions directly.
    """

    expr_name: str


schema = MagicExpr("schema")
