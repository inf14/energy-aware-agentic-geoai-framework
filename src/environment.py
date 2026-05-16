"""
environment.py

Core geo-environment simulation for the Energy-Aware Agentic Geo-AI framework.

This module defines:
- the environment state representation,
- the spatial monitoring environment,
- environmental dynamics,
- risk diffusion,
- coverage decay,
- terrain-dependent energy cost.

The environment is intentionally lightweight and interpretable,
allowing controlled experimentation without requiring high-fidelity simulation.
"""

import numpy as np

from dataclasses import dataclass


# -------------------------------------------------------------------
# Environment State Representation
# -------------------------------------------------------------------

@dataclass
class EnvState:
    """
    Represents the local observable state perceived by the agent.

    Attributes:
        position:
            Current agent position in the environment grid.

        energy:
            Remaining agent energy.

        local_risk:
            Environmental risk at the current location.

        local_cost:
            Terrain-dependent movement cost.

        local_coverage:
            Monitoring coverage value at the current location.

        neighborhood_risk:
            Local surrounding risk map.

        neighborhood_coverage:
            Local surrounding coverage map.
    """

    position: tuple
    energy: float
    local_risk: float
    local_cost: float
    local_coverage: float
    neighborhood_risk: np.ndarray
    neighborhood_coverage: np.ndarray


# -------------------------------------------------------------------
# Geo-Environment Simulation
# -------------------------------------------------------------------

