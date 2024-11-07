Wimsey is designed to be a data contracts library a lot like Soda or Great Expectations. Rather than aiming to provide new functionality, it's primary motivation is to be as lightweight as possible, and, by focusing on dataframes, allow data tests to be evaluated natively and efficiently.

It's probably a good fit for you if:

- ✅ You're working with dataframes in python (via Pandas, Polars, Dask, Modin, etc)
- ✅ You want to carry out data testing with minimal overheads
- ✅ You want to minimise your overall dependencies

It might not work for you if:

- ❌ You're wanting to test SQL data without ingesting into python
- ❌ You want a data contracts solution that also provides a business user facing GUI

## How small is Wimsey?

The answer to this is *very*, to give you an example, 

## How fast is Wimsey?

That's a very big *it depends*. Wimsey executes tests *in your own dataframe library* so performance will match your library of choice, if you're using Modin or Dask, Wimsey will operate over large distributed datasets, if you're using Polars, Wimsey will be highly performant.

Narwhals [operates natively on dataframes with minimal overhead](https://narwhals-dev.github.io/narwhals/overhead/) so you should expect to see performant operations. Additionally, if you were previously needing to convert, or sample data into another format, you'll no longer need to carry this step out, saving you more runtime.
