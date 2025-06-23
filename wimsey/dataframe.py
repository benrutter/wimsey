"""Functions for dataframe interactions, like sampling and executing expressions."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import narwhals.stable.v1 as nw

if TYPE_CHECKING:
    from collections.abc import Iterable

    from narwhals.stable.v1 import NwDataFrame
    from narwhals.stable.v1.typing import IntoFrame


def _narwhals_to_dict(df: NwDataFrame) -> dict:
    """Convert Narwhals datframe to dict.

    Private function to convert Narwhals' FrameT to dict,
    note that this will *only* present the first row because
    it is built for specific evaluation of aggergate values.

    As such it's not suitable for general use.

    Also note, this will *force computation* for lazy frames,
    this is needed in order for Wimsey to carry out certain
    tests.
    """
    try:
        return {k: v[0] for k, v in df.to_dict(as_series=False).items()}  # type: ignore[union-attr]
    except AttributeError:
        return {
            k: v[0]
            for k, v in df.collect().to_dict(as_series=False).items()  # type: ignore[union-attr]
        }


def _validate_df_has_columns(df: NwDataFrame) -> NwDataFrame:
    if not df.columns:
        msg = "Wimsey cannot build a profile of this dataframe because it has no columns"
        raise TypeError(msg)
    return df


def evaluate(
    df: IntoFrame,
    metrics: list[nw.Expr],
) -> dict[str, Any]:
    """Execute a list of scalar expressions and return dictionary of results."""
    metrics += [nw.lit(str(df.schema[c])).alias(f"type_{c}") for c in df.columns]

    evaluation_df = nw.from_native(df).pipe(_validate_df_has_columns).select(*metrics)
    evaluation_dict = _narwhals_to_dict(evaluation_df)
    type_evals: list = [i for i in evaluation_dict if i.startswith("type")]
    schema_dict: dict = {i.replace("type_", ""): evaluation_dict.pop(i) for i in type_evals}
    return evaluation_dict | {"schema": schema_dict}


def describe(
    df: IntoFrame,
) -> dict[str, Any]:
    """Retrieve dictionary discribing dataframe.

    Mimics polars 'describe' method, but returns dict.
    """
    nw_df: NwDataFrame = nw.from_native(df)
    _validate_df_has_columns(nw_df)
    columns_to_check = nw_df.columns

    # Determine which columns should get std/mean/percentile statistics
    stat_cols = {c for c, dt in nw_df.schema.items() if dt.is_numeric()}

    required_exprs: list = [
        nw.lit("_^&^_".join(nw_df.columns)).alias("columns"),
    ]
    post_exprs: list = []
    required_exprs += [
        (nw.col(c).mean() if c in stat_cols else nw.lit(None)).alias(f"mean_{c}")
        for c in columns_to_check
    ]
    required_exprs += [
        (nw.col(c).std() if c in stat_cols else nw.lit(None)).alias(f"std_{c}")
        for c in columns_to_check
    ]
    required_exprs += [
        (nw.col(c).min() if c in stat_cols else nw.lit(None)).alias(f"min_{c}")
        for c in columns_to_check
    ]
    required_exprs += [
        (nw.col(c).max() if c in stat_cols else nw.lit(None)).alias(f"max_{c}")
        for c in columns_to_check
    ]
    required_exprs += [nw.lit(str(nw_df.schema[c])).alias(f"type_{c}") for c in columns_to_check]
    required_exprs += [nw.col(*columns_to_check).count().name.prefix("count_")]
    required_exprs += [
        nw.col(*columns_to_check).null_count().name.prefix("null_count_"),
    ]
    post_exprs += [
        (nw.col(f"null_count_{c}") / (nw.col(f"count_{c}") + nw.col(f"null_count_{c}"))).alias(
            f"null_percentage_{c}",
        )
        for c in columns_to_check
    ]
    post_exprs += [
        (
            nw.col(f"count_{columns_to_check[0]}") + nw.col(f"null_count_{columns_to_check[0]}")
        ).alias("length"),
    ]
    df_metrics = nw_df.select(
        *required_exprs,
    ).with_columns(*post_exprs)
    return _narwhals_to_dict(df_metrics)


def profile_from_sampling(
    df: IntoFrame,
    samples: int = 100,
    n: int | None = None,
    fraction: int | None = None,
) -> list[dict[str, float]]:
    """Return profiles from sampling a single dataframe."""
    nw_df = nw.from_native(df)
    return [
        describe(nw_df.sample(n=n, fraction=fraction, with_replacement=True))  # type: ignore[union-attr]
        for _ in range(samples)
    ]  # type: ignore[union-attr]


def profile_from_samples(
    samples: Iterable[IntoFrame],
) -> list[dict[str, Any]]:
    """Return profiles from individual samples."""
    return [describe(i) for i in samples]
