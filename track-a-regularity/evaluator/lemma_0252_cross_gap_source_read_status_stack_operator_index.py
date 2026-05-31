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
    / "lemma_0252_cross_gap_source_read_status_stack_operator_index.md"
)
DEFAULT_JSON_OUTPUT = (
    DEFAULT_REPORT_DIR
    / "lemma_0252_cross_gap_source_read_status_stack_operator_index.json"
)
DEFAULT_STACK_DASHBOARD_MARKDOWN = (
    DEFAULT_REPORT_DIR
    / "lemma_0252_cross_gap_source_read_status_stack_dashboard.md"
)
DEFAULT_STACK_DASHBOARD_JSON = (
    DEFAULT_REPORT_DIR
    / "lemma_0252_cross_gap_source_read_status_stack_dashboard.json"
)
DEFAULT_STACK_DEPENDENCY_MARKDOWN = (
    DEFAULT_REPORT_DIR
    / "lemma_0252_cross_gap_source_read_status_stack_dashboard_dependency.md"
)
DEFAULT_STACK_DEPENDENCY_JSON = (
    DEFAULT_REPORT_DIR
    / "lemma_0252_cross_gap_source_read_status_stack_dashboard_dependency.json"
)
DEFAULT_PAPERS_INDEX = ROOT / "papers/blockers/index.md"

GAP_IDS = ("gap_002", "gap_003", "gap_004")

NON_CLAIMS = (
    "read_only_cross_gap_source_read_status_stack_operator_index",
    "operator_source_index_for_review_only",
    "non_promotional_step_127_128_stack_surface",
    "no_candidate_promotion",
    "no_candidate_emission",
    "no_blocker_discharge",
    "no_process_gate_opened",
    "no_file_copy",
    "no_finite_bound_smallness_theorem",
    "no_compactness_liouville_theorem",
    "no_bkm_serrin_high_sobolev_continuation_bridge",
    "no_weak_to_smooth_upgrade",
    "no_navier_stokes_solution",
)


@dataclass(frozen=True)
class CrossGapSourceReadStatusStackOperatorIndexSection:
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
    source_read_count: int
    blocked_source_read_count: int
    exact_discharge_artifact_count: int


@dataclass(frozen=True)
class CrossGapSourceReadStatusStackOperatorIndexCheck:
    key: str
    expected: str
    observed: str
    passed: bool
    source_artifacts: tuple[str, ...]


@dataclass(frozen=True)
class Lemma0252CrossGapSourceReadStatusStackOperatorIndex:
    schema_version: int
    lemma_id: str
    candidate_status: str
    active_candidate: bool
    gap_ids: tuple[str, ...]
    stack_dashboard_markdown: str
    stack_dashboard_json: str
    stack_dependency_markdown: str
    stack_dependency_json: str
    papers_blockers_index: str
    section_count: int
    source_report_count: int
    source_ref_count: int
    cross_gap_source_read_status_stack_operator_index_check_count: int
    passed_cross_gap_source_read_status_stack_operator_index_check_count: int
    failed_cross_gap_source_read_status_stack_operator_index_check_count: int
    cross_gap_source_read_status_stack_operator_index_consistent: bool
    stack_step_count: int
    stack_dashboard_check_count: int
    failed_stack_dashboard_check_count: int
    stack_dashboard_consistent: bool
    stack_dependency_check_count: int
    failed_stack_dependency_check_count: int
    stack_dependency_consistent: bool
    canonical_json_matches_fresh_build: bool
    canonical_markdown_matches_fresh_build: bool
    stack_json_compact: bool
    source_read_count: int
    direct_branch_source_read_count: int
    cross_cutting_source_read_count: int
    blocked_source_read_count: int
    actionable_source_read_count: int
    may_discharge_source_read_count: int
    exact_discharge_artifact_count: int
    packet_check_count: int
    failed_packet_check_count: int
    source_read_dependency_check_count: int
    failed_source_read_dependency_check_count: int
    checklist_item_count: int
    theorem_branch_count: int
    dischargeable_now_count: int
    queue_item_count: int
    blocked_queue_item_count: int
    direct_theorem_artifact_count: int
    process_gate_open_authorized: bool
    blocker_state_changed: bool
    candidate_emission_authorized: bool
    missing_source_count: int
    missing_sources: tuple[str, ...]
    sections: tuple[CrossGapSourceReadStatusStackOperatorIndexSection, ...]
    checks: tuple[CrossGapSourceReadStatusStackOperatorIndexCheck, ...]
    issues: tuple[str, ...]
    source_refs: tuple[str, ...]
    source_read_ids_by_gap: dict[str, tuple[str, ...]]
    non_claims: tuple[str, ...]
    stack_dashboard_snapshot: dict[str, object]
    stack_dependency_snapshot: dict[str, object]


