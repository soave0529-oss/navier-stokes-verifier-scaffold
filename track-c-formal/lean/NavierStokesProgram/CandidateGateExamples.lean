import NavierStokesProgram.CandidateGate

/-!
# Candidate Gate Examples

Small buildable examples for the Step 56-58 candidate-generation gate.

These examples are deliberately toy metadata checks. They do not construct a
Navier-Stokes regularity candidate and do not prove any analytic audit field.
-/

namespace NavierStokesProgram
namespace CandidateGate

/-- A toy audit whose five v4 fields are propositions equal to `True`. -/
def toyCompleteAudit : GenerationAudit where
  exactQuantityDefinitions := True
  exactFunctionSpaces := True
  knownResultSeparation := True
  proofRoute := True
  solutionClassBridge := True

theorem toyCompleteAudit_complete : Complete toyCompleteAudit := by
  exact ⟨trivial, trivial, trivial, trivial, trivial⟩

/-- A toy audit missing exact quantity definitions. -/
def toyIncompleteAudit : GenerationAudit where
  exactQuantityDefinitions := False
  exactFunctionSpaces := True
  knownResultSeparation := True
  proofRoute := True
  solutionClassBridge := True

/-- A same-class toy shell can pass the metadata gate when the audit is complete. -/
def toySmoothCandidate : CandidateShell where
  statement := True
  sourceClass := SolutionClassTag.smoothClassical
  targetClass := SolutionClassTag.smoothClassical
  audit := toyCompleteAudit

theorem toySmoothCandidate_emitReady : toySmoothCandidate.EmitReady := by
  constructor
  · exact toyCompleteAudit_complete
  · rfl

/-- An incomplete audit cannot pass, even if the source and target class match. -/
def toyIncompleteCandidate : CandidateShell where
  statement := True
  sourceClass := SolutionClassTag.smoothClassical
  targetClass := SolutionClassTag.smoothClassical
  audit := toyIncompleteAudit

theorem toyIncompleteCandidate_not_emitReady :
    ¬ toyIncompleteCandidate.EmitReady := by
  intro h
  exact h.1.exactQuantityDefinitions

/-- A class-changing toy shell is blocked even with a complete audit. -/
def toyWeakToSmoothCandidate : CandidateShell where
  statement := True
  sourceClass := SolutionClassTag.lerayHopf
  targetClass := SolutionClassTag.smoothClassical
  audit := toyCompleteAudit

theorem toyWeakToSmoothCandidate_not_emitReady :
    ¬ toyWeakToSmoothCandidate.EmitReady := by
  intro h
  cases h.2

end CandidateGate
end NavierStokesProgram
