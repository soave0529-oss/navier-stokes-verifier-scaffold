from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from lemma_0252_blocker_literature_dependency import (
    DEFAULT_JSON_OUTPUT as DEFAULT_LITERATURE_DEPENDENCY_JSON,
    DEFAULT_MARKDOWN_OUTPUT as DEFAULT_LITERATURE_DEPENDENCY_MARKDOWN,
)
from lemma_0252_blocker_literature_index import (
    DEFAULT_JSON_OUTPUT as DEFAULT_LITERATURE_JSON,
    DEFAULT_MARKDOWN_OUTPUT as DEFAULT_LITERATURE_MARKDOWN,
)
from promotion_gate_analytic_discharge_gap_index import (
    DEFAULT_JSON_OUTPUT as DEFAULT_GAP_JSON,
    DEFAULT_MARKDOWN_OUTPUT as DEFAULT_GAP_MARKDOWN,
)


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REPORT_DIR = ROOT / "track-a-regularity/reports"
DEFAULT_MARKDOWN_OUTPUT = DEFAULT_REPORT_DIR / "lemma_0252_blocker_literature_gap_matrix.md"
DEFAULT_JSON_OUTPUT = DEFAULT_REPORT_DIR / "lemma_0252_blocker_literature_gap_matrix.json"

NON_CLAIMS = (
    "read_only_literature_gap_matrix",
    "source_to_gap_triage_only",
    "no_candidate_promotion",
    "no_candidate_emission",
    "no_blocker_discharge",
    "no_process_gate_opened",
    "no_epsilon_regularity_theorem",
    "no_compactness_or_liouville_theorem",
    "no_bkm_or_serrin_or_high_sobolev_bound",
    "no_weak_to_smooth_upgrade",
    "no_navier_stokes_solution",
)

SOURCE_BRANCH_TO_PRIMARY_GAP = {
    "finite_bound_to_smallness": "gap_002",
    "compactness_liouville": "gap_003",
    "smooth_continuation_bridge": "gap_004",
}

CROSS_CUTTING_GAPS_BY_SOURCE = {
    "tao_localisation_1108_1165": ("gap_002", "gap_003", "gap_006", "gap_007"),
    "tao_averaged_1402_0290": ("gap_006", "gap_007"),
    "tao_blog_2007": ("gap_002", "gap_006", "gap_007"),
}

COMMON_CLOSURE_GAPS = ("gap_006", "gap_007")
ATTACK_ORDER_BY_GAP = {
    "gap_002": 1,
    "gap_003": 2,
    "gap_004": 3,
    "gap_006": 4,
    "gap_007": 5,
    "gap_001": 6,
    "gap_005": 7,
    "gap_008": 8,
}
GAP_ATTACK_NOTE = {
    "gap_001": "metadata update only after all substantive blocker sidecars are reviewed",
    "gap_002": "first analytic target: finite Morrey bound to epsilon-smallness",
    "gap_003": "second analytic target: compactness/Liouville branch",
    "gap_004": "third analytic target: smooth-continuation bridge",
    "gap_005": "closure dashboard refresh only after branch artifacts exist",
    "gap_006": "branch-resolution bundle waits on gaps 002-004",
    "gap_007": "substantive-discharge bundle waits on gaps 002-004",
    "gap_008": "candidate authorization is process metadata after analytic closure only",
}


@dataclass(frozen=True)
class LiteratureGapEdge:
    source_id: str
    blocker_family: str
    gap_id: str
    required_artifact_type: str
    source_branch: str
    support_kind: str
    attack_rank: int
    direct_branch_support: bool
    may_discharge_gap: bool
    actionable_now: bool


@dataclass(frozen=True)
class SourceGapSummary:
    source_id: str
    blocker_family: str
    relative_path: str
    source_type: str
    title: str
    priority: str
    verdict_hint: str
    direct_discharge: bool
    source_exists: bool
    target_gap_ids: tuple[str, ...]
    primary_gap_id: str
    support_role: str
    actionable_now: bool
    may_discharge_gap: bool


@dataclass(frozen=True)
class GapLiteratureCoverage:
    gap_id: str
    family: str
    source_branch: str
    required_artifact_type: str
    missing_artifact: str
    attack_rank: int
    attack_note: str
    literature_source_count: int
    direct_branch_source_count: int
    source_ids: tuple[str, ...]
    coverage_status: str
    actionable_now: bool
    may_discharge_gap: bool


