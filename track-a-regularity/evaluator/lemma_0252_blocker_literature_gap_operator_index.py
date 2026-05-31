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


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REPORT_DIR = ROOT / "track-a-regularity/reports"
DEFAULT_MARKDOWN_OUTPUT = (
    DEFAULT_REPORT_DIR / "lemma_0252_blocker_literature_gap_operator_index.md"
)
DEFAULT_JSON_OUTPUT = (
    DEFAULT_REPORT_DIR / "lemma_0252_blocker_literature_gap_operator_index.json"
)

NON_CLAIMS = (
    "read_only_literature_gap_operator_index",
    "source_index_for_review_only",
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


@dataclass(frozen=True)
class LiteratureGapOperatorSection:
    step: int
    name: str
    role: str
    markdown_report: str
    json_report: str
    status: str
    primary_count_label: str
    primary_count: int
    blocked_count: int
    actionable_count: int
    consistent: bool
    missing_source_count: int


@dataclass(frozen=True)
class LiteratureGapOperatorCheck:
    key: str
    expected: str
    observed: str
    passed: bool
    source_artifacts: tuple[str, ...]


@dataclass(frozen=True)
class Lemma0252BlockerLiteratureGapOperatorIndex:
    schema_version: int
    lemma_id: str
    candidate_status: str
    active_candidate: bool
    section_count: int
    source_report_count: int
    source_ref_count: int
    literature_source_count: int
    gap_count: int
    source_gap_edge_count: int
    source_with_gap_count: int
    unmapped_source_count: int
    gap_with_literature_source_count: int
    gap_without_literature_source_count: int
    direct_branch_edge_count: int
    closure_bundle_edge_count: int
    blocked_gap_count: int
    actionable_gap_count: int
    may_discharge_gap_count: int
    direct_discharge_source_count: int
    literature_gap_dependency_check_count: int
    failed_literature_gap_dependency_check_count: int
    literature_gap_dependency_consistent: bool
    analytic_gap_stack_consistent: bool
    operator_stack_consistent: bool
    literature_gap_operator_index_check_count: int
    passed_literature_gap_operator_index_check_count: int
    failed_literature_gap_operator_index_check_count: int
    literature_gap_operator_index_consistent: bool
    process_gate_open_authorized: bool
    blocker_state_changed: bool
    candidate_emission_authorized: bool
    missing_source_count: int
    missing_sources: tuple[str, ...]
    issues: tuple[str, ...]
    sections: tuple[LiteratureGapOperatorSection, ...]
    checks: tuple[LiteratureGapOperatorCheck, ...]
    source_refs: tuple[str, ...]
    non_claims: tuple[str, ...]
    literature_gap_matrix_snapshot: dict[str, object]
    literature_gap_dependency_snapshot: dict[str, object]


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
) -> LiteratureGapOperatorCheck:
    return LiteratureGapOperatorCheck(
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
        "track-a-regularity/reports/lemma_0252_blocker_literature_gap_matrix.md",
        "track-a-regularity/reports/lemma_0252_blocker_literature_gap_matrix.json",
        "track-a-regularity/reports/lemma_0252_blocker_literature_gap_dependency.md",
        "track-a-regularity/reports/lemma_0252_blocker_literature_gap_dependency.json",
    )


