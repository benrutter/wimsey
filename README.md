# Wimsey 🔍

[![PyPI version](https://badge.fury.io/py/wimsey.svg)](https://badge.fury.io/py/wimsey)
[![License](https://img.shields.io/github/license/benrutter/wimsey)](https://github.com/benrutter/wimsey/blob/main/LICENSE)

A lightweight and flexible data contract library.

Wimsey is designed a very lightweight data contracts library, simlar to great-expections or soda-core, that is built on top of [Narwhals](https://github.com/narwhals-dev/narwhals). It is designed to have minimal import times and dependencies.

## What is a data contract?

As well as being a good buzzword to mention at your next data event, data contracts are a good way of testing data values at boundary points. Ideally, all data would be usable when you recieve it, but you probably already have figured that's not always the case.

A data contract is an expression of what *should* be true of some data, such as that it should 'only have columns x and y' or 'the values of column a should never exceed 1'. Wimsey is a library built to run these contracts on a dataframe during python runtime.

## Quick Demo

Let's start by taking a look at an example data contract, Wimsey supports reading json or yaml files, or just plain old python dictionaries. Here's an example of a yaml contract:

```yaml
- column: awesome_column
  test: mean_should
  be_greater_than: -10
  be_less_than: 100
- column: another_great_column
  test: null_count_should
  be_exactly: 0
- test: row_count_should
  be_less_than_or_equal_to: 50000
- column: neato_column
  test: type_should
  be_one_of:
    - int64
    - float64
```

> Note you'll need `pyyaml` installed to support reading this, the same data can be stored as json without needing extension if you're trying to keep things lightweight

Here we have two tests, firstly, we're checking that "awesome_column" is between -10 and 100, and then we're checking that "another_great_column" has no null entries.

In terms of using the Wimsey libary, there's essentially only two functions you'll need, `validate` and/or `test`.

Because Wimsey uses Narwhals under the hood, you can run these tests directly on your dataframe library of choice ([pandas](https://pandas.pydata.org/), [polars](https://pola.rs/), [dask](https://www.dask.org/) etc) as long as it's supported via Narwhals. Here's an example of using "validate" with pandas, which will throw an exception if tests fail, and otherwise pass back your data frame so you can continue happily:

```python
import pandas as pd
import wimsey

df = (
  pd.read_csv("hopefully_nice_data.csv")
  .pipe(wimsey.validate, "tests.json")
  .groupby(["name", "type"]).sum()
)
```

Similarly, here's an example with polars, but instead using `test`, which will return a `final_results` object with a success boolean.

```python
import polars as pl
import wimsey


df = pl.read_csv("hopefully_nice_data.csv")
results = wimsey.test(df, "tests.yaml")
if results.success:
  print("Yay we have good data! 🥳")
else:
  print(f"Oh nooo, something up! 😭")
  print(results)
```

## Project Status

Wimsey is veeeery, veeerrrry early, there's a very small amount of supported tests, and even less documentation. Feedback, contributions and requests are all welcome!


## Comparison

| Tool               | Import Time  | PyPi Size   | Dependencies | Has a GUI Framework   |
|--------------------|--------------|-------------|--------------|-----------------------|
| Great Expectations | 2.7 seconds  | 5367KB      | 25           | Yes                   |
| Soda Core          | 0.4 seconds  | 145KB       | 11           | Yes (non open source) |
| Wimsey             | 0.02 seconds | 6KB         | 2            | No                    |