@dataclass(frozen=True)
class LiteratureGapMatrixCheck:
    key: str
    expected: str
    observed: str
    passed: bool
    source_artifacts: tuple[str, ...]


@dataclass(frozen=True)
class Lemma0252BlockerLiteratureGapMatrix:
    schema_version: int
    lemma_id: str
    candidate_status: str
    active_candidate: bool
    literature_index_markdown: str
    literature_index_json: str
    literature_dependency_markdown: str
    literature_dependency_json: str
    gap_index_markdown: str
    gap_index_json: str
    literature_source_count: int
    gap_count: int
    source_gap_edge_count: int
    source_with_gap_count: int
    unmapped_source_count: int
    gap_with_literature_source_count: int
    gap_without_literature_source_count: int
    direct_branch_edge_count: int
    cross_cutting_edge_count: int
    closure_bundle_edge_count: int
    blocked_gap_count: int
    actionable_gap_count: int
    may_discharge_gap_count: int
    direct_discharge_source_count: int
    literature_dependency_consistent: bool
    gap_stack_consistent: bool
    process_gate_open_authorized: bool
    blocker_state_changed: bool
    candidate_emission_authorized: bool
    missing_source_count: int
    missing_sources: tuple[str, ...]
    issues: tuple[str, ...]
    checks: tuple[LiteratureGapMatrixCheck, ...]
    source_summaries: tuple[SourceGapSummary, ...]
    gap_coverages: tuple[GapLiteratureCoverage, ...]
    edges: tuple[LiteratureGapEdge, ...]
    source_refs: tuple[str, ...]
    non_claims: tuple[str, ...]


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
) -> LiteratureGapMatrixCheck:
    return LiteratureGapMatrixCheck(
        key=key,
        expected=str(expected),
        observed=str(observed),
        passed=expected == observed,
        source_artifacts=source_artifacts,
    )


