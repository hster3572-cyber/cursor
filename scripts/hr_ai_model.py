#!/usr/bin/env python3
import json
import math
import os
from dataclasses import dataclass
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

plt.rcParams["font.family"] = "DejaVu Sans"


@dataclass
class DepartmentInput:
    department: str
    headcount: int
    fully_loaded_cost_per_fte_usd: float
    admin_time_pct: float
    baseline_productivity_index: float
    expected_automation_coverage_pct: float
    productivity_uplift_pct_from_copilot: float
    license_eligible_users_pct: float
    adoption_start_month: int
    adoption_ramp_months: int


@dataclass
class Config:
    timeframe_months: int
    currency: str
    license_cost_per_user_per_month_usd: float
    implementation_fixed_cost_usd: float
    change_management_per_department_usd: float
    training_hours_per_user: float
    discount_rate_annual: float
    productivity_monetization_share: float


# Helper functions

def monthly_discount_factor(annual_rate: float) -> float:
    return (1 + annual_rate) ** (1 / 12) - 1


def to_monthly_series(length: int, value: float) -> np.ndarray:
    return np.full(shape=(length,), fill_value=value, dtype=float)


# Modeling core

def read_inputs(inputs_csv: str, config_json: str) -> Tuple[List[DepartmentInput], Config]:
    df = pd.read_csv(inputs_csv)
    required_cols = {
        "department",
        "headcount",
        "fully_loaded_cost_per_fte_usd",
        "admin_time_pct",
        "baseline_productivity_index",
        "expected_automation_coverage_pct",
        "productivity_uplift_pct_from_copilot",
        "license_eligible_users_pct",
        "adoption_start_month",
        "adoption_ramp_months",
    }
    missing = required_cols.difference(df.columns)
    if missing:
        raise ValueError(f"Missing columns in inputs: {missing}")
    departments: List[DepartmentInput] = []
    for _, r in df.iterrows():
        departments.append(
            DepartmentInput(
                department=str(r["department"]),
                headcount=int(r["headcount"]),
                fully_loaded_cost_per_fte_usd=float(r["fully_loaded_cost_per_fte_usd"]),
                admin_time_pct=float(r["admin_time_pct"]),
                baseline_productivity_index=float(r["baseline_productivity_index"]),
                expected_automation_coverage_pct=float(r["expected_automation_coverage_pct"]),
                productivity_uplift_pct_from_copilot=float(r["productivity_uplift_pct_from_copilot"]),
                license_eligible_users_pct=float(r["license_eligible_users_pct"]),
                adoption_start_month=int(r["adoption_start_month"]),
                adoption_ramp_months=int(r["adoption_ramp_months"]),
            )
        )
    with open(config_json, "r", encoding="utf-8") as f:
        cfg_raw = json.load(f)
    cfg = Config(
        timeframe_months=int(cfg_raw["timeframe_months"]),
        currency=str(cfg_raw["currency"]),
        license_cost_per_user_per_month_usd=float(cfg_raw["license_cost_per_user_per_month_usd"]),
        implementation_fixed_cost_usd=float(cfg_raw["implementation_fixed_cost_usd"]),
        change_management_per_department_usd=float(cfg_raw["change_management_per_department_usd"]),
        training_hours_per_user=float(cfg_raw["training_hours_per_user"]),
        discount_rate_annual=float(cfg_raw["discount_rate_annual"]),
        productivity_monetization_share=float(cfg_raw["productivity_monetization_share"]),
    )
    return departments, cfg


def build_adoption_curve(months: int, start: int, ramp: int) -> np.ndarray:
    curve = np.zeros(months, dtype=float)
    start_idx = max(0, start - 1)  # 0-based
    if start_idx >= months:
        return curve
    # Linear ramp from 0 to 1 across ramp months starting at start_idx
    ramp_end = min(months, start_idx + ramp)
    if ramp <= 0:
        curve[start_idx:] = 1.0
        return curve
    if ramp_end > start_idx:
        curve[start_idx:ramp_end] = np.linspace(0, 1, ramp_end - start_idx, endpoint=False)
    if ramp_end < months:
        curve[ramp_end:] = 1.0
    return curve


