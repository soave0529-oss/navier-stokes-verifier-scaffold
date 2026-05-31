# Step 55 — Duhamel Formal-Only Evaluator Metadata

Date: 2026-05-19

Status: complete.

Scope: propagate the Step 48/46 decision that the remaining critical Duhamel bilinear variants are
formal-only vocabulary, not active theorem candidates. This is not a proof of falsehood and not a
Navier-Stokes solution claim.

## Changes

- Added `track-a-regularity/evaluator/checks/duhamel_formal_only.py`.
- Wired `duhamel_formal_only_check` after the parabolic Morrey obligation check.
- Updated expected status for:
  - `lemma_0209`
  - `lemma_0219`
  - `lemma_0229`
  - `lemma_0239`
  - `lemma_0249`
- Updated registries and summaries:
  - `track-a-regularity/PASSED.md`
  - `docs/FINAL_CANDIDATE_TRIAGE.md`
  - `docs/REMAINING_CANDIDATE_REGISTRY.md`
  - `docs/SUMMARY.md`
  - `docs/ROADMAP_STEPS.md`

## Decision

The critical Duhamel family is now non-failing `needs_review`, not active `candidate`.

Reason:

- The statements say only that a mild Duhamel bilinear term is bounded in a critical space-time norm.
- They do not define the real NSE bilinear operator, Leray projection, time integral, target space,
  or critical indices.
- Step 46 already extracted the useful portion into finite Lean vocabulary.

## Verification

```text
.venv/bin/python -m pytest -q
31 passed

.venv/bin/python track-a-regularity/evaluator/run_all.py track-a-regularity/candidates --check-expected
all 252 candidates matched expected evaluator status / first failure

distribution:
candidate 0
falsified 227
known_control 12
known_control_with_extra_assumption 6
needs_review 7
```

## Next Action

Proceed to Step 56: choose a new path now that no active candidate remains. Recommended bounded
choice is a stricter Track A generation spec that forbids formal-only placeholders and requires
exact function spaces plus known-result separation before a candidate can be emitted.
