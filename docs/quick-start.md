---
icon: lucide/rabbit
---

# Quick Start

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

## Execute tests with Wimsey's simple API

Validate is designed to work nicely with polars or pandas `pipe` methods as a handy guard:

```python
import polars as pl
import wimsey

df: pl.DataFrame = (
  pl.read_csv("hopefully_nice_data.csv")
  .pipe(wimsey.validate, "tests.json")
  .group_by("name").agg(pl.col("value").sum())
)
```

or if you need specific details on returns, test is a single function call:
```python
results: wimsey.FinalResult = wimsey.test(df, "tests.yaml")
print("Yay!" if results.success else "Boo!")
```

## Auto-magically create tests!

A lot of the time, you'll want to implement data testing on a whole load of pre-existing assets. That sounds like a lot of time typing python, json, or yaml (uh-oh!).

The good news is that Wimsey can create starter tests *for you*. Just replace the `validate` call, with the `validate_or_build`:

```python
import polars as pl
import wimsey

df = (
  pl.read_csv("hopefully_nice_data.csv")
  .pipe(wimsey.validate_or_build, "tests.json")
  .group_by("name").agg(pl.col("value").sum())
)
```

With this, if Wimsey tries to run `tests.json` only to find the file doesn't exist - it'll sample you "hopefully_nice_data.csv", and build out some sensible starter tests for you. The next time this code runs, it'll test against those created tests. This gives you a quick way to get up and running if you want data testing for a large range of pre-existing datasets.


## And much (well, at least a bit) more!

Wimsey gives you additional functionality on top of what you've seen here, but this is a quick tour. Look at the full documentation for details on all available tests, creating tests from samples/sampling, and more.