def model_department(dep: DepartmentInput, cfg: Config) -> Dict[str, pd.DataFrame]:
    months = cfg.timeframe_months
    adoption_curve = build_adoption_curve(months, dep.adoption_start_month, dep.adoption_ramp_months)

    # Baselines
    monthly_flc_per_fte = dep.fully_loaded_cost_per_fte_usd / 12.0
    eligible_users = dep.headcount * dep.license_eligible_users_pct

    # Costs
    license_cost = adoption_curve * eligible_users * cfg.license_cost_per_user_per_month_usd
    training_cost = np.zeros(months, dtype=float)
    # One-time training cost at adoption start: hours * hourly rate * eligible users
    hourly_rate = monthly_flc_per_fte * 12 / (52 * 40) * 1.0  # approx hourly from annual FLC
    if dep.adoption_start_month - 1 < months:
        training_cost[max(dep.adoption_start_month - 1, 0)] = cfg.training_hours_per_user * hourly_rate * eligible_users

    change_mgmt_cost = np.zeros(months, dtype=float)
    if dep.adoption_start_month - 1 < months:
        change_mgmt_cost[max(dep.adoption_start_month - 1, 0)] = cfg.change_management_per_department_usd

    # Savings and productivity
    # Admin time reclaimed: admin_time_pct * automation_coverage * adoption
    admin_time_reclaimed_pct = dep.admin_time_pct * dep.expected_automation_coverage_pct * adoption_curve
    # Monetizable savings from reclaimed time: portion of FLC
    admin_time_savings = admin_time_reclaimed_pct * dep.headcount * monthly_flc_per_fte * cfg.productivity_monetization_share

    # Productivity uplift value: productivity_uplift_pct_from_copilot applied to non-admin time share
    non_admin_time_pct = 1.0 - dep.admin_time_pct
    productivity_uplift_value = (
        non_admin_time_pct
        * dep.productivity_uplift_pct_from_copilot
        * adoption_curve
        * dep.headcount
        * monthly_flc_per_fte
        * cfg.productivity_monetization_share
    )

    monthly_benefit = admin_time_savings + productivity_uplift_value
    monthly_costs = license_cost + training_cost + change_mgmt_cost
    net_benefit = monthly_benefit - monthly_costs

    df = pd.DataFrame(
        {
            "month": np.arange(1, months + 1),
            "adoption": adoption_curve,
            "license_cost": license_cost,
            "training_cost": training_cost,
            "change_mgmt_cost": change_mgmt_cost,
            "admin_time_savings": admin_time_savings,
            "productivity_uplift_value": productivity_uplift_value,
            "monthly_benefit": monthly_benefit,
            "monthly_cost": monthly_costs,
            "net_benefit": net_benefit,
        }
    )

    summary = {
        "department": dep.department,
        "eligible_users": round(eligible_users),
        "annual_flc_per_fte": dep.fully_loaded_cost_per_fte_usd,
        "month_12_net": float(df["net_benefit"].sum()),
        "month_12_benefit": float(df["monthly_benefit"].sum()),
        "month_12_cost": float(df["monthly_cost"].sum()),
        "roi": float((df["monthly_benefit"].sum() - df["monthly_cost"].sum()) / max(df["monthly_cost"].sum(), 1e-9)),
        "payback_month": int((df["net_benefit"].cumsum() > 0).idxmax() + 1) if (df["net_benefit"].cumsum() > 0).any() else None,
    }

    return {"monthly": df, "summary": pd.DataFrame([summary])}


