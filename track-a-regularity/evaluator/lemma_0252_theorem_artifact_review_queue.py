from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from lemma_0252_blocker_literature_gap_matrix import (
    DEFAULT_JSON_OUTPUT as DEFAULT_GAP_MATRIX_JSON,
    DEFAULT_MARKDOWN_OUTPUT as DEFAULT_GAP_MATRIX_MARKDOWN,
)
from lemma_0252_blocker_literature_gap_operator_dependency import (
    DEFAULT_JSON_OUTPUT as DEFAULT_GAP_OPERATOR_DEPENDENCY_JSON,
    DEFAULT_MARKDOWN_OUTPUT as DEFAULT_GAP_OPERATOR_DEPENDENCY_MARKDOWN,
)
from lemma_0252_blocker_literature_gap_operator_index import (
    DEFAULT_JSON_OUTPUT as DEFAULT_GAP_OPERATOR_JSON,
    DEFAULT_MARKDOWN_OUTPUT as DEFAULT_GAP_OPERATOR_MARKDOWN,
)
from promotion_gate_analytic_discharge_gap_index import (
    DEFAULT_JSON_OUTPUT as DEFAULT_ANALYTIC_GAP_JSON,
    DEFAULT_MARKDOWN_OUTPUT as DEFAULT_ANALYTIC_GAP_MARKDOWN,
)


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REPORT_DIR = ROOT / "track-a-regularity/reports"
DEFAULT_MARKDOWN_OUTPUT = DEFAULT_REPORT_DIR / "lemma_0252_theorem_artifact_review_queue.md"
DEFAULT_JSON_OUTPUT = DEFAULT_REPORT_DIR / "lemma_0252_theorem_artifact_review_queue.json"

DIRECT_ANALYTIC_GAP_IDS = ("gap_002", "gap_003", "gap_004")
QUEUE_STATUS = "blocked_waiting_for_real_theorem_artifact"
REVIEW_PHASE = "non_promotional_theorem_artifact_review"
ACTIONABILITY_REASON = (
    "A local paper or checklist only becomes actionable after it is converted into a reviewed "
    "theorem statement or formal sidecar matching the exact lemma_0252 setting."
)

NON_CLAIMS = (
    "read_only_theorem_artifact_review_queue",
    "non_promotional_gap_review_only",
    "no_candidate_promotion",
    "no_candidate_emission",
    "no_blocker_discharge",
    "no_process_gate_opened",
    "no_file_copy",
    "no_epsilon_regularity_theorem",
    "no_compactness_or_liouville_theorem",
    "no_bkm_or_serrin_or_high_sobolev_bound",
    "no_weak_to_smooth_upgrade",
    "no_navier_stokes_solution",
)


@dataclass(frozen=True)
class TheoremArtifactReviewSource:
    source_id: str
    title: str
    blocker_family: str
    relative_path: str
    source_type: str
    priority: str
    verdict_hint: str
    support_kind: str
    direct_branch_support: bool
    source_exists: bool
    direct_discharge: bool
    actionable_now: bool
    may_discharge_gap: bool


@dataclass(frozen=True)
class TheoremArtifactReviewQueueItem:
    queue_id: str
    gap_id: str
    attack_rank: int
    source_branch: str
    family: str
    required_artifact_type: str
    missing_artifact: str
    required_review_evidence: tuple[str, ...]
    minimum_acceptance_checks: tuple[str, ...]
    queue_status: str
    review_phase: str
    actionability_reason: str
    literature_source_count: int
    direct_branch_source_count: int
    cross_cutting_source_count: int
    source_ids: tuple[str, ...]
    source_paths: tuple[str, ...]
    review_sources: tuple[TheoremArtifactReviewSource, ...]
    actionable_now: bool
    may_discharge_blocker: bool
    direct_theorem_artifact_present: bool
    process_gate_open_authorized: bool
    blocker_state_changed: bool
    candidate_emission_authorized: bool


@dataclass(frozen=True)
class TheoremArtifactReviewQueueCheck:
    key: str
    expected: str
    observed: str
    passed: bool
    source_artifacts: tuple[str, ...]


