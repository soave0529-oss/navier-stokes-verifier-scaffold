from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from generation_spec_v4 import assess_candidate
from schema import load_candidate
from v4_metadata_checklist import (
    DEFAULT_TEMPLATE_PATH,
    build_checklist,
    expected_evaluator_keys,
)


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CANDIDATE_DIR = ROOT / "track-a-regularity/candidates"
DEFAULT_REPORT_DIR = ROOT / "track-a-regularity/reports"
DEFAULT_MARKDOWN_OUTPUT = DEFAULT_REPORT_DIR / "proposed_candidate_staging_audit.md"
DEFAULT_JSON_OUTPUT = DEFAULT_REPORT_DIR / "proposed_candidate_staging_audit.json"
NON_CLAIMS = (
    "staging_audit_only",
    "no_file_copy",
    "no_candidate_emission",
    "no_navier_stokes_solution",
    "no_epsilon_regularity_theorem",
    "no_weak_to_smooth_upgrade",
)


@dataclass(frozen=True)
class ProposalAssessment:
    path: str
    candidate_id: str
    loadable: bool
    inside_active_candidate_dir: bool
    expected_status: str
    candidate_status_field: str
    emit_ready: bool
    eligible_for_candidate_pool: bool
    staging_status: str
    reasons: tuple[str, ...]


@dataclass(frozen=True)
class ProposedCandidateStagingAudit:
    schema_version: int
    checklist_marker_count: int
    expected_evaluator_key_count: int
    template_safe: bool
    proposal_count: int
    ready_count: int
    blocked_count: int
    rejected_count: int
    proposals: tuple[ProposalAssessment, ...]
    non_claims: tuple[str, ...]


def _relative(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT.resolve()))
    except ValueError:
        return str(path)


def _is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def _candidate_paths(inputs: tuple[Path, ...]) -> tuple[Path, ...]:
    paths: list[Path] = []
    for item in inputs:
        if item.is_dir():
            paths.extend(sorted(item.glob("lemma_*.yaml")))
        else:
            paths.append(item)
    return tuple(sorted(paths))


def assess_proposal(
    path: Path,
    *,
    candidate_dir: Path = DEFAULT_CANDIDATE_DIR,
) -> ProposalAssessment:
    relative_path = _relative(path)
    inside_candidate_dir = _is_relative_to(path, candidate_dir)
    reasons: list[str] = []
    if inside_candidate_dir:
        reasons.append(
            "proposal path is already inside the active candidate directory; stage it elsewhere first"
        )

    try:
        candidate = load_candidate(path)
    except Exception as exc:  # noqa: BLE001 - report malformed staging input.
        return ProposalAssessment(
            path=relative_path,
            candidate_id="",
            loadable=False,
            inside_active_candidate_dir=inside_candidate_dir,
            expected_status="",
            candidate_status_field="",
            emit_ready=False,
            eligible_for_candidate_pool=False,
            staging_status="invalid",
            reasons=tuple(reasons + [f"candidate YAML is not loadable: {exc}"]),
        )

    expected_status = str(candidate.expected_evaluator.get("status", ""))
    gate_assessment = assess_candidate(candidate)
    emit_ready = gate_assessment.emit_ready
    if expected_status == "candidate":
        reasons.extend(gate_assessment.reasons)
    else:
        reasons.append(
            f"expected_evaluator.status is {expected_status!r}, so this remains staged/review-only"
        )

    if inside_candidate_dir:
        staging_status = "rejected_location"
        eligible = False
    elif expected_status == "candidate" and emit_ready:
        staging_status = "ready_for_manual_copy"
        eligible = True
    elif expected_status == "candidate":
        staging_status = "blocked_candidate"
        eligible = False
    else:
        staging_status = "blocked_review"
        eligible = False

    return ProposalAssessment(
        path=relative_path,
        candidate_id=candidate.id,
        loadable=True,
        inside_active_candidate_dir=inside_candidate_dir,
        expected_status=expected_status,
        candidate_status_field=candidate.status,
        emit_ready=emit_ready,
        eligible_for_candidate_pool=eligible,
        staging_status=staging_status,
        reasons=tuple(reasons),
    )


