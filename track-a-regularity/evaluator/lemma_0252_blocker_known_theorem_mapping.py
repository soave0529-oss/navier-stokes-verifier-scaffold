from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path

from proof_obligation_blockers import DEFAULT_INPUT, load_blocker_summary


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REPORT_DIR = ROOT / "track-a-regularity/reports"
DEFAULT_MARKDOWN_OUTPUT = DEFAULT_REPORT_DIR / "lemma_0252_blocker_known_theorem_mapping.md"
DEFAULT_JSON_OUTPUT = DEFAULT_REPORT_DIR / "lemma_0252_blocker_known_theorem_mapping.json"

EXPECTED_BLOCKERS = (
    "finite_bound_to_smallness",
    "compactness_liouville",
    "smooth_continuation_bridge",
)
VERDICTS = (
    "resolvable_known",
    "resolvable_needs_new_result",
    "permanently_blocked",
)
LOCAL_SOURCE_REFS = (
    "docs/LEMMA_0252_PROOF_OBLIGATIONS.md",
    "docs/KNOWN_LOCAL_ENSTROPHY_CRITERIA.md",
    "docs/LEMMA_0252_LOCAL_ENERGY_FORMAL_MAP.md",
    "docs/FINAL_CANDIDATE_TRIAGE.md",
    "docs/paper_notes/1402.0290.md",
    "docs/paper_notes/1709.10033.md",
    "docs/paper_notes/1901.09023.md",
    "track-a-regularity/reports/lemma_0252_proof_obligation_graph.json",
    "track-a-regularity/reports/lemma_0252_finite_bound_smallness_source_read_packet.md",
    "track-a-regularity/reports/lemma_0252_finite_bound_smallness_source_read_packet.json",
    "track-a-regularity/reports/lemma_0252_compactness_liouville_source_read_packet.md",
    "track-a-regularity/reports/lemma_0252_compactness_liouville_source_read_packet.json",
    "track-c-formal/lean/NavierStokesProgram/ProofObligationGraph.lean",
    "track-c-formal/lean/NavierStokesProgram/SolutionClasses.lean",
    "papers/blockers/finite_bound_to_smallness/vasseur2007_partial_regularity_NS_UT.pdf",
    "papers/blockers/compactness_liouville/0709.3599_KNSS2009_liouville_acta_math.pdf",
    "papers/blockers/compactness_liouville/1509.04940_backward_uniqueness_remarks.pdf",
)
NON_CLAIMS = (
    "read_only_known_theorem_mapping",
    "no_candidate_promotion",
    "no_blocker_discharge",
    "no_epsilon_regularity_theorem",
    "no_compactness_or_liouville_theorem",
    "no_weak_to_smooth_upgrade",
    "no_navier_stokes_solution",
)


@dataclass(frozen=True)
class TheoremMappingRow:
    blocker_id: str
    candidate_theorem: str
    citation: str
    applies_directly: bool
    gap_if_partial: str
    verdict: str


@dataclass(frozen=True)
class Lemma0252KnownTheoremMapping:
    schema_version: int
    lemma_id: str
    candidate_status: str
    active_candidate: bool
    promotion_blocker_count: int
    blocker_count: int
    row_count: int
    rows_per_blocker: dict[str, int]
    resolvable_known_count: int
    resolvable_needs_new_result_count: int
    permanently_blocked_count: int
    rows: tuple[TheoremMappingRow, ...]
    source_refs: tuple[str, ...]
    non_claims: tuple[str, ...]


def _row(
    *,
    blocker_id: str,
    candidate_theorem: str,
    citation: str,
    applies_directly: bool,
    gap_if_partial: str,
    verdict: str,
) -> TheoremMappingRow:
    return TheoremMappingRow(
        blocker_id=blocker_id,
        candidate_theorem=candidate_theorem,
        citation=citation,
        applies_directly=applies_directly,
        gap_if_partial=gap_if_partial,
        verdict=verdict,
    )


