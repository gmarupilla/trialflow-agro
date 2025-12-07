#!/usr/bin/env bash
set -euo pipefail

# Run from repo root:
#   bash examples/basic_trial_analysis/run.sh

CONFIG="examples/basic_trial_analysis/config.yml"
OUT_DIR="examples/basic_trial_analysis/output"
REPORT_PATH="examples/basic_trial_analysis/report.html"

echo "[basic_trial_analysis] Running trialflow-agro fit..."
trialflow-agro fit "${CONFIG}" --out "${OUT_DIR}"

echo "[basic_trial_analysis] Building report..."
trialflow-agro report "${OUT_DIR}" --out "${REPORT_PATH}"

echo "[basic_trial_analysis] Done."
echo "  Results: ${OUT_DIR}/results.json"
echo "  Report : ${REPORT_PATH}"
