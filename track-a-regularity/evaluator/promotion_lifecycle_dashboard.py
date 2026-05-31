from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from active_pool_ingress_audit import (
    DEFAULT_JSON_OUTPUT as DEFAULT_INGRESS_JSON,
    build_ingress_audit,
)
from manual_promotion_packet import (
    DEFAULT_JSON_OUTPUT as DEFAULT_PACKET_JSON,
    PromotionPacket,
    build_manual_promotion_report,
)
from proposed_candidate_staging import (
    DEFAULT_CANDIDATE_DIR,
    DEFAULT_JSON_OUTPUT as DEFAULT_STAGING_JSON,
    DEFAULT_TEMPLATE_PATH,
    ProposalAssessment,
    build_staging_audit,
)


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REPORT_DIR = ROOT / "track-a-regularity/reports"
DEFAULT_MARKDOWN_OUTPUT = DEFAULT_REPORT_DIR / "promotion_lifecycle_dashboard.md"
DEFAULT_JSON_OUTPUT = DEFAULT_REPORT_DIR / "promotion_lifecycle_dashboard.json"
NON_CLAIMS = (
    "promotion_lifecycle_dashboard_only",
    "no_file_copy",
    "no_candidate_emission",
    "no_candidate_promotion",
    "no_navier_stokes_solution",
    "no_epsilon_regularity_theorem",
    "no_weak_to_smooth_upgrade",
)


@dataclass(frozen=True)
class LifecycleEntry:
    candidate_id: str
    staged_path: str
    manual_copy_target: str
    staging_status: str
    packet_status: str
    active_pool_status: str
    lifecycle_status: str
    promotion_allowed: bool
    reasons: tuple[str, ...]


@dataclass(frozen=True)
class PromotionLifecycleDashboard:
    schema_version: int
    candidate_dir: str
    staging_report_json: str
    manual_packet_json: str
    ingress_audit_json: str
    proposal_count: int
    staging_ready_count: int
    staging_blocked_count: int
    staging_rejected_count: int
    packet_count: int
    ready_packet_count: int
    blocked_packet_count: int
    rejected_packet_count: int
    active_candidate_file_count: int
    authorized_ingress_count: int
    ingress_violation_count: int
    lifecycle_entry_count: int
    lifecycle_ready_count: int
    lifecycle_blocked_count: int
    lifecycle_rejected_count: int
    lifecycle_authorized_count: int
    lifecycle_violation_count: int
    entries: tuple[LifecycleEntry, ...]
    non_claims: tuple[str, ...]


def _relative(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT.resolve()))
    except ValueError:
        return str(path)


