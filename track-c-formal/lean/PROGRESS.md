# Track C Formal Progress

## 2026-05-19 - Step 18 heat semigroup artifact

Artifact: `NavierStokesProgram/HeatSemigroup.lean`

This is the buildable Lean counterpart of the roadmap's `02_heat_semigroup.lean` option. The numeric
prefix was not used in the actual module name because Lean module identifiers should be regular Lean
identifiers, and a leading digit is not a safe module component.

### Scope

- Defines `FourierMode3 := Fin 3 → ℤ`.
- Defines `modeSq k = ∑ i, (k i : ℝ)^2`.
- Defines the linear heat multiplier `exp(-ν t |k|^2)`.
- Proves small closed lemmas:
  - `modeSq_nonneg`
  - `heatMultiplier_zero_time`
  - `heatMultiplier_zero_viscosity`
  - `heatMultiplier_pos`
  - `heatMultiplier_nonneg`
  - `heatMultiplier_add_time`
  - `heatStep_zero_time`
  - `heatStep_add_time`

### What this does not prove

- No Navier-Stokes regularity statement.
- No Leray projector.
- No nonlinear transport term.
- No weak solution or Leray-Hopf energy inequality.
- No quotient torus geometry.

### Dependency inventory

- `Mathlib.Analysis.SpecialFunctions.Exp`
- `Mathlib.Algebra.BigOperators.Group.Finset.Basic`

### Next formal options

- Add a finite-mode `l2Energy` and prove heat-step energy monotonicity under `ν ≥ 0`, `t ≥ 0`.
- Add a Leray-projector statement skeleton only after deciding the finite-dimensional vector API.
- Avoid full weak energy inequality until integration and function-space foundations are chosen.

## 2026-05-19 - Step 25 solution class vocabulary artifact

Artifact: `NavierStokesProgram/SolutionClasses.lean`

### Scope

- Defines separate placeholders for:
  - `SmoothClassicalSolution`
  - `WeakDistributionalSolution`
  - `LerayHopfSolution`
  - `SuitableWeakSolution`
- Adds a one-way forgetful map `SmoothClassicalSolution.toWeak`.
- Keeps smooth continuation typed only for smooth classical placeholders.
- Keeps weak uniqueness as a separate proposition.
- Proves tiny field/projection lemmas with no `sorry`.

### Why this artifact

Step 24's BV/convex-integration catalog makes weak/smooth class separation a hard guardrail. This file
turns that guardrail into local Lean vocabulary so future promoted statements do not silently treat weak
solutions as smooth ones.

### What this does not prove

- No existence theorem.
- No uniqueness theorem.
- No regularity upgrade theorem.
- No Leray-Hopf energy inequality theorem beyond carrying a placeholder field.

## 2026-05-19 - Step 38 spectral-tail vocabulary artifact

Artifact: `NavierStokesProgram/SpectralTail.lean`

### Scope

- Defines finite-mode `spectralEnergy`.
- Defines finite-mode `spectralTail` over modes satisfying `cutoffSq <= |k|^2`.
- Proves nonnegativity for both finite sums.
- Adds a `SpectralTailBound` record for diagnostic vocabulary.

### Why this artifact

Step 29 listed spectral-tail vocabulary as next-quarter infrastructure. This file gives Track C a
small buildable target that can later connect to shell projectors and Track B spectrum diagnostics
without asserting a regularity theorem.

### What this does not prove

- No spectral-tail regularity criterion.
- No implication from numerical decay to smooth continuation.
- No Littlewood-Paley theory or torus quotient geometry.
- No Navier-Stokes theorem beyond finite-mode bookkeeping vocabulary.

### Verification

- Local `lake build` passed with `1873 jobs`.
- Python regression suite passed with `27 passed` during the same step.

## 2026-05-19 - Step 42 shell-projector vocabulary artifact

Artifact: `NavierStokesProgram/ShellProjector.lean`

### Scope

- Defines finite `lowModeSet` and toy scalar-state `lowProject`.
- Adds small membership and idempotence lemmas for the finite projector.
- Defines `ShellProjector` and finite `shellEnergy`.
- Defines scalar `positivePart`, `FluxSample`, and `DyadicFluxBudget` with normalization exponent
  fixed to `alpha = 1`.
- Proves nonnegativity for positive flux samples and finite dyadic budget values.

### Why this artifact

`lemma_0251` uses `P_{<=N}`, positive `Pi_N^LES`, and dyadic `N^{-1}` summability. This artifact
keeps the finite bookkeeping vocabulary buildable before any attempt at true Littlewood-Paley,
tensor, or LES-flux formalization.

### What this does not prove

