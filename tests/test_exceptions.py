"""Tests for high quality error messages."""

from typing import Callable

import polars as pl
import pytest

import wimsey

df = pl.DataFrame({"a": [1, 2, 3], "b": ["hat", "bat", "cat"]})


@pytest.mark.parametrize(
    "to_call",
    [
        wimsey.validate,
        wimsey.test,
    ],
)
def test_exception_for_invalid_contract_format(to_call: Callable) -> None:
    """Should raise helpful user error."""
    with pytest.raises(
        ValueError,
        match="It looks like the json/yaml file parsed is either invalid",
    ):
        to_call(
            df,
            contract="tests/example-nonsense.yaml",
        )


@pytest.mark.parametrize(
    "to_call",
    [
        wimsey.validate,
        wimsey.test,
    ],
)
def test_exception_for_not_a_real_test(to_call: Callable) -> None:
    """Should raise helpful user error explaining test does not exist."""
    with pytest.raises(
        ValueError,
        match="for at least one test, either no test is named, or a mispelt/"
        "unimplemented test is given.\nSpecifically, could not find: "
        "column_should_be_nice",
    ):
        to_call(df, contract=[{"test": "column_should_be_nice", "column": "example"}])
    with pytest.raises(
        ValueError,
        match="for at least one test, either no test is named, or a mispelt/"
        "unimplemented test is given.\nSpecifically, could not interpret: "
        "{'hello': 'world'}",
    ):
        to_call(df, contract={"hello": "world"})
