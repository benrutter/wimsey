from typing import Any, Literal

import pandas as pd
import polars as pl
import pytest

import wimsey


def dataframe(backend: Literal["pandas", "polars"]) -> Any:
    """Generate example dataframe for given backend"""
    data = {
        "first_name": ["Peter", "Jane", "Father", "Hercule", "Beatrice"],
        "last_name": ["Wimsey", "Marple", "Brown", "Poirot", "Bradley"],
        "rating": [9, 9, 7, 10, 8],
        "cases_solved": [11, 12, 53, 33, 66],
    }
    if backend == "pandas":
        return pd.DataFrame(data)
    if backend == "polars":
        return pl.DataFrame(data)
    msg = "Backend not recognised"
    raise NotImplementedError(msg)


@pytest.mark.parametrize(
    ("backend", "should_pass"),
    [
        ("pandas", True),
        ("pandas", False),
        ("polars", True),
        ("polars", False),
    ],
)
def test_validation_of_passing_example(backend: str, should_pass: bool) -> None:
    """Check that given dataframe passes example suite with validate function."""
    df = dataframe(backend)
    suite = f"tests/example-{'passing' if should_pass else 'failing'}.yaml"
    try:
        wimsey.validate(df, suite)
        assert should_pass, "Test passed"
    except wimsey.DataValidationError as error:
        assert not should_pass, f"Test failed: {error}"


@pytest.mark.parametrize(
    ("backend", "should_pass"),
    [
        ("pandas", True),
        ("pandas", False),
        ("polars", True),
        ("polars", False),
    ],
)
def test_test_of_passing_example(backend: str, should_pass: bool) -> None:
    """Check that given dataframe passes example suite with validate function."""
    df = dataframe(backend)
    suite = f"tests/example-{'passing' if should_pass else 'failing'}.yaml"
    results = wimsey.test(df, suite)
    assert results.success is should_pass, str([i for i in results.results if not i.success])
    for result in results.results:
        assert result.success is should_pass, result.name
