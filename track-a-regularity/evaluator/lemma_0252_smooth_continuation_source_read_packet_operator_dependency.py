from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from lemma_0252_smooth_continuation_checklist import (
    DEFAULT_JSON_OUTPUT as DEFAULT_CHECKLIST_JSON,
    DEFAULT_MARKDOWN_OUTPUT as DEFAULT_CHECKLIST_MARKDOWN,
)
from lemma_0252_smooth_continuation_source_read_packet import (
    DEFAULT_JSON_OUTPUT as DEFAULT_PACKET_JSON,
    DEFAULT_MARKDOWN_OUTPUT as DEFAULT_PACKET_MARKDOWN,
)
from lemma_0252_smooth_continuation_source_read_packet_dependency import (
    DEFAULT_JSON_OUTPUT as DEFAULT_PACKET_DEPENDENCY_JSON,
    DEFAULT_MARKDOWN_OUTPUT as DEFAULT_PACKET_DEPENDENCY_MARKDOWN,
)
from lemma_0252_smooth_continuation_source_read_packet_operator_index import (
    DEFAULT_JSON_OUTPUT as DEFAULT_OPERATOR_JSON,
    DEFAULT_MARKDOWN_OUTPUT as DEFAULT_OPERATOR_MARKDOWN,
)
from lemma_0252_theorem_artifact_review_queue import (
    DEFAULT_JSON_OUTPUT as DEFAULT_QUEUE_JSON,
    DEFAULT_MARKDOWN_OUTPUT as DEFAULT_QUEUE_MARKDOWN,
)
from lemma_0252_theorem_artifact_review_queue_dependency import (
    DEFAULT_JSON_OUTPUT as DEFAULT_QUEUE_DEPENDENCY_JSON,
    DEFAULT_MARKDOWN_OUTPUT as DEFAULT_QUEUE_DEPENDENCY_MARKDOWN,
)
from lemma_0252_theorem_artifact_review_queue_operator_dependency import (
    DEFAULT_JSON_OUTPUT as DEFAULT_QUEUE_OPERATOR_DEPENDENCY_JSON,
    DEFAULT_MARKDOWN_OUTPUT as DEFAULT_QUEUE_OPERATOR_DEPENDENCY_MARKDOWN,
)
from lemma_0252_theorem_artifact_review_queue_operator_index import (
    DEFAULT_JSON_OUTPUT as DEFAULT_QUEUE_OPERATOR_JSON,
    DEFAULT_MARKDOWN_OUTPUT as DEFAULT_QUEUE_OPERATOR_MARKDOWN,
)


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REPORT_DIR = ROOT / "track-a-regularity/reports"
DEFAULT_MARKDOWN_OUTPUT = (
    DEFAULT_REPORT_DIR
    / "lemma_0252_smooth_continuation_source_read_packet_operator_dependency.md"
)
DEFAULT_JSON_OUTPUT = (
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
    "read_only_smooth_continuation_source_read_operator_dependency_guard",
    "canonical_report_freshness_only",
    "non_promotional_gap_004_operator_dependency_audit",
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
class SmoothContinuationSourceReadOperatorDependencyCheck:
    key: str
    expected: str
    observed: str
    passed: bool
    source_artifacts: tuple[str, ...]


@dataclass(frozen=True)
class Lemma0252SmoothContinuationSourceReadOperatorDependency:
    schema_version: int
    lemma_id: str
    candidate_status: str
    active_candidate: bool
    gap_id: str
    source_branch: str
    operator_markdown: str
    operator_json: str
    packet_markdown: str
    packet_json: str
    packet_dependency_markdown: str
    packet_dependency_json: str
    checklist_markdown: str
    checklist_json: str
    theorem_artifact_review_queue_markdown: str
    theorem_artifact_review_queue_json: str
    theorem_artifact_review_queue_dependency_markdown: str
    theorem_artifact_review_queue_dependency_json: str
    theorem_artifact_review_queue_operator_markdown: str
    theorem_artifact_review_queue_operator_json: str
    theorem_artifact_review_queue_operator_dependency_markdown: str
    theorem_artifact_review_queue_operator_dependency_json: str
    papers_blockers_index: str
    direct_source_report_count: int
    source_ref_count: int
    smooth_continuation_source_read_packet_operator_dependency_check_count: int
    passed_smooth_continuation_source_read_packet_operator_dependency_check_count: int
    failed_smooth_continuation_source_read_packet_operator_dependency_check_count: int
    smooth_continuation_source_read_packet_operator_dependency_consistent: bool
    operator_section_count: int
    operator_source_report_count: int
    operator_source_ref_count: int
    operator_check_count: int
    failed_operator_check_count: int
    operator_consistent: bool
    packet_status: str
    packet_branch_verdict: str
    packet_dependency_consistent: bool
    packet_dependency_check_count: int
    failed_packet_dependency_check_count: int
    checklist_branch_verdict: str
    checklist_item_count: int
    theorem_branch_count: int
    dischargeable_now_count: int
    source_read_count: int
    direct_branch_source_read_count: int
    cross_cutting_source_read_count: int
    blocked_source_read_count: int
    actionable_source_read_count: int
    may_discharge_source_read_count: int
    exact_discharge_artifact_count: int
    queue_item_count: int
    blocked_queue_item_count: int
    actionable_queue_item_count: int
    may_discharge_queue_item_count: int
    direct_theorem_artifact_count: int
    theorem_artifact_review_queue_dependency_check_count: int
    failed_theorem_artifact_review_queue_dependency_check_count: int
    theorem_artifact_review_queue_operator_index_check_count: int
    failed_theorem_artifact_review_queue_operator_index_check_count: int
    theorem_artifact_review_queue_operator_dependency_check_count: int
    failed_theorem_artifact_review_queue_operator_dependency_check_count: int
    theorem_artifact_review_queue_dependency_consistent: bool
    theorem_artifact_review_queue_operator_index_consistent: bool
    theorem_artifact_review_queue_operator_dependency_consistent: bool
    process_gate_open_authorized: bool
    blocker_state_changed: bool
    candidate_emission_authorized: bool
    missing_source_count: int
    missing_sources: tuple[str, ...]
    issues: tuple[str, ...]
    checks: tuple[SmoothContinuationSourceReadOperatorDependencyCheck, ...]
    source_refs: tuple[str, ...]
    source_read_ids: tuple[str, ...]
    checklist_item_ids: tuple[str, ...]
    non_claims: tuple[str, ...]
    operator_snapshot: dict[str, object]
    packet_snapshot: dict[str, object]
    packet_dependency_snapshot: dict[str, object]
    checklist_snapshot: dict[str, object]
    theorem_artifact_review_queue_snapshot: dict[str, object]
    theorem_artifact_review_queue_dependency_snapshot: dict[str, object]
    theorem_artifact_review_queue_operator_snapshot: dict[str, object]
    theorem_artifact_review_queue_operator_dependency_snapshot: dict[str, object]


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
) -> SmoothContinuationSourceReadOperatorDependencyCheck:
    return SmoothContinuationSourceReadOperatorDependencyCheck(
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
        (
            "track-a-regularity/reports/"
            "lemma_0252_smooth_continuation_source_read_packet_operator_index.md"
        ),
        (
            "track-a-regularity/reports/"
            "lemma_0252_smooth_continuation_source_read_packet_operator_index.json"
        ),
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
        "track-a-regularity/reports/lemma_0252_smooth_continuation_checklist.md",
        "track-a-regularity/reports/lemma_0252_smooth_continuation_checklist.json",
        "track-a-regularity/reports/lemma_0252_theorem_artifact_review_queue.md",
        "track-a-regularity/reports/lemma_0252_theorem_artifact_review_queue.json",
        (
            "track-a-regularity/reports/"
            "lemma_0252_theorem_artifact_review_queue_dependency.md"
        ),
        (
            "track-a-regularity/reports/"
            "lemma_0252_theorem_artifact_review_queue_dependency.json"
        ),
        (
            "track-a-regularity/reports/"
            "lemma_0252_theorem_artifact_review_queue_operator_index.md"
        ),
        (
            "track-a-regularity/reports/"
            "lemma_0252_theorem_artifact_review_queue_operator_index.json"
        ),
        (
            "track-a-regularity/reports/"
            "lemma_0252_theorem_artifact_review_queue_operator_dependency.md"
        ),
        (
            "track-a-regularity/reports/"
            "lemma_0252_theorem_artifact_review_queue_operator_dependency.json"
        ),
    )


