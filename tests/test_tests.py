from typing import Callable

from wimsey import tests


def test_that_all_possible_tests_are_functions_that_return_partials() -> None:
    for test_name, actual_test in tests.possible_tests.items():
        assert isinstance(
            actual_test(column="anything", other_column="anythin_else"), Callable
        )


def test_all_possible_tests_exposed_as_variables_of_the_same_name_in_module() -> None:
    for test_name in tests.possible_tests:
        assert isinstance(getattr(tests, test_name), Callable)


def test_average_ratio_to_other_column_should_matches_expected() -> None:
    test = tests.average_ratio_to_other_column_should(
        "a", "b", be_greater_than=0.09, be_less_than=0.11
    )
    passing_result = test({"mean_a": 13, "mean_b": 130})
    failing_result = test({"mean_a": 13, "mean_b": 160})
    assert passing_result.success
    assert not failing_result.success
