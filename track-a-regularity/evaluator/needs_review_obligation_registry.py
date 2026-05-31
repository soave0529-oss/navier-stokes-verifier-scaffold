from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from proof_obligation_blockers import (
    BlockerReportError,
    check_summary_output,
    load_blocker_summary,
)
from schema import LemmaCandidate, load_candidates


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CANDIDATE_DIR = ROOT / "track-a-regularity/candidates"
DEFAULT_REPORT_DIR = ROOT / "track-a-regularity/reports"
DEFAULT_MARKDOWN_OUTPUT = DEFAULT_REPORT_DIR / "needs_review_obligation_registry.md"
DEFAULT_JSON_OUTPUT = DEFAULT_REPORT_DIR / "needs_review_obligation_registry.json"

DUHAMEL_IDS = frozenset({"lemma_0209", "lemma_0219", "lemma_0229", "lemma_0239", "lemma_0249"})
STEP72_DOC = "docs/STEP72_CANDIDATE_OBLIGATION_TEMPLATE.md"
V4_SPEC_DOC = "docs/CANDIDATE_GENERATION_SPEC_V4.md"
FREEZE_DOC = "docs/CANDIDATE_GENERATION_FREEZE.md"
LEMMA_0252_GRAPH_JSON = DEFAULT_REPORT_DIR / "lemma_0252_proof_obligation_graph.json"


@dataclass(frozen=True)
class NeedsReviewEntry:
    candidate_id: str
    blocker_family: str
    expected_reason: str
    scaffold_report: str
    scaffold_summary: str
    scaffold_status: str
    promotion_blocker_count: int | None
    special_report: str
    next_action: str


@dataclass(frozen=True)
class NeedsReviewRegistry:
    schema_version: int
    needs_review_count: int
    blocker_family_counts: dict[str, int]
    entries: tuple[NeedsReviewEntry, ...]
    non_claims: tuple[str, ...]


