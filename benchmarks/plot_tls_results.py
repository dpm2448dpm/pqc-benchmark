#!/usr/bin/env python3
"""Generate TLS handshake latency figures from raw benchmark CSVs.

Usage:
    python benchmarks/plot_tls_results.py \
        --celeron results/raw/tls/celeron \
        --ryzen   results/raw/tls/ryzen   \
        --raspberry results/raw/tls/raspberry \
        -o results/figures
"""

import argparse
from pathlib import Path

from pqc_benchmark.reporting.plots_tls import generate_figures


def main() -> None:
    parser = argparse.ArgumentParser(description="Plot TLS handshake benchmark results")
    parser.add_argument("--celeron",   type=Path, help="TLS CSV folder for Intel Celeron platform")
    parser.add_argument("--ryzen",     type=Path, help="TLS CSV folder for AMD Ryzen platform")
    parser.add_argument("--raspberry", type=Path, help="TLS CSV folder for Raspberry Pi platform")
    parser.add_argument("-o", "--output", type=Path, default=Path("results/figures"),
                        help="Output directory for figures (default: results/figures)")
    args = parser.parse_args()

    platform_dirs: dict[str, Path] = {}
    if args.celeron:
        platform_dirs["celeron"] = args.celeron
    if args.ryzen:
        platform_dirs["ryzen"] = args.ryzen
    if args.raspberry:
        platform_dirs["raspberry"] = args.raspberry

    if not platform_dirs:
        parser.error("At least one platform directory must be provided.")

    generate_figures(platform_dirs, args.output)
    print(f"Figures written to {args.output}")


if __name__ == "__main__":
    main()
