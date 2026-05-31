from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

from proof_obligation_blockers import load_blocker_summary, write_summary


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REPORT_DIR = ROOT / "track-a-regularity/reports"
VALID_CANDIDATE_ID = re.compile(r"^lemma_[A-Za-z0-9_]+$")


@dataclass(frozen=True)
class TemplateObligation:
    key: str
    label: str
    blocker: str


TEMPLATE_OBLIGATIONS: tuple[TemplateObligation, ...] = (
    TemplateObligation(
        key="exact_quantity_definitions",
        label="Exact quantity definitions",
        blocker="Candidate has not supplied exact quantities, domains, indices, and conventions.",
    ),
    TemplateObligation(
        key="exact_function_spaces",
        label="Exact function spaces",
        blocker="Candidate has not supplied all function-space indices, time intervals, and endpoints.",
    ),
    TemplateObligation(
        key="known_result_separation",
        label="Known-result separation",
        blocker="Candidate has not separated the statement from the nearest known theorem families.",
    ),
    TemplateObligation(
        key="proof_route",
        label="Proof route",
        blocker="Candidate has not supplied a precise route from hypothesis to a continuation criterion.",
    ),
    TemplateObligation(
        key="solution_class_bridge",
        label="Solution-class bridge",
        blocker="Candidate has not named the source and target solution classes and bridge theorem.",
    ),
    TemplateObligation(
        key="analytic_promotion_blockers",
        label="Analytic promotion blockers",
        blocker="Candidate has not discharged all family-specific analytic promotion blockers.",
    ),
)


def validate_candidate_id(candidate_id: str) -> str:
    if not VALID_CANDIDATE_ID.match(candidate_id):
        raise ValueError("candidate id must match lemma_[A-Za-z0-9_]+")
    return candidate_id


def default_report_path(candidate_id: str) -> Path:
    validate_candidate_id(candidate_id)
    return DEFAULT_REPORT_DIR / f"{candidate_id}_proof_obligations.json"


def default_summary_path(candidate_id: str) -> Path:
    validate_candidate_id(candidate_id)
    return DEFAULT_REPORT_DIR / f"{candidate_id}_proof_obligation_summary.json"


def build_candidate_obligation_report(
    candidate_id: str,
    *,
    candidate_status: str = "needs_review",
    active_candidate: bool = False,
    discharged_keys: set[str] | None = None,
) -> dict[str, object]:
    validate_candidate_id(candidate_id)
    if candidate_status not in {"needs_review", "candidate"}:
        raise ValueError("candidate_status must be needs_review or candidate")

    discharged = discharged_keys or set()
    known = {obligation.key for obligation in TEMPLATE_OBLIGATIONS}
    unknown = sorted(discharged - known)
    if unknown:
        raise ValueError("unknown discharged obligation keys: " + ", ".join(unknown))

    nodes: list[dict[str, object]] = []
    promotion_blockers: list[dict[str, str]] = []
    for obligation in TEMPLATE_OBLIGATIONS:
        proved = obligation.key in discharged
        status = "discharged" if proved else "template_required"
        node = {
            "key": obligation.key,
            "label": obligation.label,
            "status": status,
            "supplied_as_assumption": False,
            "proved_in_current_artifact": proved,
            "blocker": "" if proved else obligation.blocker,
        }
        nodes.append(node)
        if not proved:
            promotion_blockers.append(
                {
                    "key": obligation.key,
                    "status": status,
                    "blocker": obligation.blocker,
                }
            )

    return {
        "schema_version": 1,
        "lemma_id": candidate_id,
        "candidate_status": candidate_status,
        "active_candidate": active_candidate,
        "docs": {
            "template_doc": "docs/STEP72_CANDIDATE_OBLIGATION_TEMPLATE.md",
            "generation_spec": "docs/CANDIDATE_GENERATION_SPEC_V4.md",
            "freeze_doc": "docs/CANDIDATE_GENERATION_FREEZE.md",
        },
        "nodes": nodes,
        "promotion_blockers": promotion_blockers,
        "non_claims": [
            "template_only",
            "no_navier_stokes_solution",
            "no_epsilon_regularity_theorem",
            "no_pressure_estimate",
            "no_compactness_or_liouville_theorem",
            "no_weak_to_smooth_upgrade",
        ],
    }


def write_report_and_summary(
    report_output: Path,
    summary_output: Path,
    report: dict[str, object],
) -> tuple[Path, Path]:
    report_output.parent.mkdir(parents=True, exist_ok=True)
    report_output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    summary = load_blocker_summary(report_output)
    write_summary(summary_output, summary, "json")
    return report_output, summary_output


def parse_discharged(values: list[str]) -> set[str]:
    discharged: set[str] = set()
    for value in values:
        for item in value.split(","):
            item = item.strip()
            if item:
                discharged.add(item)
    return discharged


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Create a candidate-specific proof-obligation report and JSON summary template."
    )
    parser.add_argument("--candidate-id", required=True, help="Candidate id, e.g. lemma_0253.")
    parser.add_argument(
        "--candidate-status",
        choices=("needs_review", "candidate"),
        default="needs_review",
        help="Report candidate status. Defaults to needs_review.",
    )
    parser.add_argument(
        "--active-candidate",
        action="store_true",
        help="Mark the report as active_candidate=true.",
    )
    parser.add_argument(
        "--discharge",
        action="append",
        default=[],
        help="Comma-separated obligation keys to mark discharged. Repeatable.",
    )
    parser.add_argument(
        "--allow-zero-blocker",
        action="store_true",
        help="Required before emitting candidate/active/zero-blocker metadata.",
    )
    parser.add_argument("--report-output", type=Path, default=None, help="Report JSON path.")
    parser.add_argument("--summary-output", type=Path, default=None, help="Summary JSON path.")
    args = parser.parse_args(argv)

    try:
        candidate_id = validate_candidate_id(args.candidate_id)
        discharged = parse_discharged(args.discharge)
        report = build_candidate_obligation_report(
            candidate_id,
            candidate_status=args.candidate_status,
            active_candidate=args.active_candidate,
            discharged_keys=discharged,
        )
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    blocker_count = len(report["promotion_blockers"])  # type: ignore[arg-type]
    zero_blocker_active = (
        args.candidate_status == "candidate"
        and args.active_candidate
        and blocker_count == 0
    )
    if zero_blocker_active and not args.allow_zero_blocker:
        print(
            "--allow-zero-blocker is required for candidate/active reports with zero blockers",
            file=sys.stderr,
        )
        return 1
    if args.candidate_status == "candidate" and blocker_count > 0:
        print(
            "candidate-status reports must discharge all template obligations before emission",
            file=sys.stderr,
        )
        return 1

    report_output = args.report_output or default_report_path(candidate_id)
    summary_output = args.summary_output or default_summary_path(candidate_id)
    report_path, summary_path = write_report_and_summary(report_output, summary_output, report)
    print(f"wrote report {report_path}")
    print(f"wrote summary {summary_path}")
    print(f"promotion_blocker_count: {blocker_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
