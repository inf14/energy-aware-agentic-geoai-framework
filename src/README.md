# Source Code Overview

This directory contains the core implementation of the lightweight decision-centric Geo-AI framework.

---

# File Structure

| File | Purpose |
|---|---|
| environment.py | Geo-environment simulation and state representation |
| agent.py | Energy-aware monitoring agent and utility reasoning |
| experiments.py | Experimental setup and evaluation pipeline |
| visualization.py | Figure generation and visualization utilities |

---

# Framework Flow

The framework follows the following interaction pipeline:

```text
Environment → State Observation → Rule Filtering → Utility Evaluation → Action Selection → Outcome Learning
```

---

# Environment

The environment models:
- spatial environmental risk,
- terrain-dependent energy cost,
- monitoring coverage,
- dynamic environmental volatility.

The environment evolves during simulation through:
- risk diffusion,
- coverage decay,
- repeated traversal penalties.

---

# Agent

The monitoring agent:
- operates under partial observability,
- applies feasibility constraints,
- evaluates actions using utility reasoning,
- optionally improves outcome estimation using lightweight online learning.

---

# Utility-Based Decision Making

Actions are selected by balancing:
- coverage improvement,
- environmental risk,
- energy consumption.

This preserves:
- interpretability,
- explicit trade-offs,
- transparent decision behavior.

---

# Outcome Learning

Learning is used only for outcome estimation.

The framework does NOT use:
- reinforcement learning,
- end-to-end policy learning,
- black-box control policies.

Instead, lightweight supervised learning models estimate:
- expected energy cost,
- expected coverage gain,
- expected environmental risk.

---

# Experimental Evaluation

The experiments compare:
- constraint-only agents,
- utility-based agents,
- utility + outcome learning agents.

Evaluation focuses on:
- energy efficiency,
- monitoring coverage,
- sustainability,
- robustness under environmental volatility.