- No Littlewood-Paley theorem.
- No vector-valued Fourier projector.
- No nonlinear energy flux identity.
- No implication from dyadic flux summability to smooth continuation.

### Verification

- Local `lake build` passed with `1874 jobs` after adding the root import.

## 2026-05-19 - Step 43 parabolic-cylinder vocabulary artifact

Artifact: `NavierStokesProgram/ParabolicCylinder.lean`

### Scope

- Defines a placeholder backward parabolic cylinder with center, top time, radius, and periodic
  lift convention.
- Defines beta=1 scale factor `r^{-1}`.
- Defines `LocalEnstrophySample`, finite `FiniteParabolicMorreyEnvelope`, and a
  `ParabolicMorreyHypothesis` typed over `SmoothClassicalSolution`.
- Proves small nonnegativity and bound-access lemmas.

### Why this artifact

`lemma_0252` uses periodic cylinders, beta=1 localized enstrophy, and a smooth-class continuation
conclusion. This artifact keeps those components typed without asserting the hard analytic
supremum or continuation theorem.

### What this does not prove

- No torus ball or periodic lift geometry theorem.
- No curl/vorticity definition.
- No supremum over all centers, times, and radii.
- No Navier-Stokes regularity criterion.

### Verification

- Local `lake build` passed with `1875 jobs` after adding the root import.
- Python regression suite passed with `29 passed`.
- Evaluator `--check-expected` matched all 252 candidates.

## 2026-05-19 - Step 46 Duhamel bilinear vocabulary artifact

Artifact: `NavierStokesProgram/DuhamelBilinear.lean`

### Scope

- Defines a placeholder `BilinearStateMap` on toy scalar Fourier states.
- Adds a toy `pointwiseBilinear` sanity-check map and zero-input lemmas.
- Defines finite `DuhamelSample` records with lag, nonnegative quadrature weight, and two states.
- Defines `sampleContribution` as weighted heat evolution of a bilinear sample.
- Defines finite `FiniteDuhamelBilinear` sums and finite-mode energy.
- Defines `CriticalDuhamelBound` as a typed placeholder that forces future statements to name a
  critical-space convention.

### Why this artifact

The round-3 critical Duhamel bilinear family is promising as formal vocabulary but too broad as a
Track A regularity candidate. This file keeps the useful mild-form bookkeeping while avoiding any
continuation theorem.

### What this does not prove

- No Navier-Stokes bilinear operator.
- No Leray projector.
- No time integral or Bochner integration theorem.
- No critical-space estimate.
- No smooth continuation theorem.

### Verification

- Local `lake build` passed with `1876 jobs`.
- Python regression suite passed with `30 passed`.
- Evaluator `--check-expected` matched all 252 candidates.

## 2026-05-19 - Step 57 candidate-generation gate vocabulary artifact

Artifact: `NavierStokesProgram/CandidateGate.lean`

### Scope

- Defines solution-class tags for smooth classical, weak distributional, Leray-Hopf, suitable weak,
  and ancient blow-up-limit placeholders.
- Defines `GenerationAudit` fields matching the Step 56 v4 generation spec:
  exact quantity definitions, exact function spaces, known-result separation, proof route, and
  solution-class bridge.
- Defines `CandidateShell` and `EmitReady`.
- Proves small projection lemmas showing `EmitReady` exposes each audit field and preserves the
  source/target solution class.

### Why this artifact

Step 55 left zero active Track A candidates. Step 56 therefore tightened the generation contract.
This artifact records that contract in Lean vocabulary so future promoted candidates can depend on
explicit audit structure instead of prose-only discipline.

### What this does not prove

- No Navier-Stokes regularity theorem.
- No analytic validation of any audit field.
- No known-result separation proof.
- No weak-to-smooth upgrade.

### Verification

- Local `lake build` passed with `1877 jobs`.
- Python regression suite passed with `34 passed`.
- Evaluator `--check-expected` matched all 252 candidates.

## 2026-05-19 - Step 58 candidate-gate examples and no-seed decision

Artifact: `NavierStokesProgram/CandidateGateExamples.lean`

### Scope

- Adds a same-class toy candidate shell with a complete v4 audit and proves it satisfies
  `EmitReady`.
- Adds an incomplete-audit toy shell and proves it cannot satisfy `EmitReady`.
- Adds a Leray-Hopf-to-smooth toy shell and proves it cannot satisfy `EmitReady`, even with a
  complete audit.

### Why this artifact

Step 58 had to decide whether to emit one v4 seed candidate. The current Track A pool has no
credible exact proof route after the flux-balance, parabolic-Morrey, Duhamel, critical-space, and
geometric known-result audits. Instead of forcing a candidate, this file strengthens the formal
metadata gate with buildable examples.