def _queue_item_for_gap(queue: dict[str, object], gap_id: str) -> dict[str, object]:
    items = queue.get("queue_items", ())
    if not isinstance(items, list):
        raise ValueError("expected list field `queue_items`")
    for item in items:
        if isinstance(item, dict) and item.get("gap_id") == gap_id:
            return item
    raise ValueError(f"missing queue item for {gap_id}")


def _source_ids_from_packet(packet: dict[str, object]) -> tuple[str, ...]:
    return tuple(
        str(item.get("source_id"))
        for item in packet.get("source_reads", ())
        if isinstance(item, dict)
    )


def _checklist_item_ids(checklist: dict[str, object]) -> tuple[str, ...]:
    return tuple(
        str(item.get("item_id"))
        for item in checklist.get("checklist_items", ())
        if isinstance(item, dict)
    )


def build_smooth_continuation_source_read_packet_operator_dependency(
    *,
    operator_json: Path = DEFAULT_OPERATOR_JSON,
    packet_json: Path = DEFAULT_PACKET_JSON,
    packet_dependency_json: Path = DEFAULT_PACKET_DEPENDENCY_JSON,
    checklist_json: Path = DEFAULT_CHECKLIST_JSON,
    theorem_artifact_review_queue_json: Path = DEFAULT_QUEUE_JSON,
    theorem_artifact_review_queue_dependency_json: Path = DEFAULT_QUEUE_DEPENDENCY_JSON,
    theorem_artifact_review_queue_operator_json: Path = DEFAULT_QUEUE_OPERATOR_JSON,
    theorem_artifact_review_queue_operator_dependency_json: Path = (
        DEFAULT_QUEUE_OPERATOR_DEPENDENCY_JSON
    ),
    papers_blockers_index: Path = DEFAULT_PAPERS_INDEX,
) -> Lemma0252SmoothContinuationSourceReadOperatorDependency:
    operator = _load_json(operator_json)
    packet = _load_json(packet_json)
    packet_dependency = _load_json(packet_dependency_json)
    checklist = _load_json(checklist_json)
    queue = _load_json(theorem_artifact_review_queue_json)
    queue_dependency = _load_json(theorem_artifact_review_queue_dependency_json)
    queue_operator = _load_json(theorem_artifact_review_queue_operator_json)
    queue_operator_dependency = _load_json(
        theorem_artifact_review_queue_operator_dependency_json
    )
    queue_item = _queue_item_for_gap(queue, GAP_ID)

    direct_reports = _direct_source_reports()
    source_refs = tuple(
        dict.fromkeys(
            direct_reports
            + ("papers/blockers/index.md",)
            + tuple(str(item) for item in operator.get("source_refs", ()))
            + tuple(str(item) for item in packet.get("source_refs", ()))
            + tuple(str(item) for item in packet_dependency.get("source_refs", ()))
            + tuple(str(item) for item in checklist.get("source_refs", ()))
            + tuple(str(item) for item in queue.get("source_refs", ()))
            + tuple(str(item) for item in queue_dependency.get("source_refs", ()))
            + tuple(str(item) for item in queue_operator.get("source_refs", ()))
            + tuple(str(item) for item in queue_operator_dependency.get("source_refs", ()))
        )
    )
    missing_sources = _missing_sources(source_refs)

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
    packet_source = (
        "track-a-regularity/reports/lemma_0252_smooth_continuation_source_read_packet.md",
        "track-a-regularity/reports/lemma_0252_smooth_continuation_source_read_packet.json",
    )
    packet_dependency_source = (
        (
            "track-a-regularity/reports/"
            "lemma_0252_smooth_continuation_source_read_packet_dependency.md"
        ),
        (
            "track-a-regularity/reports/"
            "lemma_0252_smooth_continuation_source_read_packet_dependency.json"
        ),
    )
    checklist_source = (
        "track-a-regularity/reports/lemma_0252_smooth_continuation_checklist.md",
        "track-a-regularity/reports/lemma_0252_smooth_continuation_checklist.json",
    )
    queue_source = (
        "track-a-regularity/reports/lemma_0252_theorem_artifact_review_queue.md",
        "track-a-regularity/reports/lemma_0252_theorem_artifact_review_queue.json",
    )
    queue_dependency_source = (
        (
            "track-a-regularity/reports/"
            "lemma_0252_theorem_artifact_review_queue_dependency.md"
        ),
        (
            "track-a-regularity/reports/"
            "lemma_0252_theorem_artifact_review_queue_dependency.json"
        ),
    )
    queue_operator_source = (
        (
            "track-a-regularity/reports/"
            "lemma_0252_theorem_artifact_review_queue_operator_index.md"
        ),
        (
            "track-a-regularity/reports/"
            "lemma_0252_theorem_artifact_review_queue_operator_index.json"
        ),
    )
    queue_operator_dependency_source = (
        (
            "track-a-regularity/reports/"
            "lemma_0252_theorem_artifact_review_queue_operator_dependency.md"
        ),
        (
            "track-a-regularity/reports/"
            "lemma_0252_theorem_artifact_review_queue_operator_dependency.json"
        ),
    )

    source_read_ids = _source_ids_from_packet(packet)
    checklist_item_ids = _checklist_item_ids(checklist)
    checks = (
        _check(
            key="operator.lemma_id.matches_packet",
            expected=packet.get("lemma_id"),
            observed=operator.get("lemma_id"),
            source_artifacts=operator_source + packet_source,
        ),
        _check(
            key="operator.lemma_id.matches_packet_dependency",
            expected=packet_dependency.get("lemma_id"),
            observed=operator.get("lemma_id"),
            source_artifacts=operator_source + packet_dependency_source,
        ),
        _check(
            key="operator.candidate_status.matches_packet",
            expected=packet.get("candidate_status"),
            observed=operator.get("candidate_status"),
            source_artifacts=operator_source + packet_source,
        ),
        _check(
            key="operator.active_candidate.matches_packet",
            expected=packet.get("active_candidate"),
            observed=operator.get("active_candidate"),
            source_artifacts=operator_source + packet_source,
        ),
        _check(
            key="operator.gap_id.expected_gap_004",
            expected=GAP_ID,
            observed=operator.get("gap_id"),
            source_artifacts=operator_source,
        ),
        _check(
            key="operator.source_branch.expected_smooth_continuation_bridge",
            expected=SOURCE_BRANCH,
            observed=operator.get("source_branch"),
            source_artifacts=operator_source,
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
            key="operator.source_read_count.matches_packet",
            expected=packet.get("source_read_count"),
            observed=operator.get("source_read_count"),
            source_artifacts=operator_source + packet_source,
        ),
        _check(
            key="operator.direct_branch_source_read_count.matches_packet",
            expected=packet.get("direct_branch_source_read_count"),
            observed=operator.get("direct_branch_source_read_count"),
            source_artifacts=operator_source + packet_source,
        ),
        _check(
            key="operator.cross_cutting_source_read_count.matches_packet",
            expected=packet.get("cross_cutting_source_read_count"),
            observed=operator.get("cross_cutting_source_read_count"),
            source_artifacts=operator_source + packet_source,
        ),
        _check(
            key="operator.source_read_ids.match_packet",
            expected=source_read_ids,
            observed=tuple(operator.get("source_read_ids", ())),
            source_artifacts=operator_source + packet_source,
        ),
        _check(
            key="operator.packet_check_count.matches_packet",
            expected=packet.get("packet_check_count"),
            observed=operator.get("packet_check_count"),
            source_artifacts=operator_source + packet_source,
        ),
        _check(
            key="operator.failed_packet_check_count.matches_packet",
            expected=packet.get("failed_packet_check_count"),
            observed=operator.get("failed_packet_check_count"),
            source_artifacts=operator_source + packet_source,
        ),
        _check(
            key="operator.packet_consistent.matches_packet",
            expected=packet.get("packet_consistent"),
            observed=operator.get("packet_consistent"),
            source_artifacts=operator_source + packet_source,
        ),
        _check(
            key="operator.dependency_check_count.matches_dependency",
            expected=packet_dependency.get(
                "smooth_continuation_source_read_packet_dependency_check_count"
            ),
            observed=operator.get(
                "smooth_continuation_source_read_packet_dependency_check_count"
            ),
            source_artifacts=operator_source + packet_dependency_source,
        ),
        _check(
            key="operator.dependency_failed_checks.matches_dependency",
            expected=packet_dependency.get(
                "failed_smooth_continuation_source_read_packet_dependency_check_count"
            ),
            observed=operator.get(
                "failed_smooth_continuation_source_read_packet_dependency_check_count"
            ),
            source_artifacts=operator_source + packet_dependency_source,
        ),
        _check(
            key="operator.dependency_consistent.matches_dependency",
            expected=packet_dependency.get(
                "smooth_continuation_source_read_packet_dependency_consistent"
            ),
            observed=operator.get(
                "smooth_continuation_source_read_packet_dependency_consistent"
            ),
            source_artifacts=operator_source + packet_dependency_source,
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
            key="operator.failed_checks.remains_zero",
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
            key="checklist.branch_verdict.remains_deferred_needs_new_result",
            expected=CHECKLIST_BRANCH_VERDICT,
            observed=checklist.get("branch_verdict"),
            source_artifacts=checklist_source,
        ),
        _check(
            key="checklist.checklist_item_count.expected_seven",
            expected=7,
            observed=checklist.get("checklist_item_count"),
            source_artifacts=checklist_source,
        ),
        _check(
            key="checklist.theorem_branch_count.expected_five",
            expected=5,
            observed=checklist.get("theorem_branch_count"),
            source_artifacts=checklist_source,
        ),
        _check(
            key="checklist.dischargeable_now_count.remains_zero",
            expected=0,
            observed=checklist.get("dischargeable_now_count"),
            source_artifacts=checklist_source,
        ),
        _check(
            key="queue.gap_004.status.remains_blocked",
            expected="blocked_waiting_for_real_theorem_artifact",
            observed=queue_item.get("queue_status"),
            source_artifacts=queue_source,
        ),
        _check(
            key="queue.gap_004.source_branch.matches_operator",
            expected=operator.get("source_branch"),
            observed=queue_item.get("source_branch"),
            source_artifacts=operator_source + queue_source,
        ),
        _check(
            key="queue.gap_004.direct_theorem_artifact_present.false",
            expected=False,
            observed=queue_item.get("direct_theorem_artifact_present"),
            source_artifacts=queue_source,
        ),
        _check(
            key="queue.gap_004.actionable_now.false",
            expected=False,
            observed=queue_item.get("actionable_now"),
            source_artifacts=queue_source,
        ),
        _check(
            key="queue.gap_004.may_discharge_blocker.false",
            expected=False,
            observed=queue_item.get("may_discharge_blocker"),
            source_artifacts=queue_source,
        ),
        _check(
            key="queue.blocked_queue_item_count.expected_three",
            expected=3,
            observed=queue.get("blocked_queue_item_count"),
            source_artifacts=queue_source,
        ),
        _check(
            key="queue.actionable_queue_item_count.remains_zero",
            expected=0,
            observed=queue.get("actionable_queue_item_count"),
            source_artifacts=queue_source,
        ),
        _check(
            key="queue.may_discharge_queue_item_count.remains_zero",
            expected=0,
            observed=queue.get("may_discharge_queue_item_count"),
            source_artifacts=queue_source,
        ),
        _check(
            key="queue.direct_theorem_artifact_count.remains_zero",
            expected=0,
            observed=queue.get("direct_theorem_artifact_count"),
            source_artifacts=queue_source,
        ),
        _check(
            key="queue_dependency.consistent.true",
            expected=True,
            observed=queue_dependency.get(
                "theorem_artifact_review_queue_dependency_consistent"
            ),
            source_artifacts=queue_dependency_source,
        ),
        _check(
            key="queue_dependency.failed_checks.remain_zero",
            expected=0,
            observed=queue_dependency.get(
                "failed_theorem_artifact_review_queue_dependency_check_count"
            ),
            source_artifacts=queue_dependency_source,
        ),
        _check(
            key="queue_operator.index_consistent.true",
            expected=True,
            observed=queue_operator.get(
                "theorem_artifact_review_queue_operator_index_consistent"
            ),
            source_artifacts=queue_operator_source,
        ),
        _check(
            key="queue_operator.failed_checks.remain_zero",
            expected=0,
            observed=queue_operator.get(
                "failed_theorem_artifact_review_queue_operator_index_check_count"
            ),
            source_artifacts=queue_operator_source,
        ),
        _check(
            key="queue_operator_dependency.consistent.true",
            expected=True,
            observed=queue_operator_dependency.get(
                "theorem_artifact_review_queue_operator_dependency_consistent"
            ),
            source_artifacts=queue_operator_dependency_source,
        ),
        _check(
            key="queue_operator_dependency.failed_checks.remain_zero",
            expected=0,
            observed=queue_operator_dependency.get(
                "failed_theorem_artifact_review_queue_operator_dependency_check_count"
            ),
            source_artifacts=queue_operator_dependency_source,
        ),
        _check(
            key="all.exact_discharge_artifact_count.remains_zero",
            expected=(0, 0, 0),
            observed=(
                operator.get("exact_discharge_artifact_count"),
                packet.get("exact_discharge_artifact_count"),
                packet_dependency.get("exact_discharge_artifact_count"),
            ),
            source_artifacts=operator_source + packet_source + packet_dependency_source,
        ),
        _check(
            key="all.actionable_source_read_count.remains_zero",
            expected=(0, 0, 0),
            observed=(
                operator.get("actionable_source_read_count"),
                packet.get("actionable_source_read_count"),
                packet_dependency.get("actionable_source_read_count"),
            ),
            source_artifacts=operator_source + packet_source + packet_dependency_source,
        ),
        _check(
            key="all.may_discharge_source_read_count.remains_zero",
            expected=(0, 0, 0),
            observed=(
                operator.get("may_discharge_source_read_count"),
                packet.get("may_discharge_source_read_count"),
                packet_dependency.get("may_discharge_source_read_count"),
            ),
            source_artifacts=operator_source + packet_source + packet_dependency_source,
        ),
        _check(
            key="all.process_gate_open_authorized.false",
            expected=(False, False, False, False, False, False),
            observed=(
                operator.get("process_gate_open_authorized"),
                packet.get("process_gate_open_authorized"),
                packet_dependency.get("process_gate_open_authorized"),
                queue.get("process_gate_open_authorized"),
                queue_dependency.get("process_gate_open_authorized"),
                queue_operator_dependency.get("process_gate_open_authorized"),
            ),
            source_artifacts=operator_source
            + packet_source
            + packet_dependency_source
            + queue_source
            + queue_dependency_source
            + queue_operator_dependency_source,
        ),
        _check(
            key="all.blocker_state_changed.false",
            expected=(False, False, False, False, False, False),
            observed=(
                operator.get("blocker_state_changed"),
                packet.get("blocker_state_changed"),
                packet_dependency.get("blocker_state_changed"),
                queue.get("blocker_state_changed"),
                queue_dependency.get("blocker_state_changed"),
                queue_operator_dependency.get("blocker_state_changed"),
            ),
            source_artifacts=operator_source
            + packet_source
            + packet_dependency_source
            + queue_source
            + queue_dependency_source
            + queue_operator_dependency_source,
        ),
        _check(
            key="all.candidate_emission_authorized.false",
            expected=(False, False, False, False, False, False),
            observed=(
                operator.get("candidate_emission_authorized"),
                packet.get("candidate_emission_authorized"),
                packet_dependency.get("candidate_emission_authorized"),
                queue.get("candidate_emission_authorized"),
                queue_dependency.get("candidate_emission_authorized"),
                queue_operator_dependency.get("candidate_emission_authorized"),
            ),
            source_artifacts=operator_source
            + packet_source
            + packet_dependency_source
            + queue_source
            + queue_dependency_source
            + queue_operator_dependency_source,
        ),
        _check(
            key="source_refs.missing_count.remains_zero",
            expected=0,
            observed=len(missing_sources),
            source_artifacts=source_refs,
        ),
        _check(
            key="source_refs.include_operator_reports",
            expected=True,
            observed=all(source in source_refs for source in operator_source),
            source_artifacts=operator_source,
        ),
        _check(
            key="source_refs.include_packet_reports",
            expected=True,
            observed=all(source in source_refs for source in packet_source),
            source_artifacts=packet_source,
        ),
        _check(
            key="source_refs.include_packet_dependency_reports",
            expected=True,
            observed=all(source in source_refs for source in packet_dependency_source),
            source_artifacts=packet_dependency_source,
        ),
        _check(
            key="source_refs.include_checklist_reports",
            expected=True,
            observed=all(source in source_refs for source in checklist_source),
            source_artifacts=checklist_source,
        ),
        _check(
            key="source_refs.include_queue_operator_dependency_reports",
            expected=True,
            observed=all(source in source_refs for source in queue_operator_dependency_source),
            source_artifacts=queue_operator_dependency_source,
        ),
        _check(
            key="source_refs.include_papers_blockers_index",
            expected=True,
            observed="papers/blockers/index.md" in source_refs and papers_blockers_index.exists(),
            source_artifacts=("papers/blockers/index.md",),
        ),
        _check(
            key="source_refs.include_besov_negative_math0703883",
            expected=True,
            observed=(
                "papers/blockers/smooth_continuation_bridge/"
                "math0703883_besov_negative_blowup.pdf"
            )
            in source_refs,
            source_artifacts=source_refs,
        ),
        _check(
            key="source_refs.include_robinson_review_1410_4495",
            expected=True,
            observed=(
                "papers/blockers/smooth_continuation_bridge/"
                "1410.4495_robinson_review_NSE.pdf"
            )
            in source_refs,
            source_artifacts=source_refs,
        ),
    )
    issues = tuple(check.key for check in checks if not check.passed)
    reports = (
        operator,
        packet,
        packet_dependency,
        queue,
        queue_dependency,
        queue_operator_dependency,
    )
    process_gate_open_authorized = any(
        bool(report.get("process_gate_open_authorized")) for report in reports
    )
    blocker_state_changed = any(
        bool(report.get("blocker_state_changed")) for report in reports
    )
    candidate_emission_authorized = any(
        bool(report.get("candidate_emission_authorized")) for report in reports
    )

    return Lemma0252SmoothContinuationSourceReadOperatorDependency(
        schema_version=1,
        lemma_id=str(operator.get("lemma_id")),
        candidate_status=str(operator.get("candidate_status")),
        active_candidate=bool(operator.get("active_candidate")),
        gap_id=GAP_ID,
        source_branch=SOURCE_BRANCH,
        operator_markdown=str(DEFAULT_OPERATOR_MARKDOWN),
        operator_json=str(DEFAULT_OPERATOR_JSON),
        packet_markdown=str(DEFAULT_PACKET_MARKDOWN),
        packet_json=str(DEFAULT_PACKET_JSON),
        packet_dependency_markdown=str(DEFAULT_PACKET_DEPENDENCY_MARKDOWN),
        packet_dependency_json=str(DEFAULT_PACKET_DEPENDENCY_JSON),
        checklist_markdown=str(DEFAULT_CHECKLIST_MARKDOWN),
        checklist_json=str(DEFAULT_CHECKLIST_JSON),
        theorem_artifact_review_queue_markdown=str(DEFAULT_QUEUE_MARKDOWN),
        theorem_artifact_review_queue_json=str(DEFAULT_QUEUE_JSON),
        theorem_artifact_review_queue_dependency_markdown=str(
            DEFAULT_QUEUE_DEPENDENCY_MARKDOWN
        ),
        theorem_artifact_review_queue_dependency_json=str(DEFAULT_QUEUE_DEPENDENCY_JSON),
        theorem_artifact_review_queue_operator_markdown=str(DEFAULT_QUEUE_OPERATOR_MARKDOWN),
        theorem_artifact_review_queue_operator_json=str(DEFAULT_QUEUE_OPERATOR_JSON),
        theorem_artifact_review_queue_operator_dependency_markdown=str(
            DEFAULT_QUEUE_OPERATOR_DEPENDENCY_MARKDOWN
        ),
        theorem_artifact_review_queue_operator_dependency_json=str(
            DEFAULT_QUEUE_OPERATOR_DEPENDENCY_JSON
        ),
        papers_blockers_index=str(DEFAULT_PAPERS_INDEX),
        direct_source_report_count=len(direct_reports),
        source_ref_count=len(source_refs),
        smooth_continuation_source_read_packet_operator_dependency_check_count=len(
            checks
        ),
        passed_smooth_continuation_source_read_packet_operator_dependency_check_count=sum(
            1 for check in checks if check.passed
        ),
        failed_smooth_continuation_source_read_packet_operator_dependency_check_count=len(
            issues
        ),
        smooth_continuation_source_read_packet_operator_dependency_consistent=len(
            issues
        )
        == 0,
        operator_section_count=int(operator.get("section_count", 0)),
        operator_source_report_count=int(operator.get("source_report_count", 0)),
        operator_source_ref_count=int(operator.get("source_ref_count", 0)),
        operator_check_count=int(
            operator.get(
                "smooth_continuation_source_read_packet_operator_index_check_count", 0
            )
        ),
        failed_operator_check_count=int(
            operator.get(
                "failed_smooth_continuation_source_read_packet_operator_index_check_count",
                0,
            )
        ),
        operator_consistent=bool(
            operator.get("smooth_continuation_source_read_packet_operator_index_consistent")
        ),
        packet_status=str(packet.get("packet_status")),
        packet_branch_verdict=str(packet.get("branch_verdict")),
        packet_dependency_consistent=bool(
            packet_dependency.get(
                "smooth_continuation_source_read_packet_dependency_consistent"
            )
        ),
        packet_dependency_check_count=int(
            packet_dependency.get(
                "smooth_continuation_source_read_packet_dependency_check_count", 0
            )
        ),
        failed_packet_dependency_check_count=int(
            packet_dependency.get(
                "failed_smooth_continuation_source_read_packet_dependency_check_count",
                0,
            )
        ),
        checklist_branch_verdict=str(checklist.get("branch_verdict")),
        checklist_item_count=int(checklist.get("checklist_item_count", 0)),
        theorem_branch_count=int(checklist.get("theorem_branch_count", 0)),
        dischargeable_now_count=int(checklist.get("dischargeable_now_count", 0)),
        source_read_count=int(operator.get("source_read_count", 0)),
        direct_branch_source_read_count=int(
            operator.get("direct_branch_source_read_count", 0)
        ),
        cross_cutting_source_read_count=int(
            operator.get("cross_cutting_source_read_count", 0)
        ),
        blocked_source_read_count=int(operator.get("blocked_source_read_count", 0)),
        actionable_source_read_count=int(operator.get("actionable_source_read_count", 0)),
        may_discharge_source_read_count=int(
            operator.get("may_discharge_source_read_count", 0)
        ),
        exact_discharge_artifact_count=int(
            operator.get("exact_discharge_artifact_count", 0)
        ),
        queue_item_count=int(queue.get("queue_item_count", 0)),
        blocked_queue_item_count=int(queue.get("blocked_queue_item_count", 0)),
        actionable_queue_item_count=int(queue.get("actionable_queue_item_count", 0)),
        may_discharge_queue_item_count=int(queue.get("may_discharge_queue_item_count", 0)),
        direct_theorem_artifact_count=int(queue.get("direct_theorem_artifact_count", 0)),
        theorem_artifact_review_queue_dependency_check_count=int(
            queue_dependency.get("theorem_artifact_review_queue_dependency_check_count", 0)
        ),
        failed_theorem_artifact_review_queue_dependency_check_count=int(
            queue_dependency.get(
                "failed_theorem_artifact_review_queue_dependency_check_count", 0
            )
        ),
        theorem_artifact_review_queue_operator_index_check_count=int(
            queue_operator.get("theorem_artifact_review_queue_operator_index_check_count", 0)
        ),
        failed_theorem_artifact_review_queue_operator_index_check_count=int(
            queue_operator.get(
                "failed_theorem_artifact_review_queue_operator_index_check_count", 0
            )
        ),
        theorem_artifact_review_queue_operator_dependency_check_count=int(
            queue_operator_dependency.get(
                "theorem_artifact_review_queue_operator_dependency_check_count", 0
            )
        ),
        failed_theorem_artifact_review_queue_operator_dependency_check_count=int(
            queue_operator_dependency.get(
                "failed_theorem_artifact_review_queue_operator_dependency_check_count",
                0,
            )
        ),
        theorem_artifact_review_queue_dependency_consistent=bool(
            queue_dependency.get("theorem_artifact_review_queue_dependency_consistent")
        ),
        theorem_artifact_review_queue_operator_index_consistent=bool(
            queue_operator.get("theorem_artifact_review_queue_operator_index_consistent")
        ),
        theorem_artifact_review_queue_operator_dependency_consistent=bool(
            queue_operator_dependency.get(
                "theorem_artifact_review_queue_operator_dependency_consistent"
            )
        ),
        process_gate_open_authorized=process_gate_open_authorized,
        blocker_state_changed=blocker_state_changed,
        candidate_emission_authorized=candidate_emission_authorized,
        missing_source_count=len(missing_sources),
        missing_sources=missing_sources,
        issues=issues,
        checks=checks,
        source_refs=source_refs,
        source_read_ids=source_read_ids,
        checklist_item_ids=checklist_item_ids,
        non_claims=NON_CLAIMS,
        operator_snapshot=operator,
        packet_snapshot=packet,
        packet_dependency_snapshot=packet_dependency,
        checklist_snapshot=checklist,
        theorem_artifact_review_queue_snapshot=queue,
        theorem_artifact_review_queue_dependency_snapshot=queue_dependency,
        theorem_artifact_review_queue_operator_snapshot=queue_operator,
        theorem_artifact_review_queue_operator_dependency_snapshot=queue_operator_dependency,
    )


