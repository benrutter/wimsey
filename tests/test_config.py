"""Unit tests for config module."""
import json
from collections.abc import Callable
from typing import NoReturn, Self

import pytest
import yaml

from wimsey import config
from wimsey.types import NwExpr, _MagicExpr


@pytest.fixture
def test_suite() -> list[dict]:
    """Return an example test suite."""
    return [
        {"test": "mean_should", "column": "a", "be_exactly": 34},
        {"test": "type_should", "column": "y", "be_one_of": ["int64", "float64"]},
    ]


def throw_import_error(*args, **kwargs) -> NoReturn:
    """Take any args, ignore them and throw an import error."""
    del args, kwargs
    raise ImportError


def test_collect_tests_return_type(
    test_suite: list[dict],
) -> None:
    """Collected tests should match expected type."""
    actual = config._collect_tests(test_suite)
    for expr, callable_ in actual:
        assert isinstance(expr, (NwExpr, _MagicExpr))
        assert isinstance(callable_, Callable)


@pytest.mark.parametrize(
    ("to_pop", "to_match", "error_type"),
    [
        (0, "column", TypeError),
        (1, "test", ValueError),
    ],
)
def test_collect_tests_error_throwing(
    test_suite: list[dict],
    to_pop: int,
    to_match: str,
    error_type: type[Exception],
) -> None:
    """Helpful descriptive error should be thrown."""
    test_suite[to_pop].pop(to_match)
    with pytest.raises(error_type, match=to_match):
        config._collect_tests(test_suite)


def test_repeatablility(test_suite: list[dict]) -> None:
    """Collect should support intput of test functions."""
    initial = config._collect_tests(test_suite)
    actual = config._collect_tests(initial)
    assert actual == initial


def test_read_config_for_yaml(monkeypatch: pytest.MonkeyPatch, test_suite: list[dict]) -> None:
    """Should part yaml version of tests."""
    class DummyOpenFile:
        def __enter__(self, *args, **kwargs) -> Self:
            return self

        def __exit__(self, *args, **kwargs) -> None: ...

        def read(self, *args, **kwargs) -> str:
            del args, kwargs
            return yaml.dump(test_suite)

    def open_file_patch(*args, **kwargs):
        del args, kwargs
        return DummyOpenFile()

    monkeypatch.setattr(config.fsspec, "open", open_file_patch)
    actual = config._read_config("file.yaml")
    for expr, callable_ in actual:
        assert isinstance(expr, (NwExpr, _MagicExpr))
        assert isinstance(callable_, Callable)


def test_read_config_for_yaml_with_test_section(
    monkeypatch: pytest.MonkeyPatch,
    test_suite: list[dict],
) -> None:
    """Should parse *into* a test section of file."""
    class DummyOpenFile:
        def __enter__(self, *args, **kwargs) -> Self:
            del args, kwargs
            return self

        def __exit__(self, *args, **kwargs) -> None: ...

        def read(self, *args, **kwargs) -> str:
            del args, kwargs
            return yaml.dump({"cool": ["some", "cool", "stuff"], "tests": test_suite})

    def open_file_patch(*args, **kwargs):
        del args, kwargs
        return DummyOpenFile()

    monkeypatch.setattr(config.fsspec, "open", open_file_patch)
    actual = config._read_config("file.yaml")
    for expr, callable_ in actual:
        assert isinstance(expr, (NwExpr, _MagicExpr))
        assert isinstance(callable_, Callable)


def test_read_config_parses_yaml_with_only_one_test(
    monkeypatch: pytest.MonkeyPatch,
    test_suite: list[dict],
) -> None:
    """File with only a single test (not list) should still be valid."""
    class DummyOpenFile:
        def __enter__(self, *args, **kwargs) -> Self:
            return self

        def __exit__(self, *args, **kwargs) -> None: ...

        def read(self, *args, **kwargs) -> str:
            del args, kwargs
            return yaml.dump(test_suite[0])

    def open_file_patch(*args, **kwargs):
        del args, kwargs
        return DummyOpenFile()

    monkeypatch.setattr(config.fsspec, "open", open_file_patch)
    actual = config._read_config("file.yaml")
    for expr, callable_ in actual:
        assert isinstance(expr, (NwExpr, _MagicExpr))
        assert isinstance(callable_, Callable)


def test_read_config_parses_json(
    monkeypatch: pytest.MonkeyPatch,
    test_suite: list[dict],
) -> None:
    """Parsing should work for json, as well as yaml."""
    class DummyOpenFile:
        def __enter__(self, *args, **kwargs) -> Self:
            del args, kwargs
            return self

        def __exit__(self, *args, **kwargs) -> None: ...

        def read(self, *args, **kwargs) -> str:
            del args, kwargs
            return json.dumps(test_suite)

    def open_file_patch(*args, **kwargs):
        del args, kwargs
        return DummyOpenFile()

    monkeypatch.setattr(config.fsspec, "open", open_file_patch)
    actual = config._read_config("file.json")
    for expr, callable_ in actual:
        assert isinstance(expr, (NwExpr, _MagicExpr))
        assert isinstance(callable_, Callable)


def test_error_message_for_yaml_import(
    monkeypatch: pytest.MonkeyPatch,
    test_suite: list[dict],
) -> None:
    """When yaml cannot be imported, a helpful error should be raised."""
    class DummyOpenFile:
        def __enter__(self, *args, **kwargs) -> Self:
            del args, kwargs
            return self

        def __exit__(self, *args, **kwargs) -> None: ...

        def read(self, *args, **kwargs) -> str:
            del args, kwargs
            return json.dumps(test_suite)

    def open_file_patch(*args, **kwargs):
        del args, kwargs
        return DummyOpenFile()

    monkeypatch.setattr(config.fsspec, "open", open_file_patch)
    monkeypatch.setattr(config, "_collect_tests", throw_import_error)
    with pytest.raises(ImportError, match="pip install pyyaml"):
        config._read_config("file.yaml")


def test_friendly_message_is_raised_when_yaml_does_not_return_contents(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Empty file should raise a helpful message."""
    class DummyOpenFile:
        def __enter__(self, *args, **kwargs) -> Self:
            return self

        def __exit__(self, *args, **kwargs) -> None: ...

        def read(self, *args, **kwargs) -> str:
            del args, kwargs
            return "dsafasdfasdf"

    def open_file_patch(*args, **kwargs) -> None:
        del args, kwargs
        return DummyOpenFile()

    monkeypatch.setattr(config.fsspec, "open", open_file_patch)
    with pytest.raises(ValueError, match="json/yaml"):
        config._read_config("file.yaml")

def test_friendly_message_is_raised_when_invalid_type_is_passed_down() -> None:
    """Should explain rather than throw generic error."""
    with pytest.raises(TypeError, match="does not recognise the format"):
        config._collect_tests("hello world!")
