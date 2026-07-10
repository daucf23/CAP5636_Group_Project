# Open Questions

Track decisions the team still needs to make. Move answered items into [project-overview.md](./project-overview.md) or the design spec.

## Answered

| # | Question | Answer |
| --- | --- | --- |
| 1 | Project topic / problem? | NanoWiki: pretrain small decoder-only LM on Wikipedia; study factual consistency / hallucination vs general baseline |
| 4 | Language / libraries? | Python; NanoChat (GPT-style decoder-only); Hugging Face `wikimedia/wikipedia` |
| 6 | Evaluation (high level)? | Val loss + perplexity on held-out Wikipedia; qualitative encyclopedic completions; optional step/token ablations |
| 7 | Who is on the team? | Sahil Bhikha, Thomas Belyakov, David Almeida II |

## Priority 1 — Scope still open

1. **What does the course require for submission?**  
   (code, report length, presentation, dataset constraints, individual vs group grading)

2. **What is explicitly out of scope for v1?**  
   Draft non-goals are in the overview; confirm with the team.

3. **How do we operationalize “hallucination / factual inconsistency”?**  
   Motivation emphasizes factuality, but the written eval plan is mostly perplexity + qualitative tone. Options:
   - **A)** Stick to perplexity + qualitative encyclopedic prompts (simplest)
   - **B)** Add a small closed-book QA / fact-check set (e.g. prompts with known Wikipedia answers)
   - **C)** Use an external judge / checklist for factual claims in generations

## Priority 2 — Technical decisions

4. **What is the exact baseline?**  
   - Untuned / randomly initialized NanoChat (no Wikipedia)
   - NanoChat pretrained on a general corpus (which corpus, matched token budget?)
   - Both

5. **Compute: what GPUs / cloud / local machines do we have?**  
   Full `20231101.en` (~11.6 GB) may need subsetting depending on hardware.

6. **Do we train from scratch on Wikipedia only, or continue from an existing NanoChat checkpoint?**

7. **Tokenizer:** reuse NanoChat’s tokenizer as-is, or train/adapt on Wikipedia?

8. **Model size / context length / training budget** for the first runnable experiment?

9. **Validation split strategy:** by article ID / random articles / time-based? Target val size?

## Priority 3 — Collaboration

10. **Roles / ownership** (data, training, eval, report)?

11. **Hard deadlines from the syllabus?**

12. **Day-to-day discussion channel?** (GitHub Issues, Discord, Slack, etc.)