def _canonical_rows() -> tuple[TheoremMappingRow, ...]:
    return (
        _row(
            blocker_id="finite_bound_to_smallness",
            candidate_theorem="CKN 1982 epsilon-regularity criterion",
            citation=(
                "Caffarelli-Kohn-Nirenberg 1982; "
                "docs/KNOWN_LOCAL_ENSTROPHY_CRITERIA.md; "
                "docs/LEMMA_0252_PROOF_OBLIGATIONS.md"
            ),
            applies_directly=False,
            gap_if_partial=(
                "CKN requires epsilon smallness of a local velocity, pressure, and "
                "dissipation package on a suitable weak solution cylinder. lemma_0252 "
                "only assumes a finite critical local vorticity-enstrophy envelope."
            ),
            verdict="resolvable_needs_new_result",
        ),
        _row(
            blocker_id="finite_bound_to_smallness",
            candidate_theorem="Lin 1998 streamlined CKN proof",
            citation=(
                "Lin 1998 new proof of CKN; docs/KNOWN_LOCAL_ENSTROPHY_CRITERIA.md"
            ),
            applies_directly=False,
            gap_if_partial=(
                "Lin simplifies the epsilon-regularity proof route, but it does not "
                "convert finite bounded critical mass into epsilon smallness. A "
                "monotonicity, decay, or self-improvement theorem is still missing."
            ),
            verdict="resolvable_needs_new_result",
        ),
        _row(
            blocker_id="finite_bound_to_smallness",
            candidate_theorem="Vasseur 2007 De Giorgi partial-regularity iteration",
            citation=(
                "Vasseur 2007 Theorem 1, Theorem 2, Proposition 3, and Appendix "
                "Conjecture 14; "
                "papers/blockers/finite_bound_to_smallness/"
                "vasseur2007_partial_regularity_NS_UT.pdf; "
                "track-a-regularity/reports/"
                "lemma_0252_finite_bound_smallness_source_read_packet.md"
            ),
            applies_directly=False,
            gap_if_partial=(
                "Vasseur's route gives a De Giorgi proof of CKN-type partial "
                "regularity, but Theorem 1 assumes a small local velocity, gradient, "
                "and pressure package; Theorem 2 assumes small scaled gradient "
                "dissipation; and the appendix identifies that full regularity would "
                "need a strengthened beta>3/2 iteration, while the actual local "
                "pressure term remains below that threshold. lemma_0252 supplies only "
                "finite critical parabolic Morrey/vorticity-enstrophy boundedness, "
                "not epsilon smallness, the pressure package, or the missing "
                "beta>3/2 pressure control."
            ),
            verdict="resolvable_needs_new_result",
        ),
        _row(
            blocker_id="finite_bound_to_smallness",
            candidate_theorem="Tao 2014 averaged-NSE blow-up obstruction warning",
            citation=(
                "Tao 1402.0290; docs/paper_notes/1402.0290.md; "
                "BV caution docs/paper_notes/1709.10033.md and docs/paper_notes/1901.09023.md"
            ),
            applies_directly=False,
            gap_if_partial=(
                "Negative reference rather than a route: this is outside setting for "
                "exact 3D NSE, and the Tao/BV warning is that energy-scale or "
                "critical-envelope heuristics do not create finite-bound-to-smallness "
                "without a new mechanism."
            ),
            verdict="permanently_blocked",
        ),
        _row(
            blocker_id="compactness_liouville",
            candidate_theorem="Escauriaza-Seregin-Sverak backward uniqueness branch",
            citation=(
                "ESS 2003/2004 backward uniqueness; "
                "papers/blockers/compactness_liouville/"
                "1509.04940_backward_uniqueness_remarks.pdf; "
                "docs/KNOWN_LOCAL_ENSTROPHY_CRITERIA.md; "
                "docs/LEMMA_0252_PROOF_OBLIGATIONS.md; "
                "track-a-regularity/reports/"
                "lemma_0252_compactness_liouville_source_read_packet.md"
            ),
            applies_directly=False,
            gap_if_partial=(
                "ESS is an endpoint critical-velocity/backward-uniqueness route: it "
                "needs a compatible terminal or ancient-limit setup, endpoint "
                "velocity control such as L-infinity_t L3_x, enough boundedness and "
                "decay for a Carleman/backward-uniqueness theorem, and pressure and "
                "vorticity regularity that let the parabolic argument apply. The "
                "local 1509.04940 remarks are only a caution source rather than a "
                "replacement theorem, but they highlight that vorticity, pressure, "
                "and scaling inputs cannot be treated as automatic. lemma_0252 "
                "supplies finite critical parabolic Morrey/vorticity-enstrophy "
                "metadata, not the endpoint velocity class, compactness/"
                "nontriviality package, or backward-uniqueness hypotheses."
            ),
            verdict="resolvable_needs_new_result",
        ),
        _row(
            blocker_id="compactness_liouville",
            candidate_theorem="KNSS axisymmetric Liouville/backward-uniqueness branch",
            citation=(
                "Koch-Nadirashvili-Seregin-Sverak 2009, Abstract, "
                "Theorems 5.1-5.3, Lemma 6.1, and Proposition 6.1; "
                "papers/blockers/compactness_liouville/"
                "0709.3599_KNSS2009_liouville_acta_math.pdf; "
                "track-a-regularity/reports/"
                "lemma_0252_compactness_liouville_source_read_packet.md; "
                "Tao/BV caution"
            ),
            applies_directly=False,
            gap_if_partial=(
                "Outside setting: KNSS supplies a bounded ancient mild/weak "
                "Liouville template, but the proved rigidity is two-dimensional "
                "or axisymmetric three-dimensional with no-swirl, scale-invariant, "
                "or special-geometry assumptions, while KNSS states the general "
                "three-dimensional bounded ancient problem is open. lemma_0252 is "
                "a general periodic 3D statement with only finite critical "
                "parabolic Morrey/vorticity-enstrophy metadata; it does not supply "
                "axisymmetry, global L-infinity velocity, the mild ancient-limit "
                "compactness package, pressure/local-energy compactness, or the "
                "nontriviality package needed by the KNSS blow-up route. The "
                "Tao/BV warning therefore keeps this branch as a special-case "
                "comparison, not a direct compactness/Liouville discharge."
            ),
            verdict="permanently_blocked",
        ),
        _row(
            blocker_id="compactness_liouville",
            candidate_theorem="Seregin Type-I and scale-invariant Liouville literature",
            citation=(
                "Seregin Type-I/scale-invariant criteria comparison; "
                "docs/KNOWN_LOCAL_ENSTROPHY_CRITERIA.md"
            ),
            applies_directly=False,
            gap_if_partial=(
                "Type-I or velocity-scale hypotheses must be named exactly and shown "
                "to pass to an ancient suitable limit. The current finite local "
                "vorticity-enstrophy envelope is only adjacent to that setting."
            ),
            verdict="resolvable_needs_new_result",
        ),
        _row(
            blocker_id="smooth_continuation_bridge",
            candidate_theorem="BKM 1984 vorticity continuation criterion",
            citation=(
                "Beale-Kato-Majda 1984 continuation criterion; "
                "docs/LEMMA_0252_LOCAL_ENERGY_FORMAL_MAP.md"
            ),
            applies_directly=False,
            gap_if_partial=(
                "BKM requires time-integrable L-infinity vorticity control up to the "
                "terminal time. A finite parabolic Morrey L2 vorticity envelope does "
                "not provide that continuation norm."
            ),
            verdict="resolvable_needs_new_result",
        ),
        _row(
            blocker_id="smooth_continuation_bridge",
            candidate_theorem="Prodi-Serrin velocity-class continuation criterion",
            citation=(
                "Prodi-Serrin criteria; docs/LEMMA_0252_PROOF_OBLIGATIONS.md; "
                "track-c-formal/lean/NavierStokesProgram/SolutionClasses.lean"
            ),
            applies_directly=False,
            gap_if_partial=(
                "Prodi-Serrin needs a global velocity class with the critical scaling "
                "relation and endpoint conventions. lemma_0252 supplies local "
                "vorticity-enstrophy metadata, not the required velocity norm."
            ),
            verdict="resolvable_needs_new_result",
        ),
        _row(
            blocker_id="smooth_continuation_bridge",
            candidate_theorem="Constantin-Fefferman vorticity-direction criterion",
            citation=(
                "Constantin-Fefferman 1993 geometric criterion; "
                "docs/KNOWN_GEOMETRIC_CRITERIA.md; docs/LEMMA_0252_LOCAL_ENERGY_FORMAL_MAP.md"
            ),
            applies_directly=False,
            gap_if_partial=(
                "The geometric criterion requires coherence of vorticity direction "
                "plus magnitude/localization hypotheses. lemma_0252 has only the "
                "finite local enstrophy envelope and no direction-coherence input."
            ),
            verdict="resolvable_needs_new_result",
        ),
    )