def _sections(
    matrix: dict[str, object],
    dependency: dict[str, object],
) -> tuple[LiteratureGapOperatorSection, ...]:
    return (
        LiteratureGapOperatorSection(
            step=108,
            name="blocker_literature_gap_matrix",
            role=(
                "Maps local blocker literature sources onto blocked analytic-discharge "
                "gaps and records attack-order triage."
            ),
            markdown_report=str(DEFAULT_GAP_MATRIX_MARKDOWN),
            json_report=str(DEFAULT_GAP_MATRIX_JSON),
            status="blocked_literature_gap_matrix",
            primary_count_label="source_gap_edge_count",
            primary_count=int(matrix.get("source_gap_edge_count", 0)),
            blocked_count=int(matrix.get("blocked_gap_count", 0)),
            actionable_count=int(matrix.get("actionable_gap_count", 0))
            + int(matrix.get("may_discharge_gap_count", 0)),
            consistent=bool(matrix.get("literature_dependency_consistent"))
            and bool(matrix.get("gap_stack_consistent"))
            and not matrix.get("issues"),
            missing_source_count=int(matrix.get("missing_source_count", 0)),
        ),
        LiteratureGapOperatorSection(
            step=109,
            name="blocker_literature_gap_dependency",
            role=(
                "Keeps the literature-gap matrix synchronized with the literature index, "
                "literature dependency guard, analytic gap index, and operator dashboard."
            ),
            markdown_report=str(DEFAULT_GAP_DEPENDENCY_MARKDOWN),
            json_report=str(DEFAULT_GAP_DEPENDENCY_JSON),
            status="literature_gap_dependency_guard",
            primary_count_label="literature_gap_dependency_check_count",
            primary_count=int(dependency.get("literature_gap_dependency_check_count", 0)),
            blocked_count=int(dependency.get("blocked_gap_count", 0)),
            actionable_count=int(dependency.get("actionable_gap_count", 0))
            + int(dependency.get("may_discharge_gap_count", 0)),
            consistent=bool(dependency.get("literature_gap_dependency_consistent")),
            missing_source_count=int(dependency.get("missing_source_count", 0)),
        ),
    )


