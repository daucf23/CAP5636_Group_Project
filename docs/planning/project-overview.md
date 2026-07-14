# Project Overview

**Course:** CAP 5636  
**Working final title:** NanoWiki: A Controlled Study of Wikipedia-Only vs General-Text Pretraining for a Small Transformer
**Repository:** [daucf23/CAP5636_Group_Project](https://github.com/daucf23/CAP5636_Group_Project)  
**Status:** Abstract submitted; design revised for course-rubric alignment; implementation is now on the critical path

## Team

- Sahil Bhikha
- Thomas Belyakov
- David Almeida II

**Work split (lanes only, people not assigned yet):**

| Lane | Focus |
| --- | --- |
| **A — Data** | Wikipedia prep, article-ID split, shards |
| **B — Train / infra** | NanoChat pin, configs, W-Wiki/G-General runs |
| **C — Eval / docs** | cross-domain bpb, prompts, results, README/report |

Details: [team-work-split.md](./team-work-split.md).

## Problem and motivation

Small language models are computationally accessible, but their behavior depends strongly on pretraining-data composition. Wikipedia provides a large, structured, relatively neutral corpus for studying the benefits and costs of domain-restricted pretraining.

**Research question:** At fixed model size and training-token budget, how does Wikipedia-only pretraining affect in-domain fit, out-of-domain fit, and encyclopedic generation style relative to general-text pretraining?

The submitted proposal motivates factual consistency, but v1 does not treat perplexity or style as proof of reduced hallucination.

## Approach

1. Use **NanoChat** ([karpathy/nanochat](https://github.com/karpathy/nanochat)) as a **pinned submodule / clone**; this repo is a **thin wrapper** (data prep, run configs, eval, prompts) rather than a full fork.
2. Train **W-Wiki** and **G-General** with the same depth, tokenizer, initialization recipe, optimizer settings, and consumed-token budget.
3. Prefer from-scratch pretraining; if continued pretraining becomes necessary, start both runs from the exact same checkpoint.
4. Use one pinned NanoChat tokenizer artifact for both domains and record its provenance/checksum.
5. Save intermediate checkpoints to obtain learning curves without extra training. Depth 12 and additional model families are out of scope.

## Data

| Item | Detail |
| --- | --- |
| Source | Hugging Face [`wikimedia/wikipedia`](https://huggingface.co/datasets/wikimedia/wikipedia) |
| Split | `20231101.en` |
| Size | ~11.6 GB English text (2023 dump-derived) |
| License | CC BY-SA 3.0 and GFDL (original Wikipedia content) |
| Prep | Preprocess for NanoChat pretraining; **hold out validation by article ID** (unseen articles) |

## Evaluation plan (v1 — keep simple)

**Quantitative**

- Validation **bits-per-byte (bpb)** on frozen Wikipedia and general-text holdouts
- Compare W-Wiki and G-General at equal training tokens, including intermediate checkpoints
- Report the cross-domain trade-off rather than selecting only the metric favorable to W-Wiki

**Qualitative**

- Fixed encyclopedic prompt sheet with identical decoding
- Model-anonymized scoring by at least two team members for coherence, repetition, neutral tone, and Wikipedia-like structure
- Include representative successes, failures, and disagreements

**Deferred (not v1):** full hallucination, closed-book QA, or external-judge evaluation. Claims are limited to domain fit and observed generation behavior.

**Design spec:** [2026-07-10-nanowiki-design.md](../superpowers/specs/2026-07-10-nanowiki-design.md)

## Compute posture (draft)

- Prefer **subset of Wikipedia**, not necessarily full 11.6 GB
- Guaranteed hardware: student **RTX 5090**; Newton/cloud are optional accelerators, not dependencies
- Plan (July 13–25): paired smoke → freeze equal budget → W-Wiki + G-General → cross-domain evaluation → paper/slides
- Target **0.5B tokens per run**; reduce both equally to no less than ~0.25B if measured throughput or stability requires it
- Compute/time model: [compute-budget.md](./compute-budget.md)

## Success criteria (draft)

- Reproducible training + eval pipeline from this repo
- Controlled Wikipedia-vs-general comparison at matched tokens
- Cross-domain bpb learning curves plus blinded qualitative samples
- Documented limitations (especially: perplexity ≠ factuality; corpus contamination, compute, and data caps)

## Non-goals (draft — confirm)

- Not building a production chatbot or retrieval-augmented system
- Not claiming that Wikipedia pretraining reduces hallucination without a dedicated benchmark
- Not running full NanoChat d26 8×H100 speedrun unless compute appears later
- Keep the model small and runnable for the team

## Proposed deliverables

1. **Project abstract** — **submitted** (original brief); archive copy in [project-abstract-draft.md](./project-abstract-draft.md)
2. Data preprocessing + train/eval scripts based on NanoChat
3. Experiment results (tables + sample generations)
4. 6–8 page NeurIPS-style final paper, reproducible repository, and 10–12 presentation slides

## References

1. [karpathy/nanochat](https://github.com/karpathy/nanochat)
2. [wikimedia/wikipedia on Hugging Face](https://huggingface.co/datasets/wikimedia/wikipedia)
3. [Attention Is All You Need](https://arxiv.org/pdf/1706.03762)
4. [Textbooks Are All You Need](https://arxiv.org/pdf/2306.11644)
5. [DataComp-LM](https://arxiv.org/pdf/2406.11794)

## Next step

Review the design spec: [2026-07-10-nanowiki-design.md](../superpowers/specs/2026-07-10-nanowiki-design.md). Remaining open items: [open-questions.md](./open-questions.md).
