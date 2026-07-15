# NanoWiki

**CAP 5636 Group Project** — Small LM pretraining + Wikipedia adaptation

**Team:** Sahil Bhikha · Thomas Belyakov · David Almeida II

## One-line summary

**Pretrain** a small decoder-only Transformer from scratch on **TinyStories**, then **continue-train / domain-adapt** it on **Wikipedia**, and measure Wikipedia-domain fit and encyclopedic generation style against matched controls.

## Pretraining vs fine-tuning (decision)

We do **both**, as two stages with different names on purpose:

| Stage | Correct term | What happens | Starts from |
| --- | --- | --- | --- |
| **1** | **Pretraining** | Next-token LM training on TinyStories | Random init (from scratch) |
| **2** | **Domain adaptation** (continued pretraining) | Continue next-token LM training on Wikipedia | Stage-1 checkpoint |

Stage 2 is **not** classic chat SFT (instruction/response pairs). It is still next-token prediction, but on encyclopedic text. In casual speech people say “fine-tune on Wikipedia”; in the paper we prefer **domain adaptation / continued pretraining** so graders see we know the difference.

**Locked decision:** Stage 1 = pretrain from scratch on TinyStories; Stage 2 = adapt that checkpoint on Wikipedia. We are not starting from a public pretrained model (e.g. SmolLM2) unless Stage 1 fails after smoke.

## Why this project

Small models are easy to train but often weakly grounded. Wikipedia is structured and relatively neutral. Under a single-GPU budget, we ask whether TinyStories → Wikipedia adaptation improves Wikipedia fit and encyclopedic style versus TinyStories alone (and optionally versus continued training on general text).

This is a **controlled empirical study**. Lower Wikipedia perplexity is **not** treated as proof of fewer hallucinations.

## Relation to the Week 6 LLM lab

Lab notebook: [`CAP5636_W6_Transformer(LLM).ipynb`](./CAP5636_W6_Transformer(LLM).ipynb)

| Lab module | What it teaches | NanoWiki use |
| --- | --- | --- |
| 1 | Decoder-only GPT | Small Transformer architecture |
| 2 | BPE on TinyStories | Tokenizer / data prep |
| 3 | Next-token pretraining on TinyStories | **Stage 1** |
| 4 | Temperature / top-k / top-p | Qualitative eval decoding |
| 5 | Adaptation after pretraining | **Stage 2** (Wikipedia domain adaptation) |
| SmolLM2-135M demo | ~100M-class reference | Size-class reference only |

Lab reference scale (approximate): `n_layer=6`, `n_embd=256`, `n_head=8`, `vocab_size=8000`, `block_size=256`, dataset `roneneldan/TinyStories`.

## Experiment plan (deadline-safe)

**Hardware:** student RTX 5090 preferred; Newton optional.

| Stage | Data | Goal |
| --- | --- | --- |
| 1 — Pretrain | TinyStories | Fluent small LM |
| 2 — Adapt | Wikipedia `wikimedia/wikipedia` (`20231101.en` subset) | Encyclopedic specialization |
| Eval | Held-out Wiki articles + fixed encyclopedic prompts | Loss/perplexity + style |

**Required comparisons**

1. TinyStories-only (Stage 1 checkpoint)  
2. TinyStories → Wikipedia (primary)  
3. Optional: TinyStories → matched-token general text (isolates Wikipedia vs any continued training)

Keep Stage-2 budgets **equal** across compared runs (rough target **50–150M** tokens after smoke). Save a few intermediate checkpoints as a duration ablation.

## What we are not claiming (v1)

- Perplexity ⇒ reduced hallucination  
- Reproducing SmolLM2-scale token counts  
- Requiring Newton or multi-GPU  
- RAG / chat UI / RL alignment as core deliverables  

## Team work split

Three equal lanes. Fill in names; one owner per lane end-to-end.

| Lane | Owner | Owns | Does not own |
| --- | --- | --- | --- |
| **A — Data** | `_assign_` | TinyStories download/packaging; Wikipedia subset; article-ID val holdout; manifests/checksums; license notes | Training hyperparameters; final paper prose |
| **B — Train** | `_assign_` | Model/config (lab GPT and/or NanoChat); Stage 1 + Stage 2 launch scripts; smoke + full runs; checkpoints; run cards (hardware, tokens, wall time) | Cleaning policy details; slides-only work |
| **C — Eval / paper** | `_assign_` | Metrics (Wiki val loss/PPL); fixed prompt sheet; anonymized scoring; figures/tables; root README repro section; paper + slides integration | Shard format internals; GPU job babysitting (unless helping B) |

**Shared by all three:** design decisions, interpreting results, paper review, AI Tools disclosure, presentation speaking roles.

### Suggested week calendar

| When | Lane A | Lane B | Lane C |
| --- | --- | --- | --- |
| **Now → +2 days** | TinyStories + tiny Wiki smoke shards; freeze val article IDs | Port/pin training code; Stage-1 smoke green | Paper skeleton; prompt sheet; metrics schema |
| **Next 3–4 days** | Full Wiki subset + manifests | Stage 1 complete; Stage 2 Wiki (+ optional general) | Eval harness on checkpoints; draft Methods/Related Work |
| **Final 3–4 days** | Reproduction checks / data appendix | Package configs + run cards | Results freeze; paper; slides; README “how to reproduce” |

### Handoffs

1. **A → B:** frozen data paths, val IDs, token estimates, rebuild commands  
2. **B → C:** checkpoint paths + run cards under `results/<run_id>/`  
3. **C → team:** summary table, samples, paper/slides draft for review  

### Decision gates

- No Stage-1 smoke in ~2 days → shrink model/steps; do not add optional evals  
- Stage 1 OK but Stage 2 too slow → cut Stage-2 tokens equally for all adaptation runs  
- No comparable Stage-2 pair by ~Jul 20 → freeze what exists; write an honest pilot with limitations  

## Deliverables

- Reproducible train + eval code  
- Results + samples  
- 6–8 page NeurIPS-style paper, repo link, ~10–12 slides  
- Individual contributions + AI Tools section  

**Soft deadline:** 2026-07-25 · **Hard deadline:** 2026-07-27

## Status

- [x] Proposal submitted  
- [x] Lab connection documented  
- [x] Training story locked: **pretrain TinyStories → adapt Wikipedia**  
- [ ] Assign lane owners (A / B / C)  
- [ ] Stage-1 smoke  
- [ ] Stage-2 matched runs + eval  
- [ ] Paper / slides / repro README  

## References

1. CAP 5636 Week 6 LLM lab notebook (this repo)  
2. [karpathy/nanochat](https://github.com/karpathy/nanochat)  
3. [roneneldan/TinyStories](https://huggingface.co/datasets/roneneldan/TinyStories)  
4. [wikimedia/wikipedia](https://huggingface.co/datasets/wikimedia/wikipedia) (`20231101.en`)  
5. Vaswani et al., *Attention Is All You Need*  
6. Gunasekar et al., *Textbooks Are All You Need*  
7. Li et al., *DataComp-LM*
