from __future__ import annotations

from schema import CheckResult, LemmaCandidate


BKM_INTEGRAL_PATTERNS = (
    "time integral of the l^infinity norm of curl u is finite",
    "omega l^infinity time integral is finite",
    "vorticity l^infinity time integral is finite",
    "vorticity `l^infinity` time integral",
)

EXTRA_ASSUMPTION_PATTERNS = (
    "vorticity direction modulus",
    "scale-local enstrophy flux",
    "high-frequency sobolev tail",
)


def check(candidate: LemmaCandidate) -> CheckResult:
    text = candidate.normalized_text
    bkm_patterns = [pattern for pattern in BKM_INTEGRAL_PATTERNS if pattern in text]
    extra_patterns = [pattern for pattern in EXTRA_ASSUMPTION_PATTERNS if pattern in text]
    if bkm_patterns and extra_patterns:
        return CheckResult(
            name="known_control_extension_check",
            status="known_control_with_extra_assumption",
            reason=(
                "Candidate includes a BKM-style finite vorticity L^infinity time integral "
                "plus an auxiliary assumption, so it is not counted as a new regularity candidate."
            ),
            evidence={"bkm_patterns": bkm_patterns, "extra_patterns": extra_patterns},
        )
    return CheckResult(
        name="known_control_extension_check",
        status="pass",
        reason="No BKM-with-extra-assumption pattern detected.",
    )
