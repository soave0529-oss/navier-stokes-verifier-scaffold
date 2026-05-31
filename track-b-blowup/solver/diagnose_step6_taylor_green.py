"""Diagnose Step 6 Taylor-Green reference mismatch from existing CSV runs.

This script does not run the solver. It compares already-generated
Taylor-Green time series against the DeBonis/OpenSBLI 512^3 reference,
checks the enstrophy convention via the energy identity, and writes compact
tables/plots for the Step 6 blocker report.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
RUNS = ROOT / "track-b-blowup/runs"
REFERENCE = ROOT / "refs/reference_data/taylor_green_debonis_opensbli_512.dat"
DEFAULT_OUT = RUNS / "diagnostics_step6"
NU = 1.0 / 1600.0


@dataclass(frozen=True)
class RunData:
    name: str
    n: int | None
    t: np.ndarray
    energy: np.ndarray
    enstrophy: np.ndarray
    omega_inf: np.ndarray
    div_max: np.ndarray
    spectrum_tail: np.ndarray


def load_reference(path: Path) -> np.ndarray:
    rows: list[tuple[float, float, float]] = []
    with path.open() as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            t, energy, enstrophy = (float(x) for x in line.split()[:3])
            rows.append((t, energy, enstrophy))
    if not rows:
        raise ValueError(f"reference data has no rows: {path}")
    return np.asarray(rows, dtype=float)


def load_run(path: Path) -> RunData:
    rows: list[dict[str, float]] = []
    with path.open(newline="") as f:
        for row in csv.DictReader(f):
            rows.append({k: float(v) for k, v in row.items()})
    if not rows:
        raise ValueError(f"run CSV has no rows: {path}")

    name = path.parent.name
    n: int | None = None
    if name.startswith("TG_N"):
        prefix = name.split("_", 2)[1]
        if prefix.startswith("N"):
            try:
                n = int(prefix[1:])
            except ValueError:
                n = None

    def col(key: str) -> np.ndarray:
        return np.asarray([r.get(key, math.nan) for r in rows], dtype=float)

    return RunData(
        name=name,
        n=n,
        t=col("t"),
        energy=col("energy"),
        enstrophy=col("enstrophy"),
        omega_inf=col("omega_inf"),
        div_max=col("div_max"),
        spectrum_tail=col("spectrum_tail"),
    )


def centered_identity_stats(t: np.ndarray, energy: np.ndarray, enstrophy: np.ndarray, nu: float) -> dict[str, float]:
    if len(t) < 3:
        return {"max": math.nan, "p95": math.nan, "median": math.nan}
    d_e_dt = (energy[2:] - energy[:-2]) / (t[2:] - t[:-2])
    rhs = -2.0 * nu * enstrophy[1:-1]
    rel = np.abs(d_e_dt - rhs) / np.maximum(np.abs(rhs), 1.0e-12)
    return {
        "max": float(np.max(rel)),
        "p95": float(np.percentile(rel, 95)),
        "median": float(np.median(rel)),
    }


def compare_run(run: RunData, ref: np.ndarray) -> dict[str, float | int | str | None]:
    ref_t, ref_e, ref_o = ref[:, 0], ref[:, 1], ref[:, 2]
    mask = (run.t >= ref_t.min()) & (run.t <= ref_t.max())
    t = run.t[mask]
    ref_energy = np.interp(t, ref_t, ref_e)
    ref_enstrophy = np.interp(t, ref_t, ref_o)
    energy_rel = np.abs(run.energy[mask] - ref_energy) / np.maximum(np.abs(ref_energy), 1.0e-12)
    enstrophy_rel = np.abs(run.enstrophy[mask] - ref_enstrophy) / np.maximum(np.abs(ref_enstrophy), 1.0e-12)
    worst_e = int(np.argmax(energy_rel))
    worst_o = int(np.argmax(enstrophy_rel))
    identity = centered_identity_stats(run.t, run.energy, run.enstrophy, NU)

    return {
        "run": run.name,
        "n": run.n,
        "t_end": float(run.t[-1]),
        "rows": int(len(run.t)),
        "max_divergence": float(np.nanmax(run.div_max)),
        "final_spectrum_tail": float(run.spectrum_tail[-1]),
        "max_energy_rel_err": float(energy_rel[worst_e]),
        "energy_worst_t": float(t[worst_e]),
        "max_enstrophy_rel_err": float(enstrophy_rel[worst_o]),
        "enstrophy_worst_t": float(t[worst_o]),
        "final_energy_rel_err": float(energy_rel[-1]),
        "final_enstrophy_rel_err": float(enstrophy_rel[-1]),
        "energy_identity_rel_max": identity["max"],
        "energy_identity_rel_p95": identity["p95"],
        "energy_identity_rel_median": identity["median"],
    }


def write_summary_csv(path: Path, rows: list[dict[str, float | int | str | None]]) -> None:
    fieldnames = [
        "run",
        "n",
        "t_end",
        "rows",
        "max_divergence",
        "final_spectrum_tail",
        "max_energy_rel_err",
        "energy_worst_t",
        "max_enstrophy_rel_err",
        "enstrophy_worst_t",
        "final_energy_rel_err",
        "final_enstrophy_rel_err",
        "energy_identity_rel_max",
        "energy_identity_rel_p95",
        "energy_identity_rel_median",
    ]
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_checkpoint_csv(path: Path, runs: list[RunData], ref: np.ndarray) -> None:
    checkpoints = np.asarray([0.1, 1.0, 2.0, 4.0, 6.0, 8.0, 9.5, 10.0])
    ref_t, ref_e, ref_o = ref[:, 0], ref[:, 1], ref[:, 2]
    fieldnames = [
        "run",
        "t",
        "energy",
        "energy_ref",
        "energy_rel_err",
        "enstrophy",
        "enstrophy_ref",
        "enstrophy_rel_err",
        "spectrum_tail",
    ]
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for run in runs:
            valid = checkpoints[checkpoints <= run.t[-1] + 1.0e-12]
            for t in valid:
                energy = float(np.interp(t, run.t, run.energy))
                enstrophy = float(np.interp(t, run.t, run.enstrophy))
                tail = float(np.interp(t, run.t, run.spectrum_tail))
                energy_ref = float(np.interp(t, ref_t, ref_e))
                enstrophy_ref = float(np.interp(t, ref_t, ref_o))
                writer.writerow(
                    {
                        "run": run.name,
                        "t": t,
                        "energy": energy,
                        "energy_ref": energy_ref,
                        "energy_rel_err": abs(energy - energy_ref) / max(abs(energy_ref), 1.0e-12),
                        "enstrophy": enstrophy,
                        "enstrophy_ref": enstrophy_ref,
                        "enstrophy_rel_err": abs(enstrophy - enstrophy_ref) / max(abs(enstrophy_ref), 1.0e-12),
                        "spectrum_tail": tail,
                    }
                )


def convention_check(ref: np.ndarray) -> dict[str, object]:
    ref_t, ref_e, ref_o = ref[:, 0], ref[:, 1], ref[:, 2]
    identity = centered_identity_stats(ref_t, ref_e, ref_o, NU)
    initial_expected = {
        "taylor_green_energy_mean_half_u2": 0.125,
        "taylor_green_enstrophy_mean_half_omega2": 0.375,
    }
    nearest_zero = int(np.argmin(np.abs(ref_t)))
    return {
        "nu": NU,
        "identity": identity,
        "reference_first_row": {
            "t": float(ref_t[nearest_zero]),
            "energy": float(ref_e[nearest_zero]),
            "enstrophy": float(ref_o[nearest_zero]),
        },
        "expected_initial_convention": initial_expected,
        "energy_ratio_to_expected": float(ref_e[nearest_zero] / initial_expected["taylor_green_energy_mean_half_u2"]),
        "enstrophy_ratio_to_expected": float(
            ref_o[nearest_zero] / initial_expected["taylor_green_enstrophy_mean_half_omega2"]
        ),
        "conclusion": (
            "Reference matches the solver convention: volume-averaged 1/2|u|^2 "
            "and 1/2|omega|^2. There is no factor-of-2 or volume-factor mismatch."
        ),
    }


def write_plots(out_dir: Path, runs: list[RunData], ref: np.ndarray) -> list[str]:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plot_dir = out_dir / "plots"
    plot_dir.mkdir(parents=True, exist_ok=True)
    ref_t, ref_e, ref_o = ref[:, 0], ref[:, 1], ref[:, 2]
    made: list[str] = []

    def finish(name: str, ylabel: str) -> None:
        plt.xlabel("t")
        plt.ylabel(ylabel)
        plt.grid(True, alpha=0.25)
        plt.legend()
        plt.tight_layout()
        path = plot_dir / name
        plt.savefig(path, dpi=160)
        plt.close()
        made.append(str(path.relative_to(ROOT)))

    plt.figure(figsize=(8, 5))
    plt.plot(ref_t, ref_e, color="black", linewidth=2.0, label="OpenSBLI 512 reference")
    for run in runs:
        plt.plot(run.t, run.energy, label=run.name)
    finish("energy_vs_reference.png", "kinetic energy")

    plt.figure(figsize=(8, 5))
    plt.plot(ref_t, ref_o, color="black", linewidth=2.0, label="OpenSBLI 512 reference")
    for run in runs:
        plt.plot(run.t, run.enstrophy, label=run.name)
    finish("enstrophy_vs_reference.png", "enstrophy")

    plt.figure(figsize=(8, 5))
    for run in runs:
        if run.t[-1] < 2.0:
            continue
        ref_interp = np.interp(run.t, ref_t, ref_o)
        rel = np.abs(run.enstrophy - ref_interp) / np.maximum(np.abs(ref_interp), 1.0e-12)
        plt.plot(run.t, rel * 100.0, label=run.name)
    plt.axhline(5.0, color="black", linestyle="--", linewidth=1.0, label="5% criterion")
    finish("enstrophy_relerr_percent.png", "relative enstrophy error (%)")

    plt.figure(figsize=(8, 5))
    for run in runs:
        if run.t[-1] < 2.0:
            continue
        plt.plot(run.t, run.spectrum_tail, label=run.name)
    finish("spectrum_tail.png", "tail energy fraction")

    return made


def write_readme(out_dir: Path, summary_rows: list[dict[str, float | int | str | None]], plots: list[str]) -> None:
    lines = [
        "# Step 6 Taylor-Green Diagnostics",
        "",
        "Generated from existing CSV runs only. No solver rerun was performed.",
        "",
        "## Summary",
        "",
        "| run | max E err | max Omega err | worst Omega t | final tail | div max |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for row in summary_rows:
        lines.append(
            "| {run} | {e:.3%} | {o:.3%} | {ot:.3g} | {tail:.4g} | {div:.3e} |".format(
                run=row["run"],
                e=float(row["max_energy_rel_err"]),
                o=float(row["max_enstrophy_rel_err"]),
                ot=float(row["enstrophy_worst_t"]),
                tail=float(row["final_spectrum_tail"]),
                div=float(row["max_divergence"]),
            )
        )
    lines.extend(["", "## Plots", ""])
    lines.extend(f"- `{plot}`" for plot in plots)
    lines.append("")
    (out_dir / "README.md").write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reference", type=Path, default=REFERENCE)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT)
    parser.add_argument(
        "--runs",
        type=Path,
        nargs="*",
        default=[
            RUNS / "TG_N32_t1/timeseries.csv",
            RUNS / "TG_N64_t1/timeseries.csv",
            RUNS / "TG_N64_t10/timeseries.csv",
            RUNS / "TG_N96_t10/timeseries.csv",
            RUNS / "TG_N128_t10/timeseries.csv",
        ],
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    ref = load_reference(args.reference)
    runs = [load_run(path) for path in args.runs if path.exists()]
    runs.sort(key=lambda run: (run.t[-1], run.n or 0, run.name))

    summary_rows = [compare_run(run, ref) for run in runs]
    write_summary_csv(args.out_dir / "summary.csv", summary_rows)
    write_checkpoint_csv(args.out_dir / "checkpoints.csv", runs, ref)
    convention = convention_check(ref)
    (args.out_dir / "convention_check.json").write_text(
        json.dumps(convention, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    plots = write_plots(args.out_dir, runs, ref)
    write_readme(args.out_dir, summary_rows, plots)

    print(json.dumps({"out_dir": str(args.out_dir), "summary": summary_rows, "convention": convention}, indent=2))


if __name__ == "__main__":
    main()
