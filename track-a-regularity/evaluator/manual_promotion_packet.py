from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from generation_spec_v4 import (
    BLOCKER_SOURCE_INDEX_JSON_KEY,
    BLOCKER_SOURCE_INDEX_MARKDOWN_KEY,
    PROOF_OBLIGATION_REPORT_KEY,
    PROOF_OBLIGATION_SUMMARY_KEY,
)
from proposed_candidate_staging import (
    DEFAULT_CANDIDATE_DIR,
    DEFAULT_TEMPLATE_PATH,
    ProposalAssessment,
    assess_proposal,
    build_staging_audit,
)
from schema import LemmaCandidate, load_candidate


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REPORT_DIR = ROOT / "track-a-regularity/reports"
DEFAULT_MARKDOWN_OUTPUT = DEFAULT_REPORT_DIR / "manual_promotion_packet.md"
DEFAULT_JSON_OUTPUT = DEFAULT_REPORT_DIR / "manual_promotion_packet.json"
NON_CLAIMS = (
    "manual_packet_only",
    "no_file_copy",
    "no_candidate_emission",
    "no_candidate_promotion",
    "no_navier_stokes_solution",
    "no_epsilon_regularity_theorem",
    "no_weak_to_smooth_upgrade",
)


@dataclass(frozen=True)
class PromotionRequirement:
    key: str
    artifact: str
    required_state: str
    current_state: str
    satisfied: bool
    purpose: str


@dataclass(frozen=True)
class PromotionPacket:
    candidate_id: str
    staged_path: str
    manual_copy_target: str
    staging_status: str
    packet_status: str
    pre_copy_requirements: tuple[PromotionRequirement, ...]
    post_copy_manual_actions: tuple[str, ...]
    blocking_reasons: tuple[str, ...]


@dataclass(frozen=True)
class ManualPromotionPacketReport:
    schema_version: int
    proposal_count: int
    packet_count: int
    ready_packet_count: int
    blocked_packet_count: int
    rejected_packet_count: int
    candidate_dir: str
    packets: tuple[PromotionPacket, ...]
    non_claims: tuple[str, ...]


def _relative(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT.resolve()))
    except ValueError:
        return str(path)


def _metadata_path(candidate: LemmaCandidate, key: str) -> Path | None:
    value = candidate.expected_evaluator.get(key)
    if not isinstance(value, str) or not value.strip():
        return None
    path = Path(value)
    if not path.is_absolute():
        path = ROOT / path
    return path


def _requirement(
    *,
    key: str,
    artifact: str,
    required_state: str,
    current_state: str,
    satisfied: bool,
    purpose: str,
) -> PromotionRequirement:
    return PromotionRequirement(
        key=key,
        artifact=artifact,
        required_state=required_state,
        current_state=current_state,
        satisfied=satisfied,
        purpose=purpose,
    )


def _metadata_requirement(candidate: LemmaCandidate, key: str, purpose: str) -> PromotionRequirement:
    path = _metadata_path(candidate, key)
    if path is None:
        return _requirement(
            key=key,
            artifact=f"expected_evaluator.{key}",
            required_state="non-empty path that exists",
            current_state="missing",
            satisfied=False,
            purpose=purpose,
        )
    return _requirement(
        key=key,
        artifact=_relative(path),
        required_state="path exists and is checked by v4 preflight",
        current_state="exists" if path.exists() else "missing",
        satisfied=path.exists(),
        purpose=purpose,
    )


def _manual_actions(candidate_id: str, staged_path: str, target: str) -> tuple[str, ...]:
    return (
        f"cp {staged_path} {target}",
        f"python track-a-regularity/evaluator/preflight_v4.py {target}",
        (
            "python track-a-regularity/evaluator/run_all.py "
            f"{target} --check-expected --log-dir logs/<step82_or_later>_eval"
        ),
        "bash scripts/verify_reproducibility.sh",
        (
            "update docs/SUMMARY.md, docs/ROADMAP_STEPS.md, shared-context, hot-codex, "
            f"and a step log for {candidate_id}"
        ),
    )