def _missing_source_refs() -> tuple[str, ...]:
    return tuple(source for source in LOCAL_SOURCE_REFS if not (ROOT / source).exists())


def _validate_rows(rows: tuple[TheoremMappingRow, ...]) -> None:
    expected = set(EXPECTED_BLOCKERS)
    seen = {row.blocker_id for row in rows}
    if seen != expected:
        raise ValueError(
            "known-theorem rows must cover exactly "
            f"{sorted(expected)}; got {sorted(seen)}"
        )

    for index, row in enumerate(rows):
        if row.blocker_id not in expected:
            raise ValueError(f"row {index} has unknown blocker_id: {row.blocker_id}")
        if not row.candidate_theorem:
            raise ValueError(f"row {index} has empty candidate_theorem")
        if not row.citation:
            raise ValueError(f"row {index} has empty citation")
        if not isinstance(row.applies_directly, bool):
            raise ValueError(f"row {index} applies_directly must be boolean")
        if not row.gap_if_partial:
            raise ValueError(f"row {index} has empty gap_if_partial")
        if row.verdict not in VERDICTS:
            raise ValueError(f"row {index} has unknown verdict: {row.verdict}")


def _rows_per_blocker(rows: tuple[TheoremMappingRow, ...]) -> dict[str, int]:
    return {
        blocker_id: sum(1 for row in rows if row.blocker_id == blocker_id)
        for blocker_id in EXPECTED_BLOCKERS
    }


