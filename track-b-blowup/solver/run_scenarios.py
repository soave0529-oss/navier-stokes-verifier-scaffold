"""Run bounded Track B Kida and Hou-Luo-inspired scenario diagnostics."""

from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import asdict
from pathlib import Path

import numpy as np

THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from diagnostics import compute_diagnostics, load_timeseries, summarize, write_diagnostics_csv, write_plots
from initial_conditions import anti_parallel_vortex_tubes_initial, kida_pelz_initial
from pseudospectral import PseudoSpectralNSE, SolverConfig, write_csv


ROOT = THIS_DIR.parents[1]
SCENARIOS = {
    "kida": kida_pelz_initial,
    "houluo": anti_parallel_vortex_tubes_initial,
}


def _summary_dict(summary: object) -> dict[str, object]:
    return asdict(summary)


def run_one(
    scenario: str,
    out_dir: Path,
    cfg: SolverConfig,
    sample_every: int,
    amplitude: float,
) -> dict[str, object]:
    if scenario not in SCENARIOS:
        raise ValueError(f"unknown scenario: {scenario}")
    out_dir = out_dir.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    start = time.perf_counter()
    u0 = SCENARIOS[scenario](cfg.n, amplitude=amplitude)
    solver = PseudoSpectralNSE(cfg)
    _, rows = solver.run(u0, sample_every=sample_every)
    elapsed = time.perf_counter() - start

    write_csv(out_dir / "timeseries.csv", rows)
    raw = load_timeseries(out_dir / "timeseries.csv")
    series = compute_diagnostics(raw)
    diag_summary = summarize(series)
    write_diagnostics_csv(out_dir / "diagnostics.csv", series)
    plots = write_plots(out_dir / "plots", series)

    report = {
        "scenario": scenario,
        "n": cfg.n,
        "nu": cfg.nu,
        "dt": cfg.dt,
        "t_end": cfg.t_end,
        "sample_every": sample_every,
        "integrator": cfg.integrator,
        "amplitude": amplitude,
        "elapsed_seconds": elapsed,
        "diagnostics": _summary_dict(diag_summary),
        "pass_divergence": bool(diag_summary.max_divergence < 1.0e-10),
        "not_blowup_evidence": True,
    }
    (out_dir / "config.json").write_text(json.dumps({**asdict(cfg), "sample_every": sample_every, "amplitude": amplitude}, indent=2, sort_keys=True) + "\n")
    (out_dir / "summary.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    _write_readme(out_dir, report, plots)
    return report


def _write_readme(out_dir: Path, report: dict[str, object], plots: list[Path]) -> None:
    diagnostics = report["diagnostics"]
    assert isinstance(diagnostics, dict)
    rel_plots = [path.relative_to(ROOT) for path in plots]
    lines = [
        f"# {report['scenario']} Scenario",
        "",
        "Bounded diagnostic pseudo-spectral run. This is a scenario substrate for",
        "Track B and Track A falsification, not evidence of Navier-Stokes blow-up.",
        "",
        "## Config",
        "",
        f"- N: `{report['n']}`",
        f"- nu: `{report['nu']}`",
        f"- dt: `{report['dt']}`",
        f"- t_end: `{report['t_end']}`",
        f"- integrator: `{report['integrator']}`",
        "",
        "## Diagnostics",
        "",
        f"- max divergence: `{diagnostics['max_divergence']:.3e}`",
        f"- energy: `{diagnostics['energy_start']:.10g}` -> `{diagnostics['energy_end']:.10g}`",
        f"- enstrophy: `{diagnostics['enstrophy_start']:.10g}` -> `{diagnostics['enstrophy_end']:.10g}`",
        f"- peak omega_inf: `{diagnostics['omega_inf_max']:.10g}` at `t={diagnostics['omega_inf_peak_t']:g}`",
        f"- max spectrum tail: `{diagnostics['spectrum_tail_max']:.10g}` at `t={diagnostics['spectrum_tail_peak_t']:g}`",
        "",
        "## Outputs",
        "",
        "- `timeseries.csv`",
        "- `diagnostics.csv`",
        "- `summary.json`",
        *[f"- `{path}`" for path in rel_plots],
        "",
    ]
    out_dir.joinpath("README.md").write_text("\n".join(lines))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scenario", choices=["kida", "houluo", "all"], default="all")
    parser.add_argument("--n", type=int, default=24)
    parser.add_argument("--nu", type=float, default=1.0e-3)
    parser.add_argument("--dt", type=float, default=0.0025)
    parser.add_argument("--t-end", type=float, default=0.2)
    parser.add_argument("--sample-every", type=int, default=5)
    parser.add_argument("--integrator", choices=["rk4", "ifrk4"], default="ifrk4")
    parser.add_argument("--amplitude", type=float, default=1.0)
    parser.add_argument("--out-root", type=Path, default=ROOT / "track-b-blowup/runs")
    parser.add_argument("--suffix", default="20260519")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cfg = SolverConfig(n=args.n, nu=args.nu, dt=args.dt, t_end=args.t_end, integrator=args.integrator)
    scenarios = ("kida", "houluo") if args.scenario == "all" else (args.scenario,)
    reports = []
    for scenario in scenarios:
        out_dir = args.out_root / f"{scenario}_{args.suffix}"
        reports.append(run_one(scenario, out_dir, cfg, args.sample_every, args.amplitude))
    print(json.dumps(reports, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

