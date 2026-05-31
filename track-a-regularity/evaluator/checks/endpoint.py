from __future__ import annotations

from schema import CheckResult, LemmaCandidate


ENDPOINT_PATTERNS = (
    "l^infty_t l^3_x",
    "l∞_t l^3_x",
    "l^infinity_t l^3_x",
    "l^∞(0,t; l^3",
    "q = 3",
    "q=3",
    "l^3(t^3)",
)


def check(candidate: LemmaCandidate) -> CheckResult:
    text = candidate.normalized_text
    if any(pattern in text for pattern in ENDPOINT_PATTERNS):
        return CheckResult(
            name="endpoint_check",
            status="fail",
            reason="Candidate touches a delicate endpoint case and needs a separate ESS/endpoint treatment.",
            evidence={"patterns": [pattern for pattern in ENDPOINT_PATTERNS if pattern in text]},
        )
    return CheckResult(
        name="endpoint_check",
        status="pass",
        reason="No first-pass Prodi-Serrin endpoint pattern detected.",
    )
