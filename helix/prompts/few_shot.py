"""
Step 2.2 — Few-shot prompting for Helix Prompt Desk

Theory (few-shot):
  Include 2–N worked input→output examples in the prompt so the model imitates
  the demonstrated format, labels, and style — not just the written instructions.

When to use:
  - Classification / routing / extraction where the output shape is picky
  - When a long instruction still yields messy labels, but 3 clear examples fix it
  - Teaching tone or company-specific phrasing without fine-tuning

When zero-shot is enough:
  - Open-ended prose where format is obvious and labels are not required

Notes prompt (Ch 01): *When do examples beat a longer instruction?*
  Examples win when the model must match a discrete schema (e.g. hr|security|finance)
  or a subtle style that is hard to describe in words alone.
"""

# Step 2.2 — strategy id for API routing
STRATEGY_ID = "few_shot"

# Step 2.2.1 — synthetic Meridian Q→label examples (classification / routing).
# Why classification here: Step 2.2 Check compares few-shot vs zero-shot on routing.
FEW_SHOT_SYSTEM_PROMPT = """You are Helix, Meridian Labs' internal knowledge assistant.

Your task: route each employee question to exactly one department label.
Allowed labels only: hr | security | finance
Reply with the label alone — no punctuation, no explanation.

Examples:
Q: How many PTO days do I accrue after 2 years?
A: hr

Q: Who approves badge access for Lab B after hours?
A: security

Q: What cost center do I charge conference travel to?
A: finance

Q: Can I work from home on Fridays under the hybrid policy?
A: hr

Now route the user's question the same way.
"""
