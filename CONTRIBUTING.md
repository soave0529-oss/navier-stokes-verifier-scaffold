# Contributing

Contributions are welcome if they preserve the verifier-first contract.

## Ground Rules

- Do not claim that this repository solves Navier-Stokes.
- Keep candidate lemmas blocked by default unless the promotion gate says
  otherwise.
- Add tests for new evaluator checks, solver diagnostics, or Lean vocabulary.
- Do not vendor PDFs, downloaded paper archives, large numerical runs, or
  upstream repository clones.
- Cite mathematical sources in documentation when adding known-result guards.

## Development

```bash
python -m pip install -e ".[dev]"
bash scripts/verify_public.sh
```

Lean changes should be checked from `track-c-formal/lean` with the local Lean
toolchain if available.
