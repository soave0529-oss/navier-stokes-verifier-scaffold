import NavierStokesProgram.SpectralTail

/-!
# Finite Shell Projector Vocabulary

Finite-mode shell-projector bookkeeping for the definition-tightened dyadic
flux candidate `lemma_0251`.

This file is infrastructure only. It does not define a Littlewood-Paley theory,
does not formalize the Navier-Stokes nonlinearity, and does not state a smooth
continuation theorem.
-/

namespace NavierStokesProgram

open scoped BigOperators

/-- The finite low-mode subset cut out by `|k|^2 <= cutoffSq`. -/
noncomputable def lowModeSet (cutoffSq : ℝ) (modes : Finset FourierMode3) :
    Finset FourierMode3 :=
  modes.filter fun k => modeSq k ≤ cutoffSq

/-- Project a toy scalar Fourier state onto an explicit finite low-mode set. -/
noncomputable def lowProject (cutoffSq : ℝ) (modes : Finset FourierMode3)
    (a : FourierState3) : FourierState3 :=
  fun k => if k ∈ lowModeSet cutoffSq modes then a k else 0

@[simp]
theorem lowModeSet_empty (cutoffSq : ℝ) :
    lowModeSet cutoffSq ∅ = ∅ := by
  simp [lowModeSet]

theorem mem_lowModeSet_mode_le {cutoffSq : ℝ} {modes : Finset FourierMode3}
    {k : FourierMode3} (hk : k ∈ lowModeSet cutoffSq modes) :
    modeSq k ≤ cutoffSq := by
  exact (Finset.mem_filter.mp hk).2

theorem mem_lowModeSet_mem_modes {cutoffSq : ℝ} {modes : Finset FourierMode3}
    {k : FourierMode3} (hk : k ∈ lowModeSet cutoffSq modes) :
    k ∈ modes := by
  exact (Finset.mem_filter.mp hk).1

@[simp]
theorem lowProject_apply_mem (cutoffSq : ℝ) (modes : Finset FourierMode3)
    (a : FourierState3) {k : FourierMode3}
    (hk : k ∈ lowModeSet cutoffSq modes) :
    lowProject cutoffSq modes a k = a k := by
  simp [lowProject, hk]

@[simp]
theorem lowProject_apply_not_mem (cutoffSq : ℝ) (modes : Finset FourierMode3)
    (a : FourierState3) {k : FourierMode3}
    (hk : k ∉ lowModeSet cutoffSq modes) :
    lowProject cutoffSq modes a k = 0 := by
  simp [lowProject, hk]

@[simp]
theorem lowProject_empty (cutoffSq : ℝ) (a : FourierState3) :
    lowProject cutoffSq ∅ a = 0 := by
  funext k
  simp [lowProject]

theorem lowProject_idempotent (cutoffSq : ℝ) (modes : Finset FourierMode3)
    (a : FourierState3) :
    lowProject cutoffSq modes (lowProject cutoffSq modes a) =
      lowProject cutoffSq modes a := by
  funext k
  by_cases hk : k ∈ lowModeSet cutoffSq modes
  · simp [lowProject, hk]
  · simp [lowProject, hk]

/-- A finite shell projector with an explicit cutoff and finite ambient mode set. -/
structure ShellProjector where
  modes : Finset FourierMode3
  cutoffSq : ℝ
  cutoff_nonneg : 0 ≤ cutoffSq

namespace ShellProjector

/-- Apply a finite shell projector to a toy Fourier state. -/
noncomputable def project (P : ShellProjector) (a : FourierState3) : FourierState3 :=
  lowProject P.cutoffSq P.modes a

/-- Energy in the finite low shell selected by a shell projector. -/
noncomputable def shellEnergy (P : ShellProjector) (a : FourierState3) : ℝ :=
  spectralEnergy (lowModeSet P.cutoffSq P.modes) a

theorem shellEnergy_nonneg (P : ShellProjector) (a : FourierState3) :
    0 ≤ P.shellEnergy a := by
  unfold shellEnergy
  exact spectralEnergy_nonneg (lowModeSet P.cutoffSq P.modes) a

@[simp]
theorem project_idempotent (P : ShellProjector) (a : FourierState3) :
    P.project (P.project a) = P.project a := by
  exact lowProject_idempotent P.cutoffSq P.modes a

end ShellProjector

/-- Positive part of a scalar flux sample. -/
noncomputable def positivePart (x : ℝ) : ℝ :=
  max x 0

theorem positivePart_nonneg (x : ℝ) :
    0 ≤ positivePart x := by
  unfold positivePart
  exact le_max_right x 0

/-- A single finite-mode LES-flux sample attached to a shell projector. -/
structure FluxSample where
  projector : ShellProjector
  lesFlux : ℝ

namespace FluxSample

/-- Positive flux envelope for one shell/time sample. -/
noncomputable def positiveFlux (s : FluxSample) : ℝ :=
  positivePart s.lesFlux

theorem positiveFlux_nonneg (s : FluxSample) :
    0 ≤ s.positiveFlux :=
  positivePart_nonneg s.lesFlux

end FluxSample

/--
A finite dyadic flux budget with normalization exponent fixed to `alpha = 1`.

This is bookkeeping for the finite sums that appear in `lemma_0251`; it is not
the infinite dyadic summability assumption and it is not a regularity criterion.
-/
structure DyadicFluxBudget where
  indices : Finset ℕ
  fluxIntegral : ℕ → ℝ
  fluxIntegral_nonneg : ∀ N, N ∈ indices → 0 ≤ fluxIntegral N
  normalizationExponent : ℝ
  normalization_eq_one : normalizationExponent = 1

namespace DyadicFluxBudget

/-- Finite `sum_N N^{-1} integral positive_flux_N` bookkeeping. -/
noncomputable def value (b : DyadicFluxBudget) : ℝ :=
  b.indices.sum fun N => (N : ℝ)⁻¹ * b.fluxIntegral N

@[simp]
theorem value_empty (fluxIntegral : ℕ → ℝ) :
    DyadicFluxBudget.value
      { indices := ∅
        fluxIntegral := fluxIntegral
        fluxIntegral_nonneg := by simp
        normalizationExponent := 1
        normalization_eq_one := rfl } = 0 := by
  simp [value]

theorem value_nonneg (b : DyadicFluxBudget) :
    0 ≤ b.value := by
  unfold value
  exact Finset.sum_nonneg fun N hN =>
    mul_nonneg (inv_nonneg.mpr (Nat.cast_nonneg N)) (b.fluxIntegral_nonneg N hN)

end DyadicFluxBudget

end NavierStokesProgram
