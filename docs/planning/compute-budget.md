# Compute Budget Model (v1)

Goal: stay **simple and realistic**. Prefer a small NanoChat depth, a Wikipedia **subset**, and matched-budget comparisons — not a full GPT-2-scale speedrun unless we later get multi-GPU budget.

## Decisions locked for now

| Decision | Choice |
| --- | --- |
| Eval complexity | **Simple:** held-out Wikipedia val loss / perplexity (or bits-per-byte) + fixed qualitative prompts |
| Factuality / hallucination benches | **Deferred** (not in v1) |
| Primary dial | NanoChat `--depth` (auto-scales width, tokens, LR, etc.) |

## Rough data math (Wikipedia)

| Quantity | Estimate | Notes |
| --- | --- | --- |
| `20231101.en` raw text | ~11.6 GB | From project brief |
| Characters | ~1.1e10 | Order-of-magnitude |
| Tokens (BPE ~3–4 chars/token) | **~2.5–4B tokens** | Depends on tokenizer; refine after `tok_eval` |
| Tokens needed for NanoChat d12 @ 10.5:1 | **~1B tokens** | Only a **subset** of English Wikipedia |
| Tokens needed for d20 @ ~10.5:1 | **~3B tokens** | Most / nearly all of the dump |

**Implication:** We do **not** need to train on the full 11.6 GB for a first experiment. Subsetting is the main compute lever.

## NanoChat reference points

From NanoChat docs / scaling notes (approximate):

| Depth | ~Params | ~Compute-optimal tokens | Hardware reference |
| --- | --- | --- | --- |
| 4–6 | tens of M | small / override with `--num-iterations` | CPU/MPS smoke tests |
| 12 | ~100M | ~1B | Single strong GPU feasible if we cut batch size |
| 20 | ~300M | ~3B | Multi-GPU preferred |
| 26 (speedrun) | GPT-2-ish | large | **~2.5–3h on 8×H100**, ~$50–70 on-demand / less on spot |

Training FLOPs (order of magnitude):

\[
\text{FLOPs} \approx C \times N \times D
\]

where \(N\) = parameters, \(D\) = training tokens, and \(C \approx 6\)–\(20\) depending on how carefully you count (NanoChat scaling notes use ~20 for full train cost).

Example: d12, \(N \approx 1\times10^8\), \(D \approx 1\times10^9\), \(C=6\) → **~6×10¹⁷ FLOPs**.

## Proposed experiment tiers

### Tier 0 — Pipeline smoke test (required first)

- Depth **4–6**, tiny `--num-iterations`, small seq len / batch
- Tiny Wikipedia shard (e.g. tens of MB)
- Purpose: prove download → preprocess → train → val loss → sample generations
- Hardware: laptop GPU / Colab free / CPU overnight
- Wall time: minutes to a few hours

### Tier 1 — Course-realistic main result (**recommended default**)

- Depth **8–12**
- Wikipedia **subset sized to the NanoChat token target** (or a fixed smaller budget, e.g. 100M–500M tokens if hardware is tight)
- Baseline: same architecture + **same token budget** on non-Wikipedia text **or** shorter/random-init control (pick one; see open questions)
- Eval: val bpb/perplexity on held-out Wikipedia articles + fixed prompt sheet
- Hardware target: **1× consumer GPU (24GB)** or **1× A100/L4** via Colab/Uni cloud
- Expectation: hours to ~1–2 days depending on GPU and whether we under-train vs full 10.5:1

### Tier 2 — Stretch (only if compute appears)

- Depth **12–16**, closer to full compute-optimal tokens on Wikipedia subset
- Optional ablation: 100M / 300M / 1B tokens at fixed depth
- Hardware: A100/H100 single or small multi-GPU
- Cost: can climb into tens of dollars of cloud time quickly

### Tier 3 — Out of scope for v1 unless funded

- Full NanoChat d26 8×H100 speedrun (~$50–70 on-demand)
- Full 11.6 GB multi-epoch training at large depth

## Matched-budget rule (important)

For any Wikipedia vs baseline comparison, match:

1. **Model depth / architecture**
2. **Training tokens** (or FLOPs)
3. **Tokenizer** (same vocab)
4. **Eval set** (same held-out Wikipedia articles)

Otherwise “Wikipedia helps” is confounded with “trained longer / more data.”

## Cost sketch (illustrative, not a quote)

| Setup | What it buys | Ballpark |
| --- | --- | --- |
| Free Colab / campus GPU | Tier 0 + maybe small Tier 1 | $0 |
| 1× RTX 4090 / 3090 local | Tier 1 under-trained or full d8–d12 subset | electricity only |
| 1× A100 cloud (~$1–2/hr) | Tier 1 more comfortably | ~$5–40 depending on length |
| 8×H100 node | Tier 3 NanoChat speedrun scale | ~$50–70 / run on-demand |

Refine after we know actual `tok/s` on our hardware (NanoChat logs `train/tok_per_sec`).

## Practical v1 recommendation

1. Build Tier 0 end-to-end on a tiny shard.
2. Run **one** Tier 1 Wikipedia run at depth **8 or 12** with a capped token budget we can afford twice (model + baseline).
3. Skip dedicated hallucination metrics until those two runs exist.
4. Only then consider data-size ablations.

## Still needed from the team

- What GPUs / cloud credits / campus machines we actually have
- Soft dollar cap (e.g. $0 / $20 / $100)
- Whether baseline is “general text, matched tokens” or “untuned / short-train control”
