from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from lemma_0252_finite_bound_smallness_checklist import (
    DEFAULT_JSON_OUTPUT as DEFAULT_CHECKLIST_JSON,
    DEFAULT_MARKDOWN_OUTPUT as DEFAULT_CHECKLIST_MARKDOWN,
)
from lemma_0252_finite_bound_smallness_source_read_packet import (
    DEFAULT_JSON_OUTPUT as DEFAULT_PACKET_JSON,
    DEFAULT_MARKDOWN_OUTPUT as DEFAULT_PACKET_MARKDOWN,
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
    / "lemma_0252_finite_bound_smallness_source_read_packet_dependency.md"
)
DEFAULT_JSON_OUTPUT = (
    DEFAULT_REPORT_DIR
    / "lemma_0252_finite_bound_smallness_source_read_packet_dependency.json"
)
DEFAULT_PAPERS_INDEX = ROOT / "papers/blockers/index.md"

GAP_ID = "gap_002"
SOURCE_BRANCH = "finite_bound_to_smallness"
PACKET_STATUS = "blocked_source_read_only"
PACKET_BRANCH_VERDICT = "blocked_needs_new_result"
CHECKLIST_BRANCH_VERDICT = "deferred_needs_new_result"

NON_CLAIMS = (
    "read_only_finite_bound_smallness_source_read_packet_dependency_guard",
    "canonical_report_freshness_only",
    "non_promotional_gap_002_dependency_audit",
    "no_candidate_promotion",
    "no_candidate_emission",
    "no_blocker_discharge",
    "no_process_gate_opened",
    "no_file_copy",
    "no_finite_bound_to_smallness_theorem",
    "no_epsilon_regularity_theorem",
    "no_weak_to_smooth_upgrade",
    "no_navier_stokes_solution",
)


@dataclass(frozen=True)
class FiniteBoundSmallnessSourceReadPacketDependencyCheck:
    key: str
    expected: str
    observed: str
    passed: bool
    source_artifacts: tuple[str, ...]


@dataclass(frozen=True)
class Lemma0252FiniteBoundSmallnessSourceReadPacketDependency:
    schema_version: int
    lemma_id: str
    candidate_status: str
    active_candidate: bool
    gap_id: str
    source_branch: str
    packet_markdown: str
    packet_json: str
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
    finite_bound_smallness_source_read_packet_dependency_check_count: int
    passed_finite_bound_smallness_source_read_packet_dependency_check_count: int
    failed_finite_bound_smallness_source_read_packet_dependency_check_count: int
    finite_bound_smallness_source_read_packet_dependency_consistent: bool
    packet_status: str
    packet_branch_verdict: str
    checklist_branch_verdict: str
    source_read_count: int
    direct_branch_source_read_count: int
    cross_cutting_source_read_count: int
    mismatch_field_count: int
    packet_check_count: int
    failed_packet_check_count: int
    packet_consistent: bool
    checklist_item_count: int
    theorem_branch_count: int
    dischargeable_now_count: int
    smallness_only_branch_count: int
    outside_setting_caution_count: int
    queue_item_count: int
    blocked_queue_item_count: int
    actionable_queue_item_count: int
    may_discharge_queue_item_count: int
    direct_theorem_artifact_count: int
    queue_literature_source_count: int
    queue_direct_branch_source_count: int
    queue_cross_cutting_source_count: int
    theorem_artifact_review_queue_dependency_check_count: int
    failed_theorem_artifact_review_queue_dependency_check_count: int
    theorem_artifact_review_queue_operator_index_check_count: int
    failed_theorem_artifact_review_queue_operator_index_check_count: int
    theorem_artifact_review_queue_operator_dependency_check_count: int
    failed_theorem_artifact_review_queue_operator_dependency_check_count: int
    theorem_artifact_review_queue_dependency_consistent: bool
    theorem_artifact_review_queue_operator_index_consistent: bool
    theorem_artifact_review_queue_operator_dependency_consistent: bool
    exact_discharge_artifact_count: int
    actionable_source_read_count: int
    may_discharge_source_read_count: int
    process_gate_open_authorized: bool
    blocker_state_changed: bool
    candidate_emission_authorized: bool
    missing_source_count: int
    missing_sources: tuple[str, ...]
    issues: tuple[str, ...]
    checks: tuple[FiniteBoundSmallnessSourceReadPacketDependencyCheck, ...]
    source_refs: tuple[str, ...]
    non_claims: tuple[str, ...]
    source_read_ids: tuple[str, ...]
    checklist_item_ids: tuple[str, ...]
    packet_snapshot: dict[str, object]
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


