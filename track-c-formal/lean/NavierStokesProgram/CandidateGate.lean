import NavierStokesProgram.SolutionClasses

/-!
# Candidate Generation Gate Vocabulary

Small Track C vocabulary for the Step 56 candidate-generation v4 contract.

This file records the audit gates a future Track A candidate must satisfy before
it is treated as emit-ready. It does not prove any Navier-Stokes regularity
statement and does not validate the analytic content of the gates.
-/

namespace NavierStokesProgram
namespace CandidateGate

/-- Coarse solution-class tags used to prevent silent weak-to-smooth upgrades. -/
inductive SolutionClassTag where
  | smoothClassical
  | weakDistributional
  | lerayHopf
  | suitableWeak
  | ancientBlowupLimit
deriving DecidableEq

/-- Audit propositions required by the v4 candidate generation spec. -/
structure GenerationAudit where
  exactQuantityDefinitions : Prop
  exactFunctionSpaces : Prop
  knownResultSeparation : Prop
  proofRoute : Prop
  solutionClassBridge : Prop

/-- All v4 audit propositions are supplied. -/
structure Complete (audit : GenerationAudit) : Prop where
  exactQuantityDefinitions : audit.exactQuantityDefinitions
  exactFunctionSpaces : audit.exactFunctionSpaces
  knownResultSeparation : audit.knownResultSeparation
  proofRoute : audit.proofRoute
  solutionClassBridge : audit.solutionClassBridge

/--
A candidate shell with a statement and explicit source/target solution classes.

The statement is intentionally just a proposition. This record is about metadata
discipline, not about proving the proposition.
-/
structure CandidateShell where
  statement : Prop
  sourceClass : SolutionClassTag
  targetClass : SolutionClassTag
  audit : GenerationAudit

namespace CandidateShell

/--
The v4 emit-ready gate: the audit is complete and the candidate does not change
solution class behind the statement.
-/
def EmitReady (candidate : CandidateShell) : Prop :=
  Complete candidate.audit ∧ candidate.sourceClass = candidate.targetClass

theorem emitReady_has_exact_quantities (candidate : CandidateShell)
    (h : candidate.EmitReady) :
    candidate.audit.exactQuantityDefinitions :=
  h.1.exactQuantityDefinitions

theorem emitReady_has_function_spaces (candidate : CandidateShell)
    (h : candidate.EmitReady) :
    candidate.audit.exactFunctionSpaces :=
  h.1.exactFunctionSpaces

theorem emitReady_has_known_result_separation (candidate : CandidateShell)
    (h : candidate.EmitReady) :
    candidate.audit.knownResultSeparation :=
  h.1.knownResultSeparation

theorem emitReady_has_proof_route (candidate : CandidateShell)
    (h : candidate.EmitReady) :
    candidate.audit.proofRoute :=
  h.1.proofRoute

theorem emitReady_has_solution_class_bridge (candidate : CandidateShell)
    (h : candidate.EmitReady) :
    candidate.audit.solutionClassBridge :=
  h.1.solutionClassBridge

theorem emitReady_same_solution_class (candidate : CandidateShell)
    (h : candidate.EmitReady) :
    candidate.sourceClass = candidate.targetClass :=
  h.2

end CandidateShell
end CandidateGate
end NavierStokesProgram
