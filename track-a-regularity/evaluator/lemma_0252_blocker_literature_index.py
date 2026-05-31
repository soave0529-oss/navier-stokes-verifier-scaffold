from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from proof_obligation_blockers import DEFAULT_INPUT


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REPORT_DIR = ROOT / "track-a-regularity/reports"
DEFAULT_MARKDOWN_OUTPUT = DEFAULT_REPORT_DIR / "lemma_0252_blocker_literature_index.md"
DEFAULT_JSON_OUTPUT = DEFAULT_REPORT_DIR / "lemma_0252_blocker_literature_index.json"
DEFAULT_PAPERS_DIR = ROOT / "papers/blockers"
DEFAULT_INDEX = DEFAULT_PAPERS_DIR / "index.md"

EXPECTED_BLOCKERS = (
    "finite_bound_to_smallness",
    "compactness_liouville",
    "smooth_continuation_bridge",
)
EXPECTED_FAMILIES = EXPECTED_BLOCKERS + ("cross_cutting",)
SEARCH_LOGS = (
    "papers/blockers/_search_logs/search1_eps_reg.json",
    "papers/blockers/_search_logs/search2_liouville.json",
    "papers/blockers/_search_logs/search3_bkm.json",
)
NON_CLAIMS = (
    "read_only_literature_source_index",
    "local_pdf_inventory_only",
    "no_candidate_promotion",
    "no_candidate_emission",
    "no_blocker_discharge",
    "no_process_gate_opened",
    "no_epsilon_regularity_theorem",
    "no_compactness_or_liouville_theorem",
    "no_bkm_or_serrin_or_high_sobolev_bound",
    "no_weak_to_smooth_upgrade",
    "no_navier_stokes_solution",
)


@dataclass(frozen=True)
class LiteratureSource:
    source_id: str
    blocker_family: str
    relative_path: str
    source_type: str
    title: str
    authors_year: str
    arxiv_or_url: str
    priority: str
    role: str
    applicability: str
    verdict_hint: str
    direct_discharge: bool
    exists: bool


@dataclass(frozen=True)
class LiteratureFamilySummary:
    blocker_family: str
    source_count: int
    pdf_count: int
    html_count: int
    direct_discharge_count: int
    verdict_hints: tuple[str, ...]
    source_ids: tuple[str, ...]


@dataclass(frozen=True)
class LiteratureIndexCheck:
    key: str
    expected: str
    observed: str
    passed: bool


@dataclass(frozen=True)
class Lemma0252BlockerLiteratureIndex:
    schema_version: int
    lemma_id: str
    candidate_status: str
    active_candidate: bool
    index_markdown: str
    literature_source_count: int
    pdf_count: int
    html_count: int
    search_log_count: int
    missing_source_count: int
    missing_search_log_count: int
    blocker_family_count: int
    substantive_blocker_count: int
    cross_cutting_source_count: int
    unmapped_source_count: int
    direct_discharge_source_count: int
    source_index_check_count: int
    passed_source_index_check_count: int
    failed_source_index_check_count: int
    source_index_consistent: bool
    process_gate_open_authorized: bool
    blocker_state_changed: bool
    candidate_emission_authorized: bool
    issues: tuple[str, ...]
    missing_sources: tuple[str, ...]
    missing_search_logs: tuple[str, ...]
    families: tuple[LiteratureFamilySummary, ...]
    sources: tuple[LiteratureSource, ...]
    checks: tuple[LiteratureIndexCheck, ...]
    source_refs: tuple[str, ...]
    non_claims: tuple[str, ...]


def _source(
    *,
    source_id: str,
    blocker_family: str,
    relative_path: str,
    source_type: str,
    title: str,
    authors_year: str,
    arxiv_or_url: str,
    priority: str,
    role: str,
    applicability: str,
    verdict_hint: str,
    direct_discharge: bool = False,
) -> LiteratureSource:
    return LiteratureSource(
        source_id=source_id,
        blocker_family=blocker_family,
        relative_path=relative_path,
        source_type=source_type,
        title=title,
        authors_year=authors_year,
        arxiv_or_url=arxiv_or_url,
        priority=priority,
        role=role,
        applicability=applicability,
        verdict_hint=verdict_hint,
        direct_discharge=direct_discharge,
        exists=(ROOT / relative_path).exists(),
    )


