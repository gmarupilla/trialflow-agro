# Basic Trial Analysis Example

This example demonstrates a minimal end-to-end `trialflow-agro` workflow:

- load a small on-farm trial dataset,
- compute overall and grouped summaries,
- generate diagnostics,
- write a machine-readable `results.json`,
- and build an HTML report.

## Dataset

File: `data.csv`

Each row represents a plot-level observation from a small multi-farm, multi-product trial.

Required columns (as used by trialflow-agro):

- `field_id` – string identifier for the field (e.g., `F101`)
- `farm_id` – farm identifier (e.g., `Farm1`)
- `region` – region label (e.g., `North`, `South`)
- `year` – trial year (integer)
- `product` – product / hybrid identifier (e.g., `Hybrid_A`)
- `yield` – yield in bu/ac

Optional columns shown in this example:

- `treatment` – management treatment (e.g., `standard`, `lowN`)
- `soil_class` – simple soil class (e.g., `Loam`, `Clay`, `Sandy`)
- `lat`, `lon` – approximate field centroid coordinates

These align with the `TrialRow` schema and `REQUIRED_COLUMNS` defined in
`trialflow_agro/data/schema.py`.

## Configuration

File: `config.yml`

This configuration tells `trialflow-agro`:

- where to find the data (`data.path`),
- how to group summaries (`model.groups`),
- and where to write outputs (`output.directory`).

```yaml
data:
  path: examples/basic_trial_analysis/data.csv

model:
  id: basic_trial_summary
  groups: ["product", "region"]
  min_records_per_group: 2

output:
  directory: examples/basic_trial_analysis/output