def build_blocker_literature_gap_operator_index(
    *,
    literature_gap_matrix_json: Path = DEFAULT_GAP_MATRIX_JSON,
    literature_gap_dependency_json: Path = DEFAULT_GAP_DEPENDENCY_JSON,
) -> Lemma0252BlockerLiteratureGapOperatorIndex:
    matrix = _load_json(literature_gap_matrix_json)
    dependency = _load_json(literature_gap_dependency_json)

    matrix_source = (
        "track-a-regularity/reports/lemma_0252_blocker_literature_gap_matrix.md",
        "track-a-regularity/reports/lemma_0252_blocker_literature_gap_matrix.json",
    )
    dependency_source = (
        "track-a-regularity/reports/lemma_0252_blocker_literature_gap_dependency.md",
        "track-a-regularity/reports/lemma_0252_blocker_literature_gap_dependency.json",
    )
    source_refs = tuple(
        dict.fromkeys(
            _direct_sources()
            + tuple(str(item) for item in matrix.get("source_refs", ()))
            + tuple(str(item) for item in dependency.get("source_refs", ()))
        )
    )
    missing_sources = _missing_sources(source_refs)
    sections = _sections(matrix, dependency)

    checks = (
        _check(
            key="matrix.lemma_id.matches_dependency",
            expected=dependency.get("lemma_id"),
            observed=matrix.get("lemma_id"),
            source_artifacts=matrix_source + dependency_source,
        ),
        _check(
            key="matrix.candidate_status.matches_dependency",
            expected=dependency.get("candidate_status"),
            observed=matrix.get("candidate_status"),
            source_artifacts=matrix_source + dependency_source,
        ),
        _check(
            key="matrix.active_candidate.matches_dependency",
            expected=dependency.get("active_candidate"),
            observed=matrix.get("active_candidate"),
            source_artifacts=matrix_source + dependency_source,
        ),
        _check(
            key="matrix.literature_source_count.matches_dependency",
            expected=dependency.get("literature_source_count"),
            observed=matrix.get("literature_source_count"),
            source_artifacts=matrix_source + dependency_source,
        ),
        _check(
            key="matrix.gap_count.matches_dependency",
            expected=dependency.get("gap_count"),
            observed=matrix.get("gap_count"),
            source_artifacts=matrix_source + dependency_source,
        ),
        _check(
            key="matrix.source_gap_edge_count.matches_dependency",
            expected=dependency.get("source_gap_edge_count"),
            observed=matrix.get("source_gap_edge_count"),
            source_artifacts=matrix_source + dependency_source,
        ),
        _check(
            key="matrix.source_with_gap_count.matches_dependency",
            expected=dependency.get("source_with_gap_count"),
            observed=matrix.get("source_with_gap_count"),
            source_artifacts=matrix_source + dependency_source,
        ),
        _check(
            key="matrix.unmapped_source_count.remains_zero",
            expected=0,
            observed=matrix.get("unmapped_source_count"),
            source_artifacts=matrix_source,
        ),
        _check(
            key="matrix.gap_with_literature_source_count.matches_dependency",
            expected=dependency.get("gap_with_literature_source_count"),
            observed=matrix.get("gap_with_literature_source_count"),
            source_artifacts=matrix_source + dependency_source,
        ),
        _check(
            key="matrix.gap_without_literature_source_count.matches_dependency",
            expected=dependency.get("gap_without_literature_source_count"),
            observed=matrix.get("gap_without_literature_source_count"),
            source_artifacts=matrix_source + dependency_source,
        ),
        _check(
            key="matrix.direct_branch_edge_count.matches_dependency",
            expected=dependency.get("direct_branch_edge_count"),
            observed=matrix.get("direct_branch_edge_count"),
            source_artifacts=matrix_source + dependency_source,
        ),
        _check(
            key="matrix.closure_bundle_edge_count.matches_dependency",
            expected=dependency.get("closure_bundle_edge_count"),
            observed=matrix.get("closure_bundle_edge_count"),
            source_artifacts=matrix_source + dependency_source,
        ),
        _check(
            key="matrix.blocked_gap_count.matches_dependency",
            expected=dependency.get("blocked_gap_count"),
            observed=matrix.get("blocked_gap_count"),
            source_artifacts=matrix_source + dependency_source,
        ),
        _check(
            key="matrix.actionable_gap_count.remains_zero",
            expected=0,
            observed=matrix.get("actionable_gap_count"),
            source_artifacts=matrix_source,
        ),
        _check(
            key="dependency.actionable_gap_count.remains_zero",
            expected=0,
            observed=dependency.get("actionable_gap_count"),
            source_artifacts=dependency_source,
        ),
        _check(
            key="matrix.may_discharge_gap_count.remains_zero",
            expected=0,
            observed=matrix.get("may_discharge_gap_count"),
            source_artifacts=matrix_source,
        ),
        _check(
            key="dependency.may_discharge_gap_count.remains_zero",
            expected=0,
            observed=dependency.get("may_discharge_gap_count"),
            source_artifacts=dependency_source,
        ),
        _check(
            key="matrix.direct_discharge_source_count.matches_dependency",
            expected=dependency.get("direct_discharge_source_count"),
            observed=matrix.get("direct_discharge_source_count"),
            source_artifacts=matrix_source + dependency_source,
        ),
        _check(
            key="matrix.literature_dependency_consistent.true",
            expected=True,
            observed=matrix.get("literature_dependency_consistent"),
            source_artifacts=matrix_source,
        ),
        _check(
            key="dependency.literature_gap_dependency_consistent.true",
            expected=True,
            observed=dependency.get("literature_gap_dependency_consistent"),
            source_artifacts=dependency_source,
        ),
        _check(
            key="dependency.failed_literature_gap_dependency_check_count.remains_zero",
            expected=0,
            observed=dependency.get("failed_literature_gap_dependency_check_count"),
            source_artifacts=dependency_source,
        ),
        _check(
            key="matrix.gap_stack_consistent.true",
            expected=True,
            observed=matrix.get("gap_stack_consistent"),
            source_artifacts=matrix_source,
        ),
        _check(
            key="dependency.analytic_gap_stack_consistent.true",
            expected=True,
            observed=dependency.get("analytic_gap_stack_consistent"),
            source_artifacts=dependency_source,
        ),
        _check(
            key="dependency.operator_stack_consistent.true",
            expected=True,
            observed=dependency.get("operator_stack_consistent"),
            source_artifacts=dependency_source,
        ),
        _check(
            key="source_reports.issues.all_empty",
            expected=((), ()),
            observed=(
                tuple(matrix.get("issues", ())),
                tuple(dependency.get("issues", ())),
            ),
            source_artifacts=matrix_source + dependency_source,
        ),
        _check(
            key="source_report_count.matches_sections_times_two",
            expected=len(sections) * 2,
            observed=len(_direct_sources()),
            source_artifacts=matrix_source + dependency_source,
        ),
        _check(
            key="all.process_gate_open_authorized.false",
            expected=(False, False),
            observed=(
                matrix.get("process_gate_open_authorized"),
                dependency.get("process_gate_open_authorized"),
            ),
            source_artifacts=matrix_source + dependency_source,
        ),
        _check(
            key="all.blocker_state_changed.false",
            expected=(False, False),
            observed=(
                matrix.get("blocker_state_changed"),
                dependency.get("blocker_state_changed"),
            ),
            source_artifacts=matrix_source + dependency_source,
        ),
        _check(
            key="all.candidate_emission_authorized.false",
            expected=(False, False),
            observed=(
                matrix.get("candidate_emission_authorized"),
                dependency.get("candidate_emission_authorized"),
            ),
            source_artifacts=matrix_source + dependency_source,
        ),
        _check(
            key="source_refs.missing_count.remains_zero",
            expected=0,
            observed=len(missing_sources),
            source_artifacts=source_refs,
        ),
    )

    issues = tuple(check.key for check in checks if not check.passed)
    failed_count = len(issues)
    operator_index_consistent = failed_count == 0 and not missing_sources

    return Lemma0252BlockerLiteratureGapOperatorIndex(
        schema_version=1,
        lemma_id=str(matrix.get("lemma_id")),
        candidate_status=str(matrix.get("candidate_status")),
        active_candidate=bool(matrix.get("active_candidate")),
        section_count=len(sections),
        source_report_count=len(_direct_sources()),
        source_ref_count=len(source_refs),
        literature_source_count=int(matrix.get("literature_source_count", 0)),
        gap_count=int(matrix.get("gap_count", 0)),
        source_gap_edge_count=int(matrix.get("source_gap_edge_count", 0)),
        source_with_gap_count=int(matrix.get("source_with_gap_count", 0)),
        unmapped_source_count=int(matrix.get("unmapped_source_count", 0)),
        gap_with_literature_source_count=int(
            matrix.get("gap_with_literature_source_count", 0)
        ),
        gap_without_literature_source_count=int(
            matrix.get("gap_without_literature_source_count", 0)
        ),
        direct_branch_edge_count=int(matrix.get("direct_branch_edge_count", 0)),
        closure_bundle_edge_count=int(matrix.get("closure_bundle_edge_count", 0)),
        blocked_gap_count=int(matrix.get("blocked_gap_count", 0)),
        actionable_gap_count=int(matrix.get("actionable_gap_count", 0)),
        may_discharge_gap_count=int(matrix.get("may_discharge_gap_count", 0)),
        direct_discharge_source_count=int(matrix.get("direct_discharge_source_count", 0)),
        literature_gap_dependency_check_count=int(
            dependency.get("literature_gap_dependency_check_count", 0)
        ),
        failed_literature_gap_dependency_check_count=int(
            dependency.get("failed_literature_gap_dependency_check_count", 0)
        ),
        literature_gap_dependency_consistent=bool(
            dependency.get("literature_gap_dependency_consistent")
        ),
        analytic_gap_stack_consistent=bool(
            dependency.get("analytic_gap_stack_consistent")
        ),
        operator_stack_consistent=bool(dependency.get("operator_stack_consistent")),
        literature_gap_operator_index_check_count=len(checks),
        passed_literature_gap_operator_index_check_count=len(checks) - failed_count,
        failed_literature_gap_operator_index_check_count=failed_count,
        literature_gap_operator_index_consistent=operator_index_consistent,
        process_gate_open_authorized=bool(matrix.get("process_gate_open_authorized"))
        or bool(dependency.get("process_gate_open_authorized")),
        blocker_state_changed=bool(matrix.get("blocker_state_changed"))
        or bool(dependency.get("blocker_state_changed")),
        candidate_emission_authorized=bool(matrix.get("candidate_emission_authorized"))
        or bool(dependency.get("candidate_emission_authorized")),
        missing_source_count=len(missing_sources),
        missing_sources=missing_sources,
        issues=issues,
        sections=sections,
        checks=checks,
        source_refs=source_refs,
        non_claims=NON_CLAIMS,
        literature_gap_matrix_snapshot=matrix,
        literature_gap_dependency_snapshot=dependency,
    )


