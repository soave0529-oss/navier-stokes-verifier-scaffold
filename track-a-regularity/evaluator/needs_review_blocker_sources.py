from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from needs_review_blocker_matrix import (
    DEFAULT_CANDIDATE_DIR,
    DEFAULT_REPORT_DIR,
    ROOT,
    BlockerMatrixError,
    NeedsReviewBlockerMatrix,
    build_blocker_matrix,
    check_source_refs,
)


DEFAULT_MARKDOWN_OUTPUT = DEFAULT_REPORT_DIR / "needs_review_blocker_sources.md"
DEFAULT_JSON_OUTPUT = DEFAULT_REPORT_DIR / "needs_review_blocker_sources.json"
NON_CLAIMS = (
    "source_index_only",
    "no_new_active_candidate",
    "no_navier_stokes_solution",
    "no_epsilon_regularity_theorem",
    "no_weak_to_smooth_upgrade",
)


class SourceIndexError(ValueError):
    pass


@dataclass(frozen=True)
class FamilySourceIndex:
    blocker_family: str
    candidate_count: int
    source_count: int
    source_refs: tuple[str, ...]


@dataclass(frozen=True)
class SourceUsage:
    source_ref: str
    source_kind: str
    exists: bool
    blocker_families: tuple[str, ...]
    obligation_keys: tuple[str, ...]
    row_count: int


@dataclass(frozen=True)
class NeedsReviewBlockerSourceIndex:
    schema_version: int
    needs_review_count: int
    matrix_row_count: int
    source_count: int
    missing_source_count: int
    families: tuple[FamilySourceIndex, ...]
    sources: tuple[SourceUsage, ...]
    non_claims: tuple[str, ...]


def source_kind(source_ref: str) -> str:
    path = Path(source_ref)
    if source_ref.startswith("track-c-formal/lean/") or path.suffix == ".lean":
        return "lean_vocabulary"
    if source_ref.startswith("track-a-regularity/evaluator/checks/"):
        return "evaluator_check"
    if source_ref.startswith("docs/"):
        return "doc"
    if source_ref.startswith("logs/"):
        return "log"
    return "other"


def _append_unique(items: list[str], value: str) -> None:
    if value not in items:
        items.append(value)


def build_source_index(
    *,
    candidate_dir: Path = DEFAULT_CANDIDATE_DIR,
    report_dir: Path = DEFAULT_REPORT_DIR,
) -> NeedsReviewBlockerSourceIndex:
    matrix = build_blocker_matrix(candidate_dir=candidate_dir, report_dir=report_dir)
    ok, message = check_source_refs(matrix)
    if not ok:
        raise SourceIndexError(message)
    return build_source_index_from_matrix(matrix)


def build_source_index_from_matrix(
    matrix: NeedsReviewBlockerMatrix,
) -> NeedsReviewBlockerSourceIndex:
    family_indexes: list[FamilySourceIndex] = []
    usages: dict[str, dict[str, object]] = {}
    matrix_row_count = 0

    for family in matrix.families:
        family_sources: list[str] = []
        for detail in family.details:
            matrix_row_count += 1
            for source_ref in detail.source_refs:
                _append_unique(family_sources, source_ref)
                usage = usages.setdefault(
                    source_ref,
                    {
                        "blocker_families": [],
                        "obligation_keys": [],
                        "row_count": 0,
                    },
                )
                _append_unique(
                    usage["blocker_families"],  # type: ignore[arg-type]
                    family.blocker_family,
                )
                _append_unique(
                    usage["obligation_keys"],  # type: ignore[arg-type]
                    detail.obligation_key,
                )
                usage["row_count"] = int(usage["row_count"]) + 1

        family_indexes.append(
            FamilySourceIndex(
                blocker_family=family.blocker_family,
                candidate_count=family.candidate_count,
                source_count=len(family_sources),
                source_refs=tuple(family_sources),
            )
        )

    source_usages = tuple(
        SourceUsage(
            source_ref=source_ref,
            source_kind=source_kind(source_ref),
            exists=(ROOT / source_ref).exists(),
            blocker_families=tuple(data["blocker_families"]),  # type: ignore[arg-type]
            obligation_keys=tuple(data["obligation_keys"]),  # type: ignore[arg-type]
            row_count=int(data["row_count"]),
        )
        for source_ref, data in sorted(usages.items(), key=lambda item: item[0])
    )
    missing_source_count = sum(1 for source in source_usages if not source.exists)

    return NeedsReviewBlockerSourceIndex(
        schema_version=1,
        needs_review_count=matrix.needs_review_count,
        matrix_row_count=matrix_row_count,
        source_count=len(source_usages),
        missing_source_count=missing_source_count,
        families=tuple(family_indexes),
        sources=source_usages,
        non_claims=NON_CLAIMS,
    )


def source_index_to_dict(index: NeedsReviewBlockerSourceIndex) -> dict[str, object]:
    return {
        "schema_version": index.schema_version,
        "needs_review_count": index.needs_review_count,
        "matrix_row_count": index.matrix_row_count,
        "source_count": index.source_count,
        "missing_source_count": index.missing_source_count,
        "families": [asdict(family) for family in index.families],
        "sources": [asdict(source) for source in index.sources],
        "non_claims": list(index.non_claims),
        "docs": {
            "matrix_doc": "docs/STEP75_NEEDS_REVIEW_BLOCKER_MATRIX.md",
            "consistency_doc": "docs/STEP76_SCAFFOLD_MATRIX_CONSISTENCY.md",
            "provenance_doc": "docs/STEP77_BLOCKER_MATRIX_PROVENANCE.md",
        },
    }