def _inventory() -> tuple[LiteratureSource, ...]:
    return (
        _source(
            source_id="survey_2308_04147",
            blocker_family="finite_bound_to_smallness",
            relative_path=(
                "papers/blockers/finite_bound_to_smallness/"
                "2308.04147_partial_regularity_survey.pdf"
            ),
            source_type="pdf",
            title="Partial regularity survey",
            authors_year="survey, 2023",
            arxiv_or_url="arXiv:2308.04147",
            priority="high",
            role="epsilon-regularity and partial-regularity catalogue",
            applicability="partial; known routes remain smallness-based",
            verdict_hint="needs_new_result_or_smallness_gap",
        ),
        _source(
            source_id="quantitative_2210_01783",
            blocker_family="finite_bound_to_smallness",
            relative_path=(
                "papers/blockers/finite_bound_to_smallness/"
                "2210.01783_quantitative_partial_regularity_2022.pdf"
            ),
            source_type="pdf",
            title="Quantitative partial regularity source",
            authors_year="arXiv, 2022",
            arxiv_or_url="arXiv:2210.01783",
            priority="normal",
            role="quantitative epsilon-regularity comparison",
            applicability="partial; requires matching hypotheses beyond finite Morrey bound",
            verdict_hint="partial_only",
        ),
        _source(
            source_id="local_gradient_1606_02790",
            blocker_family="finite_bound_to_smallness",
            relative_path=(
                "papers/blockers/finite_bound_to_smallness/"
                "1606.02790_local_regularity_velocity_gradient.pdf"
            ),
            source_type="pdf",
            title="Local regularity via velocity gradient conditions",
            authors_year="arXiv, 2016",
            arxiv_or_url="arXiv:1606.02790",
            priority="normal",
            role="gradient-condition comparison",
            applicability="partial; gradient criterion is not finite Morrey smallness",
            verdict_hint="partial_only",
        ),
        _source(
            source_id="serrin_refinement_1310_3112",
            blocker_family="finite_bound_to_smallness",
            relative_path=(
                "papers/blockers/finite_bound_to_smallness/"
                "1310.3112_serrin_refinement_2013.pdf"
            ),
            source_type="pdf",
            title="Local Serrin-type refinement",
            authors_year="arXiv, 2013",
            arxiv_or_url="arXiv:1310.3112",
            priority="normal",
            role="local Serrin comparison",
            applicability="partial; Serrin input is stronger/different",
            verdict_hint="partial_only",
        ),
        _source(
            source_id="vasseur_2007_deg_i",
            blocker_family="finite_bound_to_smallness",
            relative_path=(
                "papers/blockers/finite_bound_to_smallness/"
                "vasseur2007_partial_regularity_NS_UT.pdf"
            ),
            source_type="pdf",
            title="Vasseur partial regularity via De Giorgi iteration",
            authors_year="Vasseur, 2007",
            arxiv_or_url="UT Austin hosted preprint",
            priority="high",
            role="closest self-improvement mechanism candidate",
            applicability="partial_plus; would need a parabolic Morrey/vorticity variant",
            verdict_hint="resolvable_needs_new_result",
        ),
        _source(
            source_id="knss_0709_3599",
            blocker_family="compactness_liouville",
            relative_path=(
                "papers/blockers/compactness_liouville/"
                "0709.3599_KNSS2009_liouville_acta_math.pdf"
            ),
            source_type="pdf",
            title="Liouville theorem for ancient solutions",
            authors_year="Koch-Nadirashvili-Seregin-Sverak, 2009",
            arxiv_or_url="arXiv:0709.3599",
            priority="high",
            role="core ancient-solution Liouville reference",
            applicability="partial; axisymmetric restrictions do not match general T3",
            verdict_hint="outside_setting_axisymmetric",
        ),
        _source(
            source_id="axisymmetric_1011_5066",
            blocker_family="compactness_liouville",
            relative_path=(
                "papers/blockers/compactness_liouville/"
                "1011.5066_axisymmetric_liouville_2010.pdf"
            ),
            source_type="pdf",
            title="Axisymmetric Liouville follow-up",
            authors_year="arXiv, 2010",
            arxiv_or_url="arXiv:1011.5066",
            priority="normal",
            role="axisymmetric Liouville comparison",
            applicability="partial; axisymmetric setting mismatch",
            verdict_hint="outside_setting_axisymmetric",
        ),
        _source(
            source_id="backward_uniqueness_1509_04940",
            blocker_family="compactness_liouville",
            relative_path=(
                "papers/blockers/compactness_liouville/"
                "1509.04940_backward_uniqueness_remarks.pdf"
            ),
            source_type="pdf",
            title="Backward uniqueness remarks",
            authors_year="arXiv, 2015",
            arxiv_or_url="arXiv:1509.04940",
            priority="normal",
            role="backward-uniqueness branch comparison",
            applicability="partial; finite Morrey input is not enough by itself",
            verdict_hint="partial_only",
        ),
        _source(
            source_id="lorentz_1407_5129",
            blocker_family="compactness_liouville",
            relative_path=(
                "papers/blockers/compactness_liouville/"
                "1407.5129_lorentz_navier_stokes.pdf"
            ),
            source_type="pdf",
            title="Lorentz-space Navier-Stokes regularity comparison",
            authors_year="Barker, 2014/2015",
            arxiv_or_url="arXiv:1407.5129",
            priority="normal",
            role="critical-space comparison around ESS-style criteria",
            applicability="partial; Lorentz-space criterion differs from parabolic Morrey",
            verdict_hint="partial_only",
        ),
        _source(
            source_id="seregin_axisym_math0702720",
            blocker_family="compactness_liouville",
            relative_path=(
                "papers/blockers/compactness_liouville/"
                "math0702720_seregin_axisym_sufficient_2007.pdf"
            ),
            source_type="pdf",
            title="Axisymmetric sufficient local regularity",
            authors_year="Seregin, 2007",
            arxiv_or_url="arXiv:math/0702720",
            priority="normal",
            role="axisymmetric local regularity comparison",
            applicability="partial; axisymmetric setting mismatch",
            verdict_hint="outside_setting_axisymmetric",
        ),
        _source(
            source_id="besov_negative_math0703883",
            blocker_family="smooth_continuation_bridge",
            relative_path=(
                "papers/blockers/smooth_continuation_bridge/"
                "math0703883_besov_negative_blowup.pdf"
            ),
            source_type="pdf",
            title="Negative-Besov blow-up criterion",
            authors_year="arXiv, 2007",
            arxiv_or_url="arXiv:math/0703883",
            priority="normal",
            role="BKM-adjacent continuation criterion comparison",
            applicability="partial; needs bridge from local metadata to Besov/BKM input",
            verdict_hint="chain_blocked_by_smallness",
        ),
        _source(
            source_id="robinson_review_1410_4495",
            blocker_family="smooth_continuation_bridge",
            relative_path=(
                "papers/blockers/smooth_continuation_bridge/"
                "1410.4495_robinson_review_NSE.pdf"
            ),
            source_type="pdf",
            title="Navier-Stokes regularity criteria review",
            authors_year="Robinson review, 2014/2015",
            arxiv_or_url="arXiv:1410.4495",
            priority="high",
            role="BKM/Serrin/Prodi-Serrin inventory source",
            applicability="partial; continuation bridge depends on upstream local regularity",
            verdict_hint="chain_blocked_by_smallness",
        ),
        _source(
            source_id="tao_localisation_1108_1165",
            blocker_family="cross_cutting",
            relative_path=(
                "papers/blockers/cross_cutting/"
                "1108.1165_tao2013_localisation_compactness.pdf"
            ),
            source_type="pdf",
            title="Localisation and compactness for Navier-Stokes",
            authors_year="Tao, 2013",
            arxiv_or_url="arXiv:1108.1165",
            priority="top",
            role="localised energy/enstrophy framework nearest to lemma_0252",
            applicability="cross_cutting; maps framework but does not discharge blockers",
            verdict_hint="framework_anchor",
        ),
        _source(
            source_id="tao_averaged_1402_0290",
            blocker_family="cross_cutting",
            relative_path=(
                "papers/blockers/cross_cutting/"
                "1402.0290_tao2014_averaged_NSE.pdf"
            ),
            source_type="pdf",
            title="Finite-time blowup for averaged 3D Navier-Stokes",
            authors_year="Tao, 2014",
            arxiv_or_url="arXiv:1402.0290",
            priority="high",
            role="general-method caution for broad critical estimates",
            applicability="cross_cutting caution; not a discharge theorem",
            verdict_hint="caution_general_methods",
        ),
        _source(
            source_id="tao_blog_2007",
            blocker_family="cross_cutting",
            relative_path=(
                "papers/blockers/cross_cutting/"
                "tao2007_blog_why_regularity_hard.html"
            ),
            source_type="html",
            title="Why global regularity for Navier-Stokes is hard",
            authors_year="Tao, 2007",
            arxiv_or_url="Tao blog",
            priority="high",
            role="conceptual hardness anchor",
            applicability="cross_cutting caution; informal context only",
            verdict_hint="caution_general_methods",
        ),
    )