def check_permanent_blocker_justification(
    mapping: Lemma0252KnownTheoremMapping,
) -> tuple[bool, str]:
    bad_rows: list[str] = []
    for row in mapping.rows:
        if row.verdict != "permanently_blocked":
            continue
        text = f"{row.citation} {row.gap_if_partial}"
        has_outside_setting = "outside setting" in text.lower()
        has_tao_or_bv = "Tao" in text or "BV" in text
        if not has_outside_setting or not has_tao_or_bv:
            bad_rows.append(row.candidate_theorem)
    if bad_rows:
        return (
            False,
            "permanently_blocked rows lack outside-setting plus Tao/BV justification: "
            + ", ".join(bad_rows),
        )
    return True, "all permanently_blocked rows carry outside-setting plus Tao/BV justification"


def build_known_theorem_mapping(
    *,
    proof_obligation_json: Path = DEFAULT_INPUT,
) -> Lemma0252KnownTheoremMapping:
    summary = load_blocker_summary(proof_obligation_json)
    if summary.lemma_id != "lemma_0252":
        raise ValueError(f"expected lemma_0252, got {summary.lemma_id}")
    if summary.candidate_status != "needs_review":
        raise ValueError(f"expected candidate_status=needs_review, got {summary.candidate_status}")
    if summary.active_candidate:
        raise ValueError("lemma_0252 must remain active_candidate=false")

    expected = set(EXPECTED_BLOCKERS)
    observed = set(summary.promotion_blocker_keys)
    if observed != expected:
        raise ValueError(
            "lemma_0252 promotion blockers changed: "
            f"expected {sorted(expected)}, got {sorted(observed)}"
        )

    rows = _canonical_rows()
    _validate_rows(rows)
    rows_per_blocker = _rows_per_blocker(rows)

    return Lemma0252KnownTheoremMapping(
        schema_version=1,
        lemma_id=summary.lemma_id,
        candidate_status=summary.candidate_status,
        active_candidate=summary.active_candidate,
        promotion_blocker_count=summary.promotion_blocker_count,
        blocker_count=len(EXPECTED_BLOCKERS),
        row_count=len(rows),
        rows_per_blocker=rows_per_blocker,
        resolvable_known_count=sum(1 for row in rows if row.verdict == "resolvable_known"),
        resolvable_needs_new_result_count=sum(
            1 for row in rows if row.verdict == "resolvable_needs_new_result"
        ),
        permanently_blocked_count=sum(1 for row in rows if row.verdict == "permanently_blocked"),
        rows=rows,
        source_refs=LOCAL_SOURCE_REFS,
        non_claims=NON_CLAIMS,
    )


