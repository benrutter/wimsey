Alongside *running* tests, Wimsey also has some functions to aid *building* tests. This can be useful if you want to automagically create some sensible initial tests for multiple datasets, without needing to type them out by hand, or create them manually in code.

As with the rest of Wimsey, your own dataframe engine will be used to sample the relevant statistics. Wimsey can either generate starter tests from *a list of samples* or it can use *sampling with replacement* to generate samples for you from a single dataframe. If you use the latter, note that Wimsey will need to *evaluate each sample individually* so if you are using a lazy framework such as Polars' LazyFrames, Dask or Modin you will likely want to collect your results first, or implement a caching mechanism to avoid unnecessary repeated computation.


## What is margin?

You'll see the keyword *margin* throughout Wimsey test building, it's worth explaining here first.

Margin is the amount of *extra allowance* tests give, based on the sample. For instance if Wimsey has three samples, with a "column_a" maximum of 1, 2 and 3, rather than creating a test for the maximum being 3 (the highest value seen in the samples), Wimsey will allow an amount of 'give' for the tests.

This is based on the *standard deviation of the statistical metric*, and for the above example would be 1, meaning that Wimsey would build a test that expects the maximum to be less than or equal to 4.

If this is all giberish to you, don't worry, the 'margin' keyword defaults to 1, which is often a sensible choice, if you find that Wimsey is creating to strict tests, bump it up slightly, if tests are too lax, you can reduce margin to a smaller positive number.

Setting `margin` to a negative value means that your creating a test that your given sample would fail, and while supported, is unlikely to be what you're looking to do.

## From Sampling

From a single dataframe, Wimsey will sample with replacement to build a starter test. The `samples` keyword specifies the number of times you want Wimsey to build a sample, while `n` or `fraction` tell Wimsey the size (in rows) or fraction (as a float) of the sample to take. Note that you *can't supply both n AND fraction keywords to Wimsey*.

Wimsey has a `starter_tests_from_sampling` function, and a `save_starter_tests_from_sampling` function dependent on whether you're intending to return the tests as a dictionary, or save them to a file. `save_starter_tests_from_sampling` takes the exact same arguments, but with the addition of a `path` and an optional `storage_options` argument.

=== "starter_tests_from_sampling"
    ```python
    import polars as pl
    from wimsey.profile import starter_tests_from_sampling

    df = pl.DataFrame({"a": [1, 2, 3], "b": ["cool", "bat", "hat"]})
    tests: list[dict] = starter_tests_from_sampling(df, samples=5_000, n=2, margin=3)
    ```
=== "save_starter_tests_from_sampling"
    ```python
    import pandas as pd
    from wimsey.profile import starter_tests_from_sampling

    df = pd.DataFrame({"a": [1, 2, 3], "b": ["cool", "bat", "hat"]})
    tests: list[dict] = save_starter_tests_from_sampling(
        path="my-first-test.json",
        df=df,
        samples=5_000,
        fraction=0.5,
        margin=3,
    )
    ```

## From Samples

From a list (or other iterable such as a generate) of supported dataframes, Wimsey will produce a list of passing tests.

Wimsey has a `starter_tests_from_samples` function, and a `save_starter_tests_from_samples` function dependent on whether you're intending to return the tests as a dictionary, or save them to a file. `save_starter_tests_from_samples` takes the exact same arguments, but with the addition of a `path` and an optional `storage_options` argument.

=== "starter_tests_from_samples"
    ```python
    from glob import glob

    import pandas as pd
    from wimsey.profile import starter_tests_from_samples

    dfs = [pd.read_csv(i) for i in glob("folder/of/samples/*.csv")]
    tests: list[dict] = starter_tests_from_samples(dfs, margin=1.5)
    ```
=== "save_starter_tests_from_samples"
    ```python
    from glob import glob

    import polars as pl
    from wimsey.profile import save_starter_tests_from_samples

    from config import my_storage_options

    save_starter_tests_from_samples(
        path="s3://test-store/cooltest.yaml",
        samples=[pl.read_parquet(i) for i in glob("folder/of/samples/*.parquet")],
        margin=0.8,
        storage_options=my_storage_options,
    )
    ```
