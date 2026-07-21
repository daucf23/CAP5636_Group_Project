# Fact-Constrained Story Generation

**CAP 5636 Group Project** — TinyStories-scale LM + factual narrative adaptation

**Team:** Sahil Bhikha · Thomas Belyakov · David Almeida II

## One-line summary

**Pretrain** a small decoder-only Transformer on **TinyStories**, then **adapt** it so it can write short **stories that stay faithful to a provided fact card**, and measure the **faithfulness–narrative quality tradeoff** against matched controls.

## Research question

Under a fixed small-model and token budget, which adaptation strategy best improves **fact faithfulness** of short educational stories **without destroying narrative quality**, relative to TinyStories-only and pure encyclopedic continued pretraining?

## Contribution (paper framing)

We study **fact-constrained story generation** with a TinyStories-scale decoder-only LM. We build a small evaluation suite of topic–fact-card–prompt triples and compare matched-budget adaptation recipes (story-only baseline, Wiki continued pretraining, and task-specific SFT / factual-narrative adaptation). We characterize the **faithfulness vs story-quality** tradeoff and analyze failure modes (contradiction, omission, unconstrained invention, encyclopedia dump).

This is a **controlled empirical study**. We do **not** claim general truthfulness, educational safety, or open-world hallucination reduction.

## Task definition

Each eval/train item is closed-world and scoreable:

| Field | Role |
| --- | --- |
| **Topic** | e.g. water cycle, seasons, a simple historical figure |
| **Fact card** | 4–7 gold bullets the story may teach; optional notes on common false claims |
| **Prompt** | “Write a short story (≈120–180 words) that teaches this topic. Invent characters and plot freely; do **not** invent facts beyond the card.” |
| **Output** | One short story |

**Success axes**

1. **Faithfulness** — required-fact coverage; low contradiction / invention relative to the card  
2. **Story quality** — narrative structure, coherence, age-appropriate voice (not a bullet list or textbook dump)

**Data scale (target)**

- Train fact cards / SFT pairs: on the order of **80–200** topics  
- Held-out eval: **40–60** frozen topic IDs (never used for prompt tuning or SFT labels)

## Training stages

| Stage | Term | What happens | Starts from |
| --- | --- | --- | --- |
| **1** | **Pretraining** | Next-token LM training on TinyStories | Random init (from scratch) |
| **2** | **Adaptation** | Matched-budget continued pretraining and/or SFT for the fact-constrained story task | Stage-1 checkpoint |

Stage 2 may include classic **SFT** (fact card + prompt → story), not only continued pretraining. We use precise terms in the paper for each arm.

**Locked decision:** Stage 1 = pretrain from scratch on TinyStories (lab-scale GPT). We are not starting from a public pretrained model (e.g. SmolLM2) unless Stage 1 fails after smoke.

## Why this project

TinyStories yields fluent simple narrative but freely invents world knowledge. Pure encyclopedic continued pretraining may improve “fact-ish” language while **eroding story form**. Task-specific adaptation may improve checklist faithfulness with a different quality cost. Under a single-GPU budget we measure that tradeoff with fixed protocols—not vibes and not Wiki perplexity alone.

## Relation to the Week 6 LLM lab

Lab notebook: [`CAP5636_W6_Transformer(LLM).ipynb`](./CAP5636_W6_Transformer(LLM).ipynb)

| Lab module | What it teaches | Project use |
| --- | --- | --- |
| 1 | Decoder-only GPT | Small Transformer architecture |
| 2 | BPE on TinyStories | Tokenizer / data prep |
| 3 | Next-token pretraining on TinyStories | **Stage 1** |
| 4 | Temperature / top-k / top-p | Eval decoding (fixed across systems) |
| 5 | Adaptation after pretraining | **Stage 2** (CPT and/or SFT) |
| SmolLM2-135M demo | ~100M-class reference | Size-class reference only |

Lab reference scale (approximate): `n_layer=6`, `n_embd=256`, `n_head=8`, `vocab_size=8000`, `block_size=256`, dataset `roneneldan/TinyStories`.

## Experiment plan (deadline-safe)

**Hardware:** student RTX 5090 preferred; Newton optional.

Keep Stage-2 budgets **equal** across compared runs. Save intermediate checkpoints for a cheap duration/data ablation when possible.

### Core systems (minimum excellent set)

| ID | System | Role |
| --- | --- | --- |
| **B0** | TinyStories-only (Stage 1) | Narrative prior; faithfulness floor |
| **B1** | B0 + Wikipedia continued pretraining | Encyclopedic / “more world text” control |
| **M2** | B0 + SFT on (fact card + prompt → story) | Primary task adaptation |

**If time allows**

| ID | System | Role |
| --- | --- | --- |
| **M1** | B0 + CPT on factual narratives or TS + factual mixture | Domain-style adapt without explicit SFT |
| **M3** | B1 then light SFT | Does Wiki help or hurt as a middle step? |
| **Prompt ablation** | B0 / M2 with vs without fact card in context | In-weights skill vs prompt-following |

**Deadline triage:** if only three full runs fit, ship **B0, B1, M2**.

### Evaluation protocol