def render_markdown(
    report: Lemma0252SmoothContinuationSourceReadOperatorDependency,
) -> str:
    lines = [
        "# Lemma 0252 Smooth-Continuation Source Read Packet Operator Dependency",
        "",
        "## Summary",
        "",
        f"- lemma_id: `{report.lemma_id}`",
        f"- candidate_status: `{report.candidate_status}`",
        f"- active_candidate: `{str(report.active_candidate).lower()}`",
        f"- gap_id: `{report.gap_id}`",
        f"- source_branch: `{report.source_branch}`",
        f"- direct_source_report_count: `{report.direct_source_report_count}`",
        f"- source_ref_count: `{report.source_ref_count}`",
        (
            "- smooth_continuation_source_read_packet_operator_dependency_check_count: "
            f"`{report.smooth_continuation_source_read_packet_operator_dependency_check_count}`"
        ),
        (
            "- failed_smooth_continuation_source_read_packet_operator_dependency_check_count: "
            f"`{report.failed_smooth_continuation_source_read_packet_operator_dependency_check_count}`"
        ),
        (
            "- smooth_continuation_source_read_packet_operator_dependency_consistent: "
            f"`{str(report.smooth_continuation_source_read_packet_operator_dependency_consistent).lower()}`"
        ),
        f"- operator_section_count: `{report.operator_section_count}`",
        f"- operator_source_report_count: `{report.operator_source_report_count}`",
        f"- operator_source_ref_count: `{report.operator_source_ref_count}`",
        f"- operator_check_count: `{report.operator_check_count}`",
        f"- failed_operator_check_count: `{report.failed_operator_check_count}`",
        f"- operator_consistent: `{str(report.operator_consistent).lower()}`",
        f"- packet_status: `{report.packet_status}`",
        f"- packet_branch_verdict: `{report.packet_branch_verdict}`",
        f"- packet_dependency_check_count: `{report.packet_dependency_check_count}`",
        f"- failed_packet_dependency_check_count: `{report.failed_packet_dependency_check_count}`",
        f"- packet_dependency_consistent: `{str(report.packet_dependency_consistent).lower()}`",
        f"- checklist_branch_verdict: `{report.checklist_branch_verdict}`",
        f"- checklist_item_count: `{report.checklist_item_count}`",
        f"- theorem_branch_count: `{report.theorem_branch_count}`",
        f"- dischargeable_now_count: `{report.dischargeable_now_count}`",
        f"- source_read_count: `{report.source_read_count}`",
        f"- blocked_source_read_count: `{report.blocked_source_read_count}`",
        f"- actionable_source_read_count: `{report.actionable_source_read_count}`",
        f"- may_discharge_source_read_count: `{report.may_discharge_source_read_count}`",
        f"- exact_discharge_artifact_count: `{report.exact_discharge_artifact_count}`",
        f"- process_gate_open_authorized: `{str(report.process_gate_open_authorized).lower()}`",
        f"- blocker_state_changed: `{str(report.blocker_state_changed).lower()}`",
        f"- candidate_emission_authorized: `{str(report.candidate_emission_authorized).lower()}`",
        f"- missing_source_count: `{report.missing_source_count}`",
        "",
        "## Source Reads",
        "",
        *(f"- `{source_id}`" for source_id in report.source_read_ids),
        "",
        "## Checklist Items",
        "",
        *(f"- `{item_id}`" for item_id in report.checklist_item_ids),
        "",
        "## Checks",
        "",
        "| key | expected | observed | passed |",
        "|---|---|---|---:|",
    ]
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


