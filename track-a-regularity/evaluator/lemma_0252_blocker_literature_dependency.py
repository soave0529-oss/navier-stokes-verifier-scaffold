from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from lemma_0252_blocker_closure_dashboard import (
    DEFAULT_JSON_OUTPUT as DEFAULT_CLOSURE_JSON_OUTPUT,
    DEFAULT_MARKDOWN_OUTPUT as DEFAULT_CLOSURE_MARKDOWN_OUTPUT,
)
from lemma_0252_blocker_literature_index import (
    DEFAULT_JSON_OUTPUT as DEFAULT_LITERATURE_JSON_OUTPUT,
    DEFAULT_MARKDOWN_OUTPUT as DEFAULT_LITERATURE_MARKDOWN_OUTPUT,
    EXPECTED_BLOCKERS,
    EXPECTED_FAMILIES,
)
from proof_obligation_blockers import DEFAULT_INPUT as DEFAULT_PROOF_GRAPH_JSON


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REPORT_DIR = ROOT / "track-a-regularity/reports"
DEFAULT_MARKDOWN_OUTPUT = DEFAULT_REPORT_DIR / "lemma_0252_blocker_literature_dependency.md"
DEFAULT_JSON_OUTPUT = DEFAULT_REPORT_DIR / "lemma_0252_blocker_literature_dependency.json"
DEFAULT_PAPERS_INDEX = ROOT / "papers/blockers/index.md"

NON_CLAIMS = (
    "read_only_literature_dependency_guard",
    "source_index_freshness_only",
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
class LiteratureDependencyCheck:
    key: str
    expected: str
    observed: str
    passed: bool
    source_artifacts: tuple[str, ...]


@dataclass(frozen=True)
class Lemma0252BlockerLiteratureDependency:
    schema_version: int
    lemma_id: str
    candidate_status: str
    active_candidate: bool
    literature_index_markdown: str
    literature_index_json: str
    proof_obligation_graph_json: str
    closure_dashboard_markdown: str
    closure_dashboard_json: str
    papers_index_markdown: str
    direct_source_report_count: int
    source_ref_count: int
    literature_dependency_check_count: int
    passed_literature_dependency_check_count: int
    failed_literature_dependency_check_count: int
    literature_dependency_consistent: bool
    literature_source_count: int
    pdf_count: int
    html_count: int
    search_log_count: int
    blocker_family_count: int
    substantive_blocker_count: int
    proof_promotion_blocker_count: int
    closure_verdict: str
    closure_unresolved_branch_count: int
    direct_discharge_source_count: int
    closure_discharged_blocker_count: int
    closure_direct_known_route_count: int
    process_gate_open_authorized: bool
    blocker_state_changed: bool
    candidate_emission_authorized: bool
    missing_source_count: int
    missing_sources: tuple[str, ...]
    issues: tuple[str, ...]
    checks: tuple[LiteratureDependencyCheck, ...]
    source_refs: tuple[str, ...]
    non_claims: tuple[str, ...]
    literature_snapshot: dict[str, object]
    proof_graph_snapshot: dict[str, object]
    closure_snapshot: dict[str, object]


def _load_json(path: Path) -> dict[str, object]:
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"expected object JSON report: {path}")
    return data


def _check(
    *,
    key: str,
    expected: object,
    observed: object,
    source_artifacts: tuple[str, ...],
) -> LiteratureDependencyCheck:
    return LiteratureDependencyCheck(
        key=key,
        expected=str(expected),
        observed=str(observed),
        passed=expected == observed,
        source_artifacts=source_artifacts,
    )