### What this does not prove

- No Navier-Stokes regularity theorem.
- No analytic audit field.
- No weak-to-smooth upgrade theorem.
- No new Track A candidate.

### Verification

- Local `lake build` passed with `1878 jobs`.
- Python regression suite passed with `34 passed`.
- Evaluator `--check-expected` matched all 252 candidates.

## 2026-05-19 - Step 62 local-energy vocabulary artifact

Artifact: `NavierStokesProgram/LocalEnergy.lean`

### Scope

- Defines placeholder pressure metadata for local/nonlocal pressure conventions.
- Defines local-energy cutoff metadata attached to a finite parabolic cylinder.
- Defines finite local-energy samples with left and right side bookkeeping.
- Defines `FiniteLocalEnergyInequality` over `SuitableWeakSolution` and proves small accessor
  lemmas for sample inequalities and the suitable-weak local energy field.
- Adds `SmoothToLocalEnergyAudit` metadata to keep smooth-class and suitable-weak routes explicit.

### Why this artifact

The remaining parabolic-Morrey/local-enstrophy blocker depends on CKN/ESS-style local energy,
pressure, suitable weak solutions, and smooth-continuation class separation. This file creates a
small buildable vocabulary for that interface without generating a new Track A candidate.

### What this does not prove

- No epsilon-regularity theorem.
- No pressure estimate.
- No CKN/ESS theorem.
- No weak-to-smooth upgrade.
- No Navier-Stokes regularity theorem.

### Verification

- Local `lake build` passed with `1879 jobs`.
- Python regression suite passed with `37 passed`.
- Evaluator `--check-expected` matched all 252 candidates.
- v4 preflight returned `summary: checked=0 skipped=252 blocked=0`.

## 2026-05-19 - Step 64 proof-obligation graph vocabulary artifact

Artifact: `NavierStokesProgram/ProofObligationGraph.lean`

### Scope

- Defines `Lemma0252Obligation` nodes for the parabolic-Morrey/local-energy route.
- Defines `ObligationStatus` and `ObligationNode` metadata.
- Defines `Lemma0252LocalEnergyGraph` connecting a `ParabolicMorreyHypothesis` to optional
  `FiniteLocalEnergyInequality` metadata and explicit analytic blocker propositions.
- Adds `step64Node` and `step64GraphSkeleton`, where finite-bound-to-smallness,
  compactness/Liouville, and smooth-continuation mechanisms are intentionally `False`.
- Proves small accessor/blocker lemmas for the skeleton.

### Why this artifact

Step 63 mapped `lemma_0252` proof obligations in prose. This file makes that map buildable and
machine-checkable as graph metadata while preserving the fact that the hard analytic mechanisms
are absent.

### What this does not prove

- No epsilon-regularity theorem.
- No pressure estimate.
- No compactness or Liouville theorem.
- No weak-to-smooth upgrade.
- No Navier-Stokes regularity theorem.

### Verification

- Local `lake build` passed with `1880 jobs`.
- Python regression suite passed with `37 passed`.
- Evaluator `--check-expected` matched all 252 candidates.
- v4 preflight returned `summary: checked=0 skipped=252 blocked=0`.

## 2026-05-19 - Step 67 candidate-obligation bridge vocabulary artifact

Artifact: `NavierStokesProgram/CandidateObligationBridge.lean`

### Scope

- Defines `CandidateGraphAudit`, pairing a `CandidateShell` with a
  `Lemma0252LocalEnergyGraph`.
- Defines `GraphReady` and `EmitReadyWithGraph`.
- Adds accessor lemmas showing graph-backed emit-readiness exposes:
  - ordinary v4 `proofRoute`;
  - ordinary v4 `solutionClassBridge`;
  - absence of graph promotion blockers;
  - graph-level proof-route and solution-class discharges.
- Adds `step67GraphAudit`, a conservative skeleton based on `step64GraphSkeleton` that still
  blocks promotion.

### Why this artifact

The v4 candidate gate and the `lemma_0252` proof-obligation graph were separate. This bridge makes
their relationship explicit: a future candidate needs both ordinary metadata and graph-level
blocker discharge before it can be treated as graph-backed emit-ready.

### What this does not prove

- No candidate correctness theorem.
- No epsilon-regularity theorem.
- No compactness or Liouville theorem.
- No weak-to-smooth upgrade.
- No Navier-Stokes regularity theorem.

### Verification

- Local `lake build` passed with `1881 jobs`.
- Python regression suite passed with `43 passed`.
- Evaluator `--check-expected` matched all 252 candidates.
- v4 preflight returned `summary: checked=0 skipped=252 blocked=0`.
