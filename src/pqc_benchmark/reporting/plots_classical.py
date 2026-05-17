"""Figure generation for classical cryptography benchmark results (RSA, ECDSA, EdDSA)."""

from __future__ import annotations

import os
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import textwrap

sns.set_theme(style="whitegrid")
sns.set_context("paper", font_scale=1.6)

_PALETTE = {
    "rsa1024": "#1f77b4",
    "rsa2048": "#1f77b4",
    "rsa3072": "#1f77b4",
    "rsa4096": "#1f77b4",
    "ecdsap256": "#2ca02c",
    "ecdsap384": "#2ca02c",
    "ecdsap521": "#2ca02c",
    "ed25519": "#ff7f0e",
    "ed448": "#ff7f0e",
}


def load_classical_folder(folder: str | Path) -> pd.DataFrame:
    """Load all classical benchmark CSVs from *folder*."""
    folder = Path(folder)
    files = list(folder.glob("*.csv"))
    if not files:
        raise FileNotFoundError(f"No CSV files found in {folder}")

    frames = []
    for f in files:
        df = pd.read_csv(f)
        df = df[df["algo"] != "algo"]  # drop repeated header rows
        frames.append(df)

    combined = pd.concat(frames, ignore_index=True)
    combined["ops_per_sec"] = pd.to_numeric(combined["ops_per_sec"], errors="coerce")
    return combined.dropna(subset=["ops_per_sec"])


def compute_stats(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby(["algo", "op"])
        .agg(mean_ops=("ops_per_sec", "mean"), std_ops=("ops_per_sec", "std"), count=("ops_per_sec", "count"))
        .reset_index()
    )


def _plot_operation(df_all: pd.DataFrame, stats: pd.DataFrame, op: str, output_dir: Path) -> None:
    df_op = stats[stats["op"] == op].copy().sort_values("mean_ops", ascending=False)
    if df_op.empty:
        return

    plt.figure(figsize=(16, 8))
    sns.barplot(data=df_op, x="algo", y="mean_ops", hue="algo",
                palette=_PALETTE, legend=False, errorbar=None)

    if df_op["count"].max() > 1:
        plt.errorbar(x=np.arange(len(df_op)), y=df_op["mean_ops"], yerr=df_op["std_ops"],
                     fmt="none", ecolor="black", capsize=6, linewidth=1.4)

    sns.stripplot(data=df_all[df_all["op"] == op], x="algo", y="ops_per_sec",
                  color="black", jitter=True, size=6, alpha=0.6)

    labels = ["\n".join(textwrap.wrap(a, 12)) for a in df_op["algo"]]
    plt.xticks(ticks=np.arange(len(df_op)), labels=labels, rotation=15)
    plt.title(f"Classical — '{op}' throughput", fontsize=20)
    plt.ylabel("Operations per second")
    plt.subplots_adjust(left=0.12, right=0.98, top=0.90, bottom=0.25)
    plt.savefig(output_dir / f"{op}.png", dpi=300)
    plt.close()


def _plot_logscale_overview(stats: pd.DataFrame, output_dir: Path) -> None:
    plt.figure(figsize=(18, 8))
    sns.barplot(data=stats, x="algo", y="mean_ops", hue="op", palette="tab10", errorbar=None)
    plt.yscale("log")
    plt.xticks(rotation=15)
    plt.subplots_adjust(bottom=0.25)
    plt.title("Classical algorithms — all operations (log scale)")
    plt.ylabel("Operations per second (log)")
    plt.savefig(output_dir / "global_logscale.png", dpi=300)
    plt.close()


def generate_figures(input_dir: str | Path, output_dir: str | Path) -> None:
    """Generate per-operation and overview figures for classical benchmark data."""
    output_dir = Path(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    df = load_classical_folder(input_dir)
    stats = compute_stats(df)
    stats.to_csv(output_dir / "stats_summary.csv", index=False)

    for op in stats["op"].unique():
        _plot_operation(df, stats, op, output_dir)

    _plot_logscale_overview(stats, output_dir)
