import polars as pl

from wimsey import dataframe


def test_that_describe_returns_expected_dictionary_for_df() -> None:
    df = pl.DataFrame({"a": [1.2, 1.3, 1.4], "b": ["one", "two", None]})
    actual = dataframe.describe(df)
    assert 1.29 < actual["mean_a"] < 1.31
    assert actual["null_count_b"] == 1
    assert 0.332 < actual["null_percentage_b"] < 0.334
    assert actual["length"] == 3
    assert actual["columns"] == "a_^&^_b"
