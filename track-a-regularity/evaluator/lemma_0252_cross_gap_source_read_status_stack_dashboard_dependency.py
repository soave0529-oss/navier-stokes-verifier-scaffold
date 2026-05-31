from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from lemma_0252_cross_gap_source_read_status_stack_dashboard import (
    DEFAULT_JSON_OUTPUT as DEFAULT_STACK_DASHBOARD_JSON,
    DEFAULT_MARKDOWN_OUTPUT as DEFAULT_STACK_DASHBOARD_MARKDOWN,
    build_cross_gap_source_read_status_stack_dashboard,
    render_json as render_stack_dashboard_json,
    render_markdown as render_stack_dashboard_markdown,
)


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REPORT_DIR = ROOT / "track-a-regularity/reports"
DEFAULT_MARKDOWN_OUTPUT = (
    DEFAULT_REPORT_DIR
    / "lemma_0252_cross_gap_source_read_status_stack_dashboard_dependency.md"
)
DEFAULT_JSON_OUTPUT = (
    DEFAULT_REPORT_DIR
    / "lemma_0252_cross_gap_source_read_status_stack_dashboard_dependency.json"
)
DEFAULT_PAPERS_INDEX = ROOT / "papers/blockers/index.md"

GAP_IDS = ("gap_002", "gap_003", "gap_004")
MAX_COMPACT_JSON_BYTES = 200_000

NON_CLAIMS = (
    "read_only_cross_gap_source_read_status_stack_dashboard_dependency_guard",
    "canonical_stack_dashboard_freshness_only",
    "compact_snapshot_guard_only",
    "non_promotional_gap_002_gap_003_gap_004_dependency_audit",
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
class CrossGapSourceReadStatusStackDashboardDependencyCheck:
    key: str
    expected: str
    observed: str
    passed: bool
    source_artifacts: tuple[str, ...]


@dataclass(frozen=True)
class Lemma0252CrossGapSourceReadStatusStackDashboardDependency:
    schema_version: int
    lemma_id: str
    candidate_status: str
    active_candidate: bool
    stack_dashboard_markdown: str
    stack_dashboard_json: str
    papers_blockers_index: str
    direct_source_report_count: int
    source_ref_count: int
    cross_gap_source_read_status_stack_dashboard_dependency_check_count: int
    passed_cross_gap_source_read_status_stack_dashboard_dependency_check_count: int
    failed_cross_gap_source_read_status_stack_dashboard_dependency_check_count: int
    cross_gap_source_read_status_stack_dashboard_dependency_consistent: bool
    canonical_json_matches_fresh_build: bool
    canonical_markdown_matches_fresh_build: bool
    stack_step_count: int
    stack_source_report_count: int
    stack_source_ref_count: int
    stack_dashboard_check_count: int
    failed_stack_dashboard_check_count: int
    stack_dashboard_consistent: bool
    dashboard_gap_count: int
    dashboard_source_report_count: int
    dashboard_source_ref_count: int
    dashboard_check_count: int
    failed_dashboard_check_count: int
    dependency_check_count: int
    failed_dependency_check_count: int
    dependency_consistent: bool
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
    actionable_queue_item_count: int
    may_discharge_queue_item_count: int
    direct_theorem_artifact_count: int
    process_gate_open_authorized: bool
    blocker_state_changed: bool
    candidate_emission_authorized: bool
    stack_json_size_bytes: int
    stack_markdown_size_bytes: int
    max_compact_json_bytes: int
    stack_json_compact: bool
    missing_source_count: int
    missing_sources: tuple[str, ...]
    checks: tuple[CrossGapSourceReadStatusStackDashboardDependencyCheck, ...]
    issues: tuple[str, ...]
    source_refs: tuple[str, ...]
    source_read_ids_by_gap: dict[str, tuple[str, ...]]
    non_claims: tuple[str, ...]
    stack_dashboard_snapshot: dict[str, object]


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
) -> CrossGapSourceReadStatusStackDashboardDependencyCheck:
    return CrossGapSourceReadStatusStackDashboardDependencyCheck(
        key=key,
        expected=str(expected),
        observed=str(observed),
        passed=expected == observed,
        source_artifacts=source_artifacts,
    )


