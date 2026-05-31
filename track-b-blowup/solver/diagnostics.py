"""Post-process Track B solver time series into vorticity/spectrum diagnostics.

This module does not advance the Navier-Stokes solver. It reads an existing
``timeseries.csv`` produced by ``validate_taylor_green.py`` or
``pseudospectral.py`` and writes compact diagnostics and plots.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_RUN_DIR = ROOT / "track-b-blowup/runs/TG_N64_t10"


@dataclass(frozen=True)
class DiagnosticSeries:
    t: np.ndarray
    energy: np.ndarray
    enstrophy: np.ndarray
    omega_l2_mean: np.ndarray
    omega_inf: np.ndarray
    div_max: np.ndarray
    spectrum_tail: np.ndarray
    enstrophy_growth_rate: np.ndarray
    omega_inf_growth_rate: np.ndarray


@dataclass(frozen=True)
class DiagnosticSummary:
    rows: int
    t_start: float
    t_end: float
    max_divergence: float
    energy_start: float
    energy_end: float
    enstrophy_start: float
    enstrophy_end: float
    omega_l2_mean_max: float
    omega_l2_mean_peak_t: float
    omega_inf_max: float
    omega_inf_peak_t: float
    spectrum_tail_max: float
    spectrum_tail_peak_t: float
    enstrophy_growth_rate_max: float
    enstrophy_growth_rate_peak_t: float


def _column(rows: list[dict[str, float]], key: str) -> np.ndarray:
    return np.asarray([row.get(key, math.nan) for row in rows], dtype=float)


def load_timeseries(path: Path) -> dict[str, np.ndarray]:
    rows: list[dict[str, float]] = []
    with path.open(newline="") as f:
        for row in csv.DictReader(f):
            rows.append({key: float(value) for key, value in row.items()})
    if not rows:
        raise ValueError(f"empty timeseries: {path}")
    return {
        "t": _column(rows, "t"),
        "energy": _column(rows, "energy"),
        "enstrophy": _column(rows, "enstrophy"),
        "omega_inf": _column(rows, "omega_inf"),
        "div_max": _column(rows, "div_max"),
        "spectrum_tail": _column(rows, "spectrum_tail"),
    }


def _growth_rate(values: np.ndarray, t: np.ndarray) -> np.ndarray:
    if len(values) < 2:
        return np.full_like(values, math.nan, dtype=float)
    return np.gradient(values, t)


def compute_diagnostics(raw: dict[str, np.ndarray]) -> DiagnosticSeries:
    t = raw["t"]
    enstrophy = raw["enstrophy"]
    omega_inf = raw["omega_inf"]
    return DiagnosticSeries(
        t=t,
        energy=raw["energy"],
        enstrophy=enstrophy,
        omega_l2_mean=np.sqrt(np.maximum(2.0 * enstrophy, 0.0)),
        omega_inf=omega_inf,
        div_max=raw["div_max"],
        spectrum_tail=raw["spectrum_tail"],
        enstrophy_growth_rate=_growth_rate(enstrophy, t),
        omega_inf_growth_rate=_growth_rate(omega_inf, t),
    )


def _peak(values: np.ndarray, t: np.ndarray) -> tuple[float, float]:
    idx = int(np.nanargmax(values))
    return float(values[idx]), float(t[idx])


def summarize(series: DiagnosticSeries) -> DiagnosticSummary:
    omega_l2_max, omega_l2_t = _peak(series.omega_l2_mean, series.t)
    omega_inf_max, omega_inf_t = _peak(series.omega_inf, series.t)
    tail_max, tail_t = _peak(series.spectrum_tail, series.t)
    enstrophy_growth_max, enstrophy_growth_t = _peak(series.enstrophy_growth_rate, series.t)
    return DiagnosticSummary(
        rows=int(len(series.t)),
        t_start=float(series.t[0]),
        t_end=float(series.t[-1]),
        max_divergence=float(np.nanmax(series.div_max)),
        energy_start=float(series.energy[0]),
        energy_end=float(series.energy[-1]),
        enstrophy_start=float(series.enstrophy[0]),
        enstrophy_end=float(series.enstrophy[-1]),
        omega_l2_mean_max=omega_l2_max,
        omega_l2_mean_peak_t=omega_l2_t,
        omega_inf_max=omega_inf_max,
        omega_inf_peak_t=omega_inf_t,
        spectrum_tail_max=tail_max,
        spectrum_tail_peak_t=tail_t,
        enstrophy_growth_rate_max=enstrophy_growth_max,
        enstrophy_growth_rate_peak_t=enstrophy_growth_t,
    )


def write_diagnostics_csv(path: Path, series: DiagnosticSeries) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "t",
        "energy",
        "enstrophy",
        "omega_l2_mean",
        "omega_inf",
        "div_max",
        "spectrum_tail",
        "enstrophy_growth_rate",
        "omega_inf_growth_rate",
    ]
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for i, t in enumerate(series.t):
            writer.writerow(
                {
                    "t": float(t),
                    "energy": float(series.energy[i]),
                    "enstrophy": float(series.enstrophy[i]),
                    "omega_l2_mean": float(series.omega_l2_mean[i]),
                    "omega_inf": float(series.omega_inf[i]),
                    "div_max": float(series.div_max[i]),
                    "spectrum_tail": float(series.spectrum_tail[i]),
                    "enstrophy_growth_rate": float(series.enstrophy_growth_rate[i]),
                    "omega_inf_growth_rate": float(series.omega_inf_growth_rate[i]),
                }
            )


def write_plots(plot_dir: Path, series: DiagnosticSeries) -> list[Path]:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plot_dir.mkdir(parents=True, exist_ok=True)
    made: list[Path] = []

    def finish(path: Path, ylabel: str) -> None:
        plt.xlabel("t")
        plt.ylabel(ylabel)
        plt.grid(True, alpha=0.25)
        plt.tight_layout()
        plt.savefig(path, dpi=160)
        plt.close()
        made.append(path)

    plt.figure(figsize=(8, 5))
    plt.plot(series.t, series.enstrophy, label="enstrophy")
    plt.plot(series.t, series.omega_l2_mean, label="omega_l2_mean")
    plt.legend()
    finish(plot_dir / "enstrophy.png", "volume-normalized value")

    plt.figure(figsize=(8, 5))
    plt.plot(series.t, series.omega_inf, label="omega_inf")
    plt.legend()
    finish(plot_dir / "omega_inf.png", "max |omega|")

    plt.figure(figsize=(8, 5))
    plt.plot(series.t, series.spectrum_tail, label="spectrum_tail")
    plt.legend()
    finish(plot_dir / "spectrum.png", "tail energy fraction")

    return made


def write_readme(run_dir: Path, summary: DiagnosticSummary, plots: list[Path]) -> None:
    rel_plots = [path.relative_to(ROOT) for path in plots]
    lines = [
        "# Step 7 Diagnostics",
        "",
        "Generated from an existing solver `timeseries.csv`; no solver rerun was performed.",
        "",
        "## Summary",
        "",
        f"- t range: `{summary.t_start:g}` to `{summary.t_end:g}`",
        f"- max divergence: `{summary.max_divergence:.3e}`",
        f"- energy: `{summary.energy_start:.10g}` -> `{summary.energy_end:.10g}`",
        f"- enstrophy: `{summary.enstrophy_start:.10g}` -> `{summary.enstrophy_end:.10g}`",
        f"- peak omega_l2_mean: `{summary.omega_l2_mean_max:.10g}` at `t={summary.omega_l2_mean_peak_t:g}`",
        f"- peak omega_inf: `{summary.omega_inf_max:.10g}` at `t={summary.omega_inf_peak_t:g}`",
        f"- max spectrum tail: `{summary.spectrum_tail_max:.10g}` at `t={summary.spectrum_tail_peak_t:g}`",
        f"- max enstrophy growth rate: `{summary.enstrophy_growth_rate_max:.10g}` at `t={summary.enstrophy_growth_rate_peak_t:g}`",
        "",
        "## Outputs",
        "",
        "- `diagnostics.csv`",
        "- `diagnostics_summary.json`",
    ]
    lines.extend(f"- `{plot}`" for plot in rel_plots)
    lines.append("")
    (run_dir / "STEP7_DIAGNOSTICS.md").write_text("\n".join(lines), encoding="utf-8")


def run(run_dir: Path, csv_name: str = "timeseries.csv") -> dict[str, object]:
    run_dir = run_dir.resolve()
    timeseries = run_dir / csv_name
    raw = load_timeseries(timeseries)
    series = compute_diagnostics(raw)
    summary = summarize(series)
    write_diagnostics_csv(run_dir / "diagnostics.csv", series)
    (run_dir / "diagnostics_summary.json").write_text(
        json.dumps(asdict(summary), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    plots = write_plots(run_dir / "plots", series)
    write_readme(run_dir, summary, plots)
    return {
        "run_dir": str(run_dir),
        "timeseries": str(timeseries),
        "diagnostics_csv": str(run_dir / "diagnostics.csv"),
        "summary_json": str(run_dir / "diagnostics_summary.json"),
        "plots": [str(path) for path in plots],
        "summary": asdict(summary),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", type=Path, default=DEFAULT_RUN_DIR)
    parser.add_argument("--csv-name", default="timeseries.csv")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print(json.dumps(run(args.run_dir, args.csv_name), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
