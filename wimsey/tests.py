from functools import partial
from typing import Any, Callable, TypeAlias
from dataclasses import dataclass


import narwhals.stable.v1 as nw

# TODO: just missing some slightly complex tests that use dtypes or column names


@dataclass
class Result:
    name: str
    success: bool
    unexpected: Any = None


GeneratedTest: TypeAlias = tuple[nw.Expr, Callable[[Any], Result]]


def _range_check(aggregation: Callable[[str], nw.Expr], metric_name: str) -> Callable:
    """
    Factory function for generated tests of the form "x should be within range"

    Tests are also factories in themselves, they'll generate functions to take
    only a "describe" object.
    """

    def check_aggregation_is_in_range(
        column: str,
        be_exactly: float | int | None = None,
        be_less_than: float | int | None = None,
        be_less_than_or_equal_to: float | int | None = None,
        be_greater_than: float | int | None = None,
        be_greater_than_or_equal_to: float | int | None = None,
        **kwargs,
    ) -> GeneratedTest:
        """Test that column metric is within designated range"""

        def _check(value: int | float) -> Result:
            checks = []
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
            return Result(
                name=f"{metric_name}-of-{column}",
                success=all(checks),
                unexpected=value if not all(checks) else None,
            )

        return aggregation(column), _check

    return check_aggregation_is_in_range


def row_count_should(
    be_less_than: float | int | None = None,
    be_less_than_or_equal_to: float | int | None = None,
    be_greater_than: float | int | None = None,
    be_greater_than_or_equal_to: float | int | None = None,
    be_exactly: float | int | None = None,
    **kwargs,
) -> GeneratedTest:
    """Test that dataframe row count is within designated range"""

    def _check(value: int | float) -> Result:
        """Test that dataframe row count is within designated range"""
        checks: list[bool] = []
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
        return Result(
            name="row-count",
            success=all(checks),
            unexpected=value if not all(checks) else None,
        )

    return nw.len(), _check


def average_difference_from_other_column_should(
    column: str,
    other_column: str,
    be_exactly: float | int | None = None,
    be_less_than: float | int | None = None,
    be_less_than_or_equal_to: float | int | None = None,
    be_greater_than: float | int | None = None,
    be_greater_than_or_equal_to: float | int | None = None,
    **kwargs,
) -> Callable:
    """
    Test that the average difference between column and other column are
    within designated bounds.
    """

    def _check(difference: float | int) -> Result:
        """
        Test that the average difference between column and other column are
        within designated bounds.
        """
        checks: list[bool] = []
        if be_exactly is not None:
            checks.append(difference == be_exactly)
        if be_less_than is not None:
            checks.append(difference < be_less_than)
        if be_less_than_or_equal_to is not None:
            checks.append(difference <= be_less_than_or_equal_to)
        if be_greater_than is not None:
            checks.append(difference > be_greater_than)
        if be_greater_than_or_equal_to is not None:
            checks.append(difference >= be_greater_than_or_equal_to)
        return Result(
            name=f"average-difference-from-{column}-to-{other_column}",
            success=all(checks),
            unexpected=difference if not all(checks) else None,
        )

    return (nw.col(column) - nw.col(other_column)).mean(), _check


def average_ratio_to_other_column_should(
    column: str,
    other_column: str,
    be_exactly: float | int | None = None,
    be_less_than: float | int | None = None,
    be_less_than_or_equal_to: float | int | None = None,
    be_greater_than: float | int | None = None,
    be_greater_than_or_equal_to: float | int | None = None,
    **kwargs,
) -> Callable:
    """
    Test that the average ratio between column and other column are
    within designated bounds (for instance, a value of 1 has a ratio
    of 0.1 to a value of 10)
    """

    def _check(ratio: float | int) -> Result:
        """
        Test that the average ratio between column and other column are
        within designated bounds (for instance, a value of 1 has a ratio
        of 0.1 to a value of 10)
        """
        checks: list[bool] = []
        if be_exactly is not None:
            checks.append(ratio == be_exactly)
        if be_less_than is not None:
            checks.append(ratio < be_less_than)
        if be_less_than_or_equal_to is not None:
            checks.append(ratio <= be_less_than_or_equal_to)
        if be_greater_than is not None:
            checks.append(ratio > be_greater_than)
        if be_greater_than_or_equal_to is not None:
            checks.append(ratio >= be_greater_than_or_equal_to)
        return Result(
            name=f"average-ratio-between-{column}-and-{other_column}",
            success=all(checks),
            unexpected=ratio if not all(checks) else None,
        )

    return nw.col(column) / nw.col(other_column).mean(), _check


def max_string_length_should(
    column: str,
    be_less_than: int | float | None = None,
    be_greater_than: int | float | None = None,
    be_exactly: int | float | None = None,
    **kwargs,
) -> Callable:
    def _check(success: bool) -> Result:
        return Result(
            name=f"max-string-length-of-{column}",
            success=success,
            unexpected=None
            if success
            else "Length of column values did not meet bounds",
        )

    expressions: list[nw.Expr] = []
    if be_less_than:
        expr: nw.Expr = nw.col(column).str.len_chars().max() < nw.lit(be_less_than)
        expressions.append(expr)
    if be_greater_than:
        expr: nw.Expr = nw.col(column).str.len_chars().max() > nw.lit(be_greater_than)
        expressions.append(expr)
    if be_exactly:
        expr: nw.Expr = nw.col(column).str.len_chars().max() == nw.lit(be_exactly)
        expressions.append(expr)
    return nw.all_horizontal(*expressions), _check


def all_values_should(
    column: str,
    be_one_of: list[str] | None = None,
    not_be_one_of: list[str] | None = None,
    match_regex: str | None = None,
    **kwargs,
) -> None:
    def _check(
        success,
    ) -> Result:
        return Result(
            name=f"all-values-of-{column}",
            success=success,
            unexpected=None if success else "Values did not meet given conditions",
        )

    expressions: list[nw.Expr] = []
    if be_one_of:
        expressions.append(nw.col(column).is_in(be_one_of).min())
    if not_be_one_of:
        expressions.append(~(nw.col(column).is_in(not_be_one_of)).max())
    if match_regex:
        expressions.append(nw.col(column).str.contains(match_regex))
    return nw.all_horizontal(*expressions), _check


possible_tests: dict[str, Callable] = {
    "mean_should": (mean_should := _range_check(nw.mean, "mean")),
    "min_should": (min_should := _range_check(nw.min, "min")),
    "max_should": (max_should := _range_check(nw.max, "max")),
    "std_should": (std_should := _range_check(lambda col: col.std(), "stdev")),
    "count_should": (count_should := _range_check(lambda col: col.count(), "count")),
    "row_count_should": row_count_should,
    "average_difference_from_other_column_should": average_difference_from_other_column_should,
    "average_ratio_to_other_column_should": average_ratio_to_other_column_should,
    "max_string_length_should": max_string_length_should,
    "all_values_should": all_values_should,
}
