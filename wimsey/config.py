import json
from typing import Any, Callable

import fsspec

from wimsey.tests import possible_tests


def collect_tests(config: list[dict] | dict | list[Callable]) -> list[Callable]:
    """
    Take a configuration, and build out tests
    """
    list_config: list[dict] | list[Callable] = (
        config if isinstance(config, list) else [config]
    )
    if isinstance(list_config[0], Callable):
        return list_config
    tests: list[Callable] = []
    for item in list_config:
        test_name: str | None = item.get("test")
        test: Callable | None = None
        if test_name:
            test = possible_tests.get(item.get("test"))(**item)  # type: ignore[arg-type]
        if test is None:
            msg = (
                "Issue reading configuration, for at least one test, either no "
                "test is named, or a mispelt/unimplemented test is given"
            )
            raise ValueError(msg)
        tests.append(test)
    return tests


def read_config(path: str, storage_options: dict | None = None) -> list[Callable]:
    """
    Read a json or yaml configuration, and return list of test callables
    """
    storage_options_dict: dict = storage_options or {}
    config: dict
    with fsspec.open(path, "rt", **storage_options_dict) as file:
        contents = file.read()
    if path.endswith(".yaml") or path.endswith(".yml"):
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
    return collect_tests(config)  # type: ignore[arg-type]


def parse_contents(contents: Any) -> list[dict] | dict:
    if isinstance(contents, list):
        return contents
    if isinstance(contents, dict):
        if isinstance(contents.get("tests"), list):
            return contents.get("tests")
        return contents
    msg = (
        "It looks like the json/yaml file parsed in is either invalid "
        "or doesn't match what's required for Wimsey to interpret tests. \n"
        "Hint: json/yaml file should either be a list of tests, a single test "
        "or a key/value pair with a 'tests' key relating to a list of tests"
    )
    raise ValueError(msg)