def _missing_sources(source_refs: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(source for source in source_refs if not (ROOT / source).exists())


def _gap_by_id(gap_index: dict[str, object]) -> dict[str, dict[str, object]]:
    gaps = gap_index.get("gaps", ())
    if not isinstance(gaps, list):
        raise ValueError("expected list field `gaps` in gap index")
    result: dict[str, dict[str, object]] = {}
    for gap in gaps:
        if isinstance(gap, dict):
            result[str(gap.get("gap_id"))] = gap
    return result


def _literature_sources(literature: dict[str, object]) -> tuple[dict[str, object], ...]:
    sources = literature.get("sources", ())
    if not isinstance(sources, list):
        raise ValueError("expected list field `sources` in literature index")
    return tuple(source for source in sources if isinstance(source, dict))


def _target_gap_ids(source: dict[str, object]) -> tuple[str, ...]:
    family = str(source.get("blocker_family"))
    source_id = str(source.get("source_id"))
    if family in SOURCE_BRANCH_TO_PRIMARY_GAP:
        return (SOURCE_BRANCH_TO_PRIMARY_GAP[family], *COMMON_CLOSURE_GAPS)
    if family == "cross_cutting":
        return CROSS_CUTTING_GAPS_BY_SOURCE[source_id]
    raise ValueError(f"unexpected blocker family for source {source_id}: {family}")


def _support_kind(
    *,
    source: dict[str, object],
    gap: dict[str, object],
) -> str:
    family = str(source.get("blocker_family"))
    source_id = str(source.get("source_id"))
    gap_id = str(gap.get("gap_id"))
    source_branch = str(gap.get("source_branch"))
    if source_branch == family:
        return "direct_branch_literature"
    if gap_id in COMMON_CLOSURE_GAPS:
        return "closure_bundle_support"
    if source_id == "tao_localisation_1108_1165":
        return "cross_cutting_framework_anchor"
    return "cross_cutting_caution"


def _source_summary(
    *,
    source: dict[str, object],
    target_gap_ids: tuple[str, ...],
) -> SourceGapSummary:
    primary_gap_id = target_gap_ids[0]
    family = str(source.get("blocker_family"))
    if family in SOURCE_BRANCH_TO_PRIMARY_GAP:
        support_role = "primary branch source plus closure-bundle context"
    elif str(source.get("source_id")) == "tao_localisation_1108_1165":
        support_role = "framework anchor across finite-bound and compactness branches"
    else:
        support_role = "cross-cutting caution/context only"
    return SourceGapSummary(
        source_id=str(source.get("source_id")),
        blocker_family=family,
        relative_path=str(source.get("relative_path")),
        source_type=str(source.get("source_type")),
        title=str(source.get("title")),
        priority=str(source.get("priority")),
        verdict_hint=str(source.get("verdict_hint")),
        direct_discharge=bool(source.get("direct_discharge")),
        source_exists=bool(source.get("exists")),
        target_gap_ids=target_gap_ids,
        primary_gap_id=primary_gap_id,
        support_role=support_role,
        actionable_now=False,
        may_discharge_gap=False,
    )


def _edges_for_source(
    *,
    source: dict[str, object],
    target_gap_ids: tuple[str, ...],
    gaps_by_id: dict[str, dict[str, object]],
) -> tuple[LiteratureGapEdge, ...]:
    edges: list[LiteratureGapEdge] = []
    for gap_id in target_gap_ids:
        gap = gaps_by_id[gap_id]
        support_kind = _support_kind(source=source, gap=gap)
        edges.append(
            LiteratureGapEdge(
                source_id=str(source.get("source_id")),
                blocker_family=str(source.get("blocker_family")),
                gap_id=gap_id,
                required_artifact_type=str(gap.get("required_artifact_type")),
                source_branch=str(gap.get("source_branch")),
                support_kind=support_kind,
                attack_rank=ATTACK_ORDER_BY_GAP[gap_id],
                direct_branch_support=support_kind == "direct_branch_literature",
                may_discharge_gap=False,
                actionable_now=False,
            )
        )
    return tuple(edges)


def _gap_coverages(
    *,
    edges: tuple[LiteratureGapEdge, ...],
    gaps_by_id: dict[str, dict[str, object]],
) -> tuple[GapLiteratureCoverage, ...]:
    coverages: list[GapLiteratureCoverage] = []
    for gap_id in sorted(gaps_by_id, key=lambda item: ATTACK_ORDER_BY_GAP[item]):
        gap = gaps_by_id[gap_id]
        gap_edges = tuple(edge for edge in edges if edge.gap_id == gap_id)
        direct_edges = tuple(edge for edge in gap_edges if edge.direct_branch_support)
        source_ids = tuple(edge.source_id for edge in gap_edges)
        if source_ids:
            coverage_status = "literature_mapped_but_still_blocked"
        else:
            coverage_status = "metadata_or_process_gap_no_direct_literature"
        coverages.append(
            GapLiteratureCoverage(
                gap_id=gap_id,
                family=str(gap.get("family")),
                source_branch=str(gap.get("source_branch")),
                required_artifact_type=str(gap.get("required_artifact_type")),
                missing_artifact=str(gap.get("missing_artifact")),
                attack_rank=ATTACK_ORDER_BY_GAP[gap_id],
                attack_note=GAP_ATTACK_NOTE[gap_id],
                literature_source_count=len(source_ids),
                direct_branch_source_count=len(direct_edges),
                source_ids=source_ids,
                coverage_status=coverage_status,
                actionable_now=False,
                may_discharge_gap=False,
            )
        )
    return tuple(coverages)


def build_blocker_literature_gap_matrix(
    *,
    literature_json: Path = DEFAULT_LITERATURE_JSON,
    literature_dependency_json: Path = DEFAULT_LITERATURE_DEPENDENCY_JSON,
    gap_json: Path = DEFAULT_GAP_JSON,
) -> Lemma0252BlockerLiteratureGapMatrix:
    literature = _load_json(literature_json)
    dependency = _load_json(literature_dependency_json)
    gap_index = _load_json(gap_json)
    gaps_by_id = _gap_by_id(gap_index)
    sources = _literature_sources(literature)

    source_summaries: list[SourceGapSummary] = []
    edge_list: list[LiteratureGapEdge] = []
    for source in sources:
        target_gap_ids = _target_gap_ids(source)
        source_summaries.append(
            _source_summary(source=source, target_gap_ids=target_gap_ids)
        )
        edge_list.extend(
            _edges_for_source(
                source=source,
                target_gap_ids=target_gap_ids,
                gaps_by_id=gaps_by_id,
            )
        )

    edges = tuple(edge_list)
    gap_coverages = _gap_coverages(edges=edges, gaps_by_id=gaps_by_id)
    source_refs = tuple(
        dict.fromkeys(
            (
                "track-a-regularity/reports/lemma_0252_blocker_literature_index.md",
                "track-a-regularity/reports/lemma_0252_blocker_literature_index.json",
                "track-a-regularity/reports/lemma_0252_blocker_literature_dependency.md",
                "track-a-regularity/reports/lemma_0252_blocker_literature_dependency.json",
                "track-a-regularity/reports/promotion_gate_analytic_discharge_gap_index.md",
                "track-a-regularity/reports/promotion_gate_analytic_discharge_gap_index.json",
                *tuple(str(item) for item in literature.get("source_refs", ())),
                *tuple(str(item) for item in gap_index.get("source_refs", ())),
            )
        )
    )
    missing_sources = _missing_sources(source_refs)

    source_with_gap_count = sum(1 for summary in source_summaries if summary.target_gap_ids)
    unmapped_source_count = len(source_summaries) - source_with_gap_count
    gap_with_literature_source_count = sum(
        1 for coverage in gap_coverages if coverage.literature_source_count
    )
    gap_without_literature_source_count = len(gap_coverages) - gap_with_literature_source_count
    direct_branch_edge_count = sum(1 for edge in edges if edge.direct_branch_support)
    cross_cutting_edge_count = sum(
        1 for edge in edges if edge.support_kind.startswith("cross_cutting")
    )
    closure_bundle_edge_count = sum(
        1 for edge in edges if edge.support_kind == "closure_bundle_support"
    )
    blocked_gap_count = int(gap_index.get("blocked_gap_count", 0))
    actionable_gap_count = int(gap_index.get("actionable_gap_count", 0))
    may_discharge_gap_count = int(gap_index.get("may_discharge_gap_count", 0))

    literature_source = (
        "track-a-regularity/reports/lemma_0252_blocker_literature_index.md",
        "track-a-regularity/reports/lemma_0252_blocker_literature_index.json",
    )
    dependency_source = (
        "track-a-regularity/reports/lemma_0252_blocker_literature_dependency.md",
        "track-a-regularity/reports/lemma_0252_blocker_literature_dependency.json",
    )
    gap_source = (
        "track-a-regularity/reports/promotion_gate_analytic_discharge_gap_index.md",
        "track-a-regularity/reports/promotion_gate_analytic_discharge_gap_index.json",
    )
    expected_gap_ids = tuple(sorted(gaps_by_id, key=lambda item: ATTACK_ORDER_BY_GAP[item]))
    checks = (
        _check(
            key="lemma_id.matches_literature_dependency_and_gap_index",
            expected=(dependency.get("lemma_id"), gap_index.get("lemma_id")),
            observed=(literature.get("lemma_id"), literature.get("lemma_id")),
            source_artifacts=literature_source + dependency_source + gap_source,
        ),
        _check(
            key="candidate_status.remains_needs_review",
            expected="needs_review",
            observed=literature.get("candidate_status"),
            source_artifacts=literature_source,
        ),
        _check(
            key="active_candidate.remains_false",
            expected=False,
            observed=literature.get("active_candidate"),
            source_artifacts=literature_source,
        ),
        _check(
            key="literature_source_count.expected_fifteen",
            expected=15,
            observed=len(sources),
            source_artifacts=literature_source,
        ),
        _check(
            key="gap_count.expected_eight",
            expected=8,
            observed=len(gaps_by_id),
            source_artifacts=gap_source,
        ),
        _check(
            key="gap_ids.expected_full_set",
            expected=(
                "gap_002",
                "gap_003",
                "gap_004",
                "gap_006",
                "gap_007",
                "gap_001",
                "gap_005",
                "gap_008",
            ),
            observed=expected_gap_ids,
            source_artifacts=gap_source,
        ),
        _check(
            key="all_sources_have_target_gap",
            expected=0,
            observed=unmapped_source_count,
            source_artifacts=literature_source + gap_source,
        ),
        _check(
            key="source_gap_edge_count.expected_forty_five",
            expected=45,
            observed=len(edges),
            source_artifacts=literature_source + gap_source,
        ),
        _check(
            key="gap_with_literature_source_count.expected_five",
            expected=5,
            observed=gap_with_literature_source_count,
            source_artifacts=literature_source + gap_source,
        ),
        _check(
            key="gap_without_literature_source_count.expected_three",
            expected=3,
            observed=gap_without_literature_source_count,
            source_artifacts=literature_source + gap_source,
        ),
        _check(
            key="direct_discharge_source_count.remains_zero",
            expected=0,
            observed=literature.get("direct_discharge_source_count"),
            source_artifacts=literature_source,
        ),
        _check(
            key="literature_dependency_consistent.true",
            expected=True,
            observed=dependency.get("literature_dependency_consistent"),
            source_artifacts=dependency_source,
        ),
        _check(
            key="gap_index.stack_consistent.true",
            expected=True,
            observed=gap_index.get("stack_consistent"),
            source_artifacts=gap_source,
        ),
        _check(
            key="gap_index.all_gaps_blocked",
            expected=gap_index.get("gap_count"),
            observed=blocked_gap_count,
            source_artifacts=gap_source,
        ),
        _check(
            key="actionable_gap_count.remains_zero",
            expected=0,
            observed=actionable_gap_count,
            source_artifacts=gap_source,
        ),
        _check(
            key="may_discharge_gap_count.remains_zero",
            expected=0,
            observed=may_discharge_gap_count,
            source_artifacts=gap_source,
        ),
        _check(
            key="process_gate_open_authorized.false",
            expected=(False, False, False),
            observed=(
                literature.get("process_gate_open_authorized"),
                gap_index.get("process_gate_open_authorized"),
                dependency.get("process_gate_open_authorized"),
            ),
            source_artifacts=literature_source + dependency_source + gap_source,
        ),
        _check(
            key="candidate_emission_authorized.false",
            expected=False,
            observed=(
                literature.get("candidate_emission_authorized")
                or gap_index.get("candidate_emission_authorized")
                or dependency.get("candidate_emission_authorized")
            ),
            source_artifacts=literature_source + dependency_source + gap_source,
        ),
        _check(
            key="source_refs.missing_count.remains_zero",
            expected=0,
            observed=len(missing_sources),
            source_artifacts=source_refs,
        ),
    )
    issues = tuple(check.key for check in checks if not check.passed)

    return Lemma0252BlockerLiteratureGapMatrix(
        schema_version=1,
        lemma_id=str(literature.get("lemma_id")),
        candidate_status=str(literature.get("candidate_status")),
        active_candidate=bool(literature.get("active_candidate")),
        literature_index_markdown=str(DEFAULT_LITERATURE_MARKDOWN),
        literature_index_json=str(DEFAULT_LITERATURE_JSON),
        literature_dependency_markdown=str(DEFAULT_LITERATURE_DEPENDENCY_MARKDOWN),
        literature_dependency_json=str(DEFAULT_LITERATURE_DEPENDENCY_JSON),
        gap_index_markdown=str(DEFAULT_GAP_MARKDOWN),
        gap_index_json=str(DEFAULT_GAP_JSON),
        literature_source_count=len(sources),
        gap_count=len(gaps_by_id),
        source_gap_edge_count=len(edges),
        source_with_gap_count=source_with_gap_count,
        unmapped_source_count=unmapped_source_count,
        gap_with_literature_source_count=gap_with_literature_source_count,
        gap_without_literature_source_count=gap_without_literature_source_count,
        direct_branch_edge_count=direct_branch_edge_count,
        cross_cutting_edge_count=cross_cutting_edge_count,
        closure_bundle_edge_count=closure_bundle_edge_count,
        blocked_gap_count=blocked_gap_count,
        actionable_gap_count=actionable_gap_count,
        may_discharge_gap_count=may_discharge_gap_count,
        direct_discharge_source_count=int(literature.get("direct_discharge_source_count", 0)),
        literature_dependency_consistent=bool(
            dependency.get("literature_dependency_consistent")
        ),
        gap_stack_consistent=bool(gap_index.get("stack_consistent")),
        process_gate_open_authorized=False,
        blocker_state_changed=False,
        candidate_emission_authorized=False,
        missing_source_count=len(missing_sources),
        missing_sources=missing_sources,
        issues=issues,
        checks=checks,
        source_summaries=tuple(source_summaries),
        gap_coverages=gap_coverages,
        edges=edges,
        source_refs=source_refs,
        non_claims=NON_CLAIMS,
    )


def gap_matrix_to_dict(
    matrix: Lemma0252BlockerLiteratureGapMatrix,
) -> dict[str, object]:
    return {
        "schema_version": matrix.schema_version,
        "lemma_id": matrix.lemma_id,
        "candidate_status": matrix.candidate_status,
        "active_candidate": matrix.active_candidate,
        "literature_index_markdown": matrix.literature_index_markdown,
        "literature_index_json": matrix.literature_index_json,
        "literature_dependency_markdown": matrix.literature_dependency_markdown,
        "literature_dependency_json": matrix.literature_dependency_json,
        "gap_index_markdown": matrix.gap_index_markdown,
        "gap_index_json": matrix.gap_index_json,
        "literature_source_count": matrix.literature_source_count,
        "gap_count": matrix.gap_count,
        "source_gap_edge_count": matrix.source_gap_edge_count,
        "source_with_gap_count": matrix.source_with_gap_count,
        "unmapped_source_count": matrix.unmapped_source_count,
        "gap_with_literature_source_count": matrix.gap_with_literature_source_count,
        "gap_without_literature_source_count": matrix.gap_without_literature_source_count,
        "direct_branch_edge_count": matrix.direct_branch_edge_count,
        "cross_cutting_edge_count": matrix.cross_cutting_edge_count,
        "closure_bundle_edge_count": matrix.closure_bundle_edge_count,
        "blocked_gap_count": matrix.blocked_gap_count,
        "actionable_gap_count": matrix.actionable_gap_count,
        "may_discharge_gap_count": matrix.may_discharge_gap_count,
        "direct_discharge_source_count": matrix.direct_discharge_source_count,
        "literature_dependency_consistent": matrix.literature_dependency_consistent,
        "gap_stack_consistent": matrix.gap_stack_consistent,
        "process_gate_open_authorized": matrix.process_gate_open_authorized,
        "blocker_state_changed": matrix.blocker_state_changed,
        "candidate_emission_authorized": matrix.candidate_emission_authorized,
        "missing_source_count": matrix.missing_source_count,
        "missing_sources": list(matrix.missing_sources),
        "issues": list(matrix.issues),
        "checks": [asdict(check) for check in matrix.checks],
        "source_summaries": [asdict(summary) for summary in matrix.source_summaries],
        "gap_coverages": [asdict(coverage) for coverage in matrix.gap_coverages],
        "edges": [asdict(edge) for edge in matrix.edges],
        "source_refs": list(matrix.source_refs),
        "non_claims": list(matrix.non_claims),
        "docs": {
            "step_doc": "docs/STEP108_LEMMA_0252_BLOCKER_LITERATURE_GAP_MATRIX.md",
            "literature_index_doc": "docs/STEP106_LEMMA_0252_BLOCKER_LITERATURE_INDEX.md",
            "literature_dependency_doc": (
                "docs/STEP107_LEMMA_0252_BLOCKER_LITERATURE_DEPENDENCY.md"
            ),
            "gap_index_doc": "docs/STEP102_PROMOTION_GATE_ANALYTIC_DISCHARGE_GAP_INDEX.md",
            "papers_index": "papers/blockers/index.md",
        },
    }


def _format(text: str) -> str:
    return text.replace("|", "\\|")


def _gap_rows(matrix: Lemma0252BlockerLiteratureGapMatrix) -> list[str]:
    rows = [
        "| rank | gap | branch | artifact type | sources | direct branch | coverage | note |",
        "|---:|---|---|---|---:|---:|---|---|",
    ]
    for coverage in matrix.gap_coverages:
        rows.append(
            "| "
            f"{coverage.attack_rank} | "
            f"`{coverage.gap_id}` | "
            f"`{coverage.source_branch}` | "
            f"`{coverage.required_artifact_type}` | "
            f"{coverage.literature_source_count} | "
            f"{coverage.direct_branch_source_count} | "
            f"`{coverage.coverage_status}` | "
            f"{_format(coverage.attack_note)} |"
        )
    return rows


def _source_rows(matrix: Lemma0252BlockerLiteratureGapMatrix) -> list[str]:
    rows = [
        "| source | family | priority | verdict hint | target gaps | role | direct discharge |",
        "|---|---|---|---|---|---|---|",
    ]
    for source in matrix.source_summaries:
        rows.append(
            "| "
            f"`{source.source_id}` | "
            f"`{source.blocker_family}` | "
            f"`{source.priority}` | "
            f"`{source.verdict_hint}` | "
            f"{'<br>'.join(f'`{gap}`' for gap in source.target_gap_ids)} | "
            f"{_format(source.support_role)} | "
            f"`{str(source.direct_discharge).lower()}` |"
        )
    return rows


def _check_rows(matrix: Lemma0252BlockerLiteratureGapMatrix) -> list[str]:
    rows = [
        "| check | expected | observed | passed |",
        "|---|---|---|---|",
    ]
    for check in matrix.checks:
        rows.append(
            "| "
            f"`{check.key}` | "
            f"`{_format(check.expected)}` | "
            f"`{_format(check.observed)}` | "
            f"`{str(check.passed).lower()}` |"
        )
    return rows


def render_markdown(matrix: Lemma0252BlockerLiteratureGapMatrix) -> str:
    return "\n".join(
        (
            "# Lemma 0252 Blocker Literature Gap Matrix",
            "",
            "Generated by `track-a-regularity/evaluator/lemma_0252_blocker_literature_gap_matrix.py`.",
            "",
            "This read-only dashboard maps the 15 local blocker-literature sources from Step 106",
            "onto the eight blocked analytic-discharge gaps from Step 102. It is an attack-order",
            "triage surface only; mapped literature does not discharge a blocker or authorize",
            "candidate emission.",
            "",
            "## Summary",
            "",
            f"- lemma_id: `{matrix.lemma_id}`",
            f"- candidate_status: `{matrix.candidate_status}`",
            f"- active_candidate: `{str(matrix.active_candidate).lower()}`",
            f"- literature_source_count: `{matrix.literature_source_count}`",
            f"- gap_count: `{matrix.gap_count}`",
            f"- source_gap_edge_count: `{matrix.source_gap_edge_count}`",
            f"- source_with_gap_count: `{matrix.source_with_gap_count}`",
            f"- unmapped_source_count: `{matrix.unmapped_source_count}`",
            f"- gap_with_literature_source_count: `{matrix.gap_with_literature_source_count}`",
            f"- gap_without_literature_source_count: `{matrix.gap_without_literature_source_count}`",
            f"- direct_branch_edge_count: `{matrix.direct_branch_edge_count}`",
            f"- cross_cutting_edge_count: `{matrix.cross_cutting_edge_count}`",
            f"- closure_bundle_edge_count: `{matrix.closure_bundle_edge_count}`",
            f"- blocked_gap_count: `{matrix.blocked_gap_count}`",
            f"- actionable_gap_count: `{matrix.actionable_gap_count}`",
            f"- may_discharge_gap_count: `{matrix.may_discharge_gap_count}`",
            f"- direct_discharge_source_count: `{matrix.direct_discharge_source_count}`",
            f"- literature_dependency_consistent: `{str(matrix.literature_dependency_consistent).lower()}`",
            f"- gap_stack_consistent: `{str(matrix.gap_stack_consistent).lower()}`",
            f"- process_gate_open_authorized: `{str(matrix.process_gate_open_authorized).lower()}`",
            f"- blocker_state_changed: `{str(matrix.blocker_state_changed).lower()}`",
            f"- candidate_emission_authorized: `{str(matrix.candidate_emission_authorized).lower()}`",
            f"- missing_source_count: `{matrix.missing_source_count}`",
            f"- issues: `{', '.join(matrix.issues) or 'none'}`",
            "",
            "## Gap Attack Order",
            "",
            *_gap_rows(matrix),
            "",
            "## Source To Gap Map",
            "",
            *_source_rows(matrix),
            "",
            "## Consistency Checks",
            "",
            *_check_rows(matrix),
            "",
            "## Non-Claims",
            "",
            *(f"- `{item}`" for item in matrix.non_claims),
            "",
        )
    )


def render_json(matrix: Lemma0252BlockerLiteratureGapMatrix) -> str:
    return json.dumps(gap_matrix_to_dict(matrix), indent=2, sort_keys=True) + "\n"


def render_output(
    matrix: Lemma0252BlockerLiteratureGapMatrix,
    output_format: str,
) -> str:
    if output_format == "markdown":
        return render_markdown(matrix)
    if output_format == "json":
        return render_json(matrix)
    raise ValueError(f"unknown blocker literature gap matrix format: {output_format}")


def write_output(
    output: Path,
    matrix: Lemma0252BlockerLiteratureGapMatrix,
    output_format: str,
) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_output(matrix, output_format), encoding="utf-8")
    return output


