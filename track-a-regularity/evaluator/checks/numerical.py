from __future__ import annotations

import json
import re
from pathlib import Path

from schema import CheckResult, LemmaCandidate


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_SUMMARY = ROOT / "track-b-blowup/runs/TG_N64_t10/diagnostics_summary.json"


def _extract_tail_bound(text: str) -> float | None:
    match = re.search(r"spectrum[-_ ]?tail[^<]*<=\s*([0-9.]+)", text)
    if match:
        return float(match.group(1))
    match = re.search(r"spectrumtail[^<]*<=\s*([0-9.]+)", text)
    if match:
        return float(match.group(1))
    return None


def check(candidate: LemmaCandidate, summary_path: Path = DEFAULT_SUMMARY) -> CheckResult:
    text = candidate.normalized_text
    if "taylor-green" not in text and "taylorgreen" not in text and "spectrum" not in text:
        return CheckResult(
            name="taylor_green_test",
            status="pass",
            reason="Candidate has no directly testable Taylor-Green numerical bound in the Step 11 skeleton.",
        )
    if not summary_path.exists():
        return CheckResult(
            name="taylor_green_test",
            status="fail",
            reason="Candidate needs Taylor-Green diagnostics but diagnostics_summary.json is missing.",
            evidence={"summary_path": str(summary_path)},
        )

    summary = json.loads(summary_path.read_text())
    tail_max = float(summary.get("spectrum_tail_max", "nan"))
    bound = _extract_tail_bound(text)
    if bound is not None and tail_max > bound:
        return CheckResult(
            name="taylor_green_test",
            status="fail",
            reason="Existing Step 7 diagnostics violate the claimed spectrum-tail bound.",
            evidence={"spectrum_tail_max": tail_max, "claimed_bound": bound, "summary_path": str(summary_path)},
        )
    return CheckResult(
        name="taylor_green_test",
        status="pass",
        reason="No violation found against existing Taylor-Green diagnostics.",
        evidence={"spectrum_tail_max": tail_max, "summary_path": str(summary_path)},
    )