def build_packet_for_proposal(
    proposal: ProposalAssessment,
    *,
    candidate_dir: Path = DEFAULT_CANDIDATE_DIR,
) -> PromotionPacket:
    candidate: LemmaCandidate | None = None
    if proposal.loadable:
        candidate = load_candidate(ROOT / proposal.path if not Path(proposal.path).is_absolute() else Path(proposal.path))

    candidate_id = proposal.candidate_id or "unloadable"
    target_path = candidate_dir / f"{candidate_id}.yaml"
    staged_path = proposal.path
    requirements: list[PromotionRequirement] = [
        _requirement(
            key="staged_yaml_loadable",
            artifact=staged_path,
            required_state="loadable LemmaCandidate YAML",
            current_state="loadable" if proposal.loadable else "invalid",
            satisfied=proposal.loadable,
            purpose="A packet can only describe a parsed candidate record.",
        ),
        _requirement(
            key="outside_active_candidate_dir",
            artifact=staged_path,
            required_state="outside track-a-regularity/candidates/",
            current_state="outside" if not proposal.inside_active_candidate_dir else "inside active candidate dir",
            satisfied=not proposal.inside_active_candidate_dir,
            purpose="Future candidates must be audited before they enter the active pool.",
        ),
        _requirement(
            key="staging_audit_ready",
            artifact="track-a-regularity/reports/proposed_candidate_staging_audit.md",
            required_state="ready_for_manual_copy",
            current_state=proposal.staging_status,
            satisfied=proposal.staging_status == "ready_for_manual_copy",
            purpose="The Step 81 staging audit must pass before manual copy is considered.",
        ),
        _requirement(
            key="expected_status_candidate",
            artifact=f"{staged_path}:expected_evaluator.status",
            required_state="candidate",
            current_state=proposal.expected_status or "missing",
            satisfied=proposal.expected_status == "candidate",
            purpose="Only explicit v4 candidate-status records may enter the active pool.",
        ),
        _requirement(
            key="v4_emit_ready",
            artifact=f"{staged_path}:related_known/expected_evaluator",
            required_state="emit_ready true",
            current_state=str(proposal.emit_ready).lower(),
            satisfied=proposal.emit_ready,
            purpose="The v4 preflight gate must have no unresolved metadata blockers.",
        ),
        _requirement(
            key="manual_copy_target_absent",
            artifact=_relative(target_path),
            required_state="target file absent before manual copy",
            current_state="exists" if target_path.exists() else "absent",
            satisfied=not target_path.exists(),
            purpose="Manual copy must not overwrite an existing active candidate.",
        ),
    ]

    if candidate is None:
        for key, purpose in (
            (PROOF_OBLIGATION_REPORT_KEY, "Full candidate-specific proof-obligation node report."),
            (PROOF_OBLIGATION_SUMMARY_KEY, "Fresh zero-blocker proof-obligation summary."),
            (BLOCKER_SOURCE_INDEX_MARKDOWN_KEY, "Human-readable blocker provenance dashboard."),
            (BLOCKER_SOURCE_INDEX_JSON_KEY, "Machine-readable blocker provenance dashboard."),
        ):
            requirements.append(
                _requirement(
                    key=key,
                    artifact=f"expected_evaluator.{key}",
                    required_state="non-empty path that exists",
                    current_state="unavailable because YAML did not load",
                    satisfied=False,
                    purpose=purpose,
                )
            )
    else:
        requirements.extend(
            (
                _metadata_requirement(
                    candidate,
                    PROOF_OBLIGATION_REPORT_KEY,
                    "Full candidate-specific proof-obligation node report.",
                ),
                _metadata_requirement(
                    candidate,
                    PROOF_OBLIGATION_SUMMARY_KEY,
                    "Fresh zero-blocker proof-obligation summary.",
                ),
                _metadata_requirement(
                    candidate,
                    BLOCKER_SOURCE_INDEX_MARKDOWN_KEY,
                    "Human-readable blocker provenance dashboard.",
                ),
                _metadata_requirement(
                    candidate,
                    BLOCKER_SOURCE_INDEX_JSON_KEY,
                    "Machine-readable blocker provenance dashboard.",
                ),
            )
        )

    blocking_reasons = tuple(
        requirement.key for requirement in requirements if not requirement.satisfied
    ) + proposal.reasons
    if proposal.staging_status in {"invalid", "rejected_location"}:
        packet_status = "rejected"
    elif blocking_reasons:
        packet_status = "blocked"
    else:
        packet_status = "ready_for_manual_copy"

    return PromotionPacket(
        candidate_id=candidate_id,
        staged_path=staged_path,
        manual_copy_target=_relative(target_path),
        staging_status=proposal.staging_status,
        packet_status=packet_status,
        pre_copy_requirements=tuple(requirements),
        post_copy_manual_actions=_manual_actions(candidate_id, staged_path, _relative(target_path)),
        blocking_reasons=blocking_reasons,
    )


