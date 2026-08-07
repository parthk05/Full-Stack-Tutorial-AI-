"""
Helix Prompt Desk — Chapter 01 FastAPI entry

Step map in this file:
  1.2  — health + settings load
  2.1  — zero-shot POST /v1/prompt  (kept below as commented historical block)
  2.2  — few_shot strategy via registry
  2.3  — cot strategy
  2.4  — persona_hr | persona_terse | constrained
"""

from fastapi import FastAPI, HTTPException

from app.llm import complete_chat, get_client
from app.settings import get_settings
from prompts.constrained import STRATEGY_ID as CONSTRAINED
from prompts.cot import STRATEGY_ID as COT
from prompts.registry import SUPPORTED_STRATEGIES, get_system_prompt
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
    Step 2.2–2.4 — Prompt Desk with multiple strategies.

    Body: { "question": "...", "strategy": "zero_shot|few_shot|cot|persona_hr|persona_terse|constrained" }
    Returns: { answer, strategy, model, prompt_version }
    """
    settings = get_settings()

    # -------------------------------------------------------------------------
    # Step 2.1 (historical) — only zero_shot was allowed; single inline call.
    # Kept for learning track: see what Step 2.1 looked like before the router.
    # -------------------------------------------------------------------------
    # from prompts.zero_shot import STRATEGY_ID as ZERO_SHOT, ZERO_SHOT_SYSTEM_PROMPT
    #
    # if body.strategy != ZERO_SHOT:
    #     raise HTTPException(
    #         status_code=400,
    #         detail=f"Unsupported strategy '{body.strategy}'. Use '{ZERO_SHOT}' for Step 2.1.",
    #     )
    #
    # client = get_client(settings)
    # answer = complete_chat(
    #     client,
    #     model=settings.MODEL_NAME,
    #     system_prompt=ZERO_SHOT_SYSTEM_PROMPT,
    #     user_message=body.question,
    # )
    # return PromptResponse(
    #     answer=answer,
    #     strategy=ZERO_SHOT,
    #     model=settings.MODEL_NAME,
    #     prompt_version=settings.PROMPT_VERSION,
    # )
    # -------------------------------------------------------------------------

    # Step 2.2.2 — resolve strategy → system prompt (2.1–2.4 all registered)
    system_prompt = get_system_prompt(body.strategy)
    if system_prompt is None:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Unsupported strategy '{body.strategy}'. "
                f"Choose one of: {', '.join(SUPPORTED_STRATEGIES)}"
            ),
        )

    # Step 2.3 / 2.4 — light per-strategy knobs (still one LLM helper)
    # CoT: slightly higher temp for varied reasoning paths
    # Constrained: lower temp so UNKNOWN is more consistent
    temperature = 0.2
    if body.strategy == COT:
        # Step 2.3.2 — CoT may benefit from a bit more exploration in reasoning
        temperature = 0.4
    elif body.strategy == CONSTRAINED:
        # Step 2.4.2 — prefer deterministic refusal over creative invention
        temperature = 0.0

    # Step 2.1.2 shape reused — system + user only; examples live inside system prompt (few_shot)
    client = get_client(settings)
    answer = complete_chat(
        client,
        model=settings.MODEL_NAME,
        system_prompt=system_prompt,
        user_message=body.question,
        temperature=temperature,
    )

    # Step 2.1.3 contract — still required; strategy echoes whichever technique ran
    return PromptResponse(
        answer=answer,
        strategy=body.strategy,
        model=settings.MODEL_NAME,
        prompt_version=settings.PROMPT_VERSION,
    )
