from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REPORT_DIR = ROOT / "track-a-regularity/reports"
DEFAULT_MARKDOWN_OUTPUT = (
    DEFAULT_REPORT_DIR
    / "lemma_0252_smooth_continuation_source_read_stack_dashboard.md"
)
DEFAULT_JSON_OUTPUT = (
    DEFAULT_REPORT_DIR
    / "lemma_0252_smooth_continuation_source_read_stack_dashboard.json"
)
DEFAULT_PACKET_MARKDOWN = (
    DEFAULT_REPORT_DIR / "lemma_0252_smooth_continuation_source_read_packet.md"
)
DEFAULT_PACKET_JSON = (
    DEFAULT_REPORT_DIR / "lemma_0252_smooth_continuation_source_read_packet.json"
)
DEFAULT_PACKET_DEPENDENCY_MARKDOWN = (
    DEFAULT_REPORT_DIR
    / "lemma_0252_smooth_continuation_source_read_packet_dependency.md"
)
DEFAULT_PACKET_DEPENDENCY_JSON = (
    DEFAULT_REPORT_DIR
    / "lemma_0252_smooth_continuation_source_read_packet_dependency.json"
)
DEFAULT_OPERATOR_MARKDOWN = (
    DEFAULT_REPORT_DIR
    / "lemma_0252_smooth_continuation_source_read_packet_operator_index.md"
)
DEFAULT_OPERATOR_JSON = (
    DEFAULT_REPORT_DIR
    / "lemma_0252_smooth_continuation_source_read_packet_operator_index.json"
)
DEFAULT_OPERATOR_DEPENDENCY_MARKDOWN = (
    DEFAULT_REPORT_DIR
    / "lemma_0252_smooth_continuation_source_read_packet_operator_dependency.md"
)
DEFAULT_OPERATOR_DEPENDENCY_JSON = (
    DEFAULT_REPORT_DIR
    / "lemma_0252_smooth_continuation_source_read_packet_operator_dependency.json"
)
DEFAULT_PAPERS_INDEX = ROOT / "papers/blockers/index.md"

GAP_ID = "gap_004"
SOURCE_BRANCH = "smooth_continuation_bridge"
PACKET_STATUS = "blocked_source_read_only"
PACKET_BRANCH_VERDICT = "blocked_needs_new_result"
CHECKLIST_BRANCH_VERDICT = "deferred_needs_new_result"

NON_CLAIMS = (
    "read_only_smooth_continuation_source_read_stack_dashboard",
    "operator_dashboard_for_review_only",
    "non_promotional_gap_004_stack_surface",
    "no_candidate_promotion",
    "no_candidate_emission",
    "no_blocker_discharge",
    "no_process_gate_opened",
    "no_file_copy",
    "no_bkm_theorem",
    "no_serrin_theorem",
    "no_high_sobolev_continuation_bridge",
    "no_weak_to_smooth_upgrade",
    "no_navier_stokes_solution",
)


@dataclass(frozen=True)
class SmoothContinuationSourceReadStackDashboardSection:
    step: int
    name: str
    role: str
    markdown_report: str
    json_report: str
    primary_count_label: str
    primary_count: int
    failed_count_label: str
    failed_count: int
    consistent_label: str
    consistent: bool
    blocked_count: int
    actionable_count: int


@dataclass(frozen=True)
class SmoothContinuationSourceReadStackDashboardCheck:
    key: str
    expected: str
    observed: str
    passed: bool
    source_artifacts: tuple[str, ...]


@dataclass(frozen=True)
class Lemma0252SmoothContinuationSourceReadStackDashboard:
    schema_version: int
    lemma_id: str
    candidate_status: str
    active_candidate: bool
    gap_id: str
    source_branch: str
    packet_markdown: str
    packet_json: str
    packet_dependency_markdown: str
    packet_dependency_json: str
    operator_markdown: str
    operator_json: str
    operator_dependency_markdown: str
    operator_dependency_json: str
    papers_blockers_index: str
    stack_step_count: int
    source_report_count: int
    source_ref_count: int
    smooth_continuation_source_read_stack_dashboard_check_count: int
    passed_smooth_continuation_source_read_stack_dashboard_check_count: int
    failed_smooth_continuation_source_read_stack_dashboard_check_count: int
    smooth_continuation_source_read_stack_dashboard_consistent: bool
    source_read_count: int
    direct_branch_source_read_count: int
    cross_cutting_source_read_count: int
    blocked_source_read_count: int
    actionable_source_read_count: int
    may_discharge_source_read_count: int
    exact_discharge_artifact_count: int
    packet_status: str
    packet_branch_verdict: str
    packet_check_count: int
    failed_packet_check_count: int
    packet_consistent: bool
    packet_dependency_check_count: int
    failed_packet_dependency_check_count: int
    packet_dependency_consistent: bool
    operator_index_check_count: int
    failed_operator_index_check_count: int
    operator_index_consistent: bool
    operator_dependency_check_count: int
    failed_operator_dependency_check_count: int
    operator_dependency_consistent: bool
    checklist_branch_verdict: str
    checklist_item_count: int
    theorem_branch_count: int
    dischargeable_now_count: int
    queue_item_count: int
    blocked_queue_item_count: int
    actionable_queue_item_count: int
    may_discharge_queue_item_count: int
    direct_theorem_artifact_count: int
    process_gate_open_authorized: bool
    blocker_state_changed: bool
    candidate_emission_authorized: bool
    missing_source_count: int
    missing_sources: tuple[str, ...]
    sections: tuple[SmoothContinuationSourceReadStackDashboardSection, ...]
    checks: tuple[SmoothContinuationSourceReadStackDashboardCheck, ...]
    issues: tuple[str, ...]
    source_refs: tuple[str, ...]
    source_read_ids: tuple[str, ...]
    checklist_item_ids: tuple[str, ...]
    non_claims: tuple[str, ...]
    packet_snapshot: dict[str, object]
    packet_dependency_snapshot: dict[str, object]
    operator_snapshot: dict[str, object]
    operator_dependency_snapshot: dict[str, object]


