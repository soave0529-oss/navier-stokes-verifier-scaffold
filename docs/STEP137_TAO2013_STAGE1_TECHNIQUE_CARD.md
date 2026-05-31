# Step 137 - Tao 2013 Stage 1 technique card

Date: 2026-05-24

## Scope

Step 137 starts the theorem-generation pipeline's Stage 1 paper-digest path. It follows the
user's requested correction away from dashboard/freshness expansion and toward paper technique
digests.

This step does not add a dashboard, dependency guard, operator index, promotion surface, candidate
YAML, or known-theorem discharge.

## Output

- `pipeline/stage1/tao2013_localisation/technique_card.md`
- `tests/test_stage1_tao2013_technique_card.py`

## Source Read

Local source:

- `papers/blockers/cross_cutting/1108.1165_tao2013_localisation_compactness.pdf`

Relevant Tao 2013 anchors recorded in the card:

- The abstract and introduction identify localised energy and enstrophy estimates as the paper's
  main new tools for comparing global-regularity formulations.
- Proposition 9.1 gives a finite-energy `L1_t L-infinity_x` total-speed bound used by the
  localisation argument.
- Theorem 10.1 gives the localised enstrophy estimate from small local initial
  vorticity/curl-force input plus a short-time condition.
- The proof uses a shrinking radius, a Lipschitz cutoff, localised enstrophy, a pigeonhole boundary
  radius, and local harmonic-analysis estimates to avoid nonlocal leakage.
- Proposition 10.7 upgrades local enstrophy control to higher local regularity after the
  Theorem 10.1 hypotheses are already present.
- Corollary 11.1 and Remark 11.2 show why the estimate controls complete almost-smooth solutions
  but does not solve global regularity or rule out bounded-region turbulence.

## Stage 1 Digest Result

The card records Tao 2013 as a high-value technique card for future recombination:

- core technique: localised energy/enstrophy with shrinking transport cutoff;
- norm bridge: small local initial vorticity/curl-force plus finite energy and short time gives
  local enstrophy and vorticity-gradient control;
- sharpness point: finite local critical size is not the same as small local input;
- `lemma_0252` distance: adjacent in vocabulary, but not a finite-bound-to-smallness,
  compactness/Liouville, or smooth-continuation discharge.

## Stage 2 Seeds

The card records four possible recombination seeds for later human selection:

1. Vasseur De Giorgi self-improvement plus Tao's shrinking localised-enstrophy cutoff.
2. Lei-Ren regular-strip/pigeonhole methods plus Tao boundary-radius pigeonhole.
3. CKN/Lin pressure-local-energy package plus Tao local vorticity cutoff.
4. ESS/KNSS backward-uniqueness templates plus Tao exterior/localisation compactness.

These are not candidate lemmas. They are Stage 2 prompts for obstacle analysis if the user chooses
to continue the theorem-generation pipeline.

## Canonical State

- `lemma_0252` remains `candidate_status=needs_review`.
- `active_candidate=false`.
- No existing known-theorem row was turned into `resolvable_known`.
- No process gate was opened.
- No candidate was emitted or promoted.
- No blocker was discharged.
- Dashboard additions: `0`.

## Non-claims

This step does not:

- claim Tao 2013 proves `lemma_0252`;
- prove finite-bound-to-smallness;
- prove compactness/Liouville;
- prove smooth continuation;
- create or promote candidate YAML;
- copy YAML into `track-a-regularity/candidates/`;
- assert a weak-to-smooth upgrade;
- claim a Navier-Stokes solution.

## Verification

Verification is recorded in `logs/step137_tao2013_stage1_technique_card_20260524.md`.

Current verification state:

- Focused Stage 1 card tests: `3 passed`.
- Focused Tao/source-read compatibility tests: `22 passed`.
- All-candidate evaluator check matched all 252 candidates in `logs/step137_eval_expected_20260524`.
- Default v4 preflight: `checked=0 skipped=252 blocked=0`.
- Full Python suite: `497 passed`.
- Track C `lake build` and full reproducibility smoke were not rerun for this card-only change.
