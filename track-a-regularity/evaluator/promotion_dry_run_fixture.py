from __future__ import annotations

import argparse
import json
import shutil
import sys
import tempfile
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from active_pool_ingress_audit import (
    build_ingress_audit,
    render_json as render_ingress_json,
)
from candidate_obligation_template import (
    TEMPLATE_OBLIGATIONS,
    build_candidate_obligation_report,
    write_report_and_summary,
)
from generation_spec_v4 import (
    BLOCKER_SOURCE_INDEX_JSON_KEY,
    BLOCKER_SOURCE_INDEX_MARKDOWN_KEY,
    PROOF_OBLIGATION_REPORT_KEY,
    PROOF_OBLIGATION_SUMMARY_KEY,
    REQUIRED_MARKERS,
)
from manual_promotion_packet import (
    build_manual_promotion_report,
    render_json as render_packet_json,
)
from needs_review_blocker_sources import build_source_index, write_output as write_source_index
from promotion_lifecycle_dashboard import build_lifecycle_dashboard
from proposed_candidate_staging import DEFAULT_CANDIDATE_DIR, build_staging_audit


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REPORT_DIR = ROOT / "track-a-regularity/reports"
DEFAULT_MARKDOWN_OUTPUT = DEFAULT_REPORT_DIR / "promotion_dry_run_fixture.md"
DEFAULT_JSON_OUTPUT = DEFAULT_REPORT_DIR / "promotion_dry_run_fixture.json"
DRY_RUN_CANDIDATE_ID = "lemma_step85_dry_run"
TMP_TOKEN = "<tmp>"
NON_CLAIMS = (
    "temporary_fixture_only",
    "synthetic_candidate_only",
    "no_real_candidate_pool_write",
    "no_candidate_emission",
    "no_candidate_promotion",
    "no_navier_stokes_solution",
    "no_epsilon_regularity_theorem",
    "no_weak_to_smooth_upgrade",
)


@dataclass(frozen=True)
class DryRunPhase:
    name: str
    passed: bool
    details: dict[str, Any]


@dataclass(frozen=True)
class PromotionDryRunReport:
    schema_version: int
    candidate_id: str
    dry_run_passed: bool
    temp_root_removed: bool
    real_candidate_dir: str
    real_candidate_pool_untouched: bool
    real_candidate_file_count_before: int
    real_candidate_file_count_after: int
    phases: tuple[DryRunPhase, ...]
    non_claims: tuple[str, ...]


def _relative(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT.resolve()))
    except ValueError:
        return str(path)


def _candidate_snapshot() -> tuple[str, ...]:
    if not DEFAULT_CANDIDATE_DIR.exists():
        return ()
    return tuple(sorted(path.name for path in DEFAULT_CANDIDATE_DIR.glob("lemma_*.yaml")))


def _normalizer(temp_root: Path):
    temp_roots = (str(temp_root), str(temp_root.resolve()))

    def normalize(value: Any) -> Any:
        if isinstance(value, Path):
            return normalize(str(value))
        if isinstance(value, str):
            normalized = value
            for root_text in temp_roots:
                normalized = normalized.replace(root_text, TMP_TOKEN)
            return normalized
        if isinstance(value, tuple):
            return [normalize(item) for item in value]
        if isinstance(value, list):
            return [normalize(item) for item in value]
        if isinstance(value, dict):
            return {str(key): normalize(item) for key, item in value.items()}
        return value

    return normalize


def _write_source_indexes(report_dir: Path) -> tuple[Path, Path]:
    source_index = build_source_index()
    markdown_path = report_dir / "needs_review_blocker_sources.md"
    json_path = report_dir / "needs_review_blocker_sources.json"
    write_source_index(markdown_path, source_index, "markdown")
    write_source_index(json_path, source_index, "json")
    return markdown_path, json_path


def _write_zero_blocker_sidecars(report_dir: Path, candidate_id: str) -> tuple[Path, Path]:
    discharged = {obligation.key for obligation in TEMPLATE_OBLIGATIONS}
    report = build_candidate_obligation_report(
        candidate_id,
        candidate_status="candidate",
        active_candidate=True,
        discharged_keys=discharged,
    )
    report_path = report_dir / f"{candidate_id}_proof_obligations.json"
    summary_path = report_dir / f"{candidate_id}_proof_obligation_summary.json"
    return write_report_and_summary(report_path, summary_path, report)


