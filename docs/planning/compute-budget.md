# Compute Budget Model (v1)

**Purpose of this doc:** planning guidance — how we intend to run the project, and rough models of **compute, wall time, and cost**. Numbers are forecasts to refine after Tier 0 measures `train/tok_per_sec`; not hard contracts.

Goal: stay **simple and realistic**. Prefer a small NanoChat depth, a Wikipedia **subset**, and a cheap control — not a full GPT-2-scale speedrun unless Newton multi-GPU access is easy.

## Decisions locked for now

| Decision | Choice |
| --- | --- |
| Eval complexity | **Simple:** held-out Wikipedia val loss / perplexity (or bits-per-byte) + fixed qualitative prompts |
| Factuality / hallucination benches | **Deferred** (not in v1) |
| Primary dial | NanoChat `--depth` (auto-scales width, tokens, LR, etc.) |
| Hardware posture | **Newton first**, student **5090 / 3080 Ti** as backup, **cloud only if blocked** |
| First main depth | **Start at depth 8 (~0.5B tokens)**; attempt **depth 12 (~1B)** only after B+C succeed |
| v1 baseline | **C-short** (~5–25M tokens; not a full second general-text pretrain) |
| Working window | **~3 weeks** guidance to v1 results + draft write-up |

## Available hardware (team)

| Resource | Specs (known / published) | Role for NanoWiki |
| --- | --- | --- |
| **UCF Newton (ARCC)** | ~42× V100 (16/32GB) + ~90× H100 80GB across dual- and 8-GPU nodes; Slurm; campus storage | **Primary** for Tier 1 (+ optional stretch). Prefer **1× H100** jobs; use `highgpu` only if we need 8-GPU nodes and have access. |
| **Student RTX 5090** | ~32 GB VRAM (consumer) | Strong **backup / local iteration**; good for Tier 0–1 if Newton queue is slow |
| **Student RTX 3080 Ti** | Typically **12 GB** VRAM | **Dev / smoke / small depth** only; expect heavy `--device-batch-size` cuts |
| **Cloud (optional)** | On-demand / spot A100–H100 | Contingency if Newton access lags or we need a clean timed run |