def _load_json(path: Path) -> dict[str, object]:
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"expected object JSON report: {path}")
    return data


def _check(*, key: str, expected: object, observed: object) -> LiteratureIndexCheck:
    return LiteratureIndexCheck(
        key=key,
        expected=str(expected),
        observed=str(observed),
        passed=expected == observed,
    )


def _family_summaries(
    sources: tuple[LiteratureSource, ...],
) -> tuple[LiteratureFamilySummary, ...]:
    summaries: list[LiteratureFamilySummary] = []
    for family in EXPECTED_FAMILIES:
        family_sources = tuple(source for source in sources if source.blocker_family == family)
        verdict_hints = tuple(
            dict.fromkeys(source.verdict_hint for source in family_sources)
        )
        summaries.append(
            LiteratureFamilySummary(
                blocker_family=family,
                source_count=len(family_sources),
                pdf_count=sum(1 for source in family_sources if source.source_type == "pdf"),
                html_count=sum(1 for source in family_sources if source.source_type == "html"),
                direct_discharge_count=sum(
                    1 for source in family_sources if source.direct_discharge
                ),
                verdict_hints=verdict_hints,
                source_ids=tuple(source.source_id for source in family_sources),
            )
        )
    return tuple(summaries)


def _missing_refs(refs: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(ref for ref in refs if not (ROOT / ref).exists())


def build_blocker_literature_index(
    *,
    proof_obligation_json: Path = DEFAULT_INPUT,
    papers_index: Path = DEFAULT_INDEX,
) -> Lemma0252BlockerLiteratureIndex:
    proof_graph = _load_json(proof_obligation_json)
    sources = _inventory()
    families = _family_summaries(sources)
    covered_substantive = tuple(
        family for family in EXPECTED_BLOCKERS if any(
            source.blocker_family == family for source in sources
        )
    )

    source_refs = tuple(
        dict.fromkeys(
            ("papers/blockers/index.md",)
            + tuple(source.relative_path for source in sources)
            + SEARCH_LOGS
        )
    )
    missing_sources = tuple(
        source.relative_path for source in sources if not source.exists
    )
    missing_search_logs = _missing_refs(SEARCH_LOGS)
    direct_discharge_source_count = sum(1 for source in sources if source.direct_discharge)
    checks = (
        _check(
            key="lemma_id.matches_proof_graph",
            expected="lemma_0252",
            observed=proof_graph.get("lemma_id"),
        ),
        _check(
            key="candidate_status.remains_needs_review",
            expected="needs_review",
            observed=proof_graph.get("candidate_status"),
        ),
        _check(
            key="active_candidate.remains_false",
            expected=False,
            observed=proof_graph.get("active_candidate"),
        ),
        _check(
            key="substantive_blockers.covered",
            expected=EXPECTED_BLOCKERS,
            observed=covered_substantive,
        ),
        _check(
            key="literature_source_count.expected_fifteen",
            expected=15,
            observed=len(sources),
        ),
        _check(
            key="pdf_count.expected_fourteen",
            expected=14,
            observed=sum(1 for source in sources if source.source_type == "pdf"),
        ),
        _check(
            key="html_count.expected_one",
            expected=1,
            observed=sum(1 for source in sources if source.source_type == "html"),
        ),
        _check(
            key="families.expected_four",
            expected=EXPECTED_FAMILIES,
            observed=tuple(family.blocker_family for family in families),
        ),
        _check(
            key="finite_bound_to_smallness.source_count",
            expected=5,
            observed=next(
                family.source_count
                for family in families
                if family.blocker_family == "finite_bound_to_smallness"
            ),
        ),
        _check(
            key="compactness_liouville.source_count",
            expected=5,
            observed=next(
                family.source_count
                for family in families
                if family.blocker_family == "compactness_liouville"
            ),
        ),
        _check(
            key="smooth_continuation_bridge.source_count",
            expected=2,
            observed=next(
                family.source_count
                for family in families
                if family.blocker_family == "smooth_continuation_bridge"
            ),
        ),
        _check(
            key="cross_cutting.source_count",
            expected=3,
            observed=next(
                family.source_count
                for family in families
                if family.blocker_family == "cross_cutting"
            ),
        ),
        _check(
            key="all_literature_sources_exist",
            expected=0,
            observed=len(missing_sources),
        ),
        _check(
            key="all_search_logs_exist",
            expected=0,
            observed=len(missing_search_logs),
        ),
        _check(
            key="papers_index_exists",
            expected=True,
            observed=papers_index.exists(),
        ),
        _check(
            key="direct_discharge_source_count.remains_zero",
            expected=0,
            observed=direct_discharge_source_count,
        ),
    )
    issues = tuple(check.key for check in checks if not check.passed)
    failed_count = len(issues)

    return Lemma0252BlockerLiteratureIndex(
        schema_version=1,
        lemma_id=str(proof_graph.get("lemma_id")),
        candidate_status=str(proof_graph.get("candidate_status")),
        active_candidate=bool(proof_graph.get("active_candidate")),
        index_markdown=str(papers_index),
        literature_source_count=len(sources),
        pdf_count=sum(1 for source in sources if source.source_type == "pdf"),
        html_count=sum(1 for source in sources if source.source_type == "html"),
        search_log_count=len(SEARCH_LOGS),
        missing_source_count=len(missing_sources),
        missing_search_log_count=len(missing_search_logs),
        blocker_family_count=len(families),
        substantive_blocker_count=len(EXPECTED_BLOCKERS),
        cross_cutting_source_count=next(
            family.source_count for family in families if family.blocker_family == "cross_cutting"
        ),
        unmapped_source_count=sum(
            1 for source in sources if source.blocker_family not in EXPECTED_FAMILIES
        ),
        direct_discharge_source_count=direct_discharge_source_count,
        source_index_check_count=len(checks),
        passed_source_index_check_count=len(checks) - failed_count,
        failed_source_index_check_count=failed_count,
        source_index_consistent=failed_count == 0,
        process_gate_open_authorized=False,
        blocker_state_changed=False,
        candidate_emission_authorized=False,
        issues=issues,
        missing_sources=missing_sources,
        missing_search_logs=missing_search_logs,
        families=families,
        sources=sources,
        checks=checks,
        source_refs=source_refs,
        non_claims=NON_CLAIMS,
    )


def literature_index_to_dict(
    index: Lemma0252BlockerLiteratureIndex,
) -> dict[str, object]:
    return {
        "schema_version": index.schema_version,
        "lemma_id": index.lemma_id,
        "candidate_status": index.candidate_status,
        "active_candidate": index.active_candidate,
        "index_markdown": index.index_markdown,
        "literature_source_count": index.literature_source_count,
        "pdf_count": index.pdf_count,
        "html_count": index.html_count,
        "search_log_count": index.search_log_count,
        "missing_source_count": index.missing_source_count,
        "missing_search_log_count": index.missing_search_log_count,
        "blocker_family_count": index.blocker_family_count,
        "substantive_blocker_count": index.substantive_blocker_count,
        "cross_cutting_source_count": index.cross_cutting_source_count,
        "unmapped_source_count": index.unmapped_source_count,
        "direct_discharge_source_count": index.direct_discharge_source_count,
        "source_index_check_count": index.source_index_check_count,
        "passed_source_index_check_count": index.passed_source_index_check_count,
        "failed_source_index_check_count": index.failed_source_index_check_count,
        "source_index_consistent": index.source_index_consistent,
        "process_gate_open_authorized": index.process_gate_open_authorized,
        "blocker_state_changed": index.blocker_state_changed,
        "candidate_emission_authorized": index.candidate_emission_authorized,
        "issues": list(index.issues),
        "missing_sources": list(index.missing_sources),
        "missing_search_logs": list(index.missing_search_logs),
        "families": [asdict(family) for family in index.families],
        "sources": [asdict(source) for source in index.sources],
        "checks": [asdict(check) for check in index.checks],
        "source_refs": list(index.source_refs),
        "non_claims": list(index.non_claims),
        "docs": {
            "step_doc": "docs/STEP106_LEMMA_0252_BLOCKER_LITERATURE_INDEX.md",
            "proof_obligation_graph": "track-a-regularity/reports/lemma_0252_proof_obligation_graph.json",
            "papers_index": "papers/blockers/index.md",
        },
    }


def _format(text: str) -> str:
    return text.replace("|", "\\|")


def _family_rows(index: Lemma0252BlockerLiteratureIndex) -> list[str]:
    rows = [
        "| blocker family | sources | pdf | html | direct discharge | verdict hints | source ids |",
        "|---|---:|---:|---:|---:|---|---|",
    ]
    for family in index.families:
        rows.append(
            "| "
            f"`{family.blocker_family}` | "
            f"{family.source_count} | "
            f"{family.pdf_count} | "
            f"{family.html_count} | "
            f"{family.direct_discharge_count} | "
            f"{'<br>'.join(f'`{hint}`' for hint in family.verdict_hints)} | "
            f"{'<br>'.join(f'`{source_id}`' for source_id in family.source_ids)} |"
        )
    return rows


def _source_rows(index: Lemma0252BlockerLiteratureIndex) -> list[str]:
    rows = [
        "| blocker family | source id | path | type | priority | applicability | direct discharge |",
        "|---|---|---|---|---|---|---|",
    ]
    for source in index.sources:
        rows.append(
            "| "
            f"`{source.blocker_family}` | "
            f"`{source.source_id}` | "
            f"`{source.relative_path}` | "
            f"`{source.source_type}` | "
            f"`{source.priority}` | "
            f"{_format(source.applicability)} | "
            f"`{str(source.direct_discharge).lower()}` |"
        )
    return rows


def _check_rows(index: Lemma0252BlockerLiteratureIndex) -> list[str]:
    rows = [
        "| check | expected | observed | passed |",
        "|---|---|---|---|",
    ]
    for check in index.checks:
        rows.append(
            "| "
            f"`{check.key}` | "
            f"`{_format(check.expected)}` | "
            f"`{_format(check.observed)}` | "
            f"`{str(check.passed).lower()}` |"
        )
    return rows


def render_markdown(index: Lemma0252BlockerLiteratureIndex) -> str:
    return "\n".join(
        (
            "# Lemma 0252 Blocker Literature Index",
            "",
            "Generated by `track-a-regularity/evaluator/lemma_0252_blocker_literature_index.py`.",
            "",
            "This read-only report indexes the local `papers/blockers/` collection against the",
            "three substantive `lemma_0252` proof-obligation blockers. It records literature",
            "coverage and source existence only. It does not discharge a blocker, open a process",
            "gate, or authorize candidate emission.",
            "",
            "## Summary",
            "",
            f"- lemma_id: `{index.lemma_id}`",
            f"- candidate_status: `{index.candidate_status}`",
            f"- active_candidate: `{str(index.active_candidate).lower()}`",
            f"- literature_source_count: `{index.literature_source_count}`",
            f"- pdf_count: `{index.pdf_count}`",
            f"- html_count: `{index.html_count}`",
            f"- search_log_count: `{index.search_log_count}`",
            f"- missing_source_count: `{index.missing_source_count}`",
            f"- missing_search_log_count: `{index.missing_search_log_count}`",
            f"- blocker_family_count: `{index.blocker_family_count}`",
            f"- substantive_blocker_count: `{index.substantive_blocker_count}`",
            f"- cross_cutting_source_count: `{index.cross_cutting_source_count}`",
            f"- unmapped_source_count: `{index.unmapped_source_count}`",
            f"- direct_discharge_source_count: `{index.direct_discharge_source_count}`",
            f"- source_index_check_count: `{index.source_index_check_count}`",
            f"- passed_source_index_check_count: `{index.passed_source_index_check_count}`",
            f"- failed_source_index_check_count: `{index.failed_source_index_check_count}`",
            f"- source_index_consistent: `{str(index.source_index_consistent).lower()}`",
            f"- process_gate_open_authorized: `{str(index.process_gate_open_authorized).lower()}`",
            f"- blocker_state_changed: `{str(index.blocker_state_changed).lower()}`",
            f"- candidate_emission_authorized: `{str(index.candidate_emission_authorized).lower()}`",
            f"- issues: `{', '.join(index.issues) or 'none'}`",
            "",
            "## Families",
            "",
            *_family_rows(index),
            "",
            "## Sources",
            "",
            *_source_rows(index),
            "",
            "## Checks",
            "",
            *_check_rows(index),
            "",
            "## Non-Claims",
            "",
            *(f"- `{item}`" for item in index.non_claims),
            "",
        )
    )


def render_json(index: Lemma0252BlockerLiteratureIndex) -> str:
    return json.dumps(literature_index_to_dict(index), indent=2, sort_keys=True) + "\n"


def render_output(
    index: Lemma0252BlockerLiteratureIndex,
    output_format: str,
) -> str:
    if output_format == "markdown":
        return render_markdown(index)
    if output_format == "json":
        return render_json(index)
    raise ValueError(f"unknown blocker literature index format: {output_format}")


def write_output(
    output: Path,
    index: Lemma0252BlockerLiteratureIndex,
    output_format: str,
) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_output(index, output_format), encoding="utf-8")
    return output


