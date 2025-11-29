"""
Data loading and validation utilities for trialflow-agro.
"""

from pathlib import Path
from typing import Tuple

import pandas as pd
from pydantic import ValidationError

from trialflow_agro.data.schema import REQUIRED_COLUMNS, TrialRow


class TrialDataLoader:
    """
    Loads and validates on-farm trial datasets.

    - Supports CSV and Parquet inputs
    - Checks required columns
    - Spot-validates a sample of rows with Pydantic
    """

    def load(self, path: Path) -> pd.DataFrame:
        """
        Load data from CSV or Parquet and run basic validation.
        """
        df = self._read(path)
        self._validate_columns(df)
        self._validate_sample_rows(df)
        return df

    def _read(self, path: Path) -> pd.DataFrame:
        if not path.exists():
            raise FileNotFoundError(f"Data file not found: {path}")

        suffix = path.suffix.lower()
        if suffix == ".csv":
            return pd.read_csv(path)
        if suffix in {".parquet", ".pq"}:
            return pd.read_parquet(path)

        raise ValueError(f"Unsupported file type: {suffix}")

    def _validate_columns(self, df: pd.DataFrame) -> None:
        missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
        if missing:
            raise ValueError(f"Missing required columns: {missing}")

    def _validate_sample_rows(self, df: pd.DataFrame, n: int = 50) -> None:
        """
        Validate up to `n` rows using TrialRow (Pydantic) as a sanity check.
        This avoids validating the entire dataset, which can be large.
        """
        sample = df.head(n)
        errors: list[Tuple[int, str]] = []

        for idx, row in sample.iterrows():
            try:
                TrialRow(**row.to_dict())
            except ValidationError as exc:
                errors.append((idx, str(exc)))

        if errors:
            msg = "\n".join([f"Row {i}: {e}" for i, e in errors[:5]])
            raise ValueError(
                f"Sample validation failed for {len(errors)} row(s). "
                f"First few errors:\n{msg}"
            )
