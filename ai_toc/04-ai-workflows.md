# Chapter 04 — Helix Flow (AI Workflows)

**Prerequisites:** Chapters 01–03. Source Desk `/v1/ask` works; Open problem notes from Ch 03 written.

**Mini-project:** **Helix Flow** — replace the one-shot ask handler with a **LangGraph** intake workflow: classify → retrieve → draft → confidence branch → (optional) human approve → finalize.

**Goal:** Learn AI workflows by encoding Meridian’s answer pipeline as an explicit graph — and feel when fixed graphs become too rigid.

**Rules for you:**
- Do each step yourself. Do not skip ahead.
- Prefer workflows for this business pipeline; save free-form agents for Ch 05.
- FastAPI triggers/status; LangGraph orchestrates.
- Reuse Structured Desk schemas + Source Desk retriever inside nodes.

**Libraries:** `langgraph`, LangChain, existing Helix RAG/tools. Optional tracing peek.

---

## Why this chapter exists

Source Desk proved grounding helps, but production teams needed **deterministic multi-step** behavior: routing, retries, HITL, audit-friendly stages. Graphs/workflows answered that — before jumping to autonomous agents.

---

## Phase 0 — Concepts

### Step 0.1 — Workflow vs agent
Fill:

| | Workflow | Agent |
|--|----------|-------|
| Who decides the next step? | | |
| Best for | | |
| Typical failure mode | | |

### Step 0.2 — Design Helix intake on paper
Required graph for this mini-project:

1. `classify` — hr / security / finance / ops / unknown (structured, Ch 02)
2. `retrieve` — Source Desk retriever + filters
3. `draft` — grounded draft answer + citations
4. `score_confidence` — heuristic or small LLM score
5. Branch: high → `finalize` | low → `human_review` | empty context → `refuse`
6. `finalize` — persist run record (file/sqlite fine)

**Check:** Paper diagram exists before you code.

---

## Phase 1 — LangGraph fundamentals

### Step 1.1 — State
1. Typed state: `question`, `category`, `chunks`, `draft`, `citations`, `confidence`, `verdict`, `error`, `run_id`, …

### Step 1.2 — Linear skeleton
1. Implement classify → retrieve → draft → finalize **without** branches first.
2. Print/log state after each node while learning.

**Check:** Script invoke fills state step by step on a known question.

### Step 1.3 — FastAPI
1. `POST /v1/workflows/intake` runs the graph; returns final fields + `run_id`.
2. Keep `/v1/ask` working (or make it call the graph) — document the choice.

**Check:** `/docs` runs intake successfully.

---

## Phase 2 — Control flow (product behavior)

### Step 2.1 — Branching
1. Wire confidence / empty-retrieval branches to `finalize` | `refuse` | `human_review`.
2. **Check:** Crafted inputs hit each branch.

### Step 2.2 — Loop with cap
1. Optional `refine_draft` until length/citation minimum met OR max 3 loops.
2. **Check:** Cap stops infinite refine.

### Step 2.3 — Human-in-the-loop
1. Store pending runs; `POST /v1/workflows/{run_id}/approve` and `/reject`.
2. Without approval, “published” answer is not released (simulate with status field).

**Check:** Low-confidence path sits in `pending` until approve/reject.

### Step 2.4 — Reuse prior chapters
1. Classify/draft use structured outputs.
2. Retrieve uses Ch 03 index (`index_version` in output).
3. Optional node: Ch 02 `get_policy_by_id` when ids appear.

**Check:** Short module docstring lists which node uses which prior capability.

---

## Phase 3 — Reliability

### Step 3.1 — Node errors
Route failures to `finalize_error`; map to sensible HTTP errors.

### Step 3.2 — Retries
Retry transient provider errors on `draft` only; note which nodes are unsafe to retry.

### Step 3.3 — Trace peek
One full intake trace in LangSmith or Langfuse; note the slowest node.

---

## Phase 4 — Self-review checklist

- [ ] Helix Flow graph exposed via FastAPI
- [ ] Branches: allow / refuse / human_review all demoable
- [ ] HITL approve/reject works
- [ ] Iteration caps where loops exist
- [ ] Reuses RAG + structured outputs
- [ ] You can explain when a workflow beats an agent

---

## Open problem → Chapter 05

Helix Flow handles the **known** intake path well. Now try goals like:

1. “Prepare a checklist for a laptop lost abroad using whatever Helix policies apply — pull expense + security + travel.”
2. “Figure out which docs matter; I don’t know the category.”

Pain you should feel:
- Graph edges don’t cover every open-ended goal
- Adding a new tool means editing nodes/edges again
- A specialist “researcher” vs “writer” split is clumsy inside one rigid graph

**Why agents (and later MCP) arrived:** let the model **choose tools/steps** within budgets; standardize how tools are exposed across processes.

**Next chapter fixes:** Helix Agent — tool-using agent, multi-agent crew, MCP-backed policy tools.

→ [`05-agents-multiagent-mcp.md`](./05-agents-multiagent-mcp.md)

---

## How to use this file

1. Paper → linear graph → branches → HITL.
2. Write Open problem notes before Ch 05.
3. Stuck >20 minutes → LangGraph docs → **hint** for that step only.