def check_output(
    output: Path,
    index: Lemma0252BlockerLiteratureIndex,
    output_format: str,
) -> tuple[bool, str]:
    expected = render_output(index, output_format)
    if not output.exists():
        return False, f"missing lemma_0252 blocker literature index: {output}"
    current = output.read_text(encoding="utf-8")
    if current != expected:
        return False, f"stale lemma_0252 blocker literature index: {output}"
    return True, f"fresh lemma_0252 blocker literature index: {output}"


def check_sources(index: Lemma0252BlockerLiteratureIndex) -> tuple[bool, str]:
    if index.missing_source_count or index.missing_search_log_count:
        missing = index.missing_sources + index.missing_search_logs
        return False, "missing blocker literature sources: " + ", ".join(missing)
    return True, "all blocker literature sources exist"


def check_consistent(index: Lemma0252BlockerLiteratureIndex) -> tuple[bool, str]:
    if not index.source_index_consistent:
        return False, "blocker literature index inconsistent: " + ", ".join(index.issues)
    return True, "blocker literature index is consistent"


def check_blocked(index: Lemma0252BlockerLiteratureIndex) -> tuple[bool, str]:
    if index.process_gate_open_authorized:
        return False, "process gate open became authorized"
    if index.blocker_state_changed:
        return False, "blocker literature index changed blocker state"
    if index.candidate_emission_authorized:
        return False, "blocker literature index authorized candidate emission"
    if index.direct_discharge_source_count:
        return False, "blocker literature index marked a source as direct discharge"
    if index.candidate_status != "needs_review" or index.active_candidate:
        return False, "lemma_0252 candidate state changed"
    return True, "blocker literature index keeps lemma_0252 blocked"


