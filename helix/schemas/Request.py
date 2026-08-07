"""
Step 2.1 — request body for POST /v1/prompt
Step 2.2–2.4 — strategy field expanded; validation still plain str (registry enforces allow-list)

Why Pydantic: FastAPI validates JSON, rejects bad shapes early, and documents the schema in /docs.
"""

from pydantic import BaseModel, Field


class PromptRequest(BaseModel):
    # Step 2.1.1 — employee question (not a free-form "prompt" blob)
    question: str = Field(..., min_length=1, description="Policy-style question from an employee")

    # --- Step 2.1 historical description (zero_shot only) ---
    # strategy: str = Field(
    #     default="zero_shot",
    #     description="Prompting strategy id (zero_shot only in Step 2.1)",
    # )

    # Step 2.2–2.4 — strategy selects which prompts/* system prompt to use
    strategy: str = Field(
        default="zero_shot",
        description=(
            "Prompting strategy id: "
            "zero_shot | few_shot | cot | persona_hr | persona_terse | constrained"
        ),
    )
