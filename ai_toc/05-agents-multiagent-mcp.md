# Chapter 05 — Helix Agent (Agents, Multi-Agent & MCP)

**Prerequisites:** Chapters 01–04. Helix Flow works; Open problem notes from Ch 04 written.

**Mini-project:** **Helix Agent** — add a budgeted **tool-calling agent** for open-ended Meridian goals, then a small **multi-agent** crew, then expose Helix capabilities through **MCP** so tools aren’t only hardcoded in-process.

**Goal:** Learn agents / multi-agent / MCP by solving Flow’s rigidity — and discover why autonomy without measurement is dangerous.

**Rules for you:**
- Order is mandatory: **Part A → Part B → Part C**.
- Hard caps on steps / tool calls / time.
- Prefer LangGraph agent loops so Ch 04 skills transfer.
- Extend `helix/agents/` — same product.

**Libraries:** LangGraph agents, LangChain tools, MCP Python SDK (pin current recommended packages), FastAPI.

---

## Why this chapter exists

Workflows excel at known pipelines. Users still ask messy, multi-doc goals. **Agents** choose tools dynamically; **multi-agent** splits roles; **MCP** standardizes tool/context interfaces so Helix isn’t a monolith of `@tool` functions.

---

## Phase 0 — Concepts

### Step 0.1 — Agent vs Helix Flow
1. In notes: who picks the next step in Flow vs in an agent?
2. List stopping conditions you will enforce.

### Step 0.2 — Roles for Meridian
Propose specialists, e.g. **Retriever**, **Policy Analyst**, **Editor** (clear citations, refuse if thin).

### Step 0.3 — MCP one-liner
1. Write what MCP standardizes (tools/resources/prompts for hosts).
2. In notes: *How is that different from three in-process LangChain tools?*

**Check:** Plain-language explanation of workflow vs agent vs MCP.

---

## Part A — Single Helix agent

### Step 1A.1 — Tool belt
1. Expose as tools: `search_corpus`, `get_chunk`, `get_policy_by_id`, `search_policies`, optional calculator.
2. Descriptions must be crisp.

### Step 1A.2 — Agent loop
1. LangGraph tool-calling agent; state includes messages + remaining steps.
2. Budgets: max iterations, max tool calls, timeout.

**Check:** Goal needing retrieve + stub lookup succeeds within budget; forced tiny budget hits the cap cleanly.

### Step 1A.3 — FastAPI
1. `POST /v1/agent/run` `{ "goal": "...", "thread_id": null }`.
2. Return final answer + readable `step_trace`.
3. Light memory by `thread_id` (in-memory OK).

**Check:** Trace is debuggable when the agent picks a wrong tool.

---

## Part B — Multi-agent crew

### Step 2B.1 — Pattern
1. Pick **supervisor** *or* **handoff**.
2. Specialists: Retriever + Analyst (+ Editor optional).

### Step 2B.2 — Shared conventions
1. What each role may write to shared state.
2. Failure isolation: one specialist fails → controlled partial/error, not hang.

### Step 2B.3 — API
1. `POST /v1/agent/crew` for multi-agent runs.
2. Trace shows per-agent contributions.

**Check:** A dual-domain goal (e.g. travel + expense) shows ≥2 agents in the trace.

---

## Part C — MCP

### Step 3C.1 — Helix MCP server
1. Separate small process: tools like `search_corpus`, `get_policy_by_id`.
2. Optional resource: Meridian answer style guide text.

**Check:** MCP client/CLI lists tools without FastAPI.

### Step 3C.2 — Agent as host
1. Helix Agent discovers/calls MCP tools dynamically.
2. **Check:** Trace shows an MCP-backed tool call succeeding.

### Step 3C.3 — Security notes
Allowlists, untrusted servers, secret redaction in logs.

---

## Phase 4 — Compare (notes table)

| Need | Flow (Ch 04) | Single agent | Multi-agent | MCP |
|------|--------------|--------------|-------------|-----|
| Fixed intake pipeline | | | | |
| Open-ended goal | | | | |
| Specialist roles | | | | |
| Tools owned elsewhere | | | | |

---

## Phase 5 — Self-review checklist

- [ ] `/v1/agent/run` with budgets + trace
- [ ] Multi-agent path with ≥2 roles
- [ ] MCP server + agent consumption
- [ ] Side-effect policy preserved
- [ ] You can explain when *not* to use an agent

---

## Open problem → Chapter 06

Helix Agent feels powerful. Now change one prompt or tool description and re-run last week’s questions.

Pain you should feel:
- Did quality get better or worse? You’re not sure without a spreadsheet of vibes
- A bad tool loop is hard to explain to a teammate without shared traces
- `prompt_version` exists but you’re not running systematic evals on every change

**Why LLMOps became mandatory:** treat Helix like software — trace, evaluate, version, monitor.

**Next chapter fixes:** Helix Ops with LangSmith + Langfuse, golden sets, and regression runners.

→ [`06-llmops.md`](./06-llmops.md)

---

## How to use this file

1. Part A solid before B; B before C.
2. Write Open problem notes before Ch 06.
3. Stuck >20 minutes → LangGraph/MCP docs → **hint** for that step only.
