from typing import Callable, Any
from dataclasses import dataclass

from narwhals.typing import FrameT

from wimsey.dataframe import describe
from wimsey.tests import result
from wimsey.config import read_config, collect_tests


@dataclass
class final_result:
    success: bool
    results: list[result]


class DataValidationException(Exception):
    ...


def _as_set(val: Any) -> set:
    """
    Internal function, if val is none, return empty set,
    otherwise return set of just val
    """
    return {val} if val is not None else set()


def run_all_tests(df: FrameT, tests: list[Callable[[Any], result]]) -> final_result:
    columns: set[str] | None = set()
    metrics: set[str] | None = set()
    for test in tests:
        try:
            metrics |= test.required_metrics
            columns |= _as_set(test.keywords.get("column"))
            columns |= _as_set(test.keywords.get("other_column"))
        except AttributeError:
            columns = None  # fall back to calculating everything
            metrics = None
            break
    description: dict[str, Any] = describe(
        df,
        columns=list(columns),
        metrics=list(metrics),
    )
    results: list[result] = []
    for i_test in tests:
        results.append(i_test(description))
    return final_result(
        success=all(i.success for i in results),
        results=results,
    )


def test(
    df: FrameT, contract: str | list[dict] | dict, storage_options: dict | None = None
) -> final_result:
    """
    Carry out tests on dataframe and return results. This will *not* raise
    an exception on test failure, and will instead return a 'final_result'
    object, with a boolean 'success' field, and a detailed list of individual
    tests.

    If you want to halt processing in the event of a data contract failure,
    see `validate` function.
    """
    tests = (
        read_config(path=contract, storage_options=storage_options)
        if isinstance(contract, str)
        else collect_tests(contract)
    )
    return run_all_tests(df, tests)


def validate(
    df: FrameT, contract: str | list[dict] | dict, storage_options: dict | None = None
) -> FrameT:
    """
    Carry out tests on dataframe, returning original dataframe if tests are
    successful, and raising a DataValidationException in case of failure.
    """
    results = test(
        df=df,
        contract=contract,
        storage_options=storage_options,
    )
    if not results.success:
        failures: list[str] = [
            f"{i.name} (unexpected: {i.unexpected})"
            for i in results.results
            if not i.success
        ]
        newline = "\n - "
        msg = f"At least one test failed:\n - {newline.join(failures)}"
        raise DataValidationException(msg)
    return df
