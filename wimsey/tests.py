"""Wimsey test definitions.

Definitions for test functions that can be ran against a dataframe.
"""

from __future__ import annotations

from typing import Any, Callable

import narwhals.stable.v1 as nw

from wimsey.types import GeneratedTest, Result, schema


def _range_check(
    aggregation: Callable[[str], nw.Expr],
    metric_name: str,
) -> Callable:
    """Generate tests of the form "x should be within range".

    Tests are also factories in themselves, they'll generate functions to take
    only a "describe" object.
    """

    def check_aggregation_is_in_range(
        column: str,
        be_exactly: float | None = None,
        be_less_than: float | None = None,
        be_less_than_or_equal_to: float | None = None,
        be_greater_than: float | None = None,
        be_greater_than_or_equal_to: float | None = None,
        **kwargs: Any,
    ) -> GeneratedTest:
        """Test that column metric is within designated range."""
        del kwargs

        def _check(value: float) -> Result:
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
    be_less_than: float | None = None,
    be_less_than_or_equal_to: float | None = None,
    be_greater_than: float | None = None,
    be_greater_than_or_equal_to: float | None = None,
    be_exactly: float | None = None,
    **kwargs: Any,
) -> GeneratedTest:
    """Test that dataframe row count is within designated range."""
    del kwargs

    def _check(value: float) -> Result:
        """Test that dataframe row count is within designated range."""
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
    be_exactly: float | None = None,
    be_less_than: float | None = None,
    be_less_than_or_equal_to: float | None = None,
    be_greater_than: float | None = None,
    be_greater_than_or_equal_to: float | None = None,
    **kwargs: Any,
) -> GeneratedTest:
    """Compare difference between two columns.

    Test that the average difference between column and other column are
    within designated bounds.
    """
    del kwargs

    def _check(difference: float) -> Result:
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
    be_exactly: float | None = None,
    be_less_than: float | None = None,
    be_less_than_or_equal_to: float | None = None,
    be_greater_than: float | None = None,
    be_greater_than_or_equal_to: float | None = None,
    **kwargs: Any,
) -> GeneratedTest:
    """Compare ratio between two columns.

    Test that the average ratio between column and other column are
    within designated bounds (for instance, a value of 1 has a ratio
    of 0.1 to a value of 10).
    """
    del kwargs

    def _check(ratio: float) -> Result:
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

    return (nw.col(column) / nw.col(other_column)).mean(), _check


def max_string_length_should(
    column: str,
    be_exactly: float | None = None,
    be_less_than: float | None = None,
    be_less_than_or_equal_to: float | None = None,
    be_greater_than: float | None = None,
    be_greater_than_or_equal_to: float | None = None,
    **kwargs: Any,
) -> GeneratedTest:
    """Test that the maximum string length is within expected bounds."""
    del kwargs

    def _check(max_length: float) -> Result:
        checks: list[bool] = []
        if be_exactly is not None:
            checks.append(max_length == be_exactly)
        if be_less_than is not None:
            checks.append(max_length < be_less_than)
        if be_less_than_or_equal_to is not None:
            checks.append(max_length <= be_less_than_or_equal_to)
        if be_greater_than is not None:
            checks.append(max_length > be_greater_than)
        if be_greater_than_or_equal_to is not None:
            checks.append(max_length >= be_greater_than_or_equal_to)
        return Result(
            name=f"average-max-string-length-of-{column}",
            success=all(checks),
            unexpected=max_length if not all(checks) else None,
        )

    return nw.col(column).str.len_chars().max(), _check