def repo_relative(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def scaffold_report_path(candidate_id: str, report_dir: Path) -> Path:
    return report_dir / f"{candidate_id}_proof_obligations.json"


def scaffold_summary_path(candidate_id: str, report_dir: Path) -> Path:
    return report_dir / f"{candidate_id}_proof_obligation_summary.json"


def classify_blocker_family(candidate: LemmaCandidate) -> str:
    text = candidate.normalized_text
    if candidate.id in DUHAMEL_IDS or "duhamel" in text:
        return "critical_duhamel_bilinear_formal_only"
    if candidate.id == "lemma_0251" or "dyadic flux" in text or "pi_n^les" in text:
        return "dyadic_flux_exact"
    if candidate.id == "lemma_0252" or "parabolic morrey" in text:
        return "parabolic_morrey_enstrophy_exact"
    return "unknown_needs_review"


def next_action_for_family(blocker_family: str) -> str:
    if blocker_family == "critical_duhamel_bilinear_formal_only":
        return "Specify exact function spaces, Leray projection, and time integral before scaffold discharge."
    if blocker_family == "dyadic_flux_exact":
        return "Rewrite sign-corrected forward flux and coercive bridge before scaffold discharge."
    if blocker_family == "parabolic_morrey_enstrophy_exact":
        return "Supply finite-bound-to-smallness or compactness/Liouville/epsilon-pressure branch before scaffold discharge."
    return "Classify the needs_review family before scaffold discharge."


def inspect_scaffold(
    candidate_id: str,
    report_dir: Path,
) -> tuple[str, int | None]:
    report = scaffold_report_path(candidate_id, report_dir)
    summary = scaffold_summary_path(candidate_id, report_dir)
    report_exists = report.exists()
    summary_exists = summary.exists()

    if not report_exists and not summary_exists:
        return "missing", None
    if report_exists and not summary_exists:
        return "report_only", None
    if summary_exists and not report_exists:
        return "summary_only", None

    try:
        blocker_summary = load_blocker_summary(report)
    except BlockerReportError:
        return "invalid_report", None

    fresh, _ = check_summary_output(summary, blocker_summary, "json")
    if not fresh:
        return "stale_summary", blocker_summary.promotion_blocker_count

    if (
        blocker_summary.candidate_status == "candidate"
        and blocker_summary.active_candidate
        and blocker_summary.promotion_blocker_count == 0
    ):
        return "present_zero_blocker", 0
    return "present_blocked", blocker_summary.promotion_blocker_count


def special_report_for(candidate_id: str) -> str:
    if candidate_id == "lemma_0252" and LEMMA_0252_GRAPH_JSON.exists():
        return repo_relative(LEMMA_0252_GRAPH_JSON)
    return ""


def needs_review_candidates(candidate_dir: Path) -> list[LemmaCandidate]:
    candidates = load_candidates(list(candidate_dir.glob("*.yaml")))
    return [
        candidate
        for candidate in candidates
        if str(candidate.expected_evaluator.get("status", "")) == "needs_review"
    ]


def build_registry(
    *,
    candidate_dir: Path = DEFAULT_CANDIDATE_DIR,
    report_dir: Path = DEFAULT_REPORT_DIR,
) -> NeedsReviewRegistry:
    entries: list[NeedsReviewEntry] = []
    family_counts: dict[str, int] = {}

    for candidate in needs_review_candidates(candidate_dir):
        blocker_family = classify_blocker_family(candidate)
        family_counts[blocker_family] = family_counts.get(blocker_family, 0) + 1
        scaffold_status, blocker_count = inspect_scaffold(candidate.id, report_dir)
        report = scaffold_report_path(candidate.id, report_dir)
        summary = scaffold_summary_path(candidate.id, report_dir)
        entries.append(
            NeedsReviewEntry(
                candidate_id=candidate.id,
                blocker_family=blocker_family,
                expected_reason=str(candidate.expected_evaluator.get("reason", "")),
                scaffold_report=repo_relative(report),
                scaffold_summary=repo_relative(summary),
                scaffold_status=scaffold_status,
                promotion_blocker_count=blocker_count,
                special_report=special_report_for(candidate.id),
                next_action=next_action_for_family(blocker_family),
            )
        )

    return NeedsReviewRegistry(
        schema_version=1,
        needs_review_count=len(entries),
        blocker_family_counts=dict(sorted(family_counts.items())),
        entries=tuple(sorted(entries, key=lambda entry: entry.candidate_id)),
        non_claims=(
            "registry_only",
            "no_new_active_candidate",
            "no_navier_stokes_solution",
            "no_epsilon_regularity_theorem",
            "no_weak_to_smooth_upgrade",
        ),
    )


def registry_to_dict(registry: NeedsReviewRegistry) -> dict[str, object]:
    return {
        "schema_version": registry.schema_version,
        "needs_review_count": registry.needs_review_count,
        "blocker_family_counts": registry.blocker_family_counts,
        "entries": [asdict(entry) for entry in registry.entries],
        "non_claims": list(registry.non_claims),
        "docs": {
            "template_doc": STEP72_DOC,
            "generation_spec": V4_SPEC_DOC,
            "freeze_doc": FREEZE_DOC,
        },
    }


def render_markdown(registry: NeedsReviewRegistry) -> str:
    count_rows = [
        "| blocker family | count |",
        "|---|---:|",
        *(
            f"| `{family}` | {count} |"
            for family, count in registry.blocker_family_counts.items()
        ),
    ]
    if not registry.blocker_family_counts:
        count_rows.append("| none | 0 |")

    entry_rows = [
        "| candidate | blocker family | scaffold status | blockers | special report | next action |",
        "|---|---|---|---:|---|---|",
    ]
    for entry in registry.entries:
        blockers = (
            "n/a"
            if entry.promotion_blocker_count is None
            else str(entry.promotion_blocker_count)
        )
        special = f"`{entry.special_report}`" if entry.special_report else ""
        entry_rows.append(
            "| "
            f"`{entry.candidate_id}` | "
            f"`{entry.blocker_family}` | "
            f"`{entry.scaffold_status}` | "
            f"{blockers} | "
            f"{special} | "
            f"{entry.next_action} |"
        )

    non_claim_rows = [f"- `{item}`" for item in registry.non_claims]
    return "\n".join(
        (
            "# Needs-Review Proof-Obligation Registry",
            "",
            "Generated by `track-a-regularity/evaluator/needs_review_obligation_registry.py`.",
            "",
            "This report only inventories existing `needs_review` records. It does not emit a",
            "candidate, discharge analytic blockers, prove epsilon regularity, or prove",
            "Navier-Stokes regularity.",
            "",
            "## Summary",
            "",
            f"- needs_review_count: `{registry.needs_review_count}`",
            "",
            *count_rows,
            "",
            "## Entries",
            "",
            *entry_rows,
            "",
            "## Non-Claims",
            "",
            *non_claim_rows,
            "",
        )
    )


def render_json(registry: NeedsReviewRegistry) -> str:
    return json.dumps(registry_to_dict(registry), indent=2, sort_keys=True) + "\n"


def render_output(registry: NeedsReviewRegistry, output_format: str) -> str:
    if output_format == "markdown":
        return render_markdown(registry)
    if output_format == "json":
        return render_json(registry)
    raise ValueError(f"unknown registry format: {output_format}")


def write_output(output: Path, registry: NeedsReviewRegistry, output_format: str) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_output(registry, output_format), encoding="utf-8")
    return output