def plot_aggregates(all_monthly: Dict[str, pd.DataFrame], out_dir: str, currency: str) -> None:
    os.makedirs(out_dir, exist_ok=True)
    months = next(iter(all_monthly.values())).shape[0]
    month_index = np.arange(1, months + 1)

    # Aggregate time series
    agg = None
    for dep, df in all_monthly.items():
        tmp = df.copy()
        tmp["department"] = dep
        agg = tmp if agg is None else pd.concat([agg, tmp], ignore_index=True)
    pivot_benefit = agg.pivot_table(index="month", values=["monthly_benefit", "monthly_cost", "net_benefit"], aggfunc="sum")

    # ROI over time
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(pivot_benefit.index, pivot_benefit["monthly_benefit"].cumsum(), label="Кумулятивная выгода", color="#1B5E20")
    ax.plot(pivot_benefit.index, pivot_benefit["monthly_cost"].cumsum(), label="Кумулятивные затраты", color="#B71C1C")
    ax.plot(pivot_benefit.index, pivot_benefit["net_benefit"].cumsum(), label="Кумулятивный эффект", color="#0D47A1")
    ax.set_xlabel("Месяц")
    ax.set_ylabel(f"{currency}")
    ax.grid(True, alpha=0.25)
    ax.legend()
    fig.tight_layout()
    fig.savefig(os.path.join(out_dir, "roi_over_time.png"), dpi=150)
    plt.close(fig)

    # Savings by department (stacked)
    dep_totals = agg.groupby("department")["monthly_benefit"].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(dep_totals.index, dep_totals.values, color="#66BB6A")
    ax.set_title("Выгода по отделам (12 мес)")
    ax.set_ylabel(f"{currency}")
    ax.grid(True, axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(os.path.join(out_dir, "benefit_by_department.png"), dpi=150)
    plt.close(fig)

    # Costs by component (year total)
    costs = agg[["license_cost", "training_cost", "change_mgmt_cost"]].sum()
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(costs.index, costs.values, color=["#3949AB", "#8E24AA", "#E53935"])
    ax.set_title("Затраты (12 мес)")
    ax.set_ylabel(f"{currency}")
    ax.grid(True, axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(os.path.join(out_dir, "costs_breakdown.png"), dpi=150)
    plt.close(fig)


def build_gantt(out_path: str) -> None:
    # Define phases
    phases = [
        ("Подготовка и закупка", 1, 1),
        ("Пилот (HR, Finance, IT)", 2, 2),
        ("Обучение и принятие", 3, 3),
        ("Масштабирование (Operations, Legal)", 5, 3),
        ("Оптимизация и контроль", 8, 5),
    ]
    fig, ax = plt.subplots(figsize=(12, 4))
    for i, (name, start, duration) in enumerate(phases):
        ax.barh(y=i, width=duration, left=start, height=0.5, color="#42A5F5")
        ax.text(start + duration / 2, i, name, va="center", ha="center", color="white")
    ax.set_xlabel("Месяц")
    ax.set_yticks([])
    ax.set_xlim(0.5, 12.5)
    ax.set_title("Диаграмма Ганта: внедрение AI-ассистента")
    ax.grid(True, axis="x", alpha=0.2)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def currency_fmt(x: float) -> str:
    return f"${x:,.0f}"


def main():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    inputs_csv = os.path.join(base_dir, "data", "hr_ai_inputs.csv")
    config_json = os.path.join(base_dir, "data", "hr_ai_config.json")
    outputs_dir = os.path.join(base_dir, "outputs")
    model_dir = os.path.join(outputs_dir, "model")
    os.makedirs(model_dir, exist_ok=True)

    departments, cfg = read_inputs(inputs_csv, config_json)

    # Organization-level fixed implementation cost booked month 1
    org_fixed_cost = np.zeros(cfg.timeframe_months)
    org_fixed_cost[0] = cfg.implementation_fixed_cost_usd

    monthly_frames: Dict[str, pd.DataFrame] = {}
    summary_frames: List[pd.DataFrame] = []
    for dep in departments:
        res = model_department(dep, cfg)
        monthly_frames[dep.department] = res["monthly"]
        summary_frames.append(res["summary"])
    summary_df = pd.concat(summary_frames, ignore_index=True)

    # Aggregate monthly across departments and add org fixed cost
    agg_monthly = sum((df[["license_cost","training_cost","change_mgmt_cost","admin_time_savings","productivity_uplift_value","monthly_benefit","monthly_cost","net_benefit"]] for df in monthly_frames.values()))
    agg_monthly["org_fixed_cost"] = org_fixed_cost
    agg_monthly["monthly_cost"] = agg_monthly["monthly_cost"] + agg_monthly["org_fixed_cost"]
    agg_monthly["net_benefit"] = agg_monthly["monthly_benefit"] - agg_monthly["monthly_cost"]
    agg_monthly.insert(0, "month", np.arange(1, cfg.timeframe_months + 1))

    # NPV
    r_m = monthly_discount_factor(cfg.discount_rate_annual)
    agg_monthly["discount_factor"] = 1 / (1 + r_m) ** (agg_monthly["month"] - 1)
    npv = float((agg_monthly["net_benefit"] * agg_monthly["discount_factor"]).sum())

    # Save CSVs
    summary_df.to_csv(os.path.join(model_dir, "department_summary.csv"), index=False)
    for dep, df in monthly_frames.items():
        df.to_csv(os.path.join(model_dir, f"monthly_{dep.replace('/', '_')}.csv"), index=False)
    agg_monthly.to_csv(os.path.join(model_dir, "monthly_total.csv"), index=False)

    # Charts
    plot_aggregates({k: v for k, v in monthly_frames.items()}, out_dir=model_dir, currency=cfg.currency)
    build_gantt(os.path.join(model_dir, "gantt.png"))

    # Write a quick textual summary
    total_benefit = float(agg_monthly["monthly_benefit"].sum())
    total_cost = float(agg_monthly["monthly_cost"].sum())
    roi = (total_benefit - total_cost) / total_cost if total_cost else float("inf")

    with open(os.path.join(model_dir, "summary.txt"), "w", encoding="utf-8") as f:
        f.write("Финансовая сводка (12 мес)\n")
        f.write(f"NPV: {currency_fmt(npv)}\n")
        f.write(f"Суммарные выгоды: {currency_fmt(total_benefit)}\n")
        f.write(f"Суммарные затраты: {currency_fmt(total_cost)}\n")
        f.write(f"ROI: {roi:.1%}\n")

    print("Model built. See outputs/model/")


if __name__ == "__main__":
    main()
