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
from promotion_gate_analytic_discharge_gap_index import (
    DEFAULT_JSON_OUTPUT as DEFAULT_ANALYTIC_GAP_JSON,
    DEFAULT_MARKDOWN_OUTPUT as DEFAULT_ANALYTIC_GAP_MARKDOWN,
)


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REPORT_DIR = ROOT / "track-a-regularity/reports"
DEFAULT_MARKDOWN_OUTPUT = (
    DEFAULT_REPORT_DIR / "lemma_0252_theorem_artifact_review_queue_dependency.md"
)
DEFAULT_JSON_OUTPUT = (
    DEFAULT_REPORT_DIR / "lemma_0252_theorem_artifact_review_queue_dependency.json"
)
DEFAULT_PAPERS_INDEX = ROOT / "papers/blockers/index.md"

DIRECT_ANALYTIC_GAP_IDS = ("gap_002", "gap_003", "gap_004")
QUEUE_STATUS = "blocked_waiting_for_real_theorem_artifact"

NON_CLAIMS = (
    "read_only_theorem_artifact_queue_dependency_guard",
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
class TheoremArtifactReviewQueueDependencyCheck:
    key: str
    expected: str
    observed: str
    passed: bool
    source_artifacts: tuple[str, ...]


@dataclass(frozen=True)
class Lemma0252TheoremArtifactReviewQueueDependency:
    schema_version: int
    lemma_id: str
    candidate_status: str
    active_candidate: bool
    theorem_artifact_review_queue_markdown: str
    theorem_artifact_review_queue_json: str
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
    theorem_artifact_review_queue_dependency_check_count: int
    passed_theorem_artifact_review_queue_dependency_check_count: int
    failed_theorem_artifact_review_queue_dependency_check_count: int
    theorem_artifact_review_queue_dependency_consistent: bool
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
    literature_gap_dependency_check_count: int
    failed_literature_gap_dependency_check_count: int
    literature_gap_operator_index_check_count: int
    failed_literature_gap_operator_index_check_count: int
    literature_gap_operator_dependency_check_count: int
    failed_literature_gap_operator_dependency_check_count: int
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
    checks: tuple[TheoremArtifactReviewQueueDependencyCheck, ...]
    source_refs: tuple[str, ...]
    non_claims: tuple[str, ...]
    theorem_artifact_review_queue_snapshot: dict[str, object]
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


def _check(
    *,
    key: str,
    expected: object,
    observed: object,
    source_artifacts: tuple[str, ...],
) -> TheoremArtifactReviewQueueDependencyCheck:
    return TheoremArtifactReviewQueueDependencyCheck(
        key=key,
        expected=str(expected),
        observed=str(observed),
        passed=expected == observed,
        source_artifacts=source_artifacts,
    )


def _relative(path: Path) -> str:
    return str(path.relative_to(ROOT))


def _missing_sources(source_refs: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(source for source in source_refs if not (ROOT / source).exists())


def _direct_source_reports() -> tuple[str, ...]:
    return (
        "track-a-regularity/reports/lemma_0252_theorem_artifact_review_queue.md",
        "track-a-regularity/reports/lemma_0252_theorem_artifact_review_queue.json",
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


def _queue_items_by_gap(queue: dict[str, object]) -> dict[str, dict[str, object]]:
    return _rows_by_key(queue.get("queue_items", ()), "gap_id")


def _gap_rows_by_id(gap_index: dict[str, object]) -> dict[str, dict[str, object]]:
    return _rows_by_key(gap_index.get("gaps", ()), "gap_id")


def _coverage_rows_by_id(matrix: dict[str, object]) -> dict[str, dict[str, object]]:
    return _rows_by_key(matrix.get("gap_coverages", ()), "gap_id")


def _source_paths_for_item(item: dict[str, object]) -> tuple[str, ...]:
    return tuple(str(path) for path in item.get("source_paths", ()))


def _source_ids_for_item(item: dict[str, object]) -> tuple[str, ...]:
    return tuple(str(source_id) for source_id in item.get("source_ids", ()))


def _direct_branch_source_count(item: dict[str, object]) -> int:
    review_sources = item.get("review_sources", ())
    if not isinstance(review_sources, list):
        return 0
    return sum(
        1
        for source in review_sources
        if isinstance(source, dict) and bool(source.get("direct_branch_support"))
    )


def _direct_discharge_count(item: dict[str, object]) -> int:
    review_sources = item.get("review_sources", ())
    if not isinstance(review_sources, list):
        return 0
    return sum(
        1
        for source in review_sources
        if isinstance(source, dict) and bool(source.get("direct_discharge"))
    )


def _review_source_exists_count(item: dict[str, object]) -> int:
    review_sources = item.get("review_sources", ())
    if not isinstance(review_sources, list):
        return 0
    return sum(
        1
        for source in review_sources
        if isinstance(source, dict)
        and bool(source.get("source_exists"))
        and (ROOT / str(source.get("relative_path"))).exists()
    )


def build_theorem_artifact_review_queue_dependency(
    *,
    theorem_artifact_review_queue_json: Path = DEFAULT_QUEUE_JSON,
    analytic_gap_json: Path = DEFAULT_ANALYTIC_GAP_JSON,
    literature_gap_matrix_json: Path = DEFAULT_GAP_MATRIX_JSON,
    literature_gap_dependency_json: Path = DEFAULT_GAP_DEPENDENCY_JSON,
    literature_gap_operator_json: Path = DEFAULT_GAP_OPERATOR_JSON,
    literature_gap_operator_dependency_json: Path = DEFAULT_GAP_OPERATOR_DEPENDENCY_JSON,
    papers_blockers_index: Path = DEFAULT_PAPERS_INDEX,
) -> Lemma0252TheoremArtifactReviewQueueDependency:
    queue = _load_json(theorem_artifact_review_queue_json)
    analytic_gap = _load_json(analytic_gap_json)
    matrix = _load_json(literature_gap_matrix_json)
    gap_dependency = _load_json(literature_gap_dependency_json)
    operator = _load_json(literature_gap_operator_json)
    operator_dependency = _load_json(literature_gap_operator_dependency_json)

    queue_items_by_gap = _queue_items_by_gap(queue)
    gaps_by_id = _gap_rows_by_id(analytic_gap)
    coverages_by_id = _coverage_rows_by_id(matrix)

    source_refs = tuple(
        dict.fromkeys(
            _direct_sources()
            + tuple(str(item) for item in queue.get("source_refs", ()))
            + tuple(str(item) for item in analytic_gap.get("source_refs", ()))
            + tuple(str(item) for item in matrix.get("source_refs", ()))
            + tuple(str(item) for item in gap_dependency.get("source_refs", ()))
            + tuple(str(item) for item in operator.get("source_refs", ()))
            + tuple(str(item) for item in operator_dependency.get("source_refs", ()))
        )
    )
    missing_sources = _missing_sources(source_refs)

    queue_source = (
        "track-a-regularity/reports/lemma_0252_theorem_artifact_review_queue.md",
        "track-a-regularity/reports/lemma_0252_theorem_artifact_review_queue.json",
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
    operator_source = (
        "track-a-regularity/reports/lemma_0252_blocker_literature_gap_operator_index.md",
        "track-a-regularity/reports/lemma_0252_blocker_literature_gap_operator_index.json",
    )
    operator_dependency_source = (
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

    queue_gap_ids = tuple(
        gap_id for gap_id in DIRECT_ANALYTIC_GAP_IDS if gap_id in queue_items_by_gap
    )
    source_path_count_sum = sum(
        len(_source_paths_for_item(queue_items_by_gap[gap_id]))
        for gap_id in queue_gap_ids
    )
    direct_branch_source_count_sum = sum(
        _direct_branch_source_count(queue_items_by_gap[gap_id])
        for gap_id in queue_gap_ids
    )
    direct_discharge_count_sum = sum(
        _direct_discharge_count(queue_items_by_gap[gap_id]) for gap_id in queue_gap_ids
    )
    unique_literature_source_ids = tuple(
        dict.fromkeys(
            source_id
            for gap_id in queue_gap_ids
            for source_id in _source_ids_for_item(queue_items_by_gap[gap_id])
        )
    )

    checks: list[TheoremArtifactReviewQueueDependencyCheck] = [
        _check(
            key="queue.lemma_id.matches_analytic_gap",
            expected=analytic_gap.get("lemma_id"),
            observed=queue.get("lemma_id"),
            source_artifacts=queue_source + analytic_source,
        ),
        _check(
            key="queue.lemma_id.matches_literature_gap_matrix",
            expected=matrix.get("lemma_id"),
            observed=queue.get("lemma_id"),
            source_artifacts=queue_source + matrix_source,
        ),
        _check(
            key="queue.lemma_id.matches_literature_gap_dependency",
            expected=gap_dependency.get("lemma_id"),
            observed=queue.get("lemma_id"),
            source_artifacts=queue_source + gap_dependency_source,
        ),
        _check(
            key="queue.lemma_id.matches_literature_gap_operator",
            expected=operator.get("lemma_id"),
            observed=queue.get("lemma_id"),
            source_artifacts=queue_source + operator_source,
        ),
        _check(
            key="queue.lemma_id.matches_literature_gap_operator_dependency",
            expected=operator_dependency.get("lemma_id"),
            observed=queue.get("lemma_id"),
            source_artifacts=queue_source + operator_dependency_source,
        ),
        _check(
            key="queue.candidate_status.matches_analytic_gap",
            expected=analytic_gap.get("candidate_status"),
            observed=queue.get("candidate_status"),
            source_artifacts=queue_source + analytic_source,
        ),
        _check(
            key="queue.active_candidate.matches_analytic_gap",
            expected=analytic_gap.get("active_candidate"),
            observed=queue.get("active_candidate"),
            source_artifacts=queue_source + analytic_source,
        ),
        _check(
            key="queue_item_count.expected_three",
            expected=3,
            observed=queue.get("queue_item_count"),
            source_artifacts=queue_source,
        ),
        _check(
            key="direct_analytic_gap_count.expected_three",
            expected=len(DIRECT_ANALYTIC_GAP_IDS),
            observed=queue.get("direct_analytic_gap_count"),
            source_artifacts=queue_source,
        ),
        _check(
            key="queue_gap_ids.expected_direct_analytic_gaps",
            expected=DIRECT_ANALYTIC_GAP_IDS,
            observed=queue_gap_ids,
            source_artifacts=queue_source,
        ),
        _check(
            key="direct_gap_ids.present_in_analytic_gap_index",
            expected=DIRECT_ANALYTIC_GAP_IDS,
            observed=tuple(gap_id for gap_id in DIRECT_ANALYTIC_GAP_IDS if gap_id in gaps_by_id),
            source_artifacts=analytic_source,
        ),
        _check(
            key="direct_gap_ids.present_in_literature_gap_matrix",
            expected=DIRECT_ANALYTIC_GAP_IDS,
            observed=tuple(
                gap_id for gap_id in DIRECT_ANALYTIC_GAP_IDS if gap_id in coverages_by_id
            ),
            source_artifacts=matrix_source,
        ),
        _check(
            key="queue_source_edge_count.matches_queue_items",
            expected=source_path_count_sum,
            observed=queue.get("queue_source_edge_count"),
            source_artifacts=queue_source,
        ),
        _check(
            key="direct_branch_source_edge_count.matches_queue_items",
            expected=direct_branch_source_count_sum,
            observed=queue.get("direct_branch_source_edge_count"),
            source_artifacts=queue_source,
        ),
        _check(
            key="cross_cutting_source_edge_count.matches_queue_items",
            expected=source_path_count_sum - direct_branch_source_count_sum,
            observed=queue.get("cross_cutting_source_edge_count"),
            source_artifacts=queue_source,
        ),
        _check(
            key="source_edge_partition.matches_queue_source_edge_count",
            expected=queue.get("queue_source_edge_count"),
            observed=(
                int(queue.get("direct_branch_source_edge_count", 0))
                + int(queue.get("cross_cutting_source_edge_count", 0))
            ),
            source_artifacts=queue_source,
        ),
        _check(
            key="unique_literature_source_count.matches_queue_items",
            expected=len(unique_literature_source_ids),
            observed=queue.get("unique_literature_source_count"),
            source_artifacts=queue_source,
        ),
        _check(
            key="literature_source_count.matches_operator_dependency",
            expected=operator_dependency.get("literature_source_count"),
            observed=queue.get("literature_source_count"),
            source_artifacts=queue_source + operator_dependency_source,
        ),
        _check(
            key="gap_count.matches_analytic_gap_index",
            expected=analytic_gap.get("gap_count"),
            observed=queue.get("gap_count"),
            source_artifacts=queue_source + analytic_source,
        ),
        _check(
            key="source_gap_edge_count.matches_matrix",
            expected=matrix.get("source_gap_edge_count"),
            observed=queue.get("source_gap_edge_count"),
            source_artifacts=queue_source + matrix_source,
        ),
        _check(
            key="blocked_gap_count.matches_analytic_gap_index",
            expected=analytic_gap.get("blocked_gap_count"),
            observed=queue.get("blocked_gap_count"),
            source_artifacts=queue_source + analytic_source,
        ),
        _check(
            key="blocked_gap_count.matches_gap_count",
            expected=queue.get("gap_count"),
            observed=queue.get("blocked_gap_count"),
            source_artifacts=queue_source,
        ),
        _check(
            key="actionable_gap_count.remains_zero",
            expected=0,
            observed=queue.get("actionable_gap_count"),
            source_artifacts=queue_source + analytic_source,
        ),
        _check(
            key="may_discharge_gap_count.remains_zero",
            expected=0,
            observed=queue.get("may_discharge_gap_count"),
            source_artifacts=queue_source + analytic_source,
        ),
        _check(
            key="direct_discharge_source_count.remains_zero",
            expected=0,
            observed=queue.get("direct_discharge_source_count"),
            source_artifacts=queue_source + matrix_source,
        ),
        _check(
            key="all_queue_items.blocked",
            expected=queue.get("queue_item_count"),
            observed=queue.get("blocked_queue_item_count"),
            source_artifacts=queue_source,
        ),
        _check(
            key="actionable_queue_item_count.remains_zero",
            expected=0,
            observed=queue.get("actionable_queue_item_count"),
            source_artifacts=queue_source,
        ),
        _check(
            key="may_discharge_queue_item_count.remains_zero",
            expected=0,
            observed=queue.get("may_discharge_queue_item_count"),
            source_artifacts=queue_source,
        ),
        _check(
            key="direct_theorem_artifact_count.remains_zero",
            expected=0,
            observed=queue.get("direct_theorem_artifact_count"),
            source_artifacts=queue_source,
        ),
        _check(
            key="queue_review_sources_not_direct_discharge",
            expected=0,
            observed=direct_discharge_count_sum,
            source_artifacts=queue_source,
        ),
        _check(
            key="operator_dependency.check_count.matches_queue",
            expected=operator_dependency.get("literature_gap_operator_dependency_check_count"),
            observed=queue.get("literature_gap_operator_dependency_check_count"),
            source_artifacts=queue_source + operator_dependency_source,
        ),
        _check(
            key="operator_dependency.failed_checks.matches_queue",
            expected=operator_dependency.get(
                "failed_literature_gap_operator_dependency_check_count"
            ),
            observed=queue.get("failed_literature_gap_operator_dependency_check_count"),
            source_artifacts=queue_source + operator_dependency_source,
        ),
        _check(
            key="operator_dependency.consistent.matches_queue",
            expected=operator_dependency.get("literature_gap_operator_dependency_consistent"),
            observed=queue.get("literature_gap_operator_dependency_consistent"),
            source_artifacts=queue_source + operator_dependency_source,
        ),
        _check(
            key="gap_dependency.consistent.true",
            expected=True,
            observed=gap_dependency.get("literature_gap_dependency_consistent"),
            source_artifacts=gap_dependency_source,
        ),
        _check(
            key="operator.index_consistent.true",
            expected=True,
            observed=operator.get("literature_gap_operator_index_consistent"),
            source_artifacts=operator_source,
        ),
        _check(
            key="matrix.gap_stack_consistent.true",
            expected=True,
            observed=matrix.get("gap_stack_consistent"),
            source_artifacts=matrix_source,
        ),
        _check(
            key="queue.analytic_gap_stack_consistent.true",
            expected=True,
            observed=queue.get("analytic_gap_stack_consistent"),
            source_artifacts=queue_source,
        ),
        _check(
            key="queue.operator_stack_consistent.true",
            expected=True,
            observed=queue.get("operator_stack_consistent"),
            source_artifacts=queue_source,
        ),
        _check(
            key="source_reports.issues.all_empty",
            expected=((), (), (), (), (), ()),
            observed=(
                tuple(queue.get("issues", ())),
                tuple(analytic_gap.get("issues", ())),
                tuple(matrix.get("issues", ())),
                tuple(gap_dependency.get("issues", ())),
                tuple(operator.get("issues", ())),
                tuple(operator_dependency.get("issues", ())),
            ),
            source_artifacts=_direct_source_reports(),
        ),
        _check(
            key="all.process_gate_open_authorized.false",
            expected=(False, False, False, False, False, False),
            observed=(
                queue.get("process_gate_open_authorized"),
                analytic_gap.get("process_gate_open_authorized"),
                matrix.get("process_gate_open_authorized"),
                gap_dependency.get("process_gate_open_authorized"),
                operator.get("process_gate_open_authorized"),
                operator_dependency.get("process_gate_open_authorized"),
            ),
            source_artifacts=_direct_source_reports(),
        ),
        _check(
            key="all.blocker_state_changed.false",
            expected=(False, False, False, False, False, False),
            observed=(
                queue.get("blocker_state_changed"),
                analytic_gap.get("blocker_state_changed"),
                matrix.get("blocker_state_changed"),
                gap_dependency.get("blocker_state_changed"),
                operator.get("blocker_state_changed"),
                operator_dependency.get("blocker_state_changed"),
            ),
            source_artifacts=_direct_source_reports(),
        ),
        _check(
            key="all.candidate_emission_authorized.false",
            expected=(False, False, False, False, False, False),
            observed=(
                queue.get("candidate_emission_authorized"),
                analytic_gap.get("candidate_emission_authorized"),
                matrix.get("candidate_emission_authorized"),
                gap_dependency.get("candidate_emission_authorized"),
                operator.get("candidate_emission_authorized"),
                operator_dependency.get("candidate_emission_authorized"),
            ),
            source_artifacts=_direct_source_reports(),
        ),
        _check(
            key="candidate_status.remains_needs_review",
            expected="needs_review",
            observed=queue.get("candidate_status"),
            source_artifacts=queue_source,
        ),
        _check(
            key="active_candidate.remains_false",
            expected=False,
            observed=queue.get("active_candidate"),
            source_artifacts=queue_source,
        ),
        _check(
            key="source_refs.missing_count.remains_zero",
            expected=0,
            observed=len(missing_sources),
            source_artifacts=source_refs,
        ),
        _check(
            key="source_refs.include_papers_blockers_index",
            expected=True,
            observed="papers/blockers/index.md" in source_refs and papers_blockers_index.exists(),
            source_artifacts=papers_source,
        ),
        _check(
            key="source_refs.include_theorem_artifact_queue_reports",
            expected=queue_source,
            observed=tuple(source for source in queue_source if source in source_refs),
            source_artifacts=queue_source,
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
            expected=operator_source,
            observed=tuple(source for source in operator_source if source in source_refs),
            source_artifacts=operator_source,
        ),
        _check(
            key="source_refs.include_literature_gap_operator_dependency_reports",
            expected=operator_dependency_source,
            observed=tuple(source for source in operator_dependency_source if source in source_refs),
            source_artifacts=operator_dependency_source,
        ),
    ]

    for gap_id in DIRECT_ANALYTIC_GAP_IDS:
        item = queue_items_by_gap[gap_id]
        gap = gaps_by_id[gap_id]
        coverage = coverages_by_id[gap_id]
        checks.extend(
            [
                _check(
                    key=f"{gap_id}.source_branch.matches_gap_index",
                    expected=gap.get("source_branch"),
                    observed=item.get("source_branch"),
                    source_artifacts=queue_source + analytic_source,
                ),
                _check(
                    key=f"{gap_id}.artifact_type.matches_gap_index",
                    expected=gap.get("required_artifact_type"),
                    observed=item.get("required_artifact_type"),
                    source_artifacts=queue_source + analytic_source,
                ),
                _check(
                    key=f"{gap_id}.source_count.matches_matrix_coverage",
                    expected=coverage.get("literature_source_count"),
                    observed=item.get("literature_source_count"),
                    source_artifacts=queue_source + matrix_source,
                ),
                _check(
                    key=f"{gap_id}.direct_branch_source_count.matches_matrix_coverage",
                    expected=coverage.get("direct_branch_source_count"),
                    observed=item.get("direct_branch_source_count"),
                    source_artifacts=queue_source + matrix_source,
                ),
                _check(
                    key=f"{gap_id}.review_sources_exist",
                    expected=item.get("literature_source_count"),
                    observed=_review_source_exists_count(item),
                    source_artifacts=tuple(_source_paths_for_item(item)),
                ),
                _check(
                    key=f"{gap_id}.review_sources_not_direct_discharge",
                    expected=0,
                    observed=_direct_discharge_count(item),
                    source_artifacts=tuple(_source_paths_for_item(item)),
                ),
            ]
        )

    issues = tuple(check.key for check in checks if not check.passed)

    reports = (queue, analytic_gap, matrix, gap_dependency, operator, operator_dependency)
    process_gate_open_authorized = any(
        bool(report.get("process_gate_open_authorized")) for report in reports
    )
    blocker_state_changed = any(bool(report.get("blocker_state_changed")) for report in reports)
    candidate_emission_authorized = any(
        bool(report.get("candidate_emission_authorized")) for report in reports
    )

    return Lemma0252TheoremArtifactReviewQueueDependency(
        schema_version=1,
        lemma_id=str(queue.get("lemma_id")),
        candidate_status=str(queue.get("candidate_status")),
        active_candidate=bool(queue.get("active_candidate")),
        theorem_artifact_review_queue_markdown=str(DEFAULT_QUEUE_MARKDOWN),
        theorem_artifact_review_queue_json=str(DEFAULT_QUEUE_JSON),
        analytic_gap_markdown=str(DEFAULT_ANALYTIC_GAP_MARKDOWN),
        analytic_gap_json=str(DEFAULT_ANALYTIC_GAP_JSON),
        literature_gap_matrix_markdown=str(DEFAULT_GAP_MATRIX_MARKDOWN),
        literature_gap_matrix_json=str(DEFAULT_GAP_MATRIX_JSON),
        literature_gap_dependency_markdown=str(DEFAULT_GAP_DEPENDENCY_MARKDOWN),
        literature_gap_dependency_json=str(DEFAULT_GAP_DEPENDENCY_JSON),
        literature_gap_operator_markdown=str(DEFAULT_GAP_OPERATOR_MARKDOWN),
        literature_gap_operator_json=str(DEFAULT_GAP_OPERATOR_JSON),
        literature_gap_operator_dependency_markdown=str(
            DEFAULT_GAP_OPERATOR_DEPENDENCY_MARKDOWN
        ),
        literature_gap_operator_dependency_json=str(DEFAULT_GAP_OPERATOR_DEPENDENCY_JSON),
        papers_blockers_index=_relative(papers_blockers_index),
        direct_source_report_count=len(_direct_source_reports()),
        source_ref_count=len(source_refs),
        theorem_artifact_review_queue_dependency_check_count=len(checks),
        passed_theorem_artifact_review_queue_dependency_check_count=sum(
            1 for check in checks if check.passed
        ),
        failed_theorem_artifact_review_queue_dependency_check_count=len(issues),
        theorem_artifact_review_queue_dependency_consistent=not issues
        and not missing_sources,
        queue_item_count=int(queue.get("queue_item_count", 0)),
        direct_analytic_gap_count=int(queue.get("direct_analytic_gap_count", 0)),
        blocked_queue_item_count=int(queue.get("blocked_queue_item_count", 0)),
        actionable_queue_item_count=int(queue.get("actionable_queue_item_count", 0)),
        may_discharge_queue_item_count=int(
            queue.get("may_discharge_queue_item_count", 0)
        ),
        direct_theorem_artifact_count=int(queue.get("direct_theorem_artifact_count", 0)),
        queue_source_edge_count=int(queue.get("queue_source_edge_count", 0)),
        direct_branch_source_edge_count=int(
            queue.get("direct_branch_source_edge_count", 0)
        ),
        cross_cutting_source_edge_count=int(
            queue.get("cross_cutting_source_edge_count", 0)
        ),
        unique_literature_source_count=int(
            queue.get("unique_literature_source_count", 0)
        ),
        literature_source_count=int(queue.get("literature_source_count", 0)),
        gap_count=int(queue.get("gap_count", 0)),
        source_gap_edge_count=int(queue.get("source_gap_edge_count", 0)),
        blocked_gap_count=int(queue.get("blocked_gap_count", 0)),
        actionable_gap_count=int(queue.get("actionable_gap_count", 0)),
        may_discharge_gap_count=int(queue.get("may_discharge_gap_count", 0)),
        direct_discharge_source_count=int(queue.get("direct_discharge_source_count", 0)),
        literature_gap_dependency_check_count=int(
            gap_dependency.get("literature_gap_dependency_check_count", 0)
        ),
        failed_literature_gap_dependency_check_count=int(
            gap_dependency.get("failed_literature_gap_dependency_check_count", 0)
        ),
        literature_gap_operator_index_check_count=int(
            operator.get("literature_gap_operator_index_check_count", 0)
        ),
        failed_literature_gap_operator_index_check_count=int(
            operator.get("failed_literature_gap_operator_index_check_count", 0)
        ),
        literature_gap_operator_dependency_check_count=int(
            operator_dependency.get("literature_gap_operator_dependency_check_count", 0)
        ),
        failed_literature_gap_operator_dependency_check_count=int(
            operator_dependency.get(
                "failed_literature_gap_operator_dependency_check_count", 0
            )
        ),
        literature_gap_dependency_consistent=bool(
            gap_dependency.get("literature_gap_dependency_consistent")
        ),
        literature_gap_operator_index_consistent=bool(
            operator.get("literature_gap_operator_index_consistent")
        ),
        literature_gap_operator_dependency_consistent=bool(
            operator_dependency.get("literature_gap_operator_dependency_consistent")
        ),
        analytic_gap_stack_consistent=bool(queue.get("analytic_gap_stack_consistent")),
        operator_stack_consistent=bool(queue.get("operator_stack_consistent")),
        process_gate_open_authorized=process_gate_open_authorized,
        blocker_state_changed=blocker_state_changed,
        candidate_emission_authorized=candidate_emission_authorized,
        missing_source_count=len(missing_sources),
        missing_sources=missing_sources,
        issues=issues,
        checks=tuple(checks),
        source_refs=source_refs,
        non_claims=NON_CLAIMS,
        theorem_artifact_review_queue_snapshot=queue,
        analytic_gap_snapshot=analytic_gap,
        literature_gap_matrix_snapshot=matrix,
        literature_gap_dependency_snapshot=gap_dependency,
        literature_gap_operator_snapshot=operator,
        literature_gap_operator_dependency_snapshot=operator_dependency,
    )


def theorem_artifact_review_queue_dependency_to_dict(
    report: Lemma0252TheoremArtifactReviewQueueDependency,
) -> dict[str, object]:
    return {
        "schema_version": report.schema_version,
        "lemma_id": report.lemma_id,
        "candidate_status": report.candidate_status,
        "active_candidate": report.active_candidate,
        "theorem_artifact_review_queue_markdown": (
            report.theorem_artifact_review_queue_markdown
        ),
        "theorem_artifact_review_queue_json": (
            report.theorem_artifact_review_queue_json
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
        "theorem_artifact_review_queue_dependency_check_count": (
            report.theorem_artifact_review_queue_dependency_check_count
        ),
        "passed_theorem_artifact_review_queue_dependency_check_count": (
            report.passed_theorem_artifact_review_queue_dependency_check_count
        ),
        "failed_theorem_artifact_review_queue_dependency_check_count": (
            report.failed_theorem_artifact_review_queue_dependency_check_count
        ),
        "theorem_artifact_review_queue_dependency_consistent": (
            report.theorem_artifact_review_queue_dependency_consistent
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
        "literature_gap_dependency_check_count": (
            report.literature_gap_dependency_check_count
        ),
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
        "literature_gap_dependency_consistent": (
            report.literature_gap_dependency_consistent
        ),
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
        "theorem_artifact_review_queue_snapshot": (
            report.theorem_artifact_review_queue_snapshot
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
                "docs/STEP113_LEMMA_0252_THEOREM_ARTIFACT_REVIEW_QUEUE_DEPENDENCY.md"
            ),
            "theorem_artifact_review_queue_doc": (
                "docs/STEP112_LEMMA_0252_THEOREM_ARTIFACT_REVIEW_QUEUE.md"
            ),
            "literature_gap_operator_dependency_doc": (
                "docs/STEP111_LEMMA_0252_BLOCKER_LITERATURE_GAP_OPERATOR_DEPENDENCY.md"
            ),
            "literature_gap_operator_doc": (
                "docs/STEP110_LEMMA_0252_BLOCKER_LITERATURE_GAP_OPERATOR_INDEX.md"
            ),
            "literature_gap_dependency_doc": (
                "docs/STEP109_LEMMA_0252_BLOCKER_LITERATURE_GAP_DEPENDENCY.md"
            ),
            "literature_gap_matrix_doc": (
                "docs/STEP108_LEMMA_0252_BLOCKER_LITERATURE_GAP_MATRIX.md"
            ),
            "analytic_gap_doc": (
                "docs/STEP102_PROMOTION_GATE_ANALYTIC_DISCHARGE_GAP_INDEX.md"
            ),
        },
    }


def _format(text: str) -> str:
    return text.replace("|", "\\|")


def _summary_lines(
    report: Lemma0252TheoremArtifactReviewQueueDependency,
) -> tuple[str, ...]:
    keys = (
        "lemma_id",
        "candidate_status",
        "active_candidate",
        "direct_source_report_count",
        "source_ref_count",
        "theorem_artifact_review_queue_dependency_check_count",
        "passed_theorem_artifact_review_queue_dependency_check_count",
        "failed_theorem_artifact_review_queue_dependency_check_count",
        "theorem_artifact_review_queue_dependency_consistent",
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
        "literature_source_count",
        "gap_count",
        "source_gap_edge_count",
        "blocked_gap_count",
        "actionable_gap_count",
        "may_discharge_gap_count",
        "direct_discharge_source_count",
        "literature_gap_dependency_check_count",
        "failed_literature_gap_dependency_check_count",
        "literature_gap_operator_index_check_count",
        "failed_literature_gap_operator_index_check_count",
        "literature_gap_operator_dependency_check_count",
        "failed_literature_gap_operator_dependency_check_count",
        "literature_gap_dependency_consistent",
        "literature_gap_operator_index_consistent",
        "literature_gap_operator_dependency_consistent",
        "analytic_gap_stack_consistent",
        "operator_stack_consistent",
        "process_gate_open_authorized",
        "blocker_state_changed",
        "candidate_emission_authorized",
        "missing_source_count",
    )
    data = theorem_artifact_review_queue_dependency_to_dict(report)
    return tuple(f"- {key}: `{str(data[key]).lower()}`" for key in keys)


def _source_report_lines(
    report: Lemma0252TheoremArtifactReviewQueueDependency,
) -> tuple[str, ...]:
    return (
        f"- theorem_artifact_review_queue_markdown: `{report.theorem_artifact_review_queue_markdown}`",
        f"- theorem_artifact_review_queue_json: `{report.theorem_artifact_review_queue_json}`",
        f"- analytic_gap_markdown: `{report.analytic_gap_markdown}`",
        f"- analytic_gap_json: `{report.analytic_gap_json}`",
        f"- literature_gap_matrix_markdown: `{report.literature_gap_matrix_markdown}`",
        f"- literature_gap_matrix_json: `{report.literature_gap_matrix_json}`",
        f"- literature_gap_dependency_markdown: `{report.literature_gap_dependency_markdown}`",
        f"- literature_gap_dependency_json: `{report.literature_gap_dependency_json}`",
        f"- literature_gap_operator_markdown: `{report.literature_gap_operator_markdown}`",
        f"- literature_gap_operator_json: `{report.literature_gap_operator_json}`",
        (
            "- literature_gap_operator_dependency_markdown: "
            f"`{report.literature_gap_operator_dependency_markdown}`"
        ),
        (
            "- literature_gap_operator_dependency_json: "
            f"`{report.literature_gap_operator_dependency_json}`"
        ),
        f"- papers_blockers_index: `{report.papers_blockers_index}`",
    )


def _check_rows(
    report: Lemma0252TheoremArtifactReviewQueueDependency,
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
    report: Lemma0252TheoremArtifactReviewQueueDependency,
) -> str:
    return "\n".join(
        (
            "# Lemma 0252 Theorem Artifact Review Queue Dependency",
            "",
            "Generated by `track-a-regularity/evaluator/"
            "lemma_0252_theorem_artifact_review_queue_dependency.py`.",
            "",
            "This read-only dependency/freshness guard keeps the Step 112 theorem-artifact",
            "review queue synchronized with the Step 102 analytic-discharge gap index,",
            "the Step 108-111 blocker-literature gap stack, and `papers/blockers/index.md`.",
            "It is an audit surface only; it does not discharge blockers or authorize process",
            "gates.",
            "",
            "## Summary",
            "",
            *_summary_lines(report),
            f"- issues: `{', '.join(report.issues) or 'none'}`",
            "",
            "## Source Reports",
            "",
            *_source_report_lines(report),
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


def render_json(report: Lemma0252TheoremArtifactReviewQueueDependency) -> str:
    return json.dumps(
        theorem_artifact_review_queue_dependency_to_dict(report),
        indent=2,
        sort_keys=True,
    ) + "\n"


def render_output(
    report: Lemma0252TheoremArtifactReviewQueueDependency,
    output_format: str,
) -> str:
    if output_format == "markdown":
        return render_markdown(report)
    if output_format == "json":
        return render_json(report)
    raise ValueError(f"unknown theorem artifact review queue dependency format: {output_format}")


def write_output(
    output: Path,
    report: Lemma0252TheoremArtifactReviewQueueDependency,
    output_format: str,
) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_output(report, output_format), encoding="utf-8")
    return output


def check_output(
    output: Path,
    report: Lemma0252TheoremArtifactReviewQueueDependency,
    output_format: str,
) -> tuple[bool, str]:
    expected = render_output(report, output_format)
    if not output.exists():
        return False, f"missing lemma_0252 theorem artifact review queue dependency: {output}"
    current = output.read_text(encoding="utf-8")
    if current != expected:
        return False, f"stale lemma_0252 theorem artifact review queue dependency: {output}"
    return True, f"fresh lemma_0252 theorem artifact review queue dependency: {output}"


def check_consistent(
    report: Lemma0252TheoremArtifactReviewQueueDependency,
) -> tuple[bool, str]:
    if not report.theorem_artifact_review_queue_dependency_consistent:
        return (
            False,
            "lemma_0252 theorem artifact review queue dependency inconsistent: "
            + ", ".join(report.issues),
        )
    return True, "lemma_0252 theorem artifact review queue dependency is consistent"


def check_sources(
    report: Lemma0252TheoremArtifactReviewQueueDependency,
) -> tuple[bool, str]:
    if report.missing_source_count:
        return (
            False,
            "missing lemma_0252 theorem artifact review queue dependency sources: "
            + ", ".join(report.missing_sources),
        )
    return True, "all lemma_0252 theorem artifact review queue dependency sources exist"


def check_blocked(
    report: Lemma0252TheoremArtifactReviewQueueDependency,
) -> tuple[bool, str]:
    if report.process_gate_open_authorized:
        return False, "process gate open became authorized"
    if report.blocker_state_changed:
        return False, "theorem artifact review queue dependency changed blocker state"
    if report.candidate_emission_authorized:
        return False, "theorem artifact review queue dependency authorized candidate emission"
    if report.actionable_queue_item_count:
        return False, "theorem artifact review queue dependency found actionable queue items"
    if report.may_discharge_queue_item_count:
        return False, "theorem artifact review queue dependency found discharge-capable items"
    if report.direct_theorem_artifact_count:
        return False, "theorem artifact review queue dependency found direct theorem artifacts"
    if report.actionable_gap_count:
        return False, "theorem artifact review queue dependency found actionable gaps"
    if report.may_discharge_gap_count:
        return False, "theorem artifact review queue dependency found discharge-capable gaps"
    if report.direct_discharge_source_count:
        return False, "theorem artifact review queue dependency found direct discharge sources"
    if report.blocked_queue_item_count != report.queue_item_count:
        return False, "not all theorem artifact review queue items remain blocked"
    if report.blocked_gap_count != report.gap_count:
        return False, "not all upstream analytic-discharge gaps remain blocked"
    return True, "lemma_0252 theorem artifact review queue dependency keeps items blocked"


def default_output_path(output_format: str) -> Path:
    if output_format == "markdown":
        return DEFAULT_MARKDOWN_OUTPUT
    if output_format == "json":
        return DEFAULT_JSON_OUTPUT
    raise ValueError(f"unknown theorem artifact review queue dependency format: {output_format}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Check Step 112 lemma_0252 theorem-artifact review queue against its "
            "canonical upstream sources."
        )
    )
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--check-output", action="store_true")
    parser.add_argument("--require-consistent", action="store_true")
    parser.add_argument("--require-sources-exist", action="store_true")
    parser.add_argument("--require-blocked", action="store_true")
    args = parser.parse_args(argv)

    try:
        report = build_theorem_artifact_review_queue_dependency()
    except Exception as exc:  # noqa: BLE001 - CLI should report setup failures.
        print(
            f"failed to build lemma_0252 theorem artifact review queue dependency: {exc}",
            file=sys.stderr,
        )
        return 1

    output = args.output or default_output_path(args.format)
    if args.check_output:
        ok, message = check_output(output, report, args.format)
        print(message)
        if not ok:
            print(
                "run without --check-output to regenerate the theorem artifact review queue dependency",
                file=sys.stderr,
            )
            return 1
    else:
        written = write_output(output, report, args.format)
        print(f"wrote {written}")

    if args.require_consistent:
        ok, message = check_consistent(report)
        print(message)
        if not ok:
            return 1
    if args.require_sources_exist:
        ok, message = check_sources(report)
        print(message)
        if not ok:
            return 1
    if args.require_blocked:
        ok, message = check_blocked(report)
        print(message)
        if not ok:
            return 1

    print(
        "theorem_artifact_review_queue_dependency_check_count: "
        f"{report.theorem_artifact_review_queue_dependency_check_count}"
    )
    print(
        "passed_theorem_artifact_review_queue_dependency_check_count: "
        f"{report.passed_theorem_artifact_review_queue_dependency_check_count}"
    )
    print(
        "failed_theorem_artifact_review_queue_dependency_check_count: "
        f"{report.failed_theorem_artifact_review_queue_dependency_check_count}"
    )
    print(
        "theorem_artifact_review_queue_dependency_consistent: "
        f"{str(report.theorem_artifact_review_queue_dependency_consistent).lower()}"
    )
    print(
        "process_gate_open_authorized: "
        f"{str(report.process_gate_open_authorized).lower()}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
