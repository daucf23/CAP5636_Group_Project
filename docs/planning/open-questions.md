# Open Questions

Track decisions that still affect planning guidance. Move settled items into [project-overview.md](./project-overview.md) or the design spec. Planning docs model compute/time; they are not frozen contracts.

## Answered

| # | Question | Answer |
| --- | --- | --- |
| 1 | Project topic / problem? | NanoWiki: pretrain small decoder-only LM on Wikipedia; study factual consistency / hallucination vs general baseline |
| 4 | Language / libraries? | Python; NanoChat (GPT-style decoder-only); Hugging Face `wikimedia/wikipedia` |
| 6 | Evaluation (v1)? | **Simple:** held-out Wikipedia val loss / perplexity (bpb) + fixed qualitative encyclopedic prompts. No dedicated hallucination bench in v1. |
| 7 | Who is on the team? | Sahil Bhikha, Thomas Belyakov, David Almeida II |
| — | Compute posture? | Newton first; student 5090 / 3080 Ti backup; cloud contingency ~$50. See [compute-budget.md](./compute-budget.md). |
| — | Hardware inventory? | UCF Newton (V100 + H100); student RTX 5090 + 3080 Ti; optional cloud rental |
| — | First main run shape? | **Start depth 8 @ ~0.5B tokens**; scale to depth 12 only after matched d8 pair succeeds |
| — | Baseline for v1? | **C-short:** brief train (~5–25M tokens, ~1–5% of Run B) on same arch/tokenizer; full general-text matched run deferred |
| — | Timeline? | Target **~3 weeks** to a complete v1 (pipeline + d8 Wikipedia run + C-short + eval/report draft) |
| — | Train from scratch vs continue? | **Prefer A (from scratch)** for a clean story; treat **continued pretrain / light fine-tune from a small NanoChat checkpoint** as the more realistic fallback if scratch quality is weak in 3 weeks. Undecided until Tier 0 + first d8 attempt. |

## Priority 1 — Scope still open

1. **What does the course require for submission?**  
   (code, report length, presentation, dataset constraints, individual vs group grading)

2. **What is explicitly out of scope for v1?**  
   Draft non-goals are in the overview; confirm with the team.

## Priority 2 — Technical decisions

3. **Newton access status?**  
   Account ready? Faculty sponsor? Can we request 1× H100 easily, or do we need `highgpu`?

4. **Confirm soft cloud contingency cap** (proposed **$50**).

5. **Tokenizer:** reuse NanoChat’s tokenizer as-is, or train/adapt on Wikipedia?

6. **Validation split strategy:** by article ID / random articles? Target val size?

7. **If fallback to continue-pretrain:** which checkpoint / depth, and how do we keep C-short comparable?

## Priority 3 — Collaboration

8. **Roles / ownership** (data, training, eval, report)?

9. **Exact course deadlines** within / beyond the ~3-week working window?

10. **Day-to-day discussion channel?** (GitHub Issues, Discord, Slack, etc.)
