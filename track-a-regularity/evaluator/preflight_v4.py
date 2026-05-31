from __future__ import annotations

import argparse
import sys
from pathlib import Path

from generation_spec_v4 import assess_candidate
from schema import LemmaCandidate, load_candidate


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CANDIDATES = ROOT / "track-a-regularity/candidates"


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


def _should_check(candidate: LemmaCandidate, include_all: bool) -> bool:
    if include_all:
        return True
    return candidate.expected_evaluator.get("status") == "candidate"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run the v4 emit-ready preflight on proposed Track A candidates."
    )
    parser.add_argument("inputs", nargs="*", type=Path, help="YAML file(s) or directories. Defaults to candidates/.")
    parser.add_argument(
        "--all",
        action="store_true",
        help="Assess every YAML, including known controls and manual-review records.",
    )
    args = parser.parse_args(argv)

    checked = 0
    skipped = 0
    blocked = 0

    for path in _candidate_paths(args.inputs):
        candidate = load_candidate(path)
        if not _should_check(candidate, args.all):
            skipped += 1
            continue

        checked += 1
        assessment = assess_candidate(candidate)
        status = "ready" if assessment.emit_ready else "blocked"
        print(f"{candidate.id}: {status} source={path}")
        for reason in assessment.reasons:
            print(f"  - {reason}")
        if not assessment.emit_ready:
            blocked += 1

    print(f"summary: checked={checked} skipped={skipped} blocked={blocked}")
    return 1 if blocked else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
