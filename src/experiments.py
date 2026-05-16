"""
experiments.py

Experimental evaluation pipeline for the Energy-Aware Agentic Geo-AI framework.

This module contains:
- episode execution,
- benchmark experiments,
- stress testing,
- aggregate performance evaluation.

The experiments compare:
- constraint-only agents,
- utility-based agents,
- utility + outcome learning agents.

The evaluation focuses on:
- energy efficiency,
- monitoring coverage,
- sustainability,
- robustness under environmental volatility.
"""

import pandas as pd

from environment import GeoEnvironment
from agent import (
    EnergyAwareAgent,
    OperationalPriorities
)


# -------------------------------------------------------------------
# Episode Execution
# -------------------------------------------------------------------

def run_episode(env, agent, train=True):
    """
    Execute one monitoring episode.

    Args:
        env:
            Geo-environment instance.

        agent:
            Monitoring agent.

        train:
            Enables lightweight online learning.

    Returns:
        Dictionary containing experiment metrics.
    """

    state = env.reset()

    coverage = 0.0

    risk_sum = 0.0

    coverage_over_time = []

    while True:

        # -----------------------------------------------------------
        # Action selection
        # -----------------------------------------------------------
        action = agent.select_action(
            state,
            env
        )

        # -----------------------------------------------------------
        # Environment interaction
        # -----------------------------------------------------------
        next_state, outcome, done = env.step(action)

        coverage += outcome["coverage_gain"]

        risk_sum += outcome["observed_risk"]

        coverage_over_time.append(coverage)

        # -----------------------------------------------------------
        # Decision logging for visualization and analysis
        # -----------------------------------------------------------
        if hasattr(agent, "decision_log"):

            agent.decision_log.append({
                "step": env.steps,
                "action": action,
                "energy": state.energy,
                "risk": state.local_risk,
                "coverage": state.local_coverage,
                "position": state.position
            })

        # -----------------------------------------------------------
        # Lightweight online learning
        # -----------------------------------------------------------
        if train:

            agent.store(
                state,
                action,
                outcome
            )

            agent.train()

        state = next_state

        if done:
            break

    # ---------------------------------------------------------------
    # Aggregate evaluation metrics
    # ---------------------------------------------------------------
    energy_used = env.init_energy - env.energy

    sustainability = (
        coverage / (energy_used + 1e-6)
    )

    avg_risk = (
        risk_sum / max(env.steps, 1)
    )

    return {
        "energy_used": energy_used,
        "coverage": coverage,
        "sustainability": sustainability,
        "avg_risk": avg_risk,
        "steps": env.steps,
        "coverage_over_time": coverage_over_time
    }


# -------------------------------------------------------------------
# Benchmark Experiment
# -------------------------------------------------------------------

def benchmark_experiment():
    """
    Execute the primary benchmark evaluation used in the paper.

    Compares:
    - constraint-only agent,
    - utility-based agent,
    - utility + outcome learning agent.

    Returns:
        DataFrame containing all experiment results.
    """

    agent_results = []

    seeds = range(5)

    volatility_levels = [0.005, 0.02, 0.06]

    trials_per_setting = 25

    for seed in seeds:

        for volatility in volatility_levels:

            for trial in range(trials_per_setting):

                env_seed = seed * 1000 + trial

                env_config = {
                    "seed": env_seed,
                    "risk_diffusion": volatility
                }

                # ===================================================
                # Constraint-only agent
                # ===================================================

                env = GeoEnvironment(**env_config)

                agent = EnergyAwareAgent(
                    model_type="linear"
                )

                agent.energy_margin = 30.0

                agent.set_priorities(
                    OperationalPriorities(
                        risk_weight=0.0,
                        energy_weight=0.0,
                        coverage_weight=0.0
                    )
                )

                agent.trained = False

                result = run_episode(
                    env,
                    agent,
                    train=False
                )

                agent_results.append({
                    "Agent": "Constraint-only agent",
                    "Seed": seed,
                    "Volatility": volatility,
                    "Trial": trial,
                    **result
                })

                # ===================================================
                # Utility-based agent
                # ===================================================

                env = GeoEnvironment(**env_config)

                agent = EnergyAwareAgent(
                    model_type="linear"
                )

                agent.energy_margin = 15.0

                agent.set_priorities(
                    OperationalPriorities(
                        risk_weight=0.3,
                        energy_weight=2.0,
                        coverage_weight=0.2,
                        risk_aversion=0.0
                    )
                )

                result = run_episode(
                    env,
                    agent,
                    train=False
                )

                agent_results.append({
                    "Agent": "Utility-based agent",
                    "Seed": seed,
                    "Volatility": volatility,
                    "Trial": trial,
                    **result
                })

                # ===================================================
                # Utility + outcome learning agent
                # ===================================================

                env = GeoEnvironment(**env_config)

                agent = EnergyAwareAgent(
                    model_type="tree"
                )

                agent.energy_margin = 5.0

                agent.set_priorities(
                    OperationalPriorities(
                        risk_weight=2.0,
                        energy_weight=0.3,
                        coverage_weight=1.5,
                        risk_aversion=0.7
                    )
                )

                result = run_episode(
                    env,
                    agent,
                    train=True
                )

                agent_results.append({
                    "Agent":
                    "Utility + outcome learning agent",

                    "Seed": seed,

                    "Volatility": volatility,

                    "Trial": trial,

                    **result
                })

    return pd.DataFrame(agent_results)


# -------------------------------------------------------------------
# Performance Summary
# -------------------------------------------------------------------

def generate_performance_summary(df_agents):
    """
    Generate the aggregate performance summary table.

    Returns:
        Simplified paper-aligned performance table.
    """

    summary = (
        df_agents
        .groupby("Agent")
        .agg(
            Energy_Used=("energy_used", "mean"),
            Coverage=("coverage", "mean"),
            Sustainability=("sustainability", "mean")
        )
        .round(2)
    )

    return summary


# -------------------------------------------------------------------
# Stress Test Experiment
# -------------------------------------------------------------------

def stress_test_experiment(model_type="tree"):
    """
    Evaluate robustness under increasing environmental volatility.

    Risk diffusion controls environmental uncertainty.
    """

    diffusion_levels = [0.005, 0.02, 0.05, 0.1]

    results = []

    agent = EnergyAwareAgent(
        model_type=model_type
    )

    agent.set_priorities(
        OperationalPriorities(
            risk_weight=1.2,
            energy_weight=1.0,
            coverage_weight=1.2,
            risk_aversion=0.7
        )
    )

    agent.energy_margin = 5.0

    # ---------------------------------------------------------------
    # Lightweight pretraining phase
    # ---------------------------------------------------------------
    for seed in range(5):

        env_train = GeoEnvironment(seed=seed)

        run_episode(
            env_train,
            agent,
            train=True
        )

    # ---------------------------------------------------------------
    # Volatility evaluation
    # ---------------------------------------------------------------
    for rd in diffusion_levels:

        env = GeoEnvironment(
            risk_diffusion=rd,
            seed=0
        )

        results_dict = run_episode(
            env,
            agent,
            train=False
        )

        results.append({
            "RiskDiffusion": rd,
            "Sustainability":
            results_dict["sustainability"],

            "Energy":
            results_dict["energy_used"],

            "Coverage":
            results_dict["coverage"]
        })

    return pd.DataFrame(results)
