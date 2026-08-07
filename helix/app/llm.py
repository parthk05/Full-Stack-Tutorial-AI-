"""
Step 2.1 — Gemini chat client wrapper
Step 2.3 — optional temperature override (CoT / constrained knobs)

Why a thin wrapper: the FastAPI route stays about HTTP; provider details live here so
strategies (few-shot, CoT, personas) reuse one call site.
"""

from google import genai
from google.genai import types

from app.settings import Settings


def get_client(settings: Settings) -> genai.Client:
    # Step 2.1.1 — build client from settings; never log the key
    return genai.Client(api_key=settings.LLM_API_Key)


def complete_chat(
    client: genai.Client,
    *,
    model: str,
    system_prompt: str,
    user_message: str,
    # Step 2.3 / 2.4 — allow per-strategy temperature without forking the client
    temperature: float = 0.2,
) -> str:
    """
    Step 2.1.2 — one system + one user turn (message shape shared by all Phase-2 strategies).

    Why system_instruction: puts Helix's role at highest priority; user text is the question only.

    --- Step 2.1 historical signature (temperature fixed at 0.2) ---
    # def complete_chat(client, *, model, system_prompt, user_message) -> str:
    #     ...
    #     temperature=0.2,
    """
    response = client.models.generate_content(
        model=model,
        contents=user_message,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            # Step 0.1 knob — default 0.2; constrained may pass lower for stabler UNKNOWN
            temperature=temperature,
        ),
    )
    return (response.text or "").strip()