def check_output(
    output: Path,
    matrix: Lemma0252BlockerLiteratureGapMatrix,
    output_format: str,
) -> tuple[bool, str]:
    expected = render_output(matrix, output_format)
    if not output.exists():
        return False, f"missing lemma_0252 blocker literature gap matrix: {output}"
    current = output.read_text(encoding="utf-8")
    if current != expected:
        return False, f"stale lemma_0252 blocker literature gap matrix: {output}"
    return True, f"fresh lemma_0252 blocker literature gap matrix: {output}"


def check_sources(matrix: Lemma0252BlockerLiteratureGapMatrix) -> tuple[bool, str]:
    if matrix.missing_source_count:
        return False, "missing blocker literature gap matrix sources: " + ", ".join(
            matrix.missing_sources
        )
    return True, "all blocker literature gap matrix sources exist"


def check_consistent(matrix: Lemma0252BlockerLiteratureGapMatrix) -> tuple[bool, str]:
    if matrix.issues:
        return False, "blocker literature gap matrix has issues: " + ", ".join(
            matrix.issues
        )
    if not matrix.literature_dependency_consistent:
        return False, "literature dependency guard is inconsistent"
    if not matrix.gap_stack_consistent:
        return False, "analytic gap stack is inconsistent"
    return True, "blocker literature gap matrix is consistent"


