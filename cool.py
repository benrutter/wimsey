from wimsey import validate, tests
import polars as pl

pl.DataFrame({"a": [1, 2, 3]}).pipe(
    validate,
    "nice.yaml",
)
