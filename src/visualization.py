"""
visualization.py

Visualization utilities for the Energy-Aware Agentic Geo-AI framework.

This module generates the primary figures used in:
- experimental evaluation,
- manuscript visualization,
- result interpretation.

The visualizations focus on:
- agent trajectories,
- energy–coverage trade-offs,
- coverage accumulation,
- robustness to environmental volatility.
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from environment import GeoEnvironment
from agent import (
    EnergyAwareAgent,
    OperationalPriorities
)

from experiments import run_episode


# -------------------------------------------------------------------
# Agent Trajectories
# -------------------------------------------------------------------

def plot_agent_trajectories(save_path=None):
    """
    Visualize agent trajectories across independently
    generated environments.

    The trajectories illustrate how agent movement adapts to:
    - environmental risk,
    - terrain cost,
    - monitoring coverage dynamics.
    """

    plt.figure(figsize=(6, 6))

    env = GeoEnvironment(seed=0)

    plt.imshow(
        env.risk_map,
        cmap="Reds",
        alpha=0.5
    )

    seeds = [
        0,
        25,
        47,
        72,
        99,
        137,
        189,
        200
    ]

    for seed in seeds:

        env = GeoEnvironment(seed=seed)

        agent = EnergyAwareAgent(
            model_type="tree"
        )

        agent.decision_log = []

        run_episode(
            env,
            agent,
            train=True
        )

        xs = [
            d["position"][0]
            for d in agent.decision_log
        ]

        ys = [
            d["position"][1]
            for d in agent.decision_log
        ]

        plt.plot(
            ys,
            xs,
            linewidth=1.5,
            label=f"Seed {seed}"
        )

    plt.legend()

    plt.title(
        "Agent Trajectories Across Environments"
    )

    plt.tight_layout()

    if save_path:
        plt.savefig(
            save_path,
            dpi=300,
            bbox_inches="tight"
        )

    plt.show()


# -------------------------------------------------------------------
# Energy–Coverage Trade-off
# -------------------------------------------------------------------

def plot_energy_coverage_tradeoff(
    df_agents,
    save_path=None
):
    """
    Visualize the trade-off between:
    - monitoring coverage,
    - energy consumption.

    Each point represents one simulation episode.
    """

    plt.figure(figsize=(6, 5))

    for agent_name, g in df_agents.groupby("Agent"):

        plt.scatter(
            g["energy_used"],
            g["coverage"],
            alpha=0.5,
            label=agent_name
        )

    plt.xlabel("Total Energy Used")

    plt.ylabel("Total Coverage Achieved")

    plt.title(
        "Energy–Coverage Trade-off Across Agents"
    )

    plt.legend()

    plt.grid(True)

    plt.tight_layout()

    if save_path:
        plt.savefig(
            save_path,
            dpi=300,
            bbox_inches="tight"
        )

    plt.show()


# -------------------------------------------------------------------
# Coverage Accumulation
# -------------------------------------------------------------------

def plot_coverage_accumulation(
    agent_results,
    save_path=None
):
    """
    Visualize cumulative monitoring coverage over time.

    This figure illustrates:
    - monitoring efficiency,
    - long-term sustainability,
    - coverage stability.
    """

    df_agents = pd.DataFrame(agent_results)

    plt.figure(figsize=(6, 4))

    for agent in df_agents["Agent"].unique():

        curves = [
            r["coverage_over_time"]
            for r in agent_results
            if r["Agent"] == agent
        ]

        min_len = min(len(c) for c in curves)

        curves = [
            c[:min_len]
            for c in curves
        ]

        mean_curve = np.mean(
            curves,
            axis=0
        )

        plt.plot(
            mean_curve,
            label=agent
        )

    plt.xlabel("Step")

    plt.ylabel("Cumulative Coverage")

    plt.title(
        "Coverage Accumulation Over Time"
    )

    plt.legend()

    plt.grid(True)

    plt.tight_layout()

    if save_path:
        plt.savefig(
            save_path,
            dpi=300,
            bbox_inches="tight"
        )

    plt.show()


# -------------------------------------------------------------------
# Stress Test Visualization
# -------------------------------------------------------------------

def plot_stress_test(
    df_stress,
    save_path=None
):
    """
    Visualize sustainability under increasing
    environmental volatility.

    Risk diffusion controls environmental uncertainty.
    """

    plt.figure(figsize=(6, 4))

    plt.plot(
        df_stress["RiskDiffusion"],
        df_stress["Sustainability"],
        marker="s",
        linewidth=2
    )

    plt.xlabel(
        "Risk Diffusion (Environmental Volatility)"
    )

    plt.ylabel("Sustainability Index")

    plt.title(
        "Stress Test: Robustness to Environmental Change"
    )

    plt.grid(True)

    plt.tight_layout()

    if save_path:
        plt.savefig(
            save_path,
            dpi=300,
            bbox_inches="tight"
        )

    plt.show()
