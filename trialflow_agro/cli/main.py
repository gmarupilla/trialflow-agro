"""
Typer-based CLI entry point for trialflow-agro.

Commands:
- trialflow-agro fit    → run the analysis pipeline and write results.json
- trialflow-agro report → build a simple HTML report from results.json
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer

from trialflow_agro.pipeline import Pipeline
from trialflow_agro.reporting.report_builder import ReportBuilder

app = typer.Typer(
    name="trialflow-agro",
    help="Reproducible summary workflows for on-farm agricultural trials.",
)


@app.command()
def fit(
    config: Path = typer.Argument(
        ...,
        help="Path to trialflow-agro YAML config file.",
    ),
    out: Optional[Path] = typer.Option(
        None,
        "--out",
        "-o",
        help="Optional override for results directory "
        "(defaults to config.output.directory).",
    ),
) -> None:
    """
    Run the trialflow-agro analysis pipeline.

    This will:
    - load and validate the YAML config
    - load and validate the trial dataset
    - compute overall / per-product / grouped summaries
    - compute basic diagnostics
    - write results.json under the chosen output directory
    """
    typer.echo("[trialflow-agro] Starting fit workflow...")
    typer.echo(f"  Config: {config}")
    if out is not None:
        typer.echo(f"  Output override: {out}")

    pipeline = Pipeline(config_path=config, output_dir=out)
    pipeline.run()

    typer.echo(f"[trialflow-agro] Completed. Results written to: {pipeline.output_dir}")


@app.command()
def report(
    results: Path = typer.Argument(
        Path("results"),
        help="Directory containing results.json (defaults to ./results).",
    ),
    out: Path = typer.Option(
        Path("trialflow-report.html"),
        "--out",
        "-o",
        help="Path for the generated HTML report.",
    ),
) -> None:
    """
    Build a simple HTML report from results.json.

    The report includes:
    - basic dataset diagnostics
    - overall yield summary
    - per-product summaries
    - optional grouped summaries (based on config.model.groups)
    """
    typer.echo("[trialflow-agro] Building report...")
    typer.echo(f"  Results directory: {results}")
    typer.echo(f"  Output file:       {out}")

    builder = ReportBuilder(results_dir=results)
    builder.render(out_path=out)

    typer.echo(f"[trialflow-agro] Report written to: {out}")


def main() -> None:
    """Console script entrypoint."""
    app()