def literature_gap_operator_index_to_dict(
    report: Lemma0252BlockerLiteratureGapOperatorIndex,
) -> dict[str, object]:
    return {
        "schema_version": report.schema_version,
        "lemma_id": report.lemma_id,
        "candidate_status": report.candidate_status,
        "active_candidate": report.active_candidate,
        "section_count": report.section_count,
        "source_report_count": report.source_report_count,
        "source_ref_count": report.source_ref_count,
        "literature_source_count": report.literature_source_count,
        "gap_count": report.gap_count,
        "source_gap_edge_count": report.source_gap_edge_count,
        "source_with_gap_count": report.source_with_gap_count,
        "unmapped_source_count": report.unmapped_source_count,
        "gap_with_literature_source_count": report.gap_with_literature_source_count,
        "gap_without_literature_source_count": report.gap_without_literature_source_count,
        "direct_branch_edge_count": report.direct_branch_edge_count,
        "closure_bundle_edge_count": report.closure_bundle_edge_count,
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
        "literature_gap_dependency_consistent": (
            report.literature_gap_dependency_consistent
        ),
        "analytic_gap_stack_consistent": report.analytic_gap_stack_consistent,
        "operator_stack_consistent": report.operator_stack_consistent,
        "literature_gap_operator_index_check_count": (
            report.literature_gap_operator_index_check_count
        ),
        "passed_literature_gap_operator_index_check_count": (
            report.passed_literature_gap_operator_index_check_count
        ),
        "failed_literature_gap_operator_index_check_count": (
            report.failed_literature_gap_operator_index_check_count
        ),
        "literature_gap_operator_index_consistent": (
            report.literature_gap_operator_index_consistent
        ),
        "process_gate_open_authorized": report.process_gate_open_authorized,
        "blocker_state_changed": report.blocker_state_changed,
        "candidate_emission_authorized": report.candidate_emission_authorized,
        "missing_source_count": report.missing_source_count,
        "missing_sources": list(report.missing_sources),
        "issues": list(report.issues),
        "sections": [asdict(section) for section in report.sections],
        "checks": [asdict(check) for check in report.checks],
        "source_refs": list(report.source_refs),
        "non_claims": list(report.non_claims),
        "literature_gap_matrix_snapshot": report.literature_gap_matrix_snapshot,
        "literature_gap_dependency_snapshot": report.literature_gap_dependency_snapshot,
        "docs": {
            "step_doc": (
                "docs/STEP110_LEMMA_0252_BLOCKER_LITERATURE_GAP_OPERATOR_INDEX.md"
            ),
            "gap_matrix_doc": (
                "docs/STEP108_LEMMA_0252_BLOCKER_LITERATURE_GAP_MATRIX.md"
            ),
            "gap_dependency_doc": (
                "docs/STEP109_LEMMA_0252_BLOCKER_LITERATURE_GAP_DEPENDENCY.md"
            ),
        },
    }


