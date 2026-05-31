from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from promotion_gate_analytic_discharge_template_dependency import (
    DEFAULT_JSON_OUTPUT as DEFAULT_TEMPLATE_DEPENDENCY_JSON_OUTPUT,
    DEFAULT_MARKDOWN_OUTPUT as DEFAULT_TEMPLATE_DEPENDENCY_MARKDOWN_OUTPUT,
    build_analytic_discharge_template_dependency_report,
)
from promotion_gate_analytic_discharge_templates import (
    DEFAULT_JSON_OUTPUT as DEFAULT_TEMPLATE_JSON_OUTPUT,
    DEFAULT_MARKDOWN_OUTPUT as DEFAULT_TEMPLATE_MARKDOWN_OUTPUT,
    build_analytic_discharge_template_audit,
)
from promotion_gate_analytic_prerequisite_dependency import (
    DEFAULT_JSON_OUTPUT as DEFAULT_DEPENDENCY_JSON_OUTPUT,
    DEFAULT_MARKDOWN_OUTPUT as DEFAULT_DEPENDENCY_MARKDOWN_OUTPUT,
    build_analytic_prerequisite_dependency_report,
)
from promotion_gate_analytic_prerequisites import (
    DEFAULT_JSON_OUTPUT as DEFAULT_PACKET_JSON_OUTPUT,
    DEFAULT_MARKDOWN_OUTPUT as DEFAULT_PACKET_MARKDOWN_OUTPUT,
    build_analytic_prerequisite_packet,
)
from promotion_gate_analytic_work_order_matrix import (
    DEFAULT_JSON_OUTPUT as DEFAULT_MATRIX_JSON_OUTPUT,
    DEFAULT_MARKDOWN_OUTPUT as DEFAULT_MATRIX_MARKDOWN_OUTPUT,
    build_analytic_work_order_matrix,
)
from promotion_gate_regression import DEFAULT_CANDIDATE_DIR, DEFAULT_SMOKE_SUMMARY
from proof_obligation_blockers import DEFAULT_INPUT as DEFAULT_PROOF_GRAPH_JSON


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REPORT_DIR = ROOT / "track-a-regularity/reports"
DEFAULT_MARKDOWN_OUTPUT = (
    DEFAULT_REPORT_DIR / "promotion_gate_analytic_discharge_operator_dashboard.md"
)
DEFAULT_JSON_OUTPUT = (
    DEFAULT_REPORT_DIR / "promotion_gate_analytic_discharge_operator_dashboard.json"
)

STEP_DOC_REFS = (
    "docs/STEP96_PROMOTION_GATE_ANALYTIC_PREREQUISITES.md",
    "docs/STEP97_PROMOTION_GATE_ANALYTIC_PREREQUISITE_DEPENDENCY.md",
    "docs/STEP98_PROMOTION_GATE_ANALYTIC_WORK_ORDER_MATRIX.md",
    "docs/STEP99_PROMOTION_GATE_ANALYTIC_DISCHARGE_TEMPLATES.md",
    "docs/STEP100_PROMOTION_GATE_ANALYTIC_DISCHARGE_TEMPLATE_DEPENDENCY.md",
)

NON_CLAIMS = (
    "analytic_discharge_operator_dashboard_only",
    "read_only_consolidated_index",
    "no_process_gate_opened",
    "no_file_copy",
    "no_candidate_emission",
    "no_candidate_promotion",
    "no_blocker_discharge",
    "no_navier_stokes_solution",
    "no_epsilon_regularity_theorem",
    "no_compactness_or_liouville_theorem",
    "no_weak_to_smooth_upgrade",
)


@dataclass(frozen=True)
class OperatorDashboardSection:
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
    dependency_consistent: bool
    process_gate_open_authorized: bool


@dataclass(frozen=True)
class OperatorDashboardCheck:
    key: str
    expected: str
    observed: str
    passed: bool
    source_artifacts: tuple[str, ...]