def build_staging_audit(
    inputs: tuple[Path, ...] = (DEFAULT_TEMPLATE_PATH,),
    *,
    candidate_dir: Path = DEFAULT_CANDIDATE_DIR,
) -> ProposedCandidateStagingAudit:
    checklist = build_checklist()
    paths = _candidate_paths(inputs)
    proposals = tuple(assess_proposal(path, candidate_dir=candidate_dir) for path in paths)
    ready_count = sum(1 for proposal in proposals if proposal.staging_status == "ready_for_manual_copy")
    blocked_count = sum(1 for proposal in proposals if proposal.staging_status.startswith("blocked_"))
    rejected_count = sum(1 for proposal in proposals if proposal.staging_status in {"invalid", "rejected_location"})
    return ProposedCandidateStagingAudit(
        schema_version=1,
        checklist_marker_count=checklist.marker_count,
        expected_evaluator_key_count=len(expected_evaluator_keys()),
        template_safe=not checklist.template_safety.issues,
        proposal_count=len(proposals),
        ready_count=ready_count,
        blocked_count=blocked_count,
        rejected_count=rejected_count,
        proposals=proposals,
        non_claims=NON_CLAIMS,
    )


def staging_audit_to_dict(audit: ProposedCandidateStagingAudit) -> dict[str, object]:
    return {
        "schema_version": audit.schema_version,
        "checklist_marker_count": audit.checklist_marker_count,
        "expected_evaluator_key_count": audit.expected_evaluator_key_count,
        "template_safe": audit.template_safe,
        "proposal_count": audit.proposal_count,
        "ready_count": audit.ready_count,
        "blocked_count": audit.blocked_count,
        "rejected_count": audit.rejected_count,
        "proposals": [asdict(proposal) for proposal in audit.proposals],
        "non_claims": list(audit.non_claims),
        "docs": {
            "generation_spec": "docs/CANDIDATE_GENERATION_SPEC_V4.md",
            "freeze_doc": "docs/CANDIDATE_GENERATION_FREEZE.md",
            "metadata_checklist_doc": "docs/STEP80_V4_METADATA_CHECKLIST.md",
        },
    }


def _format_reasons(reasons: tuple[str, ...]) -> str:
    if not reasons:
        return "`none`"
    return "<br>".join(f"`{reason}`" for reason in reasons)


def render_markdown(audit: ProposedCandidateStagingAudit) -> str:
    proposal_rows = [
        "| path | id | expected status | staging status | emit ready | eligible | reasons |",
        "|---|---|---|---|---|---|---|",
    ]
    for proposal in audit.proposals:
        proposal_rows.append(
            "| "
            f"`{proposal.path}` | "
            f"`{proposal.candidate_id}` | "
            f"`{proposal.expected_status}` | "
            f"`{proposal.staging_status}` | "
            f"`{str(proposal.emit_ready).lower()}` | "
            f"`{str(proposal.eligible_for_candidate_pool).lower()}` | "
            f"{_format_reasons(proposal.reasons)} |"
        )

    non_claim_rows = [f"- `{item}`" for item in audit.non_claims]
    return "\n".join(
        (
            "# Proposed Candidate Staging Audit",
            "",
            "Generated by `track-a-regularity/evaluator/proposed_candidate_staging.py`.",
            "",
            "This report audits staged YAML before it can be manually copied into",
            "`track-a-regularity/candidates/`. It never copies files and never emits an",
            "active candidate.",
            "",
            "## Summary",
            "",
            f"- checklist_marker_count: `{audit.checklist_marker_count}`",
            f"- expected_evaluator_key_count: `{audit.expected_evaluator_key_count}`",
            f"- template_safe: `{str(audit.template_safe).lower()}`",
            f"- proposal_count: `{audit.proposal_count}`",
            f"- ready_count: `{audit.ready_count}`",
            f"- blocked_count: `{audit.blocked_count}`",
            f"- rejected_count: `{audit.rejected_count}`",
            "",
            "## Proposals",
            "",
            *proposal_rows,
            "",
            "## Non-Claims",
            "",
            *non_claim_rows,
            "",
        )
    )