def render_json(
    report: Lemma0252SmoothContinuationSourceReadOperatorDependency,
) -> str:
    return json.dumps(asdict(report), indent=2, sort_keys=True) + "\n"


def check_sources(
    report: Lemma0252SmoothContinuationSourceReadOperatorDependency,
) -> tuple[bool, str]:
    if report.missing_source_count:
        return False, "missing source refs: " + ", ".join(report.missing_sources)
    return True, "all smooth-continuation source-read operator dependency sources exist"


def check_consistent(
    report: Lemma0252SmoothContinuationSourceReadOperatorDependency,
) -> tuple[bool, str]:
    if not report.smooth_continuation_source_read_packet_operator_dependency_consistent:
        return (
            False,
            "inconsistent smooth-continuation source-read operator dependency: "
            + ", ".join(report.issues),
        )
    return True, "smooth-continuation source-read operator dependency is consistent"


def check_blocked(
    report: Lemma0252SmoothContinuationSourceReadOperatorDependency,
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
        or report.process_gate_open_authorized
        or report.blocker_state_changed
        or report.candidate_emission_authorized
    ):
        return False, "smooth-continuation source-read operator dependency is not blocked"
    return True, "smooth-continuation source-read operator dependency remains blocked"


def check_output(
    output: Path,
    report: Lemma0252SmoothContinuationSourceReadOperatorDependency,
    output_format: str,
) -> tuple[bool, str]:
    expected = render_json(report) if output_format == "json" else render_markdown(report)
    if not output.exists():
        return False, f"missing smooth-continuation source-read operator dependency: {output}"
    observed = output.read_text(encoding="utf-8")
    if observed != expected:
        return False, f"stale smooth-continuation source-read operator dependency: {output}"
    return True, f"fresh smooth-continuation source-read operator dependency: {output}"


