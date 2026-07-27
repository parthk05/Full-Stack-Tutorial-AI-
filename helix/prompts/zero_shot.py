"""
Step 2.1 — Zero-shot system prompt for Helix Prompt Desk

Theory (zero-shot):
  Send only a role/instruction (system) + the task (user). No worked examples.
  The model relies on pretraining + the instruction — not on demonstrated Q&A pairs.

When to use:
  - Fast baseline for open-ended answers
  - You do not yet have good examples, or the task format is obvious from the instruction
  - Comparing later strategies (few-shot / CoT / constraints) against a simple control

When NOT enough alone (preview of later chapters):
  - Private Meridian facts the model never saw → invents plausible policy (hallucination)
  - Strict output shapes or classification → few-shot / structured outputs help more
"""

# Step 2.1.3 — identity + domain; intentionally no policy facts and no example Q&A
ZERO_SHOT_SYSTEM_PROMPT = """You are Helix, Meridian Labs' internal knowledge assistant.

Answer employee questions about company policies clearly and helpfully.
Be concise. If you are unsure, still give your best helpful answer based on typical
corporate policy patterns — do not refuse solely because you lack a handbook.

Provide a concise answer
"""

# Step 2.1 — strategy id returned in API responses and used for routing
STRATEGY_ID = "zero_shot"
