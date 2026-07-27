"""
Step 2.1 — response body for POST /v1/prompt

Why these fields: callers can see *what* answered (answer), *how* (strategy),
*which model*, and *which prompt revision* — needed later for evals (Ch 06).
"""

from pydantic import BaseModel


class PromptResponse(BaseModel):
    # Step 2.1.3 — model-generated text
    answer: str

    # Step 2.1.3 — echoing strategy makes A/B comparison in notes easy
    strategy: str

    # Step 2.1.3 — which MODEL_NAME produced the answer
    model: str

    # Step 4.2 preview / Step 2.1.3 — e.g. prompt_desk_v1; bump when prompts change
    prompt_version: str
