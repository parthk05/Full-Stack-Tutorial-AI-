# Chapter 06 — Helix Ops (LLMOps with LangSmith & Langfuse)

**Prerequisites:** Chapters 01–05. Prompt / Structured / Source / Flow / Agent paths exist; Open problem notes from Ch 05 written.

**Mini-project:** **Helix Ops** — make Helix operable: end-to-end **traces**, a **golden eval set**, prompt/index **versions**, **feedback**, and a small CI-friendly eval runner. Instrument the Helix you already built — do not start a new app.

**Goal:** Learn LLMOps by measuring Helix so prompt/agent changes become visible — and recognize why metrics alone still don’t *block* dangerous answers in regulated settings.

**Rules for you:**
- Do each step yourself. Do not skip ahead.
- Evals beat vibes; keep datasets in git.
- Never commit provider, LangSmith, or Langfuse secrets.

**Libraries / services:** LangSmith, Langfuse, pytest or a script runner, FastAPI request-id middleware.

---

## Why this chapter exists

Agents and RAG demos fail quietly in production. Teams adopted tracing + evaluation platforms so regressions are caught like failing unit tests. You will put Helix on that loop.

---

## Phase 0 — Concepts

### Step 0.1 — LLMOps map
Define in notes: tracing, evaluation, prompt management, online monitoring, feedback, cost control — each tied to a Helix failure you’ve seen.

### Step 0.2 — LangSmith vs Langfuse
High-level comparison table after skimming both docs. This chapter: use **both** at least once.

**Check:** One sentence each for what problem they solve.

---

## Phase 1 — Tracing Helix

### Step 1.1 — Request correlation
1. Middleware: `request_id` on every Helix AI route.
2. Propagate into LangChain/LangGraph callbacks.

### Step 1.2 — LangSmith
1. Configure current LangSmith env vars per docs.
2. Trace at least: `/v1/prompt`, `/v1/ask`, intake workflow, `/v1/agent/run`.
3. In UI: find retrieve vs generate for a RAG call; find a tool span for an agent call.

**Check:** A failed tool call is visible with redacted inputs/outputs.

### Step 1.3 — Langfuse
1. Trace the same critical paths.
2. Attach metadata: route, `prompt_version`, `index_version`, strategy.
3. In notes: *Which UI did you prefer for RAG? For agents?*

**Check:** Same `request_id` (or equivalent) findable across systems or clearly mapped in notes.

---

## Phase 2 — Golden set & offline evals

### Step 2.1 — Dataset
1. Expand Ch 03’s 5 questions into ≥20 cases in `helix/evals/datasets/helix_v1.json`.
2. Cover: prompting classification, stub-tool questions, RAG answerable, RAG refuse, one agent-style multi-doc goal, one adversarial “invent a policy” ask.

### Step 2.2 — Runner
1. Script/pytest hits the real FastAPI routes (or graph invoke) per case.
2. Score what you can automatically (structured fields, refusal expected, citation ids exist).
3. For free text: rubric or LLM-as-judge — document bias risk.
4. Non-zero exit when pass rate < threshold.

**Check:** Runner prints pass/fail summary; breaking a prompt fails the suite.

### Step 2.3 — Platform experiments
1. Run the dataset through LangSmith and/or Langfuse experiment features.
2. Record experiment name + git commit in notes.

---

## Phase 3 — Versioning & feedback

### Step 3.1 — Versions everywhere
1. All AI responses already carry `prompt_version`; enforce it.
2. RAG responses carry `index_version`.
3. In notes: *How do the two versions explain a sudden quality drop?*

### Step 3.2 — Feedback API
1. `POST /v1/feedback` `{ request_id, rating, comment }`.
2. Attach to traces in LangSmith/Langfuse.

### Step 3.3 — Metrics snapshot
1. `GET /v1/metrics/summary` — simple aggregates from recent stored runs (counts, approx error rate). Good enough for learning.

---

## Phase 4 — Production hygiene (notes + light code)

### Step 4.1 — SLOs
Draft p95 latency / error rate / rough cost-per-request targets for `/v1/ask` and `/v1/agent/run`.

### Step 4.2 — Config flags
`AGENT_ENABLED`, max tool calls, model name per route — via settings.

### Step 4.3 — CI sketch
Document (or add) a PR check that runs the fast subset of evals.

---

## Phase 5 — Self-review checklist

- [ ] LangSmith traces on ≥4 Helix route types
- [ ] Langfuse traces on the same critical paths
- [ ] ≥20-case dataset + offline runner with threshold
- [ ] Feedback linked to traces
- [ ] Versions on responses
- [ ] You can explain the loop: change → trace → eval → ship → monitor → feedback

---

## Open problem → Chapter 07

Helix Ops tells you when quality moves. It still allows this failure mode:

1. A fluent, well-formatted `/v1/ask` answer with a **wrong or fake citation** can score “looks fine” to a shallow rubric and ship.
2. In Meridian’s world (and later real pharma/finance), “we measured average quality” is not enough — **each answer** may need faithfulness + citation grounding checks before release.
3. You need fail-closed **governance**: score claims, validate citations, allow / refuse / human-review, and prove grounded-response rate improved.

**Why eval & governance frameworks exist for high-stakes domains:** observation ≠ enforcement.

**Next chapter (capstone):** evolve Helix into **GroundGate** — domain-specific evaluation & governance for regulated pharma/finance-style Q&A.

→ [`07-llm-eval-governance-capstone.md`](./07-llm-eval-governance-capstone.md)

---

## How to use this file

1. Instrument first, then datasets — dashboards without cases lie.
2. Write Open problem notes before Ch 07.
3. Stuck >20 minutes → LangSmith/Langfuse docs → **hint** for that step only.