def _write_output(
    *,
    output: Path,
    report: Lemma0252SmoothContinuationSourceReadOperatorDependency,
    output_format: str,
) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    text = render_json(report) if output_format == "json" else render_markdown(report)
    output.write_text(text, encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Render a read-only dependency guard for the lemma_0252 "
            "smooth-continuation source-read packet operator index."
        )
    )
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--check-output", action="store_true")
    parser.add_argument("--require-sources-exist", action="store_true")
    parser.add_argument("--require-consistent", action="store_true")
    parser.add_argument("--require-blocked", action="store_true")
    args = parser.parse_args(argv)

    report = build_smooth_continuation_source_read_packet_operator_dependency()
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

    print(f"source_read_count: {report.source_read_count}")
    print(
        "smooth_continuation_source_read_packet_operator_dependency_check_count: "
        f"{report.smooth_continuation_source_read_packet_operator_dependency_check_count}"
    )
    print(
        "failed_smooth_continuation_source_read_packet_operator_dependency_check_count: "
        f"{report.failed_smooth_continuation_source_read_packet_operator_dependency_check_count}"
    )
    print(f"exact_discharge_artifact_count: {report.exact_discharge_artifact_count}")
    print(f"candidate_emission_authorized: {str(report.candidate_emission_authorized).lower()}")

    if failures:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