def check_blocked(matrix: Lemma0252BlockerLiteratureGapMatrix) -> tuple[bool, str]:
    if matrix.process_gate_open_authorized:
        return False, "process gate open became authorized"
    if matrix.blocker_state_changed:
        return False, "literature gap matrix changed blocker state"
    if matrix.candidate_emission_authorized:
        return False, "literature gap matrix authorized candidate emission"
    if matrix.actionable_gap_count:
        return False, "literature gap matrix marked a gap actionable"
    if matrix.may_discharge_gap_count:
        return False, "literature gap matrix marked a gap as blocker-discharge capable"
    if matrix.direct_discharge_source_count:
        return False, "literature gap matrix found a direct discharge source"
    return True, "blocker literature gap matrix keeps all gaps blocked"


def default_output_path(output_format: str) -> Path:
    if output_format == "markdown":
        return DEFAULT_MARKDOWN_OUTPUT
    if output_format == "json":
        return DEFAULT_JSON_OUTPUT
    raise ValueError(f"unknown blocker literature gap matrix format: {output_format}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Render a read-only literature-to-gap attack-order matrix for lemma_0252."
    )
    parser.add_argument("--literature-json", type=Path, default=DEFAULT_LITERATURE_JSON)
    parser.add_argument(
        "--literature-dependency-json",
        type=Path,
        default=DEFAULT_LITERATURE_DEPENDENCY_JSON,
    )
    parser.add_argument("--gap-json", type=Path, default=DEFAULT_GAP_JSON)
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--check-output", action="store_true")
    parser.add_argument("--require-sources-exist", action="store_true")
    parser.add_argument("--require-consistent", action="store_true")
    parser.add_argument("--require-blocked", action="store_true")
    args = parser.parse_args(argv)

    try:
        matrix = build_blocker_literature_gap_matrix(
            literature_json=args.literature_json,
            literature_dependency_json=args.literature_dependency_json,
            gap_json=args.gap_json,
        )
    except Exception as exc:  # noqa: BLE001 - CLI should report setup failures.
        print(f"failed to build blocker literature gap matrix: {exc}", file=sys.stderr)
        return 1

    output = args.output or default_output_path(args.format)
    if args.check_output:
        ok, message = check_output(output, matrix, args.format)
        print(message)
        if not ok:
            print(
                "run without --check-output to regenerate the blocker literature gap matrix",
                file=sys.stderr,
            )
            return 1
    else:
        written = write_output(output, matrix, args.format)
        print(f"wrote {written}")

    if args.require_sources_exist:
        ok, message = check_sources(matrix)
        print(message)
        if not ok:
            return 1
    if args.require_consistent:
        ok, message = check_consistent(matrix)
        print(message)
        if not ok:
            return 1
    if args.require_blocked:
        ok, message = check_blocked(matrix)
        print(message)
        if not ok:
            return 1

    print(f"literature_source_count: {matrix.literature_source_count}")
    print(f"gap_count: {matrix.gap_count}")
    print(f"source_gap_edge_count: {matrix.source_gap_edge_count}")
    print(f"unmapped_source_count: {matrix.unmapped_source_count}")
    print(f"gap_with_literature_source_count: {matrix.gap_with_literature_source_count}")
    print(f"gap_without_literature_source_count: {matrix.gap_without_literature_source_count}")
    print(f"candidate_emission_authorized: {str(matrix.candidate_emission_authorized).lower()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
