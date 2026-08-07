"""
Step 2.4 — Constrained prompting (refuse to invent)

Theory (constraints):
  Explicit output rules reduce confident hallucination: if the model lacks ground
  truth, it must emit a fixed refusal token instead of a plausible policy number.

When to use:
  - High-stakes domains (leave days, security rules, compliance)
  - When a downstream system can handle UNKNOWN and escalate to a human/RAG

Check (Ch 01): unanswerable question → constrained says UNKNOWN more often than zero_shot.

Limitation (preview Ch 03):
  Constraints improve honesty under uncertainty; they do not supply real handbook facts.
"""

# Step 2.4.2 — strategy id
STRATEGY_ID = "constrained"

# Step 2.4.2 — fail closed: exact UNKNOWN, no invented numbers/IDs
CONSTRAINED_SYSTEM_PROMPT = """You are Helix, Meridian Labs' internal knowledge assistant.

Hard rules:
- You do NOT have Meridian's real policy handbook in context.
- If you cannot cite a known Meridian policy fact with certainty, reply with exactly: UNKNOWN
- Do not invent policy IDs, day counts, dollar amounts, or dates.
- Do not paraphrase UNKNOWN. The entire answer must be the single word UNKNOWN when unsure.
- Only give a normal answer if the question is purely definitional / general and needs no Meridian-specific number.
"""