def _rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT).as_posix()


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
) -> CrossGapSourceReadStatusStackOperatorIndexCheck:
    return CrossGapSourceReadStatusStackOperatorIndexCheck(
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
        _rel(DEFAULT_STACK_DASHBOARD_MARKDOWN),
        _rel(DEFAULT_STACK_DASHBOARD_JSON),
        _rel(DEFAULT_STACK_DEPENDENCY_MARKDOWN),
        _rel(DEFAULT_STACK_DEPENDENCY_JSON),
    )


def _source_refs(
    stack_dashboard: dict[str, object],
    stack_dependency: dict[str, object],
) -> tuple[str, ...]:
    refs = {
        *_direct_source_reports(),
        _rel(DEFAULT_PAPERS_INDEX),
        *(str(source) for source in stack_dashboard.get("source_refs", ())),
        *(str(source) for source in stack_dependency.get("source_refs", ())),
    }
    return tuple(sorted(refs))


def _source_read_ids_by_gap(source: dict[str, object]) -> dict[str, tuple[str, ...]]:
    raw = source.get("source_read_ids_by_gap", {})
    if not isinstance(raw, dict):
        return {}
    return {
        str(gap_id): tuple(str(source_id) for source_id in source_ids)
        for gap_id, source_ids in raw.items()
        if isinstance(source_ids, (list, tuple))
    }


def _compact_snapshot(source: dict[str, object], keys: tuple[str, ...]) -> dict[str, object]:
    return {key: source.get(key) for key in keys if key in source}


def _sections(
    stack_dashboard: dict[str, object],
    stack_dependency: dict[str, object],
) -> tuple[CrossGapSourceReadStatusStackOperatorIndexSection, ...]:
    return (
        CrossGapSourceReadStatusStackOperatorIndexSection(
            step=127,
            name="cross_gap_source_read_status_stack_dashboard",
            role=(
                "compact operator/source dashboard for the Step 125-126 "
                "cross-gap source-read status stack"
            ),
            markdown_report=_rel(DEFAULT_STACK_DASHBOARD_MARKDOWN),
            json_report=_rel(DEFAULT_STACK_DASHBOARD_JSON),
            primary_count_label=(
                "cross_gap_source_read_status_stack_dashboard_check_count"
            ),
            primary_count=int(
                stack_dashboard.get(
                    "cross_gap_source_read_status_stack_dashboard_check_count", 0
                )
            ),
            failed_count_label=(
                "failed_cross_gap_source_read_status_stack_dashboard_check_count"
            ),
            failed_count=int(
                stack_dashboard.get(
                    "failed_cross_gap_source_read_status_stack_dashboard_check_count",
                    0,
                )
            ),
            consistent_label=(
                "cross_gap_source_read_status_stack_dashboard_consistent"
            ),
            consistent=bool(
                stack_dashboard.get(
                    "cross_gap_source_read_status_stack_dashboard_consistent"
                )
            ),
            source_read_count=int(stack_dashboard.get("source_read_count", 0)),
            blocked_source_read_count=int(
                stack_dashboard.get("blocked_source_read_count", 0)
            ),
            exact_discharge_artifact_count=int(
                stack_dashboard.get("exact_discharge_artifact_count", 0)
            ),
        ),
        CrossGapSourceReadStatusStackOperatorIndexSection(
            step=128,
            name="cross_gap_source_read_status_stack_dashboard_dependency",
            role=(
                "guards the Step 127 dashboard against drift from the "
                "cross-gap source-read stack and source references"
            ),
            markdown_report=_rel(DEFAULT_STACK_DEPENDENCY_MARKDOWN),
            json_report=_rel(DEFAULT_STACK_DEPENDENCY_JSON),
            primary_count_label=(
                "cross_gap_source_read_status_stack_dashboard_dependency_check_count"
            ),
            primary_count=int(
                stack_dependency.get(
                    "cross_gap_source_read_status_stack_dashboard_dependency_check_count",
                    0,
                )
            ),
            failed_count_label=(
                "failed_cross_gap_source_read_status_stack_dashboard_dependency_check_count"
            ),
            failed_count=int(
                stack_dependency.get(
                    "failed_cross_gap_source_read_status_stack_dashboard_dependency_check_count",
                    0,
                )
            ),
            consistent_label=(
                "cross_gap_source_read_status_stack_dashboard_dependency_consistent"
            ),
            consistent=bool(
                stack_dependency.get(
                    "cross_gap_source_read_status_stack_dashboard_dependency_consistent"
                )
            ),
            source_read_count=int(stack_dependency.get("source_read_count", 0)),
            blocked_source_read_count=int(
                stack_dependency.get("blocked_source_read_count", 0)
            ),
            exact_discharge_artifact_count=int(
                stack_dependency.get("exact_discharge_artifact_count", 0)
            ),
        ),
    )


