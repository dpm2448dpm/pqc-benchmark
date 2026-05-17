#!/usr/bin/env python3
"""Generate ML-KEM and ML-DSA performance figures from raw benchmark CSVs.

Usage:
    python benchmarks/plot_pqc_results.py results/raw/pqc/ryzen -o results/figures/pqc_ryzen
"""

import argparse
from pathlib import Path

from pqc_benchmark.reporting.plots_pqc import generate_figures


def main() -> None:
    parser = argparse.ArgumentParser(description="Plot PQC (ML-KEM / ML-DSA) benchmark results")
    parser.add_argument("results_dir", type=Path, help="Folder containing PQC benchmark CSVs")
    parser.add_argument("-o", "--output", type=Path, default=Path("results/figures"),
                        help="Output directory for figures (default: results/figures)")
    args = parser.parse_args()
    generate_figures(args.results_dir, args.output)
    print(f"Figures written to {args.output}")


if __name__ == "__main__":
    main()
