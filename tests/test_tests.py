from typing import Callable

from wimsey import tests


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
