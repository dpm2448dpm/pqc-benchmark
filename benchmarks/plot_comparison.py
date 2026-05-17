#!/usr/bin/env python3
"""Generate PQC-vs-classical comparison figures grouped by NIST security level.

Usage:
    python benchmarks/plot_comparison.py --base results/raw -o results/figures/comparison
"""

import argparse
from pathlib import Path

from pqc_benchmark.reporting.plots_comparison import generate_figures

_PLATFORMS = ["celeron", "ryzen", "raspberry"]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compare PQC and classical algorithms by NIST security level"
    )
    parser.add_argument("--base", type=Path, default=Path("results/raw"),
                        help="Base results directory containing pqc/ and classical/ sub-folders")
    parser.add_argument("-o", "--output", type=Path, default=Path("results/figures/comparison"),
                        help="Output directory for figures")
    args = parser.parse_args()

    platform_dirs: dict[str, tuple[Path, Path]] = {}
    for platform in _PLATFORMS:
        classic_dir = args.base / "classical" / platform
        pqc_dir = args.base / "pqc" / platform
        if classic_dir.is_dir() and pqc_dir.is_dir():
            platform_dirs[platform] = (classic_dir, pqc_dir)

    if not platform_dirs:
        parser.error(f"No valid platform directories found under {args.base}")

    generate_figures(platform_dirs, args.output)
    print(f"Figures written to {args.output}")


if __name__ == "__main__":
    main()