def build_manual_promotion_report(
    inputs: tuple[Path, ...] = (DEFAULT_TEMPLATE_PATH,),
    *,
    candidate_dir: Path = DEFAULT_CANDIDATE_DIR,
) -> ManualPromotionPacketReport:
    staging_audit = build_staging_audit(inputs, candidate_dir=candidate_dir)
    packets = tuple(
        build_packet_for_proposal(proposal, candidate_dir=candidate_dir)
        for proposal in staging_audit.proposals
    )
    ready_count = sum(1 for packet in packets if packet.packet_status == "ready_for_manual_copy")
    blocked_count = sum(1 for packet in packets if packet.packet_status == "blocked")
    rejected_count = sum(1 for packet in packets if packet.packet_status == "rejected")
    return ManualPromotionPacketReport(
        schema_version=1,
        proposal_count=staging_audit.proposal_count,
        packet_count=len(packets),
        ready_packet_count=ready_count,
        blocked_packet_count=blocked_count,
        rejected_packet_count=rejected_count,
        candidate_dir=_relative(candidate_dir),
        packets=packets,
        non_claims=NON_CLAIMS,
    )


def report_to_dict(report: ManualPromotionPacketReport) -> dict[str, object]:
    return {
        "schema_version": report.schema_version,
        "proposal_count": report.proposal_count,
        "packet_count": report.packet_count,
        "ready_packet_count": report.ready_packet_count,
        "blocked_packet_count": report.blocked_packet_count,
        "rejected_packet_count": report.rejected_packet_count,
        "candidate_dir": report.candidate_dir,
        "packets": [asdict(packet) for packet in report.packets],
        "non_claims": list(report.non_claims),
        "docs": {
            "generation_spec": "docs/CANDIDATE_GENERATION_SPEC_V4.md",
            "freeze_doc": "docs/CANDIDATE_GENERATION_FREEZE.md",
            "staging_doc": "docs/STEP81_PROPOSED_CANDIDATE_STAGING.md",
        },
    }


def _format_requirement_rows(packet: PromotionPacket) -> list[str]:
    rows = [
        "| key | artifact | required state | current state | satisfied | purpose |",
        "|---|---|---|---|---|---|",
    ]
    for requirement in packet.pre_copy_requirements:
        rows.append(
            "| "
            f"`{requirement.key}` | "
            f"`{requirement.artifact}` | "
            f"`{requirement.required_state}` | "
            f"`{requirement.current_state}` | "
            f"`{str(requirement.satisfied).lower()}` | "
            f"{requirement.purpose} |"
        )
    return rows


