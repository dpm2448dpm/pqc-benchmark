#!/usr/bin/env python3
"""Generate classical cryptography figures from raw benchmark CSVs.

Usage:
    python benchmarks/plot_classical_results.py results/raw/classical/ryzen -o results/figures/classical_ryzen
"""

import argparse
from pathlib import Path

from pqc_benchmark.reporting.plots_classical import generate_figures


def main() -> None:
    parser = argparse.ArgumentParser(description="Plot classical benchmark results (RSA, ECDSA, EdDSA)")
    parser.add_argument("results_dir", type=Path, help="Folder containing classical benchmark CSVs")
    parser.add_argument("-o", "--output", type=Path, default=Path("results/figures"),
                        help="Output directory for figures (default: results/figures)")
    args = parser.parse_args()
    generate_figures(args.results_dir, args.output)
    print(f"Figures written to {args.output}")


if __name__ == "__main__":
    main()
