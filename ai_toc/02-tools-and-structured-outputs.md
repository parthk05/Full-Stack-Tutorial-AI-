# Chapter 02 — Helix Structured Desk (Structured Outputs & Tools)

**Prerequisites:** Finish Chapter 01 — Helix Prompt Desk works; Open problem notes written.

**Mini-project:** **Helix Structured Desk** — upgrade Helix so answers are **typed** and the model can **call tools** against a tiny Meridian policy stub (in-memory or JSON), instead of inventing row-level facts.

**Goal:** Learn structured outputs and function calling by fixing Prompt Desk’s two loudest failures: unparseable prose and invented “database” facts.

**Rules for you:**
- Do each step yourself. Do not skip ahead.
- Complete **Part A** before **Part B**.
- Extend the existing `helix/` app — do not create a second product.
- Treat the model as an untrusted client: validate tool args.

**Libraries:** LangChain tools + `with_structured_output` (or provider JSON schema), Pydantic v2, FastAPI.

---

## Why this chapter exists

After Prompt Desk, teams needed (1) JSON the backend could trust and (2) a way for the model to **read live data** instead of guessing. Function calling / tools were the industry answer. You will add both to Helix and then hit the next wall.

---

## Phase 0 — Concepts

### Step 0.1 — From Ch 01 pain
1. Paste one hallucinated Prompt Desk answer into notes.
2. In notes: *What breaks if a frontend expects fixed fields and gets markdown paragraphs?*

### Step 0.2 — Structured output
1. Design `PolicyAnswer`: `summary`, `category` (`hr|security|finance|unknown`), `confidence` (0–1), `policy_ids: list[str]`, `caveats: list[str]`.
2. In notes: *When should a field be null instead of invented?*

### Step 0.3 — Tool loop
1. Draw: model → tool call → your code → tool result → model → final answer.
2. In notes: *How is this different from the model pretending it looked something up in prose?*

**Check:** You can explain tool call vs tool result vs final message.

---

## Part A — Structured outputs

### Step 1A.1 — Schemas
1. Add Pydantic models under `helix/` (request + `PolicyAnswer`).
2. Use the same models as FastAPI `response_model` where possible.

### Step 1A.2 — Force structure
1. `POST /v1/extract/policy-answer` — body: free-text question or pasted policy blurb.
2. Use `with_structured_output(PolicyAnswer)` (or equivalent).

**Check:** You always get valid JSON matching the schema, or a controlled error — never “almost JSON.”

### Step 1A.3 — Wire Prompt Desk (optional but good)
1. Add `strategy: "structured"` on `/v1/prompt` *or* keep extract separate — document your choice.
2. Null/unknown fields preferred over fabrication.

**Check:** Unanswerable field → null / empty list more often than a fake policy id.

---

## Part B — Tools on a stub catalog

### Step 2B.1 — Meridian stub data
1. Create `helix/data/policy_stub.json` (or Python dict) with **5–10** rows, e.g.:
   - `POL-HR-001` remote work days
   - `POL-HR-014` PTO accrual
   - `POL-SEC-003` laptop encryption
   - `POL-FIN-002` expense limit
2. Include one numeric field tools can compute on (limits, days, percentages).

### Step 2B.2 — Implement tools
1. `get_policy_by_id(policy_id: str)`
2. `search_policies(keyword: str)` (simple substring/keyword over stub — not vector search yet)
3. `calculate_prorated_limit(annual_limit: float, months: int)` (deterministic)
4. Wrap with LangChain `@tool`; write clear descriptions.

**Check:** Each tool works in plain Python without the LLM.

### Step 2B.3 — Bind + loop
1. `POST /v1/tools/chat` — model may call tools until final answer; **max iterations** enforced.
2. Response includes `answer` (prefer structured `PolicyAnswer` if you can combine) + `tool_trace[]`.

**Check:** “What is Meridian’s expense limit in POL-FIN-002, prorated for 3 months?” triggers tools — not a guessed number.

### Step 2B.4 — Validate args
1. Pydantic on tool inputs; bad ids return a tool error string the model can handle.
2. Side-effecting tools (if any) require `confirm=true` on the HTTP request.

**Check:** Unknown policy id does not crash the API; trace shows the failed lookup.

---

## Phase 3 — Product polish

### Step 3.1 — Errors & timeouts
Document HTTP vs tool-error policy; add simple timeouts.

### Step 3.2 — Keep prompt_version
Return `prompt_version` / `tool_desk_version` on responses.

---

## Phase 4 — Self-review checklist

- [ ] `PolicyAnswer` structured endpoint works
- [ ] Stub catalog with ≥5 policies
- [ ] ≥2 tools work standalone and via the model
- [ ] `/v1/tools/chat` returns a tool trace; max iterations enforced
- [ ] Tool args validated
- [ ] You can explain structured output vs tools vs Ch 01 prompting

---

## Open problem → Chapter 03

Structured Desk is a real upgrade. Now break it on purpose:

1. Ask a question whose answer is **only** in a long handbook paragraph (write that paragraph in notes — but **do not** put it in `policy_stub.json`).
2. Ask a question that needs **two documents** blended (e.g. travel + expense).
3. Watch Helix: tools return “not found” or the model invents handbook prose anyway.

**Root cause:** tools are great for **known IDs / APIs**; they do not replace **document retrieval**. Most enterprise knowledge is unstructured text.

**Why the industry moved to RAG:** embed and retrieve relevant chunks, then generate — so the model sees the handbook, not just 10 stub rows.

**Next chapter fixes:** ingest Meridian docs, retrieve, cite, and pack context on purpose.

→ [`03-rag-and-context-engineering.md`](./03-rag-and-context-engineering.md)

---

## How to use this file

1. Part A green before Part B.
2. Write Open problem notes before Ch 03.
3. Stuck >20 minutes → docs → **hint** for that step only.
