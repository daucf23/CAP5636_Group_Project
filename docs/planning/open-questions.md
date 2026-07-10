# Open Questions

Track decisions the team still needs to make. Move answered items into [project-overview.md](./project-overview.md) or the design spec.

## Answered

| # | Question | Answer |
| --- | --- | --- |
| 1 | Project topic / problem? | NanoWiki: pretrain small decoder-only LM on Wikipedia; study factual consistency / hallucination vs general baseline |
| 4 | Language / libraries? | Python; NanoChat (GPT-style decoder-only); Hugging Face `wikimedia/wikipedia` |
| 6 | Evaluation (v1)? | **Simple:** held-out Wikipedia val loss / perplexity (bpb) + fixed qualitative encyclopedic prompts. No dedicated hallucination bench in v1. |
| 7 | Who is on the team? | Sahil Bhikha, Thomas Belyakov, David Almeida II |
| — | Compute posture? | Stay realistic; subset Wikipedia; prefer Tier 0 smoke test → Tier 1 depth 8–12. See [compute-budget.md](./compute-budget.md). |

## Priority 1 — Scope still open

1. **What does the course require for submission?**  
   (code, report length, presentation, dataset constraints, individual vs group grading)

2. **What is explicitly out of scope for v1?**  
   Draft non-goals are in the overview; confirm with the team.

## Priority 2 — Technical decisions

3. **What GPUs / cloud credits / campus machines do we have, and what is the soft dollar cap?**  
   This picks Tier 1 depth + token budget. See [compute-budget.md](./compute-budget.md).

4. **What is the exact baseline (matched token budget)?**  
   - General-text NanoChat run (which corpus?)  
   - Short-train / untuned control only  
   - Both (only if compute allows)

5. **Do we train from scratch on Wikipedia only, or continue from an existing NanoChat checkpoint?**

6. **Tokenizer:** reuse NanoChat’s tokenizer as-is, or train/adapt on Wikipedia?

7. **First runnable experiment:** depth 8 or 12? Token cap (e.g. 100M / 500M / ~1B)?

8. **Validation split strategy:** by article ID / random articles? Target val size?

## Priority 3 — Collaboration

9. **Roles / ownership** (data, training, eval, report)?

10. **Hard deadlines from the syllabus?**

11. **Day-to-day discussion channel?** (GitHub Issues, Discord, Slack, etc.)
