"""
Basic diagnostics for trialflow-agro.
"""

from typing import Dict

import pandas as pd


def compute_diagnostics(df: pd.DataFrame) -> Dict[str, object]:
    """
    Compute a few simple diagnostics for the dataset.
    """
    return {
        "n_records": int(df.shape[0]),
        "n_fields": int(df["field_id"].nunique()) if "field_id" in df.columns else None,
        "n_farms": int(df["farm_id"].nunique()) if "farm_id" in df.columns else None,
        "n_products": int(df["product"].nunique()) if "product" in df.columns else None,
        "years": (
            sorted(df["year"].dropna().unique().tolist())
            if "year" in df.columns
            else []
        ),
    }
