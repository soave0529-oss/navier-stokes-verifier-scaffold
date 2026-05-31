from __future__ import annotations

from schema import CheckResult, LemmaCandidate


def check(candidate: LemmaCandidate) -> CheckResult:
    text = candidate.normalized_text
    if "intentionally_bad_galilean" in candidate.type:
        return CheckResult(
            name="galilean_check",
            status="fail",
            reason="The candidate is tagged as an absolute-velocity negative control.",
            evidence={"type": candidate.type},
        )
    uses_absolute_velocity = (
        ("l-infinity" in text or "linfinitynorm (u t)" in text or "||u(t)||" in text)
        and "curl" not in text
        and "omega" not in text
        and "prodi" not in text
        and "serrin" not in text
    )
    if uses_absolute_velocity and ("<= 1" in text or "threshold" in text):
        return CheckResult(
            name="galilean_check",
            status="fail",
            reason="Absolute velocity thresholds are not invariant under Galilean boosts.",
            evidence={"pattern": "absolute velocity threshold"},
        )
    return CheckResult(
        name="galilean_check",
        status="pass",
        reason="No absolute velocity threshold detected.",
    )

