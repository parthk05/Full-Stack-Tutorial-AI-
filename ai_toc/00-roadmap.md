# AI Learning Pathway — Roadmap

**Goal:** Learn modern LLM application development by **building one product in layers**. Each chapter ships a working mini-project that is useful — and intentionally incomplete. The pain you feel at the end of chapter *N* is exactly why chapter *N+1* exists. That is how these advancements happened in the industry, and how you will feel why they matter.

**Stack:** Python + FastAPI. LangChain / LangGraph. LangSmith + Langfuse (light mid-path, deep in Ch 06–07).

This AI track is **standalone**. It does not depend on any other tutorial project in the repo.

---

## The product you will build: Helix

**Helix** is an internal knowledge assistant for a fictional company, **Meridian Labs** (biotech — employee policies first; synthetic regulated pharma/finance docs in the capstone).

One codebase grows every chapter. Do not start unrelated demos.

| Chapter | Mini-project you ship | Works for… | Open problem left for next chapter |
|---------|----------------------|------------|-------------------------------------|
| [01](./01-prompting-and-reliability.md) | **Helix Prompt Desk** | Comparing prompt strategies over FastAPI | Fluent answers still invent policy facts; free text is hard for other systems to consume |
| [02](./02-tools-and-structured-outputs.md) | **Helix Structured Desk** | Typed replies + lookup tools on a tiny policy stub DB | Only helps when an ID/row exists — real knowledge lives in long documents tools cannot see |
| [03](./03-rag-and-context-engineering.md) | **Helix Source Desk** | RAG over the Meridian handbook with citations | One-shot retrieve→answer; no multi-step business process; weak answers can still ship |
| [04](./04-ai-workflows.md) | **Helix Flow** | LangGraph intake: classify → retrieve → draft → branch → HITL | Fixed graphs struggle with open-ended goals; tools are hardcoded inside nodes |
| [05](./05-agents-multiagent-mcp.md) | **Helix Agent** | Tool-choosing agents, multi-agent crew, MCP tools | Quality regressions are invisible; debugging is expensive; no systematic measurement |
| [06](./06-llmops.md) | **Helix Ops** | Tracing, golden evals, versions, feedback | Measuring isn’t enough for high-stakes answers — you need fail-closed faithfulness/citation gates |
| [07](./07-llm-eval-governance-capstone.md) | **GroundGate** (capstone) | Eval + governance framework for regulated Q&A | — (portfolio project) |

```text
Prompt Desk ──issue──► Structured Desk ──issue──► Source Desk ──issue──► Flow
                                                                              │
GroundGate ◄──issue── Ops ◄──issue── Agent ◄──────────────────────────────────┘
```

---

## How learning works here

| Principle | Meaning |
|-----------|---------|
| Ship, then feel the gap | Finish the mini-project and the **Open problem** section before starting the next chapter |
| Same product, new layer | Extend `helix/` — do not rewrite from scratch each time |
| Concepts before libraries | *Why* first, then implement |
| Check gates | Verify every **Check** before continuing |
| Hints, not spoilers | Stuck ~20 min → docs → hint for that step only |

---

## Topic map

| Topic | Chapter |
|-------|---------|
| Prompting methods | 01 |
| Hallucination (recognize → ground → measure → govern) | 01 → 03 → 06 → 07 |
| Structured outputs + function calling / tools | 02 |
| RAG + context engineering | 03 |
| AI workflows | 04 |
| Agents + multi-agent + MCP | 05 |
| LLMOps (LangSmith, Langfuse) | 06 |
| Eval & governance capstone | 07 |

---

## Suggested layout (stick to it)

```text
helix/
  app/                 # FastAPI entry, routers
  prompts/             # versioned prompt files
  tools/               # function-calling tools
  rag/                 # ingest, retriever, context packing
  workflows/           # LangGraph graphs
  agents/              # agent + multi-agent + MCP client
  evals/               # datasets + runners (Ch 06–07)
  data/corpus/         # Meridian synthetic docs
requirements.txt
.env.example
```

---

## Library placement

| Tool | First use | Deep use |
|------|-----------|----------|
| LangChain | Ch 01–02 | Ch 03–05 |
| LangGraph | Ch 04 | Ch 05, 07 |
| LangSmith / Langfuse | Peek Ch 03–05 | Ch 06–07 |

---

## Rules for every chapter

1. Finish the previous chapter’s checklist **and** write the **Open problem** notes before starting the next.
2. Never commit API keys — `.env` + `.gitignore`.
3. Prefer official docs when stuck.
4. Answer *why* questions in your own notes (interview layer).

---

## Suggested pace

| Chapter | Sessions |
|---------|----------|
| 01 | 1–2 |
| 02 | 2–3 |
| 03 | 3–4 |
| 04 | 2–3 |
| 05 | 4–5 |
| 06 | 2–3 |
| 07 | 6–10 |

---

## How to use this folder

1. Read this roadmap.
2. Open Chapter 01; build Helix Prompt Desk end-to-end.
3. Only after the open problem is clear in your notes, open Chapter 02.
4. Continue the chain through GroundGate (Ch 07).