@dataclass(frozen=True)
class AnalyticDischargeOperatorDashboard:
    schema_version: int
    lemma_id: str
    candidate_status: str
    active_candidate: bool
    stack_step_count: int
    source_report_count: int
    prerequisite_count: int
    unsatisfied_prerequisite_count: int
    work_order_count: int
    blocked_work_order_count: int
    actionable_work_order_count: int
    template_count: int
    blocked_template_count: int
    actionable_template_count: int
    may_discharge_template_count: int
    dependency_guard_count: int
    dependency_check_count: int
    failed_dependency_check_count: int
    stack_consistency_check_count: int
    passed_stack_consistency_check_count: int
    failed_stack_consistency_check_count: int
    stack_consistent: bool
    process_gate_open_authorized: bool
    blocker_state_changed: bool
    candidate_emission_authorized: bool
    missing_source_count: int
    missing_sources: tuple[str, ...]
    issues: tuple[str, ...]
    operator_verdict: str
    next_action_family: str
    sections: tuple[OperatorDashboardSection, ...]
    checks: tuple[OperatorDashboardCheck, ...]
    source_refs: tuple[str, ...]
    non_claims: tuple[str, ...]


def _check(
    *,
    key: str,
    expected: object,
    observed: object,
    source_artifacts: tuple[str, ...],
) -> OperatorDashboardCheck:
    return OperatorDashboardCheck(
        key=key,
        expected=str(expected),
        observed=str(observed),
        passed=expected == observed,
        source_artifacts=source_artifacts,
    )