@dataclass(frozen=True)
class Lemma0252TheoremArtifactReviewQueue:
    schema_version: int
    lemma_id: str
    candidate_status: str
    active_candidate: bool
    analytic_gap_markdown: str
    analytic_gap_json: str
    literature_gap_matrix_markdown: str
    literature_gap_matrix_json: str
    literature_gap_operator_markdown: str
    literature_gap_operator_json: str
    literature_gap_operator_dependency_markdown: str
    literature_gap_operator_dependency_json: str
    queue_item_count: int
    direct_analytic_gap_count: int
    blocked_queue_item_count: int
    actionable_queue_item_count: int
    may_discharge_queue_item_count: int
    direct_theorem_artifact_count: int
    queue_source_edge_count: int
    direct_branch_source_edge_count: int
    cross_cutting_source_edge_count: int
    unique_literature_source_count: int
    source_ref_count: int
    literature_source_count: int
    gap_count: int
    source_gap_edge_count: int
    blocked_gap_count: int
    actionable_gap_count: int
    may_discharge_gap_count: int
    direct_discharge_source_count: int
    literature_gap_operator_dependency_check_count: int
    failed_literature_gap_operator_dependency_check_count: int
    literature_gap_operator_dependency_consistent: bool
    analytic_gap_stack_consistent: bool
    operator_stack_consistent: bool
    process_gate_open_authorized: bool
    blocker_state_changed: bool
    candidate_emission_authorized: bool
    missing_source_count: int
    missing_sources: tuple[str, ...]
    issues: tuple[str, ...]
    queue_items: tuple[TheoremArtifactReviewQueueItem, ...]
    checks: tuple[TheoremArtifactReviewQueueCheck, ...]
    source_refs: tuple[str, ...]
    non_claims: tuple[str, ...]
    analytic_gap_snapshot: dict[str, object]
    literature_gap_matrix_snapshot: dict[str, object]
    literature_gap_operator_snapshot: dict[str, object]
    literature_gap_operator_dependency_snapshot: dict[str, object]


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
) -> TheoremArtifactReviewQueueCheck:
    return TheoremArtifactReviewQueueCheck(
        key=key,
        expected=str(expected),
        observed=str(observed),
        passed=expected == observed,
        source_artifacts=source_artifacts,
    )


