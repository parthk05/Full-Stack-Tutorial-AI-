"""
Step 2.2–2.4 — map strategy id → system prompt

Why a registry: /v1/prompt stays a thin switch; each technique lives in prompts/
with its own theory comments. Add new strategies here without rewriting the route.
"""

from prompts.constrained import CONSTRAINED_SYSTEM_PROMPT
from prompts.constrained import STRATEGY_ID as CONSTRAINED
from prompts.cot import COT_SYSTEM_PROMPT
from prompts.cot import STRATEGY_ID as COT
from prompts.few_shot import FEW_SHOT_SYSTEM_PROMPT
from prompts.few_shot import STRATEGY_ID as FEW_SHOT
from prompts.persona_hr import PERSONA_HR_SYSTEM_PROMPT
from prompts.persona_hr import STRATEGY_ID as PERSONA_HR
from prompts.persona_terse import PERSONA_TERSE_SYSTEM_PROMPT
from prompts.persona_terse import STRATEGY_ID as PERSONA_TERSE
from prompts.zero_shot import STRATEGY_ID as ZERO_SHOT
from prompts.zero_shot import ZERO_SHOT_SYSTEM_PROMPT

# Step 2.2+ — all Prompt Desk strategies available on POST /v1/prompt
STRATEGY_PROMPTS: dict[str, str] = {
    # Step 2.1
    ZERO_SHOT: ZERO_SHOT_SYSTEM_PROMPT,
    # Step 2.2
    FEW_SHOT: FEW_SHOT_SYSTEM_PROMPT,
    # Step 2.3
    COT: COT_SYSTEM_PROMPT,
    # Step 2.4
    PERSONA_HR: PERSONA_HR_SYSTEM_PROMPT,
    PERSONA_TERSE: PERSONA_TERSE_SYSTEM_PROMPT,
    CONSTRAINED: CONSTRAINED_SYSTEM_PROMPT,
}

SUPPORTED_STRATEGIES = tuple(STRATEGY_PROMPTS.keys())


def get_system_prompt(strategy: str) -> str | None:
    """Step 2.2.2 — resolve strategy id to system prompt text; None if unknown."""
    return STRATEGY_PROMPTS.get(strategy)
