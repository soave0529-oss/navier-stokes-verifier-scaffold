from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from lemma_0252_blocker_literature_gap_dependency import (
    DEFAULT_JSON_OUTPUT as DEFAULT_GAP_DEPENDENCY_JSON,
    DEFAULT_MARKDOWN_OUTPUT as DEFAULT_GAP_DEPENDENCY_MARKDOWN,
)
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
from lemma_0252_theorem_artifact_review_queue import (
    DEFAULT_JSON_OUTPUT as DEFAULT_QUEUE_JSON,
    DEFAULT_MARKDOWN_OUTPUT as DEFAULT_QUEUE_MARKDOWN,
)
from lemma_0252_theorem_artifact_review_queue_dependency import (
    DEFAULT_JSON_OUTPUT as DEFAULT_QUEUE_DEPENDENCY_JSON,
    DEFAULT_MARKDOWN_OUTPUT as DEFAULT_QUEUE_DEPENDENCY_MARKDOWN,
)
from lemma_0252_theorem_artifact_review_queue_operator_index import (
    DEFAULT_JSON_OUTPUT as DEFAULT_QUEUE_OPERATOR_JSON,
    DEFAULT_MARKDOWN_OUTPUT as DEFAULT_QUEUE_OPERATOR_MARKDOWN,
)
from promotion_gate_analytic_discharge_gap_index import (
    DEFAULT_JSON_OUTPUT as DEFAULT_ANALYTIC_GAP_JSON,
    DEFAULT_MARKDOWN_OUTPUT as DEFAULT_ANALYTIC_GAP_MARKDOWN,
)


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REPORT_DIR = ROOT / "track-a-regularity/reports"
DEFAULT_MARKDOWN_OUTPUT = (
    DEFAULT_REPORT_DIR
    / "lemma_0252_theorem_artifact_review_queue_operator_dependency.md"
)
DEFAULT_JSON_OUTPUT = (
    DEFAULT_REPORT_DIR
    / "lemma_0252_theorem_artifact_review_queue_operator_dependency.json"
)
DEFAULT_PAPERS_INDEX = ROOT / "papers/blockers/index.md"

NON_CLAIMS = (
    "read_only_theorem_artifact_review_queue_operator_dependency_guard",
    "canonical_report_freshness_only",
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
class TheoremArtifactReviewQueueOperatorDependencyCheck:
    key: str
    expected: str
    observed: str
    passed: bool
    source_artifacts: tuple[str, ...]


@dataclass(frozen=True)
class Lemma0252TheoremArtifactReviewQueueOperatorDependency:
    schema_version: int
    lemma_id: str
    candidate_status: str
    active_candidate: bool
    theorem_artifact_review_queue_operator_markdown: str
    theorem_artifact_review_queue_operator_json: str
    theorem_artifact_review_queue_markdown: str
    theorem_artifact_review_queue_json: str
    theorem_artifact_review_queue_dependency_markdown: str
    theorem_artifact_review_queue_dependency_json: str
    analytic_gap_markdown: str
    analytic_gap_json: str
    literature_gap_matrix_markdown: str
    literature_gap_matrix_json: str
    literature_gap_dependency_markdown: str
    literature_gap_dependency_json: str
    literature_gap_operator_markdown: str
    literature_gap_operator_json: str
    literature_gap_operator_dependency_markdown: str
    literature_gap_operator_dependency_json: str
    papers_blockers_index: str
    direct_source_report_count: int
    source_ref_count: int
    theorem_artifact_review_queue_operator_dependency_check_count: int
    passed_theorem_artifact_review_queue_operator_dependency_check_count: int
    failed_theorem_artifact_review_queue_operator_dependency_check_count: int
    theorem_artifact_review_queue_operator_dependency_consistent: bool
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
    literature_source_count: int
    gap_count: int
    source_gap_edge_count: int
    blocked_gap_count: int
    actionable_gap_count: int
    may_discharge_gap_count: int
    direct_discharge_source_count: int
    theorem_artifact_review_queue_dependency_check_count: int
    failed_theorem_artifact_review_queue_dependency_check_count: int
    theorem_artifact_review_queue_operator_index_check_count: int
    failed_theorem_artifact_review_queue_operator_index_check_count: int
    literature_gap_dependency_check_count: int
    failed_literature_gap_dependency_check_count: int
    literature_gap_operator_index_check_count: int
    failed_literature_gap_operator_index_check_count: int
    literature_gap_operator_dependency_check_count: int
    failed_literature_gap_operator_dependency_check_count: int
    theorem_artifact_review_queue_dependency_consistent: bool
    theorem_artifact_review_queue_operator_index_consistent: bool
    literature_gap_dependency_consistent: bool
    literature_gap_operator_index_consistent: bool
    literature_gap_operator_dependency_consistent: bool
    analytic_gap_stack_consistent: bool
    operator_stack_consistent: bool
    process_gate_open_authorized: bool
    blocker_state_changed: bool
    candidate_emission_authorized: bool
    missing_source_count: int
    missing_sources: tuple[str, ...]
    issues: tuple[str, ...]
    checks: tuple[TheoremArtifactReviewQueueOperatorDependencyCheck, ...]
    source_refs: tuple[str, ...]
    non_claims: tuple[str, ...]
    theorem_artifact_review_queue_operator_snapshot: dict[str, object]
    theorem_artifact_review_queue_snapshot: dict[str, object]
    theorem_artifact_review_queue_dependency_snapshot: dict[str, object]
    analytic_gap_snapshot: dict[str, object]
    literature_gap_matrix_snapshot: dict[str, object]
    literature_gap_dependency_snapshot: dict[str, object]
    literature_gap_operator_snapshot: dict[str, object]
    literature_gap_operator_dependency_snapshot: dict[str, object]


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
) -> TheoremArtifactReviewQueueOperatorDependencyCheck:
    return TheoremArtifactReviewQueueOperatorDependencyCheck(
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
            "lemma_0252_theorem_artifact_review_queue_operator_index.md"
        ),
        (
            "track-a-regularity/reports/"
            "lemma_0252_theorem_artifact_review_queue_operator_index.json"
        ),
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
        "track-a-regularity/reports/promotion_gate_analytic_discharge_gap_index.md",
        "track-a-regularity/reports/promotion_gate_analytic_discharge_gap_index.json",
        "track-a-regularity/reports/lemma_0252_blocker_literature_gap_matrix.md",
        "track-a-regularity/reports/lemma_0252_blocker_literature_gap_matrix.json",
        "track-a-regularity/reports/lemma_0252_blocker_literature_gap_dependency.md",
        "track-a-regularity/reports/lemma_0252_blocker_literature_gap_dependency.json",
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
    )


