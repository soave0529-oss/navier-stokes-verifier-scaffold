import NavierStokesProgram.Basic

/-!
# Solution Class Vocabulary

This file is a small Track C artifact that separates smooth/classical,
distributional weak, Leray-Hopf, and suitable weak placeholders.

It is intentionally lightweight. The goal is to prevent future promoted
statements from silently moving conclusions between weak and smooth classes.
-/

namespace NavierStokesProgram
namespace SolutionClasses

abbrev Time : Type := ℝ

/-- Placeholder for a smooth classical periodic solution. -/
structure SmoothClassicalSolution where
  velocity : VectorField3
  viscosity : ℝ
  viscosity_pos : 0 < viscosity
  divergence_free : IsDivergenceFreeSmooth velocity
  mean_zero : Prop
  zero_force : Prop

/-- Placeholder for a distributional weak periodic solution. -/
structure WeakDistributionalSolution where
  velocity : VectorField3
  viscosity : ℝ
  viscosity_pos : 0 < viscosity
  weak_incompressible : Prop
  distributional_momentum : Prop

/-- Placeholder for a Leray-Hopf weak solution, including energy inequality. -/
structure LerayHopfSolution extends WeakDistributionalSolution where
  energy_inequality : Prop

/-- Placeholder for a suitable weak solution, including local energy inequality. -/
structure SuitableWeakSolution extends LerayHopfSolution where
  local_energy_inequality : Prop

/-- Forget a smooth classical solution to a weak distributional placeholder. -/
def SmoothClassicalSolution.toWeak (u : SmoothClassicalSolution) : WeakDistributionalSolution where
  velocity := u.velocity
  viscosity := u.viscosity
  viscosity_pos := u.viscosity_pos
  weak_incompressible := IsDivergenceFreeSmooth u.velocity
  distributional_momentum := True

@[simp]
theorem smooth_toWeak_velocity (u : SmoothClassicalSolution) :
    u.toWeak.velocity = u.velocity :=
  rfl

@[simp]
theorem smooth_toWeak_viscosity (u : SmoothClassicalSolution) :
    u.toWeak.viscosity = u.viscosity :=
  rfl

/-- A smooth continuation conclusion is only typed for smooth classical solutions. -/
def ExtendsSmoothlyPast (_u : SmoothClassicalSolution) (_T : Time) : Prop :=
  True

/-- A weak uniqueness statement is a separate proposition, not a smooth continuation claim. -/
def WeakUniquenessClaim (u v : WeakDistributionalSolution) : Prop :=
  u.velocity = v.velocity

/-- Expose the Leray-Hopf energy inequality placeholder as a named proposition. -/
def LerayHopfEnergyInequality (u : LerayHopfSolution) : Prop :=
  u.energy_inequality

@[simp]
theorem leray_hopf_energy_inequality_eq_field (u : LerayHopfSolution) :
    LerayHopfEnergyInequality u = u.energy_inequality :=
  rfl

/-- Expose the suitable weak local energy inequality placeholder as a named proposition. -/
def SuitableLocalEnergyInequality (u : SuitableWeakSolution) : Prop :=
  u.local_energy_inequality

@[simp]
theorem suitable_local_energy_inequality_eq_field (u : SuitableWeakSolution) :
    SuitableLocalEnergyInequality u = u.local_energy_inequality :=
  rfl

end SolutionClasses
end NavierStokesProgram
