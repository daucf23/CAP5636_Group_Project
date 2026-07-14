# Compute Budget Model (v1)

**Purpose of this doc:** planning guidance — how we intend to run the project, and rough models of **compute, wall time, and cost**. Numbers are forecasts to refine after Tier 0 measures `train/tok_per_sec`; not hard contracts.

Goal: stay **simple and realistic**. Prefer a small NanoChat depth, a Wikipedia **subset**, and a cheap control — not a full GPT-2-scale speedrun unless Newton multi-GPU access is easy.

## Decisions locked for now

| Decision | Choice |
| --- | --- |
| Eval complexity | **Simple:** held-out Wikipedia val loss / perplexity (or bits-per-byte) + fixed qualitative prompts |
| Factuality / hallucination benches | **Deferred** (not in v1) |
| Primary dial | NanoChat `--depth` (auto-scales width, tokens, LR, etc.) |
| Hardware posture | **RTX 5090 is the guaranteed path**; Newton/cloud may accelerate reruns but are not dependencies |
| Primary depth | **Depth 8** for both matched runs; depth 12 is out of scope before submission |
| v1 baseline | **Matched G-General run** at the same depth, initialization recipe, and consumed-token budget |
| Init strategy | **Prefer from-scratch** on Wikipedia; **continue-pretrain / light FT from a small NanoChat ckpt** is the realistic fallback |
| Tokenizer (v1) | **Reuse NanoChat tokenizer as-is**; revisit only if Wikipedia tok_eval looks pathological |
| Val split | **By article ID** (unseen articles); size ~1–5% of used subset or fixed N (freeze in data prep) |
| Working window | **July 13–25** to soft deadline; July 27 hard deadline |

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

## Forecast: required experiment matrix

### Run A — paired Tier 0 smoke

| Item | Value |
| --- | --- |
| Depth | 4–6 |
| Tokens | ~1–10M per domain |
| Data | Tiny Wikipedia and general-text shards, each with validation |
| Hardware | RTX 5090 (3080 Ti may be used for CPU/data-path checks) |
| Exit criteria | Both roots train, evaluate bpb, save, reload, and generate |
| Wall time | Minutes–1 hour after the environment works |

The smoke run must report measured `train/tok_per_sec`, peak VRAM, attention backend, device batch size, and compile time. Forecasts remain provisional until this measurement exists.

### Runs W-Wiki and G-General — matched primary experiment

| Item | W-Wiki | G-General |
| --- | --- | --- |
| Depth | 8 | 8 |
| Tokens | Target 0.5B; floor ~0.25B | Exactly equal to W-Wiki |
| Data | Wikipedia train subset | Pinned NanoChat general-text subset |
| Validation | Wiki + general holdouts | Same Wiki + general holdouts |
| Initialization | Scratch preferred | Same seed/recipe as W-Wiki |
| Checkpoints | ~10%, 30%, 60%, 100% | Same token positions |

The token budget is frozen after the smoke benchmark. Use explicit iterations rather than relying on an evolving upstream default. If the 5090 requires a reduction, reduce both runs equally.

### Conservative 5090 time bounds

For 0.5B tokens, training-only time is approximately:

- 80k tokens/s: ~1.7 hours per run
- 20k tokens/s: ~6.9 hours per run
- 10k tokens/s: ~13.9 hours per run

Plan **8–15 hours per full run until measured otherwise**, including evaluation/checkpoint overhead and leaving room for one failed attempt. Current NanoChat may fall back to SDPA on RTX 5090; if sliding-window attention is inefficient, test full-context `--window-pattern=L` during smoke and use the same choice for both runs.

### No-extra-training ablations

- Evaluate matched checkpoints to produce bpb-vs-token learning curves.
- Evaluate the initialization checkpoint if technically convenient.
- Compare both models on both domains.

These are required because they strengthen empirical rigor without adding full training runs. Depth 12, alternative tokenizers, and extra architectures are cut.

## Resource plan

1. Treat the RTX 5090 as the only guaranteed training device.
2. Complete the paired smoke before spending time on Newton.
3. Use Newton only if access is already working and moving the exact pinned environment is low risk.
4. Keep cloud as an optional rerun contingency with a team-approved cap; do not delay local execution waiting for it.
5. Reserve the 3080 Ti for development and tiny smoke fixtures.

## Project-level forecast

| Scenario | Required runs | Estimated 5090 GPU-hours | Scientific value |
| --- | --- | --- | --- |
| **Preferred** | paired smoke + W/G at 0.5B | ~5–30 plus one retry buffer | Strongest planned comparison |
| **Deadline-safe** | paired smoke + W/G at 0.25–0.3B | ~3–18 plus retry buffer | Controlled and still reportable |
| **Invalid primary design** | W-Wiki 0.5B + undertrained control | Lower | Confounds corpus with training amount |

**Bottom line:** two matched smaller runs are preferable to one larger Wikipedia run against an intentionally weak baseline. GPU time remains manageable; engineering and writing time are the binding constraints.

## Deadline sketch

| Date | Exit criterion |
| --- | --- |
| **Jul 14** | Owners assigned; NanoChat commit, tokenizer, research question, and dataset interface frozen |
| **Jul 15** | Paired end-to-end smoke green with measured 5090 throughput |
| **Jul 16–17** | Wiki/general manifests and both validation sets frozen; final equal budget recorded |
| **Jul 18–20** | W-Wiki and G-General completed, including matched checkpoints |
| **Jul 21** | Experiment freeze; cross-domain metrics and blinded samples complete |
| **Jul 22–24** | Paper, figures, README, and slides |
| **Jul 25** | Soft submission target |
| **Jul 26–27** | Correction-only hard-deadline buffer |

## Decision gates

- **No paired smoke by Jul 15:** reduce integration surface and token budget; do not add evaluations.
- **Measured full-run estimate above 15 hours each:** freeze both runs at 0.25–0.3B tokens.
- **No matched data roots by Jul 17:** explicitly pivot the paper to a Wikipedia learning-curve pilot; do not claim a corpus comparison.
- **No comparable pair by Jul 20:** stop training and write an honest pilot/negative-results report.