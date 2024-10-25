import narwhals.stable.v1 as nw
from narwhals.stable.v1.typing import FrameT


@nw.narwhalify
def describe(df: FrameT) -> dict[str, float]:
    """
    Outputs a dictionary for use in testing, mimicking polars 'describe' method.

    Note this code is adapted from polars own descrip function.
    """
    if not df.columns:
        return {}

    # Determine which columns should get std/mean/percentile statistics
    stat_cols = {c for c, dt in df.schema.items() if dt.is_numeric()}

    required_exprs: list = []
    post_exprs: list = []
    required_exprs += [
        (nw.col(c).mean() if c in stat_cols else nw.lit(None)).alias(f"mean_{c}")
        for c in df.columns
    ]
    required_exprs += [
        (nw.col(c).std() if c in stat_cols else nw.lit(None)).alias(f"std_{c}")
        for c in df.columns
    ]
    required_exprs += [
        (nw.col(c).min() if c in stat_cols else nw.lit(None)).alias(f"min_{c}")
        for c in df.columns
    ]
    required_exprs += [
        (nw.col(c).max() if c in stat_cols else nw.lit(None)).alias(f"max_{c}")
        for c in df.columns
    ]
    required_exprs += [nw.lit(str(df.schema[c])).alias(f"type_{c}") for c in df.columns]
    required_exprs += [
        nw.lit("_^&^_".join(df.columns)).alias("columns"),
        nw.col(*df.columns).count().name.prefix("count_"),
        nw.col(*df.columns).null_count().name.prefix("null_count_"),
    ]
    post_exprs += [
        (
            nw.col(f"null_count_{c}")
            / (nw.col(f"count_{c}") + nw.col(f"null_count_{c}"))
        ).alias(f"null_percentage_{c}")
        for c in df.columns
    ]
    post_exprs += [
        (
            nw.col(f"count_{df.columns[0]}") + nw.col(f"null_count_{df.columns[0]}")
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