def mapping_to_dict(mapping: Lemma0252KnownTheoremMapping) -> dict[str, object]:
    return {
        "schema_version": mapping.schema_version,
        "lemma_id": mapping.lemma_id,
        "candidate_status": mapping.candidate_status,
        "active_candidate": mapping.active_candidate,
        "promotion_blocker_count": mapping.promotion_blocker_count,
        "blocker_count": mapping.blocker_count,
        "row_count": mapping.row_count,
        "rows_per_blocker": mapping.rows_per_blocker,
        "resolvable_known_count": mapping.resolvable_known_count,
        "resolvable_needs_new_result_count": mapping.resolvable_needs_new_result_count,
        "permanently_blocked_count": mapping.permanently_blocked_count,
        "rows": [
            {
                "blocker_id": row.blocker_id,
                "candidate_theorem": row.candidate_theorem,
                "citation": row.citation,
                "applies_directly": row.applies_directly,
                "gap_if_partial": row.gap_if_partial,
                "verdict": row.verdict,
            }
            for row in mapping.rows
        ],
        "source_refs": list(mapping.source_refs),
        "non_claims": list(mapping.non_claims),
    }


def _table_cell(value: object) -> str:
    text = str(value).replace("\n", " ").replace("|", "/")
    return text


def render_markdown(mapping: Lemma0252KnownTheoremMapping) -> str:
    rows = [
        "| blocker_id | candidate_theorem | citation | applies_directly | gap_if_partial | verdict |",
        "|---|---|---|---:|---|---|",
    ]
    for row in mapping.rows:
        rows.append(
            "| "
            f"`{_table_cell(row.blocker_id)}` | "
            f"{_table_cell(row.candidate_theorem)} | "
            f"{_table_cell(row.citation)} | "
            f"`{str(row.applies_directly).lower()}` | "
            f"{_table_cell(row.gap_if_partial)} | "
            f"`{_table_cell(row.verdict)}` |"
        )

    per_blocker_rows = [
        "| blocker_id | row_count |",
        "|---|---:|",
        *(
            f"| `{blocker_id}` | `{mapping.rows_per_blocker[blocker_id]}` |"
            for blocker_id in EXPECTED_BLOCKERS
        ),
    ]

    return "\n".join(
        (
            "# Lemma 0252 Blocker Known-Theorem Mapping",
            "",
            "Generated by `track-a-regularity/evaluator/lemma_0252_blocker_known_theorem_mapping.py`.",
            "",
            "This read-only report maps the three substantive `lemma_0252` promotion blockers",
            "to known-theorem families. It does not discharge any blocker, promote an active",
            "candidate, prove epsilon regularity, or solve Navier-Stokes.",
            "",
            "## Summary",
            "",
            f"- lemma_id: `{mapping.lemma_id}`",
            f"- candidate_status: `{mapping.candidate_status}`",
            f"- active_candidate: `{str(mapping.active_candidate).lower()}`",
            f"- promotion_blocker_count: `{mapping.promotion_blocker_count}`",
            f"- blocker_count: `{mapping.blocker_count}`",
            f"- row_count: `{mapping.row_count}`",
            f"- resolvable_known_count: `{mapping.resolvable_known_count}`",
            f"- resolvable_needs_new_result_count: `{mapping.resolvable_needs_new_result_count}`",
            f"- permanently_blocked_count: `{mapping.permanently_blocked_count}`",
            "",
            "## Rows Per Blocker",
            "",
            *per_blocker_rows,
            "",
            "## Known-Theorem Mapping",
            "",
            *rows,
            "",
            "## Local Source Refs",
            "",
            *(f"- `{source}`" for source in mapping.source_refs),
            "",
            "## Non-Claims",
            "",
            *(f"- `{claim}`" for claim in mapping.non_claims),
            "",
        )
    )


def render_json(mapping: Lemma0252KnownTheoremMapping) -> str:
    return json.dumps(mapping_to_dict(mapping), indent=2, sort_keys=True) + "\n"


def render_output(mapping: Lemma0252KnownTheoremMapping, output_format: str) -> str:
    if output_format == "markdown":
        return render_markdown(mapping)
    if output_format == "json":
        return render_json(mapping)
    raise ValueError(f"unknown lemma_0252 known-theorem mapping format: {output_format}")


