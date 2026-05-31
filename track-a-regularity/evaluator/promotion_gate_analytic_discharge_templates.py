from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from promotion_gate_analytic_work_order_matrix import (
    DEFAULT_JSON_OUTPUT as DEFAULT_MATRIX_JSON_OUTPUT,
    DEFAULT_MARKDOWN_OUTPUT as DEFAULT_MATRIX_MARKDOWN_OUTPUT,
    AnalyticWorkOrder,
    build_analytic_work_order_matrix,
    matrix_to_dict,
)
from promotion_gate_regression import DEFAULT_CANDIDATE_DIR, DEFAULT_SMOKE_SUMMARY
from proof_obligation_blockers import DEFAULT_INPUT as DEFAULT_PROOF_GRAPH_JSON


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REPORT_DIR = ROOT / "track-a-regularity/reports"
DEFAULT_MARKDOWN_OUTPUT = DEFAULT_REPORT_DIR / "promotion_gate_analytic_discharge_templates.md"
DEFAULT_JSON_OUTPUT = DEFAULT_REPORT_DIR / "promotion_gate_analytic_discharge_templates.json"

REQUIRED_EVIDENCE_KEYS = (
    "exact_statement_or_artifact_scope",
    "solution_class_and_hypothesis_match",
    "known_result_separation_or_new_theorem_scope",
    "proof_or_formal_artifact_path",
    "applicability_checks_to_current_setting",
    "post_discharge_smoke_and_metadata_update_plan",
)

FORBIDDEN_MUTATIONS = (
    "set_actionable_now_true",
    "remove_promotion_blocker",
    "open_process_gate",
    "set_candidate_emission_authorized_true",
    "copy_yaml_to_candidates",
    "mark_candidate_active",
)