def check_output(
    output: Path,
    registry: NeedsReviewRegistry,
    output_format: str,
) -> tuple[bool, str]:
    expected = render_output(registry, output_format)
    if not output.exists():
        return False, f"missing needs-review registry: {output}"
    current = output.read_text(encoding="utf-8")
    if current != expected:
        return False, f"stale needs-review registry: {output}"
    return True, f"fresh needs-review registry: {output}"


def check_required_scaffold_status(
    registry: NeedsReviewRegistry,
    required_status: str,
) -> tuple[bool, str]:
    mismatches = [
        f"{entry.candidate_id}:{entry.scaffold_status}"
        for entry in registry.entries
        if entry.scaffold_status != required_status
    ]
    if mismatches:
        return (
            False,
            "needs-review scaffold status mismatch: expected "
            f"{required_status}; " + ", ".join(mismatches),
        )
    return True, f"all needs-review scaffolds are {required_status}"


def default_output_path(output_format: str) -> Path:
    if output_format == "markdown":
        return DEFAULT_MARKDOWN_OUTPUT
    if output_format == "json":
        return DEFAULT_JSON_OUTPUT
    raise ValueError(f"unknown registry format: {output_format}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Inventory existing needs_review records and proof-obligation scaffold status."
    )
    parser.add_argument("--candidate-dir", type=Path, default=DEFAULT_CANDIDATE_DIR)
    parser.add_argument("--report-dir", type=Path, default=DEFAULT_REPORT_DIR)
    parser.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
        help="Registry output format.",
    )
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument(
        "--check-output",
        action="store_true",
        help="Check that --output already matches the rendered registry.",
    )
    parser.add_argument(
        "--require-scaffold-status",
        default=None,
        help="Fail unless every needs_review record has this scaffold status.",
    )
    parser.add_argument(
        "--require-count",
        type=int,
        default=7,
        help="Fail unless this many needs_review records are present. Use -1 to disable.",
    )
    args = parser.parse_args(argv)

    registry = build_registry(candidate_dir=args.candidate_dir, report_dir=args.report_dir)
    if args.require_count >= 0 and registry.needs_review_count != args.require_count:
        print(
            f"needs_review_count mismatch: expected {args.require_count}, "
            f"found {registry.needs_review_count}",
            file=sys.stderr,
        )
        return 1

    output = args.output or default_output_path(args.format)
    if args.check_output:
        ok, message = check_output(output, registry, args.format)
        print(message)
        if not ok:
            print("run without --check-output to regenerate the registry", file=sys.stderr)
            return 1
    else:
        written = write_output(output, registry, args.format)
        print(f"wrote {written}")
    if args.require_scaffold_status is not None:
        ok, message = check_required_scaffold_status(registry, args.require_scaffold_status)
        print(message)
        if not ok:
            return 1
    print(f"needs_review_count: {registry.needs_review_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