def _direct_sources() -> tuple[str, ...]:
    return _direct_source_reports() + ("papers/blockers/index.md",)


def _all_reports(*reports: dict[str, object]) -> tuple[dict[str, object], ...]:
    return reports


def build_theorem_artifact_review_queue_operator_dependency(
    *,
    theorem_artifact_review_queue_operator_json: Path = DEFAULT_QUEUE_OPERATOR_JSON,
    theorem_artifact_review_queue_json: Path = DEFAULT_QUEUE_JSON,
    theorem_artifact_review_queue_dependency_json: Path = DEFAULT_QUEUE_DEPENDENCY_JSON,
    analytic_gap_json: Path = DEFAULT_ANALYTIC_GAP_JSON,
    literature_gap_matrix_json: Path = DEFAULT_GAP_MATRIX_JSON,
    literature_gap_dependency_json: Path = DEFAULT_GAP_DEPENDENCY_JSON,
    literature_gap_operator_json: Path = DEFAULT_GAP_OPERATOR_JSON,
    literature_gap_operator_dependency_json: Path = DEFAULT_GAP_OPERATOR_DEPENDENCY_JSON,
    papers_blockers_index: Path = DEFAULT_PAPERS_INDEX,
) -> Lemma0252TheoremArtifactReviewQueueOperatorDependency:
    operator = _load_json(theorem_artifact_review_queue_operator_json)
    queue = _load_json(theorem_artifact_review_queue_json)
    queue_dependency = _load_json(theorem_artifact_review_queue_dependency_json)
    analytic_gap = _load_json(analytic_gap_json)
    matrix = _load_json(literature_gap_matrix_json)
    gap_dependency = _load_json(literature_gap_dependency_json)
    literature_operator = _load_json(literature_gap_operator_json)
    literature_operator_dependency = _load_json(literature_gap_operator_dependency_json)

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
    analytic_source = (
        "track-a-regularity/reports/promotion_gate_analytic_discharge_gap_index.md",
        "track-a-regularity/reports/promotion_gate_analytic_discharge_gap_index.json",
    )
    matrix_source = (
        "track-a-regularity/reports/lemma_0252_blocker_literature_gap_matrix.md",
        "track-a-regularity/reports/lemma_0252_blocker_literature_gap_matrix.json",
    )
    gap_dependency_source = (
        "track-a-regularity/reports/lemma_0252_blocker_literature_gap_dependency.md",
        "track-a-regularity/reports/lemma_0252_blocker_literature_gap_dependency.json",
    )
    literature_operator_source = (
        "track-a-regularity/reports/lemma_0252_blocker_literature_gap_operator_index.md",
        "track-a-regularity/reports/lemma_0252_blocker_literature_gap_operator_index.json",
    )
    literature_operator_dependency_source = (
        (
            "track-a-regularity/reports/"
            "lemma_0252_blocker_literature_gap_operator_dependency.md"
        ),
        (
            "track-a-regularity/reports/"
            "lemma_0252_blocker_literature_gap_operator_dependency.json"
        ),
    )
    papers_source = ("papers/blockers/index.md",)

    source_refs = tuple(
        dict.fromkeys(
            _direct_sources()
            + tuple(str(item) for item in operator.get("source_refs", ()))
            + tuple(str(item) for item in queue.get("source_refs", ()))
            + tuple(str(item) for item in queue_dependency.get("source_refs", ()))
            + tuple(str(item) for item in analytic_gap.get("source_refs", ()))
            + tuple(str(item) for item in matrix.get("source_refs", ()))
            + tuple(str(item) for item in gap_dependency.get("source_refs", ()))
            + tuple(str(item) for item in literature_operator.get("source_refs", ()))
            + tuple(
                str(item) for item in literature_operator_dependency.get("source_refs", ())
            )
        )
    )
    missing_sources = _missing_sources(source_refs)

    reports = _all_reports(
        operator,
        queue,
        queue_dependency,
        analytic_gap,
        matrix,
        gap_dependency,
        literature_operator,
        literature_operator_dependency,
    )
    all_sources = (
        operator_source
        + queue_source
        + queue_dependency_source
        + analytic_source
        + matrix_source
        + gap_dependency_source
        + literature_operator_source
        + literature_operator_dependency_source
    )

    checks = (
        _check(
            key="operator.lemma_id.matches_queue",
            expected=queue.get("lemma_id"),
            observed=operator.get("lemma_id"),
            source_artifacts=operator_source + queue_source,
        ),
        _check(
            key="operator.lemma_id.matches_queue_dependency",
            expected=queue_dependency.get("lemma_id"),
            observed=operator.get("lemma_id"),
            source_artifacts=operator_source + queue_dependency_source,
        ),
        _check(
            key="operator.lemma_id.matches_analytic_gap",
            expected=analytic_gap.get("lemma_id"),
            observed=operator.get("lemma_id"),
            source_artifacts=operator_source + analytic_source,
        ),
        _check(
            key="operator.lemma_id.matches_literature_gap_matrix",
            expected=matrix.get("lemma_id"),
            observed=operator.get("lemma_id"),
            source_artifacts=operator_source + matrix_source,
        ),
        _check(
            key="operator.lemma_id.matches_literature_gap_dependency",
            expected=gap_dependency.get("lemma_id"),
            observed=operator.get("lemma_id"),
            source_artifacts=operator_source + gap_dependency_source,
        ),
        _check(
            key="operator.lemma_id.matches_literature_gap_operator",
            expected=literature_operator.get("lemma_id"),
            observed=operator.get("lemma_id"),
            source_artifacts=operator_source + literature_operator_source,
        ),
        _check(
            key="operator.lemma_id.matches_literature_gap_operator_dependency",
            expected=literature_operator_dependency.get("lemma_id"),
            observed=operator.get("lemma_id"),
            source_artifacts=operator_source + literature_operator_dependency_source,
        ),
        _check(
            key="operator.candidate_status.matches_queue",
            expected=queue.get("candidate_status"),
            observed=operator.get("candidate_status"),
            source_artifacts=operator_source + queue_source,
        ),
        _check(
            key="operator.active_candidate.matches_queue",
            expected=queue.get("active_candidate"),
            observed=operator.get("active_candidate"),
            source_artifacts=operator_source + queue_source,
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
            key="operator.queue_item_count.matches_queue",
            expected=queue.get("queue_item_count"),
            observed=operator.get("queue_item_count"),
            source_artifacts=operator_source + queue_source,
        ),
        _check(
            key="operator.queue_item_count.matches_queue_dependency",
            expected=queue_dependency.get("queue_item_count"),
            observed=operator.get("queue_item_count"),
            source_artifacts=operator_source + queue_dependency_source,
        ),
        _check(
            key="operator.direct_analytic_gap_count.matches_queue",
            expected=queue.get("direct_analytic_gap_count"),
            observed=operator.get("direct_analytic_gap_count"),
            source_artifacts=operator_source + queue_source,
        ),
        _check(
            key="operator.blocked_queue_item_count.matches_queue",
            expected=queue.get("blocked_queue_item_count"),
            observed=operator.get("blocked_queue_item_count"),
            source_artifacts=operator_source + queue_source,
        ),
        _check(
            key="operator.blocked_queue_item_count.matches_queue_dependency",
            expected=queue_dependency.get("blocked_queue_item_count"),
            observed=operator.get("blocked_queue_item_count"),
            source_artifacts=operator_source + queue_dependency_source,
        ),
        _check(
            key="all.actionable_queue_item_count.remains_zero",
            expected=(0, 0, 0),
            observed=(
                operator.get("actionable_queue_item_count"),
                queue.get("actionable_queue_item_count"),
                queue_dependency.get("actionable_queue_item_count"),
            ),
            source_artifacts=operator_source + queue_source + queue_dependency_source,
        ),
        _check(
            key="all.may_discharge_queue_item_count.remains_zero",
            expected=(0, 0, 0),
            observed=(
                operator.get("may_discharge_queue_item_count"),
                queue.get("may_discharge_queue_item_count"),
                queue_dependency.get("may_discharge_queue_item_count"),
            ),
            source_artifacts=operator_source + queue_source + queue_dependency_source,
        ),
        _check(
            key="all.direct_theorem_artifact_count.remains_zero",
            expected=(0, 0, 0),
            observed=(
                operator.get("direct_theorem_artifact_count"),
                queue.get("direct_theorem_artifact_count"),
                queue_dependency.get("direct_theorem_artifact_count"),
            ),
            source_artifacts=operator_source + queue_source + queue_dependency_source,
        ),
        _check(
            key="operator.queue_source_edge_count.matches_queue",
            expected=queue.get("queue_source_edge_count"),
            observed=operator.get("queue_source_edge_count"),
            source_artifacts=operator_source + queue_source,
        ),
        _check(
            key="operator.queue_source_edge_count.matches_queue_dependency",
            expected=queue_dependency.get("queue_source_edge_count"),
            observed=operator.get("queue_source_edge_count"),
            source_artifacts=operator_source + queue_dependency_source,
        ),
        _check(
            key="operator.direct_branch_source_edge_count.matches_queue",
            expected=queue.get("direct_branch_source_edge_count"),
            observed=operator.get("direct_branch_source_edge_count"),
            source_artifacts=operator_source + queue_source,
        ),
        _check(
            key="operator.cross_cutting_source_edge_count.matches_queue",
            expected=queue.get("cross_cutting_source_edge_count"),
            observed=operator.get("cross_cutting_source_edge_count"),
            source_artifacts=operator_source + queue_source,
        ),
        _check(
            key="operator.unique_literature_source_count.matches_queue",
            expected=queue.get("unique_literature_source_count"),
            observed=operator.get("unique_literature_source_count"),
            source_artifacts=operator_source + queue_source,
        ),
        _check(
            key="operator.literature_source_count.matches_literature_operator_dependency",
            expected=literature_operator_dependency.get("literature_source_count"),
            observed=operator.get("literature_source_count"),
            source_artifacts=operator_source + literature_operator_dependency_source,
        ),
        _check(
            key="operator.gap_count.matches_analytic_gap",
            expected=analytic_gap.get("gap_count"),
            observed=operator.get("gap_count"),
            source_artifacts=operator_source + analytic_source,
        ),
        _check(
            key="operator.source_gap_edge_count.matches_matrix",
            expected=matrix.get("source_gap_edge_count"),
            observed=operator.get("source_gap_edge_count"),
            source_artifacts=operator_source + matrix_source,
        ),
        _check(
            key="operator.blocked_gap_count.matches_analytic_gap",
            expected=analytic_gap.get("blocked_gap_count"),
            observed=operator.get("blocked_gap_count"),
            source_artifacts=operator_source + analytic_source,
        ),
        _check(
            key="all.actionable_gap_count.remains_zero",
            expected=(0, 0, 0, 0, 0, 0, 0, 0),
            observed=tuple(int(report.get("actionable_gap_count", 0) or 0) for report in reports),
            source_artifacts=all_sources,
        ),
        _check(
            key="all.may_discharge_gap_count.remains_zero",
            expected=(0, 0, 0, 0, 0, 0, 0, 0),
            observed=tuple(int(report.get("may_discharge_gap_count", 0) or 0) for report in reports),
            source_artifacts=all_sources,
        ),
        _check(
            key="all.direct_discharge_source_count.remains_zero",
            expected=(0, 0, 0, 0, 0, 0, 0, 0),
            observed=tuple(
                int(report.get("direct_discharge_source_count", 0) or 0)
                for report in reports
            ),
            source_artifacts=all_sources,
        ),
        _check(
            key="queue_dependency.check_count.matches_operator",
            expected=queue_dependency.get("theorem_artifact_review_queue_dependency_check_count"),
            observed=operator.get("theorem_artifact_review_queue_dependency_check_count"),
            source_artifacts=operator_source + queue_dependency_source,
        ),
        _check(
            key="queue_dependency.failed_checks.matches_operator",
            expected=queue_dependency.get(
                "failed_theorem_artifact_review_queue_dependency_check_count"
            ),
            observed=operator.get(
                "failed_theorem_artifact_review_queue_dependency_check_count"
            ),
            source_artifacts=operator_source + queue_dependency_source,
        ),
        _check(
            key="queue_dependency.consistent.matches_operator",
            expected=queue_dependency.get("theorem_artifact_review_queue_dependency_consistent"),
            observed=operator.get("theorem_artifact_review_queue_dependency_consistent"),
            source_artifacts=operator_source + queue_dependency_source,
        ),
        _check(
            key="queue_dependency.consistent.true",
            expected=True,
            observed=queue_dependency.get("theorem_artifact_review_queue_dependency_consistent"),
            source_artifacts=queue_dependency_source,
        ),
        _check(
            key="operator.index_check_count.expected_forty_four",
            expected=44,
            observed=operator.get("theorem_artifact_review_queue_operator_index_check_count"),
            source_artifacts=operator_source,
        ),
        _check(
            key="operator.index_failed_checks.remains_zero",
            expected=0,
            observed=operator.get("failed_theorem_artifact_review_queue_operator_index_check_count"),
            source_artifacts=operator_source,
        ),
        _check(
            key="operator.index_consistent.true",
            expected=True,
            observed=operator.get("theorem_artifact_review_queue_operator_index_consistent"),
            source_artifacts=operator_source,
        ),
        _check(
            key="literature_gap_dependency.check_count.expected_thirty_eight",
            expected=38,
            observed=gap_dependency.get("literature_gap_dependency_check_count"),
            source_artifacts=gap_dependency_source,
        ),
        _check(
            key="literature_gap_operator.index_check_count.expected_thirty",
            expected=30,
            observed=literature_operator.get("literature_gap_operator_index_check_count"),
            source_artifacts=literature_operator_source,
        ),
        _check(
            key="literature_gap_operator_dependency.check_count.expected_forty_two",
            expected=42,
            observed=literature_operator_dependency.get(
                "literature_gap_operator_dependency_check_count"
            ),
            source_artifacts=literature_operator_dependency_source,
        ),
        _check(
            key="literature_stack.consistent.true",
            expected=(True, True, True),
            observed=(
                gap_dependency.get("literature_gap_dependency_consistent"),
                literature_operator.get("literature_gap_operator_index_consistent"),
                literature_operator_dependency.get(
                    "literature_gap_operator_dependency_consistent"
                ),
            ),
            source_artifacts=gap_dependency_source
            + literature_operator_source
            + literature_operator_dependency_source,
        ),
        _check(
            key="analytic_gap_stack_consistent.true",
            expected=(True, True, True),
            observed=(
                operator.get("analytic_gap_stack_consistent"),
                queue.get("analytic_gap_stack_consistent"),
                queue_dependency.get("analytic_gap_stack_consistent"),
            ),
            source_artifacts=operator_source + queue_source + queue_dependency_source,
        ),
        _check(
            key="operator_stack_consistent.true",
            expected=(True, True, True),
            observed=(
                operator.get("operator_stack_consistent"),
                queue.get("operator_stack_consistent"),
                queue_dependency.get("operator_stack_consistent"),
            ),
            source_artifacts=operator_source + queue_source + queue_dependency_source,
        ),
        _check(
            key="source_reports.issues.all_empty",
            expected=((), (), (), (), (), (), (), ()),
            observed=tuple(tuple(report.get("issues", ())) for report in reports),
            source_artifacts=all_sources,
        ),
        _check(
            key="direct_source_report_count.expected_sixteen",
            expected=16,
            observed=len(_direct_source_reports()),
            source_artifacts=_direct_source_reports(),
        ),
        _check(
            key="all.process_gate_open_authorized.false",
            expected=(False, False, False, False, False, False, False, False),
            observed=tuple(report.get("process_gate_open_authorized") for report in reports),
            source_artifacts=all_sources,
        ),
        _check(
            key="all.blocker_state_changed.false",
            expected=(False, False, False, False, False, False, False, False),
            observed=tuple(report.get("blocker_state_changed") for report in reports),
            source_artifacts=all_sources,
        ),
        _check(
            key="all.candidate_emission_authorized.false",
            expected=(False, False, False, False, False, False, False, False),
            observed=tuple(report.get("candidate_emission_authorized") for report in reports),
            source_artifacts=all_sources,
        ),
        _check(
            key="candidate_status.remains_needs_review",
            expected="needs_review",
            observed=operator.get("candidate_status"),
            source_artifacts=operator_source,
        ),
        _check(
            key="active_candidate.remains_false",
            expected=False,
            observed=operator.get("active_candidate"),
            source_artifacts=operator_source,
        ),
        _check(
            key="source_refs.missing_count.remains_zero",
            expected=0,
            observed=len(missing_sources),
            source_artifacts=source_refs,
        ),
        _check(
            key="source_refs.include_theorem_artifact_queue_operator_reports",
            expected=operator_source,
            observed=tuple(source for source in operator_source if source in source_refs),
            source_artifacts=operator_source,
        ),
        _check(
            key="source_refs.include_theorem_artifact_queue_reports",
            expected=queue_source,
            observed=tuple(source for source in queue_source if source in source_refs),
            source_artifacts=queue_source,
        ),
        _check(
            key="source_refs.include_theorem_artifact_queue_dependency_reports",
            expected=queue_dependency_source,
            observed=tuple(source for source in queue_dependency_source if source in source_refs),
            source_artifacts=queue_dependency_source,
        ),
        _check(
            key="source_refs.include_analytic_gap_reports",
            expected=analytic_source,
            observed=tuple(source for source in analytic_source if source in source_refs),
            source_artifacts=analytic_source,
        ),
        _check(
            key="source_refs.include_literature_gap_matrix_reports",
            expected=matrix_source,
            observed=tuple(source for source in matrix_source if source in source_refs),
            source_artifacts=matrix_source,
        ),
        _check(
            key="source_refs.include_literature_gap_dependency_reports",
            expected=gap_dependency_source,
            observed=tuple(source for source in gap_dependency_source if source in source_refs),
            source_artifacts=gap_dependency_source,
        ),
        _check(
            key="source_refs.include_literature_gap_operator_reports",
            expected=literature_operator_source,
            observed=tuple(source for source in literature_operator_source if source in source_refs),
            source_artifacts=literature_operator_source,
        ),
        _check(
            key="source_refs.include_literature_gap_operator_dependency_reports",
            expected=literature_operator_dependency_source,
            observed=tuple(
                source for source in literature_operator_dependency_source if source in source_refs
            ),
            source_artifacts=literature_operator_dependency_source,
        ),
        _check(
            key="source_refs.include_papers_blockers_index",
            expected=True,
            observed="papers/blockers/index.md" in source_refs and papers_blockers_index.exists(),
            source_artifacts=papers_source,
        ),
    )
    issues = tuple(check.key for check in checks if not check.passed)

    process_gate_open_authorized = any(
        bool(report.get("process_gate_open_authorized")) for report in reports
    )
    blocker_state_changed = any(bool(report.get("blocker_state_changed")) for report in reports)
    candidate_emission_authorized = any(
        bool(report.get("candidate_emission_authorized")) for report in reports
    )

    return Lemma0252TheoremArtifactReviewQueueOperatorDependency(
        schema_version=1,
        lemma_id=str(operator.get("lemma_id")),
        candidate_status=str(operator.get("candidate_status")),
        active_candidate=bool(operator.get("active_candidate")),
        theorem_artifact_review_queue_operator_markdown=_relative(
            DEFAULT_QUEUE_OPERATOR_MARKDOWN
        ),
        theorem_artifact_review_queue_operator_json=_relative(DEFAULT_QUEUE_OPERATOR_JSON),
        theorem_artifact_review_queue_markdown=_relative(DEFAULT_QUEUE_MARKDOWN),
        theorem_artifact_review_queue_json=_relative(DEFAULT_QUEUE_JSON),
        theorem_artifact_review_queue_dependency_markdown=_relative(
            DEFAULT_QUEUE_DEPENDENCY_MARKDOWN
        ),
        theorem_artifact_review_queue_dependency_json=_relative(
            DEFAULT_QUEUE_DEPENDENCY_JSON
        ),
        analytic_gap_markdown=_relative(DEFAULT_ANALYTIC_GAP_MARKDOWN),
        analytic_gap_json=_relative(DEFAULT_ANALYTIC_GAP_JSON),
        literature_gap_matrix_markdown=_relative(DEFAULT_GAP_MATRIX_MARKDOWN),
        literature_gap_matrix_json=_relative(DEFAULT_GAP_MATRIX_JSON),
        literature_gap_dependency_markdown=_relative(DEFAULT_GAP_DEPENDENCY_MARKDOWN),
        literature_gap_dependency_json=_relative(DEFAULT_GAP_DEPENDENCY_JSON),
        literature_gap_operator_markdown=_relative(DEFAULT_GAP_OPERATOR_MARKDOWN),
        literature_gap_operator_json=_relative(DEFAULT_GAP_OPERATOR_JSON),
        literature_gap_operator_dependency_markdown=_relative(
            DEFAULT_GAP_OPERATOR_DEPENDENCY_MARKDOWN
        ),
        literature_gap_operator_dependency_json=_relative(
            DEFAULT_GAP_OPERATOR_DEPENDENCY_JSON
        ),
        papers_blockers_index=_relative(DEFAULT_PAPERS_INDEX),
        direct_source_report_count=len(_direct_source_reports()),
        source_ref_count=len(source_refs),
        theorem_artifact_review_queue_operator_dependency_check_count=len(checks),
        passed_theorem_artifact_review_queue_operator_dependency_check_count=(
            len(checks) - len(issues)
        ),
        failed_theorem_artifact_review_queue_operator_dependency_check_count=len(issues),
        theorem_artifact_review_queue_operator_dependency_consistent=(
            not issues and not missing_sources
        ),
        queue_item_count=int(operator.get("queue_item_count", 0)),
        direct_analytic_gap_count=int(operator.get("direct_analytic_gap_count", 0)),
        blocked_queue_item_count=int(operator.get("blocked_queue_item_count", 0)),
        actionable_queue_item_count=int(operator.get("actionable_queue_item_count", 0)),
        may_discharge_queue_item_count=int(operator.get("may_discharge_queue_item_count", 0)),
        direct_theorem_artifact_count=int(operator.get("direct_theorem_artifact_count", 0)),
        queue_source_edge_count=int(operator.get("queue_source_edge_count", 0)),
        direct_branch_source_edge_count=int(operator.get("direct_branch_source_edge_count", 0)),
        cross_cutting_source_edge_count=int(operator.get("cross_cutting_source_edge_count", 0)),
        unique_literature_source_count=int(operator.get("unique_literature_source_count", 0)),
        literature_source_count=int(operator.get("literature_source_count", 0)),
        gap_count=int(operator.get("gap_count", 0)),
        source_gap_edge_count=int(operator.get("source_gap_edge_count", 0)),
        blocked_gap_count=int(operator.get("blocked_gap_count", 0)),
        actionable_gap_count=int(operator.get("actionable_gap_count", 0)),
        may_discharge_gap_count=int(operator.get("may_discharge_gap_count", 0)),
        direct_discharge_source_count=int(operator.get("direct_discharge_source_count", 0)),
        theorem_artifact_review_queue_dependency_check_count=int(
            operator.get("theorem_artifact_review_queue_dependency_check_count", 0)
        ),
        failed_theorem_artifact_review_queue_dependency_check_count=int(
            operator.get("failed_theorem_artifact_review_queue_dependency_check_count", 0)
        ),
        theorem_artifact_review_queue_operator_index_check_count=int(
            operator.get("theorem_artifact_review_queue_operator_index_check_count", 0)
        ),
        failed_theorem_artifact_review_queue_operator_index_check_count=int(
            operator.get("failed_theorem_artifact_review_queue_operator_index_check_count", 0)
        ),
        literature_gap_dependency_check_count=int(
            gap_dependency.get("literature_gap_dependency_check_count", 0)
        ),
        failed_literature_gap_dependency_check_count=int(
            gap_dependency.get("failed_literature_gap_dependency_check_count", 0)
        ),
        literature_gap_operator_index_check_count=int(
            literature_operator.get("literature_gap_operator_index_check_count", 0)
        ),
        failed_literature_gap_operator_index_check_count=int(
            literature_operator.get("failed_literature_gap_operator_index_check_count", 0)
        ),
        literature_gap_operator_dependency_check_count=int(
            literature_operator_dependency.get("literature_gap_operator_dependency_check_count", 0)
        ),
        failed_literature_gap_operator_dependency_check_count=int(
            literature_operator_dependency.get(
                "failed_literature_gap_operator_dependency_check_count", 0
            )
        ),
        theorem_artifact_review_queue_dependency_consistent=bool(
            operator.get("theorem_artifact_review_queue_dependency_consistent")
        )
        and bool(queue_dependency.get("theorem_artifact_review_queue_dependency_consistent")),
        theorem_artifact_review_queue_operator_index_consistent=bool(
            operator.get("theorem_artifact_review_queue_operator_index_consistent")
        ),
        literature_gap_dependency_consistent=bool(
            gap_dependency.get("literature_gap_dependency_consistent")
        ),
        literature_gap_operator_index_consistent=bool(
            literature_operator.get("literature_gap_operator_index_consistent")
        ),
        literature_gap_operator_dependency_consistent=bool(
            literature_operator_dependency.get("literature_gap_operator_dependency_consistent")
        ),
        analytic_gap_stack_consistent=bool(operator.get("analytic_gap_stack_consistent"))
        and bool(queue.get("analytic_gap_stack_consistent"))
        and bool(queue_dependency.get("analytic_gap_stack_consistent")),
        operator_stack_consistent=bool(operator.get("operator_stack_consistent"))
        and bool(queue.get("operator_stack_consistent"))
        and bool(queue_dependency.get("operator_stack_consistent")),
        process_gate_open_authorized=process_gate_open_authorized,
        blocker_state_changed=blocker_state_changed,
        candidate_emission_authorized=candidate_emission_authorized,
        missing_source_count=len(missing_sources),
        missing_sources=missing_sources,
        issues=issues,
        checks=checks,
        source_refs=source_refs,
        non_claims=NON_CLAIMS,
        theorem_artifact_review_queue_operator_snapshot=operator,
        theorem_artifact_review_queue_snapshot=queue,
        theorem_artifact_review_queue_dependency_snapshot=queue_dependency,
        analytic_gap_snapshot=analytic_gap,
        literature_gap_matrix_snapshot=matrix,
        literature_gap_dependency_snapshot=gap_dependency,
        literature_gap_operator_snapshot=literature_operator,
        literature_gap_operator_dependency_snapshot=literature_operator_dependency,
    )


