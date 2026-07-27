# Chapter 03 — Helix Source Desk (RAG & Context Engineering)

**Prerequisites:** Chapters 01–02. Prompt Desk + Structured Desk work; Open problem notes from Ch 02 written.

**Mini-project:** **Helix Source Desk** — give Helix a real Meridian Labs **document corpus**. Ingest → retrieve → generate with **citations**, using context engineering so the model sees the right slices of the handbook.

**Goal:** Fix “tools can’t see the handbook” by shipping grounded Q&A — and discover why one-shot RAG still isn’t a full product pipeline.

**Rules for you:**
- Do each step yourself. Do not skip ahead.
- Vertical slice first; optimize later.
- Extend `helix/` (add `rag/`, `data/corpus/`).
- Optional light LangSmith/Langfuse peek — deep ops wait for Ch 06.

**Libraries:** LangChain splitters, embeddings, vector store (Chroma / FAISS / PGVector — pick one), FastAPI.

---

## Why this chapter exists

Structured Desk stopped some ID-level hallucinations but failed on handbook knowledge. The industry response was **RAG**: retrieve evidence, then generate. **Context engineering** is the craft of what evidence enters the window — not “dump the PDF.”

---

## Phase 0 — Concepts

### Step 0.1 — Connect to Ch 02 pain
1. Restate in one sentence why stub tools were not enough.
2. Sketch: docs → chunks → embeddings → index → retrieve → prompt → answer.

### Step 0.2 — Context engineering
1. Define it in your words (select, order, compress, budget).
2. List levers: chunk size, overlap, top-k, filters, ordering, caps.
3. In notes: *Why is stuffing the whole handbook into the prompt not context engineering?*

**Check:** You can separate retrieval quality from packing quality.

---

## Phase 1 — Meridian corpus

### Step 1.1 — Write the handbook (synthetic)
1. Add 8–15 markdown files under `helix/data/corpus/` clearly marked `SYNTHETIC`.
   Examples: remote work, PTO, expenses, travel, security laptop, incident reporting, vendor access, code of conduct.
2. Plant **≥3 quiz facts** the base model won’t know (weird policy codes, odd numeric limits, a fake effective date).
3. Include one **trap**: two docs that slightly disagree, or a `SUPERSEDED` note.

### Step 1.2 — Chunk + metadata
1. Split with a text splitter; record size/overlap rationale.
2. Metadata per chunk: `doc_id`, `title`, `category` (`hr|security|finance|ops`), `chunk_id`, optional `effective_date`.

**Check:** Printed chunks look like coherent units, not random mid-sentence noise (mostly).

### Step 1.3 — Embed + index
1. `python -m helix.rag.ingest` (or similar) builds a persisted index.
2. Keep Ch 02 stub tools available — you will hybridize later.

**Check:** Similarity search for a planted phrase returns the right chunk in top-k.

---

## Phase 2 — Mini-project: Source Desk API

### Step 2.1 — RAG ask
1. `POST /v1/ask` body: `{ "question": "...", "category": null | "hr" | ... }`.
2. Retrieve → pack context → generate with Ch 01-style constraints (“only from context; else refuse”).
3. Return structured result (reuse Ch 02 habits):  
   `GroundedAnswer { answer, citations[{chunk_id, doc_id, quote}], refused, confidence, prompt_version, index_version }`.

**Check:** Planted fact → cited answer. Unknown topic → refuse (not a confident invention).

### Step 2.2 — Keep tools in the story
1. Optional hybrid: if question contains `POL-…`, call `get_policy_by_id` **and/or** retrieve.
2. In notes: *When is a stub/DB tool better than vector search?*

**Check:** At least one hybrid example works end-to-end.

---

## Phase 3 — Context engineering upgrades

Create `helix/evals/source_desk_smoke.json` with **5 fixed questions** (answerable + 1 refuse). Improve one lever at a time.

### Step 3.1 — Metadata filter
Category filter changes retrieval — prove it.

### Step 3.2 — Budget
Cap total context tokens/chars; drop lowest-score chunks first.

### Step 3.3 — Packing format
Try labeled blocks (`[chunk_id=…]`) vs plain concatenation; pick one.

### Step 3.4 — One upgrade
Rerank **or** compress-then-answer; compare on the 5-question set (table in notes).

**Check:** Notes show before/after for ≥1 lever.

---

## Phase 4 — Failure modes

### Step 4.1 — Reproduce
Wrong chunk → wrong confident answer; stale chunk; multi-doc question with top-k=1.

### Step 4.2 — Re-ingest
Edit one doc → re-ingest → answer changes; bump `index_version`.

### Step 4.3 — Optional trace peek
One `/v1/ask` trace in LangSmith or Langfuse (retrieve vs generate). No full eval harness yet.

---

## Phase 5 — Self-review checklist

- [ ] Synthetic Meridian corpus ingested
- [ ] `/v1/ask` returns citations + refusal behavior
- [ ] `index_version` + `prompt_version` on responses
- [ ] ≥2 context levers tried; smoke set of 5 questions in git
- [ ] You can explain chunking, embeddings, top-k, budgets, grounding

---

## Open problem → Chapter 04

Source Desk answers many handbook questions. Now notice product gaps:

1. Every request is still **one shot**: retrieve → answer. Real intake needs steps (classify intent → retrieve → draft → maybe notify → store transcript).
2. Low-confidence answers can still **ship** with no human review branch.
3. Retries, fallbacks, and “if expense-related run an extra check” are awkward inside a single handler.

**Why the industry adopted workflows/graphs:** business logic needs **explicit control flow**, not only a smart prompt.

**Next chapter fixes:** LangGraph pipelines with branches, caps, and human-in-the-loop — Helix Flow.

→ [`04-ai-workflows.md`](./04-ai-workflows.md)

---

## How to use this file

1. Vertical slice (Phase 2) before upgrades.
2. Write Open problem notes before Ch 04.
3. Stuck >20 minutes → LangChain RAG docs → **hint** for that step only.
