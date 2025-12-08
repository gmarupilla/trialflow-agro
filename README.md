# TrialFlowAgro

**A lightweight, reproducible workflow for analyzing agricultural field-trial datasets.**

`trialflow-agro` provides a configuration-driven, fully reproducible pipeline for loading, validating, summarizing, and reporting on agricultural field-trial data. It establishes a standardized schema for plot-level or field-level datasets, enforces validation using Pydantic, and produces machine-readable outputs suitable for downstream modeling or research workflows.

This toolkit is designed as a reproducible foundation for agricultural research, industry R&D,
and future Bayesian/hierarchical modeling extensions.

---

## ✨ Key Features

- **Validated data loading** using a Pydantic schema (`TrialRow`) with explicit required columns
- **Config-driven execution** via YAML files (no manual notebook wiring)
- **Summary inference** including overall and grouped statistical summaries
- **Dataset diagnostics** (row counts, missing values, unique categories, etc.)
- **Machine-readable results** (`results.json`)
- **HTML report generation** for reproducible communication
- **CLI interface** using Typer (`trialflow-agro fit`, `trialflow-agro report`)
- **Extensible modular design** ready for Bayesian workflows (PyMC/Stan)

---

## 📦 Installation

### From PyPI

```bash
pip install trialflow-agro
````

### From source

```bash
git clone https://github.com/gmarupilla/trialflow-agro
cd trialflow-agro
pip install -e .
```

---

## 📁 Project Structure

```
trialflow_agro/
├── cli/          # Command-line interface
├── config/       # YAML config schema + loader
├── data/         # Data loading + validation (Pydantic TrialRow)
├── inference/    # Summary inference engine
├── models/       # Model definitions (simple summary model for now)
├── reporting/    # HTML report builder (Jinja2)
└── examples/     # Fully runnable sample analysis
```

---

## 🧪 Required Dataset Schema

Your CSV must contain the following required columns:

| Column   | Type   | Description                       |
| -------- | ------ | --------------------------------- |
| field_id | string | Identifier for field/block        |
| farm_id  | string | Farm identifier                   |
| region   | string | Region label                      |
| year     | int    | Trial year                        |
| product  | string | Product/hybrid/variety identifier |
| yield    | float  | Yield value for the plot/field    |

Optional fields (automatically handled):

```
treatment, variety, soil_class, lat, lon
```

---

## ⚙️ Configuration File (YAML)

Example `config.yml`:

```yaml
data:
  path: demo.csv
  response_column: yield

model:
  group_by:
    - product
    - region

output:
  directory: results
```

This drives the entire pipeline — fully reproducible, no ad-hoc notebooks.

---

## 🚀 Running TrialFlowAgro

### 1. Run the analysis

```bash
trialflow-agro fit examples/basic_trial_analysis/config.yml \
  --out examples/basic_trial_analysis/output
```

### 2. Generate an HTML report

```bash
trialflow-agro report examples/basic_trial_analysis/output \
  --out examples/basic_trial_analysis/report.html
```

### 3. Output structure

```text
output/
├── results.json
└── report.html
```

`results.json` includes:

* resolved config
* dataset diagnostics
* summary statistics
* grouped summaries

---

## 📘 Example Workflow

A complete, runnable example is located in:

```
examples/basic_trial_analysis/
```

Includes:

* sample `demo.csv`
* ready-to-use `config.yml`
* expected output folder
* HTML report generation

---

## 🧱 Development

Install dependencies:

```bash
make dev
```

Run tests:

```bash
make test
```

Format + lint:

```bash
make lint
```


## 🙏 Acknowledgements

Built on the scientific Python ecosystem:

* NumPy
* pandas
* GeoPandas
* Pydantic
* Typer
* Jinja2

---
