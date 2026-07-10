# Compute Budget Model (v1)

Goal: stay **simple and realistic**. Prefer a small NanoChat depth, a Wikipedia **subset**, and matched-budget comparisons — not a full GPT-2-scale speedrun unless Newton multi-GPU access is easy.

## Decisions locked for now

| Decision | Choice |
| --- | --- |
| Eval complexity | **Simple:** held-out Wikipedia val loss / perplexity (or bits-per-byte) + fixed qualitative prompts |
| Factuality / hallucination benches | **Deferred** (not in v1) |
| Primary dial | NanoChat `--depth` (auto-scales width, tokens, LR, etc.) |
| Hardware posture | **Newton first**, student **5090 / 3080 Ti** as backup, **cloud only if blocked** |

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

### Run B — Main Wikipedia model (Tier 1)

| Item | Value |
| --- | --- |
| Depth | **12** (fallback **8** if VRAM/queue painful) |
| Tokens | **~0.5–1.0B** (cap explicitly; do not chase full dump) |
| Data | Wikipedia subset sized to token budget; held-out articles for val |
| Where | **Newton 1× H100** preferred; else **5090** |
| Wall time (1B tokens) | H100: **~1–3 hours**; 5090: **~2–4 hours**; V100: **~6–14 hours**; 3080 Ti: **often impractical** at 1B |
| Cloud $ if rented | **~$3–15** for a single A100/H100-class run (rate-dependent) |

### Run C — Matched-budget baseline (required for fair compare)

Same depth, tokenizer, token budget, and eval set as Run B; different **data source** (general text) **or** shorter/random-init control if general data is hard.

| Item | Value |
| --- | --- |
| Extra cost | ≈ **1× Run B** |
| Where | Same machine class as Run B |

### Run D — Optional ablation (only if A–C succeed)

| Ablation | Extra compute |
| --- | --- |
| Token budgets 100M / 300M / 1B at fixed depth | ~0.1× + 0.3× + 1× of Run B (can reuse shorter prefixes of the long run if checkpointing allows) |
| Depth 8 vs 12 | another ~0.5–1× Run B |

## Resource plan (priority order)

1. **Get Newton access early** (ARCC registration, advisor/faculty sponsorship if required, Slurm tutorial, storage quota).
2. **Tier 0 on 3080 Ti or 5090** while Newton account/queue is sorted — prove the pipeline.
3. **Submit Run B + Run C on Newton H100** (1 GPU each, sequential or two jobs). Prefer dual-H100 nodes over waiting for `highgpu` 8-GPU nodes.
4. **Use 5090** if Newton queue wait > ~1–2 days or software modules block us.
5. **Rent cloud** only if both Newton and student GPUs cannot finish B+C before a course checkpoint — budget a **soft cap of ~$50** for contingency (enough for several single-GPU runs, not an 8×H100 speedrun).

## Project-level forecast (v1 success path)

| Scenario | Hardware | Runs | Est. GPU-hours | Est. $ |
| --- | --- | --- | --- | --- |
| **Best case** | Newton H100 | A + B + C | ~5–10 GPU-h | **$0** |
| **Likely case** | Newton + some 5090 | A local, B/C Newton or 5090 | ~8–20 GPU-h | **$0** |
| **Backup case** | 5090 only | A + B + C @ 0.5–1B tokens | ~10–25 GPU-h | **$0** (electricity) |
| **Contingency** | Cloud A100/H100 | B + C only | ~4–12 GPU-h | **~$10–40** |
| **Avoid for v1** | 8×H100 NanoChat speedrun | full d26 | ~20–25 GPU-h on 8 GPUs | **~$50–70** on-demand |

**Bottom line:** For the course project, plan on **two serious single-GPU runs (~0.5–1B tokens each)** plus a tiny smoke test. That is well within Newton H100 or a 5090. The 3080 Ti is for development, not the main 1B-token run. Cloud is a **forecasted contingency (~$10–50)**, not the default.

## Matched-budget rule

For Wikipedia vs baseline, match:

1. Model depth / architecture  
2. Training tokens (or FLOPs)  
3. Tokenizer  
4. Held-out Wikipedia eval set  

## Still needed from the team

- Confirm Newton account status / faculty sponsor / queue access (`highgpu` needed or not)
- Soft cloud cap confirmation (proposed **$50**)
- Exact baseline corpus for Run C
- Whether first main run is depth **8 @ 0.5B** (safer) or **12 @ 1B** (preferred if H100/5090)
