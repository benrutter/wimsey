"""Configuration loading/saving functions."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any, cast

import fsspec

from wimsey.tests import _possible_tests
from wimsey.types import NwExpr, _MagicExpr

if TYPE_CHECKING:
    from collections.abc import Callable

    from wimsey.types import GeneratedTest


def _collect_tests(config: list[dict] | dict | list[GeneratedTest] | GeneratedTest) -> list[tuple]:
    """Take a configuration, and build out tests."""
    test_list: list[dict]
    match config:
        case (expr, _) if isinstance(expr, NwExpr | _MagicExpr):
            return cast("list[tuple]", [config])
        case [(expr, _), *_] if isinstance(expr, NwExpr | _MagicExpr):
            return cast("list[tuple]", config)
        case dict():
            test_list = [config]
        case [dict(), *_]:
            test_list = cast("list[dict]", config)
        case x:
            msg: str = (
                "Wimsey does not recognise the format of tests passed. Expected "
                "either a dict or list of dicts, or a GeneratedTest or list of "
                f"GeneratedTests. Instead recieved: {type(x)}"
            )
            raise TypeError(msg)
    tests: list[tuple] = []
    for item in test_list:
        test_name: str | None = item.get("test")
        test: Callable | None = None
        if test_name:
            test = _possible_tests.get(item.get("test"))  # type: ignore[arg-type]
        if test is None:
            msg = (
                "Issue reading configuration, for at least one test, either no "
                "test is named, or a mispelt/unimplemented test is given.\n"
            )
            msg += (
                f"Specifically, could not find: {test_name!s}"
                if test_name
                else f"Specifically, could not interpret: {item}"
            )
            raise ValueError(msg)
        tests.append(test(**item))
    return tests


def _read_config(path: str, storage_options: dict | None = None) -> list[tuple]:
    """Read a json or yaml configuration, and return list of test callables."""
    storage_options_dict: dict = storage_options or {}
    config: dict | list[dict]
    with fsspec.open(path, "rt", **storage_options_dict) as file:
        contents = file.read()
    if path.endswith((".yaml", ".yml")):
        try:
            import yaml

            config = _parse_contents(yaml.safe_load(contents))
            return _collect_tests(config)  # type: ignore[arg-type]
        except ImportError as exception:
            msg = (
                "It looks like you're trying to import a yaml configured "
                "test suite. This is supported but requires an additional "
                "install of pyyaml (`pip install pyyaml`)"
            )
            raise ImportError(msg) from exception
    config = _parse_contents(json.loads(contents))
    return _collect_tests(config)


def _parse_contents(contents: Any) -> list[dict] | dict:
    """Parse contents of loaded json/yaml into list of tests."""
    if isinstance(contents, list):
        return contents
    if isinstance(contents, dict):
        if isinstance(contents.get("tests"), list):
            return cast("dict | list[dict]", contents.get("tests"))
        return contents
    msg = (
        "It looks like the json/yaml file parsed is either invalid "
        "or doesn't match what's required for Wimsey to interpret tests. \n"
        "Hint: json/yaml file should either be a list of tests, a single test "
        "or a key/value pair with a 'tests' key relating to a list of tests"
    )
    raise ValueError(msg)
