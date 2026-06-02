# Project Status

Updated: 2026-06-02

This repository is a verifier-first research scaffold. It is not a proof of
global regularity or finite-time blow-up for the 3D incompressible
Navier-Stokes equations.

## Current Verification Surface

The public tree is intended to support three conservative checks:

- Python regression tests for candidate-gate behavior, numerical smoke tests,
  and interval-falsifier utilities.
- Candidate evaluator runs against selected YAML fixtures with
  `--check-expected`.
- Lean 4 vocabulary artifacts that track proof obligations without treating
  unfinished formal files as theorem claims.

Recommended local smoke commands:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
bash scripts/verify_public.sh
```

## Promotion Policy

Generated candidates remain blocked by default. A candidate should not be
described as mathematical progress unless it clears the evaluator checks,
matches known-result and scaling constraints, has explicit proof obligations,
and receives independent mathematical review.

## Known Limitations

- Numerical diagnostics are falsifiers and sanity checks, not evidence of a
  proof.
- Natural-language candidate statements are untrusted inputs.
- Lean files are scaffolding unless a file explicitly contains completed
  proofs.
- The public repository excludes large local artifacts, downloaded papers,
  private notes, caches, and external upstream clones.
