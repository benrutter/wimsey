import json
from collections.abc import Callable

import pytest
import yaml

from wimsey import config


@pytest.fixture
def test_suite():
    return [
        {"test": "mean_should", "column": "a", "be_exactly": 34},
        {"test": "type_should", "column": "y", "be_one_of": ["int64", "float64"]},
    ]


def throw_import_error(*args, **kwargs):
    raise ImportError


def test_collect_tests_returns_list_of_callable_functions(test_suite):
    actual = config.collect_tests(test_suite)
    assert all(isinstance(i, Callable) for i in actual)


def test_collect_tests_returns_friendly_error_when_required_value_not_give(test_suite):
    test_suite[0].pop("column")
    with pytest.raises(TypeError, match="column"):
        config.collect_tests(test_suite)


def test_collect_tests_returns_friendly_error_when_no_test_is_given(test_suite):
    test_suite[1].pop("test")
    with pytest.raises(ValueError, match="test"):
        config.collect_tests(test_suite)


def test_collect_tests_returns_input_when_input_is_already_test_functions(test_suite):
    initial = config.collect_tests(test_suite)
    actual = config.collect_tests(initial)
    assert actual == initial


def test_read_config_parses_yaml(monkeypatch, test_suite):
    class DummyOpenFile:
        def __enter__(self, *args, **kwargs):
            return self

        def __exit__(self, *args, **kwargs):
            ...

        def read(self, *args, **kwargs):
            return yaml.dump(test_suite)

    def open_file_patch(*args, **kwargs):
        return DummyOpenFile()

    monkeypatch.setattr(config.fsspec, "open", open_file_patch)
    actual = config.read_config("file.yaml")
    assert all(isinstance(i, Callable) for i in actual)


def test_read_config_parses_json(monkeypatch, test_suite):
    class DummyOpenFile:
        def __enter__(self, *args, **kwargs):
            return self

        def __exit__(self, *args, **kwargs):
            ...

        def read(self, *args, **kwargs):
            return json.dumps(test_suite)

    def open_file_patch(*args, **kwargs):
        return DummyOpenFile()

    monkeypatch.setattr(config.fsspec, "open", open_file_patch)
    actual = config.read_config("file.json")
    assert all(isinstance(i, Callable) for i in actual)


def test_friendly_message_is_raised_when_yaml_is_unimportable(test_suite, monkeypatch):
    class DummyOpenFile:
        def __enter__(self, *args, **kwargs):
            return self

        def __exit__(self, *args, **kwargs):
            ...

        def read(self, *args, **kwargs):
            return json.dumps(test_suite)

    def open_file_patch(*args, **kwargs):
        return DummyOpenFile()

    monkeypatch.setattr(config.fsspec, "open", open_file_patch)
    monkeypatch.setattr(config, "collect_tests", throw_import_error)
    with pytest.raises(ImportError, match="pip install pyyaml"):
        config.read_config("file.yaml")


def test_friendly_message_is_raised_when_yaml_does_not_return_contents(
    test_suite, monkeypatch
):
    class DummyOpenFile:
        def __enter__(self, *args, **kwargs):
            return self

        def __exit__(self, *args, **kwargs):
            ...

        def read(self, *args, **kwargs):
            return "dsafasdfasdf"

    def open_file_patch(*args, **kwargs):
        return DummyOpenFile()

    monkeypatch.setattr(config.fsspec, "open", open_file_patch)
    with pytest.raises(ValueError, match="json/yaml"):
        config.read_config("file.yaml")