def _missing_sources(source_refs: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(source for source in source_refs if not (ROOT / source).exists())


def _sections(
    *,
    prerequisite_count: int,
    unsatisfied_prerequisite_count: int,
    dependency_check_count: int,
    dependency_consistent: bool,
    work_order_count: int,
    blocked_work_order_count: int,
    actionable_work_order_count: int,
    template_count: int,
    blocked_template_count: int,
    actionable_template_count: int,
    may_discharge_template_count: int,
    template_dependency_check_count: int,
    template_dependency_consistent: bool,
) -> tuple[OperatorDashboardSection, ...]:
    return (
        OperatorDashboardSection(
            step=96,
            name="analytic_prerequisites",
            role="Lists proof-obligation and closure prerequisites required before process gates open.",
            markdown_report=str(DEFAULT_PACKET_MARKDOWN_OUTPUT),
            json_report=str(DEFAULT_PACKET_JSON_OUTPUT),
            status="blocked_packet",
            primary_count_label="prerequisite_count",
            primary_count=prerequisite_count,
            blocked_count=unsatisfied_prerequisite_count,
            actionable_count=0,
            dependency_consistent=True,
            process_gate_open_authorized=False,
        ),
        OperatorDashboardSection(
            step=97,
            name="analytic_prerequisite_dependency",
            role="Checks Step 96 against action-readiness, proof-obligation, and closure sources.",
            markdown_report=str(DEFAULT_DEPENDENCY_MARKDOWN_OUTPUT),
            json_report=str(DEFAULT_DEPENDENCY_JSON_OUTPUT),
            status="dependency_guard",
            primary_count_label="dependency_check_count",
            primary_count=dependency_check_count,
            blocked_count=0,
            actionable_count=0,
            dependency_consistent=dependency_consistent,
            process_gate_open_authorized=False,
        ),
        OperatorDashboardSection(
            step=98,
            name="analytic_work_order_matrix",
            role="Groups the eight blocked prerequisites by artifact type and source branch.",
            markdown_report=str(DEFAULT_MATRIX_MARKDOWN_OUTPUT),
            json_report=str(DEFAULT_MATRIX_JSON_OUTPUT),
            status="blocked_work_orders",
            primary_count_label="work_order_count",
            primary_count=work_order_count,
            blocked_count=blocked_work_order_count,
            actionable_count=actionable_work_order_count,
            dependency_consistent=dependency_consistent,
            process_gate_open_authorized=False,
        ),
        OperatorDashboardSection(
            step=99,
            name="analytic_discharge_templates",
            role="Provides blocked-by-default template audits for every analytic work-order type.",
            markdown_report=str(DEFAULT_TEMPLATE_MARKDOWN_OUTPUT),
            json_report=str(DEFAULT_TEMPLATE_JSON_OUTPUT),
            status="blocked_templates",
            primary_count_label="template_count",
            primary_count=template_count,
            blocked_count=blocked_template_count,
            actionable_count=actionable_template_count + may_discharge_template_count,
            dependency_consistent=dependency_consistent,
            process_gate_open_authorized=False,
        ),
        OperatorDashboardSection(
            step=100,
            name="analytic_discharge_template_dependency",
            role="Checks Step 99 against Step 98, Step 96, and Step 97 sources.",
            markdown_report=str(DEFAULT_TEMPLATE_DEPENDENCY_MARKDOWN_OUTPUT),
            json_report=str(DEFAULT_TEMPLATE_DEPENDENCY_JSON_OUTPUT),
            status="template_dependency_guard",
            primary_count_label="dependency_check_count",
            primary_count=template_dependency_check_count,
            blocked_count=0,
            actionable_count=0,
            dependency_consistent=template_dependency_consistent,
            process_gate_open_authorized=False,
        ),
    )


def build_analytic_discharge_operator_dashboard(
    *,
    candidate_dir: Path = DEFAULT_CANDIDATE_DIR,
    smoke_summary: Path = DEFAULT_SMOKE_SUMMARY,
    proof_graph_json: Path = DEFAULT_PROOF_GRAPH_JSON,
) -> AnalyticDischargeOperatorDashboard:
    packet = build_analytic_prerequisite_packet(
        candidate_dir=candidate_dir,
        smoke_summary=smoke_summary,
        proof_graph_json=proof_graph_json,
    )
    dependency = build_analytic_prerequisite_dependency_report(
        candidate_dir=candidate_dir,
        smoke_summary=smoke_summary,
        proof_graph_json=proof_graph_json,
    )
    matrix = build_analytic_work_order_matrix(
        candidate_dir=candidate_dir,
        smoke_summary=smoke_summary,
        proof_graph_json=proof_graph_json,
    )
    template_audit = build_analytic_discharge_template_audit(
        candidate_dir=candidate_dir,
        smoke_summary=smoke_summary,
        proof_graph_json=proof_graph_json,
    )
    template_dependency = build_analytic_discharge_template_dependency_report(
        candidate_dir=candidate_dir,
        smoke_summary=smoke_summary,
        proof_graph_json=proof_graph_json,
    )

    packet_source = (
        "track-a-regularity/reports/promotion_gate_analytic_prerequisites.md",
        "track-a-regularity/reports/promotion_gate_analytic_prerequisites.json",
    )
    dependency_source = (
        "track-a-regularity/reports/promotion_gate_analytic_prerequisite_dependency.md",
        "track-a-regularity/reports/promotion_gate_analytic_prerequisite_dependency.json",
    )
    matrix_source = (
        "track-a-regularity/reports/promotion_gate_analytic_work_order_matrix.md",
        "track-a-regularity/reports/promotion_gate_analytic_work_order_matrix.json",
    )
    template_source = (
        "track-a-regularity/reports/promotion_gate_analytic_discharge_templates.md",
        "track-a-regularity/reports/promotion_gate_analytic_discharge_templates.json",
    )
    template_dependency_source = (
        "track-a-regularity/reports/promotion_gate_analytic_discharge_template_dependency.md",
        "track-a-regularity/reports/promotion_gate_analytic_discharge_template_dependency.json",
    )
    source_refs = tuple(
        dict.fromkeys(
            packet_source
            + dependency_source
            + matrix_source
            + template_source
            + template_dependency_source
            + STEP_DOC_REFS
        )
    )
    missing_sources = _missing_sources(source_refs)
    sections = _sections(
        prerequisite_count=packet.prerequisite_count,
        unsatisfied_prerequisite_count=packet.unsatisfied_prerequisite_count,
        dependency_check_count=dependency.dependency_check_count,
        dependency_consistent=dependency.dependency_consistent,
        work_order_count=matrix.work_order_count,
        blocked_work_order_count=matrix.blocked_work_order_count,
        actionable_work_order_count=matrix.actionable_work_order_count,
        template_count=template_audit.template_count,
        blocked_template_count=template_audit.blocked_template_count,
        actionable_template_count=template_audit.actionable_template_count,
        may_discharge_template_count=template_audit.may_discharge_template_count,
        template_dependency_check_count=template_dependency.dependency_check_count,
        template_dependency_consistent=template_dependency.dependency_consistent,
    )
    checks = (
        _check(
            key="stack.lemma_ids.all_match",
            expected=("lemma_0252",) * 5,
            observed=(
                packet.lemma_id,
                dependency.lemma_id,
                matrix.lemma_id,
                template_audit.lemma_id,
                template_dependency.lemma_id,
            ),
            source_artifacts=source_refs[:10],
        ),
        _check(
            key="stack.candidate_status.all_needs_review",
            expected=("needs_review",) * 5,
            observed=(
                packet.candidate_status,
                dependency.candidate_status,
                matrix.candidate_status,
                template_audit.candidate_status,
                template_dependency.candidate_status,
            ),
            source_artifacts=source_refs[:10],
        ),
        _check(
            key="stack.active_candidate.all_false",
            expected=(False,) * 5,
            observed=(
                packet.active_candidate,
                dependency.active_candidate,
                matrix.active_candidate,
                template_audit.active_candidate,
                template_dependency.active_candidate,
            ),
            source_artifacts=source_refs[:10],
        ),
        _check(
            key="packet.prerequisite_count.matches_matrix_work_orders",
            expected=packet.prerequisite_count,
            observed=matrix.work_order_count,
            source_artifacts=packet_source + matrix_source,
        ),
        _check(
            key="packet.prerequisite_count.matches_template_count",
            expected=packet.prerequisite_count,
            observed=template_audit.template_count,
            source_artifacts=packet_source + template_source,
        ),
        _check(
            key="template.count.matches_template_dependency",
            expected=template_audit.template_count,
            observed=template_dependency.template_count,
            source_artifacts=template_source + template_dependency_source,
        ),
        _check(
            key="matrix.work_order_count.matches_template_dependency",
            expected=matrix.work_order_count,
            observed=template_dependency.matrix_work_order_count,
            source_artifacts=matrix_source + template_dependency_source,
        ),
        _check(
            key="packet.prerequisite_count.matches_template_dependency",
            expected=packet.prerequisite_count,
            observed=template_dependency.packet_prerequisite_count,
            source_artifacts=packet_source + template_dependency_source,
        ),
        _check(
            key="packet.all_prerequisites_unsatisfied",
            expected=packet.prerequisite_count,
            observed=packet.unsatisfied_prerequisite_count,
            source_artifacts=packet_source,
        ),
        _check(
            key="matrix.all_work_orders_blocked",
            expected=matrix.work_order_count,
            observed=matrix.blocked_work_order_count,
            source_artifacts=matrix_source,
        ),
        _check(
            key="matrix.actionable_work_orders.remain_zero",
            expected=0,
            observed=matrix.actionable_work_order_count,
            source_artifacts=matrix_source,
        ),
        _check(
            key="template.all_templates_blocked",
            expected=template_audit.template_count,
            observed=template_audit.blocked_template_count,
            source_artifacts=template_source,
        ),
        _check(
            key="template.actionable_templates.remain_zero",
            expected=0,
            observed=template_audit.actionable_template_count,
            source_artifacts=template_source,
        ),
        _check(
            key="template.may_discharge_templates.remain_zero",
            expected=0,
            observed=template_audit.may_discharge_template_count,
            source_artifacts=template_source,
        ),
        _check(
            key="dependency.guard.consistent",
            expected=True,
            observed=dependency.dependency_consistent,
            source_artifacts=dependency_source,
        ),
        _check(
            key="template_dependency.guard.consistent",
            expected=True,
            observed=template_dependency.dependency_consistent,
            source_artifacts=template_dependency_source,
        ),
        _check(
            key="process_gate_authorization.all_false",
            expected=(False,) * 5,
            observed=(
                packet.process_gate_open_authorized,
                dependency.process_gate_open_authorized,
                matrix.process_gate_open_authorized,
                template_audit.process_gate_open_authorized,
                template_dependency.process_gate_open_authorized,
            ),
            source_artifacts=source_refs[:10],
        ),
        _check(
            key="candidate_emission_authorization.all_false",
            expected=(False, False, False),
            observed=(
                matrix.candidate_emission_authorized,
                template_audit.candidate_emission_authorized,
                template_dependency.candidate_emission_authorized,
            ),
            source_artifacts=matrix_source + template_source + template_dependency_source,
        ),
        _check(
            key="blocker_state_changed.all_false",
            expected=(False, False, False),
            observed=(
                matrix.blocker_state_changed,
                template_audit.blocker_state_changed,
                template_dependency.blocker_state_changed,
            ),
            source_artifacts=matrix_source + template_source + template_dependency_source,
        ),
        _check(
            key="source_reports.issues.all_empty",
            expected=((), (), (), ()),
            observed=(
                dependency.issues,
                matrix.issues,
                template_audit.issues,
                template_dependency.issues,
            ),
            source_artifacts=dependency_source + matrix_source + template_source + template_dependency_source,
        ),
        _check(
            key="source_refs.missing_count.remains_zero",
            expected=0,
            observed=len(missing_sources),
            source_artifacts=source_refs,
        ),
        _check(
            key="dependency.failed_check_count.remains_zero",
            expected=0,
            observed=dependency.failed_dependency_check_count,
            source_artifacts=dependency_source,
        ),
        _check(
            key="template_dependency.failed_check_count.remains_zero",
            expected=0,
            observed=template_dependency.failed_dependency_check_count,
            source_artifacts=template_dependency_source,
        ),
    )

    failed_checks = tuple(check.key for check in checks if not check.passed)
    issues = failed_checks
    stack_consistent = not failed_checks and not missing_sources

    return AnalyticDischargeOperatorDashboard(
        schema_version=1,
        lemma_id=packet.lemma_id,
        candidate_status=packet.candidate_status,
        active_candidate=packet.active_candidate,
        stack_step_count=len(sections),
        source_report_count=10,
        prerequisite_count=packet.prerequisite_count,
        unsatisfied_prerequisite_count=packet.unsatisfied_prerequisite_count,
        work_order_count=matrix.work_order_count,
        blocked_work_order_count=matrix.blocked_work_order_count,
        actionable_work_order_count=matrix.actionable_work_order_count,
        template_count=template_audit.template_count,
        blocked_template_count=template_audit.blocked_template_count,
        actionable_template_count=template_audit.actionable_template_count,
        may_discharge_template_count=template_audit.may_discharge_template_count,
        dependency_guard_count=2,
        dependency_check_count=(
            dependency.dependency_check_count + template_dependency.dependency_check_count
        ),
        failed_dependency_check_count=(
            dependency.failed_dependency_check_count
            + template_dependency.failed_dependency_check_count
        ),
        stack_consistency_check_count=len(checks),
        passed_stack_consistency_check_count=len(checks) - len(failed_checks),
        failed_stack_consistency_check_count=len(failed_checks),
        stack_consistent=stack_consistent,
        process_gate_open_authorized=False,
        blocker_state_changed=False,
        candidate_emission_authorized=False,
        missing_source_count=len(missing_sources),
        missing_sources=missing_sources,
        issues=issues,
        operator_verdict="blocked_analytic_discharge_stack",
        next_action_family="analytic_theorem_artifact_before_process_gate",
        sections=sections,
        checks=checks,
        source_refs=source_refs,
        non_claims=NON_CLAIMS,
    )


def dashboard_to_dict(dashboard: AnalyticDischargeOperatorDashboard) -> dict[str, object]:
    return {
        "schema_version": dashboard.schema_version,
        "lemma_id": dashboard.lemma_id,
        "candidate_status": dashboard.candidate_status,
        "active_candidate": dashboard.active_candidate,
        "stack_step_count": dashboard.stack_step_count,
        "source_report_count": dashboard.source_report_count,
        "prerequisite_count": dashboard.prerequisite_count,
        "unsatisfied_prerequisite_count": dashboard.unsatisfied_prerequisite_count,
        "work_order_count": dashboard.work_order_count,
        "blocked_work_order_count": dashboard.blocked_work_order_count,
        "actionable_work_order_count": dashboard.actionable_work_order_count,
        "template_count": dashboard.template_count,
        "blocked_template_count": dashboard.blocked_template_count,
        "actionable_template_count": dashboard.actionable_template_count,
        "may_discharge_template_count": dashboard.may_discharge_template_count,
        "dependency_guard_count": dashboard.dependency_guard_count,
        "dependency_check_count": dashboard.dependency_check_count,
        "failed_dependency_check_count": dashboard.failed_dependency_check_count,
        "stack_consistency_check_count": dashboard.stack_consistency_check_count,
        "passed_stack_consistency_check_count": dashboard.passed_stack_consistency_check_count,
        "failed_stack_consistency_check_count": dashboard.failed_stack_consistency_check_count,
        "stack_consistent": dashboard.stack_consistent,
        "process_gate_open_authorized": dashboard.process_gate_open_authorized,
        "blocker_state_changed": dashboard.blocker_state_changed,
        "candidate_emission_authorized": dashboard.candidate_emission_authorized,
        "missing_source_count": dashboard.missing_source_count,
        "missing_sources": list(dashboard.missing_sources),
        "issues": list(dashboard.issues),
        "operator_verdict": dashboard.operator_verdict,
        "next_action_family": dashboard.next_action_family,
        "sections": [asdict(section) for section in dashboard.sections],
        "checks": [asdict(check) for check in dashboard.checks],
        "source_refs": list(dashboard.source_refs),
        "non_claims": list(dashboard.non_claims),
        "docs": {
            "analytic_prerequisites_doc": STEP_DOC_REFS[0],
            "analytic_prerequisite_dependency_doc": STEP_DOC_REFS[1],
            "analytic_work_order_matrix_doc": STEP_DOC_REFS[2],
            "analytic_discharge_templates_doc": STEP_DOC_REFS[3],
            "analytic_discharge_template_dependency_doc": STEP_DOC_REFS[4],
        },
    }


def _format(text: str) -> str:
    return text.replace("|", "\\|")


def _section_rows(dashboard: AnalyticDischargeOperatorDashboard) -> list[str]:
    rows = [
        "| step | section | status | primary count | blocked | actionable | dependency consistent | process gate |",
        "|---:|---|---|---:|---:|---:|---|---|",
    ]
    for section in dashboard.sections:
        rows.append(
            "| "
            f"{section.step} | "
            f"`{section.name}` | "
            f"`{section.status}` | "
            f"{section.primary_count} | "
            f"{section.blocked_count} | "
            f"{section.actionable_count} | "
            f"`{str(section.dependency_consistent).lower()}` | "
            f"`{str(section.process_gate_open_authorized).lower()}` |"
        )
    return rows


def _source_rows(dashboard: AnalyticDischargeOperatorDashboard) -> list[str]:
    rows = [
        "| step | markdown | json | role |",
        "|---:|---|---|---|",
    ]
    for section in dashboard.sections:
        rows.append(
            "| "
            f"{section.step} | "
            f"`{section.markdown_report}` | "
            f"`{section.json_report}` | "
            f"{_format(section.role)} |"
        )
    return rows


def _check_rows(dashboard: AnalyticDischargeOperatorDashboard) -> list[str]:
    rows = [
        "| check | expected | observed | passed |",
        "|---|---|---|---|",
    ]
    for check in dashboard.checks:
        rows.append(
            "| "
            f"`{check.key}` | "
            f"`{_format(check.expected)}` | "
            f"`{_format(check.observed)}` | "
            f"`{str(check.passed).lower()}` |"
        )
    return rows


def render_markdown(dashboard: AnalyticDischargeOperatorDashboard) -> str:
    return "\n".join(
        (
            "# Promotion Gate Analytic Discharge Operator Dashboard",
            "",
            "Generated by `track-a-regularity/evaluator/promotion_gate_analytic_discharge_operator_dashboard.py`.",
            "",
            "This compact read-only dashboard indexes the Step 96-100 analytic-discharge",
            "gate stack. It summarizes prerequisites, dependency reports, work orders,",
            "blocked templates, and template-dependency guard status in one operator surface.",
            "Dashboard presence does not discharge a blocker or authorize process work.",
            "",
            "## Summary",
            "",
            f"- lemma_id: `{dashboard.lemma_id}`",
            f"- candidate_status: `{dashboard.candidate_status}`",
            f"- active_candidate: `{str(dashboard.active_candidate).lower()}`",
            f"- operator_verdict: `{dashboard.operator_verdict}`",
            f"- next_action_family: `{dashboard.next_action_family}`",
            f"- stack_step_count: `{dashboard.stack_step_count}`",
            f"- source_report_count: `{dashboard.source_report_count}`",
            f"- prerequisite_count: `{dashboard.prerequisite_count}`",
            f"- unsatisfied_prerequisite_count: `{dashboard.unsatisfied_prerequisite_count}`",
            f"- work_order_count: `{dashboard.work_order_count}`",
            f"- blocked_work_order_count: `{dashboard.blocked_work_order_count}`",
            f"- actionable_work_order_count: `{dashboard.actionable_work_order_count}`",
            f"- template_count: `{dashboard.template_count}`",
            f"- blocked_template_count: `{dashboard.blocked_template_count}`",
            f"- actionable_template_count: `{dashboard.actionable_template_count}`",
            f"- may_discharge_template_count: `{dashboard.may_discharge_template_count}`",
            f"- dependency_guard_count: `{dashboard.dependency_guard_count}`",
            f"- dependency_check_count: `{dashboard.dependency_check_count}`",
            f"- failed_dependency_check_count: `{dashboard.failed_dependency_check_count}`",
            f"- stack_consistency_check_count: `{dashboard.stack_consistency_check_count}`",
            f"- failed_stack_consistency_check_count: `{dashboard.failed_stack_consistency_check_count}`",
            f"- stack_consistent: `{str(dashboard.stack_consistent).lower()}`",
            f"- process_gate_open_authorized: `{str(dashboard.process_gate_open_authorized).lower()}`",
            f"- blocker_state_changed: `{str(dashboard.blocker_state_changed).lower()}`",
            f"- candidate_emission_authorized: `{str(dashboard.candidate_emission_authorized).lower()}`",
            f"- missing_source_count: `{dashboard.missing_source_count}`",
            f"- issues: `{', '.join(dashboard.issues) or 'none'}`",
            "",
            "## Gate Stack",
            "",
            *_section_rows(dashboard),
            "",
            "## Source Reports",
            "",
            *_source_rows(dashboard),
            "",
            "## Consistency Checks",
            "",
            *_check_rows(dashboard),
            "",
            "## Non-Claims",
            "",
            *(f"- `{item}`" for item in dashboard.non_claims),
            "",
        )
    )


def render_json(dashboard: AnalyticDischargeOperatorDashboard) -> str:
    return json.dumps(dashboard_to_dict(dashboard), indent=2, sort_keys=True) + "\n"


def render_output(
    dashboard: AnalyticDischargeOperatorDashboard,
    output_format: str,
) -> str:
    if output_format == "markdown":
        return render_markdown(dashboard)
    if output_format == "json":
        return render_json(dashboard)
    raise ValueError(f"unknown analytic discharge operator dashboard format: {output_format}")


def write_output(
    output: Path,
    dashboard: AnalyticDischargeOperatorDashboard,
    output_format: str,
) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_output(dashboard, output_format), encoding="utf-8")
    return output