def _write_candidate_yaml(
    output: Path,
    *,
    candidate_id: str,
    proof_report: Path,
    proof_summary: Path,
    source_markdown: Path,
    source_json: Path,
) -> Path:
    related_known = "\n".join(f"  - {marker}" for marker in REQUIRED_MARKERS)
    expected_evaluator = {
        "status": "candidate",
        PROOF_OBLIGATION_REPORT_KEY: str(proof_report),
        PROOF_OBLIGATION_SUMMARY_KEY: str(proof_summary),
        BLOCKER_SOURCE_INDEX_MARKDOWN_KEY: str(source_markdown),
        BLOCKER_SOURCE_INDEX_JSON_KEY: str(source_json),
    }
    expected_yaml = "\n".join(
        f"  {key}: {json.dumps(value)}" for key, value in expected_evaluator.items()
    )
    output.write_text(
        f"""
id: {candidate_id}
generated_by: codex-step85-dry-run
date: 2026-05-20
statement_en: >
  Let u be a smooth classical solution on [0,T) x T^3. Define X(u) as the
  indexed L4_t Besov B^{{1/2}}_{{2,1}} norm on that cylinder, with exact
  quantity definitions, function spaces, known-result separation, and proof
  route recorded in the dry-run sidecars. If X(u) is finite and the proof
  route derives BKM continuation without changing solution class, then u
  extends smoothly past T.
statement_lean_skel: "def {candidate_id} : Prop := True"
type: step85_promotion_dry_run_fixture
related_known:
{related_known}
evaluator: {{}}
expected_evaluator:
{expected_yaml}
status: pending
why_interesting: Synthetic end-to-end promotion lifecycle dry-run fixture.
""".lstrip(),
        encoding="utf-8",
    )
    return output


def _phase(
    name: str,
    *,
    passed: bool,
    details: dict[str, Any],
    normalize,
) -> DryRunPhase:
    return DryRunPhase(name=name, passed=passed, details=normalize(details))


