"""Configuration loading/saving functions."""

from __future__ import annotations

import json
from typing import Any, Callable, cast

import fsspec
import narwhals.stable.v1 as nw

from wimsey.tests import possible_tests


def collect_tests(config: list[dict] | dict | list[tuple]) -> list[tuple]:
    """Take a configuration, and build out tests."""
    list_config: list[dict] | list[tuple] = config if isinstance(config, list) else [config]
    if isinstance(list_config[0], tuple) and isinstance(list_config[0][0], nw.Expr):
        return cast("list[tuple]", list_config)
    dict_list: list[dict] = list_config  # type: ignore[assignment]
    tests: list[tuple] = []
    for item in dict_list:
        test_name: str | None = item.get("test")
        test: Callable | None = None
        if test_name:
            test = possible_tests.get(item.get("test"))  # type: ignore[arg-type]
        if test is None:
            msg = (
                "Issue reading configuration, for at least one test, either no "
                "test is named, or a mispelt/unimplemented test is given.\n"
                f"Specifically, could not find: {test_name!s}"
            )
            raise ValueError(msg)
        tests.append(test(**item))
    return tests


def read_config(path: str, storage_options: dict | None = None) -> list[tuple]:
    """Read a json or yaml configuration, and return list of test callables."""
    storage_options_dict: dict = storage_options or {}
    config: dict | list[dict]
    with fsspec.open(path, "rt", **storage_options_dict) as file:
        contents = file.read()
    if path.endswith((".yaml", ".yml")):
        try:
            import yaml

            config = parse_contents(yaml.safe_load(contents))
            return collect_tests(config)  # type: ignore[arg-type]
        except ImportError as exception:
            msg = (
                "It looks like you're trying to import a yaml configured "
                "test suite. This is supported but requires an additional "
                "install of pyyaml (`pip install pyyaml`)"
            )
            raise ImportError(msg) from exception
    config = parse_contents(json.loads(contents))
    return collect_tests(config)


def parse_contents(contents: Any) -> list[dict] | dict:
    """Parse contents of loaded json/yaml into list of tests."""
    if isinstance(contents, list):
        return contents
    if isinstance(contents, dict):
        if isinstance(contents.get("tests"), list):
            return cast("dict | list[dict]", contents.get("tests"))
        return contents
    msg = (
        "It looks like the json/yaml file parsed in is either invalid "
        "or doesn't match what's required for Wimsey to interpret tests. \n"
        "Hint: json/yaml file should either be a list of tests, a single test "
        "or a key/value pair with a 'tests' key relating to a list of tests"
    )
    raise ValueError(msg)
