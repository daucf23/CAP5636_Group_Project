# Project Overview

**Course:** CAP 5636  
**Title:** NanoWiki: Pretraining a Small Decoder-Only Transformer from Scratch on Curated Wikipedia Data  
**Repository:** [daucf23/CAP5636_Group_Project](https://github.com/daucf23/CAP5636_Group_Project)  
**Status:** Planning (problem statement captured; design pending)

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

1. Use **NanoChat** ([karpathy/nanochat](https://github.com/karpathy/nanochat)) — a minimal GPT-style decoder-only transformer for autoregressive LM — as the training codebase.
2. Pretrain (or continue-pretrain) a small model on curated Wikipedia text.
3. Compare against **C-short**: same architecture, brief train (~5–25M tokens). Defer a full matched general-text pretrain if time remains.
4. Optionally scale to depth 12 and/or ablate data size / training duration after the d8 run works.

## Data

| Item | Detail |
| --- | --- |
| Source | Hugging Face [`wikimedia/wikipedia`](https://huggingface.co/datasets/wikimedia/wikipedia) |
| Split | `20231101.en` |
| Size | ~11.6 GB English text (2023 dump-derived) |
| License | CC BY-SA 3.0 and GFDL (original Wikipedia content) |
| Prep | Preprocess for NanoChat pretraining; create a held-out validation set of unseen articles |

## Evaluation plan (v1 — keep simple)

**Quantitative**

- Validation loss / perplexity (or NanoChat bits-per-byte) on held-out Wikipedia articles
- Compare Wikipedia-adapted model vs a **matched-budget** baseline

**Qualitative**

- Fixed encyclopedic prompts → compare coherence, repetition, neutral tone, Wikipedia-like structure
- Desired outcome: lower Wikipedia perplexity and more encyclopedic completions without excessive repetition or degeneration

**Deferred (not v1):** dedicated hallucination / closed-book QA / external judge metrics. Motivation still mentions factuality; we will discuss that limitation explicitly in the report.

## Compute posture (draft)

- Prefer **subset of Wikipedia**, not necessarily full 11.6 GB
- Hardware: **UCF Newton first** (H100 preferred), student **RTX 5090 / 3080 Ti** backup, cloud only as contingency (~$50 soft cap)
- Plan (~3 weeks, guidance): Tier 0 smoke → **depth 8 @ ~0.5B** Wikipedia → **C-short** → write-up; optional C-full or depth 12 only if ahead
- Compute/time model: [compute-budget.md](./compute-budget.md)

## Success criteria (draft)

- Reproducible training + eval pipeline from this repo
- Clear baseline vs Wikipedia-adapted comparison (loss/perplexity + qualitative samples)
- Documented limitations (especially: perplexity ≠ hallucination; compute/data caps)

## Non-goals (draft — confirm)

- Not building a production chatbot or retrieval-augmented system
- Not claiming SOTA factuality without dedicated hallucination / fact-checking benchmarks in v1
- Not running full NanoChat d26 8×H100 speedrun unless compute appears later
- Keep the model small and runnable for the team

## Proposed deliverables

1. Problem statement and approach write-up (this overview → design spec)
2. Data preprocessing + train/eval scripts based on NanoChat
3. Experiment results (tables + sample generations)
4. Final report and presentation materials per course requirements

## References

1. [karpathy/nanochat](https://github.com/karpathy/nanochat)
2. [wikimedia/wikipedia on Hugging Face](https://huggingface.co/datasets/wikimedia/wikipedia)
3. [Attention Is All You Need](https://arxiv.org/pdf/1706.03762)
4. [Textbooks Are All You Need](https://arxiv.org/pdf/2306.11644)
5. [DataComp-LM](https://arxiv.org/pdf/2406.11794)

## Next step

Resolve remaining items in [open-questions.md](./open-questions.md), especially compute access, exact baseline definition, and whether to add a dedicated factuality/hallucination check beyond perplexity.