def build_promotion_dry_run_report() -> PromotionDryRunReport:
    before = _candidate_snapshot()
    temp_root = Path(tempfile.mkdtemp(prefix="ns_step85_promotion_dry_run_"))
    normalize = _normalizer(temp_root)
    phases: list[DryRunPhase] = []

    try:
        staging_dir = temp_root / "staging"
        candidate_dir = temp_root / "active_candidates"
        report_dir = temp_root / "reports"
        staging_dir.mkdir(parents=True)
        candidate_dir.mkdir(parents=True)
        report_dir.mkdir(parents=True)

        proof_report, proof_summary = _write_zero_blocker_sidecars(
            report_dir,
            DRY_RUN_CANDIDATE_ID,
        )
        source_markdown, source_json = _write_source_indexes(report_dir)
        staged_yaml = _write_candidate_yaml(
            staging_dir / f"{DRY_RUN_CANDIDATE_ID}.yaml",
            candidate_id=DRY_RUN_CANDIDATE_ID,
            proof_report=proof_report,
            proof_summary=proof_summary,
            source_markdown=source_markdown,
            source_json=source_json,
        )

        staging = build_staging_audit((staged_yaml,), candidate_dir=candidate_dir)
        staging_passed = (
            staging.proposal_count == 1
            and staging.ready_count == 1
            and staging.blocked_count == 0
            and staging.rejected_count == 0
            and staging.proposals[0].staging_status == "ready_for_manual_copy"
            and staging.proposals[0].emit_ready
        )
        phases.append(
            _phase(
                "staging_ready",
                passed=staging_passed,
                details={
                    "proposal_count": staging.proposal_count,
                    "ready_count": staging.ready_count,
                    "blocked_count": staging.blocked_count,
                    "rejected_count": staging.rejected_count,
                    "staging_status": staging.proposals[0].staging_status,
                    "emit_ready": staging.proposals[0].emit_ready,
                    "inside_active_candidate_dir": staging.proposals[0].inside_active_candidate_dir,
                },
                normalize=normalize,
            )
        )

        packet_report = build_manual_promotion_report((staged_yaml,), candidate_dir=candidate_dir)
        packet_json = report_dir / "manual_promotion_packet.json"
        packet_json.write_text(render_packet_json(packet_report), encoding="utf-8")
        packet = packet_report.packets[0]
        packet_passed = (
            packet_report.packet_count == 1
            and packet_report.ready_packet_count == 1
            and packet_report.blocked_packet_count == 0
            and packet_report.rejected_packet_count == 0
            and packet.packet_status == "ready_for_manual_copy"
            and not packet.blocking_reasons
        )
        phases.append(
            _phase(
                "manual_packet_ready",
                passed=packet_passed,
                details={
                    "packet_count": packet_report.packet_count,
                    "ready_packet_count": packet_report.ready_packet_count,
                    "blocked_packet_count": packet_report.blocked_packet_count,
                    "rejected_packet_count": packet_report.rejected_packet_count,
                    "packet_status": packet.packet_status,
                    "manual_copy_target": packet.manual_copy_target,
                    "blocking_reasons": packet.blocking_reasons,
                },
                normalize=normalize,
            )
        )

        pre_ingress = build_ingress_audit(candidate_dir=candidate_dir, packet_json=packet_json)
        pre_ingress_json = report_dir / "active_pool_ingress_before_copy.json"
        pre_ingress_json.write_text(render_ingress_json(pre_ingress), encoding="utf-8")
        pre_ingress_passed = (
            pre_ingress.active_candidate_file_count == 0
            and pre_ingress.tracked_target_absent_count == 1
            and pre_ingress.authorized_ingress_count == 0
            and pre_ingress.violation_count == 0
        )
        phases.append(
            _phase(
                "pre_copy_ingress_clean",
                passed=pre_ingress_passed,
                details={
                    "active_candidate_file_count": pre_ingress.active_candidate_file_count,
                    "tracked_target_absent_count": pre_ingress.tracked_target_absent_count,
                    "authorized_ingress_count": pre_ingress.authorized_ingress_count,
                    "violation_count": pre_ingress.violation_count,
                },
                normalize=normalize,
            )
        )

        pre_lifecycle = build_lifecycle_dashboard(
            (staged_yaml,),
            candidate_dir=candidate_dir,
            packet_json=packet_json,
            ingress_audit_json=pre_ingress_json,
        )
        pre_lifecycle_passed = (
            pre_lifecycle.lifecycle_entry_count == 1
            and pre_lifecycle.lifecycle_ready_count == 1
            and pre_lifecycle.lifecycle_authorized_count == 0
            and pre_lifecycle.lifecycle_violation_count == 0
            and pre_lifecycle.entries[0].lifecycle_status == "ready_awaiting_manual_copy"
            and pre_lifecycle.entries[0].promotion_allowed
        )
        phases.append(
            _phase(
                "pre_copy_lifecycle_ready",
                passed=pre_lifecycle_passed,
                details={
                    "lifecycle_entry_count": pre_lifecycle.lifecycle_entry_count,
                    "lifecycle_ready_count": pre_lifecycle.lifecycle_ready_count,
                    "lifecycle_authorized_count": pre_lifecycle.lifecycle_authorized_count,
                    "lifecycle_violation_count": pre_lifecycle.lifecycle_violation_count,
                    "lifecycle_status": pre_lifecycle.entries[0].lifecycle_status,
                    "promotion_allowed": pre_lifecycle.entries[0].promotion_allowed,
                },
                normalize=normalize,
            )
        )

        temp_target = candidate_dir / f"{DRY_RUN_CANDIDATE_ID}.yaml"
        shutil.copyfile(staged_yaml, temp_target)
        phases.append(
            _phase(
                "temp_active_pool_copy",
                passed=temp_target.exists() and not str(temp_target).startswith(str(DEFAULT_CANDIDATE_DIR)),
                details={
                    "copied_to": str(temp_target),
                    "real_candidate_dir": str(DEFAULT_CANDIDATE_DIR),
                    "uses_real_candidate_dir": False,
                },
                normalize=normalize,
            )
        )

        post_ingress = build_ingress_audit(candidate_dir=candidate_dir, packet_json=packet_json)
        post_ingress_json = report_dir / "active_pool_ingress_after_copy.json"
        post_ingress_json.write_text(render_ingress_json(post_ingress), encoding="utf-8")
        post_ingress_passed = (
            post_ingress.active_candidate_file_count == 1
            and post_ingress.tracked_target_absent_count == 0
            and post_ingress.authorized_ingress_count == 1
            and post_ingress.violation_count == 0
        )
        phases.append(
            _phase(
                "post_copy_ingress_authorized",
                passed=post_ingress_passed,
                details={
                    "active_candidate_file_count": post_ingress.active_candidate_file_count,
                    "tracked_target_absent_count": post_ingress.tracked_target_absent_count,
                    "authorized_ingress_count": post_ingress.authorized_ingress_count,
                    "violation_count": post_ingress.violation_count,
                    "finding_type": post_ingress.findings[0].finding_type
                    if post_ingress.findings
                    else "",
                },
                normalize=normalize,
            )
        )

        post_lifecycle = build_lifecycle_dashboard(
            (staged_yaml,),
            candidate_dir=candidate_dir,
            packet_json=packet_json,
            ingress_audit_json=post_ingress_json,
        )
        post_lifecycle_passed = (
            post_lifecycle.lifecycle_entry_count == 1
            and post_lifecycle.lifecycle_ready_count == 0
            and post_lifecycle.lifecycle_authorized_count == 1
            and post_lifecycle.lifecycle_violation_count == 0
            and post_lifecycle.entries[0].lifecycle_status == "authorized_in_active_pool"
            and not post_lifecycle.entries[0].promotion_allowed
        )
        phases.append(
            _phase(
                "post_copy_lifecycle_authorized",
                passed=post_lifecycle_passed,
                details={
                    "lifecycle_entry_count": post_lifecycle.lifecycle_entry_count,
                    "lifecycle_ready_count": post_lifecycle.lifecycle_ready_count,
                    "lifecycle_authorized_count": post_lifecycle.lifecycle_authorized_count,
                    "lifecycle_violation_count": post_lifecycle.lifecycle_violation_count,
                    "lifecycle_status": post_lifecycle.entries[0].lifecycle_status,
                    "promotion_allowed": post_lifecycle.entries[0].promotion_allowed,
                },
                normalize=normalize,
            )
        )
    finally:
        if temp_root.exists():
            shutil.rmtree(temp_root)

    after = _candidate_snapshot()
    real_untouched = before == after
    cleanup_complete = not temp_root.exists()
    all_passed = all(phase.passed for phase in phases) and real_untouched and cleanup_complete
    return PromotionDryRunReport(
        schema_version=1,
        candidate_id=DRY_RUN_CANDIDATE_ID,
        dry_run_passed=all_passed,
        temp_root_removed=cleanup_complete,
        real_candidate_dir=_relative(DEFAULT_CANDIDATE_DIR),
        real_candidate_pool_untouched=real_untouched,
        real_candidate_file_count_before=len(before),
        real_candidate_file_count_after=len(after),
        phases=tuple(phases),
        non_claims=NON_CLAIMS,
    )