def _relative(path: Path) -> str:
    return str(path.relative_to(ROOT))


def _check(
    *,
    key: str,
    expected: object,
    observed: object,
    source_artifacts: tuple[str, ...],
) -> FiniteBoundSmallnessSourceReadPacketDependencyCheck:
    return FiniteBoundSmallnessSourceReadPacketDependencyCheck(
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
        "track-a-regularity/reports/lemma_0252_finite_bound_smallness_source_read_packet.md",
        "track-a-regularity/reports/lemma_0252_finite_bound_smallness_source_read_packet.json",
        "track-a-regularity/reports/lemma_0252_finite_bound_smallness_checklist.md",
        "track-a-regularity/reports/lemma_0252_finite_bound_smallness_checklist.json",
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


def _source_paths_from_packet(packet: dict[str, object]) -> tuple[str, ...]:
    return tuple(
        str(item.get("relative_path"))
        for item in packet.get("source_reads", ())
        if isinstance(item, dict)
    )


def _checklist_item_ids(checklist: dict[str, object]) -> tuple[str, ...]:
    return tuple(
        str(item.get("item_id"))
        for item in checklist.get("checklist_items", ())
        if isinstance(item, dict)
    )


def _checklist_direct_branches(checklist: dict[str, object]) -> tuple[str, ...]:
    return tuple(
        str(branch.get("theorem_family"))
        for branch in checklist.get("theorem_branches", ())
        if isinstance(branch, dict) and bool(branch.get("applies_to_lemma_0252"))
    )


def build_finite_bound_smallness_source_read_packet_dependency(
    *,
    packet_json: Path = DEFAULT_PACKET_JSON,
    checklist_json: Path = DEFAULT_CHECKLIST_JSON,
    theorem_artifact_review_queue_json: Path = DEFAULT_QUEUE_JSON,
    theorem_artifact_review_queue_dependency_json: Path = DEFAULT_QUEUE_DEPENDENCY_JSON,
    theorem_artifact_review_queue_operator_json: Path = DEFAULT_QUEUE_OPERATOR_JSON,
    theorem_artifact_review_queue_operator_dependency_json: Path = (
        DEFAULT_QUEUE_OPERATOR_DEPENDENCY_JSON
    ),
    papers_blockers_index: Path = DEFAULT_PAPERS_INDEX,
) -> Lemma0252FiniteBoundSmallnessSourceReadPacketDependency:
    packet = _load_json(packet_json)
    checklist = _load_json(checklist_json)
    queue = _load_json(theorem_artifact_review_queue_json)
    queue_dependency = _load_json(theorem_artifact_review_queue_dependency_json)
    operator = _load_json(theorem_artifact_review_queue_operator_json)
    operator_dependency = _load_json(theorem_artifact_review_queue_operator_dependency_json)
    queue_item = _queue_item_for_gap(queue, GAP_ID)

    direct_reports = _direct_source_reports()
    source_ids = _source_ids_from_packet(packet)
    source_paths = _source_paths_from_packet(packet)
    queue_source_ids = tuple(str(item) for item in queue_item.get("source_ids", ()))
    queue_source_paths = tuple(str(item) for item in queue_item.get("source_paths", ()))
    checklist_item_ids = _checklist_item_ids(checklist)
    checklist_direct_branches = _checklist_direct_branches(checklist)

    source_refs = tuple(
        dict.fromkeys(
            direct_reports
            + ("papers/blockers/index.md",)
            + source_paths
            + tuple(str(item) for item in packet.get("source_refs", ()))
            + tuple(str(item) for item in checklist.get("source_refs", ()))
            + tuple(str(item) for item in queue.get("source_refs", ()))
            + tuple(str(item) for item in queue_dependency.get("source_refs", ()))
            + tuple(str(item) for item in operator.get("source_refs", ()))
            + tuple(str(item) for item in operator_dependency.get("source_refs", ()))
        )
    )
    missing_sources = _missing_sources(source_refs)

    packet_source = (
        "track-a-regularity/reports/lemma_0252_finite_bound_smallness_source_read_packet.md",
        "track-a-regularity/reports/lemma_0252_finite_bound_smallness_source_read_packet.json",
    )
    checklist_source = (
        "track-a-regularity/reports/lemma_0252_finite_bound_smallness_checklist.md",
        "track-a-regularity/reports/lemma_0252_finite_bound_smallness_checklist.json",
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
    operator_source = (
        (
            "track-a-regularity/reports/"
            "lemma_0252_theorem_artifact_review_queue_operator_index.md"
        ),
        (
            "track-a-regularity/reports/"
            "lemma_0252_theorem_artifact_review_queue_operator_index.json"
        ),
    )
    operator_dependency_source = (
        (
            "track-a-regularity/reports/"
            "lemma_0252_theorem_artifact_review_queue_operator_dependency.md"
        ),
        (
            "track-a-regularity/reports/"
            "lemma_0252_theorem_artifact_review_queue_operator_dependency.json"
        ),
    )

    checks = (
        _check(
            key="packet.lemma_id.matches_queue",
            expected=queue.get("lemma_id"),
            observed=packet.get("lemma_id"),
            source_artifacts=packet_source + queue_source,
        ),
        _check(
            key="packet.lemma_id.matches_checklist",
            expected=checklist.get("lemma_id"),
            observed=packet.get("lemma_id"),
            source_artifacts=packet_source + checklist_source,
        ),
        _check(
            key="packet.candidate_status.matches_queue",
            expected=queue.get("candidate_status"),
            observed=packet.get("candidate_status"),
            source_artifacts=packet_source + queue_source,
        ),
        _check(
            key="packet.active_candidate.matches_queue",
            expected=queue.get("active_candidate"),
            observed=packet.get("active_candidate"),
            source_artifacts=packet_source + queue_source,
        ),
        _check(
            key="packet.gap_id.expected_gap_002",
            expected=GAP_ID,
            observed=packet.get("gap_id"),
            source_artifacts=packet_source,
        ),
        _check(
            key="packet.source_branch.expected_finite_bound_to_smallness",
            expected=SOURCE_BRANCH,
            observed=packet.get("source_branch"),
            source_artifacts=packet_source,
        ),
        _check(
            key="checklist.source_blocker_id.expected_finite_bound_to_smallness",
            expected=SOURCE_BRANCH,
            observed=checklist.get("source_blocker_id"),
            source_artifacts=checklist_source,
        ),
        _check(
            key="queue.gap_002.source_branch.matches_packet",
            expected=packet.get("source_branch"),
            observed=queue_item.get("source_branch"),
            source_artifacts=packet_source + queue_source,
        ),
        _check(
            key="packet.packet_status.remains_blocked",
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
            key="packet.source_read_count.matches_queue_gap_002",
            expected=queue_item.get("literature_source_count"),
            observed=packet.get("source_read_count"),
            source_artifacts=packet_source + queue_source,
        ),
        _check(
            key="packet.direct_branch_source_read_count.matches_queue_gap_002",
            expected=queue_item.get("direct_branch_source_count"),
            observed=packet.get("direct_branch_source_read_count"),
            source_artifacts=packet_source + queue_source,
        ),
        _check(
            key="packet.cross_cutting_source_read_count.matches_queue_gap_002",
            expected=queue_item.get("cross_cutting_source_count"),
            observed=packet.get("cross_cutting_source_read_count"),
            source_artifacts=packet_source + queue_source,
        ),
        _check(
            key="packet.source_ids.match_queue_gap_002",
            expected=queue_source_ids,
            observed=source_ids,
            source_artifacts=packet_source + queue_source,
        ),
        _check(
            key="packet.source_paths.match_queue_gap_002",
            expected=queue_source_paths,
            observed=source_paths,
            source_artifacts=packet_source + queue_source,
        ),
        _check(
            key="packet.packet_check_count.expected_thirty_four",
            expected=34,
            observed=packet.get("packet_check_count"),
            source_artifacts=packet_source,
        ),
        _check(
            key="packet.failed_packet_check_count.remains_zero",
            expected=0,
            observed=packet.get("failed_packet_check_count"),
            source_artifacts=packet_source,
        ),
        _check(
            key="packet.packet_consistent.true",
            expected=True,
            observed=packet.get("packet_consistent"),
            source_artifacts=packet_source,
        ),
        _check(
            key="packet.exact_discharge_artifact_count.remains_zero",
            expected=0,
            observed=packet.get("exact_discharge_artifact_count"),
            source_artifacts=packet_source,
        ),
        _check(
            key="packet.actionable_source_read_count.remains_zero",
            expected=0,
            observed=packet.get("actionable_source_read_count"),
            source_artifacts=packet_source,
        ),
        _check(
            key="packet.may_discharge_source_read_count.remains_zero",
            expected=0,
            observed=packet.get("may_discharge_source_read_count"),
            source_artifacts=packet_source,
        ),
        _check(
            key="checklist.checklist_item_count.expected_seven",
            expected=7,
            observed=checklist.get("checklist_item_count"),
            source_artifacts=checklist_source,
        ),
        _check(
            key="checklist.theorem_branch_count.expected_four",
            expected=4,
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
            key="checklist.direct_theorem_branches.remain_empty",
            expected=(),
            observed=checklist_direct_branches,
            source_artifacts=checklist_source,
        ),
        _check(
            key="queue.gap_002.status.remains_blocked",
            expected="blocked_waiting_for_real_theorem_artifact",
            observed=queue_item.get("queue_status"),
            source_artifacts=queue_source,
        ),
        _check(
            key="queue.gap_002.direct_theorem_artifact_present.false",
            expected=False,
            observed=queue_item.get("direct_theorem_artifact_present"),
            source_artifacts=queue_source,
        ),
        _check(
            key="queue.gap_002.actionable_now.false",
            expected=False,
            observed=queue_item.get("actionable_now"),
            source_artifacts=queue_source,
        ),
        _check(
            key="queue.gap_002.may_discharge_blocker.false",
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
            observed=operator.get("theorem_artifact_review_queue_operator_index_consistent"),
            source_artifacts=operator_source,
        ),
        _check(
            key="queue_operator.failed_checks.remain_zero",
            expected=0,
            observed=operator.get(
                "failed_theorem_artifact_review_queue_operator_index_check_count"
            ),
            source_artifacts=operator_source,
        ),
        _check(
            key="queue_operator_dependency.consistent.true",
            expected=True,
            observed=operator_dependency.get(
                "theorem_artifact_review_queue_operator_dependency_consistent"
            ),
            source_artifacts=operator_dependency_source,
        ),
        _check(
            key="queue_operator_dependency.failed_checks.remain_zero",
            expected=0,
            observed=operator_dependency.get(
                "failed_theorem_artifact_review_queue_operator_dependency_check_count"
            ),
            source_artifacts=operator_dependency_source,
        ),
        _check(
            key="all.process_gate_open_authorized.false",
            expected=(False, False, False, False, False),
            observed=(
                packet.get("process_gate_open_authorized"),
                queue.get("process_gate_open_authorized"),
                queue_dependency.get("process_gate_open_authorized"),
                operator.get("process_gate_open_authorized"),
                operator_dependency.get("process_gate_open_authorized"),
            ),
            source_artifacts=packet_source
            + queue_source
            + queue_dependency_source
            + operator_source
            + operator_dependency_source,
        ),
        _check(
            key="all.blocker_state_changed.false",
            expected=(False, False, False, False, False),
            observed=(
                packet.get("blocker_state_changed"),
                queue.get("blocker_state_changed"),
                queue_dependency.get("blocker_state_changed"),
                operator.get("blocker_state_changed"),
                operator_dependency.get("blocker_state_changed"),
            ),
            source_artifacts=packet_source
            + queue_source
            + queue_dependency_source
            + operator_source
            + operator_dependency_source,
        ),
        _check(
            key="all.candidate_emission_authorized.false",
            expected=(False, False, False, False, False),
            observed=(
                packet.get("candidate_emission_authorized"),
                queue.get("candidate_emission_authorized"),
                queue_dependency.get("candidate_emission_authorized"),
                operator.get("candidate_emission_authorized"),
                operator_dependency.get("candidate_emission_authorized"),
            ),
            source_artifacts=packet_source
            + queue_source
            + queue_dependency_source
            + operator_source
            + operator_dependency_source,
        ),
        _check(
            key="source_refs.missing_count.remains_zero",
            expected=0,
            observed=len(missing_sources),
            source_artifacts=source_refs,
        ),
        _check(
            key="source_refs.include_packet_reports",
            expected=True,
            observed=all(source in source_refs for source in packet_source),
            source_artifacts=packet_source,
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
            observed=all(source in source_refs for source in operator_dependency_source),
            source_artifacts=operator_dependency_source,
        ),
        _check(
            key="source_refs.include_papers_blockers_index",
            expected=True,
            observed="papers/blockers/index.md" in source_refs and papers_blockers_index.exists(),
            source_artifacts=("papers/blockers/index.md",),
        ),
        _check(
            key="source_refs.include_vasseur_2007",
            expected=True,
            observed=(
                "papers/blockers/finite_bound_to_smallness/"
                "vasseur2007_partial_regularity_NS_UT.pdf"
            )
            in source_refs,
            source_artifacts=source_refs,
        ),
        _check(
            key="source_refs.include_tao_localisation",
            expected=True,
            observed=(
                "papers/blockers/cross_cutting/"
                "1108.1165_tao2013_localisation_compactness.pdf"
            )
            in source_refs,
            source_artifacts=source_refs,
        ),
    )

    issues = tuple(check.key for check in checks if not check.passed)
    process_gate_open_authorized = any(
        bool(report.get("process_gate_open_authorized"))
        for report in (packet, queue, queue_dependency, operator, operator_dependency)
    )
    blocker_state_changed = any(
        bool(report.get("blocker_state_changed"))
        for report in (packet, queue, queue_dependency, operator, operator_dependency)
    )
    candidate_emission_authorized = any(
        bool(report.get("candidate_emission_authorized"))
        for report in (packet, queue, queue_dependency, operator, operator_dependency)
    )

    return Lemma0252FiniteBoundSmallnessSourceReadPacketDependency(
        schema_version=1,
        lemma_id=str(packet.get("lemma_id")),
        candidate_status=str(packet.get("candidate_status")),
        active_candidate=bool(packet.get("active_candidate")),
        gap_id=GAP_ID,
        source_branch=SOURCE_BRANCH,
        packet_markdown=str(DEFAULT_PACKET_MARKDOWN),
        packet_json=str(DEFAULT_PACKET_JSON),
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
        finite_bound_smallness_source_read_packet_dependency_check_count=len(checks),
        passed_finite_bound_smallness_source_read_packet_dependency_check_count=sum(
            1 for check in checks if check.passed
        ),
        failed_finite_bound_smallness_source_read_packet_dependency_check_count=len(
            issues
        ),
        finite_bound_smallness_source_read_packet_dependency_consistent=len(issues) == 0,
        packet_status=str(packet.get("packet_status")),
        packet_branch_verdict=str(packet.get("branch_verdict")),
        checklist_branch_verdict=str(checklist.get("branch_verdict")),
        source_read_count=int(packet.get("source_read_count", 0)),
        direct_branch_source_read_count=int(packet.get("direct_branch_source_read_count", 0)),
        cross_cutting_source_read_count=int(packet.get("cross_cutting_source_read_count", 0)),
        mismatch_field_count=int(packet.get("mismatch_field_count", 0)),
        packet_check_count=int(packet.get("packet_check_count", 0)),
        failed_packet_check_count=int(packet.get("failed_packet_check_count", 0)),
        packet_consistent=bool(packet.get("packet_consistent")),
        checklist_item_count=int(checklist.get("checklist_item_count", 0)),
        theorem_branch_count=int(checklist.get("theorem_branch_count", 0)),
        dischargeable_now_count=int(checklist.get("dischargeable_now_count", 0)),
        smallness_only_branch_count=int(checklist.get("smallness_only_branch_count", 0)),
        outside_setting_caution_count=int(
            checklist.get("outside_setting_caution_count", 0)
        ),
        queue_item_count=int(queue.get("queue_item_count", 0)),
        blocked_queue_item_count=int(queue.get("blocked_queue_item_count", 0)),
        actionable_queue_item_count=int(queue.get("actionable_queue_item_count", 0)),
        may_discharge_queue_item_count=int(queue.get("may_discharge_queue_item_count", 0)),
        direct_theorem_artifact_count=int(queue.get("direct_theorem_artifact_count", 0)),
        queue_literature_source_count=int(queue_item.get("literature_source_count", 0)),
        queue_direct_branch_source_count=int(queue_item.get("direct_branch_source_count", 0)),
        queue_cross_cutting_source_count=int(queue_item.get("cross_cutting_source_count", 0)),
        theorem_artifact_review_queue_dependency_check_count=int(
            queue_dependency.get("theorem_artifact_review_queue_dependency_check_count", 0)
        ),
        failed_theorem_artifact_review_queue_dependency_check_count=int(
            queue_dependency.get(
                "failed_theorem_artifact_review_queue_dependency_check_count",
                0,
            )
        ),
        theorem_artifact_review_queue_operator_index_check_count=int(
            operator.get("theorem_artifact_review_queue_operator_index_check_count", 0)
        ),
        failed_theorem_artifact_review_queue_operator_index_check_count=int(
            operator.get(
                "failed_theorem_artifact_review_queue_operator_index_check_count",
                0,
            )
        ),
        theorem_artifact_review_queue_operator_dependency_check_count=int(
            operator_dependency.get(
                "theorem_artifact_review_queue_operator_dependency_check_count",
                0,
            )
        ),
        failed_theorem_artifact_review_queue_operator_dependency_check_count=int(
            operator_dependency.get(
                "failed_theorem_artifact_review_queue_operator_dependency_check_count",
                0,
            )
        ),
        theorem_artifact_review_queue_dependency_consistent=bool(
            queue_dependency.get("theorem_artifact_review_queue_dependency_consistent")
        ),
        theorem_artifact_review_queue_operator_index_consistent=bool(
            operator.get("theorem_artifact_review_queue_operator_index_consistent")
        ),
        theorem_artifact_review_queue_operator_dependency_consistent=bool(
            operator_dependency.get(
                "theorem_artifact_review_queue_operator_dependency_consistent"
            )
        ),
        exact_discharge_artifact_count=int(packet.get("exact_discharge_artifact_count", 0)),
        actionable_source_read_count=int(packet.get("actionable_source_read_count", 0)),
        may_discharge_source_read_count=int(packet.get("may_discharge_source_read_count", 0)),
        process_gate_open_authorized=process_gate_open_authorized,
        blocker_state_changed=blocker_state_changed,
        candidate_emission_authorized=candidate_emission_authorized,
        missing_source_count=len(missing_sources),
        missing_sources=missing_sources,
        issues=issues,
        checks=checks,
        source_refs=source_refs,
        non_claims=NON_CLAIMS,
        source_read_ids=source_ids,
        checklist_item_ids=checklist_item_ids,
        packet_snapshot=packet,
        checklist_snapshot=checklist,
        theorem_artifact_review_queue_snapshot=queue,
        theorem_artifact_review_queue_dependency_snapshot=queue_dependency,
        theorem_artifact_review_queue_operator_snapshot=operator,
        theorem_artifact_review_queue_operator_dependency_snapshot=operator_dependency,
    )


def render_markdown(
    report: Lemma0252FiniteBoundSmallnessSourceReadPacketDependency,
) -> str:
    lines = [
        "# Lemma 0252 Finite Bound Smallness Source Read Packet Dependency",
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
            "- finite_bound_smallness_source_read_packet_dependency_check_count: "
            f"`{report.finite_bound_smallness_source_read_packet_dependency_check_count}`"
        ),
        (
            "- failed_finite_bound_smallness_source_read_packet_dependency_check_count: "
            f"`{report.failed_finite_bound_smallness_source_read_packet_dependency_check_count}`"
        ),
        (
            "- finite_bound_smallness_source_read_packet_dependency_consistent: "
            f"`{str(report.finite_bound_smallness_source_read_packet_dependency_consistent).lower()}`"
        ),
        f"- packet_status: `{report.packet_status}`",
        f"- packet_branch_verdict: `{report.packet_branch_verdict}`",
        f"- checklist_branch_verdict: `{report.checklist_branch_verdict}`",
        f"- source_read_count: `{report.source_read_count}`",
        f"- checklist_item_count: `{report.checklist_item_count}`",
        f"- theorem_branch_count: `{report.theorem_branch_count}`",
        f"- dischargeable_now_count: `{report.dischargeable_now_count}`",
        f"- exact_discharge_artifact_count: `{report.exact_discharge_artifact_count}`",
        f"- actionable_source_read_count: `{report.actionable_source_read_count}`",
        f"- may_discharge_source_read_count: `{report.may_discharge_source_read_count}`",
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
    report: Lemma0252FiniteBoundSmallnessSourceReadPacketDependency,
) -> str:
    return json.dumps(asdict(report), indent=2, sort_keys=True) + "\n"


def check_sources(
    report: Lemma0252FiniteBoundSmallnessSourceReadPacketDependency,
) -> tuple[bool, str]:
    if report.missing_source_count:
        return False, "missing source refs: " + ", ".join(report.missing_sources)
    return True, "all finite-bound-to-smallness source-read dependency sources exist"


def check_consistent(
    report: Lemma0252FiniteBoundSmallnessSourceReadPacketDependency,
) -> tuple[bool, str]:
    if not report.finite_bound_smallness_source_read_packet_dependency_consistent:
        return (
            False,
            "inconsistent finite-bound-to-smallness source-read packet dependency: "
            + ", ".join(report.issues),
        )
    return True, "finite-bound-to-smallness source-read packet dependency is consistent"


def check_blocked(
    report: Lemma0252FiniteBoundSmallnessSourceReadPacketDependency,
) -> tuple[bool, str]:
    if (
        report.packet_status != PACKET_STATUS
        or report.packet_branch_verdict != PACKET_BRANCH_VERDICT
        or report.checklist_branch_verdict != CHECKLIST_BRANCH_VERDICT
        or report.dischargeable_now_count != 0
        or report.exact_discharge_artifact_count != 0
        or report.actionable_source_read_count != 0
        or report.may_discharge_source_read_count != 0
        or report.process_gate_open_authorized
        or report.blocker_state_changed
        or report.candidate_emission_authorized
    ):
        return False, "finite-bound-to-smallness source-read packet dependency is not blocked"
    return True, "finite-bound-to-smallness source-read packet dependency remains blocked"


def check_output(
    output: Path,
    report: Lemma0252FiniteBoundSmallnessSourceReadPacketDependency,
    output_format: str,
) -> tuple[bool, str]:
    expected = render_json(report) if output_format == "json" else render_markdown(report)
    if not output.exists():
        return False, f"missing finite-bound-to-smallness source-read dependency output: {output}"
    observed = output.read_text(encoding="utf-8")
    if observed != expected:
        return False, f"stale finite-bound-to-smallness source-read dependency output: {output}"
    return True, f"fresh finite-bound-to-smallness source-read dependency output: {output}"


def _write_output(
    *,
    output: Path,
    report: Lemma0252FiniteBoundSmallnessSourceReadPacketDependency,
    output_format: str,
) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    text = render_json(report) if output_format == "json" else render_markdown(report)
    output.write_text(text, encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Render a read-only dependency guard for the lemma_0252 finite-bound-to-smallness "
            "source-read packet."
        )
    )
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--check-output", action="store_true")
    parser.add_argument("--require-sources-exist", action="store_true")
    parser.add_argument("--require-consistent", action="store_true")
    parser.add_argument("--require-blocked", action="store_true")
    args = parser.parse_args(argv)

    report = build_finite_bound_smallness_source_read_packet_dependency()
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
        "finite_bound_smallness_source_read_packet_dependency_check_count: "
        f"{report.finite_bound_smallness_source_read_packet_dependency_check_count}"
    )
    print(
        "failed_finite_bound_smallness_source_read_packet_dependency_check_count: "
        f"{report.failed_finite_bound_smallness_source_read_packet_dependency_check_count}"
    )
    print(f"exact_discharge_artifact_count: {report.exact_discharge_artifact_count}")
    print(f"candidate_emission_authorized: {str(report.candidate_emission_authorized).lower()}")

    if failures:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
