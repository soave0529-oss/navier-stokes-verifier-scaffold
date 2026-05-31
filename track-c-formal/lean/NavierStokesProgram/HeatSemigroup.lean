import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Algebra.BigOperators.Group.Finset.Basic

/-!
# Heat Semigroup Toy Artifact

This is the first local Track C artifact after the Lean project bootstrap.

It deliberately models only the linear heat multiplier on discrete Fourier modes.
It is not a Navier-Stokes regularity theorem and does not include Leray projection,
nonlinearity, weak solutions, or torus quotient geometry.
-/

namespace NavierStokesProgram

open scoped BigOperators

/-- Integer-valued 3D Fourier mode. -/
abbrev FourierMode3 : Type := Fin 3 → ℤ

/-- Squared Euclidean wave number `|k|^2` for a 3D Fourier mode. -/
noncomputable def modeSq (k : FourierMode3) : ℝ :=
  ∑ i : Fin 3, (k i : ℝ) ^ 2

/-- `|k|^2` is nonnegative. -/
theorem modeSq_nonneg (k : FourierMode3) : 0 ≤ modeSq k := by
  unfold modeSq
  exact Finset.sum_nonneg fun i _hi => sq_nonneg (k i : ℝ)

/-- Linear heat multiplier `exp(-ν t |k|^2)` on one Fourier mode. -/
noncomputable def heatMultiplier (ν t : ℝ) (k : FourierMode3) : ℝ :=
  Real.exp (-(ν * t * modeSq k))

@[simp]
theorem heatMultiplier_zero_time (ν : ℝ) (k : FourierMode3) :
    heatMultiplier ν 0 k = 1 := by
  simp [heatMultiplier]

@[simp]
theorem heatMultiplier_zero_viscosity (t : ℝ) (k : FourierMode3) :
    heatMultiplier 0 t k = 1 := by
  simp [heatMultiplier]

/-- Heat multipliers are strictly positive for all real parameters. -/
theorem heatMultiplier_pos (ν t : ℝ) (k : FourierMode3) :
    0 < heatMultiplier ν t k := by
  simp [heatMultiplier, Real.exp_pos]

/-- Heat multipliers are nonnegative. -/
theorem heatMultiplier_nonneg (ν t : ℝ) (k : FourierMode3) :
    0 ≤ heatMultiplier ν t k :=
  le_of_lt (heatMultiplier_pos ν t k)

/-- Heat multipliers compose additively in time. -/
theorem heatMultiplier_add_time (ν t s : ℝ) (k : FourierMode3) :
    heatMultiplier ν (t + s) k = heatMultiplier ν t k * heatMultiplier ν s k := by
  unfold heatMultiplier
  rw [← Real.exp_add]
  congr 1
  ring

/-- A toy Fourier state: one real amplitude per discrete mode. -/
abbrev FourierState3 : Type := FourierMode3 → ℝ

/-- Apply the heat multiplier pointwise to a Fourier state. -/
noncomputable def heatStep (ν t : ℝ) (a : FourierState3) : FourierState3 :=
  fun k => heatMultiplier ν t k * a k

@[simp]
theorem heatStep_apply (ν t : ℝ) (a : FourierState3) (k : FourierMode3) :
    heatStep ν t a k = heatMultiplier ν t k * a k :=
  rfl

@[simp]
theorem heatStep_zero_time (ν : ℝ) (a : FourierState3) :
    heatStep ν 0 a = a := by
  funext k
  simp [heatStep]

/-- The toy heat step has the expected semigroup law. -/
theorem heatStep_add_time (ν t s : ℝ) (a : FourierState3) :
    heatStep ν (t + s) a = heatStep ν t (heatStep ν s a) := by
  funext k
  simp [heatStep, heatMultiplier_add_time, mul_comm, mul_left_comm]

end NavierStokesProgram