def report_to_dict(report: PromotionDryRunReport) -> dict[str, Any]:
    return {
        "schema_version": report.schema_version,
        "candidate_id": report.candidate_id,
        "dry_run_passed": report.dry_run_passed,
        "temp_root_removed": report.temp_root_removed,
        "real_candidate_dir": report.real_candidate_dir,
        "real_candidate_pool_untouched": report.real_candidate_pool_untouched,
        "real_candidate_file_count_before": report.real_candidate_file_count_before,
        "real_candidate_file_count_after": report.real_candidate_file_count_after,
        "phases": [asdict(phase) for phase in report.phases],
        "non_claims": list(report.non_claims),
        "docs": {
            "freeze_doc": "docs/CANDIDATE_GENERATION_FREEZE.md",
            "lifecycle_doc": "docs/STEP84_PROMOTION_LIFECYCLE_DASHBOARD.md",
        },
    }


def _format_details(details: dict[str, Any]) -> str:
    if not details:
        return "`none`"
    return "<br>".join(f"`{key}={value}`" for key, value in details.items())


def render_markdown(report: PromotionDryRunReport) -> str:
    phase_rows = [
        "| phase | passed | details |",
        "|---|---|---|",
    ]
    for phase in report.phases:
        phase_rows.append(
            "| "
            f"`{phase.name}` | "
            f"`{str(phase.passed).lower()}` | "
            f"{_format_details(phase.details)} |"
        )

    return "\n".join(
        (
            "# Promotion Dry-Run Fixture",
            "",
            "Generated by `track-a-regularity/evaluator/promotion_dry_run_fixture.py`.",
            "",
            "This report exercises a synthetic ready candidate through staging, manual packet,",
            "promotion lifecycle, and active-pool ingress checks in a temporary directory only.",
            "It never writes to the real `track-a-regularity/candidates/` directory.",
            "",
            "## Summary",
            "",
            f"- candidate_id: `{report.candidate_id}`",
            f"- dry_run_passed: `{str(report.dry_run_passed).lower()}`",
            f"- temp_root_removed: `{str(report.temp_root_removed).lower()}`",
            f"- real_candidate_dir: `{report.real_candidate_dir}`",
            f"- real_candidate_pool_untouched: `{str(report.real_candidate_pool_untouched).lower()}`",
            f"- real_candidate_file_count_before: `{report.real_candidate_file_count_before}`",
            f"- real_candidate_file_count_after: `{report.real_candidate_file_count_after}`",
            "",
            "## Phases",
            "",
            *phase_rows,
            "",
            "## Non-Claims",
            "",
            *(f"- `{item}`" for item in report.non_claims),
            "",
        )
    )


