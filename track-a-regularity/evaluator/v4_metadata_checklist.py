from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from candidate_obligation_template import TEMPLATE_OBLIGATIONS
from generation_spec_v4 import (
    BLOCKER_SOURCE_INDEX_JSON_KEY,
    BLOCKER_SOURCE_INDEX_MARKDOWN_KEY,
    PROOF_OBLIGATION_REPORT_KEY,
    PROOF_OBLIGATION_SUMMARY_KEY,
    REQUIRED_MARKERS,
    assess_candidate,
)
from schema import load_candidate


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REPORT_DIR = ROOT / "track-a-regularity/reports"
DEFAULT_TEMPLATE_PATH = ROOT / "track-a-regularity/templates/v4_blocked_candidate_template.yaml"
DEFAULT_MARKDOWN_OUTPUT = DEFAULT_REPORT_DIR / "v4_candidate_metadata_checklist.md"
DEFAULT_JSON_OUTPUT = DEFAULT_REPORT_DIR / "v4_candidate_metadata_checklist.json"
NON_CLAIMS = (
    "metadata_checklist_only",
    "blocked_template_only",
    "no_new_active_candidate",
    "no_navier_stokes_solution",
    "no_epsilon_regularity_theorem",
    "no_weak_to_smooth_upgrade",
)


@dataclass(frozen=True)
class MetadataChecklistItem:
    category: str
    key: str
    required_value: str
    purpose: str


@dataclass(frozen=True)
class TemplateSafety:
    template_path: str
    exists: bool
    loadable: bool
    candidate_id: str
    expected_status: str
    status: str
    has_required_markers: bool
    has_expected_evaluator_keys: bool
    emit_ready: bool
    issues: tuple[str, ...]


@dataclass(frozen=True)
class V4MetadataChecklist:
    schema_version: int
    marker_count: int
    expected_evaluator_key_count: int
    template_obligation_count: int
    checklist_items: tuple[MetadataChecklistItem, ...]
    template_safety: TemplateSafety
    non_claims: tuple[str, ...]


