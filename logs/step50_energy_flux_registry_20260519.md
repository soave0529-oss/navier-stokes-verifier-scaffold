# Step 50 — Energy-Flux / Onsager Known-Result Comparison

Date: 2026-05-19

Status: complete.

Scope: compare `lemma_0251` against Onsager, Littlewood-Paley energy-flux, LES, energy-equality,
and cascade-locality literature before expert review.

## Artifact

- `docs/KNOWN_ENERGY_FLUX_CRITERIA.md`

## Decision

`lemma_0251` remains `candidate_substrate_high_risk`, now with `automatic_finiteness_risk`.

It is not marked as a known-overlap evaluator failure yet because the current condition is not a
standard Besov/Onsager norm assumption and not a direct energy-equality theorem.

It is also not expert-ready. The main blocker is whether

`sum_N N^{-1} integral_0^T max(Pi_N^LES(t),0) dt < infinity`

is actually automatic from the low-pass energy identity plus the standard energy inequality. If it
is automatic, the condition is too weak to be a serious continuation criterion.

## Sources Checked

- Duchon-Robert inertial/local energy dissipation;
- Cheskidov-Constantin-Friedlander-Shvydkoy Onsager/Littlewood-Paley flux locality;
- Cheskidov-Friedlander-Shvydkoy NSE energy equality;
- Cheskidov-Luo weak-in-time Onsager spaces;
- Dascaliuc-Grujic physical-scale energy cascades and flux locality;
- Drivas-Eyink Onsager singularity theorem for Leray NSE;
- Cheskidov-Dai Littlewood-Paley vorticity regularity criteria.

## Verification

No code changed in this step. Latest verification from Step 49:

- Python tests: `30 passed`.
- Evaluator expected-check matched all 252 candidates.
- Distribution: `falsified 227`, `known_control 12`, `known_control_with_extra_assumption 6`,
  `candidate 7`.

## Next

Step 51 should write `docs/LEMMA_0251_FLUX_BALANCE_AUDIT.md`.
