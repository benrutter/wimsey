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


def test_that_describe_excludes_non_specified_columns() -> None:
    df = pl.DataFrame({"a": [1.2, 1.3, 1.4], "b": ["one", "two", None]})
    actual = dataframe.describe(df, columns=["a"])
    assert "mean_a" in actual
    assert "mean_b" not in actual


def test_that_describe_excludes_non_specified_metrics() -> None:
    df = pl.DataFrame({"a": [1.2, 1.3, 1.4], "b": ["one", "two", None]})
    actual = dataframe.describe(df, metrics=["mean", "max"])
    assert "mean_a" in actual
    assert "mean_b" in actual
    assert "max_a" in actual
    assert "max_b" in actual
    assert "std_a" not in actual
    assert "std_b" not in actual


def test_that_describe_excludes_non_specified_column_and_metric_combos() -> None:
    df = pl.DataFrame({"a": [1.2, 1.3, 1.4], "b": ["one", "two", None]})
    actual = dataframe.describe(df, columns=["a"], metrics=["count"])
    assert "count_a" in actual
    assert "count_b" not in actual
    assert "min_a" not in actual


def test_that_profile_by_sampling_returns_list_of_dicts_of_expected_length() -> None:
    df = pl.DataFrame({"a": [1.2, 1.3, 1.4], "b": ["one", "two", None]})
    actual = dataframe.profile_from_sampling(df, samples=10, n=1)
    assert len(actual) == 10
    assert actual[0]["mean_a"] in [1.2, 1.3, 1.4]
    assert actual[4]["columns"] == "a_^&^_b"


def test_that_profile_from_samples_returns_list_of_dicts_of_expected_length() -> None:
    dfs = [
        pl.DataFrame({"a": [1.2, 1.3, 1.4], "b": ["one", "two", None]})
        for _ in range(20)
    ]
    actual = dataframe.profile_from_samples(dfs)
    assert len(actual) == 20
    assert actual[10]["mean_a"] == 1.3
    assert actual[4]["columns"] == "a_^&^_b"