def _load_json(path: Path) -> dict[str, object]:
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"expected object JSON report: {path}")
    return data


def _check(
    *,
    key: str,
    expected: object,
    observed: object,
    source_artifacts: tuple[str, ...],
) -> SmoothContinuationSourceReadStackDashboardCheck:
    return SmoothContinuationSourceReadStackDashboardCheck(
        key=key,
        expected=str(expected),
        observed=str(observed),
        passed=expected == observed,
        source_artifacts=source_artifacts,
    )


def _missing_sources(source_refs: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(source for source in source_refs if not (ROOT / source).exists())


def _direct_source_reports() -> tuple[str, ...]:
    return (
        "track-a-regularity/reports/lemma_0252_smooth_continuation_source_read_packet.md",
        "track-a-regularity/reports/lemma_0252_smooth_continuation_source_read_packet.json",
        (
            "track-a-regularity/reports/"
            "lemma_0252_smooth_continuation_source_read_packet_dependency.md"
        ),
        (
            "track-a-regularity/reports/"
            "lemma_0252_smooth_continuation_source_read_packet_dependency.json"
        ),
        (
            "track-a-regularity/reports/"
            "lemma_0252_smooth_continuation_source_read_packet_operator_index.md"
        ),
        (
            "track-a-regularity/reports/"
            "lemma_0252_smooth_continuation_source_read_packet_operator_index.json"
        ),
        (
            "track-a-regularity/reports/"
            "lemma_0252_smooth_continuation_source_read_packet_operator_dependency.md"
        ),
        (
            "track-a-regularity/reports/"
            "lemma_0252_smooth_continuation_source_read_packet_operator_dependency.json"
        ),
    )


def _source_ids_from_packet(packet: dict[str, object]) -> tuple[str, ...]:
    return tuple(
        str(item.get("source_id"))
        for item in packet.get("source_reads", ())
        if isinstance(item, dict)
    )


def _blocked_source_read_count(report: dict[str, object]) -> int:
    if "blocked_source_read_count" in report:
        return int(report.get("blocked_source_read_count", 0))
    if (
        int(report.get("actionable_source_read_count", 0)) == 0
        and int(report.get("may_discharge_source_read_count", 0)) == 0
    ):
        return int(report.get("source_read_count", 0))
    return 0


def _sections(
    packet: dict[str, object],
    dependency: dict[str, object],
    operator: dict[str, object],
    operator_dependency: dict[str, object],
) -> tuple[SmoothContinuationSourceReadStackDashboardSection, ...]:
    return (
        SmoothContinuationSourceReadStackDashboardSection(
            step=120,
            name="smooth_continuation_source_read_packet",
            role=(
                "Extracts theorem hypotheses, conclusion shape, and mismatch fields "
                "from local smooth-continuation sources for gap_004."
            ),
            markdown_report=str(DEFAULT_PACKET_MARKDOWN),
            json_report=str(DEFAULT_PACKET_JSON),
            primary_count_label="source_read_count",
            primary_count=int(packet.get("source_read_count", 0)),
            failed_count_label="failed_packet_check_count",
            failed_count=int(packet.get("failed_packet_check_count", 0)),
            consistent_label="packet_consistent",
            consistent=bool(packet.get("packet_consistent")),
            blocked_count=int(packet.get("blocked_source_read_count", 0)),
            actionable_count=int(packet.get("actionable_source_read_count", 0)),
        ),
        SmoothContinuationSourceReadStackDashboardSection(
            step=121,
            name="smooth_continuation_source_read_packet_dependency",
            role=(
                "Prevents the Step 120 source-read packet from drifting away from "
                "the Step 90 checklist, queue stack, and papers/blockers inventory."
            ),
            markdown_report=str(DEFAULT_PACKET_DEPENDENCY_MARKDOWN),
            json_report=str(DEFAULT_PACKET_DEPENDENCY_JSON),
            primary_count_label=(
                "smooth_continuation_source_read_packet_dependency_check_count"
            ),
            primary_count=int(
                dependency.get(
                    "smooth_continuation_source_read_packet_dependency_check_count", 0
                )
            ),
            failed_count_label=(
                "failed_smooth_continuation_source_read_packet_dependency_check_count"
            ),
            failed_count=int(
                dependency.get(
                    "failed_smooth_continuation_source_read_packet_dependency_check_count",
                    0,
                )
            ),
            consistent_label="smooth_continuation_source_read_packet_dependency_consistent",
            consistent=bool(
                dependency.get(
                    "smooth_continuation_source_read_packet_dependency_consistent"
                )
            ),
            blocked_count=_blocked_source_read_count(dependency),
            actionable_count=int(dependency.get("actionable_source_read_count", 0)),
        ),
        SmoothContinuationSourceReadStackDashboardSection(
            step=122,
            name="smooth_continuation_source_read_packet_operator_index",
            role=(
                "Consolidates the source-read packet and dependency guard into a "
                "compact operator/source index."
            ),
            markdown_report=str(DEFAULT_OPERATOR_MARKDOWN),
            json_report=str(DEFAULT_OPERATOR_JSON),
            primary_count_label=(
                "smooth_continuation_source_read_packet_operator_index_check_count"
            ),
            primary_count=int(
                operator.get(
                    "smooth_continuation_source_read_packet_operator_index_check_count",
                    0,
                )
            ),
            failed_count_label=(
                "failed_smooth_continuation_source_read_packet_operator_index_check_count"
            ),
            failed_count=int(
                operator.get(
                    "failed_smooth_continuation_source_read_packet_operator_index_check_count",
                    0,
                )
            ),
            consistent_label=(
                "smooth_continuation_source_read_packet_operator_index_consistent"
            ),
            consistent=bool(
                operator.get(
                    "smooth_continuation_source_read_packet_operator_index_consistent"
                )
            ),
            blocked_count=int(operator.get("blocked_source_read_count", 0)),
            actionable_count=int(operator.get("actionable_source_read_count", 0)),
        ),
        SmoothContinuationSourceReadStackDashboardSection(
            step=123,
            name="smooth_continuation_source_read_packet_operator_dependency",
            role=(
                "Guards the Step 122 operator/source index against drift from the "
                "underlying packet, dependency guard, checklist, queue stack, and "
                "local blocker-paper inventory."
            ),
            markdown_report=str(DEFAULT_OPERATOR_DEPENDENCY_MARKDOWN),
            json_report=str(DEFAULT_OPERATOR_DEPENDENCY_JSON),
            primary_count_label=(
                "smooth_continuation_source_read_packet_operator_dependency_check_count"
            ),
            primary_count=int(
                operator_dependency.get(
                    "smooth_continuation_source_read_packet_operator_dependency_check_count",
                    0,
                )
            ),
            failed_count_label=(
                "failed_smooth_continuation_source_read_packet_operator_dependency_check_count"
            ),
            failed_count=int(
                operator_dependency.get(
                    "failed_smooth_continuation_source_read_packet_operator_dependency_check_count",
                    0,
                )
            ),
            consistent_label=(
                "smooth_continuation_source_read_packet_operator_dependency_consistent"
            ),
            consistent=bool(
                operator_dependency.get(
                    "smooth_continuation_source_read_packet_operator_dependency_consistent"
                )
            ),
            blocked_count=int(operator_dependency.get("blocked_source_read_count", 0)),
            actionable_count=int(
                operator_dependency.get("actionable_source_read_count", 0)
            ),
        ),
    )


def build_smooth_continuation_source_read_stack_dashboard(
    *,
    packet_json: Path = DEFAULT_PACKET_JSON,
    packet_dependency_json: Path = DEFAULT_PACKET_DEPENDENCY_JSON,
    operator_json: Path = DEFAULT_OPERATOR_JSON,
    operator_dependency_json: Path = DEFAULT_OPERATOR_DEPENDENCY_JSON,
    papers_blockers_index: Path = DEFAULT_PAPERS_INDEX,
) -> Lemma0252SmoothContinuationSourceReadStackDashboard:
    packet = _load_json(packet_json)
    dependency = _load_json(packet_dependency_json)
    operator = _load_json(operator_json)
    operator_dependency = _load_json(operator_dependency_json)

    direct_reports = _direct_source_reports()
    source_refs = tuple(
        dict.fromkeys(
            direct_reports
            + ("papers/blockers/index.md",)
            + tuple(str(item) for item in packet.get("source_refs", ()))
            + tuple(str(item) for item in dependency.get("source_refs", ()))
            + tuple(str(item) for item in operator.get("source_refs", ()))
            + tuple(str(item) for item in operator_dependency.get("source_refs", ()))
        )
    )
    missing_sources = _missing_sources(source_refs)
    source_read_ids = _source_ids_from_packet(packet)
    checklist_item_ids = tuple(str(item) for item in operator_dependency.get("checklist_item_ids", ()))

    packet_source = (
        "track-a-regularity/reports/lemma_0252_smooth_continuation_source_read_packet.md",
        "track-a-regularity/reports/lemma_0252_smooth_continuation_source_read_packet.json",
    )
    dependency_source = (
        (
            "track-a-regularity/reports/"
            "lemma_0252_smooth_continuation_source_read_packet_dependency.md"
        ),
        (
            "track-a-regularity/reports/"
            "lemma_0252_smooth_continuation_source_read_packet_dependency.json"
        ),
    )
    operator_source = (
        (
            "track-a-regularity/reports/"
            "lemma_0252_smooth_continuation_source_read_packet_operator_index.md"
        ),
        (
            "track-a-regularity/reports/"
            "lemma_0252_smooth_continuation_source_read_packet_operator_index.json"
        ),
    )
    operator_dependency_source = (
        (
            "track-a-regularity/reports/"
            "lemma_0252_smooth_continuation_source_read_packet_operator_dependency.md"
        ),
        (
            "track-a-regularity/reports/"
            "lemma_0252_smooth_continuation_source_read_packet_operator_dependency.json"
        ),
    )

    checks = (
        _check(
            key="packet.lemma_id.expected_lemma_0252",
            expected="lemma_0252",
            observed=packet.get("lemma_id"),
            source_artifacts=packet_source,
        ),
        _check(
            key="dependency.lemma_id.matches_packet",
            expected=packet.get("lemma_id"),
            observed=dependency.get("lemma_id"),
            source_artifacts=packet_source + dependency_source,
        ),
        _check(
            key="operator.lemma_id.matches_packet",
            expected=packet.get("lemma_id"),
            observed=operator.get("lemma_id"),
            source_artifacts=packet_source + operator_source,
        ),
        _check(
            key="operator_dependency.lemma_id.matches_packet",
            expected=packet.get("lemma_id"),
            observed=operator_dependency.get("lemma_id"),
            source_artifacts=packet_source + operator_dependency_source,
        ),
        _check(
            key="all.candidate_status.remains_needs_review",
            expected=("needs_review",) * 4,
            observed=(
                packet.get("candidate_status"),
                dependency.get("candidate_status"),
                operator.get("candidate_status"),
                operator_dependency.get("candidate_status"),
            ),
            source_artifacts=direct_reports,
        ),
        _check(
            key="all.active_candidate.false",
            expected=(False,) * 4,
            observed=(
                packet.get("active_candidate"),
                dependency.get("active_candidate"),
                operator.get("active_candidate"),
                operator_dependency.get("active_candidate"),
            ),
            source_artifacts=direct_reports,
        ),
        _check(
            key="all.gap_id.expected_gap_004",
            expected=(GAP_ID,) * 4,
            observed=(
                packet.get("gap_id"),
                dependency.get("gap_id"),
                operator.get("gap_id"),
                operator_dependency.get("gap_id"),
            ),
            source_artifacts=direct_reports,
        ),
        _check(
            key="all.source_branch.expected_smooth_continuation_bridge",
            expected=(SOURCE_BRANCH,) * 4,
            observed=(
                packet.get("source_branch"),
                dependency.get("source_branch"),
                operator.get("source_branch"),
                operator_dependency.get("source_branch"),
            ),
            source_artifacts=direct_reports,
        ),
        _check(
            key="packet.status.remains_blocked",
            expected=PACKET_STATUS,
            observed=packet.get("packet_status"),
            source_artifacts=packet_source,
        ),
        _check(
            key="packet.branch_verdict.remains_blocked_needs_new_result",
            expected=PACKET_BRANCH_VERDICT,
            observed=packet.get("branch_verdict"),
            source_artifacts=packet_source,
        ),
        _check(
            key="all.source_read_count.matches_packet",
            expected=(2, 2, 2, 2),
            observed=(
                packet.get("source_read_count"),
                dependency.get("source_read_count"),
                operator.get("source_read_count"),
                operator_dependency.get("source_read_count"),
            ),
            source_artifacts=direct_reports,
        ),
        _check(
            key="all.blocked_source_read_count.matches_source_read_count",
            expected=(2, 2, 2, 2),
            observed=(
                _blocked_source_read_count(packet),
                _blocked_source_read_count(dependency),
                _blocked_source_read_count(operator),
                _blocked_source_read_count(operator_dependency),
            ),
            source_artifacts=direct_reports,
        ),
        _check(
            key="all.actionable_source_read_count.remains_zero",
            expected=(0, 0, 0, 0),
            observed=(
                packet.get("actionable_source_read_count"),
                dependency.get("actionable_source_read_count"),
                operator.get("actionable_source_read_count"),
                operator_dependency.get("actionable_source_read_count"),
            ),
            source_artifacts=direct_reports,
        ),
        _check(
            key="all.may_discharge_source_read_count.remains_zero",
            expected=(0, 0, 0, 0),
            observed=(
                packet.get("may_discharge_source_read_count"),
                dependency.get("may_discharge_source_read_count"),
                operator.get("may_discharge_source_read_count"),
                operator_dependency.get("may_discharge_source_read_count"),
            ),
            source_artifacts=direct_reports,
        ),
        _check(
            key="all.exact_discharge_artifact_count.remains_zero",
            expected=(0, 0, 0, 0),
            observed=(
                packet.get("exact_discharge_artifact_count"),
                dependency.get("exact_discharge_artifact_count"),
                operator.get("exact_discharge_artifact_count"),
                operator_dependency.get("exact_discharge_artifact_count"),
            ),
            source_artifacts=direct_reports,
        ),
        _check(
            key="packet.check_count.expected_thirty_four",
            expected=34,
            observed=packet.get("packet_check_count"),
            source_artifacts=packet_source,
        ),
        _check(
            key="packet.failed_checks.remain_zero",
            expected=0,
            observed=packet.get("failed_packet_check_count"),
            source_artifacts=packet_source,
        ),
        _check(
            key="packet.consistent.true",
            expected=True,
            observed=packet.get("packet_consistent"),
            source_artifacts=packet_source,
        ),
        _check(
            key="dependency.check_count.expected_fifty",
            expected=50,
            observed=dependency.get(
                "smooth_continuation_source_read_packet_dependency_check_count"
            ),
            source_artifacts=dependency_source,
        ),
        _check(
            key="dependency.failed_checks.remain_zero",
            expected=0,
            observed=dependency.get(
                "failed_smooth_continuation_source_read_packet_dependency_check_count"
            ),
            source_artifacts=dependency_source,
        ),
        _check(
            key="dependency.consistent.true",
            expected=True,
            observed=dependency.get(
                "smooth_continuation_source_read_packet_dependency_consistent"
            ),
            source_artifacts=dependency_source,
        ),
        _check(
            key="operator.index_check_count.expected_thirty_seven",
            expected=37,
            observed=operator.get(
                "smooth_continuation_source_read_packet_operator_index_check_count"
            ),
            source_artifacts=operator_source,
        ),
        _check(
            key="operator.failed_checks.remain_zero",
            expected=0,
            observed=operator.get(
                "failed_smooth_continuation_source_read_packet_operator_index_check_count"
            ),
            source_artifacts=operator_source,
        ),
        _check(
            key="operator.consistent.true",
            expected=True,
            observed=operator.get(
                "smooth_continuation_source_read_packet_operator_index_consistent"
            ),
            source_artifacts=operator_source,
        ),
        _check(
            key="operator_dependency.check_count.expected_fifty_seven",
            expected=57,
            observed=operator_dependency.get(
                "smooth_continuation_source_read_packet_operator_dependency_check_count"
            ),
            source_artifacts=operator_dependency_source,
        ),
        _check(
            key="operator_dependency.failed_checks.remain_zero",
            expected=0,
            observed=operator_dependency.get(
                "failed_smooth_continuation_source_read_packet_operator_dependency_check_count"
            ),
            source_artifacts=operator_dependency_source,
        ),
        _check(
            key="operator_dependency.consistent.true",
            expected=True,
            observed=operator_dependency.get(
                "smooth_continuation_source_read_packet_operator_dependency_consistent"
            ),
            source_artifacts=operator_dependency_source,
        ),
        _check(
            key="operator.section_count.expected_two",
            expected=2,
            observed=operator.get("section_count"),
            source_artifacts=operator_source,
        ),
        _check(
            key="operator.source_report_count.expected_four",
            expected=4,
            observed=operator.get("source_report_count"),
            source_artifacts=operator_source,
        ),
        _check(
            key="operator_dependency.direct_source_report_count.expected_sixteen",
            expected=16,
            observed=operator_dependency.get("direct_source_report_count"),
            source_artifacts=operator_dependency_source,
        ),
        _check(
            key="operator_dependency.checklist_branch_verdict.deferred",
            expected=CHECKLIST_BRANCH_VERDICT,
            observed=operator_dependency.get("checklist_branch_verdict"),
            source_artifacts=operator_dependency_source,
        ),
        _check(
            key="operator_dependency.checklist_item_count.expected_seven",
            expected=7,
            observed=operator_dependency.get("checklist_item_count"),
            source_artifacts=operator_dependency_source,
        ),
        _check(
            key="operator_dependency.theorem_branch_count.expected_five",
            expected=5,
            observed=operator_dependency.get("theorem_branch_count"),
            source_artifacts=operator_dependency_source,
        ),
        _check(
            key="operator_dependency.dischargeable_now_count.remains_zero",
            expected=0,
            observed=operator_dependency.get("dischargeable_now_count"),
            source_artifacts=operator_dependency_source,
        ),
        _check(
            key="operator_dependency.queue_counts.remain_blocked",
            expected=(3, 3, 0, 0, 0),
            observed=(
                operator_dependency.get("queue_item_count"),
                operator_dependency.get("blocked_queue_item_count"),
                operator_dependency.get("actionable_queue_item_count"),
                operator_dependency.get("may_discharge_queue_item_count"),
                operator_dependency.get("direct_theorem_artifact_count"),
            ),
            source_artifacts=operator_dependency_source,
        ),
        _check(
            key="operator_dependency.queue_dependency.failed_checks.remain_zero",
            expected=0,
            observed=operator_dependency.get(
                "failed_theorem_artifact_review_queue_dependency_check_count"
            ),
            source_artifacts=operator_dependency_source,
        ),
        _check(
            key="operator_dependency.queue_operator.failed_checks.remain_zero",
            expected=0,
            observed=operator_dependency.get(
                "failed_theorem_artifact_review_queue_operator_index_check_count"
            ),
            source_artifacts=operator_dependency_source,
        ),
        _check(
            key="operator_dependency.queue_operator_dependency.failed_checks.remain_zero",
            expected=0,
            observed=operator_dependency.get(
                "failed_theorem_artifact_review_queue_operator_dependency_check_count"
            ),
            source_artifacts=operator_dependency_source,
        ),
        _check(
            key="all.process_gate_open_authorized.false",
            expected=(False, False, False, False),
            observed=(
                packet.get("process_gate_open_authorized"),
                dependency.get("process_gate_open_authorized"),
                operator.get("process_gate_open_authorized"),
                operator_dependency.get("process_gate_open_authorized"),
            ),
            source_artifacts=direct_reports,
        ),
        _check(
            key="all.blocker_state_changed.false",
            expected=(False, False, False, False),
            observed=(
                packet.get("blocker_state_changed"),
                dependency.get("blocker_state_changed"),
                operator.get("blocker_state_changed"),
                operator_dependency.get("blocker_state_changed"),
            ),
            source_artifacts=direct_reports,
        ),
        _check(
            key="all.candidate_emission_authorized.false",
            expected=(False, False, False, False),
            observed=(
                packet.get("candidate_emission_authorized"),
                dependency.get("candidate_emission_authorized"),
                operator.get("candidate_emission_authorized"),
                operator_dependency.get("candidate_emission_authorized"),
            ),
            source_artifacts=direct_reports,
        ),
        _check(
            key="all.missing_source_count.remains_zero",
            expected=(0, 0, 0, 0),
            observed=(
                packet.get("missing_source_count"),
                dependency.get("missing_source_count"),
                operator.get("missing_source_count"),
                operator_dependency.get("missing_source_count"),
            ),
            source_artifacts=direct_reports,
        ),
        _check(
            key="source_refs.missing_count.remains_zero",
            expected=0,
            observed=len(missing_sources),
            source_artifacts=source_refs,
        ),
        _check(
            key="source_refs.include_step_120_to_123_reports",
            expected=True,
            observed=all(source in source_refs for source in direct_reports),
            source_artifacts=direct_reports,
        ),
        _check(
            key="source_refs.include_papers_blockers_index",
            expected=True,
            observed="papers/blockers/index.md" in source_refs and papers_blockers_index.exists(),
            source_artifacts=("papers/blockers/index.md",),
        ),
        _check(
            key="source_refs.include_step_90_checklist_reports",
            expected=True,
            observed=(
                "track-a-regularity/reports/lemma_0252_smooth_continuation_checklist.md"
                in source_refs
                and "track-a-regularity/reports/lemma_0252_smooth_continuation_checklist.json"
                in source_refs
            ),
            source_artifacts=source_refs,
        ),
        _check(
            key="source_refs.include_theorem_queue_stack_reports",
            expected=True,
            observed=(
                "track-a-regularity/reports/"
                "lemma_0252_theorem_artifact_review_queue_operator_dependency.json"
            )
            in source_refs,
            source_artifacts=source_refs,
        ),
        _check(
            key="source_refs.include_smooth_continuation_local_pdfs",
            expected=True,
            observed=(
                "papers/blockers/smooth_continuation_bridge/"
                "math0703883_besov_negative_blowup.pdf"
            )
            in source_refs
            and (
                "papers/blockers/smooth_continuation_bridge/"
                "1410.4495_robinson_review_NSE.pdf"
            )
            in source_refs,
            source_artifacts=source_refs,
        ),
        _check(
            key="source_read_ids.expected_two_local_sources",
            expected=("besov_negative_math0703883", "robinson_review_1410_4495"),
            observed=source_read_ids,
            source_artifacts=packet_source,
        ),
    )
    issues = tuple(check.key for check in checks if not check.passed)
    reports = (packet, dependency, operator, operator_dependency)

    return Lemma0252SmoothContinuationSourceReadStackDashboard(
        schema_version=1,
        lemma_id=str(packet.get("lemma_id")),
        candidate_status=str(packet.get("candidate_status")),
        active_candidate=bool(packet.get("active_candidate")),
        gap_id=GAP_ID,
        source_branch=SOURCE_BRANCH,
        packet_markdown=str(DEFAULT_PACKET_MARKDOWN),
        packet_json=str(DEFAULT_PACKET_JSON),
        packet_dependency_markdown=str(DEFAULT_PACKET_DEPENDENCY_MARKDOWN),
        packet_dependency_json=str(DEFAULT_PACKET_DEPENDENCY_JSON),
        operator_markdown=str(DEFAULT_OPERATOR_MARKDOWN),
        operator_json=str(DEFAULT_OPERATOR_JSON),
        operator_dependency_markdown=str(DEFAULT_OPERATOR_DEPENDENCY_MARKDOWN),
        operator_dependency_json=str(DEFAULT_OPERATOR_DEPENDENCY_JSON),
        papers_blockers_index=str(DEFAULT_PAPERS_INDEX),
        stack_step_count=4,
        source_report_count=len(direct_reports),
        source_ref_count=len(source_refs),
        smooth_continuation_source_read_stack_dashboard_check_count=len(checks),
        passed_smooth_continuation_source_read_stack_dashboard_check_count=sum(
            1 for check in checks if check.passed
        ),
        failed_smooth_continuation_source_read_stack_dashboard_check_count=len(issues),
        smooth_continuation_source_read_stack_dashboard_consistent=len(issues) == 0,
        source_read_count=int(packet.get("source_read_count", 0)),
        direct_branch_source_read_count=int(
            packet.get("direct_branch_source_read_count", 0)
        ),
        cross_cutting_source_read_count=int(
            packet.get("cross_cutting_source_read_count", 0)
        ),
        blocked_source_read_count=int(packet.get("blocked_source_read_count", 0)),
        actionable_source_read_count=int(packet.get("actionable_source_read_count", 0)),
        may_discharge_source_read_count=int(
            packet.get("may_discharge_source_read_count", 0)
        ),
        exact_discharge_artifact_count=int(
            packet.get("exact_discharge_artifact_count", 0)
        ),
        packet_status=str(packet.get("packet_status")),
        packet_branch_verdict=str(packet.get("branch_verdict")),
        packet_check_count=int(packet.get("packet_check_count", 0)),
        failed_packet_check_count=int(packet.get("failed_packet_check_count", 0)),
        packet_consistent=bool(packet.get("packet_consistent")),
        packet_dependency_check_count=int(
            dependency.get(
                "smooth_continuation_source_read_packet_dependency_check_count", 0
            )
        ),
        failed_packet_dependency_check_count=int(
            dependency.get(
                "failed_smooth_continuation_source_read_packet_dependency_check_count",
                0,
            )
        ),
        packet_dependency_consistent=bool(
            dependency.get("smooth_continuation_source_read_packet_dependency_consistent")
        ),
        operator_index_check_count=int(
            operator.get(
                "smooth_continuation_source_read_packet_operator_index_check_count", 0
            )
        ),
        failed_operator_index_check_count=int(
            operator.get(
                "failed_smooth_continuation_source_read_packet_operator_index_check_count",
                0,
            )
        ),
        operator_index_consistent=bool(
            operator.get("smooth_continuation_source_read_packet_operator_index_consistent")
        ),
        operator_dependency_check_count=int(
            operator_dependency.get(
                "smooth_continuation_source_read_packet_operator_dependency_check_count",
                0,
            )
        ),
        failed_operator_dependency_check_count=int(
            operator_dependency.get(
                "failed_smooth_continuation_source_read_packet_operator_dependency_check_count",
                0,
            )
        ),
        operator_dependency_consistent=bool(
            operator_dependency.get(
                "smooth_continuation_source_read_packet_operator_dependency_consistent"
            )
        ),
        checklist_branch_verdict=str(
            operator_dependency.get("checklist_branch_verdict")
        ),
        checklist_item_count=int(operator_dependency.get("checklist_item_count", 0)),
        theorem_branch_count=int(operator_dependency.get("theorem_branch_count", 0)),
        dischargeable_now_count=int(operator_dependency.get("dischargeable_now_count", 0)),
        queue_item_count=int(operator_dependency.get("queue_item_count", 0)),
        blocked_queue_item_count=int(operator_dependency.get("blocked_queue_item_count", 0)),
        actionable_queue_item_count=int(
            operator_dependency.get("actionable_queue_item_count", 0)
        ),
        may_discharge_queue_item_count=int(
            operator_dependency.get("may_discharge_queue_item_count", 0)
        ),
        direct_theorem_artifact_count=int(
            operator_dependency.get("direct_theorem_artifact_count", 0)
        ),
        process_gate_open_authorized=any(
            bool(report.get("process_gate_open_authorized")) for report in reports
        ),
        blocker_state_changed=any(
            bool(report.get("blocker_state_changed")) for report in reports
        ),
        candidate_emission_authorized=any(
            bool(report.get("candidate_emission_authorized")) for report in reports
        ),
        missing_source_count=len(missing_sources),
        missing_sources=missing_sources,
        sections=_sections(packet, dependency, operator, operator_dependency),
        checks=checks,
        issues=issues,
        source_refs=source_refs,
        source_read_ids=source_read_ids,
        checklist_item_ids=checklist_item_ids,
        non_claims=NON_CLAIMS,
        packet_snapshot=packet,
        packet_dependency_snapshot=dependency,
        operator_snapshot=operator,
        operator_dependency_snapshot=operator_dependency,
    )


def render_markdown(report: Lemma0252SmoothContinuationSourceReadStackDashboard) -> str:
    lines = [
        "# Lemma 0252 Smooth-Continuation Source Read Stack Dashboard",
        "",
        "## Summary",
        "",
        f"- lemma_id: `{report.lemma_id}`",
        f"- candidate_status: `{report.candidate_status}`",
        f"- active_candidate: `{str(report.active_candidate).lower()}`",
        f"- gap_id: `{report.gap_id}`",
        f"- source_branch: `{report.source_branch}`",
        f"- stack_step_count: `{report.stack_step_count}`",
        f"- source_report_count: `{report.source_report_count}`",
        f"- source_ref_count: `{report.source_ref_count}`",
        (
            "- smooth_continuation_source_read_stack_dashboard_check_count: "
            f"`{report.smooth_continuation_source_read_stack_dashboard_check_count}`"
        ),
        (
            "- failed_smooth_continuation_source_read_stack_dashboard_check_count: "
            f"`{report.failed_smooth_continuation_source_read_stack_dashboard_check_count}`"
        ),
        (
            "- smooth_continuation_source_read_stack_dashboard_consistent: "
            f"`{str(report.smooth_continuation_source_read_stack_dashboard_consistent).lower()}`"
        ),
        f"- source_read_count: `{report.source_read_count}`",
        f"- blocked_source_read_count: `{report.blocked_source_read_count}`",
        f"- actionable_source_read_count: `{report.actionable_source_read_count}`",
        f"- may_discharge_source_read_count: `{report.may_discharge_source_read_count}`",
        f"- exact_discharge_artifact_count: `{report.exact_discharge_artifact_count}`",
        f"- packet_check_count: `{report.packet_check_count}`",
        f"- packet_dependency_check_count: `{report.packet_dependency_check_count}`",
        f"- operator_index_check_count: `{report.operator_index_check_count}`",
        f"- operator_dependency_check_count: `{report.operator_dependency_check_count}`",
        f"- checklist_branch_verdict: `{report.checklist_branch_verdict}`",
        f"- dischargeable_now_count: `{report.dischargeable_now_count}`",
        f"- queue_item_count: `{report.queue_item_count}`",
        f"- blocked_queue_item_count: `{report.blocked_queue_item_count}`",
        f"- direct_theorem_artifact_count: `{report.direct_theorem_artifact_count}`",
        f"- process_gate_open_authorized: `{str(report.process_gate_open_authorized).lower()}`",
        f"- blocker_state_changed: `{str(report.blocker_state_changed).lower()}`",
        f"- candidate_emission_authorized: `{str(report.candidate_emission_authorized).lower()}`",
        f"- missing_source_count: `{report.missing_source_count}`",
        "",
        "## Stack Sections",
        "",
        "| step | name | primary | failed | consistent | blocked | actionable |",
        "|---:|---|---:|---:|---:|---:|---:|",
    ]
    for section in report.sections:
        lines.append(
            f"| {section.step} | `{section.name}` | "
            f"`{section.primary_count_label}`={section.primary_count} | "
            f"`{section.failed_count_label}`={section.failed_count} | "
            f"{str(section.consistent).lower()} | "
            f"{section.blocked_count} | {section.actionable_count} |"
        )

    lines.extend(["", "## Source Reads", ""])
    lines.extend(f"- `{source_id}`" for source_id in report.source_read_ids)
    lines.extend(["", "## Checklist Items", ""])
    lines.extend(f"- `{item_id}`" for item_id in report.checklist_item_ids)
    lines.extend(["", "## Checks", ""])
    lines.extend(["| key | expected | observed | passed |", "|---|---|---|---:|"])
    for check in report.checks:
        lines.append(
            f"| `{check.key}` | `{check.expected}` | `{check.observed}` | "
            f"{str(check.passed).lower()} |"
        )

    lines.extend(["", "## Source Refs", ""])
    lines.extend(f"- `{source}`" for source in report.source_refs)
    lines.extend(["", "## Non-Claims", ""])
    lines.extend(f"- `{claim}`" for claim in report.non_claims)
    lines.append("")
    return "\n".join(lines)


def render_json(report: Lemma0252SmoothContinuationSourceReadStackDashboard) -> str:
    return json.dumps(asdict(report), indent=2, sort_keys=True) + "\n"


def check_sources(
    report: Lemma0252SmoothContinuationSourceReadStackDashboard,
) -> tuple[bool, str]:
    if report.missing_source_count:
        return False, "missing source refs: " + ", ".join(report.missing_sources)
    return True, "all smooth-continuation source-read stack dashboard sources exist"


def check_consistent(
    report: Lemma0252SmoothContinuationSourceReadStackDashboard,
) -> tuple[bool, str]:
    if not report.smooth_continuation_source_read_stack_dashboard_consistent:
        return (
            False,
            "inconsistent smooth-continuation source-read stack dashboard: "
            + ", ".join(report.issues),
        )
    return True, "smooth-continuation source-read stack dashboard is consistent"


def check_blocked(
    report: Lemma0252SmoothContinuationSourceReadStackDashboard,
) -> tuple[bool, str]:
    if (
        report.gap_id != GAP_ID
        or report.source_branch != SOURCE_BRANCH
        or report.packet_status != PACKET_STATUS
        or report.packet_branch_verdict != PACKET_BRANCH_VERDICT
        or report.checklist_branch_verdict != CHECKLIST_BRANCH_VERDICT
        or report.dischargeable_now_count != 0
        or report.blocked_source_read_count != report.source_read_count
        or report.actionable_source_read_count != 0
        or report.may_discharge_source_read_count != 0
        or report.exact_discharge_artifact_count != 0
        or report.direct_theorem_artifact_count != 0
        or report.process_gate_open_authorized
        or report.blocker_state_changed
        or report.candidate_emission_authorized
    ):
        return False, "smooth-continuation source-read stack dashboard is not blocked"
    return True, "smooth-continuation source-read stack dashboard remains blocked"


def check_output(
    output: Path,
    report: Lemma0252SmoothContinuationSourceReadStackDashboard,
    output_format: str,
) -> tuple[bool, str]:
    expected = render_json(report) if output_format == "json" else render_markdown(report)
    if not output.exists():
        return False, f"missing smooth-continuation source-read stack dashboard: {output}"
    observed = output.read_text(encoding="utf-8")
    if observed != expected:
        return False, f"stale smooth-continuation source-read stack dashboard: {output}"
    return True, f"fresh smooth-continuation source-read stack dashboard: {output}"


def _write_output(
    *,
    output: Path,
    report: Lemma0252SmoothContinuationSourceReadStackDashboard,
    output_format: str,
) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    text = render_json(report) if output_format == "json" else render_markdown(report)
    output.write_text(text, encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Render a read-only dashboard for the lemma_0252 gap_004 "
            "smooth-continuation source-read stack."
        )
    )
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--check-output", action="store_true")
    parser.add_argument("--require-sources-exist", action="store_true")
    parser.add_argument("--require-consistent", action="store_true")
    parser.add_argument("--require-blocked", action="store_true")
    args = parser.parse_args(argv)

    report = build_smooth_continuation_source_read_stack_dashboard()
    output = args.output
    if output is None:
        output = DEFAULT_JSON_OUTPUT if args.format == "json" else DEFAULT_MARKDOWN_OUTPUT

    if not args.check_output:
        _write_output(output=output, report=report, output_format=args.format)

    failures: list[str] = []
    if args.check_output:
        ok, message = check_output(output, report, args.format)
        print(message)
        if not ok:
            failures.append(message)
    if args.require_sources_exist:
        ok, message = check_sources(report)
        print(message)
        if not ok:
            failures.append(message)
    if args.require_consistent:
        ok, message = check_consistent(report)
        print(message)
        if not ok:
            failures.append(message)
    if args.require_blocked:
        ok, message = check_blocked(report)
        print(message)
        if not ok:
            failures.append(message)

    print(f"stack_step_count: {report.stack_step_count}")
    print(f"source_read_count: {report.source_read_count}")
    print(
        "smooth_continuation_source_read_stack_dashboard_check_count: "
        f"{report.smooth_continuation_source_read_stack_dashboard_check_count}"
    )
    print(
        "failed_smooth_continuation_source_read_stack_dashboard_check_count: "
        f"{report.failed_smooth_continuation_source_read_stack_dashboard_check_count}"
    )
    print(f"exact_discharge_artifact_count: {report.exact_discharge_artifact_count}")
    print(f"candidate_emission_authorized: {str(report.candidate_emission_authorized).lower()}")

    if failures:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
