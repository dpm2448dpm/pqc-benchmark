"""Figure generation for ML-KEM and ML-DSA benchmark results."""

from __future__ import annotations

import glob
import os
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


_KEM_ORDER = ["ML-KEM-512", "ML-KEM-768", "ML-KEM-1024"]
_SIG_ORDER = ["ML-DSA-44", "ML-DSA-65", "ML-DSA-87"]


def parse_bytes_field(value: str) -> pd.Series:
    """Parse a pipe-separated key=value string into a Series.

    Example input: ``"pk=1568|sk=3168|ct=1568|ss=32"``
    """
    out: dict[str, float] = {}
    for part in str(value).split("|"):
        if "=" in part:
            k, v = part.split("=", 1)
            out[k.strip()] = pd.to_numeric(v, errors="coerce")
    return pd.Series(out)


def load_pqc_folder(folder: str | Path) -> pd.DataFrame:
    """Load all ML-KEM and ML-DSA CSVs from *folder* into a single DataFrame."""
    folder = str(folder)
    files = glob.glob(os.path.join(folder, "kem_*ML-KEM-*.csv")) + glob.glob(
        os.path.join(folder, "sig_*ML-DSA-*.csv")
    )
    if not files:
        raise FileNotFoundError(f"No PQC CSV files found in {folder}")

    frames = []
    for f in files:
        df = pd.read_csv(f)
        for col in ["iterations", "total_time_s", "mean_us"]:
            if col not in df.columns:
                df[col] = pd.NA

        sizes = df["bytes"].apply(parse_bytes_field)
        df = pd.concat([df.drop(columns=["bytes"]), sizes], axis=1)

        for col in ["pk", "sk", "ct", "ss", "sig"]:
            if col not in df.columns:
                df[col] = pd.NA

        df["source_file"] = os.path.basename(f)
        frames.append(df)

    combined = pd.concat(frames, ignore_index=True)
    combined["ms_per_op"] = 1000.0 / combined["ops_per_sec"]
    combined["algo"] = pd.Categorical(
        combined["algo"], categories=_KEM_ORDER + _SIG_ORDER, ordered=True
    )
    combined["op"] = pd.Categorical(
        combined["op"],
        categories=["keypair", "keygen", "encaps", "decaps", "sign", "verify"],
        ordered=True,
    )
    return combined


def _plot_bar(df: pd.DataFrame, metric: str, title: str, outfile: str | Path, ops: tuple[str, ...]) -> None:
    sub = df[df["op"].isin(ops)].copy()
    g = (
        sub.groupby(["algo", "op"], observed=False)[metric]
        .agg(["mean", "std"])
        .reset_index()
    )
    pivot_mean = g.pivot(index="algo", columns="op", values="mean").sort_index()
    pivot_std = g.pivot(index="algo", columns="op", values="std").reindex_like(pivot_mean)

    ax = pivot_mean.plot(kind="bar", yerr=pivot_std, capsize=3)
    ax.set_title(title)
    ax.set_ylabel(metric)
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    plt.tight_layout()
    plt.savefig(outfile, dpi=200)
    plt.close()


def save_summary(df: pd.DataFrame, outdir: str | Path) -> pd.DataFrame:
    """Aggregate statistics per (algo, op) and save to *outdir*/summary_pqc.csv."""
    agg: dict = {"ops_per_sec": ["mean", "std"], "ms_per_op": ["mean", "std"]}
    for col in ["pk", "sk", "ct", "ss", "sig"]:
        if col in df.columns:
            agg[col] = "max"

    g = df.groupby(["algo", "op"], observed=False).agg(agg)
    g.columns = [
        "_".join(c) if isinstance(c, tuple) else c for c in g.columns
    ]
    g = g.reset_index()
    g.to_csv(os.path.join(outdir, "summary_pqc.csv"), index=False)
    return g


def generate_figures(input_dir: str | Path, output_dir: str | Path) -> None:
    """Generate all PQC figures from *input_dir* CSVs and write PNGs to *output_dir*."""
    os.makedirs(output_dir, exist_ok=True)
    df = load_pqc_folder(input_dir)
    save_summary(df, output_dir)

    kem = df[df["algo"].str.contains("ML-KEM", na=False)]
    if not kem.empty:
        _plot_bar(kem, "ops_per_sec", "ML-KEM — Encaps/Decaps (ops/s)",
                  os.path.join(output_dir, "kem_ops_per_sec.png"), ("encaps", "decaps"))
        _plot_bar(kem, "ms_per_op", "ML-KEM — Encaps/Decaps (ms/op)",
                  os.path.join(output_dir, "kem_latency.png"), ("encaps", "decaps"))

        if "ct" in df.columns and df["ct"].notna().any():
            sizes = kem.groupby("algo", as_index=False)[["pk", "sk", "ct", "ss"]].max()
            sizes = sizes.set_index("algo").sort_index()
            ax = sizes.plot(kind="bar")
            ax.set_title("ML-KEM — Key/Ciphertext sizes (bytes)")
            ax.set_ylabel("bytes")
            ax.grid(axis="y", linestyle="--", alpha=0.4)
            plt.tight_layout()
            plt.savefig(os.path.join(output_dir, "kem_sizes_bytes.png"), dpi=200)
            plt.close()

    sig = df[df["algo"].str.contains("ML-DSA", na=False)]
    if not sig.empty:
        _plot_bar(sig, "ops_per_sec", "ML-DSA — Sign/Verify (ops/s)",
                  os.path.join(output_dir, "sig_ops_per_sec.png"), ("sign", "verify"))
        _plot_bar(sig, "ms_per_op", "ML-DSA — Sign/Verify (ms/op)",
                  os.path.join(output_dir, "sig_latency.png"), ("sign", "verify"))

        if "sig" in df.columns and df["sig"].notna().any():
            sizes = sig.groupby("algo", as_index=False)[["pk", "sk", "sig"]].max()
            sizes = sizes.set_index("algo").sort_index()
            ax = sizes.plot(kind="bar")
            ax.set_title("ML-DSA — Key/Signature sizes (bytes)")
            ax.set_ylabel("bytes")
            ax.grid(axis="y", linestyle="--", alpha=0.4)
            plt.tight_layout()
            plt.savefig(os.path.join(output_dir, "sig_sizes_bytes.png"), dpi=200)
            plt.close()
