"""Taylor-Green validation runner for the pseudo-spectral NSE solver."""

from __future__ import annotations

import argparse
import csv
import json
import math
import sys
import time
from pathlib import Path

import numpy as np

THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from pseudospectral import PseudoSpectralNSE, SolverConfig, taylor_green_initial, write_csv


ROOT = THIS_DIR.parents[1]
REFERENCE = ROOT / "refs/reference_data/taylor_green_debonis_opensbli_512.dat"


def load_reference(path: Path = REFERENCE) -> np.ndarray:
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


def centered_energy_residual(times: np.ndarray, energy: np.ndarray, enstrophy: np.ndarray, nu: float) -> float:
    if len(times) < 3:
        return math.nan
    d_e_dt = (energy[2:] - energy[:-2]) / (times[2:] - times[:-2])
    rhs = -2.0 * nu * enstrophy[1:-1]
    denom = np.maximum(np.abs(rhs), 1.0e-12)
    return float(np.max(np.abs(d_e_dt - rhs) / denom))


def validate(args: argparse.Namespace) -> dict[str, object]:
    cfg = SolverConfig(n=args.n, nu=args.nu, dt=args.dt, t_end=args.t_end, integrator=args.integrator)
    solver = PseudoSpectralNSE(cfg)
    start = time.perf_counter()
    _, rows = solver.run(taylor_green_initial(args.n), sample_every=args.sample_every)
    elapsed = time.perf_counter() - start

    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    csv_path = out_dir / "timeseries.csv"
    write_csv(csv_path, rows)

    t = np.asarray([r.t for r in rows])
    energy = np.asarray([r.energy for r in rows])
    enstrophy = np.asarray([r.enstrophy for r in rows])
    div_max = np.asarray([r.div_max for r in rows])

    ref = load_reference(args.reference)
    ref_t, ref_e, ref_o = ref[:, 0], ref[:, 1], ref[:, 2]
    mask = (t >= ref_t.min()) & (t <= min(ref_t.max(), args.t_end))
    if np.any(mask):
        ref_energy = np.interp(t[mask], ref_t, ref_e)
        ref_enstrophy = np.interp(t[mask], ref_t, ref_o)
        energy_rel_err = np.abs(energy[mask] - ref_energy) / np.maximum(np.abs(ref_energy), 1.0e-12)
        enstrophy_rel_err = np.abs(enstrophy[mask] - ref_enstrophy) / np.maximum(np.abs(ref_enstrophy), 1.0e-12)
        max_energy_rel_err = float(np.max(energy_rel_err))
        max_enstrophy_rel_err = float(np.max(enstrophy_rel_err))
    else:
        max_energy_rel_err = math.nan
        max_enstrophy_rel_err = math.nan

    report = {
        "n": args.n,
        "nu": args.nu,
        "re": 1.0 / args.nu if args.nu else math.inf,
        "dt": args.dt,
        "t_end": args.t_end,
        "sample_every": args.sample_every,
        "integrator": args.integrator,
        "elapsed_seconds": elapsed,
        "rows": len(rows),
        "csv": str(csv_path),
        "reference": str(args.reference),
        "max_divergence": float(np.max(div_max)),
        "energy_start": float(energy[0]),
        "energy_end": float(energy[-1]),
        "enstrophy_start": float(enstrophy[0]),
        "enstrophy_end": float(enstrophy[-1]),
        "max_energy_rel_err_vs_reference": max_energy_rel_err,
        "max_enstrophy_rel_err_vs_reference": max_enstrophy_rel_err,
        "max_energy_identity_rel_residual": centered_energy_residual(t, energy, enstrophy, args.nu),
        "pass_divergence": bool(np.max(div_max) < args.div_tol),
        "pass_reference_5pct": bool(
            np.isfinite(max_energy_rel_err)
            and np.isfinite(max_enstrophy_rel_err)
            and max_energy_rel_err <= 0.05
            and max_enstrophy_rel_err <= 0.05
        ),
    }
    report["pass"] = bool(report["pass_divergence"] and report["pass_reference_5pct"])

    report_path = out_dir / "validation_report.json"
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    (out_dir / "README.md").write_text(
        "# Taylor-Green Validation Run\n\n"
        f"- N: {args.n}\n"
        f"- integrator: {args.integrator}\n"
        f"- nu: {args.nu} (Re={1.0 / args.nu:.6g})\n"
        f"- dt: {args.dt}\n"
        f"- t_end: {args.t_end}\n"
        f"- max divergence: {report['max_divergence']:.3e}\n"
        f"- max energy rel err vs reference: {report['max_energy_rel_err_vs_reference']:.6g}\n"
        f"- max enstrophy rel err vs reference: {report['max_enstrophy_rel_err_vs_reference']:.6g}\n"
        f"- pass: {report['pass']}\n",
    )
    return report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n", type=int, default=32)
    parser.add_argument("--nu", type=float, default=1.0 / 1600.0)
    parser.add_argument("--dt", type=float, default=0.002)
    parser.add_argument("--t-end", type=float, default=1.0)
    parser.add_argument("--sample-every", type=int, default=10)
    parser.add_argument("--integrator", choices=["rk4", "ifrk4"], default="rk4")
    parser.add_argument("--div-tol", type=float, default=1.0e-10)
    parser.add_argument("--reference", type=Path, default=REFERENCE)
    parser.add_argument("--out-dir", type=Path, default=ROOT / "track-b-blowup/runs/TG_N32_t1")
    return parser.parse_args()


def main() -> None:
    report = validate(parse_args())
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
