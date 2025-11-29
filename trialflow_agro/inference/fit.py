"""
Inference logic for trialflow-agro.

For v0.1, "inference" consists of computing descriptive statistics
for overall data, per-product, and optional grouped summaries.
"""

from typing import Dict, List, Optional

import pandas as pd
from pydantic import BaseModel, Field


class StatBlock(BaseModel):
    """
    Internal block of statistics used to compute summaries.

    Using Pydantic keeps the entire inference stack consistent
    and ensures everything is JSON-serializable.
    """

    n: int
    mean: float
    std: Optional[float] = None
    min: float
    max: float


class GroupSummary(BaseModel):
    """Summary statistics for a single group."""

    group_values: Dict[str, object]
    n: int
    mean_yield: float
    std_yield: Optional[float] = None
    min_yield: float
    max_yield: float


class TrialInferenceResult(BaseModel):
    """
    Container for all summary statistics computed from the trial data.
    """

    overall: GroupSummary
    by_product: List[GroupSummary]
    by_groups: List[GroupSummary] = Field(default_factory=list)


class TrialInference:
    """
    Computes grouped summary statistics for trial data.
    """

    def __init__(
        self, groups: Optional[list[str]] = None, min_records_per_group: int = 5
    ):
        self.groups = groups or []
        self.min_records_per_group = min_records_per_group

    def run(self, df: pd.DataFrame) -> TrialInferenceResult:
        """Compute overall and grouped summary statistics."""
        overall = self._compute_summary(df, group_values={})

        by_product = self._compute_grouped(df, ["product"])

        by_groups: list[GroupSummary] = []
        if self.groups:
            by_groups = self._compute_grouped(df, self.groups)

        return TrialInferenceResult(
            overall=overall,
            by_product=by_product,
            by_groups=by_groups,
        )

    def _compute_summary(
        self, df: pd.DataFrame, group_values: Dict[str, object]
    ) -> GroupSummary:
        stats = self._stats_for_series(df["yield"])
        return GroupSummary(
            group_values=group_values,
            n=stats.n,
            mean_yield=stats.mean,
            std_yield=stats.std,
            min_yield=stats.min,
            max_yield=stats.max,
        )

    def _compute_grouped(
        self, df: pd.DataFrame, group_cols: list[str]
    ) -> List[GroupSummary]:
        summaries: list[GroupSummary] = []
        g = df.groupby(group_cols, dropna=False)

        for keys, group_df in g:
            if len(group_df) < self.min_records_per_group:
                continue

            # Normalize keys to dict
            if isinstance(keys, tuple):
                group_values = {col: val for col, val in zip(group_cols, keys)}
            else:
                group_values = {group_cols[0]: keys}

            stats = self._stats_for_series(group_df["yield"])
            summaries.append(
                GroupSummary(
                    group_values=group_values,
                    n=stats.n,
                    mean_yield=stats.mean,
                    std_yield=stats.std,
                    min_yield=stats.min,
                    max_yield=stats.max,
                )
            )

        return summaries

    def _stats_for_series(self, s: pd.Series) -> StatBlock:
        s_clean = s.dropna()
        n = int(s_clean.shape[0])
        if n == 0:
            return StatBlock(
                n=0, mean=float("nan"), std=None, min=float("nan"), max=float("nan")
            )

        return StatBlock(
            n=n,
            mean=float(s_clean.mean()),
            std=float(s_clean.std()) if n > 1 else None,
            min=float(s_clean.min()),
            max=float(s_clean.max()),
        )
