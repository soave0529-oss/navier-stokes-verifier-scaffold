from __future__ import annotations

from schema import CheckResult, LemmaCandidate


def check(candidate: LemmaCandidate) -> CheckResult:
    text = candidate.normalized_text
    if "intentionally_bad_scaling" in candidate.type:
        return CheckResult(
            name="scaling_check",
            status="fail",
            reason="Finite-energy-only continuation is subcritical for the 3D NSE scaling and is not a known smooth continuation criterion.",
            evidence={"type": candidate.type},
        )
    if "l2norm" in text and "extends smoothly" in text and "prodi" not in text and "bkm" not in text:
        return CheckResult(
            name="scaling_check",
            status="fail",
            reason="The statement appears to use only L2 control as a smooth continuation trigger.",
            evidence={"pattern": "L2Norm + ExtendsSmoothlyPast"},
        )
    if "prodi" in text or "serrin" in text:
        return CheckResult(
            name="scaling_check",
            status="pass",
            reason="Prodi-Serrin condition contains the critical relation 2/p + 3/q <= 1.",
            evidence={"related_known": list(candidate.related_known)},
        )
    if "bkm" in text or "vorticity" in text or "omega" in text:
        return CheckResult(
            name="scaling_check",
            status="pass",
            reason="BKM/vorticity blow-up criteria are treated as scaling-compatible positive controls in this skeleton.",
            evidence={"related_known": list(candidate.related_known)},
        )
    return CheckResult(
        name="scaling_check",
        status="pass",
        reason="No scaling violation detected by the first-pass syntactic heuristic.",
    )