def check_output(
    output: Path,
    dashboard: AnalyticDischargeOperatorDashboard,
    output_format: str,
) -> tuple[bool, str]:
    expected = render_output(dashboard, output_format)
    if not output.exists():
        return False, f"missing promotion gate analytic discharge operator dashboard: {output}"
    current = output.read_text(encoding="utf-8")
    if current != expected:
        return False, f"stale promotion gate analytic discharge operator dashboard: {output}"
    return True, f"fresh promotion gate analytic discharge operator dashboard: {output}"


def check_stack_consistent(
    dashboard: AnalyticDischargeOperatorDashboard,
) -> tuple[bool, str]:
    if not dashboard.stack_consistent:
        return False, "analytic discharge operator dashboard inconsistent: " + ", ".join(
            dashboard.issues
        )
    return True, "analytic discharge operator dashboard stack is consistent"


def check_sources(dashboard: AnalyticDischargeOperatorDashboard) -> tuple[bool, str]:
    if dashboard.missing_source_count:
        return False, "missing analytic discharge operator dashboard sources: " + ", ".join(
            dashboard.missing_sources
        )
    return True, "all analytic discharge operator dashboard sources exist"


def check_blocked(dashboard: AnalyticDischargeOperatorDashboard) -> tuple[bool, str]:
    if dashboard.process_gate_open_authorized:
        return False, "process gate open became authorized"
    if dashboard.blocker_state_changed:
        return False, "operator dashboard changed blocker state"
    if dashboard.candidate_emission_authorized:
        return False, "operator dashboard authorized candidate emission"
    if dashboard.actionable_work_order_count:
        return False, "operator dashboard found actionable work orders"
    if dashboard.actionable_template_count:
        return False, "operator dashboard found actionable templates"
    if dashboard.may_discharge_template_count:
        return False, "operator dashboard found blocker-discharge-capable templates"
    if dashboard.blocked_template_count != dashboard.template_count:
        return False, "not all templates remain blocked"
    if dashboard.blocked_work_order_count != dashboard.work_order_count:
        return False, "not all work orders remain blocked"
    return True, "analytic discharge operator dashboard keeps gates and templates blocked"


