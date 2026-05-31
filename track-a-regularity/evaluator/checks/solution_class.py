from __future__ import annotations

from schema import CheckResult, LemmaCandidate


def check(candidate: LemmaCandidate) -> CheckResult:
    text = candidate.normalized_text
    mentions_weak = "weak" in text or "leray-hopf" in text or "leray hopf" in text
    claims_smooth_continuation = "extends smoothly" in text or "smooth continuation" in text
    mentions_smooth_class = "smooth" in text
    mentions_nonuniqueness = "buckmaster" in text or "convex integration" in text or "nonuniqueness" in text

    if mentions_weak and claims_smooth_continuation:
        return CheckResult(
            name="solution_class_check",
            status="fail",
            reason="Candidate jumps from weak-solution premises to smooth continuation without a separate regularity upgrade theorem.",
        )
    if mentions_nonuniqueness and claims_smooth_continuation:
        return CheckResult(
            name="solution_class_check",
            status="fail",
            reason="Candidate mixes convex-integration/nonuniqueness context with smooth continuation without class separation.",
        )
    return CheckResult(
        name="solution_class_check",
        status="pass",
        reason="No weak/smooth solution-class conflict detected.",
    )
