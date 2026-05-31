# Step 54 — Parabolic Morrey Evaluator Metadata

Date: 2026-05-19

Status: complete.

Scope: propagate the Step 53 `lemma_0252` proof-obligation blocker into Track A evaluator metadata
and public candidate registries. This is not a proof of falsehood and not a Navier-Stokes solution
claim.

## Changes

- Added `track-a-regularity/evaluator/checks/parabolic_morrey_obligation.py`.
- Wired `parabolic_morrey_obligation_check` after `flux_balance_risk_check`.
- Updated `track-a-regularity/candidates/lemma_0252.yaml` expected status to `needs_review`.
- Updated registries and summaries:
  - `track-a-regularity/PASSED.md`
  - `docs/FINAL_CANDIDATE_TRIAGE.md`
  - `docs/REMAINING_CANDIDATE_REGISTRY.md`
  - `docs/KNOWN_LOCAL_ENSTROPHY_CRITERIA.md`
  - `docs/SUMMARY.md`
  - `docs/ROADMAP_STEPS.md`

## Decision

`lemma_0252` is now a non-failing manual-review item, not an active candidate.

Reason:

- Step 53 found no current path from finite critical local enstrophy boundedness to CKN-style
  epsilon smallness.
- The statement lacks pressure/local-energy control.
- A hard compactness/Liouville branch would be needed to keep the finite-envelope statement novel.

## Verification

```text
.venv/bin/python -m pytest -q
30 passed

.venv/bin/python track-a-regularity/evaluator/run_all.py track-a-regularity/candidates --check-expected
all 252 candidates matched expected evaluator status / first failure

distribution:
candidate 5
falsified 227
known_control 12
known_control_with_extra_assumption 6
needs_review 2
```

## Next Action

Proceed to Step 55: clean up the remaining critical Duhamel formal-only family. Either mark it as
non-failing review/formal-only in evaluator metadata, or choose one exact function-space rewrite if
there is a credible theorem route.
