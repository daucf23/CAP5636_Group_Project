# Training (Lane B)

Model/config, Stage 1 + Stage 2 training scripts, smoke + full runs, checkpoints, run cards.

Owns: `scripts/lab_gpt/` (model, tokenizer, datasets, decoding, trainer, run cards), `scripts/train_stage1.py`, `scripts/train_stage2.py`, `configs/*.yaml`, everything under `results/<run_id>/`.

Architecture and training loop are a direct port of `CAP5636_W6_Transformer(LLM).ipynb` (Modules 1, 2, 3, 4) into standalone scripts -- see that notebook for the pedagogical walkthrough of each component.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\Activate.ps1
# Install torch first, matched to your GPU/CUDA (see requirements.txt comment), then:
pip install -r requirements.txt
```

## Pipeline runbook

Every command runs from the repo root with `.venv` active. Steps 0-4 are Lane B;
step 5 hands off to [`eval/README.md`](./eval/README.md). Each step lists what to
check before moving on -- the whole B0 -> B1/M2 chain has to be re-run from
scratch if `block_size`, `vocab_size`, or the tokenizer changes.

```bash
# 0. Data (once; ~minutes for smoke, longer for full)
python scripts/download_data.py --smoke-only     # smoke slices only
python scripts/download_data.py                  # full TinyStories + Simple English Wikipedia

# 1. Smoke the entire path first (cheap; catches config/data breakage)
python scripts/train_stage1.py --config configs/b0_smoke.yaml
python scripts/train_stage2.py --config configs/m2_sft.yaml \
  --init-ckpt results/b0_smoke/checkpoint.pt --max-steps 20 --batch-size 1 \
  --eval-every 5 --gen-every 10

# 2. Stage 1 -- B0 pretrain. --retrain-tokenizer is REQUIRED after a smoke run
#    (see the tokenizer warning below), and writes results/b0_full_768/.
python scripts/train_stage1.py --config configs/b0_full.yaml --retrain-tokenizer

# 3. Stage 2 -- both arms from the same B0 checkpoint, matched budgets.
#    configs already point at results/b0_full_768/checkpoint.pt.
python scripts/train_stage2.py --config configs/b1_cpt.yaml
python scripts/train_stage2.py --config configs/m2_sft.yaml

# 4. Confirm the two Stage-2 arms are comparable
grep -i token results/b1_cpt_full_768/RUN_CARD.md results/m2_sft_full_768/RUN_CARD.md

