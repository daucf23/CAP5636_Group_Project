# Project Overview

**Course:** CAP 5636  
**Title:** NanoWiki: Pretraining a Small Decoder-Only Transformer from Scratch on Curated Wikipedia Data  
**Repository:** [daucf23/CAP5636_Group_Project](https://github.com/daucf23/CAP5636_Group_Project)  
**Status:** Abstract submitted; **design spec drafted** for review → then implementation plan

## Team

| Member | Role (draft) |
| --- | --- |
| Sahil Bhikha | TBD |
| Thomas Belyakov | TBD |
| David Almeida II | TBD |

## Problem and motivation

Small language models are computationally accessible but often struggle with hallucinations and factual inconsistency. Typical pretraining corpora are massive and stylistically diverse. Wikipedia provides a large, structured, neutral corpus that is a strong candidate for testing whether restricting pretraining to encyclopedic text can reduce hallucination and improve factual consistency in a small model.

**Research question:** Does pretraining a small decoder-only transformer primarily (or only) on Wikipedia improve factual consistency and encyclopedic generation quality relative to a general-text / untuned NanoChat baseline?

## Approach

1. Use **NanoChat** ([karpathy/nanochat](https://github.com/karpathy/nanochat)) as a **pinned submodule / clone**; this repo is a **thin wrapper** (data prep, run configs, eval, prompts) rather than a full fork.
2. Prefer **from-scratch** pretraining on curated Wikipedia; keep **continue-pretrain / light fine-tune from a small NanoChat checkpoint** as a realistic fallback if scratch quality is too weak in ~3 weeks.
3. **Reuse NanoChat’s tokenizer as-is** for v1 (simplest; keeps the continue-pretrain fallback viable).
4. Compare against **C-short**: same architecture/init recipe, brief train (~5–25M tokens). Defer a full matched general-text pretrain if time remains.
5. Optionally scale to depth 12 and/or ablate data size / training duration after the d8 run works.

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

- Validation **bits-per-byte (bpb)** on **article-ID** held-out Wikipedia articles (primary); loss/perplexity optional secondary
- Compare Wikipedia-trained depth-8 model (**Run B**) vs **C-short** control (same arch/tokenizer/init/eval set; **not** equal token budget)

**Qualitative**

- Fixed encyclopedic prompt sheet → compare coherence, repetition, neutral tone, Wikipedia-like structure
- Desired outcome: lower Wikipedia val loss/bpb and more encyclopedic completions without excessive repetition or degeneration

**Deferred (not v1):** dedicated hallucination / closed-book QA / external judge metrics. Motivation still mentions factuality; state that limitation explicitly in the write-up.

**Design spec:** [2026-07-10-nanowiki-design.md](../superpowers/specs/2026-07-10-nanowiki-design.md)

## Compute posture (draft)

- Prefer **subset of Wikipedia**, not necessarily full 11.6 GB
- Hardware: **UCF Newton first** (H100 preferred), student **RTX 5090 / 3080 Ti** backup, cloud only as contingency (~$50 soft cap)
- Plan (~3 weeks, guidance): Tier 0 smoke → **depth 8 @ ~0.5B** Wikipedia → **C-short** → write-up; optional C-full or depth 12 only if ahead
- Compute/time model: [compute-budget.md](./compute-budget.md)

## Success criteria (draft)

- Reproducible training + eval pipeline from this repo
- Clear baseline vs Wikipedia-adapted comparison (**bpb** + qualitative samples)
- Documented limitations (especially: perplexity ≠ hallucination; compute/data caps)

## Non-goals (draft — confirm)

- Not building a production chatbot or retrieval-augmented system
- Not claiming SOTA factuality without dedicated hallucination / fact-checking benchmarks in v1
- Not running full NanoChat d26 8×H100 speedrun unless compute appears later
- Keep the model small and runnable for the team

## Proposed deliverables

1. **Project abstract** — **submitted** (original brief); archive copy in [project-abstract-draft.md](./project-abstract-draft.md)
2. Data preprocessing + train/eval scripts based on NanoChat
3. Experiment results (tables + sample generations)
4. Final report and presentation materials per later course requirements (TBD)

## References

1. [karpathy/nanochat](https://github.com/karpathy/nanochat)
2. [wikimedia/wikipedia on Hugging Face](https://huggingface.co/datasets/wikimedia/wikipedia)
3. [Attention Is All You Need](https://arxiv.org/pdf/1706.03762)
4. [Textbooks Are All You Need](https://arxiv.org/pdf/2306.11644)
5. [DataComp-LM](https://arxiv.org/pdf/2406.11794)

## Next step

Review the design spec: [2026-07-10-nanowiki-design.md](../superpowers/specs/2026-07-10-nanowiki-design.md). Remaining open items: [open-questions.md](./open-questions.md).
