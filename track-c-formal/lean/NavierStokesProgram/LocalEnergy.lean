import NavierStokesProgram.ParabolicCylinder
import Mathlib.Data.Finset.Basic

/-!
# Local Energy Vocabulary

Finite placeholder vocabulary for suitable-weak local energy inequality metadata.

This file is intentionally small. It records local-energy bookkeeping data and
solution-class separation, but it does not prove epsilon regularity, pressure
estimates, or a weak-to-smooth upgrade.
-/

namespace NavierStokesProgram
namespace LocalEnergy

open SolutionClasses
open ParabolicMorrey

/-- Placeholder metadata for the pressure term in a local energy inequality. -/
structure LocalPressureData where
  localPart : Prop
  nonlocalPart : Prop
  pressureSpaceConvention : Prop

/-- Placeholder metadata for a nonnegative cutoff supported in a parabolic cylinder. -/
structure LocalEnergyCutoff where
  cylinder : ParabolicCylinder
  nonnegative : Prop
  compactSupportInCylinder : Prop
  derivativeBoundsNamed : Prop

/-- One finite local-energy sample attached to a suitable weak solution. -/
structure LocalEnergySample where
  cutoff : LocalEnergyCutoff
  kineticEnergyTop : ℝ
  kineticEnergyTop_nonneg : 0 ≤ kineticEnergyTop
  kineticEnergyLower : ℝ
  kineticEnergyLower_nonneg : 0 ≤ kineticEnergyLower
  viscousDissipation : ℝ
  viscousDissipation_nonneg : 0 ≤ viscousDissipation
  pressureTransport : ℝ
  cutoffError : ℝ
  pressure : LocalPressureData

namespace LocalEnergySample

/-- Left-hand side placeholder for a local energy inequality sample. -/
noncomputable def lhs (s : LocalEnergySample) : ℝ :=
  s.kineticEnergyTop + s.viscousDissipation

/-- Right-hand side placeholder for a local energy inequality sample. -/
noncomputable def rhs (s : LocalEnergySample) : ℝ :=
  s.kineticEnergyLower + s.pressureTransport + s.cutoffError

theorem lhs_nonneg (s : LocalEnergySample) : 0 ≤ s.lhs := by
  unfold lhs
  exact add_nonneg s.kineticEnergyTop_nonneg s.viscousDissipation_nonneg

end LocalEnergySample

/--
Finite record of local energy inequalities for selected samples.

The true suitable-weak definition quantifies over admissible test functions.
This finite record is only a buildable bookkeeping shell for future audits.
-/
structure FiniteLocalEnergyInequality where
  solution : SuitableWeakSolution
  indices : Finset ℕ
  sample : ℕ → LocalEnergySample
  sample_inequality :
    ∀ i, i ∈ indices → (sample i).lhs ≤ (sample i).rhs
  usesSuitableWeakClass : Prop
  noSmoothUpgradeClaim : Prop

namespace FiniteLocalEnergyInequality

theorem sample_lhs_nonneg (E : FiniteLocalEnergyInequality) {i : ℕ} :
    0 ≤ (E.sample i).lhs :=
  (E.sample i).lhs_nonneg

theorem sample_le_rhs (E : FiniteLocalEnergyInequality) {i : ℕ}
    (hi : i ∈ E.indices) :
    (E.sample i).lhs ≤ (E.sample i).rhs :=
  E.sample_inequality i hi

theorem suitable_weak_local_energy_field_eq (E : FiniteLocalEnergyInequality) :
    SuitableLocalEnergyInequality E.solution = E.solution.local_energy_inequality :=
  rfl

end FiniteLocalEnergyInequality

/--
Bridge metadata for comparing a smooth classical solution with suitable-weak local energy
vocabulary without asserting a weak-to-smooth theorem.
-/
structure SmoothToLocalEnergyAudit where
  smoothSolution : SmoothClassicalSolution
  terminalTime : Time
  localEnergyRecord : Prop
  smoothClassPreserved : Prop
  suitableWeakRouteNamed : Prop
  noWeakToSmoothUpgradeClaim : Prop

end LocalEnergy
end NavierStokesProgram