def _missing_sources(source_refs: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(source for source in source_refs if not (ROOT / source).exists())


def _literature_blocker_families(literature: dict[str, object]) -> tuple[str, ...]:
    families = literature.get("families", ())
    if not isinstance(families, list):
        raise ValueError("expected list field `families` in literature index")
    return tuple(
        str(family.get("blocker_family"))
        for family in families
        if isinstance(family, dict) and family.get("blocker_family") in EXPECTED_BLOCKERS
    )


def _proof_blocker_keys(proof_graph: dict[str, object]) -> tuple[str, ...]:
    blockers = proof_graph.get("promotion_blockers", ())
    if not isinstance(blockers, list):
        raise ValueError("expected list field `promotion_blockers` in proof graph")
    return tuple(
        str(blocker.get("key")) for blocker in blockers if isinstance(blocker, dict)
    )


def _proof_blocker_statuses(proof_graph: dict[str, object]) -> tuple[str, ...]:
    blockers = proof_graph.get("promotion_blockers", ())
    if not isinstance(blockers, list):
        raise ValueError("expected list field `promotion_blockers` in proof graph")
    return tuple(
        str(blocker.get("status")) for blocker in blockers if isinstance(blocker, dict)
    )


def _closure_branch_ids(closure: dict[str, object]) -> tuple[str, ...]:
    branches = closure.get("branch_closures", ())
    if not isinstance(branches, list):
        raise ValueError("expected list field `branch_closures` in closure dashboard")
    return tuple(
        str(branch.get("blocker_id")) for branch in branches if isinstance(branch, dict)
    )


def _papers_index_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def build_blocker_literature_dependency(
    *,
    literature_json: Path = DEFAULT_LITERATURE_JSON_OUTPUT,
    proof_graph_json: Path = DEFAULT_PROOF_GRAPH_JSON,
    closure_json: Path = DEFAULT_CLOSURE_JSON_OUTPUT,
    papers_index: Path = DEFAULT_PAPERS_INDEX,
) -> Lemma0252BlockerLiteratureDependency:
    literature = _load_json(literature_json)
    proof_graph = _load_json(proof_graph_json)
    closure = _load_json(closure_json)

    literature_source = (
        "track-a-regularity/reports/lemma_0252_blocker_literature_index.md",
        "track-a-regularity/reports/lemma_0252_blocker_literature_index.json",
    )
    proof_source = ("track-a-regularity/reports/lemma_0252_proof_obligation_graph.json",)
    closure_source = (
        "track-a-regularity/reports/lemma_0252_blocker_closure_dashboard.md",
        "track-a-regularity/reports/lemma_0252_blocker_closure_dashboard.json",
    )
    papers_source = ("papers/blockers/index.md",)
    direct_sources = literature_source + proof_source + closure_source + papers_source
    source_refs = tuple(
        dict.fromkeys(
            direct_sources
            + tuple(str(item) for item in literature.get("source_refs", ()))
            + tuple(str(item) for item in closure.get("source_refs", ()))
        )
    )
    missing_sources = _missing_sources(source_refs)

    literature_families = _literature_blocker_families(literature)
    proof_blockers = _proof_blocker_keys(proof_graph)
    proof_statuses = _proof_blocker_statuses(proof_graph)
    closure_branches = _closure_branch_ids(closure)
    papers_text = _papers_index_text(papers_index)
    papers_has_expected_families = all(family in papers_text for family in EXPECTED_FAMILIES)
    papers_mentions_inventory_count = "총 15개 자료" in papers_text or "15개 자료" in papers_text

    checks = (
        _check(
            key="literature.lemma_id.matches_proof_graph",
            expected=proof_graph.get("lemma_id"),
            observed=literature.get("lemma_id"),
            source_artifacts=literature_source + proof_source,
        ),
        _check(
            key="literature.lemma_id.matches_closure_dashboard",
            expected=closure.get("lemma_id"),
            observed=literature.get("lemma_id"),
            source_artifacts=literature_source + closure_source,
        ),
        _check(
            key="literature.candidate_status.matches_proof_graph",
            expected=proof_graph.get("candidate_status"),
            observed=literature.get("candidate_status"),
            source_artifacts=literature_source + proof_source,
        ),
        _check(
            key="literature.candidate_status.matches_closure_dashboard",
            expected=closure.get("candidate_status"),
            observed=literature.get("candidate_status"),
            source_artifacts=literature_source + closure_source,
        ),
        _check(
            key="literature.active_candidate.matches_proof_graph",
            expected=proof_graph.get("active_candidate"),
            observed=literature.get("active_candidate"),
            source_artifacts=literature_source + proof_source,
        ),
        _check(
            key="literature.active_candidate.matches_closure_dashboard",
            expected=closure.get("active_candidate"),
            observed=literature.get("active_candidate"),
            source_artifacts=literature_source + closure_source,
        ),
        _check(
            key="literature.substantive_blocker_count.matches_closure_dashboard",
            expected=closure.get("substantive_blocker_count"),
            observed=literature.get("substantive_blocker_count"),
            source_artifacts=literature_source + closure_source,
        ),
        _check(
            key="literature.blocker_families.match_proof_promotion_blockers",
            expected=proof_blockers,
            observed=literature_families,
            source_artifacts=literature_source + proof_source,
        ),
        _check(
            key="literature.blocker_families.match_closure_branches",
            expected=closure_branches,
            observed=literature_families,
            source_artifacts=literature_source + closure_source,
        ),
        _check(
            key="literature.literature_source_count.expected_fifteen",
            expected=15,
            observed=literature.get("literature_source_count"),
            source_artifacts=literature_source + papers_source,
        ),
        _check(
            key="literature.blocker_family_count.expected_four",
            expected=len(EXPECTED_FAMILIES),
            observed=literature.get("blocker_family_count"),
            source_artifacts=literature_source,
        ),
        _check(
            key="literature.source_index_check_count.expected_sixteen",
            expected=16,
            observed=literature.get("source_index_check_count"),
            source_artifacts=literature_source,
        ),
        _check(
            key="literature.failed_source_index_check_count.remains_zero",
            expected=0,
            observed=literature.get("failed_source_index_check_count"),
            source_artifacts=literature_source,
        ),
        _check(
            key="literature.source_index_consistent.true",
            expected=True,
            observed=literature.get("source_index_consistent"),
            source_artifacts=literature_source,
        ),
        _check(
            key="literature.missing_source_count.remains_zero",
            expected=0,
            observed=literature.get("missing_source_count"),
            source_artifacts=literature_source,
        ),
        _check(
            key="literature.missing_search_log_count.remains_zero",
            expected=0,
            observed=literature.get("missing_search_log_count"),
            source_artifacts=literature_source,
        ),
        _check(
            key="literature.direct_discharge_source_count.remains_zero",
            expected=0,
            observed=literature.get("direct_discharge_source_count"),
            source_artifacts=literature_source,
        ),
        _check(
            key="proof_graph.promotion_blocker_count.expected_three",
            expected=3,
            observed=len(proof_blockers),
            source_artifacts=proof_source,
        ),
        _check(
            key="proof_graph.promotion_blocker_statuses.expected_open",
            expected=("missing_mechanism", "missing_mechanism", "guardrail_only"),
            observed=proof_statuses,
            source_artifacts=proof_source,
        ),
        _check(
            key="closure.closure_verdict.blocked_no_discharge",
            expected="blocked_no_discharge",
            observed=closure.get("closure_verdict"),
            source_artifacts=closure_source,
        ),
        _check(
            key="closure.unresolved_branch_count.expected_three",
            expected=3,
            observed=closure.get("unresolved_branch_count"),
            source_artifacts=closure_source,
        ),
        _check(
            key="closure.discharged_blocker_count.remains_zero",
            expected=0,
            observed=closure.get("discharged_blocker_count"),
            source_artifacts=closure_source,
        ),
        _check(
            key="closure.direct_known_route_count.remains_zero",
            expected=0,
            observed=closure.get("direct_known_route_count"),
            source_artifacts=closure_source,
        ),
        _check(
            key="closure.direct_theorem_branch_count.remains_zero",
            expected=0,
            observed=closure.get("direct_theorem_branch_count"),
            source_artifacts=closure_source,
        ),
        _check(
            key="closure.candidate_emission_authorized.false",
            expected=False,
            observed=closure.get("candidate_emission_authorized"),
            source_artifacts=closure_source,
        ),
        _check(
            key="closure.checklist_presence_authorizes_candidate.false",
            expected=False,
            observed=closure.get("checklist_presence_authorizes_candidate"),
            source_artifacts=closure_source,
        ),
        _check(
            key="papers_index.exists",
            expected=True,
            observed=papers_index.exists(),
            source_artifacts=papers_source,
        ),
        _check(
            key="papers_index.references_expected_families",
            expected=True,
            observed=papers_has_expected_families,
            source_artifacts=papers_source,
        ),
        _check(
            key="papers_index.references_local_inventory_count",
            expected=True,
            observed=papers_mentions_inventory_count,
            source_artifacts=papers_source,
        ),
        _check(
            key="process_gate_open_authorized.false",
            expected=False,
            observed=literature.get("process_gate_open_authorized"),
            source_artifacts=literature_source,
        ),
        _check(
            key="blocker_state_changed.false",
            expected=False,
            observed=literature.get("blocker_state_changed"),
            source_artifacts=literature_source,
        ),
        _check(
            key="candidate_emission_authorized.all_false",
            expected=(False, False),
            observed=(
                literature.get("candidate_emission_authorized"),
                closure.get("candidate_emission_authorized"),
            ),
            source_artifacts=literature_source + closure_source,
        ),
        _check(
            key="source_refs.missing_count.remains_zero",
            expected=0,
            observed=len(missing_sources),
            source_artifacts=source_refs,
        ),
    )
    issues = tuple(check.key for check in checks if not check.passed)
    failed_count = len(issues)
    dependency_consistent = failed_count == 0 and not missing_sources

    return Lemma0252BlockerLiteratureDependency(
        schema_version=1,
        lemma_id=str(literature.get("lemma_id")),
        candidate_status=str(literature.get("candidate_status")),
        active_candidate=bool(literature.get("active_candidate")),
        literature_index_markdown=str(DEFAULT_LITERATURE_MARKDOWN_OUTPUT),
        literature_index_json=str(DEFAULT_LITERATURE_JSON_OUTPUT),
        proof_obligation_graph_json=str(DEFAULT_PROOF_GRAPH_JSON),
        closure_dashboard_markdown=str(DEFAULT_CLOSURE_MARKDOWN_OUTPUT),
        closure_dashboard_json=str(DEFAULT_CLOSURE_JSON_OUTPUT),
        papers_index_markdown=str(papers_index),
        direct_source_report_count=len(direct_sources),
        source_ref_count=len(source_refs),
        literature_dependency_check_count=len(checks),
        passed_literature_dependency_check_count=len(checks) - failed_count,
        failed_literature_dependency_check_count=failed_count,
        literature_dependency_consistent=dependency_consistent,
        literature_source_count=int(literature.get("literature_source_count", 0)),
        pdf_count=int(literature.get("pdf_count", 0)),
        html_count=int(literature.get("html_count", 0)),
        search_log_count=int(literature.get("search_log_count", 0)),
        blocker_family_count=int(literature.get("blocker_family_count", 0)),
        substantive_blocker_count=int(literature.get("substantive_blocker_count", 0)),
        proof_promotion_blocker_count=len(proof_blockers),
        closure_verdict=str(closure.get("closure_verdict")),
        closure_unresolved_branch_count=int(closure.get("unresolved_branch_count", 0)),
        direct_discharge_source_count=int(literature.get("direct_discharge_source_count", 0)),
        closure_discharged_blocker_count=int(closure.get("discharged_blocker_count", 0)),
        closure_direct_known_route_count=int(closure.get("direct_known_route_count", 0)),
        process_gate_open_authorized=bool(literature.get("process_gate_open_authorized")),
        blocker_state_changed=bool(literature.get("blocker_state_changed")),
        candidate_emission_authorized=(
            bool(literature.get("candidate_emission_authorized"))
            or bool(closure.get("candidate_emission_authorized"))
        ),
        missing_source_count=len(missing_sources),
        missing_sources=missing_sources,
        issues=issues,
        checks=checks,
        source_refs=source_refs,
        non_claims=NON_CLAIMS,
        literature_snapshot=literature,
        proof_graph_snapshot=proof_graph,
        closure_snapshot=closure,
    )


def literature_dependency_to_dict(
    report: Lemma0252BlockerLiteratureDependency,
) -> dict[str, object]:
    return {
        "schema_version": report.schema_version,
        "lemma_id": report.lemma_id,
        "candidate_status": report.candidate_status,
        "active_candidate": report.active_candidate,
        "literature_index_markdown": report.literature_index_markdown,
        "literature_index_json": report.literature_index_json,
        "proof_obligation_graph_json": report.proof_obligation_graph_json,
        "closure_dashboard_markdown": report.closure_dashboard_markdown,
        "closure_dashboard_json": report.closure_dashboard_json,
        "papers_index_markdown": report.papers_index_markdown,
        "direct_source_report_count": report.direct_source_report_count,
        "source_ref_count": report.source_ref_count,
        "literature_dependency_check_count": report.literature_dependency_check_count,
        "passed_literature_dependency_check_count": (
            report.passed_literature_dependency_check_count
        ),
        "failed_literature_dependency_check_count": (
            report.failed_literature_dependency_check_count
        ),
        "literature_dependency_consistent": report.literature_dependency_consistent,
        "literature_source_count": report.literature_source_count,
        "pdf_count": report.pdf_count,
        "html_count": report.html_count,
        "search_log_count": report.search_log_count,
        "blocker_family_count": report.blocker_family_count,
        "substantive_blocker_count": report.substantive_blocker_count,
        "proof_promotion_blocker_count": report.proof_promotion_blocker_count,
        "closure_verdict": report.closure_verdict,
        "closure_unresolved_branch_count": report.closure_unresolved_branch_count,
        "direct_discharge_source_count": report.direct_discharge_source_count,
        "closure_discharged_blocker_count": report.closure_discharged_blocker_count,
        "closure_direct_known_route_count": report.closure_direct_known_route_count,
        "process_gate_open_authorized": report.process_gate_open_authorized,
        "blocker_state_changed": report.blocker_state_changed,
        "candidate_emission_authorized": report.candidate_emission_authorized,
        "missing_source_count": report.missing_source_count,
        "missing_sources": list(report.missing_sources),
        "issues": list(report.issues),
        "checks": [asdict(check) for check in report.checks],
        "source_refs": list(report.source_refs),
        "non_claims": list(report.non_claims),
        "literature_snapshot": report.literature_snapshot,
        "proof_graph_snapshot": report.proof_graph_snapshot,
        "closure_snapshot": report.closure_snapshot,
        "docs": {
            "step_doc": "docs/STEP107_LEMMA_0252_BLOCKER_LITERATURE_DEPENDENCY.md",
            "literature_index_doc": "docs/STEP106_LEMMA_0252_BLOCKER_LITERATURE_INDEX.md",
            "closure_dashboard_doc": "docs/STEP91_BLOCKER_CLOSURE_DASHBOARD.md",
            "papers_index": "papers/blockers/index.md",
        },
    }


def _format(text: str) -> str:
    return text.replace("|", "\\|")


def _source_rows(report: Lemma0252BlockerLiteratureDependency) -> list[str]:
    return [
        "| source | path |",
        "|---|---|",
        f"| `literature_index_md` | `{report.literature_index_markdown}` |",
        f"| `literature_index_json` | `{report.literature_index_json}` |",
        f"| `proof_obligation_graph_json` | `{report.proof_obligation_graph_json}` |",
        f"| `closure_dashboard_md` | `{report.closure_dashboard_markdown}` |",
        f"| `closure_dashboard_json` | `{report.closure_dashboard_json}` |",
        f"| `papers_index_md` | `{report.papers_index_markdown}` |",
    ]


def _check_rows(report: Lemma0252BlockerLiteratureDependency) -> list[str]:
    rows = [
        "| check | expected | observed | passed | sources |",
        "|---|---|---|---|---|",
    ]
    for check in report.checks:
        sources = "<br>".join(f"`{source}`" for source in check.source_artifacts)
        rows.append(
            "| "
            f"`{check.key}` | "
            f"`{_format(check.expected)}` | "
            f"`{_format(check.observed)}` | "
            f"`{str(check.passed).lower()}` | "
            f"{sources} |"
        )
    return rows


def render_markdown(report: Lemma0252BlockerLiteratureDependency) -> str:
    return "\n".join(
        (
            "# Lemma 0252 Blocker Literature Dependency",
            "",
            "Generated by `track-a-regularity/evaluator/lemma_0252_blocker_literature_dependency.py`.",
            "",
            "This read-only guard keeps the Step 106 blocker-literature index tied to",
            "`papers/blockers/index.md`, the `lemma_0252` proof-obligation graph, and the",
            "Step 91 blocker-closure dashboard. It checks dependency drift only; it does",
            "not discharge a blocker, open a process gate, or authorize candidate emission.",
            "",
            "## Summary",
            "",
            f"- lemma_id: `{report.lemma_id}`",
            f"- candidate_status: `{report.candidate_status}`",
            f"- active_candidate: `{str(report.active_candidate).lower()}`",
            f"- direct_source_report_count: `{report.direct_source_report_count}`",
            f"- source_ref_count: `{report.source_ref_count}`",
            f"- literature_dependency_check_count: `{report.literature_dependency_check_count}`",
            f"- passed_literature_dependency_check_count: `{report.passed_literature_dependency_check_count}`",
            f"- failed_literature_dependency_check_count: `{report.failed_literature_dependency_check_count}`",
            f"- literature_dependency_consistent: `{str(report.literature_dependency_consistent).lower()}`",
            f"- literature_source_count: `{report.literature_source_count}`",
            f"- pdf_count: `{report.pdf_count}`",
            f"- html_count: `{report.html_count}`",
            f"- search_log_count: `{report.search_log_count}`",
            f"- blocker_family_count: `{report.blocker_family_count}`",
            f"- substantive_blocker_count: `{report.substantive_blocker_count}`",
            f"- proof_promotion_blocker_count: `{report.proof_promotion_blocker_count}`",
            f"- closure_verdict: `{report.closure_verdict}`",
            f"- closure_unresolved_branch_count: `{report.closure_unresolved_branch_count}`",
            f"- direct_discharge_source_count: `{report.direct_discharge_source_count}`",
            f"- closure_discharged_blocker_count: `{report.closure_discharged_blocker_count}`",
            f"- closure_direct_known_route_count: `{report.closure_direct_known_route_count}`",
            f"- process_gate_open_authorized: `{str(report.process_gate_open_authorized).lower()}`",
            f"- blocker_state_changed: `{str(report.blocker_state_changed).lower()}`",
            f"- candidate_emission_authorized: `{str(report.candidate_emission_authorized).lower()}`",
            f"- missing_source_count: `{report.missing_source_count}`",
            f"- issues: `{', '.join(report.issues) or 'none'}`",
            "",
            "## Direct Sources",
            "",
            *_source_rows(report),
            "",
            "## Checks",
            "",
            *_check_rows(report),
            "",
            "## Non-Claims",
            "",
            *(f"- `{item}`" for item in report.non_claims),
            "",
        )
    )


def render_json(report: Lemma0252BlockerLiteratureDependency) -> str:
    return json.dumps(
        literature_dependency_to_dict(report),
        indent=2,
        sort_keys=True,
    ) + "\n"


def render_output(
    report: Lemma0252BlockerLiteratureDependency,
    output_format: str,
) -> str:
    if output_format == "markdown":
        return render_markdown(report)
    if output_format == "json":
        return render_json(report)
    raise ValueError(f"unknown blocker literature dependency format: {output_format}")


def write_output(
    output: Path,
    report: Lemma0252BlockerLiteratureDependency,
    output_format: str,
) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_output(report, output_format), encoding="utf-8")
    return output