def render_json(report: PromotionDryRunReport) -> str:
    return json.dumps(report_to_dict(report), indent=2, sort_keys=True) + "\n"


def render_output(report: PromotionDryRunReport, output_format: str) -> str:
    if output_format == "markdown":
        return render_markdown(report)
    if output_format == "json":
        return render_json(report)
    raise ValueError(f"unknown promotion dry-run format: {output_format}")


def write_output(output: Path, report: PromotionDryRunReport, output_format: str) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_output(report, output_format), encoding="utf-8")
    return output


def check_output(
    output: Path,
    report: PromotionDryRunReport,
    output_format: str,
) -> tuple[bool, str]:
    expected = render_output(report, output_format)
    if not output.exists():
        return False, f"missing promotion dry-run fixture report: {output}"
    current = output.read_text(encoding="utf-8")
    if current != expected:
        return False, f"stale promotion dry-run fixture report: {output}"
    return True, f"fresh promotion dry-run fixture report: {output}"


def default_output_path(output_format: str) -> Path:
    if output_format == "markdown":
        return DEFAULT_MARKDOWN_OUTPUT
    if output_format == "json":
        return DEFAULT_JSON_OUTPUT
    raise ValueError(f"unknown promotion dry-run format: {output_format}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run an end-to-end temporary promotion dry-run without touching real candidates."
    )
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument(
        "--check-output",
        action="store_true",
        help="Check that --output already matches the rendered dry-run report.",
    )
    parser.add_argument(
        "--require-pass",
        action="store_true",
        help="Fail unless every dry-run phase passes and the real candidate pool is untouched.",
    )
    args = parser.parse_args(argv)

    try:
        report = build_promotion_dry_run_report()
    except Exception as exc:  # noqa: BLE001 - CLI should report fixture setup failures.
        print(f"failed to run promotion dry-run fixture: {exc}", file=sys.stderr)
        return 1

    output = args.output or default_output_path(args.format)
    if args.check_output:
        ok, message = check_output(output, report, args.format)
        print(message)
        if not ok:
            print("run without --check-output to regenerate the dry-run fixture report", file=sys.stderr)
            return 1
    else:
        written = write_output(output, report, args.format)
        print(f"wrote {written}")

    if args.require_pass and not report.dry_run_passed:
        print("promotion dry-run fixture did not pass", file=sys.stderr)
        return 1

    print(f"dry_run_passed: {str(report.dry_run_passed).lower()}")
    print(f"temp_root_removed: {str(report.temp_root_removed).lower()}")
    print(f"real_candidate_pool_untouched: {str(report.real_candidate_pool_untouched).lower()}")
    print(f"phase_count: {len(report.phases)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
