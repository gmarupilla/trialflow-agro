"""
Typer-based CLI entry point for trialflow-agro.

This module defines the CLI structure and top-level commands.
The actual analysis pipeline is not implemented yet; this
provides the interface and basic behavior for:

- trialflow-agro fit
- trialflow-agro report
"""

from pathlib import Path
import typer

app = typer.Typer(
    name="trialflow-agro",
    help="Reproducible workflow for analyzing on-farm agricultural trials.",
)


@app.command()
def fit(
    config: Path = typer.Option(
        ...,
        "--config",
        "-c",
        exists=True,
        readable=True,
        help="Path to the YAML configuration file.",
    ),
    data: Path = typer.Option(
        ...,
        "--data",
        "-d",
        exists=True,
        readable=True,
        help="Path to the trial dataset (CSV or Parquet).",
    ),
    out: Path = typer.Option(
        Path("results"),
        "--out",
        "-o",
        help="Directory to write analysis outputs.",
    ),
) -> None:
    """
    Run the trial analysis workflow.

    Steps (to be implemented later):
    - Load and validate config
    - Load trial dataset
    - Build and fit model
    - Save results to output directory
    """
    typer.echo("Starting trialflow-agro fit workflow...\n")

    typer.echo(f"Config file: {config}")
    typer.echo(f"Dataset:     {data}")
    typer.echo(f"Output dir:  {out}")

    out.mkdir(parents=True, exist_ok=True)

    typer.echo("\n[NOTE] Analysis pipeline is not implemented yet.")
    typer.echo("       This command currently runs as a placeholder.\n")


@app.command()
def report(
    results: Path = typer.Option(
        Path("results"),
        "--results",
        "-r",
        exists=True,
        file_okay=False,
        dir_okay=True,
        readable=True,
        help="Directory containing analysis results.",
    ),
    out: Path = typer.Option(
        Path("report.html"),
        "--out",
        "-o",
        help="Path to the generated report file.",
    ),
    format: str = typer.Option(
        "html",
        "--format",
        "-f",
        help="Output format for the report (html, md, etc.).",
    ),
) -> None:
    """
    Generate a report from previously computed results.

    Steps (to be implemented later):
    - Load saved model/inference results
    - Compute summaries + diagnostics
    - Render plots & tables
    - Export final report
    """
    typer.echo("Starting trialflow-agro report workflow...\n")

    typer.echo(f"Results directory: {results}")
    typer.echo(f"Output file:       {out}")
    typer.echo(f"Format:            {format}")

    typer.echo("\n[NOTE] Report generation is not implemented yet.")
    typer.echo("       This command currently runs as a placeholder.\n")


def main() -> None:
    """
    Entry point for `trialflow-agro` console script.
    """
    app()