def render_markdown(report: ManualPromotionPacketReport) -> str:
    packet_sections: list[str] = []
    for packet in report.packets:
        packet_sections.extend(
            [
                f"### `{packet.candidate_id}`",
                "",
                f"- staged_path: `{packet.staged_path}`",
                f"- manual_copy_target: `{packet.manual_copy_target}`",
                f"- staging_status: `{packet.staging_status}`",
                f"- packet_status: `{packet.packet_status}`",
                "",
                "#### Pre-Copy Requirements",
                "",
                *_format_requirement_rows(packet),
                "",
                "#### Post-Copy Manual Actions",
                "",
                *(f"- `{action}`" for action in packet.post_copy_manual_actions),
                "",
                "#### Blocking Reasons",
                "",
                *(f"- `{reason}`" for reason in packet.blocking_reasons or ("none",)),
                "",
            ]
        )

    return "\n".join(
        (
            "# Manual Promotion Packet",
            "",
            "Generated by `track-a-regularity/evaluator/manual_promotion_packet.py`.",
            "",
            "This report lists the exact pre-copy artifacts and post-copy manual actions required",
            "before any staged YAML can enter `track-a-regularity/candidates/`. It does not copy",
            "files and does not promote candidates.",
            "",
            "## Summary",
            "",
            f"- candidate_dir: `{report.candidate_dir}`",
            f"- proposal_count: `{report.proposal_count}`",
            f"- packet_count: `{report.packet_count}`",
            f"- ready_packet_count: `{report.ready_packet_count}`",
            f"- blocked_packet_count: `{report.blocked_packet_count}`",
            f"- rejected_packet_count: `{report.rejected_packet_count}`",
            "",
            "## Packets",
            "",
            *packet_sections,
            "## Non-Claims",
            "",
            *(f"- `{item}`" for item in report.non_claims),
            "",
        )
    )


def render_json(report: ManualPromotionPacketReport) -> str:
    return json.dumps(report_to_dict(report), indent=2, sort_keys=True) + "\n"


def render_output(report: ManualPromotionPacketReport, output_format: str) -> str:
    if output_format == "markdown":
        return render_markdown(report)
    if output_format == "json":
        return render_json(report)
    raise ValueError(f"unknown manual promotion packet format: {output_format}")


def write_output(output: Path, report: ManualPromotionPacketReport, output_format: str) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_output(report, output_format), encoding="utf-8")
    return output


def check_output(
    output: Path,
    report: ManualPromotionPacketReport,
    output_format: str,
) -> tuple[bool, str]:
    expected = render_output(report, output_format)
    if not output.exists():
        return False, f"missing manual promotion packet: {output}"
    current = output.read_text(encoding="utf-8")
    if current != expected:
        return False, f"stale manual promotion packet: {output}"
    return True, f"fresh manual promotion packet: {output}"


def default_output_path(output_format: str) -> Path:
    if output_format == "markdown":
        return DEFAULT_MARKDOWN_OUTPUT
    if output_format == "json":
        return DEFAULT_JSON_OUTPUT
    raise ValueError(f"unknown manual promotion packet format: {output_format}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Render a no-copy manual packet for staged candidate promotion review."
    )
    parser.add_argument(
        "inputs",
        nargs="*",
        type=Path,
        help="Staged YAML file(s) or directories. Defaults to the blocked v4 template.",
    )
    parser.add_argument("--candidate-dir", type=Path, default=DEFAULT_CANDIDATE_DIR)
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument(
        "--check-output",
        action="store_true",
        help="Check that --output already matches the rendered packet report.",
    )
    parser.add_argument(
        "--require-no-ready",
        action="store_true",
        help="Fail if any packet is ready for manual copy.",
    )
    parser.add_argument(
        "--require-no-rejected",
        action="store_true",
        help="Fail if any packet is rejected because the staged input is invalid or already active.",
    )
    args = parser.parse_args(argv)

    inputs = tuple(args.inputs) or (DEFAULT_TEMPLATE_PATH,)
    report = build_manual_promotion_report(inputs, candidate_dir=args.candidate_dir)
    output = args.output or default_output_path(args.format)

    if args.check_output:
        ok, message = check_output(output, report, args.format)
        print(message)
        if not ok:
            print("run without --check-output to regenerate the manual promotion packet", file=sys.stderr)
            return 1
    else:
        written = write_output(output, report, args.format)
        print(f"wrote {written}")

    if args.require_no_ready and report.ready_packet_count:
        print("manual promotion packet contains ready staged candidates", file=sys.stderr)
        return 1
    if args.require_no_rejected and report.rejected_packet_count:
        print("manual promotion packet contains rejected staged inputs", file=sys.stderr)
        return 1

    print(f"packet_count: {report.packet_count}")
    print(f"ready_packet_count: {report.ready_packet_count}")
    print(f"blocked_packet_count: {report.blocked_packet_count}")
    print(f"rejected_packet_count: {report.rejected_packet_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