def check_output(
    output: Path,
    report: Lemma0252BlockerLiteratureDependency,
    output_format: str,
) -> tuple[bool, str]:
    expected = render_output(report, output_format)
    if not output.exists():
        return False, f"missing lemma_0252 blocker literature dependency: {output}"
    current = output.read_text(encoding="utf-8")
    if current != expected:
        return False, f"stale lemma_0252 blocker literature dependency: {output}"
    return True, f"fresh lemma_0252 blocker literature dependency: {output}"


def check_sources(report: Lemma0252BlockerLiteratureDependency) -> tuple[bool, str]:
    if report.missing_source_count:
        return False, "missing blocker literature dependency sources: " + ", ".join(
            report.missing_sources
        )
    return True, "all blocker literature dependency sources exist"


def check_consistent(report: Lemma0252BlockerLiteratureDependency) -> tuple[bool, str]:
    if not report.literature_dependency_consistent:
        return False, "blocker literature dependency inconsistent: " + ", ".join(
            report.issues
        )
    return True, "blocker literature dependency is consistent"


def check_blocked(report: Lemma0252BlockerLiteratureDependency) -> tuple[bool, str]:
    if report.process_gate_open_authorized:
        return False, "process gate open became authorized"
    if report.blocker_state_changed:
        return False, "blocker literature dependency changed blocker state"
    if report.candidate_emission_authorized:
        return False, "blocker literature dependency authorized candidate emission"
    if report.direct_discharge_source_count or report.closure_discharged_blocker_count:
        return False, "blocker literature dependency marked a discharge"
    if report.candidate_status != "needs_review" or report.active_candidate:
        return False, "lemma_0252 candidate state changed"
    return True, "blocker literature dependency keeps lemma_0252 blocked"


