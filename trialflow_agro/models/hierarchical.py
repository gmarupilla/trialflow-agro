"""
Model specification for trialflow-agro.

For v0.1 this provides a lightweight container describing
how groups should be summarized. Statistical computation
is handled in the inference module.
"""

from pydantic import BaseModel
from trialflow_agro.config.schema import ModelConfig


class TrialModelSpec(BaseModel):
    """
    Model specification for trial summaries.

    - groups: list of columns to group by (e.g. ["product", "region"])
    - min_records_per_group: minimum records required for group statistics
    """

    groups: list[str]
    min_records_per_group: int


class TrialModel:
    """
    Thin wrapper over TrialModelSpec.

    In future versions this could be extended to define full
    Bayesian/hierarchical model structures.
    """

    def __init__(self, config: ModelConfig):
        self.spec = TrialModelSpec(
            groups=config.groups,
            min_records_per_group=config.min_records_per_group,
        )