def default_output_path(output_format: str) -> Path:
    if output_format == "markdown":
        return DEFAULT_MARKDOWN_OUTPUT
    if output_format == "json":
        return DEFAULT_JSON_OUTPUT
    raise ValueError(f"unknown analytic discharge operator dashboard format: {output_format}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Render a read-only operator dashboard for the Step 96-100 analytic-discharge gate stack."
    )
    parser.add_argument("--candidate-dir", type=Path, default=DEFAULT_CANDIDATE_DIR)
    parser.add_argument("--smoke-summary", type=Path, default=DEFAULT_SMOKE_SUMMARY)
    parser.add_argument("--proof-graph-json", type=Path, default=DEFAULT_PROOF_GRAPH_JSON)
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--check-output", action="store_true")
    parser.add_argument("--require-stack-consistent", action="store_true")
    parser.add_argument("--require-sources-exist", action="store_true")
    parser.add_argument("--require-blocked", action="store_true")
    args = parser.parse_args(argv)

    try:
        dashboard = build_analytic_discharge_operator_dashboard(
            candidate_dir=args.candidate_dir,
            smoke_summary=args.smoke_summary,
            proof_graph_json=args.proof_graph_json,
        )
    except Exception as exc:  # noqa: BLE001 - CLI should report setup failures.
        print(f"failed to build analytic discharge operator dashboard: {exc}", file=sys.stderr)
        return 1

    output = args.output or default_output_path(args.format)
    if args.check_output:
        ok, message = check_output(output, dashboard, args.format)
        print(message)
        if not ok:
            print(
                "run without --check-output to regenerate the analytic discharge operator dashboard",
                file=sys.stderr,
            )
            return 1
    else:
        written = write_output(output, dashboard, args.format)
        print(f"wrote {written}")

    if args.require_stack_consistent:
        ok, message = check_stack_consistent(dashboard)
        print(message)
        if not ok:
            return 1
    if args.require_sources_exist:
        ok, message = check_sources(dashboard)
        print(message)
        if not ok:
            return 1
    if args.require_blocked:
        ok, message = check_blocked(dashboard)
        print(message)
        if not ok:
            return 1

    print(f"stack_step_count: {dashboard.stack_step_count}")
    print(f"stack_consistency_check_count: {dashboard.stack_consistency_check_count}")
    print(f"failed_stack_consistency_check_count: {dashboard.failed_stack_consistency_check_count}")
    print(f"stack_consistent: {str(dashboard.stack_consistent).lower()}")
    print(f"process_gate_open_authorized: {str(dashboard.process_gate_open_authorized).lower()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
