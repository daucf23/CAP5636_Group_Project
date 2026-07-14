# Open Questions

Track decisions that still affect planning guidance. Move settled items into [project-overview.md](./project-overview.md) or the design spec. Planning docs model compute/time; they are not frozen contracts.

## Answered

| # | Question | Answer |
| --- | --- | --- |
| 1 | Project topic / problem? | NanoWiki: pretrain small decoder-only LM on Wikipedia; study factual consistency / hallucination vs general baseline |
| 4 | Language / libraries? | Python; NanoChat (GPT-style decoder-only); Hugging Face `wikimedia/wikipedia` |
| 6 | Evaluation (v1)? | Cross-domain bpb on frozen Wiki/general holdouts + matched-checkpoint curves + blinded fixed-prompt ratings. No full hallucination bench in v1. |
| 7 | Who is on the team? | Sahil Bhikha, Thomas Belyakov, David Almeida II |
| — | Compute posture? | RTX 5090 guaranteed; Newton/cloud optional. See [compute-budget.md](./compute-budget.md). |
| — | Hardware inventory? | UCF Newton (V100 + H100); student RTX 5090 + 3080 Ti; optional cloud rental |
| — | Primary run shape? | **Depth 8**, matched 0.25–0.5B token budgets; no depth-12 run before submission |
| — | Baseline for v1? | **G-General:** same architecture, tokenizer, recipe, and consumed-token budget as W-Wiki |
| — | Timeline? | July 13–25 soft target; July 27 hard deadline |
| — | Train from scratch vs continue? | Prefer scratch. If continued pretraining is needed, both domains start from the exact same base checkpoint and receive equal tokens. |
| — | Tokenizer (v1 default)? | **Reuse NanoChat tokenizer as-is** (simplest; keeps continue-pretrain fallback viable). Revisit only if tok_eval on Wikipedia looks pathological. |
| — | Val split? | **Hold out by article ID** (unseen articles). Target size TBD (~1–5% of used subset or a fixed article count). |
| — | Abstract milestone? | **Already submitted** (original NanoWiki brief). Working copy: [project-abstract-draft.md](./project-abstract-draft.md). |
| — | Repo / NanoChat integration? | **Thin wrapper**: NanoChat as submodule/pinned clone; this repo owns data prep, configs, eval, prompts. |
| — | Work split? | **3 unassigned lanes:** A=Data, B=Train/infra, C=Eval/docs. See [team-work-split.md](./team-work-split.md). People not assigned yet. |

## Priority 1 — Must close by Jul 14–15

1. **Assign people to lanes A / B / C immediately** ([team-work-split.md](./team-work-split.md)).

2. **Which exact NanoChat commit and tokenizer artifact are pinned?**

3. **What throughput, VRAM, and attention backend does paired smoke measure on the 5090?**
   Freeze the equal 0.25–0.5B token budget from this result.

## Priority 2 — Technical decisions

4. **Which pinned general-text shards form G-General and its holdout?**

5. **What exact validation sizes and IDs/manifests are frozen for both domains?**

6. **Does the team approve full-context attention if NanoChat’s 5090 SDPA sliding-window path is slow?**
   The choice must be identical for both runs.

7. **Is there time after core results for a small factuality benchmark?**
   Default answer is no; it must not delay matched training, cross-domain evaluation, or writing.

## Priority 3 — Collaboration

8. **Day-to-day discussion channel?** (GitHub Issues, Discord, Slack, etc.)

9. **Who owns final paper integration and slide integration?** Lane C coordinates, but all members must contribute and speak.
