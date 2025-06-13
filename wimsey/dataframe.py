from typing import Any

import narwhals.stable.v1 as nw
from narwhals.stable.v1.typing import FrameT


@nw.narwhalify
def describe(
    df: FrameT,
    metrics: list[nw.Expr],
) -> dict[str, Any]:
    """
    Outputs a dictionary for use in testing, mimicking polars 'describe' method.

    Note this code is adapted from polars own descrip function.
    """
    if not df.columns:
        return {}
    df_metrics = df.select(*metrics)
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
