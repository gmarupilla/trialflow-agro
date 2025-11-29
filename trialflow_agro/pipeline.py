"""
Pipeline orchestrator for trialflow-agro.

Ties together:
- config loading (YAML + Pydantic)
- data loading and validation
- summary "inference"
- diagnostics
- writing results.json
"""

import json
from pathlib import Path

from trialflow_agro.config.schema import ConfigLoader, TrialflowConfig
from trialflow_agro.data.loaders import TrialDataLoader
from trialflow_agro.inference.diagnostics import compute_diagnostics
from trialflow_agro.inference.fit import TrialInference
from trialflow_agro.models.hierarchical import TrialModel


class Pipeline:
    def __init__(self, config_path: Path, data_path: Path, output_dir: Path):
        self.config_path = config_path
        self.data_path = data_path
        self.output_dir = output_dir

    def run(self) -> None:
        # Load config
        cfg: TrialflowConfig = ConfigLoader().load(self.config_path)

        # Load data
        df = TrialDataLoader().load(self.data_path)

        # Build model spec & run inference
        model = TrialModel(cfg.model)
        inference_engine = TrialInference(
            groups=model.spec.groups,
            min_records_per_group=model.spec.min_records_per_group,
        )
        inference_result = inference_engine.run(df)

        # Diagnostics
        diagnostics = compute_diagnostics(df)

        # Save results
        self.output_dir.mkdir(parents=True, exist_ok=True)
        (self.output_dir / "results.json").write_text(
            json.dumps(
                {
                    "config": cfg.model_dump(),
                    "inference": inference_result.model_dump(),
                    "diagnostics": diagnostics,
                },
                indent=2,
            ),
            encoding="utf-8",
        )