def default_output_path(output_format: str) -> Path:
    if output_format == "markdown":
        return DEFAULT_MARKDOWN_OUTPUT
    if output_format == "json":
        return DEFAULT_JSON_OUTPUT
    raise ValueError(f"unknown blocker literature index format: {output_format}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Index local papers/blockers sources against lemma_0252 blockers."
    )
    parser.add_argument("--proof-obligation-json", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--papers-index", type=Path, default=DEFAULT_INDEX)
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--check-output", action="store_true")
    parser.add_argument("--require-sources-exist", action="store_true")
    parser.add_argument("--require-consistent", action="store_true")
    parser.add_argument("--require-blocked", action="store_true")
    args = parser.parse_args(argv)

    try:
        index = build_blocker_literature_index(
            proof_obligation_json=args.proof_obligation_json,
            papers_index=args.papers_index,
        )
    except Exception as exc:  # noqa: BLE001 - CLI should report setup failures.
        print(f"failed to build lemma_0252 blocker literature index: {exc}", file=sys.stderr)
        return 1

    output = args.output or default_output_path(args.format)
    if args.check_output:
        ok, message = check_output(output, index, args.format)
        print(message)
        if not ok:
            print(
                "run without --check-output to regenerate the blocker literature index",
                file=sys.stderr,
            )
            return 1
    else:
        written = write_output(output, index, args.format)
        print(f"wrote {written}")

    if args.require_sources_exist:
        ok, message = check_sources(index)
        print(message)
        if not ok:
            return 1
    if args.require_consistent:
        ok, message = check_consistent(index)
        print(message)
        if not ok:
            return 1
    if args.require_blocked:
        ok, message = check_blocked(index)
        print(message)
        if not ok:
            return 1

    print(f"literature_source_count: {index.literature_source_count}")
    print(f"source_index_check_count: {index.source_index_check_count}")
    print(f"failed_source_index_check_count: {index.failed_source_index_check_count}")
    print(f"source_index_consistent: {str(index.source_index_consistent).lower()}")
    print(f"candidate_emission_authorized: {str(index.candidate_emission_authorized).lower()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
