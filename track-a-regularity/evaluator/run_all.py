from __future__ import annotations

import argparse
import sys
from pathlib import Path

from checks import (
    convex_integration,
    critical_space_known_results,
    definition_rules,
    duplicate_family,
    duhamel_formal_only,
    endpoint,
    flux_balance_risk,
    galilean,
    geometric_known_results,
    hypotheses,
    known_control_extensions,
    known_results,
    novelty,
    numerical,
    parabolic_morrey_obligation,
    pressure_proxy,
    scaling,
    solution_class,
)
from schema import CheckResult, EvaluationReport, LemmaCandidate, load_candidate


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CANDIDATES = ROOT / "track-a-regularity/candidates"
DEFAULT_LOG_DIR = ROOT / "track-a-regularity/eval_logs"


def evaluate(candidate: LemmaCandidate) -> EvaluationReport:
    results: list[CheckResult] = []
    for check in (
        scaling.check,
        galilean.check,
        numerical.check,
        known_results.check,
        novelty.check,
        hypotheses.check,
        endpoint.check,
        convex_integration.check,
        pressure_proxy.check,
        geometric_known_results.check,
        critical_space_known_results.check,
        definition_rules.check,
        flux_balance_risk.check,
        parabolic_morrey_obligation.check,
        duhamel_formal_only.check,
        known_control_extensions.check,
        duplicate_family.check,
        solution_class.check,
    ):
        result = check(candidate)
        results.append(result)
        if result.failed:
            break
    return EvaluationReport(candidate=candidate, results=tuple(results))


def _candidate_paths(inputs: list[Path]) -> list[Path]:
    if not inputs:
        inputs = [DEFAULT_CANDIDATES]
    paths: list[Path] = []
    for item in inputs:
        if item.is_dir():
            paths.extend(sorted(item.glob("lemma_*.yaml")))
        else:
            paths.append(item)
    return sorted(paths)


def render_report(report: EvaluationReport) -> str:
    lines = [
        f"# Evaluation {report.candidate.id}",
        "",
        f"- source: `{report.candidate.path}`",
        f"- candidate type: `{report.candidate.type}`",
        f"- final_status: `{report.final_status}`",
        f"- expected_status: `{report.expected_status}`",
        f"- expected_first_failure: `{report.expected_first_failure}`",
        f"- matches_expected: `{str(report.matches_expected).lower()}`",
        "",
        "## Checks",
        "",
        "| check | status | reason | evidence |",
        "|---|---|---|---|",
    ]
    for result in report.results:
        evidence = result.evidence if result.evidence else {}
        lines.append(f"| `{result.name}` | `{result.status}` | {result.reason} | `{evidence}` |")
    first = report.first_failure
    lines.extend(
        [
            "",
            "## First Failure",
            "",
            f"- `{first.name}`: {first.reason}" if first else "- none",
            "",
        ]
    )
    return "\n".join(lines)


def write_report(log_dir: Path, report: EvaluationReport) -> Path:
    log_dir.mkdir(parents=True, exist_ok=True)
    path = log_dir / f"{report.candidate.id}.log"
    path.write_text(render_report(report))
    return path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Evaluate Track A candidate lemmas.")
    parser.add_argument("inputs", nargs="*", type=Path, help="YAML file(s) or directories. Defaults to candidates/.")
    parser.add_argument("--log-dir", type=Path, default=DEFAULT_LOG_DIR)
    parser.add_argument("--check-expected", action="store_true", help="Return non-zero if seed expected results do not match.")
    args = parser.parse_args(argv)

    reports: list[EvaluationReport] = []
    for path in _candidate_paths(args.inputs):
        candidate = load_candidate(path)
        report = evaluate(candidate)
        reports.append(report)
        log_path = write_report(args.log_dir, report)
        first = report.first_failure.name if report.first_failure else "none"
        print(
            f"{candidate.id}: {report.final_status} first_failure={first} "
            f"matches_expected={report.matches_expected} log={log_path}"
        )

    if args.check_expected and any(not report.matches_expected for report in reports):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
