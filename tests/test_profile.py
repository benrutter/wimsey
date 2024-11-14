import polars as pl

from wimsey import profile
from wimsey import execution


def test_starter_tests_from_sampling_returns_passing_test() -> None:
    df = pl.DataFrame(
        {
            "a": [1, 2, 3, 4, 5],
            "b": ["hat", "bat", "cat", "mat", "sat"],
            "c": [0.2, 0.4, 0.2, 0.56, 0.1],
        }
    )
    starter_test = profile.starter_tests_from_sampling(df, samples=100, n=5)
    result = execution.test(df, starter_test)
    assert result.success


def test_starter_tests_from_samples_returns_passing_test() -> None:
    df = pl.DataFrame(
        {
            "a": [1, 2, 3, 4, 5],
            "b": ["hat", "bat", "cat", "mat", "sat"],
            "c": [0.2, 0.4, 0.2, 0.56, 0.1],
        }
    )
    starter_test = profile.starter_tests_from_samples(
        [df.sample(fraction=0.5) for _ in range(100)]
    )
    result = execution.test(df, starter_test)
    assert result.success


def test_margin_works_as_anticipated() -> None:
    df = pl.DataFrame(
        {
            "a": [1, 2, 3, 4, 5],
            "b": ["hat", "bat", "cat", "mat", "sat"],
            "c": [0.2, 0.4, 0.2, 0.56, 0.1],
        }
    )
    starter_test = profile.starter_tests_from_sampling(df, n=5, margin=50)
    result = execution.test(df, starter_test)
    assert result.success
    impossible_test = profile.starter_tests_from_sampling(df, n=5, margin=-500)
    result = execution.test(df, impossible_test)
    assert not result.success


def test_save_tests_from_sampling_creates_expected_and_runnable_file(tmp_path) -> None:
    df = pl.DataFrame(
        {
            "a": [1, 2, 3, 4, 5],
            "b": ["hat", "bat", "cat", "mat", "sat"],
            "c": [0.2, 0.4, 0.2, 0.56, 0.1],
        }
    )
    profile.save_starter_tests_from_sampling(
        str(tmp_path / "cool.yaml"), df, n=5, margin=1
    )
    result = execution.test(df, str(tmp_path / "cool.yaml"))
    assert result.success


def test_save_tests_from_samples_creates_expected_and_runnable_file(tmp_path) -> None:
    df = pl.DataFrame(
        {
            "a": [1, 2, 3, 4, 5],
            "b": ["hat", "bat", "cat", "mat", "sat"],
            "c": [0.2, 0.4, 0.2, 0.56, 0.1],
        }
    )
    profile.save_starter_tests_from_samples(
        str(tmp_path / "cool.json"),
        [df.sample(fraction=0.5) for _ in range(10)],
    )
    result = execution.test(df, str(tmp_path / "cool.json"))
    assert result.success
