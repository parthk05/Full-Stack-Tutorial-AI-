# Chapter 07 — Capstone: GroundGate (LLM Eval & Governance for High-Stakes Domains)

**Prerequisites:** Finish Chapters 01–06 (**Helix** Prompt → Structured → Source → Flow → Agent → Ops). Open problem notes from Ch 06 written.

**Mini-project / product name:** **GroundGate** — the governance layer Meridian Labs needs when Helix answers move from HR handbooks into **synthetic regulated pharma and/or finance** corpora. You extend the same `helix/` codebase (or a clearly versioned `groundgate/` package that imports Helix) — this is not a greenfield toy.

**Goal:** Design and ship a **domain-specific LLM evaluation & governance framework** that detects hallucinations, validates **citation grounding**, and scores **faithfulness**. Resume-grade: real problem, measurable grounded-response rate, productized FastAPI — not a notebook.

**How this continues the Helix story:**  
Helix Ops can *see* quality drift. GroundGate **enforces** per-answer gates (allow / refuse / human-review) before release — the missing fail-closed step for high-stakes domains.

**Resume blurb (target — earn it by finishing):**
> Designed and implemented a domain-specific LLM evaluation framework to detect hallucinations and validate citation grounding for regulated pharma/finance use cases. Built a faithfulness and citation scoring engine that gates answers before release, improving grounded response rate under offline and online evaluation.

**Rules for you:**
- Do each phase yourself. Do not skip ahead.
- Difficulty chain: charter → corpus → RAG MVP → faithfulness → citations → gate workflow → (agents) → (MCP) → measured before/after → portfolio pack.
- Use **synthetic** documents only. No real PHI / unauthorized filings / paywalled scrapes.
- Reuse Helix patterns from Ch 01–06; do not invent a parallel stack.
- After each **Check**, verify before continuing.
- Stuck >20 minutes → prior chapter + docs → **hint** for that step only.

**Primary stack:** Python, FastAPI, LangChain, LangGraph, Helix vector store, LangSmith + Langfuse, Pydantic. Optional: MCP.

---

## Concepts you must reuse (Helix → GroundGate)

| Capstone need | Pull from Helix chapter |
|---------------|-------------------------|
| Constrained prompting / refusal | 01 Prompt Desk |
| Typed claims, scores, verdicts | 02 Structured Desk |
| Tools for lookup / calc / policy fetch | 02 |
| Corpus RAG + citations + context budgets | 03 Source Desk |
| Deterministic evaluate → score → gate pipeline | 04 Flow |
| Specialist agents (claim extract, cite-check, risk) | 05 Agent |
| MCP for shared policy/retrieval tools | 05 |
| Traces, datasets, experiments, feedback | 06 Ops |

---

## Phase 0 — Problem framing & governance charter (no coding yet)

### Step 0.1 — Pick your regulated vertical
1. Stay in the **Meridian Labs** universe. Choose **one primary regulated vertical** for v1: **Pharma** (synthetic labels / interactions) *or* **Finance** (synthetic disclosures / risk factors). Optionally design schemas for a second plugin later.
2. Write 5 example user questions that would be dangerous if hallucinated (synthetic dosing/interaction style, or synthetic disclosure questions).
3. In notes: *Which Helix Ops gap (Ch 06 Open problem) does GroundGate close first?*

### Step 0.2 — Define “grounded” for this product
1. In notes, define:
   - **Faithfulness:** answer claims are supported by provided context (no contradictions / inventions).
   - **Citation grounding:** each material claim maps to a real chunk/span that actually supports it.
   - **Grounded response:** passes both thresholds *or* explicitly refuses with reason.
2. Decide fail-closed policy: if scores are below threshold → **block** or **refuse**, never silently ship.

### Step 0.3 — Success metrics (resume-measurable)
1. Define formulas you will implement later, e.g.:
   - `grounded_response_rate = (# answers that pass gate) / (# attempted generations)`
   - `ungrounded_catch_rate` on a labeled adversarial set
   - p95 latency for `answer + evaluate`
2. Write a one-paragraph problem statement suitable for a README / resume project section.

