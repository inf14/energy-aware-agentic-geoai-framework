# Experimental Setup

## Overview

The framework is evaluated through controlled simulation experiments designed to study:
- energy efficiency,
- monitoring coverage,
- sustainability,
- robustness under environmental volatility.

Multiple independent trials are performed across different random seeds and environmental conditions.

---

# Agent Configurations

Three agent configurations are evaluated.

---

## Constraint-Only Agent

The constraint-only agent uses:
- rule-based feasibility filtering,
- no utility reasoning,
- no learning.

This agent serves as a baseline representing conservative constrained behavior.

---

## Utility-Based Agent

The utility-based agent uses:
- utility reasoning,
- explicit trade-offs,
- no learning.

This evaluates the effect of explicit decision-centric reasoning without outcome estimation.

---

## Utility + Outcome Learning Agent

The learning-augmented agent combines:
- utility reasoning,
- lightweight online learning,
- outcome estimation.

Learning improves prediction quality without directly controlling actions.

---

# Experimental Environment

The experiments use:
- randomly generated risk maps,
- terrain-dependent movement cost,
- dynamic environmental volatility,
- monitoring coverage dynamics.

Environmental volatility is controlled using risk diffusion.

---

# Evaluation Metrics

## Energy Used

Measures total energy consumption during monitoring.

Lower energy consumption indicates greater operational efficiency.

---

## Coverage

Measures accumulated monitoring coverage achieved during the episode.

Higher coverage indicates more effective environmental monitoring.

---

## Sustainability

Defined as:

Coverage / Energy Used

This measures how efficiently monitoring coverage is achieved relative to energy consumption.

---

# Coverage Accumulation Analysis

Coverage accumulation curves evaluate:
- long-term monitoring behavior,
- sustained exploration,
- monitoring stability over time.

---

# Stress Testing

Stress tests evaluate robustness under increasing environmental volatility.

Environmental uncertainty is increased through higher risk diffusion levels.

The experiments analyze whether the monitoring framework maintains stable sustainability under changing conditions.

---

# Experimental Philosophy

The experiments focus on:
- interpretability,
- controlled comparison,
- explicit reasoning behavior,
- lightweight autonomous monitoring.

The framework is designed as a lightweight experimental platform rather than a high-fidelity robotics simulator.
