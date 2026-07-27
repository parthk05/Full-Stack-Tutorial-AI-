"""
Step 2.1 — Gemini chat client wrapper

Why a thin wrapper: the FastAPI route stays about HTTP; provider details live here so
later strategies (few-shot, CoT) reuse one call site.
"""

from google import genai
from google.genai import types

from app.settings import Settings


def get_client(settings: Settings) -> genai.Client:
    # Step 2.1.1 — build client from settings; never log the key
    return genai.Client(api_key=settings.LLM_API_Key)

#This function is used to complete the chat
#It takes a client, a model, a system prompt, and a user message
#It returns a string
def complete_chat(
    client: genai.Client, #The client is the client for the Gemini API
    *,
    model: str, #The model is the model to use for the chat
    system_prompt: str, #The system prompt is the system prompt to use for the chat
    user_message: str, #The user message is the user message to use for the chat
) -> str:
    """
    Step 2.1.2 — one system + one user turn (zero-shot message shape).

    Why system_instruction: puts Helix's role at highest priority; user text is the question only.
    """
    response = client.models.generate_content(
        model=model,
        contents=user_message,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            # Step 0.1 knob — lower temp → more stable policy-style answers (still can invent facts)
            temperature=0.2,
        ),
    )
    return (response.text or "").strip()