def _missing_sources(source_refs: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(source for source in source_refs if not (ROOT / source).exists())


def _direct_sources() -> tuple[str, ...]:
    return (
        "track-a-regularity/reports/promotion_gate_analytic_discharge_gap_index.md",
        "track-a-regularity/reports/promotion_gate_analytic_discharge_gap_index.json",
        "track-a-regularity/reports/lemma_0252_blocker_literature_gap_matrix.md",
        "track-a-regularity/reports/lemma_0252_blocker_literature_gap_matrix.json",
        "track-a-regularity/reports/lemma_0252_blocker_literature_gap_operator_index.md",
        "track-a-regularity/reports/lemma_0252_blocker_literature_gap_operator_index.json",
        (
            "track-a-regularity/reports/"
            "lemma_0252_blocker_literature_gap_operator_dependency.md"
        ),
        (
            "track-a-regularity/reports/"
            "lemma_0252_blocker_literature_gap_operator_dependency.json"
        ),
        "papers/blockers/index.md",
    )


def _rows_by_key(
    rows: object,
    key_name: str,
) -> dict[str, dict[str, object]]:
    if not isinstance(rows, list):
        raise ValueError(f"expected list rows for `{key_name}`")
    result: dict[str, dict[str, object]] = {}
    for row in rows:
        if isinstance(row, dict):
            result[str(row.get(key_name))] = row
    return result


def _source_rows_by_id(matrix: dict[str, object]) -> dict[str, dict[str, object]]:
    return _rows_by_key(matrix.get("source_summaries", ()), "source_id")


def _gap_rows_by_id(gap_index: dict[str, object]) -> dict[str, dict[str, object]]:
    return _rows_by_key(gap_index.get("gaps", ()), "gap_id")


def _coverage_rows_by_id(matrix: dict[str, object]) -> dict[str, dict[str, object]]:
    return _rows_by_key(matrix.get("gap_coverages", ()), "gap_id")


def _edge_rows(matrix: dict[str, object], gap_id: str) -> tuple[dict[str, object], ...]:
    edges = matrix.get("edges", ())
    if not isinstance(edges, list):
        raise ValueError("expected list field `edges` in literature gap matrix")
    return tuple(
        edge
        for edge in edges
        if isinstance(edge, dict) and str(edge.get("gap_id")) == gap_id
    )


def _review_sources_for_gap(
    *,
    matrix: dict[str, object],
    gap_id: str,
) -> tuple[TheoremArtifactReviewSource, ...]:
    sources_by_id = _source_rows_by_id(matrix)
    review_sources: list[TheoremArtifactReviewSource] = []
    for edge in _edge_rows(matrix, gap_id):
        source_id = str(edge.get("source_id"))
        source = sources_by_id[source_id]
        relative_path = str(source.get("relative_path"))
        source_exists = bool(source.get("source_exists")) and (ROOT / relative_path).exists()
        review_sources.append(
            TheoremArtifactReviewSource(
                source_id=source_id,
                title=str(source.get("title")),
                blocker_family=str(source.get("blocker_family")),
                relative_path=relative_path,
                source_type=str(source.get("source_type")),
                priority=str(source.get("priority")),
                verdict_hint=str(source.get("verdict_hint")),
                support_kind=str(edge.get("support_kind")),
                direct_branch_support=bool(edge.get("direct_branch_support")),
                source_exists=source_exists,
                direct_discharge=bool(source.get("direct_discharge")),
                actionable_now=False,
                may_discharge_gap=False,
            )
        )
    return tuple(review_sources)


def _queue_item(
    *,
    gap: dict[str, object],
    coverage: dict[str, object],
    review_sources: tuple[TheoremArtifactReviewSource, ...],
) -> TheoremArtifactReviewQueueItem:
    source_ids = tuple(source.source_id for source in review_sources)
    source_paths = tuple(source.relative_path for source in review_sources)
    direct_branch_source_count = sum(1 for source in review_sources if source.direct_branch_support)
    return TheoremArtifactReviewQueueItem(
        queue_id=f"review_{gap['gap_id']}",
        gap_id=str(gap.get("gap_id")),
        attack_rank=int(coverage.get("attack_rank", 0)),
        source_branch=str(gap.get("source_branch")),
        family=str(gap.get("family")),
        required_artifact_type=str(gap.get("required_artifact_type")),
        missing_artifact=str(gap.get("missing_artifact")),
        required_review_evidence=tuple(str(item) for item in gap.get("required_review_evidence", ())),
        minimum_acceptance_checks=tuple(
            str(item) for item in gap.get("minimum_acceptance_checks", ())
        ),
        queue_status=QUEUE_STATUS,
        review_phase=REVIEW_PHASE,
        actionability_reason=ACTIONABILITY_REASON,
        literature_source_count=len(review_sources),
        direct_branch_source_count=direct_branch_source_count,
        cross_cutting_source_count=len(review_sources) - direct_branch_source_count,
        source_ids=source_ids,
        source_paths=source_paths,
        review_sources=review_sources,
        actionable_now=False,
        may_discharge_blocker=False,
        direct_theorem_artifact_present=False,
        process_gate_open_authorized=False,
        blocker_state_changed=False,
        candidate_emission_authorized=False,
    )


def build_theorem_artifact_review_queue(
    *,
    analytic_gap_json: Path = DEFAULT_ANALYTIC_GAP_JSON,
    literature_gap_matrix_json: Path = DEFAULT_GAP_MATRIX_JSON,
    literature_gap_operator_json: Path = DEFAULT_GAP_OPERATOR_JSON,
    literature_gap_operator_dependency_json: Path = DEFAULT_GAP_OPERATOR_DEPENDENCY_JSON,
) -> Lemma0252TheoremArtifactReviewQueue:
    analytic_gap = _load_json(analytic_gap_json)
    matrix = _load_json(literature_gap_matrix_json)
    operator = _load_json(literature_gap_operator_json)
    operator_dependency = _load_json(literature_gap_operator_dependency_json)

    gaps_by_id = _gap_rows_by_id(analytic_gap)
    coverages_by_id = _coverage_rows_by_id(matrix)

    queue_items = tuple(
        _queue_item(
            gap=gaps_by_id[gap_id],
            coverage=coverages_by_id[gap_id],
            review_sources=_review_sources_for_gap(matrix=matrix, gap_id=gap_id),
        )
        for gap_id in DIRECT_ANALYTIC_GAP_IDS
    )

    queue_source_edge_count = sum(item.literature_source_count for item in queue_items)
    direct_branch_source_edge_count = sum(
        item.direct_branch_source_count for item in queue_items
    )
    cross_cutting_source_edge_count = sum(
        item.cross_cutting_source_count for item in queue_items
    )
    unique_literature_source_ids = tuple(
        dict.fromkeys(source.source_id for item in queue_items for source in item.review_sources)
    )
    item_source_paths = tuple(
        dict.fromkeys(path for item in queue_items for path in item.source_paths)
    )

    source_refs = tuple(
        dict.fromkeys(
            _direct_sources()
            + item_source_paths
            + tuple(str(item) for item in analytic_gap.get("source_refs", ()))
            + tuple(str(item) for item in matrix.get("source_refs", ()))
            + tuple(str(item) for item in operator.get("source_refs", ()))
            + tuple(str(item) for item in operator_dependency.get("source_refs", ()))
        )
    )
    missing_sources = _missing_sources(source_refs)

    direct_sources = _direct_sources()
    analytic_source = direct_sources[:2]
    matrix_source = direct_sources[2:4]
    operator_source = direct_sources[4:6]
    operator_dependency_source = direct_sources[6:8]
    expected_source_branch_by_gap = {
        "gap_002": "finite_bound_to_smallness",
        "gap_003": "compactness_liouville",
        "gap_004": "smooth_continuation_bridge",
    }
    expected_artifact_type_by_gap = {
        "gap_002": "finite_bound_to_smallness_discharge_bundle",
        "gap_003": "compactness_liouville_discharge_bundle",
        "gap_004": "smooth_continuation_discharge_bundle",
    }

    checks: list[TheoremArtifactReviewQueueCheck] = [
        _check(
            key="operator_dependency.consistent.true",
            expected=True,
            observed=operator_dependency.get("literature_gap_operator_dependency_consistent"),
            source_artifacts=operator_dependency_source,
        ),
        _check(
            key="operator_dependency.failed_checks.remain_zero",
            expected=0,
            observed=operator_dependency.get(
                "failed_literature_gap_operator_dependency_check_count"
            ),
            source_artifacts=operator_dependency_source,
        ),
        _check(
            key="matrix.gap_stack_consistent.true",
            expected=True,
            observed=matrix.get("gap_stack_consistent"),
            source_artifacts=matrix_source,
        ),
        _check(
            key="operator.operator_stack_consistent.true",
            expected=True,
            observed=operator.get("operator_stack_consistent"),
            source_artifacts=operator_source,
        ),
        _check(
            key="direct_gap_ids.present_in_gap_index",
            expected=DIRECT_ANALYTIC_GAP_IDS,
            observed=tuple(gap_id for gap_id in DIRECT_ANALYTIC_GAP_IDS if gap_id in gaps_by_id),
            source_artifacts=analytic_source,
        ),
        _check(
            key="direct_gap_ids.present_in_literature_matrix",
            expected=DIRECT_ANALYTIC_GAP_IDS,
            observed=tuple(
                gap_id for gap_id in DIRECT_ANALYTIC_GAP_IDS if gap_id in coverages_by_id
            ),
            source_artifacts=matrix_source,
        ),
        _check(
            key="queue_item_count.expected_three",
            expected=3,
            observed=len(queue_items),
            source_artifacts=analytic_source + matrix_source,
        ),
        _check(
            key="queue_gap_ids.expected_direct_analytic_gaps",
            expected=DIRECT_ANALYTIC_GAP_IDS,
            observed=tuple(item.gap_id for item in queue_items),
            source_artifacts=analytic_source + matrix_source,
        ),
        _check(
            key="all_queue_items.blocked",
            expected=len(queue_items),
            observed=sum(1 for item in queue_items if item.queue_status == QUEUE_STATUS),
            source_artifacts=direct_sources,
        ),
        _check(
            key="actionable_queue_item_count.remains_zero",
            expected=0,
            observed=sum(1 for item in queue_items if item.actionable_now),
            source_artifacts=direct_sources,
        ),
        _check(
            key="may_discharge_queue_item_count.remains_zero",
            expected=0,
            observed=sum(1 for item in queue_items if item.may_discharge_blocker),
            source_artifacts=direct_sources,
        ),
        _check(
            key="direct_theorem_artifact_count.remains_zero",
            expected=0,
            observed=sum(1 for item in queue_items if item.direct_theorem_artifact_present),
            source_artifacts=direct_sources,
        ),
        _check(
            key="source_refs.missing_count.remains_zero",
            expected=0,
            observed=len(missing_sources),
            source_artifacts=source_refs,
        ),
        _check(
            key="literature_source_count.matches_operator_dependency",
            expected=operator_dependency.get("literature_source_count"),
            observed=operator.get("literature_source_count"),
            source_artifacts=operator_source + operator_dependency_source,
        ),
        _check(
            key="source_gap_edge_count.matches_operator_dependency",
            expected=operator_dependency.get("source_gap_edge_count"),
            observed=matrix.get("source_gap_edge_count"),
            source_artifacts=matrix_source + operator_dependency_source,
        ),
        _check(
            key="blocked_gap_count.matches_operator_dependency",
            expected=operator_dependency.get("blocked_gap_count"),
            observed=analytic_gap.get("blocked_gap_count"),
            source_artifacts=analytic_source + operator_dependency_source,
        ),
        _check(
            key="actionable_gap_count.remains_zero",
            expected=0,
            observed=analytic_gap.get("actionable_gap_count"),
            source_artifacts=analytic_source,
        ),
        _check(
            key="may_discharge_gap_count.remains_zero",
            expected=0,
            observed=analytic_gap.get("may_discharge_gap_count"),
            source_artifacts=analytic_source,
        ),
        _check(
            key="direct_discharge_source_count.remains_zero",
            expected=0,
            observed=matrix.get("direct_discharge_source_count"),
            source_artifacts=matrix_source,
        ),
        _check(
            key="all.process_gate_open_authorized.false",
            expected=(False, False, False, False),
            observed=(
                analytic_gap.get("process_gate_open_authorized"),
                matrix.get("process_gate_open_authorized"),
                operator.get("process_gate_open_authorized"),
                operator_dependency.get("process_gate_open_authorized"),
            ),
            source_artifacts=direct_sources,
        ),
        _check(
            key="all.blocker_state_changed.false",
            expected=(False, False, False, False),
            observed=(
                analytic_gap.get("blocker_state_changed"),
                matrix.get("blocker_state_changed"),
                operator.get("blocker_state_changed"),
                operator_dependency.get("blocker_state_changed"),
            ),
            source_artifacts=direct_sources,
        ),
        _check(
            key="all.candidate_emission_authorized.false",
            expected=(False, False, False, False),
            observed=(
                analytic_gap.get("candidate_emission_authorized"),
                matrix.get("candidate_emission_authorized"),
                operator.get("candidate_emission_authorized"),
                operator_dependency.get("candidate_emission_authorized"),
            ),
            source_artifacts=direct_sources,
        ),
        _check(
            key="candidate_status.remains_needs_review",
            expected="needs_review",
            observed=analytic_gap.get("candidate_status"),
            source_artifacts=analytic_source,
        ),
        _check(
            key="active_candidate.remains_false",
            expected=False,
            observed=analytic_gap.get("active_candidate"),
            source_artifacts=analytic_source,
        ),
    ]

    for item in queue_items:
        checks.extend(
            [
                _check(
                    key=f"{item.gap_id}.source_branch.expected",
                    expected=expected_source_branch_by_gap[item.gap_id],
                    observed=item.source_branch,
                    source_artifacts=analytic_source + matrix_source,
                ),
                _check(
                    key=f"{item.gap_id}.artifact_type.expected",
                    expected=expected_artifact_type_by_gap[item.gap_id],
                    observed=item.required_artifact_type,
                    source_artifacts=analytic_source + matrix_source,
                ),
                _check(
                    key=f"{item.gap_id}.source_count.matches_matrix_coverage",
                    expected=coverages_by_id[item.gap_id].get("literature_source_count"),
                    observed=item.literature_source_count,
                    source_artifacts=matrix_source,
                ),
                _check(
                    key=f"{item.gap_id}.direct_branch_source_count.matches_matrix_coverage",
                    expected=coverages_by_id[item.gap_id].get("direct_branch_source_count"),
                    observed=item.direct_branch_source_count,
                    source_artifacts=matrix_source,
                ),
                _check(
                    key=f"{item.gap_id}.review_sources_exist",
                    expected=item.literature_source_count,
                    observed=sum(1 for source in item.review_sources if source.source_exists),
                    source_artifacts=tuple(item.source_paths),
                ),
                _check(
                    key=f"{item.gap_id}.review_sources_not_direct_discharge",
                    expected=0,
                    observed=sum(1 for source in item.review_sources if source.direct_discharge),
                    source_artifacts=tuple(item.source_paths),
                ),
            ]
        )

    issues = tuple(check.key for check in checks if not check.passed)

    process_gate_open_authorized = any(
        bool(report.get("process_gate_open_authorized"))
        for report in (analytic_gap, matrix, operator, operator_dependency)
    )
    blocker_state_changed = any(
        bool(report.get("blocker_state_changed"))
        for report in (analytic_gap, matrix, operator, operator_dependency)
    )
    candidate_emission_authorized = any(
        bool(report.get("candidate_emission_authorized"))
        for report in (analytic_gap, matrix, operator, operator_dependency)
    )

    return Lemma0252TheoremArtifactReviewQueue(
        schema_version=1,
        lemma_id=str(analytic_gap.get("lemma_id")),
        candidate_status=str(analytic_gap.get("candidate_status")),
        active_candidate=bool(analytic_gap.get("active_candidate")),
        analytic_gap_markdown=str(DEFAULT_ANALYTIC_GAP_MARKDOWN),
        analytic_gap_json=str(DEFAULT_ANALYTIC_GAP_JSON),
        literature_gap_matrix_markdown=str(DEFAULT_GAP_MATRIX_MARKDOWN),
        literature_gap_matrix_json=str(DEFAULT_GAP_MATRIX_JSON),
        literature_gap_operator_markdown=str(DEFAULT_GAP_OPERATOR_MARKDOWN),
        literature_gap_operator_json=str(DEFAULT_GAP_OPERATOR_JSON),
        literature_gap_operator_dependency_markdown=str(DEFAULT_GAP_OPERATOR_DEPENDENCY_MARKDOWN),
        literature_gap_operator_dependency_json=str(DEFAULT_GAP_OPERATOR_DEPENDENCY_JSON),
        queue_item_count=len(queue_items),
        direct_analytic_gap_count=len(DIRECT_ANALYTIC_GAP_IDS),
        blocked_queue_item_count=sum(
            1 for item in queue_items if item.queue_status == QUEUE_STATUS
        ),
        actionable_queue_item_count=sum(1 for item in queue_items if item.actionable_now),
        may_discharge_queue_item_count=sum(
            1 for item in queue_items if item.may_discharge_blocker
        ),
        direct_theorem_artifact_count=sum(
            1 for item in queue_items if item.direct_theorem_artifact_present
        ),
        queue_source_edge_count=queue_source_edge_count,
        direct_branch_source_edge_count=direct_branch_source_edge_count,
        cross_cutting_source_edge_count=cross_cutting_source_edge_count,
        unique_literature_source_count=len(unique_literature_source_ids),
        source_ref_count=len(source_refs),
        literature_source_count=int(operator_dependency.get("literature_source_count", 0)),
        gap_count=int(operator_dependency.get("gap_count", 0)),
        source_gap_edge_count=int(operator_dependency.get("source_gap_edge_count", 0)),
        blocked_gap_count=int(operator_dependency.get("blocked_gap_count", 0)),
        actionable_gap_count=int(operator_dependency.get("actionable_gap_count", 0)),
        may_discharge_gap_count=int(operator_dependency.get("may_discharge_gap_count", 0)),
        direct_discharge_source_count=int(
            operator_dependency.get("direct_discharge_source_count", 0)
        ),
        literature_gap_operator_dependency_check_count=int(
            operator_dependency.get("literature_gap_operator_dependency_check_count", 0)
        ),
        failed_literature_gap_operator_dependency_check_count=int(
            operator_dependency.get(
                "failed_literature_gap_operator_dependency_check_count", 0
            )
        ),
        literature_gap_operator_dependency_consistent=bool(
            operator_dependency.get("literature_gap_operator_dependency_consistent")
        ),
        analytic_gap_stack_consistent=bool(operator_dependency.get("analytic_gap_stack_consistent")),
        operator_stack_consistent=bool(operator_dependency.get("operator_stack_consistent")),
        process_gate_open_authorized=process_gate_open_authorized,
        blocker_state_changed=blocker_state_changed,
        candidate_emission_authorized=candidate_emission_authorized,
        missing_source_count=len(missing_sources),
        missing_sources=missing_sources,
        issues=issues,
        queue_items=queue_items,
        checks=tuple(checks),
        source_refs=source_refs,
        non_claims=NON_CLAIMS,
        analytic_gap_snapshot=analytic_gap,
        literature_gap_matrix_snapshot=matrix,
        literature_gap_operator_snapshot=operator,
        literature_gap_operator_dependency_snapshot=operator_dependency,
    )


def theorem_artifact_review_queue_to_dict(
    report: Lemma0252TheoremArtifactReviewQueue,
) -> dict[str, object]:
    return {
        "schema_version": report.schema_version,
        "lemma_id": report.lemma_id,
        "candidate_status": report.candidate_status,
        "active_candidate": report.active_candidate,
        "analytic_gap_markdown": report.analytic_gap_markdown,
        "analytic_gap_json": report.analytic_gap_json,
        "literature_gap_matrix_markdown": report.literature_gap_matrix_markdown,
        "literature_gap_matrix_json": report.literature_gap_matrix_json,
        "literature_gap_operator_markdown": report.literature_gap_operator_markdown,
        "literature_gap_operator_json": report.literature_gap_operator_json,
        "literature_gap_operator_dependency_markdown": (
            report.literature_gap_operator_dependency_markdown
        ),
        "literature_gap_operator_dependency_json": (
            report.literature_gap_operator_dependency_json
        ),
        "queue_item_count": report.queue_item_count,
        "direct_analytic_gap_count": report.direct_analytic_gap_count,
        "blocked_queue_item_count": report.blocked_queue_item_count,
        "actionable_queue_item_count": report.actionable_queue_item_count,
        "may_discharge_queue_item_count": report.may_discharge_queue_item_count,
        "direct_theorem_artifact_count": report.direct_theorem_artifact_count,
        "queue_source_edge_count": report.queue_source_edge_count,
        "direct_branch_source_edge_count": report.direct_branch_source_edge_count,
        "cross_cutting_source_edge_count": report.cross_cutting_source_edge_count,
        "unique_literature_source_count": report.unique_literature_source_count,
        "source_ref_count": report.source_ref_count,
        "literature_source_count": report.literature_source_count,
        "gap_count": report.gap_count,
        "source_gap_edge_count": report.source_gap_edge_count,
        "blocked_gap_count": report.blocked_gap_count,
        "actionable_gap_count": report.actionable_gap_count,
        "may_discharge_gap_count": report.may_discharge_gap_count,
        "direct_discharge_source_count": report.direct_discharge_source_count,
        "literature_gap_operator_dependency_check_count": (
            report.literature_gap_operator_dependency_check_count
        ),
        "failed_literature_gap_operator_dependency_check_count": (
            report.failed_literature_gap_operator_dependency_check_count
        ),
        "literature_gap_operator_dependency_consistent": (
            report.literature_gap_operator_dependency_consistent
        ),
        "analytic_gap_stack_consistent": report.analytic_gap_stack_consistent,
        "operator_stack_consistent": report.operator_stack_consistent,
        "process_gate_open_authorized": report.process_gate_open_authorized,
        "blocker_state_changed": report.blocker_state_changed,
        "candidate_emission_authorized": report.candidate_emission_authorized,
        "missing_source_count": report.missing_source_count,
        "missing_sources": list(report.missing_sources),
        "issues": list(report.issues),
        "queue_items": [
            {
                **asdict(item),
                "required_review_evidence": list(item.required_review_evidence),
                "minimum_acceptance_checks": list(item.minimum_acceptance_checks),
                "source_ids": list(item.source_ids),
                "source_paths": list(item.source_paths),
                "review_sources": [asdict(source) for source in item.review_sources],
            }
            for item in report.queue_items
        ],
        "checks": [asdict(check) for check in report.checks],
        "source_refs": list(report.source_refs),
        "non_claims": list(report.non_claims),
        "analytic_gap_snapshot": report.analytic_gap_snapshot,
        "literature_gap_matrix_snapshot": report.literature_gap_matrix_snapshot,
        "literature_gap_operator_snapshot": report.literature_gap_operator_snapshot,
        "literature_gap_operator_dependency_snapshot": (
            report.literature_gap_operator_dependency_snapshot
        ),
        "docs": {
            "step_doc": "docs/STEP112_LEMMA_0252_THEOREM_ARTIFACT_REVIEW_QUEUE.md",
            "gap_operator_dependency_doc": (
                "docs/STEP111_LEMMA_0252_BLOCKER_LITERATURE_GAP_OPERATOR_DEPENDENCY.md"
            ),
            "gap_operator_doc": (
                "docs/STEP110_LEMMA_0252_BLOCKER_LITERATURE_GAP_OPERATOR_INDEX.md"
            ),
            "gap_matrix_doc": (
                "docs/STEP108_LEMMA_0252_BLOCKER_LITERATURE_GAP_MATRIX.md"
            ),
            "analytic_gap_doc": (
                "docs/STEP102_PROMOTION_GATE_ANALYTIC_DISCHARGE_GAP_INDEX.md"
            ),
        },
    }


def _format(text: str) -> str:
    return text.replace("|", "\\|")


def _summary_lines(report: Lemma0252TheoremArtifactReviewQueue) -> tuple[str, ...]:
    keys = (
        "lemma_id",
        "candidate_status",
        "active_candidate",
        "queue_item_count",
        "direct_analytic_gap_count",
        "blocked_queue_item_count",
        "actionable_queue_item_count",
        "may_discharge_queue_item_count",
        "direct_theorem_artifact_count",
        "queue_source_edge_count",
        "direct_branch_source_edge_count",
        "cross_cutting_source_edge_count",
        "unique_literature_source_count",
        "source_ref_count",
        "literature_source_count",
        "gap_count",
        "source_gap_edge_count",
        "blocked_gap_count",
        "actionable_gap_count",
        "may_discharge_gap_count",
        "direct_discharge_source_count",
        "literature_gap_operator_dependency_check_count",
        "failed_literature_gap_operator_dependency_check_count",
        "literature_gap_operator_dependency_consistent",
        "analytic_gap_stack_consistent",
        "operator_stack_consistent",
        "process_gate_open_authorized",
        "blocker_state_changed",
        "candidate_emission_authorized",
        "missing_source_count",
    )
    data = theorem_artifact_review_queue_to_dict(report)
    return tuple(f"- {key}: `{str(data[key]).lower()}`" for key in keys)


def _queue_rows(report: Lemma0252TheoremArtifactReviewQueue) -> list[str]:
    rows = [
        "| gap | branch | artifact type | sources | status | actionable | may discharge |",
        "|---|---|---|---:|---|---|---|",
    ]
    for item in report.queue_items:
        rows.append(
            "| "
            f"`{item.gap_id}` | `{item.source_branch}` | `{item.required_artifact_type}` | "
            f"{item.literature_source_count} | `{item.queue_status}` | "
            f"`{str(item.actionable_now).lower()}` | "
            f"`{str(item.may_discharge_blocker).lower()}` |"
        )
    return rows


def _source_rows(report: Lemma0252TheoremArtifactReviewQueue) -> list[str]:
    rows = [
        "| gap | source | role | priority | verdict hint | path |",
        "|---|---|---|---|---|---|",
    ]
    for item in report.queue_items:
        for source in item.review_sources:
            rows.append(
                "| "
                f"`{item.gap_id}` | `{source.source_id}` | `{source.support_kind}` | "
                f"`{source.priority}` | `{source.verdict_hint}` | "
                f"`{_format(source.relative_path)}` |"
            )
    return rows


def _check_rows(report: Lemma0252TheoremArtifactReviewQueue) -> list[str]:
    rows = [
        "| check | expected | observed | passed | sources |",
        "|---|---|---|---|---|",
    ]
    for check in report.checks:
        rows.append(
            "| "
            f"`{check.key}` | `{_format(check.expected)}` | `{_format(check.observed)}` | "
            f"`{str(check.passed).lower()}` | "
            f"{', '.join(f'`{_format(source)}`' for source in check.source_artifacts)} |"
        )
    return rows


def render_markdown(report: Lemma0252TheoremArtifactReviewQueue) -> str:
    sections = [
        "# Lemma 0252 Theorem Artifact Review Queue",
        "",
        "This is a read-only, non-promotional queue for the three direct analytic gaps in "
        "`lemma_0252`. A queue entry identifies literature that may help a future theorem-artifact "
        "review, but it does not itself discharge a blocker or authorize candidate emission.",
        "",
        "## Summary",
        "",
        *_summary_lines(report),
        "",
        "## Queue",
        "",
        *_queue_rows(report),
        "",
        "## Literature Sources",
        "",
        *_source_rows(report),
        "",
        "## Checks",
        "",
        *_check_rows(report),
        "",
        "## Non-claims",
        "",
        *(f"- `{claim}`" for claim in report.non_claims),
        "",
    ]
    return "\n".join(sections)


def render_json(report: Lemma0252TheoremArtifactReviewQueue) -> str:
    return json.dumps(
        theorem_artifact_review_queue_to_dict(report),
        indent=2,
        sort_keys=True,
    )


def check_output(
    path: Path,
    report: Lemma0252TheoremArtifactReviewQueue,
    output_format: str,
) -> tuple[bool, str]:
    expected = render_json(report) if output_format == "json" else render_markdown(report)
    if not path.exists():
        return False, f"missing lemma_0252 theorem artifact review queue: {path}"
    observed = path.read_text(encoding="utf-8")
    if observed != expected:
        return False, f"stale lemma_0252 theorem artifact review queue: {path}"
    return True, f"fresh lemma_0252 theorem artifact review queue: {path}"


def check_sources(report: Lemma0252TheoremArtifactReviewQueue) -> tuple[bool, str]:
    if report.missing_sources:
        return False, "missing sources: " + ", ".join(report.missing_sources)
    return True, "all lemma_0252 theorem artifact review queue sources exist"


def check_consistent(report: Lemma0252TheoremArtifactReviewQueue) -> tuple[bool, str]:
    if report.issues:
        return False, "inconsistent checks: " + ", ".join(report.issues)
    if not report.literature_gap_operator_dependency_consistent:
        return False, "upstream literature gap operator dependency is inconsistent"
    if not report.analytic_gap_stack_consistent or not report.operator_stack_consistent:
        return False, "upstream analytic/operator stack is inconsistent"
    return True, "lemma_0252 theorem artifact review queue is consistent"


def check_blocked(report: Lemma0252TheoremArtifactReviewQueue) -> tuple[bool, str]:
    if report.blocked_queue_item_count != report.queue_item_count:
        return False, "not every theorem artifact review queue item is blocked"
    if report.actionable_queue_item_count:
        return False, "theorem artifact review queue contains actionable entries"
    if report.may_discharge_queue_item_count:
        return False, "theorem artifact review queue contains dischargeable entries"
    if report.direct_theorem_artifact_count:
        return False, "theorem artifact review queue claims a direct theorem artifact"
    if report.process_gate_open_authorized:
        return False, "process gate was authorized"
    if report.blocker_state_changed:
        return False, "blocker state changed"
    if report.candidate_emission_authorized:
        return False, "candidate emission was authorized"
    return True, "lemma_0252 theorem artifact review queue remains blocked"


def _write_output(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _print_summary(report: Lemma0252TheoremArtifactReviewQueue) -> None:
    for line in _summary_lines(report):
        print(line.removeprefix("- "))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Build the lemma_0252 theorem-artifact review queue."
    )
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--check-output", action="store_true")
    parser.add_argument("--require-sources-exist", action="store_true")
    parser.add_argument("--require-consistent", action="store_true")
    parser.add_argument("--require-blocked", action="store_true")
    args = parser.parse_args(argv)

    report = build_theorem_artifact_review_queue()
    output = args.output
    if output is None:
        output = DEFAULT_JSON_OUTPUT if args.format == "json" else DEFAULT_MARKDOWN_OUTPUT

    text = render_json(report) if args.format == "json" else render_markdown(report)
    _write_output(output, text)

    failed = False
    if args.check_output:
        ok, message = check_output(output, report, args.format)
        print(message)
        failed = failed or not ok
    if args.require_sources_exist:
        ok, message = check_sources(report)
        print(message)
        failed = failed or not ok
    if args.require_consistent:
        ok, message = check_consistent(report)
        print(message)
        failed = failed or not ok
    if args.require_blocked:
        ok, message = check_blocked(report)
        print(message)
        failed = failed or not ok

    _print_summary(report)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