def _relative(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def expected_evaluator_keys() -> tuple[str, ...]:
    return (
        "status",
        PROOF_OBLIGATION_REPORT_KEY,
        PROOF_OBLIGATION_SUMMARY_KEY,
        BLOCKER_SOURCE_INDEX_MARKDOWN_KEY,
        BLOCKER_SOURCE_INDEX_JSON_KEY,
    )


def build_checklist_items() -> tuple[MetadataChecklistItem, ...]:
    items: list[MetadataChecklistItem] = []
    for marker in REQUIRED_MARKERS:
        items.append(
            MetadataChecklistItem(
                category="related_known marker",
                key=marker,
                required_value="present",
                purpose="Audit marker required before expected evaluator candidate emission.",
            )
        )

    items.extend(
        [
            MetadataChecklistItem(
                category="expected_evaluator",
                key="status",
                required_value="candidate",
                purpose="Activates the v4 emit-ready preflight path.",
            ),
            MetadataChecklistItem(
                category="expected_evaluator",
                key=PROOF_OBLIGATION_REPORT_KEY,
                required_value="fresh candidate-specific proof-obligation report JSON",
                purpose="Provides the full proof-obligation node list for the proposed candidate.",
            ),
            MetadataChecklistItem(
                category="expected_evaluator",
                key=PROOF_OBLIGATION_SUMMARY_KEY,
                required_value="fresh candidate-specific proof-obligation summary JSON",
                purpose="Provides the zero-blocker summary checked by v4 preflight.",
            ),
            MetadataChecklistItem(
                category="expected_evaluator",
                key=BLOCKER_SOURCE_INDEX_MARKDOWN_KEY,
                required_value="fresh blocker source-index Markdown",
                purpose="Connects the candidate to the current blocker provenance dashboard.",
            ),
            MetadataChecklistItem(
                category="expected_evaluator",
                key=BLOCKER_SOURCE_INDEX_JSON_KEY,
                required_value="fresh blocker source-index JSON",
                purpose="Provides machine-readable blocker provenance checked by v4 preflight.",
            ),
            MetadataChecklistItem(
                category="proof-obligation summary",
                key="candidate_status",
                required_value="candidate",
                purpose="Prevents review-only proof-obligation reports from being treated as active.",
            ),
            MetadataChecklistItem(
                category="proof-obligation summary",
                key="active_candidate",
                required_value="true",
                purpose="Requires explicit active-candidate status in the report sidecar.",
            ),
            MetadataChecklistItem(
                category="proof-obligation summary",
                key="promotion_blocker_count",
                required_value="0",
                purpose="Blocks candidate emission while any promotion blocker remains.",
            ),
            MetadataChecklistItem(
                category="proof-obligation summary",
                key="active_candidate_blocker_conflict",
                required_value="false",
                purpose="Guards against active-candidate metadata with unresolved blockers.",
            ),
            MetadataChecklistItem(
                category="source-index",
                key="missing_source_count",
                required_value="0",
                purpose="Ensures every blocker provenance path referenced by the source index exists.",
            ),
        ]
    )
    return tuple(items)


def check_template_safety(template_path: Path = DEFAULT_TEMPLATE_PATH) -> TemplateSafety:
    relative_path = _relative(template_path)
    issues: list[str] = []
    if not template_path.exists():
        return TemplateSafety(
            template_path=relative_path,
            exists=False,
            loadable=False,
            candidate_id="",
            expected_status="",
            status="",
            has_required_markers=False,
            has_expected_evaluator_keys=False,
            emit_ready=False,
            issues=("template file is missing",),
        )

    try:
        candidate = load_candidate(template_path)
    except Exception as exc:  # noqa: BLE001 - CLI should report parse failures.
        return TemplateSafety(
            template_path=relative_path,
            exists=True,
            loadable=False,
            candidate_id="",
            expected_status="",
            status="",
            has_required_markers=False,
            has_expected_evaluator_keys=False,
            emit_ready=False,
            issues=(f"template is not loadable: {exc}",),
        )

    marker_set = set(candidate.related_known)
    missing_markers = [marker for marker in REQUIRED_MARKERS if marker not in marker_set]
    expected_keys = expected_evaluator_keys()
    missing_keys = [key for key in expected_keys if key not in candidate.expected_evaluator]
    expected_status = str(candidate.expected_evaluator.get("status", ""))
    assessment = assess_candidate(candidate)

    if expected_status == "candidate":
        issues.append("blocked template must not set expected_evaluator.status to candidate")
    if candidate.status == "candidate":
        issues.append("blocked template must not set status to candidate")
    if missing_markers:
        issues.append("missing template markers: " + ", ".join(missing_markers))
    if missing_keys:
        issues.append("missing template expected_evaluator keys: " + ", ".join(missing_keys))
    if assessment.emit_ready:
        issues.append("blocked template unexpectedly passes v4 emit-ready assessment")

    return TemplateSafety(
        template_path=relative_path,
        exists=True,
        loadable=True,
        candidate_id=candidate.id,
        expected_status=expected_status,
        status=candidate.status,
        has_required_markers=not missing_markers,
        has_expected_evaluator_keys=not missing_keys,
        emit_ready=assessment.emit_ready,
        issues=tuple(issues),
    )


def build_checklist(template_path: Path = DEFAULT_TEMPLATE_PATH) -> V4MetadataChecklist:
    return V4MetadataChecklist(
        schema_version=1,
        marker_count=len(REQUIRED_MARKERS),
        expected_evaluator_key_count=len(expected_evaluator_keys()),
        template_obligation_count=len(TEMPLATE_OBLIGATIONS),
        checklist_items=build_checklist_items(),
        template_safety=check_template_safety(template_path),
        non_claims=NON_CLAIMS,
    )


def checklist_to_dict(checklist: V4MetadataChecklist) -> dict[str, object]:
    return {
        "schema_version": checklist.schema_version,
        "marker_count": checklist.marker_count,
        "expected_evaluator_key_count": checklist.expected_evaluator_key_count,
        "template_obligation_count": checklist.template_obligation_count,
        "checklist_items": [asdict(item) for item in checklist.checklist_items],
        "template_safety": asdict(checklist.template_safety),
        "non_claims": list(checklist.non_claims),
        "docs": {
            "generation_spec": "docs/CANDIDATE_GENERATION_SPEC_V4.md",
            "freeze_doc": "docs/CANDIDATE_GENERATION_FREEZE.md",
            "source_index_doc": "docs/STEP78_BLOCKER_SOURCE_INDEX.md",
            "source_index_gate_doc": "docs/STEP79_V4_SOURCE_INDEX_GATE.md",
        },
    }


def render_markdown(checklist: V4MetadataChecklist) -> str:
    item_rows = [
        "| category | key | required value | purpose |",
        "|---|---|---|---|",
    ]
    for item in checklist.checklist_items:
        item_rows.append(
            "| "
            f"`{item.category}` | "
            f"`{item.key}` | "
            f"`{item.required_value}` | "
            f"{item.purpose} |"
        )

    template = checklist.template_safety
    issue_rows = [f"- `{issue}`" for issue in template.issues] or ["- `none`"]
    non_claim_rows = [f"- `{item}`" for item in checklist.non_claims]
    obligation_rows = [
        f"- `{obligation.key}`: {obligation.label}" for obligation in TEMPLATE_OBLIGATIONS
    ]
    marker_rows = [f"- `{marker}`" for marker in REQUIRED_MARKERS]

    return "\n".join(
        (
            "# V4 Candidate Metadata Checklist",
            "",
            "Generated by `track-a-regularity/evaluator/v4_metadata_checklist.py`.",
            "",
            "This report documents the metadata required before a future Track A YAML can",
            "declare `expected_evaluator.status: candidate`. It is a gate checklist and a",
            "blocked-template audit, not mathematical evidence.",
            "",
            "## Summary",
            "",
            f"- marker_count: `{checklist.marker_count}`",
            f"- expected_evaluator_key_count: `{checklist.expected_evaluator_key_count}`",
            f"- template_obligation_count: `{checklist.template_obligation_count}`",
            f"- template_path: `{template.template_path}`",
            f"- template_expected_status: `{template.expected_status}`",
            f"- template_emit_ready: `{str(template.emit_ready).lower()}`",
            "",
            "## Required V4 Markers",
            "",
            *marker_rows,
            "",
            "## Template Obligations",
            "",
            *obligation_rows,
            "",
            "## Checklist Items",
            "",
            *item_rows,
            "",
            "## Blocked Template Safety",
            "",
            f"- exists: `{str(template.exists).lower()}`",
            f"- loadable: `{str(template.loadable).lower()}`",
            f"- candidate_id: `{template.candidate_id}`",
            f"- candidate_status_field: `{template.status}`",
            f"- has_required_markers: `{str(template.has_required_markers).lower()}`",
            f"- has_expected_evaluator_keys: `{str(template.has_expected_evaluator_keys).lower()}`",
            f"- emit_ready: `{str(template.emit_ready).lower()}`",
            "",
            "Issues:",
            "",
            *issue_rows,
            "",
            "## Non-Claims",
            "",
            *non_claim_rows,
            "",
        )
    )


def render_json(checklist: V4MetadataChecklist) -> str:
    return json.dumps(checklist_to_dict(checklist), indent=2, sort_keys=True) + "\n"


def render_output(checklist: V4MetadataChecklist, output_format: str) -> str:
    if output_format == "markdown":
        return render_markdown(checklist)
    if output_format == "json":
        return render_json(checklist)
    raise ValueError(f"unknown checklist format: {output_format}")


def write_output(
    output: Path,
    checklist: V4MetadataChecklist,
    output_format: str,
) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_output(checklist, output_format), encoding="utf-8")
    return output


