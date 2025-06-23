import polars as pl
import pytest

from wimsey import execution, tests


def test_run_all_tests_produces_expected_result_object() -> None:
    tests_to_carry_out = [
        tests.max_should(column="a", be_less_than=10),
        tests.std_should(column="a", be_greater_than=0),
        tests.type_should(column="b", be_one_of=["string", "int64"]),
    ]
    df = pl.DataFrame({"a": [1, 2, 3], "b": ["hat", "bat", "cat"]})
    actual = execution.run_all_tests(df, tests_to_carry_out)
    assert actual.success is True
    for result in actual.results:
        assert result.success is True


def test_validate_carries_out_tests_then_returns_object_if_passing() -> None:
    tests_to_carry_out = [
        tests.max_should(column="a", be_less_than=10),
        tests.std_should(column="a", be_greater_than=0),
        tests.type_should(column="b", be_one_of=["string", "int64"]),
    ]
    df = pl.DataFrame({"a": [1, 2, 3], "b": ["hat", "bat", "cat"]})
    actual = execution.validate(df, tests_to_carry_out)
    assert isinstance(actual, pl.DataFrame)


def test_validate_raises_error_if_tests_fail() -> None:
    tests_to_carry_out = [
        tests.max_should(column="a", be_exactly=0),
        tests.std_should(column="a", be_greater_than=10),
        tests.type_should(column="b", be_one_of=["string", "int64"]),
    ]
    df = pl.DataFrame({"a": [1, 2, 3], "b": ["hat", "bat", "cat"]})
    with pytest.raises(execution.DataValidationError):
        execution.validate(df, tests_to_carry_out)


def test_row_count_expectations_pass_when_expected() -> None:
    tests_to_carry_out = [
        tests.row_count_should(
            be_less_than=3.1,
            be_less_than_or_equal_to=3,
            be_greater_than=-2.343,
            be_greater_than_or_equal_to=0.3,
            be_exactly=3,
        ),
    ]
    df = pl.DataFrame({"a": [1, 2, 3], "b": ["hat", "bat", "cat"]})
    actual = execution.run_all_tests(df, tests_to_carry_out)
    assert actual.success is True
    for result in actual.results:
        assert result.success is True


def test_columns_should_have_expectations_fail_when_expected() -> None:
    tests_to_carry_out = [
        tests.columns_should(
            have="c",
            not_have="a",
            be=["b", "c"],
        ),
    ]
    df = pl.DataFrame({"a": [1, 2, 3], "b": ["hat", "bat", "cat"]})
    actual = execution.run_all_tests(df, tests_to_carry_out)
    assert actual.success is False


def test_column_type_tests_pass_when_expected() -> None:
    tests_to_carry_out = [
        tests.type_should(column="a", be="int64"),
        tests.type_should(column="a", be_one_of=["int64", "float64"]),
        tests.type_should(column="a", not_be="float64"),
        tests.type_should(column="b", be="string"),
    ]
    df = pl.DataFrame({"a": [1, 2, 3], "b": ["hat", "bat", "cat"]})
    actual = execution.run_all_tests(df, tests_to_carry_out)
    assert actual.success is True
    for result in actual.results:
        assert result.success is True


def test_average_column_difference_tests_pass_when_expected() -> None:
    tests_to_carry_out = [
        tests.average_difference_from_other_column_should(
            column="a",
            other_column="b",
            be_exactly=0,
            be_less_than=2,
            be_greater_than=-1,
            be_less_than_or_equal_to=0,
            be_greater_than_or_equal_to=0,
        ),
    ]
    df = pl.DataFrame({"a": [1, 2, 3], "b": [1, 2, 3]})
    actual = execution.run_all_tests(df, tests_to_carry_out)
    assert actual.success is True
    for result in actual.results:
        assert result.success is True


def test_average_column_ratio_tests_pass_when_expected() -> None:
    tests_to_carry_out = [
        tests.average_ratio_to_other_column_should(
            column="b",
            other_column="a",
            be_exactly=2,
            be_less_than=3,
            be_greater_than=1,
            be_less_than_or_equal_to=2,
            be_greater_than_or_equal_to=2,
        ),
    ]
    df = pl.DataFrame({"a": [1, 2, 3], "b": [2, 4, 6]})
    actual = execution.run_all_tests(df, tests_to_carry_out)
    assert actual.success is True
    for result in actual.results:
        assert result.success is True


def test_max_string_length_tests_fail_when_expected() -> None:
    tests_to_carry_out = [
        tests.max_string_length_should(
            column="a",
            be_less_than=4,
            be_less_than_or_equal_to=4,
            be_greater_than=2,
            be_greater_than_or_equal_to=2,
            be_exactly=3.0,
        ),
    ]
    df = pl.DataFrame({"a": ["cat", "bat", "ssssssssssssssnake"]})
    actual = execution.run_all_tests(df, tests_to_carry_out)
    assert actual.success is False


def test_all_values_tests_succeed_when_expected() -> None:
    tests_to_carry_out = [
        tests.all_values_should(
            column="a",
            be_one_of=["cat", "bat", "mat"],
            not_be_one_of=["hat"],
            match_regex="at$",
        ),
    ]
    df = pl.DataFrame({"a": ["cat", "bat"]})
    actual = execution.run_all_tests(df, tests_to_carry_out)
    assert actual.success is True
    for result in actual.results:
        assert result.success is True
