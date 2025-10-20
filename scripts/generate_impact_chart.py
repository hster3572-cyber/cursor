#!/usr/bin/env python3
import argparse
import os
from typing import Tuple

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate charts showing positive project impact.")
    parser.add_argument("--input", required=True, help="Path to CSV with columns: date, metric_before, metric_after")
    parser.add_argument("--output-dir", required=True, help="Directory to write chart images")
    parser.add_argument("--adoption-date", default="2024-04", help="Project adoption date in YYYY-MM format")
    parser.add_argument("--title", default="Эффект проекта", help="Chart title prefix")
    return parser.parse_args()


def read_and_prepare(input_path: str, adoption_date_str: str) -> pd.DataFrame:
    df = pd.read_csv(input_path)
    if "date" not in df.columns or "metric_before" not in df.columns or "metric_after" not in df.columns:
        raise ValueError("CSV must contain columns: date, metric_before, metric_after")

    df["date"] = pd.to_datetime(df["date"], format="%Y-%m")
    df = df.sort_values("date").reset_index(drop=True)

    adoption_date = pd.to_datetime(adoption_date_str, format="%Y-%m")

    df["effect_raw"] = df["metric_after"] - df["metric_before"]
    df["effect_positive"] = np.where(df["date"] >= adoption_date, df["effect_raw"].clip(lower=0), 0)
    df["cumulative_effect"] = df["effect_positive"].cumsum()

    df.attrs["adoption_date"] = adoption_date
    return df


def format_date_axis(ax):
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    for label in ax.get_xticklabels():
        label.set_rotation(45)
        label.set_ha("right")


def plot_time_series(df: pd.DataFrame, output_path: str, title_prefix: str) -> None:
    adoption_date = df.attrs["adoption_date"]

    plt.rcParams["font.family"] = "DejaVu Sans"
    fig, ax = plt.subplots(figsize=(12, 6))

    ax.plot(df["date"], df["metric_before"], label="До внедрения (база)", color="#606470", linewidth=2)
    ax.plot(df["date"], df["metric_after"], label="После внедрения", color="#2E7D32", linewidth=2.5)

    mask = df["date"] >= adoption_date
    ax.fill_between(
        df.loc[mask, "date"],
        df.loc[mask, "metric_before"],
        df.loc[mask, "metric_after"],
        where=(df.loc[mask, "metric_after"] >= df.loc[mask, "metric_before"]),
        color="#2E7D32",
        alpha=0.15,
        label="Позитивный эффект",
    )

    ax.axvline(adoption_date, color="#B71C1C", linestyle="--", linewidth=1.5)
    ax.text(
        adoption_date,
        max(df["metric_before"].max(), df["metric_after"].max()),
        " Внедрение",
        color="#B71C1C",
        va="top",
        ha="left",
    )

    ax.set_title(f"{title_prefix}: динамика показателя")
    ax.set_xlabel("Месяц")
    ax.set_ylabel("Значение показателя")
    ax.grid(True, alpha=0.25)
    ax.legend()

    format_date_axis(ax)
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)


def plot_effect(df: pd.DataFrame, output_path: str, title_prefix: str) -> None:
    adoption_date = df.attrs["adoption_date"]

    plt.rcParams["font.family"] = "DejaVu Sans"
    fig, ax1 = plt.subplots(figsize=(12, 6))

    ax1.bar(df["date"], df["effect_positive"], color="#66BB6A", label="Ежемесячный эффект")
    ax1.set_ylabel("Ежемесячный эффект")

    ax2 = ax1.twinx()
    ax2.plot(df["date"], df["cumulative_effect"], color="#1B5E20", linewidth=2.5, label="Кумулятивный эффект")
    ax2.set_ylabel("Кумулятивный эффект")

    ax1.axvline(adoption_date, color="#B71C1C", linestyle="--", linewidth=1.5)
    ax1.text(
        adoption_date,
        max(df["effect_positive"].max(), 0) * 1.05 if df["effect_positive"].max() > 0 else 1,
        " Внедрение",
        color="#B71C1C",
        va="bottom",
        ha="left",
    )

    lines_1, labels_1 = ax1.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc="upper left")

    ax1.set_title(f"{title_prefix}: эффект и кумулятивный эффект")
    ax1.set_xlabel("Месяц")
    ax1.grid(True, alpha=0.25)

    format_date_axis(ax1)
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)


def main() -> None:
    args = parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    df = read_and_prepare(args.input, args.adoption_date)

    output_time_series = os.path.join(args.output_dir, "impact_time_series.png")
    output_effect = os.path.join(args.output_dir, "impact_effect.png")

    plot_time_series(df, output_time_series, args.title)
    plot_effect(df, output_effect, args.title)

    print(f"Saved: {output_time_series}")
    print(f"Saved: {output_effect}")


if __name__ == "__main__":
    main()