def build_cross_gap_source_read_status_stack_operator_index(
    stack_dashboard_json: Path = DEFAULT_STACK_DASHBOARD_JSON,
    stack_dependency_json: Path = DEFAULT_STACK_DEPENDENCY_JSON,
) -> Lemma0252CrossGapSourceReadStatusStackOperatorIndex:
    stack_dashboard = _load_json(stack_dashboard_json)
    stack_dependency = _load_json(stack_dependency_json)
    source_refs = _source_refs(stack_dashboard, stack_dependency)
    missing_sources = _missing_sources(source_refs)
    source_read_ids_by_gap = _source_read_ids_by_gap(stack_dependency)
    sections = _sections(stack_dashboard, stack_dependency)

    dashboard_artifacts = (
        _rel(DEFAULT_STACK_DASHBOARD_MARKDOWN),
        _rel(DEFAULT_STACK_DASHBOARD_JSON),
    )
    dependency_artifacts = (
        _rel(DEFAULT_STACK_DEPENDENCY_MARKDOWN),
        _rel(DEFAULT_STACK_DEPENDENCY_JSON),
    )
    all_artifacts = dashboard_artifacts + dependency_artifacts

    checks = [
        _check(
            key="all.lemma_id.matches",
            expected="lemma_0252",
            observed=stack_dashboard.get("lemma_id"),
            source_artifacts=dashboard_artifacts,
        ),
        _check(
            key="dependency.lemma_id.matches_dashboard",
            expected=stack_dashboard.get("lemma_id"),
            observed=stack_dependency.get("lemma_id"),
            source_artifacts=all_artifacts,
        ),
        _check(
            key="all.candidate_status.remains_needs_review",
            expected="needs_review",
            observed=stack_dashboard.get("candidate_status"),
            source_artifacts=dashboard_artifacts,
        ),
        _check(
            key="dependency.candidate_status.matches_dashboard",
            expected=stack_dashboard.get("candidate_status"),
            observed=stack_dependency.get("candidate_status"),
            source_artifacts=all_artifacts,
        ),
        _check(
            key="all.active_candidate.false",
            expected=False,
            observed=stack_dashboard.get("active_candidate"),
            source_artifacts=dashboard_artifacts,
        ),
        _check(
            key="dependency.active_candidate.matches_dashboard",
            expected=stack_dashboard.get("active_candidate"),
            observed=stack_dependency.get("active_candidate"),
            source_artifacts=all_artifacts,
        ),
        _check(
            key="operator_index.section_count.expected_two",
            expected=2,
            observed=len(sections),
            source_artifacts=all_artifacts,
        ),
        _check(
            key="operator_index.source_report_count.expected_four",
            expected=4,
            observed=len(_direct_source_reports()),
            source_artifacts=all_artifacts,
        ),
        _check(
            key="stack_dashboard.check_count.expected_fifty",
            expected=50,
            observed=stack_dashboard.get(
                "cross_gap_source_read_status_stack_dashboard_check_count"
            ),
            source_artifacts=dashboard_artifacts,
        ),
        _check(
            key="stack_dashboard.failed_check_count.zero",
            expected=0,
            observed=stack_dashboard.get(
                "failed_cross_gap_source_read_status_stack_dashboard_check_count"
            ),
            source_artifacts=dashboard_artifacts,
        ),
        _check(
            key="stack_dashboard.consistent.true",
            expected=True,
            observed=stack_dashboard.get(
                "cross_gap_source_read_status_stack_dashboard_consistent"
            ),
            source_artifacts=dashboard_artifacts,
        ),
        _check(
            key="stack_dependency.check_count.expected_sixty",
            expected=60,
            observed=stack_dependency.get(
                "cross_gap_source_read_status_stack_dashboard_dependency_check_count"
            ),
            source_artifacts=dependency_artifacts,
        ),
        _check(
            key="stack_dependency.failed_check_count.zero",
            expected=0,
            observed=stack_dependency.get(
                "failed_cross_gap_source_read_status_stack_dashboard_dependency_check_count"
            ),
            source_artifacts=dependency_artifacts,
        ),
        _check(
            key="stack_dependency.consistent.true",
            expected=True,
            observed=stack_dependency.get(
                "cross_gap_source_read_status_stack_dashboard_dependency_consistent"
            ),
            source_artifacts=dependency_artifacts,
        ),
        _check(
            key="stack_dependency.canonical_json_matches_fresh_build.true",
            expected=True,
            observed=stack_dependency.get("canonical_json_matches_fresh_build"),
            source_artifacts=dependency_artifacts,
        ),
        _check(
            key="stack_dependency.canonical_markdown_matches_fresh_build.true",
            expected=True,
            observed=stack_dependency.get("canonical_markdown_matches_fresh_build"),
            source_artifacts=dependency_artifacts,
        ),
        _check(
            key="stack_dependency.stack_json_compact.true",
            expected=True,
            observed=stack_dependency.get("stack_json_compact"),
            source_artifacts=dependency_artifacts,
        ),
    ]

    for key in (
        "source_read_count",
        "direct_branch_source_read_count",
        "cross_cutting_source_read_count",
        "blocked_source_read_count",
        "actionable_source_read_count",
        "may_discharge_source_read_count",
        "exact_discharge_artifact_count",
        "packet_check_count",
        "failed_packet_check_count",
        "source_read_dependency_check_count",
        "failed_source_read_dependency_check_count",
        "checklist_item_count",
        "theorem_branch_count",
        "dischargeable_now_count",
        "queue_item_count",
        "blocked_queue_item_count",
        "direct_theorem_artifact_count",
        "process_gate_open_authorized",
        "blocker_state_changed",
        "candidate_emission_authorized",
    ):
        checks.append(
            _check(
                key=f"stack_dependency.{key}.matches_dashboard",
                expected=stack_dashboard.get(key),
                observed=stack_dependency.get(key),
                source_artifacts=all_artifacts,
            )
        )

    checks.extend(
        [
            _check(
                key="all.source_reads.remain_blocked",
                expected=stack_dependency.get("source_read_count"),
                observed=stack_dependency.get("blocked_source_read_count"),
                source_artifacts=all_artifacts,
            ),
            _check(
                key="all.actionable_source_read_count.zero",
                expected=0,
                observed=stack_dependency.get("actionable_source_read_count"),
                source_artifacts=all_artifacts,
            ),
            _check(
                key="all.may_discharge_source_read_count.zero",
                expected=0,
                observed=stack_dependency.get("may_discharge_source_read_count"),
                source_artifacts=all_artifacts,
            ),
            _check(
                key="all.exact_discharge_artifact_count.zero",
                expected=0,
                observed=stack_dependency.get("exact_discharge_artifact_count"),
                source_artifacts=all_artifacts,
            ),
            _check(
                key="all.direct_theorem_artifact_count.zero",
                expected=0,
                observed=stack_dependency.get("direct_theorem_artifact_count"),
                source_artifacts=all_artifacts,
            ),
            _check(
                key="all.process_gate_open_authorized.false",
                expected=False,
                observed=stack_dependency.get("process_gate_open_authorized"),
                source_artifacts=all_artifacts,
            ),
            _check(
                key="all.blocker_state_changed.false",
                expected=False,
                observed=stack_dependency.get("blocker_state_changed"),
                source_artifacts=all_artifacts,
            ),
            _check(
                key="all.candidate_emission_authorized.false",
                expected=False,
                observed=stack_dependency.get("candidate_emission_authorized"),
                source_artifacts=all_artifacts,
            ),
            _check(
                key="source_refs.include_step_127_and_128_reports",
                expected=True,
                observed=all(source in source_refs for source in _direct_source_reports()),
                source_artifacts=all_artifacts,
            ),
            _check(
                key="source_refs.include_step_125_and_126_reports",
                expected=True,
                observed=all(
                    source in source_refs
                    for source in (
                        "track-a-regularity/reports/"
                        "lemma_0252_cross_gap_source_read_status_dashboard.md",
                        "track-a-regularity/reports/"
                        "lemma_0252_cross_gap_source_read_status_dashboard.json",
                        "track-a-regularity/reports/"
                        "lemma_0252_cross_gap_source_read_status_dashboard_dependency.md",
                        "track-a-regularity/reports/"
                        "lemma_0252_cross_gap_source_read_status_dashboard_dependency.json",
                    )
                ),
                source_artifacts=all_artifacts,
            ),
            _check(
                key="source_refs.include_source_read_packets",
                expected=True,
                observed=all(
                    source in source_refs
                    for source in (
                        "track-a-regularity/reports/"
                        "lemma_0252_finite_bound_smallness_source_read_packet.json",
                        "track-a-regularity/reports/"
                        "lemma_0252_compactness_liouville_source_read_packet.json",
                        "track-a-regularity/reports/"
                        "lemma_0252_smooth_continuation_source_read_packet.json",
                    )
                ),
                source_artifacts=all_artifacts,
            ),
            _check(
                key="source_refs.include_theorem_queue_stack",
                expected=True,
                observed=all(
                    source in source_refs
                    for source in (
                        "track-a-regularity/reports/"
                        "lemma_0252_theorem_artifact_review_queue.json",
                        "track-a-regularity/reports/"
                        "lemma_0252_theorem_artifact_review_queue_dependency.json",
                        "track-a-regularity/reports/"
                        "lemma_0252_theorem_artifact_review_queue_operator_index.json",
                        "track-a-regularity/reports/"
                        "lemma_0252_theorem_artifact_review_queue_operator_dependency.json",
                    )
                ),
                source_artifacts=all_artifacts,
            ),
            _check(
                key="source_refs.include_branch_checklists",
                expected=True,
                observed=all(
                    source in source_refs
                    for source in (
                        "track-a-regularity/reports/"
                        "lemma_0252_finite_bound_smallness_checklist.json",
                        "track-a-regularity/reports/"
                        "lemma_0252_compactness_liouville_checklist.json",
                        "track-a-regularity/reports/"
                        "lemma_0252_smooth_continuation_checklist.json",
                    )
                ),
                source_artifacts=all_artifacts,
            ),
            _check(
                key="source_refs.include_papers_blockers_index",
                expected=True,
                observed=_rel(DEFAULT_PAPERS_INDEX) in source_refs,
                source_artifacts=(_rel(DEFAULT_PAPERS_INDEX),),
            ),
            _check(
                key="source_refs.missing_count.zero",
                expected=0,
                observed=len(missing_sources),
                source_artifacts=source_refs,
            ),
            _check(
                key="source_read_ids.cover_direct_gaps",
                expected=GAP_IDS,
                observed=tuple(source_read_ids_by_gap),
                source_artifacts=all_artifacts,
            ),
            _check(
                key="source_read_ids.total_expected_fifteen",
                expected=15,
                observed=sum(len(source_ids) for source_ids in source_read_ids_by_gap.values()),
                source_artifacts=all_artifacts,
            ),
            _check(
                key="non_claims.include_no_navier_stokes_solution",
                expected=True,
                observed="no_navier_stokes_solution" in NON_CLAIMS,
                source_artifacts=(),
            ),
        ]
    )
    issues = tuple(check.key for check in checks if not check.passed)

    return Lemma0252CrossGapSourceReadStatusStackOperatorIndex(
        schema_version=1,
        lemma_id=str(stack_dashboard.get("lemma_id")),
        candidate_status=str(stack_dashboard.get("candidate_status")),
        active_candidate=bool(stack_dashboard.get("active_candidate")),
        gap_ids=GAP_IDS,
        stack_dashboard_markdown=_rel(DEFAULT_STACK_DASHBOARD_MARKDOWN),
        stack_dashboard_json=_rel(DEFAULT_STACK_DASHBOARD_JSON),
        stack_dependency_markdown=_rel(DEFAULT_STACK_DEPENDENCY_MARKDOWN),
        stack_dependency_json=_rel(DEFAULT_STACK_DEPENDENCY_JSON),
        papers_blockers_index=_rel(DEFAULT_PAPERS_INDEX),
        section_count=len(sections),
        source_report_count=len(_direct_source_reports()),
        source_ref_count=len(source_refs),
        cross_gap_source_read_status_stack_operator_index_check_count=len(checks),
        passed_cross_gap_source_read_status_stack_operator_index_check_count=sum(
            check.passed for check in checks
        ),
        failed_cross_gap_source_read_status_stack_operator_index_check_count=len(issues),
        cross_gap_source_read_status_stack_operator_index_consistent=len(issues) == 0,
        stack_step_count=int(stack_dashboard.get("stack_step_count", 0)),
        stack_dashboard_check_count=int(
            stack_dashboard.get(
                "cross_gap_source_read_status_stack_dashboard_check_count", 0
            )
        ),
        failed_stack_dashboard_check_count=int(
            stack_dashboard.get(
                "failed_cross_gap_source_read_status_stack_dashboard_check_count", 0
            )
        ),
        stack_dashboard_consistent=bool(
            stack_dashboard.get("cross_gap_source_read_status_stack_dashboard_consistent")
        ),
        stack_dependency_check_count=int(
            stack_dependency.get(
                "cross_gap_source_read_status_stack_dashboard_dependency_check_count",
                0,
            )
        ),
        failed_stack_dependency_check_count=int(
            stack_dependency.get(
                "failed_cross_gap_source_read_status_stack_dashboard_dependency_check_count",
                0,
            )
        ),
        stack_dependency_consistent=bool(
            stack_dependency.get(
                "cross_gap_source_read_status_stack_dashboard_dependency_consistent"
            )
        ),
        canonical_json_matches_fresh_build=bool(
            stack_dependency.get("canonical_json_matches_fresh_build")
        ),
        canonical_markdown_matches_fresh_build=bool(
            stack_dependency.get("canonical_markdown_matches_fresh_build")
        ),
        stack_json_compact=bool(stack_dependency.get("stack_json_compact")),
        source_read_count=int(stack_dependency.get("source_read_count", 0)),
        direct_branch_source_read_count=int(
            stack_dependency.get("direct_branch_source_read_count", 0)
        ),
        cross_cutting_source_read_count=int(
            stack_dependency.get("cross_cutting_source_read_count", 0)
        ),
        blocked_source_read_count=int(
            stack_dependency.get("blocked_source_read_count", 0)
        ),
        actionable_source_read_count=int(
            stack_dependency.get("actionable_source_read_count", 0)
        ),
        may_discharge_source_read_count=int(
            stack_dependency.get("may_discharge_source_read_count", 0)
        ),
        exact_discharge_artifact_count=int(
            stack_dependency.get("exact_discharge_artifact_count", 0)
        ),
        packet_check_count=int(stack_dependency.get("packet_check_count", 0)),
        failed_packet_check_count=int(
            stack_dependency.get("failed_packet_check_count", 0)
        ),
        source_read_dependency_check_count=int(
            stack_dependency.get("source_read_dependency_check_count", 0)
        ),
        failed_source_read_dependency_check_count=int(
            stack_dependency.get("failed_source_read_dependency_check_count", 0)
        ),
        checklist_item_count=int(stack_dependency.get("checklist_item_count", 0)),
        theorem_branch_count=int(stack_dependency.get("theorem_branch_count", 0)),
        dischargeable_now_count=int(stack_dependency.get("dischargeable_now_count", 0)),
        queue_item_count=int(stack_dependency.get("queue_item_count", 0)),
        blocked_queue_item_count=int(
            stack_dependency.get("blocked_queue_item_count", 0)
        ),
        direct_theorem_artifact_count=int(
            stack_dependency.get("direct_theorem_artifact_count", 0)
        ),
        process_gate_open_authorized=bool(
            stack_dependency.get("process_gate_open_authorized")
        ),
        blocker_state_changed=bool(stack_dependency.get("blocker_state_changed")),
        candidate_emission_authorized=bool(
            stack_dependency.get("candidate_emission_authorized")
        ),
        missing_source_count=len(missing_sources),
        missing_sources=missing_sources,
        sections=sections,
        checks=tuple(checks),
        issues=issues,
        source_refs=source_refs,
        source_read_ids_by_gap=source_read_ids_by_gap,
        non_claims=NON_CLAIMS,
        stack_dashboard_snapshot=_compact_snapshot(
            stack_dashboard,
            (
                "lemma_id",
                "candidate_status",
                "active_candidate",
                "gap_ids",
                "stack_step_count",
                "source_report_count",
                "source_ref_count",
                "cross_gap_source_read_status_stack_dashboard_check_count",
                "failed_cross_gap_source_read_status_stack_dashboard_check_count",
                "cross_gap_source_read_status_stack_dashboard_consistent",
                "source_read_count",
                "blocked_source_read_count",
                "actionable_source_read_count",
                "may_discharge_source_read_count",
                "exact_discharge_artifact_count",
                "packet_check_count",
                "source_read_dependency_check_count",
                "checklist_item_count",
                "theorem_branch_count",
                "dischargeable_now_count",
                "queue_item_count",
                "blocked_queue_item_count",
                "direct_theorem_artifact_count",
                "process_gate_open_authorized",
                "blocker_state_changed",
                "candidate_emission_authorized",
                "missing_source_count",
            ),
        ),
        stack_dependency_snapshot=_compact_snapshot(
            stack_dependency,
            (
                "lemma_id",
                "candidate_status",
                "active_candidate",
                "direct_source_report_count",
                "source_ref_count",
                "cross_gap_source_read_status_stack_dashboard_dependency_check_count",
                "failed_cross_gap_source_read_status_stack_dashboard_dependency_check_count",
                "cross_gap_source_read_status_stack_dashboard_dependency_consistent",
                "canonical_json_matches_fresh_build",
                "canonical_markdown_matches_fresh_build",
                "stack_json_compact",
                "source_read_count",
                "blocked_source_read_count",
                "actionable_source_read_count",
                "may_discharge_source_read_count",
                "exact_discharge_artifact_count",
                "packet_check_count",
                "source_read_dependency_check_count",
                "checklist_item_count",
                "theorem_branch_count",
                "dischargeable_now_count",
                "queue_item_count",
                "blocked_queue_item_count",
                "direct_theorem_artifact_count",
                "process_gate_open_authorized",
                "blocker_state_changed",
                "candidate_emission_authorized",
                "missing_source_count",
            ),
        ),
    )


