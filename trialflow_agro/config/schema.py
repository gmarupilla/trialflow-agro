"""
Configuration models and loader for trialflow-agro.
"""

from pathlib import Path
from typing import List

import yaml
from pydantic import BaseModel, Field, ValidationError


class DataConfig(BaseModel):
    """Configuration for input trial dataset."""

    path: Path = Field(..., description="Path to the trial dataset (CSV or Parquet).")


class ModelConfig(BaseModel):
    """Configuration for the analysis model."""

    groups: List[str] = Field(
        default_factory=lambda: ["product"],
        description="Columns used to group summaries (e.g. ['product', 'region']).",
    )
    min_records_per_group: int = Field(
        5,
        description="Minimum records required for a group to be included in summaries.",
        ge=1,
    )


class OutputConfig(BaseModel):
    """Configuration for analysis outputs."""

    directory: Path = Field(
        Path("results"),
        description="Directory where results will be written.",
    )
    save_intermediate: bool = Field(
        True,
        description="Whether to save intermediate artifacts.",
    )


class TrialflowConfig(BaseModel):
    """Top-level configuration for trialflow-agro."""

    data: DataConfig
    model: ModelConfig
    output: OutputConfig


class ConfigLoader:
    """Loads and validates YAML configuration for trialflow-agro."""

    def load(self, path: Path) -> TrialflowConfig:
        if not path.exists():
            raise FileNotFoundError(f"Config file not found: {path}")

        raw = yaml.safe_load(path.read_text())
        try:
            cfg = TrialflowConfig(**raw)
        except ValidationError as exc:
            raise ValueError(f"Invalid configuration:\n{exc}") from exc

        return cfg
