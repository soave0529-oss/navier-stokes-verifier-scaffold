"""Bounded interval-style falsifier for Track B diagnostic inequalities."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Callable

import mpmath as mp


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OUT_DIR = ROOT / "track-b-blowup/solver/interval/results"


@dataclass(frozen=True)
class InequalityResult:
    id: str
    description: str
    relation: str
    lhs_interval: tuple[float, float]
    rhs_interval: tuple[float, float]
    status: str
    evidence: dict[str, Any]


def iv(value: float, rel_radius: float = 1.0e-12, abs_radius: float = 1.0e-18) -> Any:
    radius = max(abs(value) * rel_radius, abs_radius)
    return mp.iv.mpf([value - radius, value + radius])


def endpoints(value: Any) -> tuple[float, float]:
    return float(value.a), float(value.b)


def interval_le(lhs: Any, rhs: Any) -> str:
    lhs_a, lhs_b = endpoints(lhs)
    rhs_a, rhs_b = endpoints(rhs)
    if lhs_b <= rhs_a:
        return "pass"
    if lhs_a > rhs_b:
        return "fail"
    return "unknown"


def interval_gt(lhs: Any, rhs: Any) -> str:
    lhs_a, lhs_b = endpoints(lhs)
    rhs_a, rhs_b = endpoints(rhs)
    if lhs_a > rhs_b:
        return "pass"
    if lhs_b <= rhs_a:
        return "fail"
    return "unknown"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def _diag(summary: dict[str, Any], key: str) -> float:
    diagnostics = summary.get("diagnostics")
    if isinstance(diagnostics, dict) and key in diagnostics:
        return float(diagnostics[key])
    return float(summary[key])


def evaluate_default_inequalities(root: Path = ROOT) -> list[InequalityResult]:
    tg = load_json(root / "track-b-blowup/runs/TG_N64_t10/diagnostics_summary.json")
    tao = load_json(root / "track-b-blowup/runs/tao_truncated_cascade_20260519/summary.json")
    kida = load_json(root / "track-b-blowup/runs/kida_20260519/summary.json")
    houluo = load_json(root / "track-b-blowup/runs/houluo_20260519/summary.json")

    specs: list[tuple[str, str, str, Any, Any, Callable[[Any, Any], str], dict[str, Any]]] = [
        (
            "ineq_0001_tg_divergence_small",
            "Taylor-Green diagnostic divergence stays below 1e-10.",
            "<=",
            iv(float(tg["max_divergence"])),
            iv(1.0e-10),
            interval_le,
            {"source": "TG_N64_t10/diagnostics_summary.json"},
        ),
        (
            "ineq_0002_bad_tg_tail_le_005",
            "False control: Taylor-Green spectrum tail remains <= 0.05.",
            "<=",
            iv(float(tg["spectrum_tail_max"])),
            iv(0.05),
            interval_le,
            {"source": "TG_N64_t10/diagnostics_summary.json"},
        ),
        (
            "ineq_0003_tao_proxy_weighted_growth",
            "Tao cascade proxy weighted high-mode amplitude grows by more than 1.",
            ">",
            iv(float(tao["weighted_receiver_growth"])),
            iv(1.0),
            interval_gt,
            {"source": "tao_truncated_cascade_20260519/summary.json", "not_true_nse": True},
        ),
        (
            "ineq_0004_bad_kida_enstrophy_nonincreasing",
            "False control: Kida scenario enstrophy is nonincreasing over the cheap run.",
            "<=",
            iv(_diag(kida, "enstrophy_end")),
            iv(_diag(kida, "enstrophy_start")),
            interval_le,
            {"source": "kida_20260519/summary.json"},
        ),
        (
            "ineq_0005_houluo_energy_nonincreasing",
            "Hou-Luo-inspired scenario energy is nonincreasing over the cheap run.",
            "<=",
            iv(_diag(houluo, "energy_end")),
            iv(_diag(houluo, "energy_start")),
            interval_le,
            {"source": "houluo_20260519/summary.json"},
        ),
    ]

    results: list[InequalityResult] = []
    for ident, description, relation, lhs, rhs, predicate, evidence in specs:
        results.append(
            InequalityResult(
                id=ident,
                description=description,
                relation=relation,
                lhs_interval=endpoints(lhs),
                rhs_interval=endpoints(rhs),
                status=predicate(lhs, rhs),
                evidence=evidence,
            )
        )
    return results


def write_outputs(results: list[InequalityResult], out_dir: Path) -> dict[str, str]:
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / "inequalities_20260519.json"
    md_path = out_dir / "inequalities_20260519.md"
    json_path.write_text(json.dumps([asdict(result) for result in results], indent=2, sort_keys=True) + "\n")
    lines = [
        "# Step 15 Interval Falsifier Results",
        "",
        "All values are wrapped in narrow intervals before comparison. `unknown` means",
        "interval overlap, not mathematical truth.",
        "",
        "| id | relation | status | lhs interval | rhs interval | description |",
        "|---|---|---|---|---|---|",
    ]
    for result in results:
        lines.append(
            f"| `{result.id}` | `{result.relation}` | `{result.status}` | "
            f"`{result.lhs_interval}` | `{result.rhs_interval}` | {result.description} |"
        )
    lines.append("")
    md_path.write_text("\n".join(lines))
    return {"json": str(json_path), "markdown": str(md_path)}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    results = evaluate_default_inequalities()
    outputs = write_outputs(results, args.out_dir)
    print(json.dumps({"outputs": outputs, "results": [asdict(result) for result in results]}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