# 5. Hand off to eval (Lane C) -- see eval/README.md for the rest
python eval/build_eval_prompts.py --condition card --out eval/prompts/eval_prompts.jsonl
```

**Check before moving on**

| After | Verify |
| --- | --- |
| Step 0 | `data/raw/tinystories/train.jsonl` and `data/raw/wikipedia/20231101_simple.jsonl` exist (paths must match `configs/*.yaml`) |
| Step 1 | Both smoke runs finish and write a `checkpoint.pt`; M2 smoke prints no `[sft-data] WARNING` |
| Step 2 | Startup log shows `block_size=640`; `results/b0_full_768/RUN_CARD.md` exists |
| Step 3 | M2 log reads `Examples : 866` with **no** `[sft-data] WARNING: ... truncated` line |
| Step 4 | B1 and M2 report the same realized token budget |

> **Tokenizer warning.** `bpe_tokenizer/` is shared by every stage and is
> **reused whenever it already exists**, regardless of the `vocab_size` in your
> config -- and the model takes its vocab from the tokenizer on disk, not from
> the YAML. `configs/b0_smoke.yaml` trains at `vocab_size: 8000` and
> `configs/b0_full.yaml` expects `10000`, so a smoke run leaves a tokenizer that
> the full run would silently adopt. Pass `--retrain-tokenizer` (or delete
> `bpe_tokenizer/`) when starting the real B0. Stage 2 must then reuse that exact
> tokenizer -- ids are baked into the checkpoint's embedding table.

## 0. Data

Stage 1 and Stage 2 need local data from Lane A's pipeline first:

```bash
python scripts/download_data.py --smoke-only   # fast: enough for smoke runs
python scripts/download_data.py                # full TinyStories + Simple English Wikipedia
```

See [`data/README.md`](./data/README.md) and [`data/ENV_SETUP.md`](./data/ENV_SETUP.md).

## 1. Stage 1 -- pretrain from scratch (B0)

```bash
# Smoke: sanity-check the whole pipeline in minutes
python scripts/train_stage1.py --config configs/b0_smoke.yaml

# Full pretrain
python scripts/train_stage1.py --config configs/b0_full.yaml --retrain-tokenizer
```

Trains (or reuses) a Byte-Level BPE tokenizer at `bpe_tokenizer/` (shared by every later stage), then pretrains the GPT. The bare script defaults are lab scale (`n_layer=6, n_embd=256, n_head=8, vocab_size=8000, block_size=256`); the project's real geometry lives in the YAML configs, which override them (`configs/b0_full.yaml`: 10L / 768d / 12H, `vocab_size=10000`, `block_size=640`, ~78M params). See `python scripts/train_stage1.py --help` for every flag.

Pass `--retrain-tokenizer` (or delete `bpe_tokenizer/`) when moving from smoke to full — smoke uses `vocab_size: 8000`, full expects `10000`, and an existing tokenizer is reused silently otherwise (see the tokenizer warning in the runbook above).

Output: `results/<run_id>/` containing `config.yaml`, `metrics.json`, `RUN_CARD.md` (hardware, tokens, wall time), `samples/`, and `checkpoint.pt`. That `checkpoint.pt` is the required `--init-ckpt` for Stage 2.

## 2. Stage 2 -- adaptation from the B0 checkpoint

Two arms, same script, matched Stage-2 token budget (`configs/b1_cpt.yaml` and `configs/m2_sft.yaml` share `batch_size`/`max_steps` on purpose -- **keep them in sync if you edit either**):

```bash
# B1: Wikipedia continued pretraining (required baseline)
python scripts/train_stage2.py --config configs/b1_cpt.yaml

# M2: SFT on fact-card -> story pairs (primary task adaptation)
python scripts/train_stage2.py --config configs/m2_sft.yaml
```

Both Stage-2 configs already set `mode`, `run_id`, and `init_ckpt: results/b0_full_768/checkpoint.pt` (the `run_id` in `configs/b0_full.yaml`). Override with CLI flags only if you change that `run_id` or let Stage 1 auto-name the run (omitting `run_id` produces `b0_full_<timestamp>`).

M2 loads `data/fact_cards/train.jsonl` + `data/sft_pairs/train.jsonl` (approved, `split: train` only -- see `data/SCHEMA.md`), renders each card with the same `render_model_input` function Lane C's eval harness reuses (`scripts/lab_gpt/prompts.py`), and masks the loss over the prompt so only the story tokens are supervised. Lane A has landed 866 approved train cards with a 1:1 gold story each.

**Context length is an M2 constraint, not a Stage-1 preference.** Each SFT example packs the rendered card *plus the whole gold story* into one `block_size` window: measured on the current data that is up to 223 prompt + 254 story = 461 tokens. At `block_size=256` all 866 examples were truncated mid-story, so M2 never saw a story ending or an `<eos>` and never learned to stop. `block_size` is fixed by the learned positional table in the Stage-1 checkpoint and cannot be raised at Stage 2, so `configs/b0_full.yaml` pretrains at 640. Watch the M2 startup log for `[sft-data] WARNING: ... truncated` -- it should not appear.

B1 packs raw Wikipedia text the same way Stage 1 packs TinyStories (no masking -- every token is a training target).

Each run again writes `results/<run_id>/{config.yaml, metrics.json, RUN_CARD.md, samples/, checkpoint.pt}`. `RUN_CARD.md` prints the token budget so mismatched B1/M2 budgets are easy to catch before reporting results.

**What "matched budget" does and does not mean.** `tokens_seen` is
`max_steps * batch_size * block_size` — nominal compute, identical for B1 and M2
by construction (3000 x 8 x 640 = 15.4M). The two arms are *not* matched on
anything else, and the paper should say so rather than imply equal supervision:

| | B1 (CPT) | M2 (SFT) |
| --- | --- | --- |
| Window contents | packed Wikipedia, no padding | one card + story, padded to `block_size` |
| Supervised tokens | every token | story + `<eos>` only (~195 of 640 median) |
| Unique data | ~15.4M of a 40M-token cap, under one epoch | 866 pairs (~308k tokens), ~28 epochs |

So B1 gets ~3x more supervised tokens and sees each one roughly once, while M2
re-reads a small set many times. That is inherent to comparing CPT against SFT
at equal steps — the fix is to report it, not to change the budget.

## Seeds and reproducibility

Both training scripts take `--seed` (default `0`, and set explicitly in every
`configs/*.yaml`), seed CPU and all CUDA devices before the model is built, and
record the seed in `results/<run_id>/config.yaml` and `RUN_CARD.md`. Same seed +
same config + same data therefore gives the same init, the same shuffle order,
and the same training-time sample previews.

Bit-exact loss curves across *different* machines are not guaranteed: cuDNN
kernel selection and GPU reduction order vary by hardware and driver. Treat the
seed as "this run is re-runnable here", not as a cross-machine hash.

## Fixed decoding

`scripts/lab_gpt/generation.py` exposes `FIXED_EVAL_DECODING` (temperature 0.85, top-p 0.9, `max_new_tokens=300`) and `FIXED_EVAL_SEED` (default `0`). Lane C's eval harness imports these rather than redefining decoding, so B0/B1/M2 are compared under identical settings.

`eval/generate_samples.py --seed N` (default `0`) derives a per-`(system, prompt)` sample seed and records both in each JSONL row's `decoding` field. Regenerating without changing `--seed` should reproduce the same stories (same checkpoints + tokenizer).

`max_new_tokens` must clear the gold story length (max 254 tokens for the 120-180 word target) or every system gets cut off before it can emit `<eos>`, which reads as truncation in the ratings. It also has to fit alongside the prompt: `block_size (640) - max_new_tokens (300) = 340` tokens of prompt budget, against a measured max rendered card of 223. `eval/generate_samples.py` enforces that and refuses to generate otherwise.

## Smoke-testing the M2 path early

Per the project's parallel-work plan, M2 training-code work can start on toy pairs during Stage 1, ahead of Lane A's full SFT set:

```bash
python scripts/train_stage2.py --mode sft --init-ckpt results/<b0_smoke_run_id>/checkpoint.pt \
  --fact-cards data/fact_cards/train.jsonl --sft-pairs data/sft_pairs/train.jsonl \
  --max-steps 20 --batch-size 1 --eval-every 5 --gen-every 10
```

## Notes

- `bpe_tokenizer/`, `results/`, and `*.pt` are gitignored -- regenerate locally, don't commit them.
- `--ckpt-every N` saves intermediate checkpoints under `results/<run_id>/checkpoints/step_<N>.pt` for a cheap duration/data ablation later.
- Checkpoints store `config` as a plain dict (not a pickled dataclass) so they load safely under `torch.load(..., weights_only=True)`.