Newton references: [RCI Newton page](https://rci.research.ucf.edu/resource/newton/), [ARCC About Newton](https://arcc.ist.ucf.edu/index.php/resources/newton/about-newton).

## Rough data math (Wikipedia)

| Quantity | Estimate | Notes |
| --- | --- | --- |
| `20231101.en` raw text | ~11.6 GB | From project brief |
| Characters | ~1.1e10 | Order-of-magnitude |
| Tokens (BPE ~3–4 chars/token) | **~2.5–4B tokens** | Refine after tokenizer eval |
| Tokens for NanoChat d12 @ ~10.5:1 | **~1B tokens** | **Subset** of English Wikipedia |
| Tokens for d20 @ ~10.5:1 | **~3B tokens** | Most / nearly all of the dump |

**Implication:** Full dump is optional. Subsetting is the main compute lever.

## NanoChat reference points

| Depth | ~Params | ~Compute-optimal tokens | Notes |
| --- | --- | --- | --- |
| 4–6 | tens of M | override with `--num-iterations` | Smoke tests |
| 8 | ~tens–low 100M | hundreds of M tokens | Good under-budget Tier 1 |
| 12 | ~100M | ~1B | Recommended main experiment |
| 20 | ~300M | ~3B | Stretch |
| 26 | GPT-2-ish | large | NanoChat speedrun (~2.5–3h on **8×H100**) — **not required** for v1 |

Training FLOPs (order of magnitude): \(\text{FLOPs} \approx C \times N \times D\) with \(C \approx 6\)–\(20\).

Example: d12, \(N \approx 1\times10^8\), \(D \approx 1\times10^9\), \(C=6\) → **~6×10¹⁷ FLOPs**.

## Throughput assumptions (for forecasting)

These are **planning estimates**, not measured NanoChat numbers on our boxes. Replace with logged `train/tok_per_sec` after Tier 0.

| GPU | Assumed train tok/s for ~d8–d12 (bf16, tuned batch) | Confidence |
| --- | --- | --- |
| RTX 3080 Ti 12GB | **15k–40k** (VRAM-limited; small device batch) | Low–med |
| RTX 5090 32GB | **80k–160k** (consumer flagship; 4090-class runs often ~100k+) | Med |
| Newton V100 16/32GB | **20k–50k** per GPU | Med |
| Newton H100 80GB | **100k–250k** per GPU (FP8 can help if NanoChat path works) | Med |
| 2× H100 (same node) | ~1.6–1.9× single if DDP scales well | Med |

Wall time ≈ `tokens / tok_per_s` (plus eval/checkpoint overhead ~10–20%).

## Forecast: recommended experiment matrix

### Run A — Tier 0 smoke (required)

| Item | Value |
| --- | --- |
| Depth | 4–6 |
| Tokens | ~1–10M (or fixed tiny `--num-iterations`) |
| Data | Tiny Wikipedia shard |
| Where | 3080 Ti **or** 5090 **or** Newton interactive/debug |
| Wall time | **minutes–1 hour** |
| Cloud $ | **$0** |

### Run B — Main Wikipedia model (Tier 1, start here)

| Item | Value |
| --- | --- |
| Depth | **8** first |
| Tokens | **~0.5B** (explicit cap; subset Wikipedia) |
| Data | Wikipedia subset sized to token budget; held-out articles for val |
| Where | **Newton 1× H100** preferred; else **5090**; 3080 Ti only if heavily capped |
| Wall time (~0.5B) | H100: **~0.5–2 hours**; 5090: **~1–2 hours**; V100: **~3–8 hours** |
| Cloud $ if rented | **~$2–10** for a single A100/H100-class run |

### Run B2 — Scale-up (only after B + C succeed)

| Item | Value |
| --- | --- |
| Depth | **12** |
| Tokens | **~0.5–1.0B** (prefer 1B if time/queue allow) |
| Where | Same as Run B |
| Wall time (1B) | H100: **~1–3 hours**; 5090: **~2–4 hours** |

### Run C — C-short control (v1 default)

For the **3-week / cheaper** path, do **not** train a full second general-text model. Default control is **C-short**: same architecture, tokenizer, and Wikipedia eval set as Run B; train only briefly.

| Item | Value |
| --- | --- |
| Budget | **~5–25M tokens** (~1–5% of Run B’s ~0.5B), exact number frozen when we set Run B steps |
| Data for the short train | Prefer a **small generic shard** (NanoChat default / FineWeb-style) if easy; else a tiny Wikipedia shard — document which |
| Extra cost | **≪ 1× Run B** (typically minutes to ~30 min on H100/5090) |
| Trade-off | Weaker causal claim than a matched 0.5B general-text pretrain; still contrasts a Wikipedia-trained model with an undertrained twin |
| Deferred | **C-full** (same 0.5B tokens, non-Wiki data); **C0** init-only only as an emergency fallback |

### Run C-full — Deferred matched general-text baseline

Same depth/tokens/tokenizer/eval as Run B, but trained on NanoChat default / FineWeb-style general text. Schedule only if d8 Wikipedia run finishes early.

### Run D — Optional ablation (only if A–C succeed)

| Ablation | Extra compute |
| --- | --- |
| Token budgets 100M / 300M / 0.5B at depth 8 | Can often come from checkpoints of Run B |
| Depth 12 scale-up | Covered by Run B2 + C12 |

## Resource plan (priority order)

1. **Get Newton access early** (ARCC registration, advisor/faculty sponsorship if required, Slurm tutorial, storage quota).
2. **Tier 0 on 3080 Ti or 5090** while Newton account/queue is sorted — prove the pipeline.
3. **Submit Run B on Newton H100** (1 GPU). Run **C-short** on the same job or a short follow-up. Prefer dual-H100 nodes over waiting for `highgpu` 8-GPU nodes.
4. **Use 5090** if Newton queue wait > ~1–2 days or software modules block us.
5. **Rent cloud** only if both Newton and student GPUs cannot finish B+C before a course checkpoint — budget a **soft cap of ~$50** for contingency (enough for several single-GPU runs, not an 8×H100 speedrun).

## Project-level forecast (v1 success path)

| Scenario | Hardware | Runs | Est. GPU-hours | Est. $ |
| --- | --- | --- | --- | --- |
| **v1 minimum (3-week guidance)** | Newton H100 or 5090 | A + B(d8@0.5B) + C-short | **~2–6 GPU-h** | **$0** (or ~$5–15 cloud) |
| **v1 + full general baseline** | same | above + C-full @ 0.5B | **~4–10 GPU-h** | **$0** (or ~$10–25 cloud) |
| **v1 + d12 scale-up** | same | above + B2 + control | **~8–20 GPU-h** | **$0** (or ~$15–40 cloud) |
| **3080 Ti only** | 3080 Ti | A + smaller d8 (e.g. 100–200M tokens) | longer wall time | **$0** |
| **Avoid for v1** | 8×H100 NanoChat speedrun | full d26 | ~20–25 GPU-h on 8 GPUs | **~$50–70** on-demand |

**Bottom line:** For **~3 weeks**, plan on **one** serious train (**d8 @ ~0.5B Wikipedia**) plus **C-short**. Defer C-full and d12 until that lands. Cloud remains a **~$50 soft contingency**.


## Comparison rule (v1 vs stretch)

**v1 (cheap control):** match architecture, tokenizer, and held-out Wikipedia eval set. Do **not** require equal training tokens.

**Stretch (C-full / d12):** also match training tokens (or FLOPs) and document the data source.
## 3-week sketch (guidance)

| Week | Focus |
| --- | --- |
| **1** | Newton/local setup; data download + preprocess; Tier 0 smoke; freeze prompt sheet |
| **2** | Run B (d8 @ ~0.5B); Run C-short; val loss + samples |
| **3** | Tables/plots; write-up; optional C-full or d12 only if ahead of schedule |

## Still useful to confirm

- Newton account status / faculty sponsor / queue access (`highgpu` needed or not)
- Soft cloud cap (proposed **$50**)
- Exact course due date relative to this 3-week window
- Whether C-short’s brief train uses a tiny generic shard or a tiny Wikipedia shard