def write_output(
    output: Path,
    mapping: Lemma0252KnownTheoremMapping,
    output_format: str,
) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_output(mapping, output_format), encoding="utf-8")
    return output


def check_output(
    output: Path,
    mapping: Lemma0252KnownTheoremMapping,
    output_format: str,
) -> tuple[bool, str]:
    expected = render_output(mapping, output_format)
    if not output.exists():
        return False, f"missing lemma_0252 blocker known-theorem mapping: {output}"
    current = output.read_text(encoding="utf-8")
    if current != expected:
        return False, f"stale lemma_0252 blocker known-theorem mapping: {output}"
    return True, f"fresh lemma_0252 blocker known-theorem mapping: {output}"


def check_min_rows(
    mapping: Lemma0252KnownTheoremMapping,
    *,
    min_rows: int,
) -> tuple[bool, str]:
    if mapping.row_count < min_rows:
        return False, f"known-theorem mapping row_count {mapping.row_count} < {min_rows}"
    sparse = [
        f"{blocker}:{count}"
        for blocker, count in mapping.rows_per_blocker.items()
        if count < 2
    ]
    if sparse:
        return False, "known-theorem mapping has fewer than two rows for: " + ", ".join(sparse)
    return True, f"known-theorem mapping has {mapping.row_count} rows and >=2 rows per blocker"


def default_output_path(output_format: str) -> Path:
    if output_format == "markdown":
        return DEFAULT_MARKDOWN_OUTPUT
    if output_format == "json":
        return DEFAULT_JSON_OUTPUT
    raise ValueError(f"unknown lemma_0252 known-theorem mapping format: {output_format}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Map lemma_0252 promotion blockers to known theorem families."
    )
    parser.add_argument("--proof-obligation-json", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument(
        "--check-output",
        action="store_true",
        help="Check that --output already matches the rendered mapping.",
    )
    parser.add_argument(
        "--require-min-rows",
        type=int,
        default=None,
        help="Require at least this many theorem rows and at least two rows per blocker.",
    )
    parser.add_argument(
        "--require-no-resolvable-known",
        action="store_true",
        help="Fail if a known theorem is marked directly resolving a blocker.",
    )
    parser.add_argument(
        "--require-permanent-blocker-justification",
        action="store_true",
        help="Fail if permanently_blocked rows lack outside-setting plus Tao/BV justification.",
    )
    parser.add_argument(
        "--require-sources-exist",
        action="store_true",
        help="Fail if local source references are missing.",
    )
    args = parser.parse_args(argv)

    try:
        mapping = build_known_theorem_mapping(
            proof_obligation_json=args.proof_obligation_json,
        )
    except Exception as exc:  # noqa: BLE001 - CLI should return readable failures.
        print(f"failed to build lemma_0252 known-theorem mapping: {exc}", file=sys.stderr)
        return 1

    output = args.output or default_output_path(args.format)
    if args.check_output:
        ok, message = check_output(output, mapping, args.format)
        print(message)
        if not ok:
            print("run without --check-output to regenerate the known-theorem mapping", file=sys.stderr)
            return 1
    else:
        written = write_output(output, mapping, args.format)
        print(f"wrote {written}")

    if args.require_min_rows is not None:
        ok, message = check_min_rows(mapping, min_rows=args.require_min_rows)
        print(message)
        if not ok:
            return 1

    if args.require_no_resolvable_known and mapping.resolvable_known_count:
        print("at least one blocker is marked resolvable_known", file=sys.stderr)
        return 1

    if args.require_permanent_blocker_justification:
        ok, message = check_permanent_blocker_justification(mapping)
        print(message)
        if not ok:
            return 1

    if args.require_sources_exist:
        missing_sources = _missing_source_refs()
        if missing_sources:
            print("missing source refs: " + ", ".join(missing_sources), file=sys.stderr)
            return 1
        print("all lemma_0252 known-theorem mapping source refs exist")

    print(f"lemma_id: {mapping.lemma_id}")
    print(f"candidate_status: {mapping.candidate_status}")
    print(f"active_candidate: {str(mapping.active_candidate).lower()}")
    print(f"row_count: {mapping.row_count}")
    print(f"resolvable_known_count: {mapping.resolvable_known_count}")
    print(f"permanently_blocked_count: {mapping.permanently_blocked_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
