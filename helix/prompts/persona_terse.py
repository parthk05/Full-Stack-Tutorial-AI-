"""
Step 2.4 — Persona: terse ops voice

Theory (personas):
  Contrasts with persona_hr — same role (Helix), different delivery constraints.
  Useful to see how much of "behavior" is prompt-controlled vs model default.

When to use:
  - Slack/ops bots where brevity beats empathy
  - Side-by-side demos of prompt control over tone
"""

# Step 2.4.1 — strategy id
STRATEGY_ID = "persona_terse"

# Step 2.4.1 — minimal wording
PERSONA_TERSE_SYSTEM_PROMPT = """You are Helix in terse mode for Meridian Labs.

Reply in at most 2 short sentences or a 3-bullet list.
No pleasantries, no hedging essays, no follow-up offers.
"""
