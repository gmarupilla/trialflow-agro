"""
Report generation for trialflow-agro.
"""

import json
from pathlib import Path
from typing import Any, Dict

from trialflow_agro.reporting.plots import table_from_summaries


class ReportBuilder:
    """
    Assembles a simple HTML report from saved results.json.
    """

    def __init__(self, results_dir: Path):
        self.results_dir = results_dir

    def _load_results(self) -> Dict[str, Any]:
        f = self.results_dir / "results.json"
        if not f.exists():
            raise FileNotFoundError(f"No results.json found in {self.results_dir}")
        return json.loads(f.read_text())

    def render(self, out_path: Path) -> None:
        data = self._load_results()

        inference = data.get("inference", {})
        diagnostics = data.get("diagnostics", {})

        # tables: overall, by_product, by_groups
        overall = inference.get("overall")
        by_product = inference.get("by_product", [])
        by_groups = inference.get("by_groups", [])

        overall_rows = [overall] if overall else []

        html_overall = table_from_summaries("Overall Summary", overall_rows)
        html_by_product = table_from_summaries("Per-Product Summary", by_product)
        html_by_groups = table_from_summaries("Grouped Summary", by_groups)

        html_diag_list = "".join(
            f"<li><strong>{k}</strong>: {v}</li>" for k, v in diagnostics.items()
        )

        html = f"""<!DOCTYPE html>
                <html>
                <head>
                <meta charset="utf-8">
                <title>trialflow-agro Report</title>
                </head>
                <body>
                <h1>trialflow-agro Report</h1>

                <h2>Diagnostics</h2>
                <ul>
                    {html_diag_list}
                </ul>

                {html_overall}
                {html_by_product}
                {html_by_groups}
                </body>
                </html>
                """
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(html, encoding="utf-8")
