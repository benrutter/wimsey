"""Wimsey data testing is a lightweight data contracts and testing framework.

It supporting naitve execution of multiple dataframe libraries for execution.

As well as being lightweight, Wimsey is intended to have a minimal API surface, with
all public functions in the top level "wimsey.*" namespace, and all tests in the
"wimsey.tests.*" namespace.
"""

from wimsey._version import __version__
from wimsey.execution import DataValidationError, test, validate
from wimsey.profiling import (
    starter_tests_from_samples,
    starter_tests_from_sampling,
    test_or_build,
    validate_or_build,
)

__all__ = [
    "__version__",
    "DataValidationError",
    "test",
    "validate",
    "validate_or_build",
    "test_or_build",
    "starter_tests_from_samples",
    "starter_tests_from_sampling",
]
