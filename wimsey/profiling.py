"""Functions for profiling and building tests."""

from __future__ import annotations

import json
from enum import Enum, auto
from statistics import stdev
from typing import TYPE_CHECKING, Any

import fsspec

from wimsey.dataframe import profile_from_samples, profile_from_sampling
from wimsey.execution import validate

if TYPE_CHECKING:
    from collections.abc import Iterable

    from narwhals.stable.v1.typing import FrameT


class _StarterTestStatus(Enum):
    """Internal class to mark out column consistency for use."""

    UNSET = auto()
    SET = auto()
    CANCELLED = auto()


def starter_tests_from_samples(
    samples: Iterable[FrameT],
    margin: float = 1,
) -> list[dict]:
    """From a list of supported dataframes, produce a list of passing tests.

    Margin is worth explaining here, as it's the amount of *extra margin* tests
    are given, based on standard deviation. If three dataframes are given, with
    "column_a" values that have maximums of 1, 2 and 3, rather than creating a
    test that the maximum should be 3, Wimsey will give a degree of margin.

    By default this will be 1 standard deviation (of the maximum values). So for
    the above example, Wimsey will test for a maximum for 4. This can be tuned with
    the 'margin' keyword.
    """
    df_samples: list[dict[str, Any]] = profile_from_samples(samples)
    return _starter_tests_from_sample_describes(df_samples, margin)


def save_starter_tests_from_samples(
    path: str,
    samples: Iterable[FrameT],
    margin: float = 1,
    storage_options: dict | None = None,
) -> None:
    """Build and save starter tests from iterable of dataframe.

    See starter_tests_from_samples for more information, will additionally
    save tests as yaml or json dependend on path extension.
    """
    storage_options = storage_options or {}
    starter_tests = starter_tests_from_samples(samples, margin)
    _save_starter_tests(path, starter_tests, storage_options=storage_options)


def save_starter_tests_from_sampling(
    path: str,
    df: FrameT,
    samples: int = 100,
    n: int | None = None,
    fraction: int | None = None,
    margin: float = 1,
    storage_options: dict | None = None,
) -> None:
    """Create and save starter tests from dataframe.

    See starter_tests_from_sampling for more information, will additionally
    save tests as yaml or json dependend on path extension.
    """
    storage_options = storage_options or {}
    starter_tests = starter_tests_from_sampling(
        df=df,
        samples=samples,
        n=n,
        fraction=fraction,
        margin=margin,
    )
    _save_starter_tests(path, starter_tests, storage_options=storage_options)


def _save_starter_tests(
    path: str,
    tests: list[dict],
    storage_options: dict | None = None,
) -> None:
    if path.endswith((".yaml", ".yml")):
        try:
            import yaml
        except ImportError as exception:  # pragma: no cover
            msg = (
                "It looks like you're trying to import a yaml configured "
                "test suite. This is supported but requires an additional "
                "install of pyyaml (`pip install pyyaml`)"
            )
            raise ImportError(msg) from exception
        contents = yaml.dump(tests)
    else:
        contents = json.dumps(tests)
    with fsspec.open(path, mode="wt", **storage_options) as file:
        file.write(contents)


def starter_tests_from_sampling(
    df: FrameT,
    samples: int = 100,
    n: int | None = None,
    fraction: int | None = None,
    margin: float = 1,
) -> list[dict]:
    """Build out starter tests from a dataframe.

    From a supported dataframe, produce a list of passing tests by sampling the
    dataframe. Note n *or* fraction should be given, but not both. Keyword `samples`
    relates to the *number of samples* to take, whereas `n` relates to the *size of
    a given sample*.

    Margin is worth explaining here, as it's the amount of *extra margin* tests
    are given, based on standard deviation. If three dataframes are given, with
    "column_a" values that have maximums of 1, 2 and 3, rather than creating a
    test that the maximum should be 3, Wimsey will give a degree of margin.

    By default this will be 1 standard deviation (of the maximum values). So for
    the above example, Wimsey will test for a maximum for 4. This can be tuned with
    the 'margin' keyword.
    """
    df_samples = profile_from_sampling(df, samples, n, fraction)
    return _starter_tests_from_sample_describes(df_samples, margin)


