# Step 53 — Parabolic Morrey Proof Obligations

Date: 2026-05-19

Status: complete.

Scope: write the proof-obligation breakdown for `lemma_0252`, the exact parabolic Morrey localized
enstrophy candidate. This is not a proof and not a Navier-Stokes solution claim.

## Artifact

- `docs/LEMMA_0252_PROOF_OBLIGATIONS.md`

## Decision

`lemma_0252` remains blocked from expert review.

Current call:

```text
candidate_substrate_high_risk
blocked_pending_compactness_or_smallness_mechanism
```

The memo found no current route from finite scale-critical local enstrophy boundedness to CKN-style
epsilon smallness. Promotion requires either:

- a compactness/Liouville theorem for bounded-envelope blow-up limits, or
- a rewrite with epsilon smallness plus pressure/local-energy quantities, likely moving it toward
  known partial-regularity criteria.

## Obligations Identified

- admissible backward cylinder convention near `t=0`;
- local vorticity-to-gradient/CKN quantity bridge;
- pressure control;
- finite-bound-to-smallness mechanism;
- blow-up compactness and Liouville/backward-uniqueness branch;
- smooth continuation bridge from partial regularity to classical continuation;
- small Lean target limited to obligation vocabulary, not CKN formalization.

## Verification

No code changed in this step. Step 52 verification carries forward:

- Python tests: `30 passed`.
- Evaluator expected-check matched all 252 candidates.
- Distribution: `falsified 227`, `known_control 12`, `known_control_with_extra_assumption 6`,
  `needs_review 1`, `candidate 6`.

## Next

Step 54 should encode the `lemma_0252` blocker in public registries and optionally evaluator
metadata as non-failing `needs_review`.
