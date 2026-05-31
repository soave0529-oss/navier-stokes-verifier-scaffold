from __future__ import annotations

from schema import CheckResult, LemmaCandidate


DYADIC_FLUX_EXACT_PATTERNS = (
    "pi_n^les",
    "positive flux envelope",
    "normalization exponent alpha = 1",
    "p_{<=n}",
)


def check(candidate: LemmaCandidate) -> CheckResult:
    text = candidate.normalized_text
    if candidate.id == "lemma_0251" and all(pattern in text for pattern in DYADIC_FLUX_EXACT_PATTERNS):
        return CheckResult(
            name="flux_balance_risk_check",
            status="review",
            reason=(
                "Flux-balance audit found sign-convention and coercivity risks; this exact "
                "dyadic flux statement needs a sign-corrected rewrite before expert review."
            ),
            evidence={
                "family": "dyadic_flux_exact",
                "audit": "docs/LEMMA_0251_FLUX_BALANCE_AUDIT.md",
                "risk": "project Pi_N^LES positive part is backscatter under usual forward-flux sign and is noncoercive",
            },
        )

    return CheckResult(
        name="flux_balance_risk_check",
        status="pass",
        reason="No exact dyadic flux balance risk marker detected.",
    )