def _format(text: str) -> str:
    return text.replace("|", "\\|")


def _section_rows(report: Lemma0252BlockerLiteratureGapOperatorIndex) -> list[str]:
    rows = [
        "| step | section | status | primary | blocked | actionable | consistent | sources |",
        "|---:|---|---|---:|---:|---:|---|---|",
    ]
    for section in report.sections:
        sources = "<br>".join(
            (f"`{section.markdown_report}`", f"`{section.json_report}`")
        )
        rows.append(
            "| "
            f"{section.step} | "
            f"`{section.name}` | "
            f"`{section.status}` | "
            f"{section.primary_count} `{section.primary_count_label}` | "
            f"{section.blocked_count} | "
            f"{section.actionable_count} | "
            f"`{str(section.consistent).lower()}` | "
            f"{sources} |"
        )
    return rows


def _check_rows(report: Lemma0252BlockerLiteratureGapOperatorIndex) -> list[str]:
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


def render_markdown(report: Lemma0252BlockerLiteratureGapOperatorIndex) -> str:
    return "\n".join(
        (
            "# Lemma 0252 Blocker Literature Gap Operator Index",
            "",
            "Generated by `track-a-regularity/evaluator/lemma_0252_blocker_literature_gap_operator_index.py`.",
            "",
            "This read-only operator/source index consolidates the Step 108 literature-gap",
            "matrix and the Step 109 literature-gap dependency guard for future analytic",
            "review. It is an inspection surface only; it does not discharge blockers or",
            "authorize process gates.",
            "",
            "## Summary",
            "",
            f"- lemma_id: `{report.lemma_id}`",
            f"- candidate_status: `{report.candidate_status}`",
            f"- active_candidate: `{str(report.active_candidate).lower()}`",
            f"- section_count: `{report.section_count}`",
            f"- source_report_count: `{report.source_report_count}`",
            f"- source_ref_count: `{report.source_ref_count}`",
            f"- literature_source_count: `{report.literature_source_count}`",
            f"- gap_count: `{report.gap_count}`",
            f"- source_gap_edge_count: `{report.source_gap_edge_count}`",
            f"- source_with_gap_count: `{report.source_with_gap_count}`",
            f"- unmapped_source_count: `{report.unmapped_source_count}`",
            f"- gap_with_literature_source_count: `{report.gap_with_literature_source_count}`",
            f"- gap_without_literature_source_count: `{report.gap_without_literature_source_count}`",
            f"- direct_branch_edge_count: `{report.direct_branch_edge_count}`",
            f"- closure_bundle_edge_count: `{report.closure_bundle_edge_count}`",
            f"- blocked_gap_count: `{report.blocked_gap_count}`",
            f"- actionable_gap_count: `{report.actionable_gap_count}`",
            f"- may_discharge_gap_count: `{report.may_discharge_gap_count}`",
            f"- direct_discharge_source_count: `{report.direct_discharge_source_count}`",
            f"- literature_gap_dependency_check_count: `{report.literature_gap_dependency_check_count}`",
            f"- failed_literature_gap_dependency_check_count: `{report.failed_literature_gap_dependency_check_count}`",
            f"- literature_gap_dependency_consistent: `{str(report.literature_gap_dependency_consistent).lower()}`",
            f"- analytic_gap_stack_consistent: `{str(report.analytic_gap_stack_consistent).lower()}`",
            f"- operator_stack_consistent: `{str(report.operator_stack_consistent).lower()}`",
            f"- literature_gap_operator_index_check_count: `{report.literature_gap_operator_index_check_count}`",
            f"- passed_literature_gap_operator_index_check_count: `{report.passed_literature_gap_operator_index_check_count}`",
            f"- failed_literature_gap_operator_index_check_count: `{report.failed_literature_gap_operator_index_check_count}`",
            f"- literature_gap_operator_index_consistent: `{str(report.literature_gap_operator_index_consistent).lower()}`",
            f"- process_gate_open_authorized: `{str(report.process_gate_open_authorized).lower()}`",
            f"- blocker_state_changed: `{str(report.blocker_state_changed).lower()}`",
            f"- candidate_emission_authorized: `{str(report.candidate_emission_authorized).lower()}`",
            f"- missing_source_count: `{report.missing_source_count}`",
            f"- issues: `{', '.join(report.issues) or 'none'}`",
            "",
            "## Sections",
            "",
            *_section_rows(report),
            "",
            "## Operator Checks",
            "",
            *_check_rows(report),
            "",
            "## Non-Claims",
            "",
            *(f"- `{item}`" for item in report.non_claims),
            "",
        )
    )