def check_output(
    output: Path,
    checklist: V4MetadataChecklist,
    output_format: str,
) -> tuple[bool, str]:
    expected = render_output(checklist, output_format)
    if not output.exists():
        return False, f"missing v4 metadata checklist: {output}"
    current = output.read_text(encoding="utf-8")
    if current != expected:
        return False, f"stale v4 metadata checklist: {output}"
    return True, f"fresh v4 metadata checklist: {output}"


def default_output_path(output_format: str) -> Path:
    if output_format == "markdown":
        return DEFAULT_MARKDOWN_OUTPUT
    if output_format == "json":
        return DEFAULT_JSON_OUTPUT
    raise ValueError(f"unknown checklist format: {output_format}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Render the v4 candidate metadata checklist and blocked-template audit."
    )
    parser.add_argument("--template", type=Path, default=DEFAULT_TEMPLATE_PATH)
    parser.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
        help="Checklist output format.",
    )
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument(
        "--check-output",
        action="store_true",
        help="Check that --output already matches the rendered checklist.",
    )
    parser.add_argument(
        "--require-template-safe",
        action="store_true",
        help="Fail if the blocked template is missing, malformed, or emit-ready.",
    )
    args = parser.parse_args(argv)

    checklist = build_checklist(args.template)
    output = args.output or default_output_path(args.format)
    if args.check_output:
        ok, message = check_output(output, checklist, args.format)
        print(message)
        if not ok:
            print("run without --check-output to regenerate the checklist", file=sys.stderr)
            return 1
    else:
        written = write_output(output, checklist, args.format)
        print(f"wrote {written}")

    if args.require_template_safe:
        if checklist.template_safety.issues:
            print(
                "blocked template safety issues: "
                + ", ".join(checklist.template_safety.issues),
                file=sys.stderr,
            )
            return 1
        print("blocked template safety check passed")

    print(f"marker_count: {checklist.marker_count}")
    print(f"expected_evaluator_key_count: {checklist.expected_evaluator_key_count}")
    print(f"template_obligation_count: {checklist.template_obligation_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
