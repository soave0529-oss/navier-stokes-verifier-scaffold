#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

PYTHON="${PYTHON:-python3}"

"$PYTHON" -m pytest -q

PYTHONPATH=track-a-regularity/evaluator \
  "$PYTHON" track-a-regularity/evaluator/run_all.py \
  track-a-regularity/candidates/lemma_0001.yaml \
  track-a-regularity/candidates/lemma_0005.yaml \
  --check-expected