def render_json(report: Lemma0252BlockerLiteratureGapOperatorIndex) -> str:
    return json.dumps(
        literature_gap_operator_index_to_dict(report),
        indent=2,
        sort_keys=True,
    ) + "\n"


def render_output(
    report: Lemma0252BlockerLiteratureGapOperatorIndex,
    output_format: str,
) -> str:
    if output_format == "markdown":
        return render_markdown(report)
    if output_format == "json":
        return render_json(report)
    raise ValueError(f"unknown literature gap operator index format: {output_format}")


def write_output(
    output: Path,
    report: Lemma0252BlockerLiteratureGapOperatorIndex,
    output_format: str,
) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_output(report, output_format), encoding="utf-8")
    return output


def check_output(
    output: Path,
    report: Lemma0252BlockerLiteratureGapOperatorIndex,
    output_format: str,
) -> tuple[bool, str]:
    expected = render_output(report, output_format)
    if not output.exists():
        return False, f"missing lemma_0252 blocker literature gap operator index: {output}"
    current = output.read_text(encoding="utf-8")
    if current != expected:
        return False, f"stale lemma_0252 blocker literature gap operator index: {output}"
    return True, f"fresh lemma_0252 blocker literature gap operator index: {output}"


def check_consistent(
    report: Lemma0252BlockerLiteratureGapOperatorIndex,
) -> tuple[bool, str]:
    if not report.literature_gap_operator_index_consistent:
        return (
            False,
            "lemma_0252 blocker literature gap operator index inconsistent: "
            + ", ".join(report.issues),
        )
    return True, "lemma_0252 blocker literature gap operator index is consistent"


