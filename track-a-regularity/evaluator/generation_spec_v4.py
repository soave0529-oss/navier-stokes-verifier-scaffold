from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from proof_obligation_blockers import (
    BlockerReportError,
    check_summary_output,
    load_blocker_summary,
)
from needs_review_blocker_sources import (
    BlockerMatrixError,
    SourceIndexError,
    build_source_index,
    check_output as check_source_index_output,
    check_sources_exist,
)
from schema import LemmaCandidate


ROOT = Path(__file__).resolve().parents[2]

REQUIRED_MARKERS = (
    "V4:ExactQuantityDefinitions",
    "V4:ExactFunctionSpaces",
    "V4:KnownResultSeparation",
    "V4:ProofRoute",
    "V4:SolutionClassBridge",
    "V4:ZeroProofObligationBlockers",
    "V4:FreshBlockerSourceIndex",
)

PROOF_OBLIGATION_REPORT_KEY = "proof_obligation_report_json"
PROOF_OBLIGATION_SUMMARY_KEY = "proof_obligation_summary_json"
BLOCKER_SOURCE_INDEX_MARKDOWN_KEY = "blocker_source_index_markdown"
BLOCKER_SOURCE_INDEX_JSON_KEY = "blocker_source_index_json"

BLOCKED_PHRASES = (
    "critical space-time norm",
    "normalization conventions made explicit",
    "diagnostic",
    "proxy",
    "placeholder",
    "formal-only",
    "finite vocabulary",
)


@dataclass(frozen=True)
class GenerationAssessment:
    candidate_id: str
    emit_ready: bool
    reasons: tuple[str, ...]


def assess_candidate(candidate: LemmaCandidate) -> GenerationAssessment:
    text = candidate.normalized_text
    reasons: list[str] = []

    expected_status = candidate.expected_evaluator.get("status")
    if expected_status != "candidate":
        reasons.append(
            "expected_evaluator.status must be candidate for v4 emit-ready output, "
            f"got {expected_status!r}"
        )

    marker_set = set(candidate.related_known)
    missing = [marker for marker in REQUIRED_MARKERS if marker not in marker_set]
    if missing:
        reasons.append("missing v4 metadata markers: " + ", ".join(missing))

    blocked = [phrase for phrase in BLOCKED_PHRASES if phrase in text]
    if blocked:
        reasons.append("blocked under-specified/formal-only phrases: " + ", ".join(blocked))

    if (
        "weak solution" in text
        and "extends smoothly" in text
        and "V4:SolutionClassBridge" not in marker_set
    ):
        reasons.append("weak-to-smooth bridge is missing")

    if expected_status == "candidate":
        reasons.extend(_assess_proof_obligation_gate(candidate))
        reasons.extend(_assess_source_index_gate(candidate))

    return GenerationAssessment(
        candidate_id=candidate.id,
        emit_ready=not reasons,
        reasons=tuple(reasons),
    )


def _metadata_path(candidate: LemmaCandidate, key: str) -> tuple[Path | None, str | None]:
    value = candidate.expected_evaluator.get(key)
    if not isinstance(value, str) or not value.strip():
        return None, f"missing expected_evaluator.{key}"
    path = Path(value)
    if not path.is_absolute():
        path = ROOT / path
    return path, None


def _assess_proof_obligation_gate(candidate: LemmaCandidate) -> list[str]:
    reasons: list[str] = []
    report_path, report_error = _metadata_path(candidate, PROOF_OBLIGATION_REPORT_KEY)
    summary_path, summary_error = _metadata_path(candidate, PROOF_OBLIGATION_SUMMARY_KEY)
    if report_error:
        reasons.append(report_error)
    if summary_error:
        reasons.append(summary_error)
    if report_path is None or summary_path is None:
        return reasons

    try:
        summary = load_blocker_summary(report_path)
    except BlockerReportError as exc:
        reasons.append(f"invalid proof-obligation report: {exc}")
        return reasons

    fresh, message = check_summary_output(summary_path, summary, "json")
    if not fresh:
        reasons.append(message)

    if summary.lemma_id != candidate.id:
        reasons.append(
            f"proof-obligation report lemma_id {summary.lemma_id!r} does not match "
            f"candidate id {candidate.id!r}"
        )
    if summary.candidate_status != "candidate":
        reasons.append(
            f"proof-obligation report candidate_status must be 'candidate', got {summary.candidate_status!r}"
        )
    if not summary.active_candidate:
        reasons.append("proof-obligation report active_candidate must be true for candidate emission")
    if summary.promotion_blocker_count != 0:
        reasons.append(
            "proof-obligation report still has promotion blockers: "
            + ", ".join(summary.promotion_blocker_keys)
        )
    if summary.has_active_candidate_blocker_conflict:
        reasons.append("proof-obligation report has active-candidate/blocker conflict")

    return reasons


def _assess_source_index_gate(candidate: LemmaCandidate) -> list[str]:
    reasons: list[str] = []
    markdown_path, markdown_error = _metadata_path(
        candidate,
        BLOCKER_SOURCE_INDEX_MARKDOWN_KEY,
    )
    json_path, json_error = _metadata_path(candidate, BLOCKER_SOURCE_INDEX_JSON_KEY)
    if markdown_error:
        reasons.append(markdown_error)
    if json_error:
        reasons.append(json_error)
    if markdown_path is None or json_path is None:
        return reasons

    try:
        source_index = build_source_index()
    except (BlockerMatrixError, SourceIndexError) as exc:
        reasons.append(f"invalid blocker source index: {exc}")
        return reasons

    for path, output_format in (
        (markdown_path, "markdown"),
        (json_path, "json"),
    ):
        fresh, message = check_source_index_output(path, source_index, output_format)
        if not fresh:
            reasons.append(message)

    sources_ok, message = check_sources_exist(source_index)
    if not sources_ok:
        reasons.append(message)

    return reasons
