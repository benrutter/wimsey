from typing import Callable

from wimsey import tests


def test_that_all_possible_tests_are_functions_that_return_partials() -> None:
    for test_name, actual_test in tests.possible_tests.items():
        assert isinstance(actual_test(column="anything"), Callable)


def test_all_possible_tests_exposed_as_variables_of_the_same_name_in_module() -> None:
    for test_name in tests.possible_tests:
        assert isinstance(getattr(tests, test_name), Callable)
