import NavierStokesProgram.HeatSemigroup

/-!
# Spectral Tail Vocabulary

Finite-mode vocabulary for spectral-tail diagnostics.

This file is infrastructure only. It does not state a Navier-Stokes
regularity criterion and it does not connect numerical tail bounds to smooth
continuation.
-/

namespace NavierStokesProgram

open scoped BigOperators

/-- Finite-mode energy over an explicit mode set. -/
noncomputable def spectralEnergy (modes : Finset FourierMode3) (a : FourierState3) : ℝ :=
  modes.sum fun k => (a k) ^ 2

/-- Energy carried by modes whose squared wave number is at least `cutoffSq`. -/
noncomputable def spectralTail (cutoffSq : ℝ) (modes : Finset FourierMode3) (a : FourierState3) : ℝ :=
  (modes.filter fun k => cutoffSq ≤ modeSq k).sum fun k => (a k) ^ 2

@[simp]
theorem spectralEnergy_empty (a : FourierState3) :
    spectralEnergy ∅ a = 0 := by
  simp [spectralEnergy]

@[simp]
theorem spectralTail_empty (cutoffSq : ℝ) (a : FourierState3) :
    spectralTail cutoffSq ∅ a = 0 := by
  simp [spectralTail]

theorem spectralEnergy_nonneg (modes : Finset FourierMode3) (a : FourierState3) :
    0 ≤ spectralEnergy modes a := by
  unfold spectralEnergy
  exact Finset.sum_nonneg fun k _hk => sq_nonneg (a k)

theorem spectralTail_nonneg (cutoffSq : ℝ) (modes : Finset FourierMode3) (a : FourierState3) :
    0 ≤ spectralTail cutoffSq modes a := by
  unfold spectralTail
  exact Finset.sum_nonneg fun k _hk => sq_nonneg (a k)

/-- A finite-mode spectral-tail bound record for diagnostics and future vocabulary. -/
structure SpectralTailBound (a : FourierState3) where
  modes : Finset FourierMode3
  cutoffSq : ℝ
  bound : ℝ
  bound_nonneg : 0 ≤ bound
  tail_le_bound : spectralTail cutoffSq modes a ≤ bound

theorem spectralTailBound_tail_nonneg (a : FourierState3) (b : SpectralTailBound a) :
    0 ≤ spectralTail b.cutoffSq b.modes a :=
  spectralTail_nonneg b.cutoffSq b.modes a

theorem spectralTailBound_tail_le_bound (a : FourierState3) (b : SpectralTailBound a) :
    spectralTail b.cutoffSq b.modes a ≤ b.bound :=
  b.tail_le_bound

end NavierStokesProgram
