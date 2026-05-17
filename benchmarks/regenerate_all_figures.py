#!/usr/bin/env python3
"""Regenerate all figures from the raw data in results/raw/.

This is the single entry point to reproduce every figure in results/figures/
from scratch. Run from the repository root:

    python benchmarks/regenerate_all_figures.py
"""

from pathlib import Path

from pqc_benchmark.reporting.plots_pqc import generate_figures as gen_pqc
from pqc_benchmark.reporting.plots_classical import generate_figures as gen_classical
from pqc_benchmark.reporting.plots_tls import generate_figures as gen_tls
from pqc_benchmark.reporting.plots_comparison import generate_figures as gen_comparison

RAW = Path("results/raw")
FIGURES = Path("results/figures")
PLATFORMS = ["celeron", "ryzen", "raspberry"]


def main() -> None:
    print("=== Regenerating all figures ===\n")

    for platform in PLATFORMS:
        pqc_dir = RAW / "pqc" / platform
        if pqc_dir.is_dir():
            out = FIGURES / f"pqc_{platform}"
            print(f"[PQC] {platform} → {out}")
            gen_pqc(pqc_dir, out)

        classic_dir = RAW / "classical" / platform
        if classic_dir.is_dir():
            out = FIGURES / f"classical_{platform}"
            print(f"[Classical] {platform} → {out}")
            gen_classical(classic_dir, out)

    tls_dirs = {
        p: RAW / "tls" / p for p in PLATFORMS if (RAW / "tls" / p).is_dir()
    }
    if tls_dirs:
        out = FIGURES / "tls"
        print(f"[TLS] → {out}")
        gen_tls(tls_dirs, out)

    platform_dirs = {
        p: (RAW / "classical" / p, RAW / "pqc" / p)
        for p in PLATFORMS
        if (RAW / "classical" / p).is_dir() and (RAW / "pqc" / p).is_dir()
    }
    if platform_dirs:
        out = FIGURES / "comparison"
        print(f"[Comparison] → {out}")
        gen_comparison(platform_dirs, out)

    print("\nDone. All figures written to", FIGURES)


if __name__ == "__main__":
    main()
