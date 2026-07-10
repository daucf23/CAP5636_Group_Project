# NanoWiki Design Spec

**Date:** 2026-07-10  
**Status:** Draft for team review (planning guidance → implementation)  
**Course:** CAP 5636  
**Team:** Sahil Bhikha, Thomas Belyakov, David Almeida II  
**Related:** [project-overview.md](../../planning/project-overview.md), [compute-budget.md](../../planning/compute-budget.md)

## 1. Goal

Build a **reproducible thin wrapper** around NanoChat that:

1. Prepares a curated English Wikipedia subset with an **article-ID** validation holdout.
2. Trains a **depth-8** decoder-only model for about **0.5B tokens** (prefer from scratch).
3. Compares it to a **C-short** control (~5–25M tokens, same architecture/tokenizer/init recipe).
4. Reports held-out Wikipedia validation **bits-per-byte (bpb)** plus **fixed-prompt qualitative samples**.

This is guidance for execution and compute/time modeling, not a claim that perplexity equals factuality.

## 2. Non-goals (v1)

- No production chatbot, RAG system, or web UI requirement.
- No dedicated hallucination / closed-book QA / external-judge benchmark in v1.
- No full NanoChat d26 8×H100 speedrun.
- No requirement to train on the entire 11.6 GB dump.
- No full matched-token general-text pretrain in v1 (deferred as optional stretch).

## 3. Architecture / repository layout

**Choice:** thin wrapper around NanoChat (not a full fork, not a from-scratch trainer).

```
CAP5636_Group_Project/
  third_party/nanochat/     # git submodule or pinned clone of karpathy/nanochat
  nanowiki/
    data/                   # download, clean, article-ID split, export shards
    configs/                # smoke, d8 Wikipedia (Run B), C-short
    eval/                   # val metrics + generation helpers
    prompts/                # fixed encyclopedic prompt sheet
  scripts/                  # thin CLIs: prepare data, launch train, run eval
  docs/planning/            # planning guidance (existing)
  docs/superpowers/specs/   # this design
  docs/superpowers/plans/   # implementation plan (next)
  results/                  # run tables, metrics JSON/CSV, sample generations
  README.md                 # setup, train, eval for graders/teammates
```

**Ownership**

| Component | Owner |
| --- | --- |
| Model, tokenizer, optimizer, `base_train` | NanoChat (`third_party/nanochat`) |
| Wikipedia download/clean/split/export | `nanowiki/data` |
| Experiment hyperparameters / run recipes | `nanowiki/configs` |
| Val metrics + prompt generations | `nanowiki/eval` + `nanowiki/prompts` |
| How to reproduce | root `README.md` + `results/` |

Training is launched by calling NanoChat’s training entrypoint with our data paths and config flags (depth, iterations/token budget, batch size, etc.).

## 4. Data pipeline

**Source:** Hugging Face `wikimedia/wikipedia`, split `20231101.en` (~11.6 GB text; CC BY-SA 3.0 / GFDL). Record license attribution in README.

**Steps (in order)**

1. **Download** the English split (stream or cache locally / on Newton storage).
2. **Clean lightly:** drop empty or near-empty articles; keep stable fields: article id, title, text.
3. **Split by article ID:** assign each article wholly to train or val. Default val size: **~2% of articles** in the working subset (or a fixed N if 2% is awkward); freeze the ID list to disk so runs are comparable.
4. **Subset train** to about **0.5B tokens** for Run B (do not require the full dump).
5. **Export** train/val into the file/shard format NanoChat’s dataloader expects.
6. **Tokenizer:** reuse NanoChat’s tokenizer **as-is**. Only revisit if compression on Wikipedia is clearly pathological.
7. **C-short data:** prefer a **tiny generic text shard** (NanoChat default / FineWeb-style) if easy to obtain; otherwise a tiny slice of the Wikipedia train pool. **Document which** in the run card.
8. **Smoke data:** a few MB / ~1–10M tokens for Tier 0.

**Explicit rule:** validation articles never appear in training shards.

## 5. Training and experiment matrix

| Run ID | Depth | Init | Train tokens | Data | Required? |
| --- | --- | --- | --- | --- | --- |
| **A** smoke | 4–6 | scratch | ~1–10M | tiny Wiki shard | **Yes** (first) |
| **B** main | **8** | scratch (preferred) | **~0.5B** | Wiki train subset | **Yes** |
| **C-short** | **8** | same recipe as B | **~5–25M** | tiny generic or tiny Wiki | **Yes** |
| **B-FT** fallback | 8 | continue from small NanoChat ckpt | ~0.5B | same Wiki subset as B | Only if B scratch samples unusable |
| **B2** stretch | 12 | same as B | ~0.5–1B | Wiki subset | Only if ahead of schedule |
| **C-full** stretch | 8 | same as B | ~0.5B | general text | Only if ahead of schedule |