def default_output_path(output_format: str) -> Path:
    if output_format == "markdown":
        return DEFAULT_MARKDOWN_OUTPUT
    if output_format == "json":
        return DEFAULT_JSON_OUTPUT
    raise ValueError(f"unknown blocker literature dependency format: {output_format}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Guard the lemma_0252 blocker literature index against source drift."
    )
    parser.add_argument("--literature-json", type=Path, default=DEFAULT_LITERATURE_JSON_OUTPUT)
    parser.add_argument("--proof-graph-json", type=Path, default=DEFAULT_PROOF_GRAPH_JSON)
    parser.add_argument("--closure-json", type=Path, default=DEFAULT_CLOSURE_JSON_OUTPUT)
    parser.add_argument("--papers-index", type=Path, default=DEFAULT_PAPERS_INDEX)
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--check-output", action="store_true")
    parser.add_argument("--require-sources-exist", action="store_true")
    parser.add_argument("--require-consistent", action="store_true")
    parser.add_argument("--require-blocked", action="store_true")
    args = parser.parse_args(argv)

    try:
        report = build_blocker_literature_dependency(
            literature_json=args.literature_json,
            proof_graph_json=args.proof_graph_json,
            closure_json=args.closure_json,
            papers_index=args.papers_index,
        )
    except Exception as exc:  # noqa: BLE001 - CLI should report setup failures.
        print(f"failed to build lemma_0252 blocker literature dependency: {exc}", file=sys.stderr)
        return 1

    output = args.output or default_output_path(args.format)
    if args.check_output:
        ok, message = check_output(output, report, args.format)
        print(message)
        if not ok:
            print(
                "run without --check-output to regenerate the blocker literature dependency",
                file=sys.stderr,
            )
            return 1
    else:
        written = write_output(output, report, args.format)
        print(f"wrote {written}")

    if args.require_sources_exist:
        ok, message = check_sources(report)
        print(message)
        if not ok:
            return 1
    if args.require_consistent:
        ok, message = check_consistent(report)
        print(message)
        if not ok:
            return 1
    if args.require_blocked:
        ok, message = check_blocked(report)
        print(message)
        if not ok:
            return 1

    print(f"literature_dependency_check_count: {report.literature_dependency_check_count}")
    print(
        "failed_literature_dependency_check_count: "
        f"{report.failed_literature_dependency_check_count}"
    )
    print(
        "literature_dependency_consistent: "
        f"{str(report.literature_dependency_consistent).lower()}"
    )
    print(f"candidate_emission_authorized: {str(report.candidate_emission_authorized).lower()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
