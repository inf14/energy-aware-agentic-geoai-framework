"""
agent.py

Energy-aware monitoring agent for the lightweight Geo-AI framework.

This module implements:
- operational priorities,
- utility-based reasoning,
- rule-based feasibility filtering,
- lightweight online outcome learning,
- interpretable action selection.

The framework intentionally separates:
- safety constraints,
- utility reasoning,
- learning.

This preserves interpretability and explicit decision-making.
"""

import random
import numpy as np

from dataclasses import dataclass

from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor


# -------------------------------------------------------------------
# Operational Priorities
# -------------------------------------------------------------------

@dataclass
class OperationalPriorities:
    """
    Encodes the relative importance of monitoring objectives.

    Attributes:
        risk_weight:
            Importance assigned to environmental risk.

        energy_weight:
            Importance assigned to energy efficiency.

        coverage_weight:
            Importance assigned to monitoring coverage.

        risk_aversion:
            Additional penalty for high-risk situations.
    """

    risk_weight: float
    energy_weight: float
    coverage_weight: float
    risk_aversion: float = 0.0


# -------------------------------------------------------------------
# Energy-Aware Monitoring Agent
# -------------------------------------------------------------------

class EnergyAwareAgent:
    """
    Lightweight autonomous monitoring agent.

    The agent operates using:
    - feasibility constraints,
    - utility-based reasoning,
    - optional lightweight outcome learning.

    The framework avoids end-to-end policy learning
    and instead relies on explicit interpretable reasoning.
    """

    def __init__(self, model_type="linear"):
        """
        Initialize the monitoring agent.

        Args:
            model_type:
                Lightweight supervised learning model used for
                outcome estimation.
        """

        # -----------------------------------------------------------
        # Utility weights
        # -----------------------------------------------------------
        self.w_risk = 1.0
        self.w_energy = 1.0
        self.w_coverage = 1.0

        # -----------------------------------------------------------
        # Minimum safe operating energy threshold
        # -----------------------------------------------------------
        self.energy_margin = 10.0

        # -----------------------------------------------------------
        # Additional risk sensitivity factor
        # -----------------------------------------------------------
        self.risk_aversion = 0.0

        # -----------------------------------------------------------
        # Decision logging for interpretability and visualization
        # -----------------------------------------------------------
        self.decision_log = []

        # -----------------------------------------------------------
        # Lightweight outcome learning models
        # -----------------------------------------------------------
        if model_type == "linear":

            self.model = LinearRegression()

        elif model_type == "tree":

            self.model = DecisionTreeRegressor(
                max_depth=3
            )

        elif model_type == "forest":

            self.model = RandomForestRegressor(
                n_estimators=50,
                max_depth=5,
                random_state=0
            )

        else:
            raise ValueError("Unknown model type")

        self.model_type = model_type

        self.memory = []

        self.trained = False

    # -------------------------------------------------------------------

    def featurize(self, state, action):
        """
        Convert state-action information into numerical features.

        The features describe:
        - spatial position,
        - local environmental conditions,
        - neighborhood information,
        - selected action.
        """

        action_space = [
            "UP",
            "DOWN",
            "LEFT",
            "RIGHT",
            "STAY",
            "SCAN"
        ]

        action_vec = [
            1 if action == a else 0
            for a in action_space
        ]

        return np.array([
            state.position[0],
            state.position[1],
            state.energy,
            state.local_risk,
            state.local_cost,
            state.local_coverage,
            np.mean(state.neighborhood_risk),
            np.mean(state.neighborhood_coverage)
        ] + action_vec)

    # -------------------------------------------------------------------

    def apply_rules(self, state, actions):
        """
        Apply feasibility constraints before utility reasoning.

        This guarantees:
        - operational safety,
        - minimum energy availability,
        - basic risk avoidance.

        Unsafe actions are removed before evaluation.
        """

        feasible = []

        for action in actions:

            # -------------------------------------------------------
            # Prevent unsafe movement under low energy conditions
            # -------------------------------------------------------
            if (
                state.energy < self.energy_margin
                and action not in ["STAY", "SCAN"]
            ):
                continue

            # -------------------------------------------------------
            # Prevent dangerous movement in extremely risky regions
            # -------------------------------------------------------
            if (
                state.local_risk > 0.85
                and action != "SCAN"
            ):
                continue

            feasible.append(action)

        return feasible

    # -------------------------------------------------------------------

    def predict_outcome(self, state, action):
        """
        Estimate the outcome of an action.

        Before training:
            Uses simple heuristic estimates.

        After training:
            Uses lightweight learned outcome prediction.
        """

        # -----------------------------------------------------------
        # Heuristic outcome estimation before learning
        # -----------------------------------------------------------
        if not self.trained:

            return {
                "energy_cost": state.local_cost,
                "coverage_gain": 1 - state.local_coverage,
                "observed_risk": state.local_risk
            }

        # -----------------------------------------------------------
        # Lightweight sensing estimate for SCAN action
        # -----------------------------------------------------------
        if action == "SCAN":

            return {
                "energy_cost": 0.6,
                "coverage_gain": 0.15,
                "observed_risk": np.mean(
                    state.neighborhood_risk
                )
            }

        X = self.featurize(
            state,
            action
        ).reshape(1, -1)

        y = self.model.predict(X)[0]

        return {
            "energy_cost": max(y[0], 0),
            "coverage_gain": max(y[1], 0),
            "observed_risk": max(y[2], 0)
        }

    # -------------------------------------------------------------------

    def utility(self, pred):
        """
        Compute the utility score for a candidate action.

        The utility function explicitly balances:
        - environmental risk,
        - energy consumption,
        - monitoring coverage.

        Higher utility actions are preferred.

        This explicit formulation preserves interpretability
        and transparent decision-making.
        """

        risk = pred["observed_risk"]

        # -----------------------------------------------------------
        # Risk aversion increases penalty for dangerous situations
        # -----------------------------------------------------------
        risk_adjusted = (
            risk
            + self.risk_aversion * (risk ** 2)
        )

        coverage_gain = pred["coverage_gain"]

        energy_cost = pred["energy_cost"]

        # -----------------------------------------------------------
        # Exploration bonus encourages broader monitoring behavior
        # -----------------------------------------------------------
        exploration_bonus = 0.2 * coverage_gain

        # -----------------------------------------------------------
        # Utility-based trade-off balancing
        # -----------------------------------------------------------
        utility_value = (
            self.w_risk * risk_adjusted
            + self.w_coverage * coverage_gain
            - self.w_energy * energy_cost
            + exploration_bonus
        )

        return utility_value

    # -------------------------------------------------------------------

    def select_action(self, state, env, epsilon=0.02):
        """
        Select the next agent action.

        Decision pipeline:
        1. Apply feasibility constraints
        2. Predict action outcomes
        3. Compute utility scores
        4. Select highest utility action

        A small epsilon-greedy exploration factor is used
        to avoid deterministic behavior.
        """

        actions = self.apply_rules(
            state,
            env.valid_actions()
        )

        # -----------------------------------------------------------
        # Early exploration phase
        # -----------------------------------------------------------
        if env.steps < 3:

            return np.random.choice(actions)

        # -----------------------------------------------------------
        # Constraint-only agent behavior
        # -----------------------------------------------------------
        if (
            self.w_risk == 0.0
            and self.w_energy == 0.0
            and self.w_coverage == 0.0
        ):

            return random.choice(actions)

        scored = [
            (
                action,
                self.utility(
                    self.predict_outcome(
                        state,
                        action
                    )
                )
            )
            for action in actions
        ]

        utilities = np.array([
            u for _, u in scored
        ])

        # -----------------------------------------------------------
        # Epsilon-greedy exploration
        # -----------------------------------------------------------
        if np.random.rand() < epsilon:

            return np.random.choice([
                a for a, _ in scored
            ])

        return scored[np.argmax(utilities)][0]

    # -------------------------------------------------------------------

    def set_priorities(self, priorities):
        """
        Configure operational objective weights.
        """

        self.w_risk = priorities.risk_weight

        self.w_energy = priorities.energy_weight

        self.w_coverage = priorities.coverage_weight

        self.risk_aversion = priorities.risk_aversion

    # -------------------------------------------------------------------

    def store(self, state, action, outcome):
        """
        Store experience for lightweight online learning.
        """

        X = self.featurize(state, action)

        y = np.array([
            outcome["energy_cost"],
            outcome["coverage_gain"],
            outcome["observed_risk"]
        ])

        self.memory.append((X, y))

    # -------------------------------------------------------------------

    def train(self):
        """
        Train the lightweight outcome estimation model.

        Learning is used only for outcome prediction,
        not direct policy control.
        """

        if len(self.memory) < 20:
            return

        X = np.array([
            m[0] for m in self.memory
        ])

        y = np.array([
            m[1] for m in self.memory
        ])

        self.model.fit(X, y)

        self.trained = True