def all_values_should(
    column: str,
    be_one_of: list[str] | None = None,
    not_be_one_of: list[str] | None = None,
    match_regex: str | None = None,
    **kwargs: Any,
) -> GeneratedTest:
    """Test all unique values within a column are within expected group."""
    del kwargs

    def _check(
        success: bool,
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


def type_should(
    column: str,
    be: str | None = None,
    not_be: str | None = None,
    be_one_of: list[str] | None = None,
    **kwargs: Any,
) -> GeneratedTest:
    """Check for type of column.

    Check that type of column meets expected criteria. Note that because Wimsey
    is a dataframe agnostic tool, this should be of *Narwhals* expected types,
    such as Float64, Int64, String, etc.

    See Narwhals' documentation for more details:
    https://narwhals-dev.github.io/narwhals/api-reference/dtypes/
    """
    del kwargs

    def _check(schema_dict: dict) -> Result:
        col_type = schema_dict[column]
        checks: list[bool] = []
        if be is not None:
            checks.append(be.lower() == col_type.lower())
        if not_be is not None:
            checks.append(not_be.lower() != col_type.lower())
        if be_one_of is not None:
            checks.append(col_type.lower() in [i.lower() for i in be_one_of])
        return Result(
            name=f"type-of-{column}",
            success=all(checks),
            unexpected=col_type if not all(checks) else None,
        )

    return schema, _check


def columns_should(
    have: list[str] | str | None = None,
    not_have: list[str] | str | None = None,
    be: list[str] | str | None = None,
    **kwargs: Any,
) -> GeneratedTest:
    """Check that expected columns are present / non-present within dataframe."""
    del kwargs

    def _check(schema_dict: dict) -> Result:
        _have = list(have) if isinstance(have, str) else have
        _not_have = list(not_have) if isinstance(not_have, str) else not_have
        _be = list(be) if isinstance(be, str) else be
        checks: list[bool] = []
        present_columns = list(schema_dict)
        if _have is not None:
            checks.extend(col in present_columns for col in _have)
        if _not_have is not None:
            checks.extend(col not in present_columns for col in _not_have)
        if _be is not None:
            checks.append(set(present_columns) == set(_be))
            checks.append(len(present_columns) == len(_be))
        return Result(
            name="columns",
            success=all(checks),
            unexpected=present_columns if not all(checks) else None,
        )

    return schema, _check


def null_count_should(
    column: str,
    be_exactly: float | None = None,
    be_less_than: float | None = None,
    be_less_than_or_equal_to: float | None = None,
    be_greater_than: float | None = None,
    be_greater_than_or_equal_to: float | None = None,
    **kwargs: Any,
) -> GeneratedTest:
    """Check that null count of column meets expected criteria."""
    del kwargs

    def _check(null_count: float) -> Result:
        checks = []
        if be_exactly is not None:
            checks.append(null_count == be_exactly)
        if be_less_than is not None:
            checks.append(null_count < be_less_than)
        if be_greater_than is not None:
            checks.append(null_count > be_greater_than)
        if be_less_than_or_equal_to is not None:
            checks.append(null_count <= be_less_than_or_equal_to)
        if be_greater_than_or_equal_to is not None:
            checks.append(null_count >= be_greater_than_or_equal_to)
        return Result(
            name=f"null-count-of-{column}",
            success=all(checks),
            unexpected=null_count if not all(checks) else None,
        )

    return nw.col(column).null_count(), _check


def null_percentage_should(
    column: str,
    be_exactly: float | None = None,
    be_less_than: float | None = None,
    be_less_than_or_equal_to: float | None = None,
    be_greater_than: float | None = None,
    be_greater_than_or_equal_to: float | None = None,
    **kwargs: Any,
) -> GeneratedTest:
    """Check that null percentage of column meets expected criteria."""
    del kwargs

    def _check(null_percentage: float) -> Result:
        checks = []
        if be_exactly is not None:
            checks.append(null_percentage == be_exactly)
        if be_less_than is not None:
            checks.append(null_percentage < be_less_than)
        if be_greater_than is not None:
            checks.append(null_percentage > be_greater_than)
        if be_less_than_or_equal_to is not None:
            checks.append(null_percentage <= be_less_than_or_equal_to)
        if be_greater_than_or_equal_to is not None:
            checks.append(null_percentage >= be_greater_than_or_equal_to)
        return Result(
            name=f"null-percentage-of-{column}",
            success=all(checks),
            unexpected=null_percentage if not all(checks) else None,
        )

    return (nw.col(column).null_count() / nw.col(column).len()), _check


possible_tests: dict[str, Callable] = {
    "mean_should": (mean_should := _range_check(nw.mean, "mean")),
    "min_should": (min_should := _range_check(nw.min, "min")),
    "max_should": (max_should := _range_check(nw.max, "max")),
    "std_should": (std_should := _range_check(lambda col: nw.col(col).std(), "stdev")),
    "count_should": (count_should := _range_check(lambda col: nw.col(col).count(), "count")),
    "row_count_should": row_count_should,
    "average_difference_from_other_column_should": average_difference_from_other_column_should,
    "average_ratio_to_other_column_should": average_ratio_to_other_column_should,
    "max_string_length_should": max_string_length_should,
    "all_values_should": all_values_should,
    "type_should": type_should,
    "columns_should": columns_should,
    "null_count_should": null_count_should,
    "null_percentage_should": null_percentage_should,
}
