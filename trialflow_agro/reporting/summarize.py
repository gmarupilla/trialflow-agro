"""
Summary transformation utilities for trialflow-agro.
"""

from typing import Any, Dict

from trialflow_agro.inference.fit import GroupSummary, TrialInferenceResult


class TrialSummary:
    """
    Build human-readable summary structures from inference results.
    """

    def generate(self, inference_results: TrialInferenceResult) -> Dict[str, Any]:
        """
        Convert inference result into a nested dict suitable for
        serialization and reporting.
        """

        def to_dict(gs: GroupSummary) -> Dict[str, Any]:
            return {
                "group_values": gs.group_values,
                "n": gs.n,
                "mean_yield": gs.mean_yield,
                "std_yield": gs.std_yield,
                "min_yield": gs.min_yield,
                "max_yield": gs.max_yield,
            }

        return {
            "overall": to_dict(inference_results.overall),
            "by_product": [to_dict(gs) for gs in inference_results.by_product],
            "by_groups": [to_dict(gs) for gs in inference_results.by_groups],
        }