class GeoEnvironment:
    """
    Lightweight spatial monitoring environment.

    The environment is represented as a two-dimensional grid where
    each cell contains:

    - environmental risk,
    - terrain-dependent movement cost,
    - monitoring coverage information.

    The environment evolves dynamically through:
    - risk diffusion,
    - coverage decay,
    - repeated traversal penalties.
    """

    def __init__(
        self,
        size=30,
        max_steps=400,
        init_energy=600,
        perception_radius=1,
        coverage_decay=0.05,
        risk_diffusion=0.02,
        seed=None
    ):
        """
        Initialize the environment.

        Args:
            size:
                Width and height of the environment grid.

            max_steps:
                Maximum episode duration.

            init_energy:
                Initial available energy for the agent.

            perception_radius:
                Local observation radius around the agent.

            coverage_decay:
                Rate at which monitoring information becomes outdated.

            risk_diffusion:
                Environmental volatility factor controlling
                dynamic risk evolution.

            seed:
                Random seed for reproducibility.
        """

        if seed is not None:
            np.random.seed(seed)

        self.size = size
        self.max_steps = max_steps
        self.init_energy = init_energy
        self.perception_radius = perception_radius
        self.coverage_decay = coverage_decay
        self.risk_diffusion = risk_diffusion

        # -----------------------------------------------------------
        # Risk map:
        # Represents environmental hazard intensity.
        # -----------------------------------------------------------
        self.risk_map = self.smooth_map(
            np.random.rand(size, size)
        )

        # -----------------------------------------------------------
        # Terrain cost map:
        # Represents movement difficulty and energy cost.
        # -----------------------------------------------------------
        self.terrain_cost = self.smooth_map(
            0.2 + 2.0 * np.random.rand(size, size)
        )

        self.reset()

    # -------------------------------------------------------------------

    def smooth_map(self, mat, iterations=3):
        """
        Smooth spatial maps to create more realistic terrain structure.

        This avoids completely random environments by introducing
        spatial continuity between neighboring cells.
        """

        for _ in range(iterations):
            mat = (
                mat +
                np.roll(mat, 1, axis=0) +
                np.roll(mat, -1, axis=0) +
                np.roll(mat, 1, axis=1) +
                np.roll(mat, -1, axis=1)
            ) / 5.0

        return mat

    # -------------------------------------------------------------------

    def reset(self):
        """
        Reset the environment to the initial episode state.
        """

        self.agent_pos = [
            np.random.randint(0, self.size),
            np.random.randint(0, self.size)
        ]

        self.energy = self.init_energy

        # -----------------------------------------------------------
        # Coverage map:
        # Stores how recently regions have been monitored.
        # -----------------------------------------------------------
        self.coverage_map = np.zeros((self.size, self.size))

        # -----------------------------------------------------------
        # Visit map:
        # Tracks repeated traversal through locations.
        # -----------------------------------------------------------
        self.visit_map = np.zeros((self.size, self.size))

        self.cumulative_risk = 0.0
        self.risk_steps = 0

        self.steps = 0
        self.done = False

        return self.observe()

    # -------------------------------------------------------------------

    def valid_actions(self):
        """
        Return the available action space.
        """

        return [
            "UP",
            "DOWN",
            "LEFT",
            "RIGHT",
            "STAY",
            "SCAN"
        ]

    # -------------------------------------------------------------------

    def _clip(self, x, y):
        """
        Keep coordinates inside environment boundaries.
        """

        return (
            int(np.clip(x, 0, self.size - 1)),
            int(np.clip(y, 0, self.size - 1))
        )

    # -------------------------------------------------------------------

    def _neighborhood(self, mat, x, y):
        """
        Extract local neighborhood information around the agent.
        """

        r = self.perception_radius

        return mat[
            max(0, x - r):min(self.size, x + r + 1),
            max(0, y - r):min(self.size, y + r + 1)
        ]

    # -------------------------------------------------------------------

    def observe(self):
        """
        Generate the local observable state perceived by the agent.
        """

        x, y = self.agent_pos

        return EnvState(
            position=(x, y),
            energy=self.energy,
            local_risk=self.risk_map[x, y],
            local_cost=self.terrain_cost[x, y],
            local_coverage=self.coverage_map[x, y],
            neighborhood_risk=self._neighborhood(
                self.risk_map,
                x,
                y
            ),
            neighborhood_coverage=self._neighborhood(
                self.coverage_map,
                x,
                y
            )
        )

    # -------------------------------------------------------------------

    def diffuse_risk(self):
        """
        Simulate environmental volatility through stochastic diffusion.

        Risk values evolve dynamically during simulation,
        creating uncertainty and changing monitoring conditions.
        """

        noise = (
            np.random.randn(self.size, self.size)
            * self.risk_diffusion
        )

        self.risk_map = np.clip(
            self.risk_map + noise,
            0,
            1
        )

    # -------------------------------------------------------------------

    def step(self, action):
        """
        Execute an action inside the environment.

        Returns:
            next_state,
            outcome dictionary,
            done flag.
        """

        if self.done:
            raise RuntimeError("Episode finished")

        x, y = self.agent_pos

        # ===========================================================
        # SCAN ACTION
        # ===========================================================

        if action == "SCAN":

            energy_cost = 1.2

            observed_risk = np.mean(
                self._neighborhood(
                    self.risk_map,
                    x,
                    y
                )
            )

            # -------------------------------------------------------
            # Coverage decay:
            # Simulates environmental information becoming outdated.
            # Regions that are not revisited gradually lose
            # monitoring quality.
            # -------------------------------------------------------
            self.coverage_map[x, y] = max(
                self.coverage_map[x, y] - 0.2,
                0.0
            )

            coverage_gain = 0.05

            self.energy -= energy_cost
            self.steps += 1

            if (
                self.energy <= 0
                or self.steps >= self.max_steps
            ):
                self.done = True

            return self.observe(), {
                "energy_cost": energy_cost,
                "coverage_gain": coverage_gain,
                "observed_risk": observed_risk
            }, self.done

        # ===========================================================
        # MOVEMENT ACTIONS
        # ===========================================================

        nx, ny = x, y

        if action == "UP":
            nx -= 1

        elif action == "DOWN":
            nx += 1

        elif action == "LEFT":
            ny -= 1

        elif action == "RIGHT":
            ny += 1

        nx, ny = self._clip(nx, ny)

        # -----------------------------------------------------------
        # Terrain-dependent movement cost
        # -----------------------------------------------------------
        energy_cost = self.terrain_cost[nx, ny]

        # -----------------------------------------------------------
        # Repeated traversal penalty
        # -----------------------------------------------------------
        energy_cost += 0.4 * self.visit_map[nx, ny]

        # -----------------------------------------------------------
        # Risk-aware movement penalty
        # -----------------------------------------------------------
        energy_cost *= (
            1.0 + 2.0 * self.risk_map[nx, ny]
        )

        self.energy -= energy_cost

        self.agent_pos = [nx, ny]

        self.visit_map[nx, ny] += 1

        # -----------------------------------------------------------
        # Coverage decay:
        # Monitoring quality decreases over time if locations are
        # not revisited.
        # -----------------------------------------------------------
        self.coverage_map *= (
            1 - self.coverage_decay
        )

        neighbor_cov = np.mean(
            self._neighborhood(
                self.coverage_map,
                nx,
                ny
            )
        )

        coverage_gain = max(
            0.0,
            0.4 - neighbor_cov
        )

        self.coverage_map[nx, ny] += coverage_gain

        observed_risk = self.risk_map[nx, ny]

        self.cumulative_risk += observed_risk
        self.risk_steps += 1

        # -----------------------------------------------------------
        # Dynamic environmental evolution
        # -----------------------------------------------------------
        self.diffuse_risk()

        self.steps += 1

        if (
            self.energy <= 0
            or self.steps >= self.max_steps
        ):
            self.done = True

        return self.observe(), {
            "energy_cost": energy_cost,
            "coverage_gain": coverage_gain,
            "observed_risk": observed_risk
        }, self.done