NON_CLAIMS = (
    "analytic_discharge_templates_only",
    "blocked_by_default",
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
class AnalyticDischargeTemplate:
    template_id: str
    work_order_id: str
    family: str
    source_branch: str
    prerequisite_key: str
    required_artifact_type: str
    template_status: str
    actionable_now: bool
    may_discharge_blocker: bool
    blocker_state_after_template: str
    required_evidence_keys: tuple[str, ...]
    forbidden_mutations: tuple[str, ...]
    source_artifact: str
    dependency_guard_keys: tuple[str, ...]
    template_instruction: str


@dataclass(frozen=True)
class TemplateSourceBranchSummary:
    source_branch: str
    template_count: int
    blocked_template_count: int
    actionable_template_count: int
    may_discharge_template_count: int
    artifact_types: tuple[str, ...]


@dataclass(frozen=True)
class AnalyticDischargeTemplateAudit:
    schema_version: int
    lemma_id: str
    candidate_status: str
    active_candidate: bool
    matrix_markdown: str
    matrix_json: str
    template_count: int
    blocked_template_count: int
    actionable_template_count: int
    may_discharge_template_count: int
    source_branch_count: int
    artifact_type_count: int
    dependency_consistent: bool
    process_gate_open_authorized: bool
    blocker_state_changed: bool
    candidate_emission_authorized: bool
    missing_source_count: int
    missing_sources: tuple[str, ...]
    issues: tuple[str, ...]
    templates: tuple[AnalyticDischargeTemplate, ...]
    source_branch_summaries: tuple[TemplateSourceBranchSummary, ...]
    source_refs: tuple[str, ...]
    non_claims: tuple[str, ...]


def _template_instruction(order: AnalyticWorkOrder) -> str:
    return (
        f"Use this blocked template to collect evidence for `{order.required_artifact_type}`. "
        "It is not a discharge artifact until every evidence key is populated, reviewed, and "
        "propagated through the proof-obligation and closure guards."
    )


def _templates(work_orders: tuple[AnalyticWorkOrder, ...]) -> tuple[AnalyticDischargeTemplate, ...]:
    templates: list[AnalyticDischargeTemplate] = []
    for order in work_orders:
        templates.append(
            AnalyticDischargeTemplate(
                template_id=f"template_{order.work_order_id}",
                work_order_id=order.work_order_id,
                family=order.family,
                source_branch=order.source_branch,
                prerequisite_key=order.prerequisite_key,
                required_artifact_type=order.required_artifact_type,
                template_status="blocked_template",
                actionable_now=False,
                may_discharge_blocker=False,
                blocker_state_after_template=order.status,
                required_evidence_keys=REQUIRED_EVIDENCE_KEYS,
                forbidden_mutations=FORBIDDEN_MUTATIONS,
                source_artifact=order.source_artifact,
                dependency_guard_keys=order.dependency_guard_keys,
                template_instruction=_template_instruction(order),
            )
        )
    return tuple(templates)


def _source_branch_summaries(
    templates: tuple[AnalyticDischargeTemplate, ...]
) -> tuple[TemplateSourceBranchSummary, ...]:
    summaries: list[TemplateSourceBranchSummary] = []
    for branch in sorted({template.source_branch for template in templates}):
        branch_templates = tuple(
            template for template in templates if template.source_branch == branch
        )
        summaries.append(
            TemplateSourceBranchSummary(
                source_branch=branch,
                template_count=len(branch_templates),
                blocked_template_count=sum(
                    1 for template in branch_templates if template.template_status == "blocked_template"
                ),
                actionable_template_count=sum(
                    1 for template in branch_templates if template.actionable_now
                ),
                may_discharge_template_count=sum(
                    1 for template in branch_templates if template.may_discharge_blocker
                ),
                artifact_types=tuple(
                    sorted({template.required_artifact_type for template in branch_templates})
                ),
            )
        )
    return tuple(summaries)


def _missing_sources(source_refs: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(source for source in source_refs if not (ROOT / source).exists())


def build_analytic_discharge_template_audit(
    *,
    candidate_dir: Path = DEFAULT_CANDIDATE_DIR,
    smoke_summary: Path = DEFAULT_SMOKE_SUMMARY,
    proof_graph_json: Path = DEFAULT_PROOF_GRAPH_JSON,
) -> AnalyticDischargeTemplateAudit:
    matrix = build_analytic_work_order_matrix(
        candidate_dir=candidate_dir,
        smoke_summary=smoke_summary,
        proof_graph_json=proof_graph_json,
    )
    templates = _templates(matrix.work_orders)
    source_refs = tuple(
        dict.fromkeys(
            (
                "track-a-regularity/reports/promotion_gate_analytic_work_order_matrix.md",
                "track-a-regularity/reports/promotion_gate_analytic_work_order_matrix.json",
                *(template.source_artifact for template in templates),
            )
        )
    )
    missing_sources = _missing_sources(source_refs)
    blocked_template_count = sum(
        1 for template in templates if template.template_status == "blocked_template"
    )
    actionable_template_count = sum(1 for template in templates if template.actionable_now)
    may_discharge_template_count = sum(
        1 for template in templates if template.may_discharge_blocker
    )
    issues: list[str] = []
    if len(templates) != matrix.work_order_count:
        issues.append("template_count_mismatch")
    if blocked_template_count != len(templates):
        issues.append("unblocked_template_detected")
    if actionable_template_count:
        issues.append("actionable_template_detected")
    if may_discharge_template_count:
        issues.append("template_allows_blocker_discharge")
    if not matrix.dependency_consistent:
        issues.append("matrix_dependency_inconsistent")
    if matrix.process_gate_open_authorized:
        issues.append("process_gate_open_authorized")
    if missing_sources:
        issues.append("missing_sources")

    return AnalyticDischargeTemplateAudit(
        schema_version=1,
        lemma_id=matrix.lemma_id,
        candidate_status=matrix.candidate_status,
        active_candidate=matrix.active_candidate,
        matrix_markdown=str(DEFAULT_MATRIX_MARKDOWN_OUTPUT),
        matrix_json=str(DEFAULT_MATRIX_JSON_OUTPUT),
        template_count=len(templates),
        blocked_template_count=blocked_template_count,
        actionable_template_count=actionable_template_count,
        may_discharge_template_count=may_discharge_template_count,
        source_branch_count=len({template.source_branch for template in templates}),
        artifact_type_count=len({template.required_artifact_type for template in templates}),
        dependency_consistent=matrix.dependency_consistent,
        process_gate_open_authorized=matrix.process_gate_open_authorized,
        blocker_state_changed=False,
        candidate_emission_authorized=False,
        missing_source_count=len(missing_sources),
        missing_sources=missing_sources,
        issues=tuple(issues),
        templates=templates,
        source_branch_summaries=_source_branch_summaries(templates),
        source_refs=source_refs,
        non_claims=NON_CLAIMS,
    )


def audit_to_dict(audit: AnalyticDischargeTemplateAudit) -> dict[str, object]:
    return {
        "schema_version": audit.schema_version,
        "lemma_id": audit.lemma_id,
        "candidate_status": audit.candidate_status,
        "active_candidate": audit.active_candidate,
        "matrix_markdown": audit.matrix_markdown,
        "matrix_json": audit.matrix_json,
        "template_count": audit.template_count,
        "blocked_template_count": audit.blocked_template_count,
        "actionable_template_count": audit.actionable_template_count,
        "may_discharge_template_count": audit.may_discharge_template_count,
        "source_branch_count": audit.source_branch_count,
        "artifact_type_count": audit.artifact_type_count,
        "dependency_consistent": audit.dependency_consistent,
        "process_gate_open_authorized": audit.process_gate_open_authorized,
        "blocker_state_changed": audit.blocker_state_changed,
        "candidate_emission_authorized": audit.candidate_emission_authorized,
        "missing_source_count": audit.missing_source_count,
        "missing_sources": list(audit.missing_sources),
        "issues": list(audit.issues),
        "templates": [asdict(template) for template in audit.templates],
        "source_branch_summaries": [
            asdict(summary) for summary in audit.source_branch_summaries
        ],
        "source_refs": list(audit.source_refs),
        "non_claims": list(audit.non_claims),
        "matrix_snapshot": matrix_to_dict(build_analytic_work_order_matrix()),
        "docs": {
            "analytic_work_order_matrix_doc": (
                "docs/STEP98_PROMOTION_GATE_ANALYTIC_WORK_ORDER_MATRIX.md"
            ),
            "analytic_prerequisites_doc": (
                "docs/STEP96_PROMOTION_GATE_ANALYTIC_PREREQUISITES.md"
            ),
            "analytic_dependency_doc": (
                "docs/STEP97_PROMOTION_GATE_ANALYTIC_PREREQUISITE_DEPENDENCY.md"
            ),
        },
    }


def _format(text: str) -> str:
    return text.replace("|", "\\|")


def _source_branch_rows(audit: AnalyticDischargeTemplateAudit) -> list[str]:
    rows = [
        "| source branch | templates | blocked | actionable | may discharge | artifact types |",
        "|---|---:|---:|---:|---:|---|",
    ]
    for summary in audit.source_branch_summaries:
        rows.append(
            "| "
            f"`{summary.source_branch}` | "
            f"{summary.template_count} | "
            f"{summary.blocked_template_count} | "
            f"{summary.actionable_template_count} | "
            f"{summary.may_discharge_template_count} | "
            f"{'<br>'.join(f'`{item}`' for item in summary.artifact_types)} |"
        )
    return rows


def _template_rows(audit: AnalyticDischargeTemplateAudit) -> list[str]:
    rows = [
        "| template | work order | family | branch | artifact type | status | actionable | may discharge | evidence keys |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for template in audit.templates:
        rows.append(
            "| "
            f"`{template.template_id}` | "
            f"`{template.work_order_id}` | "
            f"`{template.family}` | "
            f"`{template.source_branch}` | "
            f"`{template.required_artifact_type}` | "
            f"`{template.template_status}` | "
            f"`{str(template.actionable_now).lower()}` | "
            f"`{str(template.may_discharge_blocker).lower()}` | "
            f"{'<br>'.join(f'`{key}`' for key in template.required_evidence_keys)} |"
        )
    return rows


def render_markdown(audit: AnalyticDischargeTemplateAudit) -> str:
    return "\n".join(
        (
            "# Promotion Gate Analytic Discharge Templates",
            "",
            "Generated by `track-a-regularity/evaluator/promotion_gate_analytic_discharge_templates.py`.",
            "",
            "This read-only audit provides blocked-by-default templates for the Step 98",
            "analytic work-order types. Template presence does not discharge a blocker,",
            "open a process gate, copy YAML, or authorize candidate emission.",
            "",
            "## Summary",
            "",
            f"- lemma_id: `{audit.lemma_id}`",
            f"- candidate_status: `{audit.candidate_status}`",
            f"- active_candidate: `{str(audit.active_candidate).lower()}`",
            f"- template_count: `{audit.template_count}`",
            f"- blocked_template_count: `{audit.blocked_template_count}`",
            f"- actionable_template_count: `{audit.actionable_template_count}`",
            f"- may_discharge_template_count: `{audit.may_discharge_template_count}`",
            f"- source_branch_count: `{audit.source_branch_count}`",
            f"- artifact_type_count: `{audit.artifact_type_count}`",
            f"- dependency_consistent: `{str(audit.dependency_consistent).lower()}`",
            f"- process_gate_open_authorized: `{str(audit.process_gate_open_authorized).lower()}`",
            f"- blocker_state_changed: `{str(audit.blocker_state_changed).lower()}`",
            f"- candidate_emission_authorized: `{str(audit.candidate_emission_authorized).lower()}`",
            f"- missing_source_count: `{audit.missing_source_count}`",
            f"- issues: `{', '.join(audit.issues) or 'none'}`",
            "",
            "## Source Branch Summary",
            "",
            *_source_branch_rows(audit),
            "",
            "## Templates",
            "",
            *_template_rows(audit),
            "",
            "## Non-Claims",
            "",
            *(f"- `{item}`" for item in audit.non_claims),
            "",
        )
    )


def render_json(audit: AnalyticDischargeTemplateAudit) -> str:
    return json.dumps(audit_to_dict(audit), indent=2, sort_keys=True) + "\n"


def render_output(audit: AnalyticDischargeTemplateAudit, output_format: str) -> str:
    if output_format == "markdown":
        return render_markdown(audit)
    if output_format == "json":
        return render_json(audit)
    raise ValueError(f"unknown analytic discharge template format: {output_format}")


def write_output(
    output: Path,
    audit: AnalyticDischargeTemplateAudit,
    output_format: str,
) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_output(audit, output_format), encoding="utf-8")
    return output


def check_output(
    output: Path,
    audit: AnalyticDischargeTemplateAudit,
    output_format: str,
) -> tuple[bool, str]:
    expected = render_output(audit, output_format)
    if not output.exists():
        return False, f"missing promotion gate analytic discharge template audit: {output}"
    current = output.read_text(encoding="utf-8")
    if current != expected:
        return False, f"stale promotion gate analytic discharge template audit: {output}"
    return True, f"fresh promotion gate analytic discharge template audit: {output}"


def check_blocked(audit: AnalyticDischargeTemplateAudit) -> tuple[bool, str]:
    if audit.process_gate_open_authorized:
        return False, "process gate open became authorized"
    if audit.blocker_state_changed:
        return False, "template audit changed blocker state"
    if audit.candidate_emission_authorized:
        return False, "candidate emission became authorized"
    if audit.actionable_template_count:
        return False, "template audit marked a template actionable"
    if audit.may_discharge_template_count:
        return False, "template audit marked a template as blocker-discharge capable"
    if audit.blocked_template_count != audit.template_count:
        return False, "not every template is blocked by default"
    return True, "analytic discharge templates remain blocked by default"


def check_matrix_consistent(audit: AnalyticDischargeTemplateAudit) -> tuple[bool, str]:
    if not audit.dependency_consistent:
        return False, "template audit source matrix dependency is inconsistent"
    if audit.issues:
        return False, "analytic discharge template audit has issues: " + ", ".join(
            audit.issues
        )
    return True, "analytic discharge template audit is consistent with the work-order matrix"


def check_sources(audit: AnalyticDischargeTemplateAudit) -> tuple[bool, str]:
    if audit.missing_source_count:
        return False, "missing analytic discharge template sources: " + ", ".join(
            audit.missing_sources
        )
    return True, "all analytic discharge template sources exist"


def default_output_path(output_format: str) -> Path:
    if output_format == "markdown":
        return DEFAULT_MARKDOWN_OUTPUT
    if output_format == "json":
        return DEFAULT_JSON_OUTPUT
    raise ValueError(f"unknown analytic discharge template format: {output_format}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Render blocked-by-default templates for analytic work-order discharge artifacts."
    )
    parser.add_argument("--candidate-dir", type=Path, default=DEFAULT_CANDIDATE_DIR)
    parser.add_argument("--smoke-summary", type=Path, default=DEFAULT_SMOKE_SUMMARY)
    parser.add_argument("--proof-graph-json", type=Path, default=DEFAULT_PROOF_GRAPH_JSON)
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--check-output", action="store_true")
    parser.add_argument("--require-blocked", action="store_true")
    parser.add_argument("--require-matrix-consistent", action="store_true")
    parser.add_argument("--require-sources-exist", action="store_true")
    args = parser.parse_args(argv)

    try:
        audit = build_analytic_discharge_template_audit(
            candidate_dir=args.candidate_dir,
            smoke_summary=args.smoke_summary,
            proof_graph_json=args.proof_graph_json,
        )
    except Exception as exc:  # noqa: BLE001 - CLI should report setup failures.
        print(f"failed to build analytic discharge template audit: {exc}", file=sys.stderr)
        return 1

    output = args.output or default_output_path(args.format)
    if args.check_output:
        ok, message = check_output(output, audit, args.format)
        print(message)
        if not ok:
            print(
                "run without --check-output to regenerate the analytic discharge template audit",
                file=sys.stderr,
            )
            return 1
    else:
        written = write_output(output, audit, args.format)
        print(f"wrote {written}")

    if args.require_blocked:
        ok, message = check_blocked(audit)
        print(message)
        if not ok:
            return 1
    if args.require_matrix_consistent:
        ok, message = check_matrix_consistent(audit)
        print(message)
        if not ok:
            return 1
    if args.require_sources_exist:
        ok, message = check_sources(audit)
        print(message)
        if not ok:
            return 1

    print(f"template_count: {audit.template_count}")
    print(f"blocked_template_count: {audit.blocked_template_count}")
    print(f"actionable_template_count: {audit.actionable_template_count}")
    print(f"may_discharge_template_count: {audit.may_discharge_template_count}")
    print(f"process_gate_open_authorized: {str(audit.process_gate_open_authorized).lower()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
