# Lemma 0252 Local-Energy Formal Map

Date: 2026-05-19

Status: Step 63 complete.

## Purpose

This note connects the Step 62 Lean artifact
`NavierStokesProgram/LocalEnergy.lean` to the proof obligations for `lemma_0252`.

It is a map from analytic blockers to formal vocabulary. It is not a proof, not a CKN/ESS
formalization, and not a Navier-Stokes regularity claim.

## Current Candidate Status

`lemma_0252` remains:

```text
expected_evaluator.status: needs_review
promotion gate: blocked_pending_compactness_or_smallness_mechanism
active candidate: no
```

Do not send it to experts and do not regenerate it as an active candidate without a new mechanism.

## Obligation-to-Vocabulary Map

| proof obligation | current Lean vocabulary | covered? | remaining gap |
|---|---|---:|---|
| Cylinder admissibility | `ParabolicCylinder`, `LocalEnergyCutoff.cylinder` | partial | no theorem that the cylinder lies inside `[0,T)` or handles initial-time truncation |
| Local vorticity to CKN quantities | `LocalEnergySample.viscousDissipation`, `LocalEnstrophySample.normalizedEnstrophy` | vocabulary only | no curl-to-gradient localization, no cutoff error identity, no harmonic/boundary decomposition |
| Pressure control | `LocalPressureData` | vocabulary only | no pressure equation, no Calderon-Zygmund/local-nonlocal decomposition theorem, no pressure norm estimate |
| Finite bound to smallness | none beyond finite sample records | no | no monotonicity, self-improvement, or compactness mechanism converting bounded critical mass to epsilon smallness |
| Blow-up compactness and Liouville branch | `SmoothToLocalEnergyAudit` names class routing only | no | no ancient suitable limit, no compactness theorem, no Liouville/backward-uniqueness theorem |
| Smooth continuation bridge | `SmoothToLocalEnergyAudit.noWeakToSmoothUpgradeClaim`, `SolutionClasses.ExtendsSmoothlyPast` | guardrail only | no bridge from local regularity to BKM/Serrin/high-Sobolev continuation |

## Interpretation

The Step 62 artifact is useful because it prevents three common errors:

1. treating local energy inequality metadata as if it were a smooth continuation theorem;
2. hiding pressure/local-nonlocal conventions inside an informal phrase;
3. silently switching between smooth classical, Leray-Hopf, suitable weak, and ancient-limit
   solution classes.

It does not close any analytic obligation. The highest-value remaining gap is still the
finite-bound-to-smallness or compactness/Liouville mechanism.

## Next Formal Target

The next Track C increment should not formalize CKN. A bounded target is:

- a small proof-obligation graph vocabulary connecting `ParabolicMorreyHypothesis`,
  `FiniteLocalEnergyInequality`, `LocalPressureData`, and `SmoothToLocalEnergyAudit`;
- accessor lemmas that expose which obligations are assumptions versus proved facts;
- no theorem from finite local enstrophy to smooth continuation.

This can support future review without reclassifying `lemma_0252` as an active candidate.
