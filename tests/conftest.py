from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest
import yaml


@pytest.fixture
def demo_data(tmp_path: Path) -> Path:
    """Tiny on-farm style dataset that satisfies REQUIRED_COLUMNS and TrialRow types."""

    df = pd.DataFrame(
        {
            # IMPORTANT: make these clearly strings, not numeric-looking
            "field_id": ["F101", "F101", "F102", "F102"],
            "farm_id": ["Farm1", "Farm1", "Farm2", "Farm2"],
            "region": ["North", "North", "South", "South"],
            "year": [2024, 2024, 2024, 2024],  # int – OK
            "product": ["A", "A", "B", "B"],
            "yield": [60.0, 62.0, 65.0, 63.0],  # float – OK
        }
    )
    path = tmp_path / "demo.csv"
    df.to_csv(path, index=False)
    return path


@pytest.fixture
def demo_config_path(tmp_path: Path, demo_data: Path) -> Path:
    """
    Minimal YAML config that your current ConfigLoader + TrialflowConfig
    will accept and that the pipeline can use.
    """

    cfg = {
        "data": {
            "path": str(demo_data),
        },
        "model": {
            "id": "summary_only",
            "groups": ["product"],
            "min_records_per_group": 1,
        },
        "output": {
            "directory": str(tmp_path / "results"),
        },
    }

    path = tmp_path / "config.yml"
    path.write_text(yaml.safe_dump(cfg))
    return path
