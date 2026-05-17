"""Figure generation for TLS handshake benchmark results."""

from __future__ import annotations

import os
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def load_tls_folder(folder: str | Path, platform: str) -> pd.DataFrame:
    """Load all TLS result CSVs from *folder* and tag them with *platform*."""
    folder = Path(folder)
    frames = []

    for csv_file in sorted(folder.glob("results_tls_*.csv")):
        if csv_file.stat().st_size == 0:
            continue
        try:
            df = pd.read_csv(csv_file)
        except Exception as exc:
            print(f"[WARN] Could not read {csv_file}: {exc}")
            continue

        df.columns = [c.strip() for c in df.columns]
        required = {"Iteration", "Algorithm", "Time(s)"}
        if not required.issubset(df.columns):
            print(f"[WARN] Unexpected columns in {csv_file}: {list(df.columns)}")
            continue

        df = df[["Iteration", "Algorithm", "Time(s)"]].rename(
            columns={"Iteration": "iteration", "Algorithm": "algorithm", "Time(s)": "time_s"}
        )
        df["platform"] = platform
        frames.append(df)

    if not frames:
        return pd.DataFrame(columns=["platform", "algorithm", "iteration", "time_s"])
    return pd.concat(frames, ignore_index=True)


def compute_tls_stats(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate per-(platform, algorithm) TLS statistics."""
    return (
        df.groupby(["platform", "algorithm"])["time_s"]
        .agg(count="count", mean="mean", std="std", median="median",
             p95=lambda x: x.quantile(0.95), t_min="min", t_max="max")
        .reset_index()
        .sort_values(["platform", "mean"])
        .reset_index(drop=True)
    )


def _plot_platform(stats: pd.DataFrame, platform: str, output_dir: Path) -> None:
    sub = stats[stats["platform"] == platform].copy().sort_values("mean", ascending=True)
    sub["std"] = sub["std"].fillna(0.0)

    vmin, vmax = sub["std"].min(), sub["std"].max()
    norm = plt.Normalize(vmin, vmax if vmax > vmin else vmax + 1e-9)
    cmap = plt.cm.viridis
    colors = cmap(norm(sub["std"].values))

    fig, ax = plt.subplots(figsize=(12, max(6, 0.4 * len(sub))))
    ax.barh(sub["algorithm"], sub["mean"], xerr=sub["std"],
            color=colors, ecolor="black", capsize=3, linewidth=0.4, alpha=0.9)

    ax.set_xlabel("Mean TLS handshake time (s)")
    ax.set_ylabel("Algorithm")
    ax.set_title(f"TLS handshake latency — {platform}")
    ax.grid(axis="x", linestyle="--", alpha=0.5)

    for thresh in [0.05, 0.10, 0.20]:
        ax.axvline(thresh, linestyle="--", linewidth=1)
        ax.text(thresh, -0.5, f"{int(thresh * 1000)} ms",
                rotation=90, va="bottom", ha="right")

    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    fig.colorbar(sm, ax=ax).set_label("Std deviation (s)")
    fig.tight_layout()
    fig.savefig(output_dir / f"tls_handshake_{platform}.png", dpi=200)
    plt.close(fig)


def generate_figures(
    platform_dirs: dict[str, str | Path],
    output_dir: str | Path,
) -> None:
    """Generate per-platform TLS handshake figures.

    Args:
        platform_dirs: mapping of ``{platform_name: csv_folder}``.
        output_dir: destination for PNG files and summary CSV.
    """
    output_dir = Path(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    frames = []
    for platform, folder in platform_dirs.items():
        df = load_tls_folder(folder, platform)
        if df.empty:
            print(f"[WARN] No data for platform '{platform}'")
        else:
            frames.append(df)

    if not frames:
        raise RuntimeError("No TLS data loaded from any platform directory.")

    all_df = pd.concat(frames, ignore_index=True)
    all_df.to_csv(output_dir / "tls_all_raw.csv", index=False)

    stats = compute_tls_stats(all_df)
    stats.to_csv(output_dir / "tls_stats_summary.csv", index=False)

    for platform in stats["platform"].unique():
        _plot_platform(stats, platform, output_dir)