def _resolve(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return ROOT / path


def _dedupe(items: tuple[str, ...]) -> tuple[str, ...]:
    seen: set[str] = set()
    out: list[str] = []
    for item in items:
        if item and item not in seen:
            seen.add(item)
            out.append(item)
    return tuple(out)


def _active_pool_status(
    *,
    packet: PromotionPacket,
    finding_by_target: dict[str, tuple[str, str]],
) -> str:
    target = _resolve(packet.manual_copy_target)
    target_key = str(target.resolve())
    if target_key in finding_by_target:
        severity, finding_type = finding_by_target[target_key]
        if severity == "violation":
            return "violation_present"
        if finding_type == "authorized_ready_packet_target_present":
            return "authorized_present"
    if target.exists():
        if packet.packet_status == "ready_for_manual_copy":
            return "authorized_present"
        return "unauthorized_present"
    return "target_absent"


def _lifecycle_status(
    *,
    proposal: ProposalAssessment,
    packet: PromotionPacket,
    active_pool_status: str,
) -> str:
    if active_pool_status in {"violation_present", "unauthorized_present"}:
        return "ingress_violation"
    if active_pool_status == "authorized_present":
        return "authorized_in_active_pool"
    if proposal.staging_status in {"invalid", "rejected_location"}:
        return "rejected_in_staging"
    if packet.packet_status == "rejected":
        return "rejected_in_packet"
    if proposal.staging_status.startswith("blocked_"):
        return "blocked_in_staging"
    if packet.packet_status == "blocked":
        return "blocked_in_packet"
    if packet.packet_status == "ready_for_manual_copy":
        return "ready_awaiting_manual_copy"
    return "blocked_unknown"


def _entry_reasons(
    proposal: ProposalAssessment,
    packet: PromotionPacket,
    *,
    finding_reason: str = "",
) -> tuple[str, ...]:
    return _dedupe(tuple(proposal.reasons) + tuple(packet.blocking_reasons) + (finding_reason,))


def build_lifecycle_dashboard(
    inputs: tuple[Path, ...] = (DEFAULT_TEMPLATE_PATH,),
    *,
    candidate_dir: Path = DEFAULT_CANDIDATE_DIR,
    packet_json: Path = DEFAULT_PACKET_JSON,
    staging_report_json: Path = DEFAULT_STAGING_JSON,
    ingress_audit_json: Path = DEFAULT_INGRESS_JSON,
) -> PromotionLifecycleDashboard:
    staging = build_staging_audit(inputs, candidate_dir=candidate_dir)
    packet_report = build_manual_promotion_report(inputs, candidate_dir=candidate_dir)
    ingress = build_ingress_audit(candidate_dir=candidate_dir, packet_json=packet_json)

    finding_by_target: dict[str, tuple[str, str]] = {}
    finding_reason_by_target: dict[str, str] = {}
    for finding in ingress.findings:
        path = _resolve(finding.path)
        key = str(path.resolve())
        finding_by_target[key] = (finding.severity, finding.finding_type)
        finding_reason_by_target[key] = finding.reason

    entries: list[LifecycleEntry] = []
    for proposal, packet in zip(staging.proposals, packet_report.packets, strict=True):
        active_status = _active_pool_status(packet=packet, finding_by_target=finding_by_target)
        target_key = str(_resolve(packet.manual_copy_target).resolve())
        status = _lifecycle_status(
            proposal=proposal,
            packet=packet,
            active_pool_status=active_status,
        )
        entries.append(
            LifecycleEntry(
                candidate_id=packet.candidate_id,
                staged_path=packet.staged_path,
                manual_copy_target=packet.manual_copy_target,
                staging_status=proposal.staging_status,
                packet_status=packet.packet_status,
                active_pool_status=active_status,
                lifecycle_status=status,
                promotion_allowed=status == "ready_awaiting_manual_copy",
                reasons=_entry_reasons(
                    proposal,
                    packet,
                    finding_reason=finding_reason_by_target.get(target_key, ""),
                ),
            )
        )

    ready_count = sum(1 for entry in entries if entry.lifecycle_status == "ready_awaiting_manual_copy")
    blocked_count = sum(1 for entry in entries if entry.lifecycle_status.startswith("blocked_"))
    rejected_count = sum(1 for entry in entries if entry.lifecycle_status.startswith("rejected_"))
    authorized_count = sum(1 for entry in entries if entry.lifecycle_status == "authorized_in_active_pool")
    violation_count = sum(1 for entry in entries if entry.lifecycle_status == "ingress_violation")
    return PromotionLifecycleDashboard(
        schema_version=1,
        candidate_dir=_relative(candidate_dir),
        staging_report_json=_relative(staging_report_json),
        manual_packet_json=_relative(packet_json),
        ingress_audit_json=_relative(ingress_audit_json),
        proposal_count=staging.proposal_count,
        staging_ready_count=staging.ready_count,
        staging_blocked_count=staging.blocked_count,
        staging_rejected_count=staging.rejected_count,
        packet_count=packet_report.packet_count,
        ready_packet_count=packet_report.ready_packet_count,
        blocked_packet_count=packet_report.blocked_packet_count,
        rejected_packet_count=packet_report.rejected_packet_count,
        active_candidate_file_count=ingress.active_candidate_file_count,
        authorized_ingress_count=ingress.authorized_ingress_count,
        ingress_violation_count=ingress.violation_count,
        lifecycle_entry_count=len(entries),
        lifecycle_ready_count=ready_count,
        lifecycle_blocked_count=blocked_count,
        lifecycle_rejected_count=rejected_count,
        lifecycle_authorized_count=authorized_count,
        lifecycle_violation_count=violation_count,
        entries=tuple(entries),
        non_claims=NON_CLAIMS,
    )


def dashboard_to_dict(dashboard: PromotionLifecycleDashboard) -> dict[str, object]:
    return {
        "schema_version": dashboard.schema_version,
        "candidate_dir": dashboard.candidate_dir,
        "staging_report_json": dashboard.staging_report_json,
        "manual_packet_json": dashboard.manual_packet_json,
        "ingress_audit_json": dashboard.ingress_audit_json,
        "proposal_count": dashboard.proposal_count,
        "staging_ready_count": dashboard.staging_ready_count,
        "staging_blocked_count": dashboard.staging_blocked_count,
        "staging_rejected_count": dashboard.staging_rejected_count,
        "packet_count": dashboard.packet_count,
        "ready_packet_count": dashboard.ready_packet_count,
        "blocked_packet_count": dashboard.blocked_packet_count,
        "rejected_packet_count": dashboard.rejected_packet_count,
        "active_candidate_file_count": dashboard.active_candidate_file_count,
        "authorized_ingress_count": dashboard.authorized_ingress_count,
        "ingress_violation_count": dashboard.ingress_violation_count,
        "lifecycle_entry_count": dashboard.lifecycle_entry_count,
        "lifecycle_ready_count": dashboard.lifecycle_ready_count,
        "lifecycle_blocked_count": dashboard.lifecycle_blocked_count,
        "lifecycle_rejected_count": dashboard.lifecycle_rejected_count,
        "lifecycle_authorized_count": dashboard.lifecycle_authorized_count,
        "lifecycle_violation_count": dashboard.lifecycle_violation_count,
        "entries": [asdict(entry) for entry in dashboard.entries],
        "non_claims": list(dashboard.non_claims),
        "docs": {
            "freeze_doc": "docs/CANDIDATE_GENERATION_FREEZE.md",
            "staging_doc": "docs/STEP81_PROPOSED_CANDIDATE_STAGING.md",
            "manual_packet_doc": "docs/STEP82_MANUAL_PROMOTION_PACKET.md",
            "ingress_doc": "docs/STEP83_ACTIVE_POOL_INGRESS_AUDIT.md",
        },
    }


def _format_reasons(reasons: tuple[str, ...]) -> str:
    if not reasons:
        return "`none`"
    return "<br>".join(f"`{reason}`" for reason in reasons)


def _entry_rows(dashboard: PromotionLifecycleDashboard) -> list[str]:
    rows = [
        "| id | staging | packet | active pool | lifecycle | allowed | reasons |",
        "|---|---|---|---|---|---|---|",
    ]
    if not dashboard.entries:
        rows.append("| `none` | `none` | `none` | `none` | `none` | `false` | `no entries` |")
        return rows
    for entry in dashboard.entries:
        rows.append(
            "| "
            f"`{entry.candidate_id}` | "
            f"`{entry.staging_status}` | "
            f"`{entry.packet_status}` | "
            f"`{entry.active_pool_status}` | "
            f"`{entry.lifecycle_status}` | "
            f"`{str(entry.promotion_allowed).lower()}` | "
            f"{_format_reasons(entry.reasons)} |"
        )
    return rows


def render_markdown(dashboard: PromotionLifecycleDashboard) -> str:
    return "\n".join(
        (
            "# Promotion Lifecycle Dashboard",
            "",
            "Generated by `track-a-regularity/evaluator/promotion_lifecycle_dashboard.py`.",
            "",
            "This report ties together the Step 81 staging audit, Step 82 manual promotion packet,",
            "and Step 83 active-pool ingress audit. It is a no-copy review surface and does not",
            "promote candidates.",
            "",
            "## Source Reports",
            "",
            f"- staging_report_json: `{dashboard.staging_report_json}`",
            f"- manual_packet_json: `{dashboard.manual_packet_json}`",
            f"- ingress_audit_json: `{dashboard.ingress_audit_json}`",
            f"- candidate_dir: `{dashboard.candidate_dir}`",
            "",
            "## Summary",
            "",
            f"- proposal_count: `{dashboard.proposal_count}`",
            f"- staging_ready_count: `{dashboard.staging_ready_count}`",
            f"- staging_blocked_count: `{dashboard.staging_blocked_count}`",
            f"- staging_rejected_count: `{dashboard.staging_rejected_count}`",
            f"- packet_count: `{dashboard.packet_count}`",
            f"- ready_packet_count: `{dashboard.ready_packet_count}`",
            f"- blocked_packet_count: `{dashboard.blocked_packet_count}`",
            f"- rejected_packet_count: `{dashboard.rejected_packet_count}`",
            f"- active_candidate_file_count: `{dashboard.active_candidate_file_count}`",
            f"- authorized_ingress_count: `{dashboard.authorized_ingress_count}`",
            f"- ingress_violation_count: `{dashboard.ingress_violation_count}`",
            f"- lifecycle_entry_count: `{dashboard.lifecycle_entry_count}`",
            f"- lifecycle_ready_count: `{dashboard.lifecycle_ready_count}`",
            f"- lifecycle_blocked_count: `{dashboard.lifecycle_blocked_count}`",
            f"- lifecycle_rejected_count: `{dashboard.lifecycle_rejected_count}`",
            f"- lifecycle_authorized_count: `{dashboard.lifecycle_authorized_count}`",
            f"- lifecycle_violation_count: `{dashboard.lifecycle_violation_count}`",
            "",
            "## Lifecycle Entries",
            "",
            *_entry_rows(dashboard),
            "",
            "## Non-Claims",
            "",
            *(f"- `{item}`" for item in dashboard.non_claims),
            "",
        )
    )


def render_json(dashboard: PromotionLifecycleDashboard) -> str:
    return json.dumps(dashboard_to_dict(dashboard), indent=2, sort_keys=True) + "\n"


def render_output(dashboard: PromotionLifecycleDashboard, output_format: str) -> str:
    if output_format == "markdown":
        return render_markdown(dashboard)
    if output_format == "json":
        return render_json(dashboard)
    raise ValueError(f"unknown promotion lifecycle format: {output_format}")


def write_output(output: Path, dashboard: PromotionLifecycleDashboard, output_format: str) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_output(dashboard, output_format), encoding="utf-8")
    return output


