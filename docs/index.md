# Wimsey 🔍


Wimsey is a lightweight, flexible and fully open-source data contract library. It's designed to let you:

- **Bring your own dataframe library**: Wimsey is built on top of [Narwhals](https://github.com/narwhals-dev/narwhals) so your tests are carried out natively in your own dataframe library (including Pandas, Polars, Dask, CuDF, Rapids, Arrow and Modin)
- **Bring your own contract format**: Write contracts in yaml, json or python - whichever you prefer!
- **Ultra Lightweight**: Built for fast imports and minimal overwhead with only two dependencies ([Narwhals](https://github.com/narwhals-dev/narwhals) and [FSSpec](https://github.com/fsspec/filesystem_spec))
- **Simple, easy API**: Low mental overheads with two simple functions for testing dataframes, and a simple dataclass for results.

Ideally, all data would be usable when you recieve it, but you probably already have figured that's not always the case. That's where data contracts come in.

A data contract is an expression of what *should* be true of some data, such as that it should 'only have columns x and y' or 'the values of column a should never exceed 1'. Wimsey is a library built to run these contracts on a dataframe during python runtime.

Additionally, Wimsey has tools to [help you generate sensible tests from a data sample](building-tests.md)

Wimsey is built on top of the awesome [Narwhals](https://github.com/narwhals-dev/narwhals) and natively supports any dataframes that Narwhal's does. At the time of writing, that includes Polars, Pandas, Arrow, Dask, Rapids and Modin.

If you're looking to get a quick feel for Wimsey, check out the [quick start documentation](quick-start.md)