**Fair comparison rules**

- **v1 (B vs C-short):** same depth, tokenizer, init recipe, decoding settings, and **same Wikipedia val article set**. Token budgets are **not** equal by design (C-short is intentionally cheap).
- **If B-FT is used:** C-short must start from the **same base checkpoint** and only train briefly, so the comparison stays “Wikipedia-adapted vs barely-adapted,” not “pretrained vs random.”
- **Stretch (C-full / B2):** also match token budget (or FLOPs) and document data source.

**Hardware order:** Newton 1× H100 → student RTX 5090 → cloud contingency (~$50 soft cap). RTX 3080 Ti is for smoke/dev only.

**Logging:** each run writes a run card under `results/` with: run id, depth, init, token budget, data source, hardware, wall time, val metric(s), checkpoint path.

## 6. Evaluation (capture clearly)

### 6.1 Quantitative (required)

| Item | Spec |
| --- | --- |
| Metric | **Primary:** NanoChat validation **bits-per-byte (bpb)** on the holdout (native to NanoChat logging). **Secondary (optional):** convert or also report loss/perplexity if easy — but the comparison table must always include bpb |
| Eval data | Article-ID holdout only (same list for B and C-short) |
| Comparison | Side-by-side table: Run B vs Run C-short (and B-FT if used) |
| Artifacts | `results/<run_id>/metrics.json` (or CSV) + summary table in README/report |

**Positive quantitative signal:** Run B achieves **lower** held-out Wikipedia **bpb** than C-short.

### 6.2 Qualitative (required)

| Item | Spec |
| --- | --- |
| Prompts | Fixed sheet in `nanowiki/prompts/` (encyclopedic starters; same for every model) |
| Decoding | Identical settings for all compared models (temperature, max tokens, etc. — freeze in config) |
| Outputs | Save raw generations under `results/<run_id>/samples.md` |
| Rubric | Manual checklist per sample: coherence, repetition, neutral tone, Wikipedia-like structure (short notes, not a formal human study) |

**Positive qualitative signal:** Run B samples are clearly more encyclopedic / less degenerate than C-short on the same prompts.

### 6.3 What we will state in the write-up

- Motivation mentions factual consistency / hallucination.
- v1 metrics are **proxies** (Wiki fit + style), **not** a dedicated factuality benchmark.
- Compute and data were capped (depth 8, ~0.5B tokens, subset of Wikipedia).

### 6.4 Deferred (not v1 unless spare time)

- Closed-book QA / fact-check set
- External LLM judge
- Full matched general-text baseline (C-full)
- Depth-12 scale-up (B2)

## 7. Error handling and operational notes

- **OOM:** lower NanoChat `--device-batch-size` (32 → 16 → 8 → 4 → 1); keep total token budget via grad accumulation when available.
- **Newton queue delay:** fall back to 5090 for smoke and, if needed, Run B.
- **Scratch quality failure:** switch to B-FT with documented base checkpoint; re-run C-short from the same base.
- **Data download failure:** document mirror/cache location; keep a tiny committed smoke fixture if license allows, or script-only download with checksums.

## 8. Testing / verification before claiming a run succeeded

1. Smoke (A): train briefly, log a val metric, generate one sample — must complete without crash.
2. Data: assert no article ID overlap between train and val manifests.
3. Eval: running the eval entrypoint twice on the same checkpoint yields the same primary metric (determinism within floating tolerance).
4. Comparison: B and C-short metrics land in the same results table with matching eval set id.

## 9. Deliverables from this design

| Deliverable | Location |
| --- | --- |
| Wrapper code + scripts | `nanowiki/`, `scripts/` |
| Pinned NanoChat | `third_party/nanochat/` |
| Run configs | `nanowiki/configs/` |
| Prompt sheet | `nanowiki/prompts/` |
| Results | `results/` |
| Repro instructions | `README.md` |
| Planning / compute model | `docs/planning/` |

## 10. Open items (do not block writing the implementation plan)

These can be filled during implementation without changing the design shape:

- Exact Newton account / queue details
- Exact C-short token count inside 5–25M (freeze when Run B step count is set)
- Exact val article count (~2% default)
- Which tiny corpus C-short uses (generic vs Wiki slice)
- Later course final-report / presentation requirements
- Confirm/swap lane owners in [team-work-split.md](../../planning/team-work-split.md) (proposed: Sahil=Data, Thomas=Train, David=Eval/docs)