def _format_refs(refs: tuple[str, ...]) -> str:
    return "<br>".join(f"`{ref}`" for ref in refs)


def render_markdown(index: NeedsReviewBlockerSourceIndex) -> str:
    family_rows = [
        "| blocker family | candidates | source count | source refs |",
        "|---|---:|---:|---|",
    ]
    for family in index.families:
        family_rows.append(
            "| "
            f"`{family.blocker_family}` | "
            f"{family.candidate_count} | "
            f"{family.source_count} | "
            f"{_format_refs(family.source_refs)} |"
        )

    source_rows = [
        "| source ref | kind | families | obligations | rows | exists |",
        "|---|---|---|---|---:|---|",
    ]
    for source in index.sources:
        source_rows.append(
            "| "
            f"`{source.source_ref}` | "
            f"`{source.source_kind}` | "
            f"{_format_refs(source.blocker_families)} | "
            f"{_format_refs(source.obligation_keys)} | "
            f"{source.row_count} | "
            f"`{str(source.exists).lower()}` |"
        )

    non_claim_rows = [f"- `{item}`" for item in index.non_claims]
    return "\n".join(
        (
            "# Needs-Review Blocker Source Index",
            "",
            "Generated by `track-a-regularity/evaluator/needs_review_blocker_sources.py`.",
            "",
            "This report groups the Step 77 blocker-matrix `source_refs` by blocker family",
            "and by source file. It is metadata only: it does not emit a candidate, discharge",
            "analytic blockers, prove epsilon regularity, or prove Navier-Stokes regularity.",
            "",
            "## Summary",
            "",
            f"- needs_review_count: `{index.needs_review_count}`",
            f"- matrix_row_count: `{index.matrix_row_count}`",
            f"- source_count: `{index.source_count}`",
            f"- missing_source_count: `{index.missing_source_count}`",
            "",
            "## Families",
            "",
            *family_rows,
            "",
            "## Sources",
            "",
            *source_rows,
            "",
            "## Non-Claims",
            "",
            *non_claim_rows,
            "",
        )
    )


def render_json(index: NeedsReviewBlockerSourceIndex) -> str:
    return json.dumps(source_index_to_dict(index), indent=2, sort_keys=True) + "\n"


def render_output(index: NeedsReviewBlockerSourceIndex, output_format: str) -> str:
    if output_format == "markdown":
        return render_markdown(index)
    if output_format == "json":
        return render_json(index)
    raise ValueError(f"unknown source index format: {output_format}")


def write_output(
    output: Path,
    index: NeedsReviewBlockerSourceIndex,
    output_format: str,
) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_output(index, output_format), encoding="utf-8")
    return output


def check_output(
    output: Path,
    index: NeedsReviewBlockerSourceIndex,
    output_format: str,
) -> tuple[bool, str]:
    expected = render_output(index, output_format)
    if not output.exists():
        return False, f"missing needs-review blocker source index: {output}"
    current = output.read_text(encoding="utf-8")
    if current != expected:
        return False, f"stale needs-review blocker source index: {output}"
    return True, f"fresh needs-review blocker source index: {output}"


def check_sources_exist(index: NeedsReviewBlockerSourceIndex) -> tuple[bool, str]:
    missing = [source.source_ref for source in index.sources if not source.exists]
    if missing:
        return False, "missing blocker source references: " + ", ".join(missing)
    return True, "all indexed blocker sources exist"


def default_output_path(output_format: str) -> Path:
    if output_format == "markdown":
        return DEFAULT_MARKDOWN_OUTPUT
    if output_format == "json":
        return DEFAULT_JSON_OUTPUT
    raise ValueError(f"unknown source index format: {output_format}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Render a source/provenance index for needs_review blocker rows."
    )
    parser.add_argument("--candidate-dir", type=Path, default=DEFAULT_CANDIDATE_DIR)
    parser.add_argument("--report-dir", type=Path, default=DEFAULT_REPORT_DIR)
    parser.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
        help="Source index output format.",
    )
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument(
        "--check-output",
        action="store_true",
        help="Check that --output already matches the rendered source index.",
    )
    parser.add_argument(
        "--require-sources-exist",
        action="store_true",
        help="Fail unless every indexed source path exists.",
    )
    parser.add_argument(
        "--require-count",
        type=int,
        default=7,
        help="Fail unless this many needs_review records are present. Use -1 to disable.",
    )
    args = parser.parse_args(argv)

    try:
        index = build_source_index(
            candidate_dir=args.candidate_dir,
            report_dir=args.report_dir,
        )
    except (BlockerMatrixError, SourceIndexError) as exc:
        print(str(exc), file=sys.stderr)
        return 1

    if args.require_count >= 0 and index.needs_review_count != args.require_count:
        print(
            f"needs_review_count mismatch: expected {args.require_count}, "
            f"found {index.needs_review_count}",
            file=sys.stderr,
        )
        return 1

    output = args.output or default_output_path(args.format)
    if args.check_output:
        ok, message = check_output(output, index, args.format)
        print(message)
        if not ok:
            print("run without --check-output to regenerate the source index", file=sys.stderr)
            return 1
    else:
        written = write_output(output, index, args.format)
        print(f"wrote {written}")

    if args.require_sources_exist:
        ok, message = check_sources_exist(index)
        print(message)
        if not ok:
            return 1

    print(f"source_count: {index.source_count}")
    print(f"needs_review_count: {index.needs_review_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