def _missing_sources(source_refs: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(source for source in source_refs if not (ROOT / source).exists())


def _source_refs(stack_dashboard: dict[str, object]) -> tuple[str, ...]:
    refs = {
        _rel(DEFAULT_STACK_DASHBOARD_MARKDOWN),
        _rel(DEFAULT_STACK_DASHBOARD_JSON),
        _rel(DEFAULT_PAPERS_INDEX),
        *(str(source) for source in stack_dashboard.get("source_refs", ())),
    }
    return tuple(sorted(refs))


def _direct_report_count(source_refs: tuple[str, ...]) -> int:
    return sum(
        1
        for source in source_refs
        if source.startswith("track-a-regularity/reports/")
        and (source.endswith(".md") or source.endswith(".json"))
    )


def _source_read_ids_by_gap(source: dict[str, object]) -> dict[str, tuple[str, ...]]:
    raw = source.get("source_read_ids_by_gap", {})
    if not isinstance(raw, dict):
        return {}
    return {
        str(gap_id): tuple(str(source_id) for source_id in source_ids)
        for gap_id, source_ids in raw.items()
        if isinstance(source_ids, (list, tuple))
    }


def _compact_snapshot(source: dict[str, object]) -> dict[str, object]:
    keys = (
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
        "dashboard_gap_count",
        "dashboard_source_report_count",
        "dashboard_source_ref_count",
        "dashboard_check_count",
        "failed_dashboard_check_count",
        "dependency_check_count",
        "failed_dependency_check_count",
        "dependency_consistent",
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
        "missing_source_count",
    )
    return {key: source.get(key) for key in keys if key in source}


def build_cross_gap_source_read_status_stack_dashboard_dependency(
    stack_dashboard_json: Path = DEFAULT_STACK_DASHBOARD_JSON,
    stack_dashboard_markdown: Path = DEFAULT_STACK_DASHBOARD_MARKDOWN,
) -> Lemma0252CrossGapSourceReadStatusStackDashboardDependency:
    canonical_stack = _load_json(stack_dashboard_json)
    fresh_report = build_cross_gap_source_read_status_stack_dashboard()
    fresh_stack = json.loads(render_stack_dashboard_json(fresh_report))
    canonical_markdown = stack_dashboard_markdown.read_text(encoding="utf-8")
    fresh_markdown = render_stack_dashboard_markdown(fresh_report)

    canonical_json_matches_fresh_build = canonical_stack == fresh_stack
    canonical_markdown_matches_fresh_build = canonical_markdown == fresh_markdown
    stack = fresh_stack
    source_refs = _source_refs(stack)
    missing_sources = _missing_sources(source_refs)
    source_read_ids_by_gap = _source_read_ids_by_gap(stack)
    stack_json_size_bytes = stack_dashboard_json.stat().st_size
    stack_markdown_size_bytes = stack_dashboard_markdown.stat().st_size

    artifacts = (_rel(DEFAULT_STACK_DASHBOARD_MARKDOWN), _rel(DEFAULT_STACK_DASHBOARD_JSON))
    checks = [
        _check(
            key="stack_dashboard.canonical_json.matches_fresh_build",
            expected=True,
            observed=canonical_json_matches_fresh_build,
            source_artifacts=artifacts,
        ),
        _check(
            key="stack_dashboard.canonical_markdown.matches_fresh_build",
            expected=True,
            observed=canonical_markdown_matches_fresh_build,
            source_artifacts=artifacts,
        ),
        _check(
            key="stack_dashboard.json_remains_compact",
            expected=True,
            observed=stack_json_size_bytes <= MAX_COMPACT_JSON_BYTES,
            source_artifacts=(_rel(DEFAULT_STACK_DASHBOARD_JSON),),
        ),
        _check(
            key="all.lemma_id.matches",
            expected="lemma_0252",
            observed=stack.get("lemma_id"),
            source_artifacts=artifacts,
        ),
        _check(
            key="all.candidate_status.remains_needs_review",
            expected="needs_review",
            observed=stack.get("candidate_status"),
            source_artifacts=artifacts,
        ),
        _check(
            key="all.active_candidate.false",
            expected=False,
            observed=stack.get("active_candidate"),
            source_artifacts=artifacts,
        ),
        _check(
            key="stack_dashboard.gap_ids.expected_direct_analytic_gaps",
            expected=GAP_IDS,
            observed=tuple(stack.get("gap_ids", ())),
            source_artifacts=artifacts,
        ),
        _check(
            key="stack_dashboard.stack_step_count.expected_two",
            expected=2,
            observed=stack.get("stack_step_count"),
            source_artifacts=artifacts,
        ),
        _check(
            key="stack_dashboard.source_report_count.expected_four",
            expected=4,
            observed=stack.get("source_report_count"),
            source_artifacts=artifacts,
        ),
        _check(
            key="stack_dashboard.source_ref_count.expected_106",
            expected=106,
            observed=stack.get("source_ref_count"),
            source_artifacts=artifacts,
        ),
        _check(
            key="stack_dashboard.check_count.expected_fifty",
            expected=50,
            observed=stack.get(
                "cross_gap_source_read_status_stack_dashboard_check_count"
            ),
            source_artifacts=artifacts,
        ),
        _check(
            key="stack_dashboard.failed_check_count.zero",
            expected=0,
            observed=stack.get(
                "failed_cross_gap_source_read_status_stack_dashboard_check_count"
            ),
            source_artifacts=artifacts,
        ),
        _check(
            key="stack_dashboard.consistent.true",
            expected=True,
            observed=stack.get("cross_gap_source_read_status_stack_dashboard_consistent"),
            source_artifacts=artifacts,
        ),
    ]

    for key in (
        "dashboard_gap_count",
        "dashboard_source_report_count",
        "dashboard_source_ref_count",
        "dashboard_check_count",
        "failed_dashboard_check_count",
        "dependency_check_count",
        "failed_dependency_check_count",
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
        "actionable_queue_item_count",
        "may_discharge_queue_item_count",
        "direct_theorem_artifact_count",
        "process_gate_open_authorized",
        "blocker_state_changed",
        "candidate_emission_authorized",
    ):
        checks.append(
            _check(
                key=f"stack_dashboard.{key}.matches_expected_state",
                expected=stack.get(key),
                observed=stack.get(key),
                source_artifacts=artifacts,
            )
        )

    checks.extend(
        [
            _check(
                key="all.source_reads.remain_blocked",
                expected=stack.get("source_read_count"),
                observed=stack.get("blocked_source_read_count"),
                source_artifacts=artifacts,
            ),
            _check(
                key="all.actionable_source_read_count.zero",
                expected=0,
                observed=stack.get("actionable_source_read_count"),
                source_artifacts=artifacts,
            ),
            _check(
                key="all.may_discharge_source_read_count.zero",
                expected=0,
                observed=stack.get("may_discharge_source_read_count"),
                source_artifacts=artifacts,
            ),
            _check(
                key="all.exact_discharge_artifact_count.zero",
                expected=0,
                observed=stack.get("exact_discharge_artifact_count"),
                source_artifacts=artifacts,
            ),
            _check(
                key="all.direct_theorem_artifact_count.zero",
                expected=0,
                observed=stack.get("direct_theorem_artifact_count"),
                source_artifacts=artifacts,
            ),
            _check(
                key="all.process_gate_open_authorized.false",
                expected=False,
                observed=stack.get("process_gate_open_authorized"),
                source_artifacts=artifacts,
            ),
            _check(
                key="all.blocker_state_changed.false",
                expected=False,
                observed=stack.get("blocker_state_changed"),
                source_artifacts=artifacts,
            ),
            _check(
                key="all.candidate_emission_authorized.false",
                expected=False,
                observed=stack.get("candidate_emission_authorized"),
                source_artifacts=artifacts,
            ),
            _check(
                key="source_refs.include_step_127_reports",
                expected=True,
                observed=all(source in source_refs for source in artifacts),
                source_artifacts=artifacts,
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
                source_artifacts=artifacts,
            ),
            _check(
                key="source_refs.include_source_read_packets",
                expected=True,
                observed=all(
                    source in source_refs
                    for source in (
                        "track-a-regularity/reports/"
                        "lemma_0252_finite_bound_smallness_source_read_packet.md",
                        "track-a-regularity/reports/"
                        "lemma_0252_finite_bound_smallness_source_read_packet.json",
                        "track-a-regularity/reports/"
                        "lemma_0252_finite_bound_smallness_source_read_packet_dependency.md",
                        "track-a-regularity/reports/"
                        "lemma_0252_finite_bound_smallness_source_read_packet_dependency.json",
                        "track-a-regularity/reports/"
                        "lemma_0252_compactness_liouville_source_read_packet.md",
                        "track-a-regularity/reports/"
                        "lemma_0252_compactness_liouville_source_read_packet.json",
                        "track-a-regularity/reports/"
                        "lemma_0252_compactness_liouville_source_read_packet_dependency.md",
                        "track-a-regularity/reports/"
                        "lemma_0252_compactness_liouville_source_read_packet_dependency.json",
                        "track-a-regularity/reports/"
                        "lemma_0252_smooth_continuation_source_read_packet.md",
                        "track-a-regularity/reports/"
                        "lemma_0252_smooth_continuation_source_read_packet.json",
                        "track-a-regularity/reports/"
                        "lemma_0252_smooth_continuation_source_read_packet_dependency.md",
                        "track-a-regularity/reports/"
                        "lemma_0252_smooth_continuation_source_read_packet_dependency.json",
                        "track-a-regularity/reports/"
                        "lemma_0252_smooth_continuation_source_read_packet_operator_index.md",
                        "track-a-regularity/reports/"
                        "lemma_0252_smooth_continuation_source_read_packet_operator_index.json",
                        "track-a-regularity/reports/"
                        "lemma_0252_smooth_continuation_source_read_packet_operator_dependency.md",
                        "track-a-regularity/reports/"
                        "lemma_0252_smooth_continuation_source_read_packet_operator_dependency.json",
                    )
                ),
                source_artifacts=artifacts,
            ),
            _check(
                key="source_refs.include_theorem_queue_stack",
                expected=True,
                observed=all(
                    source in source_refs
                    for source in (
                        "track-a-regularity/reports/"
                        "lemma_0252_theorem_artifact_review_queue.md",
                        "track-a-regularity/reports/"
                        "lemma_0252_theorem_artifact_review_queue.json",
                        "track-a-regularity/reports/"
                        "lemma_0252_theorem_artifact_review_queue_dependency.md",
                        "track-a-regularity/reports/"
                        "lemma_0252_theorem_artifact_review_queue_dependency.json",
                        "track-a-regularity/reports/"
                        "lemma_0252_theorem_artifact_review_queue_operator_index.md",
                        "track-a-regularity/reports/"
                        "lemma_0252_theorem_artifact_review_queue_operator_index.json",
                        "track-a-regularity/reports/"
                        "lemma_0252_theorem_artifact_review_queue_operator_dependency.md",
                        "track-a-regularity/reports/"
                        "lemma_0252_theorem_artifact_review_queue_operator_dependency.json",
                    )
                ),
                source_artifacts=artifacts,
            ),
            _check(
                key="source_refs.include_branch_checklists",
                expected=True,
                observed=all(
                    source in source_refs
                    for source in (
                        "track-a-regularity/reports/"
                        "lemma_0252_finite_bound_smallness_checklist.md",
                        "track-a-regularity/reports/"
                        "lemma_0252_finite_bound_smallness_checklist.json",
                        "track-a-regularity/reports/"
                        "lemma_0252_compactness_liouville_checklist.md",
                        "track-a-regularity/reports/"
                        "lemma_0252_compactness_liouville_checklist.json",
                        "track-a-regularity/reports/"
                        "lemma_0252_smooth_continuation_checklist.md",
                        "track-a-regularity/reports/"
                        "lemma_0252_smooth_continuation_checklist.json",
                    )
                ),
                source_artifacts=artifacts,
            ),
            _check(
                key="source_refs.include_papers_blockers_index",
                expected=True,
                observed="papers/blockers/index.md" in source_refs,
                source_artifacts=("papers/blockers/index.md",),
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
                source_artifacts=artifacts,
            ),
            _check(
                key="source_read_ids.total_expected_fifteen",
                expected=15,
                observed=sum(len(source_ids) for source_ids in source_read_ids_by_gap.values()),
                source_artifacts=artifacts,
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

    return Lemma0252CrossGapSourceReadStatusStackDashboardDependency(
        schema_version=1,
        lemma_id=str(stack.get("lemma_id")),
        candidate_status=str(stack.get("candidate_status")),
        active_candidate=bool(stack.get("active_candidate")),
        stack_dashboard_markdown=_rel(DEFAULT_STACK_DASHBOARD_MARKDOWN),
        stack_dashboard_json=_rel(DEFAULT_STACK_DASHBOARD_JSON),
        papers_blockers_index="papers/blockers/index.md",
        direct_source_report_count=_direct_report_count(source_refs),
        source_ref_count=len(source_refs),
        cross_gap_source_read_status_stack_dashboard_dependency_check_count=len(checks),
        passed_cross_gap_source_read_status_stack_dashboard_dependency_check_count=sum(
            check.passed for check in checks
        ),
        failed_cross_gap_source_read_status_stack_dashboard_dependency_check_count=len(
            issues
        ),
        cross_gap_source_read_status_stack_dashboard_dependency_consistent=len(issues)
        == 0,
        canonical_json_matches_fresh_build=canonical_json_matches_fresh_build,
        canonical_markdown_matches_fresh_build=canonical_markdown_matches_fresh_build,
        stack_step_count=int(stack.get("stack_step_count", 0)),
        stack_source_report_count=int(stack.get("source_report_count", 0)),
        stack_source_ref_count=int(stack.get("source_ref_count", 0)),
        stack_dashboard_check_count=int(
            stack.get("cross_gap_source_read_status_stack_dashboard_check_count", 0)
        ),
        failed_stack_dashboard_check_count=int(
            stack.get(
                "failed_cross_gap_source_read_status_stack_dashboard_check_count",
                0,
            )
        ),
        stack_dashboard_consistent=bool(
            stack.get("cross_gap_source_read_status_stack_dashboard_consistent")
        ),
        dashboard_gap_count=int(stack.get("dashboard_gap_count", 0)),
        dashboard_source_report_count=int(stack.get("dashboard_source_report_count", 0)),
        dashboard_source_ref_count=int(stack.get("dashboard_source_ref_count", 0)),
        dashboard_check_count=int(stack.get("dashboard_check_count", 0)),
        failed_dashboard_check_count=int(stack.get("failed_dashboard_check_count", 0)),
        dependency_check_count=int(stack.get("dependency_check_count", 0)),
        failed_dependency_check_count=int(stack.get("failed_dependency_check_count", 0)),
        dependency_consistent=bool(stack.get("dependency_consistent")),
        source_read_count=int(stack.get("source_read_count", 0)),
        direct_branch_source_read_count=int(
            stack.get("direct_branch_source_read_count", 0)
        ),
        cross_cutting_source_read_count=int(
            stack.get("cross_cutting_source_read_count", 0)
        ),
        blocked_source_read_count=int(stack.get("blocked_source_read_count", 0)),
        actionable_source_read_count=int(stack.get("actionable_source_read_count", 0)),
        may_discharge_source_read_count=int(
            stack.get("may_discharge_source_read_count", 0)
        ),
        exact_discharge_artifact_count=int(
            stack.get("exact_discharge_artifact_count", 0)
        ),
        packet_check_count=int(stack.get("packet_check_count", 0)),
        failed_packet_check_count=int(stack.get("failed_packet_check_count", 0)),
        source_read_dependency_check_count=int(
            stack.get("source_read_dependency_check_count", 0)
        ),
        failed_source_read_dependency_check_count=int(
            stack.get("failed_source_read_dependency_check_count", 0)
        ),
        checklist_item_count=int(stack.get("checklist_item_count", 0)),
        theorem_branch_count=int(stack.get("theorem_branch_count", 0)),
        dischargeable_now_count=int(stack.get("dischargeable_now_count", 0)),
        queue_item_count=int(stack.get("queue_item_count", 0)),
        blocked_queue_item_count=int(stack.get("blocked_queue_item_count", 0)),
        actionable_queue_item_count=int(stack.get("actionable_queue_item_count", 0)),
        may_discharge_queue_item_count=int(
            stack.get("may_discharge_queue_item_count", 0)
        ),
        direct_theorem_artifact_count=int(stack.get("direct_theorem_artifact_count", 0)),
        process_gate_open_authorized=bool(stack.get("process_gate_open_authorized")),
        blocker_state_changed=bool(stack.get("blocker_state_changed")),
        candidate_emission_authorized=bool(stack.get("candidate_emission_authorized")),
        stack_json_size_bytes=stack_json_size_bytes,
        stack_markdown_size_bytes=stack_markdown_size_bytes,
        max_compact_json_bytes=MAX_COMPACT_JSON_BYTES,
        stack_json_compact=stack_json_size_bytes <= MAX_COMPACT_JSON_BYTES,
        missing_source_count=len(missing_sources),
        missing_sources=missing_sources,
        checks=tuple(checks),
        issues=issues,
        source_refs=source_refs,
        source_read_ids_by_gap=source_read_ids_by_gap,
        non_claims=NON_CLAIMS,
        stack_dashboard_snapshot=_compact_snapshot(stack),
    )


def render_json(
    report: Lemma0252CrossGapSourceReadStatusStackDashboardDependency,
) -> str:
    return json.dumps(asdict(report), indent=2, sort_keys=True) + "\n"


def render_markdown(
    report: Lemma0252CrossGapSourceReadStatusStackDashboardDependency,
) -> str:
    lines = [
        "# Lemma 0252 Cross-Gap Source Read Status Stack Dashboard Dependency",
        "",
        "Read-only dependency/freshness guard for the Step 127 cross-gap source-read status stack dashboard.",
        "It consolidates freshness and source checks only; it does not discharge blockers or authorize promotion.",
        "",
        "## Summary",
        "",
        f"- lemma_id: `{report.lemma_id}`",
        f"- candidate_status: `{report.candidate_status}`",
        f"- active_candidate: `{str(report.active_candidate).lower()}`",
        f"- direct_source_report_count: `{report.direct_source_report_count}`",
        f"- source_ref_count: `{report.source_ref_count}`",
        (
            "- cross_gap_source_read_status_stack_dashboard_dependency_check_count: "
            f"`{report.cross_gap_source_read_status_stack_dashboard_dependency_check_count}`"
        ),
        (
            "- failed_cross_gap_source_read_status_stack_dashboard_dependency_check_count: "
            f"`{report.failed_cross_gap_source_read_status_stack_dashboard_dependency_check_count}`"
        ),
        (
            "- cross_gap_source_read_status_stack_dashboard_dependency_consistent: "
            f"`{str(report.cross_gap_source_read_status_stack_dashboard_dependency_consistent).lower()}`"
        ),
        f"- canonical_json_matches_fresh_build: `{str(report.canonical_json_matches_fresh_build).lower()}`",
        f"- canonical_markdown_matches_fresh_build: `{str(report.canonical_markdown_matches_fresh_build).lower()}`",
        f"- stack_step_count: `{report.stack_step_count}`",
        f"- stack_source_ref_count: `{report.stack_source_ref_count}`",
        f"- stack_dashboard_check_count: `{report.stack_dashboard_check_count}`",
        f"- failed_stack_dashboard_check_count: `{report.failed_stack_dashboard_check_count}`",
        f"- source_read_count: `{report.source_read_count}`",
        f"- blocked_source_read_count: `{report.blocked_source_read_count}`",
        f"- actionable_source_read_count: `{report.actionable_source_read_count}`",
        f"- may_discharge_source_read_count: `{report.may_discharge_source_read_count}`",
        f"- exact_discharge_artifact_count: `{report.exact_discharge_artifact_count}`",
        f"- process_gate_open_authorized: `{str(report.process_gate_open_authorized).lower()}`",
        f"- blocker_state_changed: `{str(report.blocker_state_changed).lower()}`",
        f"- candidate_emission_authorized: `{str(report.candidate_emission_authorized).lower()}`",
        f"- stack_json_size_bytes: `{report.stack_json_size_bytes}`",
        f"- max_compact_json_bytes: `{report.max_compact_json_bytes}`",
        f"- stack_json_compact: `{str(report.stack_json_compact).lower()}`",
        f"- missing_source_count: `{report.missing_source_count}`",
        "",
        "## Gap Source Reads",
        "",
        "| gap_id | source_read_ids |",
        "|---|---|",
    ]
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
    report: Lemma0252CrossGapSourceReadStatusStackDashboardDependency,
) -> tuple[bool, str]:
    if report.missing_source_count == 0:
        return True, "all cross-gap source-read status stack dashboard dependency sources exist"
    return False, f"missing sources: {', '.join(report.missing_sources)}"


def check_consistent(
    report: Lemma0252CrossGapSourceReadStatusStackDashboardDependency,
) -> tuple[bool, str]:
    if report.cross_gap_source_read_status_stack_dashboard_dependency_consistent:
        return True, "cross-gap source-read status stack dashboard dependency is consistent"
    return False, f"cross-gap source-read status stack dashboard dependency issues: {report.issues}"


def check_blocked(
    report: Lemma0252CrossGapSourceReadStatusStackDashboardDependency,
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
        return True, "cross-gap source-read status stack dashboard dependency remains blocked"
    return False, "cross-gap source-read status stack dashboard dependency opened a blocked gate"


def check_output(
    output: Path,
    report: Lemma0252CrossGapSourceReadStatusStackDashboardDependency,
    fmt: str,
) -> tuple[bool, str]:
    expected = render_json(report) if fmt == "json" else render_markdown(report)
    if not output.exists():
        return False, f"missing cross-gap source-read status stack dashboard dependency: {output}"
    observed = output.read_text(encoding="utf-8")
    if observed == expected:
        return True, f"fresh cross-gap source-read status stack dashboard dependency: {output}"
    return False, f"stale cross-gap source-read status stack dashboard dependency: {output}"


def _write_output(
    output: Path,
    report: Lemma0252CrossGapSourceReadStatusStackDashboardDependency,
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
            "stack dashboard dependency guard."
        )
    )
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--check-output", action="store_true")
    parser.add_argument("--require-sources-exist", action="store_true")
    parser.add_argument("--require-consistent", action="store_true")
    parser.add_argument("--require-blocked", action="store_true")
    args = parser.parse_args(argv)

    report = build_cross_gap_source_read_status_stack_dashboard_dependency()
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
        "cross_gap_source_read_status_stack_dashboard_dependency_check_count: "
        f"{report.cross_gap_source_read_status_stack_dashboard_dependency_check_count}"
    )
    print(
        "failed_cross_gap_source_read_status_stack_dashboard_dependency_check_count: "
        f"{report.failed_cross_gap_source_read_status_stack_dashboard_dependency_check_count}"
    )
    print(
        "cross_gap_source_read_status_stack_dashboard_dependency_consistent: "
        f"{str(report.cross_gap_source_read_status_stack_dashboard_dependency_consistent).lower()}"
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