def check_sources(
    report: Lemma0252BlockerLiteratureGapOperatorIndex,
) -> tuple[bool, str]:
    if report.missing_source_count:
        return (
            False,
            "missing lemma_0252 blocker literature gap operator index sources: "
            + ", ".join(report.missing_sources),
        )
    return True, "all lemma_0252 blocker literature gap operator index sources exist"


def check_blocked(
    report: Lemma0252BlockerLiteratureGapOperatorIndex,
) -> tuple[bool, str]:
    if report.process_gate_open_authorized:
        return False, "process gate open became authorized"
    if report.blocker_state_changed:
        return False, "literature gap operator index changed blocker state"
    if report.candidate_emission_authorized:
        return False, "literature gap operator index authorized candidate emission"
    if report.actionable_gap_count:
        return False, "literature gap operator index found actionable gaps"
    if report.may_discharge_gap_count:
        return False, "literature gap operator index found discharge-capable gaps"
    if report.direct_discharge_source_count:
        return False, "literature gap operator index found direct discharge sources"
    if report.blocked_gap_count != report.gap_count:
        return False, "not all literature-linked gaps remain blocked"
    return True, "lemma_0252 blocker literature gap operator index keeps gaps blocked"


def default_output_path(output_format: str) -> Path:
    if output_format == "markdown":
        return DEFAULT_MARKDOWN_OUTPUT
    if output_format == "json":
        return DEFAULT_JSON_OUTPUT
    raise ValueError(f"unknown literature gap operator index format: {output_format}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Summarize Step 108-109 lemma_0252 literature-gap artifacts."
    )
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--check-output", action="store_true")
    parser.add_argument("--require-consistent", action="store_true")
    parser.add_argument("--require-sources-exist", action="store_true")
    parser.add_argument("--require-blocked", action="store_true")
    args = parser.parse_args(argv)

    try:
        report = build_blocker_literature_gap_operator_index()
    except Exception as exc:  # noqa: BLE001 - CLI should report setup failures.
        print(f"failed to build lemma_0252 blocker literature gap operator index: {exc}", file=sys.stderr)
        return 1

    output = args.output or default_output_path(args.format)
    if args.check_output:
        ok, message = check_output(output, report, args.format)
        print(message)
        if not ok:
            print(
                "run without --check-output to regenerate the literature gap operator index",
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
        "literature_gap_operator_index_check_count: "
        f"{report.literature_gap_operator_index_check_count}"
    )
    print(
        "passed_literature_gap_operator_index_check_count: "
        f"{report.passed_literature_gap_operator_index_check_count}"
    )
    print(
        "failed_literature_gap_operator_index_check_count: "
        f"{report.failed_literature_gap_operator_index_check_count}"
    )
    print(
        "literature_gap_operator_index_consistent: "
        f"{str(report.literature_gap_operator_index_consistent).lower()}"
    )
    print(
        "process_gate_open_authorized: "
        f"{str(report.process_gate_open_authorized).lower()}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
