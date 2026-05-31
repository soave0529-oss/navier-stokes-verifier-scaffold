# Step 138 - Tao 2013 Stage 1 exit value assessment

Date: 2026-05-24

## Scope

Step 138 is a bounded theorem-generation pipeline decision step. It reads the Step 137 Tao 2013
Stage 1 technique card and decides whether the Tao path is worth entering Stage 2.

This step does not add a dashboard, dependency guard, operator index, promotion surface, candidate
YAML, known-theorem row, or blocker discharge.

## Output

- `pipeline/stage1/tao2013_localisation/stage2_value_assessment.md`
- `tests/test_stage1_tao2013_stage2_value_assessment.py`

## Decision

Decision: `GO_LIMITED_TO_ONE_STAGE2_OBSTACLE_TREE`.

Tao 2013 is worth exactly one Stage 2 attempt because it gives a concrete local proof architecture:
finite-energy total-speed control, shrinking radius, Lipschitz cutoff, localised enstrophy, and
local harmonic-analysis control of leakage. The value is not that Tao proves `lemma_0252`; it is
that this proof skeleton makes the pressure/local-energy mismatch precise enough for obstacle-tree
analysis.

## Selected Seed

Selected Stage 2 seed:

- `ckn_pressure_package_plus_tao_local_vorticity_cutoff`

First obstacle:

- `tao_ckn_pressure_local_energy_transfer`

The obstacle asks whether Tao's shrinking-radius local vorticity/enstrophy argument can be modified
to produce, on a smaller parabolic cylinder, a CKN/Lin epsilon-small velocity-pressure-local-energy
package from finite critical parabolic Morrey/vorticity-enstrophy metadata.

Expected first failure point:

- passing from vorticity-local control to pressure and local-energy smallness risks reintroducing
  nonlocal Biot-Savart/Leray-pressure leakage that Tao's proof avoids;
- finite critical Morrey/vorticity-enstrophy metadata may give boundedness without epsilon gain.

## Next Artifact

Recommended next Stage 2 artifact:

- `pipeline/stage2/proposals/tao_ckn_pressure_package.md`

Content should stay bounded to one proposal paragraph and one obstacle-tree pointer. It should not
create candidate YAML, promotion metadata, or another dashboard/freshness/operator layer.

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
- prove epsilon regularity;
- prove compactness/Liouville;
- prove smooth continuation;
- create or promote candidate YAML;
- copy YAML into `track-a-regularity/candidates/`;
- assert a weak-to-smooth upgrade;
- claim a Navier-Stokes solution.

## Verification

Verification is recorded in `logs/step138_tao2013_stage1_exit_value_assessment_20260524.md`.
