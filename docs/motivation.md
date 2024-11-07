Wimsey is designed to be a data contracts library a lot like Soda or Great Expectations. Rather than aiming to provide new functionality, it's primary motivation is to be as lightweight as possible, and, by focusing on dataframes, allow data tests to be evaluated natively and efficiently.

It's probably a good fit for you if:

- ✅ You're working with dataframes in python (via Pandas, Polars, Dask, Modin, etc)
- ✅ You want to carry out data testing with minimal overheads
- ✅ You want to minimise your overall dependencies
- ✅ Have an existing metadata format that you want to integrate tests into

It might not work for you if:

- ❌ You're wanting to test SQL data without ingesting into python
- ❌ You want a data contracts solution that also provides a business user facing GUI

## How small is Wimsey?

The answer is *very*. To give you a picture of comparison to alternative tools by size, here's a comparions of virtual environment sizes based on libaries + their dependencies*.


```vegalite
{
  "description": "A simple bar chart with embedded data.",
  "data": {"url" : "assets/raw-size.csv"},
  "mark": {"type": "bar", "tooltip": true},
  "encoding": {
    "x": {"field": "Package", "type": "nominal", "axis": {"labelAngle": 0}},
    "y": {"field": "Installation Size (MB)", "type": "quantitative"}
  }
}
```

It's worth bearing in mind that some of these dependencies might be ones you already need to have installed.

\* Note that soda is a little unusual here, since `soda-core` is very small (around 2x Wimsey's size), but also requires additional components to work with different data types.

## How fast is Wimsey?

That's a very big *it depends*. Wimsey executes tests *in your own dataframe library* so performance will match your library of choice, if you're using Modin or Dask, Wimsey will be able to operate over large distributed datasets, if you're using Polars, Wimsey will be blazingly fast.

Narwhals [operates natively on dataframes with minimal overhead](https://narwhals-dev.github.io/narwhals/overhead/) so you should expect to see performant operations. Additionally, if you were previously needing to convert, or sample data into another format, you'll no longer need to carry this step out, saving you more runtime.
