import NavierStokesProgram.SpectralTail

/-!
# Duhamel Bilinear Vocabulary

Finite bookkeeping for the critical Duhamel bilinear candidate family
`lemma_0209/0219/0229/0239/0249`.

This file is formal vocabulary only. It does not define the Navier-Stokes
bilinear operator, does not construct a mild solution, and does not state a
critical-space continuation theorem.
-/

namespace NavierStokesProgram
namespace Duhamel

open scoped BigOperators

/-- A placeholder bilinear map on toy scalar Fourier states. -/
abbrev BilinearStateMap : Type :=
  FourierState3 → FourierState3 → FourierState3

/-- Toy pointwise bilinear map, useful only as a sanity-check placeholder. -/
noncomputable def pointwiseBilinear : BilinearStateMap :=
  fun a b k => a k * b k

@[simp]
theorem pointwiseBilinear_zero_left (a : FourierState3) :
    pointwiseBilinear 0 a = 0 := by
  funext k
  simp [pointwiseBilinear]

@[simp]
theorem pointwiseBilinear_zero_right (a : FourierState3) :
    pointwiseBilinear a 0 = 0 := by
  funext k
  simp [pointwiseBilinear]

/-- One finite time-sample contribution to a toy Duhamel sum. -/
structure DuhamelSample where
  lag : ℝ
  lag_nonneg : 0 ≤ lag
  weight : ℝ
  weight_nonneg : 0 ≤ weight
  stateA : FourierState3
  stateB : FourierState3

/--
Apply heat flow to one bilinear sample and multiply by a nonnegative quadrature weight.

The sign and Leray projection in the real NSE Duhamel term are deliberately absent here.
-/
noncomputable def sampleContribution (ν : ℝ) (B : BilinearStateMap)
    (s : DuhamelSample) : FourierState3 :=
  fun k => s.weight * heatStep ν s.lag (B s.stateA s.stateB) k

@[simp]
theorem sampleContribution_zero_weight (ν : ℝ) (B : BilinearStateMap)
    (s : DuhamelSample) (h : s.weight = 0) :
    sampleContribution ν B s = 0 := by
  funext k
  simp [sampleContribution, h]

/-- A finite toy Duhamel bilinear sum over explicit samples. -/
structure FiniteDuhamelBilinear where
  indices : Finset ℕ
  sample : ℕ → DuhamelSample
  bilinear : BilinearStateMap
  viscosity : ℝ
  viscosity_pos : 0 < viscosity

namespace FiniteDuhamelBilinear

/-- The finite toy Duhamel state assembled from sample contributions. -/
noncomputable def value (D : FiniteDuhamelBilinear) : FourierState3 :=
  fun k => D.indices.sum fun i =>
    sampleContribution D.viscosity D.bilinear (D.sample i) k

/-- Finite-mode energy of the toy Duhamel state. -/
noncomputable def energyOn (D : FiniteDuhamelBilinear) (modes : Finset FourierMode3) : ℝ :=
  spectralEnergy modes D.value

@[simp]
theorem value_empty (sample : ℕ → DuhamelSample) (bilinear : BilinearStateMap)
    (viscosity : ℝ) (viscosity_pos : 0 < viscosity) :
    FiniteDuhamelBilinear.value
      { indices := ∅
        sample := sample
        bilinear := bilinear
        viscosity := viscosity
        viscosity_pos := viscosity_pos } = 0 := by
  funext k
  simp [value]

theorem energyOn_nonneg (D : FiniteDuhamelBilinear) (modes : Finset FourierMode3) :
    0 ≤ D.energyOn modes := by
  unfold energyOn
  exact spectralEnergy_nonneg modes D.value

end FiniteDuhamelBilinear

/--
Critical norm placeholder for Duhamel bilinear candidates.

The field `criticalSpaceConvention` must eventually name the exact function space,
indices, and time norm. Until then this is only a typed reminder that the candidate
is under-specified.
-/
structure CriticalDuhamelBound where
  duhamel : FiniteDuhamelBilinear
  criticalSpaceConvention : Prop
  bound : ℝ
  bound_nonneg : 0 ≤ bound
  finiteEnergyBound :
    ∀ modes : Finset FourierMode3, duhamel.energyOn modes ≤ bound

theorem criticalDuhamelBound_energy_nonneg (b : CriticalDuhamelBound)
    (modes : Finset FourierMode3) :
    0 ≤ b.duhamel.energyOn modes :=
  b.duhamel.energyOn_nonneg modes

theorem criticalDuhamelBound_energy_le_bound (b : CriticalDuhamelBound)
    (modes : Finset FourierMode3) :
    b.duhamel.energyOn modes ≤ b.bound :=
  b.finiteEnergyBound modes

end Duhamel
end NavierStokesProgram
