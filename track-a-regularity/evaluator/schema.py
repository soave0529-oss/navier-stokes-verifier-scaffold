from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


REQUIRED_FIELDS = {
    "id",
    "generated_by",
    "date",
    "statement_en",
    "statement_lean_skel",
    "type",
    "related_known",
    "evaluator",
    "expected_evaluator",
    "status",
}


@dataclass(frozen=True)
class LemmaCandidate:
    id: str
    generated_by: str
    date: str
    statement_en: str
    statement_lean_skel: str
    type: str
    related_known: tuple[str, ...]
    evaluator: dict[str, str]
    expected_evaluator: dict[str, Any]
    status: str
    why_interesting: str = ""
    path: Path | None = None

    @property
    def normalized_text(self) -> str:
        return " ".join(
            [
                self.id,
                self.type,
                self.statement_en,
                self.statement_lean_skel,
                self.why_interesting,
                " ".join(self.related_known),
            ]
        ).lower()


@dataclass(frozen=True)
class CheckResult:
    name: str
    status: str
    reason: str
    evidence: dict[str, Any] = field(default_factory=dict)

    @property
    def failed(self) -> bool:
        return self.status == "fail"


@dataclass(frozen=True)
class EvaluationReport:
    candidate: LemmaCandidate
    results: tuple[CheckResult, ...]

    @property
    def final_status(self) -> str:
        if self.first_failure is not None:
            return "falsified"
        if any(result.status == "known_control_with_extra_assumption" for result in self.results):
            return "known_control_with_extra_assumption"
        if any(result.status == "known_control" for result in self.results):
            return "known_control"
        if any(result.status == "review" for result in self.results):
            return "needs_review"
        return "candidate"

    @property
    def first_failure(self) -> CheckResult | None:
        for result in self.results:
            if result.failed:
                return result
        return None

    @property
    def expected_status(self) -> str | None:
        value = self.candidate.expected_evaluator.get("status")
        return str(value) if value is not None else None

    @property
    def expected_first_failure(self) -> str | None:
        value = self.candidate.expected_evaluator.get("first_expected_failure")
        return str(value) if value is not None else None

    @property
    def matches_expected(self) -> bool:
        passing_statuses = {
            "candidate",
            "known_control",
            "known_control_with_extra_assumption",
            "needs_review",
        }
        exact_statuses = passing_statuses | {"falsified"}
        if self.expected_status == "pass" and self.final_status not in passing_statuses:
            return False
        if self.expected_status == "fail" and self.final_status != "falsified":
            return False
        if self.expected_status in exact_statuses and self.final_status != self.expected_status:
            return False
        expected_first = self.expected_first_failure
        if expected_first:
            first_failure = self.first_failure.name if self.first_failure else None
            return first_failure == expected_first
        return True


def load_candidate(path: Path) -> LemmaCandidate:
    raw = yaml.safe_load(path.read_text()) or {}
    if not isinstance(raw, dict):
        raise ValueError(f"{path}: YAML root must be a mapping")
    missing = REQUIRED_FIELDS - set(raw)
    if missing:
        raise ValueError(f"{path}: missing required fields: {sorted(missing)}")

    related_known = raw["related_known"]
    if not isinstance(related_known, list) or not all(isinstance(item, str) for item in related_known):
        raise ValueError(f"{path}: related_known must be a list of strings")

    evaluator = raw["evaluator"]
    if not isinstance(evaluator, dict):
        raise ValueError(f"{path}: evaluator must be a mapping")

    expected = raw["expected_evaluator"]
    if not isinstance(expected, dict):
        raise ValueError(f"{path}: expected_evaluator must be a mapping")

    return LemmaCandidate(
        id=str(raw["id"]),
        generated_by=str(raw["generated_by"]),
        date=str(raw["date"]),
        statement_en=str(raw["statement_en"]),
        statement_lean_skel=str(raw["statement_lean_skel"]),
        type=str(raw["type"]),
        related_known=tuple(related_known),
        evaluator={str(key): str(value) for key, value in evaluator.items()},
        expected_evaluator=expected,
        status=str(raw["status"]),
        why_interesting=str(raw.get("why_interesting", "")),
        path=path,
    )


def load_candidates(paths: list[Path]) -> list[LemmaCandidate]:
    return [load_candidate(path) for path in sorted(paths)]
