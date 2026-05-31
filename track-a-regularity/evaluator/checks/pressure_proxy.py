from __future__ import annotations

from schema import CheckResult, LemmaCandidate


PRESSURE_PROXY_PATTERNS = (
    "pressure-gradient envelope",
    "pressure gradient envelope",
    "pressure proxy",
    "material-derivative pressure proxy",
)

NORMALIZATION_HINTS = (
    "mean-zero pressure",
    "pressure normalization",
    "normalized pressure",
    "poisson equation",
    "leray projection",
)


def check(candidate: LemmaCandidate) -> CheckResult:
    text = candidate.normalized_text
    pressure_patterns = [pattern for pattern in PRESSURE_PROXY_PATTERNS if pattern in text]
    if not pressure_patterns:
        return CheckResult(
            name="pressure_proxy_check",
            status="pass",
            reason="No pressure-proxy hypothesis detected.",
        )
    normalization_hints = [hint for hint in NORMALIZATION_HINTS if hint in text]
    if not normalization_hints:
        return CheckResult(
            name="pressure_proxy_check",
            status="fail",
            reason=(
                "Pressure-proxy candidates must define pressure normalization, source equation, "
                "and the exact space-time norm before they can be treated as analytic hypotheses."
            ),
            evidence={"pressure_patterns": pressure_patterns},
        )
    return CheckResult(
        name="pressure_proxy_check",
        status="pass",
        reason="Pressure-proxy statement includes at least one normalization/source hint.",
        evidence={"pressure_patterns": pressure_patterns, "normalization_hints": normalization_hints},
    )
