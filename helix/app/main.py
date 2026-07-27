"""
Helix Prompt Desk — Chapter 01 FastAPI entry

Step map in this file:
  1.2  — health + settings load
  2.1  — zero-shot POST /v1/prompt
"""

from fastapi import FastAPI, HTTPException

from app.llm import complete_chat, get_client
from app.settings import get_settings
from prompts.zero_shot import STRATEGY_ID as ZERO_SHOT, ZERO_SHOT_SYSTEM_PROMPT
from schemas.Request import PromptRequest
from schemas.Response import PromptResponse

# Step 1.2 — app shell; OpenAPI at /docs
app = FastAPI(title="Helix Prompt Desk", version="0.1.0")


@app.get("/health")
async def health():
    # Step 1.2 — liveness check; does not call the LLM
    return {"status": "ok"}


@app.post("/v1/prompt", response_model=PromptResponse)
async def prompt(body: PromptRequest) -> PromptResponse:
    """
    Step 2.1 — Zero-shot Prompt Desk endpoint.

    Body: { "question": "...", "strategy": "zero_shot" }
    Returns: { answer, strategy, model, prompt_version }
    """
    settings = get_settings()

    # Step 2.1.1 — only zero_shot in this step; other strategies arrive in 2.2+
    if body.strategy != ZERO_SHOT:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported strategy '{body.strategy}'. Use '{ZERO_SHOT}' for Step 2.1.",
        )

    # Step 2.1.2 — system role (Helix) + user question only → zero-shot
    client = get_client(settings)
    answer = complete_chat(
        client,
        model=settings.MODEL_NAME,
        system_prompt=ZERO_SHOT_SYSTEM_PROMPT,
        user_message=body.question,
    )

    # Step 2.1.3 — contract required by the chapter Check
    return PromptResponse(
        answer=answer,
        strategy=ZERO_SHOT,
        model=settings.MODEL_NAME,
        prompt_version=settings.PROMPT_VERSION,
    )
