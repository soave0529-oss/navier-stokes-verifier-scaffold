# Step 52 — Flux-Balance Risk Evaluator Metadata

Date: 2026-05-19

Status: complete.

Scope: propagate the Step 51 `lemma_0251` flux-balance audit into Track A evaluator metadata and
public candidate registries. This is not a proof of falsehood and not a Navier-Stokes solution
claim.

## Changes

- Added `track-a-regularity/evaluator/checks/flux_balance_risk.py`.
- Wired `flux_balance_risk_check` after `definition_rule_check` in the evaluator.
- Updated `schema.matches_expected` so exact expected statuses such as `needs_review` are checked
  directly, while legacy `pass` / `fail` expectations remain supported.
- Updated `track-a-regularity/candidates/lemma_0251.yaml` expected status to `needs_review`.
- Updated registries:
  - `track-a-regularity/PASSED.md`
  - `docs/FINAL_CANDIDATE_TRIAGE.md`
  - `docs/REMAINING_CANDIDATE_REGISTRY.md`
  - `docs/SUMMARY.md`
  - `docs/ROADMAP_STEPS.md`

## Decision

`lemma_0251` is now a non-failing manual-review item, not an active candidate.

Reason:

- Step 51 derived `Pi_N^LES = dE_N/dt + nu D_N` for the project sign convention.
- Positive project `Pi_N^LES` feeds resolved low-pass energy, whereas usual forward SGS flux has
  the opposite sign.
- The signed integral is energy-controlled, but the positive-part dyadic budget does not supply a
  coercive bridge to enstrophy, BKM control, pressure control, or a critical Besov norm.

Required rewrite before expert review:

```text
Pi_N^forward = - integral grad u_{<=N} : tau_N dx
```

plus a concrete implication from the flux hypothesis to a known smooth-continuation control.

## Verification

```text
.venv/bin/python -m pytest -q
30 passed

.venv/bin/python track-a-regularity/evaluator/run_all.py track-a-regularity/candidates --check-expected
all 252 candidates matched expected evaluator status / first failure

distribution:
candidate 6
falsified 227
known_control 12
known_control_with_extra_assumption 6
needs_review 1
```

## Next Action

Proceed to Step 53: write `docs/LEMMA_0252_PROOF_OBLIGATIONS.md` for the exact parabolic Morrey
candidate before any expert packet. Keep weak, suitable-weak, and smooth solution classes explicit.