def render_json(report: Lemma0252CrossGapSourceReadStatusStackOperatorIndex) -> str:
    return json.dumps(asdict(report), indent=2, sort_keys=True) + "\n"


def render_markdown(report: Lemma0252CrossGapSourceReadStatusStackOperatorIndex) -> str:
    lines = [
        "# Lemma 0252 Cross-Gap Source Read Status Stack Operator Index",
        "",
        "Compact read-only operator/source index for the Step 127-128 cross-gap source-read status stack.",
        "It consolidates status only; it does not discharge blockers or authorize promotion.",
        "",
        "## Summary",
        "",
        f"- lemma_id: `{report.lemma_id}`",
        f"- candidate_status: `{report.candidate_status}`",
        f"- active_candidate: `{str(report.active_candidate).lower()}`",
        f"- gap_ids: `{', '.join(report.gap_ids)}`",
        f"- section_count: `{report.section_count}`",
        f"- source_report_count: `{report.source_report_count}`",
        f"- source_ref_count: `{report.source_ref_count}`",
        (
            "- cross_gap_source_read_status_stack_operator_index_check_count: "
            f"`{report.cross_gap_source_read_status_stack_operator_index_check_count}`"
        ),
        (
            "- failed_cross_gap_source_read_status_stack_operator_index_check_count: "
            f"`{report.failed_cross_gap_source_read_status_stack_operator_index_check_count}`"
        ),
        (
            "- cross_gap_source_read_status_stack_operator_index_consistent: "
            f"`{str(report.cross_gap_source_read_status_stack_operator_index_consistent).lower()}`"
        ),
        f"- stack_dashboard_check_count: `{report.stack_dashboard_check_count}`",
        f"- failed_stack_dashboard_check_count: `{report.failed_stack_dashboard_check_count}`",
        f"- stack_dependency_check_count: `{report.stack_dependency_check_count}`",
        f"- failed_stack_dependency_check_count: `{report.failed_stack_dependency_check_count}`",
        f"- canonical_json_matches_fresh_build: `{str(report.canonical_json_matches_fresh_build).lower()}`",
        f"- canonical_markdown_matches_fresh_build: `{str(report.canonical_markdown_matches_fresh_build).lower()}`",
        f"- stack_json_compact: `{str(report.stack_json_compact).lower()}`",
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
        "## Sections",
        "",
        "| step | name | primary_count | failed_count | consistent | source_reads | blocked_source_reads | exact_discharge_artifacts |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for section in report.sections:
        lines.append(
            f"| `{section.step}` | `{section.name}` | `{section.primary_count}` | "
            f"`{section.failed_count}` | `{str(section.consistent).lower()}` | "
            f"`{section.source_read_count}` | `{section.blocked_source_read_count}` | "
            f"`{section.exact_discharge_artifact_count}` |"
        )

    lines.extend(["", "## Gap Source Reads", "", "| gap_id | source_read_ids |", "|---|---|"])
    for gap_id in GAP_IDS:
        source_ids = ", ".join(report.source_read_ids_by_gap.get(gap_id, ()))
        lines.append(f"| `{gap_id}` | `{source_ids}` |")

    lines.extend(["", "## Checks", "", "| key | expected | observed | passed |", "|---|---|---|---|"])
    for check in report.checks:
        lines.append(
            f"| `{check.key}` | `{check.expected}` | `{check.observed}` | "
            f"`{str(check.passed).lower()}` |"
        )

    lines.extend(["", "## Non-Claims", ""])
    lines.extend(f"- `{claim}`" for claim in report.non_claims)
    lines.extend(["", "## Source Refs", ""])
    lines.extend(f"- `{source}`" for source in report.source_refs)
    if report.issues:
        lines.extend(["", "## Issues", ""])
        lines.extend(f"- `{issue}`" for issue in report.issues)
    return "\n".join(lines) + "\n"


def check_sources(
    report: Lemma0252CrossGapSourceReadStatusStackOperatorIndex,
) -> tuple[bool, str]:
    if report.missing_source_count == 0:
        return True, "all cross-gap source-read status stack operator index sources exist"
    return False, f"missing sources: {', '.join(report.missing_sources)}"


def check_consistent(
    report: Lemma0252CrossGapSourceReadStatusStackOperatorIndex,
) -> tuple[bool, str]:
    if report.cross_gap_source_read_status_stack_operator_index_consistent:
        return True, "cross-gap source-read status stack operator index is consistent"
    return False, f"cross-gap source-read status stack operator index issues: {report.issues}"


def check_blocked(
    report: Lemma0252CrossGapSourceReadStatusStackOperatorIndex,
) -> tuple[bool, str]:
    ok = (
        report.candidate_status == "needs_review"
        and report.active_candidate is False
        and report.source_read_count == report.blocked_source_read_count
        and report.actionable_source_read_count == 0
        and report.may_discharge_source_read_count == 0
        and report.exact_discharge_artifact_count == 0
        and report.direct_theorem_artifact_count == 0
        and report.dischargeable_now_count == 0
        and report.process_gate_open_authorized is False
        and report.blocker_state_changed is False
        and report.candidate_emission_authorized is False
    )
    if ok:
        return True, "cross-gap source-read status stack operator index remains blocked"
    return False, "cross-gap source-read status stack operator index opened a blocked gate"


def check_output(
    output: Path,
    report: Lemma0252CrossGapSourceReadStatusStackOperatorIndex,
    fmt: str,
) -> tuple[bool, str]:
    expected = render_json(report) if fmt == "json" else render_markdown(report)
    if not output.exists():
        return False, f"missing cross-gap source-read status stack operator index: {output}"
    observed = output.read_text(encoding="utf-8")
    if observed == expected:
        return True, f"fresh cross-gap source-read status stack operator index: {output}"
    return False, f"stale cross-gap source-read status stack operator index: {output}"


def _write_output(
    output: Path,
    report: Lemma0252CrossGapSourceReadStatusStackOperatorIndex,
    fmt: str,
) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        render_json(report) if fmt == "json" else render_markdown(report),
        encoding="utf-8",
    )