**Check:** You have domain choice, definitions, fail-closed policy, and 3 numeric metrics written down.

---

## Phase 1 — Domain corpus & risk taxonomy (foundation)

### Step 1.1 — Build a synthetic regulated corpus
1. Add a new corpus tree alongside Helix HR docs, e.g. `helix/data/corpus/regulated/`, with 8–20 markdown/text docs labeled `SYNTHETIC — FOR EVAL ONLY`.
   - Pharma: fake drug labels, interaction tables, contraindication blurbs.
   - Finance: fake risk-factor sections, synthetic disclosures, glossary of terms.
2. Keep Helix HR corpus available — GroundGate should still refuse or risk-rank when someone asks regulated questions against the wrong index.
3. Include traps: near-duplicates, superseded docs, conflicting numbers.

### Step 1.2 — Metadata for governance
1. Each chunk/doc gets metadata: `domain`, `doc_type`, `effective_date`, `authority_level`, `superseded_by` (optional).
2. In notes: *Why does authority_level matter when two chunks disagree?*

### Step 1.3 — Risk taxonomy
1. Define severity labels for failed answers: `LOW`, `MEDIUM`, `HIGH`, `CRITICAL` (e.g. invented numeric limit = CRITICAL).
2. Map which question types inherit which default risk.

**Check:** Ingest script (reuse Ch 03) indexes the corpus; you can retrieve a known synthetic fact with source ids.

---

## Phase 2 — Grounded answerer MVP (still no scoring engine)

Difficulty: rebuild the “thing we will govern.”

### Step 2.1 — Regulated RAG answer endpoint
1. Reuse Helix Source Desk patterns. Add `POST /v1/regulated/ask` (keep ordinary `/v1/ask` for HR) returning:  
   `answer`, `citations[{chunk_id, quote_span, doc_id}]`, `prompt_version`, `index_version`, `refused: bool`.
2. System rules: answer **only** from regulated context; if insufficient → refuse.

### Step 2.2 — Context engineering baseline
1. Apply Ch 03 levers: top-k, token budget, metadata filters (`doc_type`, date).
2. Prefer higher `authority_level` when packing context.

**Check:** On a known fact → cited answer. On unknown → refuse. Both traced in LangSmith or Langfuse (Ch 06 habit).

---

## Phase 3 — Faithfulness scoring engine

Difficulty increases: you now **judge** answers, not only generate them.

### Step 3.1 — Claim extraction
1. Given `(answer, context)`, use structured output to extract atomic claims:  
   `Claim { id, text, claim_type: fact|numeric|recommendation|other }`.
2. FastAPI: `POST /v1/eval/extract-claims` (also usable as an internal function).

### Step 3.2 — Faithfulness scorer
1. For each claim, score support against context: `supported | contradicting | not_found`.
2. Aggregate to `faithfulness_score` in `[0, 1]` (document your formula — e.g. supported/total, with CRITICAL weight for numerics).
3. Implement **two modes** (compare in notes):
   - **LLM-as-judge** (structured)
   - **Heuristic / NLI-lite** (overlap, number match, or a small entailment approach — keep it honest about limits)

### Step 3.3 — Unit tests for the scorer
1. Golden fixtures: supported answer, subtle hallucination, numeric swap, refusal.
2. Tests must fail if the scorer marks a clear invention as supported.

**Check:** Fixture suite green; faithfulness drops on an intentionally hallucinated answer.

---

## Phase 4 — Citation grounding validator

### Step 4.1 — Citation schema enforcement
1. Reject responses that assert material claims with empty `citations`.
2. Each citation must reference an existing `chunk_id` in the retrieved set (or corpus).

### Step 4.2 — Span support check
1. For each citation, verify the `quote_span` appears in the chunk (exact or normalized fuzzy match).
2. Score `citation_precision` / `citation_recall` style metrics:
   - precision: cited spans that actually support the linked claim
   - coverage: claims that have ≥1 supporting citation