Primary metrics (fixed before final runs):

| Axis | Measure |
| --- | --- |
| **Faithfulness** | Per-bullet coverage; contradiction rate; optional invention rate vs card |
| **Story quality** | Rubric (structure, coherence, simplicity); or binary “is a story?” + fluency |
| **Supporting automatic** | Length, repetition; held-out TinyStories loss (prior retention); optional domain loss |

**Scoring:** blind human rubric as primary claim (team raters, short calibration set); report agreement on a double-scored subset. LLM-as-judge only secondary + audited, if used at all—disclose in AI Tools.

**Main paper figure:** faithfulness vs story quality for B0 / B1 / M2 (Pareto-style comparison).

**Error analysis:** categorize failures on a fixed sample—omission, contradiction, unconstrained invention, story collapse (encyclopedia dump), story domination (plot with no teaching content).

### Planned layout

```text
data/
  fact_cards/train.jsonl
  fact_cards/eval.jsonl          # frozen IDs
  sft_pairs/train.jsonl          # if used
  prompts/eval_prompts.jsonl
eval/
  rubric.md
  score_sheet_template.csv
results/<run_id>/
  config.yaml
  metrics.json
  samples/
```

## What we are not claiming

- Open-world truthfulness or “no hallucinations” in general  
- Perplexity alone as proof of factual stories  
- Reproducing large-LM token counts or multi-GPU training as requirements  
- RAG, chat UI, agents, or RL alignment as core deliverables  
- Real educational product readiness or -safety guarantees  

## Team work split

Three equal lanes. Fill in names; one owner per lane end-to-end.

| Lane | Owner | Owns | Does not own |
| --- | --- | --- | --- |
| **A — Data** | `_assign_` | TinyStories packaging; fact cards (train/eval split); SFT pair construction/verification; manifests; license notes | Training hyperparameters; final paper prose alone |
| **B — Train** | `_assign_` | Model/config (lab GPT); Stage 1 + Stage 2 scripts; smoke + full runs; checkpoints; run cards (hardware, tokens, wall time) | Rubric finalization; slides-only work |
| **C — Eval / paper** | `_assign_` | Rubric + scoring protocol; blind scoring sheets; figures/tables (faithfulness vs story); paper + slides; repro instructions in README | Shard format internals; GPU job babysitting (unless helping B) |

**Shared by all three:** design decisions, interpreting results, paper review, AI Tools disclosure, presentation speaking roles, individual contributions section.

### Suggested calendar

| When | Lane A | Lane B | Lane C |
| --- | --- | --- | --- |
| **Now → +2 days** | Draft ≥10 fact cards + schema; TinyStories smoke data | Port/pin training code; Stage-1 smoke green | Freeze rubric draft; paper skeleton; metrics schema |
| **Next 3–4 days** | Full train/eval cards; SFT pairs verified against cards | Stage 1 complete; Stage 2 for B1 + M2 (matched budget) | Eval harness; draft Methods / Related Work / task definition |
| **Final 3–4 days** | Data appendix + rebuild commands | Package configs + run cards | Blind scores; results freeze; paper; slides; README “how to reproduce” |

### Handoffs

1. **A → B:** frozen data paths, eval IDs, token estimates, rebuild commands  
2. **B → C:** checkpoint paths + run cards under `results/<run_id>/`  
3. **C → team:** faithfulness–story table, sample generations, paper/slides draft for review  

### Decision gates

- No Stage-1 smoke in ~2 days → shrink model/steps; do not add optional arms  
- Stage 1 OK but Stage 2 too slow → cut Stage-2 tokens **equally** for all adaptation runs  
- Only one adaptation run finishes → prioritize **M2** over extras; still report **B0** and partial **B1** if possible  
- No comparable Stage-2 pair in time → freeze what exists; write an honest pilot with limitations  

## Deliverables (course)

- Reproducible train + eval code  
- Results, samples, and main faithfulness-vs-story figure  
- 6–8 page NeurIPS-style paper (required sections + individual contributions + AI Tools), repo link  
- ~10–12 slides, 15 min presentation (all team members speak)  

**Soft deadline:** 2026-07-25 · **Hard deadline:** 2026-07-27

## Status

- [x] Proposal submitted (topic may be updated to this framing)  
- [x] Lab connection documented  
- [x] Project locked: **fact-constrained stories** (TinyStories prior → matched adaptation + dual-axis eval)  
- [ ] Assign lane owners (A / B / C)  
- [ ] Fact-card schema + seed cards + rubric  
- [ ] Stage-1 smoke  
- [ ] Matched Stage-2 runs (B0 / B1 / M2) + eval  
- [ ] Paper / slides / repro README  

## References

1. CAP 5636 Week 6 LLM lab notebook (this repo)  
2. [roneneldan/TinyStories](https://huggingface.co/datasets/roneneldan/TinyStories)  
3. [karpathy/nanochat](https://github.com/karpathy/nanochat)  
4. Vaswani et al., *Attention Is All You Need*  
5. Gunasekar et al., *Textbooks Are All You Need*  
6. Literature on continued pretraining, instruction tuning, and factuality evaluation (to be expanded in the paper)
