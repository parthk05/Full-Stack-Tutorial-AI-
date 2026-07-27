"""
Step 2.1 — request body for POST /v1/prompt

Why Pydantic: FastAPI validates JSON, rejects bad shapes early, and documents the schema in /docs.
"""

from pydantic import BaseModel, Field


class PromptRequest(BaseModel):
    # Step 2.1.1 — employee question (not a free-form "prompt" blob)
    question: str = Field(..., min_length=1, description="Policy-style question from an employee")

    # Step 2.1.1 — which prompting technique to run; only zero_shot wired in this step
    strategy: str = Field(
        default="zero_shot",
        description="Prompting strategy id (zero_shot | few_shot | cot | ...)",
    )
