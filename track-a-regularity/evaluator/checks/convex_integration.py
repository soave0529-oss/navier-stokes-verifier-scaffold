from __future__ import annotations

from schema import CheckResult, LemmaCandidate


UNIQUENESS_PATTERNS = (
    "weak solution is unique",
    "weak solutions are unique",
    "finite-energy weak solution is unique",
    "finite-energy weak solutions are unique",
    "uniqueness of weak",
)

ENERGY_EQUALITY_PATTERNS = (
    "every weak solution conserves energy",
    "all weak solutions conserve energy",
    "weak solution conserves kinetic energy",
    "weak solutions conserve kinetic energy",
    "energy equality for every weak",
    "energy equality for all weak",
)

ENERGY_PROFILE_PATTERNS = (
    "arbitrary energy profile is impossible",
    "arbitrary energy profiles are impossible",
    "weak solutions cannot prescribe energy",
)


def check(candidate: LemmaCandidate) -> CheckResult:
    text = candidate.normalized_text
    patterns = [
        *(pattern for pattern in UNIQUENESS_PATTERNS if pattern in text),
        *(pattern for pattern in ENERGY_EQUALITY_PATTERNS if pattern in text),
        *(pattern for pattern in ENERGY_PROFILE_PATTERNS if pattern in text),
    ]
    if patterns:
        return CheckResult(
            name="convex_integration_check",
            status="fail",
            reason="Candidate conflicts with BV/convex-integration weak-solution guardrails.",
            evidence={"patterns": patterns},
        )
    return CheckResult(
        name="convex_integration_check",
        status="pass",
        reason="No first-pass BV/convex-integration guardrail violation detected.",
    )
