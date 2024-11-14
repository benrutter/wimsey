As an example, let's work through a simple example, and imagine we recieve "top-5-sleuths.csv" daily, over sftp. It's meant to look something like this:

| first_name  | last_name | rating  | cases_solved |
|-------------|-----------|---------|--------------|
| Peter       | Wimsey    | 9       | 11           |
| Jane        | Marple    | 9       | 12           |
| Father      | Brown     | 7       | 53           |
| Hercule     | Poirot    | 10      | 33           |
| Beatrice    | Bradley   | 8       | 66           |

It's meant to contain the top 5 sleuths, only sometimes, it has the wrong number of entries; othertimes first names are missing; and whilst ratings *should* be out of 10, sometimes they are over that. To make things worse every now and then, someone puts "lots" into `cases_solved` meaning it's no longer a number, and that causes all kinds of trouble.

### Writing Tests

We can convert those concerns we just mentioned into four tests to carry out on our dataset:

- The row count should be 5
- `first_name` should never be null
- `rating` should be be less than 10
- `cases_solved` should be a number

We can test for a lot more than that, but that works for our example. Our first move is to write this out as a "contract". This can be a yaml or json file, or alternatively, we can code it directly into python.

=== "sleuth-checks.yaml"
    ```yaml
    - test: row_count_should
      be_exactly: 5
    - column: first_name
      test: null_percentage_should
      be_exactly: 0
    - column: rating
      test: max_should
      be_less_than_or_equal_to: 10
    - column: cases_solved
      test: type_should
      be_one_of:
        - int64
        - float64
    ```
    > Note you'll need `pyyaml` installed to support reading yaml

=== "sleuth-checks.json"
    ```json
    [
      {
        "test": "row_count_should",
        "be_exactly": 5
      },
      {
        "column": "first_name",
        "test": "null_percentage_should",
        "be_exactly": 0
      },
      {
        "column": "rating",
        "test": "max_should",
        "be_less_than_or_equal_to": 10
      },
      {
        "column": "cases_solved",
        "test": "type_should",
        "be_one_of": ["int64", "float64"]
    ]
    ```
=== "sleuth_checks.py"
    ```python
    from wimsey import tests

    checks = [
      tests.row_count_should(be_exactly=5),
      tests.null_percentage_should(column="first_name", be_exactly=0),
      tests.max_should(column="rating", be_less_than_or_equal_to=10),
      tests.type_should(column="cases_solved", be_one_of=["int64", "float64]),
    ]
    ```

See [Possible Tests](possible-tests.md) for a full catalogue of runnable tests and their configurations.

### Executing Tests

Now that we've written out tests, we just need to actually *run* them on the actual data. There's two functions `wimsey` gives you to carry out checks: `validate` and `test`. These both carry out checks in the same way, but behave slightly differently based on the results.

- `test` will return a `FinalResult` type of object. It's a dataclasses containing a `success` boolean, alongside further details on the individual tests in a `results` lists.
- `validate` will run the checks and then just return the initial dataframe assuming everything passed. If any tests failed, it'll stop execution and throw a `DataValidationException`.

These are designed to cover a couple different use cases, `test` will provide more details if you want to dig into problems in a dataset, whilst `validate` is helpful if you just want to use `wimsey` as a "guard" to catch bad data from being processed.

We'll cover `test` first, it's called the same regardless of what type your dataframe is:

=== "using sleuth-checks.yaml"
    ```python
    from wimsey import test

    result = test(df, contract="sleuth-checks.yaml")
    if result.success:
      print("Everything is as expected! 🙌")
    else:
      print("Uh-oh, something's up! 😬")
      print([i for i in result.results if not i.success])
    ```
    > Note you'll need `pyyaml` installed to support reading yaml

=== "using sleuth-checks.json"
    ```python
    from wimsey import test

    result = test(df, contract="sleuth-checks.json")
    if result.success:
      print("Everything is as expected! 🙌")
    else:
      print("Uh-oh, something's up! 😬")
      print([i for i in result.results if not i.success])
    ```
=== "using sleuth_checks.py"
    ```python
    from wimsey import test
    from sleuth_checks import checks

    result = test(df, contract=checks)
    if result.success:
      print("Everything is as expected! 🙌")
    else:
      print("Uh-oh, something's up! 😬")
      print([i for i in result.results if not i.success])
    ```

Wimsey uses [fsspec](https://pypi.org/project/fsspec/) under the hood, so configs can be from any filesystem supported by fsspec (such as S3, SSH, Azure, Google Cloud etc) - use the fsspec prefix and pass in the appropriate storage options using `test`'s `storage_options` keyword. See fsspec documentation for more details on this.

Validate, will run tests in the exact same way as `test`, but simply raises an error if data fails expectations. This, in conjunction with Wimsey's compatibility with multiple dataframe types can make it a convenient tool for providing guarantees in a data pipeline.

=== "pandas"
    ```python
    import pandas as pd
    from wimsey import validate

    from settings import sleuth_storage_options

    top_sleuth: str = (
      pd.read_csv(
        "sshfs://sleuthwatch/top-5-sleuths.csv",
        storage_options=sleuth_storage_options,
      )
      .pipe(validate, "sleuth-checks.json")  # <- this is the wimsey bit
      .assign(name=lambda df: df["first_name"] + df["last_name"])
      .sort_values("rating", ascending=False)
      ["name"][0]
    )

    print(f"{top_sleuth} is the best sleuth!")
    ```

=== "polars"
    ```python
    import polars as pl
    from wimsey import validate

    from settings import sleuth_storage_options

    top_sleuth: str = (
      pl.read_csv(
        "sshfs://sleuthwatch/top-5-sleuths.csv",
        storage_options=storage_options,
      )
      .pipe(validate, "sleuth-checks.json")  # <- this is the wimsey bit
      .with_columns(name=pl.col("first_name") + " " + pl.col("last_name"))
      .sort("rating", descending=True)
      .select("name")
      .to_series()[0]
    )

    print(f"{top_sleuth} is the best sleuth!")
    ```

=== "dask"
    ```python
    import dask.dataframe as dd
    from wimsey import validate

    from settings import sleuth_storage_options

    top_sleuth: str = (
      dd.read_csv(
        "sshfs://sleuthwatch/top-5-sleuths.csv",
        storage_options=sleuth_storage_options,
      )
      .pipe(validate, "sleuth-checks.json")  # <- this is the wimsey bit
      .assign(name=lambda df: df["first_name"] + " " + df["last_name"])
      .sort_values("rating", ascending=False)
      ["name"]
      .compute()[0]
    )

    print(f"{top_sleuth} is the best sleuth!")
    ```

=== "pyarrow"
    ```python
    from pyarrow import compute, csv
    from wimsey import validate

    from settings import download_sleuth_file

    download_sleuth_file(to="local-5-sleuths.csv")
    df = csv.read_csv("local-5-sleuths.csv")
    validate(df, "sleuth-checks.json")  # <- this is the wimsey bit
    name = compute.binary_join_element_wise(df["first_name"], df["last_name"], " ")
    df = df.append("name", name).sort_by("rating")
    top_sleuth = str(df["name"][-1])

    print(f"{top_sleuth} is the best sleuth!")
    ```

And that's it for testing, to keep things simple `validate` and `test` are the only public-intended functions in Wimsey, aside from test creation, which is covered further in the *possible tests* section.

Wimsey also support *generating tests*, see [the building tests section](building-tests.md) for how to get started.