### Step 4.3 — Combined gate score
1. Define `GroundingReport` Pydantic model: faithfulness, citation scores, per-claim breakdown, `verdict: allow|refuse|human_review`, `risk_level`.
2. `POST /v1/eval/score` accepts answer+context+citations → `GroundingReport`.

**Check:** A fluent answer with fake citation ids fails the gate. A well-cited faithful answer passes.

---

## Phase 5 — Governance workflow (LangGraph) — ship the product loop

Difficulty: wire generate → evaluate → decide as a **fail-closed workflow** (Ch 04).

### Step 5.1 — Graph design (paper first)
Nodes example:
1. `retrieve`
2. `generate`
3. `extract_claims`
4. `score_faithfulness`
5. `validate_citations`
6. `risk_classify`
7. `gate` → allow / refuse / human_review

### Step 5.2 — Implement the graph
1. Shared state includes question, chunks, draft answer, report, final response.
2. Branching: if faithfulness < T1 or citation coverage < T2 → refuse path; if mid-band → `human_review`.

### Step 5.3 — Human-in-the-loop
1. Persist pending reviews (DB or file store).
2. `POST /v1/reviews/{id}/approve` and `/reject` (Ch 04 HITL pattern).
3. Audit log every transition: who/what/when/scores.

### Step 5.4 — Product endpoint
1. `POST /v1/governed-ask` runs the full graph (this is GroundGate’s flagship Helix route).
2. Response always includes `GroundingReport` summary (even on refuse).
3. Compare in notes: ungoverned `/v1/regulated/ask` vs governed `/v1/governed-ask` on the same adversarial question.

**Check:** End-to-end: good Q → allowed+cited; adversarial hallucinating prompt → refused with report; mid-risk → lands in review queue.

---

## Phase 6 — Multi-agent evaluation crew (optional stretch → strongly recommended for resume)

Difficulty: specialists instead of one mega-judge (Ch 05).

### Step 6.1 — Roles
1. **ClaimAgent** — extracts claims.
2. **CitationAgent** — verifies spans & chunk ids (tools: `get_chunk`, `find_span`).
3. **RiskAgent** — maps failures to severity using domain policy.
4. **Supervisor** — merges into `GroundingReport` (or keep deterministic merge from workflow — hybrid is fine).

### Step 6.2 — Budgets & traces
1. Cap tool calls per agent; emit a readable evaluation trace.
2. Compare single-judge vs multi-agent on 20 labeled cases (table in notes).

**Check:** Trace shows distinct agent contributions; quality ≥ single-judge on your adversarial set *or* you document why you kept the workflow-only judge.

---

## Phase 7 — MCP for shared governance tools

### Step 7.1 — MCP server
1. Expose tools/resources: `get_chunk`, `search_corpus`, `get_policy_thresholds`, `list_doc_metadata`.
2. Policy thresholds live as an MCP resource or tool so agents/workflows don’t hardcode magic numbers only in one file.

### Step 7.2 — Consume from evaluator
1. CitationAgent / scoring nodes call MCP tools.
2. In notes: *How would a compliance team update thresholds without redeploying the judge prompt?*

**Check:** Evaluator still passes fixtures when talking to MCP-backed `get_chunk`.

---

## Phase 8 — Offline + online evaluation harness (prove the resume metric)

Difficulty: turn “feels better” into **measured** improvement (Ch 06).

### Step 8.1 — Labeled datasets
1. Create `evals/datasets/groundgate_v1.json` with ≥30 cases:
   - grounded happy path
   - insufficient context
   - citation fabrication
   - numeric hallucination
   - conflicting sources
   - superseded document temptation
2. Fields: `id`, `domain`, `question`, `expected_verdict`, `notes`.

### Step 8.2 — Baseline vs governed comparison
1. Run **ungoverned** RAG (Phase 2 only) vs **governed** graph (Phase 5) on the same dataset.
2. Compute and record:
   - grounded response rate
   - ungrounded catch rate (expected refuse/human_review correctly caught)
   - false block rate (good answers wrongly refused)
3. Save results under `evals/results/` with git commit hash + `prompt_version` + `index_version`.

### Step 8.3 — LangSmith / Langfuse experiments
1. Log each case as a traced run; attach scores as feedback/metrics.
2. Dashboard or exported chart: before/after grounded rate.

