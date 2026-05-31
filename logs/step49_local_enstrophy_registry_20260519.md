# Step 49 — Local Enstrophy / Parabolic Morrey Known-Result Comparison

Date: 2026-05-19

Status: complete.

Scope: compare `lemma_0252` against CKN/ESS/local-enstrophy and local-Morrey regularity
criteria before expert review.

## Artifact

- `docs/KNOWN_LOCAL_ENSTROPHY_CRITERIA.md`

## Decision

`lemma_0252` remains `candidate_substrate_high_risk`.

It is not marked as a known-overlap evaluator failure yet because the statement assumes finite
scale-critical local enstrophy, while CKN/local-Morrey criteria usually require epsilon smallness,
pressure/local-energy structure, or different velocity critical norms.

It is also not expert-ready. Promotion requires:

- a local vorticity-to-gradient bridge;
- pressure/local energy control;
- a finite-bound-to-smallness or compactness/Liouville mechanism;
- explicit separation of smooth, Leray-Hopf, and suitable weak solution classes.

## Sources Checked

- Fefferman Clay statement / CKN summary;
- Caffarelli-Kohn-Nirenberg 1982;
- Lin 1998;
- Escauriaza-Seregin-Sverak endpoint and backward-uniqueness sources;
- Seregin scale-invariant quantity literature;
- Grujic-Xu dynamically restricted local Morrey criterion;
- Barker-Prange quantitative regularity via spatial concentration.

## Verification

No code changed in this step. Latest carried-forward verification:

- Python tests: `30 passed`.
- Evaluator expected-check matched all 252 candidates.
- Distribution: `falsified 227`, `known_control 12`, `known_control_with_extra_assumption 6`,
  `candidate 7`.

## Next

Step 50 should write `docs/KNOWN_ENERGY_FLUX_CRITERIA.md` for `lemma_0251`.