def render_json(audit: ProposedCandidateStagingAudit) -> str:
    return json.dumps(staging_audit_to_dict(audit), indent=2, sort_keys=True) + "\n"


def render_output(audit: ProposedCandidateStagingAudit, output_format: str) -> str:
    if output_format == "markdown":
        return render_markdown(audit)
    if output_format == "json":
        return render_json(audit)
    raise ValueError(f"unknown staging audit format: {output_format}")


def write_output(
    output: Path,
    audit: ProposedCandidateStagingAudit,
    output_format: str,
) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_output(audit, output_format), encoding="utf-8")
    return output


def check_output(
    output: Path,
    audit: ProposedCandidateStagingAudit,
    output_format: str,
) -> tuple[bool, str]:
    expected = render_output(audit, output_format)
    if not output.exists():
        return False, f"missing proposed-candidate staging audit: {output}"
    current = output.read_text(encoding="utf-8")
    if current != expected:
        return False, f"stale proposed-candidate staging audit: {output}"
    return True, f"fresh proposed-candidate staging audit: {output}"


def default_output_path(output_format: str) -> Path:
    if output_format == "markdown":
        return DEFAULT_MARKDOWN_OUTPUT
    if output_format == "json":
        return DEFAULT_JSON_OUTPUT
    raise ValueError(f"unknown staging audit format: {output_format}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Audit staged candidate YAML before manual entry into the active candidate pool."
    )
    parser.add_argument(
        "inputs",
        nargs="*",
        type=Path,
        help="Staged YAML file(s) or directories. Defaults to the blocked v4 template.",
    )
    parser.add_argument("--candidate-dir", type=Path, default=DEFAULT_CANDIDATE_DIR)
    parser.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
        help="Staging audit output format.",
    )
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument(
        "--check-output",
        action="store_true",
        help="Check that --output already matches the rendered staging audit.",
    )
    parser.add_argument(
        "--require-outside-candidates",
        action="store_true",
        help="Fail if any staged input is already inside track-a-regularity/candidates/.",
    )
    parser.add_argument(
        "--require-no-ready",
        action="store_true",
        help="Fail if any staged input is emit-ready for manual copy.",
    )
    parser.add_argument(
        "--fail-on-blocked",
        action="store_true",
        help="Fail if any expected candidate proposal is blocked by v4 preflight reasons.",
    )
    args = parser.parse_args(argv)

    inputs = tuple(args.inputs) or (DEFAULT_TEMPLATE_PATH,)
    audit = build_staging_audit(inputs, candidate_dir=args.candidate_dir)
    output = args.output or default_output_path(args.format)
    if args.check_output:
        ok, message = check_output(output, audit, args.format)
        print(message)
        if not ok:
            print("run without --check-output to regenerate the staging audit", file=sys.stderr)
            return 1
    else:
        written = write_output(output, audit, args.format)
        print(f"wrote {written}")

    if not audit.template_safe:
        print("v4 metadata checklist template is not safe", file=sys.stderr)
        return 1
    if args.require_outside_candidates and audit.rejected_count:
        print("staged inputs include rejected or active-candidate-directory paths", file=sys.stderr)
        return 1
    if args.require_no_ready and audit.ready_count:
        print("staged inputs include emit-ready candidates; manual review required", file=sys.stderr)
        return 1
    if args.fail_on_blocked and audit.blocked_count:
        print("staged inputs include blocked candidate proposals", file=sys.stderr)
        return 1

    print(f"proposal_count: {audit.proposal_count}")
    print(f"ready_count: {audit.ready_count}")
    print(f"blocked_count: {audit.blocked_count}")
    print(f"rejected_count: {audit.rejected_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
