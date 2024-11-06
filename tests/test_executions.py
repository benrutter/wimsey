import polars as pl

from wimsey import execution
from wimsey import tests


def test_run_all_tests_produces_expected_result_object():
    tests_to_carry_out = [
        tests.max_should(column="a", be_less_than=10),
        tests.std_should(column="a", be_greated_than=0),
        tests.type_should(column="b", be_one_of=["string", "int64"]),
    ]
    df = pl.DataFrame({"a": [1, 2, 3], "b": ["hat", "bat", "cat"]})
    actual = execution.run_all_tests(df, tests_to_carry_out)
    assert actual.success is True
    for result in actual.results:
        assert result.success is True