def _default_output(fmt: str) -> Path:
    return DEFAULT_JSON_OUTPUT if fmt == "json" else DEFAULT_MARKDOWN_OUTPUT


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Build the read-only lemma_0252 cross-gap source-read status "
            "stack operator/source index."
        )
    )
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--check-output", action="store_true")
    parser.add_argument("--require-sources-exist", action="store_true")
    parser.add_argument("--require-consistent", action="store_true")
    parser.add_argument("--require-blocked", action="store_true")
    args = parser.parse_args(argv)

    report = build_cross_gap_source_read_status_stack_operator_index()
    output = args.output or _default_output(args.format)

    if not args.check_output:
        _write_output(output, report, args.format)

    checks: list[tuple[bool, str]] = []
    if args.check_output:
        checks.append(check_output(output, report, args.format))
    if args.require_sources_exist:
        checks.append(check_sources(report))
    if args.require_consistent:
        checks.append(check_consistent(report))
    if args.require_blocked:
        checks.append(check_blocked(report))

    for ok, message in checks:
        print(message)
        if not ok:
            return 1

    print(
        "cross_gap_source_read_status_stack_operator_index_check_count: "
        f"{report.cross_gap_source_read_status_stack_operator_index_check_count}"
    )
    print(
        "failed_cross_gap_source_read_status_stack_operator_index_check_count: "
        f"{report.failed_cross_gap_source_read_status_stack_operator_index_check_count}"
    )
    print(
        "cross_gap_source_read_status_stack_operator_index_consistent: "
        f"{str(report.cross_gap_source_read_status_stack_operator_index_consistent).lower()}"
    )
    print(f"source_ref_count: {report.source_ref_count}")
    print(f"source_read_count: {report.source_read_count}")
    print(f"blocked_source_read_count: {report.blocked_source_read_count}")
    print(f"exact_discharge_artifact_count: {report.exact_discharge_artifact_count}")
    print(f"stack_json_compact: {str(report.stack_json_compact).lower()}")
    print(f"process_gate_open_authorized: {str(report.process_gate_open_authorized).lower()}")
    print(f"candidate_emission_authorized: {str(report.candidate_emission_authorized).lower()}")
    print(f"missing_source_count: {report.missing_source_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
