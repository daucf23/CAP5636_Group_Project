# NanoWiki Design Spec

**Date:** 2026-07-10  
**Status:** Draft for team review (planning guidance → implementation)  
**Course:** CAP 5636  
**Team:** Sahil Bhikha, Thomas Belyakov, David Almeida II  
**Related:** [project-overview.md](../../planning/project-overview.md), [compute-budget.md](../../planning/compute-budget.md)

## 1. Goal

Build a **reproducible thin wrapper** around NanoChat that:

1. Prepares an English Wikipedia corpus with an **article-ID** validation holdout and a matched general-text corpus.
2. Trains two **depth-8** decoder-only models for the **same token budget** (target **0.5B each**, reducible equally after a measured smoke run).
3. Compares **W-Wiki** (Wikipedia-only) against **G-General** (general text) with architecture, tokenizer, initialization, optimization, and compute held constant.
4. Reports both models on held-out **Wikipedia and general-text bits-per-byte (bpb)**, checkpoint learning curves, and blinded fixed-prompt qualitative samples.

**Research question:** At fixed model size and training-token budget, how does Wikipedia-only pretraining change in-domain fit, out-of-domain fit, and encyclopedic generation style relative to general-text pretraining?

This is a controlled domain-specialization study. It does **not** claim that perplexity or Wikipedia-like prose equals factuality.

## 2. Non-goals (v1)

- No production chatbot, RAG system, or web UI requirement.
- No dedicated hallucination / closed-book QA / external-judge benchmark in v1.
- No full NanoChat d26 8×H100 speedrun.
- No requirement to train on the entire 11.6 GB dump.
- No claim that the experiment demonstrates reduced hallucination without a dedicated factuality benchmark.
- No intentionally undertrained model as the primary baseline.

## 3. Architecture / repository layout

**Choice:** thin wrapper around NanoChat (not a full fork, not a from-scratch trainer).

