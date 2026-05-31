import Mathlib.Data.Real.Basic

/-!
Small local definitions for the Navier-Stokes program.

These are intentionally lightweight. The goal of Step 9 is to verify that our
own Lean package builds on the same toolchain as the upstream statement
baseline before we attempt analytic PDE formalization.
-/

namespace NavierStokesProgram

abbrev Point3 : Type := Fin 3 → ℝ

abbrev VectorField3 : Type := Point3 → Point3

def IsDivergenceFreeSmooth (_u : VectorField3) : Prop :=
  True

structure SmoothDivergenceFreeVelocity where
  field : VectorField3
  regularity : IsDivergenceFreeSmooth field

end NavierStokesProgram