def theorem_artifact_review_queue_operator_dependency_to_dict(
    report: Lemma0252TheoremArtifactReviewQueueOperatorDependency,
) -> dict[str, object]:
    return {
        "schema_version": report.schema_version,
        "lemma_id": report.lemma_id,
        "candidate_status": report.candidate_status,
        "active_candidate": report.active_candidate,
        "theorem_artifact_review_queue_operator_markdown": (
            report.theorem_artifact_review_queue_operator_markdown
        ),
        "theorem_artifact_review_queue_operator_json": (
            report.theorem_artifact_review_queue_operator_json
        ),
        "theorem_artifact_review_queue_markdown": (
            report.theorem_artifact_review_queue_markdown
        ),
        "theorem_artifact_review_queue_json": report.theorem_artifact_review_queue_json,
        "theorem_artifact_review_queue_dependency_markdown": (
            report.theorem_artifact_review_queue_dependency_markdown
        ),
        "theorem_artifact_review_queue_dependency_json": (
            report.theorem_artifact_review_queue_dependency_json
        ),
        "analytic_gap_markdown": report.analytic_gap_markdown,
        "analytic_gap_json": report.analytic_gap_json,
        "literature_gap_matrix_markdown": report.literature_gap_matrix_markdown,
        "literature_gap_matrix_json": report.literature_gap_matrix_json,
        "literature_gap_dependency_markdown": report.literature_gap_dependency_markdown,
        "literature_gap_dependency_json": report.literature_gap_dependency_json,
        "literature_gap_operator_markdown": report.literature_gap_operator_markdown,
        "literature_gap_operator_json": report.literature_gap_operator_json,
        "literature_gap_operator_dependency_markdown": (
            report.literature_gap_operator_dependency_markdown
        ),
        "literature_gap_operator_dependency_json": (
            report.literature_gap_operator_dependency_json
        ),
        "papers_blockers_index": report.papers_blockers_index,
        "direct_source_report_count": report.direct_source_report_count,
        "source_ref_count": report.source_ref_count,
        "theorem_artifact_review_queue_operator_dependency_check_count": (
            report.theorem_artifact_review_queue_operator_dependency_check_count
        ),
        "passed_theorem_artifact_review_queue_operator_dependency_check_count": (
            report.passed_theorem_artifact_review_queue_operator_dependency_check_count
        ),
        "failed_theorem_artifact_review_queue_operator_dependency_check_count": (
            report.failed_theorem_artifact_review_queue_operator_dependency_check_count
        ),
        "theorem_artifact_review_queue_operator_dependency_consistent": (
            report.theorem_artifact_review_queue_operator_dependency_consistent
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
        "literature_source_count": report.literature_source_count,
        "gap_count": report.gap_count,
        "source_gap_edge_count": report.source_gap_edge_count,
        "blocked_gap_count": report.blocked_gap_count,
        "actionable_gap_count": report.actionable_gap_count,
        "may_discharge_gap_count": report.may_discharge_gap_count,
        "direct_discharge_source_count": report.direct_discharge_source_count,
        "theorem_artifact_review_queue_dependency_check_count": (
            report.theorem_artifact_review_queue_dependency_check_count
        ),
        "failed_theorem_artifact_review_queue_dependency_check_count": (
            report.failed_theorem_artifact_review_queue_dependency_check_count
        ),
        "theorem_artifact_review_queue_operator_index_check_count": (
            report.theorem_artifact_review_queue_operator_index_check_count
        ),
        "failed_theorem_artifact_review_queue_operator_index_check_count": (
            report.failed_theorem_artifact_review_queue_operator_index_check_count
        ),
        "literature_gap_dependency_check_count": report.literature_gap_dependency_check_count,
        "failed_literature_gap_dependency_check_count": (
            report.failed_literature_gap_dependency_check_count
        ),
        "literature_gap_operator_index_check_count": (
            report.literature_gap_operator_index_check_count
        ),
        "failed_literature_gap_operator_index_check_count": (
            report.failed_literature_gap_operator_index_check_count
        ),
        "literature_gap_operator_dependency_check_count": (
            report.literature_gap_operator_dependency_check_count
        ),
        "failed_literature_gap_operator_dependency_check_count": (
            report.failed_literature_gap_operator_dependency_check_count
        ),
        "theorem_artifact_review_queue_dependency_consistent": (
            report.theorem_artifact_review_queue_dependency_consistent
        ),
        "theorem_artifact_review_queue_operator_index_consistent": (
            report.theorem_artifact_review_queue_operator_index_consistent
        ),
        "literature_gap_dependency_consistent": report.literature_gap_dependency_consistent,
        "literature_gap_operator_index_consistent": (
            report.literature_gap_operator_index_consistent
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
        "checks": [asdict(check) for check in report.checks],
        "source_refs": list(report.source_refs),
        "non_claims": list(report.non_claims),
        "theorem_artifact_review_queue_operator_snapshot": (
            report.theorem_artifact_review_queue_operator_snapshot
        ),
        "theorem_artifact_review_queue_snapshot": (
            report.theorem_artifact_review_queue_snapshot
        ),
        "theorem_artifact_review_queue_dependency_snapshot": (
            report.theorem_artifact_review_queue_dependency_snapshot
        ),
        "analytic_gap_snapshot": report.analytic_gap_snapshot,
        "literature_gap_matrix_snapshot": report.literature_gap_matrix_snapshot,
        "literature_gap_dependency_snapshot": report.literature_gap_dependency_snapshot,
        "literature_gap_operator_snapshot": report.literature_gap_operator_snapshot,
        "literature_gap_operator_dependency_snapshot": (
            report.literature_gap_operator_dependency_snapshot
        ),
        "docs": {
            "step_doc": (
                "docs/"
                "STEP115_LEMMA_0252_THEOREM_ARTIFACT_REVIEW_QUEUE_OPERATOR_DEPENDENCY.md"
            ),
            "theorem_artifact_review_queue_operator_doc": (
                "docs/"
                "STEP114_LEMMA_0252_THEOREM_ARTIFACT_REVIEW_QUEUE_OPERATOR_INDEX.md"
            ),
            "theorem_artifact_review_queue_doc": (
                "docs/STEP112_LEMMA_0252_THEOREM_ARTIFACT_REVIEW_QUEUE.md"
            ),
            "theorem_artifact_review_queue_dependency_doc": (
                "docs/STEP113_LEMMA_0252_THEOREM_ARTIFACT_REVIEW_QUEUE_DEPENDENCY.md"
            ),
        },
    }


def _format(text: str) -> str:
    return text.replace("|", "\\|")


def _check_rows(
    report: Lemma0252TheoremArtifactReviewQueueOperatorDependency,
) -> list[str]:
    rows = [
        "| check | expected | observed | passed | sources |",
        "|---|---|---|---|---|",
    ]
    for check in report.checks:
        sources = "<br>".join(f"`{source}`" for source in check.source_artifacts)
        rows.append(
            "| "
            f"`{check.key}` | "
            f"`{_format(check.expected)}` | "
            f"`{_format(check.observed)}` | "
            f"`{str(check.passed).lower()}` | "
            f"{sources} |"
        )
    return rows


def render_markdown(
    report: Lemma0252TheoremArtifactReviewQueueOperatorDependency,
) -> str:
    return "\n".join(
        (
            "# Lemma 0252 Theorem Artifact Review Queue Operator Dependency",
            "",
            "Generated by `track-a-regularity/evaluator/"
            "lemma_0252_theorem_artifact_review_queue_operator_dependency.py`.",
            "",
            "This read-only dependency/freshness guard keeps the Step 114 theorem-artifact",
            "review queue operator index synchronized with the Step 112 queue, Step 113",
            "queue-dependency guard, Step 102 analytic gap index, Step 108-111",
            "blocker-literature gap stack, and `papers/blockers/index.md`.",
            "",
            "It is an audit surface only; it does not interpret local literature as a",
            "theorem artifact, discharge blockers, or authorize process gates.",
            "",
            "## Summary",
            "",
            f"- lemma_id: `{report.lemma_id}`",
            f"- candidate_status: `{report.candidate_status}`",
            f"- active_candidate: `{str(report.active_candidate).lower()}`",
            f"- direct_source_report_count: `{report.direct_source_report_count}`",
            f"- source_ref_count: `{report.source_ref_count}`",
            (
                "- theorem_artifact_review_queue_operator_dependency_check_count: "
                f"`{report.theorem_artifact_review_queue_operator_dependency_check_count}`"
            ),
            (
                "- passed_theorem_artifact_review_queue_operator_dependency_check_count: "
                f"`{report.passed_theorem_artifact_review_queue_operator_dependency_check_count}`"
            ),
            (
                "- failed_theorem_artifact_review_queue_operator_dependency_check_count: "
                f"`{report.failed_theorem_artifact_review_queue_operator_dependency_check_count}`"
            ),
            (
                "- theorem_artifact_review_queue_operator_dependency_consistent: "
                f"`{str(report.theorem_artifact_review_queue_operator_dependency_consistent).lower()}`"
            ),
            f"- queue_item_count: `{report.queue_item_count}`",
            f"- direct_analytic_gap_count: `{report.direct_analytic_gap_count}`",
            f"- blocked_queue_item_count: `{report.blocked_queue_item_count}`",
            f"- actionable_queue_item_count: `{report.actionable_queue_item_count}`",
            f"- may_discharge_queue_item_count: `{report.may_discharge_queue_item_count}`",
            f"- direct_theorem_artifact_count: `{report.direct_theorem_artifact_count}`",
            f"- queue_source_edge_count: `{report.queue_source_edge_count}`",
            f"- direct_branch_source_edge_count: `{report.direct_branch_source_edge_count}`",
            f"- cross_cutting_source_edge_count: `{report.cross_cutting_source_edge_count}`",
            f"- unique_literature_source_count: `{report.unique_literature_source_count}`",
            f"- literature_source_count: `{report.literature_source_count}`",
            f"- gap_count: `{report.gap_count}`",
            f"- source_gap_edge_count: `{report.source_gap_edge_count}`",
            f"- blocked_gap_count: `{report.blocked_gap_count}`",
            f"- actionable_gap_count: `{report.actionable_gap_count}`",
            f"- may_discharge_gap_count: `{report.may_discharge_gap_count}`",
            f"- direct_discharge_source_count: `{report.direct_discharge_source_count}`",
            (
                "- theorem_artifact_review_queue_dependency_check_count: "
                f"`{report.theorem_artifact_review_queue_dependency_check_count}`"
            ),
            (
                "- failed_theorem_artifact_review_queue_dependency_check_count: "
                f"`{report.failed_theorem_artifact_review_queue_dependency_check_count}`"
            ),
            (
                "- theorem_artifact_review_queue_operator_index_check_count: "
                f"`{report.theorem_artifact_review_queue_operator_index_check_count}`"
            ),
            (
                "- failed_theorem_artifact_review_queue_operator_index_check_count: "
                f"`{report.failed_theorem_artifact_review_queue_operator_index_check_count}`"
            ),
            f"- literature_gap_dependency_check_count: `{report.literature_gap_dependency_check_count}`",
            (
                "- literature_gap_operator_index_check_count: "
                f"`{report.literature_gap_operator_index_check_count}`"
            ),
            (
                "- literature_gap_operator_dependency_check_count: "
                f"`{report.literature_gap_operator_dependency_check_count}`"
            ),
            (
                "- theorem_artifact_review_queue_dependency_consistent: "
                f"`{str(report.theorem_artifact_review_queue_dependency_consistent).lower()}`"
            ),
            (
                "- theorem_artifact_review_queue_operator_index_consistent: "
                f"`{str(report.theorem_artifact_review_queue_operator_index_consistent).lower()}`"
            ),
            (
                "- literature_gap_dependency_consistent: "
                f"`{str(report.literature_gap_dependency_consistent).lower()}`"
            ),
            (
                "- literature_gap_operator_index_consistent: "
                f"`{str(report.literature_gap_operator_index_consistent).lower()}`"
            ),
            (
                "- literature_gap_operator_dependency_consistent: "
                f"`{str(report.literature_gap_operator_dependency_consistent).lower()}`"
            ),
            f"- analytic_gap_stack_consistent: `{str(report.analytic_gap_stack_consistent).lower()}`",
            f"- operator_stack_consistent: `{str(report.operator_stack_consistent).lower()}`",
            f"- process_gate_open_authorized: `{str(report.process_gate_open_authorized).lower()}`",
            f"- blocker_state_changed: `{str(report.blocker_state_changed).lower()}`",
            f"- candidate_emission_authorized: `{str(report.candidate_emission_authorized).lower()}`",
            f"- missing_source_count: `{report.missing_source_count}`",
            f"- issues: `{', '.join(report.issues) or 'none'}`",
            "",
            "## Dependency Checks",
            "",
            *_check_rows(report),
            "",
            "## Non-Claims",
            "",
            *(f"- `{item}`" for item in report.non_claims),
            "",
        )
    )


def render_json(report: Lemma0252TheoremArtifactReviewQueueOperatorDependency) -> str:
    return json.dumps(
        theorem_artifact_review_queue_operator_dependency_to_dict(report),
        indent=2,
        sort_keys=True,
    ) + "\n"


def render_output(
    report: Lemma0252TheoremArtifactReviewQueueOperatorDependency,
    output_format: str,
) -> str:
    if output_format == "markdown":
        return render_markdown(report)
    if output_format == "json":
        return render_json(report)
    raise ValueError(
        f"unknown theorem artifact review queue operator dependency format: {output_format}"
    )


def write_output(
    output: Path,
    report: Lemma0252TheoremArtifactReviewQueueOperatorDependency,
    output_format: str,
) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_output(report, output_format), encoding="utf-8")
    return output


def check_output(
    output: Path,
    report: Lemma0252TheoremArtifactReviewQueueOperatorDependency,
    output_format: str,
) -> tuple[bool, str]:
    expected = render_output(report, output_format)
    if not output.exists():
        return False, (
            "missing lemma_0252 theorem artifact review queue operator dependency: "
            f"{output}"
        )
    current = output.read_text(encoding="utf-8")
    if current != expected:
        return False, (
            "stale lemma_0252 theorem artifact review queue operator dependency: "
            f"{output}"
        )
    return (
        True,
        f"fresh lemma_0252 theorem artifact review queue operator dependency: {output}",
    )


def check_consistent(
    report: Lemma0252TheoremArtifactReviewQueueOperatorDependency,
) -> tuple[bool, str]:
    if not report.theorem_artifact_review_queue_operator_dependency_consistent:
        return (
            False,
            "lemma_0252 theorem artifact review queue operator dependency inconsistent: "
            + ", ".join(report.issues),
        )
    return (
        True,
        "lemma_0252 theorem artifact review queue operator dependency is consistent",
    )


def check_sources(
    report: Lemma0252TheoremArtifactReviewQueueOperatorDependency,
) -> tuple[bool, str]:
    if report.missing_source_count:
        return (
            False,
            "missing lemma_0252 theorem artifact review queue operator dependency sources: "
            + ", ".join(report.missing_sources),
        )
    return (
        True,
        "all lemma_0252 theorem artifact review queue operator dependency sources exist",
    )


def check_blocked(
    report: Lemma0252TheoremArtifactReviewQueueOperatorDependency,
) -> tuple[bool, str]:
    if report.process_gate_open_authorized:
        return False, "process gate open became authorized"
    if report.blocker_state_changed:
        return False, "theorem artifact review queue operator dependency changed blocker state"
    if report.candidate_emission_authorized:
        return False, "theorem artifact review queue operator dependency authorized emission"
    if report.actionable_queue_item_count:
        return False, "theorem artifact review queue operator dependency found actionable items"
    if report.may_discharge_queue_item_count:
        return False, "theorem artifact review queue operator dependency found discharge items"
    if report.direct_theorem_artifact_count:
        return False, "theorem artifact review queue operator dependency found theorem artifacts"
    if report.actionable_gap_count:
        return False, "theorem artifact review queue operator dependency found actionable gaps"
    if report.may_discharge_gap_count:
        return False, "theorem artifact review queue operator dependency found discharge gaps"
    if report.direct_discharge_source_count:
        return False, "theorem artifact review queue operator dependency found discharge sources"
    return True, "lemma_0252 theorem artifact review queue operator dependency remains blocked"


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render lemma_0252 theorem-artifact review queue operator dependency report.",
    )
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--check-output", action="store_true")
    parser.add_argument("--require-sources-exist", action="store_true")
    parser.add_argument("--require-consistent", action="store_true")
    parser.add_argument("--require-blocked", action="store_true")
    return parser.parse_args(argv)


