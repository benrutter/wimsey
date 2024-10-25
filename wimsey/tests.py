from functools import partial
from typing import Any, Callable
from dataclasses import dataclass


@dataclass
class result:
    name: str
    success: bool
    unexpected: Any = None


def _range_check(metric: str) -> Callable:
    """
    Factory function for generated tests of the form "x should be within range"

    Tests are also factories in themselves, they'll generate functions to take
    only a "describe" object.
    """

    def should(
        describe: dict[str, Any],
        column: str,
        be_exactly: float | int | None = None,
        be_less_than: float | int | None = None,
        be_less_than_or_equal_to: float | int | None = None,
        be_greater_than: float | int | None = None,
        be_greater_than_or_equal_to: float | int | None = None,
    ) -> result:
        """
        Test that column mean is within designated range
        """
        checks: list[bool] = []
        value: Any = describe[f"{metric}_{column}"]
        if be_exactly is not None:
            checks.append(value == be_exactly)
        if be_less_than is not None:
            checks.append(value < be_less_than)
        if be_greater_than is not None:
            checks.append(value > be_greater_than)
        if be_less_than_or_equal_to is not None:
            checks.append(value <= be_less_than_or_equal_to)
        if be_greater_than_or_equal_to is not None:
            checks.append(value >= be_greater_than_or_equal_to)
        return result(
            name=f"{metric}-of-{column}",
            success=all(checks),
            unexpected=value if not all(checks) else None,
        )

    def should_be_partial(
        column: str,
        exactly: float | int | None = None,
        less_than: float | int | None = None,
        less_than_or_equal_to: float | int | None = None,
        greater_than: float | int | None = None,
        greater_than_or_equal_to: float | int | None = None,
        **kwargs,
    ) -> Callable:
        return partial(
            should,
            column=column,
            be_exactly=exactly,
            be_less_than=less_than,
            be_less_than_or_equal_to=less_than_or_equal_to,
            be_greater_than=greater_than,
            be_greater_than_or_equal_to=greater_than_or_equal_to,
        )

    return should_be_partial


def columns_should(
    have: list[str] | str | None = None,
    not_have: list[str] | str | None = None,
    be: list[str] | str | None = None,
) -> Callable:
    def should_have(
        description: dict,
        have: list[str] | str | None = None,
        not_have: list[str] | str | None = None,
        be: list[str] | str | None = None,
    ) -> result:
        have = list(have) if isinstance(have, str) else have
        not_have = list(not_have) if isinstance(not_have, str) else not_have
        be = list(be) if isinstance(be, str) else be
        checks: list[bool] = []
        present_columns = description["columns"].split("_^&^_")
        if have is not None:
            for col in have:
                checks.append(col in present_columns)
        if not_have is not None:
            for col in not_have:
                checks.append(col not in present_columns)
        if be is not None:
            checks.append(set(present_columns) == set(be))
            checks.append(len(present_columns) == len(be))
        return result(
            name="columns",
            success=all(checks),
            unexpected=present_columns if not all(checks) else None,
        )

    return partial(should_have, have=have, not_have=not_have, be=be)


possible_tests: dict[str, Callable] = {
    "mean_should": (mean_should := _range_check("mean")),
    "min_should": (min_should := _range_check("min")),
    "max_should": (max_should := _range_check("max")),
    "null_count_should": (null_count_should := _range_check("null_count")),
    "count_should": (count_should := _range_check("count")),
    "null_percentage_should": (
        null_percentage_should := _range_check("null_percentage")
    ),
    "columns_should": columns_should,
}
