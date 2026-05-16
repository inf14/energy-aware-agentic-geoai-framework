# Utility-Based Reasoning

## Overview

The framework uses explicit utility-based reasoning instead of end-to-end policy learning.

The monitoring agent evaluates possible actions using a utility score that balances:
- monitoring coverage,
- environmental risk,
- energy consumption.

This creates a transparent and interpretable decision-making process.

---

# Why Utility-Based Reasoning?

Many autonomous systems rely on:
- reinforcement learning,
- black-box policies,
- implicit reward optimization.

While powerful, these methods often reduce interpretability.

This framework instead focuses on:
- explicit trade-offs,
- understandable decisions,
- controllable operational priorities.

---

# Utility Function

For every feasible action, the agent computes a utility value.

The utility balances:
- expected coverage improvement,
- estimated energy cost,
- environmental risk exposure.

Higher utility actions are preferred during action selection.

---

# Coverage Contribution

Coverage improvement increases utility.

This encourages the agent to:
- monitor unexplored regions,
- maintain environmental awareness,
- revisit stale areas affected by coverage decay.

An additional exploration bonus promotes broader monitoring behavior.

---

# Energy Penalty

Energy consumption reduces utility.

This encourages:
- efficient movement,
- energy-aware monitoring,
- sustainable long-duration operation.

Energy-aware reasoning is especially important in autonomous monitoring systems operating under limited resources.

---

# Risk Awareness

Environmental risk influences action desirability.

The framework also includes:
- configurable risk weighting,
- optional risk aversion.

Risk aversion increases penalties in highly dangerous regions, producing more cautious behavior.

---

# Explicit Trade-Offs

One of the key goals of the framework is explicit reasoning.

The operational priorities can be adjusted directly through:
- risk weights,
- energy weights,
- coverage weights.

This makes the decision process:
- understandable,
- controllable,
- interpretable.

---

# Separation Between Rules and Utility

The framework separates:
1. feasibility constraints,
2. utility evaluation,
3. outcome learning.

Unsafe actions are removed before utility evaluation.

This guarantees:
- operational safety,
- interpretable behavior,
- constrained decision-making.

---

# Lightweight Outcome Learning

Learning does not directly control actions.

Instead, lightweight supervised learning models estimate:
- expected energy cost,
- expected coverage gain,
- expected environmental risk.

The utility function then uses these estimates during reasoning.

This preserves explicit decision-making while improving outcome prediction quality.

---

# Design Philosophy

The framework emphasizes:
- interpretability,
- lightweight reasoning,
- explicit operational priorities,
- transparent autonomous behavior.

The goal is not to maximize black-box optimization performance, but to study explainable and energy-aware environmental monitoring behavior.