def _starter_tests_from_sample_describes(
    samples: list[dict],
    margin: float = 1,
) -> list[dict]:
    """Build out starter tests from `describe` dictionary returs."""
    column_test: dict = {"test": "columns_should", "status": _StarterTestStatus.UNSET}
    for sample in samples:
        column_test = _update_column_starter_test(column_test, sample)
    if column_test["status"] is _StarterTestStatus.CANCELLED:  # pragma: no cover
        msg = (
            "There aren't any consistently held columns in the samples "
            "so Wimsey is unable to build a start test from them."
        )
        raise ValueError(msg)
    column_test.pop("status")
    if column_test.get("be") is None:  # pragma: no cover
        return [column_test]
    column_tests = _type_starter_tests(samples, column_test["be"])
    for stat in ["mean", "std", "max", "min", "null_percentage"]:
        column_tests += _stat_starter_tests(
            stat,
            samples,
            column_test["be"],
            margin=margin,
        )
    return [*column_tests, column_test]


def _update_column_starter_test(starter: dict, sample: dict) -> dict:
    """Update column checks for a single sample."""
    sample_columns = set(sample["columns"].split("_^&^_"))
    if starter["status"] is _StarterTestStatus.UNSET:
        starter["be"] = list(sample_columns)
        starter["status"] = _StarterTestStatus.SET
    elif starter["status"] is _StarterTestStatus.CANCELLED:  # pragma: no cover
        pass
    elif starter.get("be") is not None and set(starter["be"]) != set(
        sample_columns,
    ):  # pragma: no cover
        old_be = starter.pop("be")
        new_have = set(old_be) & set(sample_columns)
        if len(new_have) > 0:
            starter["have"] = list(new_have)
        else:
            starter["status"] = _StarterTestStatus.CANCELLED
    return starter


def _stat_starter_tests(
    stat: str,
    samples: list[dict],
    columns: list[str],
    margin: float,
) -> list[dict]:
    """Build out statistical starter tests."""
    tests: list[dict] = []
    for column in columns:
        values = [i[f"{stat}_{column}"] for i in samples if i[f"{stat}_{column}"] is not None]
        if len(values) == 0:
            continue
        absolute_margin = stdev(values) * margin
        if absolute_margin == 0:
            test = {
                "column": column,
                "test": f"{stat}_should",
                "be_exactly": max(values),
            }
        else:
            test = {
                "column": column,
                "test": f"{stat}_should",
                "be_less_than_or_equal_to": max(values) + absolute_margin,
                "be_greater_than_or_equal_to": min(values) - absolute_margin,
            }
        tests.append(test)
    return tests


def _type_starter_tests(
    samples: list[dict],
    columns: list[str],
) -> list[dict]:
    """Build out type based starter tests."""
    tests: list[dict] = []
    for column in columns:
        types: set[str] = {i[f"type_{column}"] for i in samples}
        test: dict[str, Any] = {"column": column, "test": "type_should"}
        if len(types) == 1:
            test |= {"be": next(iter(types))}
        else:  # pragma: no cover
            test |= {"be_one_of": list(types)}
        tests.append(test)
    return tests


def validate_or_build(
    df: FrameT,
    contract: str,
    samples: int = 100,
    n: int | None = None,
    fraction: int | None = None,
    margin: float = 1,
    storage_options: dict | None = None,
) -> FrameT:
    """Validate dataframe if test file exists, otherwise make one.

    Test file will be generated from multple samples of dataset.

    Will fall back to starter_tests_from_sampling (a list samples is not possible with
    only one dataframe), see *starter_tests_from_sampling* and *save_starter_tests_from_sampling*
    for more details on use of keyword arguments aside from df, contract and storage_options.
    """
    try:
        return validate(df, contract=contract, storage_options=storage_options)
    except FileNotFoundError:
        save_starter_tests_from_sampling(
            path=contract,
            df=df,
            samples=samples,
            n=n,
            fraction=fraction,
            margin=margin,
        )
        return df
