# Chapter 01 — Helix Prompt Desk (Prompting & Reliability)

**Prerequisites:** Python 3.10+, basic FastAPI (app, one POST route, Pydantic body).

**Mini-project:** **Helix Prompt Desk** — first slice of Helix, Meridian Labs’ internal knowledge assistant. Employees ask policy-style questions; you return answers via FastAPI using different prompting strategies.

**Goal:** Learn prompting methods by shipping a real endpoint — and personally experience why prompting alone cannot make a trustworthy knowledge product.

**Rules for you:**
- Do each step yourself. Do not skip ahead.
- After each **Check**, verify before continuing.
- Build inside a `helix/` package (see roadmap). This track is standalone.
- Prefer provider docs + LangChain prompt docs when stuck.

**Libraries:** `fastapi`, `uvicorn`, LLM provider SDK, `langchain` + chat-model package, `python-dotenv` / `pydantic-settings`.

---

## Why this chapter exists (industry context)

Early LLM apps were “wrap a prompt in an API.” That unlocked demos — and also fluent, confident **wrong** answers. You will rebuild that moment on purpose, so later chapters (tools, RAG, gates) feel necessary rather than fashionable.

---

## Phase 0 — Concepts (no code yet)

### Step 0.1 — Messages & knobs
1. Define: system / user / assistant message, temperature, tokens.
2. In notes: *Does the model optimize for truth or plausible continuation?*

### Step 0.2 — Hallucination
1. Define hallucination in one sentence.
2. List 3 ways it hurts an internal policy assistant (wrong leave days, fake policy IDs, invented security rules).
3. In notes: *Why doesn’t “be accurate” in the system prompt fully fix this?*

**Check:** You can explain why a fluent wrong policy answer is worse than a refusal.

---

## Phase 1 — Bootstrap Helix

### Step 1.1 — Project skeleton
1. Create venv + `helix/` package layout (minimal: `app/main.py`, `prompts/`, settings).
2. `requirements.txt` + `.env` (`LLM_API_KEY`, model name) + `.gitignore`.

**Check:** REPL creates a chat client without printing the key.

### Step 1.2 — FastAPI shell
1. `GET /health`
2. Load settings; run Uvicorn with reload.

**Check:** `/docs` loads; health is 200.

---

## Phase 2 — Mini-project: Prompt Desk

Domain for all examples: **Meridian Labs employee / ops policies** (you may invent plausible policy text *inside prompts* for few-shot — you do **not** have a real handbook yet; that arrives in Ch 03).

### Step 2.1 — Zero-shot
1. `POST /v1/prompt` with `{ "question": "...", "strategy": "zero_shot" }`.
2. System prompt: “You are Helix, Meridian Labs’ internal assistant…”
3. Return `{ answer, strategy, model, prompt_version }`.

**Check:** Ask “How many remote days per week does Meridian allow?” — you get *an* answer (even if invented).

### Step 2.2 — Few-shot
1. Add strategy `few_shot` with 2–4 example Q&A pairs (synthetic Meridian style).
2. In notes: *When do examples beat a longer instruction?*

**Check:** For a **classification** task (e.g. route question → `hr` | `security` | `finance`), few-shot beats zero-shot — record both outputs.

### Step 2.3 — Chain-of-thought
1. Strategy `cot`: reason briefly, then final answer.
2. In notes: *Latency/cost tradeoff?*

### Step 2.4 — Constraints & personas
1. Strategies: `persona_hr` vs `persona_terse`.
2. Add constrained strategy: if unknown, answer exactly `UNKNOWN` — do not invent policy numbers.

**Check:** Unanswerable question → constrained strategy says `UNKNOWN` more often than zero-shot (log both).

### Step 2.5 — Decomposition (two calls)
1. Strategy `decompose`: (1) extract entities → (2) answer using only those entities.
2. Log both stages in the response or server logs.

**Check:** Intermediate extraction is visible.

---

## Phase 3 — LangChain structure

### Step 3.1 — Templates
1. Move ≥2 strategies into `ChatPromptTemplate` files under `helix/prompts/`.

### Step 3.2 — LCEL
1. `prompt | model | StrOutputParser` for at least one strategy.
2. In notes: *Why compose instead of one giant handler?*

**Check:** `/v1/prompt` still switches strategies cleanly.

---

## Phase 4 — API hygiene

### Step 4.1 — Edge cases
Document behavior for: empty question, oversized input, provider timeout/rate limit.

### Step 4.2 — Prompt versions
1. Every response includes `prompt_version` (e.g. `prompt_desk_v1`).
2. In notes: *Why will Ch 06 care about this field?*

**Check:** Response always has `strategy` + `prompt_version`.

---

## Phase 5 — Self-review checklist

- [ ] Helix FastAPI app runs with `/health` and `/v1/prompt`
- [ ] ≥3 prompting strategies implemented and compared in notes
- [ ] Constrained vs unconstrained demo recorded
- [ ] Secrets only in `.env`
- [ ] LangChain templates used for ≥1 strategy
- [ ] You can explain zero-shot / few-shot / CoT / constraints

---

## Open problem → Chapter 02

You now have a working Prompt Desk. Stress it:

1. Ask three factual Meridian questions you never put in the prompt.
2. Paste the answers into your notes.

You should see at least one of:
- Invented policy IDs, numbers, or dates stated confidently
- Free-text answers that a UI or downstream service cannot reliably parse
- “UNKNOWN” helping sometimes — but not giving *grounded* facts when facts should exist somewhere

**Why the industry moved on:** prompting improves *behavior*, not *access to private truth* or *machine-readable contracts*.

**Next chapter fixes:** structured outputs (stable shape) + function calling (fetch real stub records instead of inventing them).

→ [`02-tools-and-structured-outputs.md`](./02-tools-and-structured-outputs.md)

---

## How to use this file

1. Complete one step → mark done.
2. Do not start Ch 02 until the Open problem notes exist.
3. Stuck >20 minutes → docs → **hint** for that step only.