def check_output(
    output: Path,
    dashboard: PromotionLifecycleDashboard,
    output_format: str,
) -> tuple[bool, str]:
    expected = render_output(dashboard, output_format)
    if not output.exists():
        return False, f"missing promotion lifecycle dashboard: {output}"
    current = output.read_text(encoding="utf-8")
    if current != expected:
        return False, f"stale promotion lifecycle dashboard: {output}"
    return True, f"fresh promotion lifecycle dashboard: {output}"


def default_output_path(output_format: str) -> Path:
    if output_format == "markdown":
        return DEFAULT_MARKDOWN_OUTPUT
    if output_format == "json":
        return DEFAULT_JSON_OUTPUT
    raise ValueError(f"unknown promotion lifecycle format: {output_format}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Render a no-copy promotion lifecycle dashboard across staging, packet, and ingress audits."
    )
    parser.add_argument(
        "inputs",
        nargs="*",
        type=Path,
        help="Staged YAML file(s) or directories. Defaults to the blocked v4 template.",
    )
    parser.add_argument("--candidate-dir", type=Path, default=DEFAULT_CANDIDATE_DIR)
    parser.add_argument("--packet-json", type=Path, default=DEFAULT_PACKET_JSON)
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument(
        "--check-output",
        action="store_true",
        help="Check that --output already matches the rendered dashboard.",
    )
    parser.add_argument(
        "--require-no-ready",
        action="store_true",
        help="Fail if the lifecycle contains a ready-for-manual-copy staged candidate.",
    )
    parser.add_argument(
        "--require-clean",
        action="store_true",
        help="Fail if the lifecycle or ingress audit reports an active-pool violation.",
    )
    args = parser.parse_args(argv)

    inputs = tuple(args.inputs) or (DEFAULT_TEMPLATE_PATH,)
    try:
        dashboard = build_lifecycle_dashboard(
            inputs,
            candidate_dir=args.candidate_dir,
            packet_json=args.packet_json,
        )
    except Exception as exc:  # noqa: BLE001 - CLI should report dashboard setup failures.
        print(f"failed to build promotion lifecycle dashboard: {exc}", file=sys.stderr)
        return 1

    output = args.output or default_output_path(args.format)
    if args.check_output:
        ok, message = check_output(output, dashboard, args.format)
        print(message)
        if not ok:
            print("run without --check-output to regenerate the promotion lifecycle dashboard", file=sys.stderr)
            return 1
    else:
        written = write_output(output, dashboard, args.format)
        print(f"wrote {written}")

    if args.require_no_ready and dashboard.lifecycle_ready_count:
        print("promotion lifecycle contains ready staged candidates; manual review required", file=sys.stderr)
        return 1
    if args.require_clean and (
        dashboard.lifecycle_violation_count or dashboard.ingress_violation_count
    ):
        print("promotion lifecycle contains active-pool ingress violations", file=sys.stderr)
        return 1

    print(f"lifecycle_entry_count: {dashboard.lifecycle_entry_count}")
    print(f"lifecycle_ready_count: {dashboard.lifecycle_ready_count}")
    print(f"lifecycle_blocked_count: {dashboard.lifecycle_blocked_count}")
    print(f"lifecycle_authorized_count: {dashboard.lifecycle_authorized_count}")
    print(f"lifecycle_violation_count: {dashboard.lifecycle_violation_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
