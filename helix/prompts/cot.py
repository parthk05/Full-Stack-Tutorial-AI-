"""
Step 2.3 — Chain-of-thought (CoT) for Helix Prompt Desk

Theory (chain-of-thought):
  Ask the model to write brief intermediate reasoning before the final answer.
  This can improve multi-step or comparative questions by forcing staged thinking.

When to use:
  - Questions that need several logical steps (eligibility + exceptions + numbers)
  - Debugging why the model chose an answer (reasoning is visible in the reply)

Tradeoff (notes prompt): *Latency/cost?*
  CoT generates more tokens → higher latency and cost than a direct answer.
  Prefer CoT when accuracy on hard questions matters more than speed/budget.

When NOT to use:
  - Simple lookups or classification where few-shot already works
  - High-QPS endpoints where extra tokens dominate cost
"""

# Step 2.3 — strategy id for API routing
STRATEGY_ID = "cot"

# Step 2.3.1 — ask for short reasoning, then a clearly marked final answer
COT_SYSTEM_PROMPT = """You are Helix, Meridian Labs' internal knowledge assistant.

For every question:
1) Write a short Reasoning section (2–4 bullet points max).
2) Then write a Final answer section with the concise reply an employee would read.

Format exactly:
Reasoning:
- ...
Final answer:
...
"""
