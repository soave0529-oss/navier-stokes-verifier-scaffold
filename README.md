# Navier-Stokes Verifier Scaffold

Verifier-first research infrastructure for experimenting with AI-assisted
mathematics on the 3D incompressible Navier-Stokes regularity problem.

This repository **does not solve Navier-Stokes**. It is a scaffold for keeping
candidate mathematical claims honest: candidate lemmas are generated outside the
trusted core, then filtered by syntactic checks, known-result guards, numerical
falsifiers, proof-obligation ledgers, and small Lean artifacts.

## Scope

The default mathematical setting is the periodic 3D incompressible
Navier-Stokes equation on `T^3`, with smooth divergence-free mean-zero initial
data and zero external force.

The repository is organized into three tracks:

- `track-a-regularity`: YAML candidate lemmas plus a Python evaluator for
  scaling, Galilean invariance, endpoint pitfalls, convex-integration guards,
  known-result overlap, and promotion blockers.
- `track-b-blowup`: a small NumPy pseudo-spectral solver and diagnostics used
  as falsifiers or smoke tests, not as proof.
- `track-c-formal`: Lean 4 vocabulary and proof-obligation scaffolding for
  formalizing small pieces of the surrounding infrastructure.

## Non-Claims

- No proof of global regularity or blow-up is claimed.
- Numerical output is diagnostic only.
- Natural-language candidate statements are not accepted as proof.
- Lean files in this repository are infrastructure/vocabulary artifacts unless
  they explicitly contain completed proofs.
- Generated candidates are blocked by default until they pass the promotion
  gate and external review criteria.

## Quick Start

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest -q
```

Run the seed candidate evaluator:

```bash
PYTHONPATH=track-a-regularity/evaluator \
  python track-a-regularity/evaluator/run_all.py \
  track-a-regularity/candidates/lemma_0001.yaml \
  track-a-regularity/candidates/lemma_0005.yaml \
  --check-expected
```

Run a short Taylor-Green smoke test:

```bash
PYTHONPATH=track-b-blowup/solver pytest -q tests/test_solver_taylor_green.py
```

For the current public verification surface and promotion policy, see
[`docs/STATUS.md`](docs/STATUS.md).

## What Was Excluded

This public tree is a sanitized extraction. It intentionally excludes large
local artifacts from the original research workspace:

- downloaded papers and PDFs;
- large numerical runs and plots;
- local logs and reproducibility bundles;
- virtual environments and caches;
- local absolute paths and private notes;
- upstream repository clones.

Where upstream formalization projects influenced the design, this repository
links or documents them instead of vendoring their full source trees.

## Layout

```text
docs/                         Selected public research notes and gate specs
tests/                        Small regression and smoke tests
track-a-regularity/           Candidate evaluator and candidate fixtures
track-b-blowup/               Numerical diagnostics/falsifier code
track-c-formal/lean/          Lean vocabulary and proof-obligation scaffolding
```

## License

The original code and documentation in this sanitized repository are released
under the MIT License. External papers, mathematical results, and upstream
projects referenced in documentation remain under their own terms.
