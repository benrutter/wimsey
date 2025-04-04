# Wimsey 🔍

[![PyPI version](https://badge.fury.io/py/wimsey.svg)](https://pypi.org/project/wimsey/)
[![License](https://img.shields.io/github/license/benrutter/wimsey)](https://github.com/benrutter/wimsey/blob/main/LICENSE)
[![Static Badge](https://img.shields.io/badge/Docs-mkdocs-blue)](https://benrutter.github.io/wimsey)
![coverage](https://img.shields.io/badge/coverage-100-green)

<img src="./docs/assets/wimsey-on-a-computer.jpg" alt="A line drawing of Lord Peter Wimsey looking at a computer through a microscope" width="300" />

A lightweight, flexible and fully open-source data contract library.

- 🐋 **Bring your own dataframe library**: Built on top of [Narwhals](https://github.com/narwhals-dev/narwhals) so your tests are carried out natively in your own dataframe library (including Pandas, Polars, Pyspark, Dask, DuckDB, CuDF, Rapids, Arrow and Modin)
- 🎍 **Bring your own contract format**: Write contracts in yaml, json or python - whichever you prefer!
- 🪶 **Ultra Lightweight**: Built for fast imports and minimal overwhead with only two dependencies ([Narwhals](https://github.com/narwhals-dev/narwhals) and [FSSpec](https://github.com/fsspec/filesystem_spec))
- 🥔 **Simple, easy API**: Low mental overheads with two simple functions for testing dataframes, and a simple dataclass for results.

Check out the handy [test catalogue](https://benrutter.github.io/wimsey/possible_tests/) and [quick start guide](https://benrutter.github.io/wimsey/)

## What is a data contract?

As well as being a good buzzword to mention at your next data event, data contracts are a good way of testing data values at boundary points. Ideally, all data would be usable when you recieve it, but you probably already have figured that's not always the case.

A data contract is an expression of what *should* be true of some data - we might want to check that the only columns that exist are `first_name`, `last_name` and `rating`, or we might want to check that `rating` is a number less than 10.

Wimsey let's you write contracts in json, yaml or python, here's how the above checks would look in yaml:

```yaml
- test: columns_should
  be:
    - first_name
    - last_name
    - rating
- column: rating
  test: max_should
  be_less_than_or_equal_to: 10
```

Wimsey then can execute tests for you in a couple of ways, `validate` - which will throw an error if tests fail, and otherwise pass back your dataframe - and `test`, which will give you a detailed run down of individual test success and fails.

Validate is designed to work nicely with polars or pandas `pipe` methods as a handy guard:

```python
import polars as pl
import wimsey

df = (
  pl.read_csv("hopefully_nice_data.csv")
  .pipe(wimsey.validate, "tests.json")
  .group_by("name").agg(pl.col("value").sum())
)
```

Test is a single function call, returning a `FinalResult` data-type:

```python
import pandas as pd
import wimsey

df = pd.read_csv("hopefully_nice_data.csv")
results = wimsey.test(df, "tests.yaml")

if results.success:
  print("Yay we have good data! 🥳")
else:
  print(f"Oh nooo, something's up! 😭")
  print([i for i in results.results if not i.success])
```

# Roadmap, Contributing & Feedback

Wimsey is very new! There's a lot more to come soon in the form of additional available data tests, better test coverage, performance improvements and friendly error messages. Once the fundamentals are polished, next up is developing a handy API for "data profiling" (generate minimal tests from a sample of data).

Wimsey is ready to mingle! If you have ideas or feedback, including additional tests you'd want to see, please feel free to [raise an issue](https://github.com/benrutter/wimsey/issues) or submit [a pull request](https://github.com/benrutter/wimsey/pulls).