def _default_output(output_format: str) -> Path:
    if output_format == "json":
        return DEFAULT_JSON_OUTPUT
    return DEFAULT_MARKDOWN_OUTPUT


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    report = build_theorem_artifact_review_queue_operator_dependency()
    output = args.output or _default_output(args.format)

    if args.check_output:
        ok, message = check_output(output, report, args.format)
        print(message)
        if not ok:
            return 1
    else:
        write_output(output, report, args.format)
        print(f"wrote {output}")

    if args.require_sources_exist:
        ok, message = check_sources(report)
        print(message)
        if not ok:
            return 1
    if args.require_consistent:
        ok, message = check_consistent(report)
        print(message)
        if not ok:
            return 1
    if args.require_blocked:
        ok, message = check_blocked(report)
        print(message)
        if not ok:
            return 1

    print(
        "lemma_0252 theorem artifact review queue operator dependency: "
        f"direct_source_report_count: {report.direct_source_report_count}, "
        f"source_ref_count: {report.source_ref_count}, "
        "theorem_artifact_review_queue_operator_dependency_check_count: "
        f"{report.theorem_artifact_review_queue_operator_dependency_check_count}, "
        "failed_theorem_artifact_review_queue_operator_dependency_check_count: "
        f"{report.failed_theorem_artifact_review_queue_operator_dependency_check_count}, "
        f"missing_source_count: {report.missing_source_count}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
