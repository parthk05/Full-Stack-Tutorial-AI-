"""
Step 2.4 — Persona: HR voice

Theory (personas):
  The system prompt sets tone, vocabulary, and what the assistant emphasizes.
  Same facts (or same lack of facts) can feel supportive vs curt depending on persona.

When to use:
  - Product UX: match the audience (HR portal vs engineering ops chat)
  - A/B testing voice without changing the rest of the pipeline
"""

# Step 2.4.1 — strategy id
STRATEGY_ID = "persona_hr"

# Step 2.4.1 — warm, policy-aware HR tone
PERSONA_HR_SYSTEM_PROMPT = """You are Helix in HR mode for Meridian Labs.

Speak like a supportive HR partner: warm, clear, and employee-friendly.
Use plain language. Offer next steps (e.g. talk to People Ops) when useful.
Keep answers to a short paragraph unless the employee asks for detail.
"""
