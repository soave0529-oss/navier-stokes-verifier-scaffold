"""Run cheap dyadic LES-flux diagnostics on Taylor-Green data.

This is a Track B diagnostic harness for candidate falsification and scale
vocabulary. It is not evidence for Navier-Stokes regularity or blow-up.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
import time
from dataclasses import asdict
from pathlib import Path


THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from dyadic_flux import DyadicFluxRow, flux_row
from pseudospectral import PseudoSpectralNSE, SolverConfig, taylor_green_initial


ROOT = THIS_DIR.parents[1]


def parse_cutoffs(raw: str) -> tuple[int, ...]:
    cutoffs = tuple(int(part.strip()) for part in raw.split(",") if part.strip())
    if not cutoffs:
        raise argparse.ArgumentTypeError("at least one cutoff is required")
    if any(cutoff <= 0 for cutoff in cutoffs):
        raise argparse.ArgumentTypeError("cutoffs must be positive integers")
    return cutoffs


def write_flux_csv(path: Path, rows: list[DyadicFluxRow]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "step",
                "t",
                "cutoff",
                "pi_les",
                "positive_flux",
                "normalized_positive_flux",
            ],
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))


def summarize(rows: list[DyadicFluxRow]) -> dict[str, dict[str, float]]:
    out: dict[str, dict[str, float]] = {}
    for cutoff in sorted({row.cutoff for row in rows}):
        subset = [row for row in rows if row.cutoff == cutoff]
        peak_positive = max(subset, key=lambda row: row.positive_flux)
        peak_normalized = max(subset, key=lambda row: row.normalized_positive_flux)
        out[str(cutoff)] = {
            "samples": float(len(subset)),
            "max_abs_pi_les": max(abs(row.pi_les) for row in subset),
            "max_positive_flux": peak_positive.positive_flux,
            "max_positive_flux_t": peak_positive.t,
            "max_normalized_positive_flux": peak_normalized.normalized_positive_flux,
            "max_normalized_positive_flux_t": peak_normalized.t,
            "final_pi_les": subset[-1].pi_les,
            "final_normalized_positive_flux": subset[-1].normalized_positive_flux,
        }
    return out


def run(out_dir: Path, cfg: SolverConfig, sample_every: int, cutoffs: tuple[int, ...], alpha: float) -> dict[str, object]:
    out_dir = out_dir.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    start = time.perf_counter()
    solver = PseudoSpectralNSE(cfg)
    u_hat = solver.project(solver.fft(taylor_green_initial(cfg.n)))
    steps = int(round(cfg.t_end / cfg.dt))
    rows: list[DyadicFluxRow] = []

    for step in range(steps + 1):
        t = step * cfg.dt
        if step % sample_every == 0 or step == steps:
            for cutoff in cutoffs:
                rows.append(flux_row(solver, step=step, t=t, u_hat=u_hat, cutoff=cutoff, alpha=alpha))
        if step < steps:
            u_hat = solver.step(u_hat)

    final_diag = solver.diagnostics(steps, steps * cfg.dt, u_hat)
    elapsed = time.perf_counter() - start

    write_flux_csv(out_dir / "dyadic_flux.csv", rows)
    report = {
        "n": cfg.n,
        "nu": cfg.nu,
        "dt": cfg.dt,
        "t_end": cfg.t_end,
        "sample_every": sample_every,
        "integrator": cfg.integrator,
        "cutoffs": list(cutoffs),
        "alpha": alpha,
        "elapsed_seconds": elapsed,
        "final_divergence": final_diag.div_max,
        "final_energy": final_diag.energy,
        "final_enstrophy": final_diag.enstrophy,
        "flux_summary": summarize(rows),
        "mean_normalized": True,
        "sharp_radial_low_pass": True,
        "not_proof_evidence": True,
    }
    (out_dir / "config.json").write_text(json.dumps({**asdict(cfg), "sample_every": sample_every, "cutoffs": list(cutoffs), "alpha": alpha}, indent=2, sort_keys=True) + "\n")
    (out_dir / "summary.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    write_readme(out_dir, report)
    return report


def write_readme(out_dir: Path, report: dict[str, object]) -> None:
    summary = report["flux_summary"]
    assert isinstance(summary, dict)
    lines = [
        "# Dyadic LES-Flux Smoke Diagnostic",
        "",
        "Cheap Taylor-Green diagnostic for the exact `Pi_N^LES` candidate vocabulary.",
        "This is a Track B falsifier/support artifact, not a proof ingredient.",
        "",
        "## Config",
        "",
        f"- N: `{report['n']}`",
        f"- nu: `{report['nu']}`",
        f"- dt: `{report['dt']}`",
        f"- t_end: `{report['t_end']}`",
        f"- integrator: `{report['integrator']}`",
        f"- alpha: `{report['alpha']}`",
        f"- cutoffs: `{report['cutoffs']}`",
        "- flux convention: mean-normalized sharp radial low-pass approximation of `Pi_N^LES`",
        "",
        "## Diagnostics",
        "",
        f"- final divergence: `{report['final_divergence']:.3e}`",
        f"- final energy: `{report['final_energy']:.10g}`",
        f"- final enstrophy: `{report['final_enstrophy']:.10g}`",
        "",
        "## Flux Peaks",
        "",
    ]
    for cutoff, row in summary.items():
        assert isinstance(row, dict)
        lines.extend(
            [
                f"### cutoff {cutoff}",
                "",
                f"- max abs Pi: `{row['max_abs_pi_les']:.10g}`",
                f"- max positive flux: `{row['max_positive_flux']:.10g}` at `t={row['max_positive_flux_t']:g}`",
                f"- max normalized positive flux: `{row['max_normalized_positive_flux']:.10g}` at `t={row['max_normalized_positive_flux_t']:g}`",
                "",
            ]
        )
    lines.extend(
        [
            "## Outputs",
            "",
            "- `dyadic_flux.csv`",
            "- `summary.json`",
            "- `config.json`",
            "",
        ]
    )
    out_dir.joinpath("README.md").write_text("\n".join(lines))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n", type=int, default=16)
    parser.add_argument("--nu", type=float, default=1.0e-3)
    parser.add_argument("--dt", type=float, default=0.005)
    parser.add_argument("--t-end", type=float, default=0.05)
    parser.add_argument("--sample-every", type=int, default=5)
    parser.add_argument("--integrator", choices=["rk4", "ifrk4"], default="ifrk4")
    parser.add_argument("--cutoffs", type=parse_cutoffs, default=parse_cutoffs("2,4"))
    parser.add_argument("--alpha", type=float, default=1.0)
    parser.add_argument("--out-dir", type=Path, default=ROOT / "track-b-blowup/runs/dyadic_flux_smoke_20260519")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cfg = SolverConfig(n=args.n, nu=args.nu, dt=args.dt, t_end=args.t_end, integrator=args.integrator)
    report = run(args.out_dir, cfg, args.sample_every, args.cutoffs, args.alpha)
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
