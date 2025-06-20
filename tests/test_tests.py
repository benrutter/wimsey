from typing import Callable

import polars as pl

from wimsey import tests
from wimsey.execution import test as _test  # so pytest won't think this is test


def test_that_all_possible_tests_are_functions_that_return_partials() -> None:
    for test_name, actual_test in tests.possible_tests.items():
        assert isinstance(test_name, str)
        assert isinstance(
            actual_test(
                column="anything",
                other_column="anythin_else",
                be_less_than=3,
                be_one_of=[1, 2, 3],
            ),
            tuple,
        )


def test_all_possible_tests_exposed_as_variables_of_the_same_name_in_module() -> None:
    for test_name in tests.possible_tests:
        assert isinstance(getattr(tests, test_name), Callable)


def test_null_count_passes_and_fails_when_expected() -> None:
    df = pl.DataFrame({"a": [1, None, 2]})
    should_pass = _test(
        df,
        tests.null_count_should(
            column="a",
            be_exactly=1,
            be_less_than=2,
            be_less_than_or_equal_to=1,
            be_greater_than=0,
            be_greater_than_or_equal_to=1,
        ),
    )
    should_fail = _test(
        df,
        tests.null_count_should(
            column="a",
            be_exactly=2,
            be_less_than=1,
            be_less_than_or_equal_to=0,
            be_greater_than=1,
            be_greater_than_or_equal_to=0,
        ),
    )
    assert should_pass.success
    assert not should_fail.success


def test_null_percentage_passes_and_fails_when_expected() -> None:
    df = pl.DataFrame({"a": [1, None, 2, None]})
    should_pass = _test(
        df,
        tests.null_percentage_should(
            column="a",
            be_exactly=0.5,
            be_less_than=1,
            be_less_than_or_equal_to=0.5,
            be_greater_than=0,
            be_greater_than_or_equal_to=0.5,
        ),
    )
    should_fail = _test(
        df,
        tests.null_percentage_should(
            column="a",
            be_exactly=1,
            be_less_than=0,
            be_less_than_or_equal_to=0,
            be_greater_than=1,
            be_greater_than_or_equal_to=1,
        ),
    )
    assert should_pass.success
    assert not should_fail.success
