# Interpretation of Results

## Overview

The experimental results demonstrate how explicit utility-based reasoning influences environmental monitoring behavior under spatial and energy constraints.

The framework focuses on:
- interpretability,
- sustainability,
- lightweight reasoning,
- controlled decision-making.

---

# Constraint-Only Agent

The constraint-only agent achieves high monitoring coverage but exhibits:
- higher energy consumption,
- inconsistent behavior,
- reduced long-term efficiency.

Because the agent lacks utility reasoning, movement decisions are less strategically balanced.

---

# Utility-Based Agent

The utility-based agent introduces explicit trade-offs between:
- risk,
- energy,
- coverage.

However, without outcome learning, the agent may still produce inefficient decisions due to imperfect outcome estimation.

This results in:
- lower coverage,
- higher energy use,
- reduced sustainability.

---

# Utility + Outcome Learning Agent

The learning-augmented agent achieves the most balanced monitoring behavior.

Lightweight outcome learning improves:
- action outcome estimation,
- consistency,
- long-term monitoring efficiency.

Importantly, learning does not directly control actions.

Decision-making remains:
- interpretable,
- utility-driven,
- explicitly constrained.

---

# Energy–Coverage Trade-Off

The trade-off analysis demonstrates that the learning-augmented agent maintains:
- moderate-to-high coverage,
- lower energy consumption,
- improved sustainability.

The results suggest that lightweight outcome learning improves monitoring efficiency without requiring end-to-end policy learning.

---

# Coverage Accumulation

Coverage accumulation analysis shows that:
- the constraint-only agent plateaus early,
- the utility-based agent behaves inconsistently,
- the learning-augmented agent maintains more stable long-term accumulation.

This suggests improved long-term monitoring behavior.

---

# Robustness Under Environmental Volatility

Stress testing demonstrates that the framework maintains stable sustainability even as environmental uncertainty increases.

This indicates:
- adaptive monitoring behavior,
- stable reasoning,
- robustness under dynamic conditions.

---

# Interpretability

One of the central goals of the framework is interpretability.

The framework preserves explicit reasoning through:
- utility weighting,
- rule-based feasibility constraints,
- transparent operational priorities.

Unlike black-box policies, the decision process remains understandable and controllable.

---

# Overall Conclusion

The experiments suggest that:
- lightweight utility reasoning,
- combined with lightweight outcome learning,

can support effective and interpretable environmental monitoring behavior under energy and environmental constraints.

The framework demonstrates that explainable decision-centric Geo-AI systems can achieve balanced monitoring performance without relying on computationally expensive policy learning methods.
