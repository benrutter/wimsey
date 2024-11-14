import narwhals.stable.v1 as nw
from narwhals.stable.v1.typing import FrameT


@nw.narwhalify
def describe(
    df: FrameT,
    columns: list[str] | None = None,
    metrics: list[str] | None = None,
) -> dict[str, float]:
    """
    Outputs a dictionary for use in testing, mimicking polars 'describe' method.

    Note this code is adapted from polars own descrip function.
    """
    if not df.columns:
        return {}
    columns = columns or df.columns
    columns_to_check = [i for i in columns if i in df.columns]
    metrics = metrics or [
        "mean",
        "std",
        "min",
        "max",
        "type",
        "count",
        "null",
        "null_percentage",
        "length",
    ]

    # Determine which columns should get std/mean/percentile statistics
    stat_cols = {c for c, dt in df.schema.items() if dt.is_numeric()}

    required_exprs: list = [
        nw.lit("_^&^_".join(df.columns)).alias("columns"),
    ]
    post_exprs: list = []
    if "mean" in metrics:
        required_exprs += [
            (nw.col(c).mean() if c in stat_cols else nw.lit(None)).alias(f"mean_{c}")
            for c in columns_to_check
        ]
    if "std" in metrics:
        required_exprs += [
            (nw.col(c).std() if c in stat_cols else nw.lit(None)).alias(f"std_{c}")
            for c in columns_to_check
        ]
    if "min" in metrics:
        required_exprs += [
            (nw.col(c).min() if c in stat_cols else nw.lit(None)).alias(f"min_{c}")
            for c in columns_to_check
        ]
    if "max" in metrics:
        required_exprs += [
            (nw.col(c).max() if c in stat_cols else nw.lit(None)).alias(f"max_{c}")
            for c in columns_to_check
        ]
    if "type" in metrics:
        required_exprs += [
            nw.lit(str(df.schema[c])).alias(f"type_{c}") for c in columns_to_check
        ]
    if (
        "count" in metrics
        or "null" in metrics
        or "length" in metrics
        or "null_percentage" in metrics
    ):
        required_exprs += [nw.col(*columns_to_check).count().name.prefix("count_")]
    if "null" in metrics or "length" in metrics or "null_percentage" in metrics:
        required_exprs += [
            nw.col(*columns_to_check).null_count().name.prefix("null_count_")
        ]
        post_exprs += [
            (
                nw.col(f"null_count_{c}")
                / (nw.col(f"count_{c}") + nw.col(f"null_count_{c}"))
            ).alias(f"null_percentage_{c}")
            for c in columns_to_check
        ]
        post_exprs += [
            (
                nw.col(f"count_{columns_to_check[0]}")
                + nw.col(f"null_count_{columns_to_check[0]}")
            ).alias("length")
        ]
    df_metrics = df.select(
        *required_exprs,
    ).with_columns(*post_exprs)
    try:
        return {k: v[0] for k, v in df_metrics.to_dict(as_series=False).items()}  # type: ignore[union-attr]
    except AttributeError:
        return {
            k: v[0]
            for k, v in df_metrics.collect().to_dict(as_series=False).items()  # type: ignore[union-attr]
        }


def profile_from_sampling(
    df: FrameT,
    samples: int = 100,
    n: int | None = None,
    fraction: int | None = None,
) -> list[dict[str, float]]:
    return [
        describe(df.sample(n=n, fraction=fraction, with_replacement=True))
        for _ in range(samples)
    ]


def profile_from_samples(
    samples: list[FrameT],
) -> list[dict[str, float]]:
    return [describe(i) for i in samples]