**Check:** You can show a numeric improvement (or honest tradeoff: higher refuse rate, lower hallucination escape). Document both.

---

## Phase 9 — Production hardening & FastAPI product polish

### Step 9.1 — API surface for a portfolio demo
Minimum routes:
- `POST /v1/governed-ask`
- `POST /v1/eval/score`
- `GET /v1/reviews?status=pending`
- `POST /v1/reviews/{id}/approve|reject`
- `GET /health`
- `GET /v1/metrics/summary` (aggregate grounded rate from recent runs — simple store OK)

### Step 9.2 — Governance headers & config
1. Settings: thresholds, model ids, `FAIL_CLOSED=true`, max context tokens, feature flags.
2. Every response: `request_id`, versions, verdict, risk_level.

### Step 9.3 — Security & compliance notes (README section)
Write what you would add for real pharma/finance (even if not fully built):
- PII/PHI redaction before traces
- access control on review APIs
- retention policy for audit logs
- model/provider DPIA-style checklist (lightweight)

**Check:** Fresh clone instructions in README bring up the API; demo script hits happy + refuse paths.

---

## Phase 10 — Portfolio packaging (make it resume-ready)

### Step 10.1 — README that sells the engineering
Must include:
- Problem statement (high-stakes hallucination risk)
- Architecture diagram (retrieve → generate → score → gate)
- Metric table (before/after)
- How to run locally
- Limitations (LLM-as-judge bias, synthetic corpus, not legal/medical advice)

### Step 10.2 — Demo script & sample report
1. `scripts/demo_groundgate.py` prints a failing ungrounded answer vs governed refuse + `GroundingReport`.
2. Save one redacted sample JSON report in `docs/sample_grounding_report.json`.

### Step 10.3 — Resume / interview bullets (write your own final wording)
Draft 3 bullets from *your* measured results, e.g.:
- Built faithfulness + citation scoring with fail-closed LangGraph gate for synthetic pharma/finance RAG
- Improved grounded response rate from X% → Y% on a 30-case adversarial eval set
- Instrumented with LangSmith/Langfuse; human-review queue for mid-risk verdicts

**Check:** A stranger can run the demo in <15 minutes and understand the before/after story.

---

## Phase 11 — Self-review checklist

Before you call the capstone done:

- [ ] Synthetic regulated corpus with metadata + traps
- [ ] Grounded RAG answerer with citations + refusals
- [ ] Faithfulness scoring engine with fixture tests
- [ ] Citation grounding validator (id + span checks)
- [ ] LangGraph governance workflow with allow/refuse/human_review
- [ ] Audit log of gate decisions
- [ ] Offline eval set ≥30 cases with before/after metrics recorded
- [ ] Traces/metrics in LangSmith and/or Langfuse
- [ ] FastAPI demo routes + README + demo script
- [ ] You reused prompting, structured I/O, tools/RAG, workflows, (ideally) agents/MCP, and LLMOps
- [ ] Resume bullets match **measured** results, not aspirations

---

## Suggested build order (difficulty chain)

```text
Charter → Corpus → RAG MVP → Faithfulness → Citations → Gate workflow
    → (Agents) → (MCP) → Eval harness & metrics → Harden → Portfolio pack
```

Do not jump to agents before the scoring fixtures are green — flashy multi-agent without a correct gate is not governance.

---

## What “done” looks like for interviews

You should be able to whiteboard:
1. Why fail-closed beats “the model said so”
2. Faithfulness vs citation coverage (and why you need both)
3. Where LangGraph sits vs agents vs MCP in *your* architecture
4. How you measured grounded response rate and what still escapes the gate

---

## How to use this file

1. Complete Phase 0–2 for an MVP story.
2. Phases 3–5 are the **core resume project** — do not skip.
3. Phases 6–7 deepen seniority signals; Phase 8 is what makes the metric credible.
4. Phases 9–10 are what make it demoable to recruiters/hiring managers.
5. Stuck >20 minutes → prior chapter + docs → **hint** for that step only.
