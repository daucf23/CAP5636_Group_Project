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
3. Compare against a baseline trained on general text and/or the untuned NanoChat / NanoGPT-style model.
4. Optionally ablate **data size** and/or **training duration** (steps/tokens) to study scaling within the Wikipedia-only setting.

## Data

| Item | Detail |
| --- | --- |
| Source | Hugging Face [`wikimedia/wikipedia`](https://huggingface.co/datasets/wikimedia/wikipedia) |
| Split | `20231101.en` |
| Size | ~11.6 GB English text (2023 dump-derived) |
| License | CC BY-SA 3.0 and GFDL (original Wikipedia content) |
| Prep | Preprocess for NanoChat pretraining; create a held-out validation set of unseen articles |

## Evaluation plan

**Quantitative**

- Validation loss and perplexity on held-out Wikipedia text
- Compare Wikipedia-adapted model vs baseline (not trained on the Wikipedia subset) and/or vs models trained for different step/token budgets

**Qualitative**

- Fixed encyclopedic prompts → compare completions for coherence, repetition, neutral tone, and Wikipedia-like structure
- Desired outcome: lower Wikipedia perplexity and more encyclopedic completions without excessive repetition or degeneration

## Success criteria (draft)

- Reproducible training + eval pipeline from this repo
- Clear baseline vs Wikipedia-adapted comparison (loss/perplexity + qualitative samples)
- Documented limitations (especially: perplexity ≠ hallucination; compute/data caps)

## Non-goals (draft — confirm)

- Not building a production chatbot or retrieval-augmented system
- Not claiming SOTA factuality without dedicated hallucination / fact-checking benchmarks (unless we add them later)
- Not training a large model; keep the model small and runnable for the team

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