```
CAP5636_Group_Project/
  third_party/nanochat/     # git submodule or pinned clone of karpathy/nanochat
  nanowiki/
    data/                   # download, clean, article-ID split, export shards
    configs/                # smoke, W-Wiki, G-General
    eval/                   # cross-domain metrics + generation helpers
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

NanoChat must be pinned to an exact commit. Because its current pretraining loader assumes a fixed data directory and treats the last Parquet shard as validation, the wrapper must expose a dataset-root override (small maintained patch or adapter) and export each corpus with an explicit final validation shard.

## 4. Data pipeline

**Source:** Hugging Face `wikimedia/wikipedia`, split `20231101.en` (~11.6 GB text; CC BY-SA 3.0 / GFDL). Record license attribution in README.

**Steps (in order)**

1. **Download/stream** the English split; stop after enough source text is collected for the frozen token budget plus packing/cropping overhead.
2. **Clean lightly:** drop empty or near-empty articles; keep stable fields: article id, title, text.
3. **Split by article ID:** assign each article wholly to train or val. Default val size: **~2% of articles** in the working subset (or a fixed N if 2% is awkward); freeze the ID list to disk so runs are comparable.
4. **Subset train** to the frozen W-Wiki budget (target **0.5B consumed tokens**). Collect enough source tokens to account for NanoChat document-packing crop loss and avoid unintended corpus repetition.
5. **Prepare G-General:** use a pinned subset of NanoChat’s general pretraining corpus with the **same consumed-token budget** as W-Wiki. Freeze its source and validation manifests.
6. **Export** each corpus to NanoChat-compatible Parquet shards. The final shard for each dataset root is validation-only.
7. **Tokenizer:** use one pinned NanoChat tokenizer artifact for both corpora and both evaluations. Record its provenance and checksum.
8. **Smoke data:** a few MB / ~1–10M tokens from each domain for Tier 0 integration tests.

**Explicit rule:** validation articles never appear in training shards.

## 5. Training and experiment matrix

| Run ID | Depth | Init | Train tokens | Data | Required? |
| --- | --- | --- | --- | --- | --- |
| **A** smoke | 4–6 | scratch | ~1–10M | tiny Wiki shard | **Yes** (first) |
| **W-Wiki** | **8** | scratch (preferred) | **0.25–0.5B, frozen** | Wiki train subset | **Yes** |
| **G-General** | **8** | same as W-Wiki | **exactly matched** | pinned general text | **Yes** |
| **W/G checkpoints** | 8 | inherited | ~10%, 30%, 60%, 100% | respective corpus | **Yes** (no extra training) |
| **W/G-FT fallback** | 8 | same small base checkpoint | exactly matched | Wiki vs general | Only if scratch pipeline cannot produce usable models |
| **Factuality subset** | 8 | inherited | eval only | external fixed prompts | Optional after core results |

**Fair comparison rules**

- **Primary comparison:** same depth, tokenizer artifact, seed/init recipe, optimizer, sequence length, batch-token schedule, decoding settings, and consumed-token budget. Training corpus is the intended independent variable.
- **Cross-domain evaluation:** evaluate both models on the same frozen Wikipedia holdout and the same frozen general-text holdout.
- **If continued pretraining is used:** both runs start from the exact same checkpoint and receive equal additional tokens.
- If the measured 5090 throughput requires a smaller budget, reduce **both** runs equally; never preserve W-Wiki by weakening G-General.

**Guaranteed hardware plan:** student RTX 5090. Newton or cloud may accelerate reruns but is not on the critical path. RTX 3080 Ti is for smoke/dev only.

**Logging:** each run writes a run card under `results/` with: run id, depth, init, token budget, data source, hardware, wall time, val metric(s), checkpoint path.

## 6. Evaluation (capture clearly)

### 6.1 Quantitative (required)

| Item | Spec |
| --- | --- |
| Metric | **Primary:** NanoChat validation **bits-per-byte (bpb)** on the holdout (native to NanoChat logging). **Secondary (optional):** convert or also report loss/perplexity if easy — but the comparison table must always include bpb |
| Eval data | Frozen Wikipedia article-ID holdout **and** frozen general-text holdout |
| Comparison | 2×2 cross-domain comparison: W-Wiki and G-General on both holdouts, including saved-checkpoint learning curves |
| Artifacts | `results/<run_id>/metrics.json` (or CSV) + summary table in README/report |

**Expected domain-specialization signal:** W-Wiki achieves lower Wikipedia bpb while G-General retains lower general-text bpb. A null or reversed result is still reportable if the comparison is controlled.

### 6.2 Qualitative (required)

| Item | Spec |
| --- | --- |
| Prompts | Fixed sheet in `nanowiki/prompts/` (encyclopedic starters; same for every model) |
| Decoding | Identical settings for all compared models (temperature, max tokens, etc. — freeze in config) |
| Outputs | Save raw, model-anonymized generations under `results/<run_id>/samples.md` |
| Rubric | At least two team members independently score coherence, repetition, neutral tone, and Wikipedia-like structure before model identities are revealed; report counts/means and disagreements |

**Qualitative analysis:** compare models under identical decoding and report both successes and failure cases. Do not require the expected model to “win.”

### 6.3 What we will state in the write-up

- The submitted motivation mentions factual consistency / hallucination, but the implemented study tests **domain specialization**, not hallucination reduction.
- bpb and style scores are **not** factuality measures.
- Compute and data were capped (depth 8, equal 0.25–0.5B-token budgets).
- Negative and null results are valid outcomes under the controlled design.

### 6.4 Deferred (not v1 unless spare time)

- Full closed-book QA or fact-check benchmark
- External LLM judge
- Depth-12 scale-up
- Additional architectures or tokenizers

## 7. Error handling and operational notes

- **OOM:** lower NanoChat `--device-batch-size` (32 → 16 → 8 → 4 → 1); keep total token budget via grad accumulation when available.
- **5090 throughput below plan:** use full-context attention if the SDPA sliding-window path is inefficient, then reduce both matched token budgets equally if necessary.
- **Scratch quality failure:** retain scratch results as valid pretraining evidence; switch to matched W/G continued-pretraining runs only if time permits and clearly label the changed research design.
- **Data download failure:** document mirror/cache location; keep a tiny committed smoke fixture if license allows, or script-only download with checksums.

## 8. Testing / verification before claiming a run succeeded

1. Smoke (A): train briefly, log a val metric, generate one sample — must complete without crash.
2. Data: assert no article ID overlap between train and val manifests.
3. Eval: running the eval entrypoint twice on the same checkpoint yields the same primary metric (determinism within floating tolerance).
4. Comparison: W-Wiki and G-General metrics land in one cross-domain results table with matching eval-set IDs and token budgets.

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

- Exact matched token budget inside 0.25–0.5B, frozen from the measured 5090 smoke throughput
- Exact Wikipedia and general validation sizes
- Pinned NanoChat commit and general-corpus shard manifest
- Confirm people → lanes A/B/C in [team-work-split.md](../../planning/team-work-split.md)